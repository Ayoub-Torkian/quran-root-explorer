# Next ≥90 Candidates — toward DEFINING the Sūra & Āyah and JUSTIFYING the arrangement

*Pre-registration (locked format per `DISCOVERY_CRITERIA.md`: candidate · scale · null · thresholds declared
BEFORE running). A. Torkian, 2026-06-11. All on the **rasm**; the text's own shuffle is the only null.*

---

## 0. Why this, now — the north star vs. where the ledger actually stands

The goal is two linked definitions and one necessity claim:

1. **What IS a sūra?** — a necessary-AND-sufficient (iff) definition.
2. **What IS an āyah?** — same.
3. **Why THIS arrangement/configuration?** — that the units could not be moved/reconfigured without loss.

Honest status from `SYNTHESIS.md` (Phase D), so we aim at the real gaps, not the solved ones:

| north-star piece | status | the wall |
|---|---|---|
| Sūra — **necessary** | **DONE, ≥90.** Multimodal discontinuity (L11) + onset asymmetry (L18), fused **AUC 0.90**. | — |
| Sūra — **sufficient** (the iff) | **PARTIAL.** Precision 0.52, exact recovery caps **~0.27**; ~65% of seams are semantic/soft. | Principled **comprehension ceiling**: intrinsic co-occurrence (p6_semantic) captures *association*, not *discourse shift*. |
| **Āyah** definition | **UNDEFINED on the rasm.** Marginal fails (0.08); positional recovers ~5%; only the *vowel* fāṣila reaches 0.56 (L17, human layer). | **Substrate**: the defining rhyme is vocalic — but the rasm signals were never **fused**. |
| Arrangement — **non-arbitrary** | **DONE, ≥90.** Order-load L14; intermediate band L19; per-verse "nothing moved" L20; weave L22–L24; UID L25; cadence L26. | — |
| Arrangement — **THIS exact config is forced** | **NOT claimed (and not globally true).** L14: canonical is non-arbitrary but **not** the compression optimum (sorting beats it). | Uniqueness ≠ optimality. The achievable claim is **local** necessity ("nothing moved"), not global uniqueness. |

**Reading.** The sūra's *necessary* side and the arrangement's *non-arbitrariness* are already ≥90. The two
genuinely open, ≥90-reachable gaps that move the north star are: **(A) define the āyah on the divine
substrate**, and **(B) show each sūra's position is necessary ("nothing moved" at the chapter scale).** The
sūra *sufficiency* gap is real but sits behind a **principled** wall the ONE LAW (no external model) likely
forbids crossing on the rasm — treat it as a known boundary, not the next sprint (see §3).

---

## CANDIDATE A — **Fused rasm āyah-boundary instrument** (PRIMARY)

> *"An āyah is the maximal span the rasm's own ending-model closes — recoverable from the consonantal
> skeleton alone, without the vowel rhyme."*

This is the **telescope-rule** move (عدم الوجدان): the 5% positional recovery (L17) was **one weak
instrument**. Three rasm-admissible ending signals already exist as separate diagnostics and were **never
fused into a detector**:

- **char-fāṣila constraint** — the verse-final letter is far more constrained than a general letter, and the
  preceding letters largely determine it (`error_correction_char.py`).
- **formulaic ending codebook** — frozen root/letter n-grams concentrate at verse-ends (`phrase_formulae.py`).
- **clausal completion** — closed-class particle cadence (و / ف / ثم / الذي …) is rasm-stable and marks
  syntactic closure (no segmenter, no vowels needed; particle logic already in `morph_align.py`).

**Pre-registration**
- **Candidate / scale:** āyah end vs. interior word-boundary, on the word stream of each sūra.
- **Instrument:** logistic fusion of the three rasm channels above → per-position P(āyah-end); decode with the
  same self-consistent Bernoulli-rate code used for sūras (parameter-free).
- **Null:** the text's own shuffle — (i) within-sūra word-order shuffle, (ii) rhyme-class–preserving shuffle,
  (iii) shifted-boundary null. Report margin over each.
