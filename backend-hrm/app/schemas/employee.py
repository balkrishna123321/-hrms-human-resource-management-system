"""Employee schemas."""
from datetime import date

from pydantic import BaseModel, EmailStr, Field

from app.models.employee import EmployeeType, Gender


class EmployeeBase(BaseModel):
    """Base employee schema."""

    employee_id: str = Field(..., min_length=1, max_length=50, description="Unique employee ID")
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    phone: str | None = Field(None, max_length=20)
    department: str | None = Field(None, max_length=100)
    department_id: int | None = None
    designation: str | None = Field(None, max_length=100)
    date_of_joining: date | None = None
    manager_id: int | None = None
    address: str | None = None
    emergency_contact_name: str | None = Field(None, max_length=255)
    emergency_contact_phone: str | None = Field(None, max_length=20)
    date_of_birth: date | None = None
    gender: Gender | None = None
    employee_type: EmployeeType | None = EmployeeType.FULL_TIME


class EmployeeCreate(EmployeeBase):
    """Create employee request."""

    pass


class EmployeeUpdate(BaseModel):
    """Update employee (partial)."""

    full_name: str | None = Field(None, min_length=1, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=20)
    department: str | None = Field(None, max_length=100)
    department_id: int | None = None
    designation: str | None = Field(None, max_length=100)
    date_of_joining: date | None = None
    manager_id: int | None = None
    address: str | None = None
    emergency_contact_name: str | None = Field(None, max_length=255)
    emergency_contact_phone: str | None = Field(None, max_length=20)
    date_of_birth: date | None = None
    gender: Gender | None = None
    employee_type: EmployeeType | None = None
    is_active: bool | None = None


class EmployeeResponse(EmployeeBase):
    """Employee response."""

    id: int
    is_active: bool = True

    class Config:
        from_attributes = True


class EmployeeListResponse(EmployeeResponse):
    """Employee with optional attendance summary."""

    total_present_days: int | None = None
    department_name: str | None = None
