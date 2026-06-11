# Sequence-Scale Discovery Engine — Major Enhancement Plan

_Status: proposal, anchored by a verified proof-of-concept (2026-06-05)._
_Success criterion (user-defined): identify, extract, and PRESENT latent
features not already known. Discovery, not confirmation._

## 0. The diagnosis this plan answers

The app today is a superb **validator** (permutation/Poisson nulls, BH-FDR,
fixed seeds, length-confound discipline) sitting on **rich representations**
(network, matrix, spatial, signal, biology). What it lacks is a **generator**
of *unknown* structure: almost every method tests a pre-stated hypothesis, and
the only unsupervised tool is linear 2-way PPMI-SVD. To meet the success
criterion we add the missing middle — an unsupervised feature *generator* — and
route its candidates through the validator we already have.

We commit the generator to the **sequence (character) scale** as the primary
frontier. Rationale: the semantic/root scale rides a paved road (distributional
semantics, topic models, embeddings — heavily worked everywhere). The sequence
scale is an open frontier for THIS text, and it is the scale that the hard
sequence sciences were built for: genomics/-omics, information & communication
theory, music information retrieval, and speech/acoustic signal processing are
ALL sequence instantiations. Methods transfer in; nobody has aimed them here.

## 1. Verified proof-of-concept (already run on Book6.xlsx)

Mutual information between two symbols separated by distance d
(Lin & Tegmark 2017 criterion: natural/critical systems -> power-law decay;
Markov/IID -> exponential/zero), bias-corrected by subtracting a shuffle floor.

- Character scale (N=332,202 letters, alphabet 29): power-law decay,
  alpha = 1.71, log-log R^2 = 0.92; power-law beats exponential 0.92 vs 0.47.
  -> the letter stream is NOT a simple Markov/random source.
- Root scale (N=51,024, alphabet 1,701): power-law decay, alpha = 0.89,
  R^2 = 0.91, still ~0.025 bits excess at d=50.

This is a latent feature the app never computed: critical-like long-range order
at BOTH scales, with scale-dependent reach. It ran in <5 s, bias-corrected,
with a clean power-vs-exponential discriminator. It is the template for the
whole engine: representation -> estimator -> surrogate null -> fit/decision.

(Note the honest tension with the user's gut feeling: by raw MI the SEMANTIC
scale reached farther. That is fine — "more potential" is about the unexplored
method space and external linkages of the sequence scale, not today's effect
size. The sequence scale is where the un-traveled methods live.)

## 2. The enhancement in one line

A **Sequence-Scale Discovery Engine**: treat the Qur'anic letter stream as a
1-D symbolic signal, import the full toolkit of the sequence sciences to
*generate* candidate latent features, certify them against surrogate nulls +
BH-FDR, and present only survivors — each calibrated against physical-world
reference sequences (the literal "two books" linkage).

## 3. The discovery pipeline (every feature flows through this)

1. **Representation** — encode the stream (symbol series; numeric walk; spectral;
   block; graph-on-signal).
2. **Generator** — an unsupervised estimator that *emits candidates* (factors,
   modes, exponents, motifs), not a single pre-stated test.
3. **Estimator hygiene** — bias-correct (shuffle floor / Grassberger), report
   excess not raw, bootstrap CIs.
4. **Surrogate nulls** — not just shuffle: Markov-order-k surrogates (prove
   structure is beyond k-th order), phase-randomized surrogates (spectra),
   length/frequency-matched. Reuse `twobooks_stats.perm_p`.
5. **Multiplicity** — BH-FDR across the candidate battery
   (`twobooks_stats.benjamini_hochberg`).
6. **External calibration** — compare every signature to reference sequences
   (DNA, Arabic prose, English, music-as-symbols, IID/Markov synthetic). This
   is what turns a number into a *claim about the physical world*.

## 4. Method phases (each imports from a sequence science)

### Phase 1 — "Sequence Lab" (shippable first slice)
- MI(d) decay  [DONE — genomics/info theory]
- Block-entropy scaling: entropy rate h and excess entropy E
  (predictive information / "effective memory") — info theory.
- Detrended Fluctuation Analysis (DFA) long-range-correlation exponent on a
  principled symbol->numeric walk; robustness across encodings — physics/-omics.
- Compression complexity (LZ77 ratio) as a model-free entropy proxy that
  cross-checks Shannon — info/communication theory.
All vs shuffle + Markov-k surrogates, all with a reference-corpus column.

