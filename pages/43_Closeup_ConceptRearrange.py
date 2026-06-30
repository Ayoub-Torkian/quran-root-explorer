"""Close-up · al-Kawthar's word-web — the surah's seven content-words + what interprets each.
EGO-network: the 7 surah roots (gold) and the roots the Qur'ān distinctively uses with them (navy), bonds =
PPMI ≥0.6 with ≥2 shared verses; width = strength; hover = verse-count. Distinct from the corpus-wide Concept
Atlas (39) and the inner-self page (42). MEASURED on rasm. The two hapax (نحر/أبتر) come out isolated.

2-D (three precomputed layouts) OR 3-D (rotatable, seeded spring). Focus one surah word to open it as an
INDEPENDENT subnetwork — its ego-net re-laid on its own so every internal bond is intact; interpreters that also
bond outside it are gold-ringed and tagged «→k» (k = bonds leaving the subnetwork)."""
import os, json, math, collections
import numpy as np
import networkx as nx
import streamlit as st
import plotly.graph_objects as go

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · al-Kawthar word-web", page_icon="\U0001f9ed", layout="wide")
if S:
    try: S.log_page("closeup_kawthar_wordweb")
    except Exception: pass
    for fn in ("inject_css", "render_grouped_nav"):
        try: getattr(S, fn)()
        except Exception: pass
C.inject()

_DATA = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "concept_rearrange_data.json"), encoding="utf-8"))
_N = _DATA["nodes"]; _BONDS = _DATA.get("bonds", []); _R = _DATA["corr_form_meaning"]
_ANCH = set(_DATA.get("anchors", []))

# index helpers (bonds reference list indices, not node ids)
_idx_by_label = {n["label"]: k for k, n in enumerate(_N)}
_anch_labels = [n["label"] for n in _N if n["id"] in _ANCH]
_adj = collections.defaultdict(set)
for i, j, ppmi, co in _BONDS:
    _adj[i].add(j); _adj[j].add(i)
_edges_t = tuple((i, j) for i, j, ppmi, co in _BONDS)


@st.cache_data(show_spinner=False)
def _spring(ids_tuple, edges_tuple, dim):
    """Fresh SEEDED layout for an induced subgraph / the whole graph → independent, reproducible coordinates."""
    ids = list(ids_tuple); idset = set(ids)
    G = nx.Graph(); G.add_nodes_from(ids)
    for i, j in edges_tuple:
        if i in idset and j in idset:
            G.add_edge(i, j)
    p = nx.spring_layout(G, dim=dim, seed=42, iterations=250)
    a = np.array([p[i] for i in ids], dtype=float)
    if dim == 3:
        a = (a - a.mean(0)) / (a.std(0) + 1e-9)
        a = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-9)   # unit sphere → real depth
    else:
        a = a - a.mean(0); a = a / (np.abs(a).max() + 1e-9)         # centre, fit [-1,1]
    return {i: a[k].tolist() for k, i in enumerate(ids)}


C.hero("al-Kawthar's word-web — the surah's seven words and what interprets each",
       "al-Kawthar has seven content-words; two are used nowhere else. Read across the whole corpus, what does the "
       "Qur'ān put with each of them — and where do the rare ones land? This is the surah's own vocabulary, wired.",
       "USABILITY", "—", "rasm (Book6 PPMI, frequency-controlled)", "al-Kawthar ego-network · 2-D / 3-D · subnetwork")
C.story("The <b>seven gold nodes</b> are al-Kawthar's content-words — give · abundance (كوثر) · pray · Lord · "
        "sacrifice · hater · cut-off (أبتر). Around them sit the <b>roots the Qur'ān distinctively uses with each</b> "
        "(navy). An edge means the pair shares verses far above chance — so each surah word resolves into a measured "
        "<i>neighbourhood of meaning</i> instead of standing alone.",
        "Read it flat in three layouts, <b>rotate it in 3-D</b>, or <b>focus one surah word</b> to open its own "
        "<b>independent subnetwork</b> — re-laid so no bond is cut, with bridge interpreters tagged <b>→k</b>. The two "
        "hapax (نحر · أبتر) land where the surah says they do: alone.")
