"""pair_classification.py  ·  v1.2 enhancement
=============================================

Classifies a pair of Qurʾanic roots into one of three structural categories
based on their co-occurrence behaviour. Pure data-driven labelling — no
theological or interpretive conjecture beyond a tier name and the threshold
that produced it.

Categories
----------
- **stipulative** — lift ≥ 10. The pair is treated as a single concept in
  two words. (Examples discovered in calibration: ʿadl/qisṭ ×70.9,
  ʿusr/yusr ×78, qisṭ/mīzān ×67.)

- **independent** — lift ≤ 1.0. The two roots are statistically independent
  or repel each other. They live in separate semantic neighborhoods.
  (Example: ẓulm/ʿadl lift 0.9; silm/ṭaghā lift 0.0.)

- **embedded** — lift 2.0 ≤ lift < 10. The roots discuss each other
  often but as cross-cutting categories, not as a single concept.
  (Examples: īmān/kufr ×2.3, ḥasan/sūʾ ×6.6, ʿilm/jahl ×2.5.)

- **mild** — lift 1.0 < lift < 2.0. Above chance but only just; not a
  meaningful association.

The 12-pair reference set used for calibration (see CALIBRATION_PAIRS)
was computed in earlier sessions from the same Quranic Arabic Corpus
root tags this app uses.

Usage
-----
>>> from pair_classification import classify_pair, lift_for_pair
>>> tier, label, desc = classify_pair(root_a_mask, root_b_mask, N_ayahs)
"""
from __future__ import annotations
from typing import Iterable

# ---------------------------------------------------------------------------
# Thresholds  (data-driven, no interpretation beyond the threshold)
# ---------------------------------------------------------------------------
TIER_THRESHOLDS = [
    # (lower_bound_inclusive, upper_bound_exclusive, tier_id, label, color, desc)
    (10.0, float("inf"), "stipulative", "Stipulative pair",
     "#7209B7",
     "Treated as a single concept in two words. The corpus uses one as a "
     "near-definition of the other."),
    (2.0, 10.0, "embedded", "Embedded pair",
     "#06AED5",
     "Discussed together frequently but as cross-cutting categories, "
     "not as a single concept."),
    (1.0, 2.0, "mild", "Mild attraction",
     "#80B918",
     "Above chance but only mildly. Not a strong association."),
    (-float("inf"), 1.0, "independent", "Independent / quarantined",
     "#E63946",
     "Statistically independent or repelling. The two roots live in "
     "different semantic neighborhoods and rarely co-occur."),
]


def classify_lift(lift: float) -> tuple[str, str, str, str]:
    """Return (tier_id, label, color, description) for a given lift value."""
    for lo, hi, tier, label, color, desc in TIER_THRESHOLDS:
        if lo <= lift < hi:
            return tier, label, color, desc
    # Should never reach here, but defensively:
    return "independent", "Independent / quarantined", "#E63946", \
           "Statistically independent or repelling."


def compute_lift(mask_a: Iterable[bool], mask_b: Iterable[bool], n: int) -> float:
    """lift = P(A & B) / [P(A) * P(B)].
    Returns 0 if either root is absent. Inputs are boolean iterables of length n."""
    ma = list(mask_a); mb = list(mask_b)
    sa = sum(ma); sb = sum(mb)
    if sa == 0 or sb == 0 or n == 0:
        return 0.0
    ab = sum(1 for a, b in zip(ma, mb) if a and b)
    return (ab / n) / ((sa / n) * (sb / n))


def classify_pair(mask_a: Iterable[bool], mask_b: Iterable[bool], n: int) -> dict:
    """Return a dict with full classification of a pair.

    Keys:
      lift, joint, n_a, n_b, tier, label, color, description, ratio_a_to_b
    """
    ma = list(mask_a); mb = list(mask_b)
    sa = sum(ma); sb = sum(mb)
    ab = sum(1 for a, b in zip(ma, mb) if a and b)
    lift = compute_lift(ma, mb, n)
    tier, label, color, desc = classify_lift(lift)
    return {
        "lift": round(lift, 3),
        "joint": ab,
        "n_a": sa,
        "n_b": sb,
        "tier": tier,
        "label": label,
        "color": color,
        "description": desc,
        "ratio_a_to_b": round(sa / sb, 2) if sb else float("inf"),
    }


