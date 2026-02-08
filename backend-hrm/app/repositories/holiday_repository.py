"""Holiday repository."""
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.holiday import Holiday


class HolidayRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Holiday | None:
        result = await self.db.execute(select(Holiday).where(Holiday.id == id))
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        year: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> tuple[list[Holiday], int]:
        q = select(Holiday)
        cq = select(func.count()).select_from(Holiday)
        if year is not None:
            q = q.where((Holiday.year == year) | (Holiday.year.is_(None)))
            cq = cq.where((Holiday.year == year) | (Holiday.year.is_(None)))
        if from_date is not None:
            q = q.where(Holiday.date >= from_date)
            cq = cq.where(Holiday.date >= from_date)
        if to_date is not None:
            q = q.where(Holiday.date <= to_date)
            cq = cq.where(Holiday.date <= to_date)
        total = (await self.db.execute(cq)).scalar() or 0
        q = q.order_by(Holiday.date).offset(skip).limit(limit)
        result = await self.db.execute(q)
        return list(result.scalars().all()), total

    async def create(self, h: Holiday) -> Holiday:
        self.db.add(h)
        await self.db.flush()
        await self.db.refresh(h)
        return h

    async def delete(self, h: Holiday) -> None:
        await self.db.delete(h)
