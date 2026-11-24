"""Unit tests for validated application settings."""

import pytest
from pydantic import ValidationError

from ai_content_workforce.core.config import Settings


def test_settings_defaults_are_local_and_database_free() -> None:
    settings = Settings(_env_file=None)

    assert settings.app_env == "development"
    assert settings.log_level == "INFO"
    assert not hasattr(settings, "database_url")


def test_environment_variables_are_loaded(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "WARNING")

    settings = Settings(_env_file=None)

    assert settings.app_env == "test"
    assert settings.log_level == "WARNING"


def test_invalid_environment_is_rejected_without_echoing_input() -> None:
    secret_like_value = "not-a-valid-environment-value"

    with pytest.raises(ValidationError) as error:
        Settings(app_env=secret_like_value, _env_file=None)  # type: ignore[arg-type]

    assert "app_env" in str(error.value)


def test_startup_configuration_error_does_not_echo_value(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from ai_content_workforce.core.config import get_settings

    marker = "secret-like-invalid-setting"
    monkeypatch.setenv("APP_ENV", marker)
    get_settings.cache_clear()
    try:
        with pytest.raises(RuntimeError) as error:
            get_settings()
    finally:
        get_settings.cache_clear()

    assert "APP_ENV" in str(error.value)
    assert marker not in str(error.value)
