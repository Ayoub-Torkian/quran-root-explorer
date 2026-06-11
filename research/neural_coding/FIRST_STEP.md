# Neural coding — first concrete step (instrument validated on a simulation)

_2026-06-09. Following the genome program's hard lesson — never interpret a result from an
un-validated instrument — the first step here is NOT to download brain data; it is to build the
encoding-model harness and prove it fires on a known feature→response mapping, with our full
control stack. Real data is plugged in only once the rig is validated._

## What this step did

`scripts/encoding_sim.py` builds two synthetic brain regions with a *known* generative model:
an **"early" region** driven only by **low-level** language features (word length, vowel ratio,
log-frequency), and an **"association" region** driven only by a **semantic** feature set (a fixed
per-word-type embedding). Responses get temporal autocorrelation and measurement noise (two repeats,
for a noise ceiling). We then fit ridge encoding models and score them with the same six controls
we used on the genome.

## Result — the positive control fires (Fig. N1)

| feature set → region | early region R² | assoc region R² |
|---|---|---|
| **low-level** | **0.728** | 0.021 |
| **semantic** | 0.239 | **0.721** |
| phase-shuffled floor | ≈ 0 | ≈ 0 |

A clean **double dissociation**: low-level features predict the early region and not the
association region; semantic features predict the association region and not the early region; both
sit far above the phase-shuffled floor. `double_dissociation_ok = True`. The instrument recovers a
planted mapping when one exists — the neural analogue of the planted-cipher positive control that
the genome program lacked at first.

## Real-data result — Narratives "Pieman", sub-001 (Fig. N2)

We then ran the harness on real fMRI using only files in the OpenNeuro bucket (no transcript, no
MNI, no fMRIPrep): speech **acoustic envelope** → BOLD, two Pieman runs of one subject, fit-on-run-1
/ predict-run-2 (true cross-run), 6 mm smoothing, automatic audio↔BOLD lag alignment.

| quantity | value | read |
|---|---|---|
| noise ceiling (inter-run r) | 0.265 | the explainable bar (raw data, smoothing-raised from 0.18) |
| best audio lag | 7 TR ≈ 10.5 s | auto-recovered; matches the ~13 s music intro + HRF |
| test R² (envelope, cross-run) | **0.0085** | predicts held-out run |
| floor R² (phase-shuffled) | −0.0014 | ≈ 0 — no inflation |
| **fraction of ceiling variance** | **~12%** | a real, if modest, positive |

**Read:** a genuine positive on real brain data — the speech envelope predicts stimulus-driven
BOLD cross-run, well above a phase-shuffled floor, explaining ~12% of the explainable (noise-ceiling)
variance. Absolute R² is small because most single-subject raw BOLD variance is noise (ceiling
R² ≈ 0.07); the honest denominator is the ceiling. This is the intended contrast with the genome:
the *same* control discipline, but a target that carries signal returns a positive instead of a null.
Script: `scripts/encoding_acoustic.py`; numbers in `scripts/encoding_acoustic_result.json`.

*Caveats:* one subject, raw (un-fMRIPrepped) data, a crude 16-band acoustic model, acoustic
(low-level) arm only.

## Replication across 5 subjects (step 1, Fig. N3) — `--fwhm 8`

`scripts/encoding_multi.py` reran the pipeline on sub-001…005. The effect **replicates**:

| subject | ceiling r | lag (TR) | test R² | floor R² | frac. ceiling |
|---|---|---|---|---|---|
| sub-001 | 0.276 | 7 | 0.0074 | −0.0024 | 0.10 |
| sub-002 | 0.344 | 5 | 0.0508 | 0.0115 | 0.43 |
| sub-003 | 0.380 | 4 | 0.0319 | 0.0063 | 0.22 |
| sub-004 | 0.423 | 6 | 0.0462 | 0.0071 | 0.26 |
| sub-005 | 0.469 | 8 | 0.0567 | 0.0101 | 0.26 |
| **mean** | **0.378** | 4–8 | **0.0386** | **0.0065** | **0.25** |

**5/5 subjects** show envelope > floor; mean test R² ≈ 6× the floor; **~25% of explainable
(noise-ceiling) variance** on average. Wilcoxon p = 0.0625 — the *minimum possible* for n = 5
(a unanimous same-sign result), so the consistency, not the p, is the evidence; 2–3 more subjects
would push p < 0.05. `--fwhm 8` also raised the mean ceiling to 0.38 (from 0.27 at 6 mm), confirming
the earlier low ceiling was a smoothing/alignment limit of raw data. Numbers:
`scripts/encoding_multi_result.json`.

