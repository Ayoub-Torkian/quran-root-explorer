# Preliminary Assessment — all ~31 correspondences (pre-scrutiny triage)

*2026-06-11. First-pass confidence, NOT final. Grades: **A** strong (proper null, large effect, independent) ·
**B** moderate (real but modest or mildly confounded) · **C** weak (no proper null, trivial, or
confound-driven) · **F** fail/reopen · **—** untested. The re-scrutiny pass will confirm or demote each.*

## Grades

| # | attribute | grade | main concern to resolve in re-scrutiny |
|--|--|--|--|
| 4 | membrane (O4) | **A** | clean (0.283 vs 0.870, z=−5) + L11 — strongest |
| 5 | internal weave (O5) | **A** | own-shuffle null, t=10.9 — clean |
| 9/26 | flow-regulation / homeostasis | **A** | z=+20 vs shuffle — clean (but = one signal, see redundancy) |
| 28 | rhythm/pulse (L03/04) | **A** | DFA 0.95 / 1/f — well-established |
| 18 | propagation/formulae | **A** | z=+125; but "reproduction" is metaphor for known saj' repetition |
| 11 | external interface (E, zones) | **A−** | z=+17.6 strong; intake/output sub-probe crude |
| 1 | identity (O1) | **B** | modest margin over local coherence (7.2 vs 4.9) |
| 3 | connectivity (O3) | **B** | 44% real but modest concentration (top-5=9%); some twins thematic |
| 6 | polarity (O7) | **B** | head strong (0.75), tail marginal (0.61) |
| 10 | nervous/signal | **B−** | 10× overlap — but likely NOT independent of O5 weave |
| 24 | folding seq→network | **B** | contact-decay modest (r=0.32); multi-part, recheck |
| 16 | skeleton/muqaṭṭaʿāt | **B−** | t=3.5, but "longer verses" may be a length/Medinan confound |
| 8/23 | scaling / self-similar | **B** | power-law fits are fragile — needs goodness-of-fit |
| 14/22 | robustness/error-correction | **B−** | 73% vs a high 50% baseline — modest |
| 2 | location (O2) | **C+** | R²=0.84 partly the trivial length gradient; relocation t=5.9 modest |
| 7 | hierarchy | **C** | conceptually sound but definitional — needs a sharp test |
| 12 | digestive/reprocessing | **C** | 593 motifs but **NO null run** — may be expected for any mid-freq root |
| 30 | symmetry/twins | **C** | 16 pairs but **no null** (chance ≈ 6) — barely above |
| 25 | necessity (O11) | **C** | 78% via unique-root; instrument **misses Fātiḥa** (a keystone) |
| 20 | integration (O9) | **C−** | true but trivial (σ=1.0, near-complete graph) |
| 31 | development/two-classes | **C−** | the length gradient again |
| 13 | excretory | **C−** | speculative, no null |
| 29 | growth/Heaps | **C** | real but a universal law, not Qur'ān-specific (baseline) |
| 15 | endocrine slow-modulation | **F** | PC1 autocorr ≈ 0 — not found (refine) |
| —  | circulation (substance) (O8) | **F** | message clumps (z=+63), no perfusion (refine → recitation flow) |
| 27 | flow-direction | **F** | forward = backward entropy |
| 19 | lymphatic | **—** | untested |

## Meta-issues the re-scrutiny MUST address
1. **Redundancy — the ~18 "proven" are fewer INDEPENDENT signals.** homeostasis = flow-regulation; robustness =
   error-correction (rhyme); self-similar = scaling; integumentary = membrane; nervous-signal ≈ weave;
   identity/location/connectivity all lean on the same root-profile/keyness. **Estimated independent solid core:
   ~6–8**, not 18. Must de-duplicate before claiming a count.
2. **Missing nulls (C-grade gate):** digestive (12), symmetry (30), skeleton (16, length confound), development
   (31), excretory (13) were graded ✓/◑ **without a proper null** — re-run with one or demote.
3. **The length-gradient confound** recurs (location 2, development 31, skeleton 16): the muṣḥaf's rough
   long→short ordering can manufacture "structure." Control for verse-count everywhere.
4. **Effect sizes are mostly modest** (identity 1.5×, connectivity 44%, location t=5.9, error-correction 73/50).
   Only ~5 are large-and-clean (membrane, weave, flow-reg, rhythm, propagation, interface).

## SECOND-PASS RESULTS (2026-06-11, `second_pass.py`) — revisions
- **O2 location → DEMOTED C→F-ish.** Length alone R²=0.85; profile after removing length R²=**0.03**.
  "Location by wiring" is the **length gradient**, not organ-positioning. Headline claim retracted.
- **#12 digestive/reprocessing → KILLED.** real 593 < random 681 — trivial (any mid-freq root spans the corpus).
- **#30 symmetry/twins → CONFIRMED A−.** 16 adjacent pairs vs 5.6 random, z=+5.4.
- **#16 skeleton/muqaṭṭaʿāt → CONFIRMED B.** within-assoc z=+6.9 (null not strictly length-matched — mild caveat).
- **Length-gradient confound is now PROVEN load-bearing** (drove O2; drives #31 development). Every position/size
  claim must residualize length. **Still to do:** length-check O3 connectivity (adjacent suras ~ similar length).

## Revised solid core (after second pass)
**A (clean, independent, survived scrutiny):** O4 membrane · O5 internal weave · flow-regulation/rhythm ·
propagation/formulae · external-interface zones · symmetry/twins · skeleton/muqaṭṭaʿāt.
**B (real, modest, pending length-check):** O1 identity · O3 connectivity · O7 polarity(asym) · folding.
**OUT (demoted/killed this pass):** O2 location, digestive, development — confounded by length or trivial.
Estimated independent solid core: **~7**.

## THIRD-PASS RESULTS (2026-06-11, `third_pass.py`) — length-confound stress test
Neighbours ARE length-similar (adjacent length-gap 0.36 vs 1.71 random), so length had to be partialled out of
every relational claim:
- **O3 connectivity → SURVIVES (upgrade).** Length explains only 17% (r=+0.41); named twins stay top after
  residualizing length (113-114 100%, 2-3 100%, 8-9 97%; 105-106 1% = thematic, as expected).
- **Symmetry/twins → SURVIVES.** 14 pairs vs 5.7 on length-residual, z=+4.4.
- **Folding contact-decay → DEMOTED.** decay r=+0.32 → **−0.04** after length removed; it was a length artifact.
  (The network/community structure itself survives via O3 — only the "Hi-C folding curve" claim falls.)

## VALIDATED CORE after 3 passes (length-robust, proper-null, independent)
**A:** O4 membrane · O5 internal weave · O3 connectivity · symmetry/twins · propagation/formulae ·
external-interface zones · rhythm/flow-regulation · skeleton/muqaṭṭaʿāt.  **B:** O1 identity · O7 polarity.
**DEMOTED by length:** O2 location, folding-decay, development. **Killed/failed:** digestive, circulation-
substance, endocrine, flow-direction. **Independent solid core ≈ 8** (the A list), de-duplicated and length-safe.

## Preliminary bottom line
A genuine **solid core of ~6–8 independent, well-nulled correspondences** (membrane, internal weave,
flow-regulation, rhythm, propagation, external-interface, + likely identity & connectivity after de-confound).
The rest are moderate, redundant, missing-null, or failed. The body-as-benchmark holds at the structural level;
the catalog's *headline count* (~18) overstates it until de-duplicated and re-nulled.
