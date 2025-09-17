from sqlalchemy import (
    Column,
    BigInteger,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserFinances(Base):
    __tablename__ = "user_finances"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    total_income = Column(Numeric(12, 2), nullable=False, default=0)
    pct_fixed_expenses = Column(Numeric(5, 2), nullable=False, default=0)
    pct_free_expenses = Column(Numeric(5, 2), nullable=False, default=0)
    pct_investments = Column(Numeric(5, 2), nullable=False, default=0)
    is_self_employed = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())