### Phase 2 — Communication / transmission view
- Source-coding / redundancy and channel-style capacity of the letter stream.
- Markov-order model selection done honestly at the small alphabet (AIC/BIC),
  where the root alphabet could not support it.
- Predictive-coding: how many bits of the next symbol are predictable from a
  context window of length L (the predictability curve).

### Phase 3 — Music / speech view (the corpus as cadence)
- Verse-length and fawasil (ayah-final) series as rhythm/meter signals:
  onset/segmentation, beat-spectrum, recurrence plots.
- Cepstral / spectral-envelope features of the per-sura entropy series.
- Self-similarity matrices to surface repeated "phrases" (parallel passages)
  at the sequence scale — complements the planned Needleman-Wunsch on roots.

### Phase 4 — Cross-scale coupling (highest novelty, after the spine is solid)
- Phonosemantic Mantel test: char-composition distance vs PPMI-SVD distance.
- Consonant-slot tensor (the literal codon table): does the meaning load sit on
  particular consonant positions, like the genetic code's wobble base?
- Biconsonantal-etymon test: shared 2-letter cores predicting shared meaning.

## 5. The "two books" calibration harness (build once, in the kernel)
A reference-sequence module that ships alongside the engine: bundled symbol
streams for a DNA segment, an Arabic non-Quranic prose sample, an English
sample, a music-pitch sequence, and synthetic IID/Markov controls. Every
sequence-scale signature is reported as a ROW in a comparison table:
`signature | Qur'an | DNA | Arabic prose | English | music | IID | Markov-2`.
This operationalizes "linking language to the physical world": claims become
calibrated, never asserted in a vacuum.

## 6. UI: evolve the information architecture; do NOT rewrite

A full rebuild is unwarranted — the analytical engine is sound. But the nav is
feature-accreted (4 groups, 20+ pages) and the home screen's loud register
(pulsing red boxes, ALL-CAPS) visually resembles the pseudo-science sites this
project's rigor is meant to rise above. Recommended changes, scoped:

1. **Two-scale spine.** Reorganize the nav around the conceptual axes the work
   now has: SEQUENCE (character) vs SEMANTIC (root), each x method-lens
   (signal / matrix / network / tensor / spatial / topology), plus CROSS-SCALE.
   The pages mostly exist; this is regrouping + labels, not new code.
2. **A "Discovery" front door.** One entry point that runs the FDR-controlled
   candidate battery and presents surviving latent features ranked by surprise,
   each with a one-line "what it groups / what it does NOT mean" and a link to
   the drill-down page. This replaces the loud home as the first thing a user
   sees and directly serves the success criterion (present latent features).
3. **Calm the register.** Drop the pulsing/caps/red-alert styling for a sober
   scholarly look — credibility is the product.
4. Keep all existing pages as drill-downs behind discovery results.

Effort: IA regroup + new discovery page + restyle. Evolutionary, ~1 minor
version. No analytics rewrite.

## 7. Tested/verified protocol (acceptance gates per feature)
- Estimator validated on a synthetic stream with KNOWN answer (e.g. a generated
  power-law-MI source recovers its exponent within CI) before it touches the
  corpus.
- Two independent nulls (shuffle + Markov-k) agree on significance.
- Survives BH-FDR within its battery.
- Robust to the arbitrary choices it depends on (encoding, fit range) — reported
  as a sensitivity row, not hidden.
- Reproducible: fixed seed + exportable null distribution.
- `python audit_app.py` clean; `AppTest` passes on the new page.

## 8. Risks / honesty
- MI/entropy at large alphabets is bias-prone — mandatory bias correction +
  CIs (already applied in the PoC).
- DFA/Hurst depend on the symbol->number encoding — report across encodings.
- Power-law fits are easy to over-claim — always show the exponential alternative
  and the reference corpora.
- Topology / higher-order info (later) are high-novelty but hard to interpret —
  keep behind an "experimental" label.

## 9. Immediate next actions
1. Greenlight Phase 1 scope (the four sequence-scale signatures + reference
   harness) as the v1.4 headline.
2. Land the reference-corpus module in `twobooks_stats` (single source).
3. Build the "Sequence Lab" page (the four signatures, surrogate nulls,
   benchmark table) + the Discovery front-door stub.
4. Decide UI regroup now vs after Phase 1 (recommendation: regroup nav now,
   discovery page with Phase 1).

