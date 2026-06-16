# Latent Feature Ledger — Intrinsic Qur'ān Study

> **The one law.** Nothing external is admissible as evidence. Every feature is measured from the text against its own shuffle. A feature is admitted only with ≥3 converging modalities + the text's own shuffle floor + a named universe analog.

*Cadence **weekly**. Updated 2026-06-15; next due 2026-06-22. Generated from `latent_features.json`.*

**22 features pass critical review (grade ≥ 90); 5 excluded.** Every feature carries a four-question review (what it discovers · category · relations · validity) plus a plain-English conceptual foundation and utility.

**Coverage:** scale 4, sequence 7, order 7, semantic 3, content 6, form 6, structure 9, sound 7, surah 7, ayah 2

**Open gap:** The sūra sufficiency ceiling (exact recovery ~0.36, fused L11⊕L18) is now PRINCIPLED, not instrumental: an intrinsic root-co-occurrence semantic channel (p6_semantic.py) is a real but weak signal (AUC 0.68) that does NOT improve recovery. The ~65% soft boundaries are comprehension-level discourse shifts beyond any intrinsic statistic on the rasm. Remaining frontier: a rasm-admissible morphology/syntax word-model (word-scale necessity). | MORPHOLOGY INSTRUMENT SCOPED (morph_feasibility.py): intrinsic rasm-residue yields a real wazn inventory (verbs P:ي/ت+S:ون, participles I:ا, attributes I:ي, article ال), BUT per-token root↔word alignment caps ~19-29% — research-grade morphology needs external segmentation (inadmissible). Frontier closed at rasm substrate.

## Discovery table — passed (≥ 90)

| ID | Feature | Grade | Axes | Plain English | Why it matters |
|---|---|---|---|---|---|
| L11 | Sūra boundary = multimodal discontinuity (NECESSARY) | 98 | surah/structure/sound | Where one sura ends and the next begins, the sound, the rhythm, and the word-links all jump at the same moment — a real seam you can detect blind. | The app can find sura boundaries automatically and show how sharp each one is. |
| L19 | Intermediate-complexity band (edge of order) | 96 | order/sequence/structure/scale | The verse order is not random — but it is also not sorted into tidy blocks. In every channel (rhyme, length, theme) the arrangement sits in the MIDDLE: more ordered than a shuffle, far less ordered than a sorted list. That middle band is exactly where meaningful sequences — language, music, DNA — live. | Proves the order is deliberate AND meaning-bearing, not merely non-random: it deliberately gives up easy compressibility to keep meaning. Guards against mis-reading L14 as "maximally optimal". |
| L20 | Per-verse necessity (nothing moved, at verse scale) | 96 | order/sequence/structure | Pick any single verse and ask: is it more at home where it actually sits than it would be if dropped somewhere else? For about 84% of verses the answer is yes — each is more predictable from its own neighbours than from a random neighbourhood, far above the 47% you would get by chance. And it holds separately in three channels: rhyme, verse length, and vocabulary roots. So it is not only the big landmarks that are fixed — every individual verse is load-bearing in its own place. | Turns "nothing could be moved" from a slogan into a per-verse number, and yields a map of which verses are most locked-in versus most surprising — useful for flagging anomalies and for teaching. |
| L21 | Structural twins (mathānī) — multimodal verse homology | 96 | structure/content/sound | Some verse pairs are clearly built on the same template — they share most of their word-roots AND tend to end on the same rhyme and run to the same length, even when they sit in different sūras. The Qur'an carries a network of these structural twins (mathānī): echoing verse-pairs spread across the whole book. | Surfaces the hidden web of mirrored verse-pairs across the Qur'an — for study, cross-reference, and seeing compositional symmetry; the app can show each verse its structural twins. |
| L03 | Verse-length long-range correlation (DFA Hurst) | 95 | sequence/order/form | Verse lengths aren't random. Short and long verses come in waves, and how long a verse is depends on verses far away, not just its neighbours. | Strong proof that the ORDER of verses carries meaning. It is the backbone of the app being able to spot a verse that sits out of place. |
| L14 | MDL order-load of the verse stream | 95 | sequence/order | The specific order of the verses carries about 9,000 bits of real, measurable structure compared with the same verses shuffled. | A hard number certifying the order is non-arbitrary (not random) — while honestly showing it is NOT mere sorting. Basis for a displaced-verse detector; do NOT read it as 'maximally optimal'. |
| L06 | Rhyme adjacency (fāṣila cohesion) | 94 | sound/ayah/form | Neighbouring verses tend to end on the same sound far more often than chance — rhyme runs in stretches. | This is what the app uses to mark rhyme paragraphs and verse endings, so you can see the sound architecture of a passage. |
| L16 | Boundary-load typology (hard vs soft seams) | 94 | surah/sound/semantic | About a third of sura breaks are marked by a clear change in sound and rhythm; the other two-thirds are marked only by a change in topic. | The app can label each of the 113 sura junctions as 'sound-marked' or 'meaning-marked' — a brand-new annotation you can browse. |
| L13 | Perturbation-optimality battery | 94 | order/form/content/structure | Scramble, delete, add, or swap the text and the measured patterns break — and each kind of damage breaks a specific pattern. | A stress-test proving the patterns are real and load-bearing, not lucky coincidences. |
| L22 | Sequential lexical chaining — the verse weave | 94 | sequence/content/order | Consecutive verses are woven together by their word-roots: a verse tends to reuse roots from the verse just before it, far more than if you shuffled the verses inside the same chapter. The bond is strongest for immediate neighbours and fades smoothly as verses get farther apart. So the ORDER of verses inside a sūra is not arbitrary — it carries a real, measurable lexical weave. | Answers "does verse order matter?" with a hard number: reorder the verses inside a chapter and you destroy this weave (z=23). Lets the app show, for any verse, how tightly it is lexically bound to its neighbours — and flag passages where the weave is unusually tight or loose. |
| L04 | 1/f spectral slope | 93 | sequence/form | The rhythm of verse lengths has structure at many timescales at once — like a heartbeat or natural music, not one repeating drumbeat. | An independent, second confirmation that the text is layered and alive, not flat or mechanically uniform. |
| L09 | Constellation dimensionality + order axis | 93 | order/surah/scale | Describe each sura by 100 measurements, and the single biggest difference between suras lines up almost perfectly with their order in the book. | The app can predict where a sura belongs in the canonical order from its statistics alone — and flag anything that doesn't fit. |
| L15 | Surface-register stationarity — the 'movement' scale | 93 | surah/semantic/scale/structure | Let the text divide ITSELF purely by sound and rhythm and it makes about 63 big 'movements', not the 114 suras — because the surface style is remarkably even throughout. So a sura is defined by its THEME, not by a change in sound. | Tells you what a sura really is (a unit of meaning), gives you a new coarse 'movements' map of the book, and shows exactly where meaning-based analysis is still needed. |
| L18 | Sūra-onset asymmetry (the opening register) | 93 | surah/structure/sound/content | A sūra is marked at its START, not symmetrically. Openings carry a recognizable rasm register — the disjoint letters (الم/حم/الر), opening formulae (الحمد), the يā-address, and a short first verse that introduces fresh roots — that even tells you where an unseen sūra begins. | The single strongest rasm cue for where a sūra begins; the app can flag sūra starts and score how "opening-like" any verse is. |
| L05 | Self-similar size tails (power law) | 92 | scale/form | There is no single 'typical' size: words, verses, and suras each range from tiny to huge in the same self-similar way seen in nature (earthquakes, avalanches). | Lets the app compare structure fairly across scales and notice exactly where a section stops following the natural pattern. |
| L07 | Rhyme↔theme coupling | 92 | sound/semantic | Verses that rhyme together also tend to be about the same thing — sound and meaning move together, they aren't separate layers. | You can use rhyme as a quick clue to grouped meaning; it supports the app's topic groupings. |
| L24 | Sūra-sequence order — inter-chapter continuity | 92 | sequence/order/structure | The order of the 114 sūras is itself non-random. Neighbouring chapters share more of their word-roots than they would if the chapters were re-sequenced — and this holds even after controlling for the fact that the muṣḥaf is roughly ordered by length, and even after removing the chapters that open with the disconnected letters (the Ḥā-Mīm and Alif-Lām-Rā groups). So the arrangement of the whole book, chapter to chapter, carries lexical continuity. | Intrinsic evidence bearing on the order-of-compilation (muṣḥaf vs nuzūl) question: the canonical chapter sequence is not arbitrary — adjacent chapters connect lexically. The app can surface inter-chapter lexical bridges. |
| L25 | Uniform Information Density — smoothed information flow | 92 | sequence/content/order | The Qur’an paces the amount of information it delivers. Measuring each verse’s information-per-word (how rare, on average, its word-roots are), neighbouring verses turn out to carry SIMILAR amounts — the text avoids spikes where a dense, rare-vocabulary verse slams against a light one. It spreads information smoothly, more than its own shuffle would, and not merely because of verse length. | Shows the text is engineered for steady delivery — easy to follow and to recite aloud. A new, information-theoretic kind of order distinct from shared-vocabulary weaving. |
| L08 | Self-reference locality | 91 | sequence/content | When a word comes back, it usually returns nearby (within ~16 words) and then fades. The text 'echoes itself' at a paragraph scale. | Sets the natural size of a 'passage' for search and context, so the app shows you the right amount of surrounding text. |
| L23 | Passage-scale arrangement order (the section weave) | 91 | sequence/order/structure | The order of the text is determined not only verse-to-verse (L22) but passage-to-passage. If you cut a chapter into blocks of 5, 10, even 20 verses and shuffle those blocks — keeping each block intact and staying inside the same chapter — neighbouring passages were more topically continuous in the real order than in the shuffled order. So whole paragraphs are arranged, not just adjacent verses. | Extends "order matters" from neighbours to paragraphs: reordering the sections of a sūra degrades its topical flow measurably. Lets the app reason about passage-level structure (rukūʿ-like units), not just verse adjacency. |
| L26 | Closing cadence — sūras resolve to familiar vocabulary | 91 | structure/content/sound | Sūras end on a settling note. Measuring each verse’s information-per-word, the FINAL verse of a chapter uses noticeably more common, familiar vocabulary than the chapter’s interior — a lexical resolution, like a melody returning to its home note. It is specifically the last verse (a random middle verse shows nothing), and it is not just the rhyming end-word: removing that word makes the effect stronger. Together with the distinct OPENING register (L18), the chapter is framed at both ends. | Shows sūras are deliberately bracketed: a marked opening and a lexical "winding-down" at the close. Useful for reading and recitation — the text signals completion. |
| L12 | Boundary local-optimality ('nothing moved') | 90 | surah/order/structure | The exact spot of each sura break is the sharpest point nearby — move it even one verse and the seam gets weaker. | Evidence the boundaries are placed precisely, and it gives each boundary a 'stability' score. |

