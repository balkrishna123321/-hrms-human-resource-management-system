"""Leave request service."""
from datetime import date

from app.models.leave_request import LeaveRequest, LeaveRequestStatus
from app.repositories.leave_request_repository import LeaveRequestRepository
from app.repositories.leave_balance_repository import LeaveBalanceRepository
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestUpdate
from app.utils.exceptions import NotFoundError


class LeaveRequestService:
    def __init__(self, repo: LeaveRequestRepository, balance_repo: LeaveBalanceRepository):
        self.repo = repo
        self.balance_repo = balance_repo

    async def get_by_id(self, id: int) -> LeaveRequest:
        lr = await self.repo.get_by_id(id)
        if not lr:
            raise NotFoundError("Leave request not found", resource="leave_request_id")
        return lr

    async def get_all(
        self,
        page: int = 1,
        per_page: int = 50,
        employee_id: int | None = None,
        status: LeaveRequestStatus | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> tuple[list[LeaveRequest], int]:
        skip = (page - 1) * per_page
        return await self.repo.get_all(
            skip=skip,
            limit=per_page,
            employee_id=employee_id,
            status=status,
            from_date=from_date,
            to_date=to_date,
        )

    async def create(self, employee_id: int, payload: LeaveRequestCreate) -> LeaveRequest:
        lr = LeaveRequest(
            employee_id=employee_id,
            leave_type_id=payload.leave_type_id,
            from_date=payload.from_date,
            to_date=payload.to_date,
            reason=payload.reason,
        )
        return await self.repo.create(lr)

    async def update(self, id: int, payload: LeaveRequestUpdate, approved_by_id: int | None = None) -> LeaveRequest:
        lr = await self.get_by_id(id)
        if payload.status is not None:
            lr.status = payload.status
            if approved_by_id is not None:
                lr.approved_by_id = approved_by_id
        if payload.reason is not None:
            lr.reason = payload.reason
        return await self.repo.update(lr)
