FROM python:3.12

WORKDIR /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-ansi --no-root --only main

COPY . .

EXPOSE 8000
