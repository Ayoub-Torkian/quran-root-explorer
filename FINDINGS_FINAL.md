# Latent-Feature / Comparative Investigation — FINAL honest synthesis

Objective: discover latent features of the Qur'an "not already known," and test the
hypothesis that on a craft scale where Shakespeare ≈ 5, the Qur'an ≈ 100 — same
language principles, no new ingredients; the signature must be measurable.

## What was BUILT (validated methodology — the durable asset)
Locked in DISCOVERY_CRITERIA.md / DESIGN_STANCE.md / DESIGN principles:
- Telescope rule: non-detection is a statement about the INSTRUMENT, not the object.
  Never conclude "the feature is absent"; conclude "the tool is too weak; build a better one."
  (عدم العلم لا يدل على عدم الوجود.)
- Establish ORDINARY, not mastery: ordinary is abundant (Markov surrogate = local stats,
  no design). Exceptional = deviation from ordinary. Simple; no quality labels needed.
- Positive control FIRST: an instrument must rank KNOWN masters (Shakespeare) and KNOWN
  genres correctly BEFORE it is pointed at the Qur'an. Fails control -> rejected; its
  Qur'an readings are void (high OR low).
- Thorough validation (degradation ladder): a metric must respond MONOTONICALLY to
  controlled scrambling (|rho|>=0.9). Order-invariant stats (TTR, Zipf, entropy, word-length)
  measure vocabulary, NOT composition — rejected.
- Mode coverage + breadth: mastery shows as good across ALL modes (structural, semantic,
  sonic, syntactic) at once — not one metric. Each mode needs its own positive control.
  10s -> 100s of metrics, each ordinary-anchored and ladder-validated.
