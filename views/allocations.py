import streamlit as st
from time import sleep
from datetime import timedelta
from controllers.incomes import IncomesController
from controllers.expenses import ExpensesController
from controllers.expense_allocations import ExpenseAllocationsController

incomes_controller = IncomesController()
expenses_controller = ExpensesController()
allocations_controller = ExpenseAllocationsController()

st.set_page_config(layout="wide")
st.title("Alocação de saídas por entrada")

expenses_list = expenses_controller.list_expenses(st.session_state["user_id"])
incomes_list = incomes_controller.list_incomes(st.session_state["user_id"])

tabs = st.tabs(["Listar entradas sem alocação", "Listar saídas sem alocação","Listar alocações", "Atualizar alocação", "Criar alocação"])

with tabs[0]:
    unallocated_incomes = incomes_controller.get_unallocated_incomes(st.session_state["user_id"])
    st.dataframe(
        [{
            "ID": u.id,
            "Saída": u.description,
            "Valor": u.amount,
            "Valor utilizado": u.allocated,
            "Saldo": u.saldo,
        } for u in unallocated_incomes],
        hide_index=True
    )

with tabs[1]:
    unallocated_expenses = expenses_controller.get_unallocated_expenses(st.session_state["user_id"])
    st.dataframe(
        [{
            "ID": u.id,
            "Saída": u.description,
            "Valor": u.amount,
            "Valor utilizado": u.allocated,
            "Saldo": u.saldo,
        } for u in unallocated_expenses],
        hide_index=True
    )

with tabs[2]:
    allocations = allocations_controller.list_expense_allocations(st.session_state["user_id"])
    st.dataframe(
        [{
            "ID": a.id,
            "Entrada": a.incomes.description,
            "Saída": a.expenses.description,
            "Valor alocado": a.allocated_amount,
            "Ativo": a.is_active,
            "Criado em": a.created_at - timedelta(hours=3) if a.created_at else None,
            "Atualizado em": a.updated_at - timedelta(hours=3) if a.updated_at else None
        } for a in allocations],
        hide_index=True
    )

with tabs[3]:
    with st.container(border=True):
        col1, col2 = st.columns([4,1], vertical_alignment="bottom")

        with col1:
            allocation_id = st.text_input("Alocação", placeholder="Digite o ID da alocação")
        with col2:
            search_btn = st.button("Pesquisar", type="primary", use_container_width=True, key="allocation_search_btn")

    if search_btn:
        allocation = allocations_controller.get_expense_allocation_by_id(allocation_id)
        if allocation:
            st.session_state["allocation_to_edit"] = allocation
        else:
            st.toast("Alocação não encontrada", icon="❌")

    if "allocation_to_edit" in st.session_state:
        allocation = st.session_state["allocation_to_edit"]

        with st.form("atualizar_alocação", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)

            new_income_id = col1.selectbox("Entrada", incomes_list, format_func=lambda x: x.description, index=[c.id for c in incomes_list].index(allocation.income_id))
            new_expense_id = col2.selectbox("Saída", expenses_list, format_func=lambda x: x.description, index=[c.id for c in expenses_list].index(allocation.expense_id))
            new_allocated_amount = col3.number_input("Valor utilizado", value=float(allocation.allocated_amount))
            new_is_active = st.checkbox("Ativo?", value=allocation.is_active)

            submit = st.form_submit_button("Atualizar alocação", type="primary", use_container_width=True)

            if submit:
                try:
                    allocations_controller.update_expense_allocation(
                        allocation.id,
                        new_income_id.id,
                        new_expense_id.id,
                        new_allocated_amount,
                        new_is_active
                    )
                    st.toast(f"Alocação {new_expense_id.description} atualizada com sucesso!", icon="✅")
                    sleep(1)
                    st.session_state.pop("allocation_to_edit", None)
                    st.rerun()
                except Exception as e:
                    st.toast(f"Erro ao atualizar alocação: {str(e)}", icon="❌")

with tabs[4]:
    with st.form("criar_alocação", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)

        income_id = col1.selectbox("Entrada", incomes_list, format_func=lambda x: x.description)
        expense_id = col2.selectbox("Saída", expenses_list, format_func=lambda x: x.description)
        allocated_amount = col3.number_input("Valor")

        submit = st.form_submit_button("Criar alocação", type="primary", use_container_width=True)

        if submit:
            try:
                allocations_controller.create_expense_allocation(
                    user_id=st.session_state["user_id"],
                    income_id=income_id.id,
                    expense_id=expense_id.id,
                    allocated_amount=allocated_amount
                )
                st.toast(f"Alocação da saída {expense_id.description} na entrada {income_id.description} criada com sucesso!", icon="✅")
                sleep(1)
                st.rerun()
            except Exception as e:
                st.toast(f"Erro ao criar alocação: {str(e)}", icon="❌")