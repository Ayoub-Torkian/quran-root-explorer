"""Close-up · Concept connectome — al-Kawthar's words + the inner self.
ONE grounded connectome (edges = distinctive PPMI association with >=3 shared verses; width = strength; hover =
verse-count). Three LAYOUTS re-lay the whole graph. Full conceptual scaffolding: importance, how-to-read,
method, findings, caveats. Edges MEASURED on rasm; PPMI frequency-controlled. HUMAN-CONSTRUCT layouts tagged."""
import os, json
import streamlit as st
import plotly.graph_objects as go

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Concept connectome", page_icon="\U0001f9ed", layout="wide")
if S:
    try: S.log_page("closeup_concept_rearrange")
    except Exception: pass
    for fn in ("inject_css", "render_grouped_nav"):
        try: getattr(S, fn)()
        except Exception: pass
C.inject()

_DATA = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "concept_rearrange_data.json"), encoding="utf-8"))
_N = _DATA["nodes"]; _BONDS = _DATA.get("bonds", []); _R = _DATA["corr_form_meaning"]

# ── 1 · WHAT & WHY ──
C.hero("Concept connectome — al-Kawthar's words + the inner self",
       "Does the Qur'ān leave its words as a list, or do they form a measurable web in which each interprets the "
       "others? Here al-Kawthar's seven content-words sit in one network with the inner-self concepts they act on.",
       "USABILITY", "—", "rasm (Book6 PPMI, frequency-controlled)", "layout-tagged: meaning vs HUMAN CONSTRUCT")
C.story("A connectome is a wiring map. This one wires <b>al-Kawthar's vocabulary</b> (give · abundance · pray · "
        "Lord · sacrifice · hater · cut-off) to the <b>inner-self concepts</b> (heart · self · breast · faith · "
        "remembrance · the near/lasting …) by how the Qur'ān actually uses them together — letting you <i>see</i> "
        "how a rare word like <b>كوثر</b> or <b>أبتر</b> is defined by the company it keeps.",
        "It operationalises «القرآن يفسّر بعضه بعضاً» — the Qur'ān interprets itself. Instead of reading a word in "
        "one verse, you read it across its whole web of distinctive companions, which is where its meaning lives.")
C.kpis([
    ("22", "concepts", "al-Kawthar's 7 content roots + 15 inner-self concepts", None),
    ("54", "grounded bonds", "distinctive PPMI links, each with ≥3 shared verses", C.TEAL),
    ("قلب–مرض", "strongest bond", "heart–disease: PPMI +4.4 across 12 verses", C.CORAL),
    ("104", "دنیا–آخرة verses", "the near & the lasting — most co-present pair", None),
    ("3", "cut off", "أبتر · شنء · نحر — no distinctive repeated bond (isolated)", C.CORAL),
    ("0.12", "form↔meaning r", "spelling predicts ~nothing about meaning", C.SLATE),
])

# ── 2 · HOW TO READ ──
C.callout("How to read this map",
          "<b>Node</b> = a concept (a root, or merged roots); its size = how many verses it appears in. "
          "<b>Edge</b> = a <b>distinctive</b> association: the two concepts share ≥3 verses far more than their "
          "frequencies predict — line <b>thickness = strength</b>; <b>hover an edge</b> for its verse-count. "
          "<b>An isolated node</b> (e.g. أبتر) has no such partner — it is structurally <i>cut off</i>. "
          "<b>Layout buttons</b> only move the nodes (the edges never change): pick <i>Meaning</i> to see linked "
          "concepts pulled together. To read a concept's meaning, open it in the panel below the graph — it lists "
          "the actual roots the Qur'ān uses to interpret it.", accent=C.TEAL)
C.callout("Method — how each bond is measured (and why it doesn't 'relate everything')",
          "On the <b>rasm</b> (consonantal text, Book6), every verse is a bag of roots. For each concept-pair we "
          "count shared verses and compute <b>PPMI</b> = log₂(P(a,b) ⁄ P(a)·P(b)) — a <b>frequency-controlled</b> "
          "score, so a common word like ربب does not link to everything just because it is everywhere. A bond is "
          "kept only if <b>PPMI ≥ 0.6 AND ≥3 shared verses</b>; the ≥3 filter removes single-verse coincidences "
          "(the kind that once inflated the بتر–شنء 'bond', which rests on 108:3 alone). Node placement: "
          "<i>Meaning</i> = multidimensional scaling on co-occurrence distance; <i>Form</i> = a spelling ring "
          "[HUMAN CONSTRUCT]; <i>Rarity</i> = a frequency grid.", accent=C.SLATE)

# ── 3 · THE CONNECTOME ──
C.section("The connectome — one network, three layouts")
_LAY = {"Meaning placement": ("meaning", "nodes placed by co-occurrence proximity (divine substrate)", "#EAF2FB", "#1D3557"),
        "Form placement": ("form", "nodes placed by spelling / edit-distance — HUMAN CONSTRUCT", "#FBF1E6", "#8a5a16"),
        "Rarity placement": ("rarity", "nodes placed by corpus frequency (rare → common)", "#EFF6F2", "#0F6E56")}
_pick = st.radio("Layout", list(_LAY), horizontal=True, label_visibility="collapsed")
_key, _badge, _bg, _bc = _LAY[_pick]
st.markdown(f"<div style='display:inline-block;background:{_bg};color:{_bc};border:1px solid {_bc}33;"
            f"border-radius:6px;padding:3px 10px;font-size:12px;font-weight:700;margin:2px 0 6px'>{_badge}</div>",
            unsafe_allow_html=True)
