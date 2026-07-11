# Qurʾān chronology ledger — internal engine + event-anchor corroboration

*Status: provisional research ledger. Baseline = revelation order. The internal engine is ONE-LAW (rasm only); historical events are [REPORT], used to corroborate/reconcile, never as inputs.*

## I. Event-anchor corroboration backbone [REPORT] — 12/12 reconciled internally

Each event's cited āyahs were verified to carry the event's own vocabulary in the rasm (internal cross-reference).

| Event | Āyahs | Approx. date [REPORT] | Internal vocabulary (verified) |
|---|---|---|---|
| Qibla change | 2:142-150 | 2 AH | شطر/وجه/المسجد الحرام |
| Badr | 3:123; 8:41-44 | 2 AH | بدر(named)/غنم |
| Uhud | 3:121-128,140-147 | 3 AH | قرح |
| Muhājirūn & Anṣār | 9:100,117 | ~Hijra | هجر/نصر/سبق |
| Banū Naḍīr (Ḥashr) | 59:1-14 | 4 AH | حشر/جلو |
| Khandaq / Aḥzāb | 33:9-27 | 5 AH | حزب/جند/إذ جاءتکم جنود |
| Ḥudaybiyya / Fatḥ | 48:1,10,18,27 | 6 AH | فتح/بیعة |
| Ḥajj & ʿUmra | 2:196-203 | — | حجج/عمر/هدی |
| Conquest of Mecca | 110:1-3 | 8 AH | نصر/فتح |
| Tabūk | 9:38-52 | 9 AH | ثقل/جهد |
| Masjid Ḍirār | 9:107-110 | 9 AH | ضرر/فرق |
| Mubāhala (Najrān) | 3:61 (3:33-63) | ~9-10 AH | بهل(نبتهل)/دعو/نفس/بنو/نسو |

These give an independent within-Medinan order (Badr→Uhud→Aḥzāb→Ḥudaybiyya→Conquest→Tabūk) that the raw nuzūl column matches at Spearman 0.70.

## II. Relocation candidates (internal detector, baseline+anomaly) — ranked

Sustained off-era chunks in long sūras; coarse target (era/stratum), not exact index.

| Rank | Chunk | Len | P(Medinan) | Host | Flag | Tradition corroboration [REPORT] |
|---|---|---|---|---|---|---|
| 1 | 6:137-146 (انعام) | 10 | 0.81 | Meccan | Medinan-like (high) | ~6 verses of al-Anʿām reported Medinan |
| 2 | 7:155-159 (اعراف) | 5 | 0.83 | Meccan | Medinan-like (low) | 7:163-170 reported Medinan |
| 3 | 39:5-8 (زمر) | 4 | 0.83 | Meccan | Medinan-like (low) | — |
| 4 | 18:17-20 (کهف) | 4 | 0.81 | Meccan | Medinan-like (low) | — |
| 5 | 10:20-23 (یونس) | 4 | 0.78 | Meccan | Medinan-like (low) | — |

## II-b. Multi-temporal sūras — chunk-level dating required (the core inconsistency)

A single sūra can hold chunks revealed years apart; sūra-level nuzūl cannot represent it.

| Sūra (nuzūl) | Chunk | Event anchor [REPORT] | Approx. date |
|---|---|---|---|
| Baqara (87) | 2:142-150 (qibla) | Qibla change | 2 AH |
| Baqara (87) | 2:196-203 (ḥajj) | Ḥajj & ʿUmra | ~6 AH |
| Āl ʿImrān (89) | 3:121-175 (battle, قرح) | Uhud | 3 AH |
| Āl ʿImrān (89) | 3:33-63 (Jesus/Mary, نبتهل) | Najrān / Mubāhala | ~9-10 AH |
| Tawba (114) | 9:100,117 | Muhājirūn & Anṣār | ~early Medinan |
| Tawba (114) | 9:38-110 | Tabūk / Masjid Ḍirār | 9 AH |

Confirmed by the chunk engine via cross-referenced anchors. Within Medina the internal era-signal hovers near 0.5, so chunk dates rest on the [REPORT] event anchors; internal evidence supplies coarse placement + segmentation only.

## II-c. Gradation tracks (semantic development across revealed time) [MEASURED]

| Track | Early | Mid | Late | Reading |
|---|---|---|---|---|
| bashīr / nadhīr (warning-share) | 100% | 75% | 53% | early = pure warning; glad-tidings rises — a clean clock |
| heaven / hell (hell-share) | 57% | 43% | 44% | early terror-weighted, then balances toward paradise |
| khamr (deontic) | provision 16:67 | sin&benefit 2:219 | prohibition 5:90 | gradual ruling = revelation order = tradition |
| Jews vs Christians (sub-sense) | 0 / 0 | 4 / 0 | 8 / 14 | Christians appear only late; split ahl al-kitāb |

## II-d. The model is a partial-order GRAPH, not a line (canonical frame)

Chronology here is a consistent DAG, not a total order. The temporal element is real but **not linear**: ten developmental threads run in parallel through shared time-windows — events/community, the Prophet's household, three ruling gradients (khamr · qitāl · ribā), family law, referent-group formation, warning→glad-tidings, heaven/hell tone, ritual+promise. Nodes in the same window are **contemporaneous, not sequenced** (~2 AH: Badr ∥ qibla ∥ khamr "sin & benefit" ∥ hypocrite/PoB emergence). Incomparable (parallel) node-pairs = 23% with the dated backbone fully ordered, 60% admitting only direct before/after evidence — linearity scales with anchor coverage. This reinterprets the within-Medinan "null": not missing signal but a category error (forcing a line onto contemporaneous chunks). Figures: `chronology_web.png` (static, landscape), `chronology_web_interactive.html` (app), `chronology_braid.png`, `chunks_subgraph.png`.

