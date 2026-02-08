"""Holiday schemas."""
from datetime import date as date_type

from pydantic import BaseModel, Field


class HolidayBase(BaseModel):
    """Base holiday schema."""

    name: str = Field(..., min_length=1, max_length=100)
    date: date_type
    year: int | None = Field(None, ge=2000, le=2100)
    description: str | None = Field(None, max_length=255)


class HolidayCreate(HolidayBase):
    """Create holiday request."""

    pass


class HolidayUpdate(BaseModel):
    """Update holiday (partial)."""

    name: str | None = Field(None, min_length=1, max_length=100)
    date: date_type | None = None
    year: int | None = Field(None, ge=2000, le=2100)
    description: str | None = None


class HolidayResponse(HolidayBase):
    """Holiday response."""

    id: int

    class Config:
        from_attributes = True