fig = go.Figure()
_tiers = [(2.5, 3.4, 0.6, "#0F6E56"), (1.3, 2.1, 0.42, "#1D9E75"), (0.0, 1.0, 0.28, "#A9CFC0")]
for lo, w, op, col in _tiers:
    hi = 99 if lo == 2.5 else (2.5 if lo == 1.3 else 1.3)
    xs = []; ys = []
    for i, j, ppmi, co in _BONDS:
        if lo <= ppmi < hi:
            a = _N[i]["pos"][_key]; b = _N[j]["pos"][_key]
            xs += [a[0], b[0], None]; ys += [a[1], b[1], None]
    if xs:
        fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=col, width=w), opacity=op, hoverinfo="none", showlegend=False))
_mx = []; _my = []; _mh = []
for i, j, ppmi, co in _BONDS:
    a = _N[i]["pos"][_key]; b = _N[j]["pos"][_key]
    _mx.append((a[0] + b[0]) / 2); _my.append((a[1] + b[1]) / 2)
    _mh.append("%s — %s · %d shared verses · PPMI %+.1f" % (_N[i]["label"], _N[j]["label"], co, ppmi))
fig.add_trace(go.Scatter(x=_mx, y=_my, mode="markers", marker=dict(size=11, color="rgba(0,0,0,0)"), hovertext=_mh, hoverinfo="text", showlegend=False))
_dfmax = max(n["df"] for n in _N) or 1
fig.add_trace(go.Scatter(
    x=[n["pos"][_key][0] for n in _N], y=[n["pos"][_key][1] for n in _N], mode="markers+text",
    marker=dict(size=[15 + 11 * (n["df"] / _dfmax) ** 0.5 for n in _N], color=[n["color"] for n in _N], line=dict(width=1.5, color="#ffffff")),
    text=[n["label"] for n in _N], textposition="top center", textfont=dict(size=13, color="#10243A"),
    hovertext=["%s · %d verses" % (n["label"], n["df"]) for n in _N], hoverinfo="text", showlegend=False))
fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", margin=dict(l=6, r=6, t=8, b=6), height=560, dragmode="pan")
fig.update_xaxes(visible=False, range=[-0.12, 1.12]); fig.update_yaxes(visible=False, range=[-0.12, 1.12], scaleanchor="x", scaleratio=1)
st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
C.note("Edge thickness = PPMI strength; hover an edge for its shared-verse count. Switch layout to re-lay the whole graph; scroll to zoom.")

# ── 4 · WHAT THE MAP SHOWS ──
C.section("What the map shows — reading the meaning")
C.para("Four things read straight off the network: <b>(1) a worship core</b> — کوثر · ربب · صلو · ذکر bind together "
       "(abundance, Lord, prayer, remembrance), so al-Kawthar's command «pray to your Lord» sits in a measured "
       "devotional neighbourhood. <b>(2) An affliction chain</b> — قلب–مرض (heart–disease) is the single strongest "
       "bond (12 verses), and زاد–مرض shows the «increase» operator amplifying it: the heart's pathology is its own "
       "sub-network. <b>(3) The orientation axis</b> — دنیا–آخرة share 104 verses, the most co-present pair in the set: "
       "the near and the lasting are weighed together. <b>(4) The severance is structural</b> — أبتر, شنء and نحر have "
       "no distinctive repeated partner; they sit off the web, which is exactly what <i>cut-off</i> means.")
C.section("Strongest grounded bonds")
_rows = [["%s — %s" % (_N[i]["label"], _N[j]["label"]), "%+.1f" % p, str(co)] for i, j, p, co in _BONDS[:12]]
C.table(["bond (concept — concept)", "PPMI strength", "shared verses"], _rows)

C.section("Open a concept — its grounded interpreters")
_byid = {nd["label"]: nd for nd in _N}
_sel = st.selectbox("Concept", [nd["label"] for nd in _N], label_visibility="collapsed")
_nd = _byid[_sel]
if _nd["interp"]:
    _ir = [[x["r"], ("+" if x["ppmi"] >= 0 else "") + str(x["ppmi"]), "%.2f" % x["P"], str(x["co"])] for x in _nd["interp"]]
    C.table(["interpreter (root)", "PPMI", "P (reliability)", "co-verses"], _ir)
    C.note("PPMI = how distinctively the interpreter co-occurs; P = share of this concept's verses it appears in. "
           "Nearest by meaning: " + " · ".join("%s (%.2f)" % (s, w) for s, w in _nd["sem"]) + ".")
else:
    C.note("<b>%s</b> is a hapax — it appears once and is defined by its semantic field, not by co-occurrence." % _sel)

# ── 5 · CAVEATS & TAKEAWAY ──
C.callout("Caveats — what this is and is not",
          "This <b>organises known meaning for reading</b>; it is not a new discovery. The <b>layouts are a reading "
          "aid, never a claim about the text's order</b> — the muṣḥaf's own arrangement is studied elsewhere. <i>Form</i> "
          "and <i>Rarity</i> placements are <b>[HUMAN CONSTRUCT]</b>; only <i>Meaning</i> uses the divine substrate. "
          "The 22-concept set is curated (al-Kawthar + inner-self), not exhaustive; bonds are undirected here — the "
          "directional «who interprets whom» lives in the per-concept panel.", accent=C.CORAL)
C.callout("Takeaway — in one line",
          "al-Kawthar's rarest words are not isolated: <b>کوثر</b> sits in a measured worship core, while <b>أبتر</b> "
          "sits nowhere — and that contrast, drawn only from how the Qur'ān uses the words, is the surah's own "
          "antithesis made visible.", accent=C.TEAL)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="\U0001f50e")
