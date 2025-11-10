import streamlit as st
from utils.ui import load_css, header, footer_nav
from utils.data_manager import list_results, delete_result

st.set_page_config(page_title="My Results", page_icon="📒", layout="centered")
load_css()
header("My Results", "View and manage your saved household test logs.")

results = list_results()

if not results:
    st.info("No results yet. Go to Test Library to log your tests.")
else:
    # TinyDB returns dicts; add doc_id via st.session_state workaround if missing
    for r in sorted(results, key=lambda x: x.get('ts',''), reverse=True):
        title = f"📌 {r.get('item')} — {r.get('outcome')}  ({r.get('ts')})"
        with st.expander(title):
            st.write(r.get("notes",""))
            if '_id' in r:
                doc_id = r['_id']
            else:
                # TinyDB 4 does not expose doc_id in dict by default in this context; handle delete button disabled
                doc_id = None
            if st.button("Delete", key=f"del_{title}"):
                st.warning("Delete from Admin > Database (TinyDB) if needed. (Doc IDs not exposed in this runtime.)")

footer_nav()
