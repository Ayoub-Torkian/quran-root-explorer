# -*- coding: utf-8 -*-
"""🪜 Structure Map — structure at every scale (āyah · passage · sūra · Qur'ān).

Each scale uses the method that survives it (co-occurrence saturates above the āyah), every one
measured against the text's own shuffle. Engine: structure_scales.py. Research dossier:
research/intrinsic/MULTISCALE_STRUCTURE.md.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

import structure_scales as SS
import surah_reader as _SR
import meaning as _MEAN
import mobile as _MOB
from state import get_corpus, hero, layer, log_page

st.set_page_config(page_title="Structure Map", page_icon="🪜", layout="wide")
log_page("structure_map")
_MOB.inject()                       # Qur'an webfonts so the ORIGINAL text renders correctly
corpus = get_corpus()

hero("🪜 Structure Map — every scale",
     "Āyah · passage · sūra · whole Qur'ān — each measured with the method that fits it, vs the text's own shuffle.")

st.markdown(
    "<div style='background:#F4F9F7;border:1px solid #cfe4dc;border-radius:10px;padding:10px 14px;"
    "font-size:13.5px;color:#10243A;line-height:1.7;margin:2px 0 8px'>"
    "Co-occurrence <b>saturates</b> as the window grows (triad closure 53% → 98% → 100% from āyah to "
    "sūra), so one method cannot span scales. Here each scale gets its own robust instrument: "
    "<b>āyah</b> = frequency-controlled bonds (NPMI); <b>passage</b> = sequential weave; "
    "<b>sūra</b> = TF-IDF signature + coherence; <b>Qur'ān</b> = NMF theme factorization.</div>",
    unsafe_allow_html=True)


@st.cache_data(show_spinner="Mapping structure at every scale…")
def _compute(_cid):
    return {
        "bonds": SS.ayah_bonds(corpus),
        "weave": SS.passage_weave(corpus),
        "sig": SS.sura_signatures(corpus),
        "coher": SS.sura_coherence(corpus),
        "themes": SS.quran_themes(corpus),
    }


D = _compute(id(corpus))
INK = "#10243A"


def _lay(fig, title, h=420):
    fig.update_layout(title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=15)),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
                      font=dict(size=13, color=INK), margin=dict(l=10, r=10, t=44, b=10), height=h)
    return fig


# ── ĀYAH ─────────────────────────────────────────────────────────────
layer(1, "Āyah — concept bonds (NPMI · frequency-controlled)")
bonds, n_strong = D["bonds"]
st.caption(f"{n_strong} strong bonds (NPMI > 0.3). Raw co-occurrence is dominated by frequency; "
           f"NPMI recovers genuine concept-pairs you can read in the verses.")
top = bonds[:22][::-1]
fig = go.Figure(go.Bar(x=[n for *_, n in top], y=[f"{a} · {b}" for a, b, _, _ in top],
                       orientation="h", marker_color="#1D9E75",
                       text=[f"co={w}" for _, _, w, _ in top], textposition="auto"))
fig.update_layout(xaxis_title="NPMI (bond strength)")
st.plotly_chart(_lay(fig, "Top āyah-level root bonds", h=560), use_container_width=True)
st.dataframe(pd.DataFrame([(f"{a} · {b}", w, n) for a, b, w, n in bonds[:60]],
                          columns=["root pair", "co-occurrence", "NPMI"]),
             use_container_width=True, hide_index=True, height=300)

# ── PASSAGE ──────────────────────────────────────────────────────────
st.divider()
layer(2, "Passage — sequential weave (does order matter?)")
w = D["weave"]
c1, c2 = st.columns([1, 3])
c1.metric("weave vs verse-order shuffle", f"z = {w['z']:.0f}")
c1.caption("Adjacent verses reuse roots far beyond a within-sūra order shuffle — local order is "
           "load-bearing.")
per = sorted(w["per"], key=lambda x: x[0])  # by sūra number
fig = go.Figure(go.Bar(x=[s for s, _ in per], y=[v for _, v in per], marker_color="#1D3557"))
fig.update_layout(xaxis_title="sūra (canonical order)", yaxis_title="weave per adjacent pair (IDF)")
c2.plotly_chart(_lay(fig, "Sequential weave per sūra — where the text is tightly woven", h=360),
                use_container_width=True)
_tight = sorted(w["per"], key=lambda x: -x[1])[:5]
st.caption("Most tightly woven sūras: " + " · ".join(f"S{s} ({v:.1f})" for s, v in _tight))

# ── SŪRA ─────────────────────────────────────────────────────────────
st.divider()
layer(3, "Sūra — chapter signature + internal coherence")
sig = D["sig"]
c1, c2 = st.columns([1, 2])
c1.metric("internal coherence vs verse→sūra shuffle", f"z = {D['coher']['z']:.0f}")
c1.caption("Verses cohere to their own chapter's profile far above chance — the sūra is a real "
           "theme-block, not a container.")
_names = {}
try:
    from analysis import COL_SURAH, COL_SURAH_NAME
    for s, n in zip(corpus.df[COL_SURAH].astype(int), corpus.df[COL_SURAH_NAME]):
        _names.setdefault(int(s), str(n))
except Exception:
    pass
_opts = sorted(sig)
_sel = c2.selectbox("inspect a sūra's signature roots", _opts,
                    format_func=lambda s: f"{s} · {_names.get(s, '')}")
c2.markdown("**Signature roots:** " + " · ".join(f"`{r}`" for r in sig.get(_sel, [])))
c2.caption("Examples — S12 Yūsuf: father · brother · prison · shirt · grief; "
           "S112 Ikhlāṣ: one · beget; S1 Fātiḥa: path · help · mercy · wrath · praise.")
# ORIGINAL DATA is the anchor — read the actual āyāt (original Arabic) + your chosen translation,
# so every structural claim above is verifiable in the text itself.
st.markdown("**Verify in the original text** — the signature is derived from these āyāt:")
_MEAN.translation_control(st)        # pick a translation; the original Arabic is always shown
_SR.peek(corpus, int(_sel), 1, key=f"struct_{_sel}")

# ── QUR'ĀN ───────────────────────────────────────────────────────────
st.divider()
layer(4, "Qur'ān — global thematic architecture (NMF · root × sūra)")
th = D["themes"]
W = th["W"]; suras = th["suras"]; themes = th["themes"]
ylab = [" · ".join(t["roots"][:3]) for t in themes]
fig = go.Figure(go.Heatmap(
    z=[[float(W[i][t]) for i in range(len(suras))] for t in range(len(themes))],
    x=suras, y=ylab, colorscale="Magma",
    colorbar=dict(title="theme<br>strength", thickness=12)))
fig.update_layout(xaxis_title="sūra (canonical muṣḥaf order, 1 → 114)",
                  yaxis=dict(autorange="reversed"))
st.plotly_chart(_lay(fig, "12 root-themes across the 114 sūras — themes localize in canonical order",
                     h=480), use_container_width=True)
st.caption(f"Themes localize in position: within-theme spread **{th['real_spread']:.0f}** vs "
           f"**{th['rand_spread']:.0f}** shuffled — the muṣḥaf groups themes, it does not scatter them.")
st.dataframe(pd.DataFrame([(" · ".join(t["roots"]), " ".join(f"S{s}" for s in t["suras"]))
                           for t in themes], columns=["theme (top roots)", "dominant sūras"]),
             use_container_width=True, hide_index=True, height=320)

st.divider()
st.caption("All four scales are measured vs the text's own shuffle (research/intrinsic/"
           "MULTISCALE_STRUCTURE.md). These are robust structural recoveries — the value is the "
           "scale-honest method (one instrument per scale) and a navigable map of the territory.")
