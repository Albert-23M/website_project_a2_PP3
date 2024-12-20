""" Login related routes """
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core import security
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import Message, NewPassword, Token, UserOut
from app.utils import (
    generate_password_reset_token,
    generate_reset_password_email,
    send_email,
    verify_password_reset_token,
)
import mysql.connector
import bcrypt

router = APIRouter()
host = settings.HOST
user = settings.USERDB
password = settings.PASSWORD
database = settings.DATABASE


@router.post("/login", response_model=UserOut)
def login_user(*, email: str, pswd_input: str) -> Any:
    """
    Login a user by email and password.
    """
    try:
        # Conexión a la base de datos
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

            # Consulta para obtener el hash de la contraseña del usuario por email
            query_user = "SELECT id_user, name, surname, username, email, password FROM users WHERE email = %s"
            cursor.execute(query_user, (email,))
            user_row = cursor.fetchone()

            if not user_row:
                raise HTTPException(
                    status_code=404,
                    detail="User not found with the provided email",
                )

            # Extraer el hash almacenado y verificar la contraseña ingresada
            stored_hashed_password = user_row[5].encode('utf-8')

            # Verificar la contraseña ingresada contra el hash almacenado
            if not bcrypt.checkpw(pswd_input.encode('utf-8'), stored_hashed_password):
                raise HTTPException(
                    status_code=400,
                    detail="Incorrect password.",
                )

            # Crear el objeto UserOut basado en los datos obtenidos si la contraseña es correcta
            user_out = UserOut(
                id_user=user_row[0],  # id_user
                name=user_row[1],  # name
                surname=user_row[2],  # surname
                username=user_row[3],  # username
                email=user_row[4]  # email
            )

            print("Inicio de sesión exitoso")
            return user_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")
    except Exception as ex:
        print(f"Error al verificar el usuario: {ex}")
        raise HTTPException(status_code=400, detail=str(ex))

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")


@router.post("/login/access-token")
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return Token(
        access_token=security.create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )


@router.post("/login/test-token", response_model=UserOut)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}")
def recover_password(email: str, session: SessionDep) -> Message:
    """
    Password Recovery
    """
    user = crud.user.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Password recovery email sent")


@router.post("/reset-password/")
def reset_password(session: SessionDep, body: NewPassword) -> Message:
    """
    Reset password
    """
    email = verify_password_reset_token(token=body.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = get_password_hash(password=body.new_password)
    user.hashed_password = hashed_password
    session.add(user)
    session.commit()
    return Message(message="Password updated successfully")


@router.post(
    "/password-recovery-html-content/{email}",
    dependencies=[Depends(get_current_active_superuser)],
    response_class=HTMLResponse,
)
def recover_password_html_content(email: str, session: SessionDep) -> Any:
    """
    HTML Content for Password Recovery
    """
    user = crud.user.get_user_by_email(session=session, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )

    return HTMLResponse(
        content=email_data.html_content, headers={"subject:": email_data.subject}
    )
