# -*- coding: utf-8 -*-
"""🪜 Structure Map — structure at every scale (āyah · passage · sūra · Qur'ān).

Each scale uses the method that survives it (co-occurrence saturates above the āyah), every one
measured against the text's own shuffle. Engine: structure_scales.py. Research dossier:
research/intrinsic/MULTISCALE_STRUCTURE.md.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

import structure_scales as SS
import surah_reader as _SR
import meaning as _MEAN
import mobile as _MOB
from state import get_corpus, hero, layer, log_page

st.set_page_config(page_title="Structure Map", page_icon="🪜", layout="wide")
log_page("structure_map")
_MOB.inject()                       # Qur'an webfonts so the ORIGINAL text renders correctly
corpus = get_corpus()

hero("🪜 Structure Map — every scale",
     "Āyah · passage · sūra · whole Qur'ān — each measured with the method that fits it, vs the text's own shuffle.")

st.markdown(
    "<div style='background:#F4F9F7;border:1px solid #cfe4dc;border-radius:10px;padding:10px 14px;"
    "font-size:13.5px;color:#10243A;line-height:1.7;margin:2px 0 8px'>"
    "Co-occurrence <b>saturates</b> as the window grows (triad closure 53% → 98% → 100% from āyah to "
    "sūra), so one method cannot span scales. Here each scale gets its own robust instrument: "
    "<b>āyah</b> = frequency-controlled bonds (NPMI); <b>passage</b> = sequential weave; "
    "<b>sūra</b> = TF-IDF signature + coherence; <b>Qur'ān</b> = NMF theme factorization.</div>",
    unsafe_allow_html=True)


@st.cache_data(show_spinner="Mapping structure at every scale…")
def _compute(_cid):
    return {
        "bonds": SS.ayah_bonds(corpus),
        "clusters": SS.ayah_clusters(corpus),
        "weave": SS.passage_weave(corpus),
        "decay": SS.weave_decay(corpus),
        "sig": SS.sura_signatures(corpus),
        "coher": SS.sura_coherence(corpus),
        "themes": SS.quran_themes(corpus),
    }


D = _compute(id(corpus))
INK = "#10243A"

# ONE translation control for the whole page — ORIGINAL Arabic is always the anchor; this only
# chooses which translation rides alongside in the read-backs below.
_MP = _MEAN.translation_control(st)
st.caption("Original Arabic is the anchor (always shown). Pick a translation to read alongside.")

# ── one-glance scorecard: structure found at each scale, vs the text's own shuffle ──
_sc_bonds, _sc_n = D["bonds"]
st.dataframe(pd.DataFrame([
    {"scale": "Āyah", "structure": "concept bonds", "method": "NPMI (frequency-controlled)",
     "strength vs shuffle": f"{_sc_n} strong bonds (NPMI > 0.3)",
     "what it means": "which ideas a verse pairs together"},
    {"scale": "Passage", "structure": "sequential weave",
     "method": "adjacent-verse reuse vs order-shuffle",
     "strength vs shuffle": f"z = {D['weave']['z']:.0f}",
     "what it means": "verse order carries meaning"},
    {"scale": "Sūra", "structure": "internal coherence",
     "method": "TF-IDF signature vs verse→sūra shuffle",
     "strength vs shuffle": f"z = {D['coher']['z']:.0f}",
     "what it means": "each chapter is a real theme-unit"},
    {"scale": "Qur'ān", "structure": "thematic blocks", "method": "NMF on root × sūra",
     "strength vs shuffle": f"{len(D['themes']['themes'])} themes · localized "
     f"{D['themes']['real_spread']:.0f} vs {D['themes']['rand_spread']:.0f}",
     "what it means": "themes are placed, not scattered"},
]), use_container_width=True, hide_index=True)

_EXPL = {
    "ayah": (
        "**Concept.** An āyah is the smallest unit that carries a complete sense. Structure at this "
        "scale means which root-ideas a verse draws together more than their individual frequencies "
        "would predict — the verse's internal semantic bonds, measured frequency-controlled (NPMI), "
        "not by raw co-occurrence (which only reflects how common a word is).\n\n"
        "**Finding & significance.** The strongest bonds are the Qur'ān's own concept-pairs — جري·تحت "
        "(rivers flowing beneath), شمس·قمر, نفخ·صور (the Trumpet), مريم·عيسى — and they group into "
        "coherent families. The verse behaves as a designed semantic packet whose content roots "
        "co-select rather than co-occur by chance. Value: a verified, readable map of which ideas the "
        "text binds at verse level. Significance: it grounds every larger-scale claim in observable, "
        "frequency-honest association. [MEASURED]"),
    "passage": (
        "**Concept.** A passage is several consecutive āyāt read as one stretch (a rukūʿ-like unit). "
        "Structure here is sequential — do neighbouring verses share roots, i.e. does the ORDER of "
        "verses carry meaning? Measured as IDF-weighted root reuse between adjacent verses against a "
        "within-sūra verse-order shuffle.\n\n"
        "**Finding & significance.** The weave runs far above shuffle (z ≈ 40), and reuse decays "
        "smoothly with distance — strongest for immediate neighbours, fading over a handful of verses, "
        "which defines the natural passage size. Value: verse order is load-bearing — reorder a "
        "chapter's verses and the weave collapses. Significance: the Qur'ān is not a bag of independent "
        "verses; it is sequenced, and the sequence is intrinsic and measurable. [MEASURED]"),
    "sura": (
        "**Concept.** A sūra is a chapter — a bounded thematic unit. Structure at this scale is "
        "whole-chapter coherence: do a sūra's verses share a distinctive vocabulary (a signature) that "
        "sets the chapter apart? Measured as each verse's fit to its own chapter's root profile versus "
        "a verse→sūra reassignment shuffle.\n\n"
        "**Finding & significance.** Coherence is far above chance (z ≈ 54), the per-sūra signatures "
        "recover each chapter's identity (Yūsuf → prison · shirt · brother; Ikhlāṣ → one · beget; "
        "Fātiḥa → path · mercy · praise), and it is not a length artifact. Value: the sūra is a genuine "
        "unit of meaning, not an arbitrary container. Significance: the chapter division is intrinsic "
        "to the text's own vocabulary, not merely traditional. [MEASURED]"),
    "quran": (
        "**Concept.** At the whole-book scale, structure is the macro-architecture: do the roots "
        "organise into a few themes, and are those themes arranged — placed in particular regions of "
        "the muṣḥaf rather than scattered? Measured by factoring the root×sūra matrix (NMF) into themes "
        "and testing their positional spread against a shuffle.\n\n"
        "**Finding & significance.** Twelve interpretable themes emerge — oneness, judgment, charity, "
        "refuge, community-and-law — and they localise in canonical order (within-theme spread ≈ 19 vs "
        "≈ 30 shuffled), each tilting Meccan or Medinan. Value: a navigable map of the book's thematic "
        "territory. Significance: the canonical arrangement is not random — themes cluster by position, "
        "intrinsic evidence bearing on why the sūras sit in this order. [MEASURED]"),
}


@st.cache_data(show_spinner=False)
def _bondh(a, b):
    return SS.bond_word_hits(corpus, a, b, 30)


@st.cache_data(show_spinner=False)
def _themeh(roots):
    return SS.theme_word_hits(corpus, list(roots), 30)


@st.cache_data(show_spinner=False)
def _sighits(sura, roots):
    return SS.sura_sig_hits(corpus, sura, list(roots), 15)


def _hits(rows, empty="(none)"):
    """Dense read-out: ref + the actual words, in a multi-column grid that FILLS the width."""
    if not rows:
        st.caption(empty); return
    cells = []
    for s, a, words in rows:
        cells.append(
            "<div style='display:flex;gap:8px;align-items:baseline;padding:4px 8px;border-bottom:1px solid #eef2f4'>"
            f"<span style='font-weight:800;color:#0F6E56;font-size:13px;white-space:nowrap'>{s}:{a}</span>"
            f"<span class='qv-ar' dir='rtl' style='font-size:20px;line-height:1.6;color:#10243A'>{words}</span></div>")
    st.markdown("<div style='display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));"
                "gap:0 16px'>" + "".join(cells) + "</div>", unsafe_allow_html=True)


def _verse_cards(refs, langs, empty="(no verses)"):
    """Render āyāt: ORIGINAL Arabic (anchor) + the chosen translation."""
    if not refs:
        st.caption(empty); return
    parts = ["<div style='display:grid;grid-template-columns:1fr;gap:6px;margin-top:4px'>"]
    for s, a in refs:
        try:
            ar = _SR._aryah(f"{s}:{a}") or ""
        except Exception:
            ar = ""
        # respect the user's choice: Off (langs empty) → ORIGINAL ONLY, no translation forced
        mean = _MEAN.meaning_block_html(f"{s}:{a}", langs=langs) if langs else ""
        parts.append(
            "<div style='border:1px solid #E2E8F1;border-radius:10px;padding:8px 12px;background:#fff'>"
            f"<div style='font-size:12.5px;font-weight:800;color:#0F6E56'>{s}:{a}</div>"
            f"<div class='qv-ar' dir='rtl' style='text-align:right;font-size:23px;line-height:2;color:#10243A'>{ar}</div>"
            f"{mean}</div>")
    parts.append("</div>")
    st.markdown("".join(parts), unsafe_allow_html=True)


def _lay(fig, title, h=420):
    fig.update_layout(title=dict(text=f"<b>{title}</b>", x=0.5, font=dict(size=15)),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#F8FAFC",
                      font=dict(size=13, color=INK), margin=dict(l=10, r=10, t=44, b=10), height=h)
    return fig


# ════════════ FOUR CHARTS · ONE PER SCALE ════════════

# 1) ĀYAH — which roots bond within a verse
st.divider()
layer(1, "Āyah")
with st.expander("ℹ️ concept · finding · significance"):
    st.markdown(_EXPL["ayah"])
bonds, n_strong = D["bonds"]
st.markdown("**Strongest concept-bonds within a verse** (NPMI, frequency-controlled):")
st.dataframe(pd.DataFrame([{"bond": f"{a} · {b}", "NPMI": n, "co-occurs": w}
                           for a, b, w, n in bonds[:40]]),
             use_container_width=True, hide_index=True, height=360)
# concept families — roots that bond together (connected groups of strong bonds)
st.markdown("**Concept families** — roots that travel together within verses:")
_fcells = ["<div style='border:1px solid #cfe4dc;border-radius:8px;padding:6px 10px;background:#F4F9F7'>"
           f"<span class='qv-ar' dir='rtl' style='font-size:18px;color:#10243A'>{' · '.join(fam[:8])}</span></div>"
           for fam in D["clusters"]]
st.markdown("<div style='display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:8px'>"
            + "".join(_fcells) + "</div>", unsafe_allow_html=True)
with st.expander("read a bond in the text"):
    _bo = [f"{a} · {b}" for a, b, _, _ in bonds[:40]]
    _bi = st.selectbox("bond", range(len(_bo)), format_func=lambda i: _bo[i], key="bond_read")
    _bh = _bondh(bonds[_bi][0], bonds[_bi][1])
    _hits(_bh, "(none)")
    with st.expander("full text + translation"):
        _verse_cards([(s, a) for s, a, _ in _bh[:10]], _MP)

# 2) PASSAGE — sequential weave per sūra
st.divider()
layer(2, "Passage")
with st.expander("ℹ️ concept · finding · significance"):
    st.markdown(_EXPL["passage"])
w = D["weave"]
per = sorted(w["per"], key=lambda x: x[0])
fig = go.Figure(go.Bar(x=[s for s, _ in per], y=[v for _, v in per], marker_color="#1D3557"))
fig.update_layout(xaxis_title="sūra (1 → 114)", yaxis_title="root reuse between adjacent āyāt")
st.plotly_chart(_lay(fig, f"How tightly adjacent āyāt are woven  ·  vs verse-shuffle z = {w['z']:.0f}",
                     h=420), use_container_width=True)
# cohesion decay — how far the weave reaches (the passage size)
dc = D["decay"]
figd = go.Figure()
figd.add_trace(go.Scatter(x=dc["d"], y=dc["real"], mode="lines+markers", name="actual order",
                          line=dict(color="#1D3557", width=3)))
figd.add_trace(go.Scatter(x=dc["d"], y=dc["floor"], mode="lines", name="shuffled floor",
                          line=dict(color="#B23A3A", width=2, dash="dash")))
figd.update_layout(xaxis_title="distance between āyāt (verses apart)",
                   yaxis_title="shared-root reuse (IDF)",
                   legend=dict(font=dict(size=12), orientation="h", y=1.12, x=0))
st.plotly_chart(_lay(figd, "How far cohesion reaches — reuse fades with distance (the passage size)",
                     h=360), use_container_width=True)

# 3) SŪRA — internal coherence per chapter
st.divider()
layer(3, "Sūra")
with st.expander("ℹ️ concept · finding · significance"):
    st.markdown(_EXPL["sura"])
cper = sorted(D["coher"]["per"], key=lambda x: x[0])
fig = go.Figure(go.Bar(x=[s for s, _ in cper], y=[v for _, v in cper], marker_color="#0F6E56"))
fig.update_layout(xaxis_title="sūra (1 → 114)", yaxis_title="how tightly its āyāt cohere")
st.plotly_chart(_lay(fig, f"Each chapter's internal coherence  ·  vs verse→sūra shuffle z = {D['coher']['z']:.0f}",
                     h=420), use_container_width=True)
# coherence vs length — coherence is not merely a size effect
from analysis import COL_SURAH as _CS
import collections as _coll
_nay = _coll.Counter(int(s) for s in corpus.df[_CS].astype(int))
_cohd = dict(D["coher"]["per"])
_sx = sorted(_cohd)
figc = go.Figure(go.Scatter(
    x=[_nay.get(s, 0) for s in _sx], y=[_cohd[s] for s in _sx], mode="markers",
    marker=dict(size=8, color="#0F6E56", line=dict(width=1, color="#10243A")),
    text=[f"S{s}" for s in _sx], hoverinfo="text+x+y"))
figc.update_layout(xaxis_title="sūra length (# āyāt)", yaxis_title="internal coherence")
st.plotly_chart(_lay(figc, "Coherence vs length — coherence is not just a size effect", h=340),
                use_container_width=True)
sig = D["sig"]
with st.expander("a sūra's signature roots + text"):
    _names = {}
    try:
        from analysis import COL_SURAH, COL_SURAH_NAME
        for s, n in zip(corpus.df[COL_SURAH].astype(int), corpus.df[COL_SURAH_NAME]):
            _names.setdefault(int(s), str(n))
    except Exception:
        pass
    _sel = st.selectbox("sūra", sorted(sig), format_func=lambda s: f"{s} · {_names.get(s, '')}", key="sig_sel")
    st.markdown("**Signature roots:** " + " · ".join(f"`{r}`" for r in sig.get(_sel, [])))
    _sigh = _sighits(int(_sel), tuple(sig.get(_sel, [])))
    _hits(_sigh, "(none)")
    with st.expander("full text + translation"):
        _verse_cards([(s, a) for s, a, _ in _sigh[:10]], _MP)

# 4) QUR'ĀN — where each theme lives across the muṣḥaf
st.divider()
layer(4, "Qur'ān")
with st.expander("ℹ️ concept · finding · significance"):
    st.markdown(_EXPL["quran"])
th = D["themes"]; themes = th["themes"]
labels = [" · ".join(t["roots"][:3]) for t in themes]
fig = go.Figure()
fig.add_trace(go.Bar(orientation="h", y=labels, x=[t["hi"] - t["lo"] for t in themes],
                     base=[t["lo"] for t in themes], marker_color="#D6E3EC",
                     hoverinfo="skip", showlegend=False))
fig.add_trace(go.Scatter(
    x=[t["meanpos"] for t in themes], y=labels, mode="markers",
    marker=dict(size=13, color=[t["meccan_frac"] for t in themes], colorscale="RdBu", cmin=0, cmax=1,
                showscale=True, colorbar=dict(title="Meccan<br>share", thickness=12),
                line=dict(width=1, color="#10243A")),
    hovertext=[f"peak S{t['suras'][0]} · span S{t['lo']}–{t['hi']}" for t in themes],
    hoverinfo="text", showlegend=False))
fig.update_layout(xaxis_title="sūra position 1 → 114  (left = early, right = late)",
                  yaxis=dict(autorange="reversed"))
st.plotly_chart(_lay(fig, f"Where each theme lives  ·  themes cluster (spread {th['real_spread']:.0f} vs {th['rand_spread']:.0f} shuffled)",
                     h=440), use_container_width=True)
# Meccan / Medinan tilt per theme (the revelation-arrangement dimension)
_tilt = sorted(themes, key=lambda t: t["meccan_frac"])
figt = go.Figure(go.Bar(
    orientation="h", y=[" · ".join(t["roots"][:3]) for t in _tilt],
    x=[t["meccan_frac"] * 100 for t in _tilt],
    marker=dict(color=[t["meccan_frac"] for t in _tilt], colorscale="RdBu", cmin=0, cmax=1)))
figt.add_vline(x=50, line=dict(color="#10243A", width=1, dash="dash"))
figt.update_layout(xaxis_title="Meccan share of the theme (%)  ·  left = Medinan, right = Meccan")
st.plotly_chart(_lay(figt, "Each theme's Meccan vs Medinan tilt (revelation arrangement)", h=420),
                use_container_width=True)
st.dataframe(pd.DataFrame([{"theme (top roots)": " · ".join(t["roots"]),
                            "span": f"S{t['lo']}–{t['hi']}", "center": f"S{round(t['meanpos'])}",
                            "Meccan %": f"{t['meccan_frac']:.0%}"} for t in themes]),
             use_container_width=True, hide_index=True, height=340)
try:                       # cross-link: this is corpus-wide NMF; Topic Modeling is per-root (Louvain)
    st.page_link("pages/9_Topic_Modeling.py",
                 label="→ Topic Modeling — query-driven, per-root themes (the complementary lens)", icon="🧩")
except Exception:
    pass
with st.expander("read a theme in the text"):
    _to = [" · ".join(t["roots"][:4]) for t in themes]
    _ti = st.selectbox("theme", range(len(_to)), format_func=lambda i: _to[i], key="theme_read")
    _thh = _themeh(tuple(themes[_ti]["roots"]))
    _hits(_thh, "(none)")
    with st.expander("full text + translation"):
        _verse_cards([(s, a) for s, a, _ in _thh[:10]], _MP)

# ════════════ SYNTHESIS — the four scales as one structure ════════════
st.divider()
st.markdown("## Synthesis — the four scales as one structure")
st.markdown(
    "Read bottom-up, the scales **nest**: verse-level concept-bonds chain into a sequential "
    f"**passage** weave (z ≈ {D['weave']['z']:.0f}); passages cohere into thematic **sūras** "
    f"(z ≈ {D['coher']['z']:.0f}); sūras condense into {len(themes)} **themes** that are *placed*, "
    f"not scattered ({th['real_spread']:.0f} vs {th['rand_spread']:.0f} shuffled). The same roots, "
    "magnified, become **bond → sequence → theme → arrangement** — one object at four resolutions, "
    "each beating its own shuffle.")
st.markdown(
    "**What four scales gave us that one scale could not:** (1) a method correction — structure does "
    "**not** all live in co-occurrence; widen the window and it *saturates*, so the higher scales are "
    "invisible to the verse-level tool and need different instruments; (2) evidence the design is "
    "**multi-scale** — every rung independently beats shuffle, so it is neither merely local "
    "verse-pairing nor merely global arrangement, but a coherent ladder where each rung is load-bearing.")

# summary chart — co-occurrence saturates with scale (measured)
_sc = ["āyah", "passage", "sūra", "Qur'ān"]
figsat = go.Figure()
figsat.add_trace(go.Bar(x=_sc, y=[53, 98, 100, 100], name="triad closure %", marker_color="#B23A3A"))
figsat.add_trace(go.Scatter(x=_sc, y=[1.5, 0.0, 0.0, 0.0], name="genuine 3-way %", yaxis="y2",
                            mode="lines+markers", line=dict(color="#1D9E75", width=3)))
figsat.update_layout(yaxis=dict(title="triad closure %"),
                     yaxis2=dict(title="genuine 3-way %", overlaying="y", side="right"),
                     legend=dict(font=dict(size=12), orientation="h", y=1.15, x=0))
st.plotly_chart(_lay(figsat, "Why one method can't span scales — co-occurrence saturates as the window grows",
                     h=340), use_container_width=True)
st.caption("As the window grows almost every root-pair co-occurs (closure → 100%) and genuine "
           "higher-order signal vanishes — co-occurrence is a verse-scale tool. [MEASURED]")

# summary table — the nesting ladder
st.dataframe(pd.DataFrame([
    {"scale": "Āyah", "unit": "verse", "mechanism": "concept-bonds (which ideas pair)", "composes": "→ passages"},
    {"scale": "Passage", "unit": "~rukūʿ", "mechanism": "sequential weave (verse order)", "composes": "→ sūras"},
    {"scale": "Sūra", "unit": "chapter", "mechanism": "thematic coherence (chapter identity)", "composes": "→ the book"},
    {"scale": "Qur'ān", "unit": "muṣḥaf", "mechanism": "theme arrangement (placed by position)", "composes": "— whole"},
]), use_container_width=True, hide_index=True)

# ════════════ METHODS LANDSCAPE — where each tool fits ════════════
st.divider()
st.markdown("## Where each method fits — frequency · co-occurrence · dependency · motif")
# chart — which scale(s) each method serves
_meth = [("frequency (the null)", 1, 4, "#9AA7B2"), ("co-occurrence", 1, 1, "#1D9E75"),
         ("dependency graph", 1, 1.7, "#0F6E56"), ("motif (on bonds)", 1, 1, "#7209B7"),
         ("sequence / weave", 2, 2, "#1D3557"), ("coherence / signature", 3, 3, "#2C4A6E"),
         ("factorization (NMF)", 4, 4, "#E63946")]
figm = go.Figure()
for nm, lo, hi, col in _meth:
    figm.add_trace(go.Bar(orientation="h", y=[nm], x=[(hi - lo) + 0.8], base=[lo - 0.4],
                          marker_color=col, hovertext=nm, hoverinfo="text", showlegend=False))
figm.update_layout(barmode="overlay",
                   xaxis=dict(title="scale", tickvals=[1, 2, 3, 4],
                              ticktext=["āyah", "passage", "sūra", "Qur'ān"], range=[0.4, 4.6]),
                   yaxis=dict(autorange="reversed"))
st.plotly_chart(_lay(figm, "Which scale each method serves", h=320), use_container_width=True)
# table — the landscape
st.dataframe(pd.DataFrame([
    {"method": "Frequency", "captures": "how common each root is", "native scale": "all (control)",
     "role / limit": "NOT structure — the null you divide out (NPMI/lift)"},
    {"method": "Co-occurrence", "captures": "symmetric 'share a verse'", "native scale": "āyah",
     "role / limit": "saturates above the verse (closure→100%); no direction/order"},
    {"method": "Dependency graph", "captures": "directed P(B|A) + mediation (A–C via B)",
     "native scale": "āyah / local", "role / limit": "richest local lens; still within-verse"},
    {"method": "Motif (triads+)", "captures": "higher-order templates", "native scale": "āyah, on bond graph",
     "role / limit": "on raw co-occ only ~0.5% beyond pairwise — use on sparse bonds"},
    {"method": "Sequence (weave)", "captures": "order of verses", "native scale": "passage",
     "role / limit": "the channel co-occurrence cannot see"},
    {"method": "Coherence (signature)", "captures": "chapter identity", "native scale": "sūra",
     "role / limit": "a profile method, not pairwise"},
    {"method": "Factorization (NMF)", "captures": "themes + arrangement", "native scale": "Qur'ān",
     "role / limit": "the global tool co-occurrence saturates over"},
]), use_container_width=True, hide_index=True)
st.caption("Frequency is the yardstick, not a finding. Co-occurrence — and its directed refinement, the "
           "dependency graph — is a verse-scale tool; motif belongs on the sparsified bond graph; the "
           "higher scales need sequence, coherence, and factorization.")

# ════════════ IN PLAIN WORDS — summary & takeaway ════════════
st.divider()
st.markdown("""
## In plain words — what this tab shows

