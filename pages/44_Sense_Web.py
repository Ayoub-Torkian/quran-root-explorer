"""Close-up · Sense-resolved web (2-D / 3-D, focusable, with community metrics). Polysemous roots split into two
senses, each joining a different concept-community. Communities are labelled by their measured hub-concept; select
one (or more) to light it up while the rest grey out; full centrality/metric tables below. MEASURED on rasm
(PPMI co-occurrence + per-occurrence context 2-means)."""
import os, json, collections
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
        "Each <b>colour + legend name</b> is a family, labelled by its measured hub-concept. <b>Select a family</b> to "
        "light it up while the rest grey out; <b>rotate</b> in 3-D; and read the <b>centrality tables</b> below — so "
        "you can see not just the picture but the numbers behind every concept and family.")

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
    C.para("<b>Why sense-resolution, and its impact.</b> A word like <b>صلو</b> (prayer) means two things — inner "
           "devotion and the alms-ritual institution. Blurred, it sits as one misleading dot bridging both. "
           "<b>Resolved</b>, each sense joins its true family — and 34 of 40 such words split across families. The "
           "payoff for understanding: scattered cross-references become a <b>navigable map</b> where you can see the "
           "Qur’ān’s thematic families, the bridge-concepts that connect them, and exactly which words do two jobs.")
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
    _focus = st.selectbox("Focus a word (ego view)", ["(whole web)"] + _bases)
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
    _csel = st.multiselect("Light up family / families — pick any, or use the buttons",
                           _allids, format_func=lambda c: _clabels[c], key="csel")
_is3d = _mode.startswith("3")
_is3d = _mode.startswith("3")

_adj = collections.defaultdict(set)
for i, j in _E:
    _adj[i].add(j); _adj[j].add(i)
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
def _active(i): return (not _csel) or (_N[i]["comm"] in _csel)
# label the key concepts so the map is readable: all split-senses + the highest-degree hubs
_topdeg = sorted(keep, key=lambda i: -_N[i]["deg"])[:30]
_LABEL = {i for i in keep if _N[i]["sense"]} | set(_topdeg)

# ── FIGURE ───────────────────────────────────────────────────────────────────
def _nodes(ids, color, ring, ringcol, showtext, name, leg, sizebase):
    xs = [_N[i]["x3"] if _is3d else _N[i]["x2"] for i in ids]
    ys = [_N[i]["y3"] if _is3d else _N[i]["y2"] for i in ids]
    sz = [sizebase + 9 * (min(_N[i]["df"], 300) / 300) ** 0.5 for i in ids]
    txt = [_N[i]["label"] if (showtext or i in _LABEL) else "" for i in ids]
    hov = ["%s · %d verses · deg %d · betw %.3f" % (_N[i]["label"], _N[i]["df"], _N[i]["deg"], _N[i]["bet"]) for i in ids]
    mk = dict(size=sz, color=color, line=dict(width=ring, color=ringcol))
    if _is3d:
        zs = [_N[i]["z3"] for i in ids]
        return go.Scatter3d(x=xs, y=ys, z=zs, mode="markers+text", marker=mk, text=txt, textposition="top center",
                            textfont=dict(size=12, color="#10243A"), hovertext=hov, hoverinfo="text", name=name, showlegend=leg)
    return go.Scatter(x=xs, y=ys, mode="markers+text", marker=mk, text=txt, textposition="top center",
                      textfont=dict(size=12, color="#10243A"), hovertext=hov, hoverinfo="text", name=name, showlegend=leg)
def _line(pairs, color, width, op, name, leg):
    xs, ys, zs = [], [], []
    for i, j in pairs:
        if i in keep and j in keep:
            xs += [_N[i]["x3"] if _is3d else _N[i]["x2"], _N[j]["x3"] if _is3d else _N[j]["x2"], None]
            ys += [_N[i]["y3"] if _is3d else _N[i]["y2"], _N[j]["y3"] if _is3d else _N[j]["y2"], None]
            zs += [_N[i]["z3"], _N[j]["z3"], None] if _is3d else [None, None, None]
    if _is3d:
        return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color=color, width=width), opacity=op, hoverinfo="none", name=name, showlegend=leg)
    return go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width), opacity=op, hoverinfo="none", name=name, showlegend=leg)

