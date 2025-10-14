import streamlit as st
from views import login

st.set_page_config(
    page_title="FINTRACK",
    page_icon="💲",
)

if not st.session_state.get("logged_in"):
    login.render()
else:
    username = st.session_state.get("fullname")
    pages = [
        st.Page("views/home.py", title="Página inicial"),
        st.Page("views/transactions.py", title="Transações"),
        st.Page("views/planner.py", title="Planejamento financeiro"),
        st.Page("views/allocations.py", title="Alocação de saídas por entrada"),
    ]

    if st.session_state.get("is_admin", False):
        pages.insert(1, st.Page("views/admin.py", title="Administração"))

    menu = st.navigation(pages, position="top")
    menu.run()