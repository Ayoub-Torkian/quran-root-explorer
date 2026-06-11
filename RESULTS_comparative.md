# Comparative placement of the Qur'an vs world text (dimensionless, language-robust)
Corpus on disk: Qur'an + 7 texts / 4 languages (EN Bible, P&P, Sherlock, Aesop;
FR Candide; DE Faust; ES Quijote). Scripts: placement5.py, battery.py, battery2.py.

## Structure axis 1 — adjacent-unit coherence (z, median)
Sherlock 4.50 · P&P 4.15 · Bible 4.12 · **QURAN 3.72** · Quijote 3.03 · Faust 2.45 · Candide 1.96 · Aesop 0.07
-> QURAN ~mid/high band (45-64th pct). NOT an outlier; Bible/Austen/Doyle match-or-exceed.

## Structure axis 2 — long-range WORD memory (MI excess d>=5, % of word-entropy)
Bible 5.08 · Quijote 2.94 · **QURAN 2.84** · Candide 1.60 · P&P 1.55 · Sherlock 1.19 · Aesop 1.13 · Faust 0.96
-> QURAN 71st pct, in-band. Bible (scripture) leads.

## Frequency/form battery (zipf, heaps, ttr, gzip, word-length, burstiness)
- gzip(most compressible) & word-length(shortest) flagged "outlier" BUT = artifacts of
  consonantal Arabic rasm (short tokens) -> NOT real; language-confounded.
- zipf/heaps/ttr/burst: in-band.
- Verdict: language-dependent metrics need ARABIC comparators (not yet on disk) for a fair test.

## CONSOLIDATED VERDICT (this round)
No certified outlier on ANY universal (language-robust) dimension tested.
The Qur'an sits in the HIGH band of structured/scriptural text — closest neighbour is
consistently the Bible. Apparent "outliers" are language-representation artifacts.
Open region: language-fair FREQUENCY/FORM tests (need Arabic comparators on disk) and CONTENT semantics.
