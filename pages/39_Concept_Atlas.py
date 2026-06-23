"""Concept Atlas — the whole Qur'ān's conceptual territory in one map.
Nodes = top content roots (size = frequency); edges = ATTRACTION (PPMI) backbone (each node's top-3
above-chance partners — a legible skeleton, not a hairball); regions/colour = auto-grouped THEMES
(Louvain on the attraction graph); optional recolour by revelation (nuzūl) phase. Click any concept in
the theme index to open it in Search. Synthesis of validated engines — a navigation map, not a new claim.
"""
import math
from collections import Counter
import streamlit as st
import networkx as nx
from networkx.algorithms import community as nxcom
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from analysis import COL_SURAH, COL_SURAH_NAME, COL_AYAH, normalize_letters
from state import get_corpus, hero, layer, log_page, chip_row

st.set_page_config(page_title="Concept Atlas", page_icon="🗺️", layout="wide")
log_page("concept_atlas")
corpus = get_corpus()
INK = "#10243A"
# This is a dense analytical page (wide chart + many-column data table) — let it use the monitor.
# Must match the global selector's specificity (section[data-testid=stMain] .block-container) to win.
st.markdown("<style>section[data-testid='stMain'] .block-container{"
            "max-width:min(1850px,97vw)!important;}</style>", unsafe_allow_html=True)
THEME_COLORS = ["#0F6E56", "#1D3557", "#E63946", "#EF9F27", "#7209B7", "#2A9D8F",
                "#9C6644", "#3A86FF", "#D62828", "#588157", "#6D597A", "#B5179E"]

@st.cache_data(show_spinner=False)
def _graphfeat(_cid):
    """Precomputed per-concept GRAPH features (role bridge/hub/member, family) — built offline
    (research/intrinsic/scripts/precompute_concept_graph.py); the app only READS. Keyed by
    normalized root. Powers the 'Network role' colouring (banked finding, not a runtime compute)."""
    import json as _json, os as _os
    try:
        _p = _os.path.join(_os.path.dirname(__file__), "..", "concept_graph_features.json")
        with open(_p, encoding="utf-8") as _f:
            return _json.load(_f)["concepts"]
    except Exception:
        return {}

@st.cache_data(show_spinner=False)
def _sura_names(_cid):
    g = corpus.df.groupby(COL_SURAH)[COL_SURAH_NAME].first()
    return {int(k): str(v) for k, v in g.items()}

def _clicked(ev):
    """(point_index, curve_number) of the first clicked point from a plotly on_select event, or (None, None).
    Handles both dict and attribute access, and both 'points' and flat 'point_indices'."""
    try:
        sel = ev["selection"] if isinstance(ev, dict) else getattr(ev, "selection", None)
    except Exception:
        sel = None
    if not sel:
        return None, None
    getf = (sel.get if isinstance(sel, dict) else (lambda k, d=None: getattr(sel, k, d)))
    pts = getf("points") or []
    if pts:
        p = pts[0]
        g = (p.get if isinstance(p, dict) else (lambda k, d=None: getattr(p, k, d)))
        return g("point_index", g("point_number")), g("curve_number")
    pidx = getf("point_indices") or getf("point_index") or []
    if pidx:
        return (pidx[0] if isinstance(pidx, (list, tuple)) else pidx), None
    return None, None

ROLE_COLOR = {"connector / bridge": "#E63946", "family anchor (hub)": "#EF9F27"}  # member → muted below
ROLE_TAG = {"connector / bridge": "🌉 bridge", "family anchor (hub)": "⭐ hub"}