C.kpis([
    ("7", "surah words", "al-Kawthar's content roots: give·abundance·pray·Lord·sacrifice·hater·cut-off", "#CC8A3C"),
    ("22", "interpreters", "roots the Qur'ān distinctively uses with the surah's words", None),
    ("80", "grounded bonds", "PPMI ≥0.6 with ≥2 shared verses", C.TEAL),
    ("صلو–زکو", "tightest pair", "pray–zakāt: 28 shared verses, PPMI +5.1", C.TEAL),
    ("نحر · أبتر", "isolated", "the two hapax — no distinctive partner (cut off)", C.CORAL),
    ("0.03", "form↔meaning r", "spelling predicts ~nothing about meaning", C.SLATE),
])

# ── HOW TO READ ──
C.callout("How to read this web",
          "<b>Gold node</b> = one of al-Kawthar's seven words; <b>navy node</b> = a root the Qur'ān distinctively "
          "uses with it. Node size = how many verses the root appears in. <b>Edge</b> = a distinctive association "
          "(PPMI, ≥2 shared verses) — <b>thickness = strength</b>; <b>hover</b> for the verse-count. A surah word "
          "with <b>no edge</b> (نحر, أبتر) is a hapax with no distinctive partner — <i>cut off</i>, structurally. "
          "<b>Focus a word</b> to open its own subnetwork; open it in the panel below to read the exact interpreters.", accent=C.TEAL)
C.callout("Method — and why it doesn't 'relate everything'",
          "On the <b>rasm</b>, each verse is a bag of roots. For a surah word and a candidate we count shared verses "
          "and compute <b>PPMI</b> = log₂(P(a,b) ⁄ P(a)·P(b)) — frequency-controlled, so ubiquitous words don't link "
          "to everything. A bond needs <b>PPMI ≥ 0.6 and ≥2 shared verses</b> (the surah's words are rare, so the "
          "floor is 2; read each with its verse-count). Layouts: <i>Meaning</i> = MDS on co-occurrence; <i>Form</i> = "
          "a spelling ring [HUMAN CONSTRUCT]; <i>Rarity</i> = a frequency grid; <i>3-D</i> = a seeded force layout.", accent=C.SLATE)

# ── THE WEB ──
C.section("The word-web — flat layouts, a 3-D rotation, or one word's own subnetwork")
_LAY = {"Meaning placement": ("meaning", "nodes placed by co-occurrence proximity (divine substrate)", "#EAF2FB", "#1D3557"),
        "Form placement": ("form", "nodes placed by spelling / edit-distance — HUMAN CONSTRUCT", "#FBF1E6", "#8a5a16"),
        "Rarity placement": ("rarity", "nodes placed by corpus frequency (rare → common)", "#EFF6F2", "#0F6E56")}
_cc = st.columns([2, 2, 2])
with _cc[0]:
    _focus = st.selectbox("Focus a surah word (independent subnetwork)", ["(whole web)"] + _anch_labels)
with _cc[1]:
    _view = st.radio("View", ["3-D (rotate)", "2-D (read)"], horizontal=True)
with _cc[2]:
    _pick = st.radio("2-D layout (whole web)", list(_LAY), horizontal=True)
_key, _badge, _bg, _bc = _LAY[_pick]
_is3d = _view.startswith("3")
_focused = _focus != "(whole web)"

# positions + which nodes to keep
outward = {}
if _focused:
    _a = _idx_by_label[_focus]
    keep = {_a} | set(_adj[_a])
    if len(keep) < 2:                       # a hapax — show it alone, honestly isolated
        keep = {_a}
    _pos = _spring(tuple(sorted(keep)), _edges_t, 3 if _is3d else 2)
    outward = {i: len([j for j in _adj[i] if j not in keep]) for i in keep}
    PX = {i: _pos[i][0] for i in keep}; PY = {i: _pos[i][1] for i in keep}; PZ = {i: (_pos[i][2] if _is3d else 0.0) for i in keep}
elif _is3d:
    keep = set(range(len(_N)))
    _pos = _spring(tuple(range(len(_N))), _edges_t, 3)
    PX = {i: _pos[i][0] for i in keep}; PY = {i: _pos[i][1] for i in keep}; PZ = {i: _pos[i][2] for i in keep}
else:
    keep = set(range(len(_N)))
    PX = {i: _N[i]["pos"][_key][0] for i in keep}; PY = {i: _N[i]["pos"][_key][1] for i in keep}; PZ = {i: 0.0 for i in keep}

if (not _is3d) and (not _focused):
    st.markdown(f"<div style='display:inline-block;background:{_bg};color:{_bc};border:1px solid {_bc}33;"
                f"border-radius:6px;padding:3px 10px;font-size:12px;font-weight:700;margin:2px 0 6px'>{_badge}</div>",
                unsafe_allow_html=True)

