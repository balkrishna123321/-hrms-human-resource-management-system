"""Role service."""
from app.models.role import Role
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate
from app.utils.exceptions import ConflictError, NotFoundError


class RoleService:
    def __init__(self, role_repo: RoleRepository, perm_repo: PermissionRepository):
        self.role_repo = role_repo
        self.perm_repo = perm_repo

    async def get_by_id(self, id: int) -> Role:
        r = await self.role_repo.get_by_id(id)
        if not r:
            raise NotFoundError("Role not found", resource="role_id")
        return r

    async def get_all(self, page: int = 1, per_page: int = 50) -> tuple[list[Role], int]:
        skip = (page - 1) * per_page
        return await self.role_repo.get_all(skip=skip, limit=per_page)

    async def create(self, payload: RoleCreate) -> Role:
        if await self.role_repo.get_by_code(payload.code):
            raise ConflictError("Role code already exists", field="code")
        role = Role(name=payload.name, code=payload.code, description=payload.description)
        role = await self.role_repo.create(role)
        if payload.permission_ids:
            perms = await self.perm_repo.get_by_ids(payload.permission_ids)
            role.permissions = perms
            await self.role_repo.db.flush()
            await self.role_repo.db.refresh(role)
        return role

    async def update(self, id: int, payload: RoleUpdate) -> Role:
        role = await self.get_by_id(id)
        if payload.name is not None:
            role.name = payload.name
        if payload.code is not None:
            if await self.role_repo.get_by_code(payload.code) and (await self.role_repo.get_by_code(payload.code)).id != id:
                raise ConflictError("Role code already exists", field="code")
            role.code = payload.code
        if payload.description is not None:
            role.description = payload.description
        if payload.permission_ids is not None:
            perms = await self.perm_repo.get_by_ids(payload.permission_ids)
            role.permissions = perms
        await self.role_repo.db.flush()
        await self.role_repo.db.refresh(role)
        return role

    async def delete(self, id: int) -> None:
        role = await self.get_by_id(id)
        await self.role_repo.delete(role)
