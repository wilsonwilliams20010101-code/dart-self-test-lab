import os
import streamlit as st

def load_css():
    css_path = os.path.join("assets", "style.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception:
        st.markdown("<style>.block-container{max-width:1024px}</style>", unsafe_allow_html=True)

def header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class='card' style="padding:18px 16px;">
          <h2 style="margin:0 0 6px 0;">{title}</h2>
          <p class='small-muted' style="margin:0;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True
    )

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
        """, unsafe_allow_html=True
    )

def top_nav_home_only():
    """Apple-like hero + CTAs (home page only)."""
    st.markdown(
        """
        <section class="apple-hero apple-font">
          <h1>DART Self-Test Lab</h1>
          <p>Simple, guided checks for common adulteration — designed for families, inspired by FSSAI DART awareness.</p>
          <a class="apple-cta primary" href="?goto=test_library">Start Testing</a>
          <a class="apple-cta" href="?goto=quiz">Take a Quiz</a>
        </section>
        """, unsafe_allow_html=True
    )

def read_goto_param():
    goto = None
    try:
        goto = st.query_params.get("goto")
    except Exception:
        qp = st.experimental_get_query_params()
        goto = (qp.get("goto", [None]) or [None])[0]
    if goto:
        try:
            st.query_params.clear()
        except Exception:
            st.experimental_set_query_params()
    return goto