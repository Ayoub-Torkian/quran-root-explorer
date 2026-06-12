"""Close-up · The Āyah, defined — DEFINED. Dense, real-data charts."""
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

C.kpis([
    ("0.85", "recovery AUC", "Held-out-sūra boundary recovery from the bare root sequence", C.TEAL),
    ("0.97", "AUC · words", "With morphology on the rasm-word substrate", C.TEAL),
    ("+81.8", "onset z", "Connective opening vs within-āyah shuffle null", C.INK),
    ("−48.6", "completeness z", "Dependency-opener depletion at the verse-end", C.INK),
    ("0.73", "closure F1", "Best boundary F1 (word substrate)", C.INK),
    ("80%", "ends covered", "16 two-letter rasm endings cover 80% of all 6,236 verse-ends", C.INK),
    ("0.55", "sufficiency F1", "Root-only — substantially recoverable, not yet unique", C.GOLD),
    ("78", "grade", "Provisional · DEFINED tier", C.GOLD),
])

C.foundation(
    "A unit is real only if the text marks where it begins and ends. We hide the breaks, reduce the text to the "
    "bare consonants (rasm), and ask whether the boundaries rebuild from internal evidence alone — opening words, "
    "grammatical completeness, and the rhyme-cadence (fāṣila). If they do, the āyah is a <b>self-marking unit</b>.")

C.section("Boundary recovery — what carries it")
a, b = st.columns(2, gap="small")
with a:
    C.note("Recovery AUC by substrate — content, not the length cue")
    C.vbars([("length", 0.60, C.SLATE, "Length cue alone: AUC 0.60"),
             ("roots", 0.85, C.TEAL, "Bare content roots: AUC 0.85"),
             ("words", 0.97, C.TEAL, "+ rasm morphology: AUC 0.97")], ymax=1.0)
with b:
    C.note("Ablation — cumulative AUC as each feature is added")
    C.vbars([("length", 0.596, C.SLATE, "length prior only"),
             ("+close", 0.802, C.TEAL, "+ closing-root lexicon"),
             ("+onset", 0.816, C.TEAL, "+ opener lexicon"),
             ("+order", 0.835, C.TEAL, "+ pair transitions"),
             ("+len", 0.850, C.INK, "+ length feature")], ymax=1.0)

C.section("③ Closure — the fāṣila, and its two faces")
C.note("Share of each root's occurrences that land at a verse-end (root substrate, n ≥ 30) — the semantic fawāṣil.")
C.bars([
    (C.ar("عقل"), 0.88, "…أفلا تعقلون · reason"),
    (C.ar("عظم"), 0.84, "…العظيم · the Magnificent"),
    (C.ar("ءلم"), 0.84, "…عذاب أليم · painful"),
    (C.ar("کرم"), 0.81, "…الكريم · the Generous"),
    (C.ar("شکر"), 0.69, "…تشكرون · give thanks"),
    (C.ar("فلح"), 0.65, "…المفلحون · the successful"),
    (C.ar("خسر"), 0.65, "…الخاسرين · the losers"),
], fmt="{:.0%}", color=C.TEAL)
c, d = st.columns(2, gap="small")
with c:
    C.note("Morphological vs lexical closure (boundary AUC) — same fāṣila")
    C.vbars([("suffix", 0.859, C.TEAL, "rasm suffix only (L27 morphology)"),
             ("root", 0.818, C.TEAL, "cadential root identity only"),
             ("both", 0.862, C.INK, "combined — root adds only +0.003")], ymax=1.0)
with d:
    C.note("Closing rasm-endings · frequency vs mid-text")
    C.table(["Ending", "verse-end ×"], [
        [C.ar("ـيم"), "30×"], [C.ar("ـون"), "12×"], [C.ar("ـين"), "7×"],
        ["16 forms", "80% of all ends"],
    ])

C.section("Bracketing — opens joined, never dangles")
e, f = st.columns(2, gap="small")
with e:
    C.note("Connective (و/ف/ثم) rate at verse-START vs mid-verse")
    C.vbars([("start", 0.474, C.TEAL, "47% of āyāt open with a connective"),
             ("mid", 0.128, C.SLATE, "mid-verse baseline")], ymax=0.6, fmt="{:.0%}")
with f:
    C.note("Dangling dependency-opener at verse-END vs mid-verse")
    C.vbars([("end", 0.001, C.CORAL, "āyāt never end on a word needing continuation"),
             ("mid", 0.256, C.SLATE, "mid-verse baseline")], ymax=0.3, fmt="{:.0%}")

C.section("The four conditions, and the honest edge")
g, h = st.columns([3, 2], gap="small")
with g:
    C.table(["Condition — vs the text's own null", "Measured"], [
        ["① Connective-opened (و/ف/ثم start)", "z +81.8"],
        ["② Grammatically complete (no dangling end)", "z −48.6"],
        ["③ Fāṣila-closed (rhyme + closing roots)", "AUC 0.85–0.97"],
        ["④ Characteristic length (~8 roots)", "AUC 0.60"],
    ])
with h:
    C.note("Sufficiency — recoverable, not yet uniquely determined")
    C.scale("roots", 0.55, "words", 0.73, "target", 0.85)

C.verdict("DEFINED",
          "The four conditions co-occur at āyah boundaries far beyond the text's own null. The verse is defined "
          "to <b>necessity</b> from the consonantal skeleton — the north star's first unit, characterised.",
          "necessary-complete ~90% · each clause MEASURED",
          "a null showing the bracketing carries Qur'ān-specific info beyond generic clause grammar",
          "a parser / rhyme-scheme typing lifting sufficiency F1 → 0.85")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
