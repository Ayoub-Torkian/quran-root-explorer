"""Compare & Heatmaps — surah×root distribution and pairwise overlap."""
import streamlit as st

import plotly_charts as PC
from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, highlight_text, per_root_hint, log_page)
import analysis as A

st.set_page_config(page_title="Compare & Heatmaps", page_icon="📊", layout="wide")
log_page("compare")
corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

hero("📊 Compare & Heatmaps",
     "See how input roots distribute across surahs and where they overlap.")
per_root_hint(compact=True)

# ── LAYER 1 ──────────────────────────────────────────────────────
layer(1, "Comparison at a glance")
c1, c2, c3 = st.columns(3)
c1.metric("Input roots", len(R["input_roots"]),
          help="Roots you typed in the query bar — each becomes a row in the heatmap.")
c2.metric("Surahs with at least one hit",
          int((R["heatmap"].sum(axis=0) > 0).sum()) if not R["heatmap"].empty else 0,
          help="Surahs (out of 114) where at least one input root appears.")
total_pairs = sum(R["overlap"].values[i, j]
                  for i in range(len(R["input_roots"]))
                  for j in range(i + 1, len(R["input_roots"]))) if not R["overlap"].empty else 0
c3.metric("Shared-ayah pairs (sum)", total_pairs,
          help="Sum over all root pairs of the verses they share — a quick gauge of how "
               "intertwined your query set is at the ayah level.")

# ── LAYER 2 — heatmaps ───────────────────────────────────────────
st.divider()
layer(2, "Surah × Input-Root heatmap")
st.plotly_chart(PC.chart_surah_heatmap(R["heatmap"]), width='stretch')
try:
    _hm = R["heatmap"]
    if not _hm.empty:
        _col_tot = _hm.sum(axis=0)            # per-surah totals
        _row_tot = _hm.sum(axis=1)            # per-root totals
        _hot_surah = _col_tot.idxmax(); _hot_val = int(_col_tot.max())
        _busiest_root = _row_tot.idxmax(); _busy_val = int(_row_tot.max())
        _touched = int((_col_tot > 0).sum())
        st.markdown(
            f"**📍 What to take from this chart:** the hottest column is surah "
            f"**{_hot_surah}** ({_hot_val} ayah-hits summed over your roots), and the "
            f"busiest row is **{_busiest_root}** ({_busy_val} hits corpus-wide); "
            f"{_touched}/114 surahs are touched at all — empty columns are as "
            f"informative as hot ones (where the query set is absent)."
        )
except Exception:
    pass

st.divider()
layer(2, "Pair overlap — multi-granularity (surah-level + ayah-level)")
st.caption(
    "Each pair shows two bars: **surah-level** (teal — both roots appear somewhere in the same surah, "
    "almost always populated) and **ayah-level** (red — both roots in the same verse, often rare).  "
    "Sorted by surah overlap descending: most thematically-related pairs on top."
)
st.plotly_chart(
    PC.chart_pair_overlap_grouped(R["overlap"], R["overlap_surah"],
                                   R["input_roots"]),
    width='stretch',
)

# Augmented sortable table — Jaccard at each granularity
import pandas as _pd
_rows = []
_ir = R["input_roots"]
_n_corpus_surahs = int(corpus.df[A.COL_SURAH].nunique())
for i in range(len(_ir)):
    for j in range(i + 1, len(_ir)):
        a, b = _ir[i], _ir[j]
        ay_a = int(R["overlap"].loc[a, a])
        ay_b = int(R["overlap"].loc[b, b])
        ay_ab = int(R["overlap"].loc[a, b])
        ay_union = ay_a + ay_b - ay_ab
        ay_jac = round(ay_ab / max(ay_union, 1), 3) if ay_union else 0.0
        su_a = int(R["overlap_surah"].loc[a, a])
        su_b = int(R["overlap_surah"].loc[b, b])
        su_ab = int(R["overlap_surah"].loc[a, b])
        su_union = su_a + su_b - su_ab
        su_jac = round(su_ab / max(su_union, 1), 3) if su_union else 0.0
        _rows.append({
            "Pair": f"{a} ↔ {b}",
            "Ayahs shared": ay_ab, "Ayah Jaccard": ay_jac,
            "Surahs shared": su_ab, "Surah Jaccard": su_jac,
        })
if _rows:
    _pairs_df = _pd.DataFrame(_rows).sort_values(
        ["Surah Jaccard", "Surahs shared"], ascending=[False, False])
    try:
        _best = _pairs_df.iloc[0]
        _n_ay0 = int((_pairs_df["Ayahs shared"] == 0).sum())
        st.markdown(
            f"**📍 What to take from this chart:** the most territory-sharing pair is "
            f"**{_best['Pair']}** (surah Jaccard {_best['Surah Jaccard']}, "
            f"{int(_best['Surahs shared'])} shared surahs but only "
            f"{int(_best['Ayahs shared'])} shared verses); "
            f"{_n_ay0} of {len(_pairs_df)} pairs never share a single ayah — "
            f"surah-level co-presence is the norm, verse-level intersection the exception. "
            f"Co-occurrence measures shared placement, not semantic association."
        )
    except Exception:
        pass
    st.markdown("**Detailed pair overlap table** (sortable)")
    st.dataframe(_pairs_df, width='content', hide_index=True, height=320)
else:
    st.info("This page compares pairs of input roots. Add at least one more "
            "root above to see pair-overlap analytics.")

# ── LAYER 3 — drill into a cell ──────────────────────────────────
st.divider()
layer(3, "Drill into a specific pair — see the shared ayahs")
if len(R["input_roots"]) < 2:
    st.caption("Need at least 2 input roots to compare pairs.")
else:
    c1, c2 = st.columns(2)
    a = c1.selectbox("Root A", R["input_roots"], key="pair_a")
    b = c2.selectbox("Root B", [x for x in R["input_roots"] if x != a],
                     key="pair_b") if len(R["input_roots"]) > 1 else None
    if a and b and a != b:
        ayahs_a = set(A.search_root(corpus, a, R["normalize"]))
        ayahs_b = set(A.search_root(corpus, b, R["normalize"]))
        shared = sorted(ayahs_a & ayahs_b)
        st.caption(
            f"**{a}**: {len(ayahs_a)} ayahs · **{b}**: {len(ayahs_b)} ayahs · "
            f"**Shared:** {len(shared)} ayahs · "
            f"**Jaccard:** {len(shared) / max(len(ayahs_a | ayahs_b), 1):.3f}"
        )
        for i in shared[:50]:
            r = corpus.df.iloc[i]
            with st.expander(
                f"📖 Surah {int(r[A.COL_SURAH])} ({r[A.COL_SURAH_NAME]}) · Ayah {int(r[A.COL_AYAH])}"
            ):
                st.markdown(highlight_text(r[A.COL_SEGMENTED], [a, b]),
                            unsafe_allow_html=True)
                st.caption(f"All roots: `{r[A.COL_ROOTS]}`")
        if len(shared) > 50:
            st.caption(f"…showing first 50 of {len(shared)}.")

# ── LAYER 4 — raw matrices for export/copy ───────────────────────
st.divider()
layer(4, "Raw matrices")
st.markdown("**Surah heatmap matrix:**")
st.dataframe(R["heatmap"], width='content', height=300)
st.markdown("**Overlap matrix:**")
st.dataframe(R["overlap"], width='content')
