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
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class UserSettings(Base):
    __tablename__ = "fixed_transactions"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("public.users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(5, 2), nullable=False)
    due_day = Column(SmallInteger, nullable=False)
    description = Column(String, nullable=False)
    type = Column(String, nullable=False)
    category = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())