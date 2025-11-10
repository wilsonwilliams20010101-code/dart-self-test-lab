import streamlit as st

ADMIN_PASS = st.secrets.get("ADMIN_PASS", "admin")

def is_admin():
    return st.session_state.get("is_admin", False)

def login_form():
    st.subheader("Admin login")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == ADMIN_PASS:
            st.session_state["is_admin"] = True
            st.success("Logged in.")
            st.rerun()
        else:
            st.error("Wrong password.")