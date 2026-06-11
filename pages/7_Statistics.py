"""Statistics & Cross-reference — extensive analytics organized as tiles.

For every analysis: TILE = chart  |  summary  |  table. Easy to compare,
nothing overlapping, everything cross-referenced and validated.
"""
import pandas as pd
import streamlit as st

import analysis as A
import stats_module as S
import stats_charts as SC
from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, per_root_hint, log_page)

st.set_page_config(page_title="Statistics", page_icon="📈", layout="wide")
log_page("statistics")
corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

hero("📈 Statistics & Cross-reference",
     "Every quantitative view of your input roots. Each section is a tile: "
     "chart · summary · table.")
per_root_hint(compact=True)

# ── INTRINSIC UNIVERSAL LAWS (Latent Features L01–L05) — self-contained, reads viz_data.json ──
try:
    import os as _os
    import json as _json
    import plotly.graph_objects as _go
    _vz = _json.load(open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                                        "research", "intrinsic", "viz_data.json"), encoding="utf-8"))
    layer(1, "INTRINSIC UNIVERSAL LAWS — the whole corpus (Latent Features L01–L05)")
    st.caption("Corpus-wide laws measured against the text's own shuffle. Open the 🧬 Latent Feature Ledger "
               "for the full critical review of each. Power-law size tails (L05): word α 2.04 · verse 1.71 · sūra 1.44.")
    _a, _b = st.columns(2)

    def _mini(fig, h=240):
        fig.update_layout(height=h, margin=dict(l=6, r=6, t=8, b=6), plot_bgcolor="white",
                          paper_bgcolor="white", font=dict(size=11, color="#1D3557"))
        return fig
    with _a:
        if _vz.get("zipf"):
            st.markdown("**Zipf — rank vs frequency (L01)**")
            _z = _vz["zipf"]
            st.plotly_chart(_mini(_go.Figure(_go.Scatter(x=[p[0] for p in _z], y=[p[1] for p in _z],
                mode="markers", marker=dict(size=3, color="#457B9D")))).update_xaxes(title="log rank",
                showgrid=True, gridcolor="#EEF1F6").update_yaxes(title="log frequency", showgrid=True, gridcolor="#EEF1F6"),
                width="stretch", key="stats_zipf_L01")
        if _vz.get("spectrum"):
            st.markdown("**1/f spectrum (L04)** — slope %.2f" % _vz.get("spectrum_slope", 0))
            _sp = _vz["spectrum"]
            st.plotly_chart(_mini(_go.Figure(_go.Scatter(x=[p[0] for p in _sp], y=[p[1] for p in _sp],
                mode="lines+markers", line=dict(color="#E76F51", width=1.2), marker=dict(size=4)))).update_xaxes(
                title="log frequency", showgrid=True, gridcolor="#EEF1F6").update_yaxes(title="log power",
                showgrid=True, gridcolor="#EEF1F6"), width="stretch", key="stats_spec_L04")
    with _b:
        if _vz.get("heaps"):
            st.markdown("**Heaps — vocabulary growth (L02), β = 0.74**")
            _h = _vz["heaps"]
            st.plotly_chart(_mini(_go.Figure(_go.Scatter(x=[p[0] for p in _h], y=[p[1] for p in _h],
                mode="lines", line=dict(color="#6A4C93", width=1.6)))).update_xaxes(title="words read",
                showgrid=True, gridcolor="#EEF1F6").update_yaxes(title="distinct words", showgrid=True, gridcolor="#EEF1F6"),
                width="stretch", key="stats_heaps_L02")
        if _vz.get("wave"):
            st.markdown("**Verse-length wave (L03), DFA Hurst 0.95**")
            st.plotly_chart(_mini(_go.Figure(_go.Scatter(y=_vz["wave"], mode="lines",
                line=dict(color="#2A9D8F", width=.8)))).update_xaxes(title="verse (in order)", showgrid=True,
                gridcolor="#EEF1F6").update_yaxes(title="words/verse", showgrid=True, gridcolor="#EEF1F6"),
                width="stretch", key="stats_wave_L03")
    try:
        st.page_link("pages/25_Latent_Features.py", label="See L01–L05 in the Latent Feature Ledger", icon="🧬")
    except Exception:
        pass
