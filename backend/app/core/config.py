from functools import lru_cache
from pathlib import Path
from decimal import Decimal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    postgres_db: str = "pokemon13"
    postgres_user: str = "pokemon13_local"
    postgres_password: SecretStr | None = None
    database_host: str = "127.0.0.1"
    database_port: int = 5432
    auth_secret_key: SecretStr | None = None
    access_token_expire_minutes: int = Field(default=30, gt=0, le=10080)
    battle_engine_url: str = "http://127.0.0.1:3001"
    battle_engine_timeout_seconds: float = Field(default=15, gt=0, le=120)
    draft_tier_1_percent: Decimal | None = None
    draft_tier_2_percent: Decimal | None = None
    draft_tier_3_percent: Decimal | None = None
    draft_tier_4_percent: Decimal | None = None
    draft_tier_5_percent: Decimal | None = None

    @property
    def database_url(self) -> URL:
        password = (
            self.postgres_password.get_secret_value()
            if self.postgres_password is not None
            else None
        )
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.postgres_user,
            password=password,
            host=self.database_host,
            port=self.database_port,
            database=self.postgres_db,
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
