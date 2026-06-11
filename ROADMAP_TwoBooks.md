# Two Books — Development Roadmap

A forward-looking plan for the *Two Books* section (Disjoint Letters · Signal ·
Biology). Organizing principle: the corpus is read at three **scales** —
🧭 Position (index geometry), 🔤 Sequence (character scale, letters≈bases), and
🧩 Semantic (word/root scale, roots≈codons, words≈proteins). Every proposed
addition keeps the house rules: computed live, validated against an explicit
permutation/Poisson null, length-confounds disclosed, no "scientific-miracle"
claims.

Status legend:  ✅ shipped (v1.3)   ·   🔜 next   ·   🧪 exploratory   ·   🏗 platform

---

## 🧭 Position — index geometry (the validated pointer)

Shipped (v1.3): family explorer, label-permutation contiguity (muṣḥaf + nuzūl),
organization/length, theme null, verdict scorecard.

Value-adds:
- ✅ **Leave-one-out robustness.** Jackknife each family member and re-run
  contiguity; show how p moves. Answers "does the result hinge on one sūra?"
  *(Shipped: worst-case LOO p ≈ 0.0002 — robust to dropping any one sūra.)*
- 🔜 **Ordering sensitivity.** Re-test contiguity under alternative chronologies
  (Nöldeke, Ibn ʿAbbās) beside the Egyptian standard — a robustness panel, not a
  single ordering.
- 🧪 **Spatial autocorrelation.** Treat the 29-tag indicator as a signal over
  1..114 and compute Moran's I / run-length statistics with a permutation null —
  a second, independent lens on "clustering."
- 🧪 **Change-point detection** on the muqaṭṭaʿāt indicator (where does the
  density of tagged sūras shift?).
- 🔜 **Predictive check.** Hold out a family member; can the remaining family
  geometry predict its position better than chance? Cross-validated pointer.

## 🔤 Sequence — character scale (letters ≈ bases)

Shipped (v1.3): corpus alphabet profile, letter-density explorer + bearer
enrichment null, letter information theory (entropy, KL, redundancy).

Value-adds:
- 🔜 **Letter n-gram models.** Bigram/trigram letter entropy and conditional
  predictability; compare disjoint-letter openings to corpus baseline.
- 🧪 **Positional letter analysis.** Do a sūra's disjoint letters concentrate at
  verse-initial positions vs elsewhere? Permutation over positions.
- 🧪 **Compression complexity.** Per-sūra gzip/LZ ratio as a model-free entropy
  proxy; cross-checks the Shannon estimate.
- 🧪 **Letter co-occurrence network.** Which letters cluster within roots —
  bridges the Sequence scale into the existing Network tooling.
- 🧪 **Abjad / numerical sequence tests** (clearly framed as contested folklore)
  with strict permutation nulls — to contextualize/debunk, not endorse.

## 🧩 Semantic — word/root scale (roots ≈ codons, words ≈ proteins)

Shipped (v1.3): hypothesis lab (custom-family contiguity + attribute label-
permutation), root entropy, lexical richness.

Value-adds:
- 🔜 **Topic overlap.** Wire the Hypothesis Lab into the existing Topic Modeling
  page: do a custom family share topics above chance?
- ✅ **Root embeddings.** SVD of per-sūra root-frequency vectors; tests whether a
  tag's families cluster in embedding space (Semantic tab). *(Shipped: p≈0.09 —
  no shared theme even after denoising, reinforcing the positional reading.)*
- 🔜 **Vocabulary-growth curve.** First-occurrence of each root along revelation
  order (type-accumulation) — ties Semantic to Signal.
- ✅ **Multiple-testing correction.** Benjamini–Hochberg FDR across the section's
  permutation battery, on the *What it is NOT* tab. *(Shipped: contiguity survives
  at q≈0.0003; per-tag theme/length do not; the caption warns FDR ≠ confound
  control.)*

## 📡 Signal page

Shipped (v1.3): length signal + autocorrelation, root recurrence vs Poisson,
entropy spectrum (FFT) vs shuffled, verse rhythm.

Value-adds:
- ✅ **Wavelet / multiresolution** (Entropy-spectrum tab): (1) Haar detail-energy
  per scale vs a shuffle null — coarse scales (32–128 sūras) significant; (2) a
  pure-numpy Ricker **CWT scalogram** localizing variation in scale × position.
  Chose CWT over Daubechies/Symlets (those need pywt and add little on 114 points).
- ✅ **Cross-correlation of two roots' occurrence signals** (Co-recurrence tab) —
  normalized cross-correlation at ±15 āyah lags with a circular-shift null.
- 🧪 **Long-range dependence** (Hurst exponent) of the length series.
- 🧪 **Change-point detection** on the entropy series.

## 🧬 Biology page

Shipped (v1.3): base composition, codon-usage Zipf, di-codon bias vs shuffled,
sequence complexity.

Value-adds:
- ✅ **Markov memory** (Markov-memory tab) — conditional entropy of the letter
  (base) stream at orders 0–3 vs a within-word shuffle. *(Chose conditional
  entropy over AIC: the 1701-root alphabet makes Markov param-counting explode;
  the letter alphabet is small enough to estimate reliably. Observed 4.09→0.41
  bits vs shuffled 4.09→1.90 — real intra-word memory.)*
- 🧪 **Tri-codon bias** and higher-order k-mer tables.
- 🧪 **Sequence-alignment analogue.** Needleman–Wunsch on two sūras' root streams
  to surface conserved motifs (parallel passages).
- ✅ **Sūra phylogeny.** Sūras clustered by top-50 codon-composition (Ward) into a
  dendrogram — a "tree of chapters" by vocabulary (Sequence-complexity tab section).

---

## 🏗 Cross-cutting platform work (enables everything above)

- 🏗 **Shared stats kernel (`twobooks_stats.py`).** Entropy, KL, permutation
  nulls, and per-sūra builders are currently duplicated across the three pages.
  Extract them once so results can never drift between pages. *Shipped: `twobooks_stats.py` now holds `shannon_bits`, `perm_p`, `benjamini_hochberg`,
  the per-sūra builder, the muqaṭṭaʿāt membership/LETTERS_OF (single source — the
  DL page imports them), and the cross-domain `two_books_battery`.*
- ✅ **Global FDR dashboard.** Kernel `two_books_battery` runs one representative
  test per domain (Position/Sequence/Semantic/Signal/Biology); a dedicated **FDR
  Summary** page applies Benjamini–Hochberg across all of them. All tests live in
  the shared kernel, so the summary and the page tools cannot drift.
- 🏗 **Reproducibility.** Surface the RNG seed and let users export the full null
  distribution behind any p-value.
- 🏗 **Performance.** Precompute per-sūra stats once at corpus load (cached) and
  share across pages.
- 🏗 **Consistency surfaces (v1.3).** One Help page with a dedicated Two Books
  section (single source of truth) + per-page inline captions; per-page
  "⬇ Export this analysis" buttons (corpus-scoped, separate from the root-query
  Export). Decided against per-category Help/Export forks — they multiply
  maintenance and invite drift.

## Sequencing

1. **v1.3 (now):** ship the three pages + three-category DL layout; make Help and
   Export consistent (Two Books section in Help, per-page export buttons).
2. **v1.4:** the shared stats kernel refactor + FDR correction (pay down the
   duplication debt before adding more tests).
3. **v1.5+:** the 🔜 items per category; 🧪 items as research spikes behind a
   clearly-labeled "experimental" expander.
