# Latent Feature Ledger — Intrinsic Qur'ān Study

> **The one law.** Nothing external is admissible as evidence. Every feature is measured from the text against its own shuffle. A feature is admitted only with ≥3 converging modalities + the text's own shuffle floor + a named universe analog.

*Cadence **weekly**. Updated 2026-06-09; next due 2026-06-16. Generated from `latent_features.json`.*

**13 features pass (grade ≥ 90); 4 excluded.** Mandatory novelty gate: *what do we know about the Qur'an we didn't before?* Organized by category, sorted by grade.

**Open gap:** Thinnest axis: SEMANTIC/content modelling — only cross-channel proxies so far (L07,L15,L16). A direct semantic channel is the Phase C target that L15 and L17 point to. Until then, sūra sufficiency stays instrument-limited (عدم الوجدان).

## Rhythm / wave

| ID | Feature | Grade | In plain English | Why it matters |
|--|--|--|--|--|
| L03 | Verse-length long-range correlation (DFA Hurst) | 95 | Verse lengths aren't random. Short and long verses come in waves, and how long a verse is depends on verses far away, not just its neighbours. | Strong proof that the ORDER of verses carries meaning. It is the backbone of the app being able to spot a verse that sits out of place. |
| L04 | 1/f spectral slope | 93 | The rhythm of verse lengths has structure at many timescales at once — like a heartbeat or natural music, not one repeating drumbeat. | An independent, second confirmation that the text is layered and alive, not flat or mechanically uniform. |
| L05 | Self-similar size tails (power law) | 92 | There is no single 'typical' size: words, verses, and suras each range from tiny to huge in the same self-similar way seen in nature (earthquakes, avalanches). | Lets the app compare structure fairly across scales and notice exactly where a section stops following the natural pattern. |

## Rhyme / sound

| ID | Feature | Grade | In plain English | Why it matters |
|--|--|--|--|--|
| L06 | Rhyme adjacency (fāṣila cohesion) | 94 | Neighbouring verses tend to end on the same sound far more often than chance — rhyme runs in stretches. | This is what the app uses to mark rhyme paragraphs and verse endings, so you can see the sound architecture of a passage. |
| L07 | Rhyme↔theme coupling | 92 | Verses that rhyme together also tend to be about the same thing — sound and meaning move together, they aren't separate layers. | You can use rhyme as a quick clue to grouped meaning; it supports the app's topic groupings. |

## Self-reference / network

| ID | Feature | Grade | In plain English | Why it matters |
|--|--|--|--|--|
| L08 | Self-reference locality | 91 | When a word comes back, it usually returns nearby (within ~16 words) and then fades. The text 'echoes itself' at a paragraph scale. | Sets the natural size of a 'passage' for search and context, so the app shows you the right amount of surrounding text. |

## Constellation / matrix

| ID | Feature | Grade | In plain English | Why it matters |
|--|--|--|--|--|
| L09 | Constellation dimensionality + order axis | 93 | Describe each sura by 100 measurements, and the single biggest difference between suras lines up almost perfectly with their order in the book. | The app can predict where a sura belongs in the canonical order from its statistics alone — and flag anything that doesn't fit. |

## Sūra definition

| ID | Feature | Grade | In plain English | Why it matters |
|--|--|--|--|--|
| L11 | Sūra boundary = multimodal discontinuity (NECESSARY) | 98 | Where one sura ends and the next begins, the sound, the rhythm, and the word-links all jump at the same moment — a real seam you can detect blind. | The app can find sura boundaries automatically and show how sharp each one is. |
| L16 | Boundary-load typology (hard vs soft seams) | 94 | About a third of sura breaks are marked by a clear change in sound and rhythm; the other two-thirds are marked only by a change in topic. | The app can label each of the 113 sura junctions as 'sound-marked' or 'meaning-marked' — a brand-new annotation you can browse. |
| L15 | Surface-register stationarity — the 'movement' scale | 93 | Let the text divide ITSELF purely by sound and rhythm and it makes about 63 big 'movements', not the 114 suras — because the surface style is remarkably even throughout. So a sura is defined by its THEME, not by a change in sound. | Tells you what a sura really is (a unit of meaning), gives you a new coarse 'movements' map of the book, and shows exactly where meaning-based analysis is still needed. |
| L12 | Boundary local-optimality ('nothing moved') | 90 | The exact spot of each sura break is the sharpest point nearby — move it even one verse and the seam gets weaker. | Evidence the boundaries are placed precisely, and it gives each boundary a 'stability' score. |

