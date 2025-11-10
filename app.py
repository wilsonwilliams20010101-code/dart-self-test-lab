import streamlit as st
from utils.ui import load_css, header, footer_nav

st.set_page_config(page_title="DART Self-Test Lab", page_icon="🍽️", layout="centered")

load_css()
header("DART Self-Test Lab", "Household self-checks inspired by FSSAI DART awareness material.")

# --- Mobile-friendly navigation using buttons + switch_page ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🔎 Test Library"):
        st.switch_page("pages/1_Test_Library.py")
    if st.button("🧪 Quiz"):
        st.switch_page("pages/2_Quiz.py")
with col2:
    if st.button("📒 My Results"):
        st.switch_page("pages/3_My_Results.py")
    if st.button("⚙️ Admin"):
        st.switch_page("pages/4_Admin_Panel.py")

st.markdown(
    """
    <div class='card'>
    <h3>About</h3>
    <p>This app provides simple household awareness checks for common food adulteration scenarios.
    It is <b>not a diagnostic lab tool</b>. For confirmation and compliance, consult accredited labs and official advisories.</p>
    <p class='small-muted'>Source inspiration: Public food safety awareness materials and common home checks aligned with DART-style guides.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

footer_nav()
