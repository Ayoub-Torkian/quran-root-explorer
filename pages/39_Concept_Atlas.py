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
from analysis import COL_SURAH, COL_SURAH_NAME, COL_AYAH, normalize_letters, disp_root
from state import get_corpus, hero, layer, log_page, chip_row
import landscape as LS

st.set_page_config(page_title="Concept Atlas", page_icon="🗺️", layout="wide")
log_page("concept_atlas")
corpus = get_corpus()
INK = "#10243A"
# This is a dense analytical page (wide chart + many-column data table) — let it use the monitor.
# Must match the global selector's specificity (section[data-testid=stMain] .block-container) to win.
st.markdown("<style>section[data-testid='stMain'] .block-container{"
            "max-width:1850px!important;}</style>", unsafe_allow_html=True)
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
    _p3 = nx.spring_layout(G, dim=3, weight="weight", seed=7, k=0.5, iterations=60)
    _nl = list(_p3.keys()); _a = np.array([_p3[n] for n in _nl], float)
    _a = (_a - _a.mean(0)) / (_a.std(0) + 1e-9)                      # equalize axes (kill the flat disc)
    _a = _a / (np.linalg.norm(_a, axis=1, keepdims=True) + 1e-9)     # project onto unit sphere -> globe
    pos3 = {n: [float(_a[k][0]), float(_a[k][1]), float(_a[k][2])] for k, n in enumerate(_nl)}
    _allf = sum(docf.values()); _mapf = sum(docf[r] for r in nodes)     # coverage = mapped vs ALL roots in scope
    try:
        _modq = float(nxcom.modularity(G, comms, weight="weight"))      # how clean the family split is (>0.3 strong)
    except Exception:
        _modq = float("nan")
    return dict(nodes=nodes, docf={r: docf[r] for r in nodes}, edges=[(a, b, G[a][b]["weight"]) for a, b in G.edges()],
                theme_of=theme_of, themes=themes, nuz=nuz, pos={n: [float(p[0]), float(p[1])] for n, p in pos.items()},
                pos3=pos3, coverage=(_mapf / _allf if _allf else 0.0), n_all_roots=len(docf),
                total_mentions=int(_allf), mapped_mentions=int(_mapf), modularity=_modq)

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
    dfr = Counter()
    for s in suras:
        for r in rootcnt[s]: dfr[r] += 1
    # similarity uses only roots in ≥2 sūras: a single-sūra root can never be shared, it only dilutes the norm
    vocab = sorted({r for r in dfr if dfr[r] >= 2}); vi = {r: j for j, r in enumerate(vocab)}
    idf = {r: np.log(NS / dfr[r]) for r in vocab}
    V = np.zeros((NS, len(vocab)))
    for a, s in enumerate(suras):
        tot = sum(rootcnt[s].values()) or 1
        for r, k in rootcnt[s].items():
            if r in vi: V[a, vi[r]] = (k / tot) * idf[r]
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
    tlen = {s: int(sum(rootcnt[s].values())) for s in suras}
    rootsets = {s: set(rootcnt[s]) for s in suras}
    return dict(suras=suras, xy=np.asarray(xy, float), comm=comm, families=families,
                SIM=SIM, tlen=tlen, rootsets=rootsets)

@st.cache_data(show_spinner="Computing elaboration links…")
def _elab_engine(_cid):
    """Validated, length-controlled elaboration metric: which long sūra most develops a (short) sūra's
    distinctive concepts. spec(S,L) = idf-weighted, depth-aware match of S's distinctive concepts in L,
    normalised by how much L elaborates a TYPICAL short sūra (so length can't win)."""
    Nn = len(corpus.df); su = [int(x) for x in corpus.df[COL_SURAH]]
    rows = {}
    for i in range(Nn): rows.setdefault(su[i], []).append(i)
    rootcnt = {}; vcount = {}; present = {}; length = {}
    for s, idxs in rows.items():
        length[s] = len(idxs); rc = Counter(); vc = Counter()
        for i in idxs:
            seen = set()
            for r in corpus.root_tokens[i]:
                if r and r != "-": rc[r] += 1; seen.add(r)
            for r in seen: vc[r] += 1
        rootcnt[s] = rc; vcount[s] = vc; present[s] = set(rc)
    suras = sorted(rows); NS = len(suras)
    dfr = Counter()
    for s in suras:
        for r in present[s]: dfr[r] += 1
    idf = {r: float(np.log(NS / dfr[r])) for r in dfr}
    DIST = {}
    for s in suras:
        tot = sum(rootcnt[s].values()) or 1
        sc = {r: (rootcnt[s][r] / tot) * idf[r] for r in rootcnt[s]}
        DIST[s] = [r for r in sorted(sc, key=lambda r: -sc[r])[:8]]
    def elab(S, L):
        return sum(idf[r] * np.log(1 + vcount[L].get(r, 0)) for r in DIST[S] if r in present[L])
    shortS = [s for s in suras if length[s] <= 10]
    Lbase = {L: (float(np.mean([elab(s, L) for s in shortS if s != L])) + 1e-9) for L in suras}
    return dict(suras=suras, length=length, idf=idf, DIST=DIST, vcount=vcount, present=present, Lbase=Lbase)

@st.cache_data(show_spinner="Building semantic vectors…")
def _axis_space(_cid, n=600):
    """Dense SVD-of-PPMI embedding (count-based word2vec) for semantic-axis projection."""
    from sklearn.decomposition import TruncatedSVD
    Nn = len(corpus.df)
    vr = [set(r for r in corpus.root_tokens[i] if r and r != "-") for i in range(Nn)]
    fr = Counter(r for s in vr for r in s); drop = {r for r, _ in fr.most_common(8)}
    nodes = [r for r, k in fr.most_common() if k >= 8 and r not in drop][:n]
    ni = {r: i for i, r in enumerate(nodes)}; M = len(nodes)
    co = np.zeros((M, M))
    for s in vr:
        ix = sorted(ni[r] for r in s if r in ni)
        for a in range(len(ix)):
            for b in range(a + 1, len(ix)): co[ix[a], ix[b]] += 1; co[ix[b], ix[a]] += 1
    f = np.array([fr[r] for r in nodes], float)
    with np.errstate(divide="ignore", invalid="ignore"):
        P = co / (f[:, None] * f[None, :] / Nn); PP = np.log(np.where(P > 0, P, 1.0)); PP[PP < 0] = 0
    Vv = TruncatedSVD(n_components=min(100, M - 1), random_state=0).fit_transform(PP)
    Vv = Vv - Vv.mean(axis=0)          # mean-centre: removes the common component so valence separates cleanly
    Vv = Vv / (np.linalg.norm(Vv, axis=1, keepdims=True) + 1e-9)
    nmix = {}
    for r in nodes: nmix.setdefault(normalize_letters(r), r)   # normalized form -> raw node key
    return dict(nodes=nodes, ni=ni, V=Vv, norm_index=nmix)

@st.cache_data(show_spinner="Building the attraction–repulsion field…")
def _field_space(_cid, n=700):
    """Per-concept field: āyah co-occurrence vs a chance baseline (signed z) + same-context embedding cosine."""
    from sklearn.decomposition import TruncatedSVD
    Nn = len(corpus.df)
    vr = [set(r for r in corpus.root_tokens[i] if r and r != "-") for i in range(Nn)]
    fr = Counter(r for s in vr for r in s); drop = {r for r, _ in fr.most_common(8)}
    nodes = [r for r, k in fr.most_common() if k >= 10 and r not in drop][:n]
    ni = {r: i for i, r in enumerate(nodes)}; M = len(nodes)
    co = np.zeros((M, M))
    for s in vr:
        ix = sorted(ni[r] for r in s if r in ni)
        for a in range(len(ix)):
            for b in range(a + 1, len(ix)): co[ix[a], ix[b]] += 1; co[ix[b], ix[a]] += 1
    f = np.array([fr[r] for r in nodes], float)
    E = np.outer(f, f) / Nn                       # expected joint āyāt under independence
    defz = (co - E) / np.sqrt(E + 1e-9)           # signed deviation: + = gather, − = refrain
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = co * Nn / np.outer(f, f)
        PMI = np.log(np.where(co > 0, ratio, 1.0))
        PP = np.where(PMI > 0, PMI, 0.0)
    Vv = TruncatedSVD(n_components=min(100, M - 1), random_state=0).fit_transform(PP)
    Vv = Vv - Vv.mean(axis=0); Vv = Vv / (np.linalg.norm(Vv, axis=1, keepdims=True) + 1e-9)
    COS = Vv @ Vv.T
    mc = (COS.sum(1) - 1.0) / max(M - 1, 1)        # each concept's mean cosine to all others
    try:
        from scipy.stats import spearmanr
        frho = float(spearmanr(mc, np.log(f)).correlation)   # ≈0 ⇒ similarity is NOT frequency-anchored
    except Exception:
        frho = float("nan")
    nmix = {}
    for r in nodes: nmix.setdefault(normalize_letters(r), r)
    return dict(nodes=nodes, ni=ni, f=f, co=co, E=E, defz=defz, PMI=PMI, COS=COS, norm_index=nmix, freq_rho=frho)

