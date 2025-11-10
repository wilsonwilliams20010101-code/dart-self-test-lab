import os
import streamlit as st

def is_admin() -> bool:
    default_pw = "admin123"
    secret_pw = st.secrets.get("ADMIN_PASSWORD", None) if hasattr(st, "secrets") else None
    env_pw = os.getenv("ADMIN_PASSWORD")
    expected = secret_pw or env_pw or default_pw
    token = st.session_state.get("admin_token")
    return token == expected

def login_form():
    st.write("### Admin Login")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        default_pw = "admin123"
        secret_pw = st.secrets.get("ADMIN_PASSWORD", None) if hasattr(st, "secrets") else None
        env_pw = os.getenv("ADMIN_PASSWORD")
        expected = secret_pw or env_pw or default_pw
        if pw == expected:
            st.session_state["admin_token"] = expected
            st.success("Logged in as admin.")
            st.rerun()
        else:
            st.error("Incorrect password.")
