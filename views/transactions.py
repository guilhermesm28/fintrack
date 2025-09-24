from datetime import timedelta
import streamlit as st
from controllers.incomes import IncomesController
from controllers.expenses import ExpensesController
from controllers.categories import CategoriesController
from time import sleep

incomes_controller = IncomesController()
expenses_controller = ExpensesController()
categories_controller = CategoriesController()

st.set_page_config(layout="wide")
st.title("Transações")

incomes_expander = st.expander("Entradas")
income_tabs = incomes_expander.tabs(["Listar entradas", "Atualizar entrada", "Criar entrada"])
income_categories = categories_controller.get_categories_by_type(is_expense=False)

with income_tabs[0]:
    incomes = incomes_controller.list_incomes(st.session_state["user_id"])
    st.dataframe(
        [{
            "ID": i.id,
            "Categoria": i.category.name,
            "Valor": i.amount,
            "Dia de referência": i.due_day,
            "Descrição": i.description,
            "Descrição detalhada": i.description_detail,
            "Ativo": i.is_active,
            "Criado em": i.created_at - timedelta(hours=3) if i.created_at else None,
            "Atualizado em": i.updated_at - timedelta(hours=3) if i.updated_at else None
        } for i in incomes],
        hide_index=True
    )

with income_tabs[1]:
    with st.container(border=True):
        col1, col2 = st.columns([4,1], vertical_alignment="bottom")

        with col1:
            income_id = st.text_input("Entrada", placeholder="Digite o ID da entrada")
        with col2:
            search_btn = st.button("Pesquisar", type="primary", use_container_width=True, key="income_search_btn")

    if search_btn:
        income = incomes_controller.get_income_by_id(income_id)
        if income:
            st.session_state["income_to_edit"] = income
        else:
            st.toast("Entrada não encontrada", icon="❌")

    if "income_to_edit" in st.session_state:
        income = st.session_state["income_to_edit"]

        with st.form("atualizar_entrada", clear_on_submit=True):
            col1, col2, col3, col4, col5 = st.columns(5)

            new_category_id = col1.selectbox("Categoria", income_categories, format_func=lambda x: x.name, index=[c.id for c in income_categories].index(income.category_id))
            new_amount = col2.number_input("Valor", value=float(income.amount))
            new_due_day = col3.number_input("Dia de referência", value=income.due_day)
            new_description = col4.text_input("Descrição", value=income.description)
            new_description_detail = col5.text_input("Descrição detalhada", value=income.description_detail)
            new_is_active = st.checkbox("Ativo?", value=income.is_active)

            submit = st.form_submit_button("Atualizar entrada", type="primary", use_container_width=True)

            if submit:
                try:
                    incomes_controller.update_income(
                        income.id,
                        new_category_id.id,
                        new_amount,
                        new_due_day,
                        new_description,
                        new_description_detail,
                        new_is_active
                    )
                    st.toast(f"Entrada {new_description} atualizada com sucesso!", icon="✅")
                    sleep(1)
                    st.session_state.pop("income_to_edit", None)
                    st.rerun()
                except Exception as e:
                    st.toast(f"Erro ao atualizar entrada: {str(e)}", icon="❌")

with income_tabs[2]:
    with st.form("criar_entrada", clear_on_submit=True):
        col1, col2, col3, col4, col5 = st.columns(5)

        category_id = col1.selectbox("Categoria", income_categories, format_func=lambda x: x.name)
        amount = col2.number_input("Valor")
        due_day = col3.number_input("Dia de referência", min_value=1, max_value=31)
        description = col4.text_input("Descrição")
        description_detail = col5.text_input("Descrição detalhada")

        submit = st.form_submit_button("Criar entrada", type="primary", use_container_width=True)

        if submit:
            try:
                incomes_controller.create_income(
                    user_id=st.session_state["user_id"],
                    category_id=category_id.id,
                    amount=amount,
                    due_day=due_day,
                    description=description,
                    description_detail=description_detail
                )
                st.toast(f"Entrada {description} criada com sucesso!", icon="✅")
                sleep(1)
                st.rerun()
            except Exception as e:
                st.toast(f"Erro ao criar entrada: {str(e)}", icon="❌")

