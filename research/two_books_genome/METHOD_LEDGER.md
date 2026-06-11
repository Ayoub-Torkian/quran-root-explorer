# METHOD LEDGER — mapping the two worlds (living record)

_Stage-1 objective (user): find the char→codon/amino-acid mapping that MAXIMIZES
similarity between the world of inscription (Qur'an/text) and the world of creation
(genome/proteome). Not Qur'an-specificity yet — get the method working for any text.
We run scenarios step by step, record every one here, and reconfigure on what the data says._

## Metrics recorded every step
1. **Similarity** of the best mapping's sequence to real protein/genome (the objective).
   Proxy now = −dipeptide-KL to real CCDS protein (lower KL = closer). Swap in BLAST/`tblastx`
   for fidelity to the paper — metrics below are objective-agnostic.
2. **Floor** = same pipeline on shuffled text + random strings (the non-zero baseline;
   "zero BLAST" is never reached). **Signal Δ = floor − real** (positive = real beats floor).
3. **Identifiability** (does a "correct mapping" exist?):
   - self-consistency = agreement of two independent searches on the SAME data,
   - cross-portion = agreement of best mappings on two DIFFERENT portions,
   - chance = agreement of two random mappings.
   A real, findable mapping ⇒ self-consistency → ~1, cross-portion ≈ self-consistency ≫ chance.

## Rate to objective (what we watch as scenarios scale)
Per step, track **Δ (signal)** and **self-consistency**. The program is "working/converging"
only if, as we scale M / change scenario, **Δ trends positive on held-out data AND
self-consistency climbs toward 1**. Flat Δ≈0 and self-consistency≈chance = the method is
fitting noise (no identifiable mapping) — itself a valid recorded result.

## Steps
| # | scenario (text · granularity · objective · M) | real KL | floor KL | Δ | self-consist | cross-portion | chance | read |
|---|---|---|---|---|---|---|---|---|
| 0 | full Qur'an · char→AA · dipeptide-proxy · M=800 random | 1.18 | 0.47 (rnd) / 1.01 (shuf) | **−0.71** | 0.10 | 0.03 | 0.06 | no signal; mapping unidentifiable |
| 1 | full Qur'an · char→AA · dipeptide · **SA 14k** | 0.534 | 0.097 | **−0.44** | 0.10 | 0.13 | 0.06 | real optimizer doesn't rescue it; pointing away + unidentifiable. RECONFIG: dipeptide objective is composition-biased (rewards randomness) |
| 2 | portion 2500 · char→AA · **5-mer match (BLAST-like)** · SA 8k | 99.96% | 100% | **−0.04%pt** | 0.13 | — | 0.05 | objective SATURATES — every text hits ~100% (proteome too dense in 5-mer space); floor at ceiling, no discrimination |
| 3 | portion 3000 · char→AA · **6-mer match (BLAST-seed)** · SA 8k | 99.9% | 100% | **−0.10%pt** | **0.55** | **0.03** | 0.06 | match SATURATES even at k=6 (3.8% coverage) — free mapping makes ANY text ~100%. self-consist HIGH (0.55), cross-portion AT CHANCE (0.03) on single portions. |
| 4 | **JOINT** map (3 portions) · k=6 · SA 5k | 99.2% | — | transfer **98.9%** vs floor 3.9% | 0.52 | **0.58** | 0.06 | APPARENT HIT: joint map transfers to held-out AND converges cross-set. Suspect composition → controls 5,6. |
| 5 | control: shuffled-Qur'an & English, joint pipeline | — | — | transfer ~99% (ALL) | — | shuf **0.065**, Eng **0.000** | 0.06 | TRANSFER = composition mirage (real/shuf/Eng all ~99%). But CONVERGENCE is order-specific: shuffle→chance, English→0; real Qur'an 0.58 SURVIVES. |
| 6 | control: **RANDOM target** (genome replaced), real Qur'an | — | — | transfer **3.5%** (collapsed) | — | **0.032** | 0.06 | Convergence COLLAPSES to chance with a random target ⇒ the **real proteome structure is necessary**. Signal survived shuffle + English + random-target. **First non-null lead.** NOT yet a finding — see controls below. |

| 7 | **REPLICATION** (5 disjoint pairs each) + synthetic-repeat control + letter-dissection | — | — | — | — | real+prot **0.22±0.13**; shuf+prot **0.22±0.16** (z=0.00); real+rand 0.03; synth-repeat 0.05 | 0.055 | **CANDIDATE REFUTED.** The 0.58 was a single-pair fluke (replicated mean 0.22, range 0.03–0.39). real ≈ shuffled (z=0.00) ⇒ NO order signal. Residual ~0.22 is COMPOSITION (frequent letters 0.31 vs rare 0.14), proteome-compositional pull only (z=3.05 vs random just reflects that bias). Robust null. |

| 8 | **Route 2: codon-level** (char→codon, 64) · convergence **replicated** 4 pairs · composition-control = freq-matched random (Qur'an NEVER rearranged; files read-only) | — | — | — | — | real **0.048±0.048**; control **0.048±0.036** (z=0.00) | 0.012 | NULL. Codon-level granularity changes nothing; real = composition control. Final config — program complete. |

| BLAST | **Faithful tblastx vs CCDS** (paper's objective) · N=20 × 6 short sūras · local BLAST+ 2.17 | — | — | real bits mean **32.9**/max 50.6 vs ctrl mean **32.2**/max 43.2; **Δmean 0.74** | — | — | — | NULL. Real ≈ control; bit-scores in the low/chance band; max diff is a single unreplicated outlier. The paper's own objective agrees with Steps 0–8, Route B, and folding. **Loop closed.** |

| PC | **POSITIVE CONTROL v1 (mis-specified)** · planted bijection cipher into real protein, scored vs REAL-genome model · bijection swap-SA + trigram | — | — | — | — | planted recovery **0.30**; ≈ floor 0.263 ≈ Qur'an 0.275; chance 0.048 | 0.048 | Conflated two things (planted into flat target, scored vs a different flat model). Re-specified → PC2. Kept for the record. |

| PC2 | **POSITIVE CONTROL v2 (correct, decisive — resolves M1+M2)** · plant cipher into LANGUAGE-structured text (Arabic letters), score vs that text's OWN trigram model · bijection swap-SA, 2 disjoint halves | — | — | — | **1.000** (recovery & cross-portion both) | **1.000** | 0.032 | **INSTRUMENT VALIDATED.** Recovers a planted cipher 100% and two independent halves agree 100% on language-structured text. ⇒ the convergence machinery is correct; the Steps 0–8 / BLAST nulls are NOT a search-power artifact. The earlier "weak recovery" was the **flat target** (C1), which is a GENOME (target-side) property — so it bounds EVERY forward text→genome substitution map regardless of Word-side granularity (letters, roots, …). M1 (can it say yes?) → YES on a true signal; M2 (is the null search-weakness?) → NO, it's the data. |

| SCN | **Scenario triage (SCENARIO_MATRIX.md)** · identifiability measured on corpus | — | — | — | — | 1-char 31 units/ratio 10668; 2-char 867/191; 3-char 11,260/~10 (½ hapax) | — | 3-char→codon = **TRAP** (params≫data, Bible-Code amplified). Salvage = **root→codon/AA** (closed ~1.6k vocab). Viable set collapses to {root-map, unit→gene+prior, structural battery}. Recommend root-map + planted-root positive control. |

| R1 | **ROOT-level mapping** (salvaged 3-char) · roots from Book6.xlsx (51,044 tokens, **1,702 roots**, ratio 30 — escapes C2) · (A) planted-root cipher PC, (B) real root→codon vs genome, 5 disjoint pairs + shuffled floor | — | — | **Δ −0.001** | (A) recovery **0.867**, cross-portion **0.567** | (B) real **0.015**±0.004 vs floor **0.016** | (A) 0.033 / (B) 0.017 | **(A) instrument FIRES at root granularity** (recovery/convergence ≫ chance). **(B) NULL** — real ≈ floor ≈ chance. Root granularity does **not** rescue the mapping: confirms C1 (flat genome target is **target-side**, granularity-independent) with a validated instrument. The salvaged 3-char idea is **exhausted → null.** Forward text→genome substitution program now closed across granularities {letter, codon, root}. |

### ⚑ Candidate signal (Steps 4–6) — status: **REFUTED by replication (Step 7)**
The order-dependent convergence (real 0.58 vs shuffled 0.065) did NOT survive replication: over
5 disjoint pairs, real ≈ shuffled (both 0.22±0.13, z=0.00). The 0.58 was a single-pair fluke;
the residual ~0.22 is a composition effect carried by frequent letters, not order, not meaning.
Lesson recorded: signals can survive single-pair controls and still die under replication — n=1
is never enough. Original note kept below for the record.
The Qur'an's joint char→AA map **converges across disjoint portions (0.58 ≫ chance)** only when
(a) word ORDER is intact and (b) the target is the REAL proteome. Prime remaining (mundane)
explanation: repetitive/low-complexity structure in the Qur'an (Arabic morphology + formulaic
repetition) is statistically compatible with the proteome's low-complexity 6-mer structure —
possibly generic to repetitive text, not Qur'an-special or meaningful. **Required controls before any claim:**
(1) non-Qur'an Arabic prose/poetry — Qur'an-specific vs Arabic-general; (2) a synthetic highly-
repetitive text — is it just repetition × structured target; (3) replication across MANY portion
pairs + seeds with a significance test; (4) dissect WHICH letters converge (frequent only = weak).

(Append one row per step via `scripts/method_step.py`, which writes `scripts/ledger.json`.)

## Decision protocol (LOCKED, 2026-06-09)
At every juncture: present **3–5 routes** with critical pros/cons, then **recommend ONE**,
justified against the multivariable context (compute = CPU, no GPU; NCBI BLAST API
unreliable; harness uses fast per-eval objectives for SA) and what the ledger already shows.

## Reconfiguration policy (data-driven)
- If a scenario pushes **Δ > 0 on a held-out portion AND raises self-consistency**, keep that
  configuration and build on it.
- If not, log it and move to the next scenario. No tuning toward Δ on the same data the search
  saw (that is overfitting).
- Pre-declare the scenario order (by length, then granularity, then objective) before running,
  so we are not cherry-picking.

## Scenario backlog (to run, in order)
1. Scale M (800 → 5k → 50k) / switch to simulated annealing — does self-consistency rise?
2. Granularity: char→AA vs char→codon (1 char) vs 2-char→codon.
3. Objective: swap proxy → real `blastn`/`tblastx` vs RefSeq (faithful to the paper).
4. Length × diversity ramp: short → long → multi-sūra → multi-text (Word end);
   human CDS → whole proteome → multi-species (Act end).
5. Held-out transfer: mapping found on portion A scored on portion B vs B's floor.

## Honest standing prior
Route B (mapping-invariant), six held-out nulls, non-folding, and step 0 (negative Δ +
unidentifiable) all point the same way. We proceed anyway to let the data — at larger M, the
real BLAST objective, and more scenarios — speak for itself, and we record whatever it says.
