# re-deploy 1779671310
"""Network analysis — graph-first scrolling page.
All visualizations are visible by scrolling (no hidden tabs).
TEMPORAL section is pinned near the top.
Every chart is wrapped in try/except so one failure can't blank the page."""
import pandas as pd
import streamlit as st

import plotly_charts as PC
import analysis as A
from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, per_root_hint, log_page)

st.set_page_config(page_title="Network", page_icon="🌐", layout="wide")
log_page("network")

# ── Interpretation guide + mobile landscape hint ─────────────────────
st.markdown('<div class="landscape-hint">📱 Tip: rotate your phone sideways (landscape) for a clearer network view.</div>', unsafe_allow_html=True)
with st.expander("📌 How to read this network (1-min)", expanded=False):
    st.markdown(
        "**An edge = these two roots share ayahs.** It does **not** say "
        "they mean the same thing. Two roots can share ayahs because they "
        "are paired contrastively (e.g. mercy vs. wrath), causally, or "
        "thematically — the network does not distinguish these.\n\n"
        "- **Node size / colour** = your input roots vs. partner roots\n"
        "- **Edge thickness** = number of shared ayahs\n"
        "- **Communities** (coloured groups) = roots that cluster together\n"
        "- **Bridges** = single edges that connect otherwise separate groups\n\n"
        "To see *how* two roots actually pair, open the **Ayah Browser** "
        "page and read the verses where they co-occur. The **🧭 Reading "
        "guide** page also lists data-driven facts about your session."
    )

corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()
g = R["graph"]
ns = R["net_stats"]
has_rev = R.get("has_rev_order", False)


