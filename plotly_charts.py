"""Vibrant interactive Plotly charts for the dashboard."""
from __future__ import annotations

from collections import Counter

import networkx as nx
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Vibrant palette
PAL = {
    "input": "#E63946",       # vivid red
    "partner": "#1D3557",     # navy
    "accent": "#F77F00",      # orange
    "good": "#06A77D",        # green
    "violet": "#7209B7",
    "teal": "#06AED5",
    "gold": "#FCBF49",
    "bg": "#FFFFFF",
}

CONTINUOUS = "Plasma"
DIVERGING = "RdBu_r"


def _layout(fig: go.Figure, title: str = "", h: int | None = None) -> go.Figure:
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.5, xanchor="center", font=dict(size=18)),
        paper_bgcolor=PAL["bg"],
        plot_bgcolor="#F8FAFC",
        font=dict(family="Arial, 'Segoe UI', sans-serif", size=13, color="#1B263B"),
        margin=dict(l=30, r=20, t=46, b=30),
        hoverlabel=dict(bgcolor="white", font_size=13),
    )
    if h:
        fig.update_layout(height=h)
    return fig


# ---------------------------------------------------------------------------
# Bird's-eye / overview
# ---------------------------------------------------------------------------
def chart_summary_metric_bars(summary: pd.DataFrame) -> go.Figure:
    """Bird's-eye stacked-bar of ayahs/surahs/hits per input root."""
    df = summary[~summary["Input Root"].str.startswith("—")].copy()
    if df.empty:
        return _layout(go.Figure(), "Summary")
    df_long = df.melt(id_vars="Input Root",
                      value_vars=["Ayahs Found", "Surahs Covered", "Total Hits"],
                      var_name="Metric", value_name="Count")
    fig = px.bar(df_long, x="Input Root", y="Count", color="Metric",
                 barmode="group",
                 color_discrete_sequence=[PAL["input"], PAL["accent"], PAL["teal"]])
    return _layout(fig, "Per-root summary", h=400)


def chart_distribution_across_surahs(occurrences: pd.DataFrame) -> go.Figure:
    if occurrences.empty:
        return _layout(go.Figure(), "Distribution across surahs")
    g = occurrences.groupby(["Surah #", "Input Root"]).size().reset_index(name="hits")
    fig = px.bar(g, x="Surah #", y="hits", color="Input Root",
                 color_discrete_sequence=px.colors.qualitative.Vivid,
                 labels={"hits": "Ayah hits"})
    fig.update_layout(barmode="stack", xaxis=dict(tickmode="linear", dtick=5))
    return _layout(fig, "Surah distribution", h=420)


def chart_rarity_tier(rarity: pd.DataFrame) -> go.Figure:
    if rarity.empty:
        return _layout(go.Figure(), "Rarity vs corpus baseline")
    tier_order = ["ultra-rare", "rare", "common", "very common", "ubiquitous"]
    tier_color = {"ultra-rare": "#7209B7", "rare": "#1D3557", "common": "#06AED5",
                  "very common": "#F77F00", "ubiquitous": "#E63946"}
    rr = rarity.copy()
    # contextualise each bar so even ONE root is meaningful: count + where it sits vs the corpus
    rr["_lbl"] = rr.apply(lambda r: f"{int(r['Ayah Frequency'])}× · {r['Percentile']:.0f}th pct · z {r['Z-score']:+.1f}", axis=1)
    fig = px.bar(rr, x="Input Root", y="Ayah Frequency",
                 color="Tier", color_discrete_map=tier_color,
                 category_orders={"Tier": tier_order}, text="_lbl",
                 hover_data=["Percentile", "Z-score", "Corpus Median"])
    fig.update_traces(textposition="outside", cliponaxis=False)
    # ONE thin median reference + a single corner label (no overlapping inline text, no redundant mean line)
    try:
        _med = float(rr["Corpus Median"].iloc[0])
        fig.add_hline(y=_med, line_dash="dash", line_width=1, line_color="#8FA6BC")
        fig.add_annotation(xref="paper", yref="paper", x=0.99, y=0.98, xanchor="right", yanchor="top",
                           text=f"– – corpus median ≈ {_med:g} (the typical root)", showarrow=False,
                           font=dict(size=12, color="#10243A"),
                           bgcolor="rgba(244,249,247,0.92)", bordercolor="#cfe4dc", borderwidth=1)
    except Exception:
        pass
    return _layout(fig, "Frequency vs corpus baseline", h=380)


def chart_revelation_profile(corpus, roots, normalize: bool = False) -> go.Figure:
    """When a concept enters the text: histogram of a root's occurrences across the nuzūl
    (revelation) order, split Meccan vs Medinan. SINGLE-ROOT-meaningful — unlike the pairwise
    comparison charts. Computed straight from the corpus (revelation column + root tokens)."""
    df = corpus.df
    NZ = "ترتیب نزول"
    if NZ not in df.columns:
        return _layout(go.Figure(), "Revelation profile")
    nz = pd.to_numeric(df[NZ], errors="coerce")
    fold = lambda t: str(t).replace("ك", "ک").replace("ي", "ی")
    rootset = {fold(r) for r in roots}
    rows = []
    for i in range(len(df)):
        v = nz.iloc[i]
        if pd.isna(v):
            continue
        for r in {fold(t) for t in corpus.root_tokens[i]} & rootset:
            rows.append({"root": r, "nuzūl": int(v),
                         "era": "Meccan" if v <= 86 else "Medinan"})
    if not rows:
        return _layout(go.Figure(), "Revelation profile")
    rdf = pd.DataFrame(rows)
    multi = rdf["root"].nunique() > 1
    fig = px.histogram(rdf, x="nuzūl", color="era", nbins=38,
                       color_discrete_map={"Meccan": "#1D9E75", "Medinan": "#378ADD"},
                       facet_row="root" if multi else None)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.add_vline(x=86.5, line_dash="dash", line_color="#10243A",
                  annotation_text="Meccan ◂ │ ▸ Medinan", annotation_position="top",
                  annotation_font_color="#10243A")
    fig.update_layout(xaxis_title="revelation order  (1 = first revealed … 114 = last)",
                      yaxis_title="occurrences", bargap=0.04, legend_title_text="")
    return _layout(fig, "Revelation profile — when this concept enters the text",
                   h=380 if not multi else max(380, 180 * rdf["root"].nunique()))


def chart_meaning_neighbors(semf, root, top: int = 12) -> go.Figure:
    """Top MEANING-relatives of a concept from the on-corpus semantic embedding (cosine) — the
    'nearest in meaning' partners, distinct from co-occurrence (context) partners. Single-concept."""
    import semantic_features as _SF
    try:
        nb = _SF.root_neighbors(semf, root, topn=top)
    except Exception:
        nb = []
    if not nb:
        return _layout(go.Figure(), "Nearest in meaning")
    nb = nb[::-1]                                   # ascending → strongest at top of horizontal bar
    ys = [r for r, _ in nb]
    xs = [float(s) for _, s in nb]
    fig = px.bar(x=xs, y=ys, orientation="h", text=[f"{s:.2f}" for s in xs],
                 color=xs, color_continuous_scale="Teal")
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(coloraxis_showscale=False, xaxis_title="cosine similarity", yaxis_title="")
    return _layout(fig, f"Nearest in meaning — {root}", h=max(320, 60 + 28 * len(nb)))


def chart_network_role(feat: dict, roots) -> go.Figure:
    """Place each concept in ROLE-SPACE from the precomputed (degree-normalised) graph features:
    x = within-family anchor (hub z), y = bridge / connector (betweenness z). Quadrants name the role."""
    fold = lambda t: str(t).replace("ك", "ک").replace("ي", "ی")
    pts = [(r, feat.get(fold(r))) for r in roots]
    pts = [(r, g) for r, g in pts if g]
    if not pts:
        return _layout(go.Figure(), "Network role")
    xs = [g["hub_z"] for _, g in pts]
    ys = [g["bridge_z"] for _, g in pts]
    labels = [f"{r}<br><span style='font-size:12px'>{g['family_label']}</span>" for r, g in pts]
    fig = go.Figure(go.Scatter(
        x=xs, y=ys, mode="markers+text", text=labels, textposition="top center",
        marker=dict(size=15, color="#1D9E75", line=dict(width=1, color="#0F6E56")),
        hovertext=[g["role"] for _, g in pts], hoverinfo="text"))
    fig.add_hline(y=2, line_dash="dot", line_color="#8FA6BC")
    fig.add_vline(x=2, line_dash="dot", line_color="#8FA6BC")
    fig.add_annotation(x=2.05, y=max(ys + [2.2]), text="bridge / connector ▲", showarrow=False,
                       xanchor="left", font=dict(size=11, color="#10243A"))
    fig.add_annotation(y=2.05, x=max(xs + [2.2]), text="family anchor ▶", showarrow=False,
                       yanchor="bottom", font=dict(size=11, color="#10243A"))
    fig.update_layout(xaxis_title="within-family anchor  (hub z)",
                      yaxis_title="bridge / connector  (betweenness z)")
    return _layout(fig, "Network role — anchor vs bridge", h=440)


# ---------------------------------------------------------------------------
# Per-root deep dive
# ---------------------------------------------------------------------------
def chart_per_root_surah_strip(occurrences: pd.DataFrame, root: str) -> go.Figure:
    sub = occurrences[occurrences["Input Root"] == root]
    if sub.empty:
        return _layout(go.Figure(), "Ayah hits per surah")
    counts = sub.groupby("Surah #").size().reset_index(name="hits")
    fig = px.bar(counts, x="Surah #", y="hits",
                 color="hits", color_continuous_scale=CONTINUOUS,
                 labels={"hits": "Hits", "Surah #": "Surah"})
    fig.update_layout(
        xaxis=dict(tickmode="linear", dtick=5),
        coloraxis_colorbar=dict(title="Hits", thickness=12, len=0.7),
    )
    return _layout(fig, f"Ayah hits per surah  ·  {root}", h=320)


def chart_surface_form_sunburst(surface_forms: pd.DataFrame, root: str,
                                top_n: int = 12) -> go.Figure:
    sub = surface_forms[surface_forms["Input Root"] == root].copy()
    if sub.empty:
        return _layout(go.Figure(), f"Surface forms  ·  {root}")
    # Collapse the long tail of tiny forms into one "Other" slice so the donut
    # is not surrounded by a spider of clipped leader-line labels.
    sub = sub.sort_values("Occurrences", ascending=False)
    if len(sub) > top_n:
        head = sub.iloc[:top_n]
        tail_occ = int(sub.iloc[top_n:]["Occurrences"].sum())
        tail_cnt = len(sub) - top_n
        import pandas as _pd
        sub = _pd.concat([head, _pd.DataFrame([{
            "Input Root": root,
            "Surface Form (col 5)": f"+{tail_cnt} more",
            "Occurrences": tail_occ}])], ignore_index=True)
    fig = px.pie(sub, names="Surface Form (col 5)", values="Occurrences",
                 color_discrete_sequence=px.colors.qualitative.Bold, hole=0.42)
    # Keep labels INSIDE the wedges; hide any that cannot fit (still in hover),
    # which removes the outside leader lines that were being cut off.
    fig.update_traces(textinfo="label+percent", textposition="inside",
                      textfont=dict(size=13, color="#FFFFFF", family="Arial Black"),
                      insidetextorientation="horizontal",
                      hovertemplate="%{label}<br>%{value} occ · %{percent}<extra></extra>")
    fig.add_annotation(text=f"<b>{root}</b>", x=0.5, y=0.5,
                       showarrow=False,
                       font=dict(size=26, color="#E63946", family="Arial Black"))
    fig.update_layout(showlegend=False,
                      uniformtext=dict(minsize=10, mode="hide"))
    fig = _layout(fig, f"Surface forms  ·  {root}", h=420)
    # Apply roomy margins AFTER _layout (which would otherwise reset them small).
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=24))
    return fig


def chart_position_histogram(position_df: pd.DataFrame, root: str) -> go.Figure:
    sub = position_df[position_df["Input Root"] == root]
    if sub.empty:
        return _layout(go.Figure(), "Position in ayah")
    fig = px.histogram(sub, x="Position in ayah (0..1)", nbins=20,
                       color_discrete_sequence=[PAL["accent"]])
    fig.update_layout(xaxis_title="Relative position (start → end)",
                      yaxis_title="Occurrences")
    return _layout(fig, f"Where {root} sits in its ayahs", h=320)


def chart_ayah_length_hist(position_df: pd.DataFrame, root: str) -> go.Figure:
    sub = position_df[position_df["Input Root"] == root]
    if sub.empty:
        return _layout(go.Figure(), "Ayah-length distribution")
    fig = px.histogram(sub, x="Ayah length (roots)", nbins=25,
                       color_discrete_sequence=[PAL["teal"]])
    return _layout(fig, f"Lengths of ayahs containing {root}", h=320)


def chart_partner_motifs(pmotifs: pd.DataFrame, root: str, top: int = 15) -> go.Figure:
    sub = pmotifs[pmotifs["Input Root"] == root].head(top)
    if sub.empty:
        return _layout(go.Figure(), "Top partners")
    sub = sub.iloc[::-1]
    fig = px.bar(sub, x="Ayahs Together", y="Partner Root", orientation="h",
                 color="Affinity", color_continuous_scale=CONTINUOUS,
                 hover_data=["Total Ayahs of Input", "Affinity"])
    return _layout(fig, f"Top co-occurring partners of {root}", h=420)


# ---------------------------------------------------------------------------
# Network
# ---------------------------------------------------------------------------
def chart_network(g: nx.Graph, communities: dict[str, int]) -> go.Figure:
    if g.number_of_nodes() == 0:
        return _layout(go.Figure(), "Network")
    pos = nx.spring_layout(g, seed=42, k=1.6 / max(g.number_of_nodes(), 1) ** 0.5)

    # Edges
    edge_x, edge_y, edge_text = [], [], []
    for u, v, data in g.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(f"{u} — {v}: {data['weight']} ayahs")
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y, line=dict(width=1, color="#9CA3AF"),
        hoverinfo="none", mode="lines", showlegend=False,
    )

    # Nodes
    palette = px.colors.qualitative.Vivid
    node_x, node_y, node_text, node_color, node_size, node_label, node_line = [], [], [], [], [], [], []
    degrees = dict(g.degree(weight="weight"))
    max_deg = max(degrees.values()) if degrees else 1
    for n in g.nodes():
        x, y = pos[n]
        node_x.append(x); node_y.append(y)
        is_input = g.nodes[n].get("is_input")
        comm = communities.get(n, 0)
        c = PAL["input"] if is_input else palette[comm % len(palette)]
        node_color.append(c)
        size = 22 + 30 * (degrees.get(n, 0) / max_deg)
        if is_input:
            size += 10
        node_size.append(size)
        node_label.append(n)
        node_line.append(3 if is_input else 1)
        node_text.append(
            f"<b>{n}</b><br>"
            f"Type: {'Input root' if is_input else 'Co-occurring'}<br>"
            f"Community: {comm}<br>"
            f"Weighted degree: {degrees.get(n, 0)}<br>"
            f"Degree (edges): {g.degree(n)}"
        )
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_label, textposition="middle center",
        textfont=dict(size=12, color="white", family="Arial Black"),
        hovertext=node_text, hoverinfo="text",
        marker=dict(size=node_size, color=node_color,
                    line=dict(width=node_line, color="#1B263B")),
        showlegend=False,
    )
    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_layout(plot_bgcolor="#F8FAFC", dragmode="pan", uirevision="keep")
    return _layout(fig,
                   "Co-occurrence network",
                   h=620)


