"""Custom exceptions and exception handlers."""
from datetime import datetime, timezone

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils.responses import APIErrorDetail, APIErrorResponse


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str | None = None,
        details: list[APIErrorDetail] | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or "APP_ERROR"
        self.details = details or []
        super().__init__(message)


class NotFoundError(AppException):
    """Resource not found."""

    def __init__(self, message: str = "Resource not found", resource: str | None = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            details=[APIErrorDetail(field=resource, message=message)] if resource else None,
        )


class ConflictError(AppException):
    """Duplicate or conflict (e.g. duplicate employee ID/email)."""

    def __init__(self, message: str = "Resource already exists", field: str | None = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT",
            details=[APIErrorDetail(field=field, message=message)] if field else None,
        )


class UnauthorizedError(AppException):
    """Authentication required or invalid token."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
        )


class ForbiddenError(AppException):
    """Insufficient permissions."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
        )


def _error_response(
    message: str,
    status_code: int,
    error_code: str | None = None,
    details: list[APIErrorDetail] | None = None,
) -> JSONResponse:
    body = APIErrorResponse(
        success=False,
        message=message,
        error_code=error_code,
        details=details,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    return JSONResponse(
        status_code=status_code,
        content=body.model_dump(exclude_none=True),
    )


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle AppException."""
    return _error_response(
        message=exc.message,
        status_code=exc.status_code,
        error_code=exc.error_code,
        details=exc.details,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    details = [
        APIErrorDetail(
            field=".".join(str(loc) for loc in err.get("loc", []) if loc != "body"),
            message=err.get("msg", "Validation error"),
        )
        for err in exc.errors()
    ]
    return _error_response(
        message="Validation error",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        error_code="VALIDATION_ERROR",
        details=details,
    )