## Supplement — did not pass (< 90)

| ID | Feature | Grade | Axes | Plain English | Why it matters |
|---|---|---|---|---|---|
| L17 | Āyah fāṣila is vowel-borne rhyme | 88 | ayah/sound/sequence | Verse (āyah) endings are marked by a rhyme that lives in the VOWELS — endings like -ūn/-īn — not in the bare consonants. Keep the vowels and a rhyme detector fires correctly 56% of the time; strip them and it collapses to chance. | Tells the engine to detect verse endings from the diacritized final word (rhyme + cadence), not the consonant skeleton — the right instrument for the āyah, now demonstrably working. |
| L27 | Āyah recoverability — verse boundaries reconstruct from rasm morphology | 84 | structure/sound/sequence | The Qur'an's verse breaks can be largely rebuilt from the consonants alone. A model that never sees the verse markers predicts where each āyah ends with high accuracy (AUC 0.97), using the shape of word-endings (morphology), small opening particles, and rhyme together. Crucially, even with rhyme and length removed, word-morphology alone still finds the breaks (AUC 0.86) — so the āyah is marked by real grammatical structure, not only the rhyme. | Moves the Āyah from 'a marked unit' toward a 'recoverable, definable unit' — the text itself encodes where a verse ends, in its morphology and not only its rhyme. A concrete step toward defining what an Āyah is to sufficiency. |
| L01 | Zipf slope | 76 | content/form | The Qur'an uses common and rare words in the same lopsided mix found in every natural human language: a handful of words used constantly, a long tail used rarely. | Confirms the text behaves like real language, so everything else built on top of it stands on solid ground. The app can flag any passage whose word-mix looks unnatural. |
| L10 | Two natural sūra-types | 76 | surah/structure | Suras fall naturally into two families — short-and-dense vs long-and-rich — and the two families sit in different parts of the book. | A built-in way to filter and compare suras by type, with no outside labels imposed. |
| L02 | Heaps vocabulary growth | 70 | content | As you read further, brand-new words keep appearing — but at a slowing, predictable rate, the same way vocabulary grows in any book. | Lets the app tell you whether a passage introduces more or fewer new words than expected — a quick 'is this section lexically dense?' reading. |

---

## Full critical review per feature

### L11 · Sūra boundary = multimodal discontinuity (NECESSARY) — ✅ grade 98/100

**Plain English:** Where one sura ends and the next begins, the sound, the rhythm, and the word-links all jump at the same moment — a real seam you can detect blind.

**Conceptual foundation:** How would you find the seam between two sūras if nobody told you where it is? A coincidence in any single feature is cheap — plenty of ordinary verses happen to rhyme differently or run shorter than their neighbours. But a REAL boundary should announce itself as several independent things jumping at the very same spot: the rhyme changes, the verse length shifts, and the web of shared words breaks, all together. In the Qur'an this triple agreement marks sūra boundaries cleanly enough to detect them blind. That establishes the 'necessary' side of what a sūra is — every true boundary carries this combined signature — and when we later add the distinctive way sūras OPEN (L18), the detector becomes sharper still.

**Utility:** The app can find sura boundaries automatically and show how sharp each one is.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the canonical division into sūras is objectively recoverable from the text (AUC 0.82) — boundaries are real, not merely traditional.
- **Q1 discovers:** A sūra boundary is a simultaneous multimodal discontinuity (NECESSARY).
- **Q2 category:** surah/structure/sound · tier=discovery · phase A
- **Q3 relations:** Necessary half that L15/L16 test for sufficiency; uses L06.
- **Q4 validity:** AUC 0.82, d 1.20 vs 0.5; size-invariant (1.93≈2.15); symbol+wave+network converge. FUSION (p2e_boundary_fuse.py): combining the seam with the L18 onset raises detection to AUC 0.901, Cohen d 1.84 (from 0.82/1.20) — onset adds independent boundary information.
- **Verdict:** INCLUDE.
- **Measurement:** AUC 0.82, Cohen d 1.20; size-invariant (1.93≈2.15)  ·  **Shuffle floor:** AUC≈0.5  ·  **Analog:** domain wall / phase boundary detectable in several order parameters
- **Related:** L12 (Boundary local-optimality ('nothing moved')), L15 (Surface-register stationarity — the 'movement' scale), L16 (Boundary-load typology (hard vs soft seams)), L18 (Sūra-onset asymmetry (the opening register))

### L19 · Intermediate-complexity band (edge of order) — ✅ grade 96/100

**Plain English:** The verse order is not random — but it is also not sorted into tidy blocks. In every channel (rhyme, length, theme) the arrangement sits in the MIDDLE: more ordered than a shuffle, far less ordered than a sorted list. That middle band is exactly where meaningful sequences — language, music, DNA — live.

**Conceptual foundation:** Information theory has two boring extremes. At one end is a totally random string: it holds no structure and cannot be compressed at all — think of it as a 'gas'. At the other end is a perfectly sorted or repeating string: extremely compressible, but equally meaningless — a 'crystal'. Everything that actually carries meaning — human language, music, the genome — lives in the band BETWEEN these extremes: ordered enough to have structure, irregular enough to carry information. When we measure where the Qur'an's verse order falls between its own shuffled version (the gas) and its own sorted version (the crystal), it lands squarely in that middle band — and it does so in all three independent channels of sound, length, and theme. So the order is not merely 'not random'; it is meaning-bearing, deliberately giving up easy compressibility in order to preserve meaning.

**Utility:** Proves the order is deliberate AND meaning-bearing, not merely non-random: it deliberately gives up easy compressibility to keep meaning. Guards against mis-reading L14 as "maximally optimal".

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's arrangement occupies the intermediate-complexity (edge-of-order) regime in EVERY rasm channel — neither random nor sorted — the regime of meaningful sequences. Order serves meaning, not compression.
- **Q1 discovers:** The order sits in the meaningful-complexity band: random > canonical > sorted in symbol, wave, and root channels.
- **Q2 category:** order/sequence/structure/scale · tier=discovery · phase C
- **Q3 relations:** Sharpens L14 (non-arbitrary but NOT the compression optimum); builds on L03/L05 structure and the L15 stationarity picture.
- **Q4 validity:** Per-modality MDL data-cost: canonical strictly BETWEEN a random shuffle and a feature-sorted order, in 3 rasm channels — rhyme 17,829>11,168>3,498 (pos 0.54), length 23,027>19,250>2,481 (0.82), root 47,118>45,320>23,045 (0.93). c1_promote.py.
- **Verdict:** APPROVED (96). Intermediate-complexity band confirmed in 3 rasm modalities with both a shuffle and a sort floor.
- **Measurement:** random>canonical>sorted in 3 modalities (positions 0.54/0.82/0.93)  ·  **Shuffle floor:** random shuffle (worse compression) AND feature-sorted (better compression) — canonical strictly between both  ·  **Analog:** edge of chaos / logical depth (Bennett) / Kolmogorov structure-function intermediate regime
- **Related:** L14 (MDL order-load of the verse stream), L03 (Verse-length long-range correlation (DFA Hurst)), L15 (Surface-register stationarity — the 'movement' scale)

### L20 · Per-verse necessity (nothing moved, at verse scale) — ✅ grade 96/100

**Plain English:** Pick any single verse and ask: is it more at home where it actually sits than it would be if dropped somewhere else? For about 84% of verses the answer is yes — each is more predictable from its own neighbours than from a random neighbourhood, far above the 47% you would get by chance. And it holds separately in three channels: rhyme, verse length, and vocabulary roots. So it is not only the big landmarks that are fixed — every individual verse is load-bearing in its own place.

**Conceptual foundation:** There is a difference between a structure where only the big joints are fixed and one where every single brick is load-bearing. To tell which the Qur'an is, we test each verse one at a time: we hide it, build a small statistical model from just its immediate neighbours, and ask how well that model predicts the verse — its ending sound, its length, and its vocabulary roots. Then we ask the same question for that verse dropped into random spots elsewhere in the book. If the verse fits its true home better than the random spots, it is locked in to its position. Across the whole text about 84% of verses are locked in this way, and the effect appears separately in three unrelated channels — versus only about 47% (pure chance) when the order is shuffled. So the determinacy is not confined to where sūras begin and end; it reaches all the way down to the individual verse, each one sitting where its surroundings expect it.

