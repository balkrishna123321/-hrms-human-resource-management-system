"""Leave request repository."""
from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models.leave_request import LeaveRequest, LeaveRequestStatus


class LeaveRequestRepository:
    def __init__(self, db):
        self.db = db

    async def get_by_id(self, id: int) -> LeaveRequest | None:
        result = await self.db.execute(
            select(LeaveRequest)
            .where(LeaveRequest.id == id)
            .options(
                selectinload(LeaveRequest.employee),
                selectinload(LeaveRequest.leave_type),
            )
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 50,
        employee_id: int | None = None,
        status: LeaveRequestStatus | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> tuple[list[LeaveRequest], int]:
        q = select(LeaveRequest).options(
            selectinload(LeaveRequest.employee),
            selectinload(LeaveRequest.leave_type),
        )
        cq = select(func.count()).select_from(LeaveRequest)
        if employee_id is not None:
            q = q.where(LeaveRequest.employee_id == employee_id)
            cq = cq.where(LeaveRequest.employee_id == employee_id)
        if status is not None:
            q = q.where(LeaveRequest.status == status)
            cq = cq.where(LeaveRequest.status == status)
        if from_date is not None:
            q = q.where(LeaveRequest.from_date >= from_date)
            cq = cq.where(LeaveRequest.from_date >= from_date)
        if to_date is not None:
            q = q.where(LeaveRequest.to_date <= to_date)
            cq = cq.where(LeaveRequest.to_date <= to_date)
        total = (await self.db.execute(cq)).scalar() or 0
        q = q.order_by(LeaveRequest.from_date.desc()).offset(skip).limit(limit)
        result = await self.db.execute(q)
        return list(result.scalars().all()), total

    async def create(self, lr: LeaveRequest) -> LeaveRequest:
        self.db.add(lr)
        await self.db.flush()
        await self.db.refresh(lr)
        return lr

    async def update(self, lr: LeaveRequest) -> LeaveRequest:
        await self.db.flush()
        await self.db.refresh(lr)
        return lr