fig = go.Figure()
# edges: focus (within lit families) vs context (rest)
if _csel:
    foc = [(i, j) for i, j in _E if _N[i]["comm"] in _csel and _N[j]["comm"] in _csel]
    ctx = [(i, j) for i, j in _E if not (_N[i]["comm"] in _csel and _N[j]["comm"] in _csel)]
    fig.add_trace(_line(ctx, _GREY, 1.0, 0.30, "other bonds", False))
    fig.add_trace(_line(foc, "#4E6E92", 1.6, 0.7, "family bonds", False))
else:
    fig.add_trace(_line(_E, _GREY, 1.2, 0.5, "bonds", False))
fig.add_trace(_line(_SL, "#E63946", 2.5, 0.55, "sense fold (·a–·b)", True))
sb = 5 if _is3d else 9
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
    _ax = [n["x2"] for n in _N]; _ay = [n["y2"] for n in _N]
    _lo = min(min(_ax), min(_ay)); _hi = max(max(_ax), max(_ay)); _pd = 0.06 * (_hi - _lo + 1e-9)
    fig.update_layout(height=630, margin=dict(l=6, r=6, t=8, b=6), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                      dragmode="pan", uirevision="keep", legend=dict(font=dict(size=12), itemsizing="constant"))
    fig.update_xaxes(visible=False, range=[_lo - _pd, _hi + _pd], autorange=False)
    fig.update_yaxes(visible=False, range=[_lo - _pd, _hi + _pd], autorange=False)
st.plotly_chart(fig, use_container_width=True, key="sense_web_net", config={"scrollZoom": _is3d, "displaylogo": False,
    "displayModeBar": True, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
C.note("<b>Navigate:</b> in <b>2-D</b> drag to pan up/down/sideways and the page scrolls normally over the graph; "
       "use the graph toolbar (top-right) to zoom or reset. In <b>3-D</b> drag to rotate, scroll to zoom. "
       "Each colour + legend name is a measured family; select families above to light them while the rest grey out; "
       "coral <b>fold</b> lines join a word’s two senses; gold-ringed = split senses. Hover a node for its "
       "verse-count, degree and betweenness.")

# ── METRIC TABLES ────────────────────────────────────────────────────────────
C.section("Family metrics — the numbers behind the picture")
cdf = pd.DataFrame([{
    "family (hub-concept)": c["label"], "concepts": c["n"], "avg degree": c["avg_deg"],
    "avg betweenness": c["avg_bet"], "density": c["density"], "internal bonds": c["intra"],
    "bridge bonds": c["inter"], "top members": " · ".join(c["members"][:6])} for c in _CM])
st.dataframe(cdf, use_container_width=True, hide_index=True, height=460)

C.section("Concept metrics — full centralities" + (" (selected families)" if _csel else " (all concepts)"))
sel = [n for n in _N if (not _csel or n["comm"] in _csel)]
ndf = pd.DataFrame([{
    "concept": n["label"], "type": "split-sense" if n["sense"] else "root", "verses": n["df"],
    "degree": n["deg"], "betweenness": n["bet"], "pagerank": n["pr"], "eigenvector": n["eig"],
    "clustering": n["clu"], "family": _clabels[n["comm"]].split("  (")[0]} for n in sel])
ndf = ndf.sort_values(["family", "pagerank"], ascending=[True, False])
st.dataframe(ndf, use_container_width=True, hide_index=True, height=420)
C.note("Degree = direct co-occurrences · Betweenness = bridges between families · PageRank/eigenvector = hub "
       "influence · Clustering = how tightly its neighbours interlink. See the conceptual-foundation panel above.")

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
          "families. Rotate the web, light up a family, and read its metrics: the Qur’ān’s concept structure becomes "
          "something you can navigate, with the two-meaning words made explicit.", accent=C.TEAL)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="\U0001f50e")
