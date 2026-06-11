"""Concept Deep-Dive — understand a concept using ALL the data.

A FIRST-CLASS endeavor distinct from Root Exploration (not a tab of it). Seeds a
concept and reads it across the whole corpus by MULTIMODAL FUSION: independent
modalities (semantic ∥ co-location ∥ spatial ∥ morphology ∥ sequence) kept
separate and SYNTHESISED into a six-type relation scheme
(consensus / semantic / co-location / spatial / orthogonal / divergent) — the
SAME fusion vocabulary as the Ayah deep-dive. Spatial is ONE modality, not the
headline.

Guiding principle: القرآن یفسر بعضه بعضا — the part is understood in light of the
whole, and the whole is more than the sum of its parts. Computational DESCRIPTION,
never tafsir. The heavy full report (docx + pdf) is produced by the background
worker `deep_dive.py concept <root>`, not on this page.
"""
from __future__ import annotations

import streamlit as st

import analysis as _A
import deep_dive as DD
import plotly_charts as PC
from state import get_corpus, query_controls, hero, layer, log_page

st.set_page_config(page_title="Concept Deep-Dive", page_icon="🔬", layout="wide")
log_page("concept_deep_dive")
corpus = get_corpus()
st.markdown("<style>section[data-testid='stMain'] [data-testid='stCaptionContainer'],"
            "section[data-testid='stMain'] [data-testid='stCaptionContainer'] *"
            "{color:#3D4757 !important;font-size:14px !important;}</style>",
            unsafe_allow_html=True)
raw, normalize, top_p, min_w, run = query_controls(corpus)
input_roots = _A.parse_input_roots(raw, normalize)

hero("🔬 Concept Deep-Dive", "understand a concept by multimodal fusion · القرآن یفسر بعضه بعضا")
_fsig = st.session_state.get("_form_scope_last")
if _fsig:
    st.warning(f"🔬 Your form scope (**{_fsig[0]} → {_fsig[1]}**) is **not applied here** — "
               f"Concept Deep-Dive reads the WHOLE corpus by design (its embeddings are "
               f"corpus-level). Scoped pages: Home · Network · Motifs · Statistics · Ayah "
               f"Browser · Per-Root. To deep-dive ONLY the scoped āyahs, open 🔭 Āyah "
               f"Deep-Dive (its references are prefilled with your subset).")
st.caption("Distinct from Root Exploration: seed a concept, read it across the whole corpus "
           "through several independent lenses at once, and synthesise. "
           "Computational description, not tafsir.")

with st.expander("📐 Method — the three modalities & how this complements Motif analysis"):
    st.markdown(
        "A concept is read through **three INDEPENDENT modalities**, kept separate and "
        "synthesised (never blended — blending dilutes meaning):\n\n"
        "- **semantic** — distributional meaning (concepts used in similar contexts)\n"
        "- **co-location** — shared territory (deployed in the same surahs / regions)\n"
        "- **spatial** — distribution shape (often *null* — reported honestly, never the headline)\n\n"
        "Each related concept is typed by how the modalities **agree**: *consensus* (≥2 high), "
        "*semantic / co-location / spatial* (one high), *orthogonal* (one high, others "
        "independent), *divergent* (one high, another opposed = tension).\n\n"
        "**Where this fits vs 🔺 Motifs:** Motif analysis is the *within-verse* lens "
        "(do these roots share a verse? — directly verifiable, blind beyond the verse). "
        "This consensus lens is the *across-verse* complement (null-gated cross-modal "
        "agreement). Together they yield **latent motifs** — coherent themes the corpus "
        "weaves but never states in a single verse.")

with st.expander("📋 Or paste a word / phrase / ayah to find the concept"):
    _pst = st.text_area("Paste Arabic text — each word is mapped to its root",
                        height=80, key="concept_paste",
                        placeholder="فِي قُلُوبِهِم مَّرَضٌ")
    if _pst.strip():
        _cands = DD.match_pasted_concepts(corpus, _pst)
        if _cands:
            _pick = st.radio("Concepts found — pick one to deep-dive:",
                             [f"{r}  (×{n})" for r, n in _cands],
                             horizontal=True, key="concept_pick")
            input_roots = [_pick.split()[0]]      # override the sidebar query
        else:
            st.caption("No known concept found in that text.")

if not input_roots:
    st.info("Type a concept in the 🔎 Query box (sidebar), or paste text above, to begin.")
    st.stop()

