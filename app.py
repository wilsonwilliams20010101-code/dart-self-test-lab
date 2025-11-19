import os
import importlib.util
import streamlit as st
from utils.ui import load_css, read_goto_param

# ------------------------------------------------------
# Streamlit setup
# ------------------------------------------------------
st.set_page_config(page_title="DART Self-Test Lab", page_icon="🍽️", layout="centered")

# Load global CSS
load_css()

# Router state
if "page" not in st.session_state:
    st.session_state.page = "home"

def go(page_key: str):
    st.session_state.page = page_key
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

# Check ?goto param
goto = read_goto_param()
if goto:
    go(goto)

# ------------------------------------------------------
# Page loader
# ------------------------------------------------------
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


# ------------------------------------------------------
# SIDEBAR (clean Apple-style)
# ------------------------------------------------------
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


# ------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------
if st.session_state.page == "home":

    # Apple hero
    st.markdown("""
    <section class="apple-hero apple-font">
      <h1>DART Self-Test Lab</h1>
      <p>Simple, guided checks for common adulteration — designed for families, inspired by FSSAI DART awareness.</p>
    </section>
    """, unsafe_allow_html=True)

    # CTA BUTTONS
    ccta1, ccta2 = st.columns(2)
    with ccta1:
        st.markdown('<button class="chime-btn" onclick="window.parent.postMessage({type:\'route\',page:\'test_library\'}, \'*\')">Start Testing</button>', unsafe_allow_html=True)
    with ccta2:
        st.markdown('<button class="chime-btn" onclick="window.parent.postMessage({type:\'route\',page:\'quiz\'}, \'*\')">Take a Quiz</button>', unsafe_allow_html=True)

    # >>>>>>>>>>>>>>>>>>>>  PASTE THE CARD SECTION HERE  <<<<<<<<<<<<<<<<<<<<<<<<
    st.markdown(
        """
        <section class="section gray apple-font" style="margin-top:20px">
          <div class="grid" style="align-items:start;">

            <a href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;"
               style="text-decoration:none; color:inherit;">
              <div class="card apple" role="button">
                <h3>Milk checks</h3>
                <p>Iodine test for starch, foam check for detergent, quick spread test for water.</p>
              </div>
            </a>

            <a href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;"
               style="text-decoration:none; color:inherit;">
              <div class="card apple" role="button">
                <h3>Spice purity</h3>
                <p>Detect added dyes or brick powder in turmeric and chilli powders.</p>
              </div>
            </a>

            <a href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;"
               style="text-decoration:none; color:inherit; grid-column: 1 / -1;">
              <div class="card apple" role="button">
                <h3>Honey basics</h3>
                <p>Water glass method to observe settling vs rapid dissolution.</p>
              </div>
            </a>

          </div>
        </section>
        """,
        unsafe_allow_html=True
    )
    # --------------------------
    # Glow buttons (final)
    # --------------------------
    st.markdown(
        """
        <div class="hero-btn-wrapper" style="max-width:620px;margin:0 auto;display:flex;gap:18px;justify-content:center;">
          
          <div class="chime-glow" style="flex:1;">
            <button class="chime-btn primary"
                onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*')">
                Start Testing
            </button>
          </div>

          <div class="chime-glow" style="flex:1;">
            <button class="chime-btn"
                onclick="window.parent.postMessage({type:'route',page:'quiz'}, '*')">
                Take a Quiz
            </button>
          </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    # Feature cards
    st.markdown(
        """
        <section class="section gray apple-font">
          <div class="grid">

            <div class="card apple">
              <h3>Milk checks</h3>
              <p>Iodine test for starch, foam check for detergent, quick spread test for water.</p>
            </div>

            <div class="card apple">
              <h3>Spice purity</h3>
              <p>Detect added dyes or brick powder in turmeric and chilli powders.</p>
            </div>

            <div class="card apple">
              <h3>Honey basics</h3>
              <p>Water glass method to observe settling vs rapid dissolution.</p>
            </div>

          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


# ------------------------------------------------------
# ROUTED PAGES
# ------------------------------------------------------
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
    st.rerun()
