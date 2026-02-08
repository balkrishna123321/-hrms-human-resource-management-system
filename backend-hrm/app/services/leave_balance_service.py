"""Leave balance service."""
from app.models.leave_balance import LeaveBalance
from app.repositories.leave_balance_repository import LeaveBalanceRepository
from app.repositories.leave_type_repository import LeaveTypeRepository
from app.schemas.leave_balance import LeaveBalanceCreate, LeaveBalanceUpdate
from app.utils.exceptions import NotFoundError


class LeaveBalanceService:
    def __init__(self, repo: LeaveBalanceRepository, lt_repo: LeaveTypeRepository):
        self.repo = repo
        self.lt_repo = lt_repo

    async def get_by_id(self, id: int) -> LeaveBalance:
        lb = await self.repo.get_by_id(id)
        if not lb:
            raise NotFoundError("Leave balance not found", resource="leave_balance_id")
        return lb

    async def get_all(
        self,
        page: int = 1,
        per_page: int = 50,
        employee_id: int | None = None,
        year: int | None = None,
    ) -> tuple[list[LeaveBalance], int]:
        skip = (page - 1) * per_page
        return await self.repo.get_all(skip=skip, limit=per_page, employee_id=employee_id, year=year)

    async def create(self, payload: LeaveBalanceCreate) -> LeaveBalance:
        if not await self.lt_repo.get_by_id(payload.leave_type_id):
            raise NotFoundError("Leave type not found", resource="leave_type_id")
        lb = LeaveBalance(
            employee_id=payload.employee_id,
            leave_type_id=payload.leave_type_id,
            year=payload.year,
            balance_days=payload.balance_days,
            used_days=payload.used_days,
        )
        return await self.repo.create(lb)

    async def update(self, id: int, payload: LeaveBalanceUpdate) -> LeaveBalance:
        lb = await self.get_by_id(id)
        if payload.balance_days is not None:
            lb.balance_days = payload.balance_days
        if payload.used_days is not None:
            lb.used_days = payload.used_days
        return await self.repo.update(lb)