@st.cache_data(show_spinner="Building the concept map…")
def build_atlas(_cid, scope="all", sel=None, n_nodes=150, drop_ubiq=10, topk=3):
    N = len(corpus.df)
    su = [int(x) for x in corpus.df[COL_SURAH]]
    if scope == "sura":
        idxs = [i for i in range(N) if su[i] == sel]; drop_ubiq, n_nodes = 6, 90
    elif scope == "band":                              # relative-position band (DIVINE-ALT re-index)
        ay = [int(float(x)) for x in corpus.df[COL_AYAH]]
        order = {}
        for i in range(N): order.setdefault(su[i], []).append(i)
        for s in order: order[s].sort(key=lambda i: ay[i])
        idxs = []
        for s, rws in order.items():
            L = len(rws)
            if L < 5: continue                         # too short to band cleanly
            for k, i in enumerate(rws):
                if min(4, int(k / L * 5)) == sel: idxs.append(i)
        drop_ubiq, n_nodes = 8, 120
    else:
        idxs = list(range(N))
    rootset = [set(r for r in corpus.root_tokens[i] if r and r != "-") for i in idxs]
    docf = Counter()
    for s in rootset:
        for r in s: docf[r] += 1
    if not docf:
        return dict(nodes=[], docf={}, edges=[], theme_of={}, themes=[], nuz={}, pos={})
    M = max(1, len(idxs))                              # probability base = āyāt in scope
    drop = {r for r, _ in docf.most_common(drop_ubiq)}
    nodes = [r for r, _ in docf.most_common() if r not in drop][:n_nodes]
    nodeset = set(nodes)
    co = Counter()
    for s in rootset:
        rs = sorted(s & nodeset)
        for a in range(len(rs)):
            for b in range(a + 1, len(rs)): co[(rs[a], rs[b])] += 1
    def ppmi(a, b, w):
        pa = docf[a] / M; pb = docf[b] / M; pab = w / M
        return max(0.0, math.log(pab / (pa * pb))) if pa * pb * pab > 0 else 0.0
    adj = {n: [] for n in nodes}
    for (a, b), w in co.items():
        pm = ppmi(a, b, w)
        if pm > 0: adj[a].append((pm, b)); adj[b].append((pm, a))
    G = nx.Graph(); G.add_nodes_from(nodes)
    for n in nodes:
        for pm, m in sorted(adj[n], reverse=True)[:topk]:
            w = round(pm, 3)
            if G.has_edge(n, m): G[n][m]["weight"] = max(G[n][m]["weight"], w)
            else: G.add_edge(n, m, weight=w)
    comms = sorted(nxcom.louvain_communities(G, weight="weight", seed=1), key=len, reverse=True)
    theme_of = {}; themes = []
    for i, cm in enumerate(comms):
        ordered = sorted(cm, key=lambda r: -docf[r])
        themes.append((i, ordered, ordered[:3]))
        for r in cm: theme_of[r] = i
    snz = {}
    for i in range(N):
        ss = su[i]
        if ss not in snz:
            try: snz[ss] = int(corpus.df.iloc[i]["ترتیب نزول"])
            except Exception: pass
    occ = {r: Counter() for r in nodes}
    for li, i in enumerate(idxs):
        ss = su[i]
        for r in rootset[li]:
            if r in nodeset: occ[r][ss] += 1
    nuz = {}
    for r in nodes:
        it = [(snz[s], cc) for s, cc in occ[r].items() if s in snz]
        tot = sum(cc for _, cc in it); nuz[r] = (sum(nz * cc for nz, cc in it) / tot) if tot else 57.0
    pos = nx.spring_layout(G, weight="weight", seed=7, k=0.5, iterations=60)
    return dict(nodes=nodes, docf={r: docf[r] for r in nodes}, edges=[(a, b, G[a][b]["weight"]) for a, b in G.edges()],
                theme_of=theme_of, themes=themes, nuz=nuz, pos={n: [float(p[0]), float(p[1])] for n, p in pos.items()})

