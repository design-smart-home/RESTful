from pydantic_settings import BaseSettings
from pydantic import Field, PostgresDsn
from pathlib import Path


class Settings(BaseSettings):
    SECRET_KEY: str = Field(description="Секретный ключ для JWT")
    ALGORITHM: str = Field(description="Алгоритм шифрования JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(description="Время жизни токена в минутах")
    POSTGRES_USER: str = Field(description="Пользователь БД")
    POSTGRES_PASSWORD: str = Field(description="Пароль БД")
    POSTGRES_DB: str = Field(description="Название БД")
    POSTGRES_USER_TEST: str = Field(description="Пользователь тестовой БД")
    POSTGRES_PASSWORD_TEST: str = Field(description="Пароль тестовой БД")
    POSTGRES_DB_TEST: str = Field(description="Название тестовой БД")
    DB_URL: PostgresDsn = Field(description="URL БД")

    class Config:
        env_file = Path(__file__).resolve().parents[2] / ".env"
        env_file_encoding = "utf-8"


settings = Settings()
