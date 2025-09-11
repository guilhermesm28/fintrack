import streamlit as st
from services.security import verify_password
from repositories.user import get_user_by_username, update_last_login

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