target = input_roots[0]
if len(input_roots) > 1:
    st.caption(f"Analysing the first queried concept **{target}** (others ignored here).")


def _concept(target, normalize, unit):
    cache = st.session_state.setdefault("_concept_cache", {})
    key = (target, normalize, unit)
    if key in cache:
        return cache[key]
    bar = st.progress(0.0, text="Starting deep-dive…")
    try:
        res = DD.concept_deep_dive(target, unit=unit, normalize=normalize, corpus=corpus,
                                   progress=lambda f, m: bar.progress(min(f, 1.0), text=m))
    finally:
        bar.empty()
    cache[key] = res
    return res


if st.button(f"▶  Run deep-dive on  {target}", type="primary"):
    st.session_state["concept_go"] = target
if st.session_state.get("concept_go") != target:
    st.info(f"Ready to analyse **{target}** across the whole corpus. Click ▶ Run to start — "
            "multimodal fusion is a heavy computation, so it waits for your OK "
            "(and re-confirms whenever you change the concept).")
    st.stop()

try:
    res = _concept(target, normalize, "surah")
except Exception as e:
    st.warning(f"⚠️  {e}")
    st.stop()
fld, dist, null, cg = res["field"], res["distribution"], res["null"], res["cross_granularity"]
syn = res.get("synthesis", {}) or {}
rel = res.get("relations", {}) or {}
rbt = rel.get("related_by_type", {})
seq = res.get("sequence", {}) or {}
_REL = {"consensus": "agree on ≥2 modalities (robust)", "semantic": "meaning-mates",
        "co-location": "territory-mates", "spatial": "distribution-shape kin",
        "orthogonal": "one modality only (independent on the rest)",
        "divergent": "close on one, OPPOSED on another (tension)"}


def _chips(items, n=6):
    items = [str(x) for x in items]
    if not items:
        return "<span style='font-size:20px;color:#243447'>—</span>"
    out = " ".join(
        "<span style='font-size:22px;color:#243447;background:#EEF3FB;border-radius:7px;"
        "padding:3px 14px;margin:4px 3px;display:inline-block;font-weight:600'>" + r + "</span>"
        for r in items[:n])
    if len(items) > n:
        out += (f" <span style='font-size:14px;color:#3D4757'>+{len(items) - n} more "
                f"(full list in the table)</span>")
    return out


def _show_chips(items, n=6):
    st.markdown(_chips(items, n), unsafe_allow_html=True)


# ── v2.0 UI standard: charts everywhere (bar/scatter/pie/network) + data-driven interpretation ──
import plotly.graph_objects as _go

_RELC = {"consensus": "#1D9E75", "semantic": "#378ADD", "co-location": "#EF9F27",
         "spatial": "#B4B2A9", "orthogonal": "#B4B2A9", "divergent": "#E63946"}
_MEDC = {2, 3, 4, 5, 8, 9, 13, 22, 24, 33, 47, 48, 49, 55, 57, 58, 59, 60, 61, 62, 63,
         64, 65, 66, 76, 98, 99, 110}  # traditional cut — CONTROL-ONLY (human frame)


def _donut(counts, title):
    labs = [k for k, v in counts.items() if v]
    if not labs:
        return None
    fig = _go.Figure(_go.Pie(labels=labs, values=[counts[k] for k in labs], hole=0.55,
                             marker=dict(colors=[_RELC.get(l, "#B4B2A9") for l in labs])))
    fig.update_layout(title=title, height=300, margin=dict(l=10, r=10, t=40, b=10))
    return fig