def chart_centrality(centrality: pd.DataFrame, metric: str = "Weighted Degree", top: int = 20) -> go.Figure:
    if centrality.empty:
        return _layout(go.Figure(), "Centrality")
    sub = centrality.head(top).iloc[::-1]
    fig = px.bar(sub, x=metric, y="Root", orientation="h",
                 color="Is Input",
                 color_discrete_map={True: PAL["input"], False: PAL["partner"]})
    return _layout(fig, f"{metric} — top {top}", h=480)


def chart_communities_treemap(g: nx.Graph, communities: dict[str, int]) -> go.Figure:
    if not communities:
        return _layout(go.Figure(), "Communities")
    deg = dict(g.degree(weight="weight"))
    rows = []
    for n, c in communities.items():
        rows.append({"Community": f"Community {c}", "Root": n,
                     "Weighted Degree": deg.get(n, 1) + 1,
                     "Is Input": g.nodes[n].get("is_input", False)})
    df = pd.DataFrame(rows)
    fig = px.treemap(df, path=["Community", "Root"], values="Weighted Degree",
                     color="Weighted Degree", color_continuous_scale=CONTINUOUS,
                     hover_data=["Is Input"])
    return _layout(fig, "Community treemap", h=500)


# ---------------------------------------------------------------------------
# Motif analysis
# ---------------------------------------------------------------------------
def chart_motif_summary(triad: dict) -> go.Figure:
    keys = ["nodes", "edges", "triangles (closed triads)", "open triads (paths of length 2)"]
    values = [triad.get(k, 0) for k in keys]
    fig = go.Figure(data=[go.Bar(
        x=keys, y=values,
        marker_color=[PAL["partner"], PAL["accent"], PAL["input"], PAL["teal"]],
        text=values, textposition="outside",
    )])
    fig.update_layout(yaxis_title="Count")
    return _layout(fig, f"Motif summary (graph density = {triad.get('density', 0)})", h=350)


def chart_triangle_table_bar(triangles: pd.DataFrame, top: int = 20) -> go.Figure:
    if triangles.empty:
        return _layout(go.Figure(), "Triangles")
    sub = triangles.head(top).copy()
    sub["Triad"] = sub.apply(lambda r: f"{r['Root A']} — {r['Root B']} — {r['Root C']}", axis=1)
    sub = sub.iloc[::-1]
    fig = px.bar(sub, x="Sum Weight", y="Triad", orientation="h",
                 color="Inputs in Triad",
                 color_continuous_scale="Sunset")
    return _layout(fig, f"Top {top} triangles by combined edge weight", h=520)


# ---------------------------------------------------------------------------
# Compare — REPLACED heatmaps with clearer bar visuals
# ---------------------------------------------------------------------------
def chart_surah_heatmap(heatmap: pd.DataFrame, top_n: int = 12) -> go.Figure:
    """Small-multiples — one mini horizontal-bar chart per input root, showing
    its top N surahs by ayah hits. Replaces the previous hard-to-read heatmap.

    `heatmap` shape: rows = input roots, columns = surah numbers, values = hits.
    """
    if heatmap.empty:
        return _layout(go.Figure(), "Surah distribution per root")

    # Long-form, drop zeros
    rows = []
    for root, surah_row in heatmap.iterrows():
        for surah, hits in surah_row.items():
            try:
                h = int(hits)
            except Exception:
                continue
            if h > 0:
                rows.append({"Input Root": root,
                             "Surah": f"S{int(surah):03d}",
                             "Surah #": int(surah),
                             "Hits": h})
    if not rows:
        return _layout(go.Figure(), "Surah distribution per root")

    long = pd.DataFrame(rows)
    # Top-N surahs per root, sorted ascending so the largest sits at the top of
    # the horizontal bars after the natural y-axis flip.
    keep = []
    for root, grp in long.groupby("Input Root"):
        top = grp.nlargest(top_n, "Hits").sort_values("Hits", ascending=True)
        keep.append(top)
    long = pd.concat(keep, ignore_index=True)

    n_roots = long["Input Root"].nunique()
    n_cols = min(3, n_roots)
    n_rows_grid = (n_roots + n_cols - 1) // n_cols
    fig = px.bar(long, x="Hits", y="Surah", orientation="h",
                 facet_col="Input Root", facet_col_wrap=n_cols,
                 color="Hits", color_continuous_scale=CONTINUOUS,
                 hover_data=["Surah #"], text="Hits")
    fig.update_yaxes(matches=None, showticklabels=True, categoryorder="array",
                     categoryarray=long["Surah"].tolist())
    fig.update_xaxes(matches=None)
    fig.update_traces(textposition="outside")
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    return _layout(fig,
                   f"Top {top_n} surahs per root",
                   h=max(360, 240 * n_rows_grid))


def chart_overlap_heatmap(overlap: pd.DataFrame) -> go.Figure:
    """Sorted horizontal bar chart of root-pairs by shared ayahs.
    Replaces the previous overlap heatmap with a ranked, readable view."""
    if overlap.empty:
        return _layout(go.Figure(), "Pair overlap")
    pairs = []
    roots = list(overlap.index)
    for i in range(len(roots)):
        for j in range(i + 1, len(roots)):
            a, b = roots[i], roots[j]
            try:
                v = float(overlap.iloc[i, j])
            except Exception:
                continue
            if pd.notna(v) and v > 0:
                pairs.append({"Pair": f"{a}  ↔  {b}", "Shared ayahs": int(v)})
    if not pairs:
        return _layout(go.Figure(), "Pair overlap")
    df = pd.DataFrame(pairs).sort_values("Shared ayahs", ascending=True)
    fig = px.bar(df, x="Shared ayahs", y="Pair", orientation="h",
                 color="Shared ayahs", color_continuous_scale="Magma",
                 text="Shared ayahs")
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, coloraxis_showscale=False,
                      yaxis_title="", xaxis_title="Shared ayahs")
    return _layout(fig,
                   "Pair overlap",
                   h=max(320, 70 + 38 * len(df)))


# ---------------------------------------------------------------------------
# Morphology
# ---------------------------------------------------------------------------
def chart_morphology(morph: pd.DataFrame) -> go.Figure:
    if morph.empty:
        return _layout(go.Figure(), "Morphology")
    fig = px.bar(morph, x="Particle", y="Count", color="Position",
                 facet_col="Input Root", facet_col_wrap=3,
                 color_discrete_map={"prefix": PAL["accent"], "suffix": PAL["teal"]},
                 hover_data=["Meaning"])
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return _layout(fig, "Particles per root", h=460)


def chart_morphology_per_root(morph: pd.DataFrame, root: str) -> go.Figure:
    sub = morph[morph["Input Root"] == root]
    if sub.empty:
        return _layout(go.Figure(), "Morphology")
    fig = px.bar(sub, x="Particle", y="Count", color="Position",
                 color_discrete_map={"prefix": PAL["accent"], "suffix": PAL["teal"]},
                 hover_data=["Meaning"], barmode="group")
    return _layout(fig, f"Attached particles on {root}", h=380)



# ---------------------------------------------------------------------------
# Visual motif gallery — see the actual shape of each motif (not just text)
# ---------------------------------------------------------------------------
def _polygon_positions(n):
    """Vertex positions for a motif:  n=2 → horizontal dumbbell,  n>=3 → unit polygon."""
    import math
    if n == 2:
        # Horizontal layout reads as "edge" rather than a vertical line
        return [(-0.7, 0.0), (0.7, 0.0)]
    return [(math.sin(2 * math.pi * i / n), math.cos(2 * math.pi * i / n))
            for i in range(n)]


def count_motifs(g, size, limit=10000):
    """Efficient count of cliques of exact size, using enumerate_all_cliques's
    non-decreasing-size guarantee for early exit. Returns int (capped at limit)."""
    if g is None or g.number_of_nodes() < size:
        return 0
    if size == 2:
        return g.number_of_edges()
    n = 0
    for c in nx.enumerate_all_cliques(g):
        if len(c) > size:
            break
        if len(c) == size:
            n += 1
            if n >= limit:
                return n
    return n


def chart_motif_gallery(g, motif_size=3, top_n=6, input_roots=None):
    """Grid of mini node-edge diagrams for the top closed motifs of a given size.

    motif_size = 3 (triads / triangles), 4 (quads / 4-cliques), 5 (pentads), …
    A motif is a CLOSED k-clique: every pair of its k nodes shares an edge.
    Top-ranked by total combined edge weight inside the motif.
    """
    from itertools import combinations
    from plotly.subplots import make_subplots

    if g is None or g.number_of_nodes() < motif_size:
        fig = go.Figure()
        fig.add_annotation(text=f"(graph too small for {motif_size}-node motifs)",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=14))
        return _layout(fig, f"{motif_size}-root motifs")

    # Enumerate cliques of exactly this size
    cliques = [c for c in nx.enumerate_all_cliques(g) if len(c) == motif_size]
    if not cliques:
        fig = go.Figure()
        fig.add_annotation(text=f"No closed {motif_size}-node cliques in this network.",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=14))
        return _layout(fig, f"{motif_size}-root motifs")

    def tot_w(clique):
        return sum(g[u][v]["weight"] for u, v in combinations(clique, 2))

    cliques.sort(key=tot_w, reverse=True)
    cliques = cliques[:top_n]

    input_set = set(input_roots or [])
    n = len(cliques)
    n_cols = min(3, n)
    n_rows = (n + n_cols - 1) // n_cols
    titles = [f"Σ weight = {int(tot_w(c))}   (inputs: "
              f"{sum(1 for r in c if r in input_set)}/{motif_size})"
              for c in cliques]
    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=titles,
                        horizontal_spacing=0.04, vertical_spacing=0.16)

    positions = _polygon_positions(motif_size)
    max_w = max(tot_w(c) for c in cliques) or 1

    for idx, clique in enumerate(cliques):
        r = idx // n_cols + 1
        c = idx % n_cols + 1
        pos = {node: positions[i] for i, node in enumerate(clique)}

        # Edges first
        for u, v in combinations(clique, 2):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            w = g[u][v]["weight"]
            line_w = 1.5 + 4 * (w / max(1, max_w))
            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1], mode="lines",
                line=dict(width=line_w, color="#9CA3AF"),
                hoverinfo="skip", showlegend=False,
            ), row=r, col=c)
            # Weight label at midpoint
            fig.add_trace(go.Scatter(
                x=[(x0 + x1) / 2], y=[(y0 + y1) / 2],
                mode="text", text=[f"<b>{int(w)}</b>"],
                textfont=dict(size=13, color="#0B1320"),
                hoverinfo="skip", showlegend=False,
            ), row=r, col=c)

        # Nodes
        node_x = [pos[nd][0] for nd in clique]
        node_y = [pos[nd][1] for nd in clique]
        node_colors = [PAL["input"] if nd in input_set else PAL["partner"]
                       for nd in clique]
        hovertexts = [f"<b>{nd}</b><br>" + ("Input root" if nd in input_set
                                            else "Co-occurring root")
                      for nd in clique]
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y, mode="markers+text",
            marker=dict(size=46, color=node_colors,
                        line=dict(width=2, color="#1B263B")),
            text=list(clique), textposition="middle center",
            textfont=dict(size=13, color="white", family="Arial Black"),
            hovertext=hovertexts, hoverinfo="text",
            showlegend=False,
        ), row=r, col=c)

        fig.update_xaxes(visible=False, range=[-1.55, 1.55],
                         row=r, col=c)
        fig.update_yaxes(visible=False, range=[-1.55, 1.55],
                         row=r, col=c, scaleanchor=f"x{idx+1}" if idx > 0 else None)

    label = {3: "triads (triangles)", 4: "quads (4-cliques)",
             5: "pentads (5-cliques)"}.get(motif_size, f"{motif_size}-cliques")
    fig.update_layout(
        title=dict(text=f"<b>Top {n} {label} — red = input root, navy = partner</b>",
                   x=0.5, xanchor="center", font=dict(size=15)),
        height=max(300, 260 * n_rows),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
        margin=dict(l=20, r=20, t=70, b=20),
        font=dict(family="Arial, 'Segoe UI', sans-serif", size=12, color="#1B263B"),
    )
    return fig



# ---------------------------------------------------------------------------
# Community subnetworks — visualize each community as its own mini graph
# ---------------------------------------------------------------------------
def chart_community_subnetworks(g, communities, top_n=12):
    """Grid of mini node-edge diagrams — one per community.

    Replaces the old treemap with an actually-informative view: each tile
    shows the members of a community and the edges between them, so the
    user can see at a glance "who hangs together".

    `communities` is a dict {node: community_id}, as produced by
    `analysis.detect_communities(g)`.
    """
    import math
    from collections import defaultdict
    from plotly.subplots import make_subplots

    if g is None or g.number_of_nodes() == 0 or not communities:
        fig = go.Figure()
        fig.add_annotation(text="(no communities detected)",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=14))
        return _layout(fig, "Communities")

    # Group nodes by community
    by_comm = defaultdict(list)
    for node, cid in communities.items():
        by_comm[cid].append(node)

    # Sort communities by size descending (so biggest is top-left)
    comms = sorted(by_comm.items(),
                   key=lambda kv: (-len(kv[1]), kv[0]))[:top_n]
    if not comms:
        return _layout(go.Figure(), "Communities")

    n = len(comms)
    n_cols = min(3, n)
    n_rows = (n + n_cols - 1) // n_cols

    # Titles: include input-root count + total weight inside the community
    titles = []
    for cid, members in comms:
        sub = g.subgraph(members)
        intra_w = int(sum(d["weight"] for _, _, d in sub.edges(data=True)))
        n_inputs = sum(1 for m in members
                       if g.nodes[m].get("is_input"))
        titles.append(f"Community {cid} · {len(members)} roots "
                      f"({n_inputs} input) · Σw={intra_w}")

    fig = make_subplots(rows=n_rows, cols=n_cols, subplot_titles=titles,
                        horizontal_spacing=0.04, vertical_spacing=0.16)

    # Compute max edge weight across all selected communities for thickness
    # scaling — keeps proportions comparable across tiles.
    all_weights = []
    for cid, members in comms:
        sub = g.subgraph(members)
        all_weights.extend(d["weight"] for _, _, d in sub.edges(data=True))
    max_w = max(all_weights) if all_weights else 1

    for idx, (cid, members) in enumerate(comms):
        r = idx // n_cols + 1
        c = idx % n_cols + 1
        sub = g.subgraph(members).copy()
        n_nodes = sub.number_of_nodes()

        # Layout
        if n_nodes == 0:
            continue
        elif n_nodes == 1:
            only = next(iter(sub.nodes()))
            pos = {only: (0.0, 0.0)}
        elif n_nodes == 2:
            a, b = list(sub.nodes())
            pos = {a: (-0.7, 0.0), b: (0.7, 0.0)}
        else:
            try:
                k_layout = 2.0 / math.sqrt(n_nodes)
                pos = nx.spring_layout(sub, seed=42, k=k_layout, iterations=80)
            except Exception:
                # Fallback: arrange on a polygon
                pos = {nd: (math.sin(2*math.pi*i/n_nodes),
                            math.cos(2*math.pi*i/n_nodes))
                       for i, nd in enumerate(sub.nodes())}

        # Normalize positions to [-1, 1]
        if pos:
            xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
            x_range = max(xs) - min(xs) if max(xs) != min(xs) else 1
            y_range = max(ys) - min(ys) if max(ys) != min(ys) else 1
            scale = 1.0 / max(x_range, y_range, 0.1) * 1.6
            cx = (max(xs) + min(xs)) / 2
            cy = (max(ys) + min(ys)) / 2
            pos = {nd: ((p[0] - cx) * scale, (p[1] - cy) * scale)
                   for nd, p in pos.items()}

        # Edges first (so they appear behind nodes)
        for u, v, data in sub.edges(data=True):
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            w = data.get("weight", 1)
            line_w = 1.0 + 4.0 * (w / max(1, max_w))
            fig.add_trace(go.Scatter(
                x=[x0, x1], y=[y0, y1], mode="lines",
                line=dict(width=line_w, color="#9CA3AF"),
                hoverinfo="skip", showlegend=False,
            ), row=r, col=c)
            # Weight label at midpoint (only if there are not too many edges)
            if sub.number_of_edges() <= 10:
                fig.add_trace(go.Scatter(
                    x=[(x0 + x1) / 2], y=[(y0 + y1) / 2],
                    mode="text", text=[f"<b>{int(w)}</b>"],
                    textfont=dict(size=10, color="#1B263B"),
                    hoverinfo="skip", showlegend=False,
                ), row=r, col=c)

        # Nodes
        node_x = [pos[nd][0] for nd in sub.nodes()]
        node_y = [pos[nd][1] for nd in sub.nodes()]
        node_colors = [PAL["input"] if sub.nodes[nd].get("is_input")
                       else PAL["partner"] for nd in sub.nodes()]
        node_sizes = []
        degrees = dict(sub.degree(weight="weight"))
        max_deg = max(degrees.values()) if degrees else 1
        for nd in sub.nodes():
            size = 28 + 22 * (degrees.get(nd, 0) / max(1, max_deg))
            if sub.nodes[nd].get("is_input"):
                size += 6
            node_sizes.append(size)
        hovertexts = [
            f"<b>{nd}</b><br>"
            f"Type: {'Input root' if sub.nodes[nd].get('is_input') else 'Co-occurring'}"
            f"<br>Weighted deg in this community: {int(degrees.get(nd, 0))}"
            for nd in sub.nodes()
        ]
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y, mode="markers+text",
            marker=dict(size=node_sizes, color=node_colors,
                        line=dict(width=2, color="#1B263B")),
            text=list(sub.nodes()), textposition="middle center",
            textfont=dict(size=11, color="white", family="Arial Black"),
            hovertext=hovertexts, hoverinfo="text",
            showlegend=False,
        ), row=r, col=c)

        fig.update_xaxes(visible=False, range=[-1.6, 1.6], row=r, col=c)
        fig.update_yaxes(visible=False, range=[-1.6, 1.6], row=r, col=c)

    fig.update_layout(
        title=dict(text="<b>Communities — each tile shows who hangs together "
                        "(red = input root)</b>",
                   x=0.5, xanchor="center", font=dict(size=15)),
        height=max(320, 280 * n_rows),
        paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
        margin=dict(l=20, r=20, t=70, b=20),
        font=dict(family="Arial, 'Segoe UI', sans-serif", size=12, color="#1B263B"),
    )
    return fig



