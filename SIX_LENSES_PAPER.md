# Eighteen Computational Lenses on Qur'anic Style — Conceptual Foundations

*An orientation to what each lens looks at, why, and how it reads on the Qur'an itself.*

> Companion documents: empirical results in `EVIDENCE.md` (#18–77); integrated findings in
> `MASTERY_REPORT.md`; the next forks are scoped at the top of `HANDOFF_MASTERY.md`.
> This paper is **conceptual and illustrative**: every worked example is drawn from the Qur'an only,
> so a reader can see *what each lens measures* before consulting the numbers.

---

## Abstract

The classical claim of *iʿjāz* (the Qur'an's inimitability) is, at root, a claim that its language
occupies a region no other Arabic text reaches. To examine that claim empirically — without presuming
it — we adopted a **positive-control-first** program: a stylistic measure earns the right to be applied
to the Qur'an only after it provably separates a *known* master from ordinary writing in the same
language. Under that discipline we built and gate-validated twelve families of detectors, twelve "lenses,"
each targeting a different layer of verbal craft: (1) lexical–statistical texture and repetition,
(2) large-scale architecture (ring composition and refrain), (3) end-rhyme / *fāṣila*, (4) sound–meaning
iconicity (phonosemantics), (5) the multimodal *fusion* of these, (6) prosodic rhythm (the written
trace of *tartīl*), (7) morpho-syntactic structure (*iltifāt* — grammatical person/number/tense
shifting), (8) morphological-template (*wazn*) distribution, (9) intra-textual narrative recurrence
(the same story re-told across distant sūrahs with variation), (10) discourse macrostructure (the
sequencing of speech-act *moves* — oath, narrative, judgment, address), and (11) shallow syntactic
complexity (parataxis vs. hypotaxis — *wāw*-coordination, relative-clause embedding, clause length), and
(12) lexical-semantic field dynamics (whether the text *sequences* or *clusters* topical fields — mercy,
judgment, nature, law, covenant — distinctively), and (13) **dependency-syntax** with a real
parser (embedding depth and dependency distance — the deep test Lens 11 could only proxy), and (14)
the **recited / phonological** layer (syllable weight, *madd*, *ghunna*, isochrony — the vocalized
stratum where *tartīl* lives), and (15) the **muqaṭṭaʿāt / rasm pointer** — the disjoint opening letters
and their placement in the revealed consonantal text and canonical order, and (16) **canonical-order
thematic coherence** (whether the arrangement of sūras is thematically smooth beyond their length gradient), and (17) the **fāṣila system** — recurrence and
content-fit at the verse-end (do the endings repeat heavily, beyond rhyme, and fit their verse's content?).
This paper explains the
**conceptual foundation** of each lens and walks through a concrete Qur'anic case for it. The empirical
verdicts are summarized at the end of each section and treated fully in the companion files; the purpose
here is orientation, not adjudication. One result stands apart: lens (9), measured at passage scale with
the right controls, is the **one single axis to put the Qur'an clearly into the 2σ neighbourhood beyond
ordinary Arabic** (~+3σ after a tokenization-bug correction; EVIDENCE #43) — sharpening, rather than
replacing, the structured-repetition signature that runs through the whole sweep.

---

## 1. The question, and the rules of evidence

"Is the Qur'an a linguistic masterpiece?" is not, as stated, a testable proposition — *masterpiece* is
an evaluative word. We reformulate it into a falsifiable shape:

> **Does the Qur'an occupy a measurable region of stylistic space that ordinary Arabic — and even
> Arabic masters — do not?**

Four rules govern the search, so that conviction guides *where we look* while evidence decides *what we
claim*:

- **Divine-rootedness control.** Study the *revealed* text, not what humans later added: the priority
  object is the consonantal *rasm* and its content — roots, words, āyah boundaries and counts, sūrah
  structure, and the canonical arrangement (and the order of letters, including the *muqaṭṭaʿāt*). Human
  notational/editorial artifacts — chiefly the *ḥarakāt* (vowel pointing), and likewise tajwīd notation,
  punctuation and editorial sūra titles — are **deprioritized**, because a signal found in them describes
  the editors, not the revelation. (This is why Lens 14, built on the *ḥarakāt*, is retained but not a
  priority line.)
- **Positive-control-first.** A measure is admissible only if it first separates a known master from
  ordinary text in its own language. A yardstick that cannot tell Shakespeare from a newspaper has no
  authority to pronounce on the Qur'an. (This single rule eliminated most "obvious" measures: entropy,
  compression, and mutual information are *mastery-blind* — they fail to separate masters at all.)
- **The telescope rule.** A non-detection means *the instrument was too weak*, never that the feature is
  absent. We therefore (a) validate every detector on a synthetic positive control and a degradation
  ladder before trusting a null, and (b) report nulls as "no signal at this resolution," not "no signal."
- **The invariance gate (G10).** A cross-text verdict is inadmissible unless it survives equal-sized
  windows, at least two tokenizations, and a *same-language* ordinary baseline — with a permutation or
  bootstrap null and, ideally, a ≥2 standard-deviation separation. This is what stops a lucky artifact
  from being mistaken for a discovery (we caught two such artifacts mid-program; see Lens 5).

A recurring touchstone is the Qur'an's own statement about its genre, *Yā-Sīn* 36:69 —
وَمَا عَلَّمْنَاهُ الشِّعْرَ وَمَا يَنبَغِي لَهُ ("We did not teach him poetry, nor would it befit him").
Classical poetics define *shiʿr* as كلام موزون مقفّى — speech that is **metered and rhymed**. Several
lenses below turn out to measure exactly the two halves of that definition (rhyme; meter), which lets us
give 36:69 an empirical reading rather than only a theological one.

---

## 2. Preliminaries — text, units, and how a "lens" is built

**The text and its natural units.** The Qur'an segments naturally at two scales: the *āyah* (verse),
whose end is the *fāṣila* (the rhyme/cadence boundary), and the *sūrah* (chapter). Most lenses treat the
āyah as the basic unit and a window of consecutive āyāt (or a whole sūrah) as the sample.

**Normalization.** Arabic reaches a reader in many orthographic variants; before counting anything we
fold letters to a canonical skeleton (alif variants → ا, the *yāʾ*/*alif maqṣūra* → ي, *tāʾ marbūṭa* → ه,
etc.) and, for most lenses, strip the diacritics. This last choice matters and returns in Lens 6: it
makes lexical comparison fair but renders the short vowels — the carriers of recited rhythm — invisible.

**Anatomy of a lens.** Each detector has the same skeleton, dictated by the rules above:
1. a **feature** (what is counted — a repetition rate, a rhyme class, a phoneme ratio, …);
2. a **null model** (usually a permutation that destroys the structure while preserving the ingredients,
   e.g. shuffling āyah order to test placement);
3. a **gate** (a synthetic positive control the detector *must* flag, a degradation ladder it must track
   monotonically, and an ordinary-text negative it must read near zero) — run *before* the Qur'an;
4. a **report** as a standardized effect size (σ-gap) with a bootstrap probability, against a
   same-language baseline.

With that scaffold fixed, the eleven lenses differ only in *what layer of language they make visible*.

---

## 3. Lens 1 — Lexical–statistical texture and repetition

**Concept.** The oldest computational stylometry treats a text as a bag of tokens and measures its
information texture: vocabulary richness (type–token ratio, Yule's K), word-length regularity, and —
most relevant here — **long-range repetition**, the rate at which content recurs across a passage.
Repetition is the natural quantitative correlate of the Qur'an's celebrated *mathānī* (المثاني, "the
oft-repeated"; cf. الحجر 87, وَلَقَدْ آتَيْنَاكَ سَبْعًا مِّنَ الْمَثَانِي): refrains, formulae, and
recurring narratives.

**What it measures.** Over equal-sized windows we compute character- and word-level repetition (with
frequent function-words optionally removed, to isolate *content* repetition), lexical variety, and
word-length spread, each against a same-language ordinary baseline and ≥2 tokenizations (the G10 gate).

**A Qur'anic case.** Consider *al-Raḥmān* (55). Its verse فَبِأَيِّ آلَاءِ رَبِّكُمَا تُكَذِّبَانِ
recurs **thirty-one times**, threaded between successive descriptions of creation and reward. At the
bag-of-words level this drives the surah's content-repetition far above ordinary prose. The same texture,
softer, pervades the recurring closures of *al-Qamar* (54): after each destroyed nation the refrain
فَهَلْ مِن مُّدَّكِرٍ returns, punctuated by وَلَقَدْ يَسَّرْنَا الْقُرْآنَ لِلذِّكْرِ. And at the largest
scale, the story of Mūsā is retold across al-Baqarah, al-Aʿrāf, Ṭā-Hā, al-Qaṣaṣ and more — the same
narrative, re-voiced with variation. Lens 1 is the lens that *sees* all of this as one quantity:
structured recurrence.

**What we found.** Repetition is the Qur'an's most *consistent* statistical signature — it is genuinely
elevated and ordinary-absent in direction — but its **magnitude is modest**: ~+1σ above classical Arabic,
below the 2σ admissibility bar, and it behaves as a *register* property (shared, in kind, with oral-
formulaic and rhymed-prose Arabic) rather than a Qur'an-unique fingerprint. The cross-language twist
(Lens 5) is that this is the *opposite* of what poetic masters do: Mutanabbi, Shakespeare and Hafez
*minimize* long-range repetition; the Qur'an maximizes it. (EVIDENCE #18–30.)

---

## 4. Lens 2 — Architecture: ring composition and refrain

**Concept.** Beyond local texture lies *composition*: how a sūrah is built as a whole. Two architectural
forms are claimed for the Qur'an. **Ring composition (chiasmus)** is concentric symmetry — a passage
ordered A · B · C · Bʹ · Aʹ, so that the opening mirrors the close around a pivot; a substantial
scholarly literature (e.g. Cuypers on *al-Māʾida* and *al-Baqarah*, Farrin on whole-sūrah symmetry)
argues the Qur'an is pervasively ring-structured. **Refrain** is the opposite move in time: a fixed line
returning at regular intervals (a *periodic*, not mirror, structure).

**What it measures.** For *ring*, we cut a sūrah into blocks and ask whether block *i* is more similar
(in shared roots, then in latent *semantics*) to its mirror block than a random re-ordering of the blocks
would predict — a permutation test on *position*. For *refrain*, we locate near-identical āyāt and ask
whether their spacing is *more regular* than a shuffle of the same āyāt — i.e. whether the repetition is
*architecturally placed*, not merely frequent.

**A Qur'anic case.** *Ring*: open *al-Baqarah* and the scholarly claim is that its great blocks (the
disbelievers / the People of the Book / the Children of Israel / legislation / …) fold symmetrically
about the central passage on the *qibla* — an A·B·…·Bʹ·Aʹ arc spanning the longest sūrah. *Refrain*:
*al-Raḥmān*'s فَبِأَيِّ آلَاءِ returns on a near-fixed beat; *al-Mursalāt* (77) tolls
وَيْلٌ يَوْمَئِذٍ لِّلْمُكَذِّبِينَ ten times; *al-Qamar* alternates two refrains across its panels. These
are the textbook instances the two detectors are built to catch.

**What we found.** A clean split. **Ring composition is *not* detectable corpus-wide** — neither lexically
nor semantically, at any block scale — once tested against a permutation null (the scholarly claims are
passage-level, semantic, and rely on hand-identified pivots, which a uniform statistical sweep does not
reproduce; this is a telescope-rule non-detection, not a refutation of those readings). **Refrain is real
but localized**: only ~9 of 114 sūrahs carry a periodically-placed refrain, with *al-Raḥmān* an
overwhelming outlier (its placement is ~7σ more regular than chance). So architecture, as a *general*
signature, is a null; as a *local device*, it is unmistakably real where it occurs. (EVIDENCE #31–33b.)

---

## 5. Lens 3 — Rhyme and the *fāṣila* (presence vs. persistence)

**Concept.** Every āyah ends in a *fāṣila*, a rhyme/assonance at the pause. This is the audible spine of
Qur'anic style and the *qāfiya* half of the poetry definition. But "rhyme" hides two different
properties that must be separated: **presence** (do neighbouring units rhyme at all?) and **persistence**
(does *one* rhyme hold across a long stretch, or does it shift?). Poetry holds a single rhyme for an
entire poem (*monorhyme*); ordinary prose does not rhyme; rhymed prose (*sajʿ*) rhymes but **shifts** its
rhyme every clause or two. The Qur'an's position on these two axes is the empirical content of "rhyme."

**What it measures.** *Presence* = the rate at which adjacent units share a rhyme ending, above the
chance rate implied by their ending frequencies. *Persistence* = the share of a single dominant ending
across a 20-unit window (high ⇒ one sustained rhyme). Both are computed identically on each register's
natural pause units (āyah, verse-line, sentence, sajʿ-clause), so registers can be compared on the same
footing.

**A Qur'anic case.** Short Meccan sūrahs make the *fāṣila* vivid. *al-Ikhlāṣ* (112) holds one rhyme
across all four āyāt — أَحَدٌ · الصَّمَدُ · يُولَدْ · أَحَدٌ (the rhyme on a final *-ad*). *al-Fātiḥa*
sustains a nasal *-īm/-īn* fāṣila — الرَّحِيمِ · الْعَالَمِينَ · الرَّحِيمِ · الدِّينِ · نَسْتَعِينُ ·
الْمُسْتَقِيمَ · الضَّالِّينَ. *ash-Shams* (91) runs a long *-hā* down the whole sūrah
(ضُحَاهَا · تَلَاهَا · جَلَّاهَا · يَغْشَاهَا · بَنَاهَا · …). In each case a single rhyme is *held*, not
shuffled — the hallmark our "persistence" axis is designed to quantify.

**What we found.** Two-part result. On **presence**, the Qur'an rhymes strongly — far above ordinary prose
(~+2.5σ) and comparable to poetry — but this property is **shared with sajʿ**, so it is *not*
Qur'an-specific (sajʿ rhymes too). On **persistence**, the Qur'an separates even from sajʿ: it *sustains*
one fāṣila across a passage (dominant-rhyme share ≈ 0.49, near poetry's monorhyme ≈ 0.54) where sajʿ
restlessly shifts (≈ 0.23) — a +1.7σ gap, stable across two sajʿ masters (al-Hamadhānī, al-Ḥarīrī). So
the distinctive is not *that* the Qur'an rhymes but *how long it holds the rhyme* — verse-like
persistence, carried on prose with no meter. (EVIDENCE #34, #36–37b.)

---

## 6. Lens 4 — Phonosemantics: sound–meaning iconicity

**Concept.** Sound symbolism (phonosemantics) is the hypothesis that the *sound* of words is not
arbitrary with respect to their *meaning* — that "heavy," emphatic, guttural phonemes (the *mufakhkhama*
ص ض ط ظ ق and the gutturals خ غ ع ح ء ه) cluster in passages of harshness, force and dread, while
"light," flowing sonorants (ل ر م ن and the long vowels) gather in passages of mercy and ease. This is
a recurrent theme in Arabic rhetorical appreciation of the Qur'an: that its *jaras al-alfāẓ* (the ring of
the words) is fitted to the sense.

**What it measures.** Two tests. A **general** one asks whether semantically similar āyāt are also
phonetically similar *beyond* the trivial fact that they share words — a partial correlation between a
semantic-similarity matrix and a phoneme-class-similarity matrix, with lexical overlap partialled out.
A **targeted** one operationalizes the classic claim directly: classify āyāt by a *harsh* vs *gentle*
semantic field (seed roots: عذب، نار، سقر، بطش، غضب… vs رحم، جنة، نور، غفر…) and compare the density of
heavy phonemes between the two.

**A Qur'anic case.** The intuition is easy to *hear*. *al-Masad* (111) opens
تَبَّتْ يَدَا أَبِي لَهَبٍ وَتَبَّ — clipped plosives (ت، ب) hammering a curse. *al-Qāriʿa* (101) rolls a
heavy *qāf* through its name and refrain: الْقَارِعَةُ · مَا الْقَارِعَةُ · وَمَا أَدْرَاكَ مَا
الْقَارِعَةُ. Against these, the gentleness of *al-Kawthar* or the long-vowelled flow of mercy verses
seems to *soften* the consonantal palette. Lens 4 asks whether that felt iconicity is statistically real
and stronger in the Qur'an than elsewhere.

**What we found.** **Null** — on both tests, and this is one of the more striking results. General
sound–meaning binding beyond shared vocabulary is ≈ 0 in the Qur'an and no higher than in prose, poetry,
or sajʿ. The targeted "harsh content ⇒ heavy phonemes" test is also null and in fact slightly *reversed*
(harsh āyāt carry marginally *fewer* heavy phonemes than gentle ones). The felt iconicity of a verse like
*al-Masad* appears to be a property of *individual salient words* and the reader's interpretive framing,
not a measurable system-wide coupling of sound to meaning. (Caveat per the telescope rule: our phonetic
features are coarse consonant classes; finer prosodic/affective features could revisit — but the strong
form of the claim is cleanly unsupported.) (EVIDENCE #38.)

---

## 7. Lens 5 — Multimodal fusion: the "cell"

**Concept.** "No silver bullet": if no single axis is decisive, the signature may live in a *combination*.
Fusion asks whether the **conjunction** of features locates the Qur'an where no single feature can. The
guiding idea is a stylistic coordinate space — rhyme × meter × repetition × variety — in which each genre
occupies a *cell*. Poetry = rhyme + meter + high variety; ordinary prose = none of these; the question is
which cell the Qur'an inhabits, and whether it is one no neighbour shares.

**What it measures.** A classifier is trained to separate Qur'an windows from poetry-and-prose windows
using all axes at once; its cross-validated accuracy is compared with the best *single*-axis accuracy and
with a label-shuffle null. The decisive quantity is not raw accuracy but the **gap**: does the conjunction
beat every axis alone?

**A methodological aside (why the gate matters).** This lens is where the G10 gate earned its keep. An
early run scored a *perfect* AUC = 1.000 — which was a lie: it came from comparing the Qur'an's
*morphologically segmented* tokens against whole-word poetry/prose (a tokenization artifact), compounded
by fixed-length prose "units" that made verse-length variation separate trivially. Both artifacts were
caught and removed; the honest score is ~0.94, not 1.0. The episode is a concrete illustration of the
rule: an instrument that looks too good is usually measuring itself.

**A Qur'anic case.** Take a short Meccan sūrah and read it against the cell. *al-Ikhlāṣ* rhymes (Lens 3,
present *and* sustained), yet does **not** scan to any *baḥr* (no meter), and its diction is plain, not
ornate. That triad — *holds a rhyme like verse · keeps no meter like prose · leans on repetition/plainness
rather than poetic ornament* — is the cell. No qaṣīda sits there (it would scan); no ḫuṭba sits there (it
would not sustain rhyme); even sajʿ sits only partly (it shifts its rhyme and prizes ornament).

**What we found.** The conjunction works where the parts do not. The Qur'an is separable from poetry *and*
prose at AUC ≈ 0.94 (null 0.50); the interpretable two-axis conjunction **rhyme × (non-)meter** reaches
≈ 0.92, beating rhyme alone (~0.76) and meter alone (~0.84) — because rhyme distinguishes the Qur'an from
prose but not poetry, while non-metrical variable verse length distinguishes it from poetry but not prose.
*Only together do they isolate it.* Against the adversarial sajʿ control the bare cell is partly shared,
but the Qur'an still separates (AUC ≈ 0.96) via rhyme *persistence* and *repetition*. (EVIDENCE #35–37b.)

---

## 8. Lens 6 — Prosodic rhythm: the written trace of *tartīl*

**Concept.** Distinct from rhyme (which letters end the line) and from meter (a fixed syllabic template),
*rhythm* is the felt pulse of the recitation — *tartīl*. One text-visible facet of it is **isocolon**: the
tendency of successive pause-units to be *balanced in length*, producing parallel cola — a rhythm *without*
meter. Short Meccan sūrahs feel drum-like and rapid; later Medinan legal passages flow in long breaths.
That contrast is, in part, a rhythm of āyah lengths.

**What it measures.** *Isocolon* = whether adjacent pause-units are more length-balanced than a random
re-ordering of the same units (a placement test). A second feature, *metricality*, gauges how periodic the
consonant–vowel skeleton is (a meter proxy: high for a regular *baḥr*, low for prose).

**A Qur'anic case.** Compare extremes. *al-ʿĀdiyāt* (100) and *al-Qāriʿa* (101) move in short, near-equal
beats — clipped āyāt of similar length, a strong pulse. The "verse of debt," آية الدين (2:282), is by far
the longest āyah in the Qur'an, a single sustained legal period. Lens 6 asks whether, *within* a passage,
the Qur'an balances adjacent āyāt into parallel cola more than ordinary prose, and whether any of this
amounts to meter.

**What we found.** Null for distinctiveness — with the program's most important *caveat*. The Qur'an's
isocolon equals ordinary prose and sits *below* sajʿ (sajʿ is the genuinely isocolonic register of
balanced paired clauses); its metricality is the lowest of all (decisively *no meter*, confirming the
*wazn* half of 36:69). **But** this lens is computed from *consonantal* text — the diacritics, *madd*
(vowel lengthening), *ghunna*, and pause phonology that actually carry recited rhythm are invisible to it.
So the honest reading is "*no rhythm recoverable from the written skeleton*," not "no rhythm." This points
straight at the program's frontier (§11). (EVIDENCE #39.)

---

## 9. Lens 7 — Morpho-syntactic structure: *iltifāt*

**Concept.** Beneath texture, architecture, and sound lies the **grammatical** layer, and it houses the
device the classical critics held to be most distinctively Qur'anic: ***iltifāt*** (الالتفات, "the
turning"). An iltifāt is an abrupt, rule-governed shift of grammatical **person, number, tense, or
addressee** in mid-passage while the referent stays the same — God spoken *about* in the third person
and, a clause later, *addressed* in the second; a singular that becomes a plural; a past that slides into
a vivid present. Al-Zarkashī and al-Suyūṭī catalogue it as a beauty unique to high Arabic style and
especially dense in the Qur'an. The empirical question: does the Qur'an *shift* — in person, number, or
tense — at a higher **rate**, or in a distinctive **pattern**, than ordinary Arabic, poetry, and sajʿ?

**What it measures.** A lightweight tagger labels each pause-unit with its dominant person (1/2/3),
number, and tense, read from independent pronouns (أنا، نحن، أنتم، هو، إيّاك…), the vocative *yā*, attached
clitic pronouns (ـكم، ـهم، ـها، ـنا…) and verb agreement (imperfect prefixes ت/ن/ي/أ vs perfect suffixes).
An *iltifāt event* is a change between adjacent units along any axis. The detector reports a **shift-rate**
and a **transition-type profile** (which shifts: 3→2, 2→3, …), each against (a) a *within-text shuffle*
null that tests whether shifts are *placed* non-randomly and (b) the same-language baselines — with
quoted-speech (*qāla*-framed) boundaries controlled, since ordinary reported speech changes person
without being iltifāt. Because the comparison corpora are unsegmented, the tagger runs on raw text
identically everywhere; calibrated against the Qur'an's own gold morphological segmentation it agrees on
dominant person ~81% of the time.

**A Qur'anic case.** The textbook instance is *al-Fātiḥa*: the opening praises God in the **third**
person — الْحَمْدُ لِلّهِ … مَالِكِ يَوْمِ الدِّينِ — then pivots, mid-sūrah, to **direct address**:
إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ ("**You** [alone] we worship"). A single 3→2 turn reorients the
whole prayer. The longer-range classic is *Yūnus* 10:22, the sea-voyage: it begins addressing the
audience — هُوَ الَّذِي يُسَيِّرُكُمْ ("He it is who carries **you**") — and, as the storm rises, *turns
away* from them into the third person — وَجَرَيْنَ بِهِم … وَفَرِحُوا بِهَا ("and they sailed with
**them** … and **they** rejoiced"), the grammatical swerve enacting the passengers' estrangement. These
are exactly the events the detector is built to count.

**What we found.** **Null vs ordinary Arabic, register-level otherwise.** At equal sample size and across
two tokenizations, the Qur'an's **person**-shift rate is statistically indistinguishable from ordinary
Arabic prose (Δ ≈ ±0.1–0.25σ, P ≈ 0.44–0.50); it exceeds poetry and sajʿ only as a *genre* gap (those
registers are more person-monotone). Number-shifting is, if anything, *lower* than ordinary (more
number-stable). The transition profile does show the Qur'an to be markedly **address-oriented** — its
commonest turns are 3→2 and 2→3, and ~62% of its person-shifts involve the second person, against ~40%
for prose and sajʿ — but this is a *poetry-like* trait that lyric poetry (~69%) **exceeds**, and it sits
below the 2σ bar against every baseline. So iltifāt behaves precisely like the refrain of Lens 2: a real,
artful, **localized** device, not an elevated corpus-wide bulk statistic. One decisive caveat keeps this
from being the last word: the detector is **referent-blind**, whereas true iltifāt requires the shift to
be *referent-constant*; a referent-blind rate conflates ordinary topic-change with genuine iltifāt, and
that confound — not the device's absence — is the likeliest reason no bulk signal appears. The honest
completion needs a gold morphological tagger plus a coreference layer (§13). (EVIDENCE #40.)

---

## 10. Lens 8 — Morphological-template (*wazn*) distribution

**Concept.** Arabic is a templatic language: a consonantal *root* is poured into a *wazn* (pattern) to
make a word — the root k-t-b yields *kataba* (wrote), *kātib* (writer), *maktūb* (written), *kitāb* (book).
The distribution over these derivational templates — verb forms I–X, the participles, the intensive
"attribute" patterns (*faʿīl*, *faʿʿāl*: رَحِيم، غَفَّار) — is a stylistic fingerprint, and the Qur'an's
density of divine-attribute patterns at the verse-end is a natural place to look for one.

**What it measures.** Each content word is sorted, from its de-diacritized skeleton, into a coarse
derivational bucket (form X *istafʿala*, form VII *infaʿala*, the *mu-* participles, form IV *afʿala*,
active participle *fāʿil*, intensive *faʿīl/faʿūl*, broken plural, bare triliteral, other). Over equal-N
word windows we compute the template histogram and score its **JS-divergence from the ordinary-Arabic
histogram**, plus per-bucket rates — against ≥2 tokenizations and a permutation gate.

**A Qur'anic case.** Hear the close of countless āyāt: عَزِيزٌ حَكِيمٌ ، غَفُورٌ رَحِيمٌ ، سَمِيعٌ بَصِيرٌ —
paired *faʿīl* attributes, an intensive-adjective pattern used with unusual density. If any wazn signature
is Qur'an-distinctive, this clustering of *ṣiyaġ al-mubālaġa* (intensive patterns) is the candidate.

**What we found.** **Register-level — and exactly matched by a poetry master.** The Qur'an's template
distribution sits ~+1σ from ordinary prose (JS-divergence), stable across two tokenizations — but
Mutanabbi's poetry sits at the *same* +1σ, so the divergence is genre-level, not Qur'an-specific, and it
is below the 2σ bar. The one >2σ per-bucket cell (fewer bare four-letter *fāʿil* shapes) is
negative-direction and an artifact of classifier granularity (Qur'anic active participles mostly appear
in plural/derived forms that fall in other buckets), not a real avoidance. So *wazn*, like most lenses,
is a register property the Qur'an shares with masters, not a fingerprint. (EVIDENCE #41.)

---

## 11. Lens 9 — Intra-textual narrative recurrence

**Concept.** The Qur'an's most visible large-scale habit is **re-telling**: the story of Mūsā returns in
al-Baqara, al-Aʿrāf, Ṭā-Hā, al-Qaṣaṣ and more; Nūḥ, Ādam, and the punished nations recur across distant
sūrahs — never quite verbatim, always *re-voiced with variation*. This is the narrative correlate of the
*mathānī* (the "oft-repeated"). The question: does the Qur'an show **long-range passage recurrence** —
the same content returning across a great distance — beyond what ordinary Arabic, poetry, or sajʿ do?

**What it measures.** Text is cut into 50-content-word passages; we take their TF-IDF cosine similarities
and ask whether the *far-apart* pairs (separated by a large gap) have a **heavy upper tail** above the
far-pair median — a few distant passages that spike in similarity, the signature of a retold episode
against an otherwise diverse background (which separates true recurrence from mere topical homogeneity).
Two controls make the test decisive: an **equal passage count** per corpus (bootstrap subsampling, to
neutralize the Qur'an's size advantage), a **word-shuffle null** (shuffle all content words and re-chunk:
this preserves the Qur'an's repetitive *vocabulary* but destroys passage-level co-occurrence, so the
residual is recurrence *beyond* mere lexical repetition), and a **verbatim exclusion** (drop near-identical
pairs, so the signal cannot be the refrains of Lens 2).

**A Qur'anic case.** Set Mūsā-before-Pharaoh in al-Aʿrāf 7 beside the same confrontation in Ṭā-Hā 20 and
al-Shuʿarāʾ 26: the staff, the sorcerers, the divine reassurance recur — same lexical-semantic core,
re-ordered and re-weighted each time. No single āyah is copied; the *passage* returns. That is exactly the
0.5–0.9-similarity "far twin" the detector is built to find.

**What we found.** **The one breakthrough of the whole sweep.** This is the one single axis to place the
Qur'an clearly into the 2σ neighbourhood beyond ordinary Arabic: passage-recurrence excess, after the
word-shuffle control, is **~+3σ above ordinary prose** (corrected in #43 from a bug-inflated +3.5–4σ;
range +2.3–4.0 across passage-size, quantile, gap and seed; ordinary residual ≈0 — ordinary narrative does
not return to itself at long range), and it *survives verbatim exclusion* essentially unchanged (the
recurrence lives in the 0.5–0.9 similarity band, not in copies) — so it is genuine **varied retelling**,
not refrain. Two honest qualifications keep it in proportion. First, it is not a *new* axis so much as the
project's central **structured-repetition** signature finally measured at the right grain: the repetition
lens (Lens 1) read only ~+1σ as a bulk rate; the same craft, seen as long-range varied passage-recurrence
with the proper null, reads ~+3σ. Second, it is not unique in *kind*: poetry also clears the bar (+2σ —
Mutanabbi reuses figures and themes across the dīwān); the Qur'an simply **maximizes** a recurrence-genre
trait, by a clear margin. (Baseline magnitudes rest on small passage counts and are provisional.)
(EVIDENCE #42; magnitude **corrected to ~+3σ** in #43 after a tokenization bug — see the note below.)

A correction worth stating plainly, because the program's own rules demand it. While building the
variation profile (EVIDENCE #43) we found that Lens 9's pipeline had been tokenizing the *diacritized*
Qur'an by splitting on the word-regex *before* stripping the ḥarakāt — shattering each word into sub-word
fragments, while the plain-text comparators stayed whole. That asymmetry **inflated** the headline. With
the fix (normalize first, then split — yielding the intended 77.7k real words), the recurrence excess
**survives but settles at ~+3σ** vs ordinary Arabic (range +2.3–4.0 across passage-size, quantile, gap and
seed; word-shuffle-controlled; surviving a second, rasm-character tokenization), with poetry still ~+2σ.
The axis still crosses into the 2σ neighbourhood and remains the program's one structural distinctive — it
is simply more modest than first reported. The variation profile then *characterizes* it: the same figures
recur across vast spans (Mūsā across 32 sūrahs, Ibrāhīm 22, Nūḥ 21), yet the retellings keep verbatim runs
short (~2 tokens) and word-order heavily re-sequenced — recurrence carried by **re-expression, not
copying**. "The same story, told differently each time."

---

## 12. Lens 10 — Discourse macrostructure: the rhythm of *genres*

The nine prior lenses each read one *layer* of language. The tenth reads the *arrangement of registers*:
a sūrah is famous for moving, sometimes abruptly, between an oath, a narrative of past prophets, a scene
of the Judgment, a direct address to the listener, and a flat theological assertion. The hypothesis is
that the Qur'an's signature might live not in any single move but in how it *sequences* them — a
macro-rhythm of genres that ordinary prose, poetry and *sajʿ* (which tend to hold one register) do not
share. This is the cleanest lens to compute from bare text: no parser is needed, only a tagger that labels
each unit by its dominant *speech-act move* and a statistic on the resulting sequence.

**Anatomy.** Each unit (an āyah for the Qur'an; a clause for the comparators) is tagged with one of six
moves — *oath, address/command, narrative, judgment/eschatology, interrogation, assertion* — by
general-Arabic lexical cues applied identically to every corpus. The structural question is then put the
way Lens 9 put recurrence: compare the real move-sequence to a **reshuffle of its own labels**, so that
mere base-rate differences in how often each move appears cancel out, and only genuine *sequencing*
survives. Two statistics carry it — the **switch rate** (how often adjacent units change move) and the
**transition mutual information** (how predictable the next move is from the last) — with a run-length
check for block coherence. The gate passes cleanly: a periodic move-stream fires strongly
(MI-excess +0.85), coherent blocks register as low-switch, and a random stream nulls (~0).

**The reading.** Shuffle-controlled, the Qur'an's move-*sequencing* is **indistinguishable from ordinary
Arabic** — switch-rate −0.86σ, transition-MI +0.05σ, run-length −0.14σ, all null; poetry and *sajʿ*
likewise. The macro-rhythm hypothesis, at this operationalization, does not separate the text. What *does*
separate is the **inventory** of moves, not their order: the Qur'an's per-window genre-entropy is +2.4σ
above ordinary prose (1.01 vs 0.47), and far above poetry (0.21, the most register-monotone of all). Read
concretely: where a page of chronicle or a *qaṣīda* stays almost entirely in one mode, a Qur'anic passage
will, within a few āyāt, swear by the dawn, recount Mūsā, warn of the Reckoning and address the hearer
directly. That heterogeneity is real and felt — but it is a **register-level** fact about which genres are
present, like the repetition rate of Lens 1, not a controlled claim that their *ordering* is patterned.
So Lens 10 lands where most lenses land: a genuine descriptive texture, no structural fingerprint.
(EVIDENCE #44.)

---

## 13. Lens 11 — Shallow syntactic complexity: parataxis vs. hypotaxis

The deepest layer a text-lens can reach without a parser is the *clausal architecture*: how clauses are
joined and embedded. Two classical poles organize it. **Parataxis** strings independent clauses side by
side — the *wāw* of "and… and… and…", the additive rhythm of oral and scriptural prose. **Hypotaxis**
embeds them — relative clauses (*alladhī*, "who/which"), conditionals (*idhā*, "when/if"), complements —
the recursive nesting of elaborated written prose. A reasonable hypothesis is that the Qur'an's syntax is
distinctively one or the other: famously *wāw*-strung (paratactic) yet also rich in embedded relatives.

**Anatomy.** A true reading of embedding *depth* needs a dependency parser (which we do not have for
Classical Arabic here); but the *rate* of the relevant joiners is computable from bare text, because Arabic
marks them with a small closed set of surface function words. We detect, with one lexicon applied
identically to every corpus, the relative pronouns, the complementizer/conditional/temporal subordinators,
the standalone coordinators, the *wāw*-prefix rate (a parataxis proxy), and mean clause length on
pause-units — then compare equal-N windows against the same-language baselines. The gate is a simple
recovery check: inject relative markers at a known rate and the counter returns it (5% → 5.5, 20% → 20.5).

**The reading.** A register-level profile, no decisive fingerprint. The Qur'an embeds somewhat *more* than
ordinary prose (relatives +1.1σ, subordinators +1.2σ) — and notably more relative clauses than poetry or
*sajʿ*, which barely use them — while its clauses run about as long as ordinary prose (≈12 words), not the
clipped 4–5-word units of verse and rhymed prose. Its most salient syntactic feature is **parataxis**: the
*wāw*-initial rate stands +1.9σ above ordinary prose, the quantitative trace of the Qur'an's additive
"and… and…" cadence. But the result lands exactly where the others do — every axis is below 2σ, poetry
*matches* the subordination, and *sajʿ* **exceeds** the parataxis (+3.0σ: rhymed prose is the most
*wāw*-strung register of all). So the *wāw*-cadence is a shared oral/rhymed-register trait the Qur'an
participates in, not a signature it owns; its embedding is mid, prose-like. The honest verdict: a genuine
descriptive syntactic texture, no structural distinctive — and a frontier flag, since true embedding
*depth* (dependency distance, tree nesting) awaits a parser. (EVIDENCE #45.)

---

## 14. Lens 12 — Lexical-semantic field dynamics: the movement between meanings

**Concept.** The eleven prior lenses read texture, form, sound and grammar; the twelfth reads *meaning in
motion*. A Qur'anic passage moves between **semantic fields** — mercy and grace, judgment and the
Reckoning, the natural cosmos, law and ritual, covenant and faith — and the hypothesis is that the
*dynamics* of that movement might be distinctive: either a **cohesion** (the text dwelling within a field
across a passage more than ordinary prose) or a **sequencing** (a patterned order of field-to-field
transitions). This is deliberately *not* the whole-sūrah semantic ring of Lens 2 (mirror symmetry, which
read null); it is field movement at *passage* grain — the level at which a reader actually feels the
Qur'an turn from a scene of mercy to one of warning and back.

**Anatomy.** Each unit (an āyah; a clause for comparators) receives a single field label, and — because
any tagger embeds assumptions — the test is run with **two** independent ones: a **seed-lexicon** tagger
(five fields plus an *other* bucket, from normalized general-Arabic seed words) and a **data-driven** tagger
(per-corpus TF-IDF → SVD → *k*-means into six clusters, which labels *every* unit and so removes the
seed-lexicon's Qur'an-vocabulary bias). The structural question is then put exactly as Lenses 9 and 10 put
theirs: compare the real field-label sequence to a **reshuffle of its own labels**, so base-rate field
frequencies cancel and only genuine sequencing and cohesion survive — measured by the **switch rate** and
**transition mutual information** (sequencing) and the **run-length** (cohesion). The gate passes cleanly
(a periodic field-stream fires at MI-excess +0.85, coherent blocks at run-excess +4.3, a random stream
nulls at ~0).

**The reading.** **Null — and the two taggers agree, which is what makes it decisive.** Shuffle-controlled,
the Qur'an's field *sequencing* and *cohesion* are indistinguishable from ordinary Arabic (every |g| < 0.5σ,
P ≈ 0.4–0.6); if anything the Qur'an clusters its semantic fields *slightly less* than ordinary prose
(run-cohesion g ≈ −0.44 vs ordinary in the data-driven tagger), and *poetry* is the most field-cohesive
register of the four. This lens mattered because, going in, it was the **largest unexplored text-computable
region** — the most promising remaining lever short of the data- and parser-blocked frontiers — and it came
back null. That is itself informative: it narrows the space of where a signature could still hide and leaves
Lens 9's varied recurrence standing yet more alone. (One sub-region remains open: passage-grain cohesion
measured by *embedding* similarity rather than discrete labels, and a coarser pericope grain.) (EVIDENCE #46.)

---

## 15. Lens 13 — Dependency-syntax: real embedding depth

**Concept.** Lens 11 reached the *clausal* layer only through surface proxies (counts of relative
pronouns, *wāw*-rate, clause length) because a true reading of **embedding depth** needs a dependency
parser, which classical-Arabic work rarely has. The thirteenth lens supplies one: each unit is parsed into
a dependency tree, and we measure the structure the proxy could not — **tree depth** (how deeply clauses
nest), **dependency distance** (how far a word sits from its syntactic head — the cost of non-local
linkage), the **long-dependency rate**, and **head-final** word order. The question is the one Lens 11
left open: is the Qur'an's syntax distinctively *deep* or *complex* — or distinctively *flat* — against
ordinary Arabic, poetry and *sajʿ*?

**Anatomy.** A neural UD parser (Stanza, trained on the Prague Arabic Dependency Treebank) parses every
unit; to keep the comparison fair, all corpora are read in the same orthographic condition (diacritics
stripped, since the comparators are undiacritized and the parser is MSA-trained). Metrics are computed
per unit, sampled at equal N across corpora, and reported as σ-gaps with bootstrap probabilities against
the same-language baselines. The gate is a degradation check the parser must pass: scrambling a unit's
word order should *raise* its mean dependency distance (a real metric tracks the loss of structure) — and
it does (2.18 → 2.27).

**The reading.** **Register-level — and, against ordinary prose, the Qur'an is *simpler*, not deeper.**
On every complexity metric the Qur'an sits *below* ordinary Arabic: shallower trees (depth 6.5 vs 8.7,
g = −0.66), shorter dependencies (2.19 vs 2.38, g = −0.36), fewer long-range links (g = −0.27) — all
sub-2σ, none distinctive. It sits *above* poetry and *sajʿ* (+0.3 to +1.25σ), but that is the expected
genre gap: verse and rhymed prose run in short, flat clauses, so any connected prose out-nests them. Head
direction is flat across all four. So the real parser **confirms the parser-free verdict of Lens 11**: the
Qur'an has no syntactic-complexity fingerprint — if anything its clauses are *less* deeply embedded than
ordinary prose, consistent with its paratactic, additive *wāw*-cadence. (Caveats: an MSA-trained parser on
Classical Arabic; small baselines, N = 188; four complexity metrics, no relation-type or valency profile.)
(EVIDENCE #47.)

---

## 16. Lens 14 — The recited / phonological layer (the vocalized stratum)

**Concept.** Every prior lens read *written* text — and largely *consonantal* text, since most lenses
strip the diacritics. But the Qur'an is, in its primary mode, **recited** (*tartīl*), and its felt power
lives in a stratum the written skeleton hides: **syllable weight** (light *CV* vs heavy *CVV/CVC*),
**madd** (the prolongation of long vowels), **ghunna** (the nasal hum of *nūn*/*mīm* and *tanwīn*), and
the **isochrony** of balanced beats. Lens 6 hit this wall and named it the program's frontier. The
fourteenth lens steps through it — to the extent the data allow.

**Anatomy.** Uniquely, the Qur'anic text we hold is *fully vocalized*, so a rule-based syllabifier can read
the harakāt directly into a weight sequence (light/heavy) and compute madd, ghunna, syllable count and a
weight-sequence **rhythm** statistic per āyah. The decisive obstacle is the *comparison*: ordinary Arabic,
poetry and *sajʿ* are available to us only **unvocalized**, so the distinctiveness test is **data-blocked**
until vocalized comparators (a voweled corpus such as *Tashkeela*; a vocalized dīwān) are supplied — and
then only under a strict fairness rule: either gold-vs-gold, or, if the comparators must be
auto-diacritized, the Qur'an must be auto-diacritized by the *same* tool, never gold-against-noisy.

**The reading.** **Instrument built; Qur'an-internal structure is real; cross-text distinctiveness awaits
data.** Two internal validations confirm the lens measures something genuine. First, **isochrony**: short
Meccan sūrahs are measurably more even in syllable count (CV ≈ 0.36) than long sūrahs (≈ 0.48) — the
drum-like beat of *al-ʿĀdiyāt* or *al-Qāriʿa* made quantitative. Second, **rhythm**: the syllable-weight
sequence *alternates* light and heavy far more than a shuffle of the same syllables (lag-1 autocorrelation
z ≈ −10.7 in *al-Baqara*, −6.0 in *al-Raḥmān*) — a real, non-random recited pulse. What we **cannot** yet
say is whether this exceeds ordinary vocalized Arabic: alternation and isochrony may be partly universal
Arabic phonotactics, and only a vocalized baseline can separate Qur'anic craft from the language's own
rhythm. So Lens 14 is, honestly, the frontier now *instrumented but not yet adjudicated* — the one region
where "absence of evidence is not evidence of absence" is not a slogan but the literal state of play.
**A governing caveat, though:** these features are read from the *harakāt*, a human notational layer added
to the revealed consonantal *rasm*. Under the project's divine-rootedness control (§1) this lens is
**deprioritized** — even a positive cross-text result would describe editorial vocalization, not the
revealed text itself. The priority remains the revealed layers: *rasm*, roots, words, and the
āyah/sūrah/canonical structure. (EVIDENCE #49.)

---

## 17. Lens 15 — The muqaṭṭaʿāt / rasm pointer (the revealed-text structure)

**Concept.** The previous fourteen lenses ask whether the Qur'an's *style* occupies a region other Arabic
does not. The fifteenth asks a different, and — under the divine-rootedness control (§1) — a *higher*-
priority question: does the **revealed text itself**, read as pure *rasm* (consonant skeleton) and
canonical order, carry **designed structure**? Its sharpest instance is *al-muqaṭṭaʿāt*, the disjoint
letters that open twenty-nine sūras (*Alif-Lām-Mīm*, *Ḥā-Mīm*, *Qāf*, *Nūn* …) — letters with no lexical
meaning, whose very mystery makes them a clean test of design. This lens deliberately uses **no ḥarakāt**:
everything it measures is in the revealed consonantal text and the muṣḥaf arrangement.

**Anatomy.** Three structural tests on the 29 sūras, each against a permutation null. **Bearer enrichment:**
does a sūra's opening letters occur at an elevated rate in its *own* consonantal body, versus randomly
chosen letter-sets of the same size? **Half-alphabet:** how many distinct letters appear across all the
muqaṭṭaʿāt? **Canonical contiguity:** are the 29 sūras clustered together in the muṣḥaf order beyond what
random 29-subsets of the 114 give? A gate confirms the enrichment metric responds (a planted
over-represented letter fires at 1.49×; random letters read ~1.0×).

**The reading. A genuine, validated structure — the divinely-rooted kind of result.** All three fire.
The distinct letters number **exactly fourteen — half the twenty-eight-letter alphabet** (*niṣf al-ḥurūf*),
a clean and long-noted fact here confirmed mechanically. The opening letters are **enriched in their own
sūra's rasm** (1.06× aggregate, z = +2.2, p = 0.02), modest in bulk but concentrated exactly where one
would expect — the *single-letter* sūras lead (*Qāf* 1.73×, *Ṣād* 1.46×, *Nūn* 1.24×), the famous "*qāf*
lead," while sets containing the ultra-common *alif*/*lām* dilute toward one. And the 29 sūras are
**strongly clustered in the canonical order** — 19 adjacent pairs against a chance expectation of ~7
(p < 0.0001), the same position-pointer the app's label-permutation test reads at p ≈ 2×10⁻⁵. A proper
spatial statistic confirms it (Moran's I = +0.54, z = +5.8 over the 114-sūra sequence), and the clustering
is **robust to re-ordering**: it survives even under the revelation (*nuzūl*) chronology (Moran's I = +0.31,
contiguity p = 0.001), though it is strongest in the *muṣḥaf* arrangement — so the structure is partly
chronological and amplified by the canonical order, not an artifact of either. The bearer enrichment, in
turn, concentrates in the *distinctive* consonants (*ṭāʾ* 1.25×, *qāf* 1.24×, *nūn* 1.24×, *ṣād* 1.18×)
while the ubiquitous *alif/lām/mīm* sit at ~1.0 — the "*qāf* lead" is really an emphatic-letter lead. These are not
cross-text *style* claims (there is no "ordinary-Arabic muqaṭṭaʿāt" to compare against); they are
**internal design properties of the revealed text**, validated against permutation nulls. As such this is
the **second positive structural result of the whole program** — and, unlike #42 recurrence (which the
Qur'an shares in kind with poetry), it is *sui generis* to the revealed text. One popular *further* claim,
though, does **not** survive the gate: that the fourteen letters form a *structured* half — taking half of
every phonetic category. Some categories do split exactly (voicing: 5/10 voiceless, 9/18 voiced; emphatic
2/4; stop 4/8), which is individually striking, but the *aggregate* balance across categories is only
modestly better than a random fourteen-letter subset (p ≈ 0.14, not significant; throat and labial
deviate). So the structure that is real is **cardinality and position**, not phonetic balance — a useful
guard against over-reading. One further result, though, *deepens* the pointer rather than tempering it:
the grouping is **coherent in root-space, not merely positional**. Read as TF-IDF vectors over their
*roots*, the 29 sūras are roughly twice as similar to one another as random sūra-sets (mean cosine 0.53
vs 0.25, z = +6.9), and each same-letter subgroup is internally cohesive beyond chance — the *Ḥā-Mīm*
seven (z = +3.1), the *Alif-Lām-Rā* and *Alif-Lām-Mīm* families likewise. The opening letters thus track
**lexical-thematic families**: sūras that share a letter share content. (This is not a register artifact: against a
**Meccan-only null** the cohesion *strengthens* — z rises to +7.4, because long Medinan legal sūras
otherwise inflate the random baseline — so the grouping is genuinely letter-specific, not merely shared
Meccan vocabulary.) And the cohesion is **anchored in content**: the muqaṭṭaʿāt sūras over-express the
revelation / "the Book" lexicon (*kitāb*, *nazzala*, *āyah*, *waḥy*, *ḥikma*…) — whole-sūra rate +47%
above other sūras (z = +3.6, p = 0.0002), and in their *openings* the disjoint letters are immediately
followed by mention of the Book at roughly five times the baseline rate (*Alif-Lām-Mīm — that is the
Book*; *Ḥā-Mīm — a revelation of the Book*). The letters function as a frontispiece to scripture that
speaks about scripture. A second, important limit (EVIDENCE #59): this content-cohesion is **not unique to
the disjoint letters** — other coherent traditional groupings cohere as much or more (the seven long sūras
at cosine 0.78; the Medinan corpus at z = +5.4), so root-cohesion is a *general* property of
length- and theme-homogeneous groups and must be down-weighted as evidence of design-via-letters. What
remains *sui generis* is the **positional** pointer and the **half-alphabet cardinality**, not the content
cohesion. One further limit: the same-letter families are *not* separable from one
another as whole root-vectors (within-group ≈ between-group cohesion, p = 0.37) — there is no decodable
letter→theme cipher. Their *distinctive* roots are vividly thematic (the *Alif-Lām-Rā* group carries the
Yūsuf lexicon — prison, measure, scheming; the *Ṭā-Sīn* group the Mūsā–Pharaoh cycle — sorcery, troops,
Madyan; the *Alif-Lām-Mīm* group the legislation of *al-Baqara* — trade, *ribā*, divorce), but this simply
reflects which narratives those particular sūras contain, not a property of the letters themselves. The
established result is cohesion and content-anchoring, not a cipher. (EVIDENCE #50–56.)

**The network-first extension (#67): combinatorics, order, and time.** Three further probes, run
network-first and each against its own randomization null, sharpen what kind of design the pointer is.
First, the letter **combinatorics** survive a proper null. Read as a bipartite sūra×letter system
(29 × 14, 78 incidences) and randomized by degree-preserving swaps — every sūra keeping its letter-count,
every letter its bearer-count — the system's reuse of **whole combinations** (*Alif-Lām-Mīm* six times,
*Ḥā-Mīm* six, *Alif-Lām-Rā* five) is far beyond what the margins allow by chance (combination-entropy
z = −12.6); the letter-families form **real communities** in the projection (modularity z = +6.9),
upgrading the descriptive topology of the earlier network view to a nulled result; and the architecture
is significantly **anti-nested** (z = −7.0) — the letter-blocks *partition* the half-alphabet
({الر} | {حم-cluster} | {كهيعص} | {ن}) rather than nesting inside one another. Modular, not hierarchical.
Second, **order within the openings carries design beyond the multiset**. Treating each distinct opening
as an *ordered* rasm sequence and shuffling only within sequences, the observed transition system is
markedly concentrated — seventeen distinct letter-transitions where the null expects twenty-one
(z = −3.5), with low transition-entropy (z = −4.2): the combinations are built from a small kit of reused
ordered motifs (the *alif→lām* backbone branching to *rāʾ/mīm*, then *mīm→rāʾ/ṣād*; *ḥāʾ→mīm*;
*ṭāʾ→sīn/hāʾ*). Strikingly, **no transition is ever reversed** anywhere in the system — every letter-pair
flows in one direction only — though as a lone statistic this perfect consistency sits just under the bar
(p = 0.06) and is reported as suggestive. Third, the families are **deployed in time as blocks**: the
mean within-family rank-distance among the 29 sūras is less than half the null expectation not only in
the canonical order (z = −4.7, partly the contiguity already seen) but **at least as strongly in the
revelation chronology** (z = −5.3) — the *Ḥā-Mīm* seven arrive nearly consecutively in *nuzūl*, the
*Alif-Lām-Mīm* set in its two known blocks. The letter-system was unfolded in coherent temporal waves,
not scattered. All three results are Qur'an-internal (sui generis, randomization-null comparator) and
none re-opens content: the pointer's established anatomy is now **cardinality + position + combinatorics
+ ordered motifs + temporal deployment**, with content still not letter-organized. (EVIDENCE #67.)

**The order has a name (#68): the openings spell in the ancient alphabet.** The perfect one-directionality
invited a sharper question: is the within-opening letter order following a *known* key? Three candidate
keys were tested in both directions with a selection-corrected null — the modern *hijāʾī* alphabet (the
shape-sorted didactic order), the **abjadī order** (the ancient Semitic letter sequence *abjad hawwaz
ḥuṭṭī kalaman saʿfaṣ qarashat*, which predates and underlies the hijāʾī re-sorting), and corpus
letter-frequency rank. Only orders were tested — letter *values* and any numerology were deliberately
excluded, per the program's standing guard. The verdict is one-sided: the hijāʾī order reads at chance
(0.578) and frequency below the bar (0.644), but the **abjadī order fits at 0.889** — forty of forty-five
letter-pairs across the eleven multi-letter openings run in ancient-alphabet order (z = +4.3; corrected
for testing six keys, p = 5×10⁻⁵), rising to 0.925 (z = +6.6) when the heavily-reused families weight the
count. *Alif-Lām-Mīm*, *Alif-Lām-Rā*, *Ḥā-Mīm*, and their extensions are, letter for letter, abjadī-sorted
strings. This explains the one-directionality — pairs never reverse because the openings are (mostly)
sorted by one fixed ancient key — and it joins the half-alphabet cardinality as a second *alphabet-system*
property: the muqaṭṭaʿāt relate to the Arabic letter inventory as an ordered system, and the ordering they
honor is its **oldest attested one**, not the later scribal convention. The honest residue is reported
with the signal: five pairs violate the key (*Kāf-Hā-Yā-ʿAyn-Ṣād* opens with a *kāf* placed against it;
*Ṭā-Hā*, *ṭā-sīn-mīm*'s ending, and one pair of *ḥā-mīm-ʿayn-sīn-qāf*), and one three-cycle (م→ع→س→م) in
the transition graph means no total order — abjadī or otherwise — can sort every opening. The key is
dominant, not exceptionless, and the outliers are named, not explained. (EVIDENCE #68.)
A calibration completes the picture (#69): an exact search over *all* possible letter-orders shows the
ceiling any key could reach is 0.978 — one pair is unsortable by *any* total order (the three-cycle) —
and the abjadī key sits four pairs below that ceiling, matched by only ~0.04% of the full permutation
space; the data-fit optima themselves are uninterpretable overfit strings. A sweep of further candidate
keys (articulation order, frequency) finds nothing above the bar, and the five violations turn out to be
*local*: every deviating opening is exactly one move from its abjadī-sorted form. The residue is small,
structured, and honestly open — the fronted *kāf* of *Kāf-Hā-Yā-ʿAyn-Ṣād* stands as the named outlier.
**Stance re-weight.** One classification must be added under the divine-rootedness control: the abjadī
sequence is itself a *human* cultural convention — ancient, but of the same evidential class as the
ḥarakāt or the Meccan/Medinan labels. The *revealed-layer* fact, which stands at full weight, is the
openings' internal **order-discipline**: one-directionality, conserved transitions, and near-ceiling
consistency with a single fixed sequence. That the best-matching known key is the oldest attested
alphabet ordering is recorded as a historical frame of genuine interest — not as a design claim.

---

## 18. Lens 16 — Canonical-order thematic coherence

**Concept.** The muqaṭṭaʿāt result showed one set of sūras clustered in the canonical order; the sixteenth
lens asks the general version: is the *whole* muṣḥaf arrangement thematically coherent — are
canonically-adjacent sūras more alike in content than chance — and is that beyond the obvious fact that the
muṣḥaf is roughly ordered by length? This treats the **order itself** as a revealed datum.

**Anatomy.** Each sūra becomes a root-TF-IDF vector; the statistic is the mean cosine between consecutive
sūras in canonical order, tested against two nulls: a full re-ordering, and — decisively — a
**length-band null** that shuffles only within blocks of six consecutive sūras, preserving the global
length gradient while destroying fine adjacency. NMF then extracts latent themes as a descriptive check.

**The reading. Positive, and it survives the length control.** The muṣḥaf is strongly length-ordered
(position↔length r = −0.73), so the raw adjacency signal against a full shuffle (z ≈ +10.6) is mostly that
gradient. But against the length-band null the neighbors are *still* more root-similar than chance
(z = +3.14, p = 0.0007): there is genuine **local thematic coherence beyond length** — the arrangement
places kindred sūras together (the *Ḥawāmīm*, the *Ṭawāsīn*, the *Musabbiḥāt*), generalizing the
muqaṭṭaʿāt contiguity to the whole book. The effect is modest in size but robust. NMF independently
recovers recognizable axes — a clean refuge/*Muʿawwidhāt* cluster, eschatology, creed, devotion — evidence
the decomposition is reading real themes, not noise. **An important limit (EVIDENCE, E1-comparator):** this
local coherence is *internally* real (vs shuffle) but **not distinctive against ordinary Arabic** — a
surface-word coherence-decay comparison finds ordinary prose is *more* locally coherent than the Qur'an
(neighbour-similarity ratio 1.82 vs 1.50). So Lens 16 is a genuine description of the arrangement, not a
cross-text distinctive; the Qur'an's coherence is comparatively weak at *short* range and strong at *long*
range — its signature is the architecture of return (Lens 9), not local flow. (EVIDENCE #57.)

---

## 19. Lens 17 — The fāṣila system: recurrence and content-fit at the verse-end

**Concept.** Three earlier lenses brush the verse-end — rhyme presence/persistence (Lens 3), intratextual
recurrence (Lens 9), and the *faʿīl* divine-attribute templates (Lens 8). The seventeenth asks whether the
*fāṣila* is a **system**: do the verse-ending words *recur heavily* (beyond what rhyme requires), and does the
ending *fit* its verse's content? This is the rhyme-end grouping made into a test, with the ending taken as a
morphological wordform (رحیم, علیم, حکیم, قدیر, صادقین) — the apt unit, since the attribute lives in the form.

**Anatomy.** Two measurements. **Ending-repetition:** equal-N type-token ratio of ending words and the
fraction of units whose ending recurs ≥3×, across the Qur'an and comparators. **Content-fit:** group āyahs by
their ending (root and morphology grains), measure body-cohesion (root-TF-IDF) against a random same-size
null, with the ending's own root stripped from the body (a strict self-repetition control).

**The reading. Positive — and partly cross-text distinctive.** First, the Qur'an **heavily repeats specific
ending words**: 28% of āyāt end in a word used ≥3× elsewhere, against 2–10% in ordinary Arabic, poetry, and
*sajʿ* — and this *exceeds sajʿ*, which rhymes (so it matches type-level ending variety) yet does not repeat
the *same* word heavily (EVIDENCE #63). So the fāṣila is not mere rhyme. Second, the ending **fits the
content**: grouping by the āyah-final attribute predicts body content strongly (morphology grain, mean
z = +12.1, 16/16 classes — *qadīr* +32, *raḥīm* +29, *ḥakīm* +26), surviving the self-repetition control
(EVIDENCE #62). The picture reconciles with Lens-16's verse-end finding that the fāṣila does *not* chain to
the next āyah (#60): the ending couples **vertically**, capping its own verse's meaning, not horizontally to
its neighbour. (Honest limit: the content-fit itself is Qur'an-internal — comparators lack enough repeated
endings to group — so the cross-text distinctive is the heavy ending-repetition, on which the fit then rests.)
(EVIDENCE #60–63.)

---

## 20. Lens 18 — Temporal deployment: revelation-time as a structural dimension

**Concept.** The seventeen lenses so far read the text in space — its words, sounds, and arrangement.
The eighteenth reads it in **time**. The corpus exists in two authentic orders (muṣḥaf and nuzūl), and
the rearrangement protocol has always reported both; Lens 18 promotes the temporal side to a lens of its
own: do the text's structures *arrive* in organized ways across the years of revelation? The traditional
chronology is a human scholarly frame, used here as the established rearrangement order (never as a
revealed datum), and every claim below is Qur'an-internal — no comparator corpus has a nuzūl.

**Anatomy.** Three instruments, each with its own discipline. *Deployment waves*: per-sūra feature rates
under Moran's I in nuzūl order, with a within-period null (the Meccan/Medinan cut, control-only) so the
gross register shift cannot masquerade as fine structure (#70). *Wave content*: within-wave minus
between-wave content similarity, computed on cross-sūra pairs only with a sūra-level permutation null,
so sūra-vocabulary blocks cannot fake a temporal shift (#71). *Axis stability*: any data-derived
temporal axis must survive a restart battery — recur under random re-initialization with its temporal
clustering intact (#75). Two of this lens's own candidate findings died on these controls (تعملون's
wave-content; the first-revelations axis C5), which is what makes the survivors worth stating.

**The reading. Time is organized — selectively, and the selectivity is the finding.** The muqaṭṭaʿāt
letter-families arrive as temporal blocks (within-family nuzūl distance z = −5.3, finer than the period
split; #67). The verse-seal system splits along two *independent* temporal dimensions — usage-rate waves
and content re-aiming — populating all four cells of a 2×2 typology (#70/#74): يعلمون and اليم do both
(the ignorance-polemic re-aimed from cosmos to scripture; the punishment-seal moving from past nations
into the living community, #71); تعملون waves in rate only; عليم re-aims in content only; the great
mercy-formulas do neither. A whole-sūra devotional wave sits inside the early Meccan period (al-Aʿlā,
al-Layl, ash-Sharḥ — within-period z = +3.2, stable across restarts; #75), and the latent thematic axes
of the sūra×root matrix are themselves *order-typed* — some arranged by the canon, some by time, the
great creed/narrative axes by both (#72). Against all this stands a load-bearing null: the narrative
anchors — Mūsā (135×), Firʿawn, Ibrāhīm, Nūḥ, ʿĪsā — show **no temporal clustering at all**. The stories
are re-told continuously across the whole timeline. That null sharpens the program's central thesis from
the temporal side: the architecture of return is a *standing mode* of the text, not a phase of it — the
book returned to its matter in every year it was revealed, while its seals and letter-system deployed in
campaigns. (EVIDENCE #67, #70–#75.)

---

## 21. Synthesis — the shape of the answer, and 36:69

Read together, the seventeen lenses converge on a single, defensible picture — a small set of positive
results standing out from an otherwise register-level sweep (with two earlier "positives" since
down-weighted by comparator tests, recorded honestly below):

| Axis (lens) | Where the Qur'an sits | Distinctive? |
|---|---|---|
| Repetition (1) | high (vs masters' *low*) | yes in direction; modest as bulk rate (~+1σ) |
| Architecture (2) | ring null; refrain local (~9 sūrahs) | not corpus-wide |
| Rhyme presence (3) | high, like poetry | shared with sajʿ |
| Rhyme **persistence** (3) | sustained, like monorhyme | **yes vs sajʿ (+1.7σ)** |
| Phonosemantics (4) | ≈ 0 | no |
| Fusion cell (5) | rhyme + no-meter + repetition | **yes as a conjunction** |
| Prosody (6) | no meter; isocolon ≈ prose | null at text level |
| Morpho-syntax / *iltifāt* (7) | person-shift ≈ prose; address-oriented like poetry | null at text level; localized device |
| *Wazn* templates (8) | +1σ from prose, like poetry | register-level; no |
| **Recurrence (9)** | **varied retelling, passage-grain ~+3σ vs prose** [#43-corrected from +3.5–4σ] | **yes — the one single-axis to reach 2σ (poetry +2σ)** |
| Discourse macrostructure (10) | move-*sequencing* ≈ prose; move-*inventory* +2.4σ richer | null on structure; register-level genre diversity |
| Syntax: parataxis/hypotaxis (11) | *wāw*-paratactic +1.9σ (sajʿ exceeds); embedding mid, prose-like | register-level; no (parser-free proxy) |
| Lexical-semantic field dynamics (12) | sequencing/cohesion ≈ prose (clusters fields ≤ ordinary) | null; no |
| Dependency-syntax (13) | depth/distance *below* prose; above verse | register-level; no (real parser confirms 11) |
| Recited/phonological (14) | real internal rhythm + isochrony (vocalized) | **data-blocked** + deprioritized (ḥarakāt = human artifact) |
| **Muqaṭṭaʿāt / rasm pointer (15)** | half-alphabet (14/28); bearer enrichment z=+2.2; canonical contiguity p<10⁻⁴ | **yes — validated revealed-text design structure** (sui generis) |
| Canonical-order coherence (16) | adjacent sūras root-similar beyond length (z=+3.1, p<10⁻³) | internal only — NOT cross-text distinctive (ordinary prose more locally coherent, E1-cmp) |
| **Fāṣila system (17)** | heavy ending-repetition (≥3× share 0.18 on surface words [#76-corrected from 0.28 lemma-grain] > sajʿ 0.04, ord 0.10) + ending fits content (z≈+12) | **yes** — recurrence + content-fit at the verse-end, exceeding sajʿ (vs-ordinary margin ≈+2.2σ after correction) |
| **Temporal deployment (18)** | letter-families in nuzūl waves (z=−5.3); seal 2×2 typology (rate-waves × re-aiming); early-Meccan devotional wave (z=+3.2 within-period); narrative anchors NULL (return spans time) | **Qur'an-internal** — organized revelation-time; no comparator possible (no corpus has a nuzūl) |

The two halves of the classical poetry definition fall out cleanly: the Qur'an has the **qāfiya** (rhyme,
Lens 3) but not the **wazn** of meter (Lenses 5–6). That is the literal content of وَمَا عَلَّمْنَاهُ
الشِّعْرَ — *not poetry*. Against rhymed prose (*sajʿ*) it is *also* set apart — not by rhyming but by
**sustaining** its rhyme and by **structured repetition** — so it is not simply sajʿ either. And the
repetition theme, which threads Lenses 1, 2 and 5, finally yields a clean magnitude in Lens 9: measured
as long-range **varied recurrence** at passage scale, the Qur'an stands ~+3σ beyond ordinary Arabic
(corrected in EVIDENCE #43 from a bug-inflated +3.5–4σ; still the one axis to reach the 2σ neighbourhood).
The honest summary is therefore two-layered: a **conjunction** (sustained rhyme + absent meter + high
recurrence) that locates the Qur'an in a cell poetry, prose and sajʿ each occupy only in part; and,
within that conjunction, **one axis — structured varied recurrence — that is itself decisively elevated**,
though shared in kind with the recurrence of poetry. The Qur'an's craft signature is not ornament or
sound but *the architecture of return*.

And there is now a **second** positive result, of a different order. Where recurrence (Lens 9) is a *style*
distinctive the Qur'an shares in kind with poetry, the **muqaṭṭaʿāt / rasm pointer (Lens 15)** is a
*designed structure of the revealed text itself* — the disjoint letters drawing on exactly half the
alphabet, enriched in their own sūras' consonants, and clustered in the canonical order far beyond chance
(p < 10⁻⁴). It is *sui generis*: there is no other-Arabic baseline to share it with. Under the
divine-rootedness control this is the more important kind of finding — it concerns the revealed object, not
its editorial or stylistic surface — and it marks the most promising direction for the work that remains:
the rasm, the roots, the words, and the geometry of their placement in the canonical text.

**The consolidated picture — the architecture of return.** Pulling the survivors together, and marking what
later comparator tests *removed*, the Qur'an's distinctiveness is **structured return at several scales** —
not ornament, sound-iconicity, syntactic depth, or local flow. (i) Long-range *varied passage-recurrence*
(Lens 9, ~+3σ) is the central axis. (ii) At the verse-end the same return concentrates as a *fāṣila system*
(Lens 17): the Qur'an repeats specific, content-fitted attribute-endings more heavily than even *sajʿ*, while
rhyme *persistence* (Lens 3, +1.7σ) sustains one ending where *sajʿ* shifts. (iii) Only as a *conjunction*
(sustained rhyme + absent meter + high recurrence) does the style isolate the text (Lens 5, AUC ≈ 0.94).
(iv) A distinct, divinely-rooted layer — the muqaṭṭaʿāt *positional* pointer and *half-alphabet* cardinality
(Lens 15) — is *sui generis* to the revealed text. Two honest **down-weightings** belong in the same picture:
the muqaṭṭaʿāt *content*-cohesion and the *canonical-order* coherence (Lens 16), though internally real, proved
to be **general** grouping/coherence effects — other traditional sūra-groups cohere as much (the seven long at
cosine 0.78), and ordinary prose is *more* locally coherent than the Qur'an — so neither is a cross-text
distinctive. The unifying reading is consistent and falsifiable: **locally the Qur'an is *less* continuous
than ordinary prose (self-contained āyāt); at long range it *returns* to itself more.** Its coherence is the
architecture of return, and its one revealed-text structural signature is the disjoint-letter pointer. None
of this is stated beyond what the gates support: each positive carries its boundary, each down-weighting its
comparator, each null its caveat.

---

## 22. The frontier, and what remains

Every text-lens reads *written, largely consonantal* text. The layer they structurally cannot reach is
**recited prosody** — syllable weight, *madd*, *ghunna*, pause — where *tartīl* and the oral experience of
the Qur'an actually live (Lens 6 hit this wall; Lens 14 now instruments it). The instrument exists and the
Qur'an's internal recited rhythm is real, but the **distinctiveness** test remains **data-blocked**:
crossing it needs **vocalized comparison corpora** (fully voweled poetry/prose/sajʿ, or recited audio),
under the gold-vs-gold (or symmetric auto-diacritization) fairness rule. This is the single largest
unexplored region and the most likely home of anything new. The morpho-syntactic layer
(Lens 7) is opened but its faithful test is *referent-aware* iltifāt, which needs gold morphology plus a
coreference layer. The **dependency-syntax** frontier that Lens 11 could only proxy is now genuinely
crossed (Lens 13, with a real parser) and reads register-level — though a Classical-Arabic-tuned parser
and larger baselines would firm it. And the breakthrough lens (9) deserves **larger, genre-matched
baselines** to firm its magnitude. The pointed implication of the whole sweep: the Qur'an's distinctiveness, where it is real, is
an **architecture of recurrence and sustained sound** — and whatever remains beyond it most likely lives
in the recited/phonological stratum that text statistics cannot observe. (Remaining forks and the next
lens are scoped at the top of `HANDOFF_MASTERY.md`.)

**An emerging programme worth recording (the *signal-geometry* lens).** The reframing that the āyah is, by
its own name, a *sign* (*āyah*) invites treating each unit as a **signal** and bringing the full apparatus
of signal processing and linear algebra to bear — point/area/vector patterns, wavelet (scale-local) rather
than only Fourier (global) analysis, **masking and filtering** (both to *remove* a confound that hides a
signal and to *isolate* a band in which one lives), decomposition, projection, and the *pointer* idea that
a concept is an umbrella selecting a distributed signal (operationally, a mask plus a vector). This is a
generative frame, and its first probes are honest **negatives**, recorded so the reasoning is traceable:
naive univariate character point-patterns proved to be a sample-size artifact; a wavelet *locality* signal
on verse-length looked promising (~+2.4σ) but, once the rhyme/refrain direction was **masked out**,
collapsed below the bar and failed to generalize to a non-length formulation — i.e. it was largely Lens 2's
localized refrain seen through a new instrument, not a new axis; and a positional/directional sub-unit lens
(studying within-āyah sub-units — character → root → morpheme — left-to-right *and* reversed) is
operationally real but not, on its first feature, Qur'an-distinctive. None of these earns a coverage claim;
all stay open under the telescope rule, because a null indicts the *formulation*, not the idea. The
discipline that governs them is the same one that governs the twelve lenses, stated as a named principle:
**absence of evidence is not evidence of absence** — it licenses continued *search*, never a *claim*. (Full
register: `IDEA_SIGNALS_GEOMETRY.md`.)

---

## 22. Honest limits

- All effect sizes rest on modest non-Qur'an samples; magnitudes (not directions) should be read as
  provisional — most acutely for recurrence (Lens 9), whose baselines have only 43–92 passages.
- Field dynamics (Lens 12) used a discrete-label sequence; an *embedding*-based passage-cohesion measure
  and a coarser pericope grain are untested and could in principle revisit the null.
- Dependency-syntax (Lens 13) used an MSA-trained parser on Classical Arabic with small baselines
  (N = 188) and four complexity metrics; a Classical-Arabic-tuned parser, larger baselines, and a
  relation-type/valency profile would sharpen it (the direction — register-level — is unlikely to move).
- **Recited/phonological (Lens 14) is computed from the *harakāt*, which are a human notational artifact,
  not part of the revealed consonantal text (rasm).** Under the project's divine-rootedness control this
  layer is therefore **deprioritized**: any signal it showed would be a property of editorial vocalization,
  not of the revealed text. It is retained as instrumented and internally validated, but it is not a
  priority target; the revealed-text layers (rasm, roots, words, āyah/sūrah structure, canonical order)
  take precedence.
- Muqaṭṭaʿāt / rasm pointer (Lens 15): the bearer-enrichment aggregate is modest (1.06×) and carried by
  the single-letter sūras; the contiguity signal partly reflects the grouping of same-letter sūras (the
  *Ḥā-Mīm* septet, the *Alif-Lām-Rā* run). These are internal design facts validated by permutation, not
  cross-text style claims, and the deeper "why these letters / this placement" is not adjudicated here.
- "Rhyme" is approximated by final letters, not full pause-form *rawī*; a true *sajʿa*-boundary parser
  would sharpen Lens 3.
- *sajʿ* is represented by Maqāmāt (one genre, two authors); Nahj al-Balāgha *ḫuṭab* would broaden it.
- Architecture was tested as mirror-ring and verbatim-refrain only; verse-grain chiasm within delimited
  pericopes (the form scholars actually argue) is untested and would be *confirmatory*, not discovery.
- The iltifāt detector (Lens 7) is **referent-blind** and uses an ~81% heuristic tagger; the *wazn*
  classifier (Lens 8) is a coarse 9-bucket consonantal heuristic. Both measure proportions, not parses.
- Prosody and any recited-layer claim are data-blocked, as above.

None of these caveats is hidden in the numbers: every detector carries a synthetic positive control, a
degradation ladder, an ordinary-text negative, and a permutation/bootstrap null, so each verdict —
including each null, and the one positive — is a statement about an *instrument of known sensitivity*.

---

*This paper orients the reader to what has been looked at and why. For the measurements themselves see
`EVIDENCE.md`; for the integrated argument see `MASTERY_REPORT.md`; for the remaining forks see
`HANDOFF_MASTERY.md`.*