**Hardened to 14 subjects (Fig. N4).** Re-running over 20 requested subjects (6 lacked Pieman runs)
gave **14/14 above floor**, mean Δ(test−floor) = 0.034, ~**33% of ceiling variance**, **t-test
p = 4.2×10⁻⁵**, Wilcoxon p = 1.2×10⁻⁴, **Cohen's dz = 1.61** (very large). The 5-subject result
(Wilcoxon floor p=0.0625) is now **formally significant** — a robust, large-effect replicated
encoding of the speech envelope in real fMRI.

**Specificity control — REAL but NOT stimulus-specific (Fig. N6).** A referee-grade test: predict
Pieman BOLD from a *different* story's envelope (tunnel), given its own best lag. Across 14 subjects
the mismatched story predicts **just as well** as the real one — real 0.0368 ≈ mismatch 0.0346
(real > mismatch in only 7/14; **p = 0.49, dz = 0.19**), both ≫ phase-shuffled floor (real-vs-floor
p = 7×10⁻⁵). So the envelope→BOLD effect is genuinely real (vs a randomized floor) but reflects
**generic speech-envelope tracking / shared low-level structure, not content-specific encoding** of
this stimulus. The phase-shuffle floor alone was too weak; the mismatched-story control revealed the
non-specificity — exactly the role the genome battery's real-vs-English-vs-random-target controls
played. Our own discipline caught an over-claim in our own positive. Numbers:
`scripts/encoding_specificity_result.json`.

**Status of step 1:** a real, replicated, formally-significant **but non-stimulus-specific**
envelope-tracking effect. Content-specific encoding would need higher-level features and the
anatomical ROIs + preprocessing of step 3. Next levers: (2) semantic arm; (3) dissociation
(preprocessed data).

## Step 2 — semantic arm (variance partitioning, sub-001)

`scripts/encoding_semantic.py` (Whisper word timings: 946 words; GloVe-300d → 12 PCA comps) asks:
do semantic features predict BOLD *beyond* low-level/acoustic features? Cross-run, reliable voxels.

| quantity | value | read |
|---|---|---|
| R²_low | 0.016 | low-level predicts (consistent with step 1) |
| R²_sem | 0.008 | semantic alone (mostly shared with low-level) |
| R²_both | 0.017 | combined |
| **unique_low** = both−sem | **0.0092** | low-level adds real unique variance ✓ |
| **unique_semantic** = both−low | **0.0012** | ≈ 0 |
| unique_sem floor (shuffled sem) | 0.018 | the floor exceeds unique_semantic |

**Result — NULL for the semantic arm at this data quality.** `unique_semantic` (0.0012) sits *below*
its phase-shuffled floor (0.018): the 12 semantic regressors add only overfit noise, which the floor
correctly matches. Low-level features, by contrast, add genuine unique variance (`unique_low` 0.0092).
This is the expected limit, not a surprise — semantic-specific encoding is weak whole-brain and
concentrates in the **language network**, so detecting it needs the anatomical ROIs + preprocessing of
**step 3**. Numbers: `scripts/encoding_semantic_result.json`.

**Hardened to 14 subjects — a robust, significant NULL (Fig. N5).** `encoding_semantic_multi.py`
replicated the variance partitioning across the 14 subjects. Semantic-unique is **below** its
phase-shuffled floor in **13/14** subjects: unique_sem mean 0.0099 < floor 0.0194, **t-test
p = 0.0002, Cohen's dz = −1.35**. So the single-subject null was *not* a power problem — with full
power, meaning adds nothing beyond acoustics on whole-brain raw data. The honest parallel: the SAME
instrument on the SAME 14 subjects gives a large acoustic **positive** (dz = +1.6) and a large
semantic **null** (dz = −1.4) — opposite verdicts, both trustworthy. Power is not the limit;
anatomical localization + preprocessing is (step 3). Numbers: `scripts/encoding_semantic_multi_result.json`.

## Step 3 — auditory-vs-language dissociation (ANTsPy, sub-001): INCONCLUSIVE (and a caught false positive)

`scripts/encoding_dissociation.py` (py3.11 conda env; ANTs affine/MI registration → warp BOLD to MNI
→ Heschl vs pSTS/IFG spheres → low-level vs semantic encoding). Raw result:

| ROI | low-level R² | semantic R² | inter-run reliability |
|---|---|---|---|
| auditory | 0.0121 | −0.048 | **0.018** |
| language | 0.0081 | −0.044 | 0.11 |

