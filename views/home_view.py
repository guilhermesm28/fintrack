import streamlit as st
from controllers.fixed_transactions_controller import FixedTransactionsController
from controllers.user_settings_controller import UserSettingsController

fixed_transactions_controller = FixedTransactionsController()
user_settings_controller = UserSettingsController()

settings = user_settings_controller.get_user_settings_by_user_id(st.session_state["user_id"])

st.set_page_config(layout="wide")
st.title("Página inicial")

st.write(f"Olá, {st.session_state.get('fullname')}!")
st.write("Bem-vindo ao FINTRACK, sua ferramenta de planejamento financeiro pessoal.")

if not settings:
    st.write("Siga o passo a passo abaixo para configurar seu planejamento:")

    with st.container(border=True):
        st.write("1. Cadastre suas transações fixas (receitas e despesas):")
        st.page_link("views/fixed_transactions_view.py", label="Transações fixas", icon="📈")
        st.write("2. Cadastre seu planejamento financeiro:")
        st.page_link("views/planner_view.py", label="Planejamento financeiro", icon="📊")

else:
    receitas = fixed_transactions_controller.get_total_income(st.session_state["user_id"])
    despesas = fixed_transactions_controller.get_total_expenses(st.session_state["user_id"])

    gastos_fixos = settings.pct_fixed_expenses
    gastos_livres = settings.pct_free_expenses
    investimentos = settings.pct_investments

    st.write("Seu planejamento financeiro atual:")
    with st.container(border=True):
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("Total de receitas", f"R$ {receitas:.2f}")
        with col2:
            delta_despesas = (receitas * gastos_fixos / 100) - despesas
            st.metric("Total de despesas", f"R$ {despesas:.2f}", delta=f"R$ {delta_despesas:.2f}", help=f"R$ {receitas} * {gastos_fixos}%")
        with col3:
            st.metric("Saldo", f"R$ {receitas - despesas:.2f}")
        with col4:
            st.metric("Investimentos sugeridos", f"R$ {receitas * investimentos / 100:.2f}", help=f"R$ {receitas} * {investimentos}%")
        with col5:
            st.metric("Gastos livres sugeridos", f"R$ {receitas * gastos_livres / 100:.2f}", help=f"R$ {receitas} * {gastos_livres}%")