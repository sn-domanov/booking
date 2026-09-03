from datetime import timedelta
from functools import lru_cache
from pathlib import Path
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


class LocalObjectStorageSettings(BaseModel):
    base_dir: Path = Path(__file__).resolve().parents[2]
    root: Path = base_dir / "media"
    base_url: str = "/media"


class S3Settings(BaseModel):
    access_key: str
    secret_key: SecretStr

    endpoint_url: str | None = None
    public_base_url: str
    region: str
    bucket: str


class JwtSettings(BaseModel):
    secret_key: SecretStr
    algorithm: str = "HS256"

    access_token_ttl: timedelta
    refresh_token_ttl: timedelta

    access_token_cookie_name: str = "access_token"
    refresh_token_cookie_name: str = "refresh_token"

    cookie_secure: bool = True
    cookie_samesite: Literal["lax", "strict", "none"] | None = "lax"



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
    s3: S3Settings
    local_storage: LocalObjectStorageSettings = LocalObjectStorageSettings()
    jwt: JwtSettings

    # Limits
    max_upload_size_bytes: int = 10 * 1024 * 1024  # 10MB
    max_image_dimension: int = 10_000
    max_image_pixels: int = 20_000_000

    # SPA
    cors_origins: list[str]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]
