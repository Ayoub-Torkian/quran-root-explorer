"""Close-up · The Āyah, defined — DEFINED. Full investigative anatomy (8 sections), dense real-data charts."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · The Āyah", page_icon="📐", layout="wide")
if S:
    try:
        S.log_page("closeup_ayah")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()

# ───────────────────────── 1 · PROBLEM ─────────────────────────
C.hero("The Āyah, defined",
       "Is the verse a real unit the text itself encodes — or a convention imposed by reciters and scribes?",
       "DEFINED", 78, "ROOT + rasm-WORD", "DIVINE-DEFAULT (muṣḥaf)")
C.story(
    "Strip the Qur'ān to bare consonants, hide every verse break, and ask a blind learner to find the ends again. "
    "<b>It largely can — the āyah marks itself.</b>",
    "If the boundary is recoverable from the consonantal skeleton alone, the verse is a <b>structural</b> unit of "
    "the text, not an editorial overlay. That settles the first half of the north star: what an āyah <i>is</i>.")
C.kpis([
    ("0.85", "recovery AUC", "Held-out-sūra boundary recovery from the bare root sequence", C.TEAL),
    ("0.97", "AUC · words", "With consonantal morphology (rasm-word substrate)", C.TEAL),
    ("0.861", "morph-alone AUC", "Closure morphology with length AND rhyme removed", C.TEAL),
    ("+81.8", "onset z", "Connective opening vs the within-āyah shuffle null", C.INK),
    ("−48.6", "completeness z", "Dangling-opener depletion at the verse-end", C.INK),
    ("80%", "ends covered", "16 two-letter rasm endings cover 80% of all 6,236 verse-ends", C.INK),
    ("0.55–0.73", "sufficiency F1", "Recoverable, not yet uniquely determined", C.GOLD),
    ("78", "grade", "Provisional · DEFINED tier", C.GOLD),
])

# ───────────────────────── 2 · HYPOTHESIS ─────────────────────────
C.section("Hypothesis")
C.callout("If the āyah is self-marking, three internal signatures should survive total vowel-stripping",
          "Remove the diacritics, the spacing, the verse numbers — everything a scribe could have added — and a "
          "real unit should still betray each boundary three ways: it should <b>open</b> on a connective, run as a "
          "<b>grammatically complete</b> span, and <b>close</b> on a recurring cadence (the fāṣila). A blind learner "
          "should then rebuild the hidden breaks far above chance, and do so even after length and rhyme are "
          "stripped out — otherwise the 'unit' is just rhythm or rhyme, not structure.", accent=C.SLATE)

# ───────────────────────── 3 · METHOD & INSTRUMENTS ─────────────────────────
C.section("Method & instruments")
C.callout("The apparatus",
          "<b>Substrate</b> — the rasm only: content roots (Book6 col 4) and consonantal word-forms (col 6); "
          "diacritics demoted as a human artifact. <b>Arrangement</b> — divine-default (muṣḥaf order). "
          "<b>Test</b> — concatenate each sūra with breaks hidden; for every token predict 'is this a verse-end?' "
          "with gradient-boosted trees, scored by 5-fold cross-validation across <i>held-out sūras</i>. "
          "<b>Null</b> — random placement at the same boundary rate, plus a within-āyah word-shuffle. "
          "<b>Controls</b> — re-score with length removed, with rhyme removed, and on āyah interiors only.",
          accent=C.SLATE)

# ───────────────────────── 4 · RESULTS ─────────────────────────
C.section("Results")
a, b = st.columns(2, gap="small")
with a:
    C.note("Recovery AUC by substrate — content carries it, not the length cue (0.60 → 0.85 → 0.97).")
    C.vbars([("length", 0.60, C.SLATE, "Length cue alone"), ("roots", 0.85, C.TEAL, "Bare content roots"),
             ("words", 0.97, C.TEAL, "+ rasm morphology")], ymax=1.0)
with b:
    C.note("Feature ablation — cumulative AUC; the closing-root lexicon does almost all the work.")
    C.vbars([("length", 0.596, C.SLATE, "length prior only"), ("+close", 0.802, C.TEAL, "+ closing-root lexicon"),
             ("+onset", 0.816, C.TEAL, "+ opener lexicon"), ("+order", 0.835, C.TEAL, "+ pair transitions"),
             ("+len", 0.850, C.INK, "+ length feature")], ymax=1.0)
C.note("The closure lexicon — share of each root's occurrences that land at a verse-end (root substrate, n ≥ 30). "
       "These cadential meaning-roots <i>are</i> the semantic fawāṣil the ear already knows.")
C.bars([
    (C.ar("عقل"), 0.88, "…أفلا تعقلون · reason"), (C.ar("عظم"), 0.84, "…العظيم · the Magnificent"),
    (C.ar("ءلم"), 0.84, "…عذاب أليم · painful"), (C.ar("کرم"), 0.81, "…الكريم · the Generous"),
    (C.ar("شکر"), 0.69, "…تشكرون · give thanks"), (C.ar("فلح"), 0.65, "…المفلحون · the successful"),
    (C.ar("خسر"), 0.65, "…الخاسرين · the losers"),
], fmt="{:.0%}", color=C.TEAL)
c, d = st.columns(2, gap="small")
with c:
    C.note("Bracketing — a connective (و/ف/ثم) opens ~47% of verses, 3.7× the mid-verse rate.")
    C.vbars([("verse start", 0.474, C.TEAL, "47% open with و/ف/ثم"),
             ("mid-verse", 0.128, C.SLATE, "baseline")], ymax=0.6, fmt="{:.0%}")
with d:
    C.note("Completeness — verses essentially never end on a word that grammatically demands a continuation.")
    C.vbars([("verse end", 0.001, C.CORAL, "~0% dangling at the end"),
             ("mid-verse", 0.256, C.SLATE, "baseline")], ymax=0.3, fmt="{:.0%}")

# ───────────────────────── 5 · GATING CHAIN ─────────────────────────
C.section("Gating chain — does it survive the controls?")
C.note("Recovery AUC as each ordinary explanation is stripped away. It stays high throughout — the boundary rests "
       "on real morphology, not on length or rhyme alone.")
C.vbars([("full", 0.957, C.TEAL, "all features"), ("−context", 0.939, C.TEAL, "word-form only (order removed)"),
         ("morph-alone", 0.861, C.TEAL, "no length, no rhyme, no position"),
         ("length-only", 0.82, C.SLATE, "length cue alone"), ("rhyme-only", 0.80, C.SLATE, "rhyme cue alone")],
        ymax=1.0)
C.para("Two controls matter most. <b>Order-invariance</b>: the word-form-only model (0.939) nearly equals the full "
       "model (0.957), so closure is a property of the word's <i>shape</i>, not the surrounding sequence — it is the "
       "fāṣila. <b>Lexical vs morphological</b>: once the rasm suffix is known, the cadential root adds only "
       "<b>+0.003</b> AUC — the lexical and morphological closures are two faces of one phenomenon, not two findings.")

# ───────────────────────── 6 · INTERPRETATION ─────────────────────────
C.section("Interpretation")
C.para("On this substrate the mechanism is concrete. A verse <b>opens</b> on a connective particle, runs as one "
       "<b>complete clause</b> that never breaks mid-dependency, and <b>closes</b> on a compact lexicon of cadential "
       "meaning-roots — عقل, عظم, علم, فلح — whose consonantal endings (ـون / ـيم / ـين) <i>are</i> the rhyme. The "
       "boundary is therefore a single grammatical-prosodic event, and that event is written into the bare "
       "consonants. The āyah is the text's own sentence-unit; the reciter's pause records a structure already there.")

# ───────────────────────── 7 · CAVEATS & CONFOUNDS ─────────────────────────
C.section("Caveats & confounds")
C.para("<b>Controlled:</b> length, rhyme, word-order, and lexical-vs-morphological redundancy — the recovery "
       "survived all four. <b>Open:</b> 'grammatical completeness' is a property of clause boundaries in <i>any</i> "
       "language (the within-āyah null only rejects 'no grammar'), so it is a true property of the āyah but not a "
       "Qur'ān-unique discovery. And <b>sufficiency is partial</b> — F1 tops out at 0.55 (roots) / 0.73 (words): the "
       "cut falls at a grammatically-valid, fāṣila-marked point, but <i>which</i> valid point becomes the end is not "
       "fully fixed by the rasm alone. That residue is the instrument-limited frontier.")

# ───────────────────────── 8 · VERDICT ─────────────────────────
C.section("Verdict")
C.verdict("DEFINED",
          "The three signatures co-occur at āyah boundaries far beyond the text's own null and survive every "
          "control. The verse is defined to <b>necessity</b> from the consonantal skeleton — the north star's first "
          "unit, characterised. Sufficiency (unique segmentation) remains the open edge.",
          "necessary-complete ~90% · each clause MEASURED",
          "a null showing the bracketing carries Qur'ān-specific information beyond generic clause grammar",
          "a parser / per-sūra rhyme-scheme typing lifting sufficiency F1 → 0.85")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