# ---------------------------------------------------------------------------
# Pair overlap — multi-granularity (ayah + surah)
# ---------------------------------------------------------------------------
def chart_pair_overlap_grouped(overlap_ayah, overlap_surah, input_roots):
    """Grouped horizontal bars per pair of input roots, showing BOTH
    ayah-level overlap (rare) and surah-level overlap (usually populated).

    Each input is a square DataFrame with input roots as index/columns and the
    intersection count as the cell value.  Pairs are listed top-to-bottom in
    order of surah-overlap (descending) so the most thematically-related pairs
    sit at the top regardless of whether they share any single verse.
    """
    if (overlap_ayah is None or overlap_surah is None or
            overlap_ayah.empty or overlap_surah.empty or
            len(input_roots) < 2):
        fig = go.Figure()
        fig.add_annotation(text="(need at least 2 input roots to compare pairs)",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=14))
        return _layout(fig, "Pair overlap")

    rows = []
    for i in range(len(input_roots)):
        for j in range(i + 1, len(input_roots)):
            a, b = input_roots[i], input_roots[j]
            try:
                ay = int(overlap_ayah.loc[a, b])
            except Exception:
                ay = 0
            try:
                su = int(overlap_surah.loc[a, b])
            except Exception:
                su = 0
            rows.append({"Pair": f"{a}  ↔  {b}", "Ayahs shared": ay,
                         "Surahs shared": su})
    if not rows:
        return _layout(go.Figure(), "Pair overlap")

    df = pd.DataFrame(rows).sort_values(
        ["Surahs shared", "Ayahs shared"], ascending=[True, True])

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["Surahs shared"], y=df["Pair"], orientation="h",
        name="Surahs shared (both roots appear)", marker_color=PAL["teal"],
        text=df["Surahs shared"], textposition="outside",
        hovertemplate="<b>%{y}</b><br>Surahs shared: %{x}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=df["Ayahs shared"], y=df["Pair"], orientation="h",
        name="Ayahs shared (same verse)", marker_color=PAL["input"],
        text=df["Ayahs shared"], textposition="outside",
        hovertemplate="<b>%{y}</b><br>Ayahs shared: %{x}<extra></extra>",
    ))
    fig.update_layout(
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.04, x=0.5,
                    xanchor="center"),
        xaxis_title="Count",
        yaxis_title="",
        height=max(320, 90 + 56 * len(df)),
    )
    return _layout(fig,
                   "Pair overlap — surah vs ayah")



# ---------------------------------------------------------------------------
# ENRICHED NETWORK VIEWS — positional, spatial, rhythm, lead-lag, fingerprints
# ---------------------------------------------------------------------------

def chart_network_positional(g, communities, node_attrs, edge_attrs):
    """Enriched topology graph where node POSITION carries information:
    X = Gravitational Center (where in the mushaf the root lives, 1..6236)
    Y = Burstiness (Fano factor; high = clustered, low = evenly spread)
    Size = total occurrences   ·   Color = community
    Edge width = co-occurrence count   ·   Edge color = mean token-distance
    (darker = the two roots tend to sit close together inside ayahs).
    """
    if g is None or g.number_of_nodes() == 0:
        return _layout(go.Figure(), "Enriched topology")

    # Lookup tables from node_attrs / edge_attrs
    na = {r["Root"]: r for _, r in node_attrs.iterrows()} if node_attrs is not None and not node_attrs.empty else {}
    ea = {(r["Root A"], r["Root B"]): r for _, r in edge_attrs.iterrows()} if edge_attrs is not None and not edge_attrs.empty else {}

    # Fallback for nodes missing in node_attrs (partner roots not in input set)
    # We need positions for ALL nodes in the graph, including discovered partners.
    # For nodes without a precomputed grav/burst, leave at (0,0) and they'll cluster — but
    # better: skip those edges/nodes if data missing. We'll show input-root nodes only with
    # meaningful coords, and route others through a fallback spring layout.
    spring_pos = nx.spring_layout(g, seed=42, k=1.5 / max(g.number_of_nodes(), 1) ** 0.5)
    coords = {}
    # Find ranges for normalising spring fallback against grav/burst space
    grav_vals = [na[n]["Gravitational Center"] for n in g.nodes() if n in na]
    burst_vals = [na[n]["Burstiness (Fano)"] for n in g.nodes() if n in na]
    g_lo, g_hi = (min(grav_vals), max(grav_vals)) if grav_vals else (0, 6236)
    b_lo, b_hi = (min(burst_vals), max(burst_vals)) if burst_vals else (0, 1)
    if g_hi == g_lo: g_hi = g_lo + 1
    if b_hi == b_lo: b_hi = b_lo + 1
    for n in g.nodes():
        if n in na:
            coords[n] = (na[n]["Gravitational Center"], na[n]["Burstiness (Fano)"])
        else:
            # map spring xy [-1,1] into the input-root grav/burst range
            sx, sy = spring_pos[n]
            coords[n] = (g_lo + (sx + 1) / 2 * (g_hi - g_lo),
                         b_lo + (sy + 1) / 2 * (b_hi - b_lo))

    # ---- Edges ----
    # Color by mean token-distance: lower = darker (closer = tighter pairing)
    td_vals = [ea[(u, v)]["Mean Token-Distance"] for u, v in g.edges()
               if (u, v) in ea] or [0]
    td_max = max(td_vals) if td_vals else 1

    edge_traces = []
    weights = [d.get("weight", 1) for _, _, d in g.edges(data=True)]
    w_max = max(weights) if weights else 1
    for u, v, d in g.edges(data=True):
        x0, y0 = coords[u]; x1, y1 = coords[v]
        w = d.get("weight", 1)
        attrs = ea.get((u, v))
        if attrs is None:
            attrs = ea.get((v, u))
        td = attrs["Mean Token-Distance"] if attrs is not None else 0
        ll = attrs["Lead-Lag (A->B)"] if attrs is not None else 0
        # Color: closer = darker red, farther = lighter gray
        intensity = 1 - min(td / max(td_max, 1), 1)  # 0..1, 1 = closest
        rgb = f"rgba({int(180 - 180 * intensity)},{int(180 - 100 * intensity)},{int(220 - 200 * intensity)},0.7)"
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=0.6 + 4 * (w / w_max), color=rgb),
            hoverinfo="text",
            hovertext=(f"<b>{u} ↔ {v}</b><br>"
                       f"Co-occurring ayahs: {w}<br>"
                       f"Mean token-distance: {td:.2f}<br>"
                       f"Lead-Lag: {ll:+.2f} (positive = A leads)<br>"
                       f"Joint surahs: {attrs['Joint Surahs'] if attrs is not None else '—'}"),
            mode="lines", showlegend=False,
        ))

    # ---- Nodes ----
    palette = px.colors.qualitative.Vivid
    node_x, node_y, node_text, node_color, node_size, node_label, node_line = [], [], [], [], [], [], []
    for n in g.nodes():
        x, y = coords[n]
        node_x.append(x); node_y.append(y)
        is_input = g.nodes[n].get("is_input")
        comm = communities.get(n, 0)
        node_color.append(PAL["input"] if is_input else palette[comm % len(palette)])
        info = na.get(n)
        size = 22 + 28 * ((info["Total"] / max(node_attrs["Total"].max(), 1))
                          if info is not None and node_attrs is not None and not node_attrs.empty else 0.3)
        if is_input: size += 8
        node_size.append(size)
        node_label.append(n)
        node_line.append(3 if is_input else 1)
        if info is not None:
            node_text.append(
                f"<b>{n}</b>{' (input)' if is_input else ''}<br>"
                f"Community: {comm}<br>"
                f"Total occurrences: {info['Total']}<br>"
                f"Surahs covered: {info['Surahs Covered']}<br>"
                f"Gravitational center: ayah {info['Gravitational Center']:.0f} of {len(node_attrs) and 6236}<br>"
                f"Spread (entropy): {info['Spread (Entropy)']}<br>"
                f"Burstiness (Fano): {info['Burstiness (Fano)']}<br>"
                f"Mean pos-in-ayah: {info['Mean Pos-in-Ayah']}<br>"
                f"Mean pos-in-surah: {info['Mean Pos-in-Surah']}<br>"
                f"Peak surah: {info['Peak Surah']}"
            )
        else:
            node_text.append(f"<b>{n}</b><br>partner root (no input metrics)")

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_label, textposition="middle center",
        textfont=dict(size=12, color="white", family="Arial Black"),
        hovertext=node_text, hoverinfo="text",
        marker=dict(size=node_size, color=node_color,
                    line=dict(width=node_line, color="#1B263B")),
        showlegend=False,
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_xaxes(title="Gravitational center (mushaf ayah index, 1 → 6236)",
                     showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_yaxes(title="Burstiness (Fano)",
                     showgrid=True, gridcolor="#E5E7EB", zeroline=False)
    fig.update_layout(plot_bgcolor="#F8FAFC")
    return _layout(fig,
                   "Topology (positional)",
                   h=620)


def chart_spatial_scatter(spatial_df):
    """Every occurrence as a dot — x = surah, y = ayah within surah,
    color = root. Reveals where each concept lives across the corpus
    and where roots converge into the same verses."""
    if spatial_df is None or spatial_df.empty:
        return _layout(go.Figure(), "Spatial position")
    fig = px.scatter(spatial_df, x="Surah", y="Ayah", color="Root",
                     hover_data=["Global Idx", "Pos-in-Ayah", "Pos-in-Surah"],
                     color_discrete_sequence=px.colors.qualitative.Vivid,
                     opacity=0.72)
    fig.update_traces(marker=dict(size=8, line=dict(width=0.4, color="#1B263B")))
    fig.update_xaxes(title="Surah (1 → 114)", dtick=10,
                     showgrid=True, gridcolor="#E5E7EB")
    fig.update_yaxes(title="Ayah within surah",
                     showgrid=True, gridcolor="#E5E7EB")
    return _layout(fig,
                   "Spatial position",
                   h=520)


def chart_trajectories(trajectories_df):
    """Cumulative count of each root vs global ayah index. Slope = local
    mention rate; steep section = burst; flat = silence."""
    if trajectories_df is None or trajectories_df.empty:
        return _layout(go.Figure(), "Rhythm & growth")
    fig = go.Figure()
    palette = px.colors.qualitative.Vivid
    for i, r in enumerate(trajectories_df["Root"].unique()):
        sub = trajectories_df[trajectories_df["Root"] == r].copy()
        # add (0,0) start point and (6236, last) end point for proper line shape
        gidx = [0] + sub["Global Idx"].tolist() + [6236]
        cum = [0] + sub["Cumulative Count"].tolist() + [sub["Cumulative Count"].max()]
        fig.add_trace(go.Scatter(
            x=gidx, y=cum, mode="lines",
            line=dict(width=2.6, color=palette[i % len(palette)], shape="hv"),
            name=r,
            hovertemplate="<b>%{text}</b><br>Global idx: %{x}<br>Count so far: %{y}<extra></extra>",
            text=[r] * len(gidx),
        ))
    fig.update_xaxes(title="Global ayah index (1 → 6236, mushaf order)",
                     showgrid=True, gridcolor="#E5E7EB")
    fig.update_yaxes(title="Cumulative count of root mentions",
                     showgrid=True, gridcolor="#E5E7EB")
    return _layout(fig,
                   "Growth trajectories",
                   h=460)


def chart_burst_spread(node_attrs):
    """Two side-by-side bars: spread (entropy) and burstiness (Fano).
    Tells the user which inputs are 'pervasive' vs 'concentrated' vs 'bursty'."""
    if node_attrs is None or node_attrs.empty:
        return _layout(go.Figure(), "Spread & burstiness")
    from plotly.subplots import make_subplots
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=("Spread (entropy)",
                                        "Burstiness (Fano factor — higher = clustered)"))
    df = node_attrs.sort_values("Spread (Entropy)", ascending=True)
    fig.add_trace(go.Bar(x=df["Spread (Entropy)"], y=df["Root"], orientation="h",
                         marker_color=PAL["teal"], name="Spread"), row=1, col=1)
    df2 = node_attrs.sort_values("Burstiness (Fano)", ascending=True)
    fig.add_trace(go.Bar(x=df2["Burstiness (Fano)"], y=df2["Root"], orientation="h",
                         marker_color=PAL["accent"], name="Burst"), row=1, col=2)
    fig.update_layout(showlegend=False)
    return _layout(fig, "Spread vs burstiness", h=420)


