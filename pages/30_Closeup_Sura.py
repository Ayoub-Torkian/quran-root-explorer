"""Close-up · The Sūra, characterised — CANDIDATE. 8-section anatomy, dense full-width charts."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · The Sūra", page_icon="📜", layout="wide")
if S:
    try:
        S.log_page("closeup_sura")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()

# ── 1 · PROBLEM ──
C.hero("The Sūra, characterised",
       "Is the chapter a real bounded unit the text encodes — or just an editorial grouping of verses?",
       "CANDIDATE", 62, "ROOT + rasm-WORD", "DIVINE-DEFAULT (muṣḥaf)")
C.story(
    "Read the muṣḥaf as one stream of verses and watch the vocabulary. Inside a sūra it holds; at each chapter "
    "break it <b>drops sharply</b>, then recovers. <b>The sūra behaves like a coherent block.</b>",
    "It's the north star's second unit — but the boundary is <i>softer</i> than the verse's: a cohesion dip and a "
    "register shift, not the sharp self-marking close of the āyah. Real, not yet defined to necessity.", accent=C.GOLD)
C.kpis([
    ("4.5", "cohesion z", "Within-sūra vs across-boundary adjacent similarity, vs sūra-label shuffle", C.TEAL),
    ("2.6×", "within / across", "Adjacent verses inside a sūra vs across a boundary (0.105 vs 0.040)", C.TEAL),
    ("0.80", "onset AUC", "Sūra-opening verse recoverable from the rasm (base rate 1.8%)", C.TEAL),
    ("70%", "boundary = dip", "Sūra boundaries that are a local cohesion minimum (vs 55% interior)", C.INK),
    ("−0.84", "length law", "Spearman(sūra №, length) — the descending arrangement", C.INK),
    ("39", "median āyāt", "Median verses per sūra (mean 54.7, max 286)", C.INK),
    ("62", "grade", "Provisional · CANDIDATE — softer than the āyah", C.GOLD),
])

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If the sūra is a real unit it should be a cohesive block, register-bracketed, with marked seams",
          "A genuine chapter-unit should (a) be <b>internally cohesive</b> — verses inside share more vocabulary "
          "than verses across its border; (b) <b>open and close in a distinct register</b> — recurring formulae set "
          "it off; and (c) have <b>marked seams</b> — each boundary sitting at a local drop in verse-to-verse "
          "similarity. If the stream flows smoothly across breaks, the sūra is a container, not a textual unit.",
          accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus",
          "<b>Substrate</b> — content roots (col 4) and consonantal word-forms (col 6); rasm only. "
          "<b>Arrangement</b> — divine-default muṣḥaf. <b>Cohesion</b> — cosine of adjacent verses, WITHIN a sūra vs "
          "ACROSS a boundary, against a sūra-label permutation null. <b>Register</b> — root enrichment in the first / "
          "last verse vs the interior. <b>Onset recovery</b> — predict 'sūra-opening verse?' from the rasm with "
          "gradient-boosted trees, GroupKFold by sūra. <b>Seam profile</b> — adjacent similarity in a ±2-verse window "
          "around every boundary.", accent=C.SLATE)

# ── 4 · RESULTS ──
C.section("Results")
C.note("Onset register — roots over-represented in the OPENING verse vs the interior (× enrichment). The Musabbiḥāt "
       "(سبّح) and 'the Book' (كتب) openings show through.")
C.bars([
    (C.ar("سبح"), 5.4, "…سبّح/يسبّح · glorifies"), (C.ar("حکم"), 3.0, "…الحكيم · the Wise"),
    (C.ar("سمو"), 2.4, "name / heaven"), (C.ar("کتب"), 2.0, "…الكتاب · the Book"),
    (C.ar("ءیی"), 1.2, "آيات · signs"),
], fmt="{:.1f}×", color=C.TEAL)
C.note("Closure register — roots over-represented in the CLOSING verse: glorification, forgiveness, mercy, deeds.")
C.bars([
    (C.ar("سبح"), 5.4, "glorify"), (C.ar("غفر"), 2.5, "…الغفور · forgiveness"),
    (C.ar("سمو"), 2.1, "name"), (C.ar("رحم"), 2.0, "…الرحيم · mercy"), (C.ar("عمل"), 2.0, "deeds"),
], fmt="{:.1f}×", color=C.GOLD)

# ── 5 · GATING CHAIN ──
C.section("Gating chain — the seam, and what holds")
C.note("Seam profile — verse-to-verse similarity around a boundary (offset 0). It dips sharply at the seam, then "
       "recovers — the chapter break is a real, local cohesion minimum.")
C.vbars([("−2", 0.124, C.SLATE, "two verses before"), ("−1", 0.128, C.SLATE, "just before"),
         ("seam (0)", 0.040, C.CORAL, "across the boundary"), ("+1", 0.125, C.SLATE, "just after"),
         ("+2", 0.111, C.SLATE, "two after")], ymax=0.16, fmt="{:.3f}")
C.para("Three pillars hold against their nulls: cohesion (z = 4.5 vs a sūra-label shuffle), a recoverable onset "
       "(AUC 0.80 vs a 1.8% base rate), and seams at cohesion dips (70% of boundaries vs 55% of interior gaps). None "
       "collapses — but none is sharp. The boundary is a <b>soft seam</b>, not the crisp morphological close the "
       "āyah owns.")

# ── 6 · INTERPRETATION ──
C.section("Interpretation")
C.para("On this substrate the sūra reads as a <b>cohesive thematic block, bracketed by register</b>. It opens and "
       "closes on recurring formulae — glorification (سبّح), the Book (كتب), forgiveness and mercy (غفر، رحم) — and "
       "its interior holds a denser shared vocabulary than its neighbours, with a clear drop at each border. But "
       "where the āyah's edge is a single grammatical-prosodic event written into the word-form, the sūra's edge is "
       "a <i>statistical</i> one: a thematic membrane, recoverable but not forced by the consonants alone.")

# ── 7 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>The honest deductions.</b> The cohesion signal is real but modest (z = 4.5) and is, in substance, "
       "<b>thematic clustering</b> — the territory feature already in the ledger. The onset register overlaps "
       "<b>known sūra-families</b> (the Musabbiḥāt opening on سبّح), so part of it is recognised structure, not new. "
       "The length law (−0.84) is the well-known descending arrangement, not a property of the unit. And the seam is "
       "soft (70%, not ~100%). So the sūra is genuinely <i>characterised</i>, but its unit-hood leans on cohesion + "
       "register, both partly known — hence CANDIDATE, not DEFINED.")

# ── 8 · VERDICT ──
C.section("Verdict")
C.verdict("CANDIDATE",
          "The sūra is a <b>cohesive, register-bracketed thematic block</b> with soft but real seams — measured "
          "against the text's own nulls. It is characterised, but more weakly than the āyah, and several traits "
          "reduce to known structure. A real unit; not yet defined to necessity.",
          "block-cohesion + register ~75% MEASURED · unit-sharpness ~45% INFERRED",
          "a boundary instrument showing the seam is forced (not merely recoverable) beyond thematic clustering",
          "a sharper seam model / sūra-recovery clearing a high F1 lifts CANDIDATE → DEFINED")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
