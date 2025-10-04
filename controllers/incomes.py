from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from utils.db import get_session
from models.incomes import Incomes
from models.expense_allocations import ExpenseAllocations

class IncomesController:
    def __init__(self):
        self.session = get_session()

    def create_income(self, user_id, category_id, amount, due_day, description, description_detail):
        with self.session as session:
            new_income = Incomes(
                user_id=user_id,
                category_id=category_id,
                amount=amount,
                due_day=due_day,
                description=description,
                description_detail=description_detail
            )
            session.add(new_income)
            session.commit()
            session.refresh(new_income)
            return new_income

    def update_income(self, id, category_id, amount, due_day, description, description_detail, is_active=True):
        with self.session as session:
            db_income = session.query(Incomes).filter_by(id=id).first()
            if not db_income:
                return None

            db_income.category_id = category_id
            db_income.amount = amount
            db_income.due_day = due_day
            db_income.description = description
            db_income.description_detail = description_detail
            db_income.is_active = is_active

            session.commit()
            session.refresh(db_income)
            return db_income

    def list_incomes(self, user_id):
        with self.session as session:
            stmt = select(Incomes).where(Incomes.user_id == user_id).options(selectinload(Incomes.category)).order_by(Incomes.id)
            return session.scalars(stmt).all()

    def get_income_by_id(self, id):
        with self.session as session:
            stmt = select(Incomes).where(Incomes.id == id)
            return session.scalars(stmt).first()

    def get_total_incomes(self, user_id):
        with self.session as session:
            stmt = select(func.sum(Incomes.amount)) \
                .where(Incomes.user_id == user_id) \
                .where(Incomes.is_active == True)
            result = session.scalars(stmt).first()
            return result if result else 0

    def get_unallocated_incomes(self, user_id):
        with self.session as session:
            stmt = (
                select(
                    Incomes.id,
                    Incomes.description,
                    Incomes.amount,
                    func.coalesce(func.sum(ExpenseAllocations.allocated_amount), 0).label("allocated"),
                    (Incomes.amount - func.coalesce(func.sum(ExpenseAllocations.allocated_amount), 0)).label("saldo")
                )
                .outerjoin(ExpenseAllocations, Incomes.id == ExpenseAllocations.income_id)
                .where(Incomes.user_id == user_id)
                .where(Incomes.is_active == True)
                .group_by(Incomes.id, Incomes.description, Incomes.amount)
                .having((Incomes.amount - func.coalesce(func.sum(ExpenseAllocations.allocated_amount), 0)) > 0)
            )

            result = session.execute(stmt).all()
            return result

    def get_expense_allocations_by_income_id(self, income_id):
        with self.session as session:
            stmt = select(ExpenseAllocations) \
                .where(ExpenseAllocations.income_id == income_id) \
                .options(selectinload(ExpenseAllocations.incomes)) \
                .options(selectinload(ExpenseAllocations.expenses)) \
                .order_by(-ExpenseAllocations.allocated_amount)

            return session.scalars(stmt).all()