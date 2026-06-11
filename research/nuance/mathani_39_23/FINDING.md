# مثاني (39:23) — "a Book... oft-repeated / paired": FINDING

CLAIM (operationalized): the revealed text contains more structured verse-level
repetition (near-twin verses) than a vocabulary/length-matched random text.

METHOD: each of 6,236 verses = its set of distinct roots (Book6). Near-twin = a verse
pair with set-Jaccard >= 0.50. Statistic T = count of near-twin pairs. Null (B=300) =
redraw each verse's roots, count preserved, weighted by root document-frequency
(destroys real phrasings, keeps vocabulary + lengths). Pre-registered.

RESULT
- T_observed = 3,523 near-twin pairs;  34.5% of verses have >=1 near-twin.
- Null = 2,118 +/- 216;  0 of 300 nulls reached observed.
- z = +6.5  (permutation p <= 0.0033 at B=300; parametric p ~ 1e-10).
- ratio obs/null = 1.66  ->  genuine structured excess ~ +66% (~1,405 pairs).

VERDICT: SUPPORTED but BOUNDED. Structured verse-repetition is real and robust.
BUT the null is the headline: ~60% of apparent "pairing" is a vocabulary/length
artifact; only ~40% (the +66% excess) is genuine structure. The text is measurably
more paired than chance — moderately, not overwhelmingly.

SCOPE / HONEST LIMITS
- DESCRIPTIVE, internal. NO claim the Qur'an repeats MORE than other Arabic (no comparator).
- Threshold 0.50 pre-stated; robustness sweep (0.40-0.80) and tf-cosine variant: TODO.
- Null is df-weighted independent draw; gold-standard degree-preserving curveball null: TODO.
- Secondary (do near-twins sit closer in canonical order than chance?): TODO.
- B=300 (program precedent); protocol's "p<0.001" needs B>=1000 (logged in results.json).
