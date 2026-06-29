"""Close-up · al-Kawthar's word-web — the surah's seven content-words + what interprets each.
EGO-network: the 7 surah roots (gold) and the roots the Qur'ān distinctively uses with them (navy), bonds =
PPMI ≥0.6 with ≥2 shared verses; width = strength; hover = verse-count. Distinct from the corpus-wide Concept
Atlas (39) and the inner-self page (42). MEASURED on rasm. The two hapax (نحر/أبتر) come out isolated."""
import os, json, math
import streamlit as st
import plotly.graph_objects as go

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · al-Kawthar word-web", page_icon="\U0001f9ed", layout="wide")
if S:
    try: S.log_page("closeup_kawthar_wordweb")
    except Exception: pass
    for fn in ("inject_css", "render_grouped_nav"):
        try: getattr(S, fn)()
        except Exception: pass
C.inject()

_DATA = json.load(open(os.path.join(os.path.dirname(__file__), "..", "assets", "concept_rearrange_data.json"), encoding="utf-8"))
_N = _DATA["nodes"]; _BONDS = _DATA.get("bonds", []); _R = _DATA["corr_form_meaning"]
_ANCH = set(_DATA.get("anchors", []))

C.hero("al-Kawthar's word-web — the surah's seven words and what interprets each",
       "al-Kawthar has seven content-words; two are used nowhere else. Read across the whole corpus, what does the "
       "Qur'ān put with each of them — and where do the rare ones land? This is the surah's own vocabulary, wired.",
       "USABILITY", "—", "rasm (Book6 PPMI, frequency-controlled)", "al-Kawthar ego-network · meaning vs HUMAN CONSTRUCT")
C.story("The <b>seven gold nodes</b> are al-Kawthar's content-words — give · abundance (كوثر) · pray · Lord · "
        "sacrifice · hater · cut-off (أبتر). Around them sit the <b>roots the Qur'ān distinctively uses with each</b> "
        "(navy). An edge means the pair shares verses far above chance — so each surah word resolves into a measured "
        "<i>neighbourhood of meaning</i> instead of standing alone.",
        "It operationalises «القرآن يفسّر بعضه بعضاً» for <i>this surah specifically</i>: you read كوثر, نحر or أبتر "
        "through the company the Qur'ān actually keeps for them. And the two hapax land where the surah says they do.")
C.kpis([
    ("7", "surah words", "al-Kawthar's content roots: give·abundance·pray·Lord·sacrifice·hater·cut-off", "#CC8A3C"),
    ("22", "interpreters", "roots the Qur'ān distinctively uses with the surah's words", None),
    ("80", "grounded bonds", "PPMI ≥0.6 with ≥2 shared verses", C.TEAL),
    ("صلو–زکو", "tightest pair", "pray–zakāt: 28 shared verses, PPMI +5.1", C.TEAL),
    ("نحر · أبتر", "isolated", "the two hapax — no distinctive partner (cut off)", C.CORAL),
    ("0.03", "form↔meaning r", "spelling predicts ~nothing about meaning", C.SLATE),
])

# ── HOW TO READ ──
C.callout("How to read this web",
          "<b>Gold node</b> = one of al-Kawthar's seven words; <b>navy node</b> = a root the Qur'ān distinctively "
          "uses with it. Node size = how many verses the root appears in. <b>Edge</b> = a distinctive association "
          "(PPMI, ≥2 shared verses) — <b>thickness = strength</b>; <b>hover</b> for the verse-count. A surah word "
          "with <b>no edge</b> (نحر, أبتر) is a hapax with no distinctive partner — <i>cut off</i>, structurally. "
          "Open any surah word in the panel below to see exactly which roots interpret it.", accent=C.TEAL)
C.callout("Method — and why it doesn't 'relate everything'",
          "On the <b>rasm</b>, each verse is a bag of roots. For a surah word and a candidate we count shared verses "
          "and compute <b>PPMI</b> = log₂(P(a,b) ⁄ P(a)·P(b)) — frequency-controlled, so ubiquitous words don't link "
          "to everything. A bond needs <b>PPMI ≥ 0.6 and ≥2 shared verses</b> (the surah's words are rare, so the "
          "floor is 2; read each with its verse-count). Layouts: <i>Meaning</i> = MDS on co-occurrence; <i>Form</i> = "
          "a spelling ring [HUMAN CONSTRUCT]; <i>Rarity</i> = a frequency grid.", accent=C.SLATE)

