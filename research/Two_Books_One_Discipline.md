# Two Books, One Discipline: a controlled framework for cross-domain mapping claims, exercised on scripture↔genome and language↔brain

**A. Torkian** (torkian@sharif.edu) · *perspective / methods synthesis, 2026-06-09*

---

## Abstract

Claims that one symbolic sequence "encodes" another — a text hiding the genome, meaning written into
the brain — are recurrent, and they fail in one of two ways: a transformation searched over a long
sequence manufactures signal from noise (the "Bible Code" trap), or a real effect is over-read
beyond what the controls support. We present a single six-control discipline — composition floor,
out-of-sample transfer, convergence, replication, multiplicity, and a **planted positive control** —
and exercise it on two deliberately opposite targets. On a **statistically flat** target (the human
genome, asked whether a character→codon/amino-acid cipher links it to the Qur'ān) the discipline
returns a thorough, replicated **null**, after catching a convergence "discovery" that died under
replication. On a **signal-bearing** target (the brain's fMRI response to spoken language) the same
discipline returns a large, significant **positive** for acoustic-envelope tracking — then, with a
stronger control, **narrows** that positive to a non-content-specific effect, returns a robust
**null** for unique semantic variance, and **refuses** a thin "dissociation" flag on unreliable data.
The contribution is the discipline: applied identically to opposite targets it yields differentiated,
trustworthy verdicts — *no*, *yes-but-bounded*, *not on this data* — because the instrument is
validated and over-claims are caught, including our own.

## 1. The problem both books share

Texts and biological sequences are both discrete linear symbol strings, which makes "X encodes Y"
claims perennially tempting. The methodological trap is uniform: choose (often by searching many) a
mapping that maximizes similarity against a vast database, then present the match as discovery. With
an astronomical search space, *some* mapping matches *any* input, including noise — the failure that
discredited the Bible Code (Witztum–Rips–Rosenberg 1994; refuted by McKay et al. 1999). The
symmetric failure, on targets that *do* carry signal, is to report a real effect at face value
without testing what it is specific to. One discipline should guard against both.

## 2. The discipline (six controls)

Treat any proposed mapping as a **tested output, never an assumed input**:

0. **Mapping-invariant pre-check** — compare domains on relabeling-invariant structure; a gross
   mismatch refutes *all* mappings at once.
1. **Floor** — run the identical pipeline on shuffled/random inputs; only the margin over this floor
   counts (free mappings saturate any raw score).
2. **Out-of-sample transfer** — fit on one portion, test on unseen.
3. **Convergence** — independently optimized maps on disjoint portions must agree (the operational
   test of "a correct mapping exists").
4. **Replication + significance** — re-evaluate over many pairs/subjects; a single instance can pass
   1–3 and still be a fluke.
5. **Multiplicity** — hold across objectives, granularities, scenarios; report the whole search.
6. **Planted positive control** — prove the instrument recovers a *known* mapping, else a null is
   uninterpretable (it may just be a weak search). This control also exposes *target-side* limits.

## 3. Book of the Act — the genome, a flat target (a clean null)

We asked whether a character→codon/amino-acid mapping links the Qur'ān to the human coding genome
(NCBI CCDS), with eight control languages.

**Structure (control 0).** The genome's long-range statistical memory (MI-decay γ ≈ 0.92) sits far
from every tested language (γ ≈ 1.4–2.5; the Qur'ān at 2.29 is inside the language cluster), an
outlier at p ≈ 3×10⁻⁴, and not an alphabet-size artifact (the gap survives matched 4-symbol and
64-codon recodings). Relabeling cannot change this, so it rules out every mapping at once (Fig. 1).

![Fig. 1](F1_structural_gamma.png)

**The caught false positive (controls 3–4).** A search did surface a striking convergence — 0.58 vs
chance 0.056 — that survived shuffle, other-language, and random-target controls. Replication killed
it: over five disjoint pairs, real 0.22 ± 0.13 equalled shuffled 0.22 ± 0.16 (z = 0.00); the residual
was a composition effect, not order or meaning (Fig. 2). *n = 1 is never enough.*

![Fig. 2](F4_false_positive.png)

**Instrument validation (control 6).** A planted substitution cipher in structured text is recovered
perfectly (recovery 1.00, convergence 1.00 on letters; 0.87/0.57 on roots) — but the same instrument
collapses to chance against the genome, because protein/genome sequence is statistically **flat** at
the n-gram orders where ciphers are crackable (Fig. 3). This is a *target-side* limit: it bounds
every forward text→genome substitution map at any granularity (letter, codon, root all null). The
nulls are genuine signal-absence, not weak search.

![Fig. 3](F6_positive_control.png)

Folding (Qur'ān-derived "proteins" do not fold) and a faithful local `tblastx` run agree. The
forward text→genome program is closed.

## 4. Book of the Word as neural code — a signal-bearing target (a bounded positive)

The genome lesson — *validated instrument + flat target = defensible null* — inverts when the target
carries signal. Neural responses to language do. We ported the same controls to fMRI encoding models
(Narratives "Pieman").

**Validation, then a real positive.** On a simulation with a planted feature→response mapping the
pipeline recovers a clean double dissociation. On real fMRI, the speech acoustic envelope predicts
held-out, cross-run activity, replicated and **formally significant across 14 subjects** (t-test
p = 4×10⁻⁵, Cohen's dz = 1.6; ~33% of the noise-ceiling variance) (Fig. 4).

![Fig. 4](N4_replication14.png)

**The discipline narrows our own claim.** A stronger control than the phase-shuffle floor — a
*different* story's envelope, given its best lag — predicts equally (p = 0.49) (Fig. 5). So the
effect is real but **not Pieman-specific**: generic speech-envelope tracking, and we cannot yet
separate a coarse auditory response from a slow confound on raw data. The same logic that caught the
genome fluke here tempered our *own* positive.

![Fig. 5](N6_specificity.png)

**A robust null and a refused flag.** Across 14 subjects, *unique* semantic variance (beyond
acoustics) is a significant null (dz = −1.35) — same instrument, same subjects: acoustic **positive**
(dz +1.6), semantic **null** (dz −1.4). And an auditory-vs-language dissociation, run end-to-end with
registration, produced a `dissociation=True` flag on a near-zero-reliability ROI that the
reliability/margin gate **refused** as a false positive (verdict: inconclusive; needs proper
preprocessing).

## 5. One discipline, differentiated verdicts

| target | character | verdict | how it was earned |
|---|---|---|---|
| Qur'ān ↔ genome (cipher) | flat | **no** | structure + replication-killed fluke + validated instrument |
| speech envelope → BOLD | rich | **yes, but bounded** | replicated, significant — then narrowed by specificity |
| meaning → BOLD (unique) | rich | **no** (robust) | variance partitioning across 14 subjects |
| auditory vs language ROIs | rich | **not on this data** | false-positive flag refused on QC |

Applied identically to opposite targets, the discipline says *no*, *yes-but-bounded*, and *not yet* —
and each verdict is trustworthy because (a) the instrument was validated against a planted positive
control, (b) effects were judged against matched floors and real ceilings, and (c) replication and
reliability, not a single flag, decided. Over the program it caught four over-claims — the genome's
0.58 fluke, the dissociation flag, the acoustic over-reach, and our own specificity interpretation —
and walked each back. That refusal to take results the data cannot support is the contribution; it is
exactly what separates this from a Bible-Code exercise.

## 6. Scope and next steps

Conclusions concern the specific sequence/encoding hypotheses only; nothing here speaks to the Qur'ān
as scripture, which no similarity statistic can address. The genome program is complete. The neural
arc is a pilot on raw data; the defensible next step is fMRIPrep on the 14 subjects, after which the
existing engines test content-specificity, the language-network semantic effect, and the dissociation
properly. Full methods, data, code, and per-step ledgers: `two_books_genome/MANUSCRIPT_DRAFT.md` and
`neural_coding/NEURAL_PILOT.md` (with internal referee reports), summarized in
`two_books_genome/PROGRAM_SUMMARY.md`.

## References
Witztum, Rips & Rosenberg (1994) *Stat. Sci.* 9:429; McKay, Bar-Natan, Bar-Hillel & Kalai (1999)
*Stat. Sci.* 14:150; Peng et al. (1994) *Phys. Rev. E* 49:1685; Lin et al. (2023) *Science* 379:1123;
Altschul et al. (1990) *J. Mol. Biol.* 215:403; Pruitt et al. (2009) *Genome Res.* 19:1316;
Nastase et al. (2021, Narratives dataset) *Sci. Data*.
