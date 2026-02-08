"""Generic API response, error response, and pagination models."""
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Generic success API response wrapper."""

    success: bool = True
    message: str = "Success"
    data: T | None = None

    class Config:
        from_attributes = True


class APIErrorDetail(BaseModel):
    """Single error detail (e.g. field validation)."""

    field: str | None = None
    message: str
    code: str | None = None


class APIErrorResponse(BaseModel):
    """Generic error API response."""

    success: bool = False
    message: str = "An error occurred"
    error_code: str | None = None
    details: list[APIErrorDetail] | None = None
    timestamp: str | None = None

    class Config:
        from_attributes = True


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    page: int = Field(ge=1, description="Current page")
    per_page: int = Field(ge=1, le=100, description="Items per page")
    total: int = Field(ge=0, description="Total items")
    total_pages: int = Field(ge=0, description="Total pages")
    has_next: bool = False
    has_prev: bool = False


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""

    success: bool = True
    message: str = "Success"
    data: list[T] = Field(default_factory=list)
    meta: PaginationMeta

    class Config:
        from_attributes = True


def pagination_meta(page: int, per_page: int, total: int) -> PaginationMeta:
    """Build pagination meta from page, per_page, total."""
    total_pages = (total + per_page - 1) // per_page if per_page else 0
    return PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        total_pages=total_pages,
        has_next=page < total_pages,
        has_prev=page > 1,
    )
