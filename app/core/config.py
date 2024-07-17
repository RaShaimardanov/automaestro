from functools import lru_cache
from typing import Optional, List, Set

from pydantic import field_validator, Field
from pydantic_core.core_schema import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class TelegramBotSettings(BaseConfig):
    BOT_TOKEN: str
    BOT_PARSE_MODE: str
    BOT_PROTECT_CONTENT: bool
    BOT_DROP_PENDING_UPDATES: bool
    BOT_USERNAME: str

    WEBHOOK_URL: str
    WEBHOOK_PATH: str
    WEBHOOK_SECRET: str


class PostgresDBSettings(BaseConfig):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_ECHO: bool = False

    POSTGRES_URI: Optional[str] = None

    @field_validator("POSTGRES_URI")
    def assemble_db_connection(
        cls, v: Optional[str], values: ValidationInfo
    ) -> str:
        if isinstance(v, str):
            return v
        # Return URL-connect 'postgresql://postgres:password@localhost:5432/invoices'
        return (
            "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
                user=values.data["POSTGRES_USER"],
                password=values.data["POSTGRES_PASSWORD"],
                host=values.data["POSTGRES_HOST"],
                port=values.data["POSTGRES_PORT"],
                db=values.data["POSTGRES_DB"],
            )
        )


class ServerSettings(BaseConfig):
    SERVER_HOST: str
    SERVER_PORT: int
    SERVER_RELOAD: bool = True


class RedisSettings(BaseConfig):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL: Optional[str] = None

    @field_validator("REDIS_URL")
    def get_redis_url(cls, v: Optional[str], values: ValidationInfo) -> str:

        return "redis://{host}:{port}".format(
            host=values.data["REDIS_HOST"],
            port=values.data["REDIS_PORT"],
        )


class AppSettings(BaseConfig):
    PROJECT_NAME: str
    WEB_APP_URL: str
    API_PREFIX: str
    TESTING: bool = True
    DEBUG: str
    ADMINS_IDS: list[int]

    TELEGRAM: TelegramBotSettings = Field(default_factory=TelegramBotSettings)
    POSTGRES: PostgresDBSettings = Field(default_factory=PostgresDBSettings)
    SERVER: ServerSettings = Field(default_factory=ServerSettings)
    REDIS: RedisSettings = Field(default_factory=RedisSettings)


@lru_cache()
def get_settings():
    return AppSettings()


settings = get_settings()