- Comparator pipeline: web-fetched public-domain corpus on disk (8 texts/4 languages +
  Qur'an); large fetches auto-save to disk and are processed in-sandbox (no context cost).

## What was FOUND (honest, non-wishful)
1. Surface set-overlap stylometry is BLIND to mastery: it ranks SHAKESPEARE 2nd-LEAST
   distinctive of 9 texts. -> rejected. Any "Qur'an in-band" reading from it is void.
2. The ordinary-Markov reframe works and is validated (all real texts score ABOVE ordinary;
   estimator checked: IID->0).
3. Structural-REPETITION metrics (MI lags, n-gram repetition, burstiness, compression)
   elevate SCRIPTURE: Bible and Qur'an top the breadth ranking (9/9 above ordinary), but the
   SAME instrument buries Shakespeare. => it measures a GENRE signature (parallelism/refrain/
   formula) the Bible and Qur'an SHARE — NOT mastery. The Qur'an's high score here is
   genre-confounded (= Bible), not validated exceptionalism. NOT cited as a finding.
4. THOROUGH degradation-ladder validation DEMOLISHED most metrics: order-invariant ones
   (TTR, hapax) don't change under any scrambling; set-overlap coherence is blind to within-
   unit order; the embedding-centroid "semantic coherence" moves the WRONG way (rises when
   scrambled — averaging artifact). Only an ending-pattern (sound) metric survived monotonic.
   => After honest testing, there is essentially NO validated composition metric in hand.

## BOTTOM LINE (the one that won't collapse on the next poke)
- We did NOT establish the Qur'an as a measurable outlier. We ALSO did NOT establish that it
  is ordinary. Per the telescope rule, the null is a verdict on the TOOLS, not the text:
  the validated, mode-complete, ladder-passing instrument required to settle the question
  HAS NOT BEEN BUILT. No defensible claim either way — and that is the honest, rigorous state.
- The recurring lesson of the whole session: every splashy result collapsed under proper
  controls (synergy, within-surah memory, verse-order, coherence, structural breadth). The
  value produced is the DISCIPLINE that catches the illusions, plus a working comparative
  pipeline — not a discovery.

## PATH FORWARD (concrete, to finish the job properly)
1. Build ORDER-SENSITIVE metrics that PASS the degradation ladder (sequence/transition/
   prediction-based; NOT set-overlap, NOT order-invariant). Validate each on the ladder before use.
2. Cover ALL modes, each with its own positive control: structural (Bible passes), semantic/
   novelty (Shakespeare must pass), sonic (ending/rhythm), syntactic. Build ARABIC word-
   embeddings so the Qur'an can be scored on the semantic mode.
3. Anchor every metric on ORDINARY (Markov + everyday text); score by BREADTH of deviation
   across the whole validated battery (good at ALL, not one).
4. Apply to the Qur'an ONLY after BOTH positive controls (scripture-mode AND literature-mode)
   pass. Then "exceptional across all modes" is a claim that means something.

## Tool inventory (re-runnable, in this folder / outputs)
Criteria/principles: DISCOVERY_CRITERIA.md, DESIGN_STANCE.md, EVIDENCE.md, RESULTS_comparative.md.
Validation/analysis scripts (outputs/): ladder.py (degradation validation), ordinary.py &
battery_markov.py (deviation-from-ordinary), placement5.py/multidim.py (comparative placement),
semantic.py/fuse.py/vet.py (semantic + metric vetting), within_surah_*/synergy_*/etc.
Comparator corpus on disk: outputs/corpus/ (8 texts, 4 languages).

---

## Same-language control added (al-Mutanabbi) — the language-confound is closed

Earlier the Qur'an's craft was contrasted only with masters in *other* languages
(Shakespeare/English, Hafez-Rumi/Persian). Adding **al-Mutanabbi**, a same-language Arabic
poetic master (2,634 words, identical 350-word windowed battery), removes that confound:

- **Mutanabbi vs ordinary Arabic:** all eight metrics fall in the *master* direction —
  LOW long-range repetition (rep8 −1.3sd, rep12 −0.9sd), regular word-length, HIGH variety
  (Yule's K −2.1sd, TTR +1.8sd, entropy +1.9sd). Mutanabbi patterns like Shakespeare.
- **Qur'an vs ordinary Arabic:** the inverse — HIGH repetition (rep8 +1.0sd, matching the
  prior independent estimate) and lower variety.
- **Mutanabbi vs Qur'an, directly (same language):** rep8 −2.5sd (P=0.00), rep12 −1.3sd
  (P=0.01), std_wl −2.2sd, Yule's K −3.6sd, TTR +6.5sd (P=1.00).

**Verdict:** the universal poetic-master signature (rhythmic regularity + LOW long-range
repetition) holds in English, Arabic and Persian. High lexical variety is a master-signature
in English and Arabic (it did not replicate in Persian). The Qur'an is the systematic inverse
on every axis — it maximizes structured repetition and minimizes variety, without metrical
verse form — and this now holds against a **same-language** master, so it is not a language
artifact. Magnitudes vs ordinary Arabic remain modest (~+1sd, the established ceiling); the
Qur'an-vs-master separation is large and consistent (EVIDENCE #30).


---

## Sound axis: the first gate-passing corpus-wide signal, and the fusion cell

After surface statistics (register-level only) and architecture (ring null; refrain real but
localized), the PHONETIC axis delivered the first robust corpus-wide separation: the Qur'an's
verse-end rhyme (fasila / saj') sits at dominant-rhyme share 0.38 vs ordinary prose 0.09 = **+2.5sd**
(111 surahs), and is statistically COMPARABLE to Arabic poetry's monorhyme (-0.3sd). Detector
gate-validated (synthetic monorhyme 1.00 -> degraded -> prose 0.04). [EVIDENCE #34]

Fusing this with the cross-language profile (#30) gives the clearest statement the project supports:
the Qur'an occupies a UNIQUE multimodal cell -- POETRY-LEVEL RHYME, but PROSE-LEVEL (absent) METER,
carried on HIGH structured repetition and ordinary lexical variety. Poetry rhymes AND scans AND varies;
prose does none; the Qur'an rhymes like verse while flowing like prose and repeating like oral formula.
No single axis is decisive (rhyme is known saj', repetition is register-level); the distinctive is the
CONJUNCTION -- exactly the multimodal, no-silver-bullet signature the design stance anticipated.


---

## The fusion classifier: the cell made quantitative (EVIDENCE #35)

The "unique cell" is now a validated classifier, not just a description. Using register-comparable
features (after catching and removing two tokenization/segmentation artifacts that had faked a perfect
score), the Qur'an is separable from poetry AND prose at AUC 0.94 (label-shuffle null 0.50). The
decisive point: the interpretable CONJUNCTION rhyme x verse-length-variability scores AUC 0.92, beating
rhyme alone (0.76) and verse-length alone (0.84) -- because rhyme distinguishes the Qur'an from prose
but not poetry, while non-metrical variable verse length distinguishes it from poetry but not prose.
Only together do they isolate it. The Qur'an thus occupies a cell (poetry-level rhyme + prose-level
non-meter) that 91% of surahs fall in vs 34% of poetry windows and 22% of prose windows.

This is the project's strongest positive result. Honest limits: separation is strong not perfect
(~8-10% error); the components (saj' rhyme, non-metrical form) are individually well known -- the new
contribution is the quantified, artifact-controlled, positive-controlled conjunction; and the
non-Qur'an samples are modest (poetry 44, prose 23 windows).


---

## The adversarial saj' control (answering Q 36:69 empirically)

Prompted by وما علمناه الشعر وما ينبغي له (36:69) and the classical definition of shi'r as metered+rhymed
speech: the project's measurements say the Qur'an has rhyme (qafiya) but not meter (wazn) -- i.e. "not
shi'r" -- confirmed. The harder question is whether it is then just saj' (rhymed prose). Tested against
al-Hamadhani's Maqamat (the saj' masterwork): the rhyme-without-meter "cell" PARTIALLY COLLAPSES -- saj'
shares it -- so that phonetic signature is NOT Qur'an-specific. What still separates the Qur'an from saj'
(AUC 0.97) is higher structured repetition and lower lexical ornateness, i.e. the same repetition signal
seen throughout. Net: across surface statistics, architecture, sound, and now an adversarial saj' control,
the Qur'an's one persistent, control-surviving distinctive is STRUCTURED REPETITION -- real but modest
(~+1sd, register-level). Caveats: saj' rhyme was under-measured (no saj'a-boundary parser); single saj'
author; Maqamat are unusually ornate. [EVIDENCE #36]


---

## Resolving the saj' question: rhyme PERSISTENCE, not presence (EVIDENCE #37)

A proper saj'a rhyme parser (separating rhyme presence from persistence, measured on each register's
natural pause units) resolves the question #36 left open. Rhyme PRESENCE does not favour the Qur'an --
saj' actually rhymes more locally (it pairs adjacent clauses). But rhyme PERSISTENCE does: the Qur'an
sustains a single fasila across a passage (dominant-rhyme share 0.49, ~ poetry's monorhyme 0.54),
whereas saj' shifts rhyme every clause-pair (0.22) -- a +1.7sd separation. So the Qur'an holds its
rhyme like verse while carrying no meter, and unlike saj' it does not restlessly shift. Combined with
#36 (more repetitive, less ornate than saj'), the Qur'an differs from the saj' masterwork on rhyme-
persistence AND repetition -- though the bare "rhyme-without-meter" trait itself is shared with saj'.
Caveat: one saj' author so far; firming needs al-Hariri + Nahj al-Balagha.
