"""API v1 router aggregation."""
from fastapi import APIRouter

from app.api.v1 import (
    auth,
    employees,
    attendance,
    dashboard,
    departments,
    health,
    reports,
    permissions,
    roles,
    leave_types,
    leave_balances,
    leave_requests,
    holidays,
    calendar,
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(employees.router, prefix="/employees", tags=["employees"])
api_router.include_router(departments.router, prefix="/departments", tags=["departments"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
api_router.include_router(leave_types.router, prefix="/leave-types", tags=["leave-types"])
api_router.include_router(leave_balances.router, prefix="/leave-balances", tags=["leave-balances"])
api_router.include_router(leave_requests.router, prefix="/leave-requests", tags=["leave-requests"])
api_router.include_router(holidays.router, prefix="/holidays", tags=["holidays"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
