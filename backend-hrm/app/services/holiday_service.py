"""Holiday service."""
from datetime import date

from app.models.holiday import Holiday
from app.repositories.holiday_repository import HolidayRepository
from app.schemas.holiday import HolidayCreate, HolidayUpdate
from app.utils.exceptions import NotFoundError


class HolidayService:
    def __init__(self, repo: HolidayRepository):
        self.repo = repo

    async def get_by_id(self, id: int) -> Holiday:
        h = await self.repo.get_by_id(id)
        if not h:
            raise NotFoundError("Holiday not found", resource="holiday_id")
        return h

    async def get_all(
        self,
        page: int = 1,
        per_page: int = 100,
        year: int | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> tuple[list[Holiday], int]:
        skip = (page - 1) * per_page
        return await self.repo.get_all(
            skip=skip,
            limit=per_page,
            year=year,
            from_date=from_date,
            to_date=to_date,
        )

    async def create(self, payload: HolidayCreate) -> Holiday:
        h = Holiday(
            name=payload.name,
            date=payload.date,
            year=payload.year,
            description=payload.description,
        )
        return await self.repo.create(h)

    async def update(self, id: int, payload: HolidayUpdate) -> Holiday:
        h = await self.get_by_id(id)
        if payload.name is not None:
            h.name = payload.name
        if payload.date is not None:
            h.date = payload.date
        if payload.year is not None:
            h.year = payload.year
        if payload.description is not None:
            h.description = payload.description
        await self.repo.db.flush()
        await self.repo.db.refresh(h)
        return h

    async def delete(self, id: int) -> None:
        h = await self.get_by_id(id)
        await self.repo.delete(h)
