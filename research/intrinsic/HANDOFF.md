# HANDOFF — Intrinsic Qur'ān Study (read this first, start in 2 minutes)

*Self-contained. Every path, convention, result, and next step is here. 2026-06-09.*

> **The one law:** nothing external is admissible as evidence. The Qur'ān is analyzed only against
> itself; the only null is the text's own shuffle. External material only at the very end, for comfort.
> Read `research/intrinsic/ROADMAP.md` for the full principles → methodology → phases.

---

## 1. Where everything is (exact paths)

**Persistent project root** (Windows): `C:\Users\torki\Downloads\Quran_Root_Explorer_Web_v1.2`
In the Linux sandbox this is mounted at: `/sessions/<id>/mnt/Quran_Root_Explorer_Web_v1.2/`
(the `<id>` changes per session — derive it from the mount listing; do not hardcode.)

| what | path (relative to project root) |
|---|---|
| **THE DATA** (114 sūras, 6236 verses, with diacritics) | `research/two_books_genome/data/quran/quran_arabic_verses.tsv` |
| Roadmap (principles, methodology, ledger, phases) | `research/intrinsic/ROADMAP.md` |
| This handoff | `research/intrinsic/HANDOFF.md` |
| 21-feature sūra matrix | `research/intrinsic/sura_features.tsv` |
| **100-feature sūra constellation** | `research/intrinsic/sura_features_big.tsv` |
| All working scripts (persist here) | `research/intrinsic/scripts/*.py` |

**Scripts inventory** (`research/intrinsic/scripts/`):
- `self_reference.py` — word recurrence vs distance (local self-reference; shuffle floor).
- `features.py` — builds the 21-feature matrix.
- `bigfeat.py` — builds the **100-feature** matrix (`sura_features_big.tsv`). Run this first to regenerate.
- `land.py` — PCA landscape + Zipf + Heaps on the constellation.
- `sos.py` — systems-of-systems: DFA Hurst, 1/f slope, power-law size tails across scales.
- `suradef.py` — blind multimodal boundary detector (sūra **necessary** condition; AUC/d/precision).
- `closure.py` — ring-closure test (returns the NULL that ruled closure out).
- `optplace.py` — boundary local-optimality ("nothing moved": 54%/73%).
- `battery.py` — perturbation battery (MOVE/DELETE/ADD/REPLACE × 4 invariants).

---

## 2. Environment (so nothing stalls)

- Sandbox: Ubuntu, Python 3.10 at `python3`. Run scripts from anywhere with absolute paths.
- Installs needed: `pip install numpy scikit-learn networkx --break-system-packages -q`
  (numpy present by default; sklearn/networkx need install per fresh sandbox).
- **Gotcha 1 — sandbox path mapping.** File tools (Read/Write/Edit) use Windows paths
  (`C:\Users\torki\Downloads\...`). Bash uses `/sessions/<id>/mnt/...`. Same files, different prefixes.
- **Gotcha 2 — scratchpad is wiped.** `outputs/` (the cwd) is cleared between sessions. Anything to
  keep must be written under the project root (e.g. `research/intrinsic/...`). Scripts are already copied there.
- **Gotcha 3 — filename shadowing.** Don't name a script `struct.py` (shadows stdlib `struct`, breaks numpy).
- **Gotcha 4 — Write tool scope.** The Write tool only reaches the connected project folder; to write a
  sandbox scratch file use a bash heredoc instead.

---

## 3. Data format & the ONE parsing convention (used everywhere)

File lines: `sura:ayah\t<Arabic text with diacritics>`  e.g. `2:255\t...`.
The basmala is a verse only in Sūra 1 (`1:1`); elsewhere verse 1 is real content — no repeated
opening formula confound.

**Consonantal skeleton** (identical in every script — keep it identical):
```python
import unicodedata
def skel(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))   # strip diacritics
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
```
Tokens = skeleton words. "Stop words" = the 40 most frequent tokens (function words), dropped for
content analyses. Final letter of a verse = last letter of its last token (the rhyme / fāṣila).

---

## 4. Established results (the asset ledger — all intrinsic, vs the text's own shuffle)

