# RESULTS — Route B (structural comparison), first real run

_2026-06-08. Full corpora. Mapping-free. This is the study's first well-powered
finding. **A null was a possible successful outcome, and that is what we got.**_

## Data
- **Genome:** full Consensus CDS (CCDS) — 35,624 sequences, 62,284,229 nt.
- **Language:** Arabic Qur'an (parsquran.com), 6,236 verses → 329,141 consonantal
  letters (diacritics stripped, 28-letter skeleton).
- Engine: `scripts/run_pipeline.py` / `route_b_confirm.py`, chunkLen = 2000,
  95% CIs across non-overlapping chunks. `pipeline_results.json`.

## Table (mean ± 95% CI)
| sequence | N | chunks | gzip | Hurst (DFA) | MI-decay γ |
|---|---|---|---|---|---|
| CDS_real | 62.3M | 31,142 | 0.321±0.000 | **0.543±0.001** | **0.915±0.006** |
| CDS_shuffled | 62.3M | 31,142 | 0.344±0.000 | 0.502±0.000 | 0.001±0.012 |
| Quran_arabic | 329k | 164 | 0.341±0.002 | **0.479±0.006** | **2.285±0.107** |
| Quran_shuffled | 329k | 164 | 0.403±0.001 | 0.498±0.005 | nan (no MI to fit) |

