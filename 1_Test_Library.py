import streamlit as st
from utils.ui import load_css, header, footer_nav
from utils.data_manager import load_tests, log_result

st.set_page_config(page_title="Test Library", page_icon="🔎", layout="centered")
load_css()
header("Test Library", "Find food items, suspected adulterants, and step-by-step checks.")

tests = load_tests()
categories = sorted(set(t["category"] for t in tests)) if tests else []
q = st.text_input("Search by food item or adulterant", placeholder="e.g., milk, turmeric, starch...", help="Type to filter results")
cat = st.selectbox("Category", ["All"] + categories, index=0) if categories else "All"

def match(t):
    if cat != "All" and t["category"] != cat: return False
    if not q: return True
    hay = " ".join([t["item"]] + t.get("adulterants", [])).lower()
    return q.lower() in hay

filtered = [t for t in tests if match(t)] if tests else []

for t in filtered:
    with st.expander(f"🗂️ {t['item']} — {t['category']}"):
        st.markdown(f"""
        <div class='card'>
        <div><span class='badge'>Adulterants</span> {', '.join(t.get('adulterants', []))}</div>
        <div><span class='badge'>Materials</span> {', '.join(t.get('materials', []))}</div>
        <hr/>
        <ol>
        {''.join([f'<li>{step}</li>' for step in t.get('steps', [])])}
        </ol>
        <p class='small-muted'>Safety: {t.get('safety', 'Use basic caution')}</p>
        </div>
        """, unsafe_allow_html=True)
        with st.form(f"log_{t['item']}"):
            outcome = st.selectbox("Outcome", ["Not tested", "Likely Pure/OK", "Suspected Adulteration"])
            notes = st.text_input("Notes (optional)", placeholder="Observed color change, particles, etc.")
            if st.form_submit_button("Save to My Results"):
                log_result(t["item"], outcome, notes)
                st.success("Saved to My Results.")

if not filtered:
    st.info("No results. Try another search term or category.")

footer_nav()
