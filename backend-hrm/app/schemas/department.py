"""Department schemas."""
from pydantic import BaseModel, Field


class DepartmentBase(BaseModel):
    """Base department schema."""

    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=20)
    description: str | None = Field(None, max_length=500)


class DepartmentCreate(DepartmentBase):
    """Create department request."""

    pass


class DepartmentUpdate(BaseModel):
    """Update department (partial)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    code: str | None = Field(None, min_length=1, max_length=20)
    description: str | None = None


class DepartmentResponse(DepartmentBase):
    """Department response."""

    id: int

    class Config:
        from_attributes = True


class DepartmentWithCountResponse(DepartmentResponse):
    """Department with employee count."""

    employee_count: int = 0
