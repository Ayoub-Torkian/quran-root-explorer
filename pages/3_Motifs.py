"""Motif analysis page — triad census + triangle drill-down."""
import streamlit as st

import analysis as A
import plotly_charts as PC
from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, highlight_text, per_root_hint, log_page)

st.set_page_config(page_title="Motifs", page_icon="🔺", layout="wide")
log_page("motifs")

# ── Interpretation guide + mobile landscape hint ─────────────────────
st.markdown('<div class="landscape-hint">📱 Tip: rotate your phone sideways (landscape) for a clearer motif gallery.</div>', unsafe_allow_html=True)
with st.expander("📌 What a motif adds beyond pairwise co-occurrence (1-min)", expanded=False):
    st.markdown(
        "**Pairwise co-occurrence** asks: *do these two roots share verses?*\n\n"
        "**Motif** asks something stronger: *do these three (or four, or five) "
        "roots ALL appear in the same verse?* A motif is a higher-order pattern.\n\n"
        "Why it matters:\n"
        "- A pair sharing 50 verses is suggestive. A **triad** sharing 8 verses "
        "is structural evidence of a thematic constellation — three roots that "
        "the text deliberately brings together.\n"
        "- Pairwise stats hide cases where A-B and B-C are common, but A-B-C "
        "together is rare. Motifs make these patterns visible.\n"
        "- A high-uniqueness motif (verses contain *this exact group* and no "
        "larger group) is a stronger signal than a loose collection of pairs.\n\n"
        "To see what each motif means in context, click through to the "
        "**Ayah Browser** and read the verses that contain the full set.\n\n"
        "**Where this fits (Motif ↔ Consensus):** This page is the *within-verse* "
        "lens — directly verifiable, but blind to anything not packed into one "
        "verse. Its complement lives in **🔬 Deep Dives**: the *consensus* lens "
        "bonds concepts across THREE independent modalities (meaning · territory · "
        "distribution) and so reaches *across verses* — it finds 'latent motifs', "
        "coherent thematic triads the text weaves but never states in a single "
        "verse (e.g. لوط·ضيق·صيح). Use **Motif** for verifiable local patterns and "
        "**Deep-Dive consensus** for distributed themes; together they cover both "
        "what the text says together and what it implies apart."
    )

corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

hero("🔺 Motif Analysis",
     "Triad census, triangle subgraphs, partner-motif clusters per input root.")
per_root_hint(compact=True)

# ── LAYER 1 ──────────────────────────────────────────────────────
layer(1, "Triad census — bird's eye  (📌 comprehensive summary)")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Nodes", R["triad"]["nodes"],
          help="Roots in this co-occurrence network (your query + their partners above the "
               "weight threshold).")
c2.metric("Edges", R["triad"]["edges"],
          help="Root pairs that share at least one verse (weight = how many verses they share).")
c3.metric("Triangles (closed triads)", R["triad"]["triangles (closed triads)"],
          help="Three roots ALL pairwise verse-sharing — the structural motif unit. A triangle "
               "is much rarer than its three edges individually: it marks a deliberate "
               "thematic constellation.")
c4.metric("Open triads", R["triad"]["open triads (paths of length 2)"],
          help="A–B and B–C share verses but A–C do not (yet). The triangle/open ratio tells "
               "you how much the neighbourhood CLOSES into real constellations.")
c5.metric("Density", R["triad"]["density"],
          help="Share of all possible root-pairs that actually co-occur (0–1). Low density + "
               "many triangles = a few tight constellations inside a sparse field — the "
               "interesting regime.")
try:
    _tri = float(R["triad"]["triangles (closed triads)"])
    _opn = float(R["triad"]["open triads (paths of length 2)"])
    _clo = 3 * _tri / (3 * _tri + _opn) if (_tri + _opn) > 0 else 0.0
    st.markdown(
        f"**📍 What to take from the census:** closure rate **{_clo:.0%}** "
        f"({int(_tri)} triangles vs {int(_opn)} open paths) — "
        + ("a tightly-woven neighbourhood: partners of partners tend to also meet in verses "
           "(constellations, not chains)." if _clo > 0.3 else
           "a hub-like neighbourhood: the query root connects partners that rarely meet each "
           "other — its themes run in PARALLEL strands rather than one constellation.")
        + " Verify any triangle below by reading its actual verses (layer 4 drill-down).")
except Exception:
    pass

# ── LAYER 2 — chart ──────────────────────────────────────────────
st.divider()
layer(2, "Motif distribution")
st.plotly_chart(PC.chart_motif_summary(R["triad"]), width='stretch')

# ── LAYER 3a — VISUAL MOTIF PROGRESSION ──────────────────────────
st.divider()
layer(3, "🔭 Motif progression — dyad → triad → quad → pentad")
st.caption(
    "All four motif sizes shown together so you can see the structure grow.  "
    "🔴 red node = your input root, navy = partner; edge thickness scales with "
    "co-occurrence weight. Sections with no motifs are skipped automatically."
)

top_per_size = st.slider(
    "Top N motifs to show per size",
    min_value=1, max_value=8, value=3, key="motif_top_per_size",
    help="Each section ranks motifs by total edge weight, highest first.",
)

MOTIF_SPECS = [
    (2, "—", "Dyads", "two roots connected by a single edge"),
    (3, "🔺", "Triads", "three roots all pairwise connected (a triangle)"),
    (4, "◆", "Quads", "four roots, every pair connected (a 4-clique)"),
    (5, "⬟", "Pentads", "five roots, every pair connected (a 5-clique)"),
]

