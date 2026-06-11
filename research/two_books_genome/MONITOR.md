# MONITOR — scenario leaderboard (live)

_Operational log of the scenario sweep. CPU only. GPU folding oracle is deferred until
PROGRESS ≥ 70% (user rule). Objective = Δ / progress over the control battery, on a
held-out split (per SCENARIOS.md), NEVER raw resemblance._

## Progress scale (anchored)
- **0%** = best control under the identical search (shuffled Qur'an / other language).
- **100%** = real held-out protein vs the real reference (the floor; ≈0.001 KL — sound).
- PROGRESS = (control_baseline − Qur'an) / (control_baseline − floor) × 100.
- **70% = the gate** to bring in the GPU folding oracle. Below it, stay on CPU.

## Reference (fixed once)
Real-protein dipeptide reference built from CCDS: 2.14M real amino acids (≈4,806 CDS).
FLOOR = 0.0012 (validates the objective: real protein ≈ the reference).

## Leaderboard
| # | scenario | objective | Δ (control−Qur'an) | PROGRESS | verdict |
|---|---|---|---|---|---|
| S1 | backward · char→AA (many-to-one) · M=300 | dipeptide-KL to real protein | **−0.51** | **−65%** | NULL — Qur'an far *less* protein-like than its shuffle/English |
| S2 | backward · char→AA · M=300 | order-2 protein-Markov log-lik | **−0.15** | mirage | NULL + **objective GAMED**: optimized maps score ABOVE real protein (−3.9 vs −4.16) by piling on common transitions. Δ stays negative (ungameable); absolute %/progress is not trustworthy here. Lesson: need an ungameable objective (diversity-constrained / discriminative / folding). |
| S3 | forward · char→codon + ORF gate · M=60→200 | dipeptide-KL (floor 0) | first run +0.13 → **−0.03 (3-seed mean)** | ~0% | NULL. A small/one-seed run flashed Δ=+0.13; hardened (M=200, 45k chars, 3 seeds) it collapsed to {−0.079,−0.031,+0.013} — a caught false positive. Shuffled Qur'an beat real in 2/3 seeds. Discipline working as intended. |
| S4 | forward · āyah start-sites · one-to-one char→codon · FULL Qur'an (4,224 āyāt), M=200 | dipeptide-KL | {ctrl-fail, −0.089, +0.012} | ~0 | NULL. User's start-site hypothesis given a fair full-scale test: no powered lead; within-āyah shuffle matches/beats Qur'an; English control unstable. |
| S6 | backward · real protein→AA→char · M=150 | char-bigram KL to Qur'an | Δsrc {−0.379,−0.070,+0.014} | ~0 | NULL. Real protein lands on Qur'an-like text no better than shuffled protein; matches Qur'an COMPOSITION not ORDER (real→Qm KL < real→Q). |

**Tally: 6 scenarios, 6 held-out nulls.** Across backward (2 objectives), forward+ORF,
āyah start-sites (full scale), and backward-from-real-proteins. No configuration beats the
control battery on held-out data. Converges with RESULTS.md (Route B).

## CAPSTONE — folding oracle (ESMFold, 2026-06-09)
Generated proteins from characters (fixed frequency-rank mapping; `make_proteins.py`) and
folded the short suras on ESMFold (ColabFold). Al-Ikhlas (47aa) and An-Nas (80aa):
**pLDDT ≈ 30–45 across the chain** — the disordered/random band. Real proteins fold at
70–90. PAE mostly red (no defined 3-D arrangement); contacts hug the diagonal (local only).
Al-Ikhlas shows one short N-terminal helix (pLDDT~65 for ~12 residues) — a generic local
feature, not a fold. **Verdict: the character-derived proteins do not fold.** The strongest
structural-biology oracle confirms the CPU cascade and Route B. The two books do not share a
sequence-level code. (Scope: the specific letter→DNA→protein cipher; nothing about the text
as scripture.)

Reading: real protein has near-unbiased local statistics (floor≈0); shuffling text moves
toward that; real linguistic ORDER is specifically un-protein-like, so ordered text scores
worst. Consistent with RESULTS.md (Route B). Nowhere near the 70% gate.

## Re-steer queue (CPU)
1. **Objective swap (priority).** dipeptide-KL punishes ALL language order and may not track
   foldability. Try CPU foldability proxies: hydrophobicity patterning / amphipathic
   periodicity; Chou–Fasman secondary-structure propensity mix; low-complexity/disorder
   fraction; and (if feasible on CPU) small protein-LM (ESM-2 8M) pseudo-perplexity.
2. **Route:** forward (char→codon→ORF gate→protein) vs backward (current). Forward adds the
   Stage-C ORF checkpoint.
3. **Granularity:** 1 char=codon, 2 chars=codon, 3 chars=codon — per expressibility, codon-
   level keeps āyāt expressible.
4. **Mapping constraint:** one-to-one char→codon vs many-to-one char→AA.
5. **Unit:** āyah / multi-āyah / sūra; start-site at āyah/sūra boundary.

Each scenario logged here with Δ, progress, held-out + robustness flags, and family-wise
correction across the total scenarios tried.
