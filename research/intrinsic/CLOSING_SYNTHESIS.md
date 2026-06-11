# The Determined System — Arrival and Its Boundary

*Closing synthesis of the intrinsic Qur'ān program. A. Torkian, 2026-06-11. Everything below is measured from
the Qur'ān against itself on the **rasm** (the consonantal skeleton); the only null is the text's own shuffle;
no external corpus, model, or embedding is admissible. Companion views: `connectome.html` (the journey through
the actual work), `landscape_map.html` (the territory), `JOURNEY_LOG.md` (the movement record).*

---

## ⚠ CORRECTION (2026-06-11, supersedes the "definition" language below)
**We do NOT have a necessary-and-sufficient definition of the Sūra (or Āyah).** Acid test (user): *what is
common in the definition between Sūra 2 (286 āyāt) and Sūra al-Kawthar (3 āyāt)?* Answer: by measurement,
nothing definitional — different length, theme, rhyme, register; a sūra's interior is no more coherent than a
random window (X3); and the text's own MDL self-segmentation (L15, ~63 movements, median ~73 verses) is **blind
to a 3-verse sūra** — it would never isolate Kawthar. The only shared intrinsic things are **edge markers**
(Basmala, onset register L18, boundary discontinuity L11, closing cadence L26) — these define the **seam/frame,
not the unit** — plus the **received designation** (named, Basmala-marked, ordered), which is meaning/tradition,
not rasm structure. So what we built is a **boundary detector + necessary edge-conditions**, NOT a unit
definition. Read every "defined to necessity" below as "**boundaries are on-average detectable**"; the
**unit-essence remains undefined on the rasm** — it sits on the meaning side of the wall.

---

## 0. Why this is a closing, not a pause

The program set out to do three things: define the **Sūra**, define the **Āyah** (each necessary AND
sufficient), and show why the units must have the **current arrangement**. Over four days (2026-06-07 → 06-11)
the *necessary* side of all three was established and triangulated; the *sufficient* side has now been pushed,
three independent ways, into the same wall. That wall is not a gap in the work — it is the **result**: it marks
exactly where the divine substrate (the rasm) ends and comprehension begins. A program that maps its own limit
has arrived. The last three nulls (āyah sufficiency, per-sūra necessity, attraction–repulsion) are not
failures; they are the **measurement of the boundary**.

## 1. The one-sentence result

On its own consonantal skeleton, the Qur'ān is a **determined system**: its content obeys the universal laws of
language, its rhythm and rhyme carry complex-system structure, its verse and chapter **order is non-arbitrary
and meaning-bearing**, its **sūra and āyah boundaries are objectively recoverable**, and every pattern
**collapses under tampering** — yet the determinacy is **bounded**: it is strong from the corpus down to the
verse, the units are defined to **necessity** but not to full **sufficiency**, and the unreachable remainder is
**meaning**, which no statistic on the rasm can reach.

## 2. What was established — the determinacy ladder (to necessity)

