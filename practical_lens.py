"""practical_lens.py  ·  v1.2 enhancement
==========================================

Maps the data-driven findings of the app (pair classification, asymmetry
ratio, recurring partners) to a curated set of practical implications —
translation tips, teaching parallels, everyday-life applications.

Every implication is:
  - clearly tagged as INTERPRETIVE OVERLAY, not computed fact
  - anchored to the specific numeric finding that triggered it
  - phrased as a tip / parallel, not a theological claim
  - opt-in (the page shows them inside expanders)

The module deliberately does NOT generate spiritual or sectarian claims.
It generates [b:practical, pedagogical, and translation-related] guidance
based on the structural pattern the data reveals.
"""
from __future__ import annotations
from typing import Iterable


# ---------------------------------------------------------------------------
# Per-tier practical lenses (triggered by pair classification)
# ---------------------------------------------------------------------------
TIER_LENSES = {
    "stipulative": {
        "headline": "The Qurʾan teaches these two roots as a [b]bonded pair[/b].",
        "translation_tips": [
            "Render in English as a coupled phrase (e.g. 'with hardship — ease'). "
            "Separating them loses the pedagogical link.",
            "Avoid translating one without the other in context-sensitive passages.",
            "Look for a fixed English idiom that preserves the bond  ·  e.g. "
            "'this-world / the hereafter' kept paired in liturgical English.",
        ],
        "teaching_parallels": [
            "Like the idiom 'no pain, no gain' — the pair is the lesson; "
            "split the pair and the lesson disappears.",
            "Like 'salt and pepper' or 'thunder and lightning' — the words "
            "co-define each other in usage.",
        ],
        "everyday_implications": [
            "When invoking one half of the pair in speech or writing, "
            "explicitly recall the other half — that is how the corpus uses them.",
        ],
    },
    "embedded": {
        "headline": "These two roots are [b]frequent companions[/b] but [b]not a single concept[/b].",
        "translation_tips": [
            "Render with their own grammar.  Don't force them into a binary "
            "construction in English ('X and its opposite Y').",
            "When both appear in an ayah, translate each according to its own "
            "lexical neighborhood — they are cross-cutting categories, not "
            "two faces of one coin.",
        ],
        "teaching_parallels": [
            "Like 'work' and 'rest' in everyday English — discussed together "
            "often, but not a stipulative pair. Each has its own rich "
            "meaning that doesn't reduce to the absence of the other.",
        ],
        "everyday_implications": [
            "When teaching, present each root's profile separately first, "
            "then show how they cross-cut.  Reduce both at once and you "
            "flatten the texture.",
        ],
    },
    "mild": {
        "headline": "These roots co-occur slightly above chance — no strong pairing.",
        "translation_tips": [
            "Treat as unrelated for translation purposes unless the specific "
            "ayah pulls them together.",
        ],
        "teaching_parallels": [
            "Like two academic departments that occasionally co-author papers "
            "but maintain independent identities.",
        ],
        "everyday_implications": [
            "Mild association is a hint to look closer at individual ayahs; "
            "the structural-level story is thin.",
        ],
    },
    "independent": {
        "headline": "These roots live in [b]different semantic worlds[/b] of the corpus.",
        "translation_tips": [
            "Do [b]not[/b] render in English as 'X and its opposite Y' as a "
            "default. The corpus does not treat them that way.",
            "When both appear in the same ayah (rare), examine whether one "
            "is in a non-standard sense (e.g. cosmological vs ethical).",
        ],
        "teaching_parallels": [
            "Like 'health' and 'wealth' — sometimes contrasted in life, but "
            "not actually mirror-image opposites. Each has its own story.",
            "Like 'silence' and 'noise' — apparent opposites that, in deep "
            "musical practice, name different phenomena rather than the "
            "negation of each other.",
        ],
        "everyday_implications": [
            "Audit how often the binary 'X vs not-X' shows up in our own "
            "speech.  The corpus suggests this framing is more our habit "
            "than the text's actual structure.",
        ],
    },
}