def _ego_view(F, concept, kg=16, kr=5):
    """Embedding-space neighbourhood: concepts placed AND linked by vector cosine (used-in-similar-contexts)."""
    import pandas as pd
    from sklearn.manifold import MDS
    i = F["ni"][concept]; f, co, E, defz, COS, PMI = F["f"], F["co"], F["E"], F["defz"], F["COS"], F["PMI"]
    near = [j for j in np.argsort(-COS[i]) if j != i][:kg]
    far = [j for j in np.argsort(COS[i]) if j != i][:kr]
    S = [i] + near + far
    D = 1.0 - COS[np.ix_(S, S)]; np.fill_diagonal(D, 0.0); D = (D + D.T) / 2; D[D < 0] = 0
    xy = MDS(n_components=2, dissimilarity="precomputed", random_state=1, n_init=4,
             normalized_stress="auto").fit_transform(D)
    xy = xy - xy[0]                                   # place the chosen concept at the origin
    pos = {S[t]: (float(xy[t, 0]), float(xy[t, 1])) for t in range(len(S))}
    # edges: any pair (incl. neighbour–neighbour) alike in the embedding; width & opacity ∝ cosine
    cand = [(a, b, COS[a, b]) for ai, a in enumerate(near) for b in near[ai + 1:] if COS[a, b] >= 0.30]
    cand += [(i, j, COS[i, j]) for j in near if COS[i, j] >= 0.30]
    cand.sort(key=lambda t: -t[2]); cand = cand[:26]
    fig = go.Figure()
    if cand:
        cmn = min(c for _, _, c in cand); cmx = max(c for _, _, c in cand); rng = (cmx - cmn) or 1.0
        for a, b, cv in cand:
            frac = (cv - cmn) / rng
            fig.add_trace(go.Scatter(x=[pos[a][0], pos[b][0]], y=[pos[a][1], pos[b][1]], mode="lines",
                          line=dict(width=1.2 + 6.0 * frac, color="#1D9E75"), opacity=0.22 + 0.5 * frac,
                          hoverinfo="none"))
    for j in far:                                     # faint spokes to embedding-opposites
        fig.add_trace(go.Scatter(x=[0, pos[j][0]], y=[0, pos[j][1]], mode="lines",
                      line=dict(width=1, color="#E63946", dash="dot"), opacity=0.32, hoverinfo="none"))
    def _hov(j):
        return (f"{F['nodes'][j]} · cosine {COS[i, j]:+.2f} (used in similar contexts) · "
                f"together {int(co[i, j])}× vs ~{E[i, j]:.0f} by chance")
    fig.add_trace(go.Scatter(x=[pos[j][0] for j in near], y=[pos[j][1] for j in near], mode="markers+text",
        text=[disp_root(F["nodes"][j]) for j in near], textposition="top center",
        textfont=dict(size=13, color="#0b3b2e", family="Amiri,serif"),
        marker=dict(size=[13 + (f[j] ** 0.5) * 0.6 for j in near],
                    color=[COS[i, j] for j in near], colorscale=[[0, "#EAF7F1"], [1, "#1D9E75"]],
                    cmin=0.0, cmax=max(COS[i, j] for j in near), line=dict(width=1.4, color="#1D9E75")),
        hovertext=[_hov(j) for j in near], hoverinfo="text"))
    if far:
        fig.add_trace(go.Scatter(x=[pos[j][0] for j in far], y=[pos[j][1] for j in far], mode="markers+text",
            text=[disp_root(F["nodes"][j]) for j in far], textposition="top center",
            textfont=dict(size=12, color="#7a1620", family="Amiri,serif"),
            marker=dict(size=[11 + (f[j] ** 0.5) * 0.5 for j in far], color="#FBE0E3",
                        line=dict(width=1.2, color="#E63946")),
            hovertext=[_hov(j) for j in far], hoverinfo="text"))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers+text", text=[disp_root(concept)], textposition="middle center",
        textfont=dict(size=18, color="#ffffff", family="Amiri,serif"),
        marker=dict(size=46, color="#1D3557", line=dict(width=2, color="#ffffff")),
        hovertext=[f"{concept} · appears in {int(f[i])} āyāt"], hoverinfo="text"))
    fig.update_layout(height=600, showlegend=False, margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("<div style='font-size:13px;color:#10243A;margin:2px 0'>"
        "Placed and linked by <b>embedding cosine</b> — nearness = used in similar contexts. "
        "<span style='color:#1D9E75'>●</span> near (greener &amp; closer = more alike; <b>edge thickness = cosine</b>) "
        "&nbsp;&nbsp; <span style='color:#E63946'>●</span> opposite (negative cosine, dotted)</div>",
        unsafe_allow_html=True)
    _fr = F.get("freq_rho", float("nan"))
    _frtxt = (f"<b>Frequency check:</b> across the whole embedding, similarity↔frequency Spearman ρ = "
              f"{_fr:+.2f} — ≈0 means the cosine is <b>not</b> frequency-anchored (raw SVD would be ρ≈+0.87; "
              f"mean-centring removes it). The <i>together</i> & <i>freq</i> columns are frequency-driven by nature, "
              f"so sorting by them floats common roots up — sort by <i>cosine</i> for the embedding signal."
              if _fr == _fr else "")
    st.caption("Embedding = SVD-of-PPMI (the count-based word2vec; Levy & Goldberg 2014) — apt for a corpus this size, "
        "where neural word2vec is unstable. Relation strength = cosine, shown three ways: distance, dot colour, "
        "edge thickness. ‘Together’ in the table is literal co-occurrence — corroboration, a different signal.")
    if _frtxt:
        st.markdown(f"<div style='font-size:12px;color:#10243A;background:#EAF2FB;border:1px solid #CFE0F2;"
                    f"border-radius:8px;padding:6px 10px;margin:2px 0 8px'>{_frtxt}</div>", unsafe_allow_html=True)
    near_t = [j for j in np.argsort(-COS[i]) if j != i][:22]
    far_t = [j for j in np.argsort(COS[i]) if j != i][:8]
    cmaxn = max((COS[i, j] for j in near_t), default=1.0) or 1.0
    cminf = min((COS[i, j] for j in far_t), default=-1.0) or -1.0
    fc = max(int(f[i]), 1)
    rows = []
    for rel, js in [("near", near_t), ("opposite", far_t)]:
        for j in js:
            lift = (co[i, j] / E[i, j]) if E[i, j] > 0 else 0.0
            share = 100.0 * co[i, j] / fc
            rows.append((F["nodes"][j], rel, float(COS[i, j]), float(PMI[i, j]), float(lift),
                         int(co[i, j]), float(E[i, j]), float(defz[i, j]), share, int(f[j])))
    heads = ["#", "root", "rel.", "cosine ↓", "PMI", "lift", "together", "exp.", "z", "share", "freq"]
    al = ["right", "left", "left", "left", "right", "right", "right", "right", "right", "right", "right"]
    cw = [3, 9, 6, 23, 7, 7, 9, 7, 7, 8, 7]
    colg = "".join(f"<col style='width:{w}%'>" for w in cw)
    th = "".join(f"<th style='padding:5px 8px;font-size:12px;color:#1D3557;font-weight:700;"
                 f"border-bottom:2px solid #C9D6E8;text-align:{al[k]}'>{c}</th>" for k, c in enumerate(heads))
    trs = ""
    for n, (name, rel, cos, pmi, lift, obs, exp, z, share, frq) in enumerate(rows):
        bg = "#FFFFFF" if n % 2 == 0 else "#FAFBFD"
        isn = rel == "near"
        rc = "#1D9E75" if isn else "#E63946"
        barw = max(3, int(100 * (cos / cmaxn if isn else (cos / cminf if cminf < 0 else 0))))
        num = "padding:4px 8px;text-align:right;font-size:12px;color:#10243A"
        bar = (f"<div style='display:flex;align-items:center;gap:8px'>"
               f"<span style='min-width:36px;font-size:12px;font-weight:700;color:#10243A'>{cos:+.2f}</span>"
               f"<div style='flex:1;background:#EEF2F6;border-radius:5px'>"
               f"<div style='background:{rc};height:9px;width:{barw}%;border-radius:5px'></div></div></div>")
        trs += (f"<tr style='background:{bg}'>"
                f"<td style='padding:4px 8px;font-size:12px;color:#10243A;text-align:right'>{n + 1}</td>"
                f"<td style='padding:4px 8px;font-family:Amiri,serif;font-size:15px;color:#10243A'>{name}</td>"
                f"<td style='padding:4px 8px;font-size:12px;font-weight:600;color:{rc}'>{rel}</td>"
                f"<td style='padding:4px 8px'>{bar}</td>"
                f"<td style='{num}'>{pmi:+.2f}</td><td style='{num}'>{lift:.2f}×</td>"
                f"<td style='{num}'>{obs}</td><td style='{num}'>{exp:.1f}</td>"
                f"<td style='{num}'>{z:+.1f}</td><td style='{num}'>{share:.0f}%</td>"
                f"<td style='{num}'>{frq}</td></tr>")
    st.markdown(f"<div style='border:1px solid #E2E8F1;border-radius:8px;overflow:hidden'>"
                f"<table style='width:100%;table-layout:fixed;border-collapse:collapse'><colgroup>{colg}</colgroup>"
                f"<thead><tr style='background:#F4F9F7'>{th}</tr></thead><tbody>{trs}</tbody></table></div>",
                unsafe_allow_html=True)
    _csv = "concept,relation,cosine,PMI,lift,together_obs,expected,z_cooccur,share_pct,freq\n" + "\n".join(
        f"{r[0]},{r[1]},{r[2]:.3f},{r[3]:.3f},{r[4]:.3f},{r[5]},{r[6]:.2f},{r[7]:.2f},{r[8]:.1f},{r[9]}" for r in rows)
    st.download_button("⬇️ Download neighbours (CSV)", _csv.encode("utf-8-sig"),
                       file_name=f"{concept}_embedding_neighbours.csv", mime="text/csv", key="atlas_egocsv")

# preset semantic axes — anchor pairs (negative side, positive side); resolved against the vocab.
# NB root-level: roots like کثر (→ worldly تكاثر vs divine كوثر) are blurred; axes are directional, not exact.
AXES = {
    "Good ↔ Evil": [("هدی", "ضلل"), ("نور", "ظلم"), ("رحم", "عذب"), ("صلح", "سوء"), ("جنن", "جهنم"), ("صدق", "کذب")],
    "World ↔ Hereafter": [("دنو", "ءخر"), ("حيی", "موت")],
}

def _resolve(S, w):
    return S["norm_index"].get(normalize_letters(w))

def _axis_vec(S, pairs):
    offs = []
    for g, b in pairs:
        gk, bk = _resolve(S, g), _resolve(S, b)
        if gk and bk: offs.append(S["V"][S["ni"][bk]] - S["V"][S["ni"][gk]])
    if not offs:
        return None, 0
    ax = np.mean(offs, 0); ax /= np.linalg.norm(ax) + 1e-9
    return ax, len(offs)

def figure(d, color_by, focus=None, dim3=False):
    pos = d["pos3"] if dim3 else d["pos"]
    nodes, docf = d["nodes"], d["docf"]
    _themed = focus is not None and color_by == "Theme"
    _tcol = THEME_COLORS[focus % len(THEME_COLORS)] if _themed else "#cfd8dc"
    ex, ey, ez = [], [], []          # other (grey) edges
    tx, ty, tz = [], [], []          # focused-theme edges (coloured like its nodes)
    for a, b, _w in d["edges"]:
        _in = _themed and d["theme_of"][a] == focus and d["theme_of"][b] == focus
        X, Y = (tx, ty) if _in else (ex, ey)
        X += [pos[a][0], pos[b][0], None]; Y += [pos[a][1], pos[b][1], None]
        if dim3:
            (tz if _in else ez).extend([pos[a][2], pos[b][2], None])
    if dim3:
        edge_tr = go.Scatter3d(x=ex, y=ey, z=ez, mode="lines", line=dict(width=1.2, color="#cfd8dc"), opacity=0.45, hoverinfo="none")
        theme_edge_tr = go.Scatter3d(x=tx, y=ty, z=tz, mode="lines", line=dict(width=2.6, color=_tcol), opacity=0.85, hoverinfo="none") if tx else None
    else:
        edge_tr = go.Scatter(x=ex, y=ey, mode="lines", line=dict(width=0.6, color="#cfd8dc"), hoverinfo="none")
        theme_edge_tr = go.Scatter(x=tx, y=ty, mode="lines", line=dict(width=1.6, color=_tcol), opacity=0.9, hoverinfo="none") if tx else None
    xs = [pos[n][0] for n in nodes]; ys = [pos[n][1] for n in nodes]
    zs = [pos[n][2] for n in nodes] if dim3 else None
    sizes = [6 + (docf[n] ** 0.5) * 0.9 for n in nodes]
    top40 = set(nodes)   # label every node (was top-40 by frequency; user wants all labels)
    texts = [disp_root(n) if n in top40 else "" for n in nodes]
    gf = d.get("gf", {})
    if color_by == "Theme":
        colors = [THEME_COLORS[d["theme_of"][n] % len(THEME_COLORS)] for n in nodes]
        if focus is not None:                       # dim everything except the focused theme
            colors = [colors[i] if d["theme_of"][n] == focus else "#dce4e7" for i, n in enumerate(nodes)]
            texts = [disp_root(n) if (d["theme_of"][n] == focus and n in top40) else "" for n in nodes]
        marker = dict(size=sizes, color=colors, line=dict(width=0.5, color="#ffffff"))
    elif color_by == "Network role":               # banked graph finding: bridge / hub / member
        colors = [ROLE_COLOR.get((gf.get(normalize_letters(n)) or {}).get("role"), "#9FB3C8") for n in nodes]
        marker = dict(size=sizes, color=colors, line=dict(width=0.5, color="#ffffff"))
    elif color_by == "Semantic axis":              # project concepts onto an anchor-pair direction
        _sc = d.get("axisscore", {})
        vals = [_sc.get(n, 0.0) for n in nodes]
        _m = max((abs(v) for v in vals), default=1.0) or 1.0
        marker = dict(size=sizes, color=vals,
                      colorscale=[[0, "#1D9E75"], [0.5, "#EEEEEE"], [1, "#E63946"]],
                      cmin=-_m, cmax=_m, showscale=True,
                      colorbar=dict(title=d.get("axisname", ""), thickness=12),
                      line=dict(width=0.5, color="#ffffff"))
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
        hov.append(f"{n} · freq {docf[n]} · revelation {d['nuz'][n]:.0f}/114 · family {d['theme_of'][n] + 1}{extra}")
    if dim3:
        node_tr = go.Scatter3d(x=xs, y=ys, z=zs, mode="markers+text", text=texts, textposition="top center",
                               textfont=dict(size=12, color=INK), hovertext=hov, hoverinfo="text", marker=marker)
        fig = go.Figure([t for t in [edge_tr, theme_edge_tr, node_tr] if t is not None])
        fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=660, uirevision="atlas",
                          scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
                                     bgcolor="rgba(0,0,0,0)"), paper_bgcolor="rgba(0,0,0,0)")
    else:
        node_tr = go.Scatter(x=xs, y=ys, mode="markers+text", text=texts, textposition="top center",
                             textfont=dict(size=12, color=INK), hovertext=hov, hoverinfo="text", marker=marker)
        fig = go.Figure([t for t in [edge_tr, theme_edge_tr, node_tr] if t is not None])
        fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=650, dragmode="pan", uirevision="atlas",
                          xaxis=dict(visible=False), yaxis=dict(visible=False),
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig

hero("🗺️ Concept Atlas",
     "The conceptual territory as a map — roots linked by attraction, grouped into families, sized by "
     "frequency. Each node is a root; a curated concept can bundle several roots (see the concept profile up top). "
     "Scope it to the whole Qur'ān, a single sūra, or a relative-position band. Click any root to open it in Search.")

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
    _note = f"<b>Sūra {_sel} · {SNAME[_sel]}</b> — its <b>internal</b> root families (how this sūra is built)."
elif _scope == "Position band":
    _b = _sc2.selectbox("Relative band (pooled across all sūras)", list(range(5)),
                        format_func=lambda b: BANDS[b], key="atlas_band")
    d = build_atlas(id(corpus), "band", _b)
    _note = (f"<b>{BANDS[_b]} band</b> — verses at this relative position, pooled across all sūras. "
             "⚠️ <b>[DIVINE-ALT]</b> — an alternative re-indexing, not the muṣḥaf's primary order.")
else:
    d = build_atlas(id(corpus), "all")
    _note = "The <b>whole Qur'ān</b>'s conceptual territory."
_map_ok = len(d.get("nodes", [])) >= 4   # very short sūras can't form a graph — skip the MAP, keep the companions
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
"""**The core idea.** Each **root** is a node; an **edge** joins two roots that co-occur more than chance (PPMI); **colour** = the **family** each root falls into. (A curated **concept** can bundle several roots — قلب·صدر·فؤاد = the heart — and lives in the *concept profile* at the top.) The *same* engine drives every view below.

**Scope — three lenses on the concept web (the radio at the top):**
- **1 · Whole Qur'ān — the territory.** Every major root across all 6,236 āyāt, grouped into **families**, with the roots that **bridge** them. The master map; everything else is a zoom or a companion. *Takeaway: the vocabulary self-organises into a few coherent families.*
- **2 · A sūra — how one chapter is built.** The same graph from one sūra's verses → its **internal families**; for narratives these track the **episodes** (Yūsuf: plot · temptation · prison · reunion). *Takeaway: a chapter's skeleton is latent in its own root co-occurrence.*
- **3 · Position band — the shape of a sūra. ⚠️ [DIVINE-ALT].** Verses pooled by *where* they fall (opening→closing) across all sūras: **doxology frames the edges, exhortation closes, narrative fills the body.** An alternative re-indexing, never the muṣḥaf's primary order.

**Companion views (same data, a different question):**
- **The 114 sūras as a semantic map** (Whole scope) — each sūra is a **point**, distance ≈ vocabulary similarity; **families** emerge (one ≈ 88% Medinan, found with no labels). The **family-metrics table** gives each family's cohesion, separation, silhouette (tight vs loose), revelation tilt and defining concepts.
- **A sūra's semantic footprint** (A-sūra scope) — *where* that sūra's distinctive concepts sit in the whole meaning-space, with a **concentration score** (legal sūras tight, narrative/hymn scattered).
- **Most related sūras / mutual elaboration** (A-sūra scope) — for a sūra, the sūras most alike in **whole-vocabulary** profile (symmetric cosine, so the relation is mutual), with each pair's **shared distinctive concepts** and a marker for which side has more room to develop the shared material.
- **The data table** — every root with frequency and the full **centrality suite** (degree, betweenness, closeness, eigenvector, PageRank, clustering) plus family, revelation and top partners — sortable, copyable, Arabic-safe CSV.

**How to read it together.** Move **outward → inward**: the whole territory → one chapter's build → its opening-to-closing shape; and **macro → micro**: which sūras are alike (the 114-map) → where one sūra's concepts live (footprint) → the exact numbers (table).

**Honest scope.** Everything is **measured** (attraction, communities, centralities, MDS) and presented as a **navigation map, not a claim**. Bands and footprints are *exploratory* (DIVINE-ALT / approximate 2-D); necessity is never asserted.""")