def _network_fig(center, rbt, top=25):
    """Radial bond map with MEANINGFUL geometry: sector = relation type ·
    distance from hub = bond strength (closer = stronger) · node size = frequency."""
    import math
    rows = [(x["root"], ty, max(float(v) for v in x["axes"].values()),
             int(corpus.freq_norm.get(x["root"], 0)))
            for ty, lst in rbt.items() for x in (lst or [])]
    rows.sort(key=lambda t: -t[2])
    rows = rows[:top]
    if not rows:
        return None, []
    order = ["consensus", "semantic", "co-location", "spatial", "orthogonal", "divergent"]
    by_ty = {ty: [r for r in rows if r[1] == ty] for ty in order}
    by_ty = {ty: v for ty, v in by_ty.items() if v}
    smax = max(r[2] for r in rows); smin = min(r[2] for r in rows)
    rngs = (smax - smin) or 1.0
    step = 2 * math.pi / len(rows)
    pos, sector_mid = {}, {}
    ang = 0.0
    for ty, lst in by_ty.items():
        block = step * len(lst)
        for j, (r, _t, s_, _f) in enumerate(lst):
            a = ang + block * (j + 0.5) / len(lst)
            rad = 1.55 - 0.95 * ((s_ - smin) / rngs)
            pos[r] = (rad * math.cos(a), rad * math.sin(a))
        sector_mid[ty] = ang + block / 2
        ang += block
    fig = _go.Figure()
    for rr in (0.6, 1.55):
        fig.add_shape(type="circle", x0=-rr, y0=-rr, x1=rr, y1=rr,
                      line=dict(color="#C9D6E8", width=1, dash="dot"))
    fig.add_annotation(x=0, y=0.6, text="stronger", showarrow=False, yshift=9,
                       font=dict(size=10, color="#3D4757"))
    fig.add_annotation(x=0, y=1.55, text="weaker", showarrow=False, yshift=9,
                       font=dict(size=10, color="#3D4757"))
    for r, ty, s_, _f in rows:
        x1, y1 = pos[r]
        fig.add_trace(_go.Scatter(x=[0, x1], y=[0, y1], mode="lines",
                                  line=dict(width=1 + 2.5 * ((s_ - smin) / rngs + 0.15),
                                            color=_RELC.get(ty, "#B4B2A9")),
                                  hoverinfo="skip", showlegend=False, opacity=0.75))
    fig.add_trace(_go.Scatter(
        x=[pos[r][0] for r, *_ in rows], y=[pos[r][1] for r, *_ in rows],
        mode="markers+text", text=[r for r, *_ in rows], textposition="top center",
        textfont=dict(size=14),
        marker=dict(size=[9 + 3.2 * math.log1p(f_) for *_x, f_ in rows],
                    color=[_RELC.get(ty, "#B4B2A9") for _r, ty, *_y in rows],
                    line=dict(width=1, color="white")),
        hovertext=[f"{r} — {ty} · bond strength z≈{s_:.1f} · frequency {f_}× "
                   f"(closer to {center} = stronger)" for r, ty, s_, f_ in rows],
        hoverinfo="text", showlegend=False))
    for ty, am in sector_mid.items():
        fig.add_annotation(x=2.0 * math.cos(am), y=2.0 * math.sin(am),
                           text=f"<b>{ty}</b>", showarrow=False,
                           font=dict(size=12, color=_RELC.get(ty, "#3D4757")))
    fig.add_trace(_go.Scatter(x=[0], y=[0], mode="markers+text", text=[center],
                              textposition="middle center",
                              textfont=dict(size=17, color="white"),
                              marker=dict(size=50, color="#1D3557"),
                              hoverinfo="skip", showlegend=False))
    fig.update_layout(height=460, margin=dict(l=10, r=10, t=40, b=10),
                      xaxis=dict(visible=False, range=[-2.35, 2.35]),
                      yaxis=dict(visible=False, range=[-2.25, 2.25],
                                 scaleanchor="x", scaleratio=1),
                      title=f"{center} — bond map: sector = HOW it bonds · "
                            f"closer = STRONGER · size = frequency")
    return fig, rows[:3]


@st.cache_data
def _surah_profile(_cid, root):
    K = _A.normalize_letters
    df = corpus.df
    su = df[_A.COL_SURAH].astype(int).to_numpy()
    kt = K(root)
    counts = {}
    for i in range(len(df)):
        c = sum(1 for t in corpus.root_tokens[i] if K(t) == kt)
        if c:
            counts[int(su[i])] = counts.get(int(su[i]), 0) + c
    return counts


import re as _reF

_DIAF = _reF.compile(r"[ً-ْٰـۖ-ۭ]")
_WAF = _reF.compile(r"[^\W\d_]+", _reF.UNICODE)


def _nlf(t):
    t = _DIAF.sub("", str(t)); t = _reF.sub(r"[آأإٱ]", "ا", t)
    t = _reF.sub(r"[ىی]", "ي", t); t = _reF.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء")


@st.cache_data
def _form_profile(_cid, form):
    """Per-sūra counts of one SURFACE form (word-boundary match incl. cliticized variants)."""
    df = corpus.df
    su = df[_A.COL_SURAH].astype(int).to_numpy()
    col = _A.COL_DIACRITIZED if _A.COL_DIACRITIZED in df.columns else _A.COL_SEGMENTED
    kf = _nlf(form).strip()
    counts = {}
    for i, t in enumerate(df[col].astype(str)):
        c = sum(1 for w in _WAF.findall(_nlf(t))
                if w == kf or (w.endswith(kf) and len(w) - len(kf) <= 3
                               and set(w[:len(w) - len(kf)]) <= set("وفسلبكا")))
        if c:
            counts[int(su[i])] = counts.get(int(su[i]), 0) + c
    return counts


