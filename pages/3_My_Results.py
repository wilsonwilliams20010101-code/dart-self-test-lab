import streamlit as st
from utils.ui import load_css, header, footer_nav
from utils.data_manager import list_results

def render():
    load_css()
    header("My Results", "View and manage your saved household test logs.")

    results = list_results()
    if not results:
        st.info("No results yet. Go to Test Library to log your tests.")
    else:
        for r in sorted(results, key=lambda x: x.get('ts', ''), reverse=True):
            title = f"📌 {r.get('item')} — {r.get('outcome')}  ({r.get('ts')})"
            with st.expander(title):
                st.write(r.get("notes", ""))
                st.caption("Delete is disabled in this public build to avoid conflicting doc_id handling on Cloud.")
    footer_nav()