_concept_slot = st.container()   # THE CONCEPT PROFILE renders into here (top of page, above the map); its code lives near the file end where centralities are computed
if not _map_ok:
    st.info("This sūra is too short to draw its own concept map — but its sūra-level views below "
            "(semantic footprint and the sūras that elaborate it) still work. Pick a longer sūra for the map.")
else:
    _loc = st.session_state.pop("_atlas_locate", None)   # ← set by the concept profile's "Locate on the map" button
    if _loc is not None and _loc in d["theme_of"]:
        st.session_state["atlas_color"] = "Theme"
        _lt = d["theme_of"][_loc]
        st.session_state["atlas_focus"] = "Family %d: %s" % (_lt + 1, " · ".join(disp_root(t) for t in d["themes"][_lt][2]))
    layer(1, "🗺️ The map — roots as a web")
    c1, c2, c3 = st.columns(3)
    c1.metric("Roots mapped", len(d["nodes"]))
    c2.metric("Attraction links", len(d["edges"]))
    c3.metric("Families", len(d["themes"]))
    cc1, cc2 = st.columns([1, 1.4])
    color_by = cc1.radio("Map mode", ["Theme", "Revelation phase", "Network role", "Around a concept"],
                         horizontal=True, key="atlas_color",
                         format_func=lambda x: {"Theme": "Family", "Around a concept": "Around a root"}.get(x, x),
                         help="The first three colour the whole territory. 'Around a root' zooms to one root's field.")
    _focus = None
    if color_by == "Around a concept":
        _F = _field_space(id(corpus))
        _here = {normalize_letters(n) for n in d["nodes"]}
        _vocab = [n for n in _F["nodes"] if normalize_letters(n) in _here] or _F["nodes"]
        _vocab = sorted(_vocab, key=lambda r: normalize_letters(r))     # alphabetical — easy to browse/scan
        _dft = next((w for w in ("قلب", "رحم", "کفر") if w in _vocab), _vocab[0])
        st.markdown("<style>.st-key-atlas_concept{max-width:520px}</style>", unsafe_allow_html=True)
        _csel = cc2.selectbox("Pick a root (its embedding neighbourhood — roots used in similar contexts)",
                              _vocab, index=_vocab.index(_dft), key="atlas_concept", format_func=disp_root)
        _ego_view(_F, _csel)
    else:
        _theme_labels = ["— whole map —"] + [f"Family {ti + 1}: {' · '.join(disp_root(t) for t in top)}" for ti, _o, top in d["themes"]]
        _focus_sel = cc2.selectbox("Focus a family", _theme_labels, key="atlas_focus",
                                   disabled=(color_by != "Theme"), help="Family focus applies to the Family colouring.")
        _focus = None if _focus_sel.startswith("—") else _theme_labels.index(_focus_sel) - 1
        _dim3 = st.radio("View", ["2-D (read)", "3-D (rotate)"], horizontal=True, key="atlas_dim",
                         label_visibility="collapsed").startswith("3")
        st.plotly_chart(figure(d, color_by, _focus, _dim3), use_container_width=True,
                        config={"scrollZoom": True, "displaylogo": False})
        if color_by == "Network role":
            _nb = sum(1 for n in d["nodes"] if (d["gf"].get(normalize_letters(n)) or {}).get("role") == "connector / bridge")
            _nh = sum(1 for n in d["nodes"] if (d["gf"].get(normalize_letters(n)) or {}).get("role") == "family anchor (hub)")
            st.markdown("<div style='font-size:12px;color:#10243A;margin:2px 0 0'>"
                        f"<span style='color:#E63946'>●</span> bridge — connector across families ({_nb}) &nbsp;&nbsp;"
                        f"<span style='color:#EF9F27'>●</span> family anchor — hub ({_nh}) &nbsp;&nbsp;"
                        "<span style='color:#9FB3C8'>●</span> member"
                        "<br>Roles are a <b>banked graph finding</b> (degree-normalised betweenness for bridges, "
                        "dcSBM within-family hubs) — precomputed, not a runtime claim.</div>", unsafe_allow_html=True)
        st.caption("Edges = above-chance pairings (PPMI) only — each root's strongest 3 partners. "
                   "Families are auto-grouped (Louvain); a navigation map, not a structural claim.")

    # ── FAMILY SIZES — ranked bar chart (shared landscape.py helper) ──
    layer(2, "📊 Family sizes — the families, ranked")
    with st.expander("What this shows — open me", expanded=True):
        st.markdown(
            "<div style='font-size:14px;color:#10243A;line-height:1.65'>"
            "<b>The idea.</b> The map above shows the families as colour; here they are <b>ranked</b> — one <b>bar per "
            "family</b> (labelled by its top root), its length = a measured quantity you pick below: <b>breadth</b> "
            "(how many roots), <b>weight</b> (how much text they fill), or <b>cohesion</b> (how tightly they "
            "interlink). So you see at a glance which families dominate and how lopsided the set is.</div>"
            "<div style='font-size:14px;color:#10243A;line-height:1.65;margin-top:6px'>"
            "<b>Which roots are here — NOT every root.</b> To stay legible this covers only the <b>most frequent "
            "content roots</b> of the current scope (the same nodes as the map above) — for a sūra the top ~90, for "
            "the whole Qur’ān ~150. It is <b>not the full inventory</b>: ubiquitous ‘glue’ roots (God · say · all) "
            "are dropped as uninformative, and rare one-off roots aren’t shown. The <b>“Roots mapped”</b> number at "
            "the top of the page is exactly how many appear here — so for al-Baqarah you see its leading roots "
            "grouped into families, not its entire vocabulary.</div>"
            "<div style='font-size:14px;color:#10243A;line-height:1.65;margin-top:6px'>"
            "<b>How to read it.</b> Bars are <b>ranked longest-first</b>, so the top bar is the biggest family on the "
            "chosen metric. <b>Zoom to one family</b> switches the chart to that family’s <b>roots</b>, each a bar "
            "whose length is how many verses it appears in. Hover any bar for details; the table below has every "
            "family’s exact numbers.</div>"
            "<div style='font-size:14px;color:#10243A;line-height:1.65;margin-top:6px'>"
            "<b>What to look for — the significance.</b> <b>Switch the metric</b> to ask three questions of the SAME "
            "families: which is the <b>widest</b> (breadth), which carries the <b>most text</b> (weight), which is the "
            "<b>most tightly-knit</b> (cohesion). A family can rank high on one and low on another — a <b>broad but "
            "loose</b> family (many roots, few bonds) vs a <b>small but dense</b> one — and that contrast is the "
            "insight.</div>"
            "<div style='font-size:14px;color:#10243A;line-height:1.65;margin-top:6px'>"
            "<b>Honest reading.</b> All values are <b>MEASURED</b>; families are auto-grouped (Louvain). A navigation "
            "aid, not a structural claim.</div>",
            unsafe_allow_html=True)
    with st.expander("Where the data comes from & how the families are made — read me"):
        st.markdown(
            "<div style='font-size:14px;color:#10243A;line-height:1.65'>"
            "<b>The data.</b> Every verse in the current scope is a bag of roots; two roots get a <b>bond</b> when they "
            "co-occur <b>far above chance</b> (PPMI, which controls for how common each one is). It is all "
            "<b>measured</b> from the text — nothing is imposed by hand.</div>"
            "<div style='font-size:14px;color:#10243A;line-height:1.65;margin-top:6px'>"
            "<b>How the families are made.</b> A <b>community-detection</b> algorithm (Louvain) groups roots that bond "
            "tightly into families, each named by its most central root. The grouping is <b>measured</b> (real structure "
            "vs a random baseline), but the <b>exact number of families is not an absolute</b> — a different setting "
            "shifts a few borderline roots or changes the count by one or two. Read it as a good map, not a fixed "
            "number.</div>"
            "<div style='font-size:14px;color:#10243A;line-height:1.65;margin-top:6px'>"
            "<b>Coverage &amp; sizes.</b> As noted above, only the top ~90 (a sūra) / ~150 (whole Qur’ān) most frequent "
            "content roots are mapped — not every root. And families come out <b>unequal in size</b>; the “roots in "
            "the family” bars report exactly that.</div>",
            unsafe_allow_html=True)
    _PALA = ["#1D9E75", "#378ADD", "#7209B7", "#EF9F27", "#0F6E56", "#138A74", "#B5651D", "#94A3B8", "#E63946", "#1D3557", "#8a5a16", "#534AB7"]
    _hubA = {ti: disp_root(o[0]) for ti, o, _t in d["themes"]}
    _lcA = st.columns([2, 2])
    with _lcA[0]:
        _lh = st.radio("Rank families by", ["concepts in the theme", "total occurrences", "internal density"],
                       horizontal=True, key="atlas_land_h",
                       format_func=lambda x: x.replace("theme", "family").replace("concepts", "roots"))
    with _lcA[1]:
        _lz = st.selectbox("Zoom to one family — or see all", ["All themes"] + [_hubA[ti] for ti, _o, _t in d["themes"]],
                           key="atlas_land_z", format_func=lambda x: "All families" if x == "All themes" else x)
    _docfA = d["docf"]; _edgesA = d["edges"]
    def _hvalA(mem):
        if _lh.startswith("total"):
            return float(sum(_docfA.get(m, 0) for m in mem))
        if _lh.startswith("internal"):
            ms = set(mem); k = len(ms)
            if k < 2:
                return 0.0
            ec = sum(1 for a, b, _w in _edgesA if a in ms and b in ms)
            return ec / (k * (k - 1) / 2.0) * 10.0
        return float(len(mem))
    _MEXPLA = {
        "concepts in the theme": "<b>breadth</b> — how many roots the family holds (wide-ranging vs small and focused).",
        "total occurrences": "<b>weight</b> — how often the family’s roots occur across the Qur’ān (a frequently-invoked family).",
        "internal density": "<b>cohesion</b> — how tightly the family’s roots interlink (share of the possible bonds present).",
    }
    st.markdown("<div style='font-size:13.5px;color:#10243A;margin:2px 0 4px'><b>Bar length = %s</b> — %s</div>"
                % (_lh.replace("theme", "family").replace("concepts", "roots"), _MEXPLA[_lh]), unsafe_allow_html=True)
    _famA = [{"id": ti, "hub": _hubA[ti], "color": _PALA[ti % len(_PALA)], "members": list(o), "hval": _hvalA(o)}
             for ti, o, _t in d["themes"]]
    _nodesA = {r: {"label": disp_root(r), "full": disp_root(r), "size": _docfA.get(r, 1),
                   "hover": "%s · %d verses" % (disp_root(r), _docfA.get(r, 0))} for r in d["nodes"]}
    _surfA = LS.family_landscape(_famA, _nodesA, height_label=_lh,
                                 zoom_hub=(None if _lz == "All themes" else _lz),
                                 trace=None, edges=[(a, b) for a, b, _w in _edgesA])
    st.plotly_chart(_surfA, use_container_width=True, config={"scrollZoom": True, "displaylogo": False})
    _cov = d.get("coverage"); _nall = d.get("n_all_roots"); _modq = d.get("modularity")
    _totment = d.get("total_mentions")
    _covtxt = ("~%.0f%%" % (100 * _cov)) if _cov is not None else "—"
    _modtxt = ("%.2f" % _modq) if (_modq is not None and _modq == _modq) else "—"
    _fsz = [len(o) for _ti, o, _t in d["themes"]]
    # internal/bridge bonds per theme — built once, reused by the glance table AND the comprehensive table
    _intraA = Counter(); _interA = Counter()
    for _a, _b, _w in d["edges"]:
        _ta = d["theme_of"].get(_a); _tb = d["theme_of"].get(_b)
        if _ta is None or _tb is None:
            continue
        if _ta == _tb:
            _intraA[_ta] += 1
        else:
            _interA[_ta] += 1; _interA[_tb] += 1
    # Map at a glance — DYNAMIC: whole-scope when "All themes", else the zoomed family's own numbers
    _selti = next((ti for ti, _o, _t in d["themes"] if _hubA[ti] == _lz), None) if _lz != "All themes" else None
    if _selti is not None:
        _so = next(o for ti, o, _t in d["themes"] if ti == _selti)
        _sn = len(_so); _socc = int(sum(_docfA.get(m, 0) for m in _so))
        _sib = _intraA.get(_selti, 0); _sbr = _interA.get(_selti, 0)
        _sdens = round(_sib / (_sn * (_sn - 1) / 2), 3) if _sn > 1 else 0.0
        _scovt = ("~%.1f%%" % (100 * _socc / _totment)) if _totment else "—"
        _smapt = "~%.0f%%" % (100 * _sn / max(len(d["nodes"]), 1))
        _atheading = "“%s” at a glance — the one family you’ve zoomed to" % _lz
        _atrows = [
            ("Family", _lz, "the family in view — named by its top (most frequent) root"),
            ("Roots in it", str(_sn), "how many roots this family holds — its breadth"),
            ("Total occurrences", str(_socc), "how often this family’s roots occur across the scope — its weight"),
            ("Coverage of scope", _scovt, "share of ALL this scope’s root-mentions that this one family accounts for"),
            ("Share of the map", _smapt, "this family’s slice of the %d roots shown on the map" % len(d["nodes"])),
            ("Cohesion (internal density)", "%.3f" % _sdens, "how tightly its own roots interlink — share of possible bonds present"),
            ("Internal / bridge bonds", "%d / %d" % (_sib, _sbr), "links inside the family vs links reaching out to other families"),
        ]
    else:
        _atheading = "Map at a glance — read this so the numbers aren’t misread"
        _atrows = [
            ("Distinct roots in scope", (str(_nall) if _nall else "—"), "the full content vocabulary of this scope"),
            ("Roots mapped", str(len(d["nodes"])), "the most frequent ones — what you actually see here"),
            ("Coverage", _covtxt, "share of this scope’s root-mentions the mapped roots cover — the rest are "
             "ubiquitous ‘glue’ roots (dropped) and a long tail of rare roots (not shown)"),
            ("Families", str(len(d["themes"])), "measured groups — a good map, <b>not a fixed count</b> "
             "(a different setting gives a few more or fewer)"),
            ("Grouping strength (modularity)", _modtxt, "how cleanly the families separate — above ~0.30 = clear, real "
             "structure, not random"),
            ("Biggest / smallest family", ("%d / %d" % (max(_fsz), min(_fsz)) if _fsz else "—"),
             "roots per family — shows how lopsided the split is"),
        ]
    _th = "text-align:left;padding:6px 11px;border:1px solid #CFE0F2;font-weight:800;background:#EAF2FB"
    _td = "padding:6px 11px;border:1px solid #E2E8F1;vertical-align:top"
    _html = ("<div style='font-size:14px;color:#1D3557;font-weight:800;margin:10px 0 3px'>%s</div>" % _atheading +
             "<table style='border-collapse:collapse;width:100%%;font-size:13.5px;color:#10243A'>"
             "<tr><th style='%s'>Metric</th><th style='%s'>Value</th><th style='%s'>What it means</th></tr>" % (_th, _th, _th))
    for _m, _v, _w in _atrows:
        _html += "<tr><td style='%s'><b>%s</b></td><td style='%s'>%s</td><td style='%s'>%s</td></tr>" % (_td, _m, _td, _v, _td, _w)
    st.markdown(_html + "</table>", unsafe_allow_html=True)
    # comprehensive per-theme table — full width, headers wrap to 2 lines (LS.html_table) so no stretched-empty columns
    _pkrows = []
    for ti, o, _t in d["themes"]:
        _n = len(o); _occ = int(sum(_docfA.get(m, 0) for m in o)); _ib = _intraA.get(ti, 0)
        _pkrows.append([
            _hubA[ti], _n, _occ, int(round(_occ / max(_n, 1))),
            "%.3f" % (round(_ib / (_n * (_n - 1) / 2), 3) if _n > 1 else 0.0),
            _ib, _interA.get(ti, 0), "%.2f" % round(2 * _ib / max(_n, 1), 2),
            " · ".join(disp_root(x) for x in o[:8]),
        ])
    _pkrows.sort(key=lambda r: r[1], reverse=True)
    _pkhdr = ["family (top root)", "roots (breadth)", "total occurrences (weight)", "avg occ / root",
              "internal density (cohesion)", "internal bonds", "bridge bonds (out)", "avg degree (within)", "top roots"]
    with st.expander("🔬 Per-family detail table (breadth · weight · cohesion · connectivity)", expanded=False):
        st.markdown(LS.html_table(_pkhdr, _pkrows, num_cols={1, 2, 3, 4, 5, 6, 7}, wide_col=8), unsafe_allow_html=True)
        st.caption("Every family with all three ranking metrics side by side (breadth · weight · cohesion) plus its "
                   "connectivity — internal bonds, bridge bonds to other families, and within-family average degree. "
                   "Sorted by breadth; “Zoom to one family” above shows that family’s roots as bars.")

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
    layer(3, "🧭 Where this sūra sits in the Qur'ān's meaning-space (semantic footprint)")
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
                                   mode="markers+text", text=[disp_root(_S["nodes"][i]) for i in _idx],
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
        st.caption(f"Grey = the whole Qur'ān's roots (faint backdrop); green = this sūra's distinctive roots. "
                   f"**Concentration z = {_z:+.1f}** → the footprint is {_verdict}. "
                   "Semantic distance is from corpus-wide co-occurrence (validated z+3.6); the 2-D projection is approximate.")
    else:
        st.caption("Too few distinctive roots in the semantic space to map this sūra's footprint.")