def _profile_bar(counts, title, height=240):
    _xs = list(range(1, 115))
    fig = _go.Figure(_go.Bar(
        x=_xs, y=[counts.get(s, 0) for s in _xs],
        marker_color=["#E63946" if s in _MEDC else "#1D9E75" for s in _xs],
        hovertemplate="sūra %{x}: %{y}×<extra></extra>"))
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=38, b=10), title=title,
                      xaxis_title="sūra (muṣḥaf order)", yaxis_title="count")
    return fig


layer(1, "MULTIMODAL FUSION  (semantic ∥ co-location ∥ spatial)")
_ct = rel.get("by_relation", {})
_arch = dist.get("archetype")
g = st.columns(6)
g[0].metric("frequency", dist["frequency"], help="total occurrences of the root across the corpus")
g[1].metric("surahs", dist["n_surahs_present"], help="number of surahs the concept appears in")
g[2].metric("semantic", _ct.get("semantic", 0) + _ct.get("consensus", 0),
            help="meaning-mates (distributional neighbours), including consensus bonds")
g[3].metric("co-location", _ct.get("co-location", 0) + _ct.get("consensus", 0),
            help="territory-mates (shared deployment), including consensus bonds")
g[4].metric("consensus", _ct.get("consensus", 0), help="bonds confirmed on ≥2 independent modalities")
g[5].metric("divergent", _ct.get("divergent", 0),
            help="tension: close on one modality, opposed on another (e.g. shared territory, opposed meaning)")
g2 = st.columns(6)
g2[0].metric("orthogonal", _ct.get("orthogonal", 0), help="single-modality bonds; independent on the others")
g2[1].metric("spatial z", null["z"], help="areal-evenness vs a frequency-matched scramble; ≤ −2 = beyond chance (often null)")
g2[2].metric("archetype", (_arch["tag"] if _arch else "—"), help="spatial distribution archetype")
g2[3].metric("stability", (_arch["stability"] if _arch else "—"), help="archetype robustness under feature jitter")
g2[4].metric("in-ayah pos", seq.get("mean_within_ayah_position"),
             help="mean position within the ayah (0 = start, 1 = end) — a sequence-level feature")
g2[5].metric("ayah-final", f"{round((seq.get('ayah_final_share') or 0) * 100)}%",
             help="share of occurrences that END the ayah (rhyme / fawāṣil)")
st.caption(syn.get("reading", ""))
_pts = [dict(label=x["root"], x=x["axes"]["semantic"], y=x["axes"]["co-location"],
             relation=ty, size=x["axes"]["spatial"])
        for ty, lst in rbt.items() for x in lst]
if _pts:
    st.plotly_chart(PC.chart_fusion_scatter(_pts, "semantic", "co-location",
                    f"{target} — multimodal fusion map"), use_container_width=True)

    @st.cache_data
    def _root_sample(_cid):
        K = _A.normalize_letters
        df = corpus.df
        su = df[_A.COL_SURAH].astype(int).to_numpy()
        ay = df[_A.COL_AYAH].astype(int).to_numpy()
        dia = (df[_A.COL_DIACRITIZED].astype(str).tolist()
               if _A.COL_DIACRITIZED in df.columns else df[_A.COL_SEGMENTED].astype(str).tolist())
        samp = {}
        for i in range(len(df)):
            for r in {K(t) for t in corpus.root_tokens[i]}:
                if r not in samp:
                    samp[r] = (f"{int(su[i])}:{int(ay[i])}", dia[i][:70])
        return samp

    import pandas as _pd
    _samp = _root_sample(id(corpus))
    _crows = [{"root": x["root"], "relation": ty,
               "semantic": x["axes"]["semantic"], "co-location": x["axes"]["co-location"],
               "spatial": x["axes"]["spatial"],
               "frequency": int(corpus.freq_norm.get(x["root"], 0)),
               "sample": _samp.get(x["root"], ("—", ""))[0],
               "متن آیه با حرکت": _samp.get(x["root"], ("", ""))[1]}
              for ty, lst in rbt.items() for x in lst]
    st.markdown("**Plotted concepts — root ↔ frequency & sample (match the points above):**")
    st.dataframe(_pd.DataFrame(_crows).sort_values(["relation", "frequency"],
                                                   ascending=[True, False]),
                 use_container_width=True, hide_index=True, height=330)
