# CROSS-IMPACT — propagate every discovery across all modalities (living doc)

**Standing practice (user-mandated):** whenever something is discovered, works in practice, or moves the
objective, READ IT BACK across the whole modality set — both explored and planned — and record (a) what it
RE-INTERPRETS, (b) what it asks us to RE-RUN, (c) what new test it OPENS. Update this file at every find.
Discipline unchanged (DESIGN_STANCE gates); this is about not letting findings stay siloed.

**NOTHING IS FINAL (user-mandated, stronger form):** treat NO verdict — positive OR null — as closed.
Every "final" result is provisional and must be RE-EVALUATED whenever another modality yields a relevant
insight. Cross-reference continuously: a null in one lens may be a signal relocated to another's grain; a
positive may be a generic effect another lens exposes. Re-open finals on purpose, not only on accident.

Legend: ⟳ re-run · ↻ re-interpret · ✦ opens new test.

---

## D1 — Multimodal FUSION is the signature (no single axis; AUC ≈0.94) [#35]
- ↻ Every NULL modality (phonosemantics #38, iltifāt #40, wazn #41, discourse-sequencing #44, syntax #45/#47,
  field-dynamics #46) is "null *standalone*" — its FUSION contribution is a separate question.
- ⟳ **Re-run fusion including the NEW positives as features**: muqaṭṭaʿāt position/root-cohesion, canonical-
  order coherence (#57), recurrence-variation profile (#43). Does AUC rise above 0.94? (Grain mismatch —
  sūra-level vs window-level — must be handled; do a sūra-level fusion variant.)
- ✦ A "fusion contribution" score per lens (drop-one-out AUC) to rank lenses by marginal value, not p-value.

## D2 — VARIED RECURRENCE is the strongest axis; = self-interpretation [#42/#43]
- ↻ Refrain (#33), rings (#31–32), discourse-inventory (#44) are facets of one repetition family; recurrence
  is the one measured at the right grain.
- ✦ Field RECURRENCE (not sequencing) untested: #46 tested field *sequencing* (null) — does a semantic field
  RE-CUR across distant passages like a narrative does? Re-open #46 as recurrence, not transition.
- ⟳ Sharpen with edit-distance / Kendall (DoE E3) — quantify re-expression vs copying.

## D3 — MUQAṬṬAʿĀT = position + root-cohesion + Book-theme (divinely-rooted) [#50–56]
- ✦ The root-space-cohesion test generalizes: apply it to OTHER a-priori sūra groups — Meccan/Medinan, the
  seven long (al-sabʿ al-ṭiwāl), the Musabbiḥāt, the Ḥawāmīm beyond muqaṭṭaʿāt — is grouping-cohesion special
  to the disjoint letters or general to named groups? (Distinguishes "letters" from "any traditional set".)
- ↻ Confirms the "pointer" idea (signal-geometry §8) at root grain.
- **✓ DONE (#59): cohesion is NOT special.** Other named groups cohere as much or more (al-sabʿ al-ṭiwāl
  cos 0.78 z=+5.4; Medinan z=+5.4) → the muqaṭṭaʿāt CONTENT-cohesion (#53/#54) is a general grouping/register
  effect; DOWN-WEIGHTED. Position pointer (#50/#51) + half-alphabet stay distinctive. Nuance: letter-group >
  several meaning-defined groups. LESSON: a positive can be a generic property — always test it against
  other a-priori groupings before claiming specialness.

## D4 — REARRANGEMENT / ORDERING is first-class; āyah-final-word stream [DoE]
- ↻ Rhyme/fāṣila (#34–37) is the SOUND of the verse-end; the fāṣila ROOT/CONCEPT stream (m2) is its MEANING
  in sequence — Lens 3 × Lens 12 × Lens 16 fuse at the verse-end.
- ✦ Re-examine #57/#58 with order-aware methods (Kendall, Mantel) and the fāṣila-concept ordering.
- ⟳ Re-run #46 field-sequencing using the fāṣila-concept stream as the unit (verse-ends may chain where bodies don't).

## D5 — DIVINE-ROOTEDNESS control (rasm/roots, not ḥarakāt) [DESIGN_STANCE]
- ↻ Recited/#49 deprioritized; prosody #39 (consonantal proxy) was already rasm-ok; all other lenses rasm-based.
- ✦ Flag any future step that needs vocalization; prefer rasm/root/position reformulations.

## D6 — EDIT-DISTANCE / order-sensitivity (cosine is order-blind) [IDEA §7]
- ⟳ Any cosine/TF-IDF result (#46, #53, #54, #57, #58, recurrence) can be re-checked with an order-aware
  metric: does adding order change the verdict? Especially #53/#57 (cohesion) — is it bag-of-roots or sequenced?

## D7 — LENGTH / REGISTER-LOCALITY confound (recurs across #53/#54/#57/#58)
- ⟳ Retroactive control: any adjacency/cohesion claim needs a length/register-matched null (the Meccan-only
  null in #54 is the template). Re-audit #57 with a register-matched null (currently length-band only).
- ↻ Tempered reading of #58 (chronology interlocks more) flows from this.

## D8 — GRAIN matters; a null is "wrong scale," not "absence" [#42 word vs passage; telescope rule]
- ✦ Re-test the NULL modalities at other grains/formulations before calling them dead: phonosemantics at
  root-pair grain; field-dynamics as recurrence (D2); syntax via dependency *relation-type* profile (not just depth).
- **✓ DONE (#73): phonosemantics retested at root grain — STILL NULL** (letter-Jaccard × PPMI Mantel,
  gate-validated z≈+15 on planted coupling; obs z=−1.74). Two grains down; the letter layer is independent
  of the meaning layer wherever tested (#38, #56, #64, #73). The faint NEGATIVE (OCP-like dissimilation)
  is a linguistics observation, not a Qur'an claim.
- ↻ Reframes every null entry in EVIDENCE as scale-specific, not final.

## D10 — Latent axes are ORDER-TYPED [#72]
- ↻ #57/E4/#70 unify: one NMF decomposition shows which thematic axes the CANON arranges (eschatology),
  which TIME arranges (the nuzūl-only C4/C5 waves), which both (narrative/creed/refuge), which neither
  (worship/dīn — the pervasive-field pattern, cf. mercy #46-reading).
- **✓ DONE (#75): C4 = the early-Meccan DEVOTIONAL wave** — gated (within-period z=+3.20; 10/10 restart
  stability, z=+3.72±0.31); the whole-sūra counterpart of #71's seal campaigns. **C5 demoted**: the
  first-revelations axis is stable as an axis but its wave-claim is init-dependent (z=+1.59±0.78) —
  descriptive only. ✦ METHOD LOCKED: data-derived axes require the RESTART BATTERY before any
  order/time claim. ✦ STILL OPEN: feed axis-scores into the D1 sūra-level fusion as features.

## D9 — MUQAṬṬAʿĀT combinatorics/order/time are nulled design axes [#67]
- ↻ #52 re-read: phonetic balance failed but ORDER succeeds — the structure lives in sequence/combinatorics,
  not articulatory category. The "design grammar" of the openings is positional at every grain (sūra position
  #50/#51, family deployment in time, letter order within the opening #67).
- ↻ #64 upgraded: family-communities now survive a degree-preserving null (descriptive → gated).
- **✓ DONE (#68): the order key FOUND — ABJADĪ.** Within-opening letter order tracks the ancient Semitic
  alphabet order at 0.889/0.925 concordance (z=+4.3/+6.6, selection-corrected p=5e-5); hijāʾī ≈ chance;
  frequency sub-2σ. Explains the one-directionality (#67). Orders only — numerology door stays closed.
  **✓ (a) DONE (#69):** no secondary key (makhārij sub-2σ); abjadī is NEAR-OPTIMAL (top ~0.04% of all
  orders, 4 pairs from the 0.978 ceiling — one pair unsortable by ANY key due to the 3-cycle); violations
  are each ONE local move from abjadī-sorted; the fronted ك of كهيعص = named OPEN outlier (parked).
  ✦ STILL OPENS: (b) does the ABJADĪ order structure anything else in the rasm (fawātiḥ beyond
  muqaṭṭaʿāt, letter-frequency profiles)? (c) historical-linguistic reading: the openings spell in the
  OLDEST attested alphabet ordering — connect to half-alphabet cardinality (#50).
- **✓ DONE (#70): deployment dynamics tested — waves are FEATURE-SPECIFIC.** Some fāṣila classes are true
  nuzūl waves finer than the Meccan/Medinan split (تعملون z=+5.2/within +3.3; يعلمون; اليم); others are
  register-only (رحيم, عليم); ALL narrative anchors null (Mūsā…ʿĪsā) → return is CONTINUOUS across
  revelation time — sharpens the architecture-of-return thesis (return = standing mode, not phase).
  **✓ DONE (#71): wave content tested with the sūra-block confound killed** (cross-sūra pairs + sūra-level
  perm). يعلمون and اليم are RE-AIMED across time (cosmos→kitāb; nations→covenant→community) — gated;
  تعملون falls (al-Baqara block). ↻ #62 re-read CONFIRMED and sharpened: the content-fit is to the
  mission-PHASE's domain — the fāṣila system is dynamic, fitting in time as well as topic.
  **✓ DONE (#74): the sweep.** Survivor عليم (content-only re-aiming); 2×2 TYPOLOGY established —
  usage-rate waves and content-re-aiming are INDEPENDENT dimensions of the seal system.
  **✓ D11 CLOSED (#77): the referent-split re-audit PASSES.** #62's fit survives on BOTH sides of the
  split (divine قدیر+31/رحیم+30/حکیم+25; other صادقین+28/ألیم+16) → the content-fit is REFERENT-GENERAL:
  the seal system fits content whatever it names; divine naming is the strongest subclass, not the
  mechanism. ↻ Re-reads the 'distributed catechism' framing (Lens 17 lecture): the catechism teaches
  attribute-for-situation AND truth-challenge-for-claim AND warning-for-deed — one fitting mechanism,
  several naming registers. FLAG: exclude bare-affix buckets (the ن morpheme class) from headlines.
- ⟳ Sūra-level fusion (D1) should add #67's family/combinatorics features when re-run.

## D12 — DATA-LAYER RULE: COL_SURFACE is a LEMMA column [#76 audit; #43 family]
- ↻ #63 CORRECTED: ending-repetition 0.279 (lemma) → 0.179 (true surface); survives at reduced magnitude
  (vs-ord ≈+2.2σ; vs sajʿ/poetry 4.7×/9×). The #43 lesson generalizes: EVERY cross-text feature must use
  nrm(COL_DIACRITIZED); the lemma layer is Qur'an-internal-only (e.g. #62 morphology grain is fine).
- ⟳ SWEEP the repo: audit all sequence_tests/* for COL_SURFACE used in cross-text comparisons (queued).
- ✦ The audit-pattern itself is the asset: feature means that look "too clean" (wāw-rate 0.012) are
  tokenization smells — check the column semantics before the statistics.

---

## Priority back-propagation queue (concrete)
1. **Sūra-level FUSION re-run** with new positives (D1) — does the divinely-rooted signature integrate?
2. **Field RECURRENCE** re-open of #46 (D2/D8) — fields as recurring, not sequenced.
3. **Group-cohesion generalization** (D3) — is muqaṭṭaʿāt cohesion special vs other named groups?
4. **fāṣila-concept stream** (D4 = DoE E2) — meaning chaining at verse-ends.
5. **Register-matched re-audit of #57** (D7).

## Status
Living doc. Started this session. Update at every discovery; mirror priority items into DESIGN_OF_EXPERIMENTS.md.