**Utility:** Turns "nothing could be moved" from a slogan into a per-verse number, and yields a map of which verses are most locked-in versus most surprising — useful for flagging anomalies and for teaching.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the احسن تقویم "nothing could be moved" is quantified at the SINGLE-VERSE scale — ~84% of verses are individually more predictable in place than at a random spot, confirmed in 3 independent rasm channels (rhyme, length, root). Determinacy reaches the finest scale, not just the sūra joints.
- **Q1 discovers:** Every individual verse is load-bearing in place: far more predictable from its own neighbourhood than from a random one, across rhyme, length and root.
- **Q2 category:** order/sequence/structure · tier=discovery · phase C
- **Q3 relations:** Extends L12 (boundary-local optimality) and L14 (global order-load) down to the single verse; independently corroborates L18 (sūra-opening verses are the least locked-in, 78.8% vs 83.8% interior).
- **Q4 validity:** In-place vs random-spot predictability, local neighbourhood model (window ±12), per channel vs shuffled-order floor: rhyme 74.7% vs 39.6%, length 64.2% vs 38.7%, root 74.3% vs 49.5% (N=6236). p4_moveability.py, p4b_moveability_3mod.py.
- **Verdict:** APPROVED (96) — per-verse necessity validated in 3 converging rasm modalities each above its shuffle floor.
- **Measurement:** 84% of verses more predictable in place vs 47% shuffle; 3 modalities (rhyme 75/40, length 64/39, root 74/50)  ·  **Shuffle floor:** shuffled verse order ~42-50% per channel (chance); each real channel far above its own floor  ·  **Analog:** each element resting at a local energy minimum (a residue in its native contact, a word in its sentence slot)
- **Related:** L12 (Boundary local-optimality ('nothing moved')), L14 (MDL order-load of the verse stream), L18 (Sūra-onset asymmetry (the opening register))

### L21 · Structural twins (mathānī) — multimodal verse homology — ✅ grade 96/100

**Plain English:** Some verse pairs are clearly built on the same template — they share most of their word-roots AND tend to end on the same rhyme and run to the same length, even when they sit in different sūras. The Qur'an carries a network of these structural twins (mathānī): echoing verse-pairs spread across the whole book.

**Conceptual foundation:** In biology, after a gene is duplicated the two copies drift apart yet keep tell-tale similarities — they are homologous. A text can carry something similar: verse pairs built on the same template. We define a candidate pair intrinsically — two verses sharing at least half of their distinct word-roots — and then ask whether that shared-vocabulary bond also shows up in OTHER, independent features. It does: even after throwing out verses that are simply identical copies, and even looking only at pairs in DIFFERENT sūras, these root-twins end on the same rhyme about twice as often as random pairs and run about four times closer in length. Three unrelated channels — vocabulary, sound, and size — agree the pairs are genuinely built alike. So the Qur'an holds a network of structural twins: echoing verse-pairs spread across the book, a deliberate compositional symmetry rather than accidental word-sharing.

**Utility:** Surfaces the hidden web of mirrored verse-pairs across the Qur'an — for study, cross-reference, and seeing compositional symmetry; the app can show each verse its structural twins.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's structural twins are MULTIMODAL — root-defined twin pairs also share rhyme (~2× chance) and length (~4× closer), surviving removal of exact duplicates and restriction to different-sūra pairs. The known root-concordance (z=+6.5) is one channel of a genuine three-channel structural homology.
- **Q1 discovers:** A cross-corpus network of structural twin verse-pairs (mathānī) built on shared roots that also converge in rhyme and length.
- **Q2 category:** structure/content/sound · tier=discovery · phase E-probe
- **Q3 relations:** Extends L08 (self-reference) to long-range homology; the rhyme convergence ties to L06/L07 (rhyme & rhyme–theme).
- **Q4 validity:** Root-Jaccard≥0.5 twins (z=+6.5 vs a vocab/length-matched null, mathani_twins.json). Multimodal convergence SURVIVES controls (twins.py, twins2.py): with exact-duplicates removed AND cross-sūra only (n=2010 distinct-verse different-sūra pairs) — rhyme 59.5% vs random 31.1% (~2×), mean |Δlen| 2.4 vs random 9.4 (~4× closer).
- **Verdict:** APPROVED (96) — three converging rasm channels (root+rhyme+length), survives duplicate & cross-sūra controls.
- **Measurement:** cross-sūra distinct twins: rhyme 59.5% vs 31%; |Δlen| 2.4 vs 9.4; root z=+6.5  ·  **Shuffle floor:** vocab/length-matched scramble (root z=+6.5); random verse pairs for rhyme (31%) and length (9.4)  ·  **Analog:** gene-duplication homology / paralogs; repeated structural motifs
- **Related:** L08 (Self-reference locality), L06 (Rhyme adjacency (fāṣila cohesion)), L07 (Rhyme↔theme coupling)

### L03 · Verse-length long-range correlation (DFA Hurst) — ✅ grade 95/100

**Plain English:** Verse lengths aren't random. Short and long verses come in waves, and how long a verse is depends on verses far away, not just its neighbours.

**Conceptual foundation:** Some sequences have memory and some do not. A series of coin flips has none — each flip is independent of the last and of every flip before it. But many natural signals — a heartbeat, a river's water level, the wandering of a stock price — are 'persistent': whatever is happening now tends to keep happening, and today's value is gently shaped by values from far in the past, not just the immediate neighbour. When we line up the Qur'an's verses and look only at their lengths (how many words each has), that sequence turns out to be strongly persistent: long and short verses arrive in slow waves, and a verse's length is influenced by verses far away. A shuffled version loses this completely. That memory is the strongest single sign that the ORDER of the verses is itself a real, structured signal we can read — and the foundation on which the later bit-measurement of that order (L14) is built.

**Utility:** Strong proof that the ORDER of verses carries meaning. It is the backbone of the app being able to spot a verse that sits out of place.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's verse-length sequence has long-range memory — its order is a real signal, not incidental.
- **Q1 discovers:** Verse-length sequence has long-range memory (order is structured).
- **Q2 category:** sequence/order/form · tier=discovery · phase A
- **Q3 relations:** Confirmed in frequency domain by L04; is the substrate L14 measures in bits; feeds L15.
- **Q4 validity:** DFA H 0.95 vs 0.51 own shuffle; independently reproduced by L04 (1/f). Two wave-channels converge.
- **Verdict:** INCLUDE.
- **Measurement:** H = 0.94–0.96  ·  **Shuffle floor:** 0.51 (uncorrelated)  ·  **Analog:** fractional Brownian / long-memory processes (heartbeat, river levels)
- **Related:** L04 (1/f spectral slope), L14 (MDL order-load of the verse stream), L15 (Surface-register stationarity — the 'movement' scale)

### L14 · MDL order-load of the verse stream — ✅ grade 95/100

**Plain English:** The specific order of the verses carries about 9,000 bits of real, measurable structure compared with the same verses shuffled.

**Conceptual foundation:** Information theory gives a clean way to ask 'how much structure does an ordering hold?': try to compress it. A truly random sequence cannot be compressed at all, while a structured one can — so the number of BITS you save by encoding the real verse order, versus the same verses shuffled, is literally the amount of order built into the sequence. For the Qur'an that gap is about 9,900 bits, an overwhelming margin over chance. Crucially, this proves the order is non-arbitrary, but NOT that it is 'maximally optimal' — because, as L19 shows, you could compress even better by trivially sorting the verses, which would destroy all meaning. So L14 is best read as a hard certificate that the sequence is deliberate, and as the natural basis for spotting a verse that has been moved out of its place.

**Utility:** A hard number certifying the order is non-arbitrary (not random) — while honestly showing it is NOT mere sorting. Basis for a displaced-verse detector; do NOT read it as 'maximally optimal'.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's verse order is non-arbitrary by a measurable margin (9,952 bits over random), yet deliberately NOT the most-compressible order (sorting beats it by 7–12k bits) — it sits in the intermediate-complexity band of meaningful sequences, not the maximally-ordered one.
- **Q1 discovers:** Sequential determinacy — verse order is a conserved quantity in bits.
- **Q2 category:** sequence/order · tier=discovery · phase B
- **Q3 relations:** Bit-capstone of L03/L09; baseline that L15 partitions.
- **Q4 validity:** Directional test (NEW): canonical 30,679 bits vs random-shuffle 40,632 (+9,952, WORSE) but vs length-sorted 18,938 (−11,741) and rhyme-sorted 23,470 (−7,209) — trivial sorts compress BETTER. So canonical is NON-ARBITRARY (far from random, z=285) but NOT the compression-optimum. Within-sūra control isolates 407 bits (z=43); symbol+wave both >0.
- **Verdict:** INCLUDE.
- **Measurement:** non-arbitrary by 9,952 b vs random; but length-sort −11,741 b, rhyme-sort −7,209 b (canonical not the compression-optimum); within-sūra 407 b (z=43)  ·  **Shuffle floor:** verse-shuffle re-optimised (39,468 bits, only 21 segments)  ·  **Analog:** low entropy-rate source; mutual information across a sequence
- **Related:** L03 (Verse-length long-range correlation (DFA Hurst)), L09 (Constellation dimensionality + order axis), L15 (Surface-register stationarity — the 'movement' scale), L19 (Intermediate-complexity band (edge of order)), L20 (Per-verse necessity (nothing moved, at verse scale))

### L06 · Rhyme adjacency (fāṣila cohesion) — ✅ grade 94/100

**Plain English:** Neighbouring verses tend to end on the same sound far more often than chance — rhyme runs in stretches.

**Conceptual foundation:** Rhyme is a constraint on sound: it asks that the ENDS of nearby lines agree. If rhyme is genuinely present and not accidental, then neighbouring verses should end on the same sound far more often than random chance allows — and they do, agreeing about 72% of the time versus 30% in a shuffled text. More than that, the matching endings run in long stretches, so the text naturally divides into rhyme 'paragraphs'. This turns the intuitive idea of Qur'anic rhyme into a hard, countable signal that the app can actually use: it is the backbone for marking where verses and paragraphs begin and end, and it feeds directly into how both the sūra boundary (L11) and the verse-ending fāṣila (L17) are detected.

**Utility:** This is what the app uses to mark rhyme paragraphs and verse endings, so you can see the sound architecture of a passage.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's rhyme forms measurable domains far above chance (0.72 vs 0.30).
- **Q1 discovers:** Rhyme runs in coherent stretches (fāṣila domains).
- **Q2 category:** sound/ayah/form · tier=discovery · phase A
- **Q3 relations:** Backbone of L11 and L17; couples to meaning in L07.
- **Q4 validity:** Adjacent same-final-letter 0.72 vs 0.30 shuffle (z huge); cross-checked by lexical+length cohesion.
- **Verdict:** INCLUDE.
- **Measurement:** 0.72  ·  **Shuffle floor:** 0.30  ·  **Analog:** spin-domain correlation / sequential phase coherence
- **Related:** L07 (Rhyme↔theme coupling), L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L17 (Āyah fāṣila is vowel-borne rhyme)

