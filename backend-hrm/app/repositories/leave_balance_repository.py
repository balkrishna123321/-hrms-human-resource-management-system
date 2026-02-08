"""Leave balance repository."""
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models.leave_balance import LeaveBalance
from app.models.leave_type import LeaveType


class LeaveBalanceRepository:
    def __init__(self, db):
        self.db = db

    async def get_by_id(self, id: int) -> LeaveBalance | None:
        result = await self.db.execute(
            select(LeaveBalance)
            .where(LeaveBalance.id == id)
            .options(selectinload(LeaveBalance.employee), selectinload(LeaveBalance.leave_type))
        )
        return result.scalar_one_or_none()

    async def get_for_employee_year(self, employee_id: int, year: int) -> list[LeaveBalance]:
        result = await self.db.execute(
            select(LeaveBalance)
            .where(LeaveBalance.employee_id == employee_id, LeaveBalance.year == year)
            .options(selectinload(LeaveBalance.leave_type))
        )
        return list(result.scalars().all())

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        employee_id: int | None = None,
        year: int | None = None,
    ) -> tuple[list[LeaveBalance], int]:
        q = select(LeaveBalance).options(
            selectinload(LeaveBalance.employee),
            selectinload(LeaveBalance.leave_type),
        )
        cq = select(func.count()).select_from(LeaveBalance)
        if employee_id is not None:
            q = q.where(LeaveBalance.employee_id == employee_id)
            cq = cq.where(LeaveBalance.employee_id == employee_id)
        if year is not None:
            q = q.where(LeaveBalance.year == year)
            cq = cq.where(LeaveBalance.year == year)
        total = (await self.db.execute(cq)).scalar() or 0
        q = q.order_by(LeaveBalance.year.desc(), LeaveBalance.employee_id).offset(skip).limit(limit)
        result = await self.db.execute(q)
        return list(result.scalars().all()), total

    async def create(self, lb: LeaveBalance) -> LeaveBalance:
        self.db.add(lb)
        await self.db.flush()
        await self.db.refresh(lb)
        return lb

    async def update(self, lb: LeaveBalance) -> LeaveBalance:
        await self.db.flush()
        await self.db.refresh(lb)
        return lb
