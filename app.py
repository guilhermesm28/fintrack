import streamlit as st
from views import login_view

st.set_page_config(
    page_title="FINTRACK",
    page_icon="💲",
)

if not st.session_state.get("logged_in"):
    login_view.render()
else:
    username = st.session_state.get("fullname")
    pages = [
        st.Page("views/home_view.py", title="Página inicial"),
        st.Page("views/planner_view.py", title="Planejamento financeiro"),
    ]

    if st.session_state.get("is_admin", False):
        pages.insert(1, st.Page("views/admin_view.py", title="Administração"))

    menu = st.navigation(pages, position="top")
    menu.run()
