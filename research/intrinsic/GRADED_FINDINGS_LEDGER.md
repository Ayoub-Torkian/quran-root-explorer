# Graded Findings Ledger (PROVISIONAL) — best grade the best current instrument gives

**Why this exists.** The ≥90 bar gates the **Discovery tier** (anti‑overclaim guardrail). But a binary pass/fail
discards *real measured structure* and mislabels instrument‑limited findings as "failed." Per the BASE‑TRUTH
axiom (the wall is the instrument, not the text), this ledger records **every feature at its best MEASURED grade**,
stamped with instrument + substrate + arrangement + novelty + a **revise‑up trigger**. Nothing real is discarded;
nothing unproven is promoted. Grades are provisional and rise when a better instrument arrives.

**Two tiers:**
- **Discovery tier (≥90):** `latent_features.json` — gate‑passers only.
- **Graded tier (this file):** all real measured findings, provisional, revisable upward.

**Tags:** Substrate = ROOT (col4, content‑only, no grammar) · rasm‑WORD (col6, has morphology) · DIACRITIC (demote).
Arrangement = DIVINE‑DEFAULT (sūra→āyah) · DIVINE‑ALT (āyah→sūra, revelation) · HUMAN‑CONSTRUCT · RANDOM (null only).

| finding | best metric (instrument) | substrate · arrangement | novelty vs ledger | grade | revise‑up trigger |
|---|---|---|---|---|---|
| **Inter‑sūra lexical coherence (muṣḥaf munāsabāt)** | survived len+period+LINEAR‑size+blocks+topic (z=4.7–7.1) BUT collapses under NONLINEAR + size‑stratified control (z=−0.7); held‑out split: signal only in long‑sūra first half | ROOT · DIVINE‑DEFAULT vs DIVINE‑ALT(revelation)+RANDOM | — | **30 (REFUTED — size artifact)** | a genuinely size‑free similarity instrument could revive (~15%) |
| **A2 — frozen conceptual binomials** (سمو→ءرض, حیی→دنو→ءخر) | order consistency 0.68, z=21.9 survives position+freq+closure (pair tournament) | ROOT · DIVINE‑DEFAULT | real, gated, but pairwise‑local (transitivity sub‑random) = frozen‑binomial universal | **65** | Bradley‑Terry global‑order significance; context‑modulation test |
| **Āyah closure‑recoverable from roots** | AUC 0.85 / F1 0.55 (HistGB, GroupKFold) | ROOT · DIVINE‑DEFAULT | = fāṣila (L06/L26/L27); lexical closure redundant w/ morphological (Δ+0.003) | **60** | rasm‑word role aligner; sufficiency push to R≥0.85 |
| **L27 — āyah recoverability (word)** | AUC 0.967 / F1 0.73 (HistGB) | rasm‑WORD · DIVINE‑DEFAULT | order‑invariant = fāṣila; G7 redundant | **84** | non‑rhyme morphology beyond suffix; per‑sūra scheme typing |
| **Inter‑verse clustering** | self‑repetition z=96; regional confinement z=−26 (clump decomp) | ROOT · DIVINE‑DEFAULT | = cohesion (A1/A2) + territory (topics) | **55** | partial‑out cohesion; rooted theme model |
| **Intra position‑segregation** | Var z=89; interior z=63 (within‑āyah shuffle) | ROOT · DIVINE‑DEFAULT | = closure axis (corr 0.79 w/ closure‑rate) | **55** | role‑aware (verb/noun) position layer |
| **Within‑sūra arrangement** | cohesion t=9.0; directionality z=0.6 (PC1 drift) | ROOT · DIVINE‑DEFAULT | cohesion only; no directional necessity | **50** | legitimate‑alt arrangement comparison (muṣḥaf vs revelation) |

**Reading:** nothing on the ROOT substrate this session approaches 90 — every real signal resolves to an
already‑ledgered feature (closure, cohesion, territory). Highest provisional = **A2 (65)**. These are now
*recorded at their best*, not discarded. The clearest revise‑up levers are (a) the **rasm‑WORD** substrate
(morphology, unmined beyond L27) and (b) **divinely‑legitimate alternative arrangements** (muṣḥaf vs revelation).

---

