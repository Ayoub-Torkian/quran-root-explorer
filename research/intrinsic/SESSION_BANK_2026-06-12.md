# Discovery session — banked 2026-06-12

## The journey (where we started → went → are now)
- **Started:** north star = define a **Sūra** and an **Āyah** to *necessity AND sufficiency*. Chose the
  **sufficiency test**: can the bare rasm *recover* its own units (the 6,236 āyah breaks, 113 sūra seams)?
- **Went:** āyah recovery (5 detectors: rhyme, DP, periodicity) → sūra recovery (membrane, rhyme-run,
  length) → a **learned cross-validated** logistic model → **Viterbi** sequence decode → ran the **G0–G7
  gates** → pivoted to a fresh probe: the **attraction–repulsion root field** (cheap global test).
- **Now:** **two clean bounds banked; zero new ≥90 features.** Both candidates died on **G7 (redundancy)** —
  the right wall, the one that stops us re-labelling known measures.

## What is now established (hard, honest)
1. **Units are intrinsically MARKED on the rasm — AUC ≈ 0.85, cross-validated** (rhyme + root-membrane +
   length each discriminate alone, AUC ≥ 0.73 → ≥3 converging modalities). This is the **necessary half** of
   both unit definitions, with a number. [FINDING_unit_recovery.md]
2. **Surface-SUFFICIENCY is ruled out** — no model recovers the exact partition (best F1 ~0.3–0.4). The
   remaining definition lives in **structure beyond the surface cues** (morphology / syntax / semantics).
3. **The discriminability is rhyme-redundant** (corr 0.71 with L06) → not a *new* feature, a consolidation.
4. **The root field is attraction-dominated** (10.6× vs null); **no qualifying repulsion** (2.5×, sub-floor,
   topic-redundant). The interaction is association, not a charge-like balanced field. [FINDING_root_field.md]
5. **Meta:** the surface root/sequence statistics are **largely exhausted** — they keep collapsing into the
   app's existing measures (co-occurrence, rhyme, topics, length). G7 is the recurring ceiling.

## North-star standing
| unit | necessary (marked) | sufficient (recoverable) |
|---|---|---|
| Āyah | ✓ rhyme/fāṣila, AUC 0.81 | ✗ open — needs deeper structure |
| Sūra | ✓ multi-modal, AUC 0.87 | ✗ open — needs deeper structure |

We converted "is a unit definable?" into a measured answer: **the surface determines the boundaries to
AUC ~0.85 but not to a recoverable partition; the rest is deeper structure.** That is real direction, not a
maze — but the surface vein is worked out.

## When resumed — ranked next moves
1. **Sufficiency via deeper structure:** morphological segmentation / syntactic-pause / root-embedding-context
   features, then re-decode. The only path likely to yield a *non-redundant* unit-definition result.
2. **A structurally orthogonal probe** (conserved invariant under the arrangement; rasm letter-level
   structure) — pre-register per the gates; honest odds ~15–20%.
3. **Product/UI or another track** — the ledgers are in good shape (Determinacy + Correspondence both carry
   their discovery sections).

## Artifacts
- Findings: FINDING_ayah_recovery.md · FINDING_unit_recovery.md · FINDING_root_field.md
- Gates updated: DISCOVERY_CRITERIA.md (unit-recovery candidate marked TESTED → G7 abort)
- Full move log with timestamps + bearings: JOURNEY_LOG.md
- Scripts (run-once, not deployed): ~/ayah_*.py, ~/sura_*.py, ~/repulsion.py
