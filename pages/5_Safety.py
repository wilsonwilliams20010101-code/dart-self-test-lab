import streamlit as st
from utils.ui import load_css, header, footer_nav

st.set_page_config(page_title="Safety & Disclaimer", page_icon="⚠️", layout="centered")
load_css()
header("Safety & Disclaimer", "Please read before performing any checks.")

st.markdown("""
- These are **basic household awareness checks** inspired by public DART-style guidance.
- They are **indicative only** and not a substitute for laboratory testing.
- Avoid hazardous chemicals at home; **do not ingest** any tested samples.
- For official standards or confirmation, seek **FSSAI advisories** and **accredited labs**.
""" )

footer_nav()
