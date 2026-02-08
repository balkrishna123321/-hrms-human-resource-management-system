"""Leave balance per employee per year."""
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class LeaveBalance(Base):
    """Leave balance table - balance per employee per leave type per year."""

    __tablename__ = "leave_balances"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employees.id", ondelete="CASCADE"), nullable=False)
    leave_type_id: Mapped[int] = mapped_column(ForeignKey("leave_types.id", ondelete="CASCADE"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    balance_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    used_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    employee: Mapped["Employee"] = relationship("Employee", back_populates="leave_balances")
    leave_type: Mapped["LeaveType"] = relationship("LeaveType", back_populates="leave_balances")

    def __repr__(self) -> str:
        return f"<LeaveBalance(employee_id={self.employee_id}, year={self.year})>"
