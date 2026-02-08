"""Leave type repository."""
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.leave_type import LeaveType


class LeaveTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> LeaveType | None:
        result = await self.db.execute(select(LeaveType).where(LeaveType.id == id))
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> LeaveType | None:
        result = await self.db.execute(select(LeaveType).where(LeaveType.code == code))
        return result.scalar_one_or_none()

    async def get_all(self, *, skip: int = 0, limit: int = 50) -> tuple[list[LeaveType], int]:
        total = (await self.db.execute(select(func.count()).select_from(LeaveType))).scalar() or 0
        result = await self.db.execute(select(LeaveType).order_by(LeaveType.code).offset(skip).limit(limit))
        return list(result.scalars().all()), total

    async def create(self, lt: LeaveType) -> LeaveType:
        self.db.add(lt)
        await self.db.flush()
        await self.db.refresh(lt)
        return lt

    async def delete(self, lt: LeaveType) -> None:
        await self.db.delete(lt)
