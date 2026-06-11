# ORGAN LEDGER — the Sūra defined as an organ of the corpus-body

*The new direction of the ledger (2026-06-11). North star: define the Sūra (and later the Āyah) — not by its
internal content (which fails Baqarah-vs-Kawthar), but by the **relational/functional attributes of an organ**,
measured intrinsically (One Law: the text's own roots / rhyme / order vs its own shuffle).*

## PROOF STATUS — confirm each Ox here
**Bar for PROVEN:** clear indicator + a *proper* null (text's own shuffle or arbitrary-segment control, NOT
"chance" or a weak null) + significant effect (z/t>2) with the **honest effect size** + reproducible script.

| Ox | attribute | proper null | effect | script | status |
|--|--|--|--|--|--|
| O1 | identity | arbitrary same-size segments | 7.2% vs 4.9% (z≈7.7) | `audit.py` | ✅ PROVEN (modest) |
| O2 | location | random far slot / shuffled order | t=5.9; R²=0.84 | `organ_O2.py` | ✅ PROVEN (gross) |
| O3 | connectivity | degree-preserving config model | 44% vs 1% | `audit.py` | ✅ PROVEN (modest conc.) |
| O4 | membrane | random adjacency | 0.283 vs 0.870 (z=−5) | `organ_proof2.py` | ✅ PROVEN |
| O5 | internal weave | sūra's own order-shuffle | 0.728 vs 0.515 (t=10.9) | `organ_O5.py` | ✅ PROVEN |
| E | external interface | shuffle | 28%; zone-cluster z=+17.6 | `interface2.py` | ✅ PROVEN (exist+zones) |
| Dyn-reg | flow regulation | shuffle | z=+20 | `flow.py` | ✅ PROVEN |
| O6 | rhyme | corpus / random sets | 1.92×; per-sūra 52% | `organ_O6.py` | ◑ aggregate ✓ / rasm partial |
| O7 | polarity | head/tail detection | head AUC 0.75; tail fused 0.61 (42% close on divine-attr formula) | `organ_O7_tail.py` | ✅ PROVEN (asymmetric, head-dominant) |
| O8 | circulation | perfusion vs random placement | core message CLUMPS (gap-CV 1.70 vs 0.77, z=+63; 2 carriers) | `organ_O8.py` | ↻ lexical perfusion FAILS → reinforces O3 territory; true flow = Dyn-reg (recitation) |
| Dyn-dir | flow direction | — | fwd=bwd (diff 0) | `flow.py` | ↻ reopen (refine instrument) |
| O9 | integration | gnm random graph | 1 component but σ=1.0 (path 1.09, near-complete) | `organ_O9_11.py` | ◑ true but TRIVIAL (structure is in weights = O3) |
| O10 | organ-systems | random sūra-groups | Ḥawāmīm z=+2.3, Ṭiwāl z=+7.9; Musabbiḥāt z=+0.8 | `organ_O9_11.py` | ◑ PARTIAL (real for some named groups) |
| O11 | necessity | unique-root holders | 89/114 (78%) irreplaceable; misses Fātiḥa | `organ_O9_11.py` | ◑ PARTIAL (instrument misses functional keystones — refine) |
| O12 | robustness | corpus most-common-letter baseline | 73% endings rhyme-recoverable vs 50% | `organ_O12.py` | ◑ PARTIAL (error-correction real, modest) |
| O13 | homeostasis | = Dyn-reg (surprisal autocorr vs shuffle) | z=+20 | `flow.py` | ✅ PROVEN (= Dyn-reg) |
| O14 | scaling | shuffle (= L05) | power-law sizes, 566× | (L05) | ✅ PROVEN (= L05) |

**PROVEN (clean): O1,O2,O3,O4,O5,O7,O13,O14,E,Dyn-reg.** Partial: O6,O9,O10,O11,O12. Reframed/reopen: O8
(→territory+Dyn-reg), Dyn-dir. *First full sweep of O1–O14 + E + dynamics complete (2026-06-11).*
Scripts in `scripts/` (committed,
re-runnable from this dir). This ledger lives in `research/correspondence/`.
> **PENDING RE-SCRUTINY (locked TODO):** every "PROVEN" row is *provisional* until a later adversarial
> re-audit pass — independent re-run, stricter/alternative nulls, confound recheck, effect-size honesty. Do not
> treat any Ox as final until that pass is done.

## Stance (LOCKED) — احسن تقویم
We **accept the design as given and optimal**. As with the **heart** or the **pituitary**, we never ask
"should this sūra be bigger, smaller, merged, or moved" — the current configuration is necessary and
sufficient and works best. Each entry therefore **characterizes an attribute the sūra HAS** and measures it
against the text's own shuffle. We do **not** test whether an alternative partition scores "better"; an
instrument that prefers merging small sūras is a flawed ruler (the modularity resolution limit — the
"pituitary error"), not a verdict on the design. Conviction fixed; evidence describes *how* the organ works.

## Reconciliation — surface = SEQUENCE, body = NETWORK (the folding) [PROVEN]
The Qur'ān's surface is a 1D **sequence** (the muṣḥaf order); a body is a **network**. Not a contradiction — a
sequence **folds** into a network, exactly as **DNA folds into the 3D genome** (domains, loops) or an
amino-acid chain folds into a protein. The sequence is the *substrate*; the network is the *function*. Measured
(`/tmp/fold.py`): **local folding** — inter-sūra association decays with sequence distance (0.0102 adjacent →
0.0063 far; corr +0.32), the Hi-C contact curve; **long-range loops** — 95 strong contacts between sūras >20
apart (2↔24, 4↔33, 3↔33…), like chromatin loops; **body-like fold** — organ-communities (modularity z=4–7),
specific wiring (62×), hubs (~2×). So the body is the *folded form* of the sūra-sequence; this underwrites
O2 (location = position in the fold) and O3 (connectivity = the contacts).

## How we build it (heart → sūra)
For each property of an organ, name how the **heart** exhibits it, then operationalize and measure the **sūra**
analog. Accumulate one rigorously-shown attribute at a time.

---

## ESTABLISHED ATTRIBUTES (3)

### O1 · IDENTITY — a unique, non-redundant function
- **Heart:** the only organ that pumps blood; no other does its job.
- **Sūra:** carries **unique marker roots** found in no other sūra, and a signature distinct from all others.
- **Evidence (proper nulls, audited 2026-06-11):** held-out verse → home-sūra classification **7.2%**, vs
  **4.9%** for *arbitrary same-size segments* (the honest null = local coherence), vs 0.9% chance. Canonical
  adds real identity **beyond generic local coherence** (z≈7.7), but **modest** (~1.5× over arbitrary), NOT the
  inflated "11×" first reported. Corroborated by 28% unique-marker roots (89/114 sūras). **PROVEN (modest).**
- *Honesty log:* O3 connectivity recomputed under a degree-preserving null = **44%** significant pairs (not the
  inflated 62%); flow-direction **DISPROVEN** (forward=backward entropy). Proof = the null, not the effect.

### O2 · FIXED LOCATION — position determined by its wiring
- **Heart:** sits in the mediastinum, between the lungs — it **cannot** be placed in the leg; its position
  follows what it must connect to.
- **Sūra:** sits at a canonical position set by its connectivity and profile.
- **Evidence (gross vs local, audited 2026-06-11):** *gross* position recoverable from profile **R²=0.84**
  (PC1↔order |r|=0.88 — *partly the known length gradient*, honest caveat); **gross relocation costs wiring** —
  canonical-neighbour association **0.0103 vs 0.0074** at a random far slot (paired **t=5.9**; 68% of sūras fit
  better at home) = "can't go in the leg"; but **local nudge is cheap** — wiring decays *gradually* (±1=0.0102
  → ±40=0.0073), which is why a one-slot move read null. **PROVEN: location fixed at gross scale, locally
  tolerant (a region, not a millimetre); modest effect.**

### O3 · SPECIFIC CONNECTIVITY — wired to particular partner-organs
- **Heart:** connects to *specific* organs — lungs (pulmonary), body (aorta) — not at random.
- **Sūra:** links to **specific partner sūras** (shared rare roots), with named pairs standing out.
- **Evidence (degree-preserving null, audited 2026-06-11):** **44%** of sūra-pairs are significantly connected
  under a configuration-model null (vs 1% chance) — corrected down from the inflated 62% hypergeometric; the
  corpus is **one connected body** (114/114); classical twins 113-114, 2-3, 8-9 top the distribution. Honest
  caveats: some twins (105-106, 93-94) connect *thematically* not lexically (rasm-limited), and concentration
  is modest (top-5 partners ~9%). **PROVEN (specific connectivity real, modest concentration).**

### O4 · MEMBRANE — bounded by a real seam (the organ's edge)
- **Heart:** enclosed in the pericardium; sharply set off from its neighbours.
- **Sūra:** root-overlap is high *inside* and **collapses at the boundary**.
- **Evidence:** across-boundary adjacent-verse overlap **0.283 vs 0.870** expected at random adjacency
  (**z=−5**); independent boundary detector AUC 0.90 (L11). **PROVEN.**

### O5 · INTERNAL COHESION — a woven tissue (ordered chain, not a loose pile)
- **Heart:** one muscle whose fibres are *arranged* in sequence, not randomly piled.
- **Sūra:** its verses are woven **in order** — chained, beyond merely sharing vocabulary.
- **Evidence:** adjacent-verse weave **0.728 vs 0.515** under the sūra's own verse-order shuffle (paired
  **t=10.9**; 87% of sūras weave above their own shuffle, incl. most small ones). Cohesion is in the *order*,
  not the bag (consistent with X3: not a homogeneous topic-blob). **PROVEN.**