## 10. DE-RISKING RESULTS (verified 2026-06-05, before any build)

Full battery ran on the real letter stream (N=332,202, alphabet 29) in ~22 s.
All four Phase-1 signatures are now validated against controls AND show real
signal. The plan rests on tested ground, not assumptions.

(A) Estimator validation — IID control MI_excess = -0.0001 / +0.0000 / +0.00007
    at d=1/5/20. The bias-corrected estimator does NOT manufacture structure
    from randomness. PASS.

(B) THE decisive test — is the long-range order beyond low-order Markov?
    Compared real MI(d) to order-1/2/3 surrogates that match the stream's own
    short-range statistics:
      d=2: real 0.107  mk1 0.012  -> beyond order-1
      d=5: real 0.0153 mk2 0.0003 mk3 0.0031 -> ~5x above even Markov-3
      long-range mass (sum MI_excess, d>=5): real 0.0368 vs mk3 0.0049 = 7.5x
    The long-range structure is GENUINE, not an artifact of local letter
    correlations. PASS. (Honest magnitude note: the absolute long-range MI is
    small; the claim is "clearly beyond Markov", not "large".)

(C) Other Phase-1 signatures — all feasible, all show signal:
    - Block-entropy rate falls 4.09 -> 3.77 -> 3.28 -> 2.58 bits (real) vs flat
      4.09 -> 4.08 -> 4.04 (shuffled): strong intra-sequence memory. PASS.
    - DFA exponent 0.554 (freq encoding) / 0.580 (rank encoding) vs shuffled
      0.503: persistent long-range correlation, robust across encodings. PASS
      (modest persistence — report honestly).
    - gzip ratio 0.414 (real) vs 0.585 (shuffled) = 29% redundancy gain:
      unambiguous structure. PASS.

Verdict: Phase 1 is de-risked. The estimators are correct (controls clean), the
headline phenomenon survives the hardest null (beyond-Markov, 7.5x), and every
proposed signature produces measurable signal. Safe to initiate Phase 1.
Scripts: outputs/mi_decay_poc.py, outputs/seq_derisk.py (re-runnable).

## 11. Conceptual architecture — the landscape schema (organizing principle: integration / oneness)

The engine and the UI should both express one idea: the corpus is a single
integrated landscape, and every entity is described by the SAME small set of
primitives, each measurable at BOTH scales (sequence/character + semantic/root)
and ACROSS time — and the deepest question is whether the primitives COHERE.

Primitives (each a lens; each works at both scales; time is an axis on every one):
1. Position   — what appears WHERE: distribution, locus, archetype in the landscape.
2. Relation   — whom it sits WITH: co-occurrence, similarity, neighbourhood.
3. Communication — how information FLOWS to/from it. Symmetric: mutual information
   (relation strength). Directed: transfer entropy / directed information
   (who informs whom, with direction and lag). [the new primitive — moves us from
   static "relates to" to dynamic "communicates with"]
4. Cross-scale binding — how an entity's SEQUENCE form couples to its MEANING
   (phonosemantic; consonant-slot/codon).
5. World linkage — how its statistical signature compares to natural, biological,
   and human reference sequences (the two-books calibration): the text related to
   the physical world, to human language/speech/music, to other parts of creation.
6. Time — every lens above as a function of order/revelation: emergence, drift,
   trajectory, evolution. Time is built in, never a separate page.
7. Coherence / integration (the oneness layer) — do the lenses CONVERGE on the
   same structure? Measured as cross-lens consensus, total correlation /
   multi-information (how much the whole exceeds the sum of its parts), and
   FDR-surviving agreement across modalities. This is the empirical face of
   "integrated, coherent, interactive, evolving." The existing deep-dive
   consensus/divergence fusion is the seed; generalize it to a corpus-wide
   coherence measure and make it the product's front door.

Epistemic boundary (keep the house ethic): we can MEASURE and DESCRIBE position,
relation, information flow, cross-scale binding, world-resonance, temporal
evolution, and coherence. We do not convert these measurements into metaphysical
proof. The framework lets the structure speak; interpretation stays with the
reader. This honors the unifying vision AND the "description, not tafsir / no
scientific-miracle claims" discipline that gives the project its credibility.

UI consequence: the integration/coherence layer is literally what unifies today's
20 siloed pages into one coherent whole — so "oneness" is not just the subject
matter, it becomes the product's information architecture: a two-scale spine, a
coherence/discovery front door, every entity viewable through all seven lenses
across time.

