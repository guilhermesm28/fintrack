import streamlit as st
from controllers.users import UserController

user_controller = UserController()

def render():
    st.set_page_config(layout="centered")
    st.title("Login")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "login_submitted" not in st.session_state:
        st.session_state.login_submitted = False

    if st.session_state.login_submitted:
        st.info("Verificando login...")
        return

    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        submit = st.form_submit_button("Entrar", type="primary", use_container_width=True)

    if submit:
        st.session_state.login_submitted = True

        if user_controller.login(username, password):
            st.session_state.logged_in = True
            st.toast("✅ Login realizado com sucesso!")
            st.rerun()
        else:
            st.session_state.login_submitted = False
            st.toast("❌ Usuário e/ou senha incorreto(s) | Usuário inativo.")