"""Attendance schemas."""
from datetime import date, time
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.attendance import AttendanceStatus, AttendanceSource


class AttendanceBase(BaseModel):
    """Base attendance schema."""

    date: date
    status: AttendanceStatus = AttendanceStatus.PRESENT
    check_in_time: time | None = None
    check_out_time: time | None = None
    work_hours: Decimal | None = None
    source: AttendanceSource | None = AttendanceSource.WEB
    notes: str | None = None


class AttendanceCreate(AttendanceBase):
    """Create attendance (employee_id from path)."""

    pass


class AttendanceUpdate(BaseModel):
    """Update attendance."""

    status: AttendanceStatus | None = None
    check_in_time: time | None = None
    check_out_time: time | None = None
    work_hours: Decimal | None = None
    source: AttendanceSource | None = None
    notes: str | None = None


class AttendanceResponse(AttendanceBase):
    """Attendance response."""

    id: int
    employee_id: int

    class Config:
        from_attributes = True


class AttendanceWithEmployeeResponse(AttendanceResponse):
    """Attendance with employee info."""

    employee_employee_id: str | None = None
    employee_full_name: str | None = None
