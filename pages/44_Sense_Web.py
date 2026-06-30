"""Close-up · Sense-resolved web (2-D / 3-D, focusable, with community metrics). Polysemous roots split into two
senses, each joining a different concept-community. Communities are labelled by their measured hub-concept; select
one (or more) to light it up while the rest grey out; full centrality/metric tables below. MEASURED on rasm
(PPMI co-occurrence + per-occurrence context 2-means).

When a SINGLE family is lit OR a word is focused, the view switches to an INDEPENDENT subnetwork: the induced
subgraph is re-laid on its own (seeded), so its internal bonds stay intact and nothing dangles. Bonds to the rest
of the web are NOT severed silently — bridge nodes are gold-ringed and labelled with a "→k" outward-bond count."""
import os, json, collections
import numpy as np
import networkx as nx
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Sense-resolved web", page_icon="\U0001f578", layout="wide")
if S:
    try: S.log_page("sense_web")
    except Exception: pass
    for fn in ("inject_css", "render_grouped_nav"):
        try: getattr(S, fn)()
        except Exception: pass
C.inject()

_D = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "sense_web_data.json"), encoding="utf-8"))
_N = _D["nodes"]; _E = _D["edges"]; _SL = _D["sense_links"]; _CM = _D["communities"]; _M = _D["meta"]; _PAL = _M["palette"]
_GREY = "#D7DEE8"

C.hero("Sense-resolved web — the Qur’ān’s concept families, with two-meaning words un-blurred",
       "Concepts that recur together form a web, not a list. Here it is measured, split by sense, and made "
       "navigable: rotate it in 3-D, light up a concept-family, and read its full metrics below.",
       "USABILITY", "—", "rasm (PPMI co-occurrence + per-occurrence context)", "sense-resolved concept web · 2-D / 3-D")

C.story("The Qur’ān interprets itself — «القرآن يفسّر بعضه بعضاً». Concepts that keep company across verses form "
        "<b>families</b> (communities); a few concepts act as <b>bridges</b> between families. Our other maps blur a "
        "word with two meanings into a single dot — but measured across every occurrence, <b>34 of the 40</b> most "
        "ambiguous roots have their two senses land in <b>different families</b>. Here each appears as two sense-nodes "
        "(·a / ·b) joined by a faint <b>fold</b> line, so you watch one word stretch across two regions of meaning.",
        "Each <b>colour + legend name</b> is a family, labelled by its measured hub-concept. <b>Light up one family</b> "
        "(or <b>focus a word</b>) to open it as an <b>independent subnetwork</b> — re-laid on its own so no bond is cut; "
        "bridge nodes show a <b>→k</b> count of their bonds to other families. Read the <b>centrality tables</b> below.")

with st.expander("Conceptual foundation — why a web, why senses, what the metrics mean (read me)"):
    C.para("<b>Why a web, not a list.</b> The Qur’ān explains itself: a term left ambiguous in one verse is fixed by "
           "another. So the right object is not a glossary but a <b>network</b> — <b>nodes</b> are root-concepts, and an "
           "<b>edge</b> joins two concepts that appear in the same verses far above chance (measured by <b>PPMI</b>, "
           "which controls for how common each word is, so ubiquitous words don’t link to everything).")
    C.para("<b>Why communities.</b> Densely interlinked concepts form <b>families</b> — the Qur’ān’s natural themes. We "
           "do not impose them; we <b>measure</b> them (modularity). Each family here is named by its <b>hub-concept</b> "
           "(the most central node), so the legend reads as meaning, not as «community 1, 2 …».")
    C.para("<b>What the metrics mean.</b> <b>Degree</b> = how many concepts a word directly co-occurs with (raw "
           "connectedness). <b>Betweenness</b> = how often a concept lies on the shortest path between others — a "
           "<b>bridge</b> that ties families together. <b>PageRank / eigenvector</b> = <b>hub influence</b> (central to "
           "its family, linked to other well-linked concepts). <b>Clustering</b> = how tightly a word’s neighbours "
           "interlink. <b>Density</b> = how cohesive a whole family is.")
    C.para("<b>Independent subnetwork view.</b> When you light a single family or focus a word, we extract its "
           "<b>induced subgraph</b> and give it a <b>fresh layout</b>, so the family reads as a self-contained object "
           "with every internal bond intact. Its links to the rest of the web are <b>not deleted</b> — each bridge "
           "node is gold-ringed and tagged <b>→k</b> (k bonds leaving the subnetwork), so you still see that the "
           "family connects outward. The centrality tables keep the <b>global</b> numbers (a node’s true role in the "
           "whole web); a separate column adds its <b>within-subnetwork</b> degree.")
    C.para("<b>Honest limit.</b> This <b>refines and navigates known structure</b>; it is a reading aid, not a new "
           "discovery. Senses are a continuum (two is a floor); the split and the families are measured on the rasm "
           "surface and are approximate. 3-D is for exploring; 2-D is better for precise reading.")