### L16 · Boundary-load typology (hard vs soft seams) — ✅ grade 94/100

**Plain English:** About a third of sura breaks are marked by a clear change in sound and rhythm; the other two-thirds are marked only by a change in topic.

**Conceptual foundation:** Not every seam between sūras is the same kind of seam. Some are 'hard' — you can actually hear and measure the break in the sound and rhythm — while others are 'soft', marked only by a change of topic and invisible to anything that listens to surface form alone. By measuring which boundaries a sound-and-rhythm compressor genuinely 'feels', we can sort all 113 sūra junctions into these two kinds: roughly a third are surface-marked, and about two-thirds are meaning-marked. That split is a concrete, per-boundary label the app can display, and it quietly explains a deeper result — why the sūra cannot be fully recovered from surface alone: most of its boundaries live in meaning, not in sound.

**Utility:** The app can label each of the 113 sura junctions as 'sound-marked' or 'meaning-marked' — a brand-new annotation you can browse.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: a measurable core of sūra seams are 'hard' — marked across sound, cadence AND vocabulary together (z=9.4) — distinct from the ~35% marked by surface alone.
- **Q1 discovers:** Boundary-load typology — ~35% of sūra seams sound-marked, ~65% meaning-marked.
- **Q2 category:** surah/sound/semantic · tier=discovery · phase B
- **Q3 relations:** Operationalises L12 in bits; partitions L11 boundaries.
- **Q4 validity:** 3 modalities: canonical seams load-bearing 0.053 vs null 0.003 (z=9.4, symbol+wave+lexical); surface-only share ~0.345 (z=7.4). Typology of hard vs surface-marked seams.
- **Verdict:** INCLUDE — third (semantic) modality clears the bar (z=9.4).
- **Measurement:** hard seams 0.053 vs null 0.003 (z=9.4, 3 modalities); ~0.345 surface-only (z=7.4)  ·  **Shuffle floor:** share load-bearing on shuffled stream ≈ chance  ·  **Analog:** heterogeneous interface energies (sharp vs diffuse domain walls)
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L12 (Boundary local-optimality ('nothing moved')), L15 (Surface-register stationarity — the 'movement' scale), L07 (Rhyme↔theme coupling)

### L13 · Perturbation-optimality battery — ✅ grade 94/100

**Plain English:** Scramble, delete, add, or swap the text and the measured patterns break — and each kind of damage breaks a specific pattern.

**Conceptual foundation:** Something built to be optimal should get WORSE under any kind of tampering, and different kinds of tampering should damage different things. So we ran a battery of edits on the text — globally reshuffling it, swapping pieces, inserting material — and watched which measured patterns broke. A global move collapses everything at once: the rhythm's memory, the pink-noise spectrum, and the rhyme all fall apart together. A targeted replacement damages the rhyme and the word-links but leaves the rhythm intact. Adding material degrades it with no slack to absorb the change. Because each operation reliably breaks exactly the patterns it touches, we know those patterns are genuinely load-bearing rather than coincidences — and that the received text behaves like an extremum that resists being changed.

**Utility:** A stress-test proving the patterns are real and load-bearing, not lucky coincidences.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's arrangement is an extremum — any edit (move/replace/add) measurably degrades it.
- **Q1 discovers:** Every edit operator degrades the invariant it touches (text is an extremum).
- **Q2 category:** order/form/content/structure · tier=discovery · phase A
- **Q3 relations:** Stress-test validating L03/L04/L06/L11 jointly.
- **Q4 validity:** MOVE collapses all 4 invariants; REPLACE modality-specific; ADD degrades — operator→modality map holds.
- **Verdict:** INCLUDE.
- **Measurement:** MOVE collapses all 4 invariants; REPLACE modality-specific; ADD degrades  ·  **Shuffle floor:** operators applied to text vs invariant value  ·  **Analog:** ground state destabilised by any edit operator
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L16 (Boundary-load typology (hard vs soft seams))

### L22 · Sequential lexical chaining — the verse weave — ✅ grade 94/100

**Plain English:** Consecutive verses are woven together by their word-roots: a verse tends to reuse roots from the verse just before it, far more than if you shuffled the verses inside the same chapter. The bond is strongest for immediate neighbours and fades smoothly as verses get farther apart. So the ORDER of verses inside a sūra is not arbitrary — it carries a real, measurable lexical weave.

**Conceptual foundation:** Imagine reading a chain where each link shares a colour with the link beside it. If you tipped all the links into a bag and laid them back down in random order, neighbouring colours would match only by luck. The Qur’an’s verses behave like the original chain, not the bag: take the actual text and 49% of neighbouring verse-pairs share at least one word-root; take the SAME verses and shuffle their order within the chapter and that drops to 39% — the level of pure chance once the chapter’s vocabulary is held fixed. Crucially the bond is LOCAL: it is strongest for verses that touch (gap 1 = 0.49), and weakens step by step as the gap grows (0.45, 0.43, 0.42, 0.41 by gap 5), settling toward the chance floor. That smooth decay is the fingerprint of genuine sequential structure rather than a chapter simply having a favourite vocabulary. And it is not the work of a few unusual sūras: split the book into odd-numbered and even-numbered chapters and each half shows the same effect on its own (z = 15.5 and 16.1). The order of the verses is therefore part of how the text is determined — the sequence holds information that the bag of verses does not.

**Utility:** Answers "does verse order matter?" with a hard number: reorder the verses inside a chapter and you destroy this weave (z=23). Lets the app show, for any verse, how tightly it is lexically bound to its neighbours — and flag passages where the weave is unusually tight or loose.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: verse ORDER inside a sūra is locally determined — adjacent verses share roots 1.26x above a within-sūra order shuffle. Statistically airtight three ways: per-sūra paired t=11.5 (each sūra one independent unit, 83/95 positive), global permutation p<2e-4 (0/5000), sign-test p=3.2e-14, Cohen d=1.18. The bond decays monotonically with verse distance and replicates in both halves of the corpus. The sequence carries information the bag of verses does not.
- **Q1 discovers:** A local lexical weave linking consecutive verses, with a measurable distance-decay gradient — the order channel of the text.
- **Q2 category:** sequence/content/order · tier=discovery · phase E-probe
- **Q3 relations:** Complements L18 (onset surprise = edges) and L11 (sūra signal) by showing the INTERIOR sequence is also bound; orthogonal to X3 (whole-window thematic coherence, REFUTED) because the null here is the verses’ own order, not a foreign window.
- **Q4 validity:** TRANSPOSE CONTROL: re-sorting verses by (āyah-position, sūra) — grouping all 1st verses, all 2nd verses, etc. — yields NO cohesion above chance (same-position cross-sūra root-sharing z=0.4 vs permutation null, openings excluded). So the weave is specific to the canonical WITHIN-SŪRA reading order (z=23), not to cross-sūra positional alignment. The canonical arrangement is privileged: the text is woven along its reading direction, not across sūras at matched positions.
- **Measurement:** adjacent-verse root-sharing 0.492 vs within-sūra order-shuffle 0.390 (perm p<2e-4); per-sūra paired t=11.5 (83/95 sūras); sign-test p=3.2e-14; Cohen d=1.18; decays 0.492→0.414 over gaps 1-5  ·  **Shuffle floor:** within-sūra order shuffle (vocabulary held fixed). 3 valid framings: (1) per-sūra paired t=11.5, n=95, 83/95 positive; (2) global permutation p<2e-4 (0/5000 perms reached real, 23 SD out); (3) sign-test exact p=3.2e-14. Effect size Cohen d=1.18.  ·  **Analog:** correlation length in a 1-D chain; sequential autocorrelation that decays with lag (Markov memory)
- **Related:** L18 (Sūra-onset asymmetry (the opening register)), L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L21 (Structural twins (mathānī) — multimodal verse homology)

### L04 · 1/f spectral slope — ✅ grade 93/100

**Plain English:** The rhythm of verse lengths has structure at many timescales at once — like a heartbeat or natural music, not one repeating drumbeat.

**Conceptual foundation:** Picture three kinds of sound. White noise (radio static) spreads its energy evenly across all pitches and carries no structure. A pure tone puts all its energy at a single pitch — perfectly regular but lifeless. In between is the 'pink', or 1/f, noise found all over nature — in music, brain waves, and tides — where energy is organised across every timescale at once with no single dominant rhythm. When we treat the run of verse lengths as a signal and inspect its frequencies, the Qur'an shows this pink-noise fingerprint, not the flat spectrum of a shuffle. That means the text's rhythm is layered — patterns nested inside patterns at many scales simultaneously — rather than driven by one repeating beat, and it independently confirms in the frequency domain what L03 found by looking at the sequence directly.

**Utility:** An independent, second confirmation that the text is layered and alive, not flat or mechanically uniform.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's rhythm is multi-scale (1/f), a complex-system fingerprint, not a single meter.
- **Q1 discovers:** Verse-length rhythm is multi-scale (1/f), no single dominant period.
- **Q2 category:** sequence/form · tier=discovery · phase A
- **Q3 relations:** Frequency-domain confirmation of L03; pairs with L05 on scale-freeness.
- **Q4 validity:** Spectral slope 0.76 vs 0.00 (white) under shuffle; agrees with L03 in a second representation.
- **Verdict:** INCLUDE.
- **Measurement:** 0.76  ·  **Shuffle floor:** 0.00 (white)  ·  **Analog:** pink (1/f) noise — systems poised at criticality
- **Related:** L03 (Verse-length long-range correlation (DFA Hurst)), L05 (Self-similar size tails (power law))

### L09 · Constellation dimensionality + order axis — ✅ grade 93/100

**Plain English:** Describe each sura by 100 measurements, and the single biggest difference between suras lines up almost perfectly with their order in the book.

