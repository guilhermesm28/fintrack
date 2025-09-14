from datetime import timedelta
import streamlit as st
from controllers import user_controller

def render():
    st.set_page_config(layout="wide")
    st.title("⚙️ Painel de Administração")

    st.subheader("👤 Criar novo usuário")
    with st.form("criar_usuario"):
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Primeiro nome")
            last_name = st.text_input("Sobrenome")
        with col2:
            username = st.text_input("Novo usuário")
            password = st.text_input("Senha", type="password")
        is_admin = st.checkbox("Administrador?")
        submit = st.form_submit_button("Criar usuário")
        if submit:
            if first_name and last_name and username and password:
                user_controller.create_user(first_name, last_name, username, password, is_admin)
                st.success(f"Usuário {username} criado com sucesso!")
                st.rerun()
            else:
                st.error("Preencha todos os campos.")

    st.subheader("📋 Usuários cadastrados")
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
