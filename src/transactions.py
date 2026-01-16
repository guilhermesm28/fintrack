import streamlit as st
from utils.crud import select, insert, update

@st.dialog("Cadastrar transação")
def create_object(user_id, categories):
    transaction_type = st.selectbox(
        "Tipo de transação",
        ["Entrada", "Saída"],
        index=0,
    )

    is_expense = transaction_type == "Saída"

    with st.form("create_object_form", clear_on_submit=True):
        is_essential_expense = False
        is_free_expense = False
        is_investment = False

        if is_expense:
            expense_type = st.selectbox(
                "Tipo de saída",
                ["Gasto essencial", "Gasto livre", "Investimento"],
            )
            is_essential_expense = expense_type == "Gasto essencial"
            is_free_expense = expense_type == "Gasto livre"
            is_investment = expense_type == "Investimento"

        filtered_categories = categories[categories["is_expense"] == is_expense]

        category_id = st.selectbox(
            "Categoria",
            options=[None] + filtered_categories["id"].tolist(),
            format_func=lambda x: (
                "Selecione uma categoria"
                if x is None
                else filtered_categories.loc[filtered_categories["id"] == x, "name"].values[0]
            ),
        )

        amount = st.number_input("Valor", min_value=0.0)
        due_day = st.number_input("Dia de referência", min_value=1, max_value=31)
        description = st.text_input("Descrição", max_chars=100)
        description_detail = st.text_input("Descrição detalhada", max_chars=255)
        is_active = st.checkbox("Ativo", value=True)

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("Salvar", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.rerun()

        if submitted:
            if not category_id:
                st.error("Selecione uma categoria válida.")
                return
            if amount <= 0:
                st.error("O valor deve ser maior que zero.")
                return

            create_data = {
                "user_id": user_id,
                "is_expense": is_expense,
                "is_essential_expense": is_essential_expense,
                "is_free_expense": is_free_expense,
                "is_investment": is_investment,
                "category_id": category_id,
                "amount": amount,
                "due_day": due_day,
                "description": description,
                "description_detail": description_detail,
                "is_active": is_active,
            }

            result = insert("transactions", create_data)
            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

@st.dialog("Editar transação")
def edit_object(object, categories):
    from datetime import datetime

    transaction_type = st.selectbox(
        "Tipo de transação",
        ["Entrada", "Saída"],
        index=1 if object["is_expense"] else 0,
    )

    new_is_expense = transaction_type == "Saída"

    with st.form("edit_object_form"):
        new_is_essential_expense = False
        new_is_free_expense = False
        new_is_investment = False

        if new_is_expense:
            expense_type_index = (
                0
                if object.get("is_essential_expense")
                else 1
                if object.get("is_free_expense")
                else 2
            )
            new_expense_type = st.selectbox(
                "Tipo de saída",
                ["Gasto essencial", "Gasto livre", "Investimento"],
                index=expense_type_index,
            )
            new_is_essential_expense = new_expense_type == "Gasto essencial"
            new_is_free_expense = new_expense_type == "Gasto livre"
            new_is_investment = new_expense_type == "Investimento"

        filtered_categories = categories[categories["is_expense"] == new_is_expense].copy()

        current_cat_id = object.get("category_id")
        original_is_expense = object.get("is_expense")
        if new_is_expense != original_is_expense:
            current_cat_id = None

        options_list = filtered_categories["id"].tolist()
        id_to_name = dict(zip(filtered_categories["id"], filtered_categories["name"]))

        placeholder_mode = False
        if not options_list:
            options_list = [None]
            placeholder_mode = True

        try:
            default_index = options_list.index(current_cat_id) if current_cat_id in options_list else 0
        except Exception:
            default_index = 0

        def fmt(x):
            if x is None:
                return "Selecione uma categoria"
            return id_to_name.get(x, str(x))

        new_category_id = st.selectbox(
            "Categoria",
            options=options_list,
            format_func=fmt,
            index=default_index,
        )

        if placeholder_mode:
            st.warning("Nenhuma categoria disponível para o tipo selecionado.")

        new_amount = st.number_input("Valor", value=float(object.get("amount", 0.0)), min_value=0.0)
        new_due_day = st.number_input("Dia de referência", value=int(object.get("due_day", 1)), min_value=1, max_value=31)
        new_description = st.text_input("Descrição", value=object.get("description", ""))
        new_description_detail = st.text_input("Descrição detalhada", value=object.get("description_detail", ""))
        new_is_active = st.checkbox("Ativo?", value=bool(object.get("is_active", True)))

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("Salvar", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.rerun()

        if submitted:
            if placeholder_mode or new_category_id is None:
                st.error("Selecione uma categoria válida antes de salvar.")
                return

            update_data = {
                "is_expense": new_is_expense,
                "is_essential_expense": new_is_essential_expense,
                "is_free_expense": new_is_free_expense,
                "is_investment": new_is_investment,
                "category_id": new_category_id,
                "amount": new_amount,
                "due_day": new_due_day,
                "description": new_description,
                "description_detail": new_description_detail,
                "is_active": new_is_active,
                "updated_at": datetime.now(),
            }

            result = update("transactions", update_data, where={"id": object["id"]})
            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

try:
    st.subheader("Gerenciamento de transações")
    col1, col2, col3 = st.columns([4, 1, 1], vertical_alignment="bottom")

    categories = select(
        "SELECT id, name, is_expense FROM public.categories WHERE is_active = true ORDER BY name"
    )

    with col1:
        search_term = st.text_input(
            ":material/Search: Buscar",
            placeholder="Digite o ID ou descrição da transação...",
        )

    with col2:
        if st.button(":material/add: Cadastrar", type="primary", use_container_width=True):
            create_object(st.session_state["user_id"], categories)

    with col3:
        st.session_state["edit_clicked"] = st.button(
            ":material/edit: Editar",
            use_container_width=True,
            help="Selecione uma transação na tabela para editar",
        )

    query = f"""
        SELECT
            a.id,
            a.is_expense,
            a.is_essential_expense,
            a.is_free_expense,
            a.is_investment,
            b.name AS category_name,
            a.amount,
            a.due_day,
            a.description,
            a.description_detail,
            a.is_active,
            a.created_at,
            a.updated_at
        FROM public.transactions a
        INNER JOIN public.categories b ON a.category_id = b.id
        WHERE 1=1
            AND a.user_id = {st.session_state["user_id"]}
            AND a.is_active = TRUE
        ORDER BY a.due_day
    """
    df = select(query)

    if search_term:
        search_term_lower = search_term.lower()
        df = df[
            df.apply(
                lambda row: (
                    search_term_lower in str(row["description"]).lower()
                    or search_term_lower in str(row["id"])
                ),
                axis=1,
            )
        ]

    if df.empty:
        st.info("Nenhuma transação encontrada.")
    else:
        COLUMN_CONFIG = {
            "is_expense": st.column_config.CheckboxColumn("Saída"),
            "is_essential_expense": st.column_config.CheckboxColumn("Gasto essencial"),
            "is_free_expense": st.column_config.CheckboxColumn("Gasto livre"),
            "is_investment": st.column_config.CheckboxColumn("Investimento"),
            "category_name": st.column_config.TextColumn("Categoria"),
            "amount": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
            "due_day": st.column_config.NumberColumn("Dia ref."),
            "description": st.column_config.TextColumn("Descrição", width="small"),
            "description_detail": st.column_config.TextColumn("Descrição detalhada", width="medium"),
            "is_active": st.column_config.CheckboxColumn("Ativo"),
            "created_at": st.column_config.DatetimeColumn("Criado em"),
            "updated_at": st.column_config.DatetimeColumn("Atualizado em"),
        }

        event = st.dataframe(
            df.drop(["id"], axis=1),
            width="stretch",
            hide_index=True,
            column_config=COLUMN_CONFIG,
            selection_mode="single-row",
            on_select="rerun",
            key="transactions_table",
        )

        if st.session_state.get("edit_clicked"):
            if event.selection.rows:
                selected_index = event.selection.rows[0]
                selected_object_id = df.iloc[selected_index]["id"]
                object_data = select(f"SELECT * FROM public.transactions WHERE id = {selected_object_id}")
                if not object_data.empty:
                    edit_object(object_data.iloc[0].to_dict(), categories)

except Exception as e:
    st.error(f"Erro ao carregar página: {e}")