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

tabs = st.tabs(["Planejamento atual", "Simular planejamento"])

with tabs[0]:
    if not settings:
        st.write("Siga o passo a passo abaixo para configurar seu planejamento:")

        with st.container(border=True):
            st.write("1. Cadastre suas transações fixas (receitas e despesas):")
            st.page_link("views/fixed_transactions_view.py", label="Transações fixas", icon="📈")
            st.write("2. Cadastre seu planejamento financeiro:")
            st.page_link("views/planner_view.py", label="Planejamento financeiro", icon="📊")

    else:
        incomes = fixed_transactions_controller.get_total_income(st.session_state["user_id"])
        expenses = fixed_transactions_controller.get_total_expenses(st.session_state["user_id"])

        pct_fixed_expenses = settings.pct_fixed_expenses
        pct_free_expenses = settings.pct_free_expenses
        pct_investments = settings.pct_investments

        with st.container(border=True):
            col1, col2, col3, col4, col5, col6 = st.columns(6)

            with col1:
                st.metric("Total de receitas", f"R$ {incomes:.2f}")

            # Despesas Fixas
            with col2:
                planned_expenses = incomes * pct_fixed_expenses / 100
                delta_expenses = float(expenses - planned_expenses)

                st.metric(
                    "Total de despesas",
                    f"R$ {expenses:.2f}",
                    delta=f"{delta_expenses:.2f} planejado",
                    help=f"Planejado: R$ {planned_expenses:.2f} ({pct_fixed_expenses}%)"
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
                delta_investments = float(real_investments - planned_investments)

                st.metric(
                    "Investimentos",
                    f"R$ {real_investments:.2f}",
                    delta=f"{delta_investments:.2f} planejado",
                    help=f"Planejado: R$ {planned_investments:.2f} ({pct_investments}%)"
                )

            # Gastos livres
            with col5:
                delta_free = float(real_free - planned_free)

                st.metric(
                    "Gastos livres",
                    f"R$ {real_free:.2f}",
                    delta=f"{delta_free:.2f} planejado",
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

with tabs[1]:
    with st.form("simular_planejamento"):
        col1, col2, col3, col4, col5, col6 = st.columns(6, vertical_alignment="bottom")

        with col1:
            incomes = st.number_input("Receitas", min_value=0.0, format="%.2f")
        with col2:
            expenses = st.number_input("Despesas", min_value=0.0, format="%.2f")
        with col3:
            pct_fixed_expenses = st.number_input("Gastos fixos (%)", min_value=0.0, value=40.0, format="%.2f")
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
                pct_fixed_expenses, pct_free_expenses, pct_investments
            )
            if validate_percentages:
                with st.container(border=True):
                    col1, col2, col3, col4, col5, col6 = st.columns(6)

                    with col1:
                        st.metric("Total de receitas", f"R$ {incomes:.2f}")

                    # Despesas Fixas
                    with col2:
                        planned_expenses = incomes * pct_fixed_expenses / 100
                        delta_expenses = expenses - planned_expenses

                        st.metric(
                            "Total de despesas",
                            f"R$ {expenses:.2f}",
                            delta=f"{delta_expenses:.2f} planejado",
                            help=f"Planejado: R$ {planned_expenses:.2f} ({pct_fixed_expenses}%)"
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
                            delta=f"{delta_investments:.2f} planejado",
                            help=f"Planejado: R$ {planned_investments:.2f} ({pct_investments}%)"
                        )

                    # Gastos livres
                    with col5:
                        delta_free = real_free - planned_free

                        st.metric(
                            "Gastos livres",
                            f"R$ {real_free:.2f}",
                            delta=f"{delta_free:.2f} planejado",
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
                st.toast("Os percentuais de gastos fixos, livres e investimentos devem somar 100%.", icon="🚨")
