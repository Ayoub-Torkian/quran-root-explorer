# Background miner — Āyah thread (autonomous, scheduled every 6h)

Runs the next queued probe each cycle, gates it (G0–G7), logs the result here.
**Pings the user ONLY when a probe clears grade >90.** Otherwise it just logs and moves on.

| time (UTC) | probe | headline result | grade | verdict |
|---|---|---|---|---|
| 2026-06-12 06:25 | (baseline) L27 āyah recoverability | AUC 0.967, F1 0.73; closure-lexicon 16 forms = 80% of ends | 91 | banked |
| 2026-06-12 06:40 | P1 length-aware + rare/dual suffixes | recall 0.65→0.76, F1 0.749, AUC 0.967 | — | improves L27 recovery, still <0.85 sufficiency |
| 2026-06-12 06:48 | P4 āyah onset register | onset diffuse: top-12 openers=27% (vs closure 76%); strong markers ولقد 87x, واذا 43x | — | āyah bracketed ASYMMETRICALLY (sharp close, weak open); not >90; refines L27 = closure-defined unit |
| 2026-06-12 07:05 | ORDER-INVARIANCE scrutiny of L27 | word-only AUC 0.939 vs full 0.957 (context +0.018) | 84 | DEMOTED: morphological closure-lexicon, order-invariant, = fāṣila -> G7 fails. Pulled from ledger table. |
| 2026-06-12 07:25 | neighbour-syntax closure (G4b scrutiny) | AUC 0.816 but F1 0.36; collapses to trivial و/ف conjunction (prec 0.19) | — | NOT a discovery; auto-flag killed by scrutiny; āyah reduces to rhyme |
| 2026-06-12 08:00 | epidemiology/wave dynamic (gap-AC vs renewal null) | gap-AC1=0.054, paired Δ+0.083 t=9.2 | — | significant but TINY (<0.20 G5 floor); reduces to passage clustering; not >90 |
| 2026-06-12 08:20 | NEW INSTRUMENT: RMT eigenvalue-spacing ⟨r⟩ | observed 0.521 vs null 0.534 (z=-0.73); both ~GOE (Wishart artifact) | — | null; non-discriminating instrument; not >90 |
| 2026-06-12 08:35 | NEW: Marchenko-Pastur modes | 39 modes above bulk (null ~0) | — | real but ≈ topic structure (G7 redundant) |
| 2026-06-12 08:35 | NEW: MDL compression vs Markov-2 | real/surrogate gzip = 0.836 | — | real but ≈ known repetition/propagation A3/L08 (G7 redundant) |
| 2026-06-12 08:55 | 2-D intra-verse field (x=word-pos, y=verse) | full-verse gradient r=0.116; MIDDLE-only r=-0.037 (t=-7.7, sub-floor) | — | collapses to onset/closure extremes; no interior structure; not >90 (word-info proxy; no root-position alignment in data) |
| 2026-06-12 09:20 | root 2-D fingerprints (intra/inter/combined) | intra z=33 (not freq, corr -.12); inter z=30; combined |corr| 0.16 | — | real & strong but: intra=Arabic syntax+known rhetoric (G0 untestable w/o rooted baseline), inter=Meccan/Medinan themes (G7), combined=product (no emergent). Not >90 |
| 2026-06-12 10:10 | Step1 TDA persistent homology (sūra cloud) | H1 total 0.61 vs null 0.016 z=34, 24 loops | — | G7 FAIL: loops live in topic subspace (rank-10 projection reproduces them, 4.6>0.6). = topics. Not >90 |
| 2026-06-12 10:20 | Step2 MDS fingerprint families | corr(fp,co-occ)=0.46; corr(fp,territory)=0.59 | — | fingerprint families = territory+position marginals (known); not beyond. Not >90 |
| 2026-06-12 10:25 | Step3 FINAL SYNTHESIS | spatial program resolves to 3 known structures (position/territory/cohesion); 2-D=product | — | NO new >90; mature map. See FINAL_ANALYSIS_OUTCOME.md |
| 2026-06-12 11:10 | WHOLE-analysis variance decomp (312 roots) | product-of-marginals explains 45%→78% as count rises (rest = Poisson sparsity); residual SVD z=29 but only 1.3× null | — | sparsity-driven; flags a real coupling for scrutiny |
| 2026-06-12 11:25 | position×territory COUPLING (Cramér's V, high-count) | RAW V=0.16; within length-strata V=0.246 (NOT length); vs pos↔territory shuffle null z=10.9 | — | REAL coupling, above 0.20 floor, length-robust — promoted to full battery |
| 2026-06-12 11:40 | DENSIFY (Gaussian fields) + MI(pos;territory) | mean MI 0.008 nats; z 3.7→2.0 as roots added; only ~50% of high-count roots z>3 | — | coupling real but WEAK & non-universal; densify doesn't amplify |
| 2026-06-12 11:55 | DECISIVE novelty gate: global-register-controlled residual | raw V 0.243; residual after removing GLOBAL register gradient = 0.307 ≈ x-shuffle null 0.315 (Δ=−0.008); drift ρ=−0.01 | — | G7 FAIL: coupling is ENTIRELY one global register gradient (=territory/themes+length); ZERO root-specific migration. Not >90 |
