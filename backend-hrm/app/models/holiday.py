"""Holiday model for calendar."""
from datetime import date

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Holiday(Base):
    """Holiday table - company holidays."""

    __tablename__ = "holidays"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)  # null = applies every year
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def __repr__(self) -> str:
        return f"<Holiday(name={self.name}, date={self.date})>"
