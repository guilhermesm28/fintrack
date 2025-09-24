import streamlit as st
from utils.security import hash_password, verify_password
from utils.db import get_session
from models.users import Users
from sqlalchemy import select, func

class UserController:
    def __init__(self):
        self.session = get_session()

    def get_user_by_username(self, username):
        with self.session as session:
            stmt = select(Users).where(Users.username == username)
            return session.scalars(stmt).first()

    def update_last_login(self, username):
        with self.session as session:
            db_user = session.query(Users).filter_by(id=username.id).first()
            if db_user:
                db_user.last_login = func.now()
                session.commit()

    def list_users(self):
        with self.session as session:
            stmt = select(Users).order_by(Users.id)
            return session.scalars(stmt).all()

    def login(self, username: str, password: str) -> bool:
        user = self.get_user_by_username(username)
        if user and verify_password(password, user.password) and user.is_active:
            st.session_state.logged_in = True
            st.session_state.username = user.username
            st.session_state.fullname = f"{user.first_name} {user.last_name}"
            st.session_state.is_admin = user.is_admin
            st.session_state.user_id = user.id
            self.update_last_login(user)
            return True
        return False

    def create_user(self, first_name, last_name, username, password, is_admin=False):
        hashed_password = hash_password(password)
        with self.session as session:
            new_user = Users(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=hashed_password,
                is_admin=is_admin
            )
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user

    def update_user(self, user_id, first_name, last_name, username, password=None, is_admin=False, is_active=True):
        with self.session as session:
            db_user = session.query(Users).filter_by(id=user_id).first()
            if not db_user:
                return None

            db_user.first_name = first_name
            db_user.last_name = last_name
            db_user.username = username
            if password:
                db_user.password = hash_password(password)
            db_user.is_admin = is_admin
            db_user.is_active = is_active

            session.commit()
            session.refresh(db_user)
            return db_user

