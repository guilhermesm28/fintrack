from utils.database_util import get_session
from models.user_finance_model import UserFinances
from sqlalchemy import select, func

class UserFinanceController:
    def __init__(self):
        self.session = get_session()

    def create_user_finance(self, user_id, total_income, pct_fixed_expenses, pct_free_expenses, pct_investments, is_self_employed=False):
        with self.session as session:
            new_user_finance = UserFinances(
                user_id=user_id,
                total_income=total_income,
                pct_fixed_expenses=pct_fixed_expenses,
                pct_free_expenses=pct_free_expenses,
                pct_investments=pct_investments,
                is_self_employed=is_self_employed,
            )
            session.add(new_user_finance)
            session.commit()
            session.refresh(new_user_finance)
            return new_user_finance
