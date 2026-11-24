"""API integration tests use in-process ASGI requests and no external services."""

import asyncio
import uuid

from httpx import ASGITransport, AsyncClient

from ai_content_workforce.core.config import Settings
from ai_content_workforce.main import create_app


def request(
    app: object, path: str, method: str = "GET", **kwargs: object
) -> tuple[int, dict[str, object], dict[str, str], str]:
    async def send() -> tuple[int, dict[str, object], dict[str, str], str]:
        transport = ASGITransport(app=app, raise_app_exceptions=False)  # type: ignore[arg-type]
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            response = await client.request(method, path, **kwargs)  # type: ignore[arg-type]
            return response.status_code, response.json(), dict(response.headers), response.text

    return asyncio.run(send())


def test_health_reports_application_version_and_unconfigured_database() -> None:
    status_code, body, headers, _ = request(
        create_app(Settings(app_env="test", _env_file=None)), "/health"
    )

    assert status_code == 200
    assert uuid.UUID(headers["x-request-id"]).version == 4
    assert body == {
        "schema_version": "1.0",
        "status": "ok",
        "application": {
            "name": "ai-content-workforce",
            "version": "1.0.0",
            "environment": "test",
        },
        "database": {"status": "not_configured"},
    }


def test_versioned_health_matches_liveness_contract() -> None:
    status_code, body, _, _ = request(
        create_app(Settings(app_env="test", _env_file=None)), "/api/v1/health"
    )

    assert status_code == 200
    assert body["database"]["status"] == "not_configured"


def test_api_root_reports_major_and_schema_versions() -> None:
    status_code, body, _, _ = request(
        create_app(Settings(app_env="test", _env_file=None)), "/api/v1/"
    )

    assert status_code == 200
    assert body == {
        "api_version": "v1",
        "schema_version": "1.0",
        "application_version": "1.0.0",
    }


def test_not_found_uses_uniform_safe_error_body() -> None:
    status_code, body, _, _ = request(
        create_app(Settings(app_env="test", _env_file=None)), "/not-a-real-route"
    )

    assert status_code == 404
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["schema_version"] == "1.0"


def test_validation_error_does_not_echo_invalid_input() -> None:
    application = create_app(Settings(app_env="test", _env_file=None))

    def validated_route(quantity: int) -> dict[str, int]:
        return {"quantity": quantity}

    application.add_api_route("/__test/validated", validated_route, methods=["GET"])

    status_code, body, _, text = request(
        application, "/__test/validated", params={"quantity": "sensitive-value"}
    )

    assert status_code == 422
    assert body["error"]["code"] == "REQUEST_VALIDATION_FAILED"
    assert "sensitive-value" not in text


def test_unexpected_exception_does_not_log_exception_text(capsys: object) -> None:
    application = create_app(Settings(app_env="test", _env_file=None))

    def failing_route() -> None:
        raise RuntimeError("secret-value-must-not-be-logged")

    application.add_api_route("/__test/failure", failing_route, methods=["GET"])
    status_code, _, _, text = request(application, "/__test/failure")
    captured = capsys.readouterr()  # type: ignore[attr-defined]

    assert status_code == 500
    assert "secret-value-must-not-be-logged" not in captured.err
    assert "secret-value-must-not-be-logged" not in text
