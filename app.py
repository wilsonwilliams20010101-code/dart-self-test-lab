import streamlit as st
from utils.ui import load_css, header, footer_nav

st.set_page_config(page_title="DART Self-Test Lab", page_icon="🍽️", layout="centered")

load_css()
header("DART Self-Test Lab", "Household self-checks inspired by FSSAI DART awareness material.")

col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_Test_Library.py", label="🔎 Test Library", help="Search food items & steps")
    st.page_link("pages/2_Quiz.py", label="🧪 Quiz", help="Test your knowledge")
with col2:
    st.page_link("pages/3_My_Results.py", label="📒 My Results", help="Saved logs")
    st.page_link("pages/4_Admin_Panel.py", label="⚙️ Admin", help="Manage content")

st.markdown("""
<div class='card'>
<h3>About</h3>
<p>This app provides simple household awareness checks for common food adulteration scenarios.
It is <b>not a diagnostic lab tool</b>. For confirmation and compliance, consult accredited labs and official advisories.</p>
<p class='small-muted'>Source inspiration: Public food safety awareness materials and common home checks aligned with DART-style guides.</p>
</div>
""", unsafe_allow_html=True)

footer_nav()
