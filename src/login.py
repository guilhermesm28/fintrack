import streamlit as st
from utils.security import verify_password
from utils.crud import select, update
from datetime import datetime

def login(username: str, password: str) -> bool:
    safe_username = username.replace("'", "''")
    query = f"SELECT * FROM users WHERE username = '{safe_username}'"
    result = select(query)

    if result is None or result.empty:
        return False

    user = result.iloc[0].to_dict()

    if not user.get("is_active"):
        return False
    if not verify_password(password, user.get("password", "")):
        return False

    user_id = user.get("id")

    update_data = {"last_login": datetime.now()}
    update("users", update_data, where={"id": user_id})

    st.session_state.logged_in = True
    st.session_state.user_id = user_id
    st.session_state.username = user["username"]
    st.session_state.fullname = f"{user['first_name']} {user['last_name']}"
    st.session_state.is_admin = user["is_admin"]

    return True

def render():
    st.set_page_config(layout="centered", page_title="Login")
    st.title("Login")

    st.session_state.setdefault("logged_in", False)

    if st.session_state.logged_in:
        st.success(f"Bem-vindo, {st.session_state.fullname}")
        st.stop()

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input("Usuário", placeholder="Digite seu usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        submitted = st.form_submit_button("Entrar", type="primary", use_container_width=True)

    if submitted:
        if login(username, password):
            st.toast("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário e/ou senha incorreto(s) ou usuário inativo.")