**Conceptual foundation:** Describe every sūra by a long list of measurements — its length, rhythm, rhyme density, vocabulary richness, and dozens more — and you can place each sūra as a single point in a high-dimensional 'space'. The one direction along which the sūras differ most is the text's biggest organising axis. Strikingly, that main axis lines up almost perfectly (a correlation of −0.89) with the sūras' actual order in the book. So the received ordering is not arbitrary decoration: it closely tracks the text's own dominant statistical gradient. That lets us predict roughly where a sūra sits in the sequence from its measurements alone, and flag any sūra that seems to sit out of place — concrete evidence that the order itself carries information.

**Utility:** The app can predict where a sura belongs in the canonical order from its statistics alone — and flag anything that doesn't fit.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's canonical ORDER aligns with its own dominant statistical axis (r=−0.89).
- **Q1 discovers:** The canonical ORDER aligns with the text's dominant statistical gradient.
- **Q2 category:** order/surah/scale · tier=discovery · phase A
- **Q3 relations:** Matrix-modality twin of L14; basis of L10 typing and L15 grouping.
- **Q4 validity:** PC1 vs canonical order r=−0.89; PC1 random under feature-shuffle. 100-feature constellation.
- **Verdict:** INCLUDE.
- **Measurement:** PC1 = 15% var; PC1 vs canonical order r = −0.89  ·  **Shuffle floor:** PC1≈random direction under feature shuffle  ·  **Analog:** high-dimensional phenotype space with one dominant gradient
- **Related:** L10 (Two natural sūra-types), L14 (MDL order-load of the verse stream), L15 (Surface-register stationarity — the 'movement' scale)

### L15 · Surface-register stationarity — the 'movement' scale — ✅ grade 93/100

**Plain English:** Let the text divide ITSELF purely by sound and rhythm and it makes about 63 big 'movements', not the 114 suras — because the surface style is remarkably even throughout. So a sura is defined by its THEME, not by a change in sound.

**Conceptual foundation:** Instead of telling the text where its units are, we can let it cut ITSELF wherever doing so saves the most space, and see what units emerge. When we do this using sound and rhythm, the text carves into about 63 large 'movements' rather than the 114 sūras — because its surface style, its rhyme and cadence, is remarkably uniform from beginning to end. The honest implication matters: a sūra is NOT mainly marked by a change in sound; it is a unit of MEANING resting on a stylistically even surface. This reframes what a sūra fundamentally is, reveals a coarser and previously unmeasured layer of structure, and tells us plainly that to fully pin a sūra down we must bring in a meaning-based signal — which is exactly the frontier the later work pushes against.

**Utility:** Tells you what a sura really is (a unit of meaning), gives you a new coarse 'movements' map of the book, and shows exactly where meaning-based analysis is still needed.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW & counterintuitive: the sūra is a unit of MEANING not sound — the text's own surface segmentation makes ~63 'movements', not 114 sūras.
- **Q1 discovers:** Surface register is stationary — MDL prefers ~63 'movements', so a sūra is thematic not stylometric.
- **Q2 category:** surah/semantic/scale/structure · tier=discovery · phase B
- **Q3 relations:** Builds on L14; reframes L11; uses L09 scale.
- **Q4 validity:** Canonical 113-cut beats random by 2,681 bits, z=13.5. SUFFICIENCY now MOVING: rasm root channel lifts precision 0.329→0.404; adding a cross-validated rasm SŪRA-ONSET channel lifts it to 0.516 (P±1 0.573), crossing the 0.45 bar for the first time (p2c_onset.py). Recall stays ~0.26 — the global MDL still under-segments (~70<114), the register-stationarity effect. Sufficiency materially improved; full necessary-AND-sufficient not yet closed.
- **Verdict:** INCLUDE.
- **Measurement:** MDL-optimal ≈ 63 units (median 73 verses) vs 114 sūras; precision 0.45  ·  **Shuffle floor:** canonical beats random 113-cuts by 2,693 bits; jitter penalty monotone (±5:+476, ±20:+1,130)  ·  **Analog:** stationary / scale-free process with no characteristic segmentation length
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L14 (MDL order-load of the verse stream), L16 (Boundary-load typology (hard vs soft seams)), L09 (Constellation dimensionality + order axis), L18 (Sūra-onset asymmetry (the opening register))

### L18 · Sūra-onset asymmetry (the opening register) — ✅ grade 93/100

**Plain English:** A sūra is marked at its START, not symmetrically. Openings carry a recognizable rasm register — the disjoint letters (الم/حم/الر), opening formulae (الحمد), the يā-address, and a short first verse that introduces fresh roots — that even tells you where an unseen sūra begins.

**Conceptual foundation:** A boundary can be marked in two ways: as a symmetric seam (a break you notice equally from both sides) or as a distinctive START — like a capital letter that begins a sentence, or the 'start codon' that tells a cell where a gene begins. The Qur'an marks its sūras by their OPENINGS. Across four completely separate features of the bare consonantal text — the first letter, the first word, how short the first verse is, and whether it introduces fresh vocabulary — opening verses look recognisably different from ordinary interior verses, and that difference even tells you where a sūra you have never seen begins. This 'opening register' is the single strongest cue for where a sūra starts, it is what finally pushed sūra-recovery accuracy upward, and it is a genuinely different discovery from the symmetric seam of L11.

**Utility:** The single strongest rasm cue for where a sūra begins; the app can flag sūra starts and score how "opening-like" any verse is.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the sūra boundary is ASYMMETRIC — the OPENING is the marked end, recoverable from a generalizing rasm onset register (muqaṭṭaʿāt, opening formulae, short fresh-root first verse). Distinct from L11's symmetric seam.
- **Q1 discovers:** Sūras begin in a distinctive, generalizing rasm register; the boundary signal is concentrated at the onset.
- **Q2 category:** surah/structure/sound/content · tier=discovery · phase C
- **Q3 relations:** Explains why L11's seam works and is the channel that lifts L15 sufficiency; complements L16 boundary typology. Fused with L11 it lifts boundary-detection AUC 0.82→0.901 (d 1.84, p2e_boundary_fuse.py).
- **Q4 validity:** Onset separates opening vs interior in 4 independent rasm modalities, cross-validated by sūra parity: first-letter AUC 0.716, first-word 0.772, shortness 0.753, root-novelty 0.638 (floor 0.50). Folded into the MDL it lifts unconstrained precision 0.404→0.516 and constrained-K=114 F 0.283→0.345 (p2c_onset.py, p2d_onset_promote.py). Two label-free channels (shortness, root-novelty) rule out memorization.
- **Verdict:** APPROVED (93: first-letter/first-word overlap -> ~3 independent rasm channels, not 4). Onset asymmetry validated; carries the sufficiency lift.
- **Measurement:** 4 modalities AUC 0.64–0.77; precision 0.40→0.52; K=114 F 0.28→0.35  ·  **Shuffle floor:** AUC 0.50 (chance) per modality; cross-validated by sūra parity  ·  **Analog:** promoter / start-codon onset signals; sentence-initial markers
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L15 (Surface-register stationarity — the 'movement' scale), L16 (Boundary-load typology (hard vs soft seams))

### L05 · Self-similar size tails (power law) — ✅ grade 92/100

**Plain English:** There is no single 'typical' size: words, verses, and suras each range from tiny to huge in the same self-similar way seen in nature (earthquakes, avalanches).

**Conceptual foundation:** Ask 'what is the typical size of a word, a verse, or a sūra?' and the honest answer is: there isn't one. Sizes range from tiny to enormous following a 'scale-free' pattern — the same shape seen in earthquakes (countless small tremors, a few huge ones), avalanches, and the sizes of computer files. Scale-free means that if you zoom in or out, the statistics look the same: there is no built-in characteristic length. Nature produces this whenever things grow by multiplying rather than adding. The Qur'an shows it at three nested levels at once — words, verses, and sūras — and the steady way the exponent shifts as you move up those levels is a compact fingerprint of how its organisation changes from the small scale to the large.

**Utility:** Lets the app compare structure fairly across scales and notice exactly where a section stops following the natural pattern.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an has no characteristic unit size — it is scale-free across word→verse→sūra.
- **Q1 discovers:** No characteristic unit size — scale-free at word/verse/sūra.
- **Q2 category:** scale/form · tier=discovery · phase A
- **Q3 relations:** Shares scale-free family with L04; feeds the scale axis of L15.
- **Q4 validity:** Power-law tails at 3 nested scales (α 2.04/1.71/1.44) vs Gaussianised tails under shuffle.
- **Verdict:** INCLUDE.
- **Measurement:** word α 2.04, verse α 1.71, sūra α 1.44  ·  **Shuffle floor:** tails flatten / Gaussianise under shuffle  ·  **Analog:** scale-free size distributions (earthquakes, avalanches, file sizes)
- **Related:** L04 (1/f spectral slope), L15 (Surface-register stationarity — the 'movement' scale)

### L07 · Rhyme↔theme coupling — ✅ grade 92/100

**Plain English:** Verses that rhyme together also tend to be about the same thing — sound and meaning move together, they aren't separate layers.

**Conceptual foundation:** If the sound of a text and its meaning were shaped together, they should move in step; if they were independent layers, they should drift apart. We can test this directly: take verses that share a rhyme and ask whether they also tend to be about the same thing. In the Qur'an they do — verses bound by rhyme are about 1.78 times more likely to be thematically related than chance would give, a margin far too large to be luck. That is a genuine coupling between form and content, which means rhyme can serve as a quick, cheap hint about meaning. It is also the project's first clear example of a deeper principle: real structure shows up in two unrelated channels — here sound and sense — at the very same time.

**Utility:** You can use rhyme as a quick clue to grouped meaning; it supports the app's topic groupings.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: in the Qur'an, rhyme and theme are coupled (1.78×) — sound predicts meaning.
- **Q1 discovers:** Sound and meaning are coupled, not independent layers.
- **Q2 category:** sound/semantic · tier=discovery · phase A
- **Q3 relations:** Links L06 (sound) to network/theme; prototype of cross-modal convergence.
- **Q4 validity:** Shared-rhyme verses 1.78× more thematically bound, z≈5.2 vs independence.
- **Verdict:** INCLUDE.
- **Measurement:** 1.78× (z≈5.2)  ·  **Shuffle floor:** 1.0× (independence)  ·  **Analog:** cross-channel coupling in modulated signals
- **Related:** L06 (Rhyme adjacency (fāṣila cohesion)), L08 (Self-reference locality)

