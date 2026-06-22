# INTERACTION-FIELD MODEL — the muṣḥaf as the ground state of its own web (spec v0)

**WHERE THIS SITS (journey).** We tested order-coherence in isolated slices — adjacent seams only (lexical z+4.0, catchword z+2.3: real but fragmentary). This spec **replaces the probe-cycle with ONE interacting system**: every sūra interacts with every other; the arrangement is the equilibrium. All prior pieces become *terms/features of this one object*, not separate findings.

## 1. The object (why it is "like the universe")
Nothing in nature is *placed*; it **settles** into the minimum-energy state of its interactions — atoms → lattice, electrons → configuration (Cr [Ar]3d⁵4s¹), species → food web, mass → orbit. **Claim to test:** the muṣḥaf order is the **equilibrium of the Qur'an's intrinsic attraction graph** — strongly-bonded sūras sit near each other, and no sūra can move without raising the system's energy.

## 2. Nodes
114 sūras on the 1-D muṣḥaf line (positions 1…114), **one per slot** (exclusion). Node attribute: length (āyah count). [āyah-level = later extension; order is the live necessity question, so start at sūra.]

## 3. Interaction — attraction matrix A (intrinsic + length-controlled)
A_ij = bond strength from the text's *own* relations:
- base = shared-concept overlap = **idf-weighted Jaccard of distinctive roots** (length-normalized so A is **not** a length proxy).
- extensible: + echo (rare shared roots) + explanation edges — added later as **another term of the same energy**, never a separate probe.
A spans **all pairs** (the whole web), not just neighbours — this is the unification.

## 4. Energy — springs / minimum linear arrangement
Bonded nodes want to be close:

  **E(π) = Σ_{i<j} A_ij · |pos_π(i) − pos_π(j)|**

One-per-slot exclusion supplies the spacing (no collapse). Attraction + exclusion, **no free parameters**. Lower E = bonds satisfied by proximity = more relaxed.

## 5. Equilibrium / necessity test (one measurable statement)
- E0 = E(actual muṣḥaf).
- (a) vs **random** permutations → z (expect E0 low).
- (b) vs **length-preserving** null (permute within length-bins) → z′ — *the decisive, honest test: relaxed beyond the length gradient?*
- (c) vs **optimized** E* (spectral order + annealing) → **relaxation gap g = (E0 − E*)/(E_rand − E*)**. g ≈ 0 ⇒ muṣḥaf ≈ ground state; g ≈ 1 ⇒ no better than random. Report whatever it is.

**NECESSARY** = E0 significantly below the length-preserving null. **NECESSITY** (unique global min) = **not claimed** — instrument limit; we report the relaxation gap, never uniqueness.

## 6. Unified move-cost = restoring force (this *replaces* the seam probes)
For each sūra i: ΔE_i(p) = energy change of moving i to slot p. Its slot is an **equilibrium** iff every move raises E (a local energy well). Per-node "bond tension" falls out of the **one** global energy → a single coherent pinning map, now *derived*, not a separate test.

## 7. Emergent groups (same matrix, no new probe)
Spectral/modularity communities of A → do they reproduce known families (Ḥawāmīm 40–46, Musabbiḥāt, the 7 ṭiwāl, the mufaṣṣal)? Cross-check that the *same* field carries the documented structure.

## 8. Confound controls & nulls
- length: A length-normalized **and** length-preserving null (§5b) — the one that matters.
- de-risk: trim top-bond pairs, re-test (distributed vs a few).
- substrate honesty: A is lexical; convergence with a **non-lexical** A (echo / phonetic) is the upgrade, added as another energy term — same object.

## 9. Failure modes (declared before running — no spin)
- If E0 is **not** below the length-null ⇒ order is *not* an attraction-equilibrium beyond length. Report the null, indict the instrument per BASE-TRUTH, **do not rescue**.
- 1-D distance on a linear muṣḥaf is the model's strong assumption (apt: the book *is* linear and read in order).
- Best attainable grade here = **NECESSARY**; NECESSITY stays the asymptote.

## 10. Outputs
(i) E0, z(random), z(length-null), relaxation gap g; (ii) one unified per-sūra restoring-force / pinning map; (iii) emergent communities vs known groups; (iv) one figure — the attraction graph laid out, actual order vs energy-min order.
