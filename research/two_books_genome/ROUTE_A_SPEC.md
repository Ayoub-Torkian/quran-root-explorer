# ROUTE A — char→codon→protein, with a foldability benchmark (pre-registration)

_2026-06-08. Refines and supersedes the Route-A sketch in METHODOLOGY.md §1 by
adding the **predicted protein** (and its **foldability**) as the primary benchmark —
the user's "use the real codon→AA→ribosome→protein pipeline as a novel benchmark"
idea, made falsifiable. Read CHALLENGES.md first._

> **Gate:** Route B (RESULTS.md) found no shared structural class — so the honest prior
> is a calibrated null. Route A is run here as the *correct, falsifiable* form of the
> local-correspondence question, with a real benchmark and a symmetric null, NOT as an
> expectation of success.

---

## 0. Governing principle (agreed in discussion)

A *discovered* mapping is legitimate (the genetic code itself was discovered, not
pre-given) — but it becomes knowledge only by **out-of-sample prediction**, never by
in-sample fit. So: search the mapping on a TRAIN split, validate on a HELD-OUT split,
and require it to beat the *identical search* run on controls. The benchmark answers
"do we have an independent criterion?"; the controls answer "did we just fish for it?"

## 1. Hypothesis (falsifiable)

> Under a discovered char→codon mapping, Qur'anic text units translate (via the fixed
> genetic code) into proteins that are **more protein-like — primarily, more foldable —
> than the same Monte-Carlo search achieves on shuffled Qur'an, other-language texts,
> and random sequences**, and this **holds on a held-out split** of the Qur'an.

## 2. The mapping (the only free parameter)