# ---- thematic elaborators: which sūras most resemble THIS one by whole-vocabulary profile (df≥2 roots) ----
if _scope == "A sūra":
    _Qs = _sura_space(id(corpus))
    _SIM = _Qs.get("SIM"); _tlen = _Qs.get("tlen", {})
    if _SIM is not None and _sel in _Qs["suras"]:
        _si = _Qs["suras"].index(_sel)
        _row = _SIM[_si]
        _ord = [(_Qs["suras"][b], float(_row[b]), _tlen.get(_Qs["suras"][b], 0))
                for b in np.argsort(-_row) if _Qs["suras"][b] != _sel]
        _topc = _ord[0][1] if _ord else 0.0
        layer(4, "🧭 Most related sūras (mutual) — by whole-vocabulary similarity")
        st.caption("⤷ Sūra-level companion (the maps above are the *root* territory). Similarity is "
                   "**symmetric** — these sūras and the one you picked elaborate *each other*; the relation arrow only "
                   "marks which side has more room to develop the shared material.")
        _self_len = _tlen.get(_sel, 0) or 1
        _E = _elab_engine(id(corpus)); _dist = _E["DIST"].get(_sel, [])
        _top = _ord[:8]
        def _rel(ln):
            r = ln / _self_len
            if r >= 1.5: return "→ more room", "#0F6E56"
            if r <= 0.67: return "← you elaborate it", "#1D3557"
            return "↔ peer", "#10243A"
        _heads = ["rank", "sūra", "similarity", "length (roots)", "relation", "shared distinctive concepts"]
        _eh = "".join(f'<th style="background:#1D3557;color:#fff;padding:7px 12px;text-align:right;'
                      f'font-size:12px;white-space:nowrap">{h}</th>' for h in _heads)
        _er = ""
        _td = "padding:5px 12px;border-top:1px solid #EEF2F7;text-align:right;white-space:nowrap"
        for _rk, (L, _co, _ln) in enumerate(_top, 1):
            _rl, _rcol = _rel(_ln)
            _sh = " · ".join(disp_root(r) for r in _dist if r in _E["present"].get(L, set())) or "—"
            _er += (f'<tr><td style="{_td}">{_rk}</td>'
                    f'<td style="{_td};font-family:Amiri,serif">{SNAME.get(L, L)} ({L})</td>'
                    f'<td style="{_td};font-weight:700">{_co:.2f}</td>'
                    f'<td style="{_td}">{_ln}</td>'
                    f'<td style="{_td};color:{_rcol};font-weight:600">{_rl}</td>'
                    f'<td style="{_td};font-family:Amiri,serif">{_sh}</td></tr>')
        # content-sized table (no width:100%) → columns hug their content, zero internal gaps; box hugs the table
        st.markdown('<div style="overflow:auto;max-width:100%;display:inline-block;vertical-align:top;'
                    'border:1px solid #E2E8F1;border-radius:10px">'
                    '<table style="border-collapse:collapse;font-size:13px;color:#10243A">'
                    f'<thead><tr>{_eh}</tr></thead><tbody>{_er}</tbody></table></div>', unsafe_allow_html=True)
        _conf = ("⚠️ Weak signal — this sūra's vocabulary barely overlaps any other; treat as low-confidence. "
                 if _topc < 0.10 else "")
        st.caption(f"{_conf}Similarity = cosine of the two sūras' tf-idf vocabulary profiles (roots in ≥2 sūras only; "
                   "single-sūra roots can't be shared). It is **symmetric**, so the relationship is mutual — every pair "
                   "shares some vocabulary, making this a continuum of degree, not a one-way claim. The ‘relation’ "
                   "column compares lengths: a much longer partner simply has more room to develop the shared material.")
        with st.expander("🔬 Substantiate it — raw root-count vs similarity, side by side (exportable)"):
            _Rin = _Qs["rootsets"].get(_sel, set())
            _raw = sorted(((L, len(_Rin & _Qs["rootsets"][L]), _tlen.get(L, 0))
                           for L in _Qs["suras"] if L != _sel), key=lambda t: (-t[1], -t[2]))
            _ovv = np.array([t[1] for t in _raw], float); _lnn = np.array([t[2] for t in _raw], float)
            _simc = np.array([t[1] for t in _ord], float); _siml = np.array([t[2] for t in _ord], float)
            _rr = float(np.corrcoef(_ovv, _lnn)[0, 1]) if _ovv.std() and _lnn.std() else 0.0
            _rs = float(np.corrcoef(_simc, _siml)[0, 1]) if _simc.std() and _siml.std() else 0.0
            _hd = "".join(f'<th style="background:#1D3557;color:#fff;padding:6px 9px;font-size:12px;text-align:{a}">{h}</th>'
                          for h, a in [("rank", "right"), ("RAW count → sūra", "left"), ("len", "right"), ("shared", "right"),
                                       ("SIMILARITY → sūra", "left"), ("cos", "right"), ("len", "right")])
            _bd = ""
            for _k in range(min(5, len(_raw), len(_ord))):
                L1, sh1, ln1 = _raw[_k]; L2, c2, ln2 = _ord[_k]
                bt = "border-top:1px solid #EEF2F7"
                _bd += (f'<tr><td style="padding:5px 9px;{bt};text-align:right">{_k+1}</td>'
                        f'<td style="padding:5px 9px;{bt};font-family:Amiri,serif">{SNAME.get(L1,L1)} ({L1})</td>'
                        f'<td style="padding:5px 9px;{bt};text-align:right">{ln1}</td>'
                        f'<td style="padding:5px 9px;{bt};text-align:right">{sh1}</td>'
                        f'<td style="padding:5px 9px;{bt};border-left:2px solid #C9D6E8;font-family:Amiri,serif">{SNAME.get(L2,L2)} ({L2})</td>'
                        f'<td style="padding:5px 9px;{bt};text-align:right;font-weight:700">{c2:.2f}</td>'
                        f'<td style="padding:5px 9px;{bt};text-align:right">{ln2}</td></tr>')
            st.markdown('<div style="overflow:auto;max-width:100%;display:inline-block;vertical-align:top;'
                        'border:1px solid #E2E8F1;border-radius:10px">'
                        '<table style="border-collapse:collapse;font-size:13px;color:#10243A">'
                        f'<thead><tr>{_hd}</tr></thead><tbody>{_bd}</tbody></table></div>', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:13px;color:#10243A;margin:6px 0'>For <b>{SNAME.get(_sel,_sel)} ({_sel})</b>: "
                        f"the RAW root-count ranking tracks sūra length at <b>r = {_rr:+.2f}</b> — it returns the longest "
                        f"sūras, and nearly the same list whatever sūra you pick. The SIMILARITY ranking's tie to length "
                        f"is only <b>r = {_rs:+.2f}</b>, and it changes with the input. Same corpus, two methods.</div>",
                        unsafe_allow_html=True)
            _ccsv = "rank,raw_sura,raw_len,raw_shared,similarity_sura,sim_cosine,sim_len\n" + "\n".join(
                f"{k+1},{SNAME.get(_raw[k][0],_raw[k][0])}({_raw[k][0]}),{_raw[k][2]},{_raw[k][1]},"
                f"{SNAME.get(_ord[k][0],_ord[k][0])}({_ord[k][0]}),{_ord[k][1]:.3f},{_ord[k][2]}"
                for k in range(min(5, len(_raw), len(_ord))))
            st.download_button("⬇️ Download comparison (CSV)", _ccsv.encode("utf-8-sig"),
                               file_name=f"elaborator_compare_s{_sel}.csv", mime="text/csv", key="atlas_cmpcsv")

