"""SQLAlchemy models."""
from app.models.department import Department
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.user import User
from app.models.permission import Permission
from app.models.role import Role
from app.models.leave_type import LeaveType
from app.models.leave_balance import LeaveBalance
from app.models.leave_request import LeaveRequest
from app.models.holiday import Holiday

__all__ = [
    "Department",
    "Employee",
    "Attendance",
    "User",
    "Permission",
    "Role",
    "LeaveType",
    "LeaveBalance",
    "LeaveRequest",
    "Holiday",
]
