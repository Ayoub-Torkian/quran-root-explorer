# FINDING — Instrument upgrades move the wall (2026-06-12). Base-truth axiom, data-backed.

Three runs with sharper instruments. Two wins, one honest no-lift. Nothing changed in the text.

## 1. Āyah recovery — RECOVERED, and non-redundant (WIN)
- Rich features (morphology suffixes, letter n-grams, opener/closure) + HistGradientBoosting, group-CV:
  **AUC 0.81 → 0.958, best-F1 0.39 → 0.69** (rec 0.65 / prec 0.73).
- **G7 PASS:** non-rhyme features alone reach **AUC 0.918**; corr(full, rhyme-only) = **0.42 (<0.5)**,
  corr(non-rhyme, rhyme) = 0.16. The shallow version failed G7 at 0.71 — the deeper structure is genuinely new.
- → The Āyah is now **substantially recoverable from the rasm**, and not just rhyme. Real candidate.

## 2. Sūra seams — NO LIFT (honest)
- Same rich-feature learner: AUC **0.74** (below the membrane-logistic's 0.87); best-F1 0.38 (rec 0.24 / prec 0.87).
- Word-level morphology doesn't transfer to the sparse (113), coarse āyah-level seams. The membrane-logistic
  (AUC 0.87, F1 ~0.3) remains best. Per the axiom: still assume instrument limit (only 113 examples; coarse
  cues) — do NOT claim recovered. Needs a different instrument (more seam-specific features / more signal).

## 3. Genome FOLDING (contact-decay) — REVIVED from demotion (WIN)
- Prior: demoted as length artifact (linear corr overlap~distance = −0.04).
- Clean instrument: cosine sūra-overlap (size-normalized) + **order-permutation null** (every sūra's size held
  EXACTLY fixed). Result: adjacent sūras mean overlap **0.45 vs 0.35** null → **z=9.5**; d≤5 → **z=16**;
  reference corr **+0.32**. p<0.001 throughout. Length fully controlled by construction.
- → The muṣḥaf **clusters high-overlap sūras nearby** = real contact-decay (Hi-C/genome-folding analog). The
  earlier demotion was the INSTRUMENT (raw size-confounded overlap), not the text.
- **Status: strong REVIVAL candidate**, not yet banked as ≥90. To formalise: G0 (it is an *arrangement* feature
  — belongs with order-determinacy, the north star's "why this configuration"); G7 (novelty vs existing
  order/network measures — order-proximity coherence is distinct from co-occurrence and from the global
  order-bits, but confirm corr ≤0.5); G3/G6 robustness across overlap metrics. No overclaim until gated.

## Takeaway (the locked axiom, with data)
Two of three walls moved purely by upgrading the instrument (āyah F1 0.39→0.69; folding −0.04→+0.32, z=16).
The text was never the limit. Guardrail held: sūra reported honestly as no-lift, folding flagged as candidate
pending gates — no wishful promotion.

Scripts: ~/ayah_deep.py, ayah_g7.py, sura_deep.py, genome_folding.py (run-once, not deployed).

## GATE OUTCOMES (ran the confounds, 2026-06-12)
- **FOLDING → RE-DEMOTED (G4 FAIL).** proximity↔length-similarity corr = 0.86; partial
  corr(overlap, proximity | length) = **−0.086**; length-band null z=3.4 (vs naive 16). The size-fixed null
  last turn was too weak an instrument — folding is **mostly a length artifact**. Original demotion stands.
  (Guardrail working: a z=16 excitement walked back by the proper confound. No overclaim.)
- **ĀYAH RECOVERABILITY → PASSES the gates (genuine candidate).**
  - G0 ✓ rasm morphology (consonantal suffixes, Tier-1) · G2 ✓ vs null · G5 ✓ (AUC 0.958, F1 0.69) ·
    G6 ✓ held-out-sūra CV · G7 ✓ (corr 0.42 with rhyme; non-rhyme AUC 0.918).
  - **G4 ✓:** morphology+closure ALONE (no length, no rhyme, no position) = **AUC 0.861** — independent of
    both length (0.82) and rhyme (0.80). The recovery rests on real morphological structure.
  - → **The Āyah is substantially recoverable from the rasm via intrinsic morphological + closure structure.**
    First clean gate-passer of the arc. Value ≈ 7/10 (solid). Ready to write into the Determinacy ledger.