def chart_lead_lag(ll_matrix):
    """Directed heatmap: row A → col B reads
    'given A appears in an ayah, prob of B appearing within ±2 ayahs'."""
    if ll_matrix is None or ll_matrix.empty:
        return _layout(go.Figure(), "Lead-Lag")
    fig = go.Figure(go.Heatmap(
        z=ll_matrix.values,
        x=list(ll_matrix.columns), y=list(ll_matrix.index),
        colorscale="Plasma",
        colorbar=dict(title="P(B near A)", thickness=12),
        hovertemplate="A = %{y}<br>B = %{x}<br>P(B within ±2 ayahs of A) = %{z:.3f}<extra></extra>",
    ))
    fig.update_xaxes(title="B (downstream root)", side="bottom")
    fig.update_yaxes(title="A (upstream root)", autorange="reversed")
    return _layout(fig,
                   "Lead-lag matrix",
                   h=420)


def chart_fingerprint_radar(fp_df):
    """Overlaid radar charts — each input root is one polygon on six axes:
    Spread, Concentration, Late-in-Ayah, Late-in-Surah, Mushaf Position,
    Abundance. Side-by-side comparison of concept 'fingerprints'."""
    if fp_df is None or fp_df.empty:
        return _layout(go.Figure(), "Concept fingerprints")
    axes = ["Spread", "Concentration", "Late-in-Ayah",
            "Late-in-Surah", "Mushaf Position", "Abundance"]
    fig = go.Figure()
    palette = px.colors.qualitative.Vivid
    for i, (_, r) in enumerate(fp_df.iterrows()):
        vals = [r[a] for a in axes] + [r[axes[0]]]
        fig.add_trace(go.Scatterpolar(
            r=vals, theta=axes + [axes[0]],
            fill="toself", name=r["Root"],
            line=dict(color=palette[i % len(palette)], width=2),
            opacity=0.55,
        ))
    fig.update_polars(
        radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(size=10)),
        angularaxis=dict(tickfont=dict(size=12, color="#1D3557")),
    )
    return _layout(fig,
                   "Fingerprints",
                   h=500)


# ---------------------------------------------------------------------------
# GRAPH-FIRST visualizations for the Network tab — phase networks,
# directed lead-lag, per-root ego-networks, robustness overlay
# ---------------------------------------------------------------------------

def _draw_one_graph(ax_fig, g, communities=None, highlight_input=True,
                    title="", subplot_pos=None, edge_color_overrides=None,
                    node_color_overrides=None):
    """Helper: render one graph onto an existing figure as a subplot.
    subplot_pos is (row, col) for make_subplots; None means standalone."""
    import networkx as nx_
    if g is None or g.number_of_nodes() == 0:
        return
    pos = nx_.spring_layout(g, seed=42,
                            k=1.6 / max(g.number_of_nodes(), 1) ** 0.5)
    edge_x, edge_y, edge_hover = [], [], []
    weights = [d.get("weight", 1) for _, _, d in g.edges(data=True)]
    w_max = max(weights) if weights else 1
    palette = px.colors.qualitative.Vivid
    for u, v, d in g.edges(data=True):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_hover.append(f"{u} — {v}: w={d.get('weight', 1)}")
    color = edge_color_overrides if edge_color_overrides else "#9CA3AF"
    edge_trace = go.Scatter(x=edge_x, y=edge_y,
                            line=dict(width=1.2, color=color),
                            hoverinfo="skip", mode="lines", showlegend=False)
    node_x, node_y, node_text, node_color, node_size, node_label = [], [], [], [], [], []
    for n in g.nodes():
        x, y = pos[n]
        node_x.append(x); node_y.append(y)
        is_input = g.nodes[n].get("is_input", False)
        if node_color_overrides and n in node_color_overrides:
            c = node_color_overrides[n]
        elif is_input and highlight_input:
            c = PAL["input"]
        elif communities and n in communities:
            c = palette[communities[n] % len(palette)]
        else:
            c = PAL["partner"]
        node_color.append(c)
        node_size.append(36 if is_input else 24)
        node_label.append(n)
        node_text.append(f"<b>{n}</b><br>{'input' if is_input else 'partner'}<br>"
                          f"deg={g.degree(n)}")
    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=node_label, textposition="middle center",
        textfont=dict(size=13, color="white", family="Arial Black"),
        hovertext=node_text, hoverinfo="text",
        marker=dict(size=node_size, color=node_color,
                    line=dict(width=2, color="#1B263B")),
        showlegend=False,
    )
    if subplot_pos:
        r, c = subplot_pos
        ax_fig.add_trace(edge_trace, row=r, col=c)
        ax_fig.add_trace(node_trace, row=r, col=c)
        ax_fig.update_xaxes(showgrid=False, zeroline=False, visible=False, row=r, col=c)
        ax_fig.update_yaxes(showgrid=False, zeroline=False, visible=False, row=r, col=c)
    else:
        ax_fig.add_trace(edge_trace)
        ax_fig.add_trace(node_trace)


def chart_phase_networks(g_meccan, g_medinan):
    """Side-by-side: Meccan co-occurrence network vs Medinan co-occurrence
    network. Built from the SAME input roots but filtered to phase-specific
    ayahs. Direct visual comparison shows which partnerships are phase-locked."""
    from plotly.subplots import make_subplots
    if (g_meccan is None or g_meccan.number_of_nodes() == 0) and \
       (g_medinan is None or g_medinan.number_of_nodes() == 0):
        fig = go.Figure()
        fig.add_annotation(text="(no phase data — revelation-order column missing)",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=14))
        return _layout(fig, "Phase networks")
    n_m = g_meccan.number_of_nodes() if g_meccan else 0
    e_m = g_meccan.number_of_edges() if g_meccan else 0
    n_d = g_medinan.number_of_nodes() if g_medinan else 0
    e_d = g_medinan.number_of_edges() if g_medinan else 0
    fig = make_subplots(rows=1, cols=2,
                        subplot_titles=(f"<b>Meccan network</b> · {n_m} nodes · {e_m} edges",
                                        f"<b>Medinan network</b> · {n_d} nodes · {e_d} edges"))
    _draw_one_graph(fig, g_meccan, subplot_pos=(1, 1),
                    edge_color_overrides="#F77F00")
    _draw_one_graph(fig, g_medinan, subplot_pos=(1, 2),
                    edge_color_overrides="#06AED5")
    return _layout(fig,
                   "Meccan vs Medinan",
                   h=540)


def chart_phase_diff_graph(g_meccan, g_medinan, only_meccan, only_medinan, in_both):
    """Single merged graph where every edge is colored by its phase status:
    🟠 only in Meccan · 🔵 only in Medinan · ⚫ in both. Lets you see at a
    glance which co-occurrences are stable across the Quran and which
    appeared only in one phase of revelation."""
    import networkx as nx_
    if (g_meccan is None or g_meccan.number_of_nodes() == 0) and \
       (g_medinan is None or g_medinan.number_of_nodes() == 0):
        return _layout(go.Figure(), "Phase diff")
    # Union graph
    g_union = nx_.Graph()
    for src in (g_meccan, g_medinan):
        if src is None: continue
        for n, d in src.nodes(data=True):
            if n not in g_union: g_union.add_node(n, **d)
    pos = nx_.spring_layout(g_union, seed=42,
                            k=1.6 / max(g_union.number_of_nodes(), 1) ** 0.5)
    palette = px.colors.qualitative.Vivid

    # Three edge groups with distinct colors / dash
    def _edge_trace(edges, color, name, dash=None):
        ex, ey, htxt = [], [], []
        for (u, v, w1, w2) in edges:
            if u not in pos or v not in pos: continue
            x0, y0 = pos[u]; x1, y1 = pos[v]
            ex.extend([x0, x1, None]); ey.extend([y0, y1, None])
        return go.Scatter(x=ex, y=ey,
                          line=dict(width=2.2, color=color,
                                    dash=dash or "solid"),
                          name=name, mode="lines",
                          hoverinfo="skip", showlegend=True)

    fig = go.Figure()
    fig.add_trace(_edge_trace(in_both, "#1D3557", "in both phases"))
    fig.add_trace(_edge_trace(only_meccan, "#F77F00", "only in Meccan", dash="dot"))
    fig.add_trace(_edge_trace(only_medinan, "#06AED5", "only in Medinan", dash="dash"))

    # Nodes
    node_x, node_y, node_label, node_color, node_size = [], [], [], [], []
    for n in g_union.nodes():
        x, y = pos[n]
        node_x.append(x); node_y.append(y); node_label.append(n)
        is_input = g_union.nodes[n].get("is_input", False)
        node_color.append(PAL["input"] if is_input else "#888")
        node_size.append(26 if is_input else 16)
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode="markers+text",
                              text=node_label, textposition="middle center",
                              textfont=dict(size=11, color="white", family="Arial Black"),
                              marker=dict(size=node_size, color=node_color,
                                          line=dict(width=1.5, color="#1B263B")),
                              showlegend=False, hoverinfo="text"))
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_layout(plot_bgcolor="#F8FAFC",
                      legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.85)",
                                  bordercolor="#888", borderwidth=1))
    return _layout(fig,
                   "Phase diff",
                   h=560)


def chart_directed_lead_lag(dg):
    """Render the directed lead-lag graph: arrows go FROM the leading root
    TO the trailing one. Edge weight = conditional probability."""
    import networkx as nx_
    if dg is None or dg.number_of_nodes() == 0:
        return _layout(go.Figure(), "Directed lead-lag")
    pos = nx_.spring_layout(dg.to_undirected(), seed=42,
                            k=2.0 / max(dg.number_of_nodes(), 1) ** 0.5)
    fig = go.Figure()
    # Edges as annotations with arrows
    for u, v, d in dg.edges(data=True):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        w = d.get("weight", 0)
        asym = d.get("asymmetry", 0)
        fig.add_annotation(
            x=x1, y=y1, ax=x0, ay=y0, xref="x", yref="y",
            axref="x", ayref="y", showarrow=True,
            arrowhead=3, arrowwidth=1 + 4 * w, arrowsize=1.2,
            arrowcolor=f"rgba(230, 57, 70, {0.4 + 0.5 * w})",
            standoff=20, startstandoff=20,
            hovertext=f"{u} -> {v}<br>P(B near A) = {w:.3f}<br>asymmetry = {asym:+.3f}",
        )
    # Nodes
    nx, ny, nlabel, ncolor, nsize, nhover = [], [], [], [], [], []
    for n in dg.nodes():
        x, y = pos[n]
        nx.append(x); ny.append(y); nlabel.append(n)
        ncolor.append(PAL["input"])
        nsize.append(40)
        out_strength = sum(d.get("weight", 0) for _, _, d in dg.out_edges(n, data=True))
        in_strength = sum(d.get("weight", 0) for _, _, d in dg.in_edges(n, data=True))
        nhover.append(f"<b>{n}</b><br>out-strength (leads): {out_strength:.2f}<br>"
                       f"in-strength (follows): {in_strength:.2f}")
    fig.add_trace(go.Scatter(x=nx, y=ny, mode="markers+text",
                              text=nlabel, textposition="middle center",
                              textfont=dict(size=13, color="white", family="Arial Black"),
                              hovertext=nhover, hoverinfo="text",
                              marker=dict(size=nsize, color=ncolor,
                                          line=dict(width=2, color="#1B263B")),
                              showlegend=False))
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False,
                     range=[-1.5, 1.5])
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False,
                     range=[-1.5, 1.5])
    fig.update_layout(plot_bgcolor="#F8FAFC")
    return _layout(fig,
                   "Lead-lag (directed)",
                   h=520)


def chart_per_root_ego_gallery(g, input_roots, max_neighbors=8):
    """Grid of ego-networks: each input root rendered as the center of its
    own mini-network with its top partners and the edges among them."""
    import math
    import networkx as nx_
    from plotly.subplots import make_subplots
    valid = [r for r in input_roots if r in g.nodes()]
    if not valid:
        return _layout(go.Figure(), "Per-root ego networks")
    n = len(valid)
    n_cols = min(3, n)
    n_rows = (n + n_cols - 1) // n_cols
    fig = make_subplots(rows=n_rows, cols=n_cols,
                        subplot_titles=[f"<b>{r}</b>" for r in valid])
    for idx, root in enumerate(valid):
        nbrs = sorted(g.neighbors(root),
                      key=lambda nd: g[root][nd].get("weight", 1),
                      reverse=True)[:max_neighbors]
        nodes = {root} | set(nbrs)
        sub = g.subgraph(nodes)
        # Force root to center: custom layout
        ring_pos = {root: (0.0, 0.0)}
        for k, nb in enumerate(nbrs):
            theta = 2 * math.pi * k / max(len(nbrs), 1)
            ring_pos[nb] = (math.cos(theta), math.sin(theta))
        r_row, r_col = idx // n_cols + 1, idx % n_cols + 1
        # Edges
        edge_x, edge_y = [], []
        for u, v in sub.edges():
            x0, y0 = ring_pos[u]; x1, y1 = ring_pos[v]
            edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None])
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines",
                                  line=dict(width=1, color="#9CA3AF"),
                                  showlegend=False, hoverinfo="skip"),
                       row=r_row, col=r_col)
        # Nodes
        nx_x, nx_y, lbls, colors, sizes = [], [], [], [], []
        for nd in sub.nodes():
            x, y = ring_pos[nd]
            nx_x.append(x); nx_y.append(y); lbls.append(nd)
            is_input = (nd == root)
            colors.append(PAL["input"] if is_input else PAL["partner"])
            sizes.append(46 if is_input else 30)
        fig.add_trace(go.Scatter(x=nx_x, y=nx_y, mode="markers+text",
                                  text=lbls, textposition="middle center",
                                  textfont=dict(size=13, color="white",
                                                family="Arial Black"),
                                  marker=dict(size=sizes, color=colors,
                                              line=dict(width=2, color="#1B263B")),
                                  showlegend=False, hoverinfo="text"),
                       row=r_row, col=r_col)
        fig.update_xaxes(showgrid=False, zeroline=False, visible=False,
                         range=[-1.4, 1.4], row=r_row, col=r_col)
        fig.update_yaxes(showgrid=False, zeroline=False, visible=False,
                         range=[-1.4, 1.4], row=r_row, col=r_col)
    return _layout(fig,
                   "Ego networks",
                   h=240 * n_rows)