## 12. TESTED VERDICT — sequence vs semantic emphasis (settled, not speculative)

Head-to-head on the real corpus (outputs/scale_adjudicate.py, ran in ~9 s).
"Discovery potential" defined as structure BEYOND the stream's own low-order
baseline, normalized by its own entropy so the alphabets are comparable.

  metric                              SEQUENCE/letters   SEMANTIC/roots
  alphabet K                                       29             1701
  stream length N                              332,202           51,024
  marginal entropy H1 (bits)                      4.09             8.44
  highest ESTIMABLE Markov order                     2                1
  near MI / H1   (d=1..4)                        0.121            0.177
  long-range MI / H1   (d>=5)                    0.009            0.056
  BEYOND own-Markov ratio (d>=5)                 69.7x            11.1x
  effective memory length (symbols)                  6               50
  compression redundancy %                        26.3             14.2

Reading (critical — where the data refines the instinct; both facts are assets, neither is grounds for dropping a scale):
- On raw information the SEMANTIC scale leads: ~6x more long-range information,
  memory ~8x farther (50 vs 6 symbols). That reach is an asset we keep and use.
- The sequence scale leads on three counts that matter for DISCOVERY (and are
  combined WITH, not instead of, the above):
  1. Surprise: 69.7x of the letter scale's long-range structure is UNEXPLAINED
     by its own low-order Markov model, vs only 11.1x for roots. The sequence
     scale's structure is far more latent/non-obvious relative to the trivial
     baseline — exactly the success criterion (features not already known).
  2. Tractability: only the letter alphabet supports rigorous HIGH-ORDER
     modelling (order>=2 estimable; roots cap at order 1 because 1701^2 >> N).
     Serious sequence science is only feasible at the character scale.
  3. Mineable redundancy + untrodden method transfer (-omics, info/communication
     theory, music, speech) — 26% vs 14% model-free redundancy.

DECISION (integration, not allocation): NOTHING IS DROPPED. Everything we have
is used and valued. The sequence scale is the BUILD substrate and entry point —
it is the tractable, surprising, untrodden one, so it is where the new engine is
grown. But the semantic scale, the network, spatial, biology, the deep dives,
and every existing page are RETAINED and woven in, each contributing its own
part to one coherent whole. This is not a contest between scales and not a
budget split; it is integration. Even small-magnitude signals keep their place
in the picture — completeness over pruning. The tested findings below are not a
basis for choosing one scale over another; they are two assets to combine:
sequence brings tractable, non-obvious structure; semantic brings reach and
significance.

This is the form/content principle applied to the method itself: the rigorous,
tractable substrate (sequence) carries the structure; the meaning-rich substrate
(semantic) carries the significance; the value is in their integration, not
either alone.

## 13. SUSTAINABILITY (a build constraint, not an afterthought)

The success criterion is worthless if the result can't be maintained. This
project's own history names the failure modes: stacked duplicate builders,
stats duplicated across pages, large-file edit truncation, 20+ accreted pages,
no committed test suite (only audit scripts + manual AppTest). The engine is
built to NOT repeat them.

1. Kernel-first, single source. Every sequence-scale estimator (MI, block
   entropy, DFA, LZ redundancy, Markov/IID surrogates, reference corpora) lives
   in ONE tested module (the twobooks_stats pattern, extended). Pages call it;
   they never re-implement. Results cannot drift between pages by construction.
2. Known-answer tests, committed. The controls already run today (IID -> ~0,
   Markov surrogate recovers, shuffled -> 0.5 DFA) become a real test/ suite —
   the first in the repo. Estimator hygiene is a contract: no signature ships
   until it passes its controls.
3. Reproducible by default. Fixed seeds (already the norm) + every reported
   p-value can export its null distribution. A number on screen is regenerable.
4. IA that evolves, not accretes. ONE discovery front door + existing pages as
   drill-downs, organized on the two-scale spine. Adding a new page per idea is
   the unsustainable path and is rejected.
5. Audit-gated releases. audit_app.py (nav/manifest/help drift) + AppTest stay
   in the loop; a signature is "done" only when both pass.
6. Decision log kept (this file). Tested decisions are not re-litigated without
   new evidence.

Form and content held together: robust, tested foundations (content) and a
calm, coherent, integrated interface (form) — balanced, interwoven, purposeful.
The artifact is meant to embody the same coherence it studies.
