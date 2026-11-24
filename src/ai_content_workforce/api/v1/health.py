"""Application liveness and API version health endpoints."""

from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel

from ai_content_workforce import __version__
from ai_content_workforce.core.config import Settings

router = APIRouter()


class ApplicationHealth(BaseModel):
    name: Literal["ai-content-workforce"]
    version: str
    environment: Literal["development", "test", "production"]


class DatabaseStatus(BaseModel):
    status: Literal["not_configured"]


class HealthResponse(BaseModel):
    schema_version: Literal["1.0"]
    status: Literal["ok"]
    application: ApplicationHealth
    database: DatabaseStatus


class APIVersionInfo(BaseModel):
    api_version: Literal["v1"]
    schema_version: Literal["1.0"]
    application_version: str


@router.get("/health", name="health")
async def health(request: Request) -> HealthResponse:
    """Report application liveness without implying database availability."""

    settings: Settings = request.app.state.settings
    return HealthResponse(
        schema_version="1.0",
        status="ok",
        application=ApplicationHealth(
            name="ai-content-workforce",
            version=__version__,
            environment=settings.app_env,
        ),
        database=DatabaseStatus(status="not_configured"),
    )


@router.get("/", name="api_version_info")
async def api_version_info() -> APIVersionInfo:
    """Expose the API major version and response schema version."""

    return APIVersionInfo(
        api_version="v1",
        schema_version="1.0",
        application_version=__version__,
    )