@st.cache_data(show_spinner="Building the semantic space…")
def _semantic_space(_cid, n=750):
    """Corpus-scale semantic embedding (validated): nodes = top roots, SIM = PPMI-context cosine,
    xy = 2-D PCA for display, idf = per-sūra distinctiveness. Used by the per-sūra semantic footprint."""
    Nn = len(corpus.df)
    su = [int(x) for x in corpus.df[COL_SURAH]]
    vr = [set(r for r in corpus.root_tokens[i] if r and r != "-") for i in range(Nn)]
    fr = Counter(r for s in vr for r in s)
    drop = {r for r, _ in fr.most_common(8)}
    nodes = [r for r, k in fr.most_common() if k >= 6 and r not in drop][:n]
    ni = {r: i for i, r in enumerate(nodes)}; M = len(nodes)
    co = np.zeros((M, M))
    for s in vr:
        ix = sorted(ni[r] for r in s if r in ni)
        for a in range(len(ix)):
            for b in range(a + 1, len(ix)): co[ix[a], ix[b]] += 1; co[ix[b], ix[a]] += 1
    f = np.array([fr[r] for r in nodes], dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        P = co / (f[:, None] * f[None, :] / Nn)
        PP = np.log(np.where(P > 0, P, 1.0)); PP[PP < 0] = 0
    U = PP / (np.linalg.norm(PP, axis=1, keepdims=True) + 1e-9)
    SIM = U @ U.T; np.fill_diagonal(SIM, 0)
    sset = {}
    for i in range(Nn): sset.setdefault(su[i], set()).update(vr[i])
    NS = len(sset); sdf = Counter()
    for s, rs in sset.items():
        for r in rs:
            if r in ni: sdf[r] += 1
    idf = {r: float(np.log(NS / sdf[r])) for r in nodes if sdf.get(r)}
    try:
        from sklearn.decomposition import PCA
        xy = PCA(n_components=2, random_state=0).fit_transform(U)
    except Exception:
        xy = U[:, :2]
    return dict(nodes=nodes, ni=ni, xy=np.asarray(xy, float), SIM=SIM, idf=idf)

@st.cache_data(show_spinner="Mapping the sūras…")
def _sura_space(_cid):
    """The 114 sūras as a semantic map: each sūra = tf-idf vector over its roots; distance = cosine
    dissimilarity; xy = 2-D MDS; comm = auto families (validated: one community ~88% Medinan)."""
    Nn = len(corpus.df); su = [int(x) for x in corpus.df[COL_SURAH]]
    rootcnt = {}
    for i in range(Nn):
        dd = rootcnt.setdefault(su[i], Counter())
        for r in corpus.root_tokens[i]:
            if r and r != "-": dd[r] += 1
    suras = sorted(rootcnt); NS = len(suras)
    vocab = sorted({r for s in suras for r in rootcnt[s]}); vi = {r: j for j, r in enumerate(vocab)}
    dfr = Counter()
    for s in suras:
        for r in rootcnt[s]: dfr[r] += 1
    idf = {r: np.log(NS / dfr[r]) for r in vocab}
    V = np.zeros((NS, len(vocab)))
    for a, s in enumerate(suras):
        tot = sum(rootcnt[s].values()) or 1
        for r, k in rootcnt[s].items(): V[a, vi[r]] = (k / tot) * idf[r]
    U = V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-9)
    SIM = U @ U.T; np.fill_diagonal(SIM, 0)
    try:
        from sklearn.manifold import MDS
        Dm = 1 - SIM; np.fill_diagonal(Dm, 0)
        xy = MDS(n_components=2, dissimilarity="precomputed", random_state=0,
                 normalized_stress="auto", n_init=1).fit_transform(Dm)
    except Exception:
        from sklearn.decomposition import PCA
        xy = PCA(n_components=2, random_state=0).fit_transform(U)
    G = nx.Graph(); G.add_nodes_from(range(NS))
    for a in range(NS):
        for b in np.argsort(-SIM[a])[:6]:
            if a != int(b): G.add_edge(a, int(b), weight=float(SIM[a, int(b)]))
    comm = {}
    for k, cc in enumerate(sorted(nxcom.greedy_modularity_communities(G, weight="weight"), key=len, reverse=True)):
        for a in cc: comm[a] = k
    # per-family (cluster) metrics
    length = Counter(su)
    firstrow = {}
    for i in range(Nn):
        if su[i] not in firstrow: firstrow[su[i]] = i
    nuz = {}
    for s, i in firstrow.items():
        try: nuz[s] = int(corpus.df.iloc[i]["ترتیب نزول"])
        except Exception: nuz[s] = None
    families = []
    for fid in sorted(set(comm.values())):
        mem = [a for a in range(NS) if comm[a] == fid]
        coh = float(SIM[np.ix_(mem, mem)][np.triu_indices(len(mem), 1)].mean()) if len(mem) > 1 else 0.0
        others = [a for a in range(NS) if comm[a] != fid]
        sep = float(SIM[np.ix_(mem, others)].mean()) if (others and mem) else 0.0
        agg = Counter()
        for a in mem:
            for r, k in rootcnt[suras[a]].items(): agg[r] += k
        tot = sum(agg.values()) or 1
        sc = {r: (agg[r] / tot) * idf.get(r, 0.0) for r in agg}
        topc = [r for r in sorted(sc, key=lambda r: -sc[r])[:8]]
        msur = [suras[a] for a in mem]
        mn = [nuz[s] for s in msur if nuz.get(s)]
        families.append({"id": fid, "n": len(mem), "members": msur,
                         "cohesion": round(coh, 3), "separation": round(sep, 3),
                         "silhouette": round(coh - sep, 3),
                         "mean_nuz": (round(float(np.mean(mn))) if mn else None),
                         "mean_len": round(float(np.mean([length[s] for s in msur]))),
                         "concepts": topc})
    return dict(suras=suras, xy=np.asarray(xy, float), comm=comm, families=families)

def figure(d, color_by, focus=None):
    pos, nodes, docf = d["pos"], d["nodes"], d["docf"]
    ex, ey = [], []
    for a, b, _w in d["edges"]:
        ex += [pos[a][0], pos[b][0], None]; ey += [pos[a][1], pos[b][1], None]
    edge_tr = go.Scatter(x=ex, y=ey, mode="lines", line=dict(width=0.6, color="#cfd8dc"), hoverinfo="none")
    xs = [pos[n][0] for n in nodes]; ys = [pos[n][1] for n in nodes]
    sizes = [6 + (docf[n] ** 0.5) * 0.9 for n in nodes]
    top40 = set(sorted(nodes, key=lambda r: -docf[r])[:40])
    texts = [n if n in top40 else "" for n in nodes]
    gf = d.get("gf", {})
    if color_by == "Theme":
        colors = [THEME_COLORS[d["theme_of"][n] % len(THEME_COLORS)] for n in nodes]
        if focus is not None:                       # dim everything except the focused theme
            colors = [colors[i] if d["theme_of"][n] == focus else "#dce4e7" for i, n in enumerate(nodes)]
            texts = [n if (d["theme_of"][n] == focus and n in top40) else "" for n in nodes]
        marker = dict(size=sizes, color=colors, line=dict(width=0.5, color="#ffffff"))
    elif color_by == "Network role":               # banked graph finding: bridge / hub / member
        colors = [ROLE_COLOR.get((gf.get(normalize_letters(n)) or {}).get("role"), "#9FB3C8") for n in nodes]
        marker = dict(size=sizes, color=colors, line=dict(width=0.5, color="#ffffff"))
    else:
        colors = [d["nuz"][n] for n in nodes]
        marker = dict(size=sizes, color=colors, colorscale="YlOrRd", showscale=True,
                      colorbar=dict(title="nuzūl<br>early→late", thickness=12),
                      line=dict(width=0.5, color="#ffffff"))
    hov = []
    for n in nodes:
        f = gf.get(normalize_letters(n))
        extra = ""
        if f:
            extra = " · " + ROLE_TAG.get(f.get("role"), "member")
            if f.get("family_label"): extra += f" · family {f['family_label']}"
        hov.append(f"{n} · freq {docf[n]} · revelation {d['nuz'][n]:.0f}/114 · theme {d['theme_of'][n] + 1}{extra}")
    node_tr = go.Scatter(x=xs, y=ys, mode="markers+text", text=texts, textposition="top center",
                         textfont=dict(size=12, color=INK), hovertext=hov, hoverinfo="text", marker=marker)
    fig = go.Figure([edge_tr, node_tr])
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=650,
                      xaxis=dict(visible=False), yaxis=dict(visible=False),
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig

