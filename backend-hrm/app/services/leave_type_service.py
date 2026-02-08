"""Leave type service."""
from app.models.leave_type import LeaveType
from app.repositories.leave_type_repository import LeaveTypeRepository
from app.schemas.leave_type import LeaveTypeCreate, LeaveTypeUpdate
from app.utils.exceptions import ConflictError, NotFoundError


class LeaveTypeService:
    def __init__(self, repo: LeaveTypeRepository):
        self.repo = repo

    async def get_by_id(self, id: int) -> LeaveType:
        lt = await self.repo.get_by_id(id)
        if not lt:
            raise NotFoundError("Leave type not found", resource="leave_type_id")
        return lt

    async def get_all(self, page: int = 1, per_page: int = 50) -> tuple[list[LeaveType], int]:
        skip = (page - 1) * per_page
        return await self.repo.get_all(skip=skip, limit=per_page)

    async def create(self, payload: LeaveTypeCreate) -> LeaveType:
        if await self.repo.get_by_code(payload.code):
            raise ConflictError("Leave type code already exists", field="code")
        lt = LeaveType(
            name=payload.name,
            code=payload.code,
            default_days_per_year=payload.default_days_per_year,
            description=payload.description,
        )
        return await self.repo.create(lt)

    async def update(self, id: int, payload: LeaveTypeUpdate) -> LeaveType:
        lt = await self.get_by_id(id)
        if payload.name is not None:
            lt.name = payload.name
        if payload.code is not None:
            existing = await self.repo.get_by_code(payload.code)
            if existing and existing.id != id:
                raise ConflictError("Leave type code already exists", field="code")
            lt.code = payload.code
        if payload.default_days_per_year is not None:
            lt.default_days_per_year = payload.default_days_per_year
        if payload.description is not None:
            lt.description = payload.description
        await self.repo.db.flush()
        await self.repo.db.refresh(lt)
        return lt

    async def delete(self, id: int) -> None:
        lt = await self.get_by_id(id)
        await self.repo.delete(lt)