if _pts:
    cA, cB = st.columns([1, 2])
    with cA:
        _dn = _donut({t: len(l or []) for t, l in rbt.items()}, "relation composition")
        if _dn:
            st.plotly_chart(_dn, use_container_width=True)
            st.caption("❓ share of each bond type. Consensus-heavy ring = a robust multi-modal "
                       "concept; orthogonal-heavy = modality-specific behavior; any divergent "
                       "slice = real tension worth reading.")
    with cB:
        _nf, _top3 = _network_fig(target, rbt)
        if _nf:
            st.plotly_chart(_nf, use_container_width=True)
            st.markdown(
                "**📍 What to take from this map:** the strongest companions of "
                f"**{target}** are " +
                "، ".join(f"**{r}** ({ty}, z≈{s_:.1f})" for r, ty, s_, _f in _top3) +
                ". Read it in three moves: ① the INNER ring is the concept's core company "
                "(strongest bonds); ② the sector tells you HOW each bonds — green consensus = "
                "confirmed on ≥2 independent modalities (trust these first), red divergent = "
                "real tension (shared territory or sense, yet opposed); ③ big-but-outer nodes "
                "are frequent roots only loosely tied — frequency is not intimacy.")
            st.caption("❓ top-25 bonds. Distance = bond strength (not similarity of position); "
                       "PPMI-honest association lives on the Network page; #65 rule: this is a "
                       "MAP, not a distinctiveness claim.")

    _tot = sum(len(l or []) for l in rbt.values())
    _ncons = len(rbt.get("consensus") or [])
    _nsem = len(rbt.get("semantic") or []); _nco = len(rbt.get("co-location") or [])
    _ndiv = len(rbt.get("divergent") or [])
    _dom = ("**semantic-dominant** — the concept travels by meaning, not territory"
            if _nsem > _nco else
            "**co-location-dominant** — the concept is place-bound in the muṣḥaf"
            if _nco > _nsem else "**balanced** between meaning and territory")
    _hs = dist.get("hotspot_surahs") or []
    _top3 = sum(n for _, n in _hs[:3])
    _fin = float(seq.get("ayah_final_share") or 0)
    _conc = (100 * _top3 / max(dist["frequency"], 1))
    st.markdown(
        f"#### 🧠 Interpretation — {target}, this run (computed, not generic)\n"
        f"- **{_tot} bonded concepts**, of which **{_ncons} consensus** (confirmed on ≥2 "
        f"independent modalities — the core to trust first); profile is {_dom}; "
        f"{_ndiv} divergent bond(s).\n"
        f"- **Spatial evenness z={null['z']}** → *{null['interpretation']}* — one modality, "
        f"honestly reported; for most concepts this is null and that is informative.\n"
        f"- **Concentration:** top-3 sūras hold {_top3}/{dist['frequency']} occurrences "
        f"({_conc:.0f}%) — "
        + ("a **passage-bound** concept (LOCAL-formula mode, #66)."
           if _conc > 50 else "a **returned-to** concept (GLOBAL-motif mode, #66/#42).") + "\n"
        f"- **Verse position:** {_fin * 100:.0f}% of occurrences are āyah-FINAL — "
        + ("**seal-active**: this concept participates in the fāṣila system (Lens 17); open it "
           "in Āyah Deep-Dive to see its class content-fit."
           if _fin >= 0.25 else "a body-of-verse concept, not a seal."))

_cm = syn.get("cross_modal", {})
st.caption("divergence: " + str(_cm.get("divergence", "—")) +
           "　·　verified bonds (root∥surface): " + (", ".join(_cm.get("verified_bonds", [])) or "—"))
with st.expander("relation lists (detail)"):
    for ty in ["consensus", "semantic", "co-location", "spatial", "orthogonal", "divergent"]:
        lst = rbt.get(ty) or []
        if not lst:
            continue
        st.markdown(f"**{ty}** — {_REL[ty]}:")
        _show_chips([x["root"] for x in lst], n=8)

