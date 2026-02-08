"""Permission schemas."""
from pydantic import BaseModel, Field


class PermissionBase(BaseModel):
    """Base permission schema."""

    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=50)
    description: str | None = Field(None, max_length=255)


class PermissionCreate(PermissionBase):
    """Create permission request."""

    pass


class PermissionResponse(PermissionBase):
    """Permission response."""

    id: int

    class Config:
        from_attributes = True
