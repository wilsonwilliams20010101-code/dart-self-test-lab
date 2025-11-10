# utils/ui.py
import os
import streamlit as st

# ---------- CSS loader ----------
def load_css():
    """Inject assets/style.css if present (no crash if missing)."""
    css_path = os.path.join("assets", "style.css")
    css = ""
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
    except Exception:
        # fallback minimal readable defaults
        css = """
        <style>
          .block-container{max-width:1024px;}
          .card{background:#fff;border:1px solid rgba(0,0,0,.08);border-radius:16px;padding:16px;}
          .small-muted{color:#666;}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
        return
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ---------- Header ----------
def header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class='card' style="padding:18px 16px;">
          <h2 style="margin:0 0 6px 0;">{title}</h2>
          <p class='small-muted' style="margin:0;">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Footer (bottom nav) ----------
def footer_nav():
    st.markdown(
        """
        <div class="footer-nav">
          <div class="wrap">
            <a href="?goto=test_library">🔎 Tests</a>
            <a href="?goto=quiz">🧪 Quiz</a>
            <a href="?goto=results">📒 Results</a>
            <a href="?goto=admin">⚙️ Admin</a>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- Apple-like Top Navbar ----------
def top_nav(go):
    """
    Sticky, Apple-style top navbar. Uses a tiny query-param bridge to
    trigger your router without custom components.
    """
    st.markdown(
        """
        <div class="apple-nav apple-font">
          <div class="wrap">
            <div class="brand">DART</div>
            <div class="links">
              <a class="link" href="?goto=test_library">Tests</a>
              <a class="link" href="?goto=quiz">Quiz</a>
              <a class="link" href="?goto=results">Results</a>
              <a class="link" href="?goto=admin">Admin</a>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Read & clear ?goto param, then call your router
    goto = None
    try:
        # Streamlit ≥1.30
        goto = st.query_params.get("goto")
    except Exception:
        # Older API fallback
        qp = st.experimental_get_query_params()
        goto = (qp.get("goto", [None]) or [None])[0]

    if goto:
        # Clear param to avoid loops
        try:
            st.query_params.clear()
        except Exception:
            st.experimental_set_query_params()  # clears all
        go(goto)
