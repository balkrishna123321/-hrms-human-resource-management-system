"""Role repository."""
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.models.role import Role


class RoleRepository:
    """Role data access."""

    def __init__(self, db):
        self.db = db

    async def get_by_id(self, id: int) -> Role | None:
        result = await self.db.execute(
            select(Role).where(Role.id == id).options(selectinload(Role.permissions))
        )
        return result.scalar_one_or_none()

    async def get_by_code(self, code: str) -> Role | None:
        result = await self.db.execute(
            select(Role).where(Role.code == code).options(selectinload(Role.permissions))
        )
        return result.scalar_one_or_none()

    async def get_all(self, *, skip: int = 0, limit: int = 100) -> tuple[list[Role], int]:
        count_q = select(func.count()).select_from(Role)
        total = (await self.db.execute(count_q)).scalar() or 0
        q = select(Role).options(selectinload(Role.permissions)).order_by(Role.code).offset(skip).limit(limit)
        result = await self.db.execute(q)
        return list(result.scalars().all()), total

    async def create(self, role: Role) -> Role:
        self.db.add(role)
        await self.db.flush()
        await self.db.refresh(role)
        return role

    async def delete(self, role: Role) -> None:
        await self.db.delete(role)
