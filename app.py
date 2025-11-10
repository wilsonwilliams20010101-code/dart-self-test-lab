import os
import importlib.util
import streamlit as st
from utils.ui import load_css, header, footer_nav

st.set_page_config(page_title="DART Self-Test Lab", page_icon="🍽️", layout="centered")

# --- simple router stored in session ---
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page_key: str):
    st.session_state.page = page_key
    st.experimental_rerun()

def load_and_render(page_filename: str):
    """Dynamically load a page module by its filename and call render()."""
    pages_dir = os.path.join(os.path.dirname(__file__), "pages")
    path = os.path.join(pages_dir, page_filename)
    if not os.path.exists(path):
        st.error(f"Page file not found: {page_filename}")
        return
    spec = importlib.util.spec_from_file_location("page_mod", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    if hasattr(mod, "render"):
        mod.render()
    else:
        st.error(f"`render()` not found in {page_filename}")

load_css()

# --------- HOME ----------
if st.session_state.page == "home":
    header("DART Self-Test Lab", "Household self-checks inspired by FSSAI DART awareness material.")

    col1, col2 = st.columns(2)
    with col1:
        st.button("🔎 Test Library", use_container_width=True, on_click=lambda: go("test_library"))
        st.button("🧪 Quiz", use_container_width=True, on_click=lambda: go("quiz"))
    with col2:
        st.button("📒 My Results", use_container_width=True, on_click=lambda: go("results"))
        st.button("⚙️ Admin", use_container_width=True, on_click=lambda: go("admin"))

    st.markdown(
        """
        <div class='card'>
        <h3>About</h3>
        <p>This app provides simple household awareness checks for common food adulteration scenarios.
        It is <b>not a diagnostic lab tool</b>. For confirmation and compliance, consult accredited labs and official advisories.</p>
        <p class='small-muted'>Source inspiration: public food safety awareness materials and common home checks aligned with DART-style guides.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    footer_nav()

# --------- ROUTED PAGES ----------
elif st.session_state.page == "test_library":
    load_and_render("1_Test_Library.py")
elif st.session_state.page == "quiz":
    load_and_render("2_Quiz.py")
elif st.session_state.page == "results":
    load_and_render("3_My_Results.py")
elif st.session_state.page == "admin":
    load_and_render("4_Admin_Panel.py")
else:
    st.session_state.page = "home"
    st.experimental_rerun()
