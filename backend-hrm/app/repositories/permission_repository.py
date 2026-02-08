"""Permission repository."""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission


class PermissionRepository:
    """Permission data access."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, id: int) -> Permission | None:
        result = await self.db.execute(select(Permission).where(Permission.id == id))
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Permission | None:
        result = await self.db.execute(select(Permission).where(Permission.code == code))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Permission]:
        result = await self.db.execute(select(Permission).order_by(Permission.code))
        return list(result.scalars().all())

    async def get_by_ids(self, ids: list[int]) -> list[Permission]:
        if not ids:
            return []
        result = await self.db.execute(select(Permission).where(Permission.id.in_(ids)))
        return list(result.scalars().all())

    async def create(self, permission: Permission) -> Permission:
        self.db.add(permission)
        await self.db.flush()
        await self.db.refresh(permission)
        return permission
