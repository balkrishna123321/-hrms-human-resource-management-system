"""Leave request model."""
from datetime import date
from enum import Enum as PyEnum

from sqlalchemy import Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class LeaveRequestStatus(str, PyEnum):
    """Leave request status."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"


class LeaveRequest(Base):
    """Leave request table."""

    __tablename__ = "leave_requests"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    leave_type_id: Mapped[int] = mapped_column(ForeignKey("leave_types.id", ondelete="CASCADE"), nullable=False)
    from_date: Mapped[date] = mapped_column(Date, nullable=False)
    to_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[LeaveRequestStatus] = mapped_column(
        Enum(LeaveRequestStatus),
        default=LeaveRequestStatus.PENDING,
        nullable=False,
    )
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    approved_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    employee: Mapped["Employee"] = relationship("Employee", back_populates="leave_requests")
    leave_type: Mapped["LeaveType"] = relationship("LeaveType", back_populates="leave_requests")

    def __repr__(self) -> str:
        return f"<LeaveRequest(employee_id={self.employee_id}, {self.from_date} to {self.to_date})>"