fig = go.Figure()
_tiers = [(2.5, 3.4, 0.6, "#0F6E56"), (1.3, 2.1, 0.42, "#1D9E75"), (0.0, 1.0, 0.28, "#A9CFC0")]
for lo, w, op, col in _tiers:
    hi = 99 if lo == 2.5 else (2.5 if lo == 1.3 else 1.3)
    xs = []; ys = []; zs = []
    for i, j, ppmi, co in _BONDS:
        if i in keep and j in keep and lo <= ppmi < hi:
            xs += [PX[i], PX[j], None]; ys += [PY[i], PY[j], None]; zs += [PZ[i], PZ[j], None]
    if xs:
        if _is3d:
            fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color=col, width=w), opacity=op, hoverinfo="none", showlegend=False))
        else:
            fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=w), opacity=op, hoverinfo="none", showlegend=False))
if not _is3d:   # edge-hover midpoints (2-D only; keeps 3-D light)
    _mx = []; _my = []; _mh = []
    for i, j, ppmi, co in _BONDS:
        if i in keep and j in keep:
            _mx.append((PX[i] + PX[j]) / 2); _my.append((PY[i] + PY[j]) / 2)
            _mh.append("%s — %s · %d shared verses · PPMI %+.1f" % (_N[i]["label"], _N[j]["label"], co, ppmi))
    if _mx:
        fig.add_trace(go.Scatter(x=_mx, y=_my, mode="markers", marker=dict(size=11, color="rgba(0,0,0,0)"), hovertext=_mh, hoverinfo="text", showlegend=False))

_dfmax = max(n["df"] for n in _N) or 1
def _nodetrace(ids, ring, ringcol, labels):
    sz = [15 + 11 * (_N[i]["df"] / _dfmax) ** 0.5 for i in ids]
    cols = [_N[i]["color"] for i in ids]
    hov = ["%s · %d verses%s%s" % (_N[i]["label"], _N[i]["df"],
           " · al-Kawthar word" if _N[i]["id"] in _ANCH else "",
           ("  ·  →%d bonds out" % outward[i]) if outward.get(i, 0) > 0 else "") for i in ids]
    mk = dict(size=sz, color=cols, line=dict(width=ring, color=ringcol))
    if _is3d:
        return go.Scatter3d(x=[PX[i] for i in ids], y=[PY[i] for i in ids], z=[PZ[i] for i in ids], mode="markers+text",
                            marker=mk, text=labels, textposition="top center", textfont=dict(size=13, color="#10243A"),
                            hovertext=hov, hoverinfo="text", showlegend=False)
    return go.Scatter(x=[PX[i] for i in ids], y=[PY[i] for i in ids], mode="markers+text",
                      marker=mk, text=labels, textposition="top center", textfont=dict(size=13, color="#10243A"),
                      hovertext=hov, hoverinfo="text", showlegend=False)
if _focused:
    for isbridge, ring, rc in [(True, 3.0, "#CC8A3C"), (False, 1.6, "#FFFFFF")]:
        ids = [i for i in keep if (outward.get(i, 0) > 0) == isbridge]
        if not ids:
            continue
        labs = [_N[i]["label"] + ((" →%d" % outward[i]) if isbridge else "") for i in ids]
        fig.add_trace(_nodetrace(ids, ring, rc, labs))
else:
    ids = list(range(len(_N)))
    fig.add_trace(_nodetrace(ids, 1.6, "#FFFFFF", [_N[i]["label"] for i in ids]))

if _is3d:
    fig.update_layout(paper_bgcolor="#FFFFFF", margin=dict(l=0, r=0, t=8, b=0), height=600, uirevision="keep",
        scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor="#FFFFFF"))
elif _focused:
    _v = [PX[i] for i in keep] + [PY[i] for i in keep]
    _lo = min(_v); _hi = max(_v); _pd = 0.14 * (_hi - _lo + 1e-9)
    fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", margin=dict(l=6, r=6, t=8, b=6), height=560, dragmode="pan", uirevision="keep")
    fig.update_xaxes(visible=False, range=[_lo - _pd, _hi + _pd], autorange=False)
    fig.update_yaxes(visible=False, range=[_lo - _pd, _hi + _pd], autorange=False)
