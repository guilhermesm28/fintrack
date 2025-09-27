from sqlalchemy import (
    Column,
    BigInteger,
    SmallInteger,
    String,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import relationship
from utils.db import Base

class Expenses(Base):
    __tablename__ = "expenses"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    category_id = Column(BigInteger, ForeignKey("public.categories.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(5, 2), nullable=False)
    due_day = Column(SmallInteger, nullable=False)
    description = Column(String, nullable=False)
    description_detail = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    category = relationship("Categories", back_populates="expenses")
    expense_allocations = relationship("ExpenseAllocations", back_populates="expenses")