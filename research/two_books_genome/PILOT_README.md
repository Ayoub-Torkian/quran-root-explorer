# Route-B pilot — results & honest read (2026-06-08)

**Status: PLUMBING / CALIBRATION ONLY. Not a claim. Not a result for the thesis.**
The pilot exists to prove the mapping-free structural pipeline runs and that the
controls behave correctly. Arabic Qur'an was NOT used here (see note below); the
language modality stand-in was English prose (the repo's own .md docs), which is
also the "same raw gradient" (Shakespeare) point made in discussion.

## What ran
- `scripts/route_b_pilot.py` — no invented cipher. Computes dimensionless structural
  signatures and compares real vs shuffled vs random within and across modalities.
- Biology: 6 human RefSeq CDS (INS, HBB, TP53, ACTB, GAPDH, ALB) = 5,925 nt.
- Language: English prose, 308,948 letters (+ a CDS-length slice for fair length).
- Results: `scripts/results_pilot_2026-06-08.json`.

## What it showed (reads, not claims)
1. **The controls behave.** Shuffling destroys structure, as it must:
   - Genome local correlation MI(d=1): real **0.060** → shuffled **0.001** bits.
   - Language local correlation MI(d=1): real **0.47** → shuffled **~0** bits.
   - gzip compressibility: English **0.345** vs its shuffle **0.595** (language is
     highly ordered); CDS **0.313** vs shuffle **0.326** (DNA is only weakly ordered
     beyond composition).
2. **Both modalities are non-random and shuffle-destroyable** — they share the
   *structural class* "not i.i.d." Real CDS keeps a small positive long-range MI
   (d=20–50 ≈ 0.001–0.002) that the shuffle removes; English does too (weakly).
3. **But the strength and shape differ markedly** (English MI(d1)=0.47 vs DNA 0.06;
   very different Zipf slopes). So the pilot does **NOT** establish a specific
   quantitative correspondence between language and genome — only that the comparison
   is feasible and the pipeline + nulls are correct.

## The honest caveat this surfaces (the whole ballgame)
"Both are structured" is easy and generic — exactly the `CHALLENGES.md §2.5`
concern in live numbers. Establishing a *specific* correspondence requires the real
confirmation run, not this pilot:
- longer, larger genome sample (the 6-CDS set is short ⇒ long-range MI is noisy;
  note the CDS-length English slice goes negative at d=20–50 from finite size);
- formal exponent fits (DFA Hurst, MI-decay power law) **with error bars**;
- length-matched comparison and **replicate languages incl. Arabic Qur'an**;
- the decisive test: does language resemble the **real** CDS structure more than a
  **structure-matched surrogate** genome — beyond just "both are non-random".

## Confirmation-grade run (2026-06-08) — `scripts/route_b_confirm.py`
Formal exponent fits with chunk-based 95% CIs (`results_confirm_2026-06-08.json`).
mean ± CI, chunkLen=1000:

| sequence | gzip | Hurst (DFA) | MI_gamma (I(d)~d^-γ) |
|---|---|---|---|
| CDS_real | 0.350±0.003 | 0.539±0.050 | 0.491±0.331 |
| CDS_shuffled | 0.364±0.002 | 0.495±0.031 | 0.145±1.053 |
| English | 0.525±0.006 | 0.495±0.018 | 1.906±0.226 |
| English_shuffled | 0.589±0.001 | 0.492±0.014 | −0.776 (degenerate) |

**Honest read:**
1. **The machinery is validated.** Shuffling collapses the structure signals
   (the gzip gap, and MI_gamma turns to noise/degenerate). Error bars are produced.
2. **It does NOT show a shared language↔genome signature — if anything they look
   different.** English MI decays sharply (γ≈1.9, tight CI); the genome's MI decays
   slowly but with a huge CI (γ≈0.49±0.33). DFA Hurst: genome marginally >0.5,
   English ≈0.5 at this scale. So "both are non-random" holds, but their long-range
   *exponents do not match* — the opposite of what a shared-structure claim needs.
3. **The genome sample is far too small** (6 genes, 5 chunks ⇒ exponent CIs huge).
   No firm statement about genome exponents is possible until the whole RefSeq CDS
   is used. This is the dominant limitation, not a result about the thesis.

Net: a faithful, slightly negative-leaning pilot — exactly the honest-null posture
the project demands. The apparatus is ready; the data is not yet sufficient.

## Next steps
1. ~~Find the Qur'an endpoint~~ DONE — `parsquran.com` verified; run
   `scripts/fetch_parsquran.py` locally to build `data/quran/quran_arabic_concat.txt`.
2. Re-run `route_b_confirm.py` with: Arabic Qur'an + English + ≥1 more language; the
   WHOLE RefSeq CDS (not 6 genes); larger chunk lengths to probe true long-range scales.
3. Only if language robustly matches the real genome's structure beyond the shuffled
   surrogate (overlapping exponent CIs, both separated from shuffles) does Route A (the
   searched letter→codon BLAST test) become worth running.
