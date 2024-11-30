""" User management routes """
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.models import (
    Message,
    UpdatePassword,
    User,
    UserCreate,
    UserCreateOpen,
    UserOut,
    UserBase,
    UsersOut,
    UserUpdate,
    UserUpdateMe,
)
from app.utils import generate_new_account_email, send_email
#!pip install mysql-connector-python
import mysql.connector
import bcrypt
#
router = APIRouter()

host = settings.HOST
user = settings.USERDB
password = settings.PASSWORD
database = settings.DATABASE

@router.get("/{keyword}", response_model=UsersOut)
def read_top5_matched_users(keyword: str) -> Any:
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

            # Crear la consulta de búsqueda
            query = """
                SELECT id_user, name, surname, username, email
                   FROM users
                   WHERE name LIKE %s OR surname LIKE %s or username LIKE %s
                   LIMIT 5;
            """

            # Preparar el parámetro de búsqueda con el carácter comodín
            search_param = f"%{keyword}%"

            # Ejecutar la consulta
            cursor.execute(query, (search_param, search_param, search_param))

            # Obtener los resultados
            resultados = cursor.fetchall()

            # Contar el total de libros
            query_count = "SELECT COUNT(1) FROM Books"
            cursor.execute(query_count)
            count = cursor.fetchone()[0]

            users_data = [
                UserOut(
                    id_user=row[0],
                    name=row[1],
                    surname=row[2],
                    username=row[3],
                    email=row[4]
                ) for row in resultados
            ]

            return UsersOut(data=users_data, count=count)
    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")

@router.get("/by-id/{user_id}", response_model=UserOut)
def read_user(user_id: int) -> Any:
    """
    Retrieve a specific user by its ID.
    """
    try:
        conexion = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=3306
        )
        print("Conexión a la base de datos iniciada")

        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            cursor = conexion.cursor()

            query_user = """
                SELECT id_user, name, surname, username, email 
                FROM users 
                WHERE id_user = %s
            """
            cursor.execute(query_user, (user_id,))
            row = cursor.fetchone()

            if row is None:
                raise HTTPException(
                    status_code=404,
                    detail="User not found with the provided id"
                )

            user_out = UserOut(
                id_user=row[0],
                name=row[1],
                surname=row[2],
                username=row[3],
                email=row[4],
            )
            return user_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")

@router.get("/")
def read_users(skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    try:
        print("print-", user)
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

            # Update query to fetch users
            query_users = "SELECT id_user, name, surname, username, email FROM users LIMIT %s OFFSET %s"
            cursor.execute(query_users, (limit, skip))
            filas = cursor.fetchall()

            # Count the total number of users
            query_count = "SELECT COUNT(1) FROM users"
            cursor.execute(query_count)
            count = cursor.fetchone()[0]

            # Transform tuples to a list of UserOut
            users_data = [
                UserOut(
                    id_user=row[0],
                    name=row[1],
                    surname=row[2],
                    username=row[3],
                    email=row[4]
                ) for row in filas
            ]

            return UsersOut(data=users_data, count=count)

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")


@router.post(
    "/",
    response_model=UserOut
)
def create_user(*, session: SessionDep, user_in: UserCreate) -> Any:
    """
    Create new user.
    """
    try:
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

            # Verificar si el usuario ya existe por email
            query_check_user = "SELECT id_user FROM users WHERE email = %s"
            cursor.execute(query_check_user, (user_in.email,))
            existing_user = cursor.fetchone()

            if existing_user:
                print("El usuario ya existe")
                raise HTTPException(
                    status_code=400,
                    detail="The user with this email already exists in the system.",
                )

            # Insertar el nuevo usuario en la base de datos
            query_create_user = """
                INSERT INTO users (name, surname, username, email, password)
                VALUES (%s, %s, %s, %s, %s)
            """
            hashed_password = bcrypt.hashpw(user_in.password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute(query_create_user, (
                user_in.name,
                user_in.surname,
                user_in.username,
                user_in.email,
                hashed_password
            ))

            # Confirmar la transacción
            conexion.commit()

            # Obtener el ID del usuario recién creado
            new_user_id = cursor.lastrowid

            # Crear el objeto de salida
            user_out = UserOut(
                id_user=new_user_id,
                name=user_in.name,
                surname=user_in.surname,
                username=user_in.username,
                email=user_in.email
            )
            '''
            # Enviar correo si está habilitado
            if settings.emails_enabled and user_in.email:
                email_data = generate_new_account_email(
                    email_to=user_in.email, username=user_in.email, password=user_in.password
                )
                send_email(
                    email_to=user_in.email,
                    subject=email_data.subject,
                    html_content=email_data.html_content,
                )
            '''
            return user_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")

@router.post("/open", response_model=UserOut)
def create_user_open(session: SessionDep, user_in: UserCreateOpen) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.user.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user_create = UserCreate.from_orm(user_in)
    user = crud.user.create_user(session=session, user_create=user_create)
    return user

@router.get("/by-email", response_model=UserOut)
def read_user_by_email(*, email: str) -> Any:
    """
    Get a user by email.
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

            # Consulta para obtener el usuario por email
            query_user = "SELECT id_user, name, surname, username, email, password FROM users WHERE email = %s"
            cursor.execute(query_user, (email,))
            user_row = cursor.fetchone()

            if not user_row:
                raise HTTPException(
                    status_code=404,
                    detail="User not found with the provided email",
                )

            # Crear el objeto UserOut basado en los datos obtenidos
            user_out = UserOut(
                id_user=user_row[0],
                name=user_row[1],
                surname=user_row[2],
                username=user_row[3],
                email=user_row[4],
            )

            return user_out

    except mysql.connector.Error as e:
        print(f"Error al conectar a MySQL: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to the database.")
    except Exception as ex:
        print(f"Error al obtener el usuario: {ex}")
        raise HTTPException(status_code=400, detail=str(ex))

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print("Conexión cerrada")