layer(2, "MODALITIES IN DETAIL  (tree → forest)")
st.markdown("**Semantic field** — the meaning-bearing neighbourhood:")
_show_chips(fld["semantic_field"])
_axmap = {x["root"]: x["axes"] for lst in rbt.values() for x in (lst or [])}
_sf = [r for r in fld["semantic_field"] if r in _axmap][:12]
if _sf:
    _figb = _go.Figure(_go.Bar(
        x=[float(_axmap[r]["semantic"]) for r in _sf], y=_sf, orientation="h",
        marker_color="#378ADD",
        customdata=[[int(corpus.freq_norm.get(r, 0))] for r in _sf],
        hovertemplate="%{y} · semantic z=%{x:.1f} · frequency %{customdata[0]}<extra></extra>"))
    _figb.update_layout(height=max(220, 30 * len(_sf)), margin=dict(l=10, r=10, t=36, b=10),
                        title="semantic-field strength (distributional z per neighbour)",
                        yaxis=dict(autorange="reversed"))
    st.plotly_chart(_figb, use_container_width=True)
    st.caption("❓ context for the chips above: how strongly each neighbour shares this concept's "
               "usage contexts (z vs the corpus background). Hover for frequency; a sample verse "
               "per root is in the fusion table (layer 1).")
if fld["cross_view_consensus"]:
    st.markdown("**Robust bonds** — confirmed by ≥2 independent views:")
    _show_chips([b["root"] for b in fld["cross_view_consensus"]])
    _rb2 = [b["root"] for b in fld["cross_view_consensus"] if b["root"] in _axmap][:10]
    if _rb2:
        _figr = _go.Figure()
        _figr.add_trace(_go.Bar(y=_rb2, x=[float(_axmap[r]["semantic"]) for r in _rb2],
                                name="semantic z", orientation="h", marker_color="#378ADD"))
        _figr.add_trace(_go.Bar(y=_rb2, x=[float(_axmap[r]["co-location"]) for r in _rb2],
                                name="co-location z", orientation="h", marker_color="#EF9F27"))
        _figr.update_layout(barmode="group", height=max(240, 42 * len(_rb2)),
                            margin=dict(l=10, r=10, t=38, b=10),
                            title="why these are ROBUST — both views per bond",
                            yaxis=dict(autorange="reversed"))
        st.plotly_chart(_figr, use_container_width=True)
        st.markdown("**📍 What to take from this chart:** a robust bond needs BOTH bars "
                    "(meaning-closeness AND shared territory) — single-bar neighbours are "
                    "real but modality-specific. The longest blue+orange pair is the bond "
                    "most likely to survive any re-analysis.")
st.markdown("**Co-location territory** — shares deployment:")
_show_chips(fld["co_location_neighbours"])
_cl2 = [r for r in fld["co_location_neighbours"] if r in _axmap][:12]
if _cl2:
    _figc = _go.Figure(_go.Bar(
        x=[float(_axmap[r]["co-location"]) for r in _cl2], y=_cl2, orientation="h",
        marker_color="#EF9F27",
        customdata=[[int(corpus.freq_norm.get(r, 0))] for r in _cl2],
        hovertemplate="%{y} · co-location z=%{x:.1f} · frequency %{customdata[0]}<extra></extra>"))
    _figc.update_layout(height=max(220, 30 * len(_cl2)), margin=dict(l=10, r=10, t=36, b=10),
                        title="territory strength (co-location z per neighbour)",
                        yaxis=dict(autorange="reversed"))
    st.plotly_chart(_figc, use_container_width=True)
    st.caption("❓ context for the chips: how strongly each neighbour shares this concept's "
               "DEPLOYMENT (same sūras/regions), independent of meaning. A root high here but "
               "low on the semantic bar above travels WITH the concept without meaning the "
               "same thing — narrative companionship, not synonymy.")

layer(3, "CROSS-GRANULARITY VERIFICATION  (root ∥ surface)")
st.markdown("**Verified at BOTH levels** (robust to granularity):")
_show_chips(cg["verified_both_levels"])
c = st.columns(2)
with c[0]:
    st.markdown("**root-level only**")
    _show_chips(cg["root_level_only"])
with c[1]:
    st.markdown("**surface / sense-only**")
    _show_chips(cg["surface_level_only"])