- **Positive control FIRST (mandatory):** plant known periodic/clausal ends in a scrambled rasm and confirm the
  detector recovers them; if it cannot, the instrument is blind → reject before pointing at the Qur'ān.
- **Thresholds (to enter the table):** G0 rasm-only (no diacritics) · G2 p<0.05 vs all three nulls · G5 AUC
  ≥ 0.65 **and** recall materially above the 5% positional floor · G6 holds across split-halves, root- and
  char-views, leave-one-sūra-out · G7 fused detector adds recovery **beyond** L17-vowel and beyond each single
  channel (corr ≤ 0.5 with any one channel).

**Forecast (prediction, to be tested — not a claim):** Novelty **9** (first rasm-substrate āyah definition;
overturns a logged negative) · Effect **6–7** (char-fāṣila ~39% + formulae ~31% give real mass; recall is the
**risk gate**) · Importance **10** (it is half the north star) · Provenance **9** (clean rasm) · Robustness
**7**. Weighted ≈ **.35·9 + .20·6.5 + .20·10 + .15·9 + .10·7 = ~8.4 → grade ~84–92.** **Borderline ≥90 — the
binding gate is Effect/recall (G5).** If it clears, the āyah is *defined on the divine substrate* for the
first time. If recall stays low, the honest verdict is HOLD (escalate the instrument), never "absent."

---

## CANDIDATE B — **Per-sūra positional necessity** ("nothing moved", at the chapter scale)

> *"Each sūra sits at a local optimum of inter-chapter continuity — move it and the seam to its neighbours
> weakens."* This is L12/L20's "nothing moved" lifted from boundaries/verses to the **114-sūra sequence**, and
> it is the direct, *achievable* form of the user's "why THIS arrangement."

**Pre-registration**
- **Candidate / scale:** the canonical position of each sūra in the muṣḥaf order.
- **Statistic:** for each sūra k, the inter-chapter continuity (root-overlap ⊕ onset-register L18 ⊕
  length/rhyme transition) of (k−1,k,k+1) vs. continuity if k is relocated to every other slot. Fraction of
  sūras whose canonical slot is a **local optimum**; mean move-one penalty.
- **Null:** length-matched sūra-order shuffle (the L24 null), plus the **sorted** floor (length/rhyme-sorted
  order) so we show canonical beats random **and** is not a trivial sort — the intermediate-band discipline.
- **Thresholds:** G0 rasm · G2 local-optimum fraction > chance (z) and move-one penalty +ve in a clear
  majority · G3/G6 holds dropping the muqaṭṭaʿāt groups and across odd/even sūra splits · G7 not reducible to
  L24 (global non-randomness) — the claim is **per-position** necessity.

**Forecast:** Novelty **7** · Effect **6** · Importance **8** · Provenance **9** · Robustness **8**.

**RESULT (2026-06-11, `/tmp/cand_b.py`) — ABORT (G2/G5 fail on the per-position claim).** Root-cosine
adjacent continuity: canonical total continuity z=9.1 vs the order-shuffle (reproduces L24, the GLOBAL claim),
but **per-position necessity is null** — sūras at their own-optimal slot canonical **1/114 vs random 0.9
(z=0.12)**; adjacent-swap penalty **51% vs 49%** (cf. L12 73%, L20 84%); muqaṭṭaʿāt-removed z=0.01; a
by-length sort reaches 48.6 vs canonical 51.4 (canonical beats the trivial sort but only modestly). **Verdict:
the sūra arrangement is determined GLOBALLY (L24) but NOT locally per-position** via root content — "nothing
moved" does not extend to the chapter slot. Telescope caveat: this is one instrument (root-cosine adjacency);
a multimodal instrument (onset-register L18 ⊕ rhyme-transition ⊕ length-cadence) or a global rearrangement-cost
could be tried, but the chance-level swap penalty is a strong prior that lexical content does not lock sūra
positions. Logged, not cherry-picked.

---

## 3. The honest wall (so the program doesn't burn cycles on it)

