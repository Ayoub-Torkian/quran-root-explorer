# Āyah-thread research queue — worked top-down by the background miner

Goal: push the Āyah from "recoverable" (L27, F1 0.73) toward **sufficiency** (recall ≥0.85), and find any
new >90 on the same thread. One probe per cycle. Each: build feature/test, gate G0–G7, log a BG_MINER_LOG row,
mark done. No overclaim — only >90 surfaces to the user.

- [x] P1 — Length-aware + rare/dual-suffix features (target the missed 20%: short verses, off-lexicon ends).
       Re-grade L27 recall; if recall ≥0.85 at decent precision → Āyah-to-sufficiency upgrade.
- [ ] P2 — Per-sūra rhyme-scheme typing, then recover the hard 20% within each scheme.
- [ ] P3 — CRF / sequence decode with a learned per-sūra āyah-length law (vs the global prior used so far).
- [x] P4 — Āyah-internal onset register (does an āyah open in a distinct register, à la sūra L18?).
- [ ] P5 — Robustness: re-run L27 across an alternate orthography / split to confirm AUC holds (G6).

Notes / hypotheses live here as the miner learns.
