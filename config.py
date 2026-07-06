import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = (
    st.secrets.get("SUPABASE_URL")
    or os.getenv("SUPABASE_URL")
)

SUPABASE_KEY = (
    st.secrets.get("SUPABASE_ANON_KEY")
    or os.getenv("SUPABASE_ANON_KEY")
)

POSTGRES_HOST = (
    st.secrets.get("POSTGRES_HOST")
    or os.getenv("POSTGRES_HOST")
)

POSTGRES_PORT = (
    st.secrets.get("POSTGRES_PORT")
    or os.getenv("POSTGRES_PORT")
)

POSTGRES_DB = (
    st.secrets.get("POSTGRES_DB")
    or os.getenv("POSTGRES_DB")
)

POSTGRES_USER = (
    st.secrets.get("POSTGRES_USER")
    or os.getenv("POSTGRES_USER")
)

POSTGRES_PASSWORD = (
    st.secrets.get("POSTGRES_PASSWORD")
    or os.getenv("POSTGRES_PASSWORD")
)

# ---------- TEMP DEBUG ----------

print("SUPABASE_URL:", bool(SUPABASE_URL))
print("SUPABASE_KEY:", bool(SUPABASE_KEY))
print("POSTGRES_HOST:", bool(POSTGRES_HOST))
print("POSTGRES_USER:", bool(POSTGRES_USER))