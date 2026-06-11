# Quran Root Explorer — v1.3 changelog

Builds on v1.2. v1.3 introduces the **Two Books** section: reading the same
validated corpus not only as a root-network, but as an ordered *sequence* and a
*genome*-style object — always with explicit permutation/Poisson nulls and
length-confound disclosure. No "scientific-miracle" claims.

## New pages (Two Books nav group)

- **🔠 Disjoint Letters** (`pages/8g_Disjoint_Letters.py`) — the al-Muqaṭṭaʿāt
  pointer explorer **plus** a hypothesis-testing workbench, reorganized into
  three scale-based categories:
  - 🧭 **Position — index geometry:** family explorer · label-permutation
    contiguity (muṣḥaf + nuzūl, p≈2×10⁻⁵) · organization/length (median 85 vs 26)
    · theme null · verdict scorecard.
  - 🔤 **Sequence — character scale (letters≈bases):** corpus alphabet profile ·
    letter-density explorer with bearer-enrichment permutation (generalizes the
    ق lead) · letter information theory (entropy, KL-divergence, redundancy).
  - 🧩 **Semantic — word/root scale (roots≈codons, words≈proteins):** Hypothesis
    Lab (build any sūra family → live contiguity null; attribute label-
    permutation generalizing the length p≈0.29) · root entropy · lexical richness.
- **📡 Signal** (`pages/8h_Signal.py`) — the corpus as a 1-D signal: sūra-length
  autocorrelation, root recurrence vs a Poisson null, per-sūra entropy spectrum
  (FFT) vs a phase-shuffled null, and verse-length rhythm.
- **🧬 Biology** (`pages/8i_Biology.py`) — the genome metaphor: base (letter)
  composition, codon (root) usage with a Zipf fit, di-codon bias vs a shuffled
  stream, and sequence-complexity (length-confound made explicit).

## Structure & navigation

- Two Books pages registered in `state.py` → `NAV_SECTIONS` under "📚 TWO BOOKS".
- Disjoint Letters tabs grouped under three named categories (Position ·
  Sequence · Semantic) after design review — replacing a flat 7-tab row.

## Consistency

- **Help** extended (single source of truth, not forked): Two Books concepts,
  glossary terms (muqaṭṭaʿāt, permutation null, contiguity, KL-divergence,
  redundancy, lexical richness, Zipf, base/codon/protein mapping, enrichment),
  and page-tour entries for Disjoint Letters / Signal / Biology.
- **Export:** per-page "⬇ Export this analysis" buttons on each Two Books page
  (corpus-scoped CSV tables), kept separate from the root-query Export workflow.

## Validation

- `streamlit.testing.v1.AppTest` passes with 0 exceptions on the new pages,
  `app.py`, and existing pages, including every button-gated permutation path.
- Headline numbers reproduced: muṣḥaf contiguity p≈5×10⁻⁵, median verses 85 vs
  26, length-attribute p≈0.29, root Zipf slope ≈ −1.56.

## Notes

- Folder is still named `_v1.2` on disk; rename to `_v1.3` is a manual step
  outside the app. See `ROADMAP_TwoBooks.md` for what comes next (shared stats
  kernel, FDR correction, per-category value-adds).

## Post-1.3 increments (unpublished, still 1.3)

- **Shared stats kernel** `twobooks_stats.py` — `shannon_bits`, `perm_p`, and the
  per-sūra letter/root builder extracted from the three pages (rule-of-three on
  `shannon_bits`); dropped the dead `WORDS` variable. Behavior-preserving.
- **Leave-one-out robustness** (Position → Contiguity): drops each multi-family
  sūra in turn and re-runs the muṣḥaf null. Worst-case LOO p ≈ 0.0002 — the
  contiguity finding survives removing any single sūra.
- **Benjamini–Hochberg FDR** (`twobooks_stats.benjamini_hochberg`) + a test-battery
  dashboard on the Disjoint Letters *What it is NOT* tab: runs contiguity, theme,
  per-tag length, letter/root entropy, lexical-richness and ق-enrichment nulls,
  then shows raw p vs BH-FDR q. Contiguity survives (q≈0.0003); the caption notes
  FDR controls multiplicity, not confounding.
- **Signal · Co-recurrence tab** — normalized cross-correlation of two roots'
  āyah-occurrence signals (±15 lags) with a circular-shift null on the peak.
- **Biology · Markov-memory tab** — conditional entropy of the letter (base)
  stream at orders 0–3 vs a within-word shuffle, showing real intra-word letter
  dependence (4.09→0.41 bits observed vs 4.09→1.90 shuffled). Conditional entropy
  was chosen over AIC Markov-order selection because the 1701-root alphabet makes
  parameter counting explode; the small letter alphabet estimates reliably.

## Data-driven integrity pass

Removed hardcoded/cited statistics from the Disjoint Letters page so every number
is computed live from the corpus ("the data talks for itself"):
- **Per-family contiguity bar** — was a frozen `[5.0, 2.05, 5.0, 1.47]`; now computes
  each family's p live vs random same-size subsets (button-gated).
- **Scorecard** — was statically typed verdicts; now every row is computed on demand
  (contiguity, theme, per-tag length via permutation; medians, ق-rank, letter
  enrichment from the data) with verdicts derived from the live p-values.
- **Organization chart title** — medians now interpolated from data, frozen p removed.
- **Correction surfaced by the data:** the old "Letter-frequency code: 0/29 sūras"
  was inaccurate; the live scan shows **1/14 disjoint letters (م) enriched** in its
  bearers (a frequency artifact) — the scorecard now reports the measured count.