## III. Honest status

- **Validated:** Meccan/Medinan classifier (sūra AUC 0.86, āyah AUC 0.84); coarse revelation-order recovery (pairwise 0.74, multimodal fusion); referent-emergence sequence; event-anchor reconciliation (12/12).
- **Resolution-adding clocks:** referent-emergence; یسألونک topic-type (theological→legal); bashīr/nadhīr monotonic gradient; khamr/qitāl/ribā and heaven-hell gradations; Jews-vs-Christians sub-sense.
- **Corroboration-only (labels, not clocks):** prophet-narrative deployment + tribal punishment-cycles (mid-Meccan stratum, non-monotonic — measured NOT to add ordering resolution); event anchors (13 reconciled [REPORT]).
- **Instrument-limited (not textual absence):** fine within-Medinan ordering is NOT recoverable from internal features (per-āyah null vs raw nuzūl; only legal-density +0.41 vs event-order). Event anchors supply the fine Medinan order; internal evidence does coarse placement + segmentation.
- **Low-confidence candidates** (len-4, no tradition tag: 10:20-23, 18:17-20, 39:5-8) held pending stronger features.

## IV. External cross-reference [REPORT] — tanzil.net (traditional / Ibn-ʿAbbās · al-Zanjānī)

*Revelation order is not in the rasm, so this is [REPORT]-vs-[REPORT] corroboration between two traditional schemes, not verification against Qurʾanic data.*

**(a) Sūra order.** Book6's nuzūl column vs tanzil: **101/114 exact (89%), Spearman ρ = 0.9993.** One real divergence: **An-Nasr (110): Book6 = 102 (between 59 and 24) vs tanzil = 114 (last)** — Book6 follows **Noldeke** (flagged on tanzil's own page). The other 12 mismatches are ±1–2 shuffles in the dense late-Medinan cluster (61, 64, 9, 5, 22, 24, 48, 49, 58, 62, 63, 66). The figure dates An-Nasr/Conquest to 8 AH via the *event* anchor, independent of either scheme.

**(b) Embedded verses.** Against tanzil's exception notes as held-out gold, the internal āyah detector's flag *includes* the exact traditional verses with high recall (al-Aʿrāf 7:163-170 8/8, al-Shūrā 42:23-27 4/4, al-Anʿām 6 7/8, al-Aḥqāf 46 3/3, al-Qaṣaṣ 28 4/5) but **over-flags** — low precision throughout (<0.2; ~half a long sūra marked) — but is noisy corpus-wide (37% recall, low precision) and weak on the reverse (only 9:129). Localizes, doesn't classify. al-Shūrā 42:23-27 upgrades the earlier "NEW" candidate to tradition-corroborated.

## V. Tradition-attested embedded-verse layer [REPORT] — "passages, not just sūras," corpus-wide

~30 Meccan sūras carry Medinan verses and 6 Medinan sūras carry Meccan verses. Internal detector overlap (✓ = traditional verses caught — **recall**; the flag also marks many others, so precision is low: agreement is at the *sūra* level, not the precise verse).

| Sūra | Era | Embedded verses (opposite era) [REPORT] | Detector |
|---|---|---|---|
| al-Aʿrāf 7 | Meccan | 163-170 Medinan | ✓ 8/8 |
| al-Shūrā 42 | Meccan | 23,24,25,27 Medinan | ✓ 4/4 |
| al-Anʿām 6 | Meccan | 20,23,91,93,114,151-153 Medinan | ✓ 7/8 |
| al-Aḥqāf 46 | Meccan | 10,15,35 Medinan | ✓ 3/3 |
| al-Qaṣaṣ 28 | Meccan | 52-55,85 Medinan | ✓ 4/5 |
| al-Najm 53 | Meccan | 32 Medinan | ✓ 1/1 |
| al-Kahf 18 | Meccan | 28, 83-101 Medinan | partial |
| al-Isrāʾ 17 | Meccan | 26,32,33,57,73-80 Medinan | partial |
| Baqara 2 | Medinan | 281 Meccan (Minā, Last Ḥajj) | — |
| Anfāl 8 | Medinan | 30-36 Meccan | — |
| Tawba 9 | Medinan | 128-129 Meccan | ✓ 129 |
| Ḥajj 22 | Medinan | 52-55 (Mecca↔Medina) | — |
| Māʾida 5 | Medinan | 3 (ʿArafāt, Last Ḥajj) | — |

*The detector recovers the exact traditional span on several Meccan sūras (independent internal corroboration of [REPORT]); the reverse is mostly single verses it misses. Convergence where it occurs is strong evidence the chunk is the dating unit.*


## VI. Detector calibration (per-sūra precision vs recall) [MEASURED]

Against tanzil's embedded-verse gold, the detector is **high-recall / low-precision** everywhere — **no high-trust verse-level tier exists.** Per-ayah flag: recall 1.00 on al-Aʿrāf/al-Shūrā/al-Najm, but precision 0.08–0.16 (105 ayahs flagged in al-Aʿrāf for 8 gold). Sustained-block engine (run≥4): precision still 0.06–0.44 (best: al-Shūrā prec 0.27/rec 0.75; al-ʿAnkabūt prec 0.44). **Calibrated conclusion:** the engine reliably flags *which sūras* are temporally mixed (sūra-level corroboration of tradition) but does **not** pin the exact displaced verses. Use it as a sūra-level localizer, not a verse classifier; precise verse-dating stays with closer reading + [REPORT] anchors.
