# Methodology — Letters→Codons→Expressed-Genome (pre-registration draft)

_Drafted 2026-06-08. Status: DESIGN, pre-pilot. This is a pre-registration: the
analysis and its null are fixed in writing BEFORE results are seen. Read
`CHALLENGES.md` alongside this — it is not optional._

---

## 0. The governing rule

The alignment between language, genes, and proteins is a **tested output, never an
assumed input.** The deliverable is a *verdict* ("Qur'anic units do / do not
correspond to expressed coding sequences beyond chance and language structure"),
not a list of matches. **A null is a successful, reportable result.**

---

## AMENDMENT A1 (2026-06-08) — scope: language-general & multimodal

Pre-registration amendments are timestamped, not silently rewritten. This changes
the scope set out below; where they conflict, A1 governs.

- **Scope.** The claim is NO LONGER Qur'an-specific. The hypothesis is that **natural
  language as a modality** corresponds to genomic/protein sequence beyond chance AND
  beyond generic structural resemblance. The Qur'an is one language sample among many.
- **Other books flip role.** "Other natural-language texts" (Shakespeare, etc.) move
  OUT of the control battery and become **positive replication data** — more samples
  of the language modality. They are no longer a specificity control.
- **New mandatory control — structure-matched surrogate genome.** Because both language
  and genome are structured (low-entropy, repetitive), two structured sequences align
  better than random for generic reasons. To show a *specific* language↔biology link,
  language must align to the **real CDS better than to a shuffled CDS** (same biological
  composition, destroyed biological order), and ideally better than to a non-biological
  structured signal (e.g. a Markov surrogate matched to language n-gram structure).
  Beating only i.i.d. random now proves nothing.
- **Method fork (governs §5).** Two routes:
  - **(A)** searched letter→codon mapping + BLAST (as specified below).
  - **(B)** mapping-free **multimodal** comparison: k-mer spectra, entropy rate,
    long-range correlation decay, Zipf exponents, and/or a learned cross-modal
    embedding (contrastive). Stronger and Bible-Code-free for the *establishment* goal.
  Default recommendation: **B establishes correspondence; A is a downstream test.**
  Awaiting user's choice of A / B / B-then-A before the pilot is built.

---

## 1. Operational hypothesis (falsifiable)

> Under a one-to-one mapping from the 28 Arabic letters to DNA codons, do Qur'anic
> text units, when mapped to DNA, align (blastn) to **expressed human coding
> sequences** (RefSeq CDS) better than (a) random composition-matched sequences,
> (b) within-unit shuffles, and (c) other natural-language texts — when **all four
> arms receive the identical mapping search**?

A result counts only if the Qur'an beats **all three** baselines. Beating (a) alone
is the low-complexity artifact signature, not a finding.

---

## 2. Locked decisions (from the design dialogue — see IDEATION_LOG.md)

| Decision | Choice | Note |
|---|---|---|
| Direction | letters → codons → DNA | one-to-one feasible (28 ≤ 64) |
| Cardinality | one-to-one (injective) | minimal freedom; AA track is separate |
| Mapping chosen by | Monte Carlo search | ⇒ symmetric search on all baselines (§5) |
| Match metric | significant blastn alignment (e-value / bit-score) | self-calibrating |
| Database | RefSeq **CDS** = expressed/translated coding seqs | sidesteps introns/splicing/non-expression |
| Baselines | random-matched + within-shuffle + other-books (all mandatory) | §5–6 |
| Primary unit | āyah and larger (multi-āyah, short sūrah) | roots EXCLUDED (too short); kept as negative control |
| First pass | **pilot** = pipeline bring-up, NOT results | §7 |

## 3. The "expressed" simplification (the user's refinement)

To avoid genomic complications (introns, alternative splicing, RNA editing,
non-expression), restrict the target to **expressed coding sequences** — the codons
that actually get translated. RefSeq curated CDS implements this directly, so the
database choice already encodes the refinement. Honest caveats: "expressed" is
strictly tissue/condition-specific (true expression = GTEx/RNA-seq); RNA editing
and post-translational modification are not captured. Canonical CDS is a pragmatic
proxy, stated as such.

## 4. Two separate tracks (do NOT merge their statistics)

- **Codon track (primary, one-to-one):** letters→codons, blastn vs CDS. Clean
  constraints; this is the starter.
- **Amino-acid track (secondary, NOT one-to-one):** letters→amino acids is
  necessarily many-to-one (28 > 20); blastp vs proteome. Weaker constraints ⇒ more
  freedom ⇒ a separate pre-registration and its own null. "AA correspondence can
  differ from codon correspondence" is fine — but they are different experiments and
  the family is corrected for (§6).

## 5. Procedure (run identically on Qur'an AND on every baseline)

M = Monte Carlo mappings sampled (fixed in advance, e.g. 10,000). The injective
space is ≈10⁴⁸, so M is a tiny sample — acceptable **only because the identical
M-sample search runs on the baselines too.**

```
for a sequence-set U (Qur'an, or one baseline surrogate set):
  for m in 1..M:                         # sampled injective letter→codon maps
    s = []
    for unit u in U:
      dna = codon_map(m, letters(u))     # 3N-nt DNA
      hit = blastn(dna, RefSeq_CDS)      # best local alignment; -dust ON
      s.append(-log10(hit.evalue))
    S[m] = aggregate(s)                  # default: # units with e < 1e-3
  S_best(U) = max_m S[m]
```

**Primary statistic:** `S_best(Qur'an)`.

**Null battery (each mandatory, K ≥ 1,000 surrogate sets each):**
- (a) **random matched** — same length & letter composition, random order. NECESSARY, not sufficient.
- (b) **within-unit shuffle** — scramble each āyah's own letters, re-map. Controls composition AND low-complexity.
- (c) **other natural-language books** — Moby-Dick / War-and-Peace passages, same search. Tests Qur'an-SPECIFICITY — the thesis-relevant claim.

**p-value:** computed against each baseline; the result is the *minimum* signal across
the three (beats all, or it does not count).

## 6. Multiplicity & robustness (the anti-Bible-Code core)

- Mapping search → absorbed by the symmetric max-statistic.
- Aggregate primary statistic → no per-āyah multiplicity in the headline.
- **Family-wise correction across all "spectrums"** — every track (codon/AA), species,
  and unit-scale is another test; correct across the whole family (the "works in all
  landscapes" ambition is where look-elsewhere creeps in).
- **Held-out validation** — freeze the winning mapping on a TRAIN split of units; report
  only on an untouched TEST split. A result that does not transfer is noise.
- **Robustness replicates** — vary RNG seed, M, and the frozen normalization rule; a
  verdict fragile to a reasonable change is rejected.
- **Pre-registration timestamp + released code/seeds/data** → independent replication.

## 7. Pilot vs confirmation (the user's "simplify, get data, then refine")

- **Pilot:** small CDS subset, handful of āyāt, small M. Purpose = the pipeline runs,
  the null calibrates, the plumbing is correct. **Pilot produces NO claims.** Any
  apparent correspondence in the pilot is a hypothesis to be tested, not a result.
- **Confirmation:** full pre-registered run with the baseline battery, held-out split,
  multiplicity correction, robustness replicates.

## 8. Optional secondary (only if §5 battery is fully positive)

- Translate mapped DNA in-frame; does it yield plausible ORFs (start…stop, no
  premature stops) above baseline?

## 9. Implementation

**Offline (BLAST cannot run live):** build local BLAST DB; batch the M×|U| blastn
calls (parallelise; this is the cost); emit a results JSON (observed stat, null
distributions, p-values per baseline, winning mapping, held-out result, robustness)
mirroring `mathani_twins.json`.

**In the app:** a NEW self-contained lens (like Structural Twins) that loads only the
precomputed JSON — never the live corpus or BLAST. Honest verdict card: observed vs
each null, the explicit "mapping was searched; baselines got the same search" caveat,
and the Bible-Code precedent. If null: say so plainly as the finding.

## 10. Verdict table

- **Positive + specific:** beats all three baselines, transfers to held-out split,
  survives robustness, AND beats other books. → Interesting, still correlational;
  requires a stated mechanism before any "two books" claim is voiced.
- **Beats (a) only:** low-complexity artifact. → Null for the thesis.
- **Null:** does not beat the battery. → The finding. Expected outcome; not a failure.
