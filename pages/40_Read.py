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

# ── STICKY sūra navigation: stays pinned at the top of the screen while you scroll, so
#    you can jump to ANY sūra from ANY āyah without scrolling back to the top ──
st.markdown(
    "<style>"
    # sticky must sit on the wrapper that is a CHILD of the tall content block, not the
    # inner horizontal block (whose parent is only nav-height → zero sticky travel).
    "[data-testid='stLayoutWrapper']:has(.rdnav),"
    "[data-testid='stVerticalBlock'] > [data-testid='stElementContainer']:has(.rdnav){"
    "position:sticky;top:0;z-index:60;background:#FBFCFE;padding:6px 6px 2px;margin:-4px 0 6px;"
    "box-shadow:0 5px 12px rgba(16,36,58,.10);border-radius:0 0 12px 12px}"
    ":has(>.rdnav),.rdnav{margin:0}"
    "[data-testid='stLayoutWrapper']:has(.rdnav) .stButton button{min-height:40px}"
    "</style>", unsafe_allow_html=True)
top = st.columns([1, 4, 1])
top[1].markdown("<div class='rdnav'></div>", unsafe_allow_html=True)
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
