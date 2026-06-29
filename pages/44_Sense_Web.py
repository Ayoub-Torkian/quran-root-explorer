"""Close-up · Sense-resolved web (2-D / 3-D rotatable) — polysemous roots split into their two senses, each
landing in a different community. Pilot 3-D network: drag to rotate, scroll to zoom. MEASURED on rasm
(PPMI co-occurrence + per-occurrence context 2-means). The faint coral 'fold' links join a word's two senses."""
import os, json
import streamlit as st
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
_N = _D["nodes"]; _E = _D["edges"]; _SL = _D["sense_links"]; _M = _D["meta"]; _PAL = _M["palette"]

C.hero("Sense-resolved web — words that mean two things, mapped in two places",
       "Many key roots carry two senses. Read across the whole corpus, each sense keeps different company — so a "
       "single word actually sits in two neighbourhoods. Here the web is rebuilt on senses, in rotatable 3-D.",
       "USABILITY", "—", "rasm (PPMI + per-occurrence context)", "sense-resolved concept web · 2-D / 3-D")
C.story("Our other maps place each word at <b>one</b> point. But measured across every occurrence, <b>34 of the 40</b> "
        "most ambiguous roots have their <b>two senses fall in different communities</b> — the single dot was hiding "
        "a split. Here each such root appears as <b>two sense-nodes</b> (·a / ·b), joined by a faint <b>fold</b> "
        "line so you can see them pulled apart across the web.",
        "Switch to <b>3-D</b> and drag to rotate: the fold lines stretch between clusters, showing the word doing two "
        "jobs. This refines «القرآن يفسّر بعضه "
        "بعضاً» at the level of meaning, not just the word.")
C.kpis([
    ("34/40", "split across communities", "polysemous roots whose two senses sit in different neighbourhoods", C.TEAL),
    (str(_M["nNodes"]), "nodes shown", "sense-nodes + their strongest partners", None),
    (str(_M["nSenseLinks"]), "fold links", "each joins a word's two senses (·a — ·b)", C.CORAL),
    (str(_M["nComm"]), "communities", "greedy-modularity neighbourhoods in this view", None),
    ("صلو", "exemplar", "prayer: devotion vs the alms–ritual institution", C.TEAL),
    ("بصر", "exemplar", "sight vs sealed-blindness (the zaygh field)", C.SLATE),
])

C.callout("How to read this web",
          "<b>Drag to rotate</b> in 3-D (scroll to zoom). Each <b>colour</b> is a measured community. A root with two "
          "senses appears as two nodes tagged <b>·a</b> and <b>·b</b>; the faint <b>coral fold line</b> joins "
          "them — when it stretches across colours, that word genuinely lives in two places. Node size = how many "
          "verses the (sense-)node appears in. Hover any node for its label and verse-count.", accent=C.TEAL)
C.callout("Method — and its honest limit",
          "On the <b>rasm</b>, each verse is a bag of roots; bonds are <b>PPMI</b> co-occurrence (frequency-controlled). "
          "A polysemous root's occurrences are split into <b>two senses</b> by clustering each occurrence's neighbour-"
          "context, then the web is rebuilt on sense-nodes. This is a <b>reading aid</b>, not a verdict: senses are a "
          "continuum (two is a floor), and the split is approximate. It <b>refines</b> the map; it does not decree meaning.",
          accent=C.SLATE)

C.section("The web — rotate it, or read it flat")
_mode = st.radio("View", ["3-D (rotate)", "2-D (read)"], horizontal=True, label_visibility="collapsed")
_is3d = _mode.startswith("3")

def _col(n): return _PAL[n["comm"] % len(_PAL)]
def _size(n, base): return base + 9 * (min(n["df"], 300) / 300) ** 0.5