# ---------------------------------------------------------------------------
# Asymmetry lenses  (triggered by big A/B ratio)
# ---------------------------------------------------------------------------
def asymmetry_lens(n_a: int, n_b: int, root_a: str, root_b: str) -> dict | None:
    """Return a practical-lens dict if the ratio is sharp."""
    if n_a == 0 or n_b == 0:
        return None
    big, small = max(n_a, n_b), min(n_a, n_b)
    ratio = big / small
    if ratio < 3:
        return None
    bigger = root_a if n_a > n_b else root_b
    smaller = root_b if n_a > n_b else root_a
    return {
        "headline": f"The corpus dwells on **{bigger}** about **{ratio:.1f}×** "
                    f"more than on **{smaller}**.",
        "translation_tips": [
            f"In English contexts that pair them symmetrically, this asymmetry "
            f"is erased.  The original text emphasises one side strongly.",
        ],
        "teaching_parallels": [
            f"Like a medical textbook that spends most of its pages on disease "
            f"and only a chapter on health — the imbalance is itself the "
            f"pedagogical point.",
            f"When a teacher names one concept ten times more than its supposed "
            f"opposite, that ratio is the lesson, not the noise.",
        ],
        "everyday_implications": [
            f"Pause to notice which side of any pair our own attention naturally "
            f"goes to.  The corpus's bias toward {bigger} may or may not match "
            f"our spontaneous focus.",
        ],
    }


# ---------------------------------------------------------------------------
# Per-root practical lenses (only the well-supported ones)
# ---------------------------------------------------------------------------
# These are triggered when a SPECIFIC root is the input query. They are
# included only when the corpus evidence is strong enough that the
# implication is grounded.
ROOT_LENSES = {
    "ظلم": {
        "headline": "ẓulm  ·  the spatial-misplacement reading",
        "rationale": (
            "Classical Arabic lexicographers (Ibn Manẓūr, al-Rāghib) define "
            "ẓulm as وَضْعُ الشَّيْءِ فِي غَيْرِ مَحَلِّهِ — 'putting a thing "
            "where it does not belong.' The 23 ayahs using ẓulumāt (darknesses) "
            "preserve this spatial sense.  Combined with the strong ẓulm–nafs "
            "co-occurrence, the practical reading is:"
        ),
        "applied": [
            "**Pollution** = matter in the wrong place — a literal modern "
            "instance of ẓulm.",
            "**Urban displacement** = people in the wrong place — ẓulm of "
            "the city.",
            "**Personal**: where in my life have I misplaced my "
            "attention / time / words?",
            "**Translation**: 'misplacement,' 'wronging,' or 'displacement' "
            "may carry more of the original sense than 'injustice.'",
        ],
    },
    "عدل": {
        "headline": "ʿadl  ·  the courtroom reading",
        "rationale": (
            "The corpus binds ʿadl extremely tightly to qisṭ (lift ×70.9), "
            "and its other partners (witness, weighing, intercession, kinship) "
            "all belong to one scene: a courtroom or a measure. ʿadl is "
            "[b]procedural[/b] in the corpus, not abstract:"
        ),
        "applied": [
            "**Legal reform**: due process, honest weights, transparent "
            "contracts, settled verdicts.  These four corners are what "
            "ʿadl operationally names.",
            "**Commerce**: fair weight and measure are not optional ethical "
            "extras — they are central instances of ʿadl in the Qurʾanic "
            "vocabulary.",
            "**Translation**: 'equity,' 'fair measure,' 'balance,' or "
            "'equipoise' often fit better than 'justice.'",
        ],
    },
    "نفس": {
        "headline": "nafs  ·  the reflexive-soul reading",
        "rationale": (
            "Across the corpus, nafs is the strongest partner of ẓulm "
            "(lift ×4.4).  ~40 of the 55 joint ayahs use the explicit phrase "
            "ẓulm an-nafs (wronging one's own soul).  Practically:"
        ),
        "applied": [
            "Before naming wrongs in the world, audit the wrongs in oneself.",
            "Therapeutic / coaching parallel: most personal harm starts with "
            "self-betrayal before it shows externally.",
        ],
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def pair_lens(tier: str) -> dict:
    """Return the practical-lens dict for a pair tier."""
    return TIER_LENSES.get(tier, {})


def root_lens(root: str) -> dict | None:
    """Return a curated practical lens for a single root, if available."""
    return ROOT_LENSES.get(root)


def available_root_lenses() -> Iterable[str]:
    """Return the list of roots that have a curated practical lens."""
    return list(ROOT_LENSES.keys())


def disclaimer_text() -> str:
    return (
        "**Interpretive overlay.**  Everything below is a *practical-lens reading* "
        "of the computed numbers — translation tips, teaching parallels, and "
        "everyday parallels.  These are not facts produced by the analysis; "
        "they are reasoned suggestions that follow from the structural pattern "
        "the data reveals.  Treat them as starting points for your own thinking, "
        "not as theological claims."
    )
