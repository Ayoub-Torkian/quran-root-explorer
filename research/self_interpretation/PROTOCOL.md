# Self-Interpretation Canon — Pilot Validation Protocol v2 (PRE-REGISTERED)

Frozen on first filled `links` cell. v2 = evidence-based (no judgment bar). 2026-06-08.

## Question
Does the app's gated echo engine (root tf-idf cosine, deep_dive.py) recover the
intra-Qur'anic cross-references of classical tafsir al-Qur'an bi-l-Qur'an?

## Ground truth (TWO independent sources — needed to measure the human ceiling)
- GT1: al-Shinqiti, *Adwa' al-Bayan*.
- GT2: a second independent classical cross-reference source (al-Suyuti / Ibn Kathir
  internal citations). Same 152 verses. Separate per-verse sidecars (NOT a Book6 column).

## Sample (frozen)
152 verses, stratified 38 each across {Meccan,Medinan}x{short,long} (len median=7 words),
seed=42. File: sample_150.csv.

## Metric — rank-based, built-in null (no arbitrary threshold)
PRIMARY = rank-AUC(v) = P(engine ranks a true link of v above a random non-link of v),
over the engine's full 6235-verse ranking. Null = 0.50 exactly. Also report median rank
of true links (chance ~3118) and recall@{5,10,20} for interpretability only.

## The human ceiling (this is what replaces a guessed bar)
C = two-scholar agreement on the same verses: rank-AUC of GT2 links scored by GT1-style
overlap, and mutual recall GT1<->GT2. C is the empirical ceiling; no algorithm is expected
to beat it. Report engine as a FRACTION of C.

## Pre-registered decision criteria (FROZEN)
A. SIGNAL (gate to claim anything): engine rank-AUC > 0.50, permutation p < 0.001.
B. UTILITY (gate to call it a recovered canon): engine rank-AUC >= 0.70 * C
   (i.e. recovers >=70% of the two-scholar ceiling).
Decision: A&B -> scale + ship as recovered canon (report AUC and AUC/C).
          A only -> ship as "suggested links," reconsider matcher (lemma/semantic).
          not A -> kill; file honest null.

## If two sources are infeasible (cost fallback)
Annotate GT1 only; double-annotate >=20 verses to estimate annotator-noise AUC as a weaker
ceiling proxy; keep gate A (bar-free) as the real test; mark gate B "ceiling unmeasured."

## Annotation rules
Links verse-level (sura:ayah); expand ranges; exclude self; record source vol/section.
