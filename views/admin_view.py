from datetime import timedelta
import streamlit as st
from controllers.user_controller import UserController
from time import sleep

user_controller = UserController()

st.set_page_config(layout="wide")
st.title("Painel de Administração")

tabs = st.tabs(["Listar usuários", "Atualizar usuário", "Criar usuário"])

with tabs[0]:
    users = user_controller.list_users()
    st.dataframe(
        [{
            "ID": u.id,
            "Nome completo": f"{u.first_name} {u.last_name}",
            "Usuário": u.username,
            "Administrador": u.is_admin,
            "Ativo": u.is_active,
            "Último login": u.last_login - timedelta(hours=3) if u.last_login else None,
            "Criado em": u.created_at - timedelta(hours=3) if u.created_at else None,
            "Atualizado em": u.updated_at - timedelta(hours=3) if u.updated_at else None
        } for u in users],
        hide_index=True
    )

with tabs[1]:
    with st.container(border=True):
        col1, col2 = st.columns([4,1], vertical_alignment="bottom")

        with col1:
            username = st.text_input("Usuário")
        with col2:
            search_btn = st.button("Pesquisar", type="primary", use_container_width=True)

    if search_btn:
        user = user_controller.get_user_by_username(username)
        if user:
            st.session_state["user_to_edit"] = user
        else:
            st.toast("Usuário não encontrado", icon="❌")

    if "user_to_edit" in st.session_state:
        user = st.session_state["user_to_edit"]

        with st.form("atualizar_usuario", clear_on_submit=True):
            col1, col2, col3, col4 = st.columns(4)

            new_first_name = col1.text_input("Primeiro nome", user.first_name)
            new_last_name = col2.text_input("Sobrenome", user.last_name)
            new_username = col3.text_input("Usuário", user.username)
            new_password = col4.text_input("Senha", type="password", placeholder="Digite nova senha (opcional)")
            new_is_admin = st.checkbox("Administrador?", value=user.is_admin)
            new_is_active = st.checkbox("Ativo?", value=user.is_active)

            submit = st.form_submit_button("Atualizar usuário", type="primary", use_container_width=True)

            if submit:
                try:
                    user_controller.update_user(
                        user.id,
                        new_first_name,
                        new_last_name,
                        new_username,
                        new_password if new_password else None,
                        new_is_admin,
                        new_is_active
                    )
                    st.toast(f"Usuário {new_username} atualizado com sucesso!", icon="✅")
                    sleep(1)
                    st.session_state.pop("user_to_edit", None)
                    st.rerun()
                except Exception as e:
                    st.toast(f"Erro ao atualizar usuário: {str(e)}", icon="❌")

with tabs[2]:
    with st.form("criar_usuario", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)

        first_name = col1.text_input("Primeiro nome")
        last_name = col2.text_input("Sobrenome")
        username = col3.text_input("Usuário")
        password = col4.text_input("Senha", type="password")
        is_admin = st.checkbox("Administrador?", value=False)

        submit = st.form_submit_button("Criar usuário", type="primary", use_container_width=True)

        if submit:
            try:
                user_controller.create_user(first_name, last_name, username, password, is_admin)
                st.toast(f"Usuário {username} criado com sucesso!", icon="✅")
                sleep(1)
                st.rerun()
            except Exception as e:
                st.toast(f"Erro ao criar usuário: {str(e)}", icon="❌")