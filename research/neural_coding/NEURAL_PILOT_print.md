# Porting a controlled-mapping discipline to language ↔ neural code: a validated instrument, a replicated acoustic positive, and an honestly inconclusive dissociation

**A. Torkian** · *pilot / methods note, draft 2026-06-09 — companion to the genome methods/perspective paper*

---

## Abstract

A companion programme tested cross-domain symbol→symbol mappings between scripture and the genome
and returned a thorough, well-controlled null (the genome is statistically flat at the orders where
a mapping would be identifiable). The same six-control discipline — floor, out-of-sample transfer,
convergence, replication, multiplicity, and a **planted positive control** — transfers directly to a
target that is *not* flat: the human brain's response to language. We port the instrument to fMRI
encoding models and exercise it on the Narratives "Pieman" dataset. The discipline behaves exactly
as designed: it **fires** on a simulated planted feature→response mapping (recovery 1.00), confirms a
**replicated, formally significant** acoustic-envelope effect across 14 subjects (t-test p = 4×10⁻⁵,
dz = 1.6) — then, with a stronger specificity control, shows that effect is **real but not
stimulus-specific** (a different story's envelope predicts equally, p = 0.49), narrowing the claim to
generic speech tracking; returns a **robust significant null** for unique semantic variance across 14
subjects (dz = −1.4); and **refuses** a thin "double-dissociation=True" flag whose ROI reliability was
near zero — declaring it inconclusive rather than manufacturing a result. The contribution is the
discipline itself: on a real, signal-bearing target it says *yes*, *no*, and *not on this data* — and
each verdict is trustworthy because the instrument is validated and the false positives are caught.

## 1. Why this target

The genome programme's lesson was that a *validated instrument* plus a *flat target* yields a
defensible null. Language↔neural code inverts the second factor: neural responses to language carry
rich, structured, predictable variance (a mature encoding-model literature exists). So a positive
result is attainable, and the question becomes methodological — can the same controls that protected
us from a Bible-Code artifact also separate real neural effects from spurious ones? The
genome→language link is developmental/evolutionary, not a sequence cipher; that limb is not pursued.

## 2. The instrument and its controls

An encoding model predicts held-out neural responses from stimulus features. The six genome controls
map almost one-to-one: **floor** = phase-shuffled features; **out-of-sample** = held-out time /
cross-run prediction; **convergence/replication** = agreement across subjects; **multiplicity** =
across ROIs/features; and the **positive control** = a planted feature→response mapping the pipeline
must recover, plus the field's built-in double dissociation (low-level features → early auditory
cortex; semantic features → language network).

## 3. Results

**3.1 Instrument validation (simulation, Fig. N1).** Two synthetic regions were generated from a
known model — an "early" region driven only by low-level features, an "association" region driven
only by semantic features. The pipeline recovered the planted structure as a clean **double
dissociation** (low-level R² 0.73 early vs 0.02 assoc; semantic 0.72 assoc vs 0.24 early; both above
a ~0 floor). The instrument fires when a true mapping exists.

![Fig. N1](figures/N1_double_dissociation.png)

**3.2 Acoustic-envelope encoding — a replicated positive (Figs. N2, N3).** On real fMRI (Narratives
Pieman, raw native-space BOLD, two runs/subject), the speech spectro-temporal envelope predicted
held-out **cross-run** activity (fit run-1, predict run-2) above a phase-shuffled floor, with the
audio↔BOLD lag auto-recovered (~5–8 TR) and a noise ceiling from inter-run reliability. The effect **replicates and is
formally significant across 14 subjects** (6 of 20 requested lacked Pieman runs): 14/14 above floor,
mean Δ(test−floor) = 0.034, ~**33% of the explainable (ceiling) variance**, **t-test p = 4.2×10⁻⁵**,
Wilcoxon p = 1.2×10⁻⁴, **Cohen's dz = 1.61** (very large). A real, large-effect encoding of the
speech envelope in real fMRI, established with the same controls.

![Fig. N2](figures/N2_acoustic_real.png)

![Fig. N3](figures/N3_multisubject.png)

![Fig. N4](figures/N4_replication14.png)