_nbg = len(cg["verified_both_levels"]); _nrg = len(cg["root_level_only"])
_nsg = len(cg["surface_level_only"])
if _nbg + _nrg + _nsg:
    _figv = _go.Figure()
    _figv.add_shape(type="circle", x0=0, y0=0, x1=2.0, y1=2.0,
                    line=dict(color="#1D9E75", width=2), fillcolor="rgba(29,158,117,0.13)")
    _figv.add_shape(type="circle", x0=1.15, y0=0, x1=3.15, y1=2.0,
                    line=dict(color="#378ADD", width=2), fillcolor="rgba(55,138,221,0.13)")
    for _xv, _tv, _cv in ((0.55, f"<b>{_nrg}</b><br>root-only", "#0F6E56"),
                          (1.575, f"<b>{_nbg}</b><br>BOTH", "#1D3557"),
                          (2.6, f"<b>{_nsg}</b><br>surface-only", "#378ADD")):
        _figv.add_annotation(x=_xv, y=1.0, text=_tv, showarrow=False,
                             font=dict(size=15, color=_cv))
    _figv.add_annotation(x=0.45, y=2.12, text="ROOT grain", showarrow=False,
                         font=dict(size=12, color="#0F6E56"))
    _figv.add_annotation(x=2.7, y=2.12, text="SURFACE grain", showarrow=False,
                         font=dict(size=12, color="#378ADD"))
    _figv.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=10),
                        xaxis=dict(visible=False, range=[-0.3, 3.5]),
                        yaxis=dict(visible=False, range=[-0.3, 2.4],
                                   scaleanchor="x", scaleratio=1),
                        title="granularity Venn — does the bond survive changing the unit?")
    st.plotly_chart(_figv, use_container_width=True)
    _core = "، ".join(str(x) for x in cg["verified_both_levels"][:4])
    st.markdown(
        "**📍 What to take from the Venn:** "
        + (f"the overlap (**{_nbg}**: {_core}) is the trustworthy core — bonds that survive "
           f"switching the unit of analysis (the G10 invariance gate applied to relations). "
           if _nbg else "NO bond survives both grains — treat every relation here as "
                        "grain-dependent until verified. ")
        + (f"The big surface-only wing ({_nsg}) means this root's surface FORMS bond "
           f"differently than the root does — different inflections live different lives "
           f"(see layer 5's per-form charts); root-grain analysis alone would miss them."
           if _nsg > 2 * max(_nbg, 1) else
           f"root-only {_nrg} vs surface-only {_nsg}: moderate grain-sensitivity — quote "
           f"both-level bonds in any claim, use single-grain ones as leads.")
        + " Tokenizer-rule echo (#76): grain choices change verdicts — that is why the gate "
          "demands ≥2 tokenizations.")

layer(4, "DISTRIBUTION & SPATIAL  (one modality — often null)")
m = st.columns(3)
m[0].metric("frequency", dist["frequency"])
m[1].metric("surahs present", dist["n_surahs_present"])
arch = dist["archetype"]
m[2].metric("archetype", arch["tag"] if arch else "—")
if arch:
    st.markdown(f"**archetype:** {arch['tag']} — {arch['desc']} · stability {arch['stability']}")
st.markdown(f"**Beyond-chance null** (areal evenness vs frequency-matched scramble): "
            f"real I={null['real']}, null {null['null_mean']}±{null['null_sd']}, "
            f"**z={null['z']}** → _{null['interpretation']}_  "
            f"(this is ONE modality; for many concepts it is null — not the headline).")
if dist["hotspot_surahs"]:
    st.markdown("**top surahs by occurrence:** " +
                ", ".join(f"s{su}×{n}" for su, n in dist["hotspot_surahs"][:8]))
_prof = _surah_profile(id(corpus), target)
if _prof:
    cs1, cs2 = st.columns([2, 1])
    with cs1:
        _xs = list(range(1, 115))
        _figp = _go.Figure(_go.Bar(
            x=_xs, y=[_prof.get(s, 0) for s in _xs],
            marker_color=["#E63946" if s in _MEDC else "#1D9E75" for s in _xs],
            hovertemplate="sūra %{x}: %{y}×<extra></extra>"))
        _figp.update_layout(height=270, margin=dict(l=10, r=10, t=40, b=10),
                            title="occurrences across all 114 sūras "
                                  "(🟩 Meccan · 🟥 Medinan — control-only)",
                            xaxis_title="sūra (muṣḥaf order)", yaxis_title="count")
        st.plotly_chart(_figp, use_container_width=True)
        st.caption("❓ the full positional profile behind the hotspot list. Read with the order "
                   "lenses: adjacent sūras cohere beyond length (#57); some features ride "
                   "revelation-time waves (#70). The Meccan/Medinan cut is a human frame — "
                   "control, never a claim.")
    with cs2:
        _figz = _go.Figure()
        _figz.add_trace(_go.Bar(x=["real"], y=[null["real"]], marker_color="#1D3557",
                                showlegend=False))
        _figz.add_trace(_go.Bar(x=["scramble"], y=[null["null_mean"]],
                                error_y=dict(type="data", array=[2 * null["null_sd"]]),
                                marker_color="#B4B2A9", showlegend=False))
        _figz.update_layout(height=270, margin=dict(l=10, r=10, t=40, b=10),
                            title=f"areal evenness vs null (z={null['z']})")
        st.plotly_chart(_figz, use_container_width=True)
        st.caption("❓ dark = real statistic; grey = frequency-matched scramble ±2σ. Inside the "
                   "grey band = chance-level — most concepts are, and that honest null is the "
                   "design stance.")

