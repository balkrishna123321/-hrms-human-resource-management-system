"""Department repository."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department


class DepartmentRepository:
    """Department data access."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Department | None:
        """Get department by primary key."""
        result = await self.db.execute(select(Department).where(Department.id == id))
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Department | None:
        """Get department by code."""
        result = await self.db.execute(select(Department).where(Department.code == code))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> tuple[list[Department], int]:
        """Get paginated departments. Returns (items, total)."""
        count_query = select(func.count()).select_from(Department)
        total = (await self.db.execute(count_query)).scalar() or 0
        query = select(Department).order_by(Department.name).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def create(self, department: Department) -> Department:
        """Persist new department."""
        self.db.add(department)
        await self.db.flush()
        await self.db.refresh(department)
        return department

    async def delete(self, department: Department) -> None:
        """Delete department."""
        await self.db.delete(department)