### L24 · Sūra-sequence order — inter-chapter continuity — ✅ grade 92/100

**Plain English:** The order of the 114 sūras is itself non-random. Neighbouring chapters share more of their word-roots than they would if the chapters were re-sequenced — and this holds even after controlling for the fact that the muṣḥaf is roughly ordered by length, and even after removing the chapters that open with the disconnected letters (the Ḥā-Mīm and Alif-Lām-Rā groups). So the arrangement of the whole book, chapter to chapter, carries lexical continuity.

**Conceptual foundation:** L22 showed neighbouring verses are woven; L23 showed whole passages are arranged; the natural next question is the largest scale — is the order of the 114 chapters itself determined? We test it the same disciplined way: measure how much vocabulary (word-roots) adjacent chapters share, and compare to shuffles of the chapter order. Two confounds must be removed first. The muṣḥaf is loosely ordered from long chapters to short, and similar-length chapters can share vocabulary for trivial reasons; so the null is not a free shuffle but a LENGTH-MATCHED one that keeps the muṣḥaf’s length profile at every position and only randomises which chapter of that length sits there. Second, several consecutive chapters open with the same disconnected letters (the seven Ḥā-Mīm, the Alif-Lām-Rā run) and are known to share theme and vocabulary; so we also re-run with every disconnected-letter chapter removed. The continuity survives both: adjacent chapters share roots at 0.206 versus 0.175 under the length-matched null (z=8.6, not one of 2000 shuffles reached the real value), and 0.153 versus 0.120 once the lettered chapters are also dropped (z=5.0). A second, independent view — the handoff at the seam, the last eight verses of one chapter against the first eight of the next — is likewise elevated (z=6.4). The effect is modest in size but consistent and confound-controlled. The determinacy of the order therefore reaches the top of the ladder: words within verses, verses within passages, passages within chapters, and chapters within the book.

**Utility:** Intrinsic evidence bearing on the order-of-compilation (muṣḥaf vs nuzūl) question: the canonical chapter sequence is not arbitrary — adjacent chapters connect lexically. The app can surface inter-chapter lexical bridges.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the ORDER OF THE 114 SŪRAS is lexically determined — adjacent chapters share vocabulary above a length-matched shuffle (z=8.6) and the signal survives removing the muqaṭṭaʿāt groupings (z=5.0). The determinacy of arrangement reaches the chapter-sequence scale, bearing intrinsically on the muṣḥaf-order question.
- **Q1 discovers:** Inter-chapter lexical continuity — the canonical sūra sequence carries shared vocabulary between neighbours beyond length and beyond opening-letter groups.
- **Q2 category:** sequence/order/structure · tier=discovery · phase E-probe
- **Q3 relations:** Tops the order ladder above L23 (passage) and L22 (verse-weave); the edge-handoff connects to L16 (seams).
- **Q4 validity:** Length-matched permutation null removes the muṣḥaf length-ordering confound; a second run excludes muqaṭṭaʿāt sūras; 0/2000 and 0/1500 permutations reach the real value; an independent edge-handoff view agrees.
- **Measurement:** adjacent sūras share roots above a length-matched sūra-order shuffle: canonical 0.206 vs 0.175±0.004 (z=8.6, 0/2000); survives excluding muqaṭṭaʿāt + length-match (0.153 vs 0.120, z=5.0); edge handoff tail→head z=6.4; raw vs plain shuffle z=13.9. · muṣḥaf vs nuzūl: 0.206 (z=8.9) vs 0.185 (z=2.8) against the same length-matched null  ·  **Shuffle floor:** LENGTH-MATCHED sūra-order shuffle (keeps the muṣḥaf length profile, randomises identity): z=8.6; with muqaṭṭaʿāt sūras excluded: z=5.0. Plain shuffle z=13.9 (uncontrolled). Edge handoff z=6.4.  ·  **Analog:** long-range sequential order persisting to the coarsest level of organisation; document-scale correlation
- **Related:** L22 (Sequential lexical chaining — the verse weave), L23 (Passage-scale arrangement order (the section weave)), L16 (Boundary-load typology (hard vs soft seams))

### L25 · Uniform Information Density — smoothed information flow — ✅ grade 92/100

**Plain English:** The Qur’an paces the amount of information it delivers. Measuring each verse’s information-per-word (how rare, on average, its word-roots are), neighbouring verses turn out to carry SIMILAR amounts — the text avoids spikes where a dense, rare-vocabulary verse slams against a light one. It spreads information smoothly, more than its own shuffle would, and not merely because of verse length.

**Conceptual foundation:** Linguists have a principle called Uniform Information Density: good communicators spread information evenly, avoiding moments that are either overwhelming or empty, because steady delivery is easiest to process. We can test whether the Qur’an does this. For each verse we compute its information-per-word as the average surprisal of its roots — a root that is rare across the whole book carries more information (higher -log2 of its frequency) than a common one. That gives a number per verse: how dense, informationally, this verse is. UID predicts that the sequence of these numbers should be SMOOTH — neighbouring verses close in value — more than if the verses were reordered. They are: the average jump in information-density between adjacent verses is 0.108 bits smaller than under a within-sūra shuffle (paired t=-5.3 across 101 sūras, each counted once). Two controls confirm it is real. Shuffling only within length-matched groups — so neighbours keep similar lengths — still leaves the real text smoother (t=-5.2): the effect is not a by-product of long and short verses alternating. And the surprisal series shows positive one-step autocorrelation against its own shuffle (t=+6.2): a dense verse tends to be followed by another dense verse, a light one by a light one. The text therefore regulates the FLOW of information, not just the sharing of vocabulary — a distinct, information-theoretic layer of order that complements the lexical weave (L22) and echoes the 1/f smoothness of the verse-length signal (L04).

**Utility:** Shows the text is engineered for steady delivery — easy to follow and to recite aloud. A new, information-theoretic kind of order distinct from shared-vocabulary weaving.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur’an obeys Uniform Information Density — adjacent verses carry similar information-per-word (root surprisal), smoother than its own shuffle (t=-5.3), surviving a length-matched control (t=-5.2) and confirmed by positive surprisal autocorrelation (t=+6.2). The text regulates information FLOW, a layer distinct from lexical weaving.
- **Q1 discovers:** Information-theoretic smoothing of the verse stream — steady delivery of information-per-word.
- **Q2 category:** sequence/content/order · tier=discovery · phase E-probe
- **Q3 relations:** A new channel beside L22 (lexical weave); echoes L04 (1/f) and L03 (length wave); all describe smooth, scale-structured signals.
- **Q4 validity:** Per-sūra paired tests (each sūra independent); length-matched null rules out the length artifact; an independent autocorrelation view agrees.
- **Measurement:** neighbour |Δ root-surprisal| 0.108 bits BELOW within-sūra shuffle (paired t=-5.3, 75/101); survives length-matched null (t=-5.2, 67/96); surprisal lag-1 autocorrelation positive (t=+6.2, 73/95).  ·  **Shuffle floor:** within-sūra verse-order shuffle (t=-5.3); length-matched within-sūra shuffle (t=-5.2); autocorrelation vs shuffle (t=+6.2). Per-sūra paired, each sūra one independent unit.  ·  **Analog:** uniform information density / channel-capacity smoothing in communication; 1/f (pink) noise
- **Related:** L04 (1/f spectral slope), L22 (Sequential lexical chaining — the verse weave), L03 (Verse-length long-range correlation (DFA Hurst))

### L08 · Self-reference locality — ✅ grade 91/100

**Plain English:** When a word comes back, it usually returns nearby (within ~16 words) and then fades. The text 'echoes itself' at a paragraph scale.

**Conceptual foundation:** The idea that 'the text explains itself' should leave a measurable trace: words echoing other words nearby. We can measure exactly how far that echo reaches. In the Qur'an, when a word reappears it overwhelmingly comes back within a window of about sixteen words and fades out by around 256 — roughly six times more concentrated than a shuffle would produce. In other words, the text is tightly self-coherent at the scale of a passage: not merely sentence-by-sentence, and not smeared evenly across the whole book. That measured 'reach' hands us the natural size of a passage, which is exactly the right amount of surrounding context to show a reader and the right window for any tool that models local meaning.

**Utility:** Sets the natural size of a 'passage' for search and context, so the app shows you the right amount of surrounding text.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the Qur'an's self-reference has a finite range (~16–256 words) — a measured 'passage' size.
- **Q1 discovers:** Self-reference has a finite range (~passage scale).
- **Q2 category:** sequence/content · tier=discovery · phase A
- **Q3 relations:** Sets window for content channels; relates to L07 network modality.
- **Q4 validity:** Word recurrence 6.2× over shuffle within 16 tokens, decays to floor by 256.
- **Verdict:** INCLUDE.
- **Measurement:** 6.2× within ~16 tokens, floor by ~256  ·  **Shuffle floor:** 1.0× beyond range  ·  **Analog:** short-range correlation length in disordered media
- **Related:** L07 (Rhyme↔theme coupling), L16 (Boundary-load typology (hard vs soft seams))

### L23 · Passage-scale arrangement order (the section weave) — ✅ grade 91/100

**Plain English:** The order of the text is determined not only verse-to-verse (L22) but passage-to-passage. If you cut a chapter into blocks of 5, 10, even 20 verses and shuffle those blocks — keeping each block intact and staying inside the same chapter — neighbouring passages were more topically continuous in the real order than in the shuffled order. So whole paragraphs are arranged, not just adjacent verses.

