"""FastAPI application factory and safe error handling."""

import logging
from collections.abc import Mapping
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from ai_content_workforce.api.v1.health import health
from ai_content_workforce.api.v1.health import router as v1_router
from ai_content_workforce.core.config import Settings, get_settings
from ai_content_workforce.core.logging import configure_logging

logger = logging.getLogger("ai_content_workforce")


def _error_response(*, status_code: int, code: str, message: str, request_id: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "schema_version": "1.0",
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id,
            },
        },
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create the application with validated settings and no external connections."""

    if settings is None:
        settings = get_settings()
    configure_logging(settings.log_level)

    application = FastAPI(
        title="AI Content Workforce API",
        version="1.0.0",
        description="Phase 1 engineering foundation; no business APIs are enabled.",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url=None,
    )
    application.state.settings = settings

    @application.middleware("http")
    async def request_context(request: Request, call_next: Any) -> Any:
        request_id = str(uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["Cache-Control"] = "no-store"
        logger.info(
            "http_request_completed",
            extra={
                "event": "http_request_completed",
                "request_id": request_id,
                "method": request.method,
                "status_code": response.status_code,
            },
        )
        return response

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        del exc
        return _error_response(
            status_code=422,
            code="REQUEST_VALIDATION_FAILED",
            message="Request parameters did not pass validation.",
            request_id=getattr(request.state, "request_id", str(uuid4())),
        )

    @application.exception_handler(StarletteHTTPException)
    async def http_error_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        code = "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR"
        message = (
            "The requested resource was not found."
            if exc.status_code == 404
            else ("The request could not be completed.")
        )
        headers: Mapping[str, str] = exc.headers or {}
        response = _error_response(
            status_code=exc.status_code,
            code=code,
            message=message,
            request_id=getattr(request.state, "request_id", str(uuid4())),
        )
        for name, value in headers.items():
            response.headers[name] = value
        return response

    @application.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, exc: Exception) -> JSONResponse:
        del exc
        request_id = getattr(request.state, "request_id", str(uuid4()))
        logger.error(
            "unhandled_application_error",
            extra={"event": "unhandled_application_error", "request_id": request_id},
        )
        return _error_response(
            status_code=500,
            code="INTERNAL_ERROR",
            message="An unexpected error occurred.",
            request_id=request_id,
        )

    application.include_router(v1_router, prefix="/api/v1")
    application.add_api_route("/health", health, methods=["GET"])
    return application


app = create_app()