## Reading
1. **Controls valid.** Every shuffle loses its structure: gzip rises, Hurst → ~0.50,
   MI collapses (genome MI-γ 0.915 → 0.001; Qur'an MI degenerates entirely). The
   pipeline is measuring real structure, not artifacts.
2. **No shared long-range structure — strong, well-powered null.**
   - Hurst: genome **0.543** (long-range *persistent*) vs Qur'an **0.479**
     (non-persistent, ~uncorrelated/slightly anti-persistent). Non-overlapping CIs,
     opposite sides of 0.5.
   - MI-decay γ: genome **0.915** (slow decay = long memory) vs Qur'an **2.285**
     (fast decay = short memory). Genome correlations reach ~2.5× farther.
   - Both texts are clearly non-random (vs their shuffles), but their structural
     signatures are **different — arguably opposite**.

## Caveats (so the null is not oversold)
- The DFA-binary Hurst estimator under-detects language long-range correlation (it
  read ~0.50 for English in the pilot too). Lean on **MI-γ**, which is label-invariant
  and decisive here.
- Cross-alphabet exponent comparison (4 vs ~28 symbols) carries some confound; the
  *direction* (genome = longer memory) is robust and matches known DNA long-range-
  correlation literature (coding DNA still shows persistence; natural text decays faster).
- One structural lens at scales up to chunkLen 2000 / MI distance ~21. A pre-specified
  alternative encoding/scale could be tested — but only as a *pre-registered* follow-up,
  not a fishing expedition.

## Decision (per the pre-registered gate)
Route B was the **gate** for Route A. Route B shows **no shared structure**, so the
searched letter→codon BLAST test (Route A) — which carries the Bible-Code risk — is
**NOT justified** and should not be run. We tested the strongest honest form of the
"two books share structure" hypothesis and it came out negative, cleanly.

This is consistent with the app's ethos (most lenses are honestly null) and with the
honest prior recorded in CHALLENGES.md. The finding is reportable as-is.

## Multi-language replication (2026-06-08) — the null becomes a positive finding

Re-ran with 8 languages across 5 families (chunkLen=2000). Decisive measure = MI-decay γ
(lower = longer-range memory). All shuffles collapsed (controls valid).

| corpus | family | N | MI-γ | Hurst |
|---|---|---|---|---|
| **Human genome (CDS)** | — | 62.3M | **0.915 ± 0.006** | 0.543 |
| Finnish (Kalevala) | Finno-Ugric | 453k | 1.393 ± 0.045 | 0.506 |
| Spanish (Quijote) | Romance | 1.65M | 1.929 ± 0.031 | 0.453 |
| German (Kafka) | Germanic | 99k | 1.932 ± 0.130 | 0.487 |
| English (Moby-Dick) | Germanic | 955k | 2.249 ± 0.052 | 0.472 |
| **Arabic (Qur'an)** | Semitic | 329k | 2.285 ± 0.107 | 0.479 |
| French (Les Misérables) | Romance | 2.0M | 2.295 ± 0.037 | 0.479 |
| English (Pride) | Germanic | 564k | 2.336 ± 0.069 | 0.469 |
| Greek (Iliad) | Hellenic | 854k | 2.486 ± 0.059 | 0.483 |

**Finding (well-powered, replicated):** human language is a tight structural class —
every tested language (5 families, incl. Semitic) decays fast, γ ≈ 1.4–2.5. The human
coding genome is a sharp outlier at γ ≈ 0.92, below *every* language; the nearest
(Finnish) is 0.48 away with non-overlapping CIs. **The genome carries longer-range
statistical memory than any human language.** The Qur'an sits squarely inside the
language cluster (γ≈2.29) — it shares the genome's structure no more than Homer or
Cervantes does. That is the direct empirical answer to the original question.

Nuance: Finnish (agglutinative, long words) shows the longest language memory (γ≈1.39),
still far from the genome — a sensible morphology effect, not a confound. Alphabet-size
(4 vs ~26–30) cannot explain a result that is unanimous across 8 diverse scripts.

**Upgraded decision.** This is now a positive, citable result about a *measurable
structural difference* between the two books — not merely "no shared cipher". It
reinforces, with replication, that Route A (the searched letter→codon BLAST) must not
be run: there is no shared structural class to encode.

## Mapping-search program (Steps 0–8) — robust null + a caught false positive

After Route B, we directly pursued the stage-1 objective: find a char→codon/AA mapping that
maximizes Qur'ān↔genome similarity, via frequency-weighted Monte-Carlo + **simulated-annealing**
search, scored by three objectives (dipeptide-KL, protein-Markov likelihood, BLAST-seed k-mer
match) against the real human proteome (CCDS). Full per-step log: `METHOD_LEDGER.md`. Outcome:

- **Raw "similarity" is uninformative.** A free mapping (31 letters → 20 AA / 64 codons) makes
  *any* text ~100% match (saturation); the floor (random/shuffled) sits at the ceiling, so the
  signal-over-floor ≈ 0 for every objective tried.
- **The operational test for "does a correct mapping exist" = convergence** of independently
  optimized maps across disjoint portions. One pair gave a striking 0.58 (chance 0.056) that
  survived shuffle, English, and random-target controls — a real candidate.
- **Replication killed it.** Over 5 disjoint pairs, real Qur'ān 0.22±0.13 = shuffled 0.22±0.16
  (z = 0.00). The order-dependence was a single-pair fluke; the residual ~0.22 is a composition
  effect carried by frequent letters (0.31 vs 0.14 rare) — not order, not meaning, not Qur'ān-specific.
- **Codon-level** (char→codon, 64) replicated: real = composition control (z = 0.00).

**Conclusion:** no identifiable, generalizing char→codon/AA mapping exists under any objective tried —
consistent with Route B (mapping-invariance) and the folding null. **Methodological centerpiece for
the write-up:** a signal that survived single-pair controls yet dissolved under replication — n=1 is
never enough. (No Qur'ān text was ever altered; composition controls are frequency-matched random
sequences, and all Qur'ān files are read-only.)

## Hardening (2026-06-09): significance + alphabet-size control (referee M4)

Two checks that turn the structural contrast from "eyeballed CIs" into a defended result.

**Significance of the genome's separation.** Across the 8 languages, MI-γ = 2.113 ± 0.350
(mean ± sd); the genome's 0.915 is an outlier at **z = −3.43, one-sided p ≈ 3.0×10⁻⁴**, and is
the **minimum of all 9 corpora** (rank-based p = 1/9 = 0.11; the parametric and gap-based evidence
is far stronger than rank alone). The genome's longer-range memory is not a borderline effect.

**Alphabet-size confound — refuted.** MI-γ compares a 4-symbol genome with ~28-symbol scripts, so
a skeptic asks whether the smaller alphabet alone explains the lower γ. We recomputed γ at matched
alphabet sizes (kernel is relabeling-agnostic):

| recoding | alphabet | MI-γ | reading |
|---|---|---|---|
| genome, nucleotides | 4 | **0.888 ± 0.045** | long memory (baseline) |
| genome, **codons** | 64 | **0.273 ± 0.161** | *even longer* memory at larger alphabet |
| English (Moby-Dick), letters | ~26 | 2.254 ± 0.054 | short memory |
| English, **recoded to 4 symbols** | 4 | **1.752 ± 0.064** | still short memory |

At a *matched* 4-symbol alphabet the gap persists (genome 0.888 vs English-4 1.75; Δ ≈ 0.86), and
enlarging the genome's alphabet to 64 codons pushes γ *down* (0.273), the opposite of an
alphabet-size artifact. **The genome's long-range memory is real structure, not a symbol-count
effect** — the cross-alphabet objection (referee M4) does not hold.
Script: `scripts/` matched-alphabet recompute; kernel `route_b_confirm.py`.

## If you want to keep going (honest options, not fishing)
- **Strengthen the language estimator:** word-level / rank series DFA, or wavelet
  long-range estimators, to confirm the Hurst reading isn't an estimator artifact.
- **Pre-register one** alternative scale or encoding and test it once — accept the result.
- **Replicate across languages** (English, Latin, etc.): does language *as a class*
  sit apart from the genome? If all languages decay fast and the genome slow, the null
  is a positive finding about a real difference between the two "books".