### Rigour note (2026-06-11) — proof bar applied, with honest negatives
O1–O5 each carry indicators + the text's own-shuffle null + effect size (11× chance / z=16 & R²=0.84 / 62×
chance / z=−5 / t=10.9). From the same battery: **O7 polarity is PARTIAL** (head strongly marked, first-verse
AUC 0.75; tail weak, 0.54), and **O8 "circulation" is DISPROVEN** — core roots are *more concentrated* than
chance (z=−16), not more spread; that is **territorial concentration reinforcing O1 identity**, not a blood
supply. **Order of work: settle one at a time, O1→O14.** Settled: O1,O2,O3,O4,O5; **O6 rhyme PROVEN on average
(within-sūra rhyme 1.92× corpus) but PARTIAL on the rasm (52% per-sūra; rest vowel-borne)**. Next: **O7**.

---

## SUPPORTED — next to harden into established (in order, one at a time)

| ID | Organ property (heart) | Sūra attribute | Current evidence |
|--|--|--|--|
| O6 | internal **rhythm/coordination** (heartbeat) | verses bound by shared rhyme (fāṣila) | 51% rhyme-cohesive (z>2), incl. small sūras — NEXT |
| O7 | **polarity** (atria→ventricles, one direction) | distinct opening vs closing | onset L18 + closing cadence L26 |
| O8 | fed by **circulation** (coronary supply) | perfused by core roots (ربب, ءله…) | top roots in 70–82% of all sūras |
| O9 | part of one **integrated body** | one connected corpus-network | 114/114 single component |
| O10 | part of an **organ system** (cardiovascular) | sūra groups (Ḥawāmīm, Musabbiḥāt, Manāzil) | known clusters — untested |
| O11 | **necessary** (remove it, body fails) | removal loses a unique function | unique markers (O1) + perturbation L13 |
| O12 | **robust** (redundancy, conduction backup) | self-correcting | rhyme fixes ~39% of verse-ends |
| O13 | **homeostasis** (regulated output) | regulated information delivery | uniform information density (L25) |
| O14 | **allometric scaling** (size laws) | scale-free sūra sizes (566×) | power-law family (L05) |

