# Instrument assessment — root spatial distribution (1‑D & 2‑D). 2026‑06‑12

## Data representations now in hand
- **R1** — per‑root occurrence **series** along the 6,236 āyāt (1‑D ordered signal).
- **R2** — per‑root **intra‑āyah position** distribution (1‑D, normalised 0→1).
- **R3** — per‑root **2‑D fingerprint matrix** (intra‑position × muṣḥaf), the atlas object.
- **R4** — cross‑root **abundance matrix** (roots × windows).

## Transforms (preprocessing, not discovery)
log / √ / Anscombe / Box‑Cox — variance‑stabilise counts. Used (log1p in atlas). Helpers only.

## 1‑D / vector instruments (on R1, R2, or any‑angle Radon slice of R3)
| instrument | measures | run | result | verdict |
|---|---|---|---|---|
| Fourier / spectral | periodicity | yes (2‑D) | null | — |
| Autocorrelation (gaps) | wave/burst | yes | tiny (z=9, <0.20 floor) | passage clustering (known) |
| DFA / Hurst | long‑range scaling | ≈wavelet | α off‑white at large scale | territory (known) |
| **Wavelet variance** | scale + locality | **yes** | excess at ~256–512 āyāt | large‑scale **territory** (G7) |
| **Taylor's law** (fluctuation scaling) | Var∝Mean^β | **yes** | β=1.22, R²=0.91; →1.0 on shuffle | **passage cohesion** (G7) |
| Ripley‑K 1‑D / Clark‑Evans / dispersion | clustering vs CSR | — | — | **already in app** |

## 2‑D / matrix instruments (on R3)
| instrument | measures | run | result | verdict |
|---|---|---|---|---|
| **2‑D FFT / directional** | diagonal/any‑angle texture | **yes** | null (0/72 roots) | = product of marginals |
| SVD / low‑rank | joint coupling | implied | rank‑1‑ish (corr 0.16) | product of marginals |
| Haralick / GLCM texture | co‑occurrence texture | — | (would = marginals) | low odds |
| Persistent homology (TDA) | loops / voids | no (no lib) | — | low odds; untested |
| Morphology / hotspots / Getis‑Ord / LISA | local clusters | — | — | **already in app** |
| Radon (projections at all angles) | directional 1‑D slices | yes | dominant 0°/90° only | = the two marginals |

## Cross‑root / ensemble instruments (on R4)
| instrument | measures | run | result | verdict |
|---|---|---|---|---|
| **RMT eigen‑spacing ⟨r⟩** | level repulsion | **yes** | null (Wishart) | non‑discriminating |
| **Marchenko–Pastur modes** | # real factors | **yes** | 39 modes | = topics (G7) |
| MDS / embedding of map‑distance | pattern‑family geometry | partial (app forest) | — | ≈ topics (G7 risk) |
| Network / Laplacian spectrum | communities | — | — | **already in app** |

## Learning / information instruments
| instrument | run | result | verdict |
|---|---|---|---|
| Classifier (boundary recovery) | yes | L27 → demoted 84 | order‑invariant = fāṣila (G7) |
| MDL / compression vs Markov | yes | 0.836 | = repetition/propagation (G7) |

## Meta‑conclusion (the honest map)
Every instrument above, across 1‑D and 2‑D, resolves to **one of three already‑named structures**:
1. **Verse‑position law** (onset / closure) → rhyme + syntax (L06, L18, L26, L27).
2. **Large‑scale territory** (wavelet 256–512, MP modes, inter‑verse) → topics / themes.
3. **Mid‑scale passage cohesion** (Taylor β, autocorrelation, folding) → membrane / weave (A1, A2).

The 2‑D fingerprint = (1) × (2) with **no emergent diagonal coupling** (FFT/SVD null). So the toolbox is, in effect, **fully surveyed**: rich structure, all three components already in the ledger/app. The atlas is a strong **descriptive/visualization** asset; no instrument here yields a *new* >90, because the structure they each detect is already attributed.

**Only genuinely untested instrument:** persistent homology (TDA) — needs a library; low prior, but the one box unchecked.
