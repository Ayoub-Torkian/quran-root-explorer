# Structure at every scale — āyah · passage · sūra · Qur'ān

*Root as the anchor. Each scale needs its OWN robust method (co-occurrence saturates as the window
grows — closure 53%→98%→100%, so one instrument cannot span scales). All numbers [MEASURED] in-sandbox
on the rasm ROOT substrate, muṣḥaf (DIVINE-DEFAULT) arrangement, against the text's own shuffle.
2026-06-19. Scripts: `/tmp/multiscale.py`, `/tmp/fig.py` (→ `multiscale_theme_map.png`).*

Corpus: 6,236 verses · 1,702 roots · 114 sūras.

| scale | method (robust for this scale) | null | structure found | status |
|---|---|---|---|---|
| **Āyah** | frequency-controlled bond graph (NPMI) | freq+length curveball | **619 strong bonds** (NPMI>0.3); genuine concept-pairs | MEASURED, robust |
| **Passage** | sequential lexical weave (adjacent-verse root reuse, IDF-wt) | verse-order shuffle within sūra | weave **z = 40.1** (obs 9650 vs 4348±132) | MEASURED, robust |
| **Sūra** | TF-IDF root signature + internal coherence | verse→sūra reassignment | coherence **z = 54.5**; signatures identify each chapter | MEASURED, robust |
| **Qur'ān** | NMF block factorization (root×sūra TF-IDF) | position shuffle | **12 interpretable themes**, localized in order (spread 19 vs 30) | MEASURED, robust |

## Why a single method fails (the diagnosis that motivated this)
Co-occurrence **saturates** with scale: at sūra scale almost every root-pair shares some sūra, so the
graph is ~complete (triad closure → 100%) and "motifs" become trivial; genuine 3-way drops 1.5%→0%.
Conclusion: **motif/co-occurrence is a within-āyah tool**; passage/sūra/Qur'ān each need a different
operation (sequence · signature · factorization). This is the corrected, scale-honest frame.

## Āyah — the bond graph
Top NPMI bonds (frequency-controlled): جري·تحت (rivers flowing beneath), نخل·عنب, شمس·قمر, شرق·غرب,
نفخ·صور (the Trumpet), مريم·عيسى, شري·ثمن (selling the hereafter), لحم·دمو (flesh·blood). The āyah's
structure = a sparse graph of genuine concept-pairs (NOT raw co-occurrence, which is just frequency).

## Passage — the sequential weave
Adjacent verses reuse roots far beyond a within-sūra order shuffle (z=40). Local order is load-bearing:
reorder the verses inside a chapter and this weave collapses. (Consolidates L22/L23.)

## Sūra — signature + coherence
TF-IDF signatures recover chapter identity cleanly:
- **S1 Fātiḥa** → صرط · عون · رحم · غضب · حمد (path · help · mercy · wrath · praise)
- **S12 Yūsuf** → ءسف · ءبو · ءخو · سجن · قمص (Yūsuf · father · brother · **prison · shirt**)
- **S19 Maryam** → رحم · ولد · عبد · نبو
- **S112 Ikhlāṣ** → وحد · ولد (oneness · beget)
Verses cohere to their own sūra's profile far above chance (z=54) — the sūra is a real theme-block.
(Consolidates L15: sūra = thematic unit.)

## Qur'ān — global thematic architecture (see `multiscale_theme_map.png`)
12 NMF themes over root×sūra, each interpretable, and they **localize in canonical position** (mean
within-theme position spread 19 real vs 30 shuffled) — the muṣḥaf groups themes, it doesn't scatter them:
- charity cluster صلو·عطو·يتم·كثر·طعم → Kawthar·Ḍuḥā·Māʿūn (108/93/107)
- refuge شرر·عوذ·ملك → Falaq·Nās·Zalzala (114/113/99)
- eschatology يوم·كذب·عذب·جنن → Wāqiʿa·Dukhān·Naba' (56/44/78)
- oneness وحد·ولد → Ikhlāṣ·Jinn·Balad (112/72/90)
(Consolidates L9 PC1↔order, L24 inter-sūra continuity.)

## Honest status
These are **robust descriptive recoveries**, not new ≥90 discoveries — they largely re-confirm and
**unify** existing ledger features (L22 weave, L15 sūra-theme, L9/L24 arrangement) into one scale-by-scale
operational frame. The value is (a) the corrected scale-honest methodology (one method per scale, with
nulls), and (b) operationalization: a multi-scale **Structure Map** the user can navigate.

## Operationalization plan (priority)
1. **Qur'ān-scale theme×sūra map** (done as a figure; wire as an interactive app surface). Dense, global,
   the "map of the territory."
2. **Sūra signatures** panel (per-chapter identity roots) — cheap, high interpretive value.
3. **Passage weave** line per sūra (where the text is tightly vs loosely woven).
4. **Āyah bond graph** (already on the Network/Motif surfaces — feed the NPMI version).
Engine to add: `structure_scales.py` (the four methods as reusable functions), then one coherent page.
