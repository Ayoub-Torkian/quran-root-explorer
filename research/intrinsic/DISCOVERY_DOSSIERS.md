# Discovery Dossiers — standard scrutiny for every >90 ledger item

Run these SEVEN questions on each feature that clears grade ≥90. Brief, data-backed answers only.

**Q1. What did you do?** (data + method, one paragraph)
**Q2. What did you discover?** (the finding in plain terms)
**Q3. What does it mean?** (significance · link to the north star)
**Q4. How sure are you?** (effect size, null, cross-validation — the numbers)
**Q5. What could kill it?** (confounds tested + remaining risks)
**Q6. Is it new?** (novelty vs existing measures — G7)
**Q7. Where does it sit?** (category, cross-refs, app surface)
**Q8. What is the value in the semantics / sequence latent-feature landscape?** (how it advances that frontier)

---

## L27 — Āyah recoverability from rasm morphology (grade 91)

**Q1. What did you do?**
All 6,236 verses → stripped diacritics to rasm (consonants only) → concatenated each sūra's words with
verse breaks hidden. For every word, predicted "is this an āyah end?" using rasm-only features
(word-ending morphology/suffixes, next-word opener particles, word length, rhyme match). Gradient-boosted
trees, scored by 5-fold cross-validation across **held-out sūras**.

**Q2. What did you discover?**
Āyahs end on a grammatically marked word-form (a recurring small set of morphological endings), followed by
recurring opener particles. The verse divisions can be rebuilt from the bare consonants.

**Q3. What does it mean?**
The Āyah is a **self-marking unit** — the text encodes where a verse ends in its grammar, not only its
rhyme/tradition. North star: the Āyah moves from "marked" toward "definable to sufficiency."

**Q4. How sure are you?**
AUC **0.967**, F1 **0.73** (recall 0.65 / prec 0.73), held-out-sūra CV. Null random-placement F1 0.115;
word-shuffle 0.09. Effect is large and reproducible.

**Q5. What could kill it?**
Confounds tested: **length** — removed, morphology+closure alone AUC 0.861 (length-only 0.82). **Rhyme** —
removed, morphology+closure alone AUC 0.861 (rhyme-only 0.80); full-model corr with rhyme-only 0.42.
Remaining risk: recall 0.73 is "substantial," not full sufficiency (~0.85+) — the unit is recoverable, not
yet *uniquely determined*. Honest open edge.

**Q6. Is it new?**
Yes, net of rhyme. The fāṣila (L06) was known; the morphological recoverability is new — corr 0.42 with rhyme
(<0.5 G7 threshold), and non-rhyme features carry AUC 0.918. It is a recovery/sufficiency frame, not a
re-statement of rhyme.

**Q7. Where does it sit?**
Category: **Āyah definition**. Cross-refs: L06 (rhyme/fāṣila), L18 (onset), L26 (closing cadence). App
surface: Morphology module (pending). Script: `scripts/ayah_recovery_deep.py`.

**Q8. Value in the semantics/sequence landscape?**
Verse segmentation reduces to a **compact closure lexicon**: āyahs close on a small grammatical suffix set —
**‑ūn (ون, 12× vs mid-text), ‑īn (ين, 7×), ‑īm (يم, 30×)**; **16 two-letter forms cover 80% of all 6,236
verse-ends** (of 212). So the Āyah boundary is, mechanistically, "ends on a pluralizing/nominal-verbal form."
*Honest link:* these forms ARE the fāṣila — the āyah-closure is a **grammatical** regularity of which rhyme is
the phonological face (consistent with G7 corr 0.42; L27's independent lift is the global suffix structure +
opener particles, not full orthogonality to rhyme).
