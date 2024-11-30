FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Instalar mysql-connector-python directamente si no está en el requirements.txt
RUN pip install mysql-connector-python==9.1.0

COPY ./app /app/app/

EXPOSE 80
# COPY ./alembic.ini /app/
# COPY ./alembic /app/alembic
# COPY ./prestart.sh /app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