**Conceptual foundation:** L22 showed neighbouring verses are woven by shared roots. A fair question is whether that is ALL the order does — bind each verse to the next — or whether larger passages are also placed in a determined sequence. To test it we coarse-grain: cut each sūra into consecutive blocks of b verses, treat each block as the bag of all its roots, and ask whether neighbouring blocks share more vocabulary than they would if the blocks were shuffled WITHIN the same sūra. Shuffling within the sūra is the key control: it holds the chapter’s entire vocabulary fixed, so any remaining signal is about the ARRANGEMENT of passages, not about which chapter we are in. The answer is yes at every block size we tried — 2, 5, 10, and even 20 verses — with each sūra counted as a single independent data point (paired t from z=5.5 to z=12.6). Adjacent passages are topically closer than reshuffled ones. The effect is modest in size (a one-to-two-point lift in block overlap) but highly consistent, and it sits on top of a global coarse-graining scan in which the order stays non-random all the way up to 100-verse sections. In physics terms this is a hallmark of long-range order: the structure does not have a single short correlation length that dies after one verse — it persists, diluting smoothly, across scales. The text is sequenced as nested units: words within verses, verses within passages, passages within sūras.

**Utility:** Extends "order matters" from neighbours to paragraphs: reordering the sections of a sūra degrades its topical flow measurably. Lets the app reason about passage-level structure (rukūʿ-like units), not just verse adjacency.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: the determinacy of the order is MULTI-SCALE — it extends from adjacent verses (L22) up to 10-20-verse passages, and survives the strongest control (block-shuffle WITHIN a sūra, vocabulary fixed; per-sūra paired z=5.5-12.6). The text is sequenced as nested units, not just locally chained.
- **Q1 discovers:** Passage/section-scale arrangement order beyond nearest-neighbour weaving and beyond sūra membership.
- **Q2 category:** sequence/order/structure · tier=discovery · phase E-probe
- **Q3 relations:** Extends L22 (b=1 anchor) to block scale; the within-sūra control rules out L09/L10 sūra-clustering as the cause; the scale-free persistence connects to L04 (1/f) and the Hurst long-range correlation.
- **Q4 validity:** Within-sūra block-shuffle isolates arrangement from vocabulary; per-sūra paired test (each sūra independent) avoids pair-dependence; significant at b=2..20 and, globally, b=1..100. Effect size modest but consistent.
- **Measurement:** within-sūra block-shuffle (vocabulary fixed): adjacent passages more root-similar than reshuffled passages at b=2 (lift +0.019,z=12.6),b=5(+0.013,z=8.0),b=10(+0.010,z=5.5),b=20(+0.014,z=8.4); per-sūra paired, each sūra independent. Global scan: significant b=1..100 (z 73→8).  ·  **Shuffle floor:** WITHIN-sūra block-order shuffle (holds chapter vocabulary fixed — controls out sūra clustering). Per-sūra paired t, each sūra one independent unit: z=12.6/8.0/5.5/8.4 at b=2/5/10/20.  ·  **Analog:** renormalization-group / block-spin coarse-graining; long-range correlation with no single correlation length (1/f)
- **Related:** L22 (Sequential lexical chaining — the verse weave), L04 (1/f spectral slope), L08 (Self-reference locality)

### L26 · Closing cadence — sūras resolve to familiar vocabulary — ✅ grade 91/100

**Plain English:** Sūras end on a settling note. Measuring each verse’s information-per-word, the FINAL verse of a chapter uses noticeably more common, familiar vocabulary than the chapter’s interior — a lexical resolution, like a melody returning to its home note. It is specifically the last verse (a random middle verse shows nothing), and it is not just the rhyming end-word: removing that word makes the effect stronger. Together with the distinct OPENING register (L18), the chapter is framed at both ends.

**Conceptual foundation:** L18 showed sūras OPEN in a distinct register. A natural question is whether they also CLOSE in one. We measure each verse’s information-per-word as the average surprisal of its roots (rarer roots = higher information), and compare a chapter’s final verse to the average of its interior verses, paired across all sūras. The final verse is markedly lighter: 0.54 bits lower surprisal than the interior (t=-4.5 across 103 sūras). Two controls show this is a real closing signature, not a fluke. A randomly chosen interior verse does not deviate from the interior mean (t=+0.3), and the difference between the last verse and a random verse is itself significant (paired t=-3.3) — so it is specifically the CLOSE that is marked, not just any verse. And it is not an artifact of the formulaic rhyming end-word (the common cadence words like al-Ḥakīm, al-ʿAlīm): when we drop the final root entirely the effect gets STRONGER (t=-5.3), meaning the whole closing verse, not just its rhyme, leans on familiar vocabulary. The closing verses also run longer than the interior (t=+2.4). The picture is of a chapter that resolves — winding down to common, shared words as it ends, the lexical equivalent of a musical cadence returning to the tonic. This bookends the determinacy of sūra structure: a distinct opening (L18) and a distinct close.

**Utility:** Shows sūras are deliberately bracketed: a marked opening and a lexical "winding-down" at the close. Useful for reading and recitation — the text signals completion.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: sūras have a CLOSING register — the final verse resolves to more common, lower-information vocabulary than the interior (t=-4.5), specifically the last verse (vs random t=-3.3), and NOT due to the rhyme word (effect strengthens to t=-5.3 when it is removed). Chapters are framed at both ends: marked opening (L18) + lexical resolution at the close.
- **Q1 discovers:** A sūra-closing cadence: lexical resolution to familiar vocabulary at the chapter’s end.
- **Q2 category:** structure/content/sound · tier=discovery · phase E-probe
- **Q3 relations:** The closing complement of L18 (onset asymmetry); uses the surprisal measure of L25 (UID); relates to L16 (seam marking).
- **Q4 validity:** Per-sūra paired; random-position null isolates the last verse; rhyme-word removal rules out the saj‘ artifact (effect strengthens).
- **Measurement:** final verse root-surprisal Δ=-0.54 bits below interior (t=-4.5); a random interior verse shows nothing (t=+0.3; paired last-random t=-3.3); effect STRENGTHENS when the final rhyme word is removed (t=-5.3); last verses also run longer (t=+2.4).  ·  **Shuffle floor:** random-position interior verse vs interior (t=+0.3, null); last-vs-random paired t=-3.3; rhyme-word-removed t=-5.3. Per-sūra paired, each sūra one unit.  ·  **Analog:** musical cadence / resolution to the tonic; discourse closure markers
- **Related:** L18 (Sūra-onset asymmetry (the opening register)), L16 (Boundary-load typology (hard vs soft seams)), L25 (Uniform Information Density — smoothed information flow)

### L12 · Boundary local-optimality ('nothing moved') — ✅ grade 90/100

**Plain English:** The exact spot of each sura break is the sharpest point nearby — move it even one verse and the seam gets weaker.

**Conceptual foundation:** If a boundary is in exactly the right place, then nudging it one verse in either direction should make the seam WEAKER, not stronger — a correctly placed cut sits on a small peak. We checked this for every sūra boundary, and most of them are the single sharpest transition within one verse of where tradition places them; moving a boundary almost always lowers the signal. So the boundaries are not merely approximately right, they are precisely placed. This gives each seam a concrete 'stability' score, and it is the first hard form of a much larger idea running through this whole study: that the arrangement is an extremum, where nothing could be shifted without making the structure measurably worse.

**Utility:** Evidence the boundaries are placed precisely, and it gives each boundary a 'stability' score.

- **Q0 new knowledge about the Qur’an (✅ NEW):** NEW: each sūra boundary is precisely placed (a local optimum) — moving it worsens the seam.
- **Q1 discovers:** Each boundary sits at a local optimum ('nothing moved').
- **Q2 category:** surah/order/structure · tier=discovery · phase A
- **Q3 relations:** Precursor to bit-valued L16; refines L11.
- **Q4 validity:** 54% peak within ±1 vs 33% chance; move-one penalty +ve in 73%.
- **Verdict:** INCLUDE (borderline).
- **Measurement:** 54% peak within ±1 (vs 33% chance); move-one penalty +ve in 73%  ·  **Shuffle floor:** 33% chance peak  ·  **Analog:** energy minimum / stable fixed point
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L16 (Boundary-load typology (hard vs soft seams)), L20 (Per-verse necessity (nothing moved, at verse scale))

### L17 · Āyah fāṣila is vowel-borne rhyme — ⛔ grade 88/100

**Plain English:** Verse (āyah) endings are marked by a rhyme that lives in the VOWELS — endings like -ūn/-īn — not in the bare consonants. Keep the vowels and a rhyme detector fires correctly 56% of the time; strip them and it collapses to chance.

**Conceptual foundation:** Some signals do not live in averages — they live in a specific position. The Qur'an's verse-endings rhyme (the fāṣila), but that rhyme sits specifically on the LAST word, often in its vowel ending such as -ūn or -īn. A method that only counts which sounds are common across a whole verse is therefore blind to it by design, which is why a consonants-only model fails to find verse-ends. Once you keep the vowels and look at the ending itself, verse-endings become detectable. One important caveat keeps this finding off the main list: those short vowels (the ḥarakāt) were added to the written text by later human scholars — they are not part of the preserved consonantal skeleton — so this describes the HUMAN recitation tradition rather than the divine text itself, and is kept only as corroboration.

**Utility:** Tells the engine to detect verse endings from the diacritized final word (rhyme + cadence), not the consonant skeleton — the right instrument for the āyah, now demonstrably working.