fig = go.Figure()
if _is3d:
    ex, ey, ez = [], [], []
    for i, j in _E:
        a, b = _N[i], _N[j]
        ex += [a["x3"], b["x3"], None]; ey += [a["y3"], b["y3"], None]; ez += [a["z3"], b["z3"], None]
    fig.add_trace(go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
        line=dict(color="#C9D6E8", width=1.4), opacity=0.5, hoverinfo="none", showlegend=False))
    fx, fy, fz = [], [], []
    for i, j in _SL:
        a, b = _N[i], _N[j]
        fx += [a["x3"], b["x3"], None]; fy += [a["y3"], b["y3"], None]; fz += [a["z3"], b["z3"], None]
    fig.add_trace(go.Scatter3d(x=fx, y=fy, z=fz, mode="lines",
        line=dict(color="#E63946", width=3), opacity=0.55, hoverinfo="none", showlegend=False))
    fig.add_trace(go.Scatter3d(
        x=[n["x3"] for n in _N], y=[n["y3"] for n in _N], z=[n["z3"] for n in _N], mode="markers+text",
        marker=dict(size=[_size(n, 5) for n in _N], color=[_col(n) for n in _N],
                    line=dict(width=[2 if n["sense"] else 0.5 for n in _N], color="#CC8A3C")),
        text=[n["label"] if n["sense"] else "" for n in _N], textposition="top center",
        textfont=dict(size=12, color="#10243A"),
        hovertext=["%s · %d verses" % (n["label"], n["df"]) for n in _N], hoverinfo="text", showlegend=False))
    fig.update_layout(height=640, margin=dict(l=0, r=0, t=8, b=0), paper_bgcolor="#FFFFFF",
        scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False),
                   bgcolor="#FFFFFF"))
else:
    ex, ey = [], []
    for i, j in _E:
        a, b = _N[i], _N[j]
        ex += [a["x2"], b["x2"], None]; ey += [a["y2"], b["y2"], None]
    fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines", line=dict(color="#C9D6E8", width=1),
                             opacity=0.6, hoverinfo="none", showlegend=False))
    fx, fy = [], []
    for i, j in _SL:
        a, b = _N[i], _N[j]
        fx += [a["x2"], b["x2"], None]; fy += [a["y2"], b["y2"], None]
    fig.add_trace(go.Scatter(x=fx, y=fy, mode="lines", line=dict(color="#E63946", width=2),
                             opacity=0.5, hoverinfo="none", showlegend=False))
    fig.add_trace(go.Scatter(
        x=[n["x2"] for n in _N], y=[n["y2"] for n in _N], mode="markers+text",
        marker=dict(size=[_size(n, 9) for n in _N], color=[_col(n) for n in _N],
                    line=dict(width=[1.8 if n["sense"] else 0.4 for n in _N], color="#CC8A3C")),
        text=[n["label"] if n["sense"] else "" for n in _N], textposition="top center",
        textfont=dict(size=12, color="#10243A"),
        hovertext=["%s · %d verses" % (n["label"], n["df"]) for n in _N], hoverinfo="text", showlegend=False))
    fig.update_layout(height=620, margin=dict(l=6, r=6, t=8, b=6), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                      dragmode="pan")
    fig.update_xaxes(visible=False); fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)
st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False})
C.note("Coral 'fold' lines join a word's two senses (·a — ·b). In 3-D, drag to rotate and watch a fold "
       "span two colours — that is one word measured as two. Gold-ringed nodes are the split senses; switch to 2-D to read.")

C.section("What it shows — measured sense splits")
C.para("Each split recovers a real distinction we find elsewhere, which is the validation: <b>صلو</b> "
       "(prayer) → inner devotion (قنت·خشع·قوم) vs the "
       "prayer–almsgiving institution (زكو·بيع·ركع); "
       "<b>بصر</b> (sight) → true seeing vs <b>sealed-blindness</b> "
       "(ختم·عمي·زيغ) — the same field as the heart-anatomy; "
       "<b>كثر</b> (abundance) → worldly spoils vs fruit-abundance — the very "
       "كوثر split. The method reproduces meaning we derived independently.")

C.callout("Caveat — reading aid, not discovery",
          "This <b>refines</b> the concept-web by un-blurring two-sense words; it is not a new latent feature. Senses "
          "are a continuum (two is a floor); the split is context-based and approximate. 3-D is for <b>rotating/"
          "exploring</b>; 2-D stays better for precise reading.", accent=C.CORAL)
C.callout("Takeaway",
          "A word like صلو or بصر is not one point on the map — it is two, in two "
          "neighbourhoods. Rotate the web and the <b>fold lines</b> show, at a glance, the Qur’ān using one "
          "word for two measured meanings.", accent=C.TEAL)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="\U0001f50e")
