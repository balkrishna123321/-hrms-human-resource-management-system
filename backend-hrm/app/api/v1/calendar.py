"""Calendar API - attendance logs, holidays, leave for a date range."""
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.holiday import Holiday
from app.models.leave_request import LeaveRequest, LeaveRequestStatus
from app.utils.responses import APIResponse

router = APIRouter()


@router.get("/logs")
async def get_calendar_logs(
    from_date: date = Query(...),
    to_date: date = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Get calendar view: attendance (check-in/check-out, working hours), holidays, and approved leave
    for the date range. Used to show who logged in/out and working hours.
    """
    if to_date < from_date:
        to_date = from_date

    # Attendance in range (with employee)
    att_q = (
        select(Attendance)
        .join(Employee)
        .where(Attendance.date >= from_date, Attendance.date <= to_date, Employee.is_active == True)
        .options(selectinload(Attendance.employee))
        .order_by(Attendance.date, Attendance.employee_id)
    )
    att_result = await db.execute(att_q)
    attendances = list(att_result.scalars().unique().all())

    # Holidays in range
    hol_q = select(Holiday).where(Holiday.date >= from_date, Holiday.date <= to_date).order_by(Holiday.date)
    hol_result = await db.execute(hol_q)
    holidays = list(hol_result.scalars().all())

    # Approved leave in range
    leave_q = (
        select(LeaveRequest)
        .where(
            LeaveRequest.status == LeaveRequestStatus.APPROVED,
            LeaveRequest.from_date <= to_date,
            LeaveRequest.to_date >= from_date,
        )
        .order_by(LeaveRequest.from_date)
    )
    leave_result = await db.execute(leave_q)
    leave_requests = list(leave_result.scalars().all())

    # Build response
    attendance_logs = []
    for a in attendances:
        check_in = a.check_in_time.isoformat() if a.check_in_time else None
        check_out = a.check_out_time.isoformat() if a.check_out_time else None
        work_hours = float(a.work_hours) if a.work_hours is not None else None
        attendance_logs.append({
            "id": a.id,
            "date": a.date.isoformat(),
            "employee_id": a.employee_id,
            "employee_name": a.employee.full_name if a.employee else None,
            "employee_employee_id": a.employee.employee_id if a.employee else None,
            "status": a.status.value,
            "check_in_time": check_in,
            "check_out_time": check_out,
            "work_hours": work_hours,
            "notes": a.notes,
        })

    holiday_list = [{"id": h.id, "name": h.name, "date": h.date.isoformat(), "year": h.year} for h in holidays]

    leave_list = []
    for lr in leave_requests:
        leave_list.append({
            "id": lr.id,
            "employee_id": lr.employee_id,
            "from_date": lr.from_date.isoformat(),
            "to_date": lr.to_date.isoformat(),
            "leave_type_id": lr.leave_type_id,
        })

    return APIResponse(
        data={
            "from_date": from_date.isoformat(),
            "to_date": to_date.isoformat(),
            "attendance_logs": attendance_logs,
            "holidays": holiday_list,
            "leave": leave_list,
        },
    )
