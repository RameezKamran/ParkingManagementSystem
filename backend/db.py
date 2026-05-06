import streamlit as st
import oracledb

def get_connection():
    conn = oracledb.connect(
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        dsn=st.secrets["DB_DSN"]
    )
    return conn
