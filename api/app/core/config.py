from functools import lru_cache
from typing import Literal

from pydantic import BaseModel, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str
    port: int = 5432
    name: str
    user: str
    password: SecretStr

    @computed_field
    @property
    def url(self) -> str:
        return (
            f"postgresql+psycopg_async://"
            f"{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.name}"
        )

    @computed_field
    @property
    def sync_url(self) -> str:
        return self.url.replace(
            "+psycopg_async",
            "+psycopg",
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        extra="ignore",
    )

    app_name: str = "Booking API"

    db_echo: bool = False
    app_env: Literal[
        "development",
        "testing",
        "production",
    ]

    @property
    def docs_enabled(self) -> bool:
        return self.app_env != "production"

    db: DatabaseSettings


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
