import os

from dotenv import load_dotenv

try:
    import streamlit as st
except ImportError:
    st = None

load_dotenv()


def get_secret(name: str):

    if st is not None:

        try:

            if name in st.secrets:
                return st.secrets[name]

        except Exception:
            pass

    return os.getenv(name)


# ==================================================
# SUPABASE
# ==================================================

SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_ANON_KEY")


# ==================================================
# POSTGRES
# ==================================================

POSTGRES_HOST = get_secret("POSTGRES_HOST")
POSTGRES_PORT = get_secret("POSTGRES_PORT")
POSTGRES_DB = get_secret("POSTGRES_DB")
POSTGRES_USER = get_secret("POSTGRES_USER")
POSTGRES_PASSWORD = get_secret("POSTGRES_PASSWORD")