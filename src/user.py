import streamlit as st
from utils.crud import select, update
from utils.security import hash_password
from datetime import datetime

@st.dialog("Editar meu perfil")
def edit_user(object):
    with st.form("edit_user_form"):
        new_first_name = st.text_input("Nome", object["first_name"])
        new_last_name = st.text_input("Sobrenome", object["last_name"])
        new_password = st.text_input("Senha", type="password", placeholder="Digite nova senha (opcional)")
        new_pct_essential_expenses = st.number_input("% Gastos essenciais", min_value=0.0, value=float(object["pct_essential_expenses"]), format="%.2f")
        new_pct_free_expenses = st.number_input("% Gastos livres", min_value=0.0, value=float(object["pct_free_expenses"]), format="%.2f")
        new_pct_investments = st.number_input("% Investimentos", min_value=0.0, value=float(object["pct_investments"]), format="%.2f")
        new_is_self_employed = st.checkbox("Trabalha autônomo?", value=object["is_self_employed"])

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("Salvar", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.rerun()

        if submitted:
            update_data = {
                "first_name": new_first_name,
                "last_name": new_last_name,
                "pct_essential_expenses": new_pct_essential_expenses,
                "pct_free_expenses": new_pct_free_expenses,
                "pct_investments": new_pct_investments,
                "is_self_employed": new_is_self_employed,
                "updated_at": datetime.now(),
            }

            if new_password:
                update_data["password"] = hash_password(new_password)

            result = update("users", update_data, where={"id": object["id"]})
            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

try:
    st.subheader("Meu perfil")

    query = f"""
        SELECT
            id,
            first_name,
            last_name,
            username,
            pct_essential_expenses,
            pct_free_expenses,
            pct_investments,
            is_self_employed,
            last_login,
            created_at,
            updated_at
        FROM public.users
        WHERE id = {st.session_state["user_id"]}
        LIMIT 1
    """
    df = select(query)

    user_data = df.iloc[0]

    st.dataframe(
        df.drop("id", axis=1),
        width="stretch",
        hide_index=True,
        column_config={
            "first_name": st.column_config.TextColumn("Nome"),
            "last_name": st.column_config.TextColumn("Sobrenome"),
            "username": st.column_config.TextColumn("Usuário"),
            "pct_essential_expenses": st.column_config.NumberColumn("% gastos essenciais", format="%.2f"),
            "pct_free_expenses": st.column_config.NumberColumn("% gastos livres", format="%.2f"),
            "pct_investments": st.column_config.NumberColumn("% investimentos", format="%.2f"),
            "is_self_employed": st.column_config.CheckboxColumn("Autônomo"),
            "last_login": st.column_config.DatetimeColumn("Último login"),
            "created_at": st.column_config.DatetimeColumn("Criado em"),
            "updated_at": st.column_config.DatetimeColumn("Atualizado em"),
        },
    )

    if st.button("Editar meu perfil", type="primary", use_container_width=True):
        edit_user(user_data.to_dict())

except Exception as e:
    st.error(f"Erro ao carregar página: {e}")