import streamlit as st
from controllers.users import UserController
from time import sleep

user_controller = UserController()

def render():
    st.set_page_config(layout="centered")
    st.title("Login")

    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar", type="primary", use_container_width=True)

    if submit:
        if user_controller.login(username, password):
            st.toast("Login realizado com sucesso!", icon="✅")
            sleep(1)
            st.rerun()
        else:
            st.toast("Usuário e/ou senha incorreto(s) | Usuário inativo.", icon="❌")
