import streamlit as st
from controllers.user_controller import login

def render():
    st.set_page_config(layout="centered")
    st.title("🔐 Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar", type="primary", use_container_width=True):
        if login(username, password):
            st.success("Logado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário e/ou senha incorretos.")
