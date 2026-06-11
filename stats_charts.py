"""Tile-friendly Plotly charts for the Statistics page.

Each chart is designed to be standalone, easy to read, and uses small-multiples
(facets) instead of overlapping series when comparing across input roots.

The previous heatmap-style charts (PMI / P(B|A) / Jaccard) have been replaced
by clearer sorted bar charts of root-pairs — heatmaps are still acceptable for
expert use, but the bars are far easier to read at a glance.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

PAL = {
    "input": "#E63946", "partner": "#1D3557", "accent": "#F77F00",
    "good": "#06A77D", "violet": "#7209B7", "teal": "#06AED5",
    "gold": "#FCBF49", "bg": "#FFFFFF",
}
CONTINUOUS = "Plasma"
DIVERGING = "RdBu_r"


def _layout(fig, title="", h=None):
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", x=0.5, xanchor="center", font=dict(size=15)),
        paper_bgcolor=PAL["bg"], plot_bgcolor="#F8FAFC",
        font=dict(family="Arial, 'Segoe UI', sans-serif", size=12, color="#1B263B"),
        margin=dict(l=25, r=18, t=40, b=25),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    if h:
        fig.update_layout(height=h)
    return fig


def chart_frequency_bars(freq_df):
    if freq_df.empty:
        return _layout(go.Figure(), "Frequency")
    fig = px.bar(freq_df, x="Input Root", y="Frequency",
                 color="Input Root", text="Frequency",
                 color_discrete_sequence=px.colors.qualitative.Vivid)
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, yaxis_title="Ayahs")
    return _layout(fig, "Ayah frequency per input root", h=340)


def chart_dispersion(freq_df):
    if freq_df.empty:
        return _layout(go.Figure(), "Dispersion")
    long = freq_df.melt(id_vars="Input Root",
                        value_vars=["Juilland D (0–1)", "Entropy normalized"],
                        var_name="Metric", value_name="Value")
    fig = px.bar(long, x="Input Root", y="Value", color="Metric",
                 barmode="group", text="Value",
                 color_discrete_sequence=[PAL["teal"], PAL["accent"]])
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_layout(yaxis_range=[0, 1.1], yaxis_title="Score (0–1)")
    return _layout(fig, "Dispersion across surahs (higher = more uniform)", h=340)


def chart_position_tiles(pos_df):
    if pos_df.empty:
        return _layout(go.Figure(), "Position in ayah")
    long = pos_df.melt(id_vars="Input Root",
                       value_vars=["Start %", "Middle %", "End %"],
                       var_name="Position", value_name="%")
    fig = px.bar(long, x="Position", y="%", color="Position",
                 facet_col="Input Root", facet_col_wrap=4, text="%",
                 color_discrete_map={"Start %": PAL["teal"],
                                     "Middle %": PAL["gold"],
                                     "End %": PAL["input"]})
    fig.update_traces(texttemplate="%{text:.0f}%", textposition="outside")
    fig.update_layout(showlegend=False, yaxis_range=[0, 100])
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return _layout(fig, "Where each root sits in its ayahs (tiles)", h=360)


def _pair_list(matrix, value_label, symmetric=True):
    rows = []
    idx = list(matrix.index)
    cols = list(matrix.columns)
    for i, a in enumerate(idx):
        start = (i + 1) if symmetric else 0
        for j in range(start, len(cols)):
            b = cols[j]
            if a == b:
                continue
            try:
                v = float(matrix.iloc[i, j])
            except Exception:
                continue
            if pd.notna(v):
                rows.append({"Pair": f"{a}  ↔  {b}", "A": a, "B": b, value_label: v})
    return pd.DataFrame(rows)


def chart_pmi_heatmap(pmi_df):
    """Sorted diverging bars — positive PMI green, negative red. Replaces heatmap."""
    if pmi_df.empty:
        return _layout(go.Figure(), "PMI")
    df = _pair_list(pmi_df, "PMI", symmetric=True)
    if df.empty:
        return _layout(go.Figure(), "PMI")
    df = df.sort_values("PMI", ascending=True).reset_index(drop=True)
    colors = [PAL["good"] if v > 0 else PAL["input"] for v in df["PMI"]]
    fig = go.Figure(go.Bar(
        x=df["PMI"], y=df["Pair"], orientation="h",
        marker_color=colors,
        text=[f"{v:+.2f}" for v in df["PMI"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>PMI: %{x:.3f}<extra></extra>",
    ))
    fig.add_vline(x=0, line_color="#1B263B", line_width=1)
    fig.update_layout(xaxis_title="PMI (bits) — green > 0 associated, red < 0 avoidant",
                      yaxis_title="")
    return _layout(fig, "Pair association strength (PMI) — sorted",
                   h=max(320, 60 + 36 * len(df)))


def chart_cond_prob_heatmap(cp_df):
    """Small multiples — one bar chart per 'given A' root."""
    if cp_df.empty:
        return _layout(go.Figure(), "P(B|A)")
    rows = []
    for a in cp_df.index:
        for b in cp_df.columns:
            if a == b:
                continue
            try:
                v = float(cp_df.loc[a, b])
            except Exception:
                continue
            if pd.notna(v):
                rows.append({"Given A": str(a), "Then B": str(b), "P(B|A)": v})
    if not rows:
        return _layout(go.Figure(), "P(B|A)")
    long = pd.DataFrame(rows)
    long = long.sort_values(["Given A", "P(B|A)"], ascending=[True, True])
    n = long["Given A"].nunique()
    n_cols = min(3, n)
    n_rows_grid = (n + n_cols - 1) // n_cols
    fig = px.bar(long, x="P(B|A)", y="Then B", orientation="h",
                 facet_col="Given A", facet_col_wrap=n_cols,
                 color="P(B|A)", color_continuous_scale="Tealrose",
                 text="P(B|A)")
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_yaxes(matches=None, showticklabels=True)
    max_v = long["P(B|A)"].max() if not long.empty else 1.0
    fig.update_xaxes(range=[0, max(max_v * 1.15, 0.05)])
    fig.for_each_annotation(lambda a: a.update(text="Given: " + a.text.split("=")[-1]))
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    return _layout(fig, "Given root A appears, how often is each B also there?",
                   h=max(320, 220 * n_rows_grid))


def chart_jaccard_heatmap(j_df):
    """Sorted horizontal bars of pairs by Jaccard similarity."""
    if j_df.empty:
        return _layout(go.Figure(), "Jaccard")
    df = _pair_list(j_df, "Jaccard", symmetric=True)
    if df.empty:
        return _layout(go.Figure(), "Jaccard")
    df = df.sort_values("Jaccard", ascending=True).reset_index(drop=True)
    fig = px.bar(df, x="Jaccard", y="Pair", orientation="h",
                 color="Jaccard", color_continuous_scale="Viridis",
                 text="Jaccard")
    fig.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    max_v = df["Jaccard"].max()
    fig.update_layout(showlegend=False, coloraxis_showscale=False,
                      xaxis_range=[0, max(max_v * 1.18, 0.05)],
                      yaxis_title="", xaxis_title="Jaccard similarity (0 → 1)")
    return _layout(fig, "Pair similarity (Jaccard = shared / union) — sorted",
                   h=max(320, 60 + 36 * len(df)))


def chart_surah_role_bar(surah_role_df, top=15):
    if surah_role_df.empty:
        return _layout(go.Figure(), "Surah importance")
    sub = surah_role_df.head(top).copy()
    sub["Surah"] = sub["Surah Name"].astype(str) + " (" + sub["Surah #"].astype(str) + ")"
    sub = sub.iloc[::-1]
    fig = px.bar(sub, x="Importance score", y="Surah", orientation="h",
                 color="Input roots present", color_continuous_scale="Sunset",
                 hover_data=["Total hits", "Share of surah from input roots"])
    return _layout(fig, f"Top {top} surahs by importance to this query", h=460)


def chart_tfidf_dot(tfidf_df, top=15):
    if tfidf_df.empty:
        return _layout(go.Figure(), "TF-IDF")
    sub = tfidf_df.copy()
    sub["Surah label"] = sub["Surah Name"].astype(str) + " (" + sub["Surah #"].astype(str) + ")"
    fig = px.scatter(sub, x="TF-IDF", y="Surah label", color="Input Root",
                     size="Hits in surah", size_max=22,
                     color_discrete_sequence=px.colors.qualitative.Vivid,
                     facet_col="Input Root", facet_col_wrap=3)
    fig.update_yaxes(matches=None, showticklabels=True)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    return _layout(fig, "Surahs most characteristic for each root (TF-IDF dot)", h=440)


def chart_enrichment_scatter(enr_df, top=40):
    if enr_df.empty:
        return _layout(go.Figure(), "Enrichment")
    import math
    sub = enr_df.head(top).copy()
    sub["Surah label"] = sub["Surah Name"].astype(str) + " (" + sub["Surah #"].astype(str) + ")"
    fig = px.scatter(sub, x="Enrichment (obs/exp)", y="-log10(p)",
                     color="Input Root", size="Observed", size_max=22,
                     color_discrete_sequence=px.colors.qualitative.Vivid,
                     hover_data=["Surah label", "Observed", "Expected", "p-value"])
    fig.add_hline(y=-math.log10(0.05), line_dash="dot", line_color="gray",
                  annotation_text="p = 0.05", annotation_position="top left")
    return _layout(fig, "Surah enrichment (volcano) — top-right = strong & significant", h=440)


def chart_cumulative(cum_df):
    if cum_df.empty:
        return _layout(go.Figure(), "Cumulative")
    fig = px.line(cum_df, x="Surah #", y="Cumulative hits",
                  facet_col="Input Root", facet_col_wrap=3,
                  color_discrete_sequence=[PAL["accent"]])
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    fig.update_layout(showlegend=False)
    return _layout(fig, "Cumulative ayah-hit trajectory (Surah 1 → 114)", h=360)


def chart_network_extras(extras_df, metric="PageRank", top=20):
    if extras_df.empty:
        return _layout(go.Figure(), metric)
    sub = extras_df.head(top).iloc[::-1]
    fig = px.bar(sub, x=metric, y="Root", orientation="h",
                 color="Is Input",
                 color_discrete_map={True: PAL["input"], False: PAL["partner"]},
                 hover_data=["k-core", "Ego density", "Triangles@node"])
    return _layout(fig, f"{metric} — top {top} roots", h=460)


def chart_exclusive_partners(df, top=15):
    if df.empty:
        return _layout(go.Figure(), "Exclusive partners")
    sub = df.head(top).iloc[::-1]
    fig = px.bar(sub, x="Ayahs with input", y="Exclusive Partner", orientation="h",
                 color="Exclusivity", color_continuous_scale="Sunset",
                 hover_data=["Other ayahs"])
    return _layout(fig, "Roots that almost only appear with your input", h=400)


def chart_dendrogram(jaccard_df):
    if jaccard_df.empty or len(jaccard_df) < 2:
        return _layout(go.Figure(), "Dendrogram")
    try:
        import plotly.figure_factory as ff
        import numpy as np
        from scipy.spatial.distance import squareform
        from scipy.cluster.hierarchy import linkage
        dist = 1 - jaccard_df.values
        fig = ff.create_dendrogram(
            X=np.zeros((len(jaccard_df), 1)),
            labels=list(jaccard_df.index),
            distfun=lambda x: squareform(dist),
            linkagefun=lambda d: linkage(d, "average"),
        )
        fig.update_layout(yaxis_title="Distance (1 - Jaccard)")
        return _layout(fig, "Hierarchical clustering of input roots (average linkage)", h=360)
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"(Dendrogram needs scipy: {e})",
                           xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False)
        return _layout(fig, "Dendrogram")



def chart_cond_prob_reverse_heatmap(cp_df):
    """REVERSE direction: small multiples — one bar chart per \"given B\" root,
    showing P(A|B) for every other input root A. Read cell cp_df.loc[B, A]
    which is P(A|B) by definition."""
    if cp_df.empty:
        return _layout(go.Figure(), "P(A|B)")
    rows = []
    for b in cp_df.columns:
        for a in cp_df.index:
            if a == b:
                continue
            try:
                v = float(cp_df.loc[b, a])  # P(A|B)
            except Exception:
                continue
            if pd.notna(v):
                rows.append({"Given B": str(b), "Then A": str(a), "P(A|B)": v})
    if not rows:
        return _layout(go.Figure(), "P(A|B)")
    long = pd.DataFrame(rows).sort_values(
        ["Given B", "P(A|B)"], ascending=[True, True])
    n = long["Given B"].nunique()
    n_cols = min(3, n)
    n_rows_grid = (n + n_cols - 1) // n_cols
    fig = px.bar(long, x="P(A|B)", y="Then A", orientation="h",
                 facet_col="Given B", facet_col_wrap=n_cols,
                 color="P(A|B)", color_continuous_scale="Tealrose",
                 text="P(A|B)")
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig.update_yaxes(matches=None, showticklabels=True)
    max_v = long["P(A|B)"].max() if not long.empty else 1.0
    fig.update_xaxes(range=[0, max(max_v * 1.15, 0.05)])
    fig.for_each_annotation(lambda a: a.update(text="Given: " + a.text.split("=")[-1]))
    fig.update_layout(showlegend=False, coloraxis_showscale=False)
    return _layout(fig,
                   "REVERSE — given B, how often does A also appear?",
                   h=max(320, 220 * n_rows_grid))


def chart_metric_cross_reference(pmi_df, jaccard_df, input_roots):
    """Scatter of input-root PAIRS plotted on PMI (x) and Jaccard (y), with
    quadrant lines and labels.  Each dot is one pair, labeled.

    Quadrants tell the user immediately:
      top-right: \"Strongly associated AND frequently together\"
      top-left:  \"Often co-occur but no surprise (large common roots)\"
      bot-right: \"Hidden gems — strong association, rare overlap\"
      bot-left:  \"Weak association, rare overlap\"
    """
    if (pmi_df is None or jaccard_df is None or pmi_df.empty or jaccard_df.empty
            or len(input_roots) < 2):
        fig = go.Figure()
        fig.add_annotation(text="(need at least 2 input roots)",
                           xref="paper", yref="paper", x=0.5, y=0.5,
                           showarrow=False, font=dict(size=14))
        return _layout(fig, "Metric cross-reference")

    pairs = []
    for i in range(len(input_roots)):
        for j in range(i + 1, len(input_roots)):
            a, b = input_roots[i], input_roots[j]
            try:
                p = float(pmi_df.loc[a, b])
                jc = float(jaccard_df.loc[a, b])
            except Exception:
                continue
            if pd.notna(p) and pd.notna(jc):
                pairs.append({"Pair": f"{a} ↔ {b}", "PMI": p, "Jaccard": jc})
    if not pairs:
        return _layout(go.Figure(), "Metric cross-reference")
    df = pd.DataFrame(pairs)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["PMI"], y=df["Jaccard"], mode="markers+text",
        text=df["Pair"], textposition="top center",
        textfont=dict(size=12, color="#1B263B"),
        marker=dict(
            size=18,
            color=df["PMI"],
            colorscale="RdBu_r",
            cmid=0,
            line=dict(width=2, color="#1B263B"),
            showscale=True,
            colorbar=dict(title="PMI", thickness=12, len=0.6),
        ),
        hovertemplate=("<b>%{text}</b><br>PMI: %{x:.3f}<br>"
                       "Jaccard: %{y:.3f}<extra></extra>"),
    ))

    # Quadrant guide lines
    x_mid = 0.0
    y_mid = float(df["Jaccard"].median())
    x_min, x_max = df["PMI"].min() - 0.5, df["PMI"].max() + 0.5
    y_min, y_max = 0, max(df["Jaccard"].max() * 1.2, 0.05)
    fig.add_vline(x=x_mid, line_dash="dot", line_color="gray")
    fig.add_hline(y=y_mid, line_dash="dot", line_color="gray")

    # Quadrant labels
    fig.add_annotation(x=x_max, y=y_max, xanchor="right", yanchor="top",
                       text="<b>Strong &amp; frequent</b><br><span style=\"font-size:10px;color:#6B7280;\">"
                            "associated above chance AND share many ayahs</span>",
                       showarrow=False, font=dict(size=11, color=PAL["good"]),
                       bgcolor="rgba(6,167,125,0.10)", borderpad=4)
    fig.add_annotation(x=x_min, y=y_max, xanchor="left", yanchor="top",
                       text="<b>Frequent but no surprise</b><br><span style=\"font-size:10px;color:#6B7280;\">"
                            "common roots — high overlap, low PMI</span>",
                       showarrow=False, font=dict(size=11, color=PAL["accent"]),
                       bgcolor="rgba(247,127,0,0.10)", borderpad=4)
    fig.add_annotation(x=x_max, y=y_min, xanchor="right", yanchor="bottom",
                       text="<b>💎 Hidden gems</b><br><span style=\"font-size:10px;color:#6B7280;\">"
                            "rare pair but VERY associated — worth a closer look</span>",
                       showarrow=False, font=dict(size=11, color=PAL["violet"]),
                       bgcolor="rgba(114,9,183,0.10)", borderpad=4)
    fig.add_annotation(x=x_min, y=y_min, xanchor="left", yanchor="bottom",
                       text="<b>Weak &amp; rare</b><br><span style=\"font-size:10px;color:#6B7280;\">"
                            "no real signal</span>",
                       showarrow=False, font=dict(size=11, color="#6B7280"),
                       bgcolor="rgba(107,114,128,0.08)", borderpad=4)

    fig.update_xaxes(title="PMI (bits) — positive = above chance",
                     range=[x_min, x_max])
    fig.update_yaxes(title="Jaccard — fraction of shared / union ayahs",
                     range=[y_min, y_max])
    return _layout(fig,
                   "Metric cross-reference — PMI vs Jaccard for every pair",
                   h=520)

