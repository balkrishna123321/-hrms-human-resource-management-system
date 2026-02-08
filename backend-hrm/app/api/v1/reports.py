"""Reports API (aggregated data for export/dashboards)."""
from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.employee import Employee
from app.models.attendance import Attendance, AttendanceStatus
from app.utils.responses import APIResponse

router = APIRouter()


@router.get("/attendance-summary")
async def attendance_summary_report(
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Report: attendance counts by status in date range."""
    total_q = select(func.count()).select_from(Attendance)
    if from_date:
        total_q = total_q.where(Attendance.date >= from_date)
    if to_date:
        total_q = total_q.where(Attendance.date <= to_date)
    total = (await db.execute(total_q)).scalar() or 0

    present_q = select(func.count()).select_from(Attendance).where(Attendance.status == AttendanceStatus.PRESENT)
    if from_date:
        present_q = present_q.where(Attendance.date >= from_date)
    if to_date:
        present_q = present_q.where(Attendance.date <= to_date)
    present = (await db.execute(present_q)).scalar() or 0

    absent_q = select(func.count()).select_from(Attendance).where(Attendance.status == AttendanceStatus.ABSENT)
    if from_date:
        absent_q = absent_q.where(Attendance.date >= from_date)
    if to_date:
        absent_q = absent_q.where(Attendance.date <= to_date)
    absent = (await db.execute(absent_q)).scalar() or 0

    return APIResponse(
        data={
            "from_date": from_date.isoformat() if from_date else None,
            "to_date": to_date.isoformat() if to_date else None,
            "total_records": total,
            "present": present,
            "absent": absent,
            "other": total - present - absent,
        },
    )


@router.get("/employee-count-by-department")
async def employee_count_by_department_report(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Report: employee count grouped by department (from denormalized department field)."""
    stmt = (
        select(Employee.department, func.count(Employee.id).label("count"))
        .where(Employee.is_active == True)
        .where(Employee.department.isnot(None))
        .group_by(Employee.department)
        .order_by(Employee.department)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return APIResponse(
        data={"departments": [{"name": r.department or "Unknown", "employee_count": r.count} for r in rows]},
    )
