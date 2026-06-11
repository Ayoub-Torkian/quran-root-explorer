"""Reading guide — data-driven narrative for THIS session's results.

Every line is computed strictly from numbers in your input session.
No conjecture, no generalisation, no theological interpretation.
"""
from __future__ import annotations

import streamlit as st

from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, per_root_hint, log_page)
import interpret as I

st.set_page_config(page_title="Reading guide", page_icon="🧭", layout="wide")
log_page("interpret")

corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

hero("🧭 Reading guide",
     "Plain-English findings from your current session. Every line is a "
     "fact computed from your inputs — no conjecture, no generalisation.")
per_root_hint(compact=True)

st.info(
    "📌 **What this page is.** A summary of the actual numbers in your "
    "current analysis, written as sentences. Use it as a starting point — "
    "the per-page charts (Network, Motifs, Statistics) show the full detail."
)

# ── Headline metrics + a visual anchor for the narrative below ──
try:
    _occ = R.get("occurrences")
    if _occ is not None and not _occ.empty:
        _n_roots = len(R.get("input_roots", []))
        _n_uniq = _occ[["Surah #", "Ayah #"]].drop_duplicates().shape[0]
        _n_su = _occ["Surah #"].nunique()
        _pct = round(100 * _n_uniq / max(corpus.n_ayahs, 1), 2)
        _h1, _h2, _h3, _h4 = st.columns(4)
        _h1.metric("Input roots", _n_roots,
                   help="Roots in your current query — everything below is computed from them.")
        _h2.metric("Unique ayahs matched", _n_uniq,
                   help="Distinct verses containing at least one input root (counted once each).")
        _h3.metric("Surahs covered", f"{_n_su}/114",
                   help="Distinct surahs touched by the query.")
        _h4.metric("Share of the corpus", f"{_pct}%",
                   help=f"Matched ayahs ÷ {corpus.n_ayahs} total ayahs — how much of the text "
                        "your reading guide is actually about.")

        _per_root = (_occ.drop_duplicates(["Surah #", "Ayah #", "Input Root"])
                         .groupby("Input Root").size().sort_values(ascending=False))
        if len(_per_root) >= 2:
            import plotly.graph_objects as _go
            _fig_r = _go.Figure(_go.Bar(
                x=_per_root.index.tolist(), y=[int(v) for v in _per_root.values],
                marker_color="#1D9E75",
                text=[int(v) for v in _per_root.values], textposition="outside"))
            _fig_r.update_layout(
                title=dict(text="<b>Ayah footprint per input root</b>", x=0.5,
                           font=dict(size=14)),
                xaxis_title="input root", yaxis_title="ayahs containing it",
                height=260, margin=dict(l=10, r=10, t=40, b=10),
                paper_bgcolor="#FFFFFF", plot_bgcolor="#FAFBFD")
            st.plotly_chart(_fig_r, width='stretch')
            _big = _per_root.index[0]; _small = _per_root.index[-1]
            _ratio = round(int(_per_root.iloc[0]) / max(int(_per_root.iloc[-1]), 1), 1)
            st.markdown(
                f"**📍 What to take from this chart:** `{_big}` dominates your query "
                f"({int(_per_root.iloc[0])} ayahs) while `{_small}` is the rarest "
                f"({int(_per_root.iloc[-1])} ayahs) — a {_ratio}× asymmetry. Keep that "
                f"in mind reading the facts below: frequency differences drive many of "
                f"them, and frequency is not importance."
            )
except Exception:
    pass

sections = I.generate(R, corpus)

for section_title, facts in sections.items():
    if not facts:
        continue
    layer(0, section_title)
    for fact in facts:
        st.markdown(f"- {fact}")
    st.markdown("")
