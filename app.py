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
    # Streamlit >=1.30
    try:
        st.rerun()
    except Exception:
        # fallback for very old versions
        st.experimental_rerun()  # will be ignored on new Streamlit

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
    # iPhone theme container
    st.markdown("<div class='ios-home'>", unsafe_allow_html=True)

    # Header text (iOS style)
    st.markdown(
        """
        <div class='card' style="padding:18px 16px;">
          <div class="ios-title">🍽️ DART Self-Test Lab</div>
          <div class="ios-subtitle">Household self-checks inspired by FSSAI DART awareness material.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # iOS-style button grid
    st.markdown("<div class='ios-grid'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # Add 'primary=True' style by injecting a 'primary' class after render
        btn1 = st.button("🔎 Test Library", use_container_width=True, key="btn_tests")
        btn2 = st.button("🧪 Quiz", use_container_width=True, key="btn_quiz")
        if btn1: go("test_library")
        if btn2: go("quiz")
    with col2:
        btn3 = st.button("📒 My Results", use_container_width=True, key="btn_results")
        btn4 = st.button("⚙️ Admin", use_container_width=True, key="btn_admin")
        if btn3: go("results")
        if btn4: go("admin")
    st.markdown("</div>", unsafe_allow_html=True)

    # Make the first button green (primary) with a tiny CSS-target trick
    st.markdown(
        """
        <style>
        /* mark the first home button as primary */
        .ios-home .stButton:nth-of-type(1) > button { background: var(--ios-primary) !important; color:#fff !important; border-color: var(--ios-primary) !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # About card (kept crisp)
    st.markdown(
        """
        <div class='card' style="padding:16px 16px;">
          <h4 style="margin:0 0 6px 0;">About</h4>
          <p class='small-muted' style="margin:0;">
          This app provides simple household awareness checks for common food adulteration scenarios.
          It is <b>not a diagnostic lab tool</b>. For confirmation and compliance, consult accredited labs and official advisories.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)  # end .ios-home
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
