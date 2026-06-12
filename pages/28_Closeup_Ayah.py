"""Close-up · The Āyah, defined — DEFINED. 8-section anatomy, dense full-width charts."""
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

# ── 1 · PROBLEM ──
C.hero("The Āyah, defined",
       "Is the verse a real unit the text itself encodes — or a convention imposed by reciters and scribes?",
       "DEFINED", 78, "ROOT + rasm-WORD", "DIVINE-DEFAULT (muṣḥaf)")
C.story(
    "Strip the Qur'ān to bare consonants, hide every verse break, and ask a blind learner to find the ends again. "
    "<b>It largely can — the āyah marks itself.</b>",
    "If the boundary is recoverable from the consonantal skeleton alone, the verse is a <b>structural</b> unit of "
    "the text, not an editorial overlay — the first half of the north star: what an āyah <i>is</i>.")
C.kpis([
    ("0.85", "recovery AUC", "Held-out-sūra boundary recovery from the bare root sequence", C.TEAL),
    ("0.97", "AUC · words", "With consonantal morphology (rasm-word substrate)", C.TEAL),
    ("0.861", "morph-alone", "Closure morphology with BOTH length and rhyme removed", C.TEAL),
    ("+81.8", "onset z", "Connective opening (47% vs 13% mid-verse) vs the shuffle null", C.INK),
    ("−48.6", "completeness z", "Dangling-opener depletion at the verse-end (0% vs 26% mid)", C.INK),
    ("80%", "ends covered", "16 two-letter rasm endings cover 80% of all 6,236 verse-ends", C.INK),
    ("0.55–0.73", "sufficiency F1", "Recoverable, not yet uniquely determined", C.GOLD),
    ("78", "grade", "Provisional · DEFINED tier", C.GOLD),
])

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If the āyah is self-marking, three internal signatures should survive total vowel-stripping",
          "Remove the diacritics, spacing and verse numbers — everything a scribe could add — and a real unit should "
          "still betray each boundary three ways: a connective <b>opening</b>, a <b>grammatically complete</b> span, "
          "and a recurring <b>cadence</b> (the fāṣila). A blind learner should then rebuild the hidden breaks far "
          "above chance — and keep doing so after length and rhyme are stripped out, or the 'unit' is mere rhythm.",
          accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus",
          "<b>Substrate</b> — rasm only: content roots (Book6 col 4) and consonantal word-forms (col 6); diacritics "
          "demoted. <b>Arrangement</b> — divine-default (muṣḥaf). <b>Test</b> — concatenate each sūra with breaks "
          "hidden; for every token predict 'verse-end?' with gradient-boosted trees, 5-fold CV across <i>held-out "
          "sūras</i>. <b>Null</b> — random placement at the same rate, plus a within-āyah word-shuffle. "
          "<b>Controls</b> — re-score with length removed, with rhyme removed, and on interiors only.", accent=C.SLATE)

# ── 4 · RESULTS ──
C.section("Results")
C.note("Recovery AUC by substrate — content carries the boundary, not the length cue (0.60 → 0.85 → 0.97).")
C.vbars([("length cue", 0.60, C.SLATE, "length alone"), ("content roots", 0.85, C.TEAL, "bare roots"),
         ("+ morphology", 0.97, C.TEAL, "rasm word-forms")], ymax=1.0)
C.note("Feature ablation — cumulative AUC; the closing-root lexicon alone does almost all the work.")
C.vbars([("length", 0.596, C.SLATE, "length prior only"), ("+ closure-lex", 0.802, C.TEAL, "+ closing-root lexicon"),
         ("+ onset-lex", 0.816, C.TEAL, "+ opener lexicon"), ("+ pair-order", 0.835, C.TEAL, "+ transitions"),
         ("+ length", 0.850, C.INK, "+ length feature")], ymax=1.0)
C.note("The closure lexicon — share of each root's occurrences landing at a verse-end (root substrate, n ≥ 30). "
       "These cadential meaning-roots <i>are</i> the semantic fawāṣil.")
