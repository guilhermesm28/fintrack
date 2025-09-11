import streamlit as st
from views import admin, login, planejamento

st.set_page_config(
    page_title="FINTRACK",
    page_icon="💲",
)

if not st.session_state.get("logged_in"):
    login.render()

else:
    username = st.session_state.get("fullname")
    pages = {
        "Planejamento": planejamento,
    }

    if st.session_state.get("is_admin", False):
        pages = {"Administração": admin, **pages}

    st.title("📊 FINTRACK - Controle financeiro")
    tabs = st.tabs(list(pages.keys()))

    for i, (name, page) in enumerate(pages.items()):
        with tabs[i]:
            page.render()

    if st.button("🚪 Sair"):
        st.session_state.clear()
        st.rerun()