"""Role schemas."""
from pydantic import BaseModel, Field

from app.schemas.permission import PermissionResponse


class RoleBase(BaseModel):
    """Base role schema."""

    name: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=30)
    description: str | None = Field(None, max_length=255)


class RoleCreate(RoleBase):
    """Create role request."""

    permission_ids: list[int] = Field(default_factory=list)


class RoleUpdate(BaseModel):
    """Update role (partial)."""

    name: str | None = Field(None, min_length=1, max_length=50)
    code: str | None = Field(None, min_length=1, max_length=30)
    description: str | None = None
    permission_ids: list[int] | None = None


class RoleResponse(RoleBase):
    """Role response."""

    id: int

    class Config:
        from_attributes = True


class RoleWithPermissionsResponse(RoleResponse):
    """Role with permissions list."""

    permissions: list[PermissionResponse] = []
