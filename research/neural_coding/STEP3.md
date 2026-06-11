# Step 3 — the auditory-vs-language anatomical dissociation (the real-paper step)

_Goal: show the **double dissociation** on real brain data — low-level/acoustic features predict
AUDITORY cortex, semantic features predict the LANGUAGE network — the result that turns "encoding
works" into a publishable claim. This is the heaviest step because it is the one that genuinely
needs **preprocessed, anatomically-normalized (MNI) data**; the raw native-space BOLD we used for
steps 1–2 cannot place anatomical ROIs._

## What is already in place

- **Engine:** `scripts/encoding_real.py` — loads BOLD into MNI auditory (Heschl) and language-network
  (pSTS/IFG) spheres, builds low-level + GloVe-semantic word features, HRF-convolves, and runs the
  same floor/held-out controls, then checks the dissociation. Ready to run on preprocessed BOLD.
- **Word onsets:** produced in step 2 by Whisper and saved to `narratives_data/pieman_words.csv`
  (pass it via `--words`), so no transcript hunt is needed.
- **Validated logic:** the simulation positive control (Fig. N1) already showed the dissociation
  test fires when the generative structure is present.

## The one missing input: preprocessed MNI BOLD

The OpenNeuro `ds002345` bucket has **raw** BOLD only (no `derivatives/`, confirmed by scan). Two
honest routes to get MNI-space responses for one subject:

**Route A — fetch published fMRIPrep derivatives (no compute).** The Narratives derivatives
(fMRIPrep, in MNI152NLin2009cAsym) are distributed via DataLad, not the OpenNeuro S3. Install just
one subject:
```bash
pip install datalad
datalad install -r https://github.com/snastase/narratives   # or the DataLad catalog entry
datalad get derivatives/fmriprep/sub-001/func/sub-001_task-pieman*MNI152*desc-preproc_bold.nii.gz
```
(Exact derivative path/superdataset URL must be confirmed from the dataset's DataLad catalog; if the
GitHub superdataset doesn't expose `derivatives/`, use the Princeton/`datasets.datalad.org` mirror
named in the Narratives data descriptor, Nastase et al. 2021.)

**Route B — run fMRIPrep yourself (compute, ~3–6 h/subject, Docker).**
```bash
pip install fmriprep-docker
fmriprep-docker narratives_data fmriprep_out participant --participant-label 001 \
  --output-spaces MNI152NLin2009cAsym --fs-no-reconall
```

**Route C — self-contained ANTsPy registration (recommended; no fMRIPrep, no DataLad).**
`scripts/encoding_dissociation.py` registers the subject's mean EPI to MNI with ANTs, warps the
auditory/language ROI masks into native space, and runs the dissociation directly on the raw runs we
already have. The catch: the registration stack has **no Python 3.14 wheel** (confirmed —
`pip install antspyx` tries to compile scipy and fails for lack of a C compiler). Use a Python 3.11
conda env where `conda-forge` ships everything prebuilt:
```bash
conda create -n neuro python=3.11 -c conda-forge antspyx nibabel nilearn scipy numpy pandas
conda activate neuro
python research/neural_coding/scripts/encoding_dissociation.py ^
  --run1 narratives_data/sub-001_task-pieman_run-1_bold.nii.gz ^
  --run2 narratives_data/sub-001_task-pieman_run-2_bold.nii.gz ^
  --words narratives_data/pieman_words.csv --glove glove.6B.300d.txt
```
Output: per-ROI low-level vs semantic R²; the `dissociation` flag is true if low→auditory>language
and sem→language>auditory. (Registration on one EPI is imperfect; treat the first run as a smoke
test and expect to iterate on ROI radius / transform type.)

## Run (once preprocessed BOLD exists)

```powershell
python ..\neural_coding\scripts\encoding_real.py `
  --bold <sub-001 ...MNI152...preproc_bold.nii.gz> `
  --words narratives_data\pieman_words.csv `
  --glove glove.6B.300d.txt
```
Expect: auditory R² high for low-level / low for semantic; language R² high for semantic / low for
low-level — the double dissociation, on real brain data.

## Honest status

Step 3 is **engine-ready but gated on preprocessed data**. Routes A/B both require either a
DataLad fetch of large derivatives or hours of fMRIPrep — i.e., real infrastructure, not an
afternoon. This is the appropriate boundary for the "real-paper" version; steps 1–2 already
establish, on locally-runnable raw data, that the validated instrument produces a replicated
positive (acoustic) and a test for unique semantic variance. Recommended: attempt **Route A** first
(download-only); fall back to **Route B** if the derivative path can't be confirmed.