## Order / sequence

| ID | Feature | Grade | In plain English | Why it matters |
|--|--|--|--|--|
| L14 | MDL order-load of the verse stream | 95 | The specific order of the verses carries about 9,000 bits of real, measurable structure compared with the same verses shuffled. | A hard number certifying the order is non-arbitrary (not random) — while honestly showing it is NOT mere sorting. Basis for a displaced-verse detector; do NOT read it as 'maximally optimal'. |

## Optimality / perturbation

| ID | Feature | Grade | In plain English | Why it matters |
|--|--|--|--|--|
| L13 | Perturbation-optimality battery | 94 | Scramble, delete, add, or swap the text and the measured patterns break — and each kind of damage breaks a specific pattern. | A stress-test proving the patterns are real and load-bearing, not lucky coincidences. |

## Supplement — did not pass (< 90)

| ID | Feature | Grade | Why excluded |
|--|--|--|--|
| L01 | Zipf slope | 76 | EXCLUDE from discovery table — baseline language-likeness gate, not a latent discovery. |
| L10 | Two natural sūra-types | 76 | EXCLUDE pending stronger validation — clustering claim not yet floor-tested. |
| L17 | Āyah is positionally (not marginally) coded | 75 | EXCLUDE — positional signal real but weak (5% recall); needs the rhyme vowels (Phase C2). |
| L02 | Heaps vocabulary growth | 70 | EXCLUDE from discovery table — baseline gate. |

## Candidates — not yet in the table

### C1 · Intermediate-complexity band ('edge of order')