C.kpis([
    ("34/40", "two-sense words split", "polysemous roots whose senses fall in different families", C.TEAL),
    (str(_M["nNodes"]), "concepts shown", "sense-nodes + their strongest partners", None),
    (str(_M["nComm"]), "families", "measured concept-communities (modularity)", None),
    (str(_M["nSenseLinks"]), "fold links", "each joins a word’s two senses (·a — ·b)", C.CORAL),
    ("صلو · بصر · كثر", "exemplar splits", "prayer · sight · abundance — each two families", C.TEAL),
    ("PPMI", "edge measure", "frequency-controlled co-occurrence on the rasm", C.SLATE),
])

# ── CONTROLS ─────────────────────────────────────────────────────────────────
C.section("The web — light up a family, rotate, or read it flat")
_bases = sorted({n["label"].replace("·a", "").replace("·b", "") for n in _N if n["sense"]})
_clabels = {c["id"]: "%s  (n=%d)" % (c["label"], c["n"]) for c in _CM}
_allids = [c["id"] for c in _CM]
if "csel" not in st.session_state:
    st.session_state["csel"] = []
_fc = st.columns([2, 2, 2])
with _fc[0]:
    _focus = st.selectbox("Focus a word (independent ego-network)", ["(whole web)"] + _bases)
with _fc[1]:
    _minv = st.slider("Min verses per node", 0, 80, 0, 5)
with _fc[2]:
    _mode = st.radio("View", ["3-D (rotate)", "2-D (read)"], horizontal=True)
_qb = st.columns([1.3, 1.3, 5])
if _qb[0].button("✨ Light all"):
    st.session_state["csel"] = list(_allids)
if _qb[1].button("Clear (overview)"):
    st.session_state["csel"] = []
with _qb[2]:
    _csel = st.multiselect("Light up family / families — pick ONE to open it as an independent subnetwork",
                           _allids, format_func=lambda c: _clabels[c], key="csel")
_is3d = _mode.startswith("3")

_adj = collections.defaultdict(set)
for i, j in _E:
    _adj[i].add(j); _adj[j].add(i)

# focus ego-net (seed word + its neighbours)
keep = set(range(len(_N)))
if _focus != "(whole web)":
    seed = {n["id"] for n in _N if n["label"].replace("·a", "").replace("·b", "") == _focus}
    nb = set(seed)
    for s in seed:
        nb |= _adj[s]
    keep = nb
if _minv > 0:
    keep = {i for i in keep if _N[i]["df"] >= _minv or _N[i]["sense"]}
if not keep:
    keep = set(range(len(_N)))