def chart_robustness_overlay(g, articulation_points, bridge_edges, communities):
    """The main graph, but with articulation points marked (☆) and bridge
    edges drawn thicker/red. Reveals the structural backbone — remove these
    nodes/edges and the network falls apart."""
    import networkx as nx_
    if g is None or g.number_of_nodes() == 0:
        return _layout(go.Figure(), "Robustness")
    pos = nx_.spring_layout(g, seed=42,
                            k=1.6 / max(g.number_of_nodes(), 1) ** 0.5)
    palette = px.colors.qualitative.Vivid
    bridge_set = {tuple(sorted(b)) for b in bridge_edges}
    # Regular edges (gray), bridge edges (red)
    rx, ry, bx, by = [], [], [], []
    for u, v, d in g.edges(data=True):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        if tuple(sorted((u, v))) in bridge_set:
            bx.extend([x0, x1, None]); by.extend([y0, y1, None])
        else:
            rx.extend([x0, x1, None]); ry.extend([y0, y1, None])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rx, y=ry, mode="lines",
                              line=dict(width=1, color="#CBD5E1"),
                              hoverinfo="skip", name="regular edge"))
    fig.add_trace(go.Scatter(x=bx, y=by, mode="lines",
                              line=dict(width=4, color="#E63946"),
                              hoverinfo="skip", name="bridge edge"))
    # Nodes
    ap_set = set(articulation_points)
    nx_x, nx_y, lbls, colors, sizes, hover = [], [], [], [], [], []
    for n in g.nodes():
        x, y = pos[n]
        nx_x.append(x); nx_y.append(y)
        is_input = g.nodes[n].get("is_input", False)
        comm = communities.get(n, 0) if communities else 0
        is_ap = n in ap_set
        c = (PAL["input"] if is_input
             else palette[comm % len(palette)])
        colors.append(c)
        sizes.append(40 if is_ap else (32 if is_input else 22))
        lbls.append(("★ " + n) if is_ap else n)
        hover.append(f"<b>{n}</b><br>"
                      f"{'⚠️ articulation point' if is_ap else 'normal node'}<br>"
                      f"degree {g.degree(n)}")
    fig.add_trace(go.Scatter(x=nx_x, y=nx_y, mode="markers+text",
                              text=lbls, textposition="middle center",
                              textfont=dict(size=13, color="white",
                                            family="Arial Black"),
                              hovertext=hover, hoverinfo="text",
                              marker=dict(size=sizes, color=colors,
                                          line=dict(width=2, color="#1B263B")),
                              showlegend=False))
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_layout(plot_bgcolor="#F8FAFC",
                      legend=dict(x=0.02, y=0.98,
                                  bgcolor="rgba(255,255,255,0.85)",
                                  bordercolor="#888", borderwidth=1))
    return _layout(fig,
                   "Articulation + bridges",
                   h=600)


# ---------------------------------------------------------------------------
# DIVERSE GRAPH VISUALIZATIONS — chord, matrix, arc, k-core, MST,
# dendrogram, multi-stage evolution, Sankey
# ---------------------------------------------------------------------------

def chart_chord_diagram(g, communities=None):
    """Circular/chord layout: every node placed on a circle, every edge an
    arc. Different aesthetic from spring layout — surfaces overall density
    and major hubs more clearly when node count is moderate."""
    import math
    import networkx as nx_
    if g is None or g.number_of_nodes() == 0:
        return _layout(go.Figure(), "Chord diagram")
    nodes = list(g.nodes())
    n = len(nodes)
    pos = {nd: (math.cos(2 * math.pi * i / n - math.pi / 2),
                math.sin(2 * math.pi * i / n - math.pi / 2))
           for i, nd in enumerate(nodes)}
    palette = px.colors.qualitative.Vivid
    weights = [d.get("weight", 1) for _, _, d in g.edges(data=True)]
    w_max = max(weights) if weights else 1
    # Draw edges as Bezier-ish curves toward the center for chord look
    edge_traces = []
    for u, v, d in g.edges(data=True):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        w = d.get("weight", 1)
        # 3 points: start, midpoint-toward-center, end
        mid_x = 0.3 * (x0 + x1); mid_y = 0.3 * (y0 + y1)
        edge_traces.append(go.Scatter(
            x=[x0, mid_x, x1], y=[y0, mid_y, y1],
            mode="lines", line=dict(width=0.5 + 3 * w / w_max,
                                     color=f"rgba(29,53,87,{0.15 + 0.5 * w / w_max})",
                                     shape="spline"),
            hoverinfo="text",
            hovertext=f"{u} ↔ {v}: {w} ayahs",
            showlegend=False))
    # Nodes
    nx_x, nx_y, lbls, colors, sizes = [], [], [], [], []
    degrees = dict(g.degree(weight="weight"))
    max_deg = max(degrees.values()) if degrees else 1
    for nd in nodes:
        x, y = pos[nd]
        # Push label slightly outside the circle
        lx, ly = x * 1.12, y * 1.12
        nx_x.append(x); nx_y.append(y); lbls.append(nd)
        is_input = g.nodes[nd].get("is_input", False)
        comm = communities.get(nd, 0) if communities else 0
        colors.append(PAL["input"] if is_input else palette[comm % len(palette)])
        sizes.append(18 + 22 * degrees.get(nd, 0) / max_deg)
    node_trace = go.Scatter(x=nx_x, y=nx_y, mode="markers",
                            marker=dict(size=sizes, color=colors,
                                        line=dict(width=1.5, color="#1B263B")),
                            text=lbls, hoverinfo="text", showlegend=False)
    # Labels outside the ring
    label_x = [x * 1.18 for x in nx_x]
    label_y = [y * 1.18 for y in nx_y]
    label_trace = go.Scatter(x=label_x, y=label_y, mode="text",
                              text=lbls,
                              textfont=dict(size=14, color="#1B263B",
                                            family="Arial Black"),
                              showlegend=False, hoverinfo="skip")
    fig = go.Figure(data=edge_traces + [node_trace, label_trace])
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False,
                     range=[-1.4, 1.4])
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False,
                     range=[-1.4, 1.4], scaleanchor="x", scaleratio=1)
    fig.update_layout(plot_bgcolor="#F8FAFC")
    return _layout(fig, "Chord",
                   h=560)


def chart_adjacency_matrix(g):
    """Adjacency matrix as a heatmap. Rows and columns are nodes; cell color =
    edge weight. A complementary view to the node-link diagram — easier to
    spot dense blocks and structural holes when there are many edges."""
    import networkx as nx_
    if g is None or g.number_of_nodes() == 0:
        return _layout(go.Figure(), "Adjacency matrix")
    # Order nodes by weighted degree so dense blocks visually align
    degrees = dict(g.degree(weight="weight"))
    nodes = sorted(g.nodes(), key=lambda n: -degrees.get(n, 0))
    n = len(nodes)
    idx = {nd: i for i, nd in enumerate(nodes)}
    z = [[0] * n for _ in range(n)]
    for u, v, d in g.edges(data=True):
        w = d.get("weight", 1)
        z[idx[u]][idx[v]] = w
        z[idx[v]][idx[u]] = w
    fig = go.Figure(go.Heatmap(z=z, x=nodes, y=nodes,
                                colorscale="Plasma",
                                colorbar=dict(title="Ayahs shared", thickness=12),
                                hovertemplate="%{y} ↔ %{x}<br>shared: %{z}<extra></extra>"))
    fig.update_yaxes(autorange="reversed")
    return _layout(fig,
                   "Adjacency matrix",
                   h=540)


def chart_arc_diagram(dg):
    """Arc diagram for the directed lead-lag graph: nodes on a horizontal
    line, edges drawn as arcs above (forward) or below (reverse). Very
    clear way to see asymmetric relationships."""
    import math
    if dg is None or dg.number_of_nodes() == 0:
        return _layout(go.Figure(), "Arc diagram")
    nodes = sorted(dg.nodes(),
                   key=lambda n: -sum(d.get("weight", 0)
                                       for _, _, d in dg.out_edges(n, data=True)))
    n = len(nodes)
    if n < 2:
        return _layout(go.Figure(), "Arc diagram (need ≥2 nodes)")
    x_pos = {nd: i for i, nd in enumerate(nodes)}
    fig = go.Figure()
    palette = px.colors.qualitative.Vivid
    for u, v, d in dg.edges(data=True):
        x0, x1 = x_pos[u], x_pos[v]
        # Forward (u<v) → arc above; reverse (u>v) → arc below
        above = x0 < x1
        mid_x = (x0 + x1) / 2
        radius = abs(x1 - x0) / 2
        # Parametric semicircle
        thetas = [math.pi * t / 30 for t in range(31)]
        arc_x = [mid_x + radius * math.cos(t) for t in thetas]
        arc_y = [(radius * math.sin(t)) * (1 if above else -1) for t in thetas]
        w = d.get("weight", 0)
        fig.add_trace(go.Scatter(
            x=arc_x, y=arc_y, mode="lines",
            line=dict(width=1 + 4 * w, color=PAL["input"] if above else PAL["teal"]),
            hovertext=f"{u} → {v}<br>weight: {w:.3f}",
            hoverinfo="text", showlegend=False))
    # Nodes on the baseline
    fig.add_trace(go.Scatter(
        x=list(x_pos.values()), y=[0] * n, mode="markers+text",
        text=[nd for nd in nodes], textposition="middle center",
        textfont=dict(size=12, color="white", family="Arial Black"),
        marker=dict(size=36, color=PAL["input"],
                    line=dict(width=2, color="#1B263B")),
        showlegend=False, hoverinfo="text"))
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False,
                     range=[-0.5, n - 0.5])
    fig.update_yaxes(showgrid=False, zeroline=True, zerolinecolor="#888",
                     range=[-n / 2 - 1, n / 2 + 1], scaleanchor="x")
    return _layout(fig,
                   "Arc diagram",
                   h=400)


def chart_kcore_layered(g):
    """Concentric rings: nodes positioned by k-core membership.
    Highest-k inner ring = most densely connected; outermost = peripheral.
    Reveals the structural hierarchy."""
    import math
    import networkx as nx_
    if g is None or g.number_of_nodes() == 0:
        return _layout(go.Figure(), "k-core layers")
    cores = nx_.core_number(g)
    if not cores:
        return _layout(go.Figure(), "k-core layers")
    by_k = {}
    for nd, k in cores.items():
        by_k.setdefault(k, []).append(nd)
    k_vals = sorted(by_k.keys(), reverse=True)  # highest k → inner ring
    k_max = max(k_vals) if k_vals else 1
    pos = {}
    for ring_i, k in enumerate(k_vals):
        radius = 0.25 + 0.85 * ring_i / max(len(k_vals) - 1, 1)
        members = by_k[k]
        for j, nd in enumerate(members):
            theta = 2 * math.pi * j / max(len(members), 1)
            pos[nd] = (radius * math.cos(theta), radius * math.sin(theta))

    # Draw concentric ring guides
    fig = go.Figure()
    for ring_i, k in enumerate(k_vals):
        radius = 0.25 + 0.85 * ring_i / max(len(k_vals) - 1, 1)
        ring_x = [radius * math.cos(2 * math.pi * t / 60) for t in range(61)]
        ring_y = [radius * math.sin(2 * math.pi * t / 60) for t in range(61)]
        fig.add_trace(go.Scatter(x=ring_x, y=ring_y, mode="lines",
                                  line=dict(color="#E5E7EB", width=1, dash="dot"),
                                  hoverinfo="skip", showlegend=False))
        # k-label on the ring
        fig.add_annotation(x=0, y=radius, text=f"k={k}",
                            showarrow=False, font=dict(size=11, color="#888"))
    # Edges
    edge_x, edge_y = [], []
    for u, v in g.edges():
        x0, y0 = pos[u]; x1, y1 = pos[v]
        edge_x.extend([x0, x1, None]); edge_y.extend([y0, y1, None])
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines",
                              line=dict(width=0.8, color="#CBD5E1"),
                              hoverinfo="skip", showlegend=False))
    # Nodes colored by k
    palette = px.colors.sequential.Plasma_r
    nx_x, nx_y, lbls, colors, sizes, hover = [], [], [], [], [], []
    for nd in g.nodes():
        x, y = pos[nd]
        k = cores[nd]
        nx_x.append(x); nx_y.append(y); lbls.append(nd)
        intensity = k / max(k_max, 1)
        c = palette[int(intensity * (len(palette) - 1))]
        colors.append(c)
        is_input = g.nodes[nd].get("is_input", False)
        sizes.append(34 if is_input else 24)
        hover.append(f"<b>{nd}</b><br>k-core: {k} of {k_max}<br>degree: {g.degree(nd)}")
    fig.add_trace(go.Scatter(x=nx_x, y=nx_y, mode="markers+text",
                              text=lbls, textposition="middle center",
                              textfont=dict(size=13, color="white", family="Arial Black"),
                              marker=dict(size=sizes, color=colors,
                                          line=dict(width=2, color="#1B263B")),
                              hovertext=hover, hoverinfo="text", showlegend=False))
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False, range=[-1.2, 1.2])
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False,
                     range=[-1.2, 1.2], scaleanchor="x", scaleratio=1)
    return _layout(fig,
                   "k-core layers",
                   h=560)


def chart_mst_backbone(g):
    """Minimum spanning tree of the network. The 'spine' — the smallest set
    of edges that still connects every node. Strips away redundancy and
    reveals the essential structure."""
    import networkx as nx_
    if g is None or g.number_of_nodes() == 0:
        return _layout(go.Figure(), "MST backbone")
    # Use 1/weight so heavier (more co-occurring) edges are preferred
    g_inv = nx_.Graph()
    for u, v, d in g.edges(data=True):
        w = d.get("weight", 1)
        g_inv.add_edge(u, v, weight=1 / max(w, 1))
    try:
        mst = nx_.minimum_spanning_tree(g_inv, weight="weight")
    except Exception:
        return _layout(go.Figure(), "MST backbone (unavailable)")
    # Restore real weights for display
    for u, v in mst.edges():
        mst[u][v]["weight"] = g[u][v]["weight"]
    pos = nx_.spring_layout(mst, seed=42,
                            k=1.8 / max(mst.number_of_nodes(), 1) ** 0.5)
    edge_x, edge_y, hover = [], [], []
    weights = [d.get("weight", 1) for _, _, d in mst.edges(data=True)]
    w_max = max(weights) if weights else 1
    fig = go.Figure()
    for u, v, d in mst.edges(data=True):
        x0, y0 = pos[u]; x1, y1 = pos[v]
        w = d.get("weight", 1)
        fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode="lines",
                                  line=dict(width=1 + 5 * w / w_max,
                                            color="#06A77D"),
                                  hovertext=f"{u} — {v}: {w} ayahs",
                                  hoverinfo="text", showlegend=False))
    nx_x, nx_y, lbls, colors, sizes = [], [], [], [], []
    for nd in mst.nodes():
        x, y = pos[nd]
        nx_x.append(x); nx_y.append(y); lbls.append(nd)
        is_input = g.nodes[nd].get("is_input", False)
        colors.append(PAL["input"] if is_input else PAL["partner"])
        sizes.append(36 if is_input else 24)
    fig.add_trace(go.Scatter(x=nx_x, y=nx_y, mode="markers+text",
                              text=lbls, textposition="middle center",
                              textfont=dict(size=13, color="white",
                                            family="Arial Black"),
                              marker=dict(size=sizes, color=colors,
                                          line=dict(width=2, color="#1B263B")),
                              showlegend=False, hoverinfo="text"))
    fig.update_xaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_layout(plot_bgcolor="#F8FAFC")
    return _layout(fig,
                   f"MST backbone ({mst.number_of_edges()} edges)".format(
                       g.number_of_edges()),
                   h=520)


def chart_community_dendrogram(g, communities):
    """Treemap-style hierarchical view of community membership — each
    community is a parent block whose children are its member roots,
    sized by weighted degree."""
    if g is None or g.number_of_nodes() == 0 or not communities:
        return _layout(go.Figure(), "Community hierarchy")
    deg = dict(g.degree(weight="weight"))
    rows = []
    for n, c in communities.items():
        rows.append({"Community": f"Community {c}", "Root": n,
                     "Weighted Degree": deg.get(n, 1) + 1,
                     "Is Input": g.nodes[n].get("is_input", False)})
    df = pd.DataFrame(rows)
    fig = px.icicle(df, path=["Community", "Root"],
                    values="Weighted Degree",
                    color="Weighted Degree", color_continuous_scale="Plasma",
                    hover_data=["Is Input"])
    fig.update_traces(tiling=dict(orientation="v"))
    return _layout(fig,
                   "Community hierarchy",
                   h=500)