except Exception:
    pass


def _tile(title: str, chart=None, summary_md: str = "", table=None,
          table_height: int = 280):
    """One analytic 'tile' rendered as three sub-tiles."""
    st.subheader(title)
    cols = st.columns([5, 4])
    with cols[0]:
        if chart is not None:
            st.plotly_chart(chart, width='stretch')
    with cols[1]:
        if summary_md:
            st.markdown("**Summary**")
            st.markdown(summary_md)
        if table is not None and not table.empty:
            st.markdown("**Data**")
            st.dataframe(table, width='content', hide_index=True,
                         height=table_height)


# ───────────────────────────────────────────────────────────────────
# LAYER 1 — at a glance
# ───────────────────────────────────────────────────────────────────
layer(1, "Statistical headline  (📌 comprehensive summary)")
freq = S.frequency_analysis(corpus, R["input_roots"], R["normalize"])
c1, c2, c3, c4 = st.columns(4)
c1.metric("Input roots", len(R["input_roots"]),
          help="The roots in your query — every tile below is computed for exactly this set.")
c2.metric("Median rank", int(freq["Rank (1=top)"].median()) if not freq.empty else 0,
          help=f"Frequency rank among all {corpus.n_unique_roots} roots (1 = most frequent). "
               "Low rank = workhorse vocabulary; high rank = rare, episode-bound vocabulary.")
c3.metric("Highest Juilland D",
          f"{freq['Juilland D (0–1)'].max():.2f}" if not freq.empty else "—",
          help="Dispersion: 0 = concentrated in one sūra, 1 = perfectly even across all 114. "
               "Frequency and dispersion are INDEPENDENT — a rare root can be evenly spread "
               "and a frequent one locked to a few sūras.")
c4.metric("Highest entropy",
          f"{freq['Entropy normalized'].max():.2f}" if not freq.empty else "—",
          help="Information-theoretic spread of hits over sūras (0 = one sūra, 1 = uniform). "
               "Agrees with Juilland D for most roots; disagreement flags lumpy distributions.")
if not freq.empty:
    try:
        _fx = freq.loc[freq["Frequency"].idxmax()]
        _dx = freq.loc[freq["Juilland D (0–1)"].idxmax()]
        _dn = freq.loc[freq["Juilland D (0–1)"].idxmin()]
        _ngl = int((freq["Surahs covered"] >= 20).sum())
        st.markdown(
            f"**📍 What to take from the headline:** the workhorse here is "
            f"**{_fx['Input Root']}** ({int(_fx['Frequency'])} āyahs); most evenly deployed is "
            f"**{_dx['Input Root']}** (D={_dx['Juilland D (0–1)']:.2f}), most concentrated is "
            f"**{_dn['Input Root']}** (D={_dn['Juilland D (0–1)']:.2f}). "
            f"{_ngl}/{len(freq)} of your roots reach ≥20 sūras — the GLOBAL-motif class "
            f"(#66): vocabulary the corpus keeps RETURNING to (the #42 mode); the rest are "
            f"passage-bound formulas. Frequent ≠ spread — check tile 2 before treating any "
            f"root as corpus-wide.")
    except Exception:
        pass
st.caption(
    "Frequency, rank, dispersion, entropy, TF-IDF, PMI, conditional probability, Jaccard, "
    "hypergeometric enrichment, position categorization, cumulative trajectory, "
    "PageRank, k-core, ego density, exclusive partners, hierarchical clustering, "
    "cross-validation."
)

# ───────────────────────────────────────────────────────────────────
# LAYER 2 — frequency & dispersion (3 tiles)
# ───────────────────────────────────────────────────────────────────
st.divider()
layer(2, "Frequency, rank, dispersion")