@st.cache_data(show_spinner=False)
def _sub_layout(ids_tuple, edge_tuple, dim):
    """Fresh, SEEDED layout for an induced subgraph → independent coordinates (reproducible)."""
    ids = list(ids_tuple); idset = set(ids)
    G = nx.Graph(); G.add_nodes_from(ids)
    for i, j in edge_tuple:
        if i in idset and j in idset:
            G.add_edge(i, j)
    p = nx.spring_layout(G, dim=dim, seed=42, iterations=200)
    a = np.array([p[i] for i in ids], dtype=float)
    if dim == 3:
        a = (a - a.mean(0)) / (a.std(0) + 1e-9)
        a = a / (np.linalg.norm(a, axis=1, keepdims=True) + 1e-9)   # unit sphere → real depth
    else:
        a = a - a.mean(0); a = a / (np.abs(a).max() + 1e-9)         # centre, fit [-1,1]
    return {i: a[k].tolist() for k, i in enumerate(ids)}


# INDEPENDENT subnetwork when exactly one family is lit OR a word is focused
independent = (_focus != "(whole web)") or (len(_csel) == 1)
outward = {}
if independent:
    if _focus != "(whole web)":
        subids = set(keep)
        _subtitle = "focused word «%s» + its partners" % _focus
    else:
        cid = _csel[0]
        subids = {i for i in range(len(_N)) if _N[i]["comm"] == cid}
        if _minv > 0:
            subids = {i for i in subids if _N[i]["df"] >= _minv or _N[i]["sense"]}
        _subtitle = "family «%s»" % _clabels[cid].split("  (")[0]
    if len(subids) < 2:
        subids |= {j for i in subids for j in _adj[i]}
    keep = set(subids)
    _pos = _sub_layout(tuple(sorted(subids)), tuple(map(tuple, _E)), 3 if _is3d else 2)
    PX = {i: _pos[i][0] for i in subids}
    PY = {i: _pos[i][1] for i in subids}
    PZ = {i: (_pos[i][2] if _is3d else 0.0) for i in subids}
    outward = {i: len([j for j in _adj[i] if j not in subids]) for i in subids}
    internal_deg = {i: len([j for j in _adj[i] if j in subids]) for i in subids}
else:
    rng = range(len(_N))
    PX = {i: (_N[i]["x3"] if _is3d else _N[i]["x2"]) for i in rng}
    PY = {i: (_N[i]["y3"] if _is3d else _N[i]["y2"]) for i in rng}
    PZ = {i: _N[i]["z3"] for i in rng}

def _active(i): return (not _csel) or (_N[i]["comm"] in _csel)
# labels: independent view labels everything (it's small); else split-senses + top hubs
if independent:
    _LABEL = set(keep)
else:
    _topdeg = sorted(keep, key=lambda i: -_N[i]["deg"])[:30]
    _LABEL = {i for i in keep if _N[i]["sense"]} | set(_topdeg)


# ── FIGURE ───────────────────────────────────────────────────────────────────
def _nodes(ids, color, ring, ringcol, showtext, name, leg, sizebase, labels=None):
    xs = [PX[i] for i in ids]; ys = [PY[i] for i in ids]
    sz = [sizebase + 9 * (min(_N[i]["df"], 300) / 300) ** 0.5 for i in ids]
    if labels is not None:
        txt = labels
    else:
        txt = [_N[i]["label"] if (showtext or i in _LABEL) else "" for i in ids]
    hov = ["%s · %d verses · deg %d · betw %.3f%s" % (
        _N[i]["label"], _N[i]["df"], _N[i]["deg"], _N[i]["bet"],
        ("  ·  →%d bonds out" % outward[i]) if outward.get(i, 0) > 0 else "") for i in ids]
    mk = dict(size=sz, color=color, line=dict(width=ring, color=ringcol))
    if _is3d:
        zs = [PZ[i] for i in ids]
        return go.Scatter3d(x=xs, y=ys, z=zs, mode="markers+text", marker=mk, text=txt, textposition="top center",
                            textfont=dict(size=12, color="#10243A"), hovertext=hov, hoverinfo="text", name=name, showlegend=leg)
    return go.Scatter(x=xs, y=ys, mode="markers+text", marker=mk, text=txt, textposition="top center",
                      textfont=dict(size=12, color="#10243A"), hovertext=hov, hoverinfo="text", name=name, showlegend=leg)
