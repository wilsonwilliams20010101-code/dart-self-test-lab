import os
import importlib.util
import streamlit as st
from utils.ui import load_css, header, footer_nav, read_goto_param

st.set_page_config(page_title="DART Self-Test Lab", page_icon="🍽️", layout="centered")

# Load global CSS
load_css()

# Router state
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page_key: str):
    """Set page and rerun Streamlit to navigate."""
    st.session_state.page = page_key
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

# If app is opened with ?goto=page_key, navigate there
goto = read_goto_param() if "read_goto_param" in globals() or "read_goto_param" in dir() else None
if goto:
    go(goto)

# Safe module loader (fixed)
def load_and_render(page_filename: str):
    """Dynamically load a page module by its filename and call render()."""
    pages_dir = os.path.join(os.path.dirname(__file__), "pages")
    path = os.path.join(pages_dir, page_filename)
    if not os.path.exists(path):
        st.error(f"Page file not found: {page_filename}")
        return

    spec = importlib.util.spec_from_file_location("page_mod", path)
    if spec is None or spec.loader is None:
        st.error("Unable to load page spec.")
        return

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod, "render"):
        mod.render()
    else:
        st.error(f"`render()` not found in {page_filename}")

# ---------------- Sidebar (clean, no Amazon/Chime tile) ----------------
with st.sidebar:
    st.markdown("<div class='apple-sidebar-title'>Menu</div>", unsafe_allow_html=True)
    st.markdown("<div class='apple-sidebar-note'>Navigate</div>", unsafe_allow_html=True)

    label_map = {
        "Home": "home",
        "Test Library": "test_library",
        "Quiz": "quiz",
        "My Results": "results",
        "Admin Panel": "admin"
    }

    labels = list(label_map.keys())
    current_label = next((k for k, v in label_map.items() if v == st.session_state.page), "Home")
    sel = st.radio(" ", labels, index=labels.index(current_label), key="apple_side_nav")

    if label_map[sel] != st.session_state.page:
        go(label_map[sel])

# ---------------- HOME ----------------
if st.session_state.page == "home":
    # Hero
    st.markdown("""
    <section class="apple-hero apple-font" style="padding-top:18px;padding-bottom:6px;">
      <h1>DART Self-Test Lab</h1>
      <p>Simple, guided checks for common adulteration — designed for families, inspired by FSSAI DART awareness.</p>
    </section>
    """, unsafe_allow_html=True)

    # Two chime-styled CTA buttons (HTML + postMessage routing)
    c1, c2 = st.columns([1,1], gap="large")
    with c1:
        st.markdown(
            '<button class="chime-btn" onclick="window.parent.postMessage({type:\'route\',page:\'test_library\'}, \'*\')">Start Testing</button>',
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            '<button class="chime-btn" onclick="window.parent.postMessage({type:\'route\',page:\'quiz\'}, \'*\')">Take a Quiz</button>',
            unsafe_allow_html=True
        )

    # Feature cards
    st.markdown("""
    <section class="section gray apple-font" style="margin-top:20px">
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

# ---------------- Routed pages ----------------
elif st.session_state.page == "test_library":
    load_and_render("1_Test_Library.py")
elif st.session_state.page == "quiz":
    load_and_render("2_Quiz.py")
elif st.session_state.page == "results":
    load_and_render("3_My_Results.py")
elif st.session_state.page == "admin":
    load_and_render("4_Admin_Panel.py")
else:
    # fallback
    st.session_state.page = "home"
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()
