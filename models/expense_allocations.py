from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship
from utils.db import Base

class ExpenseAllocations(Base):
    __tablename__ = "expense_allocations"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    income_id = Column(BigInteger, ForeignKey("public.incomes.id", ondelete="CASCADE"), nullable=False)
    expense_id = Column(BigInteger, ForeignKey("public.expense.id", ondelete="CASCADE"), nullable=False)
    allocated_amount = Column(Numeric(5, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    expenses = relationship("Expenses", back_populates="expense_allocations")
    incomes = relationship("Incomes", back_populates="expense_allocations")