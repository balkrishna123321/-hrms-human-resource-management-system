"""Auth API routes."""
from fastapi import APIRouter, Depends

from app.core.config import get_settings
from app.core.dependencies import get_auth_service, get_current_user
from app.schemas.auth import LoginRequest, TokenPair, UserResponse, RefreshRequest
from app.services.auth_service import AuthService
from app.models.user import User
from app.utils.responses import APIResponse

router = APIRouter()
settings = get_settings()


@router.post("/login", response_model=APIResponse[TokenPair])
async def login(
    payload: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Login with email/password; returns access and refresh tokens."""
    user, access, refresh = await service.login(payload)
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return APIResponse(
        message="Login successful",
        data=TokenPair(
            access_token=access,
            refresh_token=refresh,
            token_type="bearer",
            expires_in=expires_in,
        ),
    )


@router.post("/refresh", response_model=APIResponse[TokenPair])
async def refresh(
    payload: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
):
    """Get new access and refresh tokens using refresh token."""
    access, refresh = await service.refresh_tokens(payload.refresh_token)
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    return APIResponse(
        message="Tokens refreshed",
        data=TokenPair(
            access_token=access,
            refresh_token=refresh,
            token_type="bearer",
            expires_in=expires_in,
        ),
    )


@router.get("/me", response_model=APIResponse[UserResponse])
async def me(current_user: User = Depends(get_current_user)):
    """Return current authenticated user."""
    return APIResponse(
        data=UserResponse(
            id=current_user.id,
            email=current_user.email,
            full_name=current_user.full_name,
            is_active=current_user.is_active,
        ),
    )