hero("🗺️ Concept Atlas",
     "The conceptual territory as a map — roots linked by attraction, grouped into communities, sized by "
     "frequency. Scope it to the whole Qur'ān, a single sūra, or a relative-position band. "
     "Click any concept to open it in Search.")

SNAME = _sura_names(id(corpus))
BANDS = ["Opening", "Early", "Middle", "Late", "Closing"]
_goto = st.session_state.pop("_atlas_goto_sura", None)        # set by the sūra-map dropdown
if _goto is not None:
    st.session_state["atlas_scope"] = "A sūra"
    st.session_state["atlas_sura"] = int(_goto)
if st.session_state.pop("_atlas_goto_whole", None):          # set by the "back" button
    st.session_state["atlas_scope"] = "Whole Qur'ān"
_sc1, _sc2 = st.columns([1, 1.7])
_scope = _sc1.radio("Scope", ["Whole Qur'ān", "A sūra", "Position band"], horizontal=True, key="atlas_scope")
if _scope == "A sūra":
    _sel = _sc2.selectbox("Sūra", sorted(SNAME), format_func=lambda s: f"{s} · {SNAME[s]}", key="atlas_sura")
    d = build_atlas(id(corpus), "sura", _sel)
    _note = f"<b>Sūra {_sel} · {SNAME[_sel]}</b> — its <b>internal</b> concept communities (how this sūra is built)."
elif _scope == "Position band":
    _b = _sc2.selectbox("Relative band (pooled across all sūras)", list(range(5)),
                        format_func=lambda b: BANDS[b], key="atlas_band")
    d = build_atlas(id(corpus), "band", _b)
    _note = (f"<b>{BANDS[_b]} band</b> — verses at this relative position, pooled across all sūras. "
             "⚠️ <b>[DIVINE-ALT]</b> — an alternative re-indexing, not the muṣḥaf's primary order.")
else:
    d = build_atlas(id(corpus), "all")
    _note = "The <b>whole Qur'ān</b>'s conceptual territory."
if len(d.get("nodes", [])) < 4:
    st.info("Not enough concepts at this scope to draw a map — pick a longer sūra or another band.")
    st.stop()
d["gf"] = _graphfeat(id(corpus))
st.markdown(f"<div style='font-size:16px;color:#10243A;margin:2px 0 6px'>{_note}</div>", unsafe_allow_html=True)                     # attach banked graph roles for the role colouring
if _scope != "Whole Qur'ān":
    if st.button("← Back to the 114-sūra map", key="atlas_back"):
        st.session_state["_atlas_goto_whole"] = True
        st.session_state["atlas_mapjump"] = 0
        st.session_state["_atlas_lastjump"] = 0
        st.rerun()
with st.expander("ℹ️ What this page shows — scales, maps & metrics (one-page guide)"):
    st.markdown(
"""**The core idea.** Concepts (grammatical roots) are **nodes**; an **edge** joins two that co-occur more than chance (PPMI); **colour** = auto-found communities (Louvain). The *same* engine drives every view below.

**Scope — three lenses on the concept web (the radio at the top):**
- **1 · Whole Qur'ān — the territory.** Every major concept across all 6,236 āyāt, grouped into **themes**, with the concepts that **bridge** them. The master map; everything else is a zoom or a companion. *Takeaway: the vocabulary self-organises into a few coherent themes.*
- **2 · A sūra — how one chapter is built.** The same graph from one sūra's verses → its **internal communities**; for narratives these track the **episodes** (Yūsuf: plot · temptation · prison · reunion). *Takeaway: a chapter's skeleton is latent in its own concept co-occurrence.*
- **3 · Position band — the shape of a sūra. ⚠️ [DIVINE-ALT].** Verses pooled by *where* they fall (opening→closing) across all sūras: **doxology frames the edges, exhortation closes, narrative fills the body.** An alternative re-indexing, never the muṣḥaf's primary order.

**Companion views (same data, a different question):**
- **The 114 sūras as a semantic map** (Whole scope) — each sūra is a **point**, distance ≈ vocabulary similarity; auto-**families** emerge (one ≈ 88% Medinan, found with no labels). The **cluster-metrics table** gives each family's cohesion, separation, silhouette (tight vs loose), revelation tilt and defining concepts.
- **A sūra's semantic footprint** (A-sūra scope) — *where* that sūra's distinctive concepts sit in the whole meaning-space, with a **concentration score** (legal sūras tight, narrative/hymn scattered).
- **The data table** — every concept with frequency and the full **centrality suite** (degree, betweenness, closeness, eigenvector, PageRank, clustering) plus community, revelation and top partners — sortable, copyable, Arabic-safe CSV.

**How to read it together.** Move **outward → inward**: the whole territory → one chapter's build → its opening-to-closing shape; and **macro → micro**: which sūras are alike (the 114-map) → where one sūra's concepts live (footprint) → the exact numbers (table).

**Honest scope.** Everything is **measured** (attraction, communities, centralities, MDS) and presented as a **navigation map, not a claim**. Bands and footprints are *exploratory* (DIVINE-ALT / approximate 2-D); necessity is never asserted.""")