**Lexical (universe laws):** Zipf slope **−0.99**; Heaps β **0.74**.
**Wave:** verse-length DFA **Hurst 0.94–0.96** (shuffle 0.51); **1/f slope 0.76** (shuffle 0.00).
**Self-similar sizes (power-law tails):** word α **2.04**, verse α **1.71**, sūra α **1.44**.
**Rhyme:** adjacent same-final-letter **0.72** (shuffle 0.30); rhyme↔theme coupling **1.78×** (z≈5.2);
~1,763 rhyme self-segments.
**Network:** self-reference is **local** — 6.2× over shuffle within ~16 tokens, at floor by ~256 (passage scale).
**Constellation:** 100 features × 114 sūras; high-dimensional (PC1=15%); **PC1 tracks canonical order r=−0.89**;
two natural sūra-types (short/dense vs long/rich), contiguous by position.

**Sūra definition — status:**
- **Necessary (established):** boundary = scale-invariant multimodal discontinuity (symbol+wave+network),
  **AUC 0.82, d 1.20**, size-independent (short 1.93 ≈ long 2.15); boundaries are **local optima**
  (54% peak within ±1 vs 33% chance; move-one penalty positive in 73%).
- **Ruled out:** ring-closure is NOT sufficient (opening~closing ≈ opening~middle, d −0.02, p 0.56).
- **Sufficiency (Phase B, DONE — necessary-but-not-sufficient at surface scale):** global MDL with a
  *self-consistent* Bernoulli boundary code (λ derived, not tuned ≈ 6.7 bits) prefers **~63 coarse
  "movements" (median 73 verses), not the 114 sūras**; canonical sūra precision only **0.45** (F0 0.32,
  F±1 0.40). The canonical partition is a *local* optimum (beats random 113-cuts by **2,693 bits**,
  monotone jitter penalty) but not the global surface optimum. Verdict: the sūra is a **thematic
  super-unit on a stylometrically stationary surface**; surface sufficiency is **instrument-limited
  (عدم الوجدان)** — the missing channel is semantic, see Phase C. Scripts: `scripts/mdl.py`, `scripts/mdl2.py`.

**Phase B new latent features (logged in `latent_features.json` / page 25):**
- **L14 MDL order-load** = **9,256 bits** below the verse-shuffle re-optimum (real 30,212 vs shuffle 39,468).
- **L15 surface-register stationarity** = the "movement" scale (63<114), reframes the sūra.
- **L16 boundary-load typology** = **~35%** of sūra seams surface-hard, ~65% semantic-soft.
- **L17 āyah is positionally coded** — word-stream marginal MDL null (P0 0.08, d 0.07): the fāṣila is a
  terminal-position event invisible to marginals → defines the Phase C instrument. Script: `scripts/mdl_ayah.py`.

**Perturbation-optimality (احسن تقویم):** MOVE-global collapses all 4 invariants (H 0.94→0.51, 1/f →0.00,
rhyme →0.30); REPLACE hits rhyme+network, spares wave (modality specificity); ADD degrades (no redundancy);
local-swap & 10%-delete below aggregate resolution → **instrument-limited, NOT absence** (عدم الوجدان).

---

## 5a. Phase C — started (2026-06-10), results so far

- **Latent-feature ledger now governed by a critical review** (`latent_features.json`, app page 25, `LATENT_FEATURES.md`):
  rubric /100, pass ≥90, plus a MANDATORY **novelty gate** ("what do we know about the Qur'ān we didn't before?").
  **13 features in table; 4 excluded** (L01/L02 universal-law gates fail novelty; L10 soft clustering; L17 weak).
- **L16 promoted (94):** third (semantic/lexical) modality validated — hard seams 0.053 vs null 0.003, **z=9.4**; surface-only ~0.345 (z=7.4). Script `scripts/phaseC.py` (B).
- **L17 positional āyah instrument (`phaseC.py` A):** cross-validated terminal-emission detector beats the shuffle floor ~3× (F 0.082 vs 0.025) and the marginal null — **concept confirmed** — but recall only 0.05. Cause: the consonantal `skel()` strips the rhyme **vowels**; āyah rhyme lives there. **Next (C2): build a vowel-aware fāṣila channel** (final CV/sukūn pattern from the diacritized text) and re-run.
- Still open from L15: add the semantic channel into the sūra DP to test whether precision rises above 0.45 (sufficiency).