# ── THE WEB ──
C.section("The word-web — one network, three layouts")
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
    marker=dict(size=[15 + 11 * (n["df"] / _dfmax) ** 0.5 for n in _N], color=[n["color"] for n in _N], line=dict(width=1.6, color="#ffffff")),
    text=[n["label"] for n in _N], textposition="top center", textfont=dict(size=13, color="#10243A"),
    hovertext=["%s · %d verses%s" % (n["label"], n["df"], " · al-Kawthar word" if n["id"] in _ANCH else "") for n in _N], hoverinfo="text", showlegend=False))
fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", margin=dict(l=6, r=6, t=8, b=6), height=560, dragmode="pan", uirevision="keep")
fig.update_xaxes(visible=False, range=[-0.12, 1.12]); fig.update_yaxes(visible=False, range=[-0.12, 1.12], scaleanchor="x", scaleratio=1)
st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]})
C.note("Gold = al-Kawthar's seven words · navy = their interpreters. Edge thickness = PPMI strength; hover an edge for its verse-count. Switch layout to re-lay the whole graph; scroll to zoom.")

# ── WHAT IT SHOWS ──
C.section("What the web shows — each word's measured neighbourhood")
C.para("Each surah word resolves into a real neighbourhood: <b>عطو</b> (give) → رضو · جزی · ربب — the gift in a "
       "<i>reward-from-the-Lord</i> frame (the كوثر-gift toward «tarḍā», 93:5). <b>كوثر</b> sits among worldly-"
       "abundance roots — فیء · غنم (spoils), فکه (fruit) — the ordinary <i>kathra</i> the surah's unique كوثر "
       "transcends. <b>صلو</b> (pray) binds hardest to <b>زکو</b> (28 verses) — the standing prayer-almsgiving pair — "
       "with بیع · نفق · قوم (trade, spending, establishing). <b>ربب</b> (Lord) → عرش · حمد · علو (throne, praise, "
       "highness). <b>شنء</b> (the hater) sits in the justice frame جرم · وقی · ءمن (crime vs God-wariness and faith, "
       "5:8). And <b>نحر · أبتر are isolated</b> — the surah's two hapax have no distinctive partner, so the very "
       "severance the surah names shows up as a structural fact in the web.")
C.section("Strongest grounded bonds — by strength × support")
_tbl = sorted(_BONDS, key=lambda b: -(b[2] * math.log(1 + b[3])))
_rows = [["%s — %s" % (_N[i]["label"], _N[j]["label"]), "%+.1f" % p, str(co)] for i, j, p, co in _tbl[:12]]
C.table(["bond (word — root)", "PPMI strength", "shared verses"], _rows)

C.section("Open a surah word — what interprets it")
_anch_labels = [n["label"] for n in _N if n["id"] in _ANCH]
_byl = {n["label"]: n for n in _N}
_sel = st.selectbox("Surah word", _anch_labels, label_visibility="collapsed")
_nd = _byl[_sel]
if _nd["interp"]:
    _ir = [[x["r"], ("+" if x["ppmi"] >= 0 else "") + str(x["ppmi"]), "%.2f" % x["P"], str(x["co"])] for x in _nd["interp"]]
    C.table(["interpreter (root)", "PPMI", "P (reliability)", "co-verses"], _ir)
    C.note("PPMI = how distinctively the interpreter co-occurs; P = share of this word's verses it appears in.")
else:
    C.note("<b>%s</b> is a hapax — it occurs once, so it has no distinctive co-occurring partner; its meaning comes "
           "from its semantic field, and structurally it sits <i>cut off</i> from the web." % _sel)

# ── CAVEATS & TAKEAWAY ──
C.callout("Caveats — what this is and is not",
          "This <b>organises known meaning for reading</b>; not a new discovery. It is the <b>al-Kawthar ego-network</b> "
          "— distinct from the corpus-wide <i>Concept Atlas</i> and the <i>inner-self</i> page. Because the surah's words "
          "are rare, bonds use a <b>≥2-verse floor</b>, so some rest on two verses — always read an edge with its "
          "verse-count. Layouts are reading aids, never a claim about the text's order; <i>Form</i>/<i>Rarity</i> are "
          "<b>[HUMAN CONSTRUCT]</b>.", accent=C.CORAL)
C.callout("Takeaway — in one line",
          "al-Kawthar's words are not isolated tokens: <b>صلو</b> is the prayer-almsgiving pair, <b>عطو</b> is the "
          "Lord's reward, <b>كوثر</b> outshines ordinary abundance — while <b>نحر</b> and <b>أبتر</b> sit alone. The "
          "surah's antithesis, abundance vs cut-off, is visible in the wiring itself.", accent=C.TEAL)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="\U0001f50e")
