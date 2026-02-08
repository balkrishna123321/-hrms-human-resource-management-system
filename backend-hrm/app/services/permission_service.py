"""Permission service."""
from app.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository
from app.schemas.permission import PermissionCreate
from app.utils.exceptions import ConflictError, NotFoundError


class PermissionService:
    def __init__(self, repo: PermissionRepository):
        self.repo = repo

    async def get_by_id(self, id: int) -> Permission:
        p = await self.repo.get_by_id(id)
        if not p:
            raise NotFoundError("Permission not found", resource="permission_id")
        return p

    async def get_all(self) -> list[Permission]:
        return await self.repo.get_all()

    async def create(self, payload: PermissionCreate) -> Permission:
        if await self.repo.get_by_code(payload.code):
            raise ConflictError("Permission code already exists", field="code")
        perm = Permission(name=payload.name, code=payload.code, description=payload.description)
        return await self.repo.create(perm)
