"""Close-up · The Āyah, defined — DEFINED. Plain English first, then deep technical."""
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

C.hero(
    title="The Āyah, defined",
    question="What IS a verse — can it be rebuilt from the bare consonants alone?",
    status="DEFINED", grade=78,
    substrate="ROOT + rasm-WORD (no diacritics)", arrangement="DIVINE-DEFAULT (muṣḥaf)",
    plain=("Strip the Qur'ān down to its consonantal skeleton — no vowels, no punctuation, verse breaks hidden — "
           "and ask the machine to find where each verse ends. It largely can. A verse turns out to be a "
           "self-marking little package: it <b>opens</b> with a joining word (and / so / then), it <b>never "
           "ends mid-grammar</b> (never on a word that needs a continuation), and it <b>closes</b> on a small, "
           "recurring family of cadence words (the rhyme, the fāṣila). Put together, those traits define the "
           "verse — though they still don't pin down its <i>exact</i> length every time."))

# ---- plain english -------------------------------------------------------
C.section("Plain English — the one-sentence definition")
st.markdown(
    "<div class='cu-wrap'><div style='font-size:17px;line-height:1.7;color:#243b53;background:#fff;"
    "border:1px solid #E2E8F0;border-radius:12px;padding:18px 20px'>"
    "An <b>āyah</b> is a <b>connective-opened</b>, <b>grammatically-complete</b>, <b>fāṣila-closed</b> "
    "clause-span of <b>characteristic length</b>.<br><span style='font-size:14px;color:#5B6B82'>Four traits, "
    "each one measured against the text's own shuffle. None is a brand-new discovery on its own — the point is "
    "that together they <i>define the unit</i> from the rasm.</span></div></div>", unsafe_allow_html=True)

# ---- deep technical: four conditions ------------------------------------
C.section("Deep technical — the four necessary conditions")
C.table(["Condition", "What it says", "Measured (vs the text's own null)"], [
    ["① Connective-opened", "≈47% of āyāt open with a connective (و / ف / ثم) — 3.7× the mid-verse rate", "z = +81.8"],
    ["② Grammatically complete", "āyāt never end on a dangling preposition/connective that demands a continuation", "z = −48.6"],
    ["③ Fāṣila-closed", "end on the cadential closure family — rhyme + a recurring set of closing roots", "AUC 0.85–0.97"],
    ["④ Characteristic length", "≈8 roots / verse; a weak but real length prior", "AUC 0.60"],
])

# ---- the closure lexicon (real Arabic data) -----------------------------
C.section("③ The closure lexicon — what āyāt actually end on")
st.markdown("<div class='cu-wrap'><div style='font-size:14px;color:#475569;margin-bottom:6px'>"
            "Share of each root's occurrences that fall at a verse-end (root substrate, n ≥ 30). These are the "
            "<b>semantic fawāṣil</b> — the cadence the ear already knows.</div></div>", unsafe_allow_html=True)
C.bars([
    (C.ar("عقل"), 0.88, "…أفلا تعقلون (reason)"),
    (C.ar("عظم"), 0.84, "…العظيم (Magnificent)"),
    (C.ar("ءلم"), 0.84, "…عذاب أليم (painful)"),
    (C.ar("کرم"), 0.81, "…الكريم (Generous)"),
    (C.ar("فسق"), 0.76, "…الفاسقين (transgressors)"),
    (C.ar("شکر"), 0.69, "…تشكرون (give thanks)"),
    (C.ar("فلح"), 0.65, "…المفلحون (successful)"),
    (C.ar("خسر"), 0.65, "…الخاسرين (the losers)"),
], fmt="{:.0%}", color="#2A9D8F")

# ---- recoverability ------------------------------------------------------
C.section("How recoverable is the boundary? (held-out sūras)")
st.markdown("<div class='cu-wrap'><div style='font-size:14px;color:#475569;margin-bottom:8px'>"
            "Boundary-recovery AUC climbs as the substrate carries more of the closure signal — but the boundary "
            "is real structure either way, not the length cue.</div></div>", unsafe_allow_html=True)
C.scale("length cue only", 0.60, "from roots", 0.85, "from words", 0.97)

# ---- sufficiency gap -----------------------------------------------------
C.section("The honest edge — necessary, not yet sufficient")
st.markdown(
    "<div class='cu-wrap cu-card'><div style='font-size:14.5px;line-height:1.65;color:#243b53'>"
    "Full reconstruction tops out at <b>F1 0.55</b> (roots) / <b>0.73</b> (words). The āyah is <b>substantially "
    "recoverable</b>, not <b>uniquely determined</b>: the cut falls at a grammatically-valid, fāṣila-marked point, "
    "but <i>which</i> valid point becomes the end is not fully fixed by the rasm alone. That gap is the open "
    "frontier — and it's instrument-limited, the honest place a sharper tool would push next.</div></div>",
    unsafe_allow_html=True)

C.verdict("DEFINED",
          "The four conditions co-occur at āyah boundaries far beyond the text's own null. The verse is "
          "defined to <b>necessity</b> from the consonantal skeleton — the north star's first unit, characterised.",
          confidence="necessary-complete ~90% · each clause MEASURED",
          flip="a stronger null showing the bracketing carries Qur'ān-specific info beyond generic clause grammar",
          revise="a parser / per-sūra rhyme-scheme typing that lifts sufficiency F1 → 0.85")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