def _line(pairs, color, width, op, name, leg):
    xs, ys, zs = [], [], []
    for i, j in pairs:
        if i in keep and j in keep:
            xs += [PX[i], PX[j], None]; ys += [PY[i], PY[j], None]
            zs += [PZ[i], PZ[j], None] if _is3d else [None, None, None]
    if _is3d:
        return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color=color, width=width), opacity=op, hoverinfo="none", name=name, showlegend=leg)
    return go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width), opacity=op, hoverinfo="none", name=name, showlegend=leg)

fig = go.Figure()
sb = 5 if _is3d else 9
if independent:
    # all internal bonds — intact, nothing dangling
    intern = [(i, j) for i, j in _E if i in keep and j in keep]
    fig.add_trace(_line(intern, "#4E6E92", 1.5, 0.6, "internal bonds", False))
    foldin = [(i, j) for i, j in _SL if i in keep and j in keep]
    if foldin:
        fig.add_trace(_line(foldin, "#E63946", 2.5, 0.6, "sense fold (·a–·b)", True))
    # nodes: split bridge (gold ring + →k) vs interior; coloured by their own family
    for isbridge, ring, rc, nm in [(True, 2.8, "#CC8A3C", "bridge → other families"), (False, 0.6, "#FFFFFF", None)]:
        gids = [i for i in keep if (outward.get(i, 0) > 0) == isbridge]
        if not gids:
            continue
        cols = [_PAL[_N[i]["comm"] % len(_PAL)] for i in gids]
        labs = [_N[i]["label"] + ((" →%d" % outward[i]) if isbridge else "") for i in gids]
        fig.add_trace(_nodes(gids, cols, ring, rc, True, nm or "", bool(nm), sb + 1, labels=labs))
else:
    # whole-web (or multi-family) view: lit families vs context
    if _csel:
        foc = [(i, j) for i, j in _E if _N[i]["comm"] in _csel and _N[j]["comm"] in _csel]
        ctx = [(i, j) for i, j in _E if not (_N[i]["comm"] in _csel and _N[j]["comm"] in _csel)]
        fig.add_trace(_line(ctx, _GREY, 1.0, 0.30, "other bonds", False))
        fig.add_trace(_line(foc, "#4E6E92", 1.6, 0.7, "family bonds", False))
    else:
        fig.add_trace(_line(_E, _GREY, 1.2, 0.5, "bonds", False))
    for c in _CM:
        cid = c["id"]
        ids = [i for i in keep if _N[i]["comm"] == cid and not _N[i]["sense"]]
        if ids:
            col = c["color"] if _active(ids[0]) else _GREY
            fig.add_trace(_nodes(ids, col, 0.5, "#FFFFFF", False, _clabels[cid], True, sb))
    for active, ring, rc, nm in [(True, 2.2, "#CC8A3C", "split senses"), (False, 1.0, _GREY, None)]:
        ids = [i for i in keep if _N[i]["sense"] and _active(i) == active]
        if ids:
            col = [_PAL[_N[i]["comm"] % len(_PAL)] if _active(i) else _GREY for i in ids]
            fig.add_trace(_nodes(ids, col, ring, rc, active, nm or "", bool(nm), sb + 1))

if _is3d:
    fig.update_layout(height=650, margin=dict(l=0, r=0, t=8, b=0), paper_bgcolor="#FFFFFF", uirevision="keep",
        legend=dict(font=dict(size=12), itemsizing="constant"),
        scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor="#FFFFFF"))
else:
    _axv = [PX[i] for i in keep]; _ayv = [PY[i] for i in keep]
    _lo = min(min(_axv), min(_ayv)); _hi = max(max(_axv), max(_ayv)); _pd = 0.08 * (_hi - _lo + 1e-9)
    fig.update_layout(height=630, margin=dict(l=6, r=6, t=8, b=6), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                      dragmode="pan", uirevision="keep", legend=dict(font=dict(size=12), itemsizing="constant"))
    fig.update_xaxes(visible=False, range=[_lo - _pd, _hi + _pd], autorange=False)
    fig.update_yaxes(visible=False, range=[_lo - _pd, _hi + _pd], autorange=False)