_tile(
    "1 · Ayah frequency & rank",
    chart=SC.chart_frequency_bars(freq),
    summary_md=(
        f"- **Most frequent input:** {freq.iloc[freq['Frequency'].idxmax()]['Input Root']} "
        f"({freq['Frequency'].max()} ayahs)\n"
        f"- **Rarest input:** {freq.iloc[freq['Frequency'].idxmin()]['Input Root']} "
        f"({freq['Frequency'].min()} ayahs)\n"
        f"- **Combined coverage:** {freq['Frequency'].sum()} ayah hits "
        f"({100 * freq['Frequency'].sum() / max(corpus.n_ayahs, 1):.1f}% of corpus)\n"
        f"- **Best rank:** {int(freq['Rank (1=top)'].min())} of {corpus.n_unique_roots}\n"
    ) if not freq.empty else "(no data)",
    table=freq[["Input Root", "Frequency", "Rank (1=top)",
                "% of all root tokens", "TF (per 1000 ayahs)"]] if not freq.empty else None,
)
st.divider()

_tile(
    "2 · Dispersion across surahs (Juilland D + entropy)",
    chart=SC.chart_dispersion(freq),
    summary_md=(
        "**How spread out is each root across the 114 surahs?**\n\n"
        "- **Juilland D**: 0 = concentrated in one surah, 1 = perfectly even spread.\n"
        "- **Entropy normalized**: 0 = all hits in a single surah, 1 = uniform.\n"
        f"- Most uniformly spread: **{freq.iloc[freq['Juilland D (0–1)'].idxmax()]['Input Root']}** "
        f"(D = {freq['Juilland D (0–1)'].max():.2f}).\n"
        f"- Most concentrated: **{freq.iloc[freq['Juilland D (0–1)'].idxmin()]['Input Root']}** "
        f"(D = {freq['Juilland D (0–1)'].min():.2f}).\n"
    ) if not freq.empty else "(no data)",
    table=freq[["Input Root", "Surahs covered", "Juilland D (0–1)",
                "Entropy (bits)", "Entropy normalized"]] if not freq.empty else None,
)
st.divider()

pos = S.position_categorization(corpus, R["input_roots"], R["normalize"])
_tile(
    "3 · Position inside the ayah (start / middle / end)",
    chart=SC.chart_position_tiles(pos),
    summary_md=(
        "Each root partitioned into thirds of the ayah it appears in. "
        "A bias toward start/end can hint at rhyme position or syntactic role.\n\n"
        + "\n".join(
            f"- **{r['Input Root']}**: "
            f"start {r['Start %']}% · middle {r['Middle %']}% · end {r['End %']}%"
            for _, r in pos.iterrows()
        ) if not pos.empty else "(no data)"
    ),
    table=pos,
)
if not pos.empty:
    try:
        _pi = pos["End %"].astype(float).idxmax()
        _pe = pos.loc[_pi]
        _ev = float(_pe["End %"])
        if _ev >= 40:
            st.markdown(
                f"**📍 Position takeaway:** **{_pe['Input Root']}** ends its āyah "
                f"**{_ev:.0f}%** of the time — well above the ~33% chance share: it is "
                f"**seal-active** (Lens 17). The verse-end is the corpus's distinctive "
                f"machine — endings repeat far beyond sajʿ (0.18 vs 0.04, #63/#76) and "
                f"PREDICT their verse's content (z≈+12, #62). Open this root in 🔭 Āyah "
                f"Deep-Dive to see its seal class and live content-fit.")
        else:
            st.markdown(
                f"**📍 Position takeaway:** no input root is end-biased beyond chance "
                f"(max: {_pe['Input Root']} at {_ev:.0f}% vs ~33% baseline) — these are "
                f"body-of-verse concepts; the verse-end channel (Lens 17) is not where "
                f"they work.")
    except Exception:
        pass

