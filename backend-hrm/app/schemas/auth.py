"""Auth schemas."""
import re

from pydantic import BaseModel, EmailStr, Field, field_validator


def _is_local_email(value: str) -> bool:
    """Accept *@*.local (e.g. admin@hrms.local) for dev/default admin."""
    if not value or "@" not in value:
        return False
    part_after_at = value.split("@", 1)[1].strip()
    return bool(part_after_at and part_after_at.endswith(".local") and re.match(r"^[^@]+@[^@\s]+\.local$", value.strip()))


class LoginRequest(BaseModel):
    """Login request."""

    email: str
    password: str = Field(..., min_length=6)

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not isinstance(v, str):
            raise ValueError("Email must be a string")
        s = v.strip().lower()
        if _is_local_email(s):
            return s
        # Standard email validation
        from email_validator import validate_email, EmailNotValidError
        try:
            result = validate_email(s)
            return result.email
        except EmailNotValidError as e:
            raise ValueError(str(e))


class TokenPair(BaseModel):
    """Access and refresh token pair."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RefreshRequest(BaseModel):
    """Refresh token request."""

    refresh_token: str


class UserResponse(BaseModel):
    """Current user response."""

    id: int
    email: str
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    """Change password request."""

    current_password: str
    new_password: str = Field(..., min_length=6)
