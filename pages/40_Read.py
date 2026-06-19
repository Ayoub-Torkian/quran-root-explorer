# -*- coding: utf-8 -*-
"""📖 Read — the primary reading surface. Pick a sūra and read it top to bottom
(original Arabic + your chosen translation), on phone or computer. The page scrolls
naturally (no nested box). Reuses the sūra engine + the shared translation/text-size
controls so a choice made here carries everywhere."""
import streamlit as st

import meaning as _MEAN
import mobile as _MOB
import surah_reader as _SR
from analysis import COL_SURAH, COL_SURAH_NAME
from state import get_corpus, hero, log_page

st.set_page_config(page_title="Read", page_icon="📖", layout="wide")
_MOB.inject()
log_page("read")
corpus = get_corpus()
df = corpus.df

hero("📖 Read the Qur'an",
     "Pick a sūra and read it top to bottom — original Arabic with your chosen translation.")

suras = sorted(set(df[COL_SURAH].astype(int)))
names = {}
_col_name = COL_SURAH_NAME if COL_SURAH_NAME in df.columns else COL_SURAH
for s, n in zip(df[COL_SURAH].astype(int), df[_col_name]):
    names.setdefault(int(s), str(n))

if "read_s" not in st.session_state:
    st.session_state["read_s"] = 1

# ── sūra navigation: prev / picker / next (buttons run before the picker so it stays in sync) ──
top = st.columns([1, 4, 1])
if top[0].button("◀ Prev", use_container_width=True):
    st.session_state["read_s"] = max(1, int(st.session_state["read_s"]) - 1)
if top[2].button("Next ▶", use_container_width=True):
    st.session_state["read_s"] = min(114, int(st.session_state["read_s"]) + 1)
sel = top[1].selectbox("Sūra", suras, index=suras.index(int(st.session_state["read_s"])),
                       format_func=lambda s: f"{s} · {names.get(s, '')}")
st.session_state["read_s"] = sel

# ── translation choice + text size (shared across the app) ──
_MP = _MEAN.translation_control(st)
_MOB.settings_controls(st)

# ── the whole sūra, inline (page scrolls) ──
st.markdown(_SR.inline_html(corpus, sel, _MP), unsafe_allow_html=True)

# ── bottom nav ──
b = st.columns(2)
if sel > 1 and b[0].button("← Previous sūra", use_container_width=True, key="prevb"):
    st.session_state["read_s"] = sel - 1; st.rerun()
if sel < 114 and b[1].button("Next sūra →", use_container_width=True, key="nextb"):
    st.session_state["read_s"] = sel + 1; st.rerun()
