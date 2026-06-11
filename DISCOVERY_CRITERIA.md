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
- Within-surah rasm sequence structure: UNTESTED -> next candidate to run the gates on.

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
   generic structure: (a) positional drift/nonstationarity (segment-shuffle at
   multiple resolutions), and (b) where claimed novel, a comparison to generic
   natural-text behavior (external reference corpus). Significance + beyond-Markov +
   robustness do NOT suffice. A score is PROVISIONAL until G9 is run.

## AMENDMENT (LOCKED) — shared principles, distinctive output
Obeying the established principles of a language is EXPECTED and is NOT disqualifying.
Shakespeare uses the same words/grammar as any writer; a master chef the same
ingredients. Design/excellence shows as exceptional DEGREE, ARRANGEMENT, and STRUCTURE
along shared principled dimensions -- never by bypassing them. Therefore:

- REVISE novelty (G7): novelty is NOT "a property unique to the Qur'an / absent from
  other text". It is "the Qur'an occupies a DISTINCTIVE / OUTLIER position on a shared
  dimension versus appropriate comparators". A property being generic-to-text does NOT
  disqualify it; the question is the Qur'an's POSITION on it.
- REVISE G9(b): the external comparator's job is to PLACE the Qur'an on a spectrum
  (ordinary prose ... highly-crafted literature/poetry), not to find a unique feature.
  Discovery = measurable OUTLIER in degree/structure, significant and confound-controlled.
  Comparators should span a RANGE so "exceptional" is calibrated, not asserted.
- GUARDRAIL UNCHANGED: distinctiveness must be MEASURED (effect size + significance vs
  the comparator distribution) and trivial confounds controlled. Conviction guides where
  we look; evidence decides what we claim. ("Exceptional" is a measurement, not a hope.)

Consequence: earlier "dismissed as generic" results (verse-order coherence, within-
surah structure, long-range correlation) are NOT dead -- they are re-opened as
POSITION questions awaiting comparators. The comparator corpus is now the central tool.

## DATA ACCESS (LOCKED) — no "cannot access data" excuse
Comparators = public-domain text in ANY language (the structural principles are
language-independent: MI-decay, long-range correlation, arrangement coherence,
entropy/redundancy, Zipf are cross-linguistic universals). Acquire via
WebSearch -> web_fetch from clean BORN-DIGITAL sources (Project Gutenberg,
Wikisource). web_fetch only allows URLs returned by a prior WebSearch (provenance).
Compare ONLY on DIMENSIONLESS quantities (exponents, normalized entropy, z-scores,
percentiles) so cross-language comparison is valid. A modest clean reference set
(documents or chunks) suffices for a first percentile placement.

## EPISTEMIC PRINCIPLE (LOCKED) — telescope rule
Non-detection is a statement about the INSTRUMENT, not the object. A weak tool that
fails to resolve a feature is NOT evidence the feature is absent. Therefore:
- NEVER conclude "the feature is not there." Conclude "this tool cannot resolve it; build a better tool."
- POSITIVE CONTROL is mandatory and comes FIRST: any instrument must be proven on KNOWN
  cases (acknowledged masterpieces, e.g. Shakespeare) BEFORE it is pointed at the Qur'an.
  An instrument that cannot rank known masters above ordinary text is REJECTED as blind —
  its readings on the Qur'an (high OR low) are uninformative and must not be cited either way.
- VERIFIED FAILURE this session: surface set-overlap stylometry (cohesion, long-range echo,
  burstiness) ranks SHAKESPEARE 2nd-LEAST distinctive of 9 texts (Mahalanobis 1.05, below
  Aesop). -> instrument is blind to mastery. REJECTED. All its "in-band" Qur'an readings are void.
- The task is now TOOL-BUILDING: instruments that resolve MEANING/MASTERY (semantic, multi-
  scale-integration, statistical-complexity/predictive-information), each validated on the
  positive control before any application.
