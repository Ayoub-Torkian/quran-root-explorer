"""Shared 3-D 'meaning landscape' — concept-families as a labelled mountain-range.

Each family is a HILL whose HEIGHT is a measured per-family value the caller supplies; a family's concepts are
packed as dots on its hill-top (dot size = a measured per-node value). The left-right PLACEMENT of hills is for
legibility only and carries no measured meaning — read the elevation, not the compass direction.

Used by the Sense-web (pages/44) and the Concept Atlas (pages/39) so both landscapes stay identical and DRY.

family_landscape(families, nodes, *, height_label, zoom_hub, trace, edges) -> go.Figure
  families : list of {"id", "hub": str, "members": [node_key, ...], "hval": float, "color": "#hex"}
  nodes    : {node_key: {"label": str (shown on dot), "full": str (hover/trace label), "size": float,
                          "hover": str (optional full hover text)}}
  height_label : axis/caption text for what the height encodes
  zoom_hub : a family hub string to isolate as a single broad hill (or None for the whole range)
  trace    : (node_key_a, node_key_b) to draw ONE highlighted link in the all-families view (or None)
  edges    : list of (node_key_a, node_key_b) internal bonds, drawn only in the zoomed single-family view
"""
import math as _ma
import numpy as np
import plotly.graph_objects as go

_CS = [[0.0, "#F5FBF8"], [0.4, "#D2ECE0"], [0.72, "#8FCDB0"], [1.0, "#2BA37D"]]


def _pack(cx, cy, k, rad):
    """Sunflower packing — tight, deterministic dots clustered on a hill-top."""
    out = []
    for t in range(k):
        rr = rad * ((t + 0.5) / max(k, 1)) ** 0.5
        aa = t * 2.399963229
        out.append((cx + rr * _ma.cos(aa), cy + rr * _ma.sin(aa)))
    return out


def family_landscape(families, nodes, *, height_label="value", zoom_hub=None, trace=None, edges=None):
    fams = [f for f in families if f.get("members")]
    if not fams:
        return go.Figure()
    zoomed = zoom_hub is not None and any(f["hub"] == zoom_hub for f in fams)
    show = [f for f in fams if f["hub"] == zoom_hub] if zoomed else sorted(fams, key=lambda f: -f["hval"])
    allmax = max((f["hval"] for f in fams), default=1.0) or 1.0

    cx = {}; cy = {}; ch = {}
    if zoomed:
        f = show[0]; cx[f["id"]] = 0.0; cy[f["id"]] = 0.0
        ch[f["id"]] = 0.4 + 0.6 * (f["hval"] / allmax)          # dome height still tracks the chosen metric
        sig = 1.35; ext = 2.8; nrad = 1.0
    else:
        R = 4.0; sig = 0.72; ext = R + 1.4; nrad = 0.34
        for i, f in enumerate(show):
            a = 2 * _ma.pi * i / max(len(show), 1)
            cx[f["id"]] = R * _ma.cos(a); cy[f["id"]] = R * _ma.sin(a); ch[f["id"]] = f["hval"]
        hmax = max(ch.values()) or 1.0
        for k in ch:
            ch[k] = ch[k] / hmax

    gx = np.linspace(-ext, ext, 120); gy = np.linspace(-ext, ext, 120)
    GX, GY = np.meshgrid(gx, gy)
    Z = np.zeros_like(GX)
    for cid in ch:
        Z += ch[cid] * np.exp(-(((GX - cx[cid]) ** 2 + (GY - cy[cid]) ** 2) / (2 * sig ** 2)))

    def zat(px, py):
        return float(sum(ch[c] * _ma.exp(-(((px - cx[c]) ** 2 + (py - cy[c]) ** 2) / (2 * sig ** 2))) for c in ch))

    fig = go.Figure(go.Surface(x=gx, y=gy, z=Z, colorscale=_CS, showscale=False, opacity=0.8, hoverinfo="skip",
                               contours=dict(z=dict(show=True, color="#CFE4DC", width=1, project_z=True))))

    npos = {}
    for f in show:
        mem = [m for m in f["members"] if m in nodes]
        if not mem:
            continue
        pts = _pack(cx[f["id"]], cy[f["id"]], len(mem), nrad)
        zz = [zat(p[0], p[1]) + 0.02 for p in pts]
        for k, p, z in zip(mem, pts, zz):
            npos[k] = (p[0], p[1], z)
        sz = [4 + 6 * (min(nodes[m].get("size", 1), 300) / 300) ** 0.5 for m in mem]
        md = "markers+text" if zoomed else "markers"
        fig.add_trace(go.Scatter3d(
            x=[p[0] for p in pts], y=[p[1] for p in pts], z=zz, mode=md,
            marker=dict(size=sz, color=f.get("color", "#1D9E75"), line=dict(width=0.7, color="#FFFFFF")),
            text=["<b>%s</b>" % nodes[m]["label"] for m in mem], textposition="top center",
            textfont=dict(size=13, color="#0B2A1E"),
            hovertext=[nodes[m].get("hover", nodes[m]["label"]) for m in mem], hoverinfo="text", showlegend=False))

    if zoomed and edges:                                        # internal bonds, only in the focused single hill
        ex = []; ey = []; ez = []
        for a, b in edges:
            if a in npos and b in npos:
                ex += [npos[a][0], npos[b][0], None]; ey += [npos[a][1], npos[b][1], None]; ez += [npos[a][2], npos[b][2], None]
        if ex:
            fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines", line=dict(color="#6E86A6", width=1.6),
                                       opacity=0.4, hoverinfo="none", showlegend=False))

    if (not zoomed) and trace and trace[0] in npos and trace[1] in npos:   # one highlighted link, on demand
        a, b = trace
        fig.add_trace(go.Scatter3d(x=[npos[a][0], npos[b][0], None], y=[npos[a][1], npos[b][1], None],
                                   z=[npos[a][2], npos[b][2], None], mode="lines",
                                   line=dict(color="#E63946", width=4), opacity=0.95, hoverinfo="none", showlegend=False))
        fig.add_trace(go.Scatter3d(x=[npos[a][0], npos[b][0]], y=[npos[a][1], npos[b][1]],
                                   z=[npos[a][2] + 0.05, npos[b][2] + 0.05], mode="markers+text",
                                   text=["<b>%s</b>" % nodes[a].get("full", nodes[a]["label"]), "<b>%s</b>" % nodes[b].get("full", nodes[b]["label"])],
                                   textposition="top center", textfont=dict(size=14, color="#C1121F"),
                                   marker=dict(size=13, color="#E63946", line=dict(width=1.5, color="#FFFFFF")),
                                   hoverinfo="skip", showlegend=False))

    if not zoomed:                                              # label each hill with its family hub
        fig.add_trace(go.Scatter3d(x=[cx[f["id"]] for f in show], y=[cy[f["id"]] for f in show],
                                   z=[ch[f["id"]] + 0.12 for f in show], mode="text",
                                   text=["<b>%s</b>" % f["hub"] for f in show],
                                   textfont=dict(size=15, color="#14304F"), hoverinfo="none", showlegend=False))

    fig.update_layout(height=640, margin=dict(l=0, r=0, t=8, b=0), paper_bgcolor="#FFFFFF", uirevision="land",
                      scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False),
                                 zaxis=dict(title="height = " + height_label, color="#10243A", gridcolor="#E2E8F1"),
                                 bgcolor="#FFFFFF", aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.5),
                                 camera=dict(eye=dict(x=1.5, y=1.5, z=0.9))))
    return fig
