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
    pages = {
        "Planejamento financeiro" : [
            st.Page("views/planner_view.py", title="Planejamento financeiro"),
        ]
    }

    if st.session_state.get("is_admin", False):
        pages = {
            "Administração" : [
                st.Page("views/admin_view.py", title="Administração"),
            ],
        **pages}

    with st.container():
        cols = st.columns([0.8, 0.2])
        cols[0].markdown(f"### Bem-vindo, {username}!")
        if cols[1].button("Logout"):
            st.session_state.clear()
            st.rerun()

    menu = st.navigation(pages, position="top")

    menu.run()