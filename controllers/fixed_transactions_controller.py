from sqlalchemy import select
from utils.database_util import get_session
from models.fixed_transactions_model import FixedTransactions

class FixedTransactionsController:
    def __init__(self):
        self.session = get_session()

    def get_fixed_transaction_by_id(self, id):
        with self.session as session:
            stmt = select(FixedTransactions).where(FixedTransactions.id == id)
            return session.scalars(stmt).first()

    def create_fixed_transaction(self, user_id, amount, due_day, description, type, category):
        with self.session as session:
            new_fixed_transaction = FixedTransactions(
                user_id=user_id,
                amount=amount,
                due_day=due_day,
                description=description,
                type=type,
                category=category
            )
            session.add(new_fixed_transaction)
            session.commit()
            session.refresh(new_fixed_transaction)
            return new_fixed_transaction

    def list_fixed_transactions(self, user_id):
        with self.session as session:
            stmt = select(FixedTransactions).where(FixedTransactions.user_id == user_id).order_by(FixedTransactions.id)
            return session.scalars(stmt).all()

    def update_fixed_transaction(self, id, amount, due_day, description, type, category):
        with self.session as session:
            db_fixed_transaction = session.query(FixedTransactions).filter_by(id=id).first()
            if not db_fixed_transaction:
                return None

            db_fixed_transaction.amount = amount
            db_fixed_transaction.due_day = due_day
            db_fixed_transaction.description = description
            db_fixed_transaction.type = type
            db_fixed_transaction.category = category

            session.commit()
            session.refresh(db_fixed_transaction)
            return db_fixed_transaction