for size, icon, label, desc in MOTIF_SPECS:
    n_motifs = PC.count_motifs(R["graph"], size)
    if n_motifs == 0:
        st.markdown(
            f"<div style=\"opacity:0.55; margin:6px 0 10px 0; font-size:13px;\">"
            f"{icon}&nbsp;<b>{label}</b> &nbsp;— none in this network (the graph "
            f"isn't dense enough at size {size})."
            f"</div>",
            unsafe_allow_html=True,
        )
        continue
    st.markdown(
        f"<div style=\"margin:10px 0 4px 0; font-size:15px; font-weight:700; "
        f"color:#1D3557;\">{icon}&nbsp;{label}&nbsp;<span style=\"color:#10243A; "
        f"font-weight:600; font-size:13px;\">— {n_motifs:,} found in the network "
        f"({desc})</span></div>",
        unsafe_allow_html=True,
    )
    st.plotly_chart(
        PC.chart_motif_gallery(R["graph"], motif_size=size,
                                top_n=min(top_per_size, n_motifs),
                                input_roots=R["input_roots"]),
        width='stretch',
    )

# ── LAYER 3 — triangles ranked HONESTLY (frequency- & length-controlled) ──────────
st.divider()
layer(3, "Top triangles by association — frequency- & length-honest")
_sig, _glob = A.triad_significance(corpus, R["triangles"], R["normalize"], top=40)
with st.expander("📌 Why this no longer ranks by raw co-occurrence (1-min)", expanded=False):
    st.markdown(
        "Raw **Sum Weight** (verses the three roots share) is dominated by two things that "
        "are **not** structure:\n\n"
        "- **Frequency** — ubiquitous roots (ءله، ربب، قول) top every triangle just because "
        "they are everywhere. We divide by what each root's own frequency predicts → **Lift** "
        "(Obs ÷ Expected) and **Z (assoc)**. Lift ≈ 1 means *no more than frequency predicts*.\n"
        "- **Verse length** — long verses pack many roots, so any triple appears more often in "
        "them. **Verse len** = mean roots/verse of the shared verses; far above the global "
        f"**{_glob:.1f}** flags a long-verse artifact.\n\n"
        "**3-way p** asks the deeper question — does the triple occur more than its three "
        "*pairwise* rates already imply? Measured across the whole corpus, genuine higher-order "
        "(3-way) structure is **rare (~0.5% of triads)**: most association is pairwise + "
        "frequency + length. A **gold ring** marks the few triads that pass (3-way p < 0.05).")
if _sig is None or len(_sig) == 0:
    st.caption("(no triangles in this query's network)")
else:
    st.plotly_chart(PC.chart_triad_significance(_sig, _glob), width='stretch')
    _g = _sig[_sig["3-way p"] < 0.05]
    _top = _sig.iloc[0]
    st.markdown(
        f"**📍 What to take from this map:** ranked by **association beyond frequency**, the "
        f"strongest triad is **{_top['Root A']} · {_top['Root B']} · {_top['Root C']}** "
        f"(Lift {_top['Lift']}×, Z {_top['Z (assoc)']}). Points low on the Lift axis but far "
        f"right are **frequency artifacts**; hot-coloured points are **long-verse artifacts**. "
        + (f"**{len(_g)}** triad(s) here carry genuine 3-way structure (gold ring) — read their "
           f"verses below before calling them a theme."
           if len(_g) else "No triad here shows genuine 3-way structure beyond its pairs — "
           "treat these as pairwise associations, verified by reading the verses below."))
    st.dataframe(_sig, width='content', hide_index=True, height=360)

# ── LAYER 4 — drill into a specific triangle ─────────────────────
st.divider()
layer(4, "Drill into a triangle — see every ayah that contains all 3 roots")
if R["triangles"].empty:
    st.caption("(no triangles to drill into)")
else:
    options = [
        f"{r['Root A']} — {r['Root B']} — {r['Root C']}   (weight {r['Sum Weight']})"
        for _, r in R["triangles"].iterrows()
    ]
    pick_idx = st.selectbox("Pick a triangle", range(len(options)),
                            format_func=lambda i: options[i], key="tri_pick")
    chosen = R["triangles"].iloc[pick_idx]
    triad_tuple = (chosen["Root A"], chosen["Root B"], chosen["Root C"])
    st.markdown(
        f"<span class='pill pill-input'>{triad_tuple[0]}</span>"
        f"<span class='pill pill-input'>{triad_tuple[1]}</span>"
        f"<span class='pill pill-input'>{triad_tuple[2]}</span>",
        unsafe_allow_html=True,
    )
    ayahs = A.triangle_ayahs(corpus, triad_tuple, R["normalize"])
    st.caption(f"{len(ayahs)} ayahs contain all three roots together — laid out in 2 columns.")
    st.markdown("""
<style>
.tri-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;}
.tri-card{border:1px solid #E2E8F1;border-radius:10px;padding:8px 12px;background:#FFFFFF;}
.tri-card .ar{direction:rtl;text-align:right;font-family:'Amiri','Amiri Quran','Noto Naskh Arabic',serif;font-size:18px;line-height:1.55;color:#243447;margin:0 0 4px 0;}
.tri-card .meta{font-size:12px;color:#10243A;margin:0;}
</style>
""", unsafe_allow_html=True)
    cards = []
    for _, row in ayahs.iterrows():
        ar = row.get("Quranic Text (diacritized)") or row["Segmented Ayah"]
        meta = f"S{row['Surah #']}·A{row['Ayah #']} · {row['Surah Name']} · roots: {row['All Roots']}"
        cards.append(f"<div class='tri-card'><div class='ar'>{ar}</div><div class='meta'>{meta}</div></div>")
    st.markdown(f"<div class='tri-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)

# ── LAYER 3b — partner-motif clusters per input root ─────────────
st.divider()
layer(3, "Partner-motif clusters — top 20 partners per input root")
st.dataframe(R["pmotifs"], width='content', hide_index=True, height=380)