# ---- the 114 sūras as a semantic map (which sūras are alike) — whole-Qur'ān companion view ----
if _scope == "Whole Qur'ān":
    _Q = _sura_space(id(corpus))
    layer(3, "🗺️ The 114 sūras as a semantic map — which sūras are alike")
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
    layer(4, "📊 Cluster metrics — the sūra families")
    _hdr = "".join(
        f'<th style="position:sticky;top:0;background:#1D3557;color:#fff;padding:7px 9px;'
        f'text-align:right;font-size:12px;white-space:nowrap">{h}</th>'
        for h in ["family", "# sūras", "cohesion", "separation", "silhouette",
                  "mean revelation", "mean length", "defining roots", "members"])
    _trs = []
    for _f in _F:
        _col = THEME_COLORS[_f["id"] % len(THEME_COLORS)]
        _mem = " · ".join(SNAME.get(s, str(s)) for s in _f["members"][:14]) + (f" …(+{_f['n'] - 14})" if _f["n"] > 14 else "")
        _cells = [f'<span style="display:inline-block;width:11px;height:11px;border-radius:3px;'
                  f'background:{_col};margin-left:5px"></span> {_f["id"] + 1}',
                  _f["n"], _f["cohesion"], _f["separation"], _f["silhouette"],
                  (_f["mean_nuz"] if _f["mean_nuz"] is not None else "—"), _f["mean_len"],
                  " · ".join(disp_root(c) for c in _f["concepts"]), _mem]
        _tds = "".join(
            f'<td style="padding:5px 9px;border-top:1px solid #EEF2F7;text-align:right;'
            f'{"font-family:Amiri,serif;" if _k in (7, 8) else ""}">{_c}</td>'
            for _k, _c in enumerate(_cells))
        _trs.append(f"<tr>{_tds}</tr>")
    st.markdown('<div style="overflow:auto;max-width:100%;display:inline-block;vertical-align:top;'
                'border:1px solid #E2E8F1;border-radius:10px">'
                '<table style="border-collapse:collapse;font-size:13px;color:#10243A">'
                f'<thead><tr>{_hdr}</tr></thead><tbody>{"".join(_trs)}</tbody></table></div>',
                unsafe_allow_html=True)
    st.caption("Cohesion = mean within-family vocabulary similarity; separation = mean similarity to other families; "
               "silhouette = cohesion − separation (higher = tighter & more distinct). Mean revelation = nuzūl order (early→late).")
    st.markdown(
        "<div style='font-size:13px;color:#10243A;background:#F4F9F7;border:1px solid #cfe4dc;border-radius:8px;"
        "padding:8px 11px;margin-top:6px'><b>How the families were found (plain English):</b> every sūra is turned "
        "into a list of the word-roots it uses, weighted so common roots count less and distinctive ones count more "
        "(roots appearing in only one sūra are dropped). Two sūras are called <i>similar</i> when those lists overlap "
        "(cosine similarity). Each sūra is then linked to its handful of most-similar sūras, and a standard "
        "community-detection step (greedy modularity) keeps the groups whose members link to each other more than to "
        "everyone else. Those groups are the families — numbered 1–5 here. <b>No labels were used</b> (not Meccan/"
        "Medinan, not topic, not length): the grouping emerges only from shared vocabulary, which is why it's notable "
        "that one family turns out ≈88% Medinan on its own.</div>", unsafe_allow_html=True)

