"""Shared theme-ranking chart — concept-families compared on a chosen measured metric.

Replaces the earlier 3-D "mountain range" (which dressed a single number per family as terrain with a meaningless
left-right axis) with a clean, sortable HORIZONTAL BAR CHART:

  • whole view  — one bar per family, length = the chosen family metric (breadth / weight / cohesion), ranked.
  • zoomed view — one family's CONCEPTS as bars, length = each concept's size (verse-count / frequency).

Used by the Sense-web (pages/44) and the Concept Atlas (pages/39) so both stay identical and DRY.

family_landscape(families, nodes, *, height_label, zoom_hub, trace, edges) -> go.Figure
  families : [{"id", "hub": str, "members": [node_key, ...], "hval": float, "color": "#hex"}]
  nodes    : {node_key: {"label": str, "full": str, "size": float, "hover": str (optional)}}
  height_label : what the family metric is (x-axis + title text)
  zoom_hub : a family hub string to show its concepts instead of the all-family ranking (or None)
  trace, edges : accepted for call-compatibility; not used by the bar chart.
"""
import plotly.graph_objects as go

_INK = "#10243A"


def family_landscape(families, nodes, *, height_label="value", zoom_hub=None, trace=None, edges=None):
    fams = [f for f in families if f.get("members")]
    if not fams:
        return go.Figure()
    zoomed = zoom_hub is not None and any(f["hub"] == zoom_hub for f in fams)

    if zoomed:
        f = [x for x in fams if x["hub"] == zoom_hub][0]
        mem = [m for m in f["members"] if m in nodes]
        mem = sorted(mem, key=lambda m: nodes[m].get("size", 0))[-30:]          # top 30 by size, ascending
        ys = [nodes[m]["label"] for m in mem]                                   # plain word; ·a/·b only in the hover
        xs = [nodes[m].get("size", 0) for m in mem]
        hov = [nodes[m].get("hover", nodes[m]["label"]) for m in mem]
        fig = go.Figure(go.Bar(x=xs, y=ys, orientation="h", marker_color=f.get("color", "#1D9E75"),
                               text=[str(int(v)) for v in xs], textposition="outside", cliponaxis=False,
                               hovertext=hov, hoverinfo="text"))
        fig.update_layout(title=dict(text="<b>%s — its concepts, by size</b>" % f["hub"], x=0.5, font=dict(size=14, color=_INK)),
                          height=max(300, 24 * len(mem) + 90), margin=dict(l=6, r=44, t=42, b=6),
                          paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC", font=dict(size=13, color=_INK), showlegend=False)
        fig.update_xaxes(title=dict(text="size = verses the concept appears in", font=dict(size=12, color=_INK)), gridcolor="#E4ECF3")
        fig.update_yaxes(tickfont=dict(size=13, color=_INK))
        return fig

    order = sorted(fams, key=lambda f: f["hval"])                               # ascending → biggest on top
    ys = [f["hub"] for f in order]
    xs = [f["hval"] for f in order]
    cols = [f.get("color", "#1D9E75") for f in order]
    txt = [("%.2f" % v if v < 10 else "%d" % round(v)) for v in xs]
    hov = ["%s · %d concepts" % (f["hub"], len(f["members"])) for f in order]
    fig = go.Figure(go.Bar(x=xs, y=ys, orientation="h", marker_color=cols,
                           text=txt, textposition="outside", cliponaxis=False, hovertext=hov, hoverinfo="text"))
    fig.update_layout(title=dict(text="<b>Families ranked by %s</b>" % height_label, x=0.5, font=dict(size=14, color=_INK)),
                      height=max(320, 26 * len(order) + 90), margin=dict(l=6, r=48, t=42, b=6),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC", font=dict(size=13, color=_INK), showlegend=False)
    fig.update_xaxes(title=dict(text=height_label, font=dict(size=12, color=_INK)), gridcolor="#E4ECF3")
    fig.update_yaxes(tickfont=dict(size=13, color=_INK))
    return fig


def html_table(headers, rows, *, num_cols=None, wide_col=None):
    """A full-width HTML table that fixes the 'stretched columns / empty space' look of st.dataframe:
    column HEADERS wrap to multiple lines (so they don't force wide columns), numeric columns stay tight and
    right-aligned, and one long-text column (wide_col) absorbs the slack so the table fills the row with no gaps.
    headers: list of titles · rows: list of row-lists (already-stringified) · num_cols: indices to right-align ·
    wide_col: index of the text column that should expand. Returns an HTML string for st.markdown."""
    num = set(num_cols or [])
    n = len(headers)
    nnum = sum(1 for i in range(n) if i in num)
    has_wide = wide_col is not None
    # Deterministic fixed layout via <colgroup>: the wide text column takes a fixed big share,
    # label columns a medium share, numeric columns split the rest evenly. No width:99% hack
    # (that fought width:100% and caused horizontal overflow + very tall rows). table-layout:fixed
    # keeps columns honest; numeric cells are nowrap+tight, the text column wraps within its share.
    wide_w, label_w = (30.0, 11.0) if has_wide else (0.0, 16.0)
    nlabel = n - nnum - (1 if has_wide else 0)
    rest = max(0.0, 100.0 - wide_w - label_w * nlabel)
    each_num = (rest / nnum) if nnum else 0.0
    widths = []
    for i in range(n):
        if has_wide and i == wide_col:
            widths.append(wide_w)
        elif i in num:
            widths.append(each_num)
        else:
            widths.append(label_w)
    colg = "<colgroup>" + "".join("<col style='width:%.2f%%'>" % w for w in widths) + "</colgroup>"
    _th = "padding:6px 9px;border:1px solid #CFE0F2;background:#EAF2FB;font-weight:800;line-height:1.2;white-space:normal;vertical-align:bottom"
    out = ["<table style='border-collapse:collapse;width:100%;table-layout:fixed;font-size:13px;color:#10243A'>",
           colg, "<tr>"]
    for i, h in enumerate(headers):
        out.append("<th style='%s;text-align:%s'>%s</th>" % (_th, ("right" if i in num else "left"), h))
    out.append("</tr>")
    for r in rows:
        out.append("<tr>")
        for i, c in enumerate(r):
            al = "right" if i in num else "left"
            nw = "white-space:nowrap;" if i in num else "word-break:break-word;"
            out.append("<td style='padding:5px 9px;border:1px solid #E2E8F1;vertical-align:top;line-height:1.35;%stext-align:%s'>%s</td>"
                       % (nw, al, c))
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)
