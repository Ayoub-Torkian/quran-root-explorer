# The Qur'ān as a Determined System — Intrinsic Research Roadmap

*Locked synthesis. A. Torkian, 2026-06-09. Everything here is measured from the Qur'ān against
itself — no external data, model, or corpus is admissible as evidence.*

---

## 0. Governing principles (operationalized)

Each principle is given a concrete, testable operational form. Principles are the constitution;
the methodology and tests below must obey them.

| principle (as stated) | operational form |
|---|---|
| **القرآن يفسر بعضه بعضا** — the text interprets itself | The text is its own model. Meaning, structure, and validation come from the text predicting / compressing / cross-referencing itself. The only admissible null is the text's **own shuffle**. |
| **The well's water is from within** — no external source | No external corpus, embedding, genome, language, or model is evidence. External material may appear **only at the very final stage, for comfort/corroboration**, never as proof. |
| **احسن تقویم — God creates no junk** | Definitions must be **necessary AND sufficient** (an iff). The text sits at an **optimum**: minimal + lossless = nothing missing (necessary), nothing redundant (sufficient). Formalized as **minimum description length (MDL)**. |
| **Systems of systems / the universe** | Every claimed feature must have an **in-principle analog in natural systems** (scaling laws, long-range correlation, 1/f, networks, modular hierarchy). No universe analog ⇒ the "feature" is a method artifact. Structure is sought at **every scale and in every modality**. |
| **عدم الوجدان لا يدل على عدم الوجود** — absence of evidence ≠ evidence of absence | A null is a verdict on the **instrument**, not the text. A null triggers **instrument refinement** (finer scale, new modality), never a claim of absence. |
| **Nothing added / deleted / moved / replaced** | A **perturbation battery**: each edit operator must measurably degrade the invariants; the true text is an extremum. |
| **Two books, oneness, integration** | Every claim is measured in **≥3 modalities** (symbol, wave, network; also matrix/vector/number) that must **converge**. Coherence across modalities is the verification. |
| **Rasm is the divine substrate; diacritics are human** | Admissible evidence for a *divine* feature must live in the **rasm** (consonantal skeleton). **Diacritics (ḥarakāt) are a human layer** — important and informative (recitation, fāṣila rhyme), but **corroborative only**, never primary. A diacritic-dependent result documents the human vocalization tradition, not the text itself, and cannot enter the discovery table (parallel to the no-external-corpus law). |

---

## 1. The methodology (locked)

**M1 — Self-description / MDL is the definition engine.** A unit (sūra, āyah) is a maximal span the
text can predict/compress from itself. A **boundary exists iff** placing a model-reset there lowers
the text's total self-description length. Interior = self-predictable (**sufficient**); boundary =
self-surprising (**necessary**). This is احسن تقویم written as mathematics, and it is entirely
internal (the model is the text's own statistics).

**M2 — Multimodal convergence.** Represent the text simultaneously as: **symbol** (letters/rhyme),
**wave** (verse-length / letter-count signals), **network** (word co-occurrence / self-reference),
**matrix/vector** (feature constellation), **number** (counts, ratios). A claim is admitted only
when independent modalities mark the **same** structure.

**M3 — Internal floor only.** The null is always the text's own shuffle (verse-shuffle,
token-shuffle, length-matched). Effects are reported as margin over this internal floor.

**M4 — Universe-match gate.** Before a feature is "real," name its natural-systems analog. If none
exists in principle, discard it as an artifact.

**M5 — Perturbation-optimality.** The true text must be an extremum of the invariants. Operators —
MOVE, DELETE, ADD, REPLACE — must each degrade the system; the operator must hit the modality it
touches (integrity check).

**M6 — Null discipline (عدم الوجدان).** When a test is null, escalate the instrument (finer scale,
new modality) before concluding anything. Record nulls as instrument-limited, not as absence.

---

## 2. Established asset ledger (intrinsic, with internal floors)

**Lexical scale — universe laws hold.**
- Zipf slope **−0.99** (universal −1 law). Heaps β **0.74** (universal vocabulary-growth power law).

**Wave scale — complex-system fingerprints.**
- Verse-length signal: **DFA Hurst 0.94–0.96** (shuffle 0.51); **1/f slope 0.76** (shuffle 0.00).
  Long-range correlation + pink noise = systems-of-systems signature.