if _scope != "Whole Qur'ān":
    if st.button("← Back to the 114-sūra map", key="atlas_back2"):
        st.session_state["_atlas_goto_whole"] = True
        st.session_state["atlas_mapjump"] = 0
        st.session_state["_atlas_lastjump"] = 0
        st.rerun()

# ---- data table behind the map (sortable · scrollable · copyable) ----
if not _map_ok:
    st.stop()   # short sūra: graph-derived data table & themes below need a real map; companions above already shown
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
_clab = {ti: " · ".join(disp_root(t) for t in top) for ti, _o, top in d["themes"]}
_rolemap = {"connector / bridge": "bridge", "family anchor (hub)": "hub"}
_rows = []
for n in d["nodes"]:
    _ti = d["theme_of"][n]
    _role = _rolemap.get((d["gf"].get(normalize_letters(n)) or {}).get("role"), "member")
    _rows.append({"root": disp_root(n), "frequency": d["docf"][n], "family #": _ti + 1,
                  "family": _clab.get(_ti, ""), "role": _role,
                  "degree": _deg.get(n, 0), "degree_cent": round(_degc.get(n, 0.0), 3),
                  "betweenness": round(_bet.get(n, 0.0), 3), "closeness": round(_clo.get(n, 0.0), 3),
                  "eigenvector": round(_eig.get(n, 0.0), 3), "pagerank": round(_pr.get(n, 0.0), 4),
                  "clustering": round(_clu.get(n, 0.0), 3), "revelation 1–114": round(d["nuz"][n]),
                  "top partners": " · ".join(disp_root(p) for p in _partners[n])})
