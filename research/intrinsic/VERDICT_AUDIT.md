# Verdict audit — MEASURED vs INFERRED re-tagging of every probe (2026-06-12)

Purpose: expose which "reduces to known → not >90" calls were actually **measured** and which were **asserted**
(INFERRED). An INFERRED dismissal does **not** close a candidate — it reopens it. Substrate tagged throughout:
**WORD** = rasm words (has morphology/function-words/fāṣila) · **ROOT** = content-roots only (NO grammar).

| # | probe | the NUMBER (measured) | the VERDICT's attribution | tag | substrate | status |
|---|---|---|---|---|---|---|
| 1 | L27 āyah recoverability | AUC 0.967, F1 0.73 — **[MEASURED]** | "self-marking unit" | mixed | WORD | number solid; meaning fair |
| 2 | P1 length-aware suffixes | recall 0.65→0.76 — **[MEASURED]** | "still <0.85 sufficiency" | MEASURED | WORD | solid |
| 3 | P4 onset register | openers 27% vs closure 76% — **[MEASURED]** | "= closure-defined unit" | INFERRED | WORD | reframe, not measured |
| 4 | order-invariance of L27 | word-only 0.939 vs full 0.957 — **[MEASURED]** | "= the fāṣila" | INFERRED | WORD | reduction asserted; defensible on WORD only |
| 5 | neighbour-syntax closure | precision 0.19 — **[MEASURED]** | "trivial و/ف conjunction" | MEASURED | WORD | solid |
| 6 | epidemiology gap-AC | Δ+0.083, <0.20 floor — **[MEASURED]** | "= passage clustering" | INFERRED | ROOT | tiny is measured; the label is not |
| 7 | RMT eigen-spacing | z=−0.73 null — **[MEASURED]** | "non-discriminating" | MEASURED | ROOT | solid null |
| 8 | Marchenko–Pastur modes | 39 modes vs ~0 — **[MEASURED]** | **"≈ topic structure"** | **INFERRED** | ROOT | **never measured vs a topic model — REOPEN** |
| 9 | MDL compression | gzip 0.836 — **[MEASURED]** | **"≈ A3/L08 repetition"** | **INFERRED** | ROOT | **equivalence asserted, not tested — REOPEN** |
| 10 | 2-D intra-verse field | middle r=−0.037 — **[MEASURED]** | "no interior structure" | MEASURED | WORD-proxy | solid (but word-info proxy) |
| 11a | root fingerprint INTRA | z=33 vs shuffle — **[MEASURED]** | **"= Arabic syntax + rhetoric"** | **INFERRED — WRONG** | ROOT | **no grammar in roots; reduction invalid — REOPEN** |
| 11b | root fingerprint INTER | z=30 vs shuffle — **[MEASURED]** | **"= Meccan/Medinan themes"** | **INFERRED** | ROOT | **never measured vs a theme model — REOPEN** |
| 11c | fingerprint COMBINED | FFT/SVD null — **[MEASURED]** | "= product of marginals" | MEASURED | ROOT | solid |
| 12 | TDA persistent homology | rank-10 proj 4.6 > 0.6 — **[MEASURED]** | "loops live in topic subspace" | MEASURED | ROOT | reduction WAS measured |
| 13 | MDS fingerprint families | corr 0.46 / 0.59 — **[MEASURED]** | "= territory+position" | MEASURED(moderate) | ROOT | corr is moderate, not decisive |
| 14 | position×territory coupling | V=0.243, z=10.9, length-robust — **[MEASURED]** | (promoted) | MEASURED | ROOT | solid signal |
| 15 | register-control residual | residual 0.307 ≈ null 0.315 — **[MEASURED]** | "= one global register gradient" | MEASURED | ROOT | decisive — this dismissal IS measured |

## Tally
- **MEASURED dismissals (genuinely closed):** order-invariance, neighbour-syntax, RMT, fingerprint-combined,
  TDA topic-projection, MDS (moderate), register-control residual. These stand.
- **INFERRED dismissals (asserted, NOT closed → reopened):** **MP modes ≈ topics (#8)**, **MDL ≈ A3/L08 (#9)**,
  **intra-fingerprint = "Arabic syntax" (#11a, invalid — no grammar in roots)**, **inter-fingerprint = "themes"
  (#11b, never tested vs a theme model)**, onset "= closure unit" (#3), epidemiology "= passage clustering" (#6).
- So **6 of ~15 verdicts were attribution asserted, not measured.** The strongest-sounding reductions
  (MP=topics, MDL=A3/L08, intra=syntax, inter=themes) are exactly the unverified ones.

## What this means (honest)
The "mature map / spatial program exhausted" conclusion **rested partly on INFERRED reductions**, not only
measured ones. It is therefore **not safe as stated.** The measured negatives hold; the asserted ones do not
close anything. The intra-āyah root-ordering signal (z=33) in particular was killed by a reduction (grammar)
that **cannot exist in the root substrate** — that is a reasoning error, not a finding.

## Ranked recommendation
1. **#1 — Re-run #11a (intra-āyah root ordering, z=33) as a TEST on the ROOT substrate** — does a bag-of-roots-
   with-position-bias null reproduce it, or is there genuine order information beyond position preference? No
   grammar appeal. *Why:* it was dismissed by an invalid reduction; it is the most under-examined real signal.
2. **#2 — Convert #8 and #9 into measurements** — actually fit a topic model / A3-L08 predictor and measure the
   residual, instead of asserting "≈". Either closes them honestly or reopens them.
3. **#3 — Annotate `BG_MINER_LOG` + `FINAL_ANALYSIS_OUTCOME` with these tags** so the conclusion carries its
   evidence grade on its face.

Recommend **#1**.
