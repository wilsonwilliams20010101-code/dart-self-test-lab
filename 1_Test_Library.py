import time, difflib
import streamlit as st
from utils.ui import load_css, header, footer_nav
from utils.data_manager import load_tests, log_result

def render():
    load_css()
    header("Test Library", "Find food items, suspected adulterants, and step-by-step checks.")

    tests = load_tests()
    categories = sorted({t["category"] for t in tests}) if tests else []
    q = st.text_input("Search by food item or adulterant", placeholder="e.g., milk, turmeric, starch...")
    cat = st.selectbox("Category", ["All"] + categories, index=0) if categories else "All"

    def haystack(t):
        parts = [t["item"]] + t.get("adulterants", []) + t.get("materials", []) + t.get("tags", [])
        return " ".join(parts).lower()

    def match(t):
        if cat != "All" and t["category"] != cat: return False
        if not q: return True
        text = q.lower().strip()
        hay = haystack(t)
        if text in hay: return True
        return difflib.SequenceMatcher(None, text, hay).ratio() > 0.55

    filtered = [t for t in tests if match(t)] if tests else []
    if not filtered:
        st.info("No results. Try another search term or category.")
        footer_nav(); return

    if "t_start" not in st.session_state: st.session_state.t_start = None
    if "active_test" not in st.session_state: st.session_state.active_test = None

    for t in filtered:
        with st.expander(f"🗂️ {t['item']} — {t['category']}", expanded=False):
            st.markdown(
                f"""
                <div class='card'>
                <div><span class='badge'>Adulterants</span> {', '.join(t.get('adulterants', []))}</div>
                <div><span class='badge'>Materials</span> {', '.join(t.get('materials', []))}</div>
                <p class='small-muted'>Safety: {t.get('safety','Use basic caution')}</p>
                </div>
                """, unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("▶️ Start", key=f"start_{t['item']}"):
                    st.session_state.active_test = t['item']
                    st.session_state.t_start = time.time()
            with c2:
                if st.button("⏹ Stop", key=f"stop_{t['item']}"):
                    st.session_state.active_test = None

            with c3:
                if st.session_state.t_start and st.session_state.active_test == t['item']:
                    elapsed = int(time.time() - st.session_state.t_start)
                    st.markdown(f"**⏱ {elapsed}s**")
                else:
                    st.write("")

            st.write("### Steps")
            for i, step in enumerate(t.get("steps", []), start=1):
                st.markdown(f"<div class='step'><div class='num'>{i}</div><div>{step}</div></div>", unsafe_allow_html=True)

            st.write("### Save Observation")
            with st.form(f"log_{t['item']}"):
                outcome = st.selectbox("Outcome", ["Not tested", "Likely Pure/OK", "Suspected Adulteration"])
                confidence = st.slider("Confidence", 0, 100, 70)
                notes = st.text_input("Notes (optional)", placeholder="Observed color change, foam, sediment, etc.")
                submit = st.form_submit_button("Save to My Results")
                if submit:
                    duration = None
                    if st.session_state.t_start and st.session_state.active_test in (t['item'], None):
                        duration = int(time.time() - st.session_state.t_start)
                    log_result(t["item"], outcome, notes, confidence=confidence, duration_sec=duration or 0)
                    st.success("Saved to My Results ✅")
    footer_nav()