c1, c2, c3 = st.columns(3)
c1.metric("Concepts mapped", len(d["nodes"]))
c2.metric("Attraction links", len(d["edges"]))
c3.metric("Themes", len(d["themes"]))
cc1, cc2 = st.columns([1, 1.4])
color_by = cc1.radio("Colour by", ["Theme", "Revelation phase", "Network role"], horizontal=True, key="atlas_color")
_theme_labels = ["— whole map —"] + [f"Theme {ti + 1}: {' · '.join(top)}" for ti, _o, top in d["themes"]]
_focus_sel = cc2.selectbox("Focus a theme", _theme_labels, key="atlas_focus",
                           disabled=(color_by != "Theme"), help="Theme focus applies to the Theme colouring.")
_focus = None if _focus_sel.startswith("—") else _theme_labels.index(_focus_sel) - 1
st.plotly_chart(figure(d, color_by, _focus), use_container_width=True)
if color_by == "Network role":
    _nb = sum(1 for n in d["nodes"] if (d["gf"].get(normalize_letters(n)) or {}).get("role") == "connector / bridge")
    _nh = sum(1 for n in d["nodes"] if (d["gf"].get(normalize_letters(n)) or {}).get("role") == "family anchor (hub)")
    st.markdown("<div style='font-size:12px;color:#10243A;margin:2px 0 0'>"
                f"<span style='color:#E63946'>●</span> bridge — connector across themes ({_nb}) &nbsp;&nbsp;"
                f"<span style='color:#EF9F27'>●</span> family anchor — hub ({_nh}) &nbsp;&nbsp;"
                "<span style='color:#9FB3C8'>●</span> member"
                "<br>Roles are a <b>banked graph finding</b> (degree-normalised betweenness for bridges, "
                "dcSBM within-family hubs) — precomputed, not a runtime claim.</div>", unsafe_allow_html=True)
st.caption("Edges = above-chance pairings (PPMI) only — each concept's strongest 3 partners. "
           "Themes are auto-grouped (Louvain); a navigation map, not a structural claim.")

