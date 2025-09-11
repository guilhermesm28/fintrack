import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@st.cache_resource
def get_engine():
    db_url = st.secrets["database"]["url"]
    return create_engine(db_url)

def get_session():
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    return SessionLocal()
