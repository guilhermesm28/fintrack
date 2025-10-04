import streamlit as st
from controllers.expenses import ExpensesController
from controllers.incomes import IncomesController
from controllers.user_settings import UserSettingsController

incomes_controller = IncomesController()
expenses_controller = ExpensesController()
user_settings_controller = UserSettingsController()

settings = user_settings_controller.get_user_settings_by_user_id(st.session_state["user_id"])

st.set_page_config(layout="wide")
st.title("Página inicial")

st.write(f"Olá, {st.session_state.get('fullname')}!")
st.write("Bem-vindo ao FINTRACK, sua ferramenta de planejamento financeiro pessoal.")

tabs = st.tabs(["Planejamento atual", "Simular planejamento"])

with tabs[0]:
    if not settings:
        st.write("Siga o passo a passo abaixo para configurar seu planejamento:")

        with st.container(border=True):
            st.write("1. Cadastre suas transações (receitas e despesas):")
            st.page_link("views/transactions.py", label="Transações", icon="📈")
            st.write("2. Cadastre seu planejamento financeiro:")
            st.page_link("views/planner.py", label="Planejamento financeiro", icon="📊")

    else:
        incomes = incomes_controller.get_total_incomes(st.session_state["user_id"])
        expenses = expenses_controller.get_total_essential_expenses(st.session_state["user_id"])
        investments = expenses_controller.get_total_investments(st.session_state["user_id"])
        free_expenses = expenses_controller.get_total_free_expenses(st.session_state["user_id"])

        pct_essential_expenses = settings.pct_essential_expenses
        pct_free_expenses = settings.pct_free_expenses
        pct_investments = settings.pct_investments

        with st.container(border=True):
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                st.metric("Total de entradas", f"R$ {incomes:.2f}")

            # Gastos essenciais
            with col2:
                planned_expenses = incomes * pct_essential_expenses / 100
                delta_expenses = float(expenses - planned_expenses)

                st.metric(
                    "Gastos essenciais",
                    f"R$ {expenses:.2f}",
                    delta=f"{delta_expenses:.2f} do planejado",
                    delta_color="inverse",
                    help=f"Planejado: R$ {planned_expenses:.2f} ({pct_essential_expenses}%)"
                )

            # Saldo
            with col3:
                balance = incomes - expenses
                st.metric("Saldo", f"R$ {balance:.2f}")

                # Planejado
                planned_investments = incomes * pct_investments / 100
                planned_free = incomes * pct_free_expenses / 100

            # Investimentos
            with col4:
                delta_investments = float(investments - planned_investments)

                st.metric(
                    "Investimentos",
                    f"R$ {investments:.2f}",
                    delta=f"{delta_investments:.2f} do planejado",
                    delta_color="inverse",
                    help=f"Planejado: R$ {planned_investments:.2f} ({pct_investments}%)"
                )

            # Gastos livres
            with col5:
                delta_free = float(free_expenses - planned_free)

                st.metric(
                    "Gastos livres",
                    f"R$ {free_expenses:.2f}",
                    delta=f"{delta_free:.2f} do planejado",
                    delta_color="inverse",
                    help=f"Planejado: R$ {planned_free:.2f} ({pct_free_expenses}%)"
                )

            # Reserva
            with col6:
                is_self_employed = settings.is_self_employed
                reserve_months = 12 if is_self_employed else 6

                st.metric(
                    "Reserva de emergência",
                    f"R$ {expenses * reserve_months:.2f}",
                    help=f"R$ {expenses} * {reserve_months} meses"
                )

        list_incomes = incomes_controller.list_incomes(st.session_state["user_id"])

        cols = st.columns(len(list_incomes))

        for col, income in zip(cols, list_incomes):
            with col.container(border=True):
                st.markdown(f"#### R$ {income.amount} - {income.description}")
                expenses_by_income = incomes_controller.get_expense_allocations_by_income_id(income.id)

                for expense in expenses_by_income:
                    st.markdown(f" - R$ {expense.allocated_amount} - {expense.expenses.description}")

with tabs[1]:
    with st.form("simular_planejamento"):
        col1, col2, col3, col4, col5, col6 = st.columns(6, vertical_alignment="bottom")

        with col1:
            incomes = st.number_input("Entradas", min_value=0.0, format="%.2f")
        with col2:
            expenses = st.number_input("Gastos essenciais", min_value=0.0, format="%.2f")
        with col3:
            pct_essential_expenses = st.number_input("Gastos essenciais (%)", min_value=0.0, value=40.0, format="%.2f")
        with col4:
            pct_free_expenses = st.number_input("Gastos livres (%)", min_value=0.0, value=30.0, format="%.2f")
        with col5:
            pct_investments = st.number_input("Investimentos (%)", min_value=0.0, value=30.0, format="%.2f")
        with col6:
            is_self_employed = st.checkbox("Trabalha autônomo?", value=False)
            reserve_months = 12 if is_self_employed else 6

        submit = st.form_submit_button("Simular planejamento", type="primary", use_container_width=True)

        if submit:
            validate_percentages = user_settings_controller.validate_percentages(
                pct_essential_expenses, pct_free_expenses, pct_investments
            )
            if validate_percentages:
                with st.container(border=True):
                    col1, col2, col3, col4, col5, col6 = st.columns(6)

                    with col1:
                        st.metric("Total de entradas", f"R$ {incomes:.2f}")

                    # Gastos essenciais
                    with col2:
                        planned_expenses = incomes * pct_essential_expenses / 100
                        delta_expenses = expenses - planned_expenses

                        st.metric(
                            "Gastos essenciais",
                            f"R$ {expenses:.2f}",
                            delta=f"{delta_expenses:.2f} do planejado",
                            delta_color="inverse",
                            help=f"Planejado: R$ {planned_expenses:.2f} ({pct_essential_expenses}%)"
                        )

                    # Saldo
                    with col3:
                        balance = incomes - expenses

                        st.metric("Saldo", f"R$ {balance:.2f}")

                        # Planejado
                        planned_investments = incomes * pct_investments / 100
                        planned_free = incomes * pct_free_expenses / 100

                        # Real proporcional ao saldo
                        total_var_pct = pct_investments + pct_free_expenses
                        if total_var_pct > 0:
                            real_investments = balance * (pct_investments / total_var_pct)
                            real_free = balance * (pct_free_expenses / total_var_pct)
                        else:
                            real_investments = 0
                            real_free = 0

                    # Investimentos
                    with col4:
                        delta_investments = real_investments - planned_investments

                        st.metric(
                            "Investimentos",
                            f"R$ {real_investments:.2f}",
                            delta=f"{delta_investments:.2f} do planejado",
                            delta_color="inverse",
                            help=f"Planejado: R$ {planned_investments:.2f} ({pct_investments}%)"
                        )

                    # Gastos livres
                    with col5:
                        delta_free = real_free - planned_free

                        st.metric(
                            "Gastos livres",
                            f"R$ {real_free:.2f}",
                            delta=f"{delta_free:.2f} do planejado",
                            delta_color="inverse",
                            help=f"Planejado: R$ {planned_free:.2f} ({pct_free_expenses}%)"
                        )

                    # Reserva
                    with col6:
                        st.metric(
                            "Reserva de emergência",
                            f"R$ {expenses * reserve_months:.2f}",
                            help=f"R$ {expenses} * {reserve_months} meses"
                        )
            else:
                st.toast("Os percentuais de Gastos essenciais, livres e investimentos devem somar 100%.", icon="🚨")
