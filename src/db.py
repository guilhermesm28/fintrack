import streamlit as st
from sqlalchemy import create_engine

@st.cache_resource
def get_engine():
    db_url = st.secrets["database"]["url"]
    engine = create_engine(db_url)
    return engine