# ─────────────────────────────────────────────────────────────────
# VERSION BANNER — so the user can confirm they're on the latest build
# ─────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="background:#1D3557;
                color:white; padding:6px 14px; border-radius:8px;
                margin-bottom:6px; font-size:12px; font-weight:700;
                letter-spacing:0.4px;">
      Network v10
    </div>
    """,
    unsafe_allow_html=True,
)

hero("🌐 Root Co-occurrence Network",
     "16 network views — scroll to see all"
     + ("  ·  Revelation-order ✓" if has_rev else "  ·  ⚠️ no revelation-order column"))
per_root_hint(compact=True)

# ── SELF-REFERENCE LOCALITY (Latent Feature L08) — self-contained, reads viz_data.json ──
try:
    import os as _os
    import json as _json
    import plotly.graph_objects as _go
    _vzp = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                         "research", "intrinsic", "viz_data.json")
    _rec = _json.load(open(_vzp, encoding="utf-8")).get("recurrence2", [])
    if _rec:
        layer(1, "SELF-REFERENCE RANGE — how far the text echoes itself")
        st.caption("A word's recurrence over a shuffle baseline, by window size. The text references itself "
                   "at a definite ~passage scale — strong within ~16 tokens, back to chance (1.0) by ~256 "
                   "(Latent Feature L08). Open the 🧬 Latent Feature Ledger for the full review.")
        _f = _go.Figure(_go.Scatter(x=[p[0] for p in _rec], y=[p[1] for p in _rec], mode="lines+markers",
            line=dict(color="#118AB2", width=1.6), marker=dict(size=6)))
        _f.add_hline(y=1.0, line_dash="dash", line_color="#C1121F", annotation_text="chance")
        _f.update_layout(height=300, margin=dict(l=6, r=6, t=8, b=6), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="window (tokens, log)", type="log", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="recurrence × shuffle", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=11, color="#1D3557"))
        st.plotly_chart(_f, width='stretch', key="net_self_reference_L08")
        try:
            st.page_link("pages/25_Latent_Features.py", label="See L08 in the Latent Feature Ledger", icon="🧬")
        except Exception:
            pass
except Exception:
    pass


# Helper: safe plotly_chart that won't blank the rest of the page on failure
def safe_chart(fn, *args, **kwargs):
    try:
        fig = fn(*args, **kwargs)
        st.plotly_chart(fig, width='stretch')
    except Exception as e:
        st.error(f"⚠️ Chart `{fn.__name__}` failed: {type(e).__name__}: {e}")


# ─────────────────────────────────────────────────────────────────
# § 1 — NETWORK STATISTICS (always at top)
# ─────────────────────────────────────────────────────────────────
st.markdown("## 📊 Stats")
st.caption("Whole-graph metrics.")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Nodes", ns["nodes"], help="Roots in this network: your query + partners above threshold.")
c2.metric("Edges", ns["edges"], help="Root pairs sharing ≥1 verse; weight = number of shared verses.")
c3.metric("Density", ns["density"],
          help="Share of all possible pairs that actually co-occur (0–1). Sparse + clustered "
               "is the interesting regime.")
c4.metric("Modularity", ns["modularity"],
          help="0 = no community structure; >0.3 = clear communities (the colour groups below "
               "are real, not cosmetic).")
c5.metric("Diameter", ns["diameter"],
          help="Longest shortest-path between any two roots — how 'wide' the theme field is.")
c6.metric("k-core max", ns["k_core_max"],
          help="Depth of the densest shell: the max k where every member still has k "
               "neighbours inside the shell. High = a hard thematic core.")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Mean degree", ns["mean_degree"], help="Average partners per root in this neighbourhood.")
c2.metric("Mean path", ns["mean_shortest_path"],
          help="Average hops between roots — small-world neighbourhoods sit around 2–3.")
c3.metric("Assortativity", ns["assortativity"],
          help="> 0: hubs link to hubs (elite core). < 0: hubs link to periphery "
               "(star/broadcast shape — typical for a strong seed root).")
c4.metric("Articulation pts", ns["n_articulation_points"],
          help="Roots whose removal would DISCONNECT the network — single points of failure, "
               "i.e. the roots that alone hold themes together (drawn ★ in §5).")
c5.metric("Bridges", ns["n_bridges"],
          help="Edges whose removal would split the network — one-verse lifelines between "
               "otherwise separate themes (drawn red in §5).")
c6.metric("Giant comp %", f"{ns['giant_component_pct']}%",
          help="Share of roots in the single largest connected piece. 100% = one connected "
               "theme field; lower = islands.")
try:
    _mod = float(ns["modularity"]); _gc = float(ns["giant_component_pct"])
    _nart = int(ns["n_articulation_points"]); _nbr = int(ns["n_bridges"])
    _cm = R.get("communities")
    try:
        _ncomm = (len(set(_cm.values())) if hasattr(_cm, "values") else len(_cm))
    except Exception:
        _ncomm = "several"
    st.markdown(
        "**📍 What to take from the stats:** "
        + (f"clear community structure (modularity {_mod} > 0.3) — this neighbourhood splits "
           f"into ~{_ncomm} real thematic clusters; read the Communities gallery (§7) next."
           if _mod > 0.3 else
           f"weak community structure (modularity {_mod} ≤ 0.3) — one blended field rather "
           f"than separable themes; centrality (§8) is more informative than communities here.")
        + f" {_gc:.0f}% of roots form one connected field; "
        + (f"**{_nart} articulation point(s) + {_nbr} bridge(s)** are load-bearing — §5 names "
           f"the exact roots/edges holding themes together."
           if (_nart + _nbr) > 0 else
           "no articulation points or bridges — robust: no single root holds it together.")
        + " Boundary (#65): this topology is GENERAL to language — a MAP of your query, never "
          "a distinctiveness claim; PPMI-normalize before reading hubs as important.")
except Exception:
    pass

st.divider()


# ── Edge weighting (ONE control governing ALL graph views below) ──────────────
import math as _m
from collections import Counter as _C
st.markdown("### Edge weighting")
_wmode = st.radio("Weight every graph's edges by",
                  ["Attraction · PPMI (recommended)", "Shared verses (raw)"],
                  horizontal=True, index=0, key="net_wmode",
                  help="Raw count is dominated by ubiquitous roots (الله, قوم). PPMI = co-occurrence "
                       "BEYOND chance, so true concept pairs dominate and ubiquitous edges shrink/drop.")
_attraction = _wmode.startswith("Attraction")
@st.cache_data(show_spinner=False)
def _docf_cached(_cid):
    d = _C()
    for _i in range(len(corpus.df)):
        for _r in {t for t in corpus.root_tokens[_i] if t and t != "-"}: d[_r] += 1
    return dict(d)
_DOCF = _docf_cached(id(corpus)); _NV = len(corpus.df)
def _apply_w(graph):
    """Return a PPMI-reweighted copy (above-chance edges only) when attraction mode is on."""
    if not _attraction or graph is None or graph.number_of_edges() == 0: return graph
    g2 = graph.copy(); _drop = []
    for _a, _b, _d in g2.edges(data=True):
        _w = _d.get("weight", 1); _pa = _DOCF.get(_a, 1) / _NV; _pb = _DOCF.get(_b, 1) / _NV; _pab = _w / _NV
        _pm = max(0.0, _m.log(_pab / (_pa * _pb))) if _pa > 0 and _pb > 0 and _pab > 0 else 0.0
        if _pm <= 0: _drop.append((_a, _b))
        else: _d["weight"] = round(_pm, 3)
    g2.remove_edges_from(_drop)
    return g2
if _attraction:
    st.caption("All graphs below are weighted by **attraction (PPMI)** — above-chance pairings only; "
               "ubiquitous-root edges drop out. Switch to raw to compare.")

# ─────────────────────────────────────────────────────────────────
# § 2 — TEMPORAL / PHASE ANALYSIS (pinned high — most novel content)
# ─────────────────────────────────────────────────────────────────
st.markdown("## 📜 Temporal")
if not has_rev:
    st.warning("This section needs the revelation-order column in book6. "
               "Without it the rest of the page still works in mushaf order.")
else:
    st.caption(
        "Networks built from phase-filtered ayahs."
    )

    # § 2a — Side-by-side Meccan vs Medinan networks
    st.markdown("### Meccan vs Medinan")
    gm, gd = _apply_w(R["g_meccan"]), _apply_w(R["g_medinan"])
    cM1, cM2, cM3 = st.columns(3)
    cM1.metric("Meccan edges", gm.number_of_edges() if gm else 0)
    cM2.metric("Medinan edges", gd.number_of_edges() if gd else 0)
    cM3.metric("Shared edges", len(R["phase_in_both"]),
               help="Co-occurrences that appear in BOTH phases")
    safe_chart(PC.chart_phase_networks, gm, gd)

    # § 2b — 4-stage evolution
    st.markdown("### 4-stage evolution")
    st.caption(
        "Early / Middle / Late Meccan · Medinan."
    )
    def _build(lo, hi):
        return A.build_phase_subgraph(corpus, R["input_roots"], normalize,
                                       lo, hi,
                                       top_partners=top_p, min_weight=min_w)
    safe_chart(PC.chart_4stage_evolution, corpus, _build)

    # § 2c — Phase Diff
    st.markdown("### Phase diff")
    cP1, cP2, cP3 = st.columns(3)
    cP1.metric("⚫ Stable (both)", len(R["phase_in_both"]))
    cP2.metric("🟠 Meccan-only", len(R["phase_only_meccan"]))
    cP3.metric("🔵 Medinan-only", len(R["phase_only_medinan"]))
    safe_chart(PC.chart_phase_diff_graph, R["g_meccan"], R["g_medinan"],
                R["phase_only_meccan"], R["phase_only_medinan"],
                R["phase_in_both"])
    try:
        _nb = len(R["phase_in_both"]); _nm = len(R["phase_only_meccan"])
        _nd = len(R["phase_only_medinan"]); _tp = _nb + _nm + _nd
        if _tp:
            st.markdown(
                f"**📍 What to take from the phase diff:** {_nb}/{_tp} pairings "
                f"(**{100 * _nb / _tp:.0f}%**) survive BOTH periods — the stable spine of this "
                f"concept's company; {_nm} are Meccan-only, {_nd} Medinan-only — vocabulary the "
                f"mission phase added or retired. Filed context (#70): narrative anchors stay "
                f"continuous across revelation time while some seals ride waves — check whether "
                f"your phase-specific pairs are seal-like or narrative-like. The Meccan/Medinan "
                f"cut is a traditional control frame, not a claim.")
    except Exception:
        pass

    # § 2c+ — ATTRACTION-edge phase diff: which PAIRINGS are stable vs phase-specific
    if _attraction and gm is not None and gd is not None and (gm.number_of_edges() or gd.number_of_edges()):
        _em = {frozenset((a, b)): d["weight"] for a, b, d in gm.edges(data=True)}
        _ed = {frozenset((a, b)): d["weight"] for a, b, d in gd.edges(data=True)}
        _stable = _em.keys() & _ed.keys(); _mo = _em.keys() - _ed.keys(); _do = _ed.keys() - _em.keys()
        st.markdown("#### Pairing diff — attraction edges")
        _a1, _a2, _a3 = st.columns(3)
        _a1.metric("⚫ Stable pairings", len(_stable))
        _a2.metric("🟠 Meccan-only", len(_mo))
        _a3.metric("🔵 Medinan-only", len(_do))
        def _pchips(_S, _d, _bg):
            _it = sorted(_S, key=lambda e: -_d[e])[:10]
            return " ".join(f"<span style='background:{_bg};border-radius:5px;padding:1px 7px;"
                            f"white-space:nowrap;font-size:12px'>{'—'.join(sorted(e))}</span>" for e in _it)
        st.markdown(
            "<div style='direction:rtl;text-align:right;line-height:2.1'>"
            "<div style='font-size:12px;color:#10243A;margin-top:2px'><b>⚫ Stable (both phases)</b></div>"
            + _pchips(_stable, {**_em, **_ed}, "#e7eef0")
            + "<div style='font-size:12px;color:#10243A;margin-top:4px'><b>🟠 Meccan-only</b></div>"
            + _pchips(_mo, _em, "#fdebd3")
            + "<div style='font-size:12px;color:#10243A;margin-top:4px'><b>🔵 Medinan-only</b></div>"
            + _pchips(_do, _ed, "#dbe7f5") + "</div>", unsafe_allow_html=True)
        st.caption("Above-chance concept PAIRINGS that persist vs are unique to a phase — what the "
                   "mission phase kept, added, or retired. Attraction edges only; switch to raw to compare.")

    # § 2d — Sankey
    st.markdown("### Phase-flow Sankey")
    st.caption(
        "Meccan ayahs (left) → Medinan ayahs (right). Width = weight."
    )
    safe_chart(PC.chart_sankey_phase_flow, R["g_meccan"], R["g_medinan"])

    # § 2e — Per-pair Meccan/Medinan breakdown
    st.markdown("### Per-pair phase split")
    if not R["pair_phase"].empty:
        st.dataframe(R["pair_phase"], width='content',
                     hide_index=True, height=240)

st.divider()


# ─────────────────────────────────────────────────────────────────
# § 3 — TOPOLOGY — three layouts of the SAME graph
# ─────────────────────────────────────────────────────────────────
st.markdown("## 🕸️ Topology")
st.caption(
    "Same graph, three layouts."
)

gv = _apply_w(g)
if _attraction and g.number_of_edges():
    st.caption(f"Force / chord / adjacency weighted by **attraction (PPMI)** — {gv.number_of_edges()} of "
               f"{g.number_of_edges()} edges are above-chance pairings.")

st.markdown("### Force-directed")
st.markdown(
    '<div style="background:#EEF3FB;'
    'border-left:5px solid #1D3557;padding:10px 14px;border-radius:8px;'
    'font-size:13.5px;line-height:1.55;color:#243447;margin:6px 0;">'
    '<b>Legend.</b> '
    '<span style="background:#E63946;color:#fff;padding:2px 8px;border-radius:8px;font-weight:700;">RED</span> = '
    'your input root(s). '
    '<span style="background:#EF9F27;color:#fff;padding:2px 8px;border-radius:8px;font-weight:700;">ORANGE</span> / '
    '<span style="background:#378ADD;color:#fff;padding:2px 8px;border-radius:8px;font-weight:700;">BLUE</span> / '
    '<span style="background:#7209B7;color:#fff;padding:2px 8px;border-radius:8px;font-weight:700;">PURPLE</span> = '
    'distinct <b>Louvain communities</b> (each colour is one cluster of partner roots that travel together). '
    '<b>Node size</b> = weighted degree (more shared ayahs = larger). '
    '<b>Edge thickness</b> = how often the two roots appear together.'
    '</div>',
    unsafe_allow_html=True,
)
safe_chart(PC.chart_network, gv, R["communities"])

st.markdown("### Chord")
st.caption("Nodes on a ring, edges as chords.")
safe_chart(PC.chart_chord_diagram, gv, R["communities"])

st.markdown("### Adjacency matrix")
st.caption("Roots × roots, cell = ayahs shared.")
safe_chart(PC.chart_adjacency_matrix, gv)

st.divider()


# ─────────────────────────────────────────────────────────────────
# § 4 — LEAD-LAG — directed graph + arc diagram
# ─────────────────────────────────────────────────────────────────
st.markdown("## ➡️ Lead-Lag")
dg = R["dg_lead_lag"]
if dg.number_of_edges() == 0:
    st.info("No directional lead-lag relationships above threshold for current roots.")
else:
    st.markdown("### Directed graph")
    st.caption(
        "Arrow A→B means A leads B. Thickness = P(B near A)."
    )
    safe_chart(PC.chart_directed_lead_lag, dg)

    st.markdown("### Arc diagram")
    st.caption("Arcs above = forward; arcs below = reverse.")
    safe_chart(PC.chart_arc_diagram, dg)

st.divider()


# ─────────────────────────────────────────────────────────────────
# § 5 — ROBUSTNESS — articulation, bridges, MST, k-core
# ─────────────────────────────────────────────────────────────────
st.markdown("## 🛡️ Robustness")

st.markdown("### Articulation + bridges")
st.caption(
    "★ = articulation point. Red edge = bridge. Zero of each = robust."
)
safe_chart(PC.chart_robustness_overlay, g, ns["articulation_points"],
            ns["bridge_edges"], R["communities"])
if ns["articulation_points"]:
    st.markdown("**Articulation points:** "
                + " · ".join(f"`{n}`" for n in ns["articulation_points"]))
if ns["bridge_edges"]:
    st.markdown("**Bridge edges:** "
                + " · ".join(f"`{u} — {v}`" for u, v in ns["bridge_edges"]))

st.markdown("### MST backbone")
st.caption("The network's spine.")
safe_chart(PC.chart_mst_backbone, g)

st.markdown("### k-core layers")
st.caption("Inner ring = dense core; outer = peripheral.")
safe_chart(PC.chart_kcore_layered, g)

st.divider()


# ─────────────────────────────────────────────────────────────────
# § 6 — EGO NETWORKS — per-root mini graphs
# ─────────────────────────────────────────────────────────────────
st.markdown("## 🎯 Ego networks")
st.caption(
    "One mini-network per input root."
)
safe_chart(PC.chart_per_root_ego_gallery, g, R["input_roots"], max_neighbors=8)

st.divider()


# ─────────────────────────────────────────────────────────────────
# § 7 — COMMUNITIES — gallery + hierarchy
# ─────────────────────────────────────────────────────────────────
st.markdown("## 🌐 Communities")

st.markdown("### Gallery")
st.caption("One mini-network per community.")
safe_chart(PC.chart_community_subnetworks, g, R["communities"], top_n=12)

st.markdown("### Hierarchy")
st.caption("Parent = community; children = its roots.")
safe_chart(PC.chart_community_dendrogram, g, R["communities"])

st.divider()


# ─────────────────────────────────────────────────────────────────
# § 8 — CENTRALITY & DETAIL TABLES
# ─────────────────────────────────────────────────────────────────
st.markdown("## 📈 Centrality & tables")
metric_pick = st.selectbox(
    "Rank by", ["Weighted Degree", "Degree", "Betweenness",
                "Eigenvector", "Clustering"], key="cent_metric")
safe_chart(PC.chart_centrality, R["centrality"], metric=metric_pick, top=20)

with st.expander("📊 Full centrality table", expanded=False):
    st.dataframe(R["centrality"], width='content',
                 hide_index=True, height=420)
