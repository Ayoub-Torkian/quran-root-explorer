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
        "clusters": SS.ayah_clusters(corpus),
        "weave": SS.passage_weave(corpus),
        "decay": SS.weave_decay(corpus),
        "sig": SS.sura_signatures(corpus),
        "coher": SS.sura_coherence(corpus),
        "themes": SS.quran_themes(corpus),
    }


D = _compute(id(corpus))
INK = "#10243A"

# ONE translation control for the whole page — ORIGINAL Arabic is always the anchor; this only
# chooses which translation rides alongside in the read-backs below.
_MP = _MEAN.translation_control(st)
st.caption("Original Arabic is the anchor (always shown). Pick a translation to read alongside.")


@st.cache_data(show_spinner=False)
def _bondh(a, b):
    return SS.bond_word_hits(corpus, a, b, 30)


@st.cache_data(show_spinner=False)
def _themeh(roots):
    return SS.theme_word_hits(corpus, list(roots), 30)


@st.cache_data(show_spinner=False)
def _sighits(sura, roots):
    return SS.sura_sig_hits(corpus, sura, list(roots), 15)


def _hits(rows, empty="(none)"):
    """Dense read-out: ref + the actual words, in a multi-column grid that FILLS the width."""
    if not rows:
        st.caption(empty); return
    cells = []
    for s, a, words in rows:
        cells.append(
            "<div style='display:flex;gap:8px;align-items:baseline;padding:4px 8px;border-bottom:1px solid #eef2f4'>"
            f"<span style='font-weight:800;color:#0F6E56;font-size:13px;white-space:nowrap'>{s}:{a}</span>"
            f"<span class='qv-ar' dir='rtl' style='font-size:20px;line-height:1.6;color:#10243A'>{words}</span></div>")
    st.markdown("<div style='display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));"
                "gap:0 16px'>" + "".join(cells) + "</div>", unsafe_allow_html=True)


def _verse_cards(refs, langs, empty="(no verses)"):
    """Render āyāt: ORIGINAL Arabic (anchor) + the chosen translation."""
    if not refs:
        st.caption(empty); return
    parts = ["<div style='display:grid;grid-template-columns:1fr;gap:6px;margin-top:4px'>"]
    for s, a in refs:
        try:
            ar = _SR._aryah(f"{s}:{a}") or ""
        except Exception:
            ar = ""
        # respect the user's choice: Off (langs empty) → ORIGINAL ONLY, no translation forced
        mean = _MEAN.meaning_block_html(f"{s}:{a}", langs=langs) if langs else ""
        parts.append(
            "<div style='border:1px solid #E2E8F1;border-radius:10px;padding:8px 12px;background:#fff'>"
            f"<div style='font-size:12.5px;font-weight:800;color:#0F6E56'>{s}:{a}</div>"
            f"<div class='qv-ar' dir='rtl' style='text-align:right;font-size:23px;line-height:2;color:#10243A'>{ar}</div>"
            f"{mean}</div>")
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def _lay(fig, title, h=420):
    fig.update_layout(title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=15)),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
                      font=dict(size=13, color=INK), margin=dict(l=10, r=10, t=44, b=10), height=h)
    return fig


# ════════════ FOUR CHARTS · ONE PER SCALE ════════════

# 1) ĀYAH — which roots bond within a verse
st.divider()
layer(1, "Āyah")
bonds, n_strong = D["bonds"]
top = bonds[:20][::-1]
fig = go.Figure(go.Bar(x=[n for *_, n in top], y=[f"{a} · {b}" for a, b, _, _ in top],
                       orientation="h", marker_color="#1D9E75",
                       hovertext=[f"co-occur {w}×" for _, _, w, _ in top], hoverinfo="text"))
fig.update_layout(xaxis_title="bond strength (NPMI · frequency-controlled)")
st.plotly_chart(_lay(fig, "Strongest concept-bonds within a verse", h=520), use_container_width=True)
# concept families — roots that bond together (connected groups of strong bonds)
st.markdown("**Concept families** — roots that travel together within verses:")
_fcells = ["<div style='border:1px solid #cfe4dc;border-radius:8px;padding:6px 10px;background:#F4F9F7'>"
           f"<span class='qv-ar' dir='rtl' style='font-size:18px;color:#10243A'>{' · '.join(fam[:8])}</span></div>"
           for fam in D["clusters"]]
st.markdown("<div style='display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:8px'>"
            + "".join(_fcells) + "</div>", unsafe_allow_html=True)
with st.expander("read a bond in the text"):
    _bo = [f"{a} · {b}" for a, b, _, _ in bonds[:40]]
    _bi = st.selectbox("bond", range(len(_bo)), format_func=lambda i: _bo[i], key="bond_read")
    _bh = _bondh(bonds[_bi][0], bonds[_bi][1])
    _hits(_bh, "(none)")
    with st.expander("full text + translation"):
        _verse_cards([(s, a) for s, a, _ in _bh[:10]], _MP)

# 2) PASSAGE — sequential weave per sūra
st.divider()
layer(2, "Passage")
w = D["weave"]
per = sorted(w["per"], key=lambda x: x[0])
fig = go.Figure(go.Bar(x=[s for s, _ in per], y=[v for _, v in per], marker_color="#1D3557"))
fig.update_layout(xaxis_title="sūra (1 → 114)", yaxis_title="root reuse between adjacent āyāt")
st.plotly_chart(_lay(fig, f"How tightly adjacent āyāt are woven  ·  vs verse-shuffle z = {w['z']:.0f}",
                     h=420), use_container_width=True)
# cohesion decay — how far the weave reaches (the passage size)
dc = D["decay"]
figd = go.Figure()
figd.add_trace(go.Scatter(x=dc["d"], y=dc["real"], mode="lines+markers", name="actual order",
                          line=dict(color="#1D3557", width=3)))
