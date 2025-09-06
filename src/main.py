import streamlit as st
from auth import login

st.set_page_config(
    page_title="FINTRACK",
    page_icon="💲",
    layout="centered",
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("login"):
        st.title("Login")
        st.caption("Please enter your username and password to log in.")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submit_btn = st.form_submit_button("Submit", type="primary", use_container_width=True)

        if submit_btn:
            login(user, pwd)

else:
    st.sidebar.success(f"Bem-vindo(a), {st.session_state.username}!")
    if st.sidebar.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🏠 Página inicial")
    st.write("Use o menu lateral para navegar.")