else:
    fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", margin=dict(l=6, r=6, t=8, b=6), height=560, dragmode="pan", uirevision="keep")
    fig.update_xaxes(visible=False, range=[-0.12, 1.12])
    fig.update_yaxes(visible=False, range=[-0.12, 1.12], scaleanchor="x", scaleratio=1)

if _focused:
    st.caption("Independent subnetwork — «%s» + its interpreters — re-laid on its own; every internal bond is intact. "
               "Gold-ringed nodes are bridges; «→k» = bonds leaving this subnetwork." % _focus)

st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
C.note("Gold = al-Kawthar's seven words · navy = their interpreters. Edge thickness = PPMI strength; hover an edge for "
       "its verse-count. <b>3-D</b>: drag to rotate, scroll to zoom. <b>Focus a word</b> to open its own re-laid "
       "subnetwork (bonds intact, bridges tagged <b>→k</b>); 2-D whole-web switches layout to re-lay the graph.")

# ── WHAT IT SHOWS ──
C.section("What the web shows — each word's measured neighbourhood")
C.para("Each surah word resolves into a real neighbourhood: <b>عطو</b> (give) → رضو · جزی · ربب — the gift in a "
       "<i>reward-from-the-Lord</i> frame (the كوثر-gift toward «tarḍā», 93:5). <b>كوثر</b> sits among worldly-"
       "abundance roots — فیء · غنم (spoils), فکه (fruit) — the ordinary <i>kathra</i> the surah's unique كوثر "
       "transcends. <b>صلو</b> (pray) binds hardest to <b>زکو</b> (28 verses) — the standing prayer-almsgiving pair — "
       "with بیع · نفق · قوم (trade, spending, establishing). <b>ربب</b> (Lord) → عرش · حمد · علو (throne, praise, "
       "highness). <b>شنء</b> (the hater) sits in the justice frame جرم · وقی · ءمن (crime vs God-wariness and faith, "
       "5:8). And <b>نحر · أبتر are isolated</b> — the surah's two hapax have no distinctive partner, so the very "
       "severance the surah names shows up as a structural fact in the web.")
C.section("Strongest grounded bonds — by strength × support")
_tbl = sorted(_BONDS, key=lambda b: -(b[2] * math.log(1 + b[3])))
_rows = [["%s — %s" % (_N[i]["label"], _N[j]["label"]), "%+.1f" % p, str(co)] for i, j, p, co in _tbl[:12]]
C.table(["bond (word — root)", "PPMI strength", "shared verses"], _rows)

C.section("Open a surah word — what interprets it")
_byl = {n["label"]: n for n in _N}
_sel = st.selectbox("Surah word", _anch_labels, label_visibility="collapsed")
_nd = _byl[_sel]
if _nd["interp"]:
    _ir = [[x["r"], ("+" if x["ppmi"] >= 0 else "") + str(x["ppmi"]), "%.2f" % x["P"], str(x["co"])] for x in _nd["interp"]]
    C.table(["interpreter (root)", "PPMI", "P (reliability)", "co-verses"], _ir)
    C.note("PPMI = how distinctively the interpreter co-occurs; P = share of this word's verses it appears in.")
else:
    C.note("<b>%s</b> is a hapax — it occurs once, so it has no distinctive co-occurring partner; its meaning comes "
           "from its semantic field, and structurally it sits <i>cut off</i> from the web." % _sel)

# ── CAVEATS & TAKEAWAY ──
C.callout("Caveats — what this is and is not",
          "This <b>organises known meaning for reading</b>; not a new discovery. It is the <b>al-Kawthar ego-network</b> "
          "— distinct from the corpus-wide <i>Concept Atlas</i> and the <i>inner-self</i> page. Because the surah's words "
          "are rare, bonds use a <b>≥2-verse floor</b>, so some rest on two verses — always read an edge with its "
          "verse-count. Layouts (incl. 3-D) are reading aids, never a claim about the text's order; <i>Form</i>/<i>Rarity</i> are "
          "<b>[HUMAN CONSTRUCT]</b>.", accent=C.CORAL)
C.callout("Takeaway — in one line",
          "al-Kawthar's words are not isolated tokens: <b>صلو</b> is the prayer-almsgiving pair, <b>عطو</b> is the "
          "Lord's reward, <b>كوثر</b> outshines ordinary abundance — while <b>نحر</b> and <b>أبتر</b> sit alone. The "
          "surah's antithesis, abundance vs cut-off, is visible in the wiring itself.", accent=C.TEAL)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="\U0001f50e")
