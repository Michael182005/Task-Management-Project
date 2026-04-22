from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = Field(default="Task Management API")
    api_v1_prefix: str = Field(default="/api")
    database_url: str = Field(...)
    secret_key: SecretStr = Field(...)
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=60, ge=1)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
