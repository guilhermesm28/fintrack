import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")
st.title("Planejamento financeiro")

with st.container(border=True):
    tabs = st.tabs(["Receitas e planejamento", "Detalhamento de despesas"])
    with tabs[0]:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            receitas = st.number_input("Receitas", min_value=0.0, format="%.2f")
        with col2:
            gastos_fixos = st.number_input("Gastos Fixos (%)", min_value=0.0, value=40.0, format="%.2f")
        with col3:
            gastos_livres = st.number_input("Gastos Livres (%)", min_value=0.0, value=30.0, format="%.2f")
        with col4:
            investimentos = st.number_input("Investimentos (%)", min_value=0.0, value=30.0, format="%.2f")

with tabs[1]:
    df_gastos_fixos = pd.DataFrame([{"Despesa": "Descreva a despesa", "Valor": 0.0}])
    df_gastos_fixos_edited = st.data_editor(df_gastos_fixos, width="stretch", hide_index=True, num_rows="dynamic")
    despesas = df_gastos_fixos_edited["Valor"].sum() if df_gastos_fixos_edited is not None else 0

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
