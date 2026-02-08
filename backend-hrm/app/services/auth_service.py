"""Auth business logic."""
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.config import get_settings
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest
from app.utils.exceptions import UnauthorizedError

settings = get_settings()


class AuthService:
    """Auth use cases."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, payload: LoginRequest) -> tuple[User, str, str]:
        """Validate credentials and return user + access_token + refresh_token."""
        user = await self.user_repo.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.hashed_password):
            raise UnauthorizedError("Invalid email or password")
        if not user.is_active:
            raise UnauthorizedError("Account is disabled")
        access = create_access_token(str(user.id))
        refresh = create_refresh_token(str(user.id))
        return user, access, refresh

    async def refresh_tokens(self, refresh_token: str) -> tuple[str, str]:
        """Validate refresh token and return new access + refresh."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise UnauthorizedError("Invalid or expired refresh token")
        user_id = payload.get("sub")
        user = await self.user_repo.get_by_id(int(user_id))
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")
        access = create_access_token(str(user.id))
        refresh = create_refresh_token(str(user.id))
        return access, refresh

    async def get_current_user(self, user_id: int) -> User:
        """Get user by id or raise."""
        user = await self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedError("User not found or inactive")
        return user