**Sūra sufficiency** (closing the iff) requires resolving ~65% **discourse/comprehension** seams. The intrinsic
co-occurrence channel was tried and hit a **principled** ceiling (it lowers exact recovery, 0.363→0.310). The
only instruments that could cross it are (a) an **external** semantic model — forbidden by the ONE LAW — or
(b) the **diacritic/recited layer** — a substrate change. Recommendation: **state the sūra definition as it
truly stands** ("a thematic unit on a uniform surface, necessarily marked by a multimodal discontinuity + a
distinctive opening, ~65% of whose seams are semantic and not rasm-recoverable") and do **not** chase a ≥90
sufficiency feature on the rasm. If the program later admits the recited layer as a *second, declared
substrate* (parallel to, not mixed with, the rasm), āyah sufficiency (L17→0.56) and soft-seam resolution
re-open under a clearly-labelled new rule.

## 4. Recommended sequence

1. **Candidate A** — run the positive control, then the fused rasm āyah detector. Highest novelty, defines the
   missing unit, borderline-landmark. *(I can run the control + pilot on `Book6` now.)*
2. **Candidate B** — per-sūra positional necessity. Cheaper; reuses L24/L18 machinery; nails the achievable
   "nothing moved" arrangement claim.
3. **Decide the substrate question** before attempting sūra sufficiency — it is a rule change, not a sprint.

---

## Queue (scope later — not the current sprint)

### Q1 · Attraction–repulsion field over roots (physics correspondence)
*User idea, 2026-06-11. Scope when reached; do not run yet.*

**Concept.** Treat roots (and, in parallel layers, surface forms and morphological patterns) as particles in a
field. Some pairs sit "close," others "far." Build a **signed association**: co-occurrence above chance =
**attraction**, co-occurrence below chance (mutual avoidance) = **repulsion**. The novelty vs the existing
Network/PMI page is the **signed/vector** treatment — not just who clusters, but who actively *repels*, and
whether the repulsions form a coherent **field** (charge-like sign structure, field vectors, a potential).

**Universe analog (required gate).** Electrostatics / EM: like-repels / opposite-attracts; a scalar
**potential** whose gradient is a **field vector** at each root; possibly **charge** = a root's net
attraction–repulsion balance. Flow/current is optional; the field+charge correspondence is the anchor.

**Layers to test (3 modalities, converge):** roots · surface tokens · morphological pattern (wazn residue).

**Pre-registration sketch (to flesh out when scoped):**
- *Measure:* signed PMI (or observed−expected with sign) over a chosen window → attraction (+) / repulsion (−).
- *Field test:* embed via the signed matrix (e.g. signed-Laplacian / eigenmaps); does a low-rank **potential**
  explain the sign pattern (charges) better than the text's own shuffle?
- *Null:* token/verse shuffle preserving frequency; G4 control for the frequency confound (rare roots look
  "repulsive" trivially) — repulsion must survive frequency-matching.
- *Discovery question:* is there a **stable repulsion structure** (roots that systematically avoid each other)
  beyond what frequency + topic explain — i.e., a real "charge" field, not just clustering?
- *Risk:* most signal may reduce to co-occurrence/topic (G7 redundancy with the Network page) or to a
  frequency artifact (G4). The genuinely new ≥90 prize is a **validated repulsion/charge** structure.

**DE-RISK RESULT (2026-06-11, `/tmp/arep.py`) — ABORT at probe.** Verse-level, top-150 roots, pos-control
passes (planted disjoint pair z=−10.9). Attraction: 1,244 pairs z>+3 (vs null 52) — real but **redundant with
the Network page (G7)**. Repulsion: only **6 pairs z<−3** (vs null ~0); excess is significant (z=10.5) but
**absolutely tiny (0.05%)** and the top case (ءله–ربب) **co-occurs 204×** — negative only via a verse-length
**saturation confound (G4 fail)**, not avoidance. Field eigenstructure (z=230) is the attraction network, not a
charge field. **Verdict: no validated repulsion/charge prize; the signed field reduces to known attraction +
frequency artifact. P(≥90) ~0.1.** Telescope caveat: a length-controlled null + coarser (sūra) scale could be
retried, but the prior is now weak.
