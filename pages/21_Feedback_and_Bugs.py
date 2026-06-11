"""Feedback, Bugs & Ideas — v1.4 user-signal page."""
import streamlit as st

import state as S
import feedback as FB

st.set_page_config(page_title="Feedback & Bugs", page_icon="💬", layout="wide")
S.log_page("feedback")
try:
    S.inject_css()
except Exception:
    pass
try:
    S.render_grouped_nav()
except Exception:
    pass

FB.render_feedback_page()
