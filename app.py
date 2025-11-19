import os
import importlib.util
import streamlit as st
from utils.ui import load_css, read_goto_param

# -----------------------
# App config + CSS
# -----------------------
st.set_page_config(page_title="DART Self-Test Lab", page_icon="🍽️", layout="centered")
load_css()  # ensure your CSS defines .chime-btn, .chime-glow, .card.apple, etc.

# -----------------------
# Router state
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page_key: str):
    st.session_state.page = page_key
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

# support ?goto=page query param
goto = read_goto_param()
if goto:
    go(goto)

# -----------------------
# Page loader helper
# -----------------------
def load_and_render(page_filename: str):
    pages_dir = os.path.join(os.path.dirname(__file__), "pages")
    path = os.path.join(pages_dir, page_filename)

    if not os.path.exists(path):
        st.error(f"Page not found: {page_filename}")
        return

    spec = importlib.util.spec_from_file_location("page_mod", path)
    if spec is None or spec.loader is None:
        st.error("Failed to load module spec.")
        return

    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    if hasattr(mod, "render"):
        mod.render()
    else:
        st.error(f"`render()` missing in {page_filename}")

# -----------------------
# Sidebar
# -----------------------
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
    }
    labels = list(label_map.keys())
    current_label = next((k for k, v in label_map.items() if v == st.session_state.page), "Home")
    sel = st.radio(" ", labels, index=labels.index(current_label), key="side_nav")
    if label_map[sel] != st.session_state.page:
        go(label_map[sel])

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------
# HOME page
# -----------------------
if st.session_state.page == "home":
    # Hero
    st.markdown(
        """
        <section class="apple-hero apple-font">
          <h1>DART Self-Test Lab</h1>
          <p>Simple, guided checks for common adulteration — designed for families, inspired by FSSAI DART awareness.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    # Glow CTA buttons (single authoritative source of truth)
    st.markdown(
        """
        <div class="hero-btn-wrapper" style="max-width:760px;margin:10px auto 28px;display:flex;gap:24px;justify-content:center;flex-wrap:wrap;">
          <div class="chime-glow" style="flex:1;min-width:220px;">
            <button class="chime-btn primary" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*')">Start Testing</button>
          </div>

          <div class="chime-glow" style="flex:1;min-width:220px;">
            <button class="chime-btn" onclick="window.parent.postMessage({type:'route',page:'quiz'}, '*')">Take a Quiz</button>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Clickable feature cards (renders using your .card.apple CSS)
    st.markdown(
        """
        <section class="section gray apple-font" style="margin-top:8px;">
          <div class="grid" style="align-items:start;">

            <a href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;"
               style="text-decoration:none; color:inherit;">
              <div class="card apple" role="button" aria-label="Milk checks — open test library">
                <h3>Milk checks</h3>
                <p>Iodine test for starch, foam check for detergent, quick spread test for water.</p>
              </div>
            </a>

            <a href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;"
               style="text-decoration:none; color:inherit;">
              <div class="card apple" role="button" aria-label="Spice purity — open test library">
                <h3>Spice purity</h3>
                <p>Detect added dyes or brick powder in turmeric and chilli powders.</p>
              </div>
            </a>

            <a href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;"
               style="text-decoration:none; color:inherit; grid-column:1 / -1;">
              <div class="card apple" role="button" aria-label="Honey basics — open test library">
                <h3>Honey basics</h3>
                <p>Water glass method to observe settling vs rapid dissolution.</p>
              </div>
            </a>

          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

# -----------------------
# Routed pages
# -----------------------
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