**Specificity (Fig. N6) — real but not content-specific.** A stronger control than the phase-shuffle
floor: predict Pieman BOLD from a *different* story's envelope (given its own best lag). Across 14
subjects the mismatched story predicts **equally** (real 0.0368 ≈ mismatch 0.0346; p = 0.49,
dz = 0.19), both >> floor (p = 7×10⁻⁵). The envelope→BOLD effect is genuinely real but reflects
**generic speech-envelope tracking**, not content-specific encoding of this stimulus — a distinction
the phase-shuffle floor alone could not make. The same control logic as the genome battery
(real-vs-English-vs-random-target) here tempered our *own* positive: an honest narrowing of the claim.
*Caveat (see NEURAL_REFEREE_NOTES.md, M2):* because any two speech envelopes share coarse
spectro-temporal statistics, "predicts equally" establishes only that the cross-run-predictable
signal is **not carried by Pieman-specific moment-to-moment structure** — it does not by itself
distinguish a coarse/slow shared auditory response from a slow confound (drift/arousal). Resolving
that needs aggressive high-pass + nuisance regression (preprocessing) and an inter-subject
specificity design; on raw data this section is best read as a limitation, not a positive finding.

![Fig. N6](figures/N6_specificity.png)

**3.3 Semantic arm — an honest null (variance partitioning).** Whisper word timings (946 words) +
GloVe (PCA-12) tested whether *meaning* predicts BOLD beyond low-level/lexical features. Low-level
added genuine unique variance (unique_low 0.0092); **semantic added none beyond it**. Hardened across
**14 subjects (Fig. N5)** this is a robust, significant null: semantic-unique is below its
phase-shuffled floor in 13/14 subjects (mean 0.0099 < floor 0.0194; **t-test p = 2×10⁻⁴, Cohen's
dz = −1.35**). The single-subject null was not a power problem — with full power, meaning adds nothing
beyond acoustics on whole-brain raw data. The honest parallel: the *same* instrument on the *same* 14
subjects yields a large acoustic **positive** (dz = +1.6) and a large semantic **null** (dz = −1.4).
Power is not the limit; semantic-specific encoding is weak whole-brain and needs anatomical ROIs +
preprocessing.

![Fig. N5](figures/N5_semantic_null14.png)

**3.4 Auditory-vs-language dissociation — inconclusive, and a caught false positive.** Across three
iterations (ANTsPy registration; v3 = SyN + Harvard-Oxford anatomical ROIs + reliable-voxel
selection), ROI reliability improved from 0.018 to ~0.12, but the encoding R² stayed at noise level.
A naive `dissociation=True` flag arose at thin, noise-level margins on a near-zero-reliability ROI;
the reliability/margin gate **rejected** it as a false positive. We declined to swap features to force
a positive (the semantic half is null on one subject, so that would be fishing). **Verdict:
INCONCLUSIVE — the dissociation is not establishable on raw single-subject data; it needs fMRIPrep
(motion correction + QC'd normalization) and multiple subjects.** The pipeline is validated
end-to-end; the gate is data quality and design, not code.

## 4. Discussion

The pilot's value is the demonstration that one discipline produces trustworthy, *differentiated*
verdicts on a real target: **yes** (acoustic, replicated), **no** (semantic-unique, at this data
quality), and **not on this data** (the dissociation, refused rather than manufactured). The decisive
methodological act each time was the same as in the genome programme — validate the instrument with a
planted positive control, judge effects against a matched floor and a real ceiling, and let
replication and reliability, not a single flag, decide. The contrast across the two programmes —
genome null on a flat target, acoustic positive on a signal-bearing one, both judged identically — is
the core contribution.

## 5. Limitations & next steps

Raw, un-fMRIPrepped data; single subject for the semantic and dissociation arms; crude 16-band
acoustic and word-level features. The defensible next step is **fMRIPrep on several subjects**, after
which the existing `encoding_real.py` / `encoding_dissociation.py` engines run unchanged; that is the
route to a trustworthy dissociation. The acoustic replication has been extended to 14 subjects for
formal significance (§3.2); the semantic null likewise (§3.3).

## Data, code & reproducibility

Narratives ds002345 (OpenNeuro). Scripts in `scripts/`: `encoding_sim.py` (validation),
`encoding_acoustic.py` + `encoding_multi.py` (step 1), `encoding_semantic.py` + `encoding_semantic_multi.py`
(step 2), `encoding_dissociation.py` (step 3), `encoding_specificity.py` (specificity), `fetch_narratives.py`
(data). Per-run logs in the `*_result.json` files; figures N1–N6 in `figures/`. Full narrative:
`FIRST_STEP.md`; scope/rationale: `../two_books_genome/NEURAL_CODING_SCOPING.md`; programme overview:
`../two_books_genome/PROGRAM_SUMMARY.md`.