The naive flag (low→aud>lang AND sem→lang>aud) is **True** — but it is a **false positive**, and our
own discipline catches it: (i) the auditory ROI inter-run reliability is **0.018 ≈ 0** (whole-brain
step 1 had ~0.27; for a listening task auditory cortex should be the *most* reliable — it's the least,
so the sphere isn't on responsive cortex); (ii) semantic R² is **negative in both ROIs**; (iii) the
between-region gaps are ~0.004–0.005, at noise level. The gated verdict is therefore **INCONCLUSIVE —
ROI reliability/margins at noise level (raw single-subject; needs fMRIPrep).**

**v3 refinement (SyN + Harvard-Oxford anatomical ROIs + reliable-voxel selection).** Auditory ROI =
604 voxels, language = 9251; ROI reliability improved 0.018 → **0.123 / 0.133** (registration+atlas
genuinely better). Yet `low→auditory` stayed ≈0 (−0.0005), all R² ≈0/negative → **VERDICT still
INCONCLUSIVE.** Diagnostic: the ROIs now carry real cross-run signal, but step-3's *word-level*
features (rate/length/freq) don't predict it — whereas step 1's working driver was the 16-band
acoustic **spectral envelope**, which word-rate only weakly proxies.

**Where we stopped, and why (a disciplinary decision).** Swapping the acoustic envelope back in would
likely make `low→auditory` positive — but step 2 already showed the semantic half is null on one raw
subject, so a full double dissociation won't materialize here, and tuning features until the flag
flips would be fishing — exactly what this framework refuses. **Honest conclusion for step 3:** the
dissociation is *not establishable* on raw single-subject data; a trustworthy version needs fMRIPrep
(motion correction + QC'd normalization) and multiple subjects. The pipeline is built and validated
end-to-end (3 iterations, recorded); the gate is data quality and study design, not code. The same
vigilance that killed the genome's 0.58 fluke refuses to bless a manufactured dissociation.

## How the six controls transferred

floor = phase/circular-shift of features (→ R² ≈ 0); out-of-sample = contiguous 70/30 time split;
convergence = (next step) agreement across subjects; replication = (next step) across subjects/
datasets; multiplicity = (next step) voxelwise FDR; **positive control = the double dissociation**.
The target here carries real, structured variance — so unlike the flat genome, a positive result is
attainable.

## The concrete next step: one real open dataset

The rig is ready for real fMRI. Because the target is non-flat and our positive control is built in
(low-level→auditory cortex, semantic→language network), the smallest honest real test is one subject
from a public story-listening dataset.

**Routes (LOCKED protocol: 3–5, recommend 1).**
1. **Narratives ("Pieman"), one subject** (Nastase et al. 2021, OpenNeuro ds002345). Story-listening
   fMRI with a *repeated* stimulus → a real noise ceiling; modest size. Features: low-level (word
   rate, phoneme rate, word length) vs semantic (GloVe or an LLM embedding), HRF-convolved; predict
   auditory-cortex vs language-network ROIs; expect the same dissociation. *Pro:* repeats give a
   ceiling; well-documented; one subject is laptop-feasible. *Con:* still a multi-GB download (run
   locally, like BLAST).
2. **LeBel et al. 2023**, one subject. *Pro:* huge, high-quality. *Con:* very large; overkill for a
   first step.
3. **Pereira et al. 2018** (sentence-level fMRI). *Pro:* small, semantic-focused. *Con:* no
   continuous stimulus / weaker low-level contrast, so the dissociation is less clean.
4. **MEG/EEG "Little Prince"**. *Pro:* small, fast. *Con:* source-space messier; ceiling harder.

**Recommendation: Route 1 — one Narratives subject.** It uniquely gives a real noise ceiling (the
repeated story), a clean low-level vs semantic dissociation against auditory vs language ROIs, and a
laptop-feasible footprint. The harness in `scripts/encoding_sim.py` already implements the floor,
held-out split, ceiling normalization, and the dissociation check; the real-data version swaps the
synthetic responses for the subject's voxel time series and adds HRF convolution + voxelwise FDR.
The download + fit run locally (the dataset is too large and network is restricted here), exactly as
we did for BLAST. I'll provide the data-loading + HRF adapter when you want to proceed.

## Honest caveats (carried from the scoping doc)
Predictivity is representational *alignment*, not proof the brain computes the model. No genome
bridge — that limb was rejected. This is a different, mature field; our contribution is methodological
discipline (the planted positive control + convergence + replication), ported to a target that can
actually carry signal.
