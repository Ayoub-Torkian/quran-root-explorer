# IDEA — Āyah-as-Signal · Point/Area/Volume Patterns · Linear-Algebra Geometry

**Status: RECORDED, prelim-tested, PARKED in refined form (naive form fails the gate).**
Origin: user intuition, session post-#45. Do not add coverage credit until a refined version clears G10.

---

## 1. The intuition (kept verbatim in spirit)

*Āyah* literally means **"sign."** Divine naming of verses as signs is itself an indication that
the units are signal-bearing — we cannot bypass that framing. A signal can be 1D, 2D, …:
- **Point patterns** — where a character (or a few characters concurrently) occurs along the
  corpus index; compare the patterns.
- **Root point patterns** — same, at root grain.
- **Area / image** — a combination of signals as a matrix/image; a set of vectors.
- **Vector / direction** — an āyah (or a set of āyāt) as a vector, i.e. a *direction*.
- **All of linear algebra in play** — transformation, decomposition (SVD/PCA), collinearity, subspace.

**Companion framing (user, same session):** this is the same family as the **pointer** ideas.
A *concept* is an umbrella / surrogate — a label that points to a distributed signal (other
ideas, other signals). The space is therefore **open-ended, with infinite evolution and
emergence potential.** That richness is the value *and* the hazard (see §5).

---

## 2. Why it is principled (not a stretch)

- The **disjoint-letters / pointer** thread already found a *real* position signal
  (muqaṭṭaʿāt bearer enrichment, label-permutation **p ≈ 2×10⁻⁵**, LOO-robust). That is a
  point/position pattern tied to a *specific hypothesis* that survived. So the signal frame
  has already produced one of the project's cleaner wins.
- It is the natural home of the **Position (index geometry)** scale already shipped in v1.3.

## 3. Preliminary test (this session) — `sequence_tests/signals_geom_prelim.py`

Three probes, each with a permutation null and ordinary-Arabic comparators (news, novel,
classical, Ṭabarī):
- **Q1 point-pattern clustering** — Fano factor (index of dispersion) of inter-occurrence
  gaps per letter, vs position-permutation null.
- **Q2 bivariate co-location** — windowed count-correlation of two letters, vs shuffle.
- **Q3 vector/area** — āyah-window × letter matrix, leading-SVD energy share, vs column-shuffle.

### Result — HONEST NEGATIVE on the naive form
At full length the Qur'an looked spectacular (alef Fano z = **−24**, SVD z = **+51**). But the
Qur'an stream is 171k letters vs comparators' 3–20k, and these z-magnitudes **grow with N**.
**Re-run at equal-N (3,107 letters):** alef z = **−3.6** — squarely in the comparator pack
(−2.6 to −5.9); SVD edge evaporates. Only *lam* point-pattern stayed mildly distinctive
(**+1.1sd**, others negative) — sub-2sd, register-level.

**Verdict:** the naive univariate point-pattern / generic-SVD instantiation is an **N-confound
artifact** — the exact #18–22 trap. It does **not** clear the G10 gate. Killing the naive
version is itself a useful result.

## 4. What survives the critique (the refined directions worth pipelining)

The idea is **not** dead — only the generic instantiation is. Survivable, gate-shaped versions:
1. **Hypothesis-anchored point patterns** (like disjoint-letters did) — a *specific* claim with
   a built-in positive control, not generic clustering. Highest proven yield.