# ───────────────────────────────────────────────────────────────────
# LAYER 3 — pairwise relationships (heatmap tiles)
# ───────────────────────────────────────────────────────────────────
st.divider()
layer(3, "Pairwise association — PMI · P(B|A) · Jaccard")

pmi = S.pmi_matrix(corpus, R["input_roots"], R["normalize"])
cond = S.conditional_probability(corpus, R["input_roots"], R["normalize"])
jac = S.jaccard_matrix(corpus, R["input_roots"], R["normalize"])
dice = S.dice_matrix(corpus, R["input_roots"], R["normalize"])


def _matrix_summary(m, label):
    if m.empty:
        return "(no data)"
    off = []
    for i, a in enumerate(m.index):
        for j, b in enumerate(m.columns):
            if i < j:
                off.append((a, b, m.iloc[i, j]))
    if not off:
        return "(no pairs)"
    off_clean = [t for t in off if pd.notna(t[2])]
    if not off_clean:
        return "(all NaN — no shared ayahs)"
    top = max(off_clean, key=lambda x: x[2])
    bot = min(off_clean, key=lambda x: x[2])
    return (f"- **Highest {label}**: {top[0]} ↔ {top[1]} = {top[2]:.3f}\n"
            f"- **Lowest {label}**: {bot[0]} ↔ {bot[1]} = {bot[2]:.3f}")


_tile("4 · PMI — positive = associated above chance",
      chart=SC.chart_pmi_heatmap(pmi),
      summary_md=_matrix_summary(pmi, "PMI"),
      table=pmi.reset_index().rename(columns={"index": "Root"}))
st.divider()

_tile("5 · Conditional probability P(B | A) — read row by row",
      chart=SC.chart_cond_prob_heatmap(cond),
      summary_md=(
          "Each row shows: given that root A appears, what's the chance B is also there?\n\n"
          + _matrix_summary(cond, "P(B|A) off-diag")
      ),
      table=cond.reset_index().rename(columns={"index": "Given A"}))
st.divider()

# 5b — REVERSE direction: P(A|B)
import pandas as _pd_asym
_tile("5b · REVERSE direction — P(A | B): does B imply A?",
      chart=SC.chart_cond_prob_reverse_heatmap(cond),
      summary_md=(
          "Same data, different question.  P(B|A) ≠ P(A|B) because the roots "
          "have different sizes.  When one direction is much higher than the "
          "other, you have a one-way implication."
      ),
      table=cond.T.reset_index().rename(columns={"index": "Given B"}))
st.divider()

# Asymmetry summary table — which pairs are most lopsided?
st.subheader("5c · Implication asymmetry — which pairs are most one-way?")
_asym_rows = []
for _a in R["input_roots"]:
    for _b in R["input_roots"]:
        if _a == _b:
            continue
        try:
            _pba = float(cond.loc[_a, _b])  # P(B|A)
            _pab = float(cond.loc[_b, _a])  # P(A|B)
        except Exception:
            continue
        _diff = abs(_pba - _pab)
        _stronger = f"{_a} → {_b}" if _pba > _pab else f"{_b} → {_a}"
        _asym_rows.append({
            "Pair": f"{_a} ↔ {_b}" if _a < _b else f"{_b} ↔ {_a}",
            "P(B|A)": round(_pba, 3),
            "P(A|B)": round(_pab, 3),
            "|asymmetry|": round(_diff, 3),
            "Stronger direction": _stronger,
        })
if _asym_rows:
    _asym_df = (_pd_asym.DataFrame(_asym_rows)
                  .drop_duplicates(subset=["Pair", "Stronger direction"])
                  .sort_values("|asymmetry|", ascending=False)
                  .head(20))
else:
    _asym_df = _pd_asym.DataFrame()
