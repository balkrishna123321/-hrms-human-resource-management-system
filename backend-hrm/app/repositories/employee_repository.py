"""Employee repository."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.employee import Employee


class EmployeeRepository:
    """Employee data access."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Employee | None:
        """Get employee by primary key (eager-load department for async safety)."""
        result = await self.db.execute(
            select(Employee).where(Employee.id == id).options(selectinload(Employee.department_rel))
        )
        return result.scalar_one_or_none()

    async def get_by_employee_id(self, employee_id: str) -> Employee | None:
        """Get employee by unique employee_id."""
        result = await self.db.execute(select(Employee).where(Employee.employee_id == employee_id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Employee | None:
        """Get employee by email."""
        result = await self.db.execute(select(Employee).where(Employee.email == email))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        department: str | None = None,
        department_id: int | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[Employee], int]:
        """Get paginated employees with optional filters. Returns (items, total)."""
        query = select(Employee)
        count_query = select(func.count()).select_from(Employee)
        if department:
            query = query.where(Employee.department == department)
            count_query = count_query.where(Employee.department == department)
        if department_id is not None:
            query = query.where(Employee.department_id == department_id)
            count_query = count_query.where(Employee.department_id == department_id)
        if is_active is not None:
            query = query.where(Employee.is_active == is_active)
            count_query = count_query.where(Employee.is_active == is_active)
        total = (await self.db.execute(count_query)).scalar() or 0
        query = (
            query.options(selectinload(Employee.department_rel))
            .order_by(Employee.id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def create(self, employee: Employee) -> Employee:
        """Persist new employee."""
        self.db.add(employee)
        await self.db.flush()
        await self.db.refresh(employee)
        return employee

    async def delete(self, employee: Employee) -> None:
        """Delete employee."""
        await self.db.delete(employee)
