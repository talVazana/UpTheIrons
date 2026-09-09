import json
import logging
import sys
import time
from typing import Any, Dict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class StructuredFormatter(logging.Formatter):
    """Formats log records as structured JSON text for observability."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_fields") and isinstance(record.extra_fields, dict):
            log_entry.update(record.extra_fields)
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logging(log_level: str = "INFO", json_format: bool = True) -> logging.Logger:
    """Configures application logger with structured output."""
    logger = logging.getLogger("blacksmith_knight")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        if json_format:
            handler.setFormatter(StructuredFormatter())
        else:
            handler.setFormatter(
                logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s")
            )
        logger.addHandler(handler)
        logger.propagate = False

    return logger


logger = setup_logging()


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Starlette middleware to log HTTP requests and measure duration."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        record_extra = {
            "http_method": request.method,
            "http_path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": process_time_ms,
        }
        log_msg = f"{request.method} {request.url.path} -> {response.status_code} ({process_time_ms}ms)"

        log_record = logging.LogRecord(
            name="blacksmith_knight.access",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=log_msg,
            args=(),
            exc_info=None,
        )
        log_record.extra_fields = record_extra
        logging.getLogger("blacksmith_knight").handle(log_record)

        response.headers["X-Process-Time-Ms"] = str(process_time_ms)
        return response
