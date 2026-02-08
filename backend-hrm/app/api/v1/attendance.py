"""Attendance API routes."""
from datetime import date

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_attendance_service, get_current_user
from app.models.user import User
from app.models.attendance import AttendanceStatus
from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse,
    AttendanceWithEmployeeResponse,
)
from app.services.attendance_service import AttendanceService
from app.utils.responses import APIResponse, PaginatedResponse, pagination_meta

router = APIRouter()


@router.get("", response_model=PaginatedResponse[AttendanceWithEmployeeResponse])
async def list_attendance(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    status: AttendanceStatus | None = Query(None),
    department: str | None = Query(None),
    current_user: User = Depends(get_current_user),
    service: AttendanceService = Depends(get_attendance_service),
):
    """List all attendance with filters (date range, status, department)."""
    items, total = await service.get_all(
        page=page,
        per_page=per_page,
        from_date=from_date,
        to_date=to_date,
        status=status,
        department=department,
    )
    meta = pagination_meta(page, per_page, total)
    data = [
        AttendanceWithEmployeeResponse(
            id=a.id,
            employee_id=a.employee_id,
            date=a.date,
            status=a.status,
            check_in_time=a.check_in_time,
            check_out_time=a.check_out_time,
            work_hours=a.work_hours,
            source=a.source,
            notes=a.notes,
            employee_employee_id=a.employee.employee_id if a.employee else None,
            employee_full_name=a.employee.full_name if a.employee else None,
        )
        for a in items
    ]
    return PaginatedResponse(data=data, meta=meta)


@router.get("/employee/{employee_id}", response_model=PaginatedResponse[AttendanceResponse])
async def list_attendance_by_employee(
    employee_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    status: AttendanceStatus | None = Query(None),
    current_user: User = Depends(get_current_user),
    service: AttendanceService = Depends(get_attendance_service),
):
    """List attendance for a specific employee with optional date/status filters."""
    items, total = await service.get_by_employee(
        employee_id,
        page=page,
        per_page=per_page,
        from_date=from_date,
        to_date=to_date,
        status=status,
    )
    meta = pagination_meta(page, per_page, total)
    data = [
        AttendanceResponse(
            id=a.id,
            employee_id=a.employee_id,
            date=a.date,
            status=a.status,
            check_in_time=a.check_in_time,
            check_out_time=a.check_out_time,
            work_hours=a.work_hours,
            source=a.source,
            notes=a.notes,
        )
        for a in items
    ]
    return PaginatedResponse(data=data, meta=meta)


@router.get("/employee/{employee_id}/present-days")
async def get_present_days(
    employee_id: int,
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    service: AttendanceService = Depends(get_attendance_service),
):
    """Get total present days for an employee (optional date range)."""
    count = await service.count_present_days(employee_id, from_date=from_date, to_date=to_date)
    return APIResponse(data={"employee_id": employee_id, "present_days": count})


@router.post("/employee/{employee_id}", response_model=APIResponse[AttendanceResponse], status_code=201)
async def mark_attendance(
    employee_id: int,
    payload: AttendanceCreate,
    current_user: User = Depends(get_current_user),
    service: AttendanceService = Depends(get_attendance_service),
):
    """Mark attendance for an employee on a date (Present/Absent)."""
    record = await service.create(employee_id, payload)
    return APIResponse(
        message="Attendance marked",
        data=AttendanceResponse(
            id=record.id,
            employee_id=record.employee_id,
            date=record.date,
            status=record.status,
            check_in_time=record.check_in_time,
            check_out_time=record.check_out_time,
            work_hours=record.work_hours,
            source=record.source,
            notes=record.notes,
        ),
    )


@router.patch("/{attendance_id}", response_model=APIResponse[AttendanceResponse])
async def update_attendance(
    attendance_id: int,
    payload: AttendanceUpdate,
    current_user: User = Depends(get_current_user),
    service: AttendanceService = Depends(get_attendance_service),
):
    """Update an attendance record."""
    record = await service.update(attendance_id, payload)
    return APIResponse(
        message="Attendance updated",
        data=AttendanceResponse(
            id=record.id,
            employee_id=record.employee_id,
            date=record.date,
            status=record.status,
            check_in_time=record.check_in_time,
            check_out_time=record.check_out_time,
            work_hours=record.work_hours,
            source=record.source,
            notes=record.notes,
        ),
    )


@router.delete("/{attendance_id}", status_code=204)
async def delete_attendance(
    attendance_id: int,
    current_user: User = Depends(get_current_user),
    service: AttendanceService = Depends(get_attendance_service),
):
    """Delete an attendance record."""
    await service.delete(attendance_id)
