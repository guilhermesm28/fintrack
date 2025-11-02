import streamlit as st
from utils.crud import select, insert, update
from utils.security import hash_password

@st.dialog("Cadastrar usuário")
def create_user():
    with st.form("create_user_form", clear_on_submit=True):
        first_name = st.text_input("Primeiro nome")
        last_name = st.text_input("Sobrenome")
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")
        is_admin = st.checkbox("Administrador?", value=False)
        pct_essential_expenses = st.number_input("% Gastos essenciais", min_value=0.0, format="%.2f", value=40.0)
        pct_free_expenses = st.number_input("% Gastos livres", min_value=0.0, format="%.2f", value=30.0)
        pct_investments = st.number_input("% Investimentos", min_value=0.0, format="%.2f", value=30.0)
        is_self_employed = st.checkbox("Trabalha autônomo?", value=False)
        is_active = st.checkbox("Ativo", value=True)

        hashed_password = hash_password(password)

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("Salvar", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.rerun()

        if submitted:
            if not password or not username:
                st.error("Usuário e senha são obrigatórios.")
                return
            create_data = {
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "password": hashed_password,
                "is_admin": is_admin,
                "pct_essential_expenses": pct_essential_expenses,
                "pct_free_expenses": pct_free_expenses,
                "pct_investments": pct_investments,
                "is_self_employed": is_self_employed,
                "is_active": is_active
            }

            result = insert("users", create_data)
            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

@st.dialog("Cadastrar categoria")
def create_category():
    with st.form("create_category_form", clear_on_submit=True):
        name = st.text_input("Categoria")
        is_expense = st.checkbox("Saída", value=True)
        is_active = st.checkbox("Ativo", value=True)

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("Salvar", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.rerun()

        if submitted:
            create_data = {
                "name": name,
                "is_expense": is_expense,
                "is_active": is_active
            }

            result = insert("categories", create_data)
            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

@st.dialog("Editar usuário")
def edit_user(object):
    from datetime import datetime

    with st.form("edit_user_form"):
        new_first_name = st.text_input("Nome", object["first_name"])
        new_last_name = st.text_input("Sobrenome", object["last_name"])
        new_username = st.text_input("Usuário", object["username"])
        new_password = st.text_input("Senha", type="password", placeholder="Digite nova senha (opcional)")
        new_is_admin = st.checkbox("Administrador?", value=object["is_admin"])
        new_pct_essential_expenses = st.number_input("% Gastos essenciais", min_value=0.0, value=float(object["pct_essential_expenses"]), format="%.2f")
        new_pct_free_expenses = st.number_input("% Gastos livres", min_value=0.0, value=float(object["pct_free_expenses"]), format="%.2f")
        new_pct_investments = st.number_input("% Investimentos", min_value=0.0, value=float(object["pct_investments"]), format="%.2f")
        new_is_self_employed = st.checkbox("Trabalha autônomo?", value=object["is_self_employed"])
        new_is_active = st.checkbox("Ativo?", value=object["is_active"])

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("Salvar", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.rerun()

        if submitted:
            update_data = {
                "first_name": new_first_name,
                "last_name": new_last_name,
                "username": new_username,
                "is_admin": new_is_admin,
                "pct_essential_expenses": new_pct_essential_expenses,
                "pct_free_expenses": new_pct_free_expenses,
                "pct_investments": new_pct_investments,
                "is_self_employed": new_is_self_employed,
                "is_active": new_is_active,
                "updated_at": datetime.now(),
            }

            if new_password:
                new_hashed_password = hash_password(new_password)
                update_data["password"] = new_hashed_password

            result = update("users", update_data, where={"id": object["id"]})
            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

@st.dialog("Editar categoria")
def edit_category(object):
    from datetime import datetime

    with st.form("edit_category_form"):
        new_name = st.text_input("Categoria", object["name"])
        new_is_expense = st.checkbox("Saída", value=object["is_expense"])
        new_is_active = st.checkbox("Ativo?", value=object["is_active"])

        col1, col2 = st.columns(2)
        submitted = col1.form_submit_button("Salvar", type="primary", use_container_width=True)
        cancel = col2.form_submit_button("Cancelar", use_container_width=True)

        if cancel:
            st.rerun()

        if submitted:
            update_data = {
                "name": new_name,
                "is_expense": new_is_expense,
                "is_active": new_is_active,
                "updated_at": datetime.now(),
            }

            result = update("categories", update_data, where={"id": object["id"]})
            if result["success"]:
                st.success(result["message"])
                st.rerun()
            else:
                st.error(result["message"])

try:
    st.subheader("Administração do sistema")

    tabs = st.tabs(["Usuários", "Categorias"])

    with tabs[0]:
        col1, col2, col3 = st.columns([4, 1, 1], vertical_alignment="bottom")

        with col1:
            search_term = st.text_input(
                ":material/Search: Buscar",
                placeholder="Digite o ID ou nome do usuário...",
            )

        with col2:
            if st.button(":material/add: Cadastrar", type="primary", use_container_width=True, key="create_user_button"):
                create_user()

        with col3:
            st.session_state["edit_clicked"] = st.button(
                ":material/edit: Editar",
                use_container_width=True,
                help="Selecione um usuário na tabela para editar",
                key="edit_user_button",
            )

        query = """
            select
                id,
                first_name || ' ' || last_name as full_name,
                username,
                is_admin,
                pct_essential_expenses,
                pct_free_expenses,
                pct_investments,
                is_self_employed,
                is_active,
                last_login,
                created_at,
                updated_at
            from public.users
            order by id
        """
        df = select(query)

        if search_term:
            search_term_lower = search_term.lower()
            df = df[
                df.apply(
                    lambda row: (
                        search_term_lower in str(row["username"]).lower()
                        or search_term_lower in str(row["id"])
                    ),
                    axis=1,
                )
            ]

        if df.empty:
            st.info("Nenhum usuário encontrado.")
        else:
            COLUMN_CONFIG = {
                "full_name": st.column_config.TextColumn("Nome completo"),
                "username": st.column_config.TextColumn("Usuário"),
                "is_admin": st.column_config.CheckboxColumn("Administrador"),
                "pct_essential_expenses": st.column_config.NumberColumn("% gastos essenciais", format="%.2f"),
                "pct_free_expenses": st.column_config.NumberColumn("% gastos livres", format="%.2f"),
                "pct_investments": st.column_config.NumberColumn("% investimentos", format="%.2f"),
                "is_self_employed": st.column_config.CheckboxColumn("Autônomo"),
                "is_active": st.column_config.CheckboxColumn("Ativo"),
                "last_login": st.column_config.DatetimeColumn("Último login"),
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
                key="users_table",
            )

            if st.session_state.get("edit_clicked"):
                if event.selection.rows:
                    selected_index = event.selection.rows[0]
                    selected_user_id = df.iloc[selected_index]["id"]
                    user_data = select(f"SELECT * FROM public.users WHERE id = {selected_user_id}")
                    if not user_data.empty:
                        edit_user(user_data.iloc[0].to_dict())

    with tabs[1]:
        col1, col2, col3 = st.columns([4, 1, 1], vertical_alignment="bottom")

        with col1:
            search_term = st.text_input(
                ":material/Search: Buscar",
                placeholder="Digite o ID ou nome da categoria...",
            )

        with col2:
            if st.button(":material/add: Cadastrar", type="primary", use_container_width=True, key="create_category_button"):
                create_category()

        with col3:
            st.session_state["edit_clicked"] = st.button(
                ":material/edit: Editar",
                use_container_width=True,
                help="Selecione uma categoria na tabela para editar",
                key="edit_category_button",
            )

        query = """
            select
                id,
                name,
                is_expense,
                is_active,
                created_at,
                updated_at
            from public.categories
            order by id
        """
        df = select(query)

        if search_term:
            search_term_lower = search_term.lower()
            df = df[
                df.apply(
                    lambda row: (
                        search_term_lower in str(row["name"]).lower()
                        or search_term_lower in str(row["id"])
                    ),
                    axis=1,
                )
            ]

        if df.empty:
            st.info("Nenhuma categoria encontrada.")
        else:
            COLUMN_CONFIG = {
                "name": st.column_config.TextColumn("Categoria"),
                "is_expense": st.column_config.CheckboxColumn("Saída"),
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
                key="categories_table",
            )

            if st.session_state.get("edit_clicked"):
                if event.selection.rows:
                    selected_index = event.selection.rows[0]
                    selected_category_id = df.iloc[selected_index]["id"]
                    category_data = select(f"SELECT * FROM public.categories WHERE id = {selected_category_id}")
                    if not category_data.empty:
                        edit_category(category_data.iloc[0].to_dict())

except Exception as e:
    st.error(f"Erro ao carregar página: {e}")