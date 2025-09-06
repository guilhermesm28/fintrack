import streamlit as st
from sqlalchemy import text
import bcrypt
from db import get_engine
from time import sleep

def create_user(username: str, password: str):
    ''' Criar um novo usuário '''
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO users (username, password) VALUES (:u, :p)"),
            {"u": username, "p": hashed}
        )

@st.dialog("Login")
def login(user: str, pwd: str):
    ''' Fazer login '''
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT password FROM users WHERE username = :u"), {"u": user}
        ).fetchone()
        if result and bcrypt.checkpw(pwd.encode(), result[0].encode()):
            st.success("Logado com sucesso!")
            st.session_state.logged_in = True
            st.session_state.username = user
            sleep(1)
            st.rerun()
        else:
            st.error("Usuário ou senha incorretos.")