# ---------------------------------------------------------------------------
# Reference pairs from the calibration study (used by 8e_Calibration page)
# ---------------------------------------------------------------------------
#
# Each row: anchorA, anchorB, anchorA_count, anchorB_count, joint, lift, tier
#
# These twelve pairs were computed on the same Book6.xlsx the app uses, with
# the same ayah-as-unit co-occurrence rule. See WHAT_WE_LEARN.md from the
# zulm/adl study for the narrative summary.

CALIBRATION_PAIRS = [
    # (label,                anchorA, anchorB, nA,  nB,  joint, lift,    tier,
    #  description)
    ("ʿusr / yusr",          "عسر",   "یسر",   12,  40,  6,    77.95, "stipulative",
     "hardship / ease — bonded at the famous Q94:5-6"),
    ("ʿadl / qisṭ",          "عدل",   "قسط",   24,  22,  6,    70.86, "stipulative",
     "justice / equity — qisṭ is the definition of ʿadl"),
    ("qisṭ / mīzān",         "قسط",   "وزن",   22,  21,  10,   67.49, "stipulative",
     "equity / balance — the procedural triangle's inner bond"),
    ("rashad / ghayy",       "رشد",   "غوی",   19,  18,  2,    36.47, "stipulative",
     "guidance / error — Q2:256 'no compulsion in religion'"),
    ("ṣabr / jazaʿ",         "صبر",   "جزع",   93,  2,   1,    33.53, "stipulative",
     "patience / panic — extreme asymmetry, sparse base"),
    ("dunyā / ākhira",       "دنو",   "ءخر",   128, 242, 57,   11.48, "stipulative",
     "this-world / hereafter — the master time-axis"),
    ("ḥasan / sūʾ",          "حسن",   "سوء",   177, 150, 28,    6.58, "embedded",
     "good / bad — woven through ethical discourse"),
    ("taqwā / fujūr",        "وقی",   "فجر",   237, 21,  3,     3.76, "embedded",
     "taqwā / debauchery — virtue dwarfs vice 11×"),
    ("ḥikma / hawā",         "حکم",   "هوی",   189, 37,  4,     3.57, "embedded",
     "wisdom / caprice — moderate bond"),
    ("nūr / ẓulm",           "نور",   "ظلم",   174, 290, 28,    3.46, "embedded",
     "light / darkness (cosmic, not ethical)"),
    ("ʿilm / jahl",          "علم",   "جهل",   728, 24,  7,     2.50, "embedded",
     "knowledge / ignorance — knowledge wins 30×"),
    ("īmān / kufr",          "ءمن",   "کفر",   723, 465, 126,   2.34, "embedded",
     "faith / disbelief — the largest moral dyad"),
    ("ẓulm / ʿadl",          "ظلم",   "عدل",   290, 24,  1,     0.90, "independent",
     "wrongdoing / justice — independent universes"),
    ("silm / ṭaghā",         "سلم",   "طغی",   142, 39,  0,     0.00, "independent",
     "peace / tyranny — quarantined, zero joint ayahs"),
]


def tier_legend() -> list[dict]:
    """Return a stable legend for the four tiers, for UI display."""
    return [
        {"tier": "stipulative", "label": "Stipulative", "lift_range": "≥ 10",
         "color": "#7209B7",
         "meaning": "Treated as a single concept in two words"},
        {"tier": "embedded",    "label": "Embedded",    "lift_range": "2 - 10",
         "color": "#06AED5",
         "meaning": "Frequent co-occurrence, cross-cutting categories"},
        {"tier": "mild",        "label": "Mild",        "lift_range": "1 - 2",
         "color": "#80B918",
         "meaning": "Above chance but only just"},
        {"tier": "independent", "label": "Independent", "lift_range": "≤ 1",
         "color": "#E63946",
         "meaning": "Statistically independent or repelling"},
    ]