if independent:
    st.caption("Independent subnetwork — %s — re-laid on its own; every internal bond is intact. "
               "Gold-ringed nodes are bridges; «→k» = bonds leaving this subnetwork. "
               "Pick the whole web (Clear + no focus) to see all families together." % _subtitle)

st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False,
    "displayModeBar": True, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
C.note("<b>Navigate:</b> in <b>2-D</b> drag to pan and use the toolbar (top-right) to zoom or reset; in <b>3-D</b> "
       "drag to rotate, scroll to zoom. <b>Light one family</b> or <b>focus a word</b> to open it as an independent "
       "subnetwork (re-laid, bonds intact, bridges tagged <b>→k</b>); pick several families to compare them in place. "
       "Coral <b>fold</b> lines join a word’s two senses; gold rings mark split-senses / bridges. Hover for metrics.")

# ── METRIC TABLES ────────────────────────────────────────────────────────────
C.section("Family metrics — the numbers behind the picture")
cdf = pd.DataFrame([{
    "family (hub-concept)": c["label"], "concepts": c["n"], "avg degree": c["avg_deg"],
    "avg betweenness": c["avg_bet"], "density": c["density"], "internal bonds": c["intra"],
    "bridge bonds": c["inter"], "top members": " · ".join(c["members"][:6])} for c in _CM])
st.markdown("<style>[data-testid='stDataFrame'],[data-testid='stDataFrameResizable']{width:100% !important;max-width:100% !important}</style>", unsafe_allow_html=True)
st.dataframe(cdf, width="stretch", hide_index=True, height=460)

_scope = ("subnetwork: " + _subtitle) if independent else ("selected families" if _csel else "all concepts")
C.section("Concept metrics — full centralities (%s)" % _scope)
if independent:
    sel = [n for n in _N if n["id"] in keep]
else:
    sel = [n for n in _N if (not _csel or n["comm"] in _csel)]
def _row(n):
    r = {"concept": n["label"], "type": "split-sense" if n["sense"] else "root", "verses": n["df"],
         "degree (global)": n["deg"], "betweenness (global)": n["bet"], "pagerank": n["pr"],
         "eigenvector": n["eig"], "clustering": n["clu"], "family": _clabels[n["comm"]].split("  (")[0]}
    if independent:
        r["within-subnet degree"] = internal_deg.get(n["id"], 0)
        r["→ outward bonds"] = outward.get(n["id"], 0)
    return r
ndf = pd.DataFrame([_row(n) for n in sel])
ndf = ndf.sort_values(["family", "pagerank"], ascending=[True, False])
st.dataframe(ndf, width="stretch", hide_index=True, height=420)
C.note("Degree/betweenness shown are <b>global</b> (the concept’s role in the whole web). In the subnetwork view, "
       "<b>within-subnet degree</b> and <b>→ outward bonds</b> are added so you can tell interior concepts from "
       "bridges. PageRank/eigenvector = hub influence · Clustering = how tightly its neighbours interlink.")

