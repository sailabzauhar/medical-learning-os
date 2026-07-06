import streamlit as st

from services.auth_service import (
    sign_in,
    sign_up
)

st.set_page_config(
    page_title="Login"
)

st.title("🔐 Learning OS Login")

tab1, tab2 = st.tabs([
    "Login",
    "Register"
])

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

with tab1:

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login"):

        try:

            result = sign_in(
                email,
                password
            )

            st.session_state[
                "user_id"
            ] = result.user.id

            st.session_state[
                "email"
            ] = result.user.email

            st.success(
                "Login successful"
            )

            st.rerun()

        except Exception as e:

            st.error(str(e))

# --------------------------------------------------
# REGISTER
# --------------------------------------------------

with tab2:

    email = st.text_input(
        "Email",
        key="register_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    if st.button("Register"):

        try:

            sign_up(
                email,
                password
            )

            st.success(
                "Account created"
            )

        except Exception as e:

            st.error(str(e))

