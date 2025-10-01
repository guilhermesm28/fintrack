from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from utils.db import get_session
from models.expenses import Expenses
from models.expense_allocations import ExpenseAllocations
from models.categories import Categories

class ExpensesController:
    def __init__(self):
        self.session = get_session()

    def get_expense_by_id(self, id):
        with self.session as session:
            stmt = select(Expenses).where(Expenses.id == id)
            return session.scalars(stmt).first()

    def create_expense(self, user_id, category_id, amount, due_day, description, description_detail):
        with self.session as session:
            new_expense = Expenses(
                user_id=user_id,
                category_id=category_id,
                amount=amount,
                due_day=due_day,
                description=description,
                description_detail=description_detail
            )
            session.add(new_expense)
            session.commit()
            session.refresh(new_expense)
            return new_expense

    def list_expenses(self, user_id):
        with self.session as session:
            stmt = select(Expenses).where(Expenses.user_id == user_id).options(selectinload(Expenses.category)).order_by(Expenses.id)
            return session.scalars(stmt).all()

    def update_expense(self, id, category_id, amount, due_day, description, description_detail, is_active=True):
        with self.session as session:
            db_expense = session.query(Expenses).filter_by(id=id).first()
            if not db_expense:
                return None

            db_expense.category_id = category_id
            db_expense.amount = amount
            db_expense.due_day = due_day
            db_expense.description = description
            db_expense.description_detail = description_detail
            db_expense.is_active = is_active

            session.commit()
            session.refresh(db_expense)
            return db_expense

    def get_total_fixed_expenses(self, user_id):
        with self.session as session:
            stmt = select(func.sum(Expenses.amount)) \
                .where(Expenses.user_id == user_id) \
                .where(Expenses.is_fixed_expense == True) \
                .where(Expenses.is_active == True)
            result = session.scalars(stmt).first()
            return result if result else 0

    def get_total_investments(self, user_id):
        with self.session as session:
            stmt = select(func.sum(Expenses.amount)) \
                .join(Categories, Expenses.category_id == Categories.id and Categories.is_active == True and Categories.is_expense == True) \
                .where(Categories.name == "Investimentos") \
                .where(Expenses.user_id == user_id) \
                .where(Expenses.is_fixed_expense == False) \
                .where(Expenses.is_active == True)
            result = session.scalars(stmt).first()
            return result if result else 0

    def get_total_free_expenses(self, user_id):
        with self.session as session:
            stmt = select(func.sum(Expenses.amount)) \
                .join(Categories, Expenses.category_id == Categories.id and Categories.is_active == True and Categories.is_expense == True) \
                .where(Categories.name == "Gastos livres") \
                .where(Expenses.user_id == user_id) \
                .where(Expenses.is_fixed_expense == False) \
                .where(Expenses.is_active == True)
            result = session.scalars(stmt).first()
            return result if result else 0

    def get_unallocated_expenses(self, user_id):
        with self.session as session:
            stmt = (
                select(
                    Expenses.id,
                    Expenses.description,
                    Expenses.amount,
                    func.coalesce(func.sum(ExpenseAllocations.allocated_amount), 0).label("allocated"),
                    (Expenses.amount - func.coalesce(func.sum(ExpenseAllocations.allocated_amount), 0)).label("saldo")
                )
                .outerjoin(ExpenseAllocations, Expenses.id == ExpenseAllocations.expense_id)
                .where(Expenses.user_id == user_id)
                .where(Expenses.is_active == True)
                .group_by(Expenses.id, Expenses.description, Expenses.amount)
                .having((Expenses.amount - func.coalesce(func.sum(ExpenseAllocations.allocated_amount), 0)) > 0)
            )

            result = session.execute(stmt).all()
            return result