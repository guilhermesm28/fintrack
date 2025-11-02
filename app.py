import streamlit as st
from src import login

st.set_page_config(
    page_title="FINTRACK",
    page_icon="💲",
    layout="wide"
)

if not st.session_state.get("logged_in"):
    login.render()
else:
    username = st.session_state.get("fullname")
    pages = [
        st.Page("src/dashboard.py", title="Dashboard"),
        st.Page("src/transactions.py", title="Transações"),
    ]

    if st.session_state.get("is_admin", False):
        pages.insert(1, st.Page("src/admin.py", title="Administração"))
    else:
        pages.insert(1, st.Page("src/user.py", title="Meu perfil"))

    menu = st.navigation(pages, position="top")
    menu.run()