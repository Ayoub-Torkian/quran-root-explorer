# DESIGN OF EXPERIMENTS — the REARRANGEMENT / ORDERING program

Live experiment matrix for the rearrangement lens family (user-mandated as first-class). Companion to
IDEA_SIGNALS_GEOMETRY.md §9 (method register) and DESIGN_STANCE.md (gates). Divinely-rooted only
(rasm / roots / words / canonical order; NO ḥarakāt). Everything here is gated: permutation/structure-
preserving null at the SAME scale, equal-N, comparator where cross-text; "allowed-practice" reorderings
(nuzūl, Nöldeke) reported ALONGSIDE the random null, never instead of it.

## LOCKED PROTOCOL — rearrangement is part of EVERY experiment (user-mandated)
For any test, rearrangement is a built-in step, not an afterthought:
1. Run the BASELINE statistic.
2. Run it under REARRANGEMENT variants (alternative orderings/scales/ordering-mechanisms + the matching nulls).
3. If the baseline is NULL → before filing it, check whether a rearrangement (different scale, ordering
   mechanism, or order-aware metric) changes the result. A null is not filed until rearrangements are tried.
4. If any rearrangement looks PROMISING → try SEVERAL (multiple scales/mechanisms/metrics) and gate each.
This operationalizes "absence of evidence ≠ evidence of absence" through the rearrangement axis specifically.

## The two questions
- **(A) Is the actual ORDER special?** Compare the realized arrangement to legitimate alternatives and to a
  random null. (Done: #57 canonical adjacency; #58 seam-interlock canonical vs nuzūl.)
- **(B) How is recurring content RE-ARRANGED?** Quantify re-sequencing of passages that recur. (Partly: #42
  reorder ~0.45 proxy; to sharpen with edit-distance / Kendall / LCS.)

## Three axes of the matrix
**1) ORDERING MECHANISM** (what defines "position")
  m1 linear index (token/āyah/sūra)   m2 āyah-FINAL word as root/concept stream (fāṣila-concept; sound×meaning×order)
  m3 rhyme-class sequence   m4 root first-occurrence order   m5 frequency-rank order

**2) SCALE**
  s1 word/root within āyah   s2 āyah within sūra   s3 sūra within muṣḥaf   s4 cross-passage recurrence pairs

**3) METHOD** (IDEA §9)
  edit-distance / Smith-Waterman · LCS · Kendall τ / inversion / Spearman / RBO · genome-rearrangement
  (reversal/transposition/breakpoint) · DTW · optimal transport · permutation entropy (Bandt–Pompe) ·
  Moran's I / Geary's C / runs · Mantel test · block-permutation sensitivity (the multi-scale localizer)

## NULL / comparison discipline (every cell)
random permutation at the same scale (statistical null) + allowed-practice reorderings (nuzūl, Nöldeke;
comparison, not null) + cross-text comparator where applicable + equal-N + effect floor + positive-control.

## Prioritized experiment queue
- **E1 — Block-permutation sensitivity curve.** Apply one statistic (recurrence or adjacency cohesion) while
  rearranging at s1→s2→s3; the degradation curve localizes the scale where order matters. (Highest value:
  one figure that maps "where order lives.")
- **E2 — fāṣila-concept stream (m2).** Build the sequence of āyah-final roots; test autocorrelation /
  recurrence of the stream vs within-sūra shuffle, and vs the body-word stream. Does meaning chain at the
  verse-ends beyond rhyme? Multimodal (sound×meaning×order). NOVEL.
- **E3 — Edit-distance / Kendall on #42 recurrence pairs (s4).** Re-measure the Mūsā/Ibrāhīm/Nūḥ recurring
  passages with multi-grain (char/rasm, root, word) edit-distance + Kendall τ to quantify re-expression vs
  copying more sharply than the run-length/reorder proxy.
- **E4 — Mantel (position vs content) at s3.** corr(positional-distance, root-content-distance) over sūras,
  canonical vs nuzūl, permutation null. Generalizes #57/#58.
- **E5 — Permutation entropy of root/letter streams (m1, s1–s2)** vs comparators — ordinal complexity, a
  fresh order-complexity axis distinct from cosine/TF-IDF.

## Status
- DONE: #57 (Moran's I, canonical adjacency, length-controlled), #58 (seam-interlock, canonical vs nuzūl).
- DONE E2 (#60): fāṣila-concept stream → NEGATIVE for special hypothesis (verse-ends chain LEAST; start z=+17.6
  > random +10 > end +7.2). General adjacency continuity confirmed; rhyme decouples end-concept (Lens 3×16).
- DONE D3 (#59): group-cohesion generalization → muqaṭṭaʿāt content-cohesion is a GENERAL grouping effect; down-weighted.
- DONE E3 (#61): re-expression quantified (recurrence pairs cos 0.68, edit-sim 0.27). #62/#63 fāṣila system (Lens 17).
- DONE E1: coherence-length curve → order lives at the fine scale (~few āyāt); decays to baseline by ~lag 8–13. Sharpens #57.
- DONE wazn@fāṣila (re-open #41): register-level, shared w/ saj'; sharpens #63. D2 (#46 field-recurrence): still null.
- DONE E1-comparator: local coherence NOT distinctive (ord-Arabic ratio 1.82 > Qur'an 1.50) → tempered #57 to internal-only.
- DONE E4 (Mantel): position tracks content both orders (canonical r=+0.325 > nuzūl +0.290, p<1e-4); canonical favors GLOBAL grouping (reverses #58). Internal; length-gradient caveat.
REMAINING queue: E5 (permutation entropy); D1 (fusion of surviving positives — the big 'fuse modalities' capstone).
- RECORDED methods: IDEA_SIGNALS_GEOMETRY §7 (edit distance) + §9 (full register + ordering mechanisms).
- NEXT (recommended #59): E2 (fāṣila-concept stream) — novel, multimodal, divinely-rooted; then E1, E3.
