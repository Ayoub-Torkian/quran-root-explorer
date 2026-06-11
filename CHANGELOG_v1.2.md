# Quran Root Explorer — v1.2 changelog

Build on top of v1.1 (the working version deployed to Hugging Face).
Strict policy: [b]do not touch any file v1.1 depends on except via additive
extensions[/b]. Two file edits, three new files.

## What's new

### 1. Pair classification (data-driven tier labels)
New module: `pair_classification.py`

For any two roots, computes:
```
lift = P(A ∩ B) / [ P(A) · P(B) ]
```
and assigns a tier label based on threshold:

| Tier | Lift range | Meaning |
|------|-----------|---------|
| stipulative | ≥ 10 | Treated as a single concept in two words |
| embedded | 2 - 10 | Frequent companions, cross-cutting categories |
| mild | 1 - 2 | Above chance but only slightly |
| independent | ≤ 1 | Separate semantic neighborhoods |

The module also ships with a `CALIBRATION_PAIRS` reference set of 12 famous
Qurʾanic dyads (ʿusr/yusr, dunyā/ākhira, rashad/ghayy, ẓulm/ʿadl, etc.)
that act as ground-truth examples of each tier.

### 2. New page  ·  Calibration  (📏)
`pages/8e_Calibration.py`

Benchmarks the user's current pair(s) against the 12 reference pairs on a
log-scale lift spectrum. Shows tier dividers, color-coded reference pairs,
and the user's pair(s) as highlighted star markers. Plus the tier-legend
table and a "how to read" footer.

### 3. New page  ·  Practical Lens  (🧰)
`pages/8f_Practical_Lens.py` + `practical_lens.py`

Maps the computed findings to translation tips, teaching parallels, and
everyday-life parallels. Every overlay is:

- opt-in (inside expanders, default collapsed)
- clearly labeled as INTERPRETIVE OVERLAY (banner at top)
- anchored to the specific numeric finding that triggered it
- tier-based, not theological

Per-pair lenses (one per tier) plus per-root lenses for ẓulm, ʿadl, nafs
where the corpus evidence is strong enough to support a curated practical
overlay.

### 4. Reading Guide enhancement
`interpret.py` — `pairwise_facts()` function extended.

Each pairwise fact line now appends the lift value and tier label:

```
before:  ظلم <-> عدل: 1 shared ayahs, P(عدل|ظلم) = 0.3%.
after:   ظلم <-> عدل: 1 shared ayahs, P(عدل|ظلم) = 0.3% · lift = 0.90 · tier: Independent / quarantined.
```

The change is graceful: if `pair_classification` import fails, the function
silently falls back to v1.1 output.

## Files touched

```
NEW: pair_classification.py          ·  thresholds + 12-pair reference set
NEW: practical_lens.py               ·  tier-based applied lenses
NEW: pages/8e_Calibration.py         ·  benchmark vs reference pairs
NEW: pages/8f_Practical_Lens.py      ·  interpretive overlay page
EDITED: interpret.py                 ·  pairwise_facts() appends tier
EDITED: CHANGELOG_v1.2.md            ·  this file
```

## Files NOT touched
Everything else. The v1.1 page set (Per Root Profile, Network, Motifs,
Ayah Browser, Compare/Heatmaps, Morphology, Statistics, Export, Reading
Guide, Topic pages, Surface Divergence, Help, Usage) is unchanged.

## Roll-back
To revert to v1.1 behaviour exactly: delete the four new files and revert
the single edit in `interpret.py`. There are no other coupling points.

## Design principle
v1.2 respects the v1.1 principle that the [b]factual layer[/b] of the app
(Reading Guide, Statistics, Network) is strictly data-driven with no
conjecture. The Practical Lens page adds an [b]interpretive overlay[/b]
that is clearly labeled, opt-in, and visually separated from the factual
layer. Translation tips, teaching parallels, and everyday-life parallels
are explicitly tagged as reasoned suggestions rather than computed facts.
