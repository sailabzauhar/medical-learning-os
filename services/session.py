import streamlit as st


def require_login():

    if "user_id" not in st.session_state:

        st.warning(
            "Please login first."
        )

        st.stop()


def get_user_id():

    return st.session_state["user_id"]


def get_email():

    return st.session_state["email"]