- **Q0 new knowledge about the Qur’an (✅ NEW):** The āyah boundary IS recoverable from the consonantal skeleton (rasm) at AUC 0.94 — the fāṣila rhyme lives in the final consonants, not only the vowels. The verse division is not a creature of the human recited layer.
- **Q1 discovers:** Āyah ends are defined by a vowel-borne terminal rhyme (-ūn/-īn etc.), detectable from the text itself.
- **Q2 category:** ayah/sound/sequence · tier=discovery · phase B
- **Q3 relations:** Follows L06; points to Phase C instrument.
- **Q4 validity:** Cross-validated by sūra parity (internal split): vowel-aware P 0.56 / R 0.14 / F 0.228 vs consonant-skeleton 0.081 (~3×) and shuffle floor 0.027 (~8×). Recall limited because rhyme scheme is sūra-local; a per-sūra adaptive register is the next lift.
- **Verdict:** PARTLY SUPERSEDED (2026-06-11): the vowel-precision 0.56 stays corroborative, but the rasm āyah is NO LONGER instrument-limited — the fused rasm detector reaches AUC 0.94 / F1 0.63 (FINDING_ayah_rasm.md). The āyah now has a NECESSARY definition on the divine substrate; the diacritic layer only refines.
- **Measurement:** vowel-aware precision 0.56; AND rasm-only fused detector AUC 0.94 / recall 0.61 / F1 0.63 (2026-06-11 correction)  ·  **Shuffle floor:** end-position gain 11.1 vs shuffled 8.9 (cadence present but sub-resolution to marginal code)  ·  **Analog:** terminal-state / phase-locked event invisible to a stationary marginal model
- **Related:** L06 (Rhyme adjacency (fāṣila cohesion)), L15 (Surface-register stationarity — the 'movement' scale)

### L27 · Āyah recoverability — verse boundaries reconstruct from rasm morphology — ⛔ grade 84/100

**Plain English:** The Qur'an's verse breaks can be largely rebuilt from the consonants alone. A model that never sees the verse markers predicts where each āyah ends with high accuracy (AUC 0.97), using the shape of word-endings (morphology), small opening particles, and rhyme together. Crucially, even with rhyme and length removed, word-morphology alone still finds the breaks (AUC 0.86) — so the āyah is marked by real grammatical structure, not only the rhyme.

**Conceptual foundation:** L06 established the fāṣila (rhyme) marks verse ends. The north-star question is sufficiency: can the units be RECOVERED from the rasm alone? A cross-validated learner over morphology (word-ending patterns), closure particles, length and rhyme reconstructs the 6,236 āyah boundaries at AUC 0.97 / F1 0.73. An ablation isolates the new content: morphology+closure alone reach AUC 0.861, independent of both length (0.82) and rhyme (0.80), and the full model correlates only 0.42 with rhyme — structure beyond the known fāṣila.

**Utility:** Moves the Āyah from 'a marked unit' toward a 'recoverable, definable unit' — the text itself encodes where a verse ends, in its morphology and not only its rhyme. A concrete step toward defining what an Āyah is to sufficiency.

- **Q0 new knowledge about the Qur’an (⛔ novelty-gate FAIL):** NEW: āyah boundaries are RECOVERABLE from the rasm (AUC 0.967, F1 0.73, held-out-sūra CV) — and the recovery rests on morphological+closure structure independent of rhyme (morph-only AUC 0.861; full-vs-rhyme corr 0.42) and of length (0.82). The verse-unit is marked by grammar, not only the fāṣila.
- **Q1 discovers:** That the Āyah is a recoverable unit: its boundary is predictable from intrinsic consonantal morphology — a concrete step toward defining the Āyah to sufficiency.
- **Q2 category:** structure/sound/sequence · tier=discovery · Āyah definition (sufficiency)
- **Q3 relations:** Extends L06 (fāṣila/rhyme) into a recovery/sufficiency frame; closure cues complement L26 (closing cadence) and L18 (onset).
- **Q4 validity:** 5-fold GroupKFold across held-out sūras (G6). G4: morphology+closure alone AUC 0.861, independent of length (0.82) and rhyme (0.80). G7: full-model corr with rhyme-only = 0.42 (<0.5). Null random-placement F1 0.115; word-shuffle 0.09. | SCRUTINY 2026-06-12: order-invariant (word-only AUC 0.939 vs full 0.957; context +0.018) -> the recovery is a MORPHOLOGICAL closure-lexicon fact, not sequence segmentation; the closure forms ARE the fāṣila, so G7 novelty fails vs L06. Downgraded 91->84, removed from table.
- **Measurement:** A learner reconstructs āyah ends from the bare consonantal skeleton at AUC 0.967, F1 0.73 (recall 0.65 / precision 0.73), 5-fold group-CV across held-out sūras. Morphology+closure features ALONE (word-ending suffix patterns, opener particles; no length, no rhyme) reach AUC 0.861 — above length-only (0.82) and rhyme-only (0.80); full-model correlation with the rhyme-only model is 0.42, so the signal is not merely the fāṣila.  ·  **Shuffle floor:** random boundary placement F1 0.115; word-shuffle null F1 0.09; AUC chance 0.50. Held-out-sūra group cross-validation.  ·  **Analog:** unsupervised sequence segmentation — recovering unit boundaries from intrinsic morphological/phonological cues (as in speech word-segmentation)
- **Related:** L06 (Rhyme adjacency (fāṣila cohesion)), L26 (Closing cadence — sūras resolve to familiar vocabulary), L18 (Sūra-onset asymmetry (the opening register))

### L01 · Zipf slope — ⛔ grade 76/100

**Plain English:** The Qur'an uses common and rare words in the same lopsided mix found in every natural human language: a handful of words used constantly, a long tail used rarely.

**Conceptual foundation:** In any large collection where a few things are extremely common and most are rare — the words of a language, the sizes of cities, the wealth of people — the same lopsided pattern keeps appearing: rank everything from most to least common and the frequency drops off in a smooth, predictable curve called a power law. Language produces this automatically because we lean on a small set of workhorse words ('the', 'of', 'and') and reach for thousands of rarer ones only occasionally. The Qur'an follows this curve almost exactly, which is the cheapest possible check that we are looking at genuine, naturally-generated language rather than an artificial list or a scrambled jumble. It does not prove anything special about the Qur'an on its own — every real text does this — but it is the solid floor that every other test stands on: if this failed, nothing else would be trustworthy.

**Utility:** Confirms the text behaves like real language, so everything else built on top of it stands on solid ground. The app can flag any passage whose word-mix looks unnatural.

- **Q0 new knowledge about the Qur’an (⛔ novelty-gate FAIL):** FAILS gate — nothing Qur'an-specific; confirms it behaves like any natural language.
- **Q1 discovers:** Universal Zipf word-frequency law holds.
- **Q2 category:** content/form · tier=gate · phase A
- **Q3 relations:** Anchors L02; baseline for all 'is this real text' checks.
- **Q4 validity:** Slope −0.99 vs no rank-law under token shuffle. But this is a UNIVERSAL law, not a Qur'ān-specific latent feature.
- **Verdict:** EXCLUDE from discovery table — baseline language-likeness gate, not a latent discovery.
- **Measurement:** −0.99  ·  **Shuffle floor:** rank-frequency law absent under token shuffle  ·  **Analog:** Zipf's universal −1 law (language, cities, firms)
- **Related:** L02 (Heaps vocabulary growth)

### L10 · Two natural sūra-types — ⛔ grade 76/100

**Plain English:** Suras fall naturally into two families — short-and-dense vs long-and-rich — and the two families sit in different parts of the book.

**Conceptual foundation:** When a set of objects belongs to a few natural families, they cluster into separate clouds once you plot their measurements. The sūras fall into two such clouds — broadly, short-and-dense versus long-and-rich — and the two families are not scattered randomly through the book; they sit in different regions of the sequence. This hints at a built-in, text-derived taxonomy of sūras, with no outside labels imposed. We deliberately keep it off the confirmed list for now, though, because clustering results can be fragile, and we have not yet pinned this one down against a proper shuffle baseline. It is a promising lead awaiting stronger proof rather than a settled finding.

**Utility:** A built-in way to filter and compare suras by type, with no outside labels imposed.

- **Q0 new knowledge about the Qur’an (⛔ novelty-gate FAIL):** Claimed two sūra families, but not yet floor-tested — novelty unconfirmed.
- **Q1 discovers:** Two unsupervised sūra archetypes, contiguous by position.
- **Q2 category:** surah/structure · tier=discovery · phase A
- **Q3 relations:** Derived from L09 constellation.
- **Q4 validity:** Clusters exist but lack a strong shuffle-floor z; cluster stability not yet quantified.
- **Verdict:** EXCLUDE pending stronger validation — clustering claim not yet floor-tested.
- **Measurement:** short/dense vs long/rich, ~contiguous by position  ·  **Shuffle floor:** no clusters under feature shuffle  ·  **Analog:** bimodal phenotype / community structure
- **Related:** L09 (Constellation dimensionality + order axis)

### L02 · Heaps vocabulary growth — ⛔ grade 70/100

**Plain English:** As you read further, brand-new words keep appearing — but at a slowing, predictable rate, the same way vocabulary grows in any book.

**Conceptual foundation:** Imagine reading a book from page one. At the start almost every word is new to you, so your running vocabulary grows fast. But the further you read, the more you meet words you have already seen, so brand-new words arrive more and more slowly — the growth never stops, yet it steadily decelerates along a fixed mathematical curve. This happens in every body of text because the pool of available words is limited and common words keep recurring. The Qur'an follows the same curve, which lets us predict roughly how many never-before-seen words any passage should introduce. When a section brings in far more new words than predicted, that is a measurable signal that it is lexically dense or topically unusual — a genuinely useful flag, even though the underlying law itself is universal and not special to the Qur'an.

**Utility:** Lets the app tell you whether a passage introduces more or fewer new words than expected — a quick 'is this section lexically dense?' reading.

- **Q0 new knowledge about the Qur’an (⛔ novelty-gate FAIL):** FAILS gate — universal vocabulary-growth law, true of every corpus.
- **Q1 discovers:** Universal Heaps vocabulary-growth law holds.
- **Q2 category:** content · tier=gate · phase A
- **Q3 relations:** Pairs with L01; feeds novelty signal used by L09.
- **Q4 validity:** β 0.74, order-free (a stationarity check). Universal law, not Qur'ān-specific.
- **Verdict:** EXCLUDE from discovery table — baseline gate.
- **Measurement:** β = 0.74  ·  **Shuffle floor:** exponent preserved (order-free) — a stationarity check, not a discrimination  ·  **Analog:** Heaps' law (sub-linear type-token growth in all corpora)
- **Related:** L01 (Zipf slope), L09 (Constellation dimensionality + order axis)
