import streamlit as st

st.set_page_config(layout="wide")
st.title("Página inicial")

st.write(f"Olá, {st.session_state.get('fullname')}!")
st.write("Bem-vindo ao FINTRACK, sua ferramenta de planejamento financeiro pessoal.")
