from typing import Optional

from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramBotSettings(BaseSettings):
    BOT_TOKEN: str
    BOT_PARSE_MODE: str
    BOT_PROTECT_CONTENT: bool
    BOT_DROP_PENDING_UPDATES: bool

    WEBHOOK_URL: str
    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str


class PostgresDBSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_ECHO: bool = False

    POSTGRES_URI: Optional[str] = None

    @field_validator("POSTGRES_URI")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> str:
        if isinstance(v, str):
            return v
        # Return URL-connect 'postgresql://postgres:password@localhost:5432/invoices'
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            user=values.data["POSTGRES_USER"],
            password=values.data["POSTGRES_PASSWORD"],
            host=values.data["POSTGRES_HOST"],
            port=values.data["POSTGRES_PORT"],
            db=values.data["POSTGRES_DB"],
        )


class ServerSettings(BaseSettings):
    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_RELOAD: bool = True


settings = [TelegramBotSettings, ServerSettings, PostgresDBSettings]


class AppSettings(*settings):
    PROJECT_NAME: str
    API_PREFIX: str
    DEBUG: str

    model_config = SettingsConfigDict(env_file=".env")


settings = AppSettings()