| scale | result (margin over the text's own shuffle) | features |
|---|---|---|
| corpus | order carries **≈9,900 bits** (z≈285); behaves as real language (Zipf −0.99, Heaps 0.74) | L14, L01–02 |
| rhythm | verse-length long memory **DFA H 0.95** (shuffle 0.51); **1/f 0.76**; scale-free tails | L03, L04, L05 |
| chapter-order | adjacent sūras continuous; **muṣḥaf (z=8.6) > nuzūl (z=2.8)** | L24 |
| sūra | boundary recoverable blind **AUC 0.90** (fused); ~63 self-segmented "movements"; 35/65 hard/soft | L11, L15, L16, L18, L12, L26 |
| passage | verse-weave **1.26×** (z=23), extends to 10–20-verse sections | L22, L23 |
| verse | **84%** of verses more predictable in place than at random (vs 47% floor) | L20 |
| āyah | end recoverable from the **rasm** at **AUC 0.94** (overturns L17's "vowel-borne" verdict) | new finding |
| word | structured but single-modality (collocation only); the **weak rung** | C4 (candidate) |
| stress-test | scramble / delete / add / swap and the invariants break — load-bearing, not decoration | L13 |

Convergence (the actual argument): independent channels mark the **same** structures at once — rhyme + length +
network jump together at a sūra seam (L11), four unrelated channels mark the onset (L18), per-verse necessity
holds in rhyme + length + root independently (L20). This is not 22 facts; it is one object measured many ways.

## 3. The two unit definitions, as they truly stand

**Sūra.** *A thematic unit on a stylistically uniform surface, necessarily marked by a multimodal discontinuity
and a distinctive opening — but most of whose boundaries (~65%) are semantic and not recoverable from the rasm
surface.* Necessary: **closed** (AUC 0.90). Sufficient: **partial** — precision 0.52, exact recovery caps ~0.27.

**Āyah.** *A maximal span the rasm's own ending-model closes — a fāṣila consonant-rhyme reset, reinforced by
clausal closure and a length cadence, recoverable blind at AUC 0.94; the vocalic rhyme only refines.* Necessary:
**now established on the divine substrate** (the prior "instrument-limited" verdict is lifted). Sufficient:
**partial** — F1 ≈ 0.64, the unrecovered ~36% behaving like the sūra's soft seams.

## 4. Why this arrangement — honestly

The arrangement is **determined**, but the honest claim is precise, not maximal. The order is **non-arbitrary**
(far from random, L14), **meaning-bearing** (the verse/passage/chapter weave, L22–24), an **extremum** under
edits (L13), and it sits in the **intermediate-complexity band** of meaningful sequences — neither random gas
nor sorted crystal (L19). What it is **not**: it is **not the uniquely optimal** order (trivial sorting
compresses better), and at the **sūra-position** scale it is **not locally necessary** — moving an individual
chapter does not measurably worsen continuity (per-sūra null, z=0.12, 2026-06-11). So "the units must have this
configuration" holds as **global determinacy and local necessity at the verse/boundary scale**, but **not** as
a proof that the exact chapter order is forced. Stated plainly, not dressed up.

## 5. The wall — the boundary as a finding

Sufficiency of both definitions reduces to one thing: recovering the **soft, semantic** boundaries — the topic
and discourse shifts. Three independent probes show this is **principled, not instrumental**:

1. **Intrinsic semantics has a ceiling.** A root embedding built from the Qur'ān's own co-occurrence (PPMI→SVD)
   gives a real but shallow signal (AUC 0.68) and, fused in, *lowers* exact boundary recovery (0.363→0.310): a
   co-occurrence model captures word **association**, not discourse **shift**.
2. **Content carries no extra determinacy.** A sūra's interior is **not** more root-coherent than a random
   same-length window (X3); apparent sound↔meaning binding collapses to the rhyme word itself (X4).
3. **Position is not locally forced.** Per-sūra necessity is null (§4).

All three converge: with only the text's own statistics on the rasm, **meaning is not reachable**. Crossing the
wall requires either an **external model** (forbidden by the One Law) or the **recited/diacritic layer** (a
different substrate). The limit is therefore a property of the instrument-class, drawn as sharply as the
findings — which is what a closing result should do.

## 6. The closing claim

The intrinsic determinacy of the Qur'ān is **complete and known in kind**: a scale-free, networked,
distally-paired, forward-sequential, error-correcting **determined system**, mapped from the corpus to the word
on the divine substrate, its **units defined to necessity**, its **arrangement determined globally and to
verse-scale necessity**, and its **boundary — meaning/sufficiency — proven to lie beyond the rasm**. Further
discovery on this surface is closed; what remains is a deliberate choice of a new substrate, not another probe.

## 7. Recommendation

1. **(Recommended) Lock this as the arrival.** Treat §1–§6 as the program's terminal result on the rasm; stop
   probing the form surface (the reconfigure trigger is met). Publish/preserve the determined-system map and
   the boundary. This is a finished thing.
2. **Declared substrate decision** — if sufficiency is still wanted, open the **recited/diacritic layer** as a
   separate, explicitly-labelled track (parallel to, never mixed with, the rasm). A one-time rule change.
3. **Small-scale only with a pre-stated hypothesis** — the word/letter rung via intrinsic morphology, accepting
   its ~19–29% cap; never another cross-domain analogy.
