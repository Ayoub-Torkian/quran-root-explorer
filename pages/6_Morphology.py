"""Morphology — attached particles (col 6 segmentation) per input root."""
import streamlit as st

import plotly_charts as PC
from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, per_root_hint, log_page)

st.set_page_config(page_title="Morphology", page_icon="🧬", layout="wide")
log_page("morphology")
corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

hero("🧬 Morphology",
     "Prefix/suffix particles attached to each input root, learned from col 6.")
per_root_hint(compact=True)

morph = R["morphology"]

# ── LAYER 1 ──────────────────────────────────────────────────────
layer(1, "Morphology summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Input roots analysed", len(R["input_roots"]),
          help="Roots from your query whose attached particles were scanned.")
c2.metric("Unique particles found", morph["Particle"].nunique() if not morph.empty else 0,
          help="Distinct prefix/suffix particles (al-, wa, bi, li, pronominal suffixes…) "
               "detected on your roots' surface forms.")
c3.metric("Total prefix attachments",
          int(morph[morph["Position"] == "prefix"]["Count"].sum()) if not morph.empty else 0,
          help="How many times a recognised particle appears BEFORE one of your roots (e.g. wa-, al-).")
c4.metric("Total suffix attachments",
          int(morph[morph["Position"] == "suffix"]["Count"].sum()) if not morph.empty else 0,
          help="How many times a recognised particle appears AFTER one of your roots "
               "(mostly pronominal suffixes — his/their/your).")

# ── LAYER 2 — chart ──────────────────────────────────────────────
st.divider()
layer(2, "Particle distribution — all input roots")
st.plotly_chart(PC.chart_morphology(morph), width='stretch')
try:
    if not morph.empty:
        import plotly.graph_objects as _go
        _by_part = morph.groupby("Particle")["Count"].sum().sort_values(ascending=False)
        _tot_att = int(_by_part.sum())
        _top_p = _by_part.index[0]; _top_c = int(_by_part.iloc[0])
        _pre = int(morph[morph["Position"] == "prefix"]["Count"].sum())
        _suf = int(morph[morph["Position"] == "suffix"]["Count"].sum())
        _cm1, _cm2 = st.columns([1, 1.6])
        with _cm1:
            _fig_d = _go.Figure(_go.Pie(
                labels=["prefix", "suffix"], values=[_pre, _suf], hole=0.55,
                marker=dict(colors=["#378ADD", "#EF9F27"]),
                textinfo="label+percent"))
            _fig_d.update_layout(
                title=dict(text="<b>Prefix vs suffix share</b>", x=0.5,
                           font=dict(size=14)),
                height=260, margin=dict(l=10, r=10, t=40, b=10),
                showlegend=False, paper_bgcolor="#FFFFFF")
            st.plotly_chart(_fig_d, width='stretch')
        with _cm2:
            _lead = "prefixes" if _pre >= _suf else "suffixes"
            _lead_pct = round(100 * max(_pre, _suf) / max(_pre + _suf, 1), 1)
            st.markdown(
                f"**📍 What to take from this chart:** across {_tot_att} particle "
                f"attachments on your roots, the most common particle is "
                f"**{_top_p}** ({_top_c} attachments, "
                f"{round(100 * _top_c / max(_tot_att, 1), 1)}% of all), and "
                f"**{_lead}** dominate at {_lead_pct}% — i.e. your roots are mostly "
                f"modified {'before' if _lead == 'prefixes' else 'after'} the stem. "
                f"This describes surface grammar around the roots, not meaning.")
except Exception:
    pass

# ── LAYER 3 — per-root ───────────────────────────────────────────
st.divider()
layer(3, "Drill into one root")
if R["input_roots"]:
    pick = st.selectbox("Pick root", R["input_roots"], key="morph_pick")
    st.plotly_chart(PC.chart_morphology_per_root(morph, pick), width='stretch')
    sub = morph[morph["Input Root"] == pick]
    try:
        if not sub.empty:
            _sg = sub.groupby("Particle")["Count"].sum().sort_values(ascending=False)
            _stot = int(_sg.sum())
            st.markdown(
                f"**📍 What to take from this chart:** `{pick}` carries {_stot} particle "
                f"attachments over {len(_sg)} distinct particles; its single most frequent "
                f"companion is **{_sg.index[0]}** ({int(_sg.iloc[0])}×, "
                f"{round(100 * int(_sg.iloc[0]) / max(_stot, 1), 1)}% of its attachments).")
    except Exception:
        pass
    st.dataframe(sub, width='content', hide_index=True, height=320)

# ── LAYER 4 — full table ─────────────────────────────────────────
st.divider()
layer(4, "Full morphology table")
st.dataframe(morph, width='content', hide_index=True, height=400)
st.caption(
    "Particle attachments are detected by aligning surface forms (col 5) against "
    "tokens in the segmented column (col 6) and noting recognized prefix/suffix "
    "particles within ±2 tokens. The recognised set covers al-, wa, fa, bi, li, ka, "
    "sa, plus pronominal suffixes."
)
