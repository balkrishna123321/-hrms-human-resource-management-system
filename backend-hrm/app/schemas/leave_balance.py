"""Leave balance schemas."""
from pydantic import BaseModel, Field


class LeaveBalanceBase(BaseModel):
    """Base leave balance schema."""

    employee_id: int
    leave_type_id: int
    year: int = Field(..., ge=2000, le=2100)
    balance_days: int = Field(0, ge=0)
    used_days: int = Field(0, ge=0)


class LeaveBalanceCreate(LeaveBalanceBase):
    """Create leave balance request."""

    pass


class LeaveBalanceUpdate(BaseModel):
    """Update leave balance (partial)."""

    balance_days: int | None = Field(None, ge=0)
    used_days: int | None = Field(None, ge=0)


class LeaveBalanceResponse(LeaveBalanceBase):
    """Leave balance response."""

    id: int

    class Config:
        from_attributes = True


class LeaveBalanceWithDetailsResponse(LeaveBalanceResponse):
    """Leave balance with employee and leave type names."""

    employee_name: str | None = None
    leave_type_name: str | None = None
    available_days: int = 0
