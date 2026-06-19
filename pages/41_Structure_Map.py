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

# ONE translation control for the whole page — ORIGINAL Arabic is always the anchor; this only
# chooses which translation rides alongside in the read-backs below.
_MP = _MEAN.translation_control(st)
st.caption("Original Arabic is the anchor (always shown). Pick a translation to read alongside.")


@st.cache_data(show_spinner=False)
def _bondv(a, b):
    return SS.bond_verses(corpus, a, b, 20)


@st.cache_data(show_spinner=False)
def _themev(roots):
    return SS.theme_exemplars(corpus, list(roots), 20)


def _verse_cards(refs, langs, empty="(no verses)"):
    """Render āyāt: ORIGINAL Arabic (anchor) + the chosen translation."""
    if not refs:
        st.caption(empty); return
    rl = langs if langs else ("en",)
    parts = ["<div style='display:grid;grid-template-columns:1fr;gap:6px;margin-top:4px'>"]
    for s, a in refs:
        try:
            ar = _SR._aryah(f"{s}:{a}") or ""
        except Exception:
            ar = ""
        mean = _MEAN.meaning_block_html(f"{s}:{a}", langs=rl)
        parts.append(
            "<div style='border:1px solid #E2E8F1;border-radius:10px;padding:8px 12px;background:#fff'>"
            f"<div style='font-size:12.5px;font-weight:800;color:#0F6E56'>{s}:{a}</div>"
            f"<div class='qv-ar' dir='rtl' style='text-align:right;font-size:19px;line-height:2;color:#10243A'>{ar}</div>"
            f"{mean}</div>")
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


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
# read-back: the actual āyāt where a chosen bond's two roots co-occur (original + translation)
_bo = [f"{a} · {b}" for a, b, _, _ in bonds[:40]]
if _bo:
    _bi = st.selectbox("Read a bond in the original text — āyāt where both roots occur",
                       range(len(_bo)), format_func=lambda i: _bo[i], key="bond_read")
    _verse_cards(_bondv(bonds[_bi][0], bonds[_bi][1]), _MP, "(no shared verses)")

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
_SR.peek(corpus, int(_sel), 1, key=f"struct_{_sel}")

# ── QUR'ĀN ───────────────────────────────────────────────────────────
st.divider()
layer(4, "Qur'ān — global thematic architecture (NMF · root × sūra)")
th = D["themes"]
themes = th["themes"]; suras = th["suras"]; dom = th["dom_per_sura"]
labels = [" · ".join(t["roots"][:3]) for t in themes]
st.caption("Each theme is a cluster of roots. Three simple views: WHERE each theme lives, the "
           "dominant theme of each sūra, and the full directory — all original-anchored.")

# View 1 — where each theme lives (span + center), ordered early → late
figA = go.Figure()
figA.add_trace(go.Bar(orientation="h", y=labels, x=[t["hi"] - t["lo"] for t in themes],
                      base=[t["lo"] for t in themes], marker_color="#D6E3EC",
                      hoverinfo="skip", showlegend=False))
figA.add_trace(go.Scatter(
    x=[t["meanpos"] for t in themes], y=labels, mode="markers",
    marker=dict(size=13, color=[t["meccan_frac"] for t in themes], colorscale="RdBu",
                cmin=0, cmax=1, showscale=True,
                colorbar=dict(title="Meccan<br>share", thickness=12), line=dict(width=1, color="#10243A")),
    text=[f"peak S{t['suras'][0]} · span S{t['lo']}–{t['hi']} · Meccan {t['meccan_frac']:.0%}"
          for t in themes], hoverinfo="text", showlegend=False))
figA.update_layout(xaxis_title="sūra position 1 → 114  (left = early/short sūras, right = late)",
                   yaxis=dict(autorange="reversed"))
st.plotly_chart(_lay(figA, "1) Where each theme lives — bar = middle-80% span, dot = center",
                     h=420), use_container_width=True)
st.caption("Blue dots = Meccan-tilted themes (oneness, refuge, judgment — cluster early/late short "
           "sūras); red = Medinan-tilted (community, law — cluster in the long early-middle sūras).")

# View 2 — the territory as one strip: dominant theme of each sūra
figB = go.Figure(go.Heatmap(
    z=[dom], x=suras, y=[""], colorscale="Turbo", showscale=False,
    customdata=[[labels[d] for d in dom]],
    hovertemplate="sūra %{x}<br>theme: %{customdata}<extra></extra>"))
figB.update_layout(xaxis_title="sūra (1 → 114)", yaxis=dict(showticklabels=False))
st.plotly_chart(_lay(figB, "2) Dominant theme of each sūra — colour = the theme that most defines it",
                     h=190), use_container_width=True)
st.caption(f"Runs of one colour = thematic regions. Themes cluster in position (within-theme spread "
           f"**{th['real_spread']:.0f}** vs **{th['rand_spread']:.0f}** shuffled) — the order is not random.")

# View 3 — the directory table
st.markdown("**3) Theme directory**")
st.dataframe(pd.DataFrame([
    {"theme (top roots)": " · ".join(t["roots"]),
     "peak sūras": " ".join(f"S{s}" for s in t["suras"]),
     "span": f"S{t['lo']}–{t['hi']}",
     "center": f"S{round(t['meanpos'])}",
     "Meccan share": f"{t['meccan_frac']:.0%}"} for t in themes]),
    use_container_width=True, hide_index=True, height=380)
# read-back: the actual āyāt that most express a chosen theme (original + translation)
_to = [" · ".join(t["roots"][:4]) for t in themes]
if _to:
    _ti = st.selectbox("Read a theme in the original text — āyāt that most carry its roots",
                       range(len(_to)), format_func=lambda i: _to[i], key="theme_read")
    _verse_cards(_themev(tuple(themes[_ti]["roots"])), _MP, "(no exemplar verses)")

st.divider()
st.caption("All four scales are measured vs the text's own shuffle (research/intrinsic/"
           "MULTISCALE_STRUCTURE.md). These are robust structural recoveries — the value is the "
           "scale-honest method (one instrument per scale) and a navigable map of the territory.")