expenses_expander = st.expander("Saídas")
expense_tabs = expenses_expander.tabs(["Listar saídas", "Atualizar saída", "Criar saída"])
expense_categories = categories_controller.get_categories_by_type(is_expense=True)

with expense_tabs[0]:
    expenses = expenses_controller.list_expenses(st.session_state["user_id"])
    st.dataframe(
        [{
            "ID": e.id,
            "Categoria": e.category.name,
            "Valor": e.amount,
            "Dia de referência": e.due_day,
            "Descrição": e.description,
            "Descrição detalhada": e.description_detail,
            "Ativo": e.is_active,
            "Criado em": e.created_at - timedelta(hours=3) if e.created_at else None,
            "Atualizado em": e.updated_at - timedelta(hours=3) if e.updated_at else None
        } for e in expenses],
        hide_index=True
    )

with expense_tabs[1]:
    with st.container(border=True):
        col1, col2 = st.columns([4,1], vertical_alignment="bottom")

        with col1:
            expense_id = st.text_input("Saída", placeholder="Digite o ID da saída")
        with col2:
            search_btn = st.button("Pesquisar", type="primary", use_container_width=True, key="expense_search_btn")

    if search_btn:
        expense = expenses_controller.get_expense_by_id(expense_id)
        if expense:
            st.session_state["expense_to_edit"] = expense
        else:
            st.toast("Saída não encontrada", icon="❌")

    if "expense_to_edit" in st.session_state:
        expense = st.session_state["expense_to_edit"]

        with st.form("atualizar_saida", clear_on_submit=True):
            col1, col2, col3, col4, col5 = st.columns(5)

            new_category_id = col1.selectbox("Categoria", expense_categories, format_func=lambda x: x.name, index=[c.id for c in expense_categories].index(expense.category_id))
            new_amount = col2.number_input("Valor", value=float(expense.amount))
            new_due_day = col3.number_input("Dia de referência", value=expense.due_day)
            new_description = col4.text_input("Descrição", value=expense.description)
            new_description_detail = col5.text_input("Descrição detalhada", value=expense.description_detail)
            new_is_active = st.checkbox("Ativo?", value=expense.is_active)

            submit = st.form_submit_button("Atualizar saída", type="primary", use_container_width=True)

            if submit:
                try:
                    expenses_controller.update_expense(
                        expense.id,
                        new_category_id.id,
                        new_amount,
                        new_due_day,
                        new_description,
                        new_description_detail,
                        new_is_active
                    )
                    st.toast(f"Saída {new_description} atualizada com sucesso!", icon="✅")
                    sleep(1)
                    st.session_state.pop("expense_to_edit", None)
                    st.rerun()
                except Exception as e:
                    st.toast(f"Erro ao atualizar saída: {str(e)}", icon="❌")

with expense_tabs[2]:
    with st.form("criar_saida", clear_on_submit=True):
        col1, col2, col3, col4, col5 = st.columns(5)

        category_id = col1.selectbox("Categoria", expense_categories, format_func=lambda x: x.name)
        amount = col2.number_input("Valor")
        due_day = col3.number_input("Dia de referência", min_value=1, max_value=31)
        description = col4.text_input("Descrição")
        description_detail = col5.text_input("Descrição detalhada")

        submit = st.form_submit_button("Criar entrada", type="primary", use_container_width=True)

        if submit:
            try:
                expenses_controller.create_expense(
                    user_id=st.session_state["user_id"],
                    category_id=category_id.id,
                    amount=amount,
                    due_day=due_day,
                    description=description,
                    description_detail=description_detail
                )
                st.toast(f"Saída {description} criada com sucesso!", icon="✅")
                sleep(1)
                st.rerun()
            except Exception as e:
                st.toast(f"Erro ao criar saída: {str(e)}", icon="❌")
