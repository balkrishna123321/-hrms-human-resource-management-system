"""Department business logic."""
from app.models.department import Department
from app.repositories.department_repository import DepartmentRepository
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.utils.exceptions import ConflictError, NotFoundError


class DepartmentService:
    """Department use cases."""

    def __init__(self, repo: DepartmentRepository):
        self.repo = repo

    async def get_by_id(self, id: int) -> Department:
        """Get department or raise NotFound."""
        department = await self.repo.get_by_id(id)
        if not department:
            raise NotFoundError("Department not found", resource="department_id")
        return department

    async def get_all(self, page: int = 1, per_page: int = 50) -> tuple[list[Department], int]:
        """Get paginated departments."""
        skip = (page - 1) * per_page
        return await self.repo.get_all(skip=skip, limit=per_page)

    async def create(self, payload: DepartmentCreate) -> Department:
        """Create department; enforce unique code."""
        if await self.repo.get_by_code(payload.code):
            raise ConflictError("Department code already exists", field="code")
        department = Department(
            name=payload.name,
            code=payload.code.strip().upper(),
            description=payload.description,
        )
        return await self.repo.create(department)

    async def update(self, id: int, payload: DepartmentUpdate) -> Department:
        """Update department."""
        department = await self.get_by_id(id)
        if payload.name is not None:
            department.name = payload.name
        if payload.code is not None:
            if await self.repo.get_by_code(payload.code) and (await self.repo.get_by_code(payload.code)).id != id:
                raise ConflictError("Department code already exists", field="code")
            department.code = payload.code.strip().upper()
        if payload.description is not None:
            department.description = payload.description
        await self.repo.db.flush()
        await self.repo.db.refresh(department)
        return department

    async def delete(self, id: int) -> None:
        """Delete department."""
        department = await self.get_by_id(id)
        await self.repo.delete(department)
