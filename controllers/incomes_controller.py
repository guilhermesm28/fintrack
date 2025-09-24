from sqlalchemy.orm import selectinload
from sqlalchemy import select, func
from utils.database_util import get_session
from models.incomes_model import Incomes

class IncomesController:
    def __init__(self):
        self.session = get_session()

    def get_income_by_id(self, id):
        with self.session as session:
            stmt = select(Incomes).where(Incomes.id == id)
            return session.scalars(stmt).first()

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

    def list_incomes(self, user_id):
        with self.session as session:
            stmt = select(Incomes).where(Incomes.user_id == user_id).options(selectinload(Incomes.category)).order_by(Incomes.id)
            return session.scalars(stmt).all()

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

    def get_total_incomes(self, user_id):
        with self.session as session:
            stmt = select(func.sum(Incomes.amount)) \
                .where(Incomes.user_id == user_id) \
                .where(Incomes.is_active == True)
            result = session.scalars(stmt).first()
            return result if result else 0