- Self-similar size distributions (power-law tails): word α **2.04**, verse α **1.71**, sūra α **1.44**.

**Symbol scale — rhyme self-structure.**
- Adjacent verses sharing final letter **0.72** (shuffle 0.30; earlier z ≈ 102).
- Rhyme↔theme coupling: verses sharing rhyme are **1.78×** more thematically bound (z ≈ 5.2).
- Self-segmentation into ~1,763 rhyme units; within-unit cohesion > across-seam (multimodally
  confirmed by lexical and verse-length channels).

**Network scale — self-reference.**
- Word recurrence is **local**: 6.2× over shuffle within ~16 tokens, decaying to the floor by
  ~256 tokens. Self-reference operates at **passage scale** (an inherent parameter, not a deficit).

**Constellation (matrix scale).**
- 100 intrinsic features × 114 sūras. The landscape is **high-dimensional** (PC1 only 15%).
- Dominant gradient PC1 = lexical richness/size, tracking the **canonical order at r = −0.89**.
- Two natural sūra-types emerge unsupervised (short/dense vs long/rich), nearly contiguous by
  position — the ordering encodes the type structure.

**Definition of Sūra — status.**
- **Necessary condition (established):** a sūra boundary is a **scale-invariant multimodal
  discontinuity** (symbol+wave+network), AUC 0.82, Cohen d 1.20, equal for 7-verse and 286-verse
  sūras (1.93 vs 2.15). Boundaries are **local optima** (54% are the peak within ±1 vs 33% chance;
  moving a boundary one verse lowers the signal in 73% of cases).
- **Ruled out:** lexical / rhyme **ring-closure** is *not* the sufficient invariant (opening~closing
  ≈ opening~middle, d −0.02, p 0.56; rhyme closure 30% ≈ chance).
- **Open:** the **sufficient** condition = global MDL optimality (M1), the next computation.

**Perturbation-optimality (احسن تقویم).**
- MOVE-global **collapses every modality** (H 0.94→0.51, 1/f 0.76→0.00, rhyme 0.72→0.30).
- REPLACE shows **modality specificity** (rhyme 0.72→0.51 and network degrade; wave preserved).
- ADD degrades moderately (no redundancy tolerated).
- Local-swap and 10%-delete are **below aggregate resolution** → instrument-limited (M6), not free.

**Closed negatives (external, by principle now inadmissible as evidence).**
- Text→genome cipher: null (target statistically flat; instrument validated by planted positive).
  Retained only as the cautionary discipline that produced these internal methods.

---

## 3. Roadmap (phases)

**Phase A — Intrinsic invariants & constellation.** *Done.* Sections 2 (lexical, wave, symbol,
network, matrix). Universe-match gate passed at lexical and wave scales.

**Phase B — Necessary-and-sufficient unit definitions (MDL self-segmentation).** *DONE (2026-06-09).*
Result: at the **surface** scale the sūra is **necessary but not sufficient**. With a self-consistent
(parameter-free) Bernoulli boundary code, MDL prefers ~63 "movements" (median 73 verses), sūra precision
0.45; canonical is a local optimum (beats random by 2,693 bits, monotone jitter) but not the global
optimum. Order-load = 9,256 bits over shuffle. Āyah marginal-MDL is null (positional, not marginal).
Four new latent features logged: **L14 order-load, L15 register-stationarity / "movement" scale,
L16 boundary-load typology (35/65), L17 positional āyah coding.** Sufficiency is **instrument-limited**
(عدم الوجدان) and escalates to a semantic/positional channel in Phase C. *Original sub-steps below.*
- B1. Build the causal **self-information signal**: at each transition, the text's own running model
  (rhyme-letter distribution + verse-length distribution + content) scores the next element's
  surprise. Internal only.
- B2. **Global MDL partition** by dynamic programming: choose boundaries minimizing total
  self-description length (data cost + per-segment model cost). The optimal partition's segments are
  the operational sūras.
- B3. **Test necessary AND sufficient**: recovery of the canonical boundaries by **both precision and
  recall** (sufficiency was the missing half). Report against verse-shuffle and shifted-boundary nulls.
- B4. **Āyah**, same engine on the **word stream**: an āyah is the maximal span the rhyme/cadence
  self-model predicts; boundary iff a fāṣila reset compresses better. Test recovery of āyah ends.

