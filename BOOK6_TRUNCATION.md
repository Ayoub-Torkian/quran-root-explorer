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

## CORRECTION (re-verified) — the substrate was NOT truncated  ✅ [MEASURED]
An earlier draft claimed the root/segmented/surface columns were also short. **That was
wrong** — an attribution error: it compared Book6's *content*-root count (e.g. 20 for 2:25)
against the *canonical word count* (~39), which inflates the figure with function words and
pause marks (و، ال، مِنْ، ۖ) that carry no root.

Direct inspection of the stored columns shows the roots reach the **end** of every one of
the 9 āyāt:

| āyah | last content word | Book6's last stored root |
|------|-------------------|--------------------------|
| 2:25 | خالدون | خلد (أزواج→زوج, مطهرة→طهر also present) |
| 2:264 | الكافرين | کفر |
| 5:45 | الظالمون | ظلم |
| 6:6 | آخرين | ءخر |
| 6:128 | عليم | علم |
| 33:53 | عظيمًا | عظم |
| 47:15 | أمعاءهم | معی |
| 48:29 | عظيمًا | عظم |
| 59:2 | الأبصار | بصر |

So the **only** defect was the diacritized *display* column, now repaired. The analytical
substrate (roots/surface/segmented) was complete all along — **no re-derivation needed**,
no root-based analysis was ever affected.

## Files
- `Book6.xlsx` — display column repaired (this change).
- `arabic.json` — complete canonical Arabic (6,236), used by the reader for display.
- No other workspace file stores āyah Arabic text; the derived JSONs hold analysis outputs.