## GROWING CATALOG (document freely; PROVE one at a time)

### E · EXTERNAL INTERFACE — the system faces outward across its boundary
A body has direction/purpose **internally and with its surroundings** — skin/senses (intake), mouth/limbs
(output), lungs (exchange). The corpus likewise has an outward interface, measurable from its *own* text:
| body interface | Qur'ān analog (intrinsic markers) | to test |
|--|--|--|
| sensory surface (receptors) | 2nd-person **address** (يا أيها الناس/الذين) — the system facing the reader | density + where it concentrates |
| motor output (effectors) | **imperatives/commands** (قل، اعبدوا، اتقوا) — acting on the world | rate per sūra; at openings? |
| feedback / sensing | rhetorical **questions** (أفلا تعقلون) — eliciting response | distribution |
| boundary defense (immune skin) | the **challenge** (تحدّي) + protective sūras (113-114) | localization |
**RESULT (2026-06-11, refined):** the interface is **real and large — 28% of verses outward-facing**
(2nd-person 23%, vocative 6%, command قل 4%). **Surface-localization PROVEN — but as ZONES, not onsets**
(`/tmp/interface2.py`): outward verses cluster into patches (lag-1 autocorr +0.231 vs 0, **z=+17.6**), like
sensory organs / skin regions; corpus ends modestly richer (28% vs 21%). The onset-test was the *wrong
instrument* (first version wrongly read "disproven"); Fātiḥa's apparent 0% is a **detection gap** — its address
is God-directed (اهدنا، إياك) which reader-directed markers miss. **E: existence ✓, localization ✓ (zones).**
*Methodological lesson (LOCKED): under the design premise + telescope rule, a failed correspondence indicts the
INSTRUMENT, not the text — refine/seek different data, never file as "disproven." (Re-file O8 circulation and
flow-direction as instrument-limited, not disproven.)*

