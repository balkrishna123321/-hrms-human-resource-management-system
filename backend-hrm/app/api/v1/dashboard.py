"""Dashboard API (summary stats)."""
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


@router.get("/summary")
async def dashboard_summary(
    from_date: date | None = Query(None),
    to_date: date | None = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Dashboard summary: total employees, total attendance records, present/absent counts."""
    # Total employees (active)
    emp_count = await db.execute(select(func.count()).select_from(Employee).where(Employee.is_active == True))
    total_employees = emp_count.scalar() or 0

    # Total attendance records in date range
    total_q = select(func.count()).select_from(Attendance)
    if from_date:
        total_q = total_q.where(Attendance.date >= from_date)
    if to_date:
        total_q = total_q.where(Attendance.date <= to_date)
    total_records = (await db.execute(total_q)).scalar() or 0

    present_q = select(func.count()).select_from(Attendance).where(Attendance.status == AttendanceStatus.PRESENT)
    if from_date:
        present_q = present_q.where(Attendance.date >= from_date)
    if to_date:
        present_q = present_q.where(Attendance.date <= to_date)
    present_count = (await db.execute(present_q)).scalar() or 0
    absent_count = total_records - present_count

    return APIResponse(
        data={
            "total_employees": total_employees,
            "total_attendance_records": total_records,
            "present_count": present_count,
            "absent_count": absent_count,
            "from_date": from_date.isoformat() if from_date else None,
            "to_date": to_date.isoformat() if to_date else None,
        },
    )


@router.get("/departments")
async def department_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List departments with employee count."""
    stmt = (
        select(Employee.department, func.count(Employee.id).label("count"))
        .where(Employee.is_active == True)
        .group_by(Employee.department)
        .order_by(Employee.department)
    )
    result = await db.execute(stmt)
    rows = result.all()
    return APIResponse(
        data={"departments": [{"name": r.department, "employee_count": r.count} for r in rows]},
    )
