# fMRIPrep setup — the deliberate step that makes the neural empirical claims real

_fMRIPrep does motion correction + distortion handling + QC'd normalization to MNI. With its output
the existing engines test content-specificity, the language-network semantic effect, and the
auditory-vs-language dissociation properly — the three things raw single-subject data could not
support. This is heavy: plan a focused afternoon for ONE subject first, then scale._

## What it needs (and rough costs)
- **Docker Desktop** (Windows → requires WSL2). fMRIPrep ships as a ~8–10 GB Docker image.
- **A FreeSurfer license** (free) — required even when we skip surface recon.
- **BIDS-valid input** including the **T1w anatomical** (not just BOLD). Our `narratives_data/` is not
  BIDS; `fetch_bids_subject.py` builds a proper `bids/` root.
- **Resources:** ~16 GB RAM recommended, ~20–30 GB disk, and ~1–2 h per subject with
  `--fs-no-reconall` (much longer with surface recon, which we don't need for volumetric ROIs).

## Stage A — Docker
1. Install Docker Desktop for Windows (enables WSL2 automatically). Reboot if prompted.
2. Confirm:
   ```powershell
   docker --version
   docker run --rm hello-world
   ```

## Stage B — FreeSurfer license (free)
Register at https://surfer.nmr.mgh.harvard.edu/registration.html → you receive a `license.txt`.
Save it somewhere stable, e.g. `C:\Users\torki\freesurfer_license.txt`.

## Stage C — build a BIDS root for ONE subject
From `research/two_books_genome` (or anywhere; uses default Python with botocore):
```powershell
python ..\neural_coding\scripts\fetch_bids_subject.py --sub sub-001 --tasks pieman --out bids
```
This downloads the subject's **anat/T1w** + **func/pieman** (+ JSON sidecars) and dataset-level
metadata into `bids/`. If it warns "no anat/", that subject lacks a T1w — pick another (e.g.,
`--sub sub-002`). Optional sanity check: `npx bids-validator bids` (needs Node).

## Stage D — install + run fMRIPrep (one subject)
```powershell
python -m pip install fmriprep-docker
```
Run (one line; `--fs-no-reconall` skips the slow surface step we don't need):
```powershell
fmriprep-docker bids fmriprep_out participant --participant-label 001 --output-spaces MNI152NLin2009cAsym:res-2 --fs-no-reconall --fs-license-file C:\Users\torki\freesurfer_license.txt --nthreads 4 --mem-mb 12000 --low-mem
```
Output of interest:
`fmriprep_out/fmriprep/sub-001/func/sub-001_task-pieman_run-1_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz`
plus `..._desc-confounds_timeseries.tsv` (motion/physio nuisance regressors).

## Stage E — run our engines on the preprocessed output
The data is now in MNI, so the MNI-ROI engine is valid as-is:
```powershell
C:\Users\torki\miniconda3\envs\neuro\python.exe ..\neural_coding\scripts\encoding_real.py --bold fmriprep_out\fmriprep\sub-001\func\sub-001_task-pieman_run-1_space-MNI152NLin2009cAsym_res-2_desc-preproc_bold.nii.gz --words narratives_data\pieman_words.csv --glove glove.6B.300d.txt
```
For the dissociation, `encoding_dissociation.py` currently does its *own* registration; with fMRIPrep
input that step is redundant — I'll add a `--preprocessed` flag (skip registration, read ROIs
directly in MNI) once you have one subject's output, so we don't double-transform.

## Recommended path
1. **One subject, smoke test** (Stages A–E on sub-001). Confirm the auditory ROI inter-run
   reliability jumps well above the 0.12 we got from raw data — that is the QC that says
   preprocessing fixed the localization problem.
2. **Then scale** to the 14 subjects (loop `--participant-label`), and re-run the three tests
   (content-specificity with nuisance regression, language-network semantics, dissociation) with the
   confounds regressed out. That converts the pilot's bounded/null/inconclusive results into real,
   QC'd findings.

## Honest note
This is genuinely a multi-hour, human-in-the-loop job (Docker install, license, per-subject compute).
Do sub-001 end-to-end first; if its preprocessed reliability and the content-specificity test behave,
scaling is mechanical. The engines and the analysis plan are already in place — the only missing
ingredient was preprocessed data, and this is how you get it.