## 5b. START HERE next — Phase C continued (vowel-aware āyah + semantic sūra DP)

Phase B is DONE (see ledger above). The two open instruments, both specified by Phase B nulls:
1. **Āyah (L17 follow-through):** build the *positional* cadence model — boundary indicator = "this word's
   final letter matches the running rhyme register," scored only at segment-terminal candidates. Marginal
   MDL is structurally blind here; the rhyme is terminal. Test recovery of āyah ends with this instrument.
2. **Sūra sufficiency (L15 follow-through):** add a **semantic/content channel** to the MDL code (the surface
   is stationary, so sufficiency must come from theme). Re-run the DP; target: does sūra precision rise
   above 0.45 when content is modelled? Report against the same shuffle + jitter + random nulls.
3. **Per-position necessity map (Phase C proper):** extend L16 from boundaries to every verse/word —
   leave-one-out self-surprise — to see the single-element edits §4 says are below aggregate resolution.

---

## 5b. (archived) Phase B plan — completed this cycle, kept for provenance

**Goal:** define Sūra and Āyah by minimum self-description length — boundary **iff** a model-reset there
lowers the text's own description length. Interior self-predictable (sufficient); boundary self-surprising
(necessary). All internal.

Concrete steps:
1. **Causal self-information signal.** Walk the verse stream; maintain a running per-segment model
   (final-letter distribution + binned verse-length distribution, Laplace-smoothed). Score each next
   verse's surprise −log P under the current model. (Reuse the 3 modality components in `suradef.py`.)