figd.add_trace(go.Scatter(x=dc["d"], y=dc["floor"], mode="lines", name="shuffled floor",
                          line=dict(color="#B23A3A", width=2, dash="dash")))
figd.update_layout(xaxis_title="distance between āyāt (verses apart)",
                   yaxis_title="shared-root reuse (IDF)",
                   legend=dict(font=dict(size=12), orientation="h", y=1.12, x=0))
st.plotly_chart(_lay(figd, "How far cohesion reaches — reuse fades with distance (the passage size)",
                     h=360), use_container_width=True)

# 3) SŪRA — internal coherence per chapter
st.divider()
layer(3, "Sūra")
cper = sorted(D["coher"]["per"], key=lambda x: x[0])
fig = go.Figure(go.Bar(x=[s for s, _ in cper], y=[v for _, v in cper], marker_color="#0F6E56"))
fig.update_layout(xaxis_title="sūra (1 → 114)", yaxis_title="how tightly its āyāt cohere")
st.plotly_chart(_lay(fig, f"Each chapter's internal coherence  ·  vs verse→sūra shuffle z = {D['coher']['z']:.0f}",
                     h=420), use_container_width=True)
# coherence vs length — coherence is not merely a size effect
from analysis import COL_SURAH as _CS
import collections as _coll
_nay = _coll.Counter(int(s) for s in corpus.df[_CS].astype(int))
_cohd = dict(D["coher"]["per"])
_sx = sorted(_cohd)
figc = go.Figure(go.Scatter(
    x=[_nay.get(s, 0) for s in _sx], y=[_cohd[s] for s in _sx], mode="markers",
    marker=dict(size=8, color="#0F6E56", line=dict(width=1, color="#10243A")),
    text=[f"S{s}" for s in _sx], hoverinfo="text+x+y"))
figc.update_layout(xaxis_title="sūra length (# āyāt)", yaxis_title="internal coherence")
st.plotly_chart(_lay(figc, "Coherence vs length — coherence is not just a size effect", h=340),
                use_container_width=True)
sig = D["sig"]
with st.expander("a sūra's signature roots + text"):
    _names = {}
    try:
        from analysis import COL_SURAH, COL_SURAH_NAME
        for s, n in zip(corpus.df[COL_SURAH].astype(int), corpus.df[COL_SURAH_NAME]):
            _names.setdefault(int(s), str(n))
    except Exception:
        pass
    _sel = st.selectbox("sūra", sorted(sig), format_func=lambda s: f"{s} · {_names.get(s, '')}", key="sig_sel")
    st.markdown("**Signature roots:** " + " · ".join(f"`{r}`" for r in sig.get(_sel, [])))
    _sigh = _sighits(int(_sel), tuple(sig.get(_sel, [])))
    _hits(_sigh, "(none)")
    with st.expander("full text + translation"):
        _verse_cards([(s, a) for s, a, _ in _sigh[:10]], _MP)

# 4) QUR'ĀN — where each theme lives across the muṣḥaf
st.divider()
layer(4, "Qur'ān")
th = D["themes"]; themes = th["themes"]
labels = [" · ".join(t["roots"][:3]) for t in themes]
fig = go.Figure()
fig.add_trace(go.Bar(orientation="h", y=labels, x=[t["hi"] - t["lo"] for t in themes],
                     base=[t["lo"] for t in themes], marker_color="#D6E3EC",
                     hoverinfo="skip", showlegend=False))
fig.add_trace(go.Scatter(
    x=[t["meanpos"] for t in themes], y=labels, mode="markers",
    marker=dict(size=13, color=[t["meccan_frac"] for t in themes], colorscale="RdBu", cmin=0, cmax=1,
                showscale=True, colorbar=dict(title="Meccan<br>share", thickness=12),
                line=dict(width=1, color="#10243A")),
    hovertext=[f"peak S{t['suras'][0]} · span S{t['lo']}–{t['hi']}" for t in themes],
    hoverinfo="text", showlegend=False))
fig.update_layout(xaxis_title="sūra position 1 → 114  (left = early, right = late)",
                  yaxis=dict(autorange="reversed"))
st.plotly_chart(_lay(fig, f"Where each theme lives  ·  themes cluster (spread {th['real_spread']:.0f} vs {th['rand_spread']:.0f} shuffled)",
                     h=440), use_container_width=True)
# Meccan / Medinan tilt per theme (the revelation-arrangement dimension)
_tilt = sorted(themes, key=lambda t: t["meccan_frac"])
figt = go.Figure(go.Bar(
    orientation="h", y=[" · ".join(t["roots"][:3]) for t in _tilt],
    x=[t["meccan_frac"] * 100 for t in _tilt],
    marker=dict(color=[t["meccan_frac"] for t in _tilt], colorscale="RdBu", cmin=0, cmax=1)))
figt.add_vline(x=50, line=dict(color="#10243A", width=1, dash="dash"))
figt.update_layout(xaxis_title="Meccan share of the theme (%)  ·  left = Medinan, right = Meccan")
st.plotly_chart(_lay(figt, "Each theme's Meccan vs Medinan tilt (revelation arrangement)", h=420),
                use_container_width=True)
with st.expander("read a theme in the text"):
    _to = [" · ".join(t["roots"][:4]) for t in themes]
    _ti = st.selectbox("theme", range(len(_to)), format_func=lambda i: _to[i], key="theme_read")
    _thh = _themeh(tuple(themes[_ti]["roots"]))
    _hits(_thh, "(none)")
    with st.expander("full text + translation"):
        _verse_cards([(s, a) for s, a, _ in _thh[:10]], _MP)
