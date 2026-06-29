"""Close-up · Sense-resolved web (2-D / 3-D rotatable, focusable) — polysemous roots split into their two senses,
each landing in a different community. Drag to rotate (3-D), scroll to zoom, focus a word/community, toggle
communities in the legend. MEASURED on rasm (PPMI co-occurrence + per-occurrence context 2-means). The faint
coral 'fold' links join a word's two senses."""
import os, json, collections
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
        "Switch to <b>3-D</b> and drag to rotate; <b>focus</b> a word or community; <b>click the legend</b> to isolate "
        "clusters. This refines «القرآن يفسّر بعضه بعضاً» at the level of meaning, not just the word.")
C.kpis([
    ("34/40", "split across communities", "polysemous roots whose two senses sit in different neighbourhoods", C.TEAL),
    (str(_M["nNodes"]), "nodes", "sense-nodes + their strongest partners", None),
    (str(_M["nSenseLinks"]), "fold links", "each joins a word's two senses (·a — ·b)", C.CORAL),
    (str(_M["nComm"]), "communities", "greedy-modularity neighbourhoods in this view", None),
    ("صلو", "exemplar", "prayer: devotion vs the alms–ritual institution", C.TEAL),
    ("بصر", "exemplar", "sight vs sealed-blindness (the zaygh field)", C.SLATE),
])

C.callout("How to read & explore",
          "<b>Drag to rotate</b> in 3-D (scroll to zoom). Each <b>colour</b> is a measured community — <b>click a "
          "legend entry</b> to hide/isolate it. <b>Focus a word</b> to see just its two senses + neighbours, or "
          "<b>focus a community</b>, or raise <b>min verses</b> to thin the web. Gold-ringed nodes are the split "
          "senses (·a/·b); the coral <b>fold line</b> joins them — when it stretches across colours, that word "
          "genuinely lives in two places. Hover any node for its verse-count.", accent=C.TEAL)
C.callout("Method — and its honest limit",
          "On the <b>rasm</b>, each verse is a bag of roots; bonds are <b>PPMI</b> co-occurrence (frequency-controlled). "
          "A polysemous root's occurrences are split into <b>two senses</b> by clustering each occurrence's neighbour-"
          "context, then the web is rebuilt on sense-nodes. This is a <b>reading aid</b>, not a verdict: senses are a "
          "continuum (two is a floor), and the split is approximate. It <b>refines</b> the map; it does not decree meaning.",
          accent=C.SLATE)

# ── THE WEB ──────────────────────────────────────────────────────────────────
C.section("The web — focus, rotate, or read it flat")
_bases = sorted({n["label"].replace("·a", "").replace("·b", "") for n in _N if n["sense"]})
_comms = sorted({n["comm"] for n in _N})
_fc = st.columns([2, 2, 2])
with _fc[0]:
    _focus = st.selectbox("Focus a word (ego view)", ["(whole web)"] + _bases)
with _fc[1]:
    _csel = st.multiselect("Focus communities", _comms, default=[], format_func=lambda c: "community %d" % (c + 1))
with _fc[2]:
    _minv = st.slider("Min verses per node", 0, 80, 0, 5)
_mode = st.radio("View", ["3-D (rotate)", "2-D (read)"], horizontal=True, label_visibility="collapsed")
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
if _csel:
    keep = {i for i in keep if _N[i]["comm"] in _csel}
if _minv > 0:
    keep = {i for i in keep if _N[i]["df"] >= _minv or _N[i]["sense"]}
if not keep:
    keep = set(range(len(_N)))

def _xyz(i):
    n = _N[i]
    return (n["x3"], n["y3"], n["z3"]) if _is3d else (n["x2"], n["y2"], None)
def _seg(pairs):
    xs, ys, zs = [], [], []
    for i, j in pairs:
        if i in keep and j in keep:
            ax, ay, az = _xyz(i); bx, by, bz = _xyz(j)
            xs += [ax, bx, None]; ys += [ay, by, None]; zs += [az, bz, None]
    return xs, ys, zs
def _line(xs, ys, zs, color, width, op, name, leg):
    if _is3d:
        return go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color=color, width=width),
                            opacity=op, hoverinfo="none", name=name, showlegend=leg)
    return go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=width),
                      opacity=op, hoverinfo="none", name=name, showlegend=leg)
def _nodes(ids, color, ring, ringcol, showtext, name, leg, sizebase):
    xs = [_N[i]["x3"] if _is3d else _N[i]["x2"] for i in ids]
    ys = [_N[i]["y3"] if _is3d else _N[i]["y2"] for i in ids]
    sz = [sizebase + 9 * (min(_N[i]["df"], 300) / 300) ** 0.5 for i in ids]
    txt = [_N[i]["label"] if showtext else "" for i in ids]
    hov = ["%s · %d verses" % (_N[i]["label"], _N[i]["df"]) for i in ids]
    mk = dict(size=sz, color=color, line=dict(width=ring, color=ringcol))
    if _is3d:
        zs = [_N[i]["z3"] for i in ids]
        return go.Scatter3d(x=xs, y=ys, z=zs, mode="markers+text", marker=mk, text=txt,
                            textposition="top center", textfont=dict(size=12, color="#10243A"),
                            hovertext=hov, hoverinfo="text", name=name, showlegend=leg)
    return go.Scatter(x=xs, y=ys, mode="markers+text", marker=mk, text=txt, textposition="top center",
                      textfont=dict(size=12, color="#10243A"), hovertext=hov, hoverinfo="text",
                      name=name, showlegend=leg)

fig = go.Figure()
ex, ey, ez = _seg(_E); fig.add_trace(_line(ex, ey, ez, "#C9D6E8", 1.2, 0.5, "bonds", False))
fx, fy, fz = _seg(_SL); fig.add_trace(_line(fx, fy, fz, "#E63946", 2.5, 0.55, "sense fold (·a–·b)", True))
sb = 5 if _is3d else 9
for c in _comms:
    ids = [i for i in keep if _N[i]["comm"] == c and not _N[i]["sense"]]
    if ids:
        fig.add_trace(_nodes(ids, _PAL[c % len(_PAL)], 0.5, "#FFFFFF", False, "community %d" % (c + 1), True, sb))
sense_ids = [i for i in keep if _N[i]["sense"]]
if sense_ids:
    fig.add_trace(_nodes(sense_ids, [_PAL[_N[i]["comm"] % len(_PAL)] for i in sense_ids], 2.2, "#CC8A3C",
                         True, "split senses (·a/·b)", True, sb + 1))
if _is3d:
    fig.update_layout(height=640, margin=dict(l=0, r=0, t=8, b=0), paper_bgcolor="#FFFFFF",
        legend=dict(font=dict(size=12), itemsizing="constant"),
        scene=dict(xaxis=dict(visible=False), yaxis=dict(visible=False), zaxis=dict(visible=False), bgcolor="#FFFFFF"))
else:
    fig.update_layout(height=620, margin=dict(l=6, r=6, t=8, b=6), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
                      dragmode="pan", legend=dict(font=dict(size=12), itemsizing="constant"))
    fig.update_xaxes(visible=False); fig.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)
st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False})
C.note("Coral <b>fold</b> lines join a word's two senses (·a — ·b); watch one span two colours in 3-D — one word "
       "measured as two. Gold-ringed = split senses. Use the focus row to zoom into a word or cluster; click legend to isolate.")

# ── WHAT IT SHOWS ────────────────────────────────────────────────────────────
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
