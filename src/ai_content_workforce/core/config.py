"""Validated application settings loaded from environment or the project .env file."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Settings safe for local startup; database integration is deliberately absent."""

    app_env: Literal["development", "test", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings, hiding raw Pydantic input values on configuration errors."""

    try:
        return Settings()
    except ValidationError as exc:
        fields = sorted(
            {".".join(str(part).upper() for part in error["loc"]) for error in exc.errors()}
        )
        field_list = ", ".join(fields)
        raise RuntimeError(
            f"Invalid application configuration for: {field_list}. "
            "Check .env.example for allowed values."
        ) from None