if not _asym_df.empty:
    st.dataframe(_asym_df, width='content', hide_index=True, height=300)
    st.caption(
        "**Read it like this:** a row with `P(B|A)=0.80, P(A|B)=0.10` means "
        "*whenever A appears, B follows 80% of the time, but B alone only "
        "accompanies A in 10% of B-ayahs* — so A practically implies B but not vice versa."
    )
st.divider()

_tile("6 · Jaccard similarity (intersection / union)",
      chart=SC.chart_jaccard_heatmap(jac),
      summary_md=_matrix_summary(jac, "Jaccard"),
      table=jac.reset_index().rename(columns={"index": "Root"}))
st.divider()

# Cluster dendrogram if scipy available
_tile("7 · Hierarchical clustering (dendrogram)",
      chart=SC.chart_dendrogram(jac),
      summary_md=(
          "Average-linkage clustering on distance = 1 − Jaccard. "
          "Close branches = roots that share many ayahs."
      ),
      table=dice.reset_index().rename(columns={"index": "Root"}),
      table_height=200)
st.divider()

# 7b — Metric cross-reference (PMI vs Jaccard scatter with quadrants)
_tile("7b · 💡 METRIC CROSS-REFERENCE — do PMI and Jaccard agree?",
      chart=SC.chart_metric_cross_reference(pmi, jac, R["input_roots"]),
      summary_md=(
          "Each dot is one pair of your input roots.  X = PMI (above-chance "
          "association in bits).  Y = Jaccard (fraction of shared / union ayahs).\n\n"
          "- **Top-right** (green corner): strongly associated AND frequent — clear semantic pair.\n"
          "- **Top-left** (orange corner): frequent but unsurprising — large common roots that "
          "coincide by sheer volume, not by meaning.\n"
          "- **Bottom-right** (violet corner): 💎 **hidden gems** — strong association but rare "
          "overlap. Small pairs that carry disproportionate semantic weight; worth investigating "
          "the actual ayahs they share.\n"
          "- **Bottom-left** (gray): no real signal in either dimension.\n\n"
          "When the two metrics agree (dots line up roughly diagonally) you have a "
          "robust pattern.  When they disagree, the corner the dot sits in tells you "
          "WHY they disagree."
      ),
      table=None)

# ───────────────────────────────────────────────────────────────────
# LAYER 4 — surahs (importance · TF-IDF · enrichment)
# ───────────────────────────────────────────────────────────────────
st.divider()
layer(4, "Surah role & importance for the query")

sr = S.surah_role(corpus, R["input_roots"], R["normalize"])
_tile("8 · Surah importance ranking",
      chart=SC.chart_surah_role_bar(sr),
      summary_md=(
          f"**{len(sr)} surahs** contain at least one input root.\n\n"
          + (f"- Highest-importance surah: **{sr.iloc[0]['Surah Name']}** "
             f"(#{sr.iloc[0]['Surah #']}) with score {sr.iloc[0]['Importance score']}\n"
             f"- {sr.iloc[0]['Total hits']} total hits across "
             f"{sr.iloc[0]['Input roots present']} of {len(R['input_roots'])} input roots\n"
             f"- {sr.iloc[0]['Share of surah from input roots']}% of this surah's root "
             f"tokens are from your input set"
             if not sr.empty else "")
      ),
      table=sr.head(30))
st.divider()

tfidf = S.surah_tfidf(corpus, R["input_roots"], R["normalize"])
_tile("9 · TF-IDF — surahs most characteristic for each root",
      chart=SC.chart_tfidf_dot(tfidf),
      summary_md=(
          "TF-IDF rewards surahs where a root is over-represented relative to the rest "
          "of the corpus. A high TF-IDF means the root really 'belongs' to that surah.\n\n"
          + (f"- Top TF-IDF overall: **{tfidf.iloc[0]['Surah Name']} (#{tfidf.iloc[0]['Surah #']})** "
             f"for root **{tfidf.iloc[0]['Input Root']}**" if not tfidf.empty else "")
      ),
      table=tfidf,
      table_height=320)
st.divider()

