"""Close-up · The Āyah, defined — DEFINED. Story-first, full-width, readable."""
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

C.hero("The Āyah, defined",
       "What IS a verse — can it be rebuilt from the bare consonants alone?",
       "DEFINED", 78, "ROOT + rasm-WORD", "DIVINE-DEFAULT (muṣḥaf)")

C.story(
    "Hide every verse break and strip the Qur'ān to bare consonants — the verse boundaries can still be rebuilt. "
    "<b>The āyah marks itself.</b>",
    "The verse is a real structural unit encoded in the text, not just a reciter's convention — the first half "
    "of the north star, achieved.")

C.headline([("0.85", "ayah-recovery AUC", C.TEAL), ("81.8", "onset signal z", C.INK),
            ("0.73", "closure F1 (words)", C.INK), ("78", "grade", C.GOLD)])

C.foundation(
    "A unit is real only if the text marks where it begins and ends. We hide the breaks, reduce the text to the "
    "bare consonants (rasm), and ask whether the boundaries rebuild from internal evidence alone — opening words, "
    "grammatical completeness, and the rhyme-cadence (fāṣila). If they do, the āyah is a <b>self-marking unit</b>.")

C.section("The four necessary conditions")
C.table(["Condition — measured against the text's own null", "Measured"], [
    ["① Connective-opened — ~47% of āyāt open with و / ف / ثم (3.7× mid-verse)", "z +81.8"],
    ["② Grammatically complete — never end on a dangling preposition/connective", "z −48.6"],
    ["③ Fāṣila-closed — rhyme + a recurring set of closing roots", "AUC 0.85–0.97"],
    ["④ Characteristic length — ~8 roots per verse, a weak length prior", "AUC 0.60"],
])

C.section("③ The closure lexicon — what verses end on")
C.note("Share of each root's occurrences that land at a verse-end (root substrate). These are the semantic fawāṣil — the cadence the ear already knows.")
C.bars([
    (C.ar("عقل"), 0.88, "…أفلا تعقلون · reason"),
    (C.ar("عظم"), 0.84, "…العظيم · the Magnificent"),
    (C.ar("ءلم"), 0.84, "…عذاب أليم · painful"),
    (C.ar("کرم"), 0.81, "…الكريم · the Generous"),
    (C.ar("شکر"), 0.69, "…تشكرون · give thanks"),
    (C.ar("فلح"), 0.65, "…المفلحون · the successful"),
    (C.ar("خسر"), 0.65, "…الخاسرين · the losers"),
], fmt="{:.0%}", color=C.TEAL)

C.section("How recoverable is the boundary?")
C.note("Recovery AUC across held-out sūras climbs as the substrate carries more of the closure signal — real structure, not the length cue.")
C.scale("length cue", 0.60, "from roots", 0.85, "from words", 0.97)

C.section("The honest edge — necessary, not yet sufficient")
C.note("Full reconstruction tops out at F1 0.55 (roots) / 0.73 (words): the āyah is substantially recoverable, not "
       "uniquely determined. The cut falls at a grammatically-valid, fāṣila-marked point — but which valid point "
       "becomes the end isn't fully fixed by the rasm alone. That gap is the open, instrument-limited frontier.")

C.verdict("DEFINED",
          "The four conditions co-occur at āyah boundaries far beyond the text's own null. The verse is defined "
          "to <b>necessity</b> from the consonantal skeleton — the north star's first unit, characterised.",
          "necessary-complete ~90% · each clause MEASURED",
          "a null showing the bracketing carries Qur'ān-specific info beyond generic clause grammar",
          "a parser / rhyme-scheme typing lifting sufficiency F1 → 0.85")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
