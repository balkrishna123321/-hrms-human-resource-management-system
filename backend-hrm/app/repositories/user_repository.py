"""User repository."""
from sqlalchemy import select

from app.models.user import User


class UserRepository:
    """User data access."""

    def __init__(self, db):
        self.db = db

    async def get_by_id(self, id: int) -> User | None:
        """Get user by id."""
        result = await self.db.execute(select(User).where(User.id == id))
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Persist new user."""
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user
