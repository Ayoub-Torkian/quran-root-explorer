"""Close-up · Inter-Sūra coherence — REFUTED-ARTIFACT. 8-section anatomy, dense full-width charts."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Inter-Sūra", page_icon="🗺️", layout="wide")
if S:
    try:
        S.log_page("closeup_intersura")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()

# ── 1 · PROBLEM ──
C.hero("Inter-Sūra coherence (munāsabāt)",
       "Does the muṣḥaf place lexically-similar sūras side by side — by deliberate design?",
       "REFUTED-ARTIFACT", 30, "ROOT", "DIVINE-DEFAULT vs DIVINE-ALT · RANDOM null")
C.story(
    "The chapter order looked <b>designed</b> to seat similar sūras together — a strong signal that survived "
    "control after control. Then a tougher size control made it <b>vanish</b>.",
    "Had it held, it would be measured evidence the <i>arrangement</i> is intentional. Instead it's a clean lesson "
    "in the method refusing to fool itself — the discipline, not the headline.", accent=C.CORAL)
C.kpis([
    ("11.1", "z · vs random", "Adjacency coherence vs random shuffle of the 114 sūras", C.TEAL),
    ("9.8", "z · period-ctrl", "Survives controlling revelation era", C.TEAL),
    ("5.8", "z · size-linear", "Still alive under a linear size control", C.GOLD),
    ("−0.7", "z · size-nonlin", "Collapses under nonlinear + stratified size", C.CORAL),
    ("0.45", "optimality", "Fraction from random to the lexical optimum", C.INK),
    ("2.5 / 0", "split z", "First half (long) z 2.5 · second half (short) z ≈ 0 — the tell", C.CORAL),
    ("30", "grade", "REFUTED-ARTIFACT — recorded, not promoted", C.CORAL),
])

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If the order is designed for coherence, neighbours beat chance AND beat the mundane explanations",
          "A deliberate arrangement should seat lexically-similar chapters side by side — so adjacent sūras should "
          "share more distinctive roots than a random ordering, <i>and</i> more than length, revelation era, or "
          "sheer size already force. A surplus surviving <b>every</b> such control would fingerprint intent. A "
          "surplus that dies under one was never design — only that confound wearing a halo.", accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus",
          "<b>Substrate</b> — content roots per sūra (col 4) as TF-IDF vectors. <b>Arrangement</b> — divine-default "
          "muṣḥaf vs a divine-alternative (revelation order) and a random shuffle (null only). <b>Test</b> — mean "
          "cosine between adjacent sūras, then a regression of pairwise similarity on length-, period- and "
          "size-proximity, reading the muṣḥaf's adjacency <i>residual</i>. <b>Controls, in sequence</b> — "
          "length-matched, period, muqaṭṭaʿāt blocks, linear size, topic membership, then nonlinear + "
          "size-stratified. <b>Cross-checks</b> — held-out halves, topic-count sweep, an independent Jaccard metric.",
          accent=C.SLATE)

# ── 4 · RESULTS ──
C.section("Results")
C.note("Adjacent-sūra lexical coherence — both legitimate orders beat random; the muṣḥaf only edges revelation.")
C.vbars([("muṣḥaf", 0.202, C.TEAL, "canonical order"), ("revelation", 0.190, C.GOLD, "chronological order"),
         ("random", 0.160, C.SLATE, "shuffle null")], ymax=0.24, fmt="{:.3f}")
C.note("Length smoothness (mean |Δroots| between neighbours, lower = smoother) — the muṣḥaf is length-ordered.")
C.vbars([("muṣḥaf", 161, C.TEAL, "near length-descending"), ("revelation", 352, C.GOLD, "chronological"),
         ("random", 550, C.SLATE, "shuffle null")], ymax=620, fmt="{:.0f}")
C.note("What predicts adjacent similarity (regression β) — size, not theme, dominates after the controls.")
C.vbars([("len-prox", -0.010, C.SLATE, "length proximity (after size)"),
         ("period", 0.013, C.GOLD, "revelation-era proximity"), ("size-sum", 0.033, C.CORAL, "both chapters' size"),
         ("size-min", 0.070, C.CORAL, "smaller chapter's size")], fmt="{:.3f}")
C.note("The coherence residual after each control is layered on — it shrinks, then goes negative.")
C.vbars([("+len/period", 0.066, C.TEAL, "beyond length + period"), ("+ size", 0.027, C.GOLD, "beyond linear size"),
         ("+ topic", 0.020, C.GOLD, "beyond topic membership"),
         ("+ nonlinear", -0.008, C.CORAL, "beyond nonlinear size — gone")], fmt="{:.3f}")
C.note("Pre-size topic-control z across topic-model sizes k — robust, right up until size killed it.")
C.vbars([("k = 5", 5.2, C.SLATE, "5 topics"), ("k = 8", 5.6, C.SLATE, "8"), ("k = 15", 4.3, C.SLATE, "15"),
         ("k = 20", 4.8, C.SLATE, "20"), ("k = 30", 6.2, C.SLATE, "30")], ymax=7, fmt="{:.1f}")
C.note("The strongest 'coherent' adjacencies — every one a pair of long front sūras: the tell.")
C.table(["Adjacent sūras", "№", "residual"], [
    [C.ar("البقرة — آل عمران"), "2 – 3", "+0.52"], [C.ar("آل عمران — النساء"), "3 – 4", "+0.51"],
    [C.ar("النساء — المائدة"), "4 – 5", "+0.47"], [C.ar("الأنعام — الأعراف"), "6 – 7", "+0.47"],
])

# ── 5 · GATING CHAIN ──
C.section("Gating chain — survival, then collapse")
C.note("Each point is one control, applied in sequence. Green = survived; red = died. Height = strength (z).")
C.cascade([
    ("vs random", "11.1", 11.1, True), ("length", "3.4", 3.4, True), ("period", "9.8", 9.8, True),
    ("blocks", "8.7", 8.7, True), ("size · linear", "5.8", 5.8, True),
    ("split · 2nd half", "0.0", 0.0, False), ("size · nonlinear", "−0.7", -0.7, False),
], zmax=12.0)

# ── 6 · INTERPRETATION ──
C.section("Interpretation")
C.para("The mechanism is mundane and entirely on the surface. The muṣḥaf is ordered <b>by length</b> "
       "(Spearman −0.84), and length co-varies with register: the long front chapters are the Medinan "
       "legal-narrative sūras, sharing a thick common vocabulary simply because they are long and of a kind. Two "
       "big chapters overlap more <i>mechanically</i> — more text, more shared roots — no thematic intent needed. A "
       "linear size control under-removes that effect (cosine grows non-linearly with size), leaving a residue that "
       "<i>looks</i> like design. It isn't.")

# ── 7 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>Controlled:</b> random, length, revelation period, letter-block families, linear size, topic membership "
       "(k-robust) — it survived all, which is exactly why it was tempting. <b>What broke it:</b> the held-out split "
       "warned first — the effect sat only on the long first half (z 2.5), absent in the short second half (z ≈ 0). "
       "Then nonlinear size terms plus a size-stratified null dropped the residual to <b>z −0.7</b>, confirmed by an "
       "independent Jaccard metric. <b>Flip:</b> a genuinely size-free similarity instrument could revive a residual "
       "— odds ≈ 15%.")

# ── 8 · VERDICT ──
C.section("Verdict")
C.verdict("REFUTED-ARTIFACT",
          "The apparent inter-sūra coherence is a <b>chapter-size artifact</b>, not design — recorded honestly, "
          "<b>not</b> written to the discovery ledger. The muṣḥaf is really ordered (by length); no extra "
          "lexical-coherence layer survives proper size control.",
          "~85% size artifact (nonlinear + stratified agree, two metrics)",
          "a genuinely size-free similarity instrument reviving the residual",
          "such an instrument (≈15% odds) moves this off REFUTED")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