- **Status:** candidate — needs multimodal validation before entering the table
- **Evidence:** Canonical MDL cost 30,679 b sits BETWEEN random 40,632 b (gap-to-random = +9,952 b, the L14 order-load) and sorted-homogeneous 18,938–23,470 b (gap-to-sorted = 7,209–11,741 b, the text's resistance to trivial sorting). Two distinct measurable quantities, not one.
- **What would be new about the Qur'an:** Sorting the verses compresses BETTER than canonical — but that is meaningless ordering, so it does NOT mean a rearrangement is 'better'. Instead the sorting test DISCOVERS new features: (1) gap-to-random = how non-arbitrary the order is; (2) gap-to-sorted = how much the order sacrifices compressibility to preserve meaning. The Qur'an occupies the intermediate band of meaningful sequences.
- **Universe analog:** edge-of-chaos / logical depth / Kolmogorov-structure-function intermediate regime
- **To promote:** need ≥3 modalities showing the same intermediate position + a shuffle AND a sort floor in each.

---

## Full critical review per feature (by category)

### ▸ Lexical baselines

#### L01 · Zipf slope — ⛔ grade 76/100

**Plain:** The Qur'an uses common and rare words in the same lopsided mix found in every natural human language: a handful of words used constantly, a long tail used rarely.

**Conceptual foundation:** Any system where a few things are very common and many are rare, all by one proportional rule, produces a power law — language does this naturally with words. So the −1 slope is a cheap, universal 'does this behave like real language?' test, and anything that breaks it is stylistically odd.

**Utility:** Confirms the text behaves like real language, so everything else built on top of it stands on solid ground. The app can flag any passage whose word-mix looks unnatural.

- **Q0 new knowledge (⛔ novelty FAIL):** FAILS gate — nothing Qur'an-specific; confirms it behaves like any natural language.
- **Q1 discovers:** Universal Zipf word-frequency law holds.
- **Q2 category:** Lexical baselines — content/form · tier=gate · phase A
- **Q3 relations:** Anchors L02; baseline for all 'is this real text' checks.
- **Q4 validity:** Slope −0.99 vs no rank-law under token shuffle. But this is a UNIVERSAL law, not a Qur'ān-specific latent feature.
- **Verdict:** EXCLUDE from discovery table — baseline language-likeness gate, not a latent discovery.
- **Related:** L02 (Heaps vocabulary growth)

#### L02 · Heaps vocabulary growth — ⛔ grade 70/100

**Plain:** As you read further, brand-new words keep appearing — but at a slowing, predictable rate, the same way vocabulary grows in any book.

**Conceptual foundation:** Vocabulary is limited, so the further you read the more you reuse words and the fewer brand-new ones you meet — that slowdown follows a fixed power. Knowing the expected rate lets us see when a passage brings unusually many or few new words.

**Utility:** Lets the app tell you whether a passage introduces more or fewer new words than expected — a quick 'is this section lexically dense?' reading.

- **Q0 new knowledge (⛔ novelty FAIL):** FAILS gate — universal vocabulary-growth law, true of every corpus.
- **Q1 discovers:** Universal Heaps vocabulary-growth law holds.
- **Q2 category:** Lexical baselines — content · tier=gate · phase A
- **Q3 relations:** Pairs with L01; feeds novelty signal used by L09.
- **Q4 validity:** β 0.74, order-free (a stationarity check). Universal law, not Qur'ān-specific.
- **Verdict:** EXCLUDE from discovery table — baseline gate.
- **Related:** L01 (Zipf slope), L09 (Constellation dimensionality + order axis)

### ▸ Rhythm / wave

#### L03 · Verse-length long-range correlation (DFA Hurst) — ✅ grade 95/100

**Plain:** Verse lengths aren't random. Short and long verses come in waves, and how long a verse is depends on verses far away, not just its neighbours.

**Conceptual foundation:** Some sequences have memory: what comes now leans on what came long before (persistence), unlike independent coin flips. Verse lengths show that memory, which means the sequence is a real signal — so we can treat the order as information and notice when it is disturbed.

**Utility:** Strong proof that the ORDER of verses carries meaning. It is the backbone of the app being able to spot a verse that sits out of place.

- **Q0 new knowledge (✅ NEW):** NEW: the Qur'an's verse-length sequence has long-range memory — its order is a real signal, not incidental.
- **Q1 discovers:** Verse-length sequence has long-range memory (order is structured).
- **Q2 category:** Rhythm / wave — sequence/order/form · tier=discovery · phase A
- **Q3 relations:** Confirmed in frequency domain by L04; is the substrate L14 measures in bits; feeds L15.
- **Q4 validity:** DFA H 0.95 vs 0.51 own shuffle; independently reproduced by L04 (1/f). Two wave-channels converge.
- **Verdict:** INCLUDE.
- **Related:** L04 (1/f spectral slope), L14 (MDL order-load of the verse stream), L15 (Surface-register stationarity — the 'movement' scale)

#### L04 · 1/f spectral slope — ✅ grade 93/100

**Plain:** The rhythm of verse lengths has structure at many timescales at once — like a heartbeat or natural music, not one repeating drumbeat.

**Conceptual foundation:** When a system is organised at all timescales at once (not one repeating beat), its energy spreads out as 1-over-frequency — the known signature of complex, self-organised systems. Finding it in the verse rhythm shows the text is layered rather than mechanical.

**Utility:** An independent, second confirmation that the text is layered and alive, not flat or mechanically uniform.

- **Q0 new knowledge (✅ NEW):** NEW: the Qur'an's rhythm is multi-scale (1/f), a complex-system fingerprint, not a single meter.
- **Q1 discovers:** Verse-length rhythm is multi-scale (1/f), no single dominant period.
- **Q2 category:** Rhythm / wave — sequence/form · tier=discovery · phase A
- **Q3 relations:** Frequency-domain confirmation of L03; pairs with L05 on scale-freeness.
- **Q4 validity:** Spectral slope 0.76 vs 0.00 (white) under shuffle; agrees with L03 in a second representation.
- **Verdict:** INCLUDE.
- **Related:** L03 (Verse-length long-range correlation (DFA Hurst)), L05 (Self-similar size tails (power law))

#### L05 · Self-similar size tails (power law) — ✅ grade 92/100

**Plain:** There is no single 'typical' size: words, verses, and suras each range from tiny to huge in the same self-similar way seen in nature (earthquakes, avalanches).

**Conceptual foundation:** 'Scale-free' means the statistics look the same whether you zoom in or out — there is no single typical size — which is what nature produces when things grow by multiplication. It gives one compact fingerprint per level to compare structure across scales.

**Utility:** Lets the app compare structure fairly across scales and notice exactly where a section stops following the natural pattern.

- **Q0 new knowledge (✅ NEW):** NEW: the Qur'an has no characteristic unit size — it is scale-free across word→verse→sūra.
- **Q1 discovers:** No characteristic unit size — scale-free at word/verse/sūra.
- **Q2 category:** Rhythm / wave — scale/form · tier=discovery · phase A
- **Q3 relations:** Shares scale-free family with L04; feeds the scale axis of L15.
- **Q4 validity:** Power-law tails at 3 nested scales (α 2.04/1.71/1.44) vs Gaussianised tails under shuffle.
- **Verdict:** INCLUDE.
- **Related:** L04 (1/f spectral slope), L15 (Surface-register stationarity — the 'movement' scale)

### ▸ Rhyme / sound

#### L06 · Rhyme adjacency (fāṣila cohesion) — ✅ grade 94/100

**Plain:** Neighbouring verses tend to end on the same sound far more often than chance — rhyme runs in stretches.

**Conceptual foundation:** Rhyme is a constraint on sound: if it is really present, neighbouring endings will agree far more than chance allows. Measuring that agreement turns 'rhyme' into a hard, usable signal for where verses and paragraphs begin and end.

**Utility:** This is what the app uses to mark rhyme paragraphs and verse endings, so you can see the sound architecture of a passage.

- **Q0 new knowledge (✅ NEW):** NEW: the Qur'an's rhyme forms measurable domains far above chance (0.72 vs 0.30).
- **Q1 discovers:** Rhyme runs in coherent stretches (fāṣila domains).
- **Q2 category:** Rhyme / sound — sound/ayah/form · tier=discovery · phase A
- **Q3 relations:** Backbone of L11 and L17; couples to meaning in L07.
- **Q4 validity:** Adjacent same-final-letter 0.72 vs 0.30 shuffle (z huge); cross-checked by lexical+length cohesion.
- **Verdict:** INCLUDE.
- **Related:** L07 (Rhyme↔theme coupling), L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L17 (Āyah is positionally (not marginally) coded)

#### L07 · Rhyme↔theme coupling — ✅ grade 92/100

**Plain:** Verses that rhyme together also tend to be about the same thing — sound and meaning move together, they aren't separate layers.

**Conceptual foundation:** If form and meaning are shaped together they should move together; if they are separate layers they should be independent. Testing whether rhyming verses also share themes decides this — and lets sound act as a quick hint of meaning.

**Utility:** You can use rhyme as a quick clue to grouped meaning; it supports the app's topic groupings.

- **Q0 new knowledge (✅ NEW):** NEW: in the Qur'an, rhyme and theme are coupled (1.78×) — sound predicts meaning.
- **Q1 discovers:** Sound and meaning are coupled, not independent layers.
- **Q2 category:** Rhyme / sound — sound/semantic · tier=discovery · phase A
- **Q3 relations:** Links L06 (sound) to network/theme; prototype of cross-modal convergence.
- **Q4 validity:** Shared-rhyme verses 1.78× more thematically bound, z≈5.2 vs independence.
- **Verdict:** INCLUDE.
- **Related:** L06 (Rhyme adjacency (fāṣila cohesion)), L08 (Self-reference locality)

### ▸ Self-reference / network

#### L08 · Self-reference locality — ✅ grade 91/100

**Plain:** When a word comes back, it usually returns nearby (within ~16 words) and then fades. The text 'echoes itself' at a paragraph scale.

**Conceptual foundation:** The idea that 'the text explains itself' should leave a measurable footprint — words echoing other words nearby. Measuring how far that echo reaches tells us the range over which the text is self-coherent, which sets the natural size of a 'passage'.

**Utility:** Sets the natural size of a 'passage' for search and context, so the app shows you the right amount of surrounding text.

- **Q0 new knowledge (✅ NEW):** NEW: the Qur'an's self-reference has a finite range (~16–256 words) — a measured 'passage' size.
- **Q1 discovers:** Self-reference has a finite range (~passage scale).
- **Q2 category:** Self-reference / network — sequence/content · tier=discovery · phase A
- **Q3 relations:** Sets window for content channels; relates to L07 network modality.
- **Q4 validity:** Word recurrence 6.2× over shuffle within 16 tokens, decays to floor by 256.
- **Verdict:** INCLUDE.
- **Related:** L07 (Rhyme↔theme coupling), L16 (Boundary-load typology (hard vs soft seams))

### ▸ Constellation / matrix

#### L09 · Constellation dimensionality + order axis — ✅ grade 93/100

**Plain:** Describe each sura by 100 measurements, and the single biggest difference between suras lines up almost perfectly with their order in the book.

**Conceptual foundation:** Describe each sūra as a point in a 100-number space; the single direction along which sūras differ most is the text's biggest organising axis. That this axis lines up with the canonical order means the order itself is informative, so we can predict a sūra's position and flag misfits.

**Utility:** The app can predict where a sura belongs in the canonical order from its statistics alone — and flag anything that doesn't fit.

- **Q0 new knowledge (✅ NEW):** NEW: the Qur'an's canonical ORDER aligns with its own dominant statistical axis (r=−0.89).
- **Q1 discovers:** The canonical ORDER aligns with the text's dominant statistical gradient.
- **Q2 category:** Constellation / matrix — order/surah/scale · tier=discovery · phase A
- **Q3 relations:** Matrix-modality twin of L14; basis of L10 typing and L15 grouping.
- **Q4 validity:** PC1 vs canonical order r=−0.89; PC1 random under feature-shuffle. 100-feature constellation.
- **Verdict:** INCLUDE.
- **Related:** L10 (Two natural sūra-types), L14 (MDL order-load of the verse stream), L15 (Surface-register stationarity — the 'movement' scale)

#### L10 · Two natural sūra-types — ⛔ grade 76/100

**Plain:** Suras fall naturally into two families — short-and-dense vs long-and-rich — and the two families sit in different parts of the book.

**Conceptual foundation:** If items belong to natural families, they cluster together in feature space. Two clusters appear here — but clustering can be fragile, and this one has not yet been tested against a shuffle floor, so it does not yet earn a place.

**Utility:** A built-in way to filter and compare suras by type, with no outside labels imposed.

- **Q0 new knowledge (⛔ novelty FAIL):** Claimed two sūra families, but not yet floor-tested — novelty unconfirmed.
- **Q1 discovers:** Two unsupervised sūra archetypes, contiguous by position.
- **Q2 category:** Constellation / matrix — surah/structure · tier=discovery · phase A
- **Q3 relations:** Derived from L09 constellation.
- **Q4 validity:** Clusters exist but lack a strong shuffle-floor z; cluster stability not yet quantified.
- **Verdict:** EXCLUDE pending stronger validation — clustering claim not yet floor-tested.
- **Related:** L09 (Constellation dimensionality + order axis)

### ▸ Sūra definition

#### L11 · Sūra boundary = multimodal discontinuity (NECESSARY) — ✅ grade 98/100

**Plain:** Where one sura ends and the next begins, the sound, the rhythm, and the word-links all jump at the same moment — a real seam you can detect blind.

**Conceptual foundation:** A genuine seam should appear as a jump in several independent measurements at once; a coincidence in one channel is cheap, but agreement across sound, rhythm and word-links together is not. That convergence is what lets us detect sūra boundaries blind.

**Utility:** The app can find sura boundaries automatically and show how sharp each one is.

- **Q0 new knowledge (✅ NEW):** NEW: the canonical division into sūras is objectively recoverable from the text (AUC 0.82) — boundaries are real, not merely traditional.
- **Q1 discovers:** A sūra boundary is a simultaneous multimodal discontinuity (NECESSARY).
- **Q2 category:** Sūra definition — surah/structure/sound · tier=discovery · phase A
- **Q3 relations:** Necessary half that L15/L16 test for sufficiency; uses L06.
- **Q4 validity:** AUC 0.82, d 1.20 vs 0.5; size-invariant (1.93≈2.15); symbol+wave+network converge.
- **Verdict:** INCLUDE.
- **Related:** L12 (Boundary local-optimality ('nothing moved')), L15 (Surface-register stationarity — the 'movement' scale), L16 (Boundary-load typology (hard vs soft seams))

#### L16 · Boundary-load typology (hard vs soft seams) — ✅ grade 94/100

**Plain:** About a third of sura breaks are marked by a clear change in sound and rhythm; the other two-thirds are marked only by a change in topic.

**Conceptual foundation:** Some seams are marked by a change in sound, others only by a change in topic; a sound-based compressor will 'feel' the first kind and miss the second. Measuring which seams it feels separates sound-marked from meaning-marked junctions — though confirming this fully needs a meaning channel too.

**Utility:** The app can label each of the 113 sura junctions as 'sound-marked' or 'meaning-marked' — a brand-new annotation you can browse.

- **Q0 new knowledge (✅ NEW):** NEW: a measurable core of sūra seams are 'hard' — marked across sound, cadence AND vocabulary together (z=9.4) — distinct from the ~35% marked by surface alone.
- **Q1 discovers:** Boundary-load typology — ~35% of sūra seams sound-marked, ~65% meaning-marked.
- **Q2 category:** Sūra definition — surah/sound/semantic · tier=discovery · phase B
- **Q3 relations:** Operationalises L12 in bits; partitions L11 boundaries.
- **Q4 validity:** 3 modalities: canonical seams load-bearing 0.053 vs null 0.003 (z=9.4, symbol+wave+lexical); surface-only share ~0.345 (z=7.4). Typology of hard vs surface-marked seams.
- **Verdict:** INCLUDE — third (semantic) modality clears the bar (z=9.4).
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L12 (Boundary local-optimality ('nothing moved')), L15 (Surface-register stationarity — the 'movement' scale), L07 (Rhyme↔theme coupling)

#### L15 · Surface-register stationarity — the 'movement' scale — ✅ grade 93/100

**Plain:** Let the text divide ITSELF purely by sound and rhythm and it makes about 63 big 'movements', not the 114 suras — because the surface style is remarkably even throughout. So a sura is defined by its THEME, not by a change in sound.

**Conceptual foundation:** If you let a compressor place its cuts wherever they save the most space, it reveals the text's own natural units rather than the ones we assume. Here it cuts coarser than the 114 sūras, which means the surface style is uniform throughout and the sūra must be a unit of meaning, not of sound — and it hands us a new 'movements' map.

**Utility:** Tells you what a sura really is (a unit of meaning), gives you a new coarse 'movements' map of the book, and shows exactly where meaning-based analysis is still needed.

- **Q0 new knowledge (✅ NEW):** NEW & counterintuitive: the sūra is a unit of MEANING not sound — the text's own surface segmentation makes ~63 'movements', not 114 sūras.
- **Q1 discovers:** Surface register is stationary — MDL prefers ~63 'movements', so a sūra is thematic not stylometric.
- **Q2 category:** Sūra definition — surah/semantic/scale/structure · tier=discovery · phase B
- **Q3 relations:** Builds on L14; reframes L11; uses L09 scale.
- **Q4 validity:** Canonical 113-cut beats random by 2,681 bits, z=13.5; monotone jitter penalty; precision 0.45 reported honestly (necessary≠sufficient).
- **Verdict:** INCLUDE.
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L14 (MDL order-load of the verse stream), L16 (Boundary-load typology (hard vs soft seams)), L09 (Constellation dimensionality + order axis)

#### L12 · Boundary local-optimality ('nothing moved') — ✅ grade 90/100

**Plain:** The exact spot of each sura break is the sharpest point nearby — move it even one verse and the seam gets weaker.

**Conceptual foundation:** If a boundary is correctly placed, nudging it in either direction should only make the seam weaker — meaning it sits on a peak. Checking that gives each boundary a stability score and shows the placement is not arbitrary.

**Utility:** Evidence the boundaries are placed precisely, and it gives each boundary a 'stability' score.

- **Q0 new knowledge (✅ NEW):** NEW: each sūra boundary is precisely placed (a local optimum) — moving it worsens the seam.
- **Q1 discovers:** Each boundary sits at a local optimum ('nothing moved').
- **Q2 category:** Sūra definition — surah/order/structure · tier=discovery · phase A
- **Q3 relations:** Precursor to bit-valued L16; refines L11.
- **Q4 validity:** 54% peak within ±1 vs 33% chance; move-one penalty +ve in 73%.
- **Verdict:** INCLUDE (borderline).
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L16 (Boundary-load typology (hard vs soft seams))

### ▸ Order / sequence

#### L14 · MDL order-load of the verse stream — ✅ grade 95/100

**Plain:** The specific order of the verses carries about 9,000 bits of real, measurable structure compared with the same verses shuffled.

**Conceptual foundation:** Information theory: random can't be compressed, structure can. The real order beats random by ~10k bits, so it is structured. But maximal compression is achieved by SORTING (a crystal), which destroys meaning — and canonical refuses that, sitting between random and sorted. Meaningful sequences (language, music, DNA) live in exactly this intermediate band, which is why compression certifies non-arbitrariness but never proves a sequence is 'best'.

**Utility:** A hard number certifying the order is non-arbitrary (not random) — while honestly showing it is NOT mere sorting. Basis for a displaced-verse detector; do NOT read it as 'maximally optimal'.

- **Q0 new knowledge (✅ NEW):** NEW: the Qur'an's verse order is non-arbitrary by a measurable margin (9,952 bits over random), yet deliberately NOT the most-compressible order (sorting beats it by 7–12k bits) — it sits in the intermediate-complexity band of meaningful sequences, not the maximally-ordered one.
- **Q1 discovers:** Sequential determinacy — verse order is a conserved quantity in bits.
- **Q2 category:** Order / sequence — sequence/order · tier=discovery · phase B
- **Q3 relations:** Bit-capstone of L03/L09; baseline that L15 partitions.
- **Q4 validity:** Directional test (NEW): canonical 30,679 bits vs random-shuffle 40,632 (+9,952, WORSE) but vs length-sorted 18,938 (−11,741) and rhyme-sorted 23,470 (−7,209) — trivial sorts compress BETTER. So canonical is NON-ARBITRARY (far from random, z=285) but NOT the compression-optimum. Within-sūra control isolates 407 bits (z=43); symbol+wave both >0.
- **Verdict:** INCLUDE.
- **Related:** L03 (Verse-length long-range correlation (DFA Hurst)), L09 (Constellation dimensionality + order axis), L15 (Surface-register stationarity — the 'movement' scale)

### ▸ Optimality / perturbation

#### L13 · Perturbation-optimality battery — ✅ grade 94/100

**Plain:** Scramble, delete, add, or swap the text and the measured patterns break — and each kind of damage breaks a specific pattern.

**Conceptual foundation:** A thing that is built to be optimal should get worse under any kind of edit, and each kind of edit probes a different sort of optimality. Systematically damaging the text and watching specific patterns break proves those patterns are load-bearing, not decorative.

**Utility:** A stress-test proving the patterns are real and load-bearing, not lucky coincidences.

- **Q0 new knowledge (✅ NEW):** NEW: the Qur'an's arrangement is an extremum — any edit (move/replace/add) measurably degrades it.
- **Q1 discovers:** Every edit operator degrades the invariant it touches (text is an extremum).
- **Q2 category:** Optimality / perturbation — order/form/content/structure · tier=discovery · phase A
- **Q3 relations:** Stress-test validating L03/L04/L06/L11 jointly.
- **Q4 validity:** MOVE collapses all 4 invariants; REPLACE modality-specific; ADD degrades — operator→modality map holds.
- **Verdict:** INCLUDE.
- **Related:** L11 (Sūra boundary = multimodal discontinuity (NECESSARY)), L16 (Boundary-load typology (hard vs soft seams))

### ▸ Āyah

#### L17 · Āyah is positionally (not marginally) coded — ⛔ grade 75/100

**Plain:** You can't find verse endings just by counting which sounds are common in a verse, because the rhyme lives specifically on the LAST word. You have to look at the ending itself.

**Conceptual foundation:** Some signals live in a specific position — the rhyme on the last word — not in overall averages, and a method that only looks at averages is blind to them by design. So a flat result here is not 'no structure'; it is a precise instruction to look at the ending, not the bulk.

**Utility:** Stops a false 'no structure here' conclusion and tells the app precisely how to detect verse endings: look at the final word.

- **Q0 new knowledge (⛔ novelty FAIL):** Lead, not a finding: a positional rhyme detector beats chance ~3× but recovers only 5% of āyah ends — because the consonantal skeleton strips the rhyme vowels. Tells us āyah rhyme lives in the vowels we removed.
- **Q1 discovers:** Āyah ends are positionally (terminal-word) coded, invisible to marginal stats.
- **Q2 category:** Āyah — ayah/sound/sequence · tier=discovery · phase B
- **Q3 relations:** Follows L06; points to Phase C instrument.
- **Q4 validity:** Positional (terminal-emission) detector, cross-validated internal split: F 0.082 vs shuffle floor 0.025 (~3×) and vs marginal null 0.03 — concept confirmed, but recall only 0.05 because the consonantal skeleton strips rhyme vowels.
- **Verdict:** EXCLUDE — positional signal real but weak (5% recall); needs the rhyme vowels (Phase C2).
- **Related:** L06 (Rhyme adjacency (fāṣila cohesion)), L15 (Surface-register stationarity — the 'movement' scale)
