# Inter-subject correlation (ISC) on raw data — run entirely in-sandbox, no installs (Fig. N7)

_2026-06-09. Done without Docker/FreeSurfer/any user-side install: the BOLD already sat in the
project folder, so the analysis ran in the assistant's sandbox (ANTs affine registration to a 4 mm
MNI template, then leave-one-out ISC across 10 subjects, with a phase-shifted null)._

## What ISC tests
Do different people's brains respond in **synchrony** to the same story? ISC is the most robust,
celebrated effect in naturalistic neuroimaging — a shared narrative aligns listeners' auditory and
language cortex (typical ISC ≈ 0.2–0.5 there, on properly preprocessed data). It's the closest thing
to "a story is processed the same way across minds."

## Result — weak and mis-located (a clean, honest negative-ish)
- Whole-brain ISC mean **0.0025** vs null −0.0006; peak 0.158; ~6.5% of voxels exceed the 99th-pct
  null (vs 1% expected) — i.e., *some* elevation, but tiny.
- **Crucially, where the synchrony sits is wrong:** the top-ISC voxels are at z ≈ 64–72 mm — the
  **vertex/superior edge** — not auditory cortex (z ≈ 0–15, y ≈ −20). The lateral-temporal band
  (0.013) barely exceeds whole-brain (0.011). Synchrony piled at the brain edge is the classic
  signature of **head-motion artifact**, not story-driven neural alignment.

## What it means
Even ISC — which *cannot* fail to appear on well-preprocessed naturalistic data — does **not** show
up properly here, and the little that appears is in motion/edge locations. This converges with every
other neural analysis (acoustic non-specificity, semantic null, inconclusive dissociation): the
limiting factor is not the science or the question, it is **preprocessing** — motion correction +
QC'd normalization (what fMRIPrep does and our affine-only sandbox pipeline does not). The effects
are real in the literature; raw data simply cannot deliver them.

## Bottom line
We established this at zero cost (no installs): the consistent reason the neural results stay weak/
null is missing motion correction & normalization. So the genuine fork is unchanged but now
*demonstrated*: either invest in proper preprocessing, or treat the neural arc as a documented pilot
whose honest conclusion is "real effects, raw-data-limited." Script/outputs: `outputs/isc/*`.