# ── MEANING LANDSCAPE (3-D family mountain-range — explainable) ───────────────
import math as _ma
C.section("Meaning landscape — the concept-families as a mountain range")
with st.expander("What this is and how to read it — open me first", expanded=True):
    C.para("<b>The idea.</b> Everything above is a flat web. Here the SAME measured families become <b>terrain</b>: "
           "each <b>hill is one concept-family</b>, labelled by its hub-concept; the <b>height</b> is a measured "
           "quantity you pick (size · internal density · hub-influence). The low ground between hills is where "
           "families meet.")
    C.para("<b>How to read it.</b> Tall hill = a big/central family; low hill = a minor one; the <b>dots packed on a "
           "hill-top</b> are that family’s own concepts (bigger dot = more verses). <b>Drag</b> to rotate, "
           "<b>scroll</b> to zoom. To study one family up close, use <b>“Zoom to one family”</b> — it segments out "
           "that single hill with every concept named. The table below gives the exact numbers.")
    C.para("<b>What ·a and ·b mean.</b> A two-meaning word appears as <b>two</b> dots — <b>·a</b> and <b>·b</b>, one "
           "per sense — and (the key finding) they sit on <b>different hills</b>, because each sense keeps different "
           "company. A <b>coral line</b> joins the two senses, so you can watch one word stretch across two families "
           "(e.g. <b>صلو·a</b> inner prayer vs <b>صلو·b</b> the prayer–almsgiving institution).")
    C.para("<b>The lines (relations).</b> The terrain stays clean by default. Pick a word under <b>Trace a two-meaning "
           "word</b> to light <b>one</b> coral ·a–·b link (its two senses); <b>zoom one family</b> to see that family’s "
           "internal bonds. Bonds here are above-chance links (PPMI-thresholded) and <b>unweighted in this map — "
           "uniform width, no thickness</b>; the web at the top of the page is the full relational view.")
    C.para("<b>Honest reading (the one law).</b> <b>Height and dot-sizes are MEASURED</b>; the left–right "
           "<b>placement is for legibility only</b> and means nothing — read the elevation, not the compass "
           "direction. A reading aid, not a discovery.")
_hub = {c["id"]: _clabels[c["id"]].split("  (")[0] for c in _CM}
_foldof = {}
for _i, _j in _SL:
    _foldof[_N[_i]["label"].replace("·a", "").replace("·b", "")] = (_i, _j)
_lc = st.columns([2, 2, 2])
with _lc[0]:
    _hsrc = st.radio("Hill height =", ["concepts in the family", "internal density", "hub-influence (PageRank)"],
                     horizontal=True, key="land_h")
with _lc[1]:
    _zoom = st.selectbox("Zoom to one family (segment) — or see all",
                         ["All families"] + [_hub[c["id"]] for c in sorted(_CM, key=lambda c: -c["n"])], key="land_zoom")
with _lc[2]:
    _trace = st.selectbox("Trace a two-meaning word (·a–·b link)", ["(none)"] + sorted(_foldof), key="land_trace")
_MEXPL = {
    "concepts in the family": "<b>how many distinct concepts</b> the family holds — its <b>breadth</b>. A tall hill is a wide-ranging theme (many ideas travel together); a low hill is a small, focused family.",
    "internal density": "<b>how tightly its concepts interlink</b> (share of the possible bonds that are present) — its <b>cohesion</b>. A tall hill is a tight-knit theme where almost everything connects; a low hill is loose.",
    "hub-influence (PageRank)": "<b>the family’s total hub-influence</b> across the whole web (summed PageRank of its concepts) — its <b>centrality</b>. A tall hill is a theme the rest of the Qur’ān leans on; a low hill sits at the periphery.",
}
C.note("<b>Hill height = %s</b> — %s" % (_hsrc, _MEXPL[_hsrc]))
def _cval(c):
    if _hsrc.startswith("internal"): return float(c["density"]) * 10.0
    if _hsrc.startswith("hub"): return float(sum(n["pr"] for n in _N if n["comm"] == c["id"]))
    return float(c["n"])
_order = sorted(_CM, key=lambda c: -_cval(c))
_zoomed = _zoom != "All families"
_show = [c for c in _CM if _hub[c["id"]] == _zoom] if _zoomed else _order
_cx = {}; _cy = {}; _ch = {}
if _zoomed:
    c = _show[0]; _cx[c["id"]] = 0.0; _cy[c["id"]] = 0.0
    _ch[c["id"]] = 0.4 + 0.6 * (_cval(c) / (max(_cval(x) for x in _CM) or 1.0))   # dome height tracks the chosen metric
    _sig = 1.35; _ext = 2.8; _nrad = 1.0