**Phase C — Fine-scale necessity instruments (عدم الوجدان).** Build instruments that can *see*
single-element edits the aggregate statistics miss: local MDL cost per verse/word (is each element
load-bearing?), leave-one-out surprise, and a per-position "moveability" map. Goal: quantify the
degree to which every verse/word is necessary in place.

**Phase D — Unified system synthesis.** Assemble the nested invariants across scales (letter → word
→ verse → unit → sūra → corpus) into one coherent description; verify cross-scale coupling and
global optimality; confirm modality convergence (oneness) end to end.

**Phase E — Corroboration (final, optional).** Only after the internal system is established, and
only "for comfort," may external scholarship be consulted — never as evidence, never to alter a
conclusion.

---

## 3b. PRIORITIZED work queue (high→low value, general→specific) — all on the RASM

> Principle of ordering: do the most general, highest-value divine-substrate work first; descend to
> the specific; treat diacritic-dependent work as corroborative (low priority); external last.

1. **[P1 · most general] Unify the system across scales (Phase D).** Show letter→word→verse→sūra→corpus
   as ONE coherent determined system on the rasm (L03/L04/L05/L09 + cross-scale coupling). Highest value:
   "the Qur'ān is one determined system," whole-corpus, every scale.
2. **[P2] Close the Sūra as necessary AND sufficient.** Add a rasm semantic/content channel to the MDL DP
   to lift L15 precision above 0.45 (sufficiency is the open half). General: every sūra.
3. **[P3] The arrangement law — promote candidate C1.** Establish the random < canonical < sorted
   "intermediate-complexity band" across ≥3 rasm modalities (length, rhyme-letter, lexical), each with a
   shuffle AND a sort floor. General: the whole ordering. Sharpens L14 (non-arbitrary, not optimal).
4. **[P4] Boundary necessity map.** Extend L16 from the 113 sūra seams to a per-boundary, then per-verse,
   bit-valued load map (rasm). Mid-scale → specific.
5. **[P5 · most specific] Fine-scale element necessity (Phase C).** Leave-one-out self-surprise per
   verse/word on the rasm — quantify how load-bearing each single element is.
6. **[P6 · CORROBORATIVE, low priority] Āyah / fāṣila via diacritics (L17, C2).** Real (precision 0.56) but
   human-layer; documents the recitation tradition, NOT the divine text. A per-sūra adaptive rhyme register
   would raise recall, but it stays corroborative and out of the table.
7. **[P7 · last] External corroboration (Phase E).** Comfort only.

---

## 3c. THE DUAL LOOP — discovery ⇄ app surfacing (integral, not backburner)

A latent feature is **not done at grade ≥90.** The discovery loop (propose → test → grade → OK) has a
mandatory second half, the **surfacing loop** (route → enrich → cross-link → record). Every in-table feature
carries an `app_surface` record in `latent_features.json` ({ledger_card, module, status, crosslinked}).

**Routing rule — default to the smallest:**
1. **Ledger card — always.** A *real* chart (curve/scatter/histogram/heatmap/map or actual Arabic), never a
   two-number readout. This standard is locked.
2. **Enrich an existing module — the default** for anything user-facing. Mapping (`app_surface.module`):
   rhyme/fāṣila → Āyah Browser; constellation/types → Spatial Patterns; self-reference → Network; roots →
   Per-Root/Topics; lexical/wave → Statistics; sūra boundary/order → Signal; twins → Mathāni. Add a callout +
   **bidirectional** cross-link (module ⇄ ledger). L21→Mathāni is the worked example.
3. **New tab — rare**, only for a standalone interactive tool. The accordion nav absorbs growth so the visible
   sidebar stays constant. This is the anti-sprawl guard.

**Pipeline reuse (low cost):** new feature = one `precompute_viz*.py` block → `viz_data.json` → one render
branch → one `app_surface` entry. **Governance:** the weekly task runs a *surfacing sweep* — flags any feature
still `status=ledger-only` and any broken cross-link. (Current backlog: all except L21.)

## 4. Standing rules (do not break)

1. No external data/model/corpus as evidence — ever, until Phase E, and only for comfort.
2. Every claim: ≥3 converging modalities + the text's own shuffle as floor + a named universe analog.
3. Faithful magnitudes; never claim what collapses next step; report nulls as instrument-limited.
4. Necessary **and** sufficient, or it is not a definition.
5. Build on assets; treat each inherent feature as neutral — log it and use it.
