from sqlalchemy import select, func
from models.user_model import User
from utils.database_util import get_session

def create_user(first_name, last_name, username, password_hash, is_admin=False):
    session = get_session()
    try:
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password_hash,
            is_admin=is_admin
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except:
        session.rollback()
        raise
    finally:
        session.close()

def get_user_by_username(username):
    session = get_session()
    try:
        stmt = select(User).where(User.username == username)
        return session.scalars(stmt).first()
    finally:
        session.close()

def update_last_login(username):
    session = get_session()
    try:
        db_user = session.query(User).filter_by(id=username.id).first()
        if db_user:
            db_user.last_login = func.now()
            session.commit()
    finally:
        session.close()

def list_users():
    session = get_session()
    try:
        stmt = select(User).order_by(User.id)
        return session.scalars(stmt).all()
    finally:
        session.close()