C.bars([
    (C.ar("عقل"), 0.88, "…أفلا تعقلون · reason"), (C.ar("عظم"), 0.84, "…العظيم · the Magnificent"),
    (C.ar("ءلم"), 0.84, "…عذاب أليم · painful"), (C.ar("کرم"), 0.81, "…الكريم · the Generous"),
    (C.ar("شکر"), 0.69, "…تشكرون · give thanks"), (C.ar("فلح"), 0.65, "…المفلحون · the successful"),
    (C.ar("خسر"), 0.65, "…الخاسرين · the losers"),
], fmt="{:.0%}", color=C.TEAL)
C.note("Bracketing — verses open on a connective (47% vs 13% mid) and never end on a word needing continuation "
       "(0% vs 26% mid). The verse is a complete clause.")
C.vbars([("open · start", 0.474, C.TEAL, "connective opens 47% of verses"),
         ("open · mid", 0.128, C.SLATE, "mid-verse connective rate"),
         ("close · end", 0.001, C.CORAL, "~0% dangling at the verse-end"),
         ("close · mid", 0.256, C.SLATE, "mid-verse dangling rate")], ymax=0.6, fmt="{:.0%}")

# ── 5 · GATING CHAIN ──
C.section("Gating chain — does it survive the controls?")
C.note("Recovery AUC as each ordinary explanation is stripped away. It stays high throughout — the boundary rests "
       "on real morphology, not on length or rhyme alone.")
C.vbars([("full model", 0.957, C.TEAL, "all features"), ("− word order", 0.939, C.TEAL, "word-form only"),
         ("morph-alone", 0.861, C.TEAL, "no length, no rhyme, no position"),
         ("length-only", 0.82, C.SLATE, "length cue alone"), ("rhyme-only", 0.80, C.SLATE, "rhyme cue alone")],
        ymax=1.0)
C.para("Two controls decide it. <b>Order-invariance</b>: word-form-only (0.939) nearly equals the full model "
       "(0.957), so closure is a property of the word's <i>shape</i>, not the sequence — it is the fāṣila. "
       "<b>Lexical vs morphological</b>: once the rasm suffix is known, the cadential root adds only <b>+0.003</b> "
       "AUC — two faces of one phenomenon, not two findings.")

# ── 6 · INTERPRETATION ──
C.section("Interpretation")
C.para("The mechanism is concrete. A verse <b>opens</b> on a connective particle, runs as one <b>complete clause</b> "
       "that never breaks mid-dependency, and <b>closes</b> on a compact lexicon of cadential meaning-roots — عقل, "
       "عظم, علم, فلح — whose consonantal endings (ـون / ـيم / ـين) <i>are</i> the rhyme. The boundary is a single "
       "grammatical-prosodic event, written into the bare consonants. The āyah is the text's own sentence-unit; the "
       "reciter's pause merely records a structure already there.")

# ── 7 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>Controlled:</b> length, rhyme, word-order, lexical-vs-morphological redundancy — survived all four. "
       "<b>Open:</b> 'grammatical completeness' is a property of clause boundaries in <i>any</i> language (the "
       "within-āyah null only rejects 'no grammar'), so it is a true property of the āyah but not a Qur'ān-unique "
       "discovery. And <b>sufficiency is partial</b> — F1 0.55 (roots) / 0.73 (words): the cut falls at a "
       "grammatically-valid, fāṣila-marked point, but <i>which</i> valid point becomes the end is not fully fixed by "
       "the rasm. That residue is the instrument-limited frontier.")

# ── 8 · VERDICT ──
C.section("Verdict")
C.verdict("DEFINED",
          "The three signatures co-occur at āyah boundaries far beyond the text's own null and survive every "
          "control. The verse is defined to <b>necessity</b> from the consonantal skeleton — the north star's first "
          "unit, characterised. Sufficiency (unique segmentation) remains the open edge.",
          "necessary-complete ~90% · each clause MEASURED",
          "a null showing the bracketing carries Qur'ān-specific information beyond generic clause grammar",
          "a parser / per-sūra rhyme-scheme typing lifting sufficiency F1 → 0.85")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
