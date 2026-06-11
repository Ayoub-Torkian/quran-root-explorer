"""Lens Lab — the 18 computational lenses, one honest verdict card each.

v2.0 re-spine surface (APP_PLAN.md). Every card shows: claim · key statistic vs
its null · comparator boundary · GATE verdict. Honest nulls are first-class
results — most modalities ARE null; that is the finding. Single source of truth:
FINDINGS_SYNTHESIS.md (kept in lockstep with EVIDENCE.md / SIX_LENSES_PAPER.md).
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

import state as S
import lens_live as LL

st.set_page_config(page_title="Lens Lab", page_icon="🧪", layout="wide")
S.log_page("lens_lab")
try:
    S.inject_css()
except Exception:
    pass
try:
    S.render_grouped_nav()
except Exception:
    pass

NAVY = "#1D3557"; TEAL = "#1D9E75"; RED = "#E63946"; AMBER = "#E9C46A"; GREY = "#B4B2A9"

VERDICT_STYLE = {
    "DISTINCTIVE":   (TEAL,  "✅ DISTINCTIVE (cross-text, gated)"),
    "INTERNAL-ONLY": (AMBER, "🟡 INTERNAL-ONLY / down-weighted"),
    "NULL":          (GREY,  "⚪ NULL / register-level"),
    "BLOCKED":       (RED,   "⛔ DATA/TOOL-BLOCKED"),
}

# (lens#, name, scales, verdict, claim, stat-vs-null, boundary, evidence refs)
LENSES = [
    (9, "Varied long-range recurrence — Architecture of Return", "🧩 Semantic",
     "DISTINCTIVE",
     "The Qur'an re-expresses the same content across long ranges far more than ordinary prose — return without refrain.",
     "~+3σ vs ordinary (word-shuffle null, verbatim excluded); recurrence pairs cos 0.68 but edit-sim 0.27 (#61: same matter, re-sequenced).",
     "Shared in kind with poetry (+2σ); the Qur'an maximises it. THE unifying thesis.",
     "#42/#43/#61"),
    (17, "Fāṣila system (verse-end seals)", "🔤 Sequence · 🧩 Semantic",
     "DISTINCTIVE",
     "Endings repeat heavily AND predict their āyah's body content, whatever the seal names.",
     "Repeat-share 0.18 surface vs sajʿ 0.04 / ord 0.10 / poetry 0.02 (#63, #76-corrected); content-fit z≈+12 root & morph grain (#62); referent-general 15/16 classes (#77).",
     "Repetition is cross-text (vs-ord ≈+2.2σ); content-fit is Qur'an-internal. Sajʿ rhymes but does not return.",
     "#62/#63/#76/#77"),
    (15, "Muqaṭṭaʿāt — rasm pointer", "🧭 Position · 🔤 Sequence",
     "DISTINCTIVE",
     "Exactly half the alphabet, spatially clustered, internally order-disciplined, deployed in revelation-time waves.",
     "14/28 letters; Moran's I +0.54 p<1e-4 (robust under nuzūl); no letter-pair ever reversed, order-consistency near ceiling (#68/#69); combo-reuse z=−12.6, family waves z≈−5 (#67).",
     "Sui generis (no comparator has this layer). Content is NOT letter-organized (#56/#64/#73 — honest negative). Abjadī key-match = human historical frame (stance re-weight).",
     "#50/#51/#64/#67–69"),
    (18, "Temporal deployment (waves & campaigns)", "🧭 Position · 🧩 Semantic",
     "DISTINCTIVE",
     "Some seals come in revelation-time waves and are RE-AIMED across the mission; narrative return never is.",
     "True waves survive within-period null: تعملون +5.2 / يعلمون +3.3 / اليم +3.5 (#70); content re-aiming gated: يعلمون z=+3.38, اليم +2.48, عليم +3.52 (#71/#74); 2×2 rate×content typology.",
     "Narrative anchors (Mūsā 135×…) ALL NULL — return is a standing mode, not a phase. Sharpens, not contradicts, Lens 9.",
     "#70/#71/#74/#75"),
    (3, "Rhyme persistence", "🔤 Sequence",
     "DISTINCTIVE",
     "The dominant fāṣila persists over long windows beyond sajʿ practice.",
     "+1.7σ vs sajʿ (dominant-ending share over a window).",
     "Rhyme PRESENCE itself is shared with sajʿ; persistence is the distinctive part.",
     "#34–37"),
    (5, "Fusion cell (style conjunction)", "🔤 Sequence · 🧩 Semantic",
     "DISTINCTIVE",
     "Only the CONJUNCTION (sustained rhyme × no meter × recurrence) isolates the style.",
     "Classifier AUC ≈0.94; rhyme×non-meter pair 0.92 > single axes 0.76/0.84. D1 re-run (#76): no additive synergy — the signature is a PROFILE, not a summed score.",
     "Single axes never separate; survivors live at different grains.",
     "#35/#76 (D1)"),
    (16, "Canonical-order coherence", "🧭 Position",
     "INTERNAL-ONLY",
     "Adjacent sūras are root-similar beyond the length gradient; themes are order-typed.",
     "Length-band null z=+3.14 (#57); Mantel canonical r=+0.325 > nuzūl (E4); NMF axes order-typed (#72).",
     "Ordinary prose is MORE locally coherent (E1-cmp) — internally real, not cross-text distinctive. Nuzūl interlocks seams more (#58).",
     "#57/#58/E1/E4/#72"),
    (15.1, "Muqaṭṭaʿāt content-cohesion", "🧩 Semantic",
     "INTERNAL-ONLY",
     "Muqaṭṭaʿāt sūras cohere in root-space and over-express the Book theme.",
     "Cohesion z=+6.9 (register-controlled +7.4); REV-lexicon z=+3.55, openings ~5×.",
     "Down-weighted by #59: a GENERAL grouping effect (sabʿ ṭiwāl cohere as much). Distinctiveness = position + cardinality, not content.",
     "#53–55 → #59"),
    (1, "Repetition as bulk rate", "🧩 Semantic", "NULL",
     "Is the Qur'an simply more repetitive overall?", "~+1σ — register-level only.",
     "The interesting structure is WHERE repetition sits (Lenses 9/17), not how much.", "#18s"),
    (2, "Ring composition / refrain", "🧭 Position", "NULL",
     "Global rings? Refrains?", "Rings null; refrain real but local (~9 sūras).",
     "Refrain ≠ the recurrence signature (which is varied, long-range).", "EVIDENCE"),
    (4, "Phonosemantics (sound↔meaning)", "🔤 Sequence", "NULL",
     "Do letter-sounds carry meaning?", "Null; re-confirmed at root grain by the multi-layer connectome (corr −0.018, gate fires z≈+15).",
     "Letter layer ⊥ meaning layer everywhere tested (#38/#56/#64/#73).", "#38/#73"),
    (6, "Prosody at text level", "🔤 Sequence", "NULL",
     "Text-level prosodic fingerprint?", "Null at this grain.",
     "The recited layer needs vocalized comparators (Lens 14).", "EVIDENCE"),
    (7, "Iltifāt (person-shift)", "🧩 Semantic", "NULL",
     "Is grammatical person-shift rate distinctive?", "Null vs prose (referent-blind count).",
     "Referent-AWARE iltifāt remains coref-blocked (frontier).", "#40"),
    (8, "Wazn (morphological templates)", "🔤 Sequence", "NULL",
     "Template distribution distinctive? At the fāṣila?", "Register-level; attr-ending enrichment 1.21× ≈ sajʿ 1.32×.",
     "Sharpens Lens 17: the distinctive part is repetition of the SAME attributes + content-fit, not the template class.", "#41"),
    (10, "Discourse macro-structure", "🧩 Semantic", "NULL",
     "Are speech-act move SEQUENCES distinctive?", "Sequencing null (switch d=−0.86); move-INVENTORY +2.4σ register-level.",
     "The Qur'an interleaves more genres, but their ordering is not a fingerprint.", "#44"),
    (11, "Shallow syntax (parataxis)", "🔤 Sequence", "NULL",
     "Parataxis vs hypotaxis fingerprint?", "Register-level; wāw-parataxis +1.9σ but sajʿ exceeds.",
     "Confirmed by the real parser (Lens 13).", "#45"),
    (12, "Lexical-semantic field dynamics", "🧩 Semantic", "NULL",
     "Do topical fields sequence/cluster distinctively?", "Both taggers null (|g|<0.5σ); Qur'an clusters fields LESS than ordinary if anything.",
     "Field-recurrence re-open (D2) also null.", "#46"),
    (13, "Dependency syntax (real parser)", "🔤 Sequence", "NULL",
     "Embedding-depth fingerprint?", "Qur'an BELOW ordinary prose on every metric (depth g=−0.66); above poetry/sajʿ; all sub-2σ.",
     "Syntactically SIMPLER than prose — self-contained āyāt (fits the thesis).", "#47"),
    (14, "Recited / phonological layer", "🔤 Sequence", "BLOCKED",
     "Rhythm/tajwīd distinctiveness in the VOCALIZED text.",
     "Instrument built & internally valid: short sūras more isochronous (CV 0.36 vs 0.48); weight-alternation z=−10.7 (Baqara).",
     "DATA-BLOCKED: needs vocalized comparators (drop Tashkeela / voc dīwān into corpus/, run run_recited_phon.py). Deprioritized: ḥarakāt = human layer.",
     "#49"),
]


S.hero("🧪 Lens Lab — Eighteen Computational Lenses",
       "One card per lens: claim · statistic vs null · comparator boundary · gate verdict. "
       "Honest nulls are first-class results.")

st.markdown(
    f"<div style='background:#EEF3FB;border-left:5px solid {NAVY};border-radius:8px;"
    "padding:10px 14px;margin:6px 0 14px;font-size:14px;'>"
    "<b>The thesis (falsifiable):</b> locally the Qur'an is <i>less</i> continuous than ordinary "
    "prose (self-contained āyāt); at long range it <b>returns</b> to itself more — the "
    "<b>Architecture of Return</b>. Four lens families survive every control; ~12 are honest "
    "nulls; one layer (muqaṭṭaʿāt) is sui generis. Coverage ≈74% of the search space "
    "(<code>COVERAGE_MAP.html</code>). Full numbers: <code>EVIDENCE.md</code> · digest: "
    "<code>FINDINGS_SYNTHESIS.md</code> · narrative: <code>SIX_LENSES_PAPER.md</code>.</div>",
    unsafe_allow_html=True)

# ── LOCKED UI STANDARD: comprehensive-summary headline metrics FIRST, then charts ──
from collections import Counter as _Ctr

import plotly.graph_objects as _go

_vc = _Ctr(L[3] for L in LENSES)
st.markdown("#### 📌 Comprehensive summary")
sm = st.columns(5)
sm[0].metric("lenses tested", "18", f"{len(LENSES)} verdict cards", delta_color="off",
             help="The full modality sweep since v1.2 — every way we know to read the text "
                  "computationally. One lens can carry several filed experiments (#18–#77).")
sm[1].metric("distinctive", _vc["DISTINCTIVE"], "cross-text, gated", delta_color="off",
             help="Survived ALL controls: equal-N + null + same-language comparators + "
                  "positive-control gate. Four families: return (#42), fāṣila system (L17), "
                  "muqaṭṭaʿāt (L15), temporal deployment (L18) — plus rhyme persistence and "
                  "the #35 conjunction.")
sm[2].metric("honest nulls", _vc["NULL"], "register-level", delta_color="off",
             help="Most modalities are NULL — that IS the finding. Sound-symbolism, syntax "
                  "depth, discourse ordering, field dynamics: indistinguishable from register "
                  "once properly nulled. Their presence is what makes the positives credible.")
sm[3].metric("coverage", "≈74%", "of the search space", delta_color="off",
             help="COVERAGE_MAP accounting after consolidation #77. Largest unexplored region: "
                  "the recited/phonological layer (blocked until vocalized comparators exist).")
sm[4].metric("strongest", "+3σ", "#42 recurrence", delta_color="off",
             help="Long-range varied recurrence vs ordinary Arabic — word-shuffle-netted, "
                  "verbatim excluded, canonical cell B=300. Poetry shares it in kind (+2σ); "
                  "the Qur'an maximises it. The unifying thesis: Architecture of Return.")

_cc1, _cc2 = st.columns([1, 2])
with _cc1:
    _fig_d = _go.Figure(_go.Pie(
        labels=["distinctive", "internal-only", "null / register", "blocked"],
        values=[_vc["DISTINCTIVE"], _vc["INTERNAL-ONLY"], _vc["NULL"], _vc["BLOCKED"]],
        hole=0.55, marker=dict(colors=[TEAL, AMBER, GREY, RED])))
    _fig_d.update_layout(title="verdict composition", height=300,
                         margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(_fig_d, use_container_width=True)
    st.caption("❓ the honest shape of the investigation: most lenses are null — the few "
               "positives stand on that swept ground.")
with _cc2:
    _hl = [("seal content-fit #62 (z)", 12.0),
           ("muqaṭṭaʿāt position #51 (z, Moran)", 5.8),
           ("seal wave تعملون #70 (z)", 5.2),
           ("recurrence #42 (σ vs ordinary)", 3.0),
           ("ending-repetition #63/#76 (σ vs ordinary)", 2.2),
           ("rhyme persistence #34–37 (σ vs sajʿ)", 1.7)]
    _fig_h = _go.Figure(_go.Bar(
        x=[v for _, v in _hl], y=[k for k, _ in _hl], orientation="h",
        marker_color=TEAL, hovertemplate="%{y}: %{x}<extra></extra>"))
    _fig_h.add_vline(x=2.0, line_dash="dash", line_color="#E63946")
    _fig_h.update_layout(title="headline statistics of the gated positives "
                               "(σ or z as filed — units differ, red line = 2σ bar)",
                         height=300, margin=dict(l=10, r=10, t=40, b=10),
                         yaxis=dict(autorange="reversed"))
    st.plotly_chart(_fig_h, use_container_width=True)
    st.caption("❓ every bar already survived its gate; σ = effect size vs a comparator corpus, "
               "z = permutation-null score (Qur'an-internal where marked). Full numbers and "
               "boundaries are on each card below — and #35 fusion (AUC 0.94) is a different "
               "unit, so it lives on its card.")

c1, c2 = st.columns([2, 2])
with c1:
    verdict_filter = st.multiselect(
        "Verdict", list(VERDICT_STYLE), default=list(VERDICT_STYLE))
with c2:
    scale_filter = st.multiselect(
        "Scale", ["🧭 Position", "🔤 Sequence", "🧩 Semantic"], default=[])


def _card(num, name, scales, verdict, claim, stat, boundary, refs):
    color, badge = VERDICT_STYLE[verdict]
    n = int(num) if float(num).is_integer() else num
    st.markdown(
        f"<div style='border:1px solid #E2E8F1;border-left:6px solid {color};"
        "border-radius:10px;padding:12px 16px;margin:8px 0;background:#FFFFFF;'>"
        f"<div style='display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;'>"
        f"<b style='color:{NAVY};font-size:15px;'>Lens {n} — {name}</b>"
        f"<span style='font-size:12px;font-weight:700;color:{color};'>{badge}</span></div>"
        f"<div style='font-size:12px;color:#3D4757;margin:2px 0 6px;'>{scales} &nbsp;·&nbsp; EVIDENCE {refs}</div>"
        f"<div style='font-size:13.5px;margin-bottom:4px;'><b>Claim:</b> {claim}</div>"
        f"<div style='font-size:13.5px;margin-bottom:4px;'><b>Statistic vs null:</b> {stat}</div>"
        f"<div style='font-size:13px;color:#3D4757;'><b>Boundary:</b> {boundary}</div>"
        "</div>", unsafe_allow_html=True)


def _hbar(label, val, vmax, color, fmt):
    pct = max(2, min(100, int(100 * val / (vmax + 1e-9))))
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:8px;font-size:13px;margin:2px 0;'>"
        f"<span style='width:70px;'>{label}</span>"
        f"<div style='flex:1;background:#E2E8F1;border-radius:4px;height:13px;'>"
        f"<div style='width:{pct}%;height:13px;border-radius:4px;background:{color};'></div></div>"
        f"<span style='width:80px;font-weight:700;color:{NAVY};'>{fmt}</span></div>",
        unsafe_allow_html=True)


def _live_recurrence():
    st.caption("Re-runs the #42 instrument now (intratext_lock_fixed logic): equal-P bootstrap, "
               "word-shuffle null, one cell K=50/topq=.95/gap=.25, B=20 — indicative; "
               "full battery = EVIDENCE #43.")
    if st.button("▶ Run live (~seconds; first run loads corpora)", key="run42"):
        with st.spinner("Tokenizing corpora (cached) and running the cell…"):
            df = S.corpus_data().df
            import analysis as A
            qw, _ = LL.quran_tokens(df, A.COL_DIACRITIZED)
            st.session_state["live42"] = LL.live_recurrence(qw)
    r = st.session_state.get("live42")
    if r:
        gQ, gP, gS = r["g"]["QURAN"], r["g"]["poetry"], r["g"]["saj"]
        vmax = max(abs(gQ), abs(gP), abs(gS), 0.1)
        _hbar("Qur'an", abs(gQ), vmax, TEAL, f"{gQ:+.2f}σ")
        _hbar("poetry", abs(gP), vmax, "#B4B2A9", f"{gP:+.2f}σ")
        _hbar("sajʿ", abs(gS), vmax, GREY, f"{gS:+.2f}σ")
        st.caption(f"vs ORDINARY baseline · net of word-shuffle · equal-P={r['P']} passages, "
                   f"B={r['B']} · canonical cell filed at B=300: +3.0σ (EVIDENCE #43) · "
                   f"gate {'✅ net excess > 0' if r['gate_ok'] else '⚠️ check'} · NOTE: sajʿ net is "
                   f"small-corpus unstable here; the filed sajʿ contrast is content-RETURN at window "
                   f"grain (#76: 0.407 vs 0.145 — sajʿ rhymes but does not return)")


def _live_rhyme():
    st.caption("Re-runs rhyme persistence now (#76 feature f1): dominant last-char share per "
               "K=25-unit window, unit-shuffle null × 60 — indicative; filed record = EVIDENCE #34–37/#76.")
    if st.button("▶ Run live (~seconds; first run loads corpora)", key="run03"):
        with st.spinner("Computing windows + shuffle null…"):
            df = S.corpus_data().df
            import analysis as A
            _, qu = LL.quran_tokens(df, A.COL_DIACRITIZED)
            st.session_state["live03"] = LL.live_rhyme(qu)
    r = st.session_state.get("live03")
    if r:
        m = r["means"]; vmax = max(m.values())
        _hbar("Qur'an", m["QURAN"], vmax, TEAL, f"{m['QURAN']:.3f}")
        _hbar("poetry", m["poetry"], vmax, "#B4B2A9", f"{m['poetry']:.3f}")
        _hbar("ordinary", m["ord"], vmax, GREY, f"{m['ord']:.3f}")
        _hbar("sajʿ", m["saj"], vmax, GREY, f"{m['saj']:.3f}")
        st.caption(f"dominant-ending share per window (n={r['n_windows']['QURAN']} Qur'an windows) · "
                   f"shuffle-null {r['null_mean']:.3f} → z={r['z_shuffle']:+.1f} "
                   f"{'✅ gate' if r['gate_ok'] else '⚠️'} · g vs sajʿ {r['g_vs']['saj']:+.2f}σ, "
                   f"vs ord {r['g_vs']['ord']:+.2f}σ")


LIVE = {9: ("🧪 Run this lens LIVE on the corpus", _live_recurrence),
        3: ("🧪 Run this lens LIVE on the corpus", _live_rhyme)}

shown = 0
for verdict_class in VERDICT_STYLE:
    if verdict_class not in verdict_filter:
        continue
    group = [L for L in LENSES if L[3] == verdict_class
             and (not scale_filter or any(s in L[2] for s in scale_filter))]
    if not group:
        continue
    st.markdown(f"### {VERDICT_STYLE[verdict_class][1]}")
    for L in group:
        _card(*L)
        if L[0] in LIVE:
            title, fn = LIVE[L[0]]
            with st.expander(title):
                try:
                    fn()
                except Exception as e:
                    st.error(f"Live run failed: {e}")
        shown += 1
if not shown:
    st.info("No lenses match the current filters.")

st.divider()
st.markdown(
    "**Methodology (locked, `DESIGN_STANCE.md`):** every test = equal-N + null + same-language "
    "comparator + positive-control gate; rearrangement variants built in; cross-impact propagated "
    "(nothing is final); no miracle-tone — measurements with boundaries. "
    "Try a lens live on a verse: the **Āyah Deep-Dive** page runs the Lens-17 content-fit (#62) "
    "with 150 same-N nulls per seed āyah.")
cov = Path(__file__).resolve().parent.parent / "COVERAGE_MAP.html"
if cov.exists():
    with st.expander("🗺️ Coverage map (where we are, ~74%)"):
        components.html(cov.read_text(encoding="utf-8"), height=620, scrolling=True)
