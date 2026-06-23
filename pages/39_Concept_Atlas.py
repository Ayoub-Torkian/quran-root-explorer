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
with st.expander("ℹ️ What this map is — the three scales (one-page synthesis)"):
    st.markdown(
"""**The map, and why three scales.** Concepts (grammatical roots) are **nodes**; an **edge** joins two concepts that co-occur more than chance (PPMI); **colour** groups them into communities (Louvain). The *same* engine is read at three scales — the whole Qur'ān, one sūra, and a relative-position band — because structure lives at every scale and each scale answers a different question.

**1 · Whole Qur'ān — the territory.**
&nbsp;&nbsp;*Foundation:* every major concept, linked by attraction, across all 6,236 āyāt. &nbsp;*Significance:* the global conceptual **themes** and the concepts that **bridge** them. &nbsp;*Why:* to see the Book as one connected system, not a list of topics. &nbsp;*Fits:* the master map — the sūra and band views are zoom-ins of it. &nbsp;*Real-world:* a navigation atlas for study/teaching — find a concept, its theme, its neighbours. &nbsp;*Takeaway:* the vocabulary self-organises into a few coherent themes.

**2 · A Sūra — the architecture of one chapter.**
&nbsp;&nbsp;*Foundation:* the same graph built from one sūra's verses only. &nbsp;*Significance:* recovers a sūra's **internal communities** — for narrative sūras these track the **episodes** (e.g. Yūsuf: plot · temptation · prison · reunion). &nbsp;*Why:* to read *how* a chapter is built, not just which words it uses. &nbsp;*Fits:* a zoom-in (a **row**) of the whole map. &nbsp;*Real-world:* a study aid — a chapter's structure at a glance; lesson/sermon planning. &nbsp;*Takeaway:* a sūra's narrative/argument skeleton is latent in its concept co-occurrence.

**3 · Relative-position band — the shape of a sūra. ⚠️ [DIVINE-ALT]**
&nbsp;&nbsp;*Foundation:* verses pooled by *where* they fall in their sūra (opening→closing), across all sūras. &nbsp;*Significance:* positional structure — **doxology (سبّح/حمد) frames the edges**, narrative/warning fills the body, **exhortation (صبر/غفر/وقي) closes**. &nbsp;*Why:* to test whether position carries meaning (it does — strongest at the edges). &nbsp;*Fits:* an alternative re-indexing (a **column**), tagged **DIVINE-ALT** — explorable, never the muṣḥaf's primary order. &nbsp;*Real-world:* the rhetorical/homiletic shape of a sūra. &nbsp;*Takeaway:* sūras open and close with glorification and exhortation and narrate in between — a measurable homiletic form.

**Synthesis.** Row (sūra) and column (band) are two cuts of the *same* concept matrix the whole-Qur'ān map summarises; together they let you move from the entire territory → to one chapter's build → to the universal shape of a chapter, all from one measured, attraction-based web — presented as a **navigation map, not a claim.**""")

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