_df = pd.DataFrame(_rows).sort_values(["family #", "frequency"], ascending=[True, False])
layer(5, "📋 Data behind the map — scrollable · copyable (use the CSV below to sort)")
# Full-width HTML table — st.dataframe won't stretch on this Streamlit build, so we control width directly.
_cols = list(_df.columns)
_arab = {"root", "family", "top partners"}
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
"""Each row is one **root** (a node in the web). The columns answer different questions about its place in the web.

**Prominence**
- **frequency** — in how many āyāt (at the current scope) the root appears. *Why:* raw weight — how much of the text it touches.

**Grouping**
- **family # / family** — the group it belongs to (Louvain community), labelled by that group's lead roots. *Why:* which **family of ideas** it lives in.
- **role** — a banked graph role: **bridge** (connects different families), **hub** (anchor of its family), or **member**. *Why:* its structural job in the map.

**Centrality — different senses of "important"**
- **degree** — how many strong (above-chance) partners it links to. *Why:* direct reach — a high-degree root attracts many others.
- **degree_cent** — the same, normalised 0–1 by network size. *Why:* lets you compare across scopes (a sūra vs the whole Qur'ān).
- **betweenness** — how often it lies on the shortest path between other roots. *Why:* a **broker/bridge** — high betweenness means removing it would fragment the map; it links otherwise-separate families.
- **closeness** — how short its average path is to *every* other root. *Why:* **reach** — a high-closeness root is "near everything," touching the whole web quickly.
- **eigenvector** — importance by the *company it keeps* (connected to other well-connected roots). *Why:* **prestige** — embedded among the central, not just busy.
- **pagerank** — a random-walk version of the same idea, robust to quirks. *Why:* where "attention" flows in the web; a stable importance ranking.
- **clustering** — how tightly its own neighbours interlink (0–1). *Why:* **cohesion vs brokerage** — high = sits inside a tight, self-contained family; low = spans loosely-linked groups (more bridge-like).

**Context**
- **revelation 1–114** — the mean revelation order (nuzūl) of the sūras it appears in, early (Meccan) → late (Medinan). *Why:* *when* in the revelation the root concentrates.
- **top partners** — its strongest co-occurring roots. *Why:* what it "goes with" — its immediate meaning-company.

**Reading them together:** *degree / eigenvector / pagerank* tell you **how central** a root is; *betweenness* tells you whether it's a **bridge**; *closeness* tells you its **reach**; *clustering* tells you whether it sits in a **tight family or brokers between families**. A root high in betweenness but low in clustering is a connector across the Qur'ān's families; one high in eigenvector and clustering is a core anchor of its own family.

**Takeaway.** This table turns the map into numbers you can rank, sort, and export: find the root that most **bridges** the Qur'ān's families (top *betweenness*), the **anchor** of each family (top *eigenvector* within a family), the most far-reaching ones (top *closeness*), and how a root's weight tilts **Meccan → Medinan** (*revelation*) — at whichever scale you choose (whole Qur'ān, one sūra, or a position band). It makes the picture **measurable and checkable**, not just visual.""")

# ── In-context CONCEPT PROFILE — part-in-whole: the profile opens HERE, the map/families stay framed
#    (the elephant is never lost). Structural-type comes from a curated registry that grows as concepts
#    are mapped (MISSION §5/§6); un-profiled concepts show measured attributes only. ──
def _load_concept_profiles():
    import json, os
    try:
        with open(os.path.join(os.path.dirname(__file__), "..", "concept_profiles.json"), encoding="utf-8") as _f:
            return json.load(_f).get("profiles", {})
    except Exception:
        return {}
_PROFILES = _load_concept_profiles()   # curated registry — add a concept by editing concept_profiles.json (no code change)
def _load_concept_families():
    import json, os
    try:
        with open(os.path.join(os.path.dirname(__file__), "..", "concept_families.json"), encoding="utf-8") as _f:
            return json.load(_f).get("families", {})
    except Exception:
        return {}
_FAM_OF = {}   # root -> (family name, organ_role) from the curated families registry (the "organs")
for _fid, _fv in _load_concept_families().items():
    for _m in _fv.get("members", []):
        _FAM_OF[_m] = (_fv.get("name", _fid), _fv.get("organ_role", ""))
with _concept_slot:
    st.markdown("<div style='display:inline-block;background:#1D3557;color:#fff;font-weight:800;font-size:15px;"
                "padding:7px 15px;border-radius:8px;margin:2px 0 8px;letter-spacing:.03em'>🧬 CONCEPT PROFILE</div>",
                unsafe_allow_html=True)
    _pick = st.selectbox("🔍 Pick a root — its concept profile opens here (the map & families are below)",
                         [""] + sorted(d["nodes"], key=disp_root),
                         format_func=lambda r: "— pick a root —" if r == "" else disp_root(r), key="atlas_pick")
    if _pick:
        _th = d["theme_of"][_pick]; _top = d["themes"][_th][2]
        _role = ((d.get("gf", {}).get(normalize_letters(_pick)) or {}).get("role")) or "member"
        _rolelab = {"connector / bridge": "bridge", "family anchor (hub)": "hub"}.get(_role, "member")
        _nb = sorted(((w, (b if a == _pick else a)) for a, b, w in d["edges"] if _pick in (a, b)), reverse=True)[:6]
        _N = len(d["nodes"])
        _drank = sorted(d["nodes"], key=lambda n: -_deg.get(n, 0)).index(_pick) + 1
        _brank = sorted(d["nodes"], key=lambda n: -_bet.get(n, 0.0)).index(_pick) + 1
        _prof = _PROFILES.get(_pick) or _PROFILES.get(normalize_letters(_pick))
        _typ = _prof["structural_type"] if _prof else "not yet profiled — measured attributes only"
        _tcol = "#1D9E75" if _prof else "#8FA6BC"
        _fam = _FAM_OF.get(_pick) or _FAM_OF.get(normalize_letters(_pick))
        _famtxt = _fam[0] if _fam else ("Family %d (%s)" % (_th + 1, " · ".join(disp_root(t) for t in _top)))
        st.markdown("<div style='font-size:12.5px;color:#10243A;margin:6px 0 3px'>"
                    "🐘 <b>Whole</b> &nbsp;›&nbsp; 🗂 <b>Family</b>: %s &nbsp;›&nbsp; 🌱 <b>%s</b></div>"
                    % (_famtxt, disp_root(_pick)), unsafe_allow_html=True)
        _read = ""
        if _prof:
            _rd = _prof.get("reading", {})
            for _lab, _k in (("form ↔ content", "form_content"), ("grammar ↔ semantics", "grammar_semantics"), ("structure ↔ function", "structure_function")):
                if _rd.get(_k):
                    _read += "<br><b style='color:#1D3557'>%s:</b> %s" % (_lab, _rd[_k])
            if _prof.get("senses"):
                _read += "<br><b style='color:#1D3557'>senses:</b> " + " · ".join(_prof["senses"])
        if _fam and _fam[1]:
            _read += "<br><b style='color:#1D3557'>family role (in the whole):</b> %s" % _fam[1]
        _mm = ("freq <b>%d</b> · role <b>%s</b> · degree <b>%d</b> (#%d/%d) · betweenness <b>#%d</b> · revelation <b>%.0f/114</b>"
               % (d["docf"][_pick], _rolelab, _deg.get(_pick, 0), _drank, _N, _brank, d["nuz"][_pick]))
        _partners = ("<br>pairs with <b>" + " · ".join(disp_root(m) for _w, m in _nb) + "</b>") if _nb else ""
        st.markdown("<div style='background:#F4F9F7;border:1px solid #cfe4dc;border-left:4px solid %s;border-radius:10px;"
                    "padding:9px 14px;margin:2px 0 8px;font-size:13px;color:#10243A;line-height:1.7'>"
                    "structural type: <b style='color:%s'>%s</b>%s<br>%s%s</div>"
                    % (_tcol, _tcol, _typ, _read, _mm, _partners), unsafe_allow_html=True)
        st.markdown("<div class='t-cap' style='margin:0 0 6px'>↓ <b>How this connects:</b> above is this one concept in depth; the "
                    "<b>map below</b> is the whole web — this root sits in <b>%s</b>. Hit “Locate on the map” to light it up there.</div>"
                    % _famtxt, unsafe_allow_html=True)
        _bc = st.columns([1.1, 1.2, 2])
        if _bc[0].button("🔎 Open in Search →", key="atlas_open"):
            st.session_state._pending_q = _pick; st.switch_page("pages/38_Search.py")
        if _bc[1].button("📍 Locate on the map ↓", key="atlas_locate"):
            st.session_state["_atlas_locate"] = _pick; st.rerun()
        _cp = _prof.get("closeup_page") if _prof else None
        if _cp and _bc[2].button("🗺 Full close-up →", key="atlas_closeup"):
            st.switch_page(_cp)