- **Verified against data:** 28/29 muqaṭṭaʿāt openings appear in āyah 1 directly in
  the text (sūra 42's second set عسق is in āyah 2) — the family list is corpus-
  consistent, not an external assumption. No external chronology is fabricated;
  nuzūl analyses use only the revelation-order column present in the sheet.
- **Help case-study converted to live computation.** The ظلم·عدل·رحم worked
  example now computes every figure from the corpus on load (cached `_cs_live`),
  replacing hardcoded numbers and chart arrays. This surfaced and fixed two stale
  errors in the old static version: the network was mislabelled (live: 18 nodes,
  **152 edges, 800 triads**, not 147/735) and the density table **omitted the true
  top sūra, S49 at 33.3%**. Frequency/PMI/Jaccard figures were already accurate and
  now recompute live. Also stripped the last course-cited p-values (0.27/0.29) from
  the Disjoint Letters captions so only live numbers appear.
- **Biology · sūra phylogeny** — sūras clustered by their top-50 codon (root)
  composition via Ward linkage into a dendrogram (added as a section in the
  Sequence-complexity tab, not a new tab, to keep the tab count disciplined).
- **Disjoint Letters · embedding-space theme test** (Semantic) — SVD of per-sūra
  root-frequency vectors; within-family cosine distance vs a label-permutation
  null. p≈0.09: families do not cluster even after denoising — a stronger negative
  than the raw-profile theme test, reinforcing the positional-pointer reading.
- **FDR battery made cross-domain** — added a Signal-domain sūra-length
  autocorrelation test to the Benjamini–Hochberg battery so multiplicity is
  corrected across Position/Sequence/Semantic/Signal in one view.

## Global FDR + kernel-isation

- **`twobooks_stats` is now the single source** for the muqaṭṭaʿāt membership
  (`MUQ_FAMILIES`, `MUQ`, `MUQ_SIZES`, `LETTERS_OF`, `DISJOINT_LETTERS`) — the
  Disjoint Letters page imports them instead of redefining (UI colours/labels stay
  on the page). Verified the refactor changed no results (DL deep tests unchanged).
- **`two_books_battery(corpus, ndraw)`** added to the kernel: one representative
  permutation test per domain (Position contiguity ×2, Sequence letter-entropy,
  Semantic theme + root-entropy, per-tag length, Signal length-autocorrelation,
  Biology di-codon structure).
- **New page `8j_Two_Books_Summary.py` (FDR Summary)** — runs the battery and
  applies Benjamini–Hochberg across all domains in one view; registered in the
  Two Books nav group. Contiguity (both orders) + Signal/Biology structure survive;
  per-tag theme (q≈0.06) and per-tag length (q≈0.31) do not.
- **Signal · Haar wavelet multiresolution** (Entropy-spectrum tab) — pure-numpy
  Haar transform of the per-sūra entropy series; detail energy per scale tested
  against a shuffle null. Result: coarse scales (32–128 sūras) carry significant
  energy (slow trend, p<0.001) while fine scales sit at/below chance (no local
  periodicity). No external wavelet library; caption corrected to match the data.
- **Signal · Ricker CWT scalogram** (Entropy-spectrum tab) — pure-numpy continuous
  wavelet transform; heatmap of |coefficient| over scale × sūra-position, localizing
  where the entropy variation sits (not just at which scale). Chosen over discrete
  Daubechies/Symlets, which need an external library and add little on a 114-point
  series; no new dependency.

## Publishing & courses

- **Help · new "🧭 Two Books" guide tab** — how to use Disjoint Letters / Signal /
  Biology / FDR Summary, plus how to read permutation p-values, null histograms,
  BH-FDR q-values, the length confound, and the scalogram. Single Help page (no fork).
- **Publishing plan:** ship v1.3 as current, keep v1.2 frozen as a reference snapshot
  so existing lectures stay valid while courses are updated.
- **Course-update impact (v1.2 → v1.3):** root-tools pages unchanged (root course safe);
  Disjoint-Letters course needs a walkthrough update (4 flat tabs → Position/Sequence/
  Semantic workbench); any slide citing the old Help case-study network numbers
  (147 edges / 735 triads) must update to the corrected live values (152 / 800) and the
  density top now includes S49 (33.3%); Signal/Biology/FDR are new and now covered by
  the in-app guide tab.

## Deep Dives — sense-cohesion + concept IMRaD (2026-06-04)
- Concept plain-language report rewritten to full IMRaD, mirroring the ayah plain
  report: Abstract · Introduction · Method · Results (one compact companion table:
  relation | concept | meaning | territory | shape) · Discussion · Limitations ·
  Conclusion.
- New gated **sense-cohesion** signal in all three concept registers: mean pairwise
  Jaccard of the per-surface-form co-locator sets decides cohesive / mixed / split,
  reported as one sentence (plain) or quantified with the Jaccard (technical). Gated
  on >=2 high-mass forms each with >=2 significant co-locators; says nothing when too
  sparse. Surface-only associations are never listed (kept to the form-robust core),
  honouring the pipeline's root-vs-surface verification epistemics. Worked example
  قلب -> split (Jaccard 0.02): heart vs the turning/overturning verbal forms.
- **Ayah deep dive deliberately unchanged.** The ayah is analysed as a root-level,
  multi-root entity (idf-weighted centroid of its roots); there is no single root
  whose surface forms could be examined, so the concept-style cohesion signal has no
  analog. A cross-verse "verbatim echo" would duplicate the lexical axis, risk
  reproducing verse text, and be mostly empty — rejected on a data/architecture basis.
- Pruned orphaned report helpers (_concept_type_note, _roots6).
