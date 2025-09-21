import streamlit as st
from time import sleep
from datetime import timedelta
from controllers.fixed_transactions_controller import FixedTransactionsController

fixed_transactions_controller = FixedTransactionsController()

st.set_page_config(layout="wide")
st.title("Transações fixas")

tabs = st.tabs(["Listar transações", "Atualizar transação", "Criar transação"])

with tabs[0]:
    transactions = fixed_transactions_controller.list_fixed_transactions(st.session_state["user_id"])
    st.dataframe(
        [{
            "ID": t.id,
            "Valor": t.amount,
            "Dia de referência": t.due_day,
            "Descrição": t.description,
            "Tipo": t.type,
            "Categoria": t.category,
            "Ativo": t.is_active,
            "Criado em": t.created_at - timedelta(hours=3) if t.created_at else None,
            "Atualizado em": t.updated_at - timedelta(hours=3) if t.updated_at else None
        } for t in transactions],
        hide_index=True
    )

with tabs[1]:
    with st.container(border=True):
        col1, col2 = st.columns([4,1], vertical_alignment="bottom")

        with col1:
            fixed_transaction_id = st.number_input("ID", min_value=1, value=None, placeholder="Digite o ID da transação")
        with col2:
            search_btn = st.button("Pesquisar", type="primary", use_container_width=True)

    if search_btn:
        fixed_transaction = fixed_transactions_controller.get_fixed_transaction_by_id(fixed_transaction_id)
        if fixed_transaction:
            st.session_state["fixed_transaction_to_edit"] = fixed_transaction
        else:
            st.toast("Transação não encontrada", icon="❌")

    if "fixed_transaction_to_edit" in st.session_state:
        fixed_transaction = st.session_state["fixed_transaction_to_edit"]

        with st.form("atualizar_transacao", clear_on_submit=True):
            col1, col2, col3, col4, col5 = st.columns(5)

            new_amount = col1.number_input("Valor", min_value=0.0, value=float(fixed_transaction.amount), format="%.2f")
            new_due_day = col2.number_input("Dia de referência", min_value=1, max_value=31, value=fixed_transaction.due_day)
            new_description = col3.text_input("Descrição", value=fixed_transaction.description)

            type_options = ["Receita", "Despesa"]
            new_type = col4.selectbox("Tipo", type_options, index=type_options.index(fixed_transaction.type))

            new_category = col5.text_input("Categoria", value=fixed_transaction.category)
            new_is_active = st.checkbox("Ativo?", value=fixed_transaction.is_active)

            submit = st.form_submit_button("Atualizar transação", type="primary", use_container_width=True)

            if submit:
                try:
                    fixed_transactions_controller.update_fixed_transaction(
                        fixed_transaction.id,
                        new_amount,
                        new_due_day,
                        new_description,
                        new_type,
                        new_category,
                        new_is_active
                    )
                    st.toast(f"Transação {new_description} atualizado com sucesso!", icon="✅")
                    sleep(1)
                    st.session_state.pop("fixed_transaction_to_edit", None)
                    st.rerun()
                except Exception as e:
                    st.toast(f"Erro ao atualizar transação: {str(e)}", icon="❌")

with tabs[2]:
    with st.form("criar_transacao", clear_on_submit=True):
        col1, col2, col3, col4, col5 = st.columns(5)

        amount = col1.number_input("Valor", min_value=0.0, format="%.2f")
        due_day = col2.number_input("Dia de referência", min_value=1, max_value=31, value=1)
        description = col3.text_input("Descrição")
        type = col4.selectbox("Tipo", ["Receita", "Despesa"])
        category = col5.text_input("Categoria")

        submit = st.form_submit_button("Criar transação", type="primary", use_container_width=True)

        if submit:
            try:
                fixed_transactions_controller.create_fixed_transaction(
                    user_id=st.session_state["user_id"],
                    amount=amount,
                    due_day=due_day,
                    description=description,
                    type=type,
                    category=category
                )
                st.toast("Transação criada com sucesso!", icon="✅")
                sleep(1)
                st.rerun()
            except Exception as e:
                st.toast(f"Erro ao criar transação: {str(e)}", icon="❌")