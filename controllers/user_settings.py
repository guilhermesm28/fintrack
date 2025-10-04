from utils.db import get_session
from sqlalchemy import select
from models.user_settings import UserSettings


class UserSettingsController:
    def __init__(self):
        self.session = get_session()

    def get_user_settings_by_id(self, id):
        with self.session as session:
            stmt = select(UserSettings).where(UserSettings.id == id)
            return session.scalars(stmt).first()

    def get_user_settings_by_user_id(self, user_id):
        with self.session as session:
            stmt = select(UserSettings).where(UserSettings.user_id == user_id)
            return session.scalars(stmt).first()

    def validate_percentages(self, pct_essential_expenses, pct_free_expenses, pct_investments):
        total_percentage = pct_essential_expenses + pct_free_expenses + pct_investments
        if total_percentage > 100 or total_percentage < 100:
            return False
        return True

    def create_user_settings(self, user_id, pct_essential_expenses, pct_free_expenses, pct_investments, is_self_employed=False):
        with self.session as session:
            new_user_settings = UserSettings(
                user_id=user_id,
                pct_essential_expenses=pct_essential_expenses,
                pct_free_expenses=pct_free_expenses,
                pct_investments=pct_investments,
                is_self_employed=is_self_employed,
            )
            session.add(new_user_settings)
            session.commit()
            session.refresh(new_user_settings)
            return new_user_settings

    def list_user_settings(self, user_id):
        with self.session as session:
            stmt = select(UserSettings).where(UserSettings.user_id == user_id)
            return session.scalars(stmt).all()

    def update_user_settings(self, id, pct_essential_expenses, pct_free_expenses, pct_investments, is_self_employed=False, is_active=True):
        with self.session as session:
            db_user_settings = session.query(UserSettings).filter_by(id=id).first()
            if not db_user_settings:
                return None

            db_user_settings.pct_essential_expenses = pct_essential_expenses
            db_user_settings.pct_free_expenses = pct_free_expenses
            db_user_settings.pct_investments = pct_investments
            db_user_settings.is_self_employed = is_self_employed
            db_user_settings.is_active = is_active

            session.commit()
            session.refresh(db_user_settings)
            return db_user_settings
