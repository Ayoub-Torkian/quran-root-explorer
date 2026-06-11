# MANUSCRIPT (living draft + support-data index)

_Working title:_ **A molecular-biology data-mining framework for mapping Qur'anic
letter sequences to the genome/proteome — method, controls, and findings.**
_Lead/author:_ A. Torkian (torkian@sharif.edu). _Assembled with assistance; author owns it._

> **Honest target note.** Aim high, but the manuscript's strength = its controls. A
> *positive* result is only publishable (anywhere, let alone a top venue) if it survives
> the floor, held-out, convergence, and multiplicity checks below — those ARE the referee's
> first questions. A rigorous *null* is a valid contribution at an appropriate venue. We
> collect support data so EITHER outcome is fully defensible.

## Abstract (fill from results)
[one paragraph: claim · method (freq-weighted MC/annealing mapping + BLAST/proxy) · the
control framework · headline result (Δ-over-floor, convergence) · interpretation].

## 1. Introduction
Two books (Word=Qur'an, Act=genome); the falsifiable claim (a char→codon/AA mapping);
why naive maximize-match is the Bible-Code trap; the design that avoids it.
→ source: METHODOLOGY.md, CHALLENGES.md (pre-registration, timestamped).

## 2. Methods
- **Corpora & provenance** (see index below): Qur'an text (parsquran.com), human coding
  genome (NCBI CCDS), control texts (Project Gutenberg).
- **Mapping generation**: frequency-weighted Monte-Carlo; **simulated-annealing** optimizer
  for the 64^L space (pure random sampling cannot search it). Knobs pre-declared per step:
  injective vs many-to-one; direction (→64 codons / →20 AA); M / annealing schedule.
- **Objective**: BLAST/`tblastx` similarity vs RefSeq (paper-faithful) and a CPU proxy
  (−dipeptide-KL to real protein) for speed. Hook in `scripts/method_step.py`.
- **The control framework (the core)**: (i) **Floor** = identical pipeline on shuffled +
  random inputs; report Δ = floor − real. (ii) **Held-out transfer**: mapping from portion A
  scored on unseen portion B vs B's floor. (iii) **Convergence/identifiability**: agreement
  of independent best mappings (self-consistency, cross-portion) vs chance. (iv) **Multiplicity**:
  FDR/family-wise correction across all scenarios. (v) **Robustness**: ≥2 seeds, ≥2 M.

## 3. Results (fed live by the ledger)
- Route B — replicated structural contrast (genome vs 8 languages): RESULTS.md.
- Folding capstone (ESMFold, Al-Ikhlas/An-Nas pLDDT 34–50): MONITOR.md.
- Mapping-search steps (Δ-over-floor, convergence per step): **scripts/ledger.json** + METHOD_LEDGER.md.
- [tables/figures auto-built from ledger as steps accumulate].

## 4. Discussion / 5. Conclusion
[interpretation; mapping-invariance argument; scope = sequence cipher, not theology].

## Figures (to assemble)
F1 language-vs-genome γ contrast · F2 the pipeline · F3 Δ-over-floor trajectory (rate to
objective) · F4 convergence (self-consistency vs chance) · F5 folding pLDDT vs controls.

## Data & code availability / Reproducibility
- Qur'an: parsquran.com (fetch_parsquran.py) → 6236 verses.
- Genome: NCBI CCDS `CCDS_nucleotide.current.fna.gz` (fetch_refseq_cds.py), 35,624 CDS.
- Languages: Project Gutenberg IDs in fetch_languages.py.
- All scripts in scripts/; every run logs config + **seed** + timestamp to ledger.json.
- Pre-registration: METHODOLOGY.md, CHALLENGES.md (committed, timestamped in git history).

## Support-data index (what's collected, where) — keep current
| item | location | status |
|---|---|---|
| Pre-registration & guardrails | METHODOLOGY.md, CHALLENGES.md, SCENARIOS.md | ✓ |
| Route B structural result + data | RESULTS.md, scripts/results_*.json | ✓ |
| Folding capstone + numbers | MONITOR.md (+ Colab pLDDT) | ✓ |
| Mapping-step results (provenance) | scripts/ledger.json, METHOD_LEDGER.md | accruing |
| Generated proteins | generated_proteins/ (gitignored, local) | ✓ |
| Corpora provenance + fetch scripts | data/README.md, scripts/fetch_*.py | ✓ |
| Narrative / history of decisions | JOURNEY.md, IDEATION_LOG.md | ✓ |

## Status log
- 2026-06-09: scaffold created; harness (method_step.py) + ledger live; step 0 baseline logged.
- 2026-06-09: mapping-search program run, Steps 0–8 (SA engine added). Three objectives
  (dipeptide-KL, protein-Markov, BLAST-seed k-mer), char→AA and char→codon. **Robust null.**
  A single-pair convergence of 0.58 survived shuffle/English/random-target controls but was
  **refuted by replication** (real 0.22 = shuffled 0.22, z=0.00); residual is composition.
  Program complete; centerpiece = the replication-killed-the-fluke cautionary result.
- 2026-06-09: **MANUSCRIPT_DRAFT.md reshaped into methods/perspective framing** (framework first,
  Qur'ān↔genome as worked example, replication-killed-the-fluke as centerpiece). Added figure
  captions (F1–F5 tied to real numbers) and a reference list (Witztum/McKay, Peng, ESMFold/AlphaFold,
  BLAST, CCDS). Draft is now a complete standalone preprint draft.
- 2026-06-09: built figures F1–F5 as images (build_figures.py); internal referee pass
  (REFEREE_NOTES.md, verdict: major revision, key gap = no positive control).
- 2026-06-09: **resolved the referee's central gap.** Positive control v1 (planted into flat
  protein) recovered poorly → re-specified as v2 (cipher into language-structured text, scored vs
  its own model): **recovery 1.00, convergence 1.00** (positive_control_cipher.py). Instrument
  validated; the genome nulls are a **target-side flatness** ceiling (C1), not weak search.
- 2026-06-09: **exhaustive scenario triage** (SCENARIO_MATRIX.md). 3-char→codon = unidentifiable
  trap; salvage = root-level. **R1 root→codon** run (root_map_test.py): planted-root PC fires
  (0.87/0.57), real root→codon = null (0.015 ≈ floor). Forward text→genome program **closed across
  letter/codon/root** with a validated instrument.
- 2026-06-09: **structural battery hardened** — genome γ outlier z=−3.43 (p≈3e-4); cross-alphabet
  confound (referee M4) refuted via matched 4-symbol & 64-codon recodings (matched_alphabet.py).
- 2026-06-09: **whole-unit→gene scoped and declined** (GENE_PRIOR_SCOPING.md): no defensible
  independent prior exists; any constructed prior reintroduces Bible-Code DOF.
- 2026-06-09: **manuscript finalized** — control (6) positive control added; §3.2b instrument
  validation + flat-target ceiling; §3.6 granularity (root); §3.1 alphabet-size control; F6 added;
  scope note declining unit→gene; conclusion = program closed across granularities.
- **Status: content-complete preprint draft.** Remaining = optional venue formatting (e.g.,
  export to PDF/LaTeX) and, if desired, the language↔neural-coding pivot (NEURAL_CODING_SCOPING.md).
