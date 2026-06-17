"""Discovery Map — how the graded latent-feature discoveries connect (organisational view).
A connectome of the L-features: nodes = discoveries (size = grade, colour = scale-category),
edges = their cross-references, laid out along the synthesis ladder (atom → whole text). Plus the
integration HUBS (most-connected, load-bearing discoveries) and the TEMPORAL JOURNEY (where we
started → where we are now). No new claims — this makes the dense ledger navigable."""
from __future__ import annotations
import json, os
from collections import defaultdict
import streamlit as st
import plotly.graph_objects as go
from state import hero, layer, log_page

st.set_page_config(page_title="Discovery Map", page_icon="🗺️", layout="wide")
log_page("discovery_map")
INK = "#10243A"
DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "research", "intrinsic", "latent_features.json")

@st.cache_data(show_spinner=False)
def load(mtime):
    L = json.load(open(DATA, encoding="utf-8"))
    return L

L = load(os.path.getmtime(DATA))
feats = [f for f in L["features"] if f.get("in_table")]   # graded discoveries on the map
by_id = {f["id"]: f for f in feats}
cats = [c for c in L.get("category_order", []) if any(f["category"] == c for f in feats)]
PAL = ["#1D3557", "#2A9D8F", "#E76F51", "#6A4C93", "#E9C46A", "#1D9E75", "#C1666B",
       "#457B9D", "#8A5A44"]
ccolor = {c: PAL[i % len(PAL)] for i, c in enumerate(cats)}

# ---- layout along the synthesis ladder (x = category rung, y = stack within) ----
xpos = {c: i for i, c in enumerate(cats)}
col = defaultdict(list)
for f in feats:
    col[f["category"]].append(f["id"])
pos = {}
for c, ids in col.items():
    ids = sorted(ids)
    n = len(ids)
    for k, fid in enumerate(ids):
        pos[fid] = (xpos[c] + ((k % 2) * 0.28 - 0.14), (k - (n - 1) / 2))

# ---- edges (undirected, only between graded nodes) ----
edges = set()
deg = defaultdict(int)
for f in feats:
    for r in f.get("cross_refs", []) or []:
        if r in by_id:
            e = tuple(sorted((f["id"], r)))
            if e not in edges:
                edges.add(e); deg[e[0]] += 1; deg[e[1]] += 1

hero("🗺️ Discovery Map — how the findings connect",
     "A connectome of the graded latent features: laid out atom → whole along the scale ladder, "
     "linked by their cross-references. Where we started, how it integrates, where we are now.")

st.markdown(
    "<div style='font-size:14px;color:#10243A;line-height:1.6'>Each dot is a graded discovery "
    "(bigger = higher grade). Columns are <b>scales</b>, left→right from word-level to whole-text "
    "(the synthesis ladder). Lines are <b>cross-references</b> — how a finding at one scale leans on "
    "others. Dense vertical-and-diagonal linking = the text's structure is <i>integrated across "
    "scales</i>. Use this to see the whole landscape and find your way in.</div>", unsafe_allow_html=True)

layer(1, "The connectome")
ex, ey = [], []
for a, b in edges:
    ex += [pos[a][0], pos[b][0], None]; ey += [pos[a][1], pos[b][1], None]
fig = go.Figure()
fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines", line=dict(color="#C7D2DD", width=1),
                         hoverinfo="skip", showlegend=False))
for c in cats:
    ids = [f["id"] for f in feats if f["category"] == c]
    fig.add_trace(go.Scatter(
        x=[pos[i][0] for i in ids], y=[pos[i][1] for i in ids], mode="markers+text",
        text=ids, textposition="middle center", textfont=dict(size=12, color="white"),
        marker=dict(size=[16 + (by_id[i]["review"]["grade"] - 88) * 2.2 for i in ids],
                    color=ccolor[c], line=dict(color="white", width=1.5)),
        name=c,
        customdata=[[by_id[i]["name"], by_id[i]["review"]["grade"], by_id[i].get("plain", "")[:120]] for i in ids],
        hovertemplate="<b>%{text} · %{customdata[0]}</b><br>grade %{customdata[1]}<br>%{customdata[2]}<extra></extra>"))
fig.update_layout(height=560, plot_bgcolor="white", margin=dict(l=10, r=10, t=10, b=40),
                  legend=dict(orientation="h", y=-0.08, font=dict(size=12, color=INK)),
                  xaxis=dict(tickmode="array", tickvals=list(range(len(cats))), ticktext=cats,
                             tickfont=dict(size=12, color=INK), showgrid=False, zeroline=False),
                  yaxis=dict(showticklabels=False, showgrid=False, zeroline=False))
st.plotly_chart(fig, use_container_width=True)

layer(2, "Integration hubs — the load-bearing discoveries")
st.caption("Most cross-referenced features: the findings the rest of the structure leans on most.")
hubs = sorted(feats, key=lambda f: -deg[f["id"]])[:6]
cols = st.columns(6)
for k, f in enumerate(hubs):
    cols[k].metric(f"{f['id']} · {deg[f['id']]} links", f"grade {f['review']['grade']}",
                   help=f["name"] + " — " + f.get("plain", "")[:140])

layer(3, "The temporal journey — where we started → where we are")
phases = [("Phase A · founding (2026-06-09)", [f for f in feats if f.get("phase") == "A"]),
          ("Phase B · boundary & order (2026-06-09)", [f for f in feats if f.get("phase") == "B"]),
          ("Expansion (2026-06-10 →)", [f for f in feats if not f.get("phase")])]
for title, fs in phases:
    if not fs: continue
    chips = " ".join(f"<span style='background:{ccolor[x['category']]};color:white;border-radius:10px;"
                     f"padding:2px 8px;font-size:12px;margin:2px;display:inline-block'>{x['id']}</span>"
                     for x in sorted(fs, key=lambda z: z["id"]))
    st.markdown(f"<div style='font-size:13px;color:#10243A;margin:4px 0'><b>{title}</b> &nbsp;{chips}</div>",
                unsafe_allow_html=True)

layer(4, "Inspect a discovery")
pick = st.selectbox("Feature", [f"{f['id']} · {f['name']}" for f in sorted(feats, key=lambda z: z['id'])])
f = by_id[pick.split(" · ")[0]]
linked = [r for r in (f.get("cross_refs") or []) if r in by_id]
st.markdown(
    f"<div style='border:1px solid {ccolor[f['category']]};border-radius:8px;padding:12px 16px;font-size:14px;color:#10243A;line-height:1.6'>"
    f"<b style='font-size:16px'>{f['id']} · {f['name']}</b> &nbsp; grade <b>{f['review']['grade']}</b> "
    f"&nbsp;|&nbsp; scale: {f['category']} &nbsp;|&nbsp; substrate: {f.get('substrate','')}<br>"
    f"<b>What it is:</b> {f.get('plain','')}<br>"
    f"<b>Why it's useful:</b> {f.get('user_value','')}<br>"
    f"<b>Universe analog:</b> {f.get('universe_analog','')}<br>"
    f"<b>Connects to:</b> {' · '.join(linked) if linked else '—'} &nbsp;|&nbsp; "
    f"<b>Surfaced in:</b> {f.get('app_surface',{}).get('module','—')}</div>", unsafe_allow_html=True)

try:
    st.page_link("pages/25_Latent_Features.py", label="→ Full Latent-Feature Ledger (grades, evidence, charts)", icon="🧬")
except Exception:
    pass
st.caption(f"{len(feats)} graded discoveries · {len(edges)} cross-reference links · laid out along {len(cats)} scale-rungs.")
