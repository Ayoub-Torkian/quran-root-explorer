# Probe: مثاني (39:23) — "a Book... oft-repeated / paired" (PRE-REGISTERED, frozen)
Frozen 2026-06-08, BEFORE running. Revealed-layer only; no comparators, no external data.

## Claim (operationalized)
39:23 calls the text *mathani* (paired / oft-repeated). Testable structural reading:
the revealed text contains MORE structured verse-level repetition (near-twin verses
that recur in paired phrasing) than a vocabulary-matched random text would.

## Data
Book6 ayah-level roots (COL_ROOTS). Each verse = its SET of distinct roots. 6236 verses.

## Similarity
set-Jaccard(i,j) = |Ri ∩ Rj| / |Ri ∪ Rj|. A pair is a "near-twin" if Jaccard >= 0.50
(primary, pre-stated). Self-pairs excluded. (Robustness: also report sweep 0.40..0.80
and a tf-cosine variant — descriptive, not the gate.)

## Primary statistic
T = number of unordered near-twin pairs (Jaccard >= 0.50) in the whole corpus.
Secondary S = fraction of verses with >= 1 near-twin partner.

## Null (degree/frequency-matched scramble), B = 300
Per verse, keep its distinct-root COUNT k_i; redraw k_i distinct roots weighted by each
root's document frequency (verses it appears in). Preserves verse-length distribution and
root popularity; destroys genuine repeated phrasings. Recompute T on each null draw.
(Gold-standard follow-up if positive: degree-preserving bipartite swap/curveball null.)

## Inference + decision (frozen)
z = (T_obs - mean(T_null)) / sd(T_null); permutation p = (#null >= obs + 1)/(B+1).
A. EXISTS: T_obs > null with p < 0.001  -> "structured verse-repetition is real, beyond
   vocabulary chance"; report magnitude T_obs and ratio T_obs/mean(null).
B. If not -> honest null: the 'paired' claim is not supported at verse-Jaccard level.
SCOPE (stated up front): this is a DESCRIPTIVE internal measure. It does NOT claim the
Qur'an repeats MORE than other Arabic texts (no comparator) — only that its repetition is
structured, not a vocabulary artifact.

## Secondary (arrangement, reported separately)
Are near-twin partners closer in canonical order than chance? median |pos_i - pos_j| of
near-twin pairs vs an order-shuffle null. Tests positional pairing, not amount.
