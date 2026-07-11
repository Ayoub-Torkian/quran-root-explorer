## 5.22 The surah in the web: a graph-theoretic view

Because the Qurʾān can be read as a **web** of roots — nodes joined when they share a verse — we can place al-Kawthar's seven roots inside that network and measure where they sit. Building the co-occurrence graph over the whole corpus yields **1,694 nodes and 78,111 edges**; each root's **degree** is the number of distinct roots it ever shares a verse with. Table 6 and Figures 11–12 report the result.

| Root | Degree | Weighted degree | Clustering | Degree percentile |
|---|--:|--:|--:|--:|
| *r-b-b* (Lord) | 853 | 7,177 | 0.16 | 99.8 |
| *k-th-r* (abundance) | 461 | 1,582 | 0.33 | 97.0 |
| *ṣ-l-w* (prayer) | 348 | 967 | 0.42 | 93.8 |
| *ʿ-ṭ-w* (give) | 45 | 55 | 0.65 | 54.7 |
| *sh-n-ʾ* (hate) | 34 | 39 | 0.83 | 48.0 |
| ***n-ḥ-r*** (sacrifice) | **2** | 2 | 1.00 | **3.6** |
| ***b-t-r*** (cut off) | **1** | 1 | 0.00 | **0.0** |

*Table 6. Graph-theoretic metrics for the seven roots in the corpus co-occurrence web. [MEASURED]*

Three things stand out. First, the surah spans the **entire range of network centrality at once**: *r-b-b* is a top hub (99.8th percentile — the Lord is linked to roughly half the lexicon), *k-th-r* and *ṣ-l-w* are major hubs (97th, 94th), while the two hapax sit at the floor. Second — and this is the striking image — *b-t-r* is a **degree-1 pendant node** (0th percentile): in the graph it literally hangs by a **single edge**, its lone link being to *sh-n-ʾ*, "hate." The network structure *enacts* the word's meaning: *abtar*, "cut off," is the most nearly **cut-off node** in the whole web [MEASURED degree; INFERRED resonance]. *n-ḥ-r*, "sacrifice," is a near-isolate too (degree 2), but with clustering 1.0 — its two neighbours (*ṣ-l-w* and *r-b-b*) are themselves linked, so it sits inside a tight little **worship triangle** (prayer–Lord–sacrifice), exactly the devotional cluster of verse 2. Third, the surah yokes the **most central** root (*r-b-b*) to the **most peripheral** (*b-t-r*) within ten words — centre and edge of the web in one tiny chapter.

**An essential caveat, lest the graph oversell itself.** Degree in a co-occurrence web is largely a **function of frequency**: a word used once *cannot* have many neighbours, so the hapax were guaranteed to be low-degree the moment we knew they were hapax. The graph view is therefore mostly a **re-encoding** of the lexical fingerprint of §5.1, not an independent modality, and we should not present it as fresh evidence of design. What it adds beyond frequency is modest but real: the **clustering** figures (n-ḥ-r = 1.0, embedded in the worship triangle; b-t-r = 0, a bare pendant) describe *how* the rare roots attach, not merely *that* they are rare; and the visualization makes the centre-vs-edge structure legible at a glance. So we record the graph metrics as a **measured restatement** of the fingerprint, with one genuinely additional, and pleasingly apt, fact: the root meaning "cut off" is, structurally, the corpus's most cut-off node. [MEASURED: all degrees/clustering; INFERRED: that the structure "mirrors" the meaning, offered as resonance, not proof; and CONCEDED: degree ≈ frequency, so this is largely a re-encoding.]
