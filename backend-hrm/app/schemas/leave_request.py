"""Leave request schemas."""
from datetime import date

from pydantic import BaseModel, Field

from app.models.leave_request import LeaveRequestStatus


class LeaveRequestBase(BaseModel):
    """Base leave request schema."""

    leave_type_id: int
    from_date: date
    to_date: date
    reason: str | None = None


class LeaveRequestCreate(LeaveRequestBase):
    """Create leave request (employee_id from path or current user)."""

    pass


class LeaveRequestUpdate(BaseModel):
    """Update leave request (e.g. approve/reject)."""

    status: LeaveRequestStatus | None = None
    reason: str | None = None


class LeaveRequestResponse(LeaveRequestBase):
    """Leave request response."""

    id: int
    employee_id: int
    status: LeaveRequestStatus
    approved_by_id: int | None = None

    class Config:
        from_attributes = True


class LeaveRequestWithDetailsResponse(LeaveRequestResponse):
    """Leave request with employee and leave type names."""

    employee_name: str | None = None
    leave_type_name: str | None = None
    total_days: int = 0
