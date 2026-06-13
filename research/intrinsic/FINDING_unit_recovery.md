# FINDING — Unit recovery (Āyah & Sūra) from the rasm: marked, not yet recoverable (2026-06-12)

**Goal (north star, sufficiency half):** recover the canonical partition — the 6,236 āyah breaks and
the 113 sūra seams — from the bare consonantal skeleton (One Law: diacritics demoted; text's own
shuffle / random placement as null). Sufficiency = the text itself locates its units.

## Āyah recovery (6,236 breaks)
- Best intrinsic detector (rhyme + length-cadence): **F1 0.30, recall 0.41** vs random 0.115 (**z≈60**)
  and word-shuffle 0.09 (**z≈37**).
- Oracle (rhyme handed in): F1 0.65. Modal final consonant covers **80%** of āyah-ends.
- Instrument-upgrade attempts (periodicity rhyme-ID, length-prior DP, insertion) REGRESSED (F1 0.27, 0.12).
- **Bottleneck:** intrinsic fāṣila identification, not cadence.

## Sūra recovery (113 seams)
- Cues tested (on āyah sequence): block root-overlap collapse (membrane), rhyme-run change, length-regime
  change, muqaṭṭaʿāt opener (no āyah has 0 roots, so that cue is unavailable in this corpus).
- Single best: sustained rhyme-run change — **F1 0.25, z≈17.6** vs random; rhyme *changes* at **75%** of
  true seams (high recall) but also mid-sūra (precision ~4% as a raw filter).
- Combined (membrane+length+rhyme) top-113: F1 0.20, z≈5.3.

## Consolidated verdict — honest
| unit | NECESSARY (marked, vs null) | SUFFICIENT (recoverable) |
|---|---|---|
| Āyah | **YES** — ends in the fāṣila; 80% modal-consonant; z≈37–60 | **NO** — F1 0.30 intrinsic (0.65 oracle) |
| Sūra | **YES** — rhyme switches at 75% of seams; z≈5–18 | **NO** — F1 0.20–0.25 |

Both units are **intrinsically marked** (their boundaries carry real, significant signal on the rasm), but
**neither is cleanly recoverable** by hand-built surface detectors. Per TELESCOPE this is an **instrument
limit**, not a text limit — two non-exclusive readings:
1. The proper instrument is a **learned multi-cue segmentation model** (HMM/CRF or logistic over the cue
   features, cross-validated across sūras) — hand-tuned thresholds leave most of the signal on the table.
2. The units may be **under-determined by surface cues**, with part of the definition carried by deeper
   (morphological/semantic) structure — itself a north-star-relevant claim if it survives the learned model.

**Grade:** neither recovery clears ≥90. We have firmly established the **necessary half** of both unit
definitions on the rasm (significant vs the text's own null); **sufficiency remains open**, now pinned to a
specific next instrument.

## Learned model (the recommended instrument) — cross-validated
- **Logistic combiner over the cue features, grouped 5-fold CV (held-out sūras):**
  - Sūra seams: **AUC 0.872** (z≈21 vs random); best-threshold F1 0.28 (rec 0.34 / prec 0.24).
  - Āyah breaks: **AUC 0.81**; best-threshold F1 0.39 (rec 0.56 / prec 0.30).
  - Top cues: rhyme-change, short next-unit, membrane drop (sūra); word-length, ends-in-top-rhyme (āyah).
- **Sequence model (learned per-position probs + Viterbi + āyah-length prior):** precision rises to 0.66
  but recall falls to 0.18 — net F1 0.28. The length prior makes it under-segment; AUC doesn't convert
  to a clean partition.

### Final verdict (after the full instrument campaign)
The Sūra and Āyah boundaries are **strongly discriminable** from the bare rasm — cross-validated
**AUC ≈ 0.81 (āyah) / 0.87 (sūra)**, far above null. But across hand-built, learned, and sequence models
the **exact partition is NOT recoverable** (best F1 ≈ 0.3–0.4). So:
- **Necessary half — established, hard number:** the units are marked AND identifiable from the consonants
  with AUC ~0.85 (cross-validated). Strong, gradeable.
- **Sufficiency from the SURFACE — ruled out (for these cues):** rhyme + length + root-overlap do not
  uniquely reconstruct the partition. The remaining definition is carried by structure **beyond** the
  surface rasm cues tested (morphology / syntax / semantics), or needs features we haven't built. This is
  itself a north-star result: it bounds how far the bare consonantal surface determines the units.

## Gate results (DISCOVERY_CRITERIA G0–G7) — ran as a ledger candidate
Candidate: "intrinsic unit-boundary discriminability from the rasm (sūra seams)."
- G0 provenance ✓ (rasm, fawāṣil, within/across-sūra order) · G1 estimator ✓ (nulls return chance) ·
  G2 significance ✓ (z≈21–60) · G3 multiplicity ✓ (one global AUC) · G5 effect ✓ (AUC 0.87; 15× over null) ·
  G6 robustness ✓ (held-out-sūra CV; consistent across logistic/Viterbi/hand-built).
- **G4 confound ✓:** AUC 0.872→0.840 when length cues removed; each modality discriminates alone
  (rhyme 0.80, membrane/roots 0.75, length 0.73) → ≥3 converging modalities, not a length artifact.
- **G7 novelty ✗ (FAIL):** corr(full-model, rhyme-only) = **0.71** (> 0.5). The discriminability is
  largely the existing fāṣila/rhyme feature (L06). → **Does NOT enter the ledger as a new feature** (redundant).

**Honest disposition:** ABORT-on-G7 as a *new atomic feature*. The non-redundant, durable contributions are
(a) the **multi-modal convergence** — rhyme, roots, and length each independently mark the seams (AUC≥0.73) —
and (b) the **surface-sufficiency bound** (AUC ~0.85 discriminability, but no recoverable partition, F1 ~0.3).
Both are consolidations/north-star bounds, not a ≥90 ledger entry. Recorded; not banked as a feature.

## Reconfigure note (movement rule)
Two surfaces (āyah, sūra) both sub-90 with hand-built detectors → STOP grinding hand-built thresholds.
Next instrument = a **learned cross-validated segmentation model** over the (already-built) cue features.

Scripts (run-once, not deployed): `~/ayah_*.py`, `~/sura_*.py`.
