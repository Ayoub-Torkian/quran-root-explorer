# Book6 truncation — found & partially repaired (2026-06-19)

## What was wrong
Nine āyāt were stored **truncated at the end** in `Book6.xlsx` — the import cut the
whole row, so not only the diacritized display text but the segmented/surface/**root**
columns were short. Detected by comparing each verse's consonant skeleton against the
canonical Tanzil text (`ara-quransimple`, which matches parsquran.com).

The 9 āyāt (missing tail length):

| āyah | missing | example of what was cut |
|------|--------:|--------------------------|
| 2:25   | ~19 | …أَزْوَاجٌ مُطَهَّرَةٌ ۖ وَهُمْ فِيهَا خَالِدُونَ |
| 2:264  | ~43 | …وَاللَّهُ لَا يَهْدِي الْقَوْمَ الْکَافِرِينَ |
| 5:45   | ~13 | |
| 6:6    | ~14 | |
| 6:128  | ~25 | |
| 33:53  | ~164 | (the longest cut) |
| 47:15  | ~54 | |
| 48:29  | ~126 | |
| 59:2   | ~61 | |

## What was repaired  ✅ [MEASURED]
The **diacritized DISPLAY column** (`متن آیه با حرکت`) for all 9 was replaced with the
complete canonical text, converted to Book6's orthography (`ك`→`ک`; stripped pause /
sajda / dagger-alef marks Book6 doesn't use). Each repair was validated so the original
truncated text is a clean **prefix** of the repaired text (no content changed, only the
missing tail restored). All 6,236 rows still load; untouched verses are byte-identical.

Because Search / Ayah Browser / Deep-Dive read this column, they now display the full
āyāt. The dedicated **Read** page + pop-out reader already use `arabic.json` (the complete
canonical text, 6,236 verses) for display.

## What still needs doing  ⚠️ [substrate — do NOT guess-fill]
The **root / segmented / surface columns** for these 9 āyāt are **still truncated** (e.g.
2:25 stores 20 root-tokens but the full verse has ~23 — missing **زوج · طهر · خلد**).
These are the analytical *substrate*. Per the locked BASE-TRUTH rules, the correct fix is
to **re-run Book6's own morphology pipeline** on the now-complete text — NOT to inject
hand-derived roots (which would contaminate the corpus). Until then, root-based analyses
(network/stats/mathānī, and any derived JSON computed from them) under-count these 9 verses
only. Low impact (9 / 6236), but logged here so it is not forgotten.

## Files
- `Book6.xlsx` — display column repaired (this change).
- `arabic.json` — complete canonical Arabic (6,236), used by the reader for display.
- No other workspace file stores āyah Arabic text; the derived JSONs hold analysis outputs.