enr = S.surah_enrichment(corpus, R["input_roots"], R["normalize"], max_p=0.5)
_tile("10 · Surah enrichment — hypergeometric test",
      chart=SC.chart_enrichment_scatter(enr),
      summary_md=(
          "Volcano plot: x = how many times more than expected, y = significance (−log₁₀ p). "
          "Top-right corner = both strongly enriched AND statistically significant.\n\n"
          + (f"- {len(enr[enr['p-value'] < 0.05])} (root, surah) pairs significant at p<0.05\n"
             f"- Strongest: **{enr.iloc[0]['Input Root']}** in **{enr.iloc[0]['Surah Name']}** "
             f"(p = {enr.iloc[0]['p-value']:.2e}, enrichment = "
             f"{enr.iloc[0]['Enrichment (obs/exp)']}×)" if not enr.empty else "")
      ),
      table=enr.head(30),
      table_height=320)
st.divider()

cum = S.cumulative_trajectory(corpus, R["input_roots"], R["normalize"])
_tile("11 · Cumulative trajectory across surah order",
      chart=SC.chart_cumulative(cum),
      summary_md=(
          "How each root accumulates hits as you read through surahs 1 → 114. "
          "A steep slope = the root concentrates in those surahs."
      ),
      table=cum.groupby("Input Root").tail(1)[["Input Root", "Surah #", "Cumulative hits"]]
            .rename(columns={"Surah #": "At surah", "Cumulative hits": "Total"}),
      table_height=200)

# ───────────────────────────────────────────────────────────────────
# LAYER 5 — network extras + exclusive partners
# ───────────────────────────────────────────────────────────────────
st.divider()
layer(5, "Network depth — PageRank, k-core, ego density")

net = S.network_extras(R["graph"])
metric = st.selectbox("Rank by", ["PageRank", "k-core", "Ego density", "Triangles@node"],
                      key="net_metric")
_tile(f"12 · {metric} ranking",
      chart=SC.chart_network_extras(net, metric=metric),
      summary_md=(
          "- **PageRank**: random-walk importance (weighted edges).\n"
          "- **k-core**: highest k such that this node sits in a k-densely-connected subgraph.\n"
          "- **Ego density**: how densely THIS node's immediate neighborhood interconnects.\n"
          "- **Triangles@node**: number of closed triangles touching the node.\n"
          + (f"\nTop by {metric}: **{net.iloc[0]['Root']}** "
             f"({metric.lower()} = {net.iloc[0][metric]})"
             if not net.empty else "")
      ),
      table=net.head(25),
      table_height=320)
st.divider()

excl = S.exclusive_partners(corpus, R["input_roots"], R["normalize"], max_other=0)
_tile("13 · Exclusive partners — roots that only appear with yours",
      chart=SC.chart_exclusive_partners(excl),
      summary_md=(
          f"- **{len(excl)}** roots appear ≥2 times AND never outside the input-root ayahs.\n"
          "- These are 'signature' companions: extremely associated with your query.\n"
      ),
      table=excl.head(40),
      table_height=320)

st.divider()

# ───────────────────────────────────────────────────────────────────
# LAYER 5b — GRAPH-LEVEL STATISTICS  (mirrors Network page §1)
# ───────────────────────────────────────────────────────────────────
layer(5, "Graph-level statistics — surfaced from the Network tab")
st.caption(
    "These are properties of the **whole input-root co-occurrence graph**.  "
    "For full graph visualisations of each, open the 🌐 Network tab."
)
_ns = R.get("net_stats", {})
if _ns:
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Nodes", _ns.get("nodes", 0))
    c2.metric("Edges", _ns.get("edges", 0))
    c3.metric("Density", _ns.get("density", 0))
    c4.metric("Modularity", _ns.get("modularity", 0),
              help="0 = no community structure; >0.3 = clear themes")
    c5.metric("Diameter", _ns.get("diameter", 0))
    c6.metric("k-core max", _ns.get("k_core_max", 0))
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Mean degree", _ns.get("mean_degree", 0))
    c2.metric("Mean path", _ns.get("mean_shortest_path", 0))
    c3.metric("Assortativity", _ns.get("assortativity", 0),
              help="Positive = hubs link to hubs; negative = hubs link to peripherals")
    c4.metric("Articulation pts", _ns.get("n_articulation_points", 0))
    c5.metric("Bridges", _ns.get("n_bridges", 0))
    c6.metric("Giant comp %", f"{_ns.get('giant_component_pct', 0)}%")

