"""Attendance repository."""
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models.attendance import Attendance, AttendanceStatus
from app.models.employee import Employee


class AttendanceRepository:
    """Attendance data access."""

    def __init__(self, db):
        self.db = db

    async def get_by_id(self, id: int) -> Attendance | None:
        """Get attendance record by id."""
        result = await self.db.execute(
            select(Attendance).where(Attendance.id == id).options(selectinload(Attendance.employee))
        )
        return result.scalar_one_or_none()

    async def get_by_employee_and_date(self, employee_id: int, d: date) -> Attendance | None:
        """Get attendance for employee on date."""
        result = await self.db.execute(
            select(Attendance).where(
                Attendance.employee_id == employee_id,
                Attendance.date == d,
            )
        )
        return result.scalar_one_or_none()

    async def get_by_employee(
        self,
        employee_id: int,
        *,
        skip: int = 0,
        limit: int = 100,
        from_date: date | None = None,
        to_date: date | None = None,
        status: AttendanceStatus | None = None,
    ) -> tuple[list[Attendance], int]:
        """Get paginated attendance for one employee. Returns (items, total)."""
        query = select(Attendance).where(Attendance.employee_id == employee_id)
        count_query = select(func.count()).select_from(Attendance).where(Attendance.employee_id == employee_id)
        if from_date:
            query = query.where(Attendance.date >= from_date)
            count_query = count_query.where(Attendance.date >= from_date)
        if to_date:
            query = query.where(Attendance.date <= to_date)
            count_query = count_query.where(Attendance.date <= to_date)
        if status is not None:
            query = query.where(Attendance.status == status)
            count_query = count_query.where(Attendance.status == status)
        total = (await self.db.execute(count_query)).scalar() or 0
        query = query.order_by(Attendance.date.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        from_date: date | None = None,
        to_date: date | None = None,
        status: AttendanceStatus | None = None,
        department: str | None = None,
    ) -> tuple[list[Attendance], int]:
        """Get all attendance with filters, joined with employee. Returns (items, total)."""
        query = select(Attendance).join(Employee).where(Employee.is_active == True)
        count_query = select(func.count()).select_from(Attendance).join(Employee).where(Employee.is_active == True)
        if from_date:
            query = query.where(Attendance.date >= from_date)
            count_query = count_query.where(Attendance.date >= from_date)
        if to_date:
            query = query.where(Attendance.date <= to_date)
            count_query = count_query.where(Attendance.date <= to_date)
        if status is not None:
            query = query.where(Attendance.status == status)
            count_query = count_query.where(Attendance.status == status)
        if department:
            query = query.where(Employee.department == department)
            count_query = count_query.where(Employee.department == department)
        total = (await self.db.execute(count_query)).scalar() or 0
        query = (
            query.options(selectinload(Attendance.employee))
            .order_by(Attendance.date.desc(), Attendance.id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def count_present_days(self, employee_id: int, from_date: date | None = None, to_date: date | None = None) -> int:
        """Count present days for employee in optional date range."""
        q = select(func.count()).select_from(Attendance).where(
            Attendance.employee_id == employee_id,
            Attendance.status == AttendanceStatus.PRESENT,
        )
        if from_date:
            q = q.where(Attendance.date >= from_date)
        if to_date:
            q = q.where(Attendance.date <= to_date)
        return (await self.db.execute(q)).scalar() or 0

    async def create(self, attendance: Attendance) -> Attendance:
        """Persist new attendance."""
        self.db.add(attendance)
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def update(self, attendance: Attendance) -> Attendance:
        """Update attendance."""
        await self.db.flush()
        await self.db.refresh(attendance)
        return attendance

    async def delete(self, attendance: Attendance) -> None:
        """Delete attendance record."""
        await self.db.delete(attendance)
