# Discovery Go/Abort Criteria — pre-registered gates for any candidate latent feature
# LOCKED. Apply to EVERY candidate. Declare candidate + scale + null + thresholds
# BEFORE running. Report all candidates incl. aborted (no cherry-picking).

Success criterion: a latent feature that is (1) attributable to the transmitted
text, (2) statistically real under a proper null, (3) survives multiplicity and
confounds, (4) of non-trivial magnitude, (5) robust, and (6) NOT already in the app.

## HARD GATES (fail any -> ABORT)
G0 PROVENANCE. Computed on Tier-1 layers (rasm letters/words, within-verse and
   within-surah order, fawasil). If it depends primarily on mushaf surah-order,
   nuzul chronology, or diacritics -> ABORT (or demote to "mushaf-organization",
   not a divine-attributable feature).
G1 ESTIMATOR VALIDITY. On known-answer controls (IID -> null; Markov -> exp/null)
   the bias-corrected estimator returns the correct answer. Manufactures structure
   from controls -> ABORT.
G2 SIGNIFICANCE. p < 0.05 vs a STRUCTURE-PRESERVING surrogate null (preserves
   rate / length / autocorrelation as relevant), not a plain shuffle.
G3 MULTIPLICITY. If the feature makes many claims (per triple/pair/root): require
   BH-FDR q < 0.10 with >= 5 surviving items, OR one pre-specified GLOBAL statistic
   significant. Nothing survives FDR -> ABORT as a nameable feature.
G4 CONFOUND. Survives the relevant control(s): frequency-matched, length-matched,
   within-surah detrend (block structure), provenance. Collapses -> ABORT.
G5 EFFECT SIZE (meaningfulness floor, not just significance):
     - info measures: bias-corrected excess >= 1% of the relevant marginal entropy
       AND beyond-baseline ratio >= 3x.
     - scaling exponents (DFA/Hurst): |alpha-0.5| >= 0.10 AND z >= 5 vs surrogate.
     - correlations: |partial r| after controls >= 0.20 AND p < 0.01.
   Tiny-but-significant -> ABORT or demote to "aggregate diagnostic".
G6 ROBUSTNESS. Same sign and within ~20% across >= 2 estimator/parameter choices
   (encoding, bins, seed) AND leave-one-out (drop any one surah/root) stays sig.
G7 NOVELTY. |correlation| with the nearest existing app measure (co-occurrence,
   PMI/Jaccard, lead-lag, co-location, motifs, topics, spatial) <= 0.5. Largely
   reproduces an existing measure -> ABORT (redundant).

## SOFT GATE (scored, not pass/fail)
G8 INTERPRETABILITY. Do the top outputs cohere (recognizable structure)? Raises
   confidence; NOT sufficient alone (synergy had face validity but failed G3).

## DECISION
GO    = all hard gates pass -> implement (find its home in the app).
HOLD  = one fixable gate fails (borderline size, wrong scope) -> refine, re-test ONCE.
ABORT = an intrinsic hard gate fails (provenance, redundancy, FDR-null w/ no path).

## RETROACTIVE CHECK (the gates reproduce this session's actual calls)
- Rhyme / fawasil: G0 ok, G2 ok (p=.003), G4 ok, G5 large -> GO (but G7 weak: known).
- Within-verse synergy: G3 FAIL (0 survive FDR), G5 fail (~0.0008 bits) -> ABORT (demote to aggregate).
- Across-verse synergy: G2 FAIL (below chance) -> ABORT.
- Cross-scale binding: G2 FAIL (p=0.28) -> ABORT.
- Tensor (position mode): G5/G6 FAIL (z=2.2) -> ABORT/HOLD.
- Transfer entropy: G7 FAIL (r=0.80 w/ co-location; redundant w/ lead-lag) -> ABORT.
- Verse-length DFA: G4 FAIL (0.97 -> 0.53 within-surah) -> ABORT.
- Revelation vs richness: G4 FAIL (partial r = -0.08) -> ABORT.
- Within-surah/unit-boundary recovery (rasm): TESTED 2026-06-12. G0-G6 PASS; G4 PASS (AUC survives length
  removal 0.87->0.84; 3 converging modalities); G7 FAIL (corr 0.71 with rhyme L06) -> ABORT as new feature.
  Durable value = multi-modal convergence + surface-sufficiency BOUND (AUC~0.85, no recoverable partition
  F1~0.3). See research/intrinsic/FINDING_unit_recovery.md.

