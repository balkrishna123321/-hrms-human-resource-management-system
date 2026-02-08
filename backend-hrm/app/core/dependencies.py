"""FastAPI dependencies."""
from typing import Annotated

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import decode_token
from app.db.base import get_db
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.department_repository import DepartmentRepository
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.user_repository import UserRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.repositories.leave_type_repository import LeaveTypeRepository
from app.repositories.leave_balance_repository import LeaveBalanceRepository
from app.repositories.leave_request_repository import LeaveRequestRepository
from app.repositories.holiday_repository import HolidayRepository
from app.services.attendance_service import AttendanceService
from app.services.auth_service import AuthService
from app.services.department_service import DepartmentService
from app.services.employee_service import EmployeeService
from app.services.permission_service import PermissionService
from app.services.role_service import RoleService
from app.services.leave_type_service import LeaveTypeService
from app.services.leave_balance_service import LeaveBalanceService
from app.services.leave_request_service import LeaveRequestService
from app.services.holiday_service import HolidayService
from app.models.user import User
from app.utils.exceptions import UnauthorizedError

settings = get_settings()


async def get_current_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    authorization: Annotated[str | None, Header()] = None,
) -> User:
    """Extract JWT from Authorization header and return current user."""
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Missing or invalid authorization header")
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise UnauthorizedError("Invalid or expired access token")
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token")
    repo = UserRepository(db)
    service = AuthService(repo)
    return await service.get_current_user(int(user_id))


# Optional: unauthenticated access for health, etc.
def get_optional_user(
    authorization: Annotated[str | None, Header()] = None,
) -> User | None:
    """Return user if valid token present, else None. Not async for simplicity; use get_current_user for required auth."""
    return None  # Use get_current_user for protected routes


# Service dependencies
def get_employee_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> EmployeeRepository:
    return EmployeeRepository(db)


def get_attendance_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> AttendanceRepository:
    return AttendanceRepository(db)


def get_user_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)


def get_department_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> DepartmentRepository:
    return DepartmentRepository(db)


def get_department_service(repo: Annotated[DepartmentRepository, Depends(get_department_repo)]) -> DepartmentService:
    return DepartmentService(repo)


def get_employee_service(
    repo: Annotated[EmployeeRepository, Depends(get_employee_repo)],
    department_repo: Annotated[DepartmentRepository, Depends(get_department_repo)],
) -> EmployeeService:
    return EmployeeService(repo, department_repo)


def get_attendance_service(
    att_repo: Annotated[AttendanceRepository, Depends(get_attendance_repo)],
    emp_repo: Annotated[EmployeeRepository, Depends(get_employee_repo)],
) -> AttendanceService:
    return AttendanceService(att_repo, emp_repo)


def get_auth_service(repo: Annotated[UserRepository, Depends(get_user_repo)]) -> AuthService:
    return AuthService(repo)


def get_permission_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> PermissionRepository:
    return PermissionRepository(db)


def get_role_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> RoleRepository:
    return RoleRepository(db)


def get_permission_service(repo: Annotated[PermissionRepository, Depends(get_permission_repo)]) -> PermissionService:
    return PermissionService(repo)


def get_role_service(
    role_repo: Annotated[RoleRepository, Depends(get_role_repo)],
    perm_repo: Annotated[PermissionRepository, Depends(get_permission_repo)],
) -> RoleService:
    return RoleService(role_repo, perm_repo)


def get_leave_type_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> LeaveTypeRepository:
    return LeaveTypeRepository(db)


def get_leave_balance_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> LeaveBalanceRepository:
    return LeaveBalanceRepository(db)


def get_leave_request_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> LeaveRequestRepository:
    return LeaveRequestRepository(db)


def get_holiday_repo(db: Annotated[AsyncSession, Depends(get_db)]) -> HolidayRepository:
    return HolidayRepository(db)


def get_leave_type_service(repo: Annotated[LeaveTypeRepository, Depends(get_leave_type_repo)]) -> LeaveTypeService:
    return LeaveTypeService(repo)


def get_leave_balance_service(
    repo: Annotated[LeaveBalanceRepository, Depends(get_leave_balance_repo)],
    lt_repo: Annotated[LeaveTypeRepository, Depends(get_leave_type_repo)],
) -> LeaveBalanceService:
    return LeaveBalanceService(repo, lt_repo)


def get_leave_request_service(
    repo: Annotated[LeaveRequestRepository, Depends(get_leave_request_repo)],
    balance_repo: Annotated[LeaveBalanceRepository, Depends(get_leave_balance_repo)],
) -> LeaveRequestService:
    return LeaveRequestService(repo, balance_repo)


def get_holiday_service(repo: Annotated[HolidayRepository, Depends(get_holiday_repo)]) -> HolidayService:
    return HolidayService(repo)