2. **Bivariate / multivariate co-location at strict equal-N** — Q2 hinted (Qur'an لن z=−7.9)
   but was N-confounded; redo equal-N with bootstrap CIs and a same-language baseline.
3. **Vector/direction geometry** — āyah-as-vector angles, subspace/decomposition, collinearity
   — but only against **length-matched** nulls and comparators (length is the dominant confound).
4. **Root-grain** versions of all three (roots ≈ codons) to connect to the Semantic scale.
5. **Wavelet analysis** (user, same session) — *strong fit.* The Signal page already has FFT,
   but FFT is **global**: it cannot say *where* a rhythm lives. Wavelets are **scale-localized**,
   so they can detect structure that is periodic in one region and not another — exactly the
   profile of the Qur'an's **localized refrains** (#33: ar-Raḥmān/Mursalāt real but local) and
   of varied recurrence (#42). Plan: continuous wavelet transform (Morlet, `pywt`)
   of a 1D signal (verse-length series, or a letter/root indicator), then a **wavelet-power
   intermittency vs a phase-randomized null**, equal-N, comparator-checked. This is the
   most promising *method* on the list because it targets locality, where the corpus's only
   surviving repetition signal actually lives. Same guardrails (§5) apply.

   **PRELIM RESULT (this session) — `sequence_tests/wavelet_prelim.py`, the lead candidate.**
   Signal = letters-per-āyah (Qur'an) / per-sentence (comparators). Statistic = mean-over-scales
   wavelet-power intermittency; null = phase-randomized surrogate (same spectrum, no locality);
   equal-N. **Unlike the naive point-pattern, this SURVIVES equal-N:**

   | corpus | locality-z (equal-N=188) |
   |---|---|
   | **QUR'AN** | **+2.35** (real locality beyond its own spectrum) |
   | ar_novel (ordinary) | −1.16 (none) |
   | ar_poetry (Mutanabbi) | −1.00 (none) |
   | ar_sajprose (saj') | +0.65 (mild) |

   Reproducible across slices/seeds; at a larger N=477 (saj'+poetry only) saj' rose to +3.47 —
   i.e. **saj' is the one genre that can match/exceed**, exactly as the rhyme/refrain prior (#33)
   predicts. So: a genuine, equal-N-surviving locality signal, NOT unique-in-kind (saj' shares it).
   **CAVEAT (must clear before fusion):** verse-length partly encodes saj'/rhyme, so this may be
   re-detecting #33's localized refrains rather than a new axis — prove independence (residualize
   on rhyme/refrain, and try non-length signal formulations: root-novelty, semantic-field) first.

   **GATE RESULT (this session) — `sequence_tests/wavelet_indep.py`-style, /tmp/wav2.py. NO CREDIT.**
   Two checks, equal-N=188, phase-randomized null:

   | signal | QUR'AN | ar_novel | ar_poetry | ar_sajprose |
   |---|---|---|---|---|
   | baseline raw length | **+2.35** | −1.16 | −1.00 | +0.65 |
   | length residualized on rhyme-ending (project out #33) | **+1.37** | −1.35 | +0.98 | **+2.04** |
   | lexical-novelty (non-length, content) | **+0.37** | +1.66 | +1.75 | +0.05 |

   - **Independence FAILS:** masking the rhyme/fāṣila class collapses Qur'an 2.35→1.37 (sub-2sd),
     and saj' now exceeds it (2.04). Most of the locality WAS the #33 rhyme/refrain axis; the
     residual is only register-level.
   - **2nd formulation FAILS:** on content-novelty the Qur'an is null (0.37) and BELOW ordinary
     prose/poetry — the effect is length-channel-specific, does not generalize.
   - **Disposition: DEMOTED. Wavelet-on-length earns NO coverage credit — it is largely #33 seen
     through the length channel.** This is a clean negative (the gate + masking did their job).
   - **Still OPEN (telescope rule, not closed):** the *method* stays in the register; untested
     formulations remain — root-grain signals, masked/subspace signals, 2D area/image, semantic-
     field signals. A null here indicts THIS formulation, not the wavelet/signal idea.

## 5. Methodological guardrail (because the space is infinite)

The user's own observation — concepts are umbrellas, the space has infinite emergence — is
precisely **why discipline is mandatory**. An unbounded hypothesis space is unfalsifiable
without:
- **Pre-registered statistic + null** before looking (no garden of forking paths).
- **Equal-N** always (this session's lesson, in red).
- **Positive-control gate** — the measure must separate a known master/control first.
- **Comparator-relative effect** (z vs same-language ordinary), never a raw within-Qur'an number.
Infinite generativity is an asset only when each spawned hypothesis is forced through this gate.

## 6. Disposition

- **Recorded** here. **Parked** as a refined modality candidate ("signal-geometry / pointer
  lens"), NOT yet in the fusion pipeline and NOT credited in COVERAGE_MAP.html.
- **Promote to fusion** only if a refined direction (§4.1 or §4.2) clears 2sd at equal-N with
  a comparator. At that point it would join the **Position** scale and feed the per-āyah
  fusion vector (the shared-index hierarchy: bases→codons→proteins).
- Next scheduled work remains **modality #46 (lexical-semantic)**; this idea is queued behind it.

---

## 7. METHODS REGISTER — signal-geometry toolkit (PERMANENT; operationalize over time)

Standing instruction (user): keep ALL of the below in scope, never forget them, operationalize
each when suitable. Every tool below is admissible only through the §5 gate (equal-N + null +
comparator + positive-control). This is the *vocabulary* of the lens; formulation is the open work.

**Masking / filtering — TWO roles (both mandatory to keep in mind):**
1. *Mask as confound — "we don't see it because it's masked."* A dominant component (length,
   frequency, register, a known axis like rhyme) can HIDE a real signal. Operationalize: **partial
   it out / residualize / project onto its orthogonal complement**, then re-test the residual.
   → Immediate use: the wavelet locality lead must be tested *after projecting out the rhyme/refrain
     direction* (#33) to prove it is a new axis, not a re-detection.
2. *Mask as instrument — "we need a filter to see it."* Some structure is visible only inside a
   band/region/subspace. Operationalize: **band-pass (wavelet/Fourier), unit-masks (include only
   Meccan / only narrative / only a character's verses), feature-masks, attention weights**, then
   test within the masked view (with the mask declared in advance — no post-hoc mask fishing).

**Linear-algebra & geometry arsenal (each = a way to formulate or interrogate the signal):**
- **Vectors** — the āyah (or passage) as a feature vector; the shared-index fusion unit.
- **Signal combination** — stack/concatenate multi-scale features into one vector (fusion).
- **Transformation** — change of basis; Fourier (global), wavelet (local), normalization/whitening.
- **Translation (in vector space)** — centering, common-origin alignment across corpora; analogy
  geometry (v_a − v_b + v_c) for concept/pointer relations.
- **Decomposition** — SVD / PCA / ICA / NMF / eigendecomposition: find latent components / subspaces.
- **Projection & collinearity** — cosine/angle between units, project-out a known direction, test
  the orthogonal complement, detect collinear (redundant) axes.
- **Distance / metric** — Euclidean, Mahalanobis (whitened), cosine, geodesic on the unit manifold.
- **Filtering** — denoise/smooth, high/low/band-pass, scale-selective reconstruction (inverse CWT).
- **Edit distance / sequence alignment (user-flagged; the ORDER-aware complement to cosine).** Cosine and
  TF-IDF are bag-of-words — order-blind; Levenshtein / Smith-Waterman alignment is order-SENSITIVE. The
  *value* is precisely the gap between them: two recurring passages with the same content but re-sequenced
  show HIGH cosine yet HIGH edit distance — which is exactly the #42 "varied recurrence" finding (short
  verbatim runs ~2, high reorder ~0.45) operationalized directly. Multimodal use: compute it at MULTIPLE
  grains — character/rasm, root, morpheme, word — so the *profile across grains* becomes a feature (e.g.
  low char-edit + high word-edit = orthographic variants; high edit + high semantic cosine = re-expression).
  Local alignment (Smith-Waterman) reads off the longest shared run = a direct "verbatim-run" measure;
  normalized edit-similarity (1 − dist/maxlen) is a fusion axis alongside cosine and rhyme. Cost is O(n·m),
  so apply to candidate recurrence pairs, not all-pairs; length-normalize; gate as usual. NEXT CONCRETE USE:
  re-measure #42's recurring passages with multi-grain edit distance to quantify re-expression vs copying
  more sharply than the current run-length/reorder proxy.

**Pointer/surrogate framing (carried from earlier):** a concept (mercy, Mūsā, a disjoint letter,
cosmos, day/night, history) is an umbrella that *points to* a distributed signal. Operationalize a
pointer as a **mask + a vector**: the mask selects the units the concept tags; the vector is their
aggregated signal. Pointer-tests then become projection/decomposition tests on masked subspaces.

**Discipline reminder:** this toolkit is generative and unbounded — precisely why every spawned
test is pre-registered and gated. Telescope rule holds: non-detection indicts the tool, never
declares absence. Lack of evidence ≠ evidence of absence.

---

## 8. SUB-UNIT POSITIONAL / DIRECTIONAL LENS (user-mandated; VERIFIED viable, recorded)

**Principle (user, locked):** the āyah is an **inviolate divine unit** — never divided arbitrarily —
but we MAY study **sub-units** along a spectrum: **character → root → morphological token**. This
is a *positional / spatial* lens. The natural scan is **right-to-left** (how it is read,
semantically); the **reverse (or other) scan is allowed for pattern discovery**. Positional AND
directional views of the āyah — and their combinations — are a real methodology to operationalize
when useful.

**Verification (this session) — `sequence_tests/posdir_prelim.py`, equal-N=97, within-unit-shuffle null:**

| corpus | slope (len vs pos) | slope-z | argmax-pos |
|---|---|---|---|
| QUR'AN | 0.132 | 3.33 | 0.438 |
| ar_news | 0.121 | 3.77 | 0.491 |
| ar_novel | 0.159 | 3.99 | 0.512 |
| ar_poetry | 0.344 | 6.41 | 0.537 |
| ar_sajprose | 0.185 | 3.85 | 0.469 |

- **Lens is VIABLE:** sub-unit length rises toward the unit end in *every* corpus, null-significant
  (z 3.3–6.4) — a real, measurable positional structure (heavy-final cadence).
- **First feature NOT Qur'an-distinctive:** Qur'an slope 0.132 sits LOW; poetry leads (0.344). No claim.
- **Directionality is real but the demo was trivial:** the linear position-slope flips sign exactly
  under reversal (+0.147→−0.147) — antisymmetric by construction, so it shows direction-*sensitivity*
  only, not hidden directional structure. A genuine directional probe needs a **non-antisymmetric**
  statistic (forward vs backward predictive entropy; triplet up/down asymmetry) — QUEUED.

**Disposition:** methodology RECORDED and validated as operational; **NO coverage credit** (first
feature null for the Qur'an). To pursue: (a) the sub-unit spectrum at **root / morphological-token**
grain (corpus has `COL_SEGMENTED` morph tokens — Qur'an-internal; needs a segmented comparator for
cross-text), (b) **genuine directional statistics** (non-antisymmetric), (c) positional profiles of
*specific* features (rare roots, morphological categories) rather than raw length. Telescope rule:
this null indicts the chosen feature, not the positional/directional lens.

**FOLLOW-UP #48 (this session) — genuine directional statistic + root-grain positional. `directional48.py`.**
Closes items (b) and (c) above.
- **(b) Directional time-irreversibility** (signed skew of within-unit increment series — flips SIGN under
  reversal, dies under shuffle, so a *real* directional measure unlike the trivial position-slope flip):
  all corpora mildly negative; poetry z=−2.06, saj' −1.80 show it most; the **QUR'AN is the LEAST
  directional** (−0.054, z=−1.23). NOT distinctive, sub-2σ. Directional lens = real but Qur'an-null.
- **(c) Root-rarity vs position** (Qur'an-internal, shuffle null): **+0.072, z=+13.4 — rarer roots sit
  toward the āyah END (fāṣila).** Strong & significant, BUT Qur'an-internal only (comparators lack roots)
  and CONFOUNDED by generic Arabic word order (particles-first / content-later) and the rhyme position
  (Lens 3). A real internal gradient, NOT a distinctiveness claim.
- **Disposition:** NO coverage credit. Directional sub-unit lens = Qur'an-null. Root-rarity gradient =
  noted internal structure, PARKED pending a root/morph-annotated comparator + rhyme-residual. EVIDENCE #48.

---

## 9. REARRANGEMENT — a first-class lens family (multi-scale, multi-method; user-mandated)

Two senses, both in scope: **(A) rearrangement of UNITS as comparison/null** — is the actual order
special? canonical vs nuzūl vs alternative chronologies vs random (cf. #57, #58); and **(B) rearrangement
WITHIN recurrence** — how is a recurring passage re-sequenced? (cf. #42 reorder ~0.45). Edit distance is
ONE defensible method; the full defensible set:

**Order-comparison metrics (between two sequences/orderings):**
- **Edit distance (Levenshtein) / Smith-Waterman local alignment** — order-aware similarity; SW reads off
  verbatim runs. (See §7.)
- **Longest Common Subsequence (LCS)** — order-preserving shared content; LCS/len = preserved-order fraction.
- **Kendall's τ / Kendall distance (inversion count)** — the canonical "how reordered" metric for shared
  items; Spearman ρ as the rank-correlation cousin; **rank-biased overlap (RBO)** for top-weighted orders.
- **Genome-rearrangement distances (reversal / transposition / breakpoint distance)** — from comp-bio;
  apt under our genome metaphor (roots≈codons): how many reversals/transpositions convert one order to another.
- **Dynamic Time Warping** — alignment allowing local stretch (multi-scale via window); **optimal transport /
  earth-mover's distance** — mass to move one positional distribution into another.

**Sequence-internal order/complexity:**
- **Permutation entropy (Bandt–Pompe)** — ordinal-pattern complexity at embedding dim m (multi-scale by m,τ).
- **Moran's I / Geary's C / autocorrelation / runs tests** — positional dependence (Moran used in #57).

**Arrangement-vs-content association:**
- **Mantel test** — corr(positional-distance matrix, content-distance matrix) + permutation null; does
  arrangement track content at a chosen scale?
- **Block-permutation sensitivity** — the key MULTI-SCALE method: rearrange at increasing granularity and
  profile how a statistic degrades; the degradation curve localizes the scale at which order matters.

**Scales (apply each method at each):** (1) word/root within āyah · (2) āyah within sūra · (3) sūra within
muṣḥaf (canonical vs nuzūl vs Nöldeke vs random) · (4) cross-passage recurrence pairs (#42 re-expression).

**ORDERING MECHANISMS — what defines "position" (user-mandated; multiple, not just linear index):**
- linear token/āyah/sūra index (the default).
- **āyah-FINAL word as an ordering stream** — the sequence of verse-final words, taken as their ROOT or
  CONCEPT, is its own derived ordering. The fāṣila already carries rhyme (sound); its root/concept carries
  meaning; the SEQUENCE of fāṣila-concepts down a sūra/corpus is a multimodal signal fusing sound × meaning
  × order. Tests: autocorrelation of the fāṣila-concept stream (do consecutive verse-ends form a semantic
  chain beyond shuffle?); recurrence of fāṣila-concepts; rearrangement metrics on this stream vs the body.
- other derived orderings: rhyme-class sequence; root first-occurrence order; frequency-rank order.
Each ordering mechanism is a distinct lens; the same rearrangement methods apply to each, with its own null.

**Discipline:** every rearrangement claim needs the permutation/structure-preserving null at the SAME scale,
equal-N, comparator where cross-text. "Allowed-practice" reorderings (nuzūl, alternative chronologies) are
legitimate *comparison* orderings — report them ALONGSIDE the random null, not instead of it (cf. #58).
