from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Boolean,
    DateTime,
    func
)
from sqlalchemy.orm import relationship
from utils.db import Base

class Categories(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "public"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    is_expense = Column(Boolean, nullable=False, default=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now())

    expenses = relationship("Expenses", back_populates="category")
    incomes = relationship("Incomes", back_populates="category")