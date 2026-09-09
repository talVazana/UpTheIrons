from typing import Any, Dict, Optional
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse
import logging

logger = logging.getLogger("blacksmith_knight")


class AppException(Exception):
    """Base application exception for consistent API error responses."""

    def __init__(
        self,
        message: str,
        code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Any] = None,
    ):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details


class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found", details: Optional[Any] = None):
        super().__init__(message=message, code="NOT_FOUND", status_code=404, details=details)


class BadRequestError(AppException):
    def __init__(self, message: str = "Invalid request", details: Optional[Any] = None):
        super().__init__(message=message, code="BAD_REQUEST", status_code=400, details=details)


class ValidationError(AppException):
    def __init__(self, message: str = "Validation failed", details: Optional[Any] = None):
        super().__init__(message=message, code="VALIDATION_ERROR", status_code=422, details=details)


class SourceError(AppException):
    def __init__(self, message: str = "External source failure", details: Optional[Any] = None):
        super().__init__(message=message, code="SOURCE_ERROR", status_code=502, details=details)


def format_error_response(code: str, message: str, details: Optional[Any] = None) -> Dict[str, Any]:
    return {
        "error": {
            "code": code,
            "message": message,
            "details": details,
        }
    }


def register_error_handlers(app: FastAPI) -> None:
    """Registers global exception handlers on the FastAPI application."""

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(
            f"AppException: {exc.code} - {exc.message} on {request.method} {request.url.path}"
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=format_error_response(
                code=exc.code,
                message=exc.message,
                details=exc.details,
            ),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.info(f"Validation error on {request.method} {request.url.path}: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content=format_error_response(
                code="VALIDATION_ERROR",
                message="Request validation failed",
                details=exc.errors(),
            ),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        code = "HTTP_ERROR"
        if exc.status_code == 404:
            code = "NOT_FOUND"
        elif exc.status_code == 400:
            code = "BAD_REQUEST"
        elif exc.status_code == 403:
            code = "FORBIDDEN"
        elif exc.status_code == 401:
            code = "UNAUTHORIZED"

        return JSONResponse(
            status_code=exc.status_code,
            content=format_error_response(
                code=code,
                message=str(exc.detail) if exc.detail else "An HTTP error occurred",
                details=None,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception(f"Unhandled server error on {request.method} {request.url.path}: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content=format_error_response(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected internal server error occurred.",
                details=None,
            ),
        )