def chart_4stage_evolution(corpus, build_phase_subgraph_fn):
    """Four side-by-side networks for revelation phases:
    Early Meccan (rev 1-30) · Middle Meccan (31-60) · Late Meccan (61-86) ·
    Medinan (87-114). Shows network evolution over the corpus's revelation
    timeline. build_phase_subgraph_fn(lo, hi) -> nx.Graph"""
    from plotly.subplots import make_subplots
    stages = [
        ("Early Meccan", 1, 30),
        ("Middle Meccan", 31, 60),
        ("Late Meccan", 61, 86),
        ("Medinan", 87, 114),
    ]
    graphs = [(name, build_phase_subgraph_fn(lo, hi))
              for (name, lo, hi) in stages]
    titles = [f"<b>{name}</b><br>{(g.number_of_nodes() if g else 0)}n · "
              f"{(g.number_of_edges() if g else 0)}e"
              for (name, g) in graphs]
    fig = make_subplots(rows=1, cols=4, subplot_titles=titles)
    for col_i, (name, gph) in enumerate(graphs, start=1):
        _draw_one_graph(fig, gph, subplot_pos=(1, col_i),
                        edge_color_overrides="#F77F00" if col_i <= 3 else "#06AED5")
    # No figure title — the page already renders a "### 4-stage evolution" header above it; an
    # internal title duplicated that AND overlapped the four subplot titles (Early Meccan …).
    return _layout(fig, "", h=420)


def chart_sankey_phase_flow(g_meccan, g_medinan):
    """Sankey diagram of edge flow between phases: every edge weighted by
    its weight in each phase, showing how partnerships migrate between
    Meccan and Medinan."""
    if not g_meccan or not g_medinan:
        return _layout(go.Figure(), "Phase flow")
    # Build node list: each root appears twice (Meccan side + Medinan side)
    roots = sorted(set(g_meccan.nodes()) | set(g_medinan.nodes()))
    if not roots:
        return _layout(go.Figure(), "Phase flow")
    # Index nodes: 0..n-1 = Meccan, n..2n-1 = Medinan
    n = len(roots)
    labels = [r for r in roots] + [r for r in roots]
    colors = ["#F77F00"] * n + ["#06AED5"] * n
    # Flow: for each pair (u, v) that exists in either, send weight from u-Meccan to v-Medinan
    edges_m = {tuple(sorted((u, v))): d.get("weight", 1)
               for u, v, d in g_meccan.edges(data=True)}
    edges_d = {tuple(sorted((u, v))): d.get("weight", 1)
               for u, v, d in g_medinan.edges(data=True)}
    sources, targets, values, link_colors = [], [], [], []
    idx = {r: i for i, r in enumerate(roots)}
    for pair in set(edges_m) | set(edges_d):
        u, v = pair
        wm = edges_m.get(pair, 0); wd = edges_d.get(pair, 0)
        # Use min(wm, wd) as the persistent flow, plus separate-flows for the deltas
        if wm > 0 and wd > 0:
            shared = min(wm, wd)
            sources.append(idx[u]); targets.append(n + idx[v]); values.append(shared)
            link_colors.append("rgba(29,53,87,0.4)")
            if wm > shared:
                sources.append(idx[u]); targets.append(n + idx[u]); values.append(wm - shared)
                link_colors.append("rgba(247,127,0,0.4)")
        elif wm > 0:
            sources.append(idx[u]); targets.append(n + idx[u]); values.append(wm)
            link_colors.append("rgba(247,127,0,0.5)")
        elif wd > 0:
            sources.append(idx[u]); targets.append(n + idx[v]); values.append(wd)
            link_colors.append("rgba(6,174,213,0.5)")
    fig = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(label=labels, color=colors, pad=18, thickness=22,
                  line=dict(color="black", width=0.5)),
        link=dict(source=sources, target=targets, value=values, color=link_colors),
        textfont=dict(size=14, color="#1B263B", family="Arial"),
    ))
    return _layout(fig,
                   "Phase flow",
                   h=580)


# ---------------------------------------------------------------------------
# Per-Root Profile enhancements (v1.3)
# ---------------------------------------------------------------------------
def chart_surface_partner_lift(df: pd.DataFrame, root: str, top: int = 15) -> go.Figure:
    """Top surface-form collocates of `root`, ranked by lift (bar length = lift,
    colour = shared-ayah support)."""
    sub = df[df["Input Root"] == root].head(top)
    if sub.empty:
        return _layout(go.Figure(), f"Surface-form collocates of {root}")
    sub = sub.iloc[::-1]
    fig = px.bar(sub, x="Lift", y="Partner Surface", orientation="h",
                 color="Ayahs Together", color_continuous_scale=CONTINUOUS,
                 hover_data=["Ayahs Together", "Global Ayahs", "Affinity"])
    fig.update_layout(coloraxis_colorbar=dict(title="Shared<br>ayahs", thickness=12))
    return _layout(fig, f"Top surface-form collocates of {root} (by lift)", h=420)


def chart_density_home_surahs(occurrences: pd.DataFrame, ayahs_per_surah: dict,
                              surah_names: dict, root: str, top: int = 7,
                              min_hits: int = 3, min_size: int = 10) -> go.Figure:
    """Where the root is DENSEST - hits per 1,000 ayahs (size-true). All surahs are
    shown; bars below the support floor (<min_hits or <min_size) are greyed and flagged
    as not statistically reliable."""
    sub = occurrences[occurrences["Input Root"] == root]
    if sub.empty:
        return _layout(go.Figure(), f"Density home surahs - {root}")
    rows = []
    for sid, h in sub.groupby("Surah #").size().items():
        size = int(ayahs_per_surah.get(int(sid), 0))
        if size <= 0:
            continue
        below = (h < min_hits or size < min_size)
        rows.append({"Surah": f"{surah_names.get(int(sid), '')} ({int(sid)})",
                     "Density /1k": round(1000 * h / size, 1),
                     "Hits": int(h), "Ayahs": size, "Surah #": int(sid),
                     "Support": "below floor (unreliable)" if below else "clears floor"})
    if not rows:
        return _layout(go.Figure(), f"Density home surahs - {root}")
    d = pd.DataFrame(rows).nlargest(top, "Density /1k").sort_values("Density /1k")
    n_below = int((d["Support"] == "below floor (unreliable)").sum())
    H = max(360, 26 * len(d) + 150)
    fig = px.bar(d, x="Density /1k", y="Surah", orientation="h",
                 color="Support",
                 color_discrete_map={"clears floor": PAL["good"],
                                     "below floor (unreliable)": "#9AA5B1"},
                 category_orders={"Surah": d["Surah"].tolist()},
                 hover_data=["Hits", "Ayahs", "Surah #"], text="Density /1k")
    fig.update_traces(textposition="outside", width=0.84)
    fig.update_layout(bargap=0.12, height=H,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                  xanchor="right", x=1, title_text=""))
    return _layout(fig, f"Where {root} is densest \u2014 per 1,000 ayahs (all surahs)", h=H)


# ═══════════════════════════════════════════════════════════════════════════
# SPATIAL PATTERNS  (point-pattern + areal/lattice GIS views)
# ═══════════════════════════════════════════════════════════════════════════

def chart_point_pattern(xy, target, order_label, feature="root"):
    """The concept landscape: every occurrence as a point — x = position within
    the ayah, y = global ayah index under the chosen rearrangement."""
    if xy is None or len(xy) == 0:
        return _layout(go.Figure(), f"Point pattern · {target}")
    fig = go.Figure(go.Scattergl(
        x=xy[:, 1], y=xy[:, 0], mode="markers",
        marker=dict(size=5, color=PAL["violet"], opacity=0.55,
                    line=dict(width=0)),
        hovertemplate="y (ayah index)=%{x}<br>x (pos in ayah)=%{y}<extra></extra>",
    ))
    unit = "letter" if feature == "letter" else "root"
    fig.update_xaxes(title=f"Global ayah index — {order_label}",
                     showgrid=True, gridcolor="#EEF2F7")
    fig.update_yaxes(title=f"Position of {unit} within ayah",
                     showgrid=True, gridcolor="#EEF2F7")
    return _layout(fig, f"Point pattern · {target}  ({len(xy)} pts)", h=420)


def chart_ripley_l(kl, target):
    """Ripley's L(r) − r vs the CSR envelope. Above band = clustering at that
    radius; below = regularity. Small r = local scale, large r = global scale."""
    if not kl:
        return _layout(go.Figure(), f"Ripley L(r) · {target}")
    # Centered on the CSR mean so the (large, anisotropy-driven) baseline cancels
    # and the clustering/regularity signal is visible. D(r)=L_obs-L_csr_mean.
    r = kl["radii"]
    m = kl["L_mean"]
    d_obs = kl["L_obs"] - m
    d_hi = kl["L_hi"] - m
    d_lo = kl["L_lo"] - m
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.concatenate([r, r[::-1]]),
                             y=np.concatenate([d_hi, d_lo[::-1]]),
                             fill="toself", fillcolor="rgba(150,160,180,0.25)",
                             line=dict(width=0), name="CSR 95% envelope",
                             hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=r, y=d_obs, mode="lines",
                             line=dict(color=PAL["input"], width=3),
                             name="Observed − CSR",
                             hovertemplate="r=%{x:.0f}<br>L_obs−CSR=%{y:.2f}<extra></extra>"))
    fig.add_hline(y=0, line=dict(color="#1B263B", width=1, dash="dot"))
    fig.update_xaxes(title="Radius r  (small = local · large = global)",
                     showgrid=True, gridcolor="#EEF2F7")
    fig.update_yaxes(title="L(r) − CSR   (above band = clustered · below = regular)",
                     showgrid=True, gridcolor="#EEF2F7")
    return _layout(fig, f"Ripley multiscale · {target}  (K_Max={kl['k_max']})", h=420)


def chart_areal_lattice(values, labels, unit_label, gstar=None, lisa=None,
                        target=""):
    """Choropleth-as-strip over areal units (surah 114 / ayah-band 286 / nuzūl).
    Bars = per-unit counts; colour = Getis-Ord G* z (hot red / cold blue) when
    supplied; LISA HH/LL units flagged with a marker."""
    if values is None or len(values) == 0:
        return _layout(go.Figure(), f"Areal pattern · {target}")
    if gstar is not None and "z" in gstar:
        color = gstar["z"]
        cbar = dict(title="G* z", thickness=12)
        cs = [[0, "#2166AC"], [0.5, "#F7F7F7"], [1, "#B2182B"]]
        zmax = max(2.5, float(np.max(np.abs(color)))) if len(color) else 2.5
        marker = dict(color=color, colorscale=cs, cmin=-zmax, cmax=zmax,
                      colorbar=cbar)
    else:
        marker = dict(color=values, colorscale="Viridis",
                      colorbar=dict(title="Count", thickness=12))
    fig = go.Figure(go.Bar(x=labels, y=values, marker=marker, name="count",
                           showlegend=False,
                           hovertemplate=f"{unit_label} %{{x}}<br>count=%{{y}}<extra></extra>"))
    if lisa is not None and "quad" in lisa:
        hh = [labels[i] for i in range(len(labels)) if lisa["quad"][i] == "HH"]
        yh = [values[i] for i in range(len(labels)) if lisa["quad"][i] == "HH"]
        if hh:
            fig.add_trace(go.Scatter(x=hh, y=yh, mode="markers", name="LISA HH",
                                     marker=dict(symbol="star", size=11,
                                                 color="#FCBF49",
                                                 line=dict(width=1, color="#1B263B"))))
    fig.update_xaxes(title=unit_label, showgrid=False)
    fig.update_yaxes(title="Occurrences", showgrid=True, gridcolor="#EEF2F7")
    fig.update_layout(showlegend=bool(lisa is not None))
    fig = _layout(fig, f"Areal pattern · {target}  ({unit_label})", h=400)
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.18,
                                  xanchor="center", x=0.5),
                      margin=dict(t=46, l=30, r=20, b=60))
    return fig


def chart_gstar_focal(gs1d, target):
    """1-D moving-window focal z along the sequence — local hotspots / silences."""
    if not gs1d:
        return _layout(go.Figure(), f"Local focal score · {target}")
    z = gs1d["z"]; x = gs1d["centres"]
    colors = ["#B2182B" if v >= 1.96 else ("#2166AC" if v <= -1.96 else "#C7CDD8")
              for v in z]
    fig = go.Figure(go.Bar(x=x, y=z, marker_color=colors,
                           hovertemplate="idx=%{x:.0f}<br>focal z=%{y:.2f}<extra></extra>"))
    fig.add_hline(y=1.96, line=dict(color="#B2182B", dash="dot", width=1))
    fig.add_hline(y=-1.96, line=dict(color="#2166AC", dash="dot", width=1))
    fig.update_xaxes(title="Global ayah index", showgrid=False)
    fig.update_yaxes(title="Focal z (hot >1.96 · cold <−1.96)",
                     showgrid=True, gridcolor="#EEF2F7")
    return _layout(fig, f"Local focal hotspots · {target}", h=320)


def chart_forest_fingerprint(rows, scenario_label):
    """The 'latent feature' map: every root placed by global spread (coverage,
    x) vs local clustering (Fano, y), coloured by its areal Moran class. Reveals
    the corpus-wide signature — pervasive-but-bursty vs confined."""
    if not rows:
        return _layout(go.Figure(), "Spatial fingerprint")
    import pandas as _pd
    df = _pd.DataFrame(rows)
    cmap = {"clustered": PAL["input"], "regular": PAL["good"],
            "random": "#9AA3B2", "n/a": "#C7CDD8"}
    fig = go.Figure()
    for cls, sub in df.groupby("I_class"):
        fig.add_trace(go.Scattergl(
            x=sub["coverage"], y=sub["fano"], mode="markers", name=f"Moran {cls}",
            marker=dict(size=7, color=cmap.get(cls, "#888"), opacity=0.7,
                        line=dict(width=0.4, color="#1B263B")),
            text=sub["root"],
            hovertemplate="%{text}<br>coverage=%{x:.2f}<br>Fano=%{y:.2f}<extra></extra>",
        ))
    fig.add_hline(y=1.5, line=dict(color="#1B263B", dash="dot", width=1),
                  annotation_text="Fano=1.5 (bursty ↑)")
    fig.update_xaxes(title="Global spread → coverage (fraction of units touched)",
                     showgrid=True, gridcolor="#EEF2F7", range=[0, 1])
    fig.update_yaxes(title="Local clustering → Fano (gap variance/mean)",
                     showgrid=True, gridcolor="#EEF2F7", type="log")
    fig = _layout(fig, f"Corpus spatial fingerprint · {scenario_label}", h=480)
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.12,
                                  xanchor="center", x=0.5),
                      margin=dict(t=48, l=40, r=20, b=60))
    return fig


def chart_forest_summary_bars(summary):
    """Headline percentages for one rearrangement: local clustering, mean
    coverage (unsaturation), and the areal Moran breakdown."""
    if not summary:
        return _layout(go.Figure(), "Forest summary")
    labels = ["Local clustered<br>(Fano>thr)", "Mean coverage<br>(×100)",
              "Moran clustered", "Moran regular", "Moran random"]
    vals = [summary.get("local_clustered", 0),
            round(100 * summary.get("mean_coverage", 0), 1),
            summary.get("I_clustered", 0), summary.get("I_regular", 0),
            summary.get("I_random", 0)]
    colors = [PAL["input"], PAL["accent"], PAL["violet"], PAL["good"], "#9AA3B2"]
    fig = go.Figure(go.Bar(x=labels, y=vals, marker_color=colors,
                           text=[f"{v:.0f}" for v in vals], textposition="outside"))
    fig.update_yaxes(title="Percent", range=[0, 109], showgrid=True,
                     gridcolor="#EEF2F7")
    return _layout(fig, f"Forest headline · n={summary.get('n_roots',0)} roots", h=360)


