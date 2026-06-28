"""Close-up · Concept connectome — al-Kawthar's words + the inner self.
ONE grounded connectome (edges = distinctive PPMI association with >=3 shared verses; width = strength; hover =
the verse-count grounding). Three LAYOUTS of that same connectome (meaning / form / rarity placement): switching
the layout re-lays the WHOLE graph (nodes AND edges move together). Edges are MEASURED on the rasm; PPMI is
frequency-controlled so the network does NOT 'relate everything'. Pan/scroll to zoom. HUMAN-CONSTRUCT tagged."""
import os, json
import streamlit as st
import plotly.graph_objects as go

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Concept connectome", page_icon="\U0001f9ed", layout="wide")
if S:
    try: S.log_page("closeup_concept_rearrange")
    except Exception: pass
    for fn in ("inject_css", "render_grouped_nav"):
        try: getattr(S, fn)()
        except Exception: pass
C.inject()

_DATA = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "concept_rearrange_data.json"), encoding="utf-8"))
_N = _DATA["nodes"]; _BONDS = _DATA.get("bonds", []); _R = _DATA["corr_form_meaning"]

C.hero("Concept connectome — al-Kawthar's words + the inner self",
       "One measured network of distinctive associations (PPMI, ≥3 shared verses), re-laid under three layouts. "
       "Switching the layout moves the whole graph — nodes and edges together; the relationships are constant. "
       "Computation localizes known meaning for reading — it is not a claim about the text's order.",
       "USABILITY", "—", "rasm (Book6 PPMI, frequency-controlled)", "layout-tagged: meaning vs HUMAN CONSTRUCT")

_LAY = {"Meaning placement": ("meaning", "nodes placed by co-occurrence proximity (divine substrate)", "#EAF2FB", "#1D3557"),
        "Form placement": ("form", "nodes placed by spelling / edit-distance — HUMAN CONSTRUCT", "#FBF1E6", "#8a5a16"),
        "Rarity placement": ("rarity", "nodes placed by corpus frequency (rare → common)", "#EFF6F2", "#0F6E56")}
st.caption("Pick a layout — the connectome (edges) is constant; only node placement changes:")
_pick = st.radio("Layout", list(_LAY), horizontal=True, label_visibility="collapsed")
_key, _badge, _bg, _bc = _LAY[_pick]
st.markdown(f"<div style='display:inline-block;background:{_bg};color:{_bc};border:1px solid {_bc}33;"
            f"border-radius:6px;padding:3px 10px;font-size:12px;font-weight:700;margin:2px 0 6px'>{_badge}</div>",
            unsafe_allow_html=True)

fig = go.Figure()
# edges by PPMI tier (width = strength)
_tiers = [(2.5, 3.4, 0.6, "#0F6E56"), (1.3, 2.1, 0.42, "#1D9E75"), (0.0, 1.0, 0.28, "#A9CFC0")]
for lo, w, op, col in _tiers:
    hi = 99 if lo == 2.5 else (2.5 if lo == 1.3 else 1.3)
    xs = []; ys = []
    for i, j, ppmi, co in _BONDS:
        if lo <= ppmi < hi:
            a = _N[i]["pos"][_key]; b = _N[j]["pos"][_key]
            xs += [a[0], b[0], None]; ys += [a[1], b[1], None]
    if xs:
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=w), opacity=op,
                                 hoverinfo="none", showlegend=False))
# edge-grounding hover at midpoints
_mx = []; _my = []; _mh = []
for i, j, ppmi, co in _BONDS:
    a = _N[i]["pos"][_key]; b = _N[j]["pos"][_key]
    _mx.append((a[0] + b[0]) / 2); _my.append((a[1] + b[1]) / 2)
    _mh.append("%s — %s · %d shared verses · PPMI %+.1f" % (_N[i]["label"], _N[j]["label"], co, ppmi))
fig.add_trace(go.Scatter(x=_mx, y=_my, mode="markers", marker=dict(size=11, color="rgba(0,0,0,0)"),
                         hovertext=_mh, hoverinfo="text", showlegend=False))
# nodes: ONE markers+text trace -> nodes, labels and edges all re-lay together on layout switch
_dfmax = max(n["df"] for n in _N) or 1
fig.add_trace(go.Scatter(
    x=[n["pos"][_key][0] for n in _N], y=[n["pos"][_key][1] for n in _N], mode="markers+text",
    marker=dict(size=[15 + 11 * (n["df"] / _dfmax) ** 0.5 for n in _N], color=[n["color"] for n in _N],
                line=dict(width=1.5, color="#ffffff")),
    text=[n["label"] for n in _N], textposition="top center", textfont=dict(size=13, color="#10243A"),
    hovertext=["%s · %d verses" % (n["label"], n["df"]) for n in _N], hoverinfo="text", showlegend=False))
fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", margin=dict(l=6, r=6, t=8, b=6), height=560, dragmode="pan")
fig.update_xaxes(visible=False, range=[-0.12, 1.12])
fig.update_yaxes(visible=False, range=[-0.12, 1.12], scaleanchor="x", scaleratio=1)
st.plotly_chart(fig, use_container_width=True,
                config={"scrollZoom": True, "displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})

C.note("<b>The connectome (constant in every layout):</b> an edge = a <b>distinctive</b> association (PPMI, "
       "frequency-controlled) with <b>≥3 shared verses</b>; line thickness = strength; hover an edge for its verse-count. "
       "Because it is PPMI, not raw co-occurrence, it does <i>not</i> 'relate everything'. "
       "<b>Switch layout</b> to re-lay the whole graph: <i>Meaning</i> = co-occurrence proximity (divine substrate); "
       "<i>Form</i> = spelling ring [HUMAN CONSTRUCT]; <i>Rarity</i> = frequency. Node placement r(form,meaning) = %.2f — "
       "near 0, so spelling tells you nothing about meaning. <i>Scroll to zoom into any cluster.</i>" % _R)

C.section("Strongest grounded bonds — built-in interpretation")
_rows = [["%s — %s" % (_N[i]["label"], _N[j]["label"]), "%+.1f" % p, str(co)] for i, j, p, co in _BONDS[:12]]
C.table(["bond (concept — concept)", "PPMI strength", "shared verses"], _rows)

C.section("How the Qur'ān interprets a concept")
_byid = {nd["label"]: nd for nd in _N}
_sel = st.selectbox("Concept", [nd["label"] for nd in _N], label_visibility="collapsed")
_nd = _byid[_sel]
if _nd["interp"]:
    _ir = [[x["r"], ("+" if x["ppmi"] >= 0 else "") + str(x["ppmi"]), "%.2f" % x["P"], str(x["co"])] for x in _nd["interp"]]
    C.table(["interpreter (root)", "PPMI", "P (reliability)", "co-verses"], _ir)
    C.note("Nearest by meaning: " + " · ".join("%s (%.2f)" % (s, w) for s, w in _nd["sem"]) + ".")
else:
    C.note("<b>%s</b> is a hapax — defined by its semantic field, not by co-occurrence." % _sel)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="\U0001f50e")
