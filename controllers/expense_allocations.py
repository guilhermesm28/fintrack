from sqlalchemy.orm import selectinload
from sqlalchemy import select
from utils.db import get_session
from models.expense_allocations import ExpenseAllocations

class ExpenseAllocationsController:
    def __init__(self):
        self.session = get_session()

    def get_expense_allocation_by_id(self, id):
        with self.session as session:
            stmt = select(ExpenseAllocations).where(ExpenseAllocations.id == id)
            return session.scalars(stmt).first()

    def create_expense_allocation(self, user_id, income_id, expense_id, allocated_amount):
        with self.session as session:
            new_expense_allocation = ExpenseAllocations(
                user_id=user_id,
                income_id=income_id,
                expense_id=expense_id,
                allocated_amount=allocated_amount
            )
            session.add(new_expense_allocation)
            session.commit()
            session.refresh(new_expense_allocation)
            return new_expense_allocation

    def list_expense_allocations(self, user_id):
        with self.session as session:
            stmt = select(ExpenseAllocations) \
                .where(ExpenseAllocations.user_id == user_id) \
                .options(selectinload(ExpenseAllocations.incomes)) \
                .options(selectinload(ExpenseAllocations.expenses)) \
                .order_by(ExpenseAllocations.id)

            return session.scalars(stmt).all()

    def update_expense_allocation(self, id, income_id, expense_id, allocated_amount, is_active=True):
        with self.session as session:
            db_expense_allocation = session.query(ExpenseAllocations).filter_by(id=id).first()
            if not db_expense_allocation:
                return None

            db_expense_allocation.income_id = income_id
            db_expense_allocation.expense_id = expense_id
            db_expense_allocation.allocated_amount = allocated_amount
            db_expense_allocation.is_active = is_active

            session.commit()
            session.refresh(db_expense_allocation)
            return db_expense_allocation