if res["senses"]:
    layer(5, "SURFACE-FORM SENSES  (the sense geography)")
    _sn = [(s["form"], int(s["count"])) for s in res["senses"][:8]]
    if len(_sn) > 1:
        _figs = _go.Figure(_go.Pie(labels=[f for f, _ in _sn], values=[c for _, c in _sn],
                                   hole=0.5))
        _figs.update_layout(height=290, margin=dict(l=10, r=10, t=40, b=10),
                            title="surface-form share — which inflections carry the concept")
        st.plotly_chart(_figs, use_container_width=True)
        st.caption("❓ one root, several surface lives. A form holding >60% = a frozen formula; "
                   "an even split = a productive root. Morphology grain matters: the seal's apt "
                   "unit is the FORM, not the root (#62).")
    for s in res["senses"][:6]:
        with st.expander(f"{s['form']}   (×{s['count']})"):
            _fp = _form_profile(id(corpus), s["form"])
            if _fp:
                st.plotly_chart(
                    _profile_bar(_fp, f"{s['form']} — frequency by sūra "
                                      "(🟩 Meccan · 🟥 Medinan, control-only)"),
                    use_container_width=True, key=f"fp_{s['form']}")
                _mx = max(_fp, key=_fp.get)
                _med_n = sum(v for k, v in _fp.items() if k in _MEDC)
                _tot_n = sum(_fp.values())
                st.caption(f"❓ word-boundary matches incl. cliticized variants (n={_tot_n}; the "
                           f"×{s['count']} headline uses the worker's own tokenization). Peak: "
                           f"sūra {_mx} ({_fp[_mx]}×) · Medinan share {100 * _med_n / _tot_n:.0f}% "
                           f"— compare this form's geography with the ROOT profile in layer 4: a "
                           f"form whose shape departs from its root's is doing its own work "
                           f"(#62: the seal's apt unit is the form).")
            st.markdown("**co-locators:**")
            _show_chips([r for r, a, p in s["share"]], n=6)

mrows = res["morphology"]
if mrows and isinstance(mrows[0], dict) and "error" not in mrows[0]:
    layer(6, "MORPHOLOGY  (attached particles)")
    import pandas as pd
    st.dataframe(pd.DataFrame(mrows), use_container_width=True, hide_index=True)

st.divider()
layer(7, "REPORT  (Word · three registers)")
if st.button("Generate report", type="primary", key="gen_concept"):
    try:
        import report_dive as RP
        _regs = ["technical", "plain_en", "plain_fa"]
        _b = st.progress(0.0, text="Generating report…")
        _docs = {}
        for _i, _reg in enumerate(_regs):
            _b.progress(_i / len(_regs), text=f"Generating {_reg.replace('_', ' ')}…")
            _docs[_reg] = RP.docx_bytes_from_result(res, _reg)
        _b.empty()
        st.session_state["concept_report"] = {"target": target, "docs": _docs}
    except Exception as e:
        st.warning(f"Report generation unavailable: {e}")
_rep = st.session_state.get("concept_report")
if _rep and _rep.get("target") == target:
    dl = st.columns(3)
    for col, (reg, label) in zip(dl, [("technical", "Technical"),
                                      ("plain_en", "Plain English"),
                                      ("plain_fa", "فارسی / Persian")]):
        col.download_button(f"⬇ {label}", _rep["docs"][reg],
                            file_name=f"concept_{target}_{reg}.docx",
                            mime=("application/vnd.openxmlformats-officedocument"
                                  ".wordprocessingml.document"),
                            key=f"dl_concept_{reg}", use_container_width=True)
    st.caption(f"Generated on demand. Matching PDFs come from the local worker: "
               f"`python deep_dive.py concept {target} --reports`.")
