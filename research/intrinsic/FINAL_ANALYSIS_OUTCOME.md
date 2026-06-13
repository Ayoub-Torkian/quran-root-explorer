# Final analysis outcome — root spatial distribution program (2026‑06‑12)

## What we did
Treated each root's occurrences as a spatial object in the muṣḥaf — a 1‑D signal (along the 6,236 āyāt),
a 1‑D intra‑āyah position distribution, and a 2‑D fingerprint matrix (position‑in‑āyah × muṣḥaf). Surveyed
the full instrument toolbox against it, every test under the locked gates (incl. G4b order/invariance +
known‑measure ablation, and the G5 effect floor).

## The decomposition — everything resolves to THREE structures
1. **Verse‑position law** (where a root sits *within* the āyah): onset = function words, closure = rhyme/
   grammatical suffixes. → already **L06 (fāṣila), L18 (onset), L26/L27 (closure)**. Order‑invariant (it's
   word‑form, not sequence).
2. **Large‑scale territory** (where a root sits *across* the muṣḥaf): broad regional concentration.
   → **topics/themes**. Detected identically by wavelet (excess at 256–512 āyāt), TDA H1 loops (live in the
   rank‑10 topic subspace), Marchenko–Pastur (39 modes), inter‑verse variance (z=30).
3. **Mid‑scale passage cohesion** (roots recur within a passage): → **membrane / internal weave (A1, A2)**.
   Detected by Taylor's law (β=1.22, collapses to 1.0 when āyāt are shuffled — i.e. arrangement‑driven),
   gap‑autocorrelation (tiny), folding.

The **2‑D fingerprint = structure‑1 × structure‑2** (FFT/SVD null; intra⊥inter, corr 0.16): no emergent
diagonal/joint coupling. The map is the product of two independent 1‑D laws.

## Instruments run (all gated, none new)
FFT(2‑D)→null · SVD→rank‑1 · Radon→0°/90° only · wavelet→territory · Taylor→cohesion(G7) ·
autocorrelation→sub‑floor · RMT→null · Marchenko–Pastur→topics(G7) · MDL→repetition(G7) ·
**TDA persistent homology→topics(G7)** · **MDS fingerprint families→territory+position** · classifier→L27 demoted.
Untouched only: nothing material (Ripley/Moran/Getis/LISA already in app).

## Verdict
**No new >90 from the spatial‑distribution program.** The root area distribution is genuinely non‑random and
specific to the arrangement (confirmed against the text's own shuffle, z=30–34), but every structure it carries
is already named in the ledger (rhyme, topics, cohesion). The instruments differ; the structure they find is one.
This is a *mature map*, not an instrument failure and not textual absence — the three laws above ARE the structure.

## Assets produced (descriptive, not ledger discoveries)
- **Root distribution atlas** (`root_atlas.png`, `root_fingerprints.png`) — geochemical‑style abundance maps.
- **Taylor's‑law narrative** — the muṣḥaf obeys Var∝Mean^1.22 that a shuffled text does not (β→1.0).
- **`INSTRUMENT_ASSESSMENT.md`** — the full toolbox × data‑representation matrix.

## Addendum (2026‑06‑12, exhaustive coupling battery — sharper instrument, same landing)
The earlier "2‑D = product of marginals, corr 0.16" was the *crude* test. Re‑ran it rigorously after densifying:
- The **position×territory coupling is REAL** — Cramér's V = 0.243, length‑robust (within‑length V=0.246), z=10.9
  vs a proper position↔territory shuffle null. It briefly looked like the first floor‑clearing lead in a while.
- **Decisive novelty gate killed it cleanly.** Remove the single **global register gradient** (the whole text's
  intra‑verse usage shifting across the muṣḥaf, pooled MI=0.0138 nats) and the per‑root **residual coupling = 0.307
  ≈ the shuffle null 0.315** (Δ=−0.008). Directional drift ρ=−0.01. → **No root carries its own territory‑dependent
  migration.** The entire coupling is one global gradient = verse‑position law × territory (= themes + verse‑length),
  both already named. **Not >90.**
- Net: the 2‑D fingerprint really is the product of the two 1‑D laws — now confirmed by the *rigorous* register‑control
  decomposition, not just the crude correlation. The spectrum is exhausted; the three‑structure map holds.

## Session safeguards (carried forward)
- L27 corrected: 91 → **84**, removed from the ledger table (order‑invariant = fāṣila).
- **G4b locked** in DISCOVERY_CRITERIA: no ≥90 without an order/invariance test + known‑measure ablation.
- Complete negative/bound record in `BG_MINER_LOG.md` + `JOURNEY_LOG.md` — nothing cherry‑picked.
