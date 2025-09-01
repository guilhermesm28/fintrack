import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FINTRACK",
    page_icon="💲",
    layout="wide",
)

st.title("Planejamento Financeiro")
st.write("Descreva abaixo suas receitas e despesas fixas para calcular o saldo mensal.")

with st.expander("Dados"):
    tabs = st.tabs(["Receitas, Despesas e Planejamento de gastos", "Detalhamento de gastos fixos"])
    with tabs[0]:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            receitas = st.number_input("Receitas", min_value=0.0, format="%.2f")

        with col2:
            despesas = st.number_input("Despesas", min_value=0.0, format="%.2f")

        with col3:
            gastos_fixos = st.number_input("Gastos Fixos (%)", min_value=0.0, value= 40.0, format="%.2f")

        with col4:
            gastos_livres = st.number_input("Gastos Livres (%)", min_value=0.0, value= 30.0, format="%.2f")

        with col5:
            investimentos = st.number_input("Investimentos (%)", min_value=0.0, value= 30.0, format="%.2f")

    with tabs[1]:
        df_gastos_fixos = pd.DataFrame([{"Gasto": "Aluguel", "Valor": 1000.00}])
        df_gastos_fixos_edited = st.data_editor(df_gastos_fixos, width="stretch", hide_index=True, num_rows="dynamic")

with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de receitas", f"R$ {receitas:.2f}")
        st.metric("Investimentos sugeridos", f"R$ {receitas * investimentos / 100:.2f}",
                   help=f"R$ {receitas} * {investimentos}%")
    with col2:
        st.metric("Despesas fixas", f"R$ {despesas:.2f}")
        st.metric("Gastos fixos sugeridos", f"R$ {receitas * gastos_fixos / 100:.2f}",
                   help=f"R$ {receitas} * {gastos_fixos}%")
    with col3:
        st.metric("Saldo", f"R$ {receitas - despesas:.2f}")
        st.metric("Gastos livres sugeridos", f"R$ {receitas * gastos_livres / 100:.2f}",
                   help=f"R$ {receitas} * {gastos_livres}%")