else:
    _R = 4.0; _sig = 0.72; _ext = _R + 1.4; _nrad = 0.34
    for _i, c in enumerate(_show):
        _ang = 2 * _ma.pi * _i / max(len(_show), 1)
        _cx[c["id"]] = _R * _ma.cos(_ang); _cy[c["id"]] = _R * _ma.sin(_ang); _ch[c["id"]] = _cval(c)
    _hmax = max(_ch.values()) or 1.0
    for _k in _ch: _ch[_k] = _ch[_k] / _hmax
_gx = np.linspace(-_ext, _ext, 120); _gy = np.linspace(-_ext, _ext, 120)
_GXX, _GYY = np.meshgrid(_gx, _gy)
_Z = np.zeros_like(_GXX)
for _cid in _ch:
    _Z += _ch[_cid] * np.exp(-(((_GXX - _cx[_cid]) ** 2 + (_GYY - _cy[_cid]) ** 2) / (2 * _sig ** 2)))
def _zat(px, py):
    return float(sum(_ch[c] * _ma.exp(-(((px - _cx[c]) ** 2 + (py - _cy[c]) ** 2) / (2 * _sig ** 2))) for c in _ch))
_CS = [[0.0, "#F5FBF8"], [0.4, "#D2ECE0"], [0.72, "#8FCDB0"], [1.0, "#2BA37D"]]
_surf = go.Figure(go.Surface(x=_gx, y=_gy, z=_Z, colorscale=_CS, showscale=False, opacity=0.8, hoverinfo="skip",
                             contours=dict(z=dict(show=True, color="#CFE4DC", width=1, project_z=True))))
def _pack(cx, cy, k, rad):
    out = []
    for _t in range(k):
        _rr = rad * ((_t + 0.5) / max(k, 1)) ** 0.5; _aa = _t * 2.399963229
        out.append((cx + _rr * _ma.cos(_aa), cy + _rr * _ma.sin(_aa)))
    return out
_NPOS = {}                                   # node-id -> (x, y, z) so we can draw the relations
for c in _show:
    _cid = c["id"]; _mem = [n for n in _N if n["comm"] == _cid]
    if not _mem:
        continue
    _pts = _pack(_cx[_cid], _cy[_cid], len(_mem), _nrad)
    _xx = [p[0] for p in _pts]; _yy = [p[1] for p in _pts]; _zz = [_zat(p[0], p[1]) + 0.02 for p in _pts]
    for _n2, _p2, _z2 in zip(_mem, _pts, _zz):
        _NPOS[_n2["id"]] = (_p2[0], _p2[1], _z2)
    _sz = [4 + 6 * (min(n["df"], 300) / 300) ** 0.5 for n in _mem]
    _hv = ["%s · %d verses" % (n["label"], n["df"]) for n in _mem]
    _md = "markers+text" if _zoomed else "markers"
    _surf.add_trace(go.Scatter3d(x=_xx, y=_yy, z=_zz, mode=_md,
        marker=dict(size=_sz, color=_PAL[_cid % len(_PAL)], line=dict(width=0.5, color="#FFFFFF")),
        text=[n["label"] for n in _mem], textposition="top center", textfont=dict(size=12, color="#10243A"),
        hovertext=_hv, hoverinfo="text", showlegend=False))
# RELATIONS (bonds). Edges are above-chance bonds (unweighted in this map → uniform width, no thickness).
def _eline(pairs, col, w, op):
    _ex = []; _ey = []; _ez = []
    for _ii, _jj in pairs:
        if _ii in _NPOS and _jj in _NPOS:
            _ex += [_NPOS[_ii][0], _NPOS[_jj][0], None]; _ey += [_NPOS[_ii][1], _NPOS[_jj][1], None]
            _ez += [_NPOS[_ii][2], _NPOS[_jj][2], None]
    if _ex:
        _surf.add_trace(go.Scatter3d(x=_ex, y=_ey, z=_ez, mode="lines",
            line=dict(color=col, width=w), opacity=op, hoverinfo="none", showlegend=False))
