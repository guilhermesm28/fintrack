from sqlalchemy import select
from utils.database_util import get_session
from models.categories_model import Categories

class CategoriesController:
    def __init__(self):
        self.session = get_session()

    def get_categories_by_id(self, id):
        with self.session as session:
            stmt = select(Categories).where(Categories.id == id)
            return session.scalars(stmt).first()

    def get_categories_by_type(self, is_expense):
        with self.session as session:
            stmt = select(Categories).where(Categories.is_expense == is_expense)
            return session.scalars(stmt).all()

    def create_category(self, name, is_expense):
        with self.session as session:
            new_category = Categories(
                name=name,
                is_expense=is_expense
            )
            session.add(new_category)
            session.commit()
            session.refresh(new_category)
            return new_category

    def list_categories(self):
        with self.session as session:
            stmt = select(Categories).order_by(Categories.id)
            return session.scalars(stmt).all()

    def update_category(self, id, name, is_expense=True, is_active=True):
        with self.session as session:
            db_category = session.query(Categories).filter_by(id=id).first()
            if not db_category:
                return None

            db_category.name = name
            db_category.is_expense = is_expense
            db_category.is_active = is_active

            session.commit()
            session.refresh(db_category)
            return db_category