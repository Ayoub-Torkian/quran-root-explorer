# FINDING — The Āyah is recoverable from the RASM (fused detector pilot)

*A. Torkian, 2026-06-11. Full pilot of Candidate A (`/tmp/ayah_pilot.py`). Rasm only; null = the text's own
shuffle; two-way cross-validation (train odd sūras / test even, and reverse).*

## Result (held-out)

A logistic fusion of three rasm-only channels recovers canonical āyah ends from the bare consonantal word
stream:

| channel (rasm, modality) | test AUC | recall @ budget |
|---|---|---|
| M1 rhyme — final 3 letters (symbol/sound) | 0.936 / 0.926 | 0.61 / 0.55 |
| M2 clausal — next word opens و/ف (syntax) | 0.650 / 0.629 | 0.23 / 0.23 |
| M3 length cadence — final-word length (wave) | 0.776 / 0.786 | 0.24 / 0.30 |
| **FUSED (trained LR)** | **0.943 / 0.938** | **0.61 / 0.63**, best-F1 **0.63 / 0.64** |

Recall 0.61 vs a base rate of 0.080 = **7.6× chance**. Modalities are not redundant (pairwise r: rhyme–clausal
0.20, clausal–length 0.23, rhyme–length 0.48), so ≥2 genuinely independent channels converge on the same
boundary.

## Gate audit (DISCOVERY_CRITERIA, locked)

- **G0 provenance** — PASS. Uses only rasm letters (the fāṣila rhyme lives in the *final consonants* ـون=و+ن,
  ـين=ي+ن, ـات, …). No diacritics.
- **G1 estimator validity** — PASS. Positive control (planted nun-rhyme + waw-opener in a random corpus)
  recovers planted ends at AUC 0.98 / 0.95. Not blind.
- **G2 significance** — PASS. Within-sūra word-shuffle null collapses AUC 0.94→**0.52**.
- **G3 multiplicity** — PASS (global statistic: held-out AUC, pre-specified).
- **G4 confound** — PASS. (a) length-matched **fake-boundary** recovery AUC **0.518** → the signal is at the
  *real* positions, not an artifact of chunking into verse-length pieces. (c) drop the top-30 ending trigrams
  and the detector still scores **AUC 0.903 / recall 0.35 on the RARE endings** → it is not merely the saj'
  formulae.
- **G5 effect size** — PASS, large. AUC 0.94; recall 7.6× base; F1 0.63.
- **G6 robustness** — PASS. Both CV directions agree (0.943/0.938); 3 representations; **56/57 test sūras**
  have rhyme-AUC > 0.70 (98%).
- **G7 novelty** — PARTIAL/PASS. Not redundant with any in-table measure; it **overturns L17**, which logs the
  āyah as "vowel-borne / instrument-limited on the rasm (~5% recall)." The fāṣila *rhyme* is textbook-known —
  what is new is that the āyah boundary is **objectively recoverable from the consonantal skeleton alone**
  (the divine substrate), i.e. the verse division is not a creature of the human recited/diacritic layer.
- **G9 trivial-explanation** — (a) PASS. Drift/chunking controlled internally by the **length-matched
  fake-boundary null** (AUC 0.52) and the within-sūra shuffle (0.52). **(b) N/A under the One Law.** External
  comparison is inadmissible (the 2026-06-07 pivot to Qur'an-internal instruments; no external source is
  evidence). The trivial-explanation control is therefore satisfied by the internal nulls alone; the score is
  **not** provisional on any external step.

## Grade (Stage-2 weighted, honest)

Novelty 7–8 · Effect 9 · Importance 9 · Provenance 9 · Robustness 9
→ weighted **≈ 0.83–0.87 → grade ~85/100 (final on internal criteria; not provisional).**

**It lands just under the ≥90 table bar, and novelty is the single swing factor.** Read as "the fāṣila is
known," novelty ≈ 7 → ~83. Read as "this **corrects the program's own logged conclusion** that the āyah needs
the vocalised layer — the verse is defined on the divine substrate," novelty ≈ 8 → ~86. Either way it sits
**below ≥90**, so it does **not** enter the discovery table; it lands as a **logged correction to L17 + a
sub-90 "necessary rasm āyah definition."** The rubric makes novelty the human call — but no reading reaches 90
without inflating the known fāṣila, which we will not do.

## What this means for the north star

The **āyah now has a necessary definition on the divine substrate**, parallel to L11 for the sūra: *an āyah end
is a multimodal rasm discontinuity — a fāṣila consonant-rhyme reset, reinforced by clausal closure and a
length cadence — recoverable blind at AUC 0.94.* The prior "instrument-limited on the rasm" verdict was an
instrument limitation (the telescope rule), now lifted. Two honest residuals: (i) ~39% of ends are not yet
recovered at the F1 operating point — the *sufficient* half of the āyah definition is still open; (ii) the
finest rhyme distinctions (ـِ vs ـُ) remain vocalic and corroborative only.

## Sufficiency pilot (2026-06-11, `/tmp/ayah_suff.py`)

Decoded the fused detector to a real segmentation (best-F1 operating point, held out both directions):
**P ≈ 0.60, R ≈ 0.69, F1 ≈ 0.64.** So the rasm āyah is **multimodally necessary** (three converging,
reasonably-independent channels: rhyme/sound AUC 0.94, clausal/syntax 0.65, length/wave 0.78 — rhyme–clausal
r=0.20) but **only partially sufficient** (~36% of ends unrecovered at best-F1). The attempt to add a fourth,
**lexical** modality (root-novelty reset across the boundary) was **inconclusive — instrument-limited**: only
~8% of words could be aligned rasm→root (hamza/weak-radical mismatch; greedy subsequence), so M4 sat at chance
(AUC 0.50) and added nothing. This is an alignment-instrument failure, **not** evidence that lexical reset
carries no signal. A proper morphological alignment (capped ~19–29% per `SYNTHESIS.md` §8) is the only way to
test it, and likely will not close the gap — the unrecovered ~36% are plausibly the same kind of "soft" ends
the sūra faces. **Working verdict: the āyah's NECESSARY rasm definition is established; full sufficiency on the
rasm likely faces a partial ceiling, as the sūra does.**

## Status
1. **L17 revised** ✓ (2026-06-11): "vowel-borne / instrument-limited" → "rasm-recoverable at AUC 0.94; vocalic
   layer only refines."
2. **Grade FINAL at ~85 on internal criteria** — below the ≥90 table bar. Logged as a correction to L17 + a
   sub-90 necessary rasm-āyah definition. (No external comparator — inadmissible under the One Law.)
3. **Sufficiency stays open** at F1 ~0.64; the lexical modality is alignment-blocked. Likely a partial ceiling
   like the sūra. Not pursued further unless a rasm-admissible morphology channel is built.
