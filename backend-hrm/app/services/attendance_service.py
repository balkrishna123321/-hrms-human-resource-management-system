"""Attendance business logic."""
from datetime import date

from app.models.attendance import Attendance, AttendanceStatus
from app.repositories.attendance_repository import AttendanceRepository
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate
from app.utils.exceptions import ConflictError, NotFoundError


class AttendanceService:
    """Attendance use cases."""

    def __init__(self, attendance_repo: AttendanceRepository, employee_repo: EmployeeRepository):
        self.attendance_repo = attendance_repo
        self.employee_repo = employee_repo

    async def get_by_id(self, id: int) -> Attendance:
        """Get attendance record or raise NotFound."""
        record = await self.attendance_repo.get_by_id(id)
        if not record:
            raise NotFoundError("Attendance record not found", resource="attendance_id")
        return record

    async def get_by_employee(
        self,
        employee_id: int,
        page: int = 1,
        per_page: int = 20,
        from_date: date | None = None,
        to_date: date | None = None,
        status: AttendanceStatus | None = None,
    ) -> tuple[list[Attendance], int]:
        """Get paginated attendance for employee."""
        if await self.employee_repo.get_by_id(employee_id) is None:
            raise NotFoundError("Employee not found", resource="employee_id")
        skip = (page - 1) * per_page
        return await self.attendance_repo.get_by_employee(
            employee_id, skip=skip, limit=per_page, from_date=from_date, to_date=to_date, status=status
        )

    async def get_all(
        self,
        page: int = 1,
        per_page: int = 20,
        from_date: date | None = None,
        to_date: date | None = None,
        status: AttendanceStatus | None = None,
        department: str | None = None,
    ) -> tuple[list[Attendance], int]:
        """Get all attendance with filters."""
        skip = (page - 1) * per_page
        return await self.attendance_repo.get_all(
            skip=skip,
            limit=per_page,
            from_date=from_date,
            to_date=to_date,
            status=status,
            department=department,
        )

    async def create(self, employee_id: int, payload: AttendanceCreate) -> Attendance:
        """Mark attendance for employee on date; one record per employee per date."""
        employee = await self.employee_repo.get_by_id(employee_id)
        if not employee:
            raise NotFoundError("Employee not found", resource="employee_id")
        existing = await self.attendance_repo.get_by_employee_and_date(employee_id, payload.date)
        if existing:
            raise ConflictError(
                f"Attendance already marked for this employee on {payload.date}",
                field="date",
            )
        record = Attendance(
            employee_id=employee_id,
            date=payload.date,
            status=payload.status,
            check_in_time=payload.check_in_time,
            check_out_time=payload.check_out_time,
            work_hours=payload.work_hours,
            source=payload.source,
            notes=payload.notes,
        )
        return await self.attendance_repo.create(record)

    async def update(self, id: int, payload: AttendanceUpdate) -> Attendance:
        """Update attendance record."""
        record = await self.get_by_id(id)
        if payload.status is not None:
            record.status = payload.status
        if payload.check_in_time is not None:
            record.check_in_time = payload.check_in_time
        if payload.check_out_time is not None:
            record.check_out_time = payload.check_out_time
        if payload.work_hours is not None:
            record.work_hours = payload.work_hours
        if payload.source is not None:
            record.source = payload.source
        if payload.notes is not None:
            record.notes = payload.notes
        return await self.attendance_repo.update(record)

    async def delete(self, id: int) -> None:
        """Delete attendance record."""
        record = await self.get_by_id(id)
        await self.attendance_repo.delete(record)

    async def count_present_days(
        self,
        employee_id: int,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> int:
        """Total present days for employee in optional range."""
        if await self.employee_repo.get_by_id(employee_id) is None:
            raise NotFoundError("Employee not found", resource="employee_id")
        return await self.attendance_repo.count_present_days(employee_id, from_date=from_date, to_date=to_date)
