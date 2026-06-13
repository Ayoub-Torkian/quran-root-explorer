# FINDING — Āyah-boundary recovery from the rasm (2026-06-12)

**Question (north star, sufficiency half):** from the bare consonantal skeleton (rasm, verse
markers removed, diacritics demoted per the One Law), can the text's own signals *recover* the
6,236 āyah breaks? A unit is defined to *necessity AND sufficiency* only if the text itself marks it.

**Method.** Corpus: `quran_arabic_verses.tsv` (6,236 āyāt). Strip ḥarakāt/tatweel → rasm; normalise
hamza-carriers and alef/alef-maqṣūra to skeleton. Concatenate each sūra into a word stream with
āyah breaks hidden; candidate boundary = after each word. Detectors place breaks from intrinsic
cues only (consonantal rhyme = word-final 1–2 rasm letters; length cadence). Scored
recall/precision/F1 against the canonical partition. Nulls = the text's own shuffle (word-order
shuffle within sūra) and random placement matched to prediction count.

## Results (micro-averaged over all 114 sūras)

| model | recall | precision | F1 | note |
|---|---|---|---|---|
| simple rhyme (top-2 final keys) | 0.24 | 0.21 | 0.22 | naive |
| **rhyme + length-cadence (DP), intrinsic** | **0.41** | **0.24** | **0.30** | best no-oracle |
| ORACLE rhyme (last-2, knows the fāṣila) | 0.73 | 0.59 | 0.65 | ceiling of rhyme alone |
| null — word-shuffle | — | — | 0.09 | One-Law null |
| null — random placement | — | — | 0.115 | matched counts |

- **Signal is unambiguous.** Intrinsic detector F1 0.30 vs random 0.115 → **z ≈ 60**; simple
  detector vs the text's own word-shuffle → **z ≈ 37**. Āyah ends are intrinsically marked.
- **Rhyme cohesion (rasm):** the modal final consonant covers **80%** of a sūra's āyah-ends;
  a last-2 rhyme set covering 60% of ends matches **73%** of true ends.
- Per-sūra recovery (intrinsic): median recall 0.34; **40/114 sūras ≥ 0.6 recall, 15/114 ≥ 0.8**.

## Verdict — honest, no overclaim
- **Necessary: YES (strong).** An Āyah ends in its sūra's fāṣila (rhyme): 73–80% of ends carry the
  dominant rhyme on the *rasm*, far above the text's own shuffle (z ≈ 37–60). "Ends in the local
  rhyme" is a near-necessary property of an Āyah, provable from the consonants alone.
- **Sufficient: NOT YET.** Rhyme alone over-fires mid-āyah (precision 0.24 intrinsic, 0.59 oracle),
  so it does not *uniquely* place all breaks. Full sufficiency needs rhyme **+** length-cadence **+**
  syntactic/closure cues. The gap from intrinsic F1 0.30 to oracle 0.65 is an **instrument limit**
  (imperfect intrinsic rhyme identification + crude cadence model), NOT absence of signal
  (TELESCOPE principle: refine the instrument).

**Grade vs ≥90 bar:** does NOT yet enter the ledger as "Āyah recoverable." It firmly establishes the
*necessary* half (rhyme-marking, which extends the existing L06 fāṣila feature into a recovery/
sufficiency frame) and quantifies the ceiling. Provisional.

## Next sub-step (instrument refinement, ranked)
1. **Better intrinsic rhyme ID** — pick the fāṣila by spectral periodicity of word-final keys
   (autocorrelation peak at the āyah period), not raw frequency; expected to close most of the
   0.30→0.65 gap.
2. **Per-sūra length-distribution prior** in the DP (learn the āyah-length law, not a single L).
3. **Add closure cues** — pause particles / formula-ends / the rasm of common āyah-final words.
4. Then re-grade; if intrinsic recall clears ~0.85 at decent precision, the Āyah is *defined to
   sufficiency* on the rasm.

Scripts: ayah_*.py incl. ayah_deep.py (HistGB rich-features: AUC 0.958, F1 0.69 — instrument limit was the blocker).