## DISCOVERY VALUE SCORE (1-10) — LOCKED scoring scheme for every candidate
Two stages. Eligibility first, then a weighted score. No score is assigned until
the candidate has been TESTED on real data.

STAGE 1 — Eligibility (the hard gates G0-G7 above).
  - Fails any hard gate -> NOT a discovery. Score 1-3 (how close it got). Stop.
  - Passes all hard gates -> eligible; go to Stage 2 (score 4-10).

STAGE 2 — Weighted value score (only for gate-passers), each sub-score 0-10:
  Novelty / "not already known"   x 35%   (unknown phenomenon=9-10; known-but-never-
                                           -quantified/validated or absent-from-app=5-6;
                                           already in app or textbook-measured=1-2)
  Effect size / magnitude         x 20%   (large & obvious=9-10; clears floor only=3-4)
  Importance / interpretability   x 20%   (reshapes understanding=9-10; minor=3-4)
  Provenance / divine-attribution x 15%   (clean Tier-1=9-10; human-layer caveats lower)
  Robustness / reproducibility    x 10%   (holds across params/splits/representations)
  (Significance/gate-passing is Stage-1 eligibility, not re-scored.)

Bands: 8-10 landmark · 6-7 solid, implement · 4-5 marginal, implement only if cheap ·
       1-3 aborted/failed.

### Worked example (LOCKED reference): within-surah passage structure
  Eligibility: PASS all gates.
  Novelty 5 (sectioning is qualitatively known to scholarship; NEW as a gate-passing
    quantification + absent from app) · Effect 4 (~1.3% of entropy, just over floor) ·
    Importance 6 (clear meaning: passage organization) · Provenance 8 (Tier-1 order,
    survives surface words) · Robustness 9 (split-half identical, roots+surface, beyond-Markov).
  Weighted = .35*5 + .20*4 + .20*6 + .15*8 + .10*9 = 5.85 -> SCORE 6/10. Solid; implement.

### Retroactive scores (this session)
  within-surah passage structure ... 6  (GO)
  rhyme / fawasil ................... 3-4 (passes gates but novelty ~1: textbook-known)
  higher-order synergy ............. 3  (fails FDR + effect size)
  cross-scale binding .............. 1  (fails significance)
  tensor (position mode) ........... 2  (fails effect size/robustness)
  transfer entropy ................. 2  (fails novelty: redundant with lead-lag/co-location)
  verse-length long memory ......... 2  (fails confound: surah-block)
  revelation vs lexical richness ... 2  (fails confound: length artifact)

## CORRECTION (supersedes the worked example above) + new mandatory gate
Scrutiny of the within-surah candidate with a drift control (drift_control.py) showed
the signal is largely COARSE within-surah compositional DRIFT, not fine structure:
beyond-drift residual erodes monotonically 1.32% -> 1.10% -> 0.83% (3/6/12 segments),
dropping below the effect floor. Drift/topical nonstationarity is the most generic
property of any long text -> novelty ~2.
  REVISED SCORE: within-surah passage structure  6 -> 3/10. NOT a discovery (real but
  generic/known). The GO was premature.

NEW HARD GATE (add to Stage 1):
G9 TRIVIAL-EXPLANATION CONTROL. The effect must survive nulls that preserve known
   generic structure, ALL INTERNAL (the One Law — no external corpus is admissible as
   evidence, ever): (a) positional drift/nonstationarity (segment-shuffle at multiple
   resolutions); (b) structure-preserving surrogates built from the TEXT'S OWN material
   (length-/rate-/rhyme-class-matched shuffles; length-matched fake boundaries at shifted
   offsets). Distinctiveness = measurable departure from the text's OWN null at meaningful
   effect size, NEVER a comparison to other texts. Significance + beyond-Markov +
   robustness do NOT suffice. A score is PROVISIONAL until G9 is run.