# ───────────────────────────────────────────────────────────────────
# LAYER 5c — TEMPORAL STATISTICS (Meccan vs Medinan)
# ───────────────────────────────────────────────────────────────────
if R.get("has_rev_order"):
    st.divider()
    layer(5, "Temporal statistics — Meccan vs Medinan")
    st.caption(
        "Powered by the **revelation-order column** in book6.  "
        "Phase split uses the Egyptian-standard cutoff (rev_order ≤ 86 = Meccan)."
    )

    # Per-root Meccan/Medinan tally (from node_attrs if available)
    _na = R.get("node_attrs")
    if _na is not None and not _na.empty and "Meccan Ayahs" in _na.columns:
        _phase_view = _na[["Root", "Total", "Meccan Ayahs", "Medinan Ayahs",
                           "Meccan %", "First Rev-Order Surah",
                           "Gravitational Center"]].copy()
        st.markdown("**Per-root Meccan/Medinan distribution**")
        st.dataframe(_phase_view, width='content', hide_index=True,
                     height=240)

    # Per-pair Meccan/Medinan distribution (joint ayahs)
    _pp = R.get("pair_phase")
    if _pp is not None and not _pp.empty:
        st.markdown("**Per-pair joint-ayah Meccan/Medinan distribution**")
        st.caption("Of all ayahs where BOTH roots in the pair co-occur, "
                   "what fraction is Meccan vs Medinan?")
        st.dataframe(_pp, width='content', hide_index=True,
                     height=240)

    # Phase-diff edge counts (from network)
    n_both = len(R.get("phase_in_both", []))
    n_meccan_only = len(R.get("phase_only_meccan", []))
    n_medinan_only = len(R.get("phase_only_medinan", []))
    if n_both or n_meccan_only or n_medinan_only:
        st.markdown("**Phase-diff edge counts** (from the input-root co-occurrence graph)")
        c1, c2, c3 = st.columns(3)
        c1.metric("⚫ Stable (both phases)", n_both)
        c2.metric("🟠 Meccan-only", n_meccan_only)
        c3.metric("🔵 Medinan-only", n_medinan_only)
        _total = max(n_both + n_meccan_only + n_medinan_only, 1)
        st.caption(f"**Stability:** {round(100 * n_both / _total, 1)}% of "
                   f"co-occurrences appear in both phases.  "
                   f"For the full phase-diff network visualisation, "
                   f"open the 🌐 Network tab.")

st.divider()

# ───────────────────────────────────────────────────────────────────
# LAYER 6 — cross-validation
# ───────────────────────────────────────────────────────────────────
st.divider()
layer(6, "Cross-validation — sanity checks across pages")

xv = S.cross_validation(corpus, R["input_roots"], R["normalize"], R)
st.dataframe(xv, width='content', hide_index=True, height=320)
n_ok = (xv["Status"] == "✓").sum() if not xv.empty else 0
n_warn = (xv["Status"] == "⚠").sum() if not xv.empty else 0
if n_warn == 0:
    st.success(f"All {n_ok} checks consistent.")
else:
    st.warning(f"{n_warn} check(s) inconsistent — see status column.")

st.caption(
    "Every chart above has the same source table shown next to it, so any number "
    "in any chart can be traced back to a row in the corresponding table. Use the "
    "**Export** page to download all of these tables as Excel / CSV."
)
