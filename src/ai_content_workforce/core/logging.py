"""Allowlisted JSON logging that avoids request bodies, query strings, and secrets."""

import json
import logging
from datetime import UTC, datetime


class JsonFormatter(logging.Formatter):
    """Serialize a small, explicit set of safe log fields."""

    def format(self, record: logging.LogRecord) -> str:
        event = getattr(record, "event", "application_event")
        if event not in {"http_request_completed", "unhandled_application_error"}:
            event = "application_event"
        payload: dict[str, object] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname.lower(),
            "logger": record.name,
            "event": event,
        }
        for field in ("request_id", "method", "status_code"):
            value = getattr(record, field, None)
            if value is not None:
                payload[field] = value
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_logging(level: str) -> None:
    """Configure the application logger with an allowlisted formatter."""

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    app_logger = logging.getLogger("ai_content_workforce")
    app_logger.handlers.clear()
    app_logger.addHandler(handler)
    app_logger.setLevel(level)
    app_logger.propagate = False
