# app.py — clean order + Apple navbar + sidebar

import os
import importlib.util
import streamlit as st
from utils.ui import load_css, header, footer_nav, top_nav

st.set_page_config(page_title="DART Self-Test Lab", page_icon="🍽️", layout="centered")

# 1) Load global CSS
load_css()

# 2) Router state
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page_key: str):
    st.session_state.page = page_key
    try:
        st.rerun()              # Streamlit ≥1.30
    except Exception:
        st.experimental_rerun() # fallback

# 3) Top Apple-like navbar (works on all pages)
top_nav(go)

# 4) Helper to load page modules (expects pages/<file>.py with render())
def load_and_render(page_filename: str):
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

# 5) Apple-styled sidebar menu (kept, not hidden)
with st.sidebar:
    st.markdown("<div class='apple-sidebar-title'>Menu</div>", unsafe_allow_html=True)
    st.markdown("<div class='apple-sidebar-note'>Navigate</div>", unsafe_allow_html=True)
    st.markdown("<div class='apple-sidenav'>", unsafe_allow_html=True)

    label_map = {
        "Home": "home",
        "Test Library": "test_library",
        "Quiz": "quiz",
        "My Results": "results",
        "Admin Panel": "admin",
        # "Safety": "safety",  # add back if you have this page
    }
    labels = list(label_map.keys())
    current_label = next((k for k, v in label_map.items() if v == st.session_state.page), "Home")
    sel = st.radio(" ", labels, index=labels.index(current_label), key="apple_side_nav")
    if label_map[sel] != st.session_state.page:
        go(label_map[sel])

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HOME ----------------
if st.session_state.page == "home":
    # Apple hero (simple, no JS)
    st.markdown("""
    <section class="apple-hero apple-font">
      <h1>DART Self-Test Lab</h1>
      <p>Simple, guided checks for common adulteration — designed for families, inspired by FSSAI DART awareness.</p>
      <a class="apple-cta primary" href="#" id="cta-tests">Start Testing</a>
      <a class="apple-cta" href="#" id="cta-quiz">Take a Quiz</a>
    </section>
    """, unsafe_allow_html=True)

    # Buttons as fallback (always work)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔎 Tests", use_container_width=True): go("test_library")
        if st.button("🧪 Quiz", use_container_width=True): go("quiz")
    with c2:
        if st.button("📒 My Results", use_container_width=True): go("results")
        if st.button("⚙️ Admin", use_container_width=True): go("admin")

    # Feature cards
    st.markdown("""
    <section class="section gray apple-font">
      <div class="grid">
        <div class="card apple"><h3>Milk checks</h3>
          <p>Iodine test for starch, foam check for detergent, quick spread test for water.</p></div>
        <div class="card apple"><h3>Spice purity</h3>
          <p>Detect added dyes or brick powder in turmeric and chilli powders.</p></div>
        <div class="card apple"><h3>Honey basics</h3>
          <p>Water glass method to observe settling vs rapid dissolution.</p></div>
      </div>
    </section>
    """, unsafe_allow_html=True)

    footer_nav()

# --------------- ROUTED PAGES ---------------
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
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()