def chart_archetype_embedding(res):
    """PCA(2) scatter of every root coloured by its k-means spatial archetype —
    the 'latent feature' map. Nearby roots share spatial behaviour."""
    if not res:
        return _layout(go.Figure(), "Spatial archetypes")
    emb = res["emb"]; lab = res["labels"]; roots = res["roots"]
    arche = {a["cluster"]: a for a in res["archetypes"]}
    pal = [PAL["input"], PAL["good"], PAL["violet"], PAL["accent"],
           PAL["teal"], PAL["gold"], "#9AA3B2", "#1D3557"]
    fig = go.Figure()
    for j in sorted(set(lab)):
        msk = lab == j
        name = f"{arche[j]['tag']} (n={arche[j]['n']})"
        fig.add_trace(go.Scattergl(
            x=emb[msk, 0], y=emb[msk, 1], mode="markers", name=name,
            marker=dict(size=7, color=pal[j % len(pal)], opacity=0.72,
                        line=dict(width=0.4, color="#1B263B")),
            text=[roots[i] for i in range(len(roots)) if msk[i]],
            hovertemplate="%{text}<br>PC1=%{x:.2f} PC2=%{y:.2f}<extra></extra>"))
    # Label a couple of representative roots per cluster (nearest its centroid)
    for j in sorted(set(lab)):
        idxs = np.where(lab == j)[0]
        if len(idxs) == 0:
            continue
        cen = emb[idxs].mean(0)
        near = idxs[np.argsort(((emb[idxs] - cen) ** 2).sum(1))[:2]]
        for ii in near:
            fig.add_annotation(x=emb[ii, 0], y=emb[ii, 1], text=roots[ii],
                               showarrow=False, yshift=9,
                               font=dict(size=10, color="#111"),
                               bgcolor="rgba(255,255,255,0.55)")
    # Biplot: PCA feature direction vectors (loadings) — which spatial features
    # pull along each axis. Shows the strongest few to stay legible.
    comps = res.get("components")
    feats = res.get("feat_names")
    if comps is not None and feats is not None:
        comps = np.asarray(comps)
        if comps.shape[0] >= 2 and comps.shape[1] == len(feats):
            lx, ly = comps[0], comps[1]
            mag = np.sqrt(lx ** 2 + ly ** 2)
            span = max(float(np.abs(emb[:, 0]).max()),
                       float(np.abs(emb[:, 1]).max()), 1e-9)
            fac = 0.78 * span / (mag.max() if mag.max() > 0 else 1.0)
            for idx in np.argsort(-mag)[:8]:
                ex, ey = float(lx[idx] * fac), float(ly[idx] * fac)
                fig.add_annotation(x=ex, y=ey, ax=0, ay=0, xref="x", yref="y",
                                   axref="x", ayref="y", showarrow=True,
                                   arrowhead=2, arrowsize=1, arrowwidth=1.4,
                                   arrowcolor="#33415C", opacity=0.8)
                fig.add_annotation(x=ex * 1.13, y=ey * 1.13, text=feats[idx],
                                   showarrow=False, font=dict(size=10, color="#1B263B"),
                                   bgcolor="rgba(255,255,255,0.65)")
    v = res["var"]
    fig.update_xaxes(title=f"PC1 ({v[0]*100:.0f}% var)", showgrid=True,
                     gridcolor="#EEF2F7", zeroline=True, zerolinecolor="#D7DCE5")
    fig.update_yaxes(title=f"PC2 ({v[1]*100:.0f}% var)", showgrid=True,
                     gridcolor="#EEF2F7", zeroline=True, zerolinecolor="#D7DCE5")
    fig = _layout(fig, "Latent spatial archetypes — PCA biplot (k-means clusters + feature vectors)", h=520)
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.13,
                                  xanchor="center", x=0.5),
                      margin=dict(t=48, l=40, r=20, b=64))
    return fig


def chart_archetype_profiles(res):
    """Heatmap of each archetype's standardised centroid across features — what
    DEFINES each cluster (red = above-average, blue = below)."""
    if not res:
        return _layout(go.Figure(), "Archetype profiles")
    Cz = np.asarray(res["centroids_z"])
    feats = res["feat_names"]
    arche = {a["cluster"]: a for a in res["archetypes"]}
    ylab = [f"c{j} · {arche[j]['tag']}" for j in range(len(Cz))]
    zmax = max(1.5, float(np.max(np.abs(Cz))))
    fig = go.Figure(go.Heatmap(
        z=Cz, x=feats, y=ylab, colorscale=[[0, "#2166AC"], [0.5, "#F7F7F7"],
                                           [1, "#B2182B"]],
        zmin=-zmax, zmax=zmax, colorbar=dict(title="z", thickness=12),
        hovertemplate="%{y}<br>%{x} = %{z:.2f} σ<extra></extra>"))
    fig.update_xaxes(tickangle=-40)
    return _layout(fig, "What defines each archetype (centroid, σ units)", h=360)


def chart_density_series(sp, order_label):
    """A concept's density as a 1-D spatial series along the chosen ordering."""
    if not sp:
        return _layout(go.Figure(), "Spatial series")
    fig = go.Figure(go.Scatter(x=sp["centres"], y=sp["series"], mode="lines",
                               line=dict(color=PAL["violet"], width=2),
                               fill="tozeroy", fillcolor="rgba(114,9,183,0.12)",
                               hovertemplate="pos=%{x:.0f}<br>count=%{y}<extra></extra>"))
    fig.update_xaxes(title=f"Position — {order_label}", showgrid=True,
                     gridcolor="#EEF2F7")
    fig.update_yaxes(title="Occurrences / bin", showgrid=True, gridcolor="#EEF2F7")
    return _layout(fig, f"Spatial series · {sp['target']}", h=300)


def chart_acf(sp):
    """Autocorrelation of the density series with a ±95% white-noise band.
    Bars outside the band = real memory / periodicity at that lag."""
    if not sp:
        return _layout(go.Figure(), "Autocorrelation")
    a = sp["acf"]; lags = np.arange(len(a))
    n = max(len(sp["series"]), 2)
    conf = 1.96 / np.sqrt(n)
    fig = go.Figure(go.Bar(x=lags, y=a, marker_color=PAL["teal"],
                           hovertemplate="lag=%{x}<br>acf=%{y:.3f}<extra></extra>"))
    fig.add_hline(y=conf, line=dict(color="#B2182B", dash="dot", width=1))
    fig.add_hline(y=-conf, line=dict(color="#B2182B", dash="dot", width=1))
    fig.update_xaxes(title="Lag (bins)", showgrid=False)
    fig.update_yaxes(title="ACF", showgrid=True, gridcolor="#EEF2F7")
    return _layout(fig, f"Autocorrelation · {sp['target']}", h=300)


def chart_periodogram(sp):
    """Power spectrum: which recurrence wavelengths carry energy. Dominant
    period flagged. (Detrended; treat broad low-frequency peaks as trend, not
    true periodicity.)"""
    if not sp:
        return _layout(go.Figure(), "Periodogram")
    per = sp["periods"]; pw = sp["power"]
    msk = np.isfinite(per) & (per > 1)
    per = per[msk]; pw = pw[msk]
    if len(per) == 0:
        return _layout(go.Figure(), f"Periodogram · {sp['target']}")
    order = np.argsort(per)
    fig = go.Figure(go.Scatter(x=per[order], y=pw[order], mode="lines",
                               line=dict(color=PAL["accent"], width=2),
                               hovertemplate="period=%{x:.1f} bins<br>power=%{y:.2g}<extra></extra>"))
    if np.isfinite(sp["dom_period"]):
        fig.add_vline(x=sp["dom_period"], line=dict(color=PAL["input"], dash="dot"),
                      annotation_text=f"dominant ≈ {sp['dom_period']:.0f} bins")
    fig.update_xaxes(title="Period (bins, log)", type="log", showgrid=True,
                     gridcolor="#EEF2F7")
    fig.update_yaxes(title="Spectral power", showgrid=True, gridcolor="#EEF2F7")
    return _layout(fig, f"Periodogram · {sp['target']}", h=300)


def chart_cross_correlation(lags, xc, a_label, b_label, n=120):
    """Cross-correlation of two concept density series; peak lag = which leads.
    A ±95% white-noise band (≈1.96/√n) gates real signal from chance."""
    peak = int(lags[int(np.argmax(np.abs(xc)))]) if len(xc) else 0
    conf = 1.96 / np.sqrt(max(n, 2))
    sig = bool(len(xc) and np.abs(xc).max() > conf)
    fig = go.Figure(go.Bar(x=lags, y=xc, marker_color=PAL["partner"],
                           hovertemplate="lag=%{x}<br>xcorr=%{y:.3f}<extra></extra>"))
    fig.add_hline(y=conf, line=dict(color="#B2182B", dash="dot", width=1))
    fig.add_hline(y=-conf, line=dict(color="#B2182B", dash="dot", width=1))
    fig.add_vline(x=0, line=dict(color="#1B263B", width=1))
    if sig:
        fig.add_vline(x=peak, line=dict(color=PAL["input"], dash="dot"),
                      annotation_text=f"peak lag {peak:+d}")
    else:
        fig.add_annotation(text="no lag clears the 95% band — within noise",
                           x=0.5, xref="paper", y=1.0, yref="paper",
                           showarrow=False, font=dict(color="#B2182B", size=12))
    fig.update_xaxes(title=f"Lag (bins) — positive = {a_label} leads {b_label}",
                     showgrid=False)
    fig.update_yaxes(title="Normalised cross-corr", showgrid=True,
                     gridcolor="#EEF2F7")
    return _layout(fig, f"Cross-correlation · {a_label} ↔ {b_label}", h=320)


def chart_k_scan(k_scan):
    """Mean bootstrap stability vs k — how many spatial archetypes the data
    actually supports. Stability stays high then drops at the right k."""
    if not k_scan:
        return _layout(go.Figure(), "How many archetypes?")
    ks = [x[0] for x in k_scan]; ss = [x[1] for x in k_scan]
    fig = go.Figure(go.Scatter(x=ks, y=ss, mode="lines+markers",
                               line=dict(color=PAL["violet"], width=3),
                               marker=dict(size=10, color=PAL["violet"]),
                               hovertemplate="k=%{x}<br>stability=%{y:.2f}<extra></extra>"))
    fig.add_hline(y=0.9, line=dict(color=PAL["good"], dash="dot", width=1),
                  annotation_text="0.9 = robust")
    fig.update_xaxes(title="k (number of archetypes)", dtick=1, showgrid=True,
                     gridcolor="#EEF2F7")
    fig.update_yaxes(title="mean bootstrap stability", range=[0, 1.04],
                     showgrid=True, gridcolor="#EEF2F7")
    return _layout(fig, "How many archetypes does the data support?", h=320)


def chart_density_surface(su, ay, target):
    """2-D kernel-density 'hotspot surface' over the muṣḥaf grid — x = surah,
    y = ayah within surah. Bright cells = where the concept concentrates."""
    if su is None or len(su) == 0:
        return _layout(go.Figure(), f"Hotspot surface · {target}")
    fig = go.Figure(go.Histogram2d(
        x=su, y=ay, colorscale="Hot", reversescale=True,
        nbinsx=57, nbinsy=40, colorbar=dict(title="density", thickness=12),
        hovertemplate="surah %{x}<br>ayah %{y}<br>count %{z}<extra></extra>"))
    fig.update_xaxes(title="Surah (1 → 114)", dtick=10)
    fig.update_yaxes(title="Ayah within surah")
    return _layout(fig, f"Density hotspot surface · {target}", h=400)


def chart_cumulative_growth(xy, target, order_label):
    """Cumulative occurrence count along the ordering — slope = local rate,
    flat = silence, steep = a burst. Shows WHERE the concept accumulates."""
    if xy is None or len(xy) < 2:
        return _layout(go.Figure(), f"Growth · {target}")
    y = np.sort(xy[:, 1])
    cum = np.arange(1, len(y) + 1)
    ymax = float(y.max()) if len(y) else 1
    fig = go.Figure(go.Scatter(
        x=[0] + y.tolist() + [ymax], y=[0] + cum.tolist() + [len(y)],
        mode="lines", line=dict(color=PAL["good"], width=2.6, shape="hv"),
        fill="tozeroy", fillcolor="rgba(6,167,93,0.10)",
        hovertemplate="index %{x:.0f}<br>count so far %{y}<extra></extra>"))
    fig.update_xaxes(title=f"Global ayah index — {order_label}", showgrid=True,
                     gridcolor="#EEF2F7")
    fig.update_yaxes(title="Cumulative occurrences", showgrid=True,
                     gridcolor="#EEF2F7")
    return _layout(fig, f"Growth trajectory · {target}", h=340)


def chart_control_comparison(res):
    """Real Qur'an vs frequency-matched scramble — grouped bars per headline
    metric, with the scramble's ±σ as error bars. Bars that match = frequency
    artifacts; bars that differ (beyond the error) = real structure."""
    if not res:
        return _layout(go.Figure(), "Control comparison")
    metrics = ["local_clustered", "I_clustered", "I_regular", "I_random"]
    labels = ["Local clustered", "Moran clustered", "Moran regular", "Moran random"]
    real = [res["verdict"][m]["real"] for m in metrics]
    null = [res["verdict"][m]["null_mean"] for m in metrics]
    sd = [res["verdict"][m]["null_sd"] for m in metrics]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=labels, y=real, name="Real Qur'an",
                         marker_color=PAL["input"],
                         text=[f"{r:.0f}" for r in real], textposition="outside"))
    fig.add_trace(go.Bar(x=labels, y=null, name="Scramble (μ±σ)",
                         marker_color="#9AA3B2",
                         error_y=dict(type="data", array=sd, visible=True)))
    fig.update_yaxes(title="Percent of roots", range=[0, 112])
    fig.update_layout(barmode="group")
    fig = _layout(fig, "Real vs frequency-matched scrambled scripture", h=380)
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.12,
                                  xanchor="center", x=0.5),
                      margin=dict(t=46, l=40, r=20, b=56))
    return fig


def chart_colocation_heatmap(res):
    """Concept × concept areal co-location: red = share territory, blue = avoid.
    Significant cells (perm p≤0.05) outlined. The latent 'semantic geography'."""
    if not res:
        return _layout(go.Figure(), "Co-location")
    roots = res["roots"]; aff = res["affinity"]; p = res["pvals"]
    z = np.where(np.isnan(aff), 0.0, aff)
    txt = [[("✶" if (i != j and p[i, j] <= 0.05) else "") for j in range(len(roots))]
           for i in range(len(roots))]
    fig = go.Figure(go.Heatmap(
        z=z, x=roots, y=roots, colorscale=[[0, "#2166AC"], [0.5, "#F7F7F7"],
                                           [1, "#B2182B"]], zmid=0,
        text=txt, texttemplate="%{text}", textfont=dict(size=14, color="#1B263B"),
        colorbar=dict(title="affinity", thickness=12),
        hovertemplate="%{y} ↔ %{x}<br>affinity %{z:.2f}<extra></extra>"))
    fig.update_yaxes(autorange="reversed")
    h = min(540, max(220, 34 * len(roots) + 130))
    return _layout(fig, "Concept co-location  (✶ = significant, p≤0.05)", h=h)


