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
from analysis import COL_SURAH
from state import get_corpus, hero, layer, log_page

st.set_page_config(page_title="Concept Atlas", page_icon="🗺️", layout="wide")
log_page("concept_atlas")
corpus = get_corpus()
INK = "#10243A"
THEME_COLORS = ["#0F6E56", "#1D3557", "#E63946", "#EF9F27", "#7209B7", "#2A9D8F",
                "#9C6644", "#3A86FF", "#D62828", "#588157", "#6D597A", "#B5179E"]

@st.cache_data(show_spinner="Building the concept atlas…")
def build_atlas(_cid, n_nodes=150, drop_ubiq=10, topk=3):
    N = len(corpus.df)
    rootset = [set(r for r in corpus.root_tokens[i] if r and r != "-") for i in range(N)]
    docf = Counter()
    for s in rootset:
        for r in s: docf[r] += 1
    drop = {r for r, _ in docf.most_common(drop_ubiq)}
    nodes = [r for r, _ in docf.most_common() if r not in drop][:n_nodes]
    nodeset = set(nodes)
    co = Counter()
    for s in rootset:
        rs = sorted(s & nodeset)
        for a in range(len(rs)):
            for b in range(a + 1, len(rs)): co[(rs[a], rs[b])] += 1
    def ppmi(a, b, w):
        pa = docf[a] / N; pb = docf[b] / N; pab = w / N
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
        ss = int(corpus.df.iloc[i][COL_SURAH])
        if ss not in snz:
            try: snz[ss] = int(corpus.df.iloc[i]["ترتیب نزول"])
            except Exception: pass
    occ = {r: Counter() for r in nodes}
    for i in range(N):
        ss = int(corpus.df.iloc[i][COL_SURAH])
        for r in rootset[i]:
            if r in nodeset: occ[r][ss] += 1
    nuz = {}
    for r in nodes:
        it = [(snz[s], cc) for s, cc in occ[r].items() if s in snz]
        tot = sum(cc for _, cc in it); nuz[r] = (sum(nz * cc for nz, cc in it) / tot) if tot else 57.0
    pos = nx.spring_layout(G, weight="weight", seed=7, k=0.5, iterations=60)
    return dict(nodes=nodes, docf={r: docf[r] for r in nodes}, edges=[(a, b, G[a][b]["weight"]) for a, b in G.edges()],
                theme_of=theme_of, themes=themes, nuz=nuz, pos={n: [float(p[0]), float(p[1])] for n, p in pos.items()})

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
    if color_by == "Theme":
        colors = [THEME_COLORS[d["theme_of"][n] % len(THEME_COLORS)] for n in nodes]
        if focus is not None:                       # dim everything except the focused theme
            colors = [colors[i] if d["theme_of"][n] == focus else "#dce4e7" for i, n in enumerate(nodes)]
            texts = [n if (d["theme_of"][n] == focus and n in top40) else "" for n in nodes]
        marker = dict(size=sizes, color=colors, line=dict(width=0.5, color="#ffffff"))
    else:
        colors = [d["nuz"][n] for n in nodes]
        marker = dict(size=sizes, color=colors, colorscale="YlOrRd", showscale=True,
                      colorbar=dict(title="nuzūl<br>early→late", thickness=12),
                      line=dict(width=0.5, color="#ffffff"))
    hov = [f"{n} · freq {docf[n]} · revelation {d['nuz'][n]:.0f}/114 · theme {d['theme_of'][n] + 1}" for n in nodes]
    node_tr = go.Scatter(x=xs, y=ys, mode="markers+text", text=texts, textposition="top center",
                         textfont=dict(size=12, color=INK), hovertext=hov, hoverinfo="text", marker=marker)
    fig = go.Figure([edge_tr, node_tr])
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=650,
                      xaxis=dict(visible=False), yaxis=dict(visible=False),
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig

hero("🗺️ Concept Atlas",
     "The whole Qur'ān's conceptual territory in one map — every major root, linked by attraction, "
     "grouped into themes, sized by frequency. Click any concept to open it in Search.")

d = build_atlas(id(corpus))
c1, c2, c3 = st.columns(3)
c1.metric("Concepts mapped", len(d["nodes"]))
c2.metric("Attraction links", len(d["edges"]))
c3.metric("Themes", len(d["themes"]))
cc1, cc2 = st.columns([1, 1.4])
color_by = cc1.radio("Colour by", ["Theme", "Revelation phase"], horizontal=True, key="atlas_color")
_theme_labels = ["— whole map —"] + [f"Theme {ti + 1}: {' · '.join(top)}" for ti, _o, top in d["themes"]]
_focus_sel = cc2.selectbox("Focus a theme", _theme_labels, key="atlas_focus")
_focus = None if _focus_sel.startswith("—") else _theme_labels.index(_focus_sel) - 1
st.plotly_chart(figure(d, color_by, _focus), use_container_width=True)
st.caption("Edges = above-chance pairings (PPMI) only — each concept's strongest 3 partners. "
           "Themes are auto-grouped (Louvain); a navigation map, not a structural claim.")

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
    rr = ordered[:12]
    cols = st.columns(12, gap="small")
    for k, r in enumerate(rr):
        if cols[k].button(r, key=f"atlas_{ti}_{k}", use_container_width=True):
            st.session_state._pending_q = r
            st.switch_page("pages/38_Search.py")
