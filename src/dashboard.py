import streamlit as st
from utils.crud import select

try:
    st.subheader("Dashboard")

    tabs = st.tabs(["Balanço"])

    with tabs[0]:
        query = f"""
            with cte_incomes as (
                select
                    due_day,
                    sum(amount) as amount
                from transactions
                where is_expense = false and user_id = {st.session_state.user_id}
                group by due_day
            ),

            cte_expenses as (
                select
                    due_day,
                    sum(amount) as amount
                from transactions
                where is_expense = true and user_id = {st.session_state.user_id}
                group by due_day
            )

            select
                a.due_day,
                a.amount as total_incomes,
                b.amount as total_expenses,
                a.amount - b.amount as balance
            from cte_incomes a
            inner join cte_expenses b on a.due_day = b.due_day
            order by a.due_day
        """
        df = select(query)

        if df.empty:
            st.info("Nenhum dado encontrado.")
        else:
            COLUMN_CONFIG = {
                "due_day": st.column_config.NumberColumn("Dia de referência", width="small"),
                "total_incomes": st.column_config.NumberColumn("Entradas", format="R$ %.2f"),
                "total_expenses": st.column_config.NumberColumn("Saídas", format="R$ %.2f"),
                "balance": st.column_config.NumberColumn("Saldo", format="R$ %.2f"),
            }

            st.dataframe(
                df,
                width="stretch",
                hide_index=True,
                column_config=COLUMN_CONFIG,
            )

except Exception as e:
    st.error(f"Erro ao carregar página: {e}")