import streamlit as st
from utils.security import hash_password
from repositories import user_repository
from utils.security import verify_password
from repositories.user_repository import get_user_by_username, update_last_login

def login(username: str, password: str) -> bool:
    user = get_user_by_username(username)
    if user and verify_password(password, user.password):
        st.session_state.logged_in = True
        st.session_state.username = user.username
        st.session_state.is_admin = user.is_admin
        update_last_login(user)
        return True
    return False

def is_admin(username: str) -> bool:
    user = get_user_by_username(username)
    return user.is_admin if user else False

def create_user(first_name: str, last_name: str, username: str, password: str, is_admin: bool = False):
    hashed_password = hash_password(password)
    return user_repository.create_user(first_name, last_name, username, hashed_password, is_admin)

def list_users():
    return user_repository.list_users()
