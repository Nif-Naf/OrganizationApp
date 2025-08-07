# syntax=docker/dockerfile:1.4

FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-root --only main

COPY . .

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 ENV=dev

EXPOSE 8000

ENTRYPOINT ["sh", "-c", "alembic upgrade head && python -m app.main"]