# ---- semantic footprint: where THIS sūra's distinctive concepts sit in the whole-Qur'ān meaning-space ----
if _scope == "A sūra":
    _S = _semantic_space(id(corpus))
    _su = [int(x) for x in corpus.df[COL_SURAH]]
    _rc = Counter()
    for _i in range(len(corpus.df)):
        if _su[_i] == _sel:
            for _r in corpus.root_tokens[_i]:
                if _r and _r != "-" and _r in _S["ni"]: _rc[_r] += 1
    _tot = sum(_rc.values()) or 1
    _scd = {r: (_rc[r] / _tot) * _S["idf"].get(r, 0.0) for r in _rc}
    _top = sorted(_scd, key=lambda r: -_scd[r])[:25]
    _idx = [_S["ni"][r] for r in _top]
    layer(1, "🧭 Where this sūra sits in the Qur'ān's meaning-space (semantic footprint)")
    if len(_idx) >= 6:
        _iu = np.triu_indices(len(_idx), 1)
        _obs = float(_S["SIM"][np.ix_(_idx, _idx)][_iu].mean())
        _rng = np.random.default_rng(0); _MM = len(_S["nodes"]); _null = []
        for _ in range(800):
            _rr = _rng.choice(_MM, len(_idx), replace=False)
            _null.append(_S["SIM"][np.ix_(_rr, _rr)][_iu].mean())
        _nm = float(np.mean(_null)); _nsd = float(np.std(_null)) + 1e-9
        _z = (_obs - _nm) / _nsd
        _xy = _S["xy"]; _hot = set(_idx)
        _fig2 = go.Figure()
        _fig2.add_trace(go.Scatter(x=[_xy[i, 0] for i in range(_MM) if i not in _hot],
                                   y=[_xy[i, 1] for i in range(_MM) if i not in _hot],
                                   mode="markers", marker=dict(size=4, color="#DCE4EA"), hoverinfo="none"))
        _fig2.add_trace(go.Scatter(x=[_xy[i, 0] for i in _idx], y=[_xy[i, 1] for i in _idx],
                                   mode="markers+text", text=[_S["nodes"][i] for i in _idx],
                                   textposition="top center", textfont=dict(size=13, color=INK),
                                   marker=dict(size=11, color="#1D9E75", line=dict(width=1, color="#ffffff")),
                                   hoverinfo="text"))
        _fig2.update_layout(showlegend=False, height=560, margin=dict(l=0, r=0, t=0, b=0),
                            xaxis=dict(visible=False), yaxis=dict(visible=False),
                            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(_fig2, use_container_width=True, key="atlas_footprint")
        _verdict = ("tightly unified — its distinctive vocabulary clusters in one region (typical of legal / thematic sūras)"
                    if _z > 3 else
                    "scattered — its distinctive words span several regions (typical of narrative / imagery sūras)"
                    if _z < 0.8 else "moderately focused")
        st.caption(f"Grey = the whole Qur'ān's concepts (faint backdrop); green = this sūra's distinctive concepts. "
                   f"**Concentration z = {_z:+.1f}** → the footprint is {_verdict}. "
                   "Semantic distance is from corpus-wide co-occurrence (validated z+3.6); the 2-D projection is approximate.")
    else:
        st.caption("Too few distinctive concepts in the semantic space to map this sūra's footprint.")

# ---- the 114 sūras as a semantic map (which sūras are alike) — whole-Qur'ān companion view ----
if _scope == "Whole Qur'ān":
    _Q = _sura_space(id(corpus))
    layer(1, "🗺️ The 114 sūras as a semantic map — which sūras are alike")
    _qx, _qs, _qc = _Q["xy"], _Q["suras"], _Q["comm"]
    _fam = {}
    for a, s in enumerate(_qs): _fam.setdefault(_qc.get(a, 0), []).append(s)
    _leg = "".join(
        "<span style='display:inline-block;margin:0 14px 4px 0;font-size:12px;color:#10243A'>"
        f"<span style='display:inline-block;width:11px;height:11px;border-radius:3px;"
        f"background:{THEME_COLORS[k % len(THEME_COLORS)]};margin-left:5px;vertical-align:-1px'></span> "
        f"family {k + 1}: {' · '.join(SNAME.get(s, str(s)) for s in _fam[k][:3])}…</span>"
        for k in sorted(_fam))
    st.markdown(f"<div style='margin:2px 0 6px'>{_leg}</div>", unsafe_allow_html=True)
    _fig3 = go.Figure()
    _fig3.add_trace(go.Scatter(
        x=_qx[:, 0], y=_qx[:, 1], mode="markers+text",
        text=[str(s) for s in _qs], textposition="top center", textfont=dict(size=10, color=INK),
        marker=dict(size=12, color=[THEME_COLORS[_qc.get(a, 0) % len(THEME_COLORS)] for a in range(len(_qs))],
                    line=dict(width=0.5, color="#ffffff")),
        hovertext=[f"Sūra {s} · {SNAME.get(s, '')}" for s in _qs], hoverinfo="text"))
    _fig3.update_layout(showlegend=False, height=600, margin=dict(l=0, r=0, t=0, b=0),
                        dragmode=False,
                        xaxis=dict(visible=False), yaxis=dict(visible=False),
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(_fig3, use_container_width=True, key="atlas_suramap")
    _jc1, _jc2 = st.columns([2, 3])
    _jump = _jc1.selectbox("🔎 Open a sūra from the map →", [0] + _qs,
                           format_func=lambda s: "— pick a sūra —" if s == 0 else f"{s} · {SNAME.get(s, '')}",
                           key="atlas_mapjump")
    if _jump and _jump != st.session_state.get("_atlas_lastjump"):
        st.session_state["_atlas_lastjump"] = _jump
        st.session_state["_atlas_goto_sura"] = int(_jump); st.rerun()
    st.caption("Each point is a sūra; distance ≈ vocabulary similarity (MDS on tf-idf cosine). "
               "Colour = family (legend above). Hover a point to see its name; use the dropdown to open a sūra's internal map + footprint. A navigation map, not a claim.")
    # ---- cluster (family) metrics table ----
    _F = _Q["families"]
    layer(1, "📊 Cluster metrics — the sūra families")
    _hdr = "".join(
        f'<th style="position:sticky;top:0;background:#1D3557;color:#fff;padding:7px 9px;'
        f'text-align:right;font-size:12px;white-space:nowrap">{h}</th>'
        for h in ["family", "# sūras", "cohesion", "separation", "silhouette",
                  "mean revelation", "mean length", "defining concepts", "members"])
    _trs = []
    for _f in _F:
        _col = THEME_COLORS[_f["id"] % len(THEME_COLORS)]
        _mem = " · ".join(SNAME.get(s, str(s)) for s in _f["members"][:14]) + (f" …(+{_f['n'] - 14})" if _f["n"] > 14 else "")
        _cells = [f'<span style="display:inline-block;width:11px;height:11px;border-radius:3px;'
                  f'background:{_col};margin-left:5px"></span> family {_f["id"] + 1}',
                  _f["n"], _f["cohesion"], _f["separation"], _f["silhouette"],
                  (_f["mean_nuz"] if _f["mean_nuz"] is not None else "—"), _f["mean_len"],
                  " · ".join(_f["concepts"]), _mem]
        _tds = "".join(
            f'<td style="padding:5px 9px;border-top:1px solid #EEF2F7;text-align:right;'
            f'{"font-family:Amiri,serif;" if _k in (7, 8) else ""}">{_c}</td>'
            for _k, _c in enumerate(_cells))
        _trs.append(f"<tr>{_tds}</tr>")
    st.markdown('<div style="overflow:auto;border:1px solid #E2E8F1;border-radius:10px">'
                '<table style="width:100%;border-collapse:collapse;font-size:13px;color:#10243A">'
                f'<thead><tr>{_hdr}</tr></thead><tbody>{"".join(_trs)}</tbody></table></div>',
                unsafe_allow_html=True)
    st.caption("Cohesion = mean within-family vocabulary similarity; separation = mean similarity to other families; "
               "silhouette = cohesion − separation (higher = tighter & more distinct). Mean revelation = nuzūl order (early→late).")

if _scope != "Whole Qur'ān":
    if st.button("← Back to the 114-sūra map", key="atlas_back2"):
        st.session_state["_atlas_goto_whole"] = True
        st.session_state["atlas_mapjump"] = 0
        st.session_state["_atlas_lastjump"] = 0
        st.rerun()

# ---- data table behind the map (sortable · scrollable · copyable) ----
_tG = nx.Graph(); _tG.add_nodes_from(d["nodes"])
for _a, _b, _w in d["edges"]:
    _tG.add_edge(_a, _b, weight=_w, dist=1.0 / max(_w, 1e-6))
_deg = dict(_tG.degree())
_NA = {n: 0.0 for n in d["nodes"]}
def _safe(fn, **kw):
    try: return fn(_tG, **kw)
    except Exception: return dict(_NA)
_degc = _safe(nx.degree_centrality)
_bet  = _safe(nx.betweenness_centrality, weight="dist")
_clo  = _safe(nx.closeness_centrality, distance="dist")
_eig  = _safe(nx.eigenvector_centrality_numpy, weight="weight")
_pr   = _safe(nx.pagerank, weight="weight")
_clu  = _safe(nx.clustering, weight="weight")
_partners = {n: [] for n in d["nodes"]}
for _a, _b, _w in sorted(d["edges"], key=lambda e: -e[2]):
    if len(_partners[_a]) < 3: _partners[_a].append(_b)
    if len(_partners[_b]) < 3: _partners[_b].append(_a)
_clab = {ti: " · ".join(top) for ti, _o, top in d["themes"]}
_rolemap = {"connector / bridge": "bridge", "family anchor (hub)": "hub"}
_rows = []
for n in d["nodes"]:
    _ti = d["theme_of"][n]
    _role = _rolemap.get((d["gf"].get(normalize_letters(n)) or {}).get("role"), "member")
    _rows.append({"concept": n, "frequency": d["docf"][n], "community #": _ti + 1,
                  "community": _clab.get(_ti, ""), "role": _role,
                  "degree": _deg.get(n, 0), "degree_cent": round(_degc.get(n, 0.0), 3),
                  "betweenness": round(_bet.get(n, 0.0), 3), "closeness": round(_clo.get(n, 0.0), 3),
                  "eigenvector": round(_eig.get(n, 0.0), 3), "pagerank": round(_pr.get(n, 0.0), 4),
                  "clustering": round(_clu.get(n, 0.0), 3), "revelation 1–114": round(d["nuz"][n]),
                  "top partners": " · ".join(_partners[n])})
_df = pd.DataFrame(_rows).sort_values(["community #", "frequency"], ascending=[True, False])
layer(1, "📋 Data behind the map — scrollable · copyable (use the CSV below to sort)")
# Full-width HTML table — st.dataframe won't stretch on this Streamlit build, so we control width directly.
_cols = list(_df.columns)
_arab = {"concept", "community", "top partners"}
_head = "".join(
    f'<th style="position:sticky;top:0;background:#1D3557;color:#fff;padding:7px 9px;'
    f'text-align:right;font-size:12px;white-space:nowrap">{c}</th>'
    for c in _cols)
_body = []
for _i, (_, _row) in enumerate(_df.iterrows()):
    _bg = "#FFFFFF" if _i % 2 == 0 else "#F7F9FC"
    _tds = "".join(
        f'<td style="padding:5px 9px;border-top:1px solid #EEF2F7;text-align:right;'
        f'{"font-family:Amiri,serif;font-size:15px;" if c in _arab else ""}">{_row[c]}</td>'
        for c in _cols)
    _body.append(f'<tr style="background:{_bg}">{_tds}</tr>')
_table = (f'<div style="max-height:480px;overflow:auto;border:1px solid #E2E8F1;border-radius:10px">'
          f'<table style="width:100%;border-collapse:collapse;font-size:13px;color:#10243A">'
          f'<thead><tr>{_head}</tr></thead><tbody>{"".join(_body)}</tbody></table></div>')
st.markdown(_table, unsafe_allow_html=True)
st.download_button("⬇️ Download table (CSV — Arabic-safe for Excel)",
                   _df.to_csv(index=False).encode("utf-8-sig"),  # BOM so Excel detects UTF-8 (Arabic shows correctly)
                   file_name="concept_atlas_data.csv", mime="text/csv", key="atlas_csv")
with st.expander("ℹ️ What the columns mean — and why each matters"):
    st.markdown(
"""Each row is one **concept** (a grammatical root = a node). The columns answer different questions about its place in the web.

**Prominence**
- **frequency** — in how many āyāt (at the current scope) the concept appears. *Why:* raw weight — how much of the text it touches.

**Grouping**
- **community # / community** — the auto-detected cluster it belongs to (Louvain), labelled by that cluster's lead concepts. *Why:* its **thematic neighbourhood** — which family of ideas it lives in.
- **role** — a banked graph role: **bridge** (connects different themes), **hub** (anchor of its family), or **member**. *Why:* its structural job in the map.

**Centrality — different senses of "important"**
- **degree** — how many strong (above-chance) partners it links to. *Why:* direct reach — a high-degree concept attracts many others.
- **degree_cent** — the same, normalised 0–1 by network size. *Why:* lets you compare across scopes (a sūra vs the whole Qur'ān).
- **betweenness** — how often it lies on the shortest path between other concepts. *Why:* a **broker/bridge** — high betweenness means removing it would fragment the map; it links otherwise-separate themes.
- **closeness** — how short its average path is to *every* other concept. *Why:* **reach** — a high-closeness concept is "near everything," touching the whole web quickly.
- **eigenvector** — importance by the *company it keeps* (connected to other well-connected concepts). *Why:* **prestige** — embedded among the central, not just busy.
- **pagerank** — a random-walk version of the same idea, robust to quirks. *Why:* where "attention" flows in the web; a stable importance ranking.
- **clustering** — how tightly its own neighbours interlink (0–1). *Why:* **cohesion vs brokerage** — high = sits inside a tight, self-contained theme; low = spans loosely-linked groups (more bridge-like).

**Context**
- **revelation 1–114** — the mean revelation order (nuzūl) of the sūras it appears in, early (Meccan) → late (Medinan). *Why:* *when* in the revelation the concept concentrates.
- **top partners** — its strongest co-occurring concepts. *Why:* what it "goes with" — its immediate meaning-company.

**Reading them together:** *degree / eigenvector / pagerank* tell you **how central** a concept is; *betweenness* tells you whether it's a **bridge**; *closeness* tells you its **reach**; *clustering* tells you whether it sits in a **tight theme or brokers between themes**. A concept high in betweenness but low in clustering is a connector across the Qur'ān's themes; one high in eigenvector and clustering is a core anchor of its own theme.

**Takeaway.** This table turns the map into numbers you can rank, sort, and export: find the concept that most **bridges** the Qur'ān's themes (top *betweenness*), the **anchor** of each theme (top *eigenvector* within a community), the most far-reaching ideas (top *closeness*), and how a concept's weight tilts **Meccan → Medinan** (*revelation*) — at whichever scale you choose (whole Qur'ān, one sūra, or a position band). It makes the picture **measurable and checkable**, not just visual.""")

# inline concept peek — quick profile without leaving the map
_pick = st.selectbox("🔍 Inspect a concept", [""] + d["nodes"],
                     format_func=lambda r: "— pick a root —" if r == "" else r, key="atlas_pick")
if _pick:
    _nb = sorted(((w, (b if a == _pick else a)) for a, b, w in d["edges"] if _pick in (a, b)), reverse=True)[:6]
    _th = d["theme_of"][_pick]; _top = d["themes"][_th][2]
    _bits = [f"freq <b>{d['docf'][_pick]}</b>", f"theme <b>{_th + 1}</b> ({' · '.join(_top)})",
             f"revelation <b>{d['nuz'][_pick]:.0f}/114</b>"]
    if _nb: _bits.append("pairs with <b>" + " · ".join(m for _w, m in _nb) + "</b>")
    st.markdown("<div style='background:#F4F9F7;border:1px solid #cfe4dc;border-radius:10px;"
                "padding:8px 14px;margin:4px 0 8px;font-size:13.5px;color:#10243A;line-height:1.75'>"
                f"🌱 <b>{_pick}</b> &nbsp;·&nbsp; " + " &nbsp;·&nbsp; ".join(_bits) + "</div>", unsafe_allow_html=True)
    if st.button(f"Open {_pick} in Search →", key="atlas_open"):
        st.session_state._pending_q = _pick
        st.switch_page("pages/38_Search.py")

layer(1, "Themes — click a concept to open it in Search")
for ti, ordered, top in d["themes"]:
    col = THEME_COLORS[ti % len(THEME_COLORS)]
    st.markdown(f"<div style='margin:8px 0 2px;font-size:13.5px;color:{INK}'>"
                f"<span style='display:inline-block;width:11px;height:11px;border-radius:3px;"
                f"background:{col};margin-left:4px'></span> <b>Theme {ti + 1}</b> · {' · '.join(top)}</div>",
                unsafe_allow_html=True)
    rr = ordered[:18]
    with chip_row(f"atlas-{ti}"):                          # content-sized wrapping chips (density rule), not full-width
        cols = st.columns(len(rr))
        for k, r in enumerate(rr):
            if cols[k].button(r, key=f"atlas_{ti}_{k}"):    # NO use_container_width → small chip
                st.session_state._pending_q = r
                st.switch_page("pages/38_Search.py")
