FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    libsodium23 \
    wget \
    build-essential \
    libffi-dev \
    curl

WORKDIR /app

ENV PIP_NO_CACHE_DIR=false \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=10 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/home/user/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

ENV VENV_PATH="/app/.venv"
ENV PATH="${POETRY_HOME}/bin:${VENV_PATH}/bin:${PATH}"
ENV PYTHONPATH="${PYTHONPATH}:/app"

RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY app/ /app/app/
COPY tests/ /app/tests/