if _zoomed:                                  # one family: show its internal bonds (uncluttered)
    _eline([(i, j) for i, j in _E], "#6E86A6", 1.6, 0.4)
if (not _zoomed) and _trace != "(none)" and _trace in _foldof:   # ONE word's ·a–·b link, on demand (no spaghetti)
    _ti, _tj = _foldof[_trace]
    _eline([(_ti, _tj)], "#E63946", 4.0, 0.95)
    if _ti in _NPOS and _tj in _NPOS:        # highlight & label its two sense-dots
        _surf.add_trace(go.Scatter3d(x=[_NPOS[_ti][0], _NPOS[_tj][0]], y=[_NPOS[_ti][1], _NPOS[_tj][1]],
            z=[_NPOS[_ti][2] + 0.05, _NPOS[_tj][2] + 0.05], mode="markers+text",
            text=[_N[_ti]["label"], _N[_tj]["label"]], textposition="top center",
            textfont=dict(size=13, color="#E63946"),
            marker=dict(size=13, color="#E63946", line=dict(width=1.5, color="#FFFFFF")),
            hoverinfo="skip", showlegend=False))
if not _zoomed:
    _surf.add_trace(go.Scatter3d(x=[_cx[c["id"]] for c in _show], y=[_cy[c["id"]] for c in _show],
        z=[_ch[c["id"]] + 0.1 for c in _show], mode="text", text=[_hub[c["id"]] for c in _show],
        textfont=dict(size=13, color="#10243A"), hoverinfo="none", showlegend=False))
_surf.update_layout(height=640, margin=dict(l=0, r=0, t=8, b=0), paper_bgcolor="#FFFFFF", uirevision="land",
    scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False),
               zaxis=dict(title="height = " + _hsrc, color="#10243A", gridcolor="#E2E8F1"), bgcolor="#FFFFFF",
               aspectmode="manual", aspectratio=dict(x=1, y=1, z=0.5), camera=dict(eye=dict(x=1.5, y=1.5, z=0.9))))
st.plotly_chart(_surf, use_container_width=True, config={"scrollZoom": True, "displaylogo": False})
C.note("Showing <b>%s</b> alone, with its internal bonds — every concept labelled." % _zoom if _zoomed else
       "Hover a dot for its concept and verse-count; use <b>Trace a two-meaning word</b> to light a single ·a–·b link.")
_peakdf = pd.DataFrame([{
    "family (hub-concept)": _hub[c["id"]], "concepts": c["n"], "avg degree": c["avg_deg"],
    "density": c["density"], "internal bonds": c["intra"], "bridge bonds (saddles out)": c["inter"]}
    for c in _order])
st.dataframe(_peakdf, width="stretch", hide_index=True, height=300)
C.note("The terrain is just this table made visual: the taller a family’s hill, the larger its value in the chosen "
       "column. <b>Bridge bonds</b> are the links leaving a family — the saddles between the hills.")

# ── WHAT IT SHOWS ────────────────────────────────────────────────────────────
C.section("What it shows — measured sense splits")
C.para("Each split recovers a real distinction we find elsewhere, which is the validation: <b>صلو</b> "
       "(prayer) → inner devotion (قنت·خشع·قوم) vs the prayer–almsgiving institution "
       "(زكو·بيع·ركع); <b>بصر</b> (sight) → true seeing vs <b>sealed-blindness</b> "
       "(ختم·عمي·زيغ) — the same field as the heart-anatomy; <b>كثر</b> (abundance) → "
       "worldly spoils vs fruit-abundance — the very كوثر split. The method reproduces meaning "
       "we derived independently, which is why we trust the map.")
C.callout("Takeaway",
          "A word like صلو or بصر is not one point on the map — it is two, in two "
          "families. Light up a family or focus a word to open it as its own intact subnetwork, rotate it, and read "
          "its metrics: the Qur’ān’s concept structure becomes something you can navigate.", accent=C.TEAL)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="\U0001f50e")
# independent-subnetwork mode + bridge badges — verified 2026-06-29
