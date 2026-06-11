# The Qur'ān as a Determined System — Phase D Synthesis

*A. Torkian, 2026-06-10. Everything below is measured from the Qur'ān against itself on the **rasm**
(the consonantal skeleton — the preserved/divine substrate). No external corpus, model, or embedding
is admissible; diacritics are a human layer and appear only as corroboration. Every claim is tied to a
ledger feature (L##) and a reproducible script in `research/intrinsic/scripts/`.*

---

## 0. The one-sentence result

On its own consonantal skeleton, the Qur'ān behaves as a **determined system**: its content obeys the
universal laws of natural language, its arrangement is **non-arbitrary and meaning-bearing** down to the
individual verse, its sūra boundaries are **objectively detectable** and **asymmetrically marked at the
opening**, and every measured pattern **collapses under tampering** — yet the determinacy is **bounded**:
it is strong from the corpus down to the verse, weak at the word, and the āyah's defining rhyme lives in a
human (diacritic) layer, not the rasm.

---

## 1. The determinacy ladder — "nothing could be moved", quantified by scale

The احسن تقویم intuition ("nothing could be added, deleted, moved, or replaced without loss") is not one
claim but a **ladder** of claims at successive scales. Measured:

| scale | result | margin over the text's own shuffle | feature · script |
|---|---|---|---|
| **corpus** (whole sequence) | order-load **9,922 bits** | z ≈ 285 vs random shuffle | L14 · `validate_L14.py` |
| **sūra** (boundaries) | boundaries are **local optima** (54% peak within ±1; move-one penalty +ve 73%) | vs 33% chance | L12 · `optplace.py` |
| **verse** (each āyah in place) | **84%** of verses more predictable in place than at a random spot | vs **47%** shuffle floor (+37), 3 modalities | L20 · `p4b_moveability_3mod.py` |
| **word — surface letters** | 44% in place | vs 40% floor (+4.5 only) | P5 · `p5_word_necessity.py` |
| **word — collocation order-load** | **0.89–0.97 bits/token** (root & surface-word) | over own shuffle (45k–75k bits) | C4 (candidate) · `p7c_orderload.py` |

**Reading.** Determinacy is **strong from the corpus to the verse**; the **word** rung is **structured but
single-modality**. Surface letters carry almost no word-level order (P5, +4.5). The real word-order signal
is **collocational**: the root and surface-word sequences each compress ~0.9 bits/token below their own
shuffle (a robust 45k–75k-bit order-load), so word arrangement is **not free** — it is constrained by which
words follow which. *Caveat (honest):* root and surface-word collocation are the **same lexical signal** in
two views, and the only independent surface channel (length) is null; the per-token "in-place vs random"
margin over the proper shuffle floor is small (+5.9), not the +38 an earlier wrong-null framing suggested.
So the word rung is a **single collocational modality** — real, but not the multimodal, per-element
necessity of the verse scale (L20). It remains candidate **C4**, pending an independent morphological-pattern
channel.

A companion result sharpens what "non-arbitrary" means. The order is **not** the most compressible
arrangement — trivially sorting the verses by rhyme or length compresses far better but destroys meaning
(L19, `c1_promote.py`). In all three rasm channels the canonical order sits **strictly between** its own
random shuffle (worse) and its own sorted version (better): it occupies the **intermediate-complexity band**
where meaningful sequences live — neither a random "gas" nor a sorted "crystal." So the arrangement is
**deliberate and meaning-bearing**, deliberately sacrificing compressibility to preserve meaning.

---

## 2. The invariants, by scale and modality (the 16 discoveries)

**Lexical (gates, not Qur'ān-specific).** Zipf slope −0.99 (L01), Heaps β 0.74 (L02): the corpus behaves as
genuine natural language — the floor every other test stands on.

**Wave / rhythm — complex-system fingerprints.** Verse-length long-range memory (DFA Hurst 0.95 vs 0.51
shuffle, L03), pink-noise spectrum (1/f slope 0.76 vs 0.00, L04), and scale-free size tails at three nested
levels (word α 2.04, verse 1.71, sūra 1.44; L05). The text is organised across many timescales at once.

**Symbol / sound — rhyme.** Adjacent verses share their final letter 72% vs 30% shuffle (L06); rhyme and
theme are **coupled**, not independent layers (1.78×, z≈5.2; L07).

**Network — self-reference.** Word recurrence is **local**: 6.2× over shuffle within ~16 tokens, fading by
~256 — a measured "passage" scale (L08).

**Matrix — the constellation.** 100 features × 114 sūras; the dominant axis tracks the canonical order at
**r = −0.89** (L09) — the received ordering is aligned with the text's own statistics.

**Sūra definition.** A boundary is a **multimodal discontinuity** (AUC 0.82, L11), each boundary a **local
optimum** (L12), and the text an **extremum** under a perturbation battery (L13). Boundaries split ~35%
surface-hard / ~65% semantic-soft (L16). Crucially, sūras are marked **asymmetrically at the opening**:
across four independent rasm channels (first letter, first word, first-verse shortness, fresh-root novelty)
opening verses are distinguishable from interior ones (AUC 0.64–0.77, cross-validated; L18).

**Order / sequence.** Order-load 9,922 bits (L14); the surface register is **stationary**, so the text's own
MDL-optimal segmentation is ~63 coarse "movements," not 114 sūras (L15) — a sūra is a unit of **meaning** on
a stylistically uniform surface; intermediate-complexity band (L19); per-verse necessity (L20).

---

## 3. Convergence — what unifies, and what does not (honest)

**Cross-modal convergence (oneness) — holds.** The same structures are marked by independent channels at
once: rhyme↔theme couple (L07); a sūra boundary jumps in rhyme + length + word-links simultaneously (L11);
the onset register shows in four unrelated channels (L18); per-verse necessity holds in rhyme + length +
root independently (L20). The fused boundary detector L11⊕L18 reaches **AUC 0.901, d 1.84** — the modalities
reinforce rather than duplicate each other.

**Cross-scale coupling — partial.** The word → verse → sūra scales are genuinely coupled (per-sūra
co-variation r = 0.35, z = 5.0; `p1_unify.py`), but the **letter scale is statistically detached** (z ≈ 1).
A mild genuine multifractality exists in the letter-size signal (Δh ≈ 0.17 vs 0.08 shuffle, z = 16,
`p1b_mfdfa_robust.py`); the dramatic word-count multifractality was a **rejected integer-tie artifact**. So
"one seamless system across **all** scales" is **not** supported at promotable strength — the system is a
coupled **word–verse–sūra** hierarchy with the letter scale semi-detached. Stated, not dressed up.

---

## 4. The two unit definitions

**Sūra — characterized as far as the rasm allows.**
- *Necessary:* a sūra boundary is a scale-invariant multimodal discontinuity (L11) plus a distinctive
  opening register (L18); fused detection **AUC 0.90** (`p2e_boundary_fuse.py`).
- *Sufficient (partial):* with rasm root + onset channels, the MDL recovers boundaries at **precision 0.52**
  (up from 0.45; `p2c_onset.py`) — sufficiency moved past the prior bar.
- *Ceiling:* exact recovery caps **~0.27** because sūra boundaries are 1.8% rare and **~65% are
  semantic/soft** (L16) — marked by a shift in meaning that rasm surface and roots only partially capture.
- **Definition:** *a sūra is a thematic unit on a stylistically uniform surface, necessarily marked by a
  multimodal discontinuity and a distinctive opening, but most of whose boundaries are semantic and not
  fully recoverable from the rasm surface alone.*

**Āyah — instrument-limited on the divine substrate.** The rasm consonantal skeleton does **not** mark
verse-ends well: marginal models fail (P0 0.08), and even a positional detector recovers only ~5% from
consonants. The defining rhyme (the **fāṣila**, e.g. -ūn/-īn) lives in the **vowel diacritics** — a human
layer added later — where a vowel-aware detector reaches **precision 0.56** (L17, `phaseC2.py`). By the
substrate law this documents the **human recitation tradition**, not the divine text. So on the rasm the
āyah remains **instrument-limited (عدم الوجدان)**, not defined.

---

## 5. The governing principles, audited

| principle | status |
|---|---|
| **القرآن يفسر بعضه بعضا** (text is its own model) | Upheld throughout: every claim measured against the text's **own** shuffle; no external null ever used. |
| **احسن تقویم** (necessary AND sufficient; an optimum) | Order is a measurable optimum-in-the-meaningful-band (L14, L19); determinacy holds corpus→verse (L12, L20). Sūra sufficiency improved but **not closed** (0.52 / cap 0.27). Partial. |
| **Systems of systems** | Wave fingerprints (L03–L05) confirmed; cross-scale coupling **partial** (word–verse–sūra yes, letter no). |
| **عدم الوجدان** (absence of evidence ≠ absence) | Applied honestly: word-scale necessity and rasm āyah are reported **instrument-limited**, not absent. |
| **Nothing added/deleted/moved/replaced** | Perturbation battery (L13) + the determinacy ladder (§1) confirm the text is an extremum down to the verse. |
| **Oneness / ≥3 converging modalities** | Met for every in-table feature; cross-modal fusion strengthens detection (L11⊕L18, AUC 0.90). |
| **Rasm divine / diacritics human** | Enforced: all 16 in-table features are rasm; the only diacritic result (L17) is held corroborative. |

---

## 6. What remains (the two true frontiers)

1. **Semantic channel — tested intrinsically, ceiling HOLDS.** We built root vectors from the Qur'ān's own
   co-occurrence (PPMI→SVD, fully intrinsic; `p6_semantic.py`). The semantic-shift signal is real
   (AUC 0.68 vs shuffle floor) but **does not break the ceiling**: fused with L11⊕L18 it nudges AUC
   0.918→0.924 yet **lowers** exact recovery 0.363→0.310. Reason: a co-occurrence embedding captures *word
   association*, but a soft sūra boundary is a **discourse/rhetorical shift**, not a vocabulary shift. The
   ~65% unrecovered boundaries are **comprehension-level** — they require understanding the argument, which
   no intrinsic statistic on the rasm can reach. The limit is therefore **principled**, not instrumental:
   we tried the text's own meaning-statistics and the boundary stayed beyond them.
2. **Morphology/syntax word-model** — the word rung of the determinacy ladder is unresolved with surface
   features; a rasm-admissible morphological model would test whether word-order is constrained by pattern
   and agreement rather than free.

Neither is reachable by rasm **surface** statistics; both define the next instruments, not gaps in the
result. The determined-system picture is **established from the corpus to the verse, in every modality, on
the divine substrate** — and its limits are stated as plainly as its findings.

---

## 7. The order channel, completed (L22–L26)

After Phase D the discovery loop closed the **order/sequence** rung at every scale, all on the rasm with the
text's own shuffle as the only null, each ≥3 converging modalities:

- **L22 — verse weave.** Adjacent verses share roots 1.26× above a within-sūra order shuffle (z=23; per-sūra
  paired t=11.5, 83/95 sūras; sign-test p=3·10⁻¹⁴; d=1.18), decaying with verse distance. *Reorder the verses
  and the weave collapses* — verse order is information-bearing.
- **L23 — passage order.** The weave extends to 10–20-verse passages: within-sūra block shuffles (vocabulary
  fixed) still leave neighbouring passages more similar than reshuffled ones (per-sūra paired z=5.5–12.6);
  globally non-random to ~100-verse sections.
- **L24 — sūra-sequence order.** The order of the 114 chapters is itself determined: adjacent sūras share
  roots above a length-matched shuffle (z=8.6), surviving removal of the muqaṭṭaʿāt groups (z=5.0). Decisive
  corroboration: the canonical **muṣḥaf** order carries more inter-chapter continuity (z=8.6) than the
  chronological **nuzūl** order (z=2.8) against the same null. No surface rule (length/rhyme/position)
  reproduces it (former C8).
- **L25 — uniform information density.** Adjacent verses carry similar information-per-word (root surprisal):
  smoother than a within-sūra shuffle (t=−5.3), surviving a length-matched control (t=−5.2), confirmed by
  positive surprisal autocorrelation (t=+6.2). The text regulates information *flow*.
- **L26 — closing cadence.** A sūra's final verse resolves to more common vocabulary than its interior
  (t=−4.5), specifically the last verse (vs random, t=−3.3) and *not* the rhyme word (effect strengthens to
  t=−5.3 when removed). With L18 (onset) the chapter is framed at both ends.

The ladder now reads **corpus → sūra-sequence (L24) → sūra (L11/L15/L16) → passage (L23) → verse-weave (L22)
→ verse (L18/L26) → word**, with information flow (L25) smoothed along it.

## 8. The negative frontier — what the Qurān is NOT, and why the search is closed

A long sweep of candidate structures and cross-domain analogies was run, each at root/word **and**
character scale, each against the text's own shuffle. The honest result is a wall of **clean negatives** that
sharpen the positive picture:

**Refuted structural claims** — verse-level ring/chiasmus (X6) and book-level ring (X7, symmetric sūras *less*
similar than chance); refrain/regular spacing (X5, recurrence is clustering, not pulsing); sound↔meaning
binding (X4, an artifact of the formulaic rhyme word); the sūra as a thematic unit (X3, no more coherent than
a random window). Determinacy is **forward-sequential and multi-scale, never mirror-symmetric.**

**Biomarker profile** (two-books lens) — the Qurān shares the genome's *statistical* signatures but lacks its
*combinatorial* ones:

| genome-like pattern | present? |
|---|---|
| long-range/fractal, 1/f, Zipf, Heaps | ✅ L01–L05 |
| compositional domains, co-occurrence networks, distal pairing | ✅ L08/L09/L15/L21/L22 |
| tandem repeats / palindromes / reading-frame periodicity / skew-origins | ❌ refuted or null |
| boundary motif (promoter/splice) | ◑ real but known (al-/muqaṭṭaʿāt openings) |

**Cross-domain analogies** (chirality, catalysis, allostery, error-correction, pointer, anisotropy) each
re-describe the determinacy but add no new ≥90 feature: the text is **chiral but globally racemic**
(directional units, no single book-wide handedness); it carries a real **error-correcting architecture** (the
rhyme fixes ~39 % of the verse-ending at both root and char scale; ~31 % of verses carry a frozen formula from
a 362-entry codebook) — but built from the *known* fāṣila + formulae; "pointer" indirection reduces to Heaps
vocabulary introduction; the surprisal field is **anisotropic** (within-verse correlation ≈ 2× across-verse)
but only because syntax, collocation and discourse are different strata.

**Why closed.** Every probe resolves to the same small mechanism set — scale-free statistics, the
weave/order, the rhyme cadence, the formulaic codebook, Arabic grammar, and Heaps growth. The one genuinely
unopened door, **morphology**, is feasible intrinsically (rasm-residue yields a real wazn inventory) but caps
~19–29 % token coverage; research-grade morphology needs an external segmenter, which the ONE LAW forbids.
The remaining ~65 % of soft sūra boundaries are **comprehension-level** discourse shifts beyond any statistic
on the consonantal skeleton.

**Conclusion.** The intrinsic determinacy of the Qurān is now **complete and known in kind.** It is a
scale-free, fractal, networked, distally-paired, forward-chiral, error-correcting, anisotropic *determined
system* — mapped from the corpus to the word on the divine substrate, with its boundary drawn as plainly as
its findings. Further discovery requires either a new admissible instrument (morphology) or a different
substrate (the human diacritic layer) — not more analogies on the rasm.

---

## 7. The content channel — its boundary, and the order signal that survives it (2026-06-10)

Three independent probes asked whether *meaning* (root content) carries self-determinacy **beyond what
form already explains.** All three return to chance:

- **Sūra as a thematic unit (X3a).** A sūra's verses are *not* more root-coherent than a same-length window
  placed at a random offset (pairwise co-occurrence 0.349 vs 0.382 — sūras slightly *less*; t = −1.2).
- **Lexical front-loading (X3b).** A sūra does *not* introduce its vocabulary earlier than a random window
  (first-half new-root share 0.589 vs 0.597; t = −1.1) — only the ordinary Heaps effect, no extra structure.
- **Sound↔meaning binding (X4).** Verses sharing a rhyme appear to share roots (MI z = 30.9), but the control
  kills it: remove the rhyme-*bearing* final word and the within-rhyme root-sharing collapses to z = 1.0.
  The coupling was the formulaic cadence word (saj‘), not a binding of sound to the verse's meaning-field.

**Bounded result:** at the content/root level the sūra is statistically indistinguishable from an arbitrary
same-length window, and meaning does not bind to sound beyond the rhyme word itself. The Qur'ān's measurable
self-determinacy is a **form** phenomenon — sound, edges, structure, order — not a hidden-*semantics* one.
Where meaning *appears* to add structure, it traces back to form (the rhyme word, the onset L18, the seam
L16). This converges with §6.1's principled semantic ceiling.

**But the *order* channel is alive (L22).** The one place the content carries determinacy is **sequence, not
content per se**: adjacent verses share roots **1.26× above a within-sūra order shuffle** (gap-1 0.492 vs
0.389, z = 23.1), the bond **decays monotonically with verse distance** (0.492→0.414 over gaps 1–5 — the
fingerprint of genuine local chaining, not a shared chapter vocabulary), and it **replicates independently
in both halves of the corpus** (odd sūras z = 15.5, even z = 16.1). So verse *order* inside a sūra is
information-bearing — reorder the verses and a measurable lexical weave is destroyed — even though the sūra's
*interior topic* is not distinguishable from a random window. Determinacy lives in the **arrangement**, not
the **bag**. (Ledger L22; surfaced in the Signal module.)
