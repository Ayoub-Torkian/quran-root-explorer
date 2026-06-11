# Two Books — program summary (the whole arc, one page)

_The authoritative map of the investigation: what we asked, how we tested it without fooling
ourselves, what the data said, what is closed, and the one direction now open. Last updated
2026-06-09._

## The question

Is there a sequence-level correspondence between a text (the Qur'ān, or any language) and the human
genome/proteome — a char/unit → codon/amino-acid mapping that makes the "word" and the "act" line
up better than chance? And can such a claim be tested rigorously rather than asserted (the Bible-
Code failure mode) or dismissed?

## The framework (the real contribution)

Treat any proposed mapping as a *tested output, never an assumed input*, and require **six controls**
plus a mapping-invariant pre-check:

0. **Structural pre-check** (relabeling-invariant): if the two domains differ on label-invariant
   structure, *no* mapping can reconcile them — refute the whole class before searching.
1. **Floor**: identical pipeline on shuffled/random inputs; only margin-over-floor counts.
2. **Out-of-sample transfer**: fit on one portion, test on unseen.
3. **Convergence**: do independently-optimized maps agree? — the operational test of "a correct
   mapping exists."
4. **Replication + significance**: many disjoint pairs/seeds (a single instance can fool you).
5. **Multiplicity**: hold across objectives, granularities, scenarios.
6. **Planted positive control**: prove the instrument recovers a *known* mapping — else a null is
   uninterpretable (it might just be a weak search).

## What the data said — every line agrees (null)

| test | result | verdict |
|---|---|---|
| Structural γ (genome vs 8 languages) | genome 0.92 vs language 1.4–2.5; outlier z=−3.43, p≈3e-4 | no shared structure |
| Alphabet-size control (referee M4) | matched 4-sym: genome 0.89 vs Eng-4 1.75; codon-64: 0.27 | not an artifact |
| Mapping search (letter→AA/codon) | saturates; Δ-over-floor ≈ 0 | similarity uninformative |
| Convergence false positive | 0.58 single pair → **0.22 = shuffled 0.22 (z=0)** on replication | fluke (composition) |
| Folding (ESMFold) | pLDDT 34–50, pTM 0.15–0.30 | proteins don't fold |
| Faithful tblastx vs CCDS | real 32.9 ≈ control 32.2 | null |
| **Positive control** | cipher recovery **1.00** (letters), **0.87** (roots) | **instrument validated** |
| Root→codon (salvaged 3-char) | convergence 0.015 ≈ floor 0.016 ≈ chance | null |

**Bottom line:** the forward text→genome substitution program is **closed** across all three sensible
granularities (letter, codon, root), with a *validated* instrument. The decisive insight: the
genome is statistically **flat** at low n-gram orders — a *target-side* property — so no mapping of
any source granularity can be identifiable. The nulls are real signal-absence, not weak search.

## What we deliberately did NOT do

Whole-unit→gene correspondence (sūra/root/ayah → gene) was scoped and **declined**: the 10⁶–10⁸
pairing space needs an independent mechanistic prior to control multiplicity, and none exists; every
prior we could invent reintroduces the exact Bible-Code degrees of freedom the framework removes
(`GENE_PRIOR_SCOPING.md`).

## What is now open (the one direction with a non-flat target)

**Language ↔ neural code** (`../neural_coding/`). Real mechanism, mature literature, and a target
that carries structured signal — so a positive result is attainable. Progress so far:
(i) harness validated on a simulation (positive control = clean double dissociation);
(ii) **first real-fMRI result** — speech acoustic envelope predicts cross-run BOLD on Narratives
"Pieman"; (iii) **replicated and formally significant across 14 subjects** (`encoding_multi.py`): 14/14
envelope > phase-shuffled floor, ~33% of ceiling, t-test p = 4.2×10⁻⁵, dz = 1.61 — but a stronger
**specificity control** (`encoding_specificity.py`) shows the effect is **real yet NOT
stimulus-specific** (a different story's envelope predicts equally, p = 0.49): generic speech tracking,
not content-specific encoding. Our own control narrowed our own positive. (iv) **step 2 (semantic arm)** via variance partitioning (Whisper word timings + GloVe), hardened to
14 subjects: semantic-unique is a **robust significant null** (13/14 below floor, t-test p=2e-4, dz=−1.35)
— with full power, meaning adds nothing beyond acoustics on whole-brain raw data. Same instrument, same
14 subjects: acoustic **positive** dz=+1.6, semantic **null** dz=−1.4 — opposite verdicts, both trusted. The *same* six-control
discipline that returned null on the flat genome returns a **replicated positive** (acoustic) and
correctly a **null** (semantic-unique, at this data quality) here — separating real from spurious on
real brain data. (v) **step 3 (auditory-vs-language dissociation)** built and run end-to-end across 3 iterations
(ANTsPy SyN registration + Harvard-Oxford ROIs + reliable-voxel selection, py3.11 env). ROI
reliability improved 0.018 → 0.12, but the encoding R² stayed at noise level → **INCONCLUSIVE on raw
single-subject data.** A v1 "dissociation=True" flag was a thin false positive our reliability/margin
gate rejects; we then declined to swap features to force a positive (that would be fishing). A
trustworthy dissociation needs fMRIPrep + multiple subjects — the gate is data quality and design,
not code. The discipline that killed the genome fluke also refuses this one.
The genome→language link is developmental/evolutionary, **not** a sequence bridge — that limb stays
rejected.

## Deliverable index

**Write-up:** `MANUSCRIPT_DRAFT.md` (methods/perspective preprint, 6 figures), `MANUSCRIPT.md`
(index + status log), `REFEREE_NOTES.md` (internal review). **Compiled PDFs:**
`Genome_Framework_Torkian.pdf` (8 pp, figs F1–F6) and `../neural_coding/Neural_Pilot_Torkian.pdf`
(6 pp, figs N1–N6); print sources `*_print.md`.
**Evidence & design:** `METHOD_LEDGER.md` (per-step ledger), `RESULTS.md` (structural + hardening),
`SCENARIO_MATRIX.md` (exhaustive triage), `METHODOLOGY.md`, `CHALLENGES.md`, `SCENARIOS.md`,
`PIPELINE.md`, `GENE_PRIOR_SCOPING.md`, `NEURAL_CODING_SCOPING.md`.
**Key scripts:** `positive_control_cipher.py`, `root_map_test.py`, `extract_roots.py`,
`matched_alphabet.py`, `run_blast.py`, `build_figures.py`; neural: `../neural_coding/encoding_sim.py`,
`encoding_real.py`.
**Figures:** `figures/F1`–`F6`; `../neural_coding/figures/N1`.

## Status & recommended next action

The genome methods/perspective paper is **content-complete** and every referee objection I could
raise is answered in-file. Two honest options: **(a) finalize for a preprint** (export to PDF/LaTeX,
pick a venue), or **(b) take the neural-coding step** (run `encoding_real.py` on one subject). They
are independent; (a) closes a finished result, (b) opens the one direction that can still go
positive. Recommended order: do (a) — lock the finished result — then (b).
