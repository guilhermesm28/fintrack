import streamlit as st
from time import sleep
from datetime import timedelta
from controllers.user_settings import UserSettingsController

user_settings_controller = UserSettingsController()

st.set_page_config(layout="wide")
st.title("Planejamento financeiro")

tabs = st.tabs(["Listar planejamentos", "Atualizar planejamento", "Criar planejamento"])

with tabs[0]:
    settings = user_settings_controller.list_user_settings(st.session_state["user_id"])
    st.dataframe(
        [{
            "ID": s.id,
            "% Gastos fixos": s.pct_fixed_expenses,
            "% Gastos livres": s.pct_free_expenses,
            "% Investimentos": s.pct_investments,
            "Trabalha autônomo?": s.is_self_employed,
            "Ativo": s.is_active,
            "Criado em": s.created_at - timedelta(hours=3) if s.created_at else None,
            "Atualizado em": s.updated_at - timedelta(hours=3) if s.updated_at else None
        } for s in settings],
        hide_index=True
    )

with tabs[1]:
    with st.container(border=True):
        col1, col2 = st.columns([4,1], vertical_alignment="bottom")

        with col1:
            user_settings_id = st.number_input("ID", min_value=1, value=None, placeholder="Digite o ID do planejamento")
        with col2:
            search_btn = st.button("Pesquisar", type="primary", use_container_width=True)

    if search_btn:
        user_settings = user_settings_controller.get_user_settings_by_id(user_settings_id)
        if user_settings:
            st.session_state["user_settings_to_edit"] = user_settings
        else:
            st.toast("Planejamento não encontrado", icon="❌")

    if "user_settings_to_edit" in st.session_state:
        user_settings = st.session_state["user_settings_to_edit"]

        with st.form("atualizar_planejamento", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)

            new_pct_fixed_expenses = col1.number_input("% Gastos fixos", min_value=0.0, value=float(user_settings.pct_fixed_expenses), format="%.2f")
            new_pct_free_expenses = col2.number_input("% Gastos livres", min_value=0.0, value=float(user_settings.pct_free_expenses), format="%.2f")
            new_pct_investments = col3.number_input("% Investimentos", min_value=0.0, value=float(user_settings.pct_investments), format="%.2f")
            new_is_self_employed = st.checkbox("Trabalha autônomo?", value=user_settings.is_self_employed)
            new_is_active = st.checkbox("Ativo?", value=user_settings.is_active)

            submit = st.form_submit_button("Atualizar planejamento", type="primary", use_container_width=True)

            if submit:
                validate_percentages = user_settings_controller.validate_percentages(new_pct_fixed_expenses, new_pct_free_expenses, new_pct_investments)
                if validate_percentages:
                    try:
                        user_settings_controller.update_user_settings(
                            user_settings.id,
                            new_pct_fixed_expenses,
                            new_pct_free_expenses,
                            new_pct_investments,
                            new_is_self_employed,
                            new_is_active
                        )
                        st.toast(f"Planejamento atualizado com sucesso!", icon="✅")
                        sleep(1)
                        st.session_state.pop("user_settings_to_edit", None)
                        st.rerun()
                    except Exception as e:
                        st.toast(f"Erro ao atualizar planejamento: {str(e)}", icon="❌")
                else:
                    st.toast("A soma das porcentagens deve ser igual a 100%", icon="❌")

with tabs[2]:
    with st.form("criar_planejamento", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)

        pct_fixed_expenses = col1.number_input("% Gastos fixos", min_value=0.0, format="%.2f", value=40.0)
        pct_free_expenses = col2.number_input("% Gastos livres", min_value=0.0, format="%.2f", value=30.0)
        pct_investments = col3.number_input("% Investimentos", min_value=0.0, format="%.2f", value=30.0)
        new_is_self_employed = st.checkbox("Trabalha autônomo?", value=False)

        submit = st.form_submit_button("Criar planejamento", type="primary", use_container_width=True)

        if submit:
            validate_percentages = user_settings_controller.validate_percentages(new_pct_fixed_expenses, new_pct_free_expenses, new_pct_investments)
            if validate_percentages:
                try:
                    user_settings_controller.create_user_settings(
                        user_id=st.session_state["user_id"],
                        pct_fixed_expenses=pct_fixed_expenses,
                        pct_free_expenses=pct_free_expenses,
                        pct_investments=pct_investments,
                        is_self_employed=new_is_self_employed
                    )
                    st.toast("Planejamento criado com sucesso!", icon="✅")
                    sleep(1)
                    st.rerun()
                except Exception as e:
                    st.toast(f"Erro ao criar planejamento: {str(e)}", icon="❌")
            else:
                st.toast("A soma das porcentagens deve ser igual a 100%", icon="❌")