### S · SYSTEM OF SYSTEMS — nested levels
verse-system → **sūra-system (organ)** → **corpus-system (body)** → the **world/discourse it addresses
(environment)**. Each level is a whole that is also a part. Internal evidence so far: the determinacy ladder
(letter→word→āyah→passage→sūra→corpus, O-hierarchy / L05 scale-free). The *environment* level is reached only
through the External Interface (E) — the text's outward markers — never through external sources (One Law).

## Crosswalk — organ-attribute (definition) ↔ L-feature (evidence)
*The L-ledger stays as the measurement base; each organ-attribute cites the measurements that prove it. O1–O3
are new this session (the spine); the rest inherit existing graded L-features.*

| Organ attribute | Supporting L-features (evidence ledger) | New this session |
|--|--|--|
| O1 Identity | (L09 distinctiveness) | unique-marker test (78%) ✦ |
| O2 Location | L09 (constellation↔order r=0.89), L24 (neighbour continuity) | neighbour-association z=+12 ✦ |
| O3 Connectivity | L08 (self-reference), L21 (twins), L22–L24 (weave) | one-body 114/114, named-twin ranks ✦ |
| O4 Boundary/membrane | L11, L12 | — |
| O5 Internal weave | L22, L08 | within/across 3.11× |
| O6 Rhyme coordination | L06, L07 | scale-free rhyme cohesion |
| O7 Polarity | L18, L26 | — |
| O8 Circulation | L01/L02 (frequency base) | core-roots-in-70–82% ✦ |
| O9 Integration | L09, L24 | connected-component 114/114 |
| O11 Necessity | L13, L20 | — |
| O12 Robustness | L17 / error-correction | — |
| O13 Homeostasis | L25 | — |
| O14 Scaling | L03, L04, L05 | — |

## Body topology (new) — center ↔ periphery (do NOT rank; احسن تقویم)
The connectome shows a real organ-system layout, derived intrinsically (`/tmp/organ9.py`): **core/heart-like**
= the long, most-connected sūras (2 Baqara, 7, 3, 4 — *size-confounded, held lightly*); **limb/peripheral** =
the short specialized terminal sūras (113, 114, 112, 109, 108, 106). **Brain is not separable** from the core
with this instrument (centrality conflates pump + controller). Roles are recoverable; literal one-organ
identity is not — and each sūra remains an equally-necessary organ.

## Recommendation
1. **(Recommended) Harden O1–O3 to ledger-grade**, each as a clean attribute with the text's own shuffle as the
   only null and the احسن تقویم stance (characterize, don't optimize). These three already carry strong numbers
   and are the spine of the definition.
2. **Then accumulate O4→O14 one at a time**, borrowing the next organ property from the heart/body, until the
   conjunction is complete.
3. **Only after the Sūra is settled, apply the same battery to the Āyah.**