## 2026-06-16 20:32 — session additions (stylometry / cross-corpus + Two-Books closure)

| finding | best metric (instrument) | substrate · arrangement | novelty vs ledger | grade | revise-up trigger |
|---|---|---|---|---|---|
| **Mathānī — localized refrain/repetition** | recurring-trigram density per sūra; repetition LOCALIZED (top-10 sūras ≈ 49% of recurring-trigram mass); 15/114 sūras carry 26 whole-āyah refrains (Ar-Raḥmān ×31, Al-Mursalāt ×10); two modes (litany refrain vs formulaic phrase) | rasm-WORD · DIVINE-DEFAULT vs matched-Arabic + non-Arabic | **NEW** (oral-formulaic typology; not closure/cohesion) | **55 (MEASURED, descriptive)** | larger genre-matched Arabic corpus; per-refrain network/role analysis |
| **Qur'ān stylometric distinctiveness vs matched Arabic** | size+genre-matched: TTR d=−4.3, hapax d=−4.7, entropy d=−3.0, compress d=−2.4, short-word d=+1.5 vs saj'; rhyme d=−0.4 (≈ saj' = genre, not unique) | rasm-WORD · DIVINE-DEFAULT vs saj'/classical | NEW (cross-corpus); confounds (size, genre) controlled | **45 (provisional — tiny baseline n=2–6 chunks)** | enlarge matched-Arabic; bootstrap CIs |
| **Comparative repetition band** | median recurring-trigram (350-w chunks): Qur'ān 0.029 — BELOW Finnish-Kalevala 0.049, above prose; Iliad more concentrated (53%) | rasm-WORD vs 5 non-Arabic texts | NEW | **50 (MEASURED)** | more oral-formulaic comparators (Avesta, Vedas, Beowulf) |
| **Two-Books char→protein correspondence** | optimized code-search manufactures low-E alignments for ANY input incl. RANDOM; under a FIXED code Qur'ān ≈ random at proteome scale (≈12% coverage, 0 significant) | rasm-WORD/ROOT → AA | — | **REFUTED as correspondence; MEASURED methodological caution** | a sequence-level mapping that beats its composition control (none found) |
| **Genome "long-range memory" (audit correction)** | MI-decay γ outlier (0.92) is mostly codon PERIOD-3, not long range; excluding multiples-of-3 → γ=1.69 (inside language band) | genome vs language | corrects prior structural claim | **restate** | period-decomposed MI; report gap not parametric p |

**Reading:** the genuine *positive* this session is **Mathānī (oral-formulaic repetition)** — real, localized,
typologically situated (Qur'ān < Kalevala), *distinctive not unique*; surfaced as the new **Mathānī Lab** module
(pages/35). The Two-Books char→protein program is **closed as an artifact** (code-search fabricates matches;
Qur'ān=random under a fair fixed code) — kept only as a methodological caution. Genome MI-γ "long memory" restated
as codon period-3 (audit). Nothing here approaches the ≥90 discovery bar.

### 2026-06-16 20:52 — stylometry baseline ENLARGED (Nahj al-Balāgha, 76k words saj')
Replaced the tiny matched-Arabic baseline (n=2–6 chunks) with **Nahj al-Balāgha** (genre-matched
rhymed-prose sermons, 152 chunks) + bootstrap CIs. Outcome:
- **Qur'ān more repetitive / lower lexical diversity than genre-matched saj' — CONFIRMED, powered.**
  hapax d=−2.05 [−2.33,−1.80]; TTR d=−1.00; compressibility d=−0.91; letter-entropy d=−0.72; all CIs exclude 0.
  (Earlier d=−4.7 was small-n inflation; true powered effect ≈ −2.0, still large.)
- **Rhyme comparison RETRACTED as a segmentation artifact** — āyah boundaries are placed at the fāṣila
  by construction; Nahj was segmented arbitrarily. Not a clean finding.
- **Revised grade for "Qur'ān stylometric distinctiveness (repetition/low-diversity vs saj')": 45 → 62**
  (MEASURED, powered, genre-matched, bootstrap-CI'd; distinctive-not-unique; oral-formulaic band).
  Revise-up trigger: clause-aligned rhyme comparison; add more saj' authors (Hamadhānī, kuhhān).