def chart_colocation_neighbors(res):
    """Top corpus co-locators of one concept — red bars = share its surahs,
    blue bars = avoid. The concept's 'neighbours' in semantic geography."""
    if not res:
        return _layout(go.Figure(), "Co-locators")
    share = res["share"][:12]
    avoid = [a for a in res["avoid"] if a[1] < 0][:6]
    rows = list(reversed(avoid)) + list(reversed(share))
    if not rows:
        return _layout(go.Figure(), f"Co-locators · {res['target']}")
    labels = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    cols = [PAL["input"] if v > 0 else "#2166AC" for v in vals]
    star = ["✶" if r[2] <= 0.05 else "" for r in rows]
    fig = go.Figure(go.Bar(x=vals, y=labels, orientation="h", marker_color=cols,
                           text=star, textposition="outside",
                           hovertemplate="%{y}<br>affinity %{x:.2f}<extra></extra>"))
    fig.add_vline(x=0, line=dict(color="#1B263B", width=1))
    fig.update_xaxes(title="affinity  (← avoid · share →)", showgrid=True,
                     gridcolor="#EEF2F7")
    return _layout(fig, f"Corpus co-locators · {res['target']}  (✶ p≤0.05)", h=440)


def chart_colocation_network(net):
    """Node-link graph of the expanding co-location field: seeds (gold) + their
    corpus co-locators (violet), red edges = share territory, blue = avoid."""
    if not net or not net.get("edges"):
        return _layout(go.Figure(), "Co-location network")
    g = nx.Graph()
    for n in net["nodes"]:
        g.add_node(n)
    for a, b, aff, p, rel in net["edges"]:
        g.add_edge(a, b, weight=abs(aff), aff=aff)
    pos = nx.spring_layout(g, seed=2, k=1.1 / (len(net["nodes"]) ** 0.5))
    fig = go.Figure()
    for a, b, aff, p, rel in net["edges"]:
        x0, y0 = pos[a]; x1, y1 = pos[b]
        fig.add_trace(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None], mode="lines",
            line=dict(width=0.4 + 1.8 * abs(aff),
                      color=("rgba(178,24,43,%.2f)" % (0.35 + 0.5 * abs(aff))) if aff > 0
                      else ("rgba(33,102,172,%.2f)" % (0.35 + 0.5 * abs(aff)))),
            hoverinfo="skip", showlegend=False))
    for role, col in (("colocator", PAL["violet"]), ("seed", PAL["gold"])):
        ns = [n for n in net["nodes"] if net["roles"][n] == role]
        if not ns:
            continue
        fig.add_trace(go.Scatter(
            x=[pos[n][0] for n in ns], y=[pos[n][1] for n in ns],
            mode="markers+text", text=ns, textposition="top center",
            textfont=dict(size=16, color="#1B263B"),
            marker=dict(size=[20 if role == "seed" else 13 for _ in ns],
                        color=col, line=dict(width=1.5, color="#1B263B")),
            name=("seeds (your query)" if role == "seed" else "corpus co-locators"),
            hovertemplate="%{text}<extra></extra>"))
    fig.update_xaxes(visible=False); fig.update_yaxes(visible=False)
    fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.04,
                                  xanchor="center", x=0.5))
    return _layout(fig, "Co-location network — seeds → corpus co-locators "
                        "(red=share · blue=avoid)", h=560)


def chart_fusion_scatter(points, xlab, ylab, title, zlab="spatial"):
    """Dense multimodal-FUSION map. Each related item is placed by two independent
    modality z-scores (x, y); MARKER SIZE encodes the THIRD modality |z|; COLOUR
    encodes its six-type relation; the seed sits at the origin and the relation
    REGIONS are annotated. Three modalities + relation type + labels in one view."""
    REL = {"consensus": "#0F6E56", "semantic": "#185FA5", "co-location": "#BA7517",
           "spatial": "#7209B7", "orthogonal": "#5F5E5A", "divergent": "#E63946",
           "resonant": "#185FA5", "direct": "#06A77D"}
    fig = go.Figure()
    if not points:
        return _layout(fig, title)
    xs = [p["x"] for p in points]; ys = [p["y"] for p in points]
    span = max(2.2, max(abs(v) for v in xs + ys) + 0.6)
    fig.add_hline(y=0, line=dict(color="#C9D2DE", width=1))
    fig.add_vline(x=0, line=dict(color="#C9D2DE", width=1))
    # faint relation-zone shading reinforces the corner labels
    fig.add_shape(type="rect", x0=0, y0=0, x1=span, y1=span, layer="below",
                  fillcolor="rgba(15,110,86,0.06)", line_width=0)      # consensus
    fig.add_shape(type="rect", x0=0, y0=-span, x1=span, y1=0, layer="below",
                  fillcolor="rgba(227,57,70,0.05)", line_width=0)      # divergent
    fig.add_shape(type="rect", x0=-span, y0=0, x1=0, y1=span, layer="below",
                  fillcolor="rgba(227,57,70,0.05)", line_width=0)
    # what each zone MEANS in the fusion (corners + edges)
    fig.add_annotation(x=span * 0.9, y=span * 0.92, text="<b>consensus</b>", showarrow=False,
                       font=dict(size=14, color="#0B5440"), opacity=1)
    fig.add_annotation(x=span * 0.9, y=-span * 0.92, text="<b>divergent</b>", showarrow=False,
                       font=dict(size=14, color="#A32D2D"), opacity=1)
    fig.add_annotation(x=span * 0.9, y=0.22, text=f"<b>{xlab}-only</b>", showarrow=False,
                       font=dict(size=12, color="#0C447C"), opacity=1)
    fig.add_annotation(x=0.26, y=span * 0.92, text=f"<b>{ylab}-only</b>", showarrow=False,
                       font=dict(size=12, color="#854F0B"), opacity=1)
    by = {}
    for p in points:
        by.setdefault(p["relation"], []).append(p)
    order = ["consensus", "semantic", "co-location", "resonant", "direct",
             "spatial", "orthogonal", "divergent"]
    for rel in [r for r in order if r in by] + [r for r in by if r not in order]:
        pts = by[rel]
        sizes = [9 + min(22, abs(p.get("size", 0)) * 6) for p in pts]
        fig.add_trace(go.Scatter(
            x=[p["x"] for p in pts], y=[p["y"] for p in pts],
            mode="markers+text", name=rel,
            text=[p["label"] for p in pts], textposition="top center",
            textfont=dict(size=13, color="#0B1320"),
            marker=dict(size=sizes, color=REL.get(rel, "#888"), opacity=0.82,
                        line=dict(width=0.6, color="#FFFFFF")),
            customdata=[[p.get("size", 0)] for p in pts],
            hovertemplate=("<b>%{text}</b><br>" + xlab + "=%{x:+.1f}  " + ylab +
                           "=%{y:+.1f}  " + zlab +
                           "=%{customdata[0]:+.1f}<extra>" + rel + "</extra>")))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers+text", text=["◆ seed"],
                             textposition="bottom center",
                             textfont=dict(size=12, color="#1D3557"),
                             marker=dict(size=12, color="#1D3557", symbol="diamond"),
                             showlegend=False, hoverinfo="skip"))
    _layout(fig, title, h=470)
    fig.update_layout(margin=dict(l=20, r=10, t=42, b=70))
    fig.update_layout(
        xaxis_title=f"{xlab} (z)", yaxis_title=f"{ylab} (z)  ·  marker size = |{zlab}|",
        legend=dict(orientation="h", yanchor="top", y=-0.14, x=0.5, xanchor="center",
                    font=dict(size=13, color="#1B263B")),
        xaxis=dict(range=[-span, span], zeroline=False, gridcolor="#EDF1F6",
                   tickfont=dict(size=12, color="#1B263B"), title_font=dict(size=14)),
        yaxis=dict(range=[-span, span], zeroline=False, gridcolor="#EDF1F6",
                   tickfont=dict(size=12, color="#1B263B"), title_font=dict(size=14)))
    return fig


def chart_triad_significance(df: pd.DataFrame, glob_len: float) -> go.Figure:
    """Honest triad diagnostic. One dense scatter that EXPOSES why raw co-occurrence
    misleads and shows which triads are genuinely associated:
      • x = raw co-occurrence (Sum Weight, log) — what the old ranking used
      • y = Lift = Obs / Expected-under-frequency (log) — association beyond chance;
        the dashed line at Lift=1 is "no more than frequency predicts"
      • colour = verse length (mean roots/verse of the shared verses); points far above
        the global mean (✦) are long-verse saturation artifacts
      • a gold ring = the rare triad with genuine 3-way structure (3-way p < 0.05)
    Reading: points bottom-right = high raw weight but low lift = frequency artifacts;
    hot-coloured points = long-verse artifacts; top points = real association."""
    if df is None or len(df) == 0:
        return _layout(go.Figure(), "Triad significance")
    d = df.copy()
    sw = d["Sum Weight"].clip(lower=1).astype(float)
    lift = d["Lift"].clip(lower=0.1).astype(float)
    genuine = d["3-way p"] < 0.05
    hover = [
        f"<b>{a} · {b} · {c}</b><br>Obs together: {o}<br>Expected (freq): {e}<br>"
        f"Lift: {l}×<br>Z (assoc): {z}<br>3-way p: {p}<br>Verse len: {vl} (global {glob_len:.1f})"
        for a, b, c, o, e, l, z, p, vl in zip(
            d["Root A"], d["Root B"], d["Root C"], d["Obs"], d["Expected"],
            d["Lift"], d["Z (assoc)"], d["3-way p"], d["Verse len"])]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sw, y=lift, mode="markers",
        marker=dict(size=(8 + 3 * np.sqrt(d["Obs"].astype(float))),
                    color=d["Verse len"].astype(float), colorscale=CONTINUOUS,
                    cmin=glob_len * 0.6, cmax=glob_len * 2.2, showscale=True,
                    colorbar=dict(title="verse<br>length", thickness=12),
                    line=dict(width=1, color="#10243A")),
        text=hover, hoverinfo="text", showlegend=False))
    # gold rings on genuine 3-way triads + labels
    if genuine.any():
        g = d[genuine]
        fig.add_trace(go.Scatter(
            x=g["Sum Weight"].clip(lower=1), y=g["Lift"].clip(lower=0.1),
            mode="markers+text",
            text=[f"{a}·{b}·{c}" for a, b, c in zip(g["Root A"], g["Root B"], g["Root C"])],
            textposition="top center", textfont=dict(size=12, color="#10243A"),
            marker=dict(size=20, color="rgba(0,0,0,0)",
                        line=dict(width=3, color=PAL["gold"])),
            hoverinfo="skip", showlegend=False))
    fig.add_hline(y=1.0, line=dict(color="#10243A", width=1, dash="dash"),
                  annotation_text="Lift = 1 (frequency-only)", annotation_position="bottom right",
                  annotation_font=dict(size=12, color="#10243A"))
    _layout(fig, "Triad honesty map — association vs raw co-occurrence vs verse length", h=520)
    fig.update_layout(
        xaxis=dict(title="raw co-occurrence (Sum Weight) — log", type="log",
                   gridcolor="#EDF1F6", tickfont=dict(size=12, color="#10243A"),
                   title_font=dict(size=14, color="#10243A")),
        yaxis=dict(title="Lift = Obs / Expected (log) — association beyond frequency",
                   type="log", gridcolor="#EDF1F6", tickfont=dict(size=12, color="#10243A"),
                   title_font=dict(size=14, color="#10243A")))
    return fig


def chart_dependency(dep: dict, root: str, max_each: int = 7) -> go.Figure:
    """Directed dependency radial for one root. LEFT (teal) = roots that IMPLY this root
    (X ⇒ root, satellites); RIGHT (orange) = what this root BRINGS (root ⇒ X). Arrow width
    scales with LIFT (frequency-controlled). `dep` = {'in':[(x,w,conf,lift)], 'out':[...]}."""
    ins = (dep.get("in") or [])[:max_each]
    outs = (dep.get("out") or [])[:max_each]
    fig = go.Figure()
    if not ins and not outs:
        return _layout(fig, f"Dependencies · {root}")
    import math as _m
    mlift = max([t[3] for t in ins + outs] + [2.0])

    def _ew(lift):
        return 1.5 + 4.5 * (_m.log(max(lift, 1.01)) / _m.log(max(mlift, 1.02)))

    def _ys(n):
        if n <= 1:
            return [0.0]
        return [1.0 - 2.0 * k / (n - 1) for k in range(n)]

    TEAL, ORANGE, NAVY = "#06AED5", "#F77F00", "#1D3557"
    nx_, ny_, ntext, ncol, nhov = [], [], [], [], []
    # incoming (left): arrow X -> root. Clean arrow only — the P·lift values live in the hover and
    # in the caption above, NOT stamped on the node (which overlapped the root label = clutter).
    for (x, w, conf, lift), y in zip(ins, _ys(len(ins))):
        nx_.append(-1); ny_.append(y); ntext.append(x); ncol.append(TEAL)
        nhov.append(f"{x} ⇒ {root} · P={conf:.2f} · {lift:.0f}× lift · {int(w)} shared verses")
        fig.add_annotation(ax=-1, ay=y, x=-0.10, y=0, xref="x", yref="y",
                           axref="x", ayref="y", showarrow=True, arrowhead=3,
                           arrowsize=1, arrowwidth=_ew(lift), arrowcolor=TEAL, opacity=0.85)
    # outgoing (right): arrow root -> X
    for (x, w, conf, lift), y in zip(outs, _ys(len(outs))):
        nx_.append(1); ny_.append(y); ntext.append(x); ncol.append(ORANGE)
        nhov.append(f"{root} ⇒ {x} · P={conf:.2f} · {lift:.0f}× lift · {int(w)} shared verses")
        fig.add_annotation(ax=0.10, ay=0, x=1, y=y, xref="x", yref="y",
                           axref="x", ayref="y", showarrow=True, arrowhead=3,
                           arrowsize=1, arrowwidth=_ew(lift), arrowcolor=ORANGE, opacity=0.85)
    # leaf nodes — label sits OUTSIDE the dot (left of the left column, right of the right column)
    # so the Arabic root is NEVER clipped by the circle (it was occluded inside the 40px marker).
    # Ink text on the light background; smaller solid dots since they no longer hold text.
    _tpos = ["middle left" if xx < 0 else "middle right" for xx in nx_]
    fig.add_trace(go.Scatter(
        x=nx_, y=ny_, mode="markers+text", text=[f"  {t}  " for t in ntext], textposition=_tpos,
        textfont=dict(size=14, color="#10243A"),
        marker=dict(size=28, color=ncol, line=dict(width=1.5, color="#FFFFFF")),
        hoverinfo="text", hovertext=nhov, showlegend=False, cliponaxis=False))
    # centre root
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode="markers+text", text=[root], textposition="middle center",
        textfont=dict(size=18, color="#FFFFFF"),
        marker=dict(size=66, color=NAVY, line=dict(width=2, color="#10243A")),
        hoverinfo="skip", showlegend=False))
    # side labels
    fig.add_annotation(x=-1, y=1.28, text="<b>implies →</b> "+root, showarrow=False,
                       font=dict(size=13, color=TEAL), xanchor="center")
    fig.add_annotation(x=1, y=1.28, text=root+" <b>→ brings</b>", showarrow=False,
                       font=dict(size=13, color=ORANGE), xanchor="center")
    _layout(fig, f"Directed dependencies · {root}  (arrow width = lift)", h=460)
    fig.update_layout(
        xaxis=dict(visible=False, range=[-1.95, 1.95]),
        yaxis=dict(visible=False, range=[-1.45, 1.45]),
        margin=dict(l=10, r=10, t=46, b=10))
    return fig
