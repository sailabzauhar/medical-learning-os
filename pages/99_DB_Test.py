import streamlit as st

from services.db import get_connection

st.title("PostgreSQL Test")

try:

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("SELECT version();")

    version = cur.fetchone()

    st.success("Connected Successfully")

    st.write(version)

    cur.close()
    conn.close()

except Exception as e:

    st.error(str(e))