- 28 Arabic consonantal letters → **distinct sense codons** (one-to-one; exclude the 3
  stop codons UAA/UAG/UGA so translation never truncates internally). Search space ≈
  61·60·…·34 ≈ 10⁴⁸. Monte Carlo samples it (the user's combinatorics solution — valid).
- **Note on the protein level:** since codon→amino-acid is fixed and degenerate, the
  *protein* depends only on the **induced char→AA map** (28 letters → ≤20 AAs). Distinct
  char→codon maps using synonymous codons give the *same* protein. So the effective
  protein-level search is ~20²⁸ ≈ 10³⁶ — still astronomical, but smaller than the DNA-
  level space, and this is the space the foldability benchmark actually probes. (The DNA-
  level char→codon map is retained only if also running blastn vs the genome.)

## 3. The fixed pipeline (zero freedom — the validated half)

char → codon → **standard genetic code** → amino acid → protein. This is the universal,
experimentally-established code (Nirenberg 1961); it is the "as-good-as-fixed" component
we build on. Each unit of N letters → an N-residue peptide.

## 4. Benchmarks / oracles (independent of the mapping search)

1. **Foldability (PRIMARY).** Predict structure with ESMFold/AlphaFold; score = mean
   pLDDT and fraction of residues in confident, well-packed secondary structure. Most
   random sequences do **not** fold — this is the strong, hard-to-fake oracle. It knows
   nothing about the mapping.
2. **Proteome match (secondary).** blastp / DIAMOND vs UniProt-SwissProt; score = best
   bit-score / −log10(e-value).
3. **Protein-likeness (cheap, tertiary).** AA-composition distance to the proteome,
   hydrophobicity patterning, predicted secondary-structure content, low-complexity
   fraction.

## 4b. Benchmark calibration on known-answer REAL samples (do this FIRST)

Before any mapping search, validate the benchmark on real data from **both ends** —
the "Act" (real proteins) and the "Word" (real text) — so we know the oracle actually
discriminates. `scripts/route_a_calibration.py` does the CPU part (foldability/ESMFold
is the GPU confirmation; same idea, run on real proteins as a positive control).

Pilot run (2026-06-08), real human CDS translated to protein vs controls, length 1969:

| sample | compKL_unif | adj-residue MI | dipeptide-KL to real protein |
|---|---|---|---|
| ACT real protein | 0.141 | 0.030 | 0.000 (reference) |
| ACT shuffled | 0.141 | 0.024 | 0.767 |
| ACT random uniform | 0.013 | 0.008 | 2.163 |
| ACT random comp | 0.162 | 0.011 | 0.818 |
| WORD text→peptide (arbitrary map) | 0.320 | 0.420 | 2.777 |
| WORD shuffled | 0.320 | ~0 | 2.749 |

Reads: real proteins are separable — protein-specific dipeptide bias (KL≈0) that shuffling
destroys (KL→0.77). A naive text→peptide lands *farthest* from real protein (KL 2.78):
it has strong order, but **language order, not protein order**. Positive controls (real
proteins) and negative controls (shuffled/random) behave correctly, so the proxy is a
valid pre-filter. **ESMFold calibration:** confirm real proteins score high pLDDT and
shuffled/random score low — establishes the foldability threshold on known answers before
judging any Qur'an-derived peptide.

(Caveat: the WORD row above uses ONE arbitrary map — it is a baseline, not the search
result. Route A's question is whether the MC *search* closes that gap, and whether it
closes it more for the Qur'an than for the control battery.)

## 5. Two-stage compute (this is what makes folding feasible)

ESMFold is seconds–minutes/protein on GPU — you CANNOT fold 10⁴–10⁶ candidate mappings.
So:

- **Stage 1 — cheap MC search (CPU, offline).** Objective = a **pre-declared cheap proxy**
  (DIAMOND bit-score vs SwissProt, and/or a fast protein-likeness composite). Run M
  sampled mappings; keep the top finalists. The proxy MUST be fixed before running.
- **Stage 2 — expensive confirmation (GPU).** Fold ONLY the finalists with ESMFold:
  the Qur'an's best mapping, each control's best mapping, and the held-out evaluation set.
  Dozens–hundreds of proteins total — GPU-feasible.

Controls get the **identical** two-stage treatment (same proxy, same M, same ESMFold
confirmation), so the comparison stays symmetric.

## 6. Null battery (mandatory, symmetric — run the SAME search on each)

- (a) **shuffled Qur'an** — same letters, broken order (isolates order).
- (b) **other-language texts** — Homer, Cervantes, etc. (is the Qur'an special, or is this
  generic to language? — given Route B, expect generic).
- (c) **random sequences** — matched to Qur'an letter composition.
Qur'an's best finalist (proxy and ESMFold) must exceed the distribution of each control's
best finalist. Beating none/some but not all ⇒ no result.

## 7. Train / held-out validation (the out-of-sample requirement)

Split Qur'an units into TRAIN and TEST before anything. Search the mapping on TRAIN only;
freeze it; report foldability/match on the untouched TEST set, vs controls treated the
same way. A mapping that does not transfer to held-out text is overfit — rejected.

## 8. Units & length

Multi-ayah blocks / short suras giving **≥50-residue** peptides (folding needs length;
single roots/short ayahs are too short and are excluded from the folding track, kept only
as a short-peptide / blastp-only side analysis).

## 9. Expression / context slots (pre-specified — the user's "context" idea, made safe)

Context-dependence is allowed but the contexts must be **enumerated in advance**
(e.g., normalization scheme, unit grouping, declared thematic subsets) and the family
corrected for. No post-hoc "wrong context" rescue of a null — that is the unfalsifiability
trap from CHALLENGES.md.

## 10. Multiplicity & robustness

Max-statistic null absorbs the mapping search. Correct across any pre-declared contexts /
tracks (folding, blastp, blastn). Robustness: ≥2 seeds, ≥2 values of M, ≥1 alternate
normalization. Report all.

## 11. Compute scoping — offline CPU vs GPU

| Component | Where | Notes |
|---|---|---|
| char→codon MC sampling, translation | CPU, offline | cheap; parallelize |
| Stage-1 proxy: DIAMOND vs SwissProt | CPU, offline | DIAMOND is fast; SwissProt ~570k seqs |
| Stage-1 proxy: protein-likeness stats | CPU, offline | composition, hydrophobicity, low-complexity |
| Control-search bookkeeping, null, FDR | CPU, offline | the whole symmetric battery |
| **Stage-2: ESMFold/AlphaFold folding** | **GPU** | finalists only (Qur'an + controls + held-out); dozens–hundreds of proteins |
| blastp confirmation of finalists | CPU | NCBI BLAST+ or DIAMOND --sensitive |
| Databases to fetch once | CPU | SwissProt (UniProt), ESMFold weights |

Practical: everything except the folding oracle runs on a normal machine offline. The
GPU step is bounded and small because it only ever sees finalists, never the search space.

## 12. Verdict table

- **Positive:** Qur'an finalists fold (pLDDT) and/or blastp-match **above all three control
  batteries**, transfers to the **held-out** split, survives robustness, with multiplicity
  correction. → A real, surprising, defensible result; still correlational, but the
  foldability oracle makes it hard to dismiss as a string coincidence.
- **Beats random but not shuffled/other-text:** generic / artifact. → Null for the thesis.
- **Null:** does not beat the battery. → The finding (expected per the gate); reportable.

## 13. Honest prior

Route B says language and genome are structurally different, and a substitution preserves
the text's (language-like, not protein-like) order statistics — so the predicted proteins
are *a priori* less likely to fold than real proteins, and the most probable outcome is a
calibrated null. We run it anyway because (a) foldability is a strong, modern, independent
benchmark that a null here would meaningfully establish, and (b) it is the correct,
falsifiable form of the local-correspondence question — the opposite of the Bible-Code
error, which never ran the controls.
