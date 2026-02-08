"""Leave type schemas."""
from pydantic import BaseModel, Field


class LeaveTypeBase(BaseModel):
    """Base leave type schema."""

    name: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=20)
    default_days_per_year: int = Field(0, ge=0)
    description: str | None = Field(None, max_length=255)


class LeaveTypeCreate(LeaveTypeBase):
    """Create leave type request."""

    pass


class LeaveTypeUpdate(BaseModel):
    """Update leave type (partial)."""

    name: str | None = Field(None, min_length=1, max_length=50)
    code: str | None = Field(None, min_length=1, max_length=20)
    default_days_per_year: int | None = Field(None, ge=0)
    description: str | None = None


class LeaveTypeResponse(LeaveTypeBase):
    """Leave type response."""

    id: int

    class Config:
        from_attributes = True
