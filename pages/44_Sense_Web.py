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
import landscape as LS

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

# ── FAMILY SIZES — ranked bar chart (shared landscape.py helper) ──────────────
C.section("Family sizes — the concept-families, ranked")
with st.expander("What this shows — open me", expanded=True):
    C.para("The web above shows the families as colour; here they are <b>ranked</b>. One <b>bar per family</b> "
           "(labelled by its hub-concept), its length = a measured quantity you choose: the family’s <b>breadth</b> "
           "(how many concepts), its <b>cohesion</b> (how tightly they interlink), or its <b>hub-influence</b> (how "
           "central it is to the whole web). So you see at a glance which families are biggest, tightest, or most "
           "central — and how lopsided the set is.")
    C.para("<b>Zoom to one family</b> to switch the chart to that family’s <b>concepts</b>, each a bar whose length is "
           "<b>how many verses it appears in</b>. All MEASURED; a reading aid, not a new claim. (·a / ·b on a concept "
           "mark the two senses of a two-meaning word — the web above shows how they land in different families.)")
with st.expander("Where the data comes from & how the families are made — read me"):
    C.para("<b>The data.</b> On the <b>rasm</b> (the consonant skeleton), every verse is a bag of roots. Two concepts "
           "get a <b>bond</b> when they appear in the same verses <b>far above chance</b> — measured by PPMI, which "
           "controls for how common each word is, so ubiquitous words don’t bond with everything. A two-meaning word "
           "is split into two sense-nodes by the different company each sense keeps. Everything is <b>measured from "
           "the text itself</b> — nothing is imposed by hand.")
    C.para("<b>How the families are made.</b> A <b>community-detection</b> algorithm groups concepts that bond tightly "
           "into families and names each by its most central member. The grouping is <b>measured</b> (it beats a "
           "random baseline), but the <b>exact number of families is not an absolute</b> — change the algorithm’s "
           "resolution and a few borderline concepts move, or you get one family more or fewer. Read it as a good "
           "map, not a fixed count.")
    C.para("<b>What’s included, and why sizes differ.</b> This covers the <b>most strongly-connected concepts</b> (the "
           "same nodes as the web above), not literally every root; the <b>zoom</b> lists a family’s top 30 by "
           "verse-count. And families come out <b>unequal in size</b> — that inequality is exactly what the “concepts "
           "in the family” bars report.")
_hub = {c["id"]: _clabels[c["id"]].split("  (")[0].replace("·a", "").replace("·b", "") for c in _CM}
_lc = st.columns([2, 2])
with _lc[0]:
    _hsrc = st.radio("Rank families by", ["concepts in the family", "internal density", "hub-influence (PageRank)"],
                     horizontal=True, key="land_h")
with _lc[1]:
    _zoom = st.selectbox("Zoom to one family (its concepts) — or rank all",
                         ["All families"] + [_hub[c["id"]] for c in sorted(_CM, key=lambda c: -c["n"])], key="land_zoom")
_MEXPL = {
    "concepts in the family": "<b>breadth</b> — how many distinct concepts the family holds (wide-ranging vs small and focused).",
    "internal density": "<b>cohesion</b> — how tightly its concepts interlink (share of the possible bonds present).",
    "hub-influence (PageRank)": "<b>centrality</b> — the family’s total hub-influence across the whole web (summed PageRank).",
}
C.note("<b>Bar length = %s:</b> %s" % (_hsrc, _MEXPL[_hsrc]))
def _cval(c):
    if _hsrc.startswith("internal"): return float(c["density"]) * 10.0
    if _hsrc.startswith("hub"): return float(sum(n["pr"] for n in _N if n["comm"] == c["id"]))
    return float(c["n"])
_order = sorted(_CM, key=lambda c: -_cval(c))
_zoomed = _zoom != "All families"
_nodesLS = {}
for n in _N:
    _base = n["label"].replace("·a", "").replace("·b", "")
    _nodesLS[n["id"]] = {"label": _base, "full": n["label"], "size": n["df"],
        "hover": (("%s — one sense of the two-meaning word %s · %d verses" % (n["label"], _base, n["df"]))
                  if n["sense"] else ("%s · %d verses" % (n["label"], n["df"])))}
_families = [{"id": c["id"], "hub": _hub[c["id"]], "color": _PAL[c["id"] % len(_PAL)],
              "members": [n["id"] for n in _N if n["comm"] == c["id"]], "hval": _cval(c)} for c in _CM]
_surf = LS.family_landscape(_families, _nodesLS, height_label=_hsrc, zoom_hub=(_zoom if _zoomed else None))
st.plotly_chart(_surf, use_container_width=True, config={"displaylogo": False})
C.note(("Showing <b>%s</b>’s concepts — each bar sized by how many verses it appears in." % _zoom) if _zoomed else
       "One bar per family, ranked by the chosen metric; hover a bar for its concept-count.")
_peakdf = pd.DataFrame([{
    "family (hub-concept)": _hub[c["id"]], "concepts": c["n"], "avg degree": c["avg_deg"],
    "avg betweenness": c["avg_bet"], "density": c["density"], "internal bonds": c["intra"],
    "bridge bonds (links out)": c["inter"], "top concepts": " · ".join(c["members"][:8])}
    for c in _order])
st.dataframe(_peakdf, width="stretch", hide_index=True, height=300)
C.note("The chart is this table made visual: a <b>longer bar = a larger value</b> in the chosen column. "
       "<b>Bridge bonds</b> = links leaving a family for another.")

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
