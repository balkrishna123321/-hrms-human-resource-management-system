"""Attendance model."""
from datetime import date, time
from decimal import Decimal
from enum import Enum as PyEnum

from sqlalchemy import Date, Enum, ForeignKey, Numeric, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AttendanceStatus(str, PyEnum):
    """Attendance status enum."""

    PRESENT = "present"
    ABSENT = "absent"
    HALF_DAY = "half_day"
    ON_LEAVE = "on_leave"
    WFH = "wfh"  # work from home


class AttendanceSource(str, PyEnum):
    """How attendance was recorded."""

    WEB = "web"
    MANUAL = "manual"
    BIOMETRIC = "biometric"
    API = "api"


class Attendance(Base):
    """Attendance table."""

    __tablename__ = "attendance"
    __table_args__ = (UniqueConstraint("employee_id", "date", name="uq_employee_date"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[AttendanceStatus] = mapped_column(
        Enum(AttendanceStatus),
        nullable=False,
        default=AttendanceStatus.PRESENT,
    )
    check_in_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    check_out_time: Mapped[time | None] = mapped_column(Time, nullable=True)
    work_hours: Mapped[Decimal | None] = mapped_column(Numeric(4, 2), nullable=True)
    source: Mapped[AttendanceSource | None] = mapped_column(
        Enum(AttendanceSource),
        nullable=True,
        default=AttendanceSource.WEB,
    )
    notes: Mapped[str | None] = mapped_column(nullable=True)

    employee: Mapped["Employee"] = relationship("Employee", back_populates="attendance_records")

    def __repr__(self) -> str:
        return f"<Attendance(employee_id={self.employee_id}, date={self.date}, status={self.status})>"