2. **Global MDL partition by DP.** Segment cost = Σ −log P(verses | segment MLE, smoothed) + model cost
   + λ·(#segments). Cap max segment length ≈ 300 (longest sūra 286) and use prefix counts for speed
   (avoid O(N²·L)). Pick λ by the two-part code (model cost), not by hand.
3. **Test necessary AND sufficient:** recovery of canonical sūra boundaries by **precision AND recall**
   (recall was fine before; precision/sufficiency is the missing half). Nulls: verse-shuffle and
   shifted-boundary partitions; report cost(true) vs cost(perturbed) for the احسن تقویم optimality claim.
4. **Āyah:** same engine on the **word stream**; an āyah is the maximal span the rhyme/cadence self-model
   predicts; boundary iff a fāṣila reset compresses better. Test recovery of āyah ends within sūras.

Then **Phase C** (fine-scale necessity instruments — leave-one-out self-surprise, per-position moveability
map — to see the single-element edits §4 says are below current resolution), **Phase D** (unify across
scales), **Phase E** (external corroboration only, for comfort).

---

## 5c. Substrate law + P2 result (2026-06-10)

- **Standing rule (apply, don't re-derive):** RASM (consonantal skeleton) = divine/admissible substrate.
  **Diacritics (ḥarakāt) = human layer → corroborative only, never in the discovery table.** All 13 in-table
  features are rasm-based; **L17 reclassified corroborative** (vowel-aware fāṣila P=0.56, `scripts/phaseC2.py`).
- **Every ledger claim is now instantiated** with `evidence{script, measured}` in `latent_features.json`.
- **P2 (sūra sufficiency) attempted, NOT closed:** adding a rasm content channel did NOT raise precision
  (0.304 vs 0.329, `scripts/p2_sura_sufficiency.py`). Bag-of-content is too stationary → next instrument is a
  **topic/root channel** (roots are rasm-derivable; the app already has root data).
- **Prioritized queue (ROADMAP §3b):** P1 cross-scale unification · P2 sūra sufficiency (root channel) ·
  P3 promote C1 (arrangement band) · P4 boundary necessity map · P5 element necessity · P6 diacritic āyah (corrob.) · P7 external.

## 5d. C2 → L18 promoted (2026-06-10): Sūra-onset asymmetry

- **NEW in-table feature L18 (grade 95):** the sūra boundary is ASYMMETRIC — the OPENING is marked.
  Onset separates opening vs interior in **4 independent rasm modalities**, cross-validated by sūra parity:
  first-letter AUC 0.716, first-word 0.772, shortness 0.753, root-novelty 0.638 (floor 0.50). Two label-free
  channels (shortness, root-novelty) rule out memorization. Scripts: `scripts/p2c_onset.py`, `scripts/p2d_onset_promote.py`.
- **Effect on sūra definition:** onset lifts unconstrained precision 0.404→0.516 (crosses 0.45) and constrained
  K=114 F 0.283→0.345. **Sufficiency materially improved; full necessary-AND-sufficient still open** — global MDL
  under-segments (~70<114) from register stationarity (L15). Next: push recall higher (the necessity half).
- **14 in-table discoveries** now; candidates left: C1 (intermediate-complexity band).

## 5e. Sūra definition — characterized as far as the rasm allows (2026-06-10)

- **Sufficiency (precision):** 0.45 → 0.52 with the onset channel (p2c). **Necessity (detection):** fused L11⊕L18
  per-transition classifier **AUC 0.901, d 1.84** (p2e_boundary_fuse.py) — best yet.
- **BUT exact top-113 recovery caps ~0.27** (verse-shuffle floor 0.017). Cause: sūra boundaries are 1.8% rare and
  ~65% are SOFT/semantic (L16) — no surface discontinuity or distinctive onset. The rasm carries strong but
  **bounded** boundary information; the residual is meaning, which by the substrate law lies beyond rasm-surface
  instruments. **Verdict: the sūra is characterized as far as the rasm permits** — necessity AUC 0.90, sufficiency
  precision 0.52, exact recovery 0.27 (soft-boundary bound). Further closure needs a semantic layer the rasm doesn't expose.
- **Next high-value (general):** P3 — promote candidate **C1** (arrangement intermediate-complexity band) across
  ≥3 rasm modalities with shuffle AND sort floors. Then P1 cross-scale unification.

## 5f. P1 cross-scale unification — attempted, NO feature (2026-06-10)

- **Multifractality (p1_unify.py, p1b_mfdfa_robust.py):** the dramatic word-count Δh (1.56→3.5 under robust handling)
  is an **integer-tie ARTIFACT** — rejected by the stability check. Genuine but **MILD** multifractality in the
  letter-size series: Δh 0.168 vs shuffle 0.076 (z=16, q∈[-2,2]).
- **Cross-scale coupling:** only word→verse→sūra significant (r=0.35, z=5.0); the **letter scale is semi-detached** (z≈1).
- **Verdict:** "one determined system across ALL scales" NOT supported at promotable strength. Scales are PARTIALLY
  coupled. No feature added. Lesson logged: small-integer signals need tie-robust MFDFA; trust the letter-count channel.
- **Next:** P4 boundary necessity map · P5 element necessity. (P2 sūra characterized as far as rasm allows, §5e.)

## 5g. The "nothing moved" determinacy LADDER (2026-06-10)

- corpus **L14** (order-load 9,922 bits) · sūra **L12** (boundary local-optima) · **verse L20** (84% in-place vs
  47% floor, +37, 3 modalities — APPROVED) · **word P5** (44% vs 40% floor, **+4.5 only**, p5_word_necessity.py).
- **Verdict:** determinacy is STRONG corpus→sūra→verse, but **WEAK at the word scale** under rasm SURFACE features
  (no word-level rhyme; adjacent words don't share final letters). Honest read = **instrument-limited** (عدم الوجدان):
  word-order constraints live in morphology/syntax, which surface features can't see and the rasm doesn't expose.
  **No feature added.** The ladder bounds the determinacy claim — it does not reach uniformly to the finest scale via surface.
- **Next high-value:** Phase D synthesis (assemble the confirmed ladder + invariants into one description), or a
  morphology/syntax word-model (richer instrument) if a rasm-admissible one can be built.

## 6. Working rules (do not break)
1. No external data/model/corpus as evidence (until Phase E, comfort only).
2. Every claim: ≥3 converging modalities + the text's own shuffle floor + a named universe analog.
3. Faithful magnitudes; never claim what collapses next step; report nulls as instrument-limited (عدم الوجدان).
4. Necessary **and** sufficient, or it is not a definition (احسن تقویم).
5. Treat each inherent feature as neutral — log it and use it; build on assets, don't re-litigate deficits.
