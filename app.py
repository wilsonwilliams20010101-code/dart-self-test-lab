import os
import importlib.util
import streamlit as st
from utils.ui import load_css, header, footer_nav, top_nav

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
    # Apple typography wrapper
    st.markdown("<div class='apple-font'>", unsafe_allow_html=True)

    # Sticky nav (links call your router)
    st.markdown("""
    <div class="apple-nav"><div class="wrap">
      <div class="brand">DART</div>
      <div class="links">
        <a href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;">Tests</a>
        <a href="#" onclick="window.parent.postMessage({type:'route',page:'quiz'}, '*'); return false;">Quiz</a>
        <a href="#" onclick="window.parent.postMessage({type:'route',page:'results'}, '*'); return false;">Results</a>
        <a href="#" onclick="window.parent.postMessage({type:'route',page:'admin'}, '*'); return false;">Admin</a>
      </div>
    </div></div>
    """, unsafe_allow_html=True)

    # JS bridge to call your router from anchor clicks
    st.markdown("""
    <script>
    window.addEventListener('message', (e)=>{
      const d = e.data||{};
      if(d.type==='route' && d.page){
        const streamlitSet = window.parent.Streamlit?.setComponentValue;
        // Fallback: use query params trigger
        const qs = new URLSearchParams(window.location.search);
        qs.set('goto', d.page);
        window.location.search = qs.toString();
      }
    });
    </script>
    """, unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <section class="apple-hero">
      <div class="eyebrow">Household Food Safety</div>
      <h1>DART Self-Test Lab</h1>
      <p class="sub">Simple, guided checks for common adulteration — designed for families, inspired by FSSAI DART awareness.</p>
      <a class="apple-cta primary" href="#" onclick="window.parent.postMessage({type:'route',page:'test_library'}, '*'); return false;">Start Testing</a>
      <a class="apple-cta" href="#" onclick="window.parent.postMessage({type:'route',page:'quiz'}, '*'); return false;">Take a Quiz</a>
    </section>
    """, unsafe_allow_html=True)

    # Feature cards
    st.markdown("""
    <section class="section gray">
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
    """, unsafe_allow_html=True)

    # Simple button grid (still works with your router)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔎 Tests", use_container_width=True): go("test_library")
        if st.button("🧪 Quiz", use_container_width=True): go("quiz")
    with c2:
        if st.button("📒 My Results", use_container_width=True): go("results")
        if st.button("⚙️ Admin", use_container_width=True): go("admin")

    st.markdown("</div>", unsafe_allow_html=True)  # end apple-font

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