**The idea in one breath.** Think of the Qur'ān like a piece of music, or a building: you can look at
a single note, a phrase, a movement, or the whole symphony — and each level has its own kind of order.
This tab looks at the text's **root-words** (the original Arabic, stripped to their core) at four zoom
levels — a verse, a few verses, a chapter, and the whole book — and at each level asks: is there real
structure here, or is it random? To stay honest, every pattern is compared against the text's **own
shuffled version** (its words reshuffled by chance). Only patterns that beat that shuffle count.

**Āyah — the words that keep company.** Inside one verse, certain ideas travel together far more than
chance: sun with moon, rivers with "flowing beneath," the Trumpet with "blowing." It is like noticing
which instruments tend to play in the same chord. We measure it *fairly* — dividing out how common each
word is — so everyday words can't fake a bond. The result is a clean map of the Qur'ān's own
concept-pairs, and they fall into natural families.

**Passage — verses holding hands.** Move up to a handful of consecutive verses and a second order
appears: each verse reuses words from the one before it, like a melody where every phrase echoes the
last. It runs far beyond a shuffled order, and it fades the farther apart two verses sit — which reveals
the natural size of a "paragraph." Reorder a chapter's verses and the thread breaks: the sequence is
doing real work.

**Sūra — each chapter's fingerprint.** Zoom to a whole chapter and it has a distinctive vocabulary — a
fingerprint. Joseph's chapter leans on *father, brother, prison, shirt*; Sincerity on *one, beget*; the
Opening on *path, mercy, praise*. Its verses cling to that fingerprint far more than chance, so a chapter
is a real unit of meaning, not just a box drawn around some verses.

**Qur'ān — the shelves of the whole library.** Step all the way back and the thousands of roots collapse
into about a dozen themes — oneness, judgment, charity, refuge, community and law. The striking part:
these themes are **placed, not scattered** — like a library where books on one subject sit on the same
shelf, related chapters cluster in one region of the book, each theme leaning earlier (Meccan) or later
(Medinan). The order of the chapters carries design.

**Why four different tools?** You'd expect one method to handle all of it. It can't — and that's a real
lesson. "Co-occurrence" (do two words share a verse?) works beautifully up close, but as you zoom out it
blurs: in a whole chapter almost every word shares space with every other, so the lens goes white.
Different distances need different instruments — a microscope for the verse, a thread-tracer for the
passage, a fingerprint reader for the chapter, a floor-plan for the book. Frequency itself is never the
structure; it is only how loudly a word is repeated — the yardstick we divide out.

**The takeaway.** Anchored entirely on the original Arabic roots and tested only against the text's own
shuffle, structure shows up at **every** scale — and the scales **nest**: word-bonds build passages,
passages build chapters, chapters arrange into a themed whole. The Qur'ān is not a bag of verses, and
its order is not arbitrary; it is organized top to bottom, and that organization is measurable.
""")