## AMENDMENT (LOCKED) — shared principles, distinctive output
Obeying the established principles of a language is EXPECTED and is NOT disqualifying.
Shakespeare uses the same words/grammar as any writer; a master chef the same
ingredients. Design/excellence shows as exceptional DEGREE, ARRANGEMENT, and STRUCTURE
along shared principled dimensions -- never by bypassing them. Therefore:

- REVISE novelty (G7): novelty is NOT "a property unique to the Qur'an / absent from
  other text", NOR "an outlier versus external comparators". It is "the Qur'an departs
  from its OWN shuffle/null by an exceptional DEGREE, ARRANGEMENT, or STRUCTURE on a
  shared principled dimension." A property being generic-to-text does NOT disqualify it;
  the question is the magnitude of the Qur'an's departure from its own null.
- G9(b) (INTERNAL): calibrate "exceptional" against the text's OWN structure-preserving
  surrogates at multiple resolutions — not against other texts. The spectrum is
  random-shuffle ... canonical ... trivially-sorted, all computed on the Qur'an itself
  (cf. L14/L19 intermediate-band). Outlier-ness is departure from this internal spectrum.
- GUARDRAIL: distinctiveness must be MEASURED (effect size + significance vs the text's
  own null) and trivial confounds controlled. Conviction guides where we look; evidence
  decides what we claim. ("Exceptional" is a measurement, not a hope.)

## DATA ACCESS (LOCKED, 2026-06-11 RECONCILIATION) — the One Law, no external source
SUPERSEDES the prior external-comparator regime (struck above and here). Per the
2026-06-07 pivot to Qur'an-internal instruments: **no external corpus, model, or
embedding is admissible as evidence — ever.** The only null/comparator is the text's
OWN shuffle (verse/token/segment shuffles; length-, rate-, rhyme-class-matched
surrogates; length-matched fake boundaries). There is no "cannot access data" issue
because no external data is needed or allowed. Earlier "dismissed as generic" results
(verse-order coherence, within-surah structure, long-range correlation) are re-opened
as INTERNAL position questions — placed on the text's own random→canonical→sorted
spectrum — not against any external corpus.

## EPISTEMIC PRINCIPLE (LOCKED) — telescope rule
Non-detection is a statement about the INSTRUMENT, not the object. A weak tool that
fails to resolve a feature is NOT evidence the feature is absent. Therefore:
- NEVER conclude "the feature is not there." Conclude "this tool cannot resolve it; build a better tool."
- POSITIVE CONTROL is mandatory and comes FIRST, and is INTERNAL (One Law): prove the
  instrument on PLANTED/SYNTHETIC signals injected into the text's OWN material — e.g. a
  planted rhyme/boundary/period in a shuffled rasm — and confirm it recovers the planted
  signal. An instrument that cannot recover a known planted effect is REJECTED as blind;
  its readings on the Qur'an (high OR low) are uninformative and must not be cited.
  (Do NOT use external masterpieces as the control — external text is inadmissible.)
- HISTORICAL NOTE (pre-pivot, VOID as evidence): a surface set-overlap stylometry once
  ranked 
## G4b — REDUCTION / INVARIANCE TEST (MANDATORY before any grade ≥90). LOCKED 2026-06-12.
A feature is NOT a discovery if the signal it claims is reproduced by a simpler/known thing.
Before grading ≥90, you MUST run BOTH and pass BOTH:
  (a) INVARIANCE: strip the structure the claim depends on (order/position/sequence/neighbours) and re-measure.
      If a position/order-free version reproduces it (e.g. word-only ≈ full), the "structure" claim is FALSE —
      it is a vocabulary/marginal fact, not the claimed structural law. → fail / recast.
  (b) KNOWN-MEASURE ABLATION: train/measure using ONLY each nearest existing measure (rhyme L06, length,
      co-occurrence, onset L18…); if any reproduces the signal, or if corr(full, known) > 0.5, → G7 fail.
Lesson that forced this (L27 āyah-recovery, banked 91 then DEMOTED to 84): it was ORDER-INVARIANT
(word-only AUC 0.939 ≈ full 0.957) and the closure forms ARE the fāṣila — a morphological restatement of rhyme,
not a segmentation discovery. NEVER grade ≥90 before G4b passes.
