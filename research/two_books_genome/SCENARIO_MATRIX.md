# Scenario matrix — exhaustive enumeration + critical triage

_2026-06-09. Answers: "we ran 1-char→1-codon; how about 3-char→1-codon? what other
scenarios?" and "exhaust many scenarios." Every cell of the mapping-design space is listed,
scored, and triaged. Numbers are measured from our corpora, not assumed._

## Three umbrella constraints that pre-decide most cells

Before listing scenarios, three results already in hand bound the whole space. A scenario is
only worth running if it escapes all three.

**C1 — Flat-target ceiling (NEW, from today's positive control).** We planted a *known*
bijection cipher into real protein space and tried to recover it with the textbook instrument
(bijection swap-SA maximizing trigram log-likelihood — how substitution ciphers are actually
broken). Recovery reached only ~0.30 and did **not** separate from its shuffled floor or from
the Qur'ān (all ≈0.25). Reason: protein/genome sequence is **statistically flat at low n-gram
orders** — it lacks the strong, peaked n-gram regularities that make language ciphers crackable.
**Consequence:** *no* substitution-style char/k-gram→codon/AA mapping is reliably identifiable,
no matter how clean the data — the instrument's sensitivity floor sits above the signal.

**C2 — Parameter explosion (identifiability).** Measured on the 330,719-letter Qur'ān skeleton:

| Word unit | distinct units | tokens | data/params ratio | identifiable? |
|---|---|---|---|---|
| 1-char (letter) | 31 | 330,719 | 10,668 | yes (but capped by C1) |
| 2-char (digraph) | 867 | 165,359 | 191 | marginal |
| **3-char (trigraph)** | **11,260** | **110,239** | **~10** | **no — ~half are hapax** |
| word / ayah / sūra | 10⁴–10⁵ | ≤77k / 6,236 | <1 | no |

A map with more free parameters than data points fits noise by construction — the Bible-Code
trap, amplified.

**C3 — Structural mismatch (Route B, replicated).** Genome MI-decay γ ≈ 0.92 (long memory) vs
every tested language 1.4–2.5 (short memory), non-overlapping CIs. A one-to-one mapping only
relabels symbols and cannot change this — so no substitution map of any granularity can make the
two share structure.

## The full cross-product (Word-unit × Act-unit × direction × objective)

Verdict key: **RUN** = viable, worth a controlled run · **GATE** = run only with extra controls /
new data · **TRAP** = overfit/multiplicity risk, avoid unless heavily controlled · **DONE** =
already run, null · **DOOMED** = killed by C1–C3 regardless of effort.

| # | Word unit → Act unit | direction | objective | params/data | killed by | verdict |
|---|---|---|---|---|---|---|
| 1 | letter → amino acid | fwd | dipeptide / trigram / k-mer | fine | C1, C3 | **DONE** (null) |
| 2 | letter → codon | fwd | tblastx / k-mer | fine | C1, C3 | **DONE** (null) |
| 3 | letter → nucleotide | fwd | blastn | fine | C1, C3 | DOOMED (sub-codon, even flatter) |
| 4 | digraph → codon | fwd | tblastx / convergence | marginal (191) | C1 | GATE (identifiable but flat-target) |
| 5 | **trigraph (3-char) → codon** | fwd | any | **~10, half hapax** | **C2 (+C1)** | **TRAP** (unidentifiable) |
| 6 | **root (triliteral) → codon/AA** | fwd | convergence + BLAST | closed ~1.6k vocab | (escapes C2) | **RUN** (best new lead) |
| 7 | root → gene/protein (whole) | fwd | feature-match | 1.6k → 35k genes | multiplicity | GATE (needs bio prior) |
| 8 | word → gene | fwd | feature-match | ~77k → 35k | C2, multiplicity | TRAP |
| 9 | ayah → gene/protein | fwd | feature-match | 6,236 → 35k | multiplicity | TRAP (Bible-Code at unit level) |
| 10 | sūra → proteome region | fwd | folding / BLAST | 114 → genome | multiplicity | TRAP |
| 11 | any unit, reverse (protein→text) | rev | same | same | C1 | mirrors fwd; no escape |
| 12 | letter/codon, frame = sūra/ayah start | fwd | ORF + tblastx | fine | C1 | GATE-cheap (free knob, already ~S3) |
| 13 | no mapping — structural signatures | — | γ / Hurst / gzip / MI | n/a | — | **RUN-cheap** (extend Route B) |
| 14 | mapping + 3D folding | fwd | ESMFold pLDDT | n=2 done | CPU/GPU | DOOMED to scale on CPU |

## Critical review — the specific question: 3-char → 1-codon

The 3:3 symmetry (three letters ↔ a codon's three nucleotides) is aesthetically appealing, and
"three" echoes the Arabic triliteral root. But as **arbitrary trigraphs** it is the worst cell in
the table, for two compounding reasons:

1. **Unidentifiable (C2).** 11,260 distinct trigraphs, ~110k tokens → ~10 observations per unit on
   average, and roughly half occur only once. You would be assigning a codon to thousands of units
   you have seen once or never — pure overfitting. Any "match" is guaranteed and meaningless; this
   is exactly the Bible-Code failure, scaled up ~360× over the letter case.
2. **Flat target (C1).** Even with infinite data, the protein target is too n-gram-flat for the
   assignment to be pinned down.

So **3-char→1-codon as written is not worth running** — it would manufacture a false positive.

**But the idea has a salvageable, stronger form:** the unit that motivates "three letters" is the
**triliteral root**, a *closed* vocabulary (~1,600–2,000 roots in the Qur'ān, which the app
already segments). Root→codon or root→AA replaces 11,260 noisy trigraphs with ~1,600 well-attested
units, restoring identifiability (escapes C2), and is far better motivated (the root is the
Qur'ān's semantic atom). It still faces C1, so it must ship with its own **planted-root positive
control** and full floor+convergence+replication — but it is the one genuinely new, defensible
granularity left.

## What "exhausting the scenarios" actually shows

Sweeping the whole space, the viable set collapses to three:

- **(a) Root-level mapping** (#6) — the salvage of the 3-char idea; closed vocabulary, motivated,
  identifiable; the only untested substitution granularity with a real chance.
- **(b) Whole-unit→gene correspondence** (#7, #9) — only legitimate *with a pre-registered
  biological prior* to control the 6,236×35,624 multiplicity; otherwise a guaranteed trap.
- **(c) Structural / mapping-invariant battery** (#13) — cheap, already decisive as a null,
  strengthened by adding languages/segments.

Everything finer than a letter (#3) is flatter and worse; everything coarser without a closed
vocabulary (#8–#10) is a multiplicity trap; the reverse direction (#11) mirrors the forward and
escapes nothing; folding at scale (#14) needs a GPU.

## Recommendation (LOCKED protocol: routes → one)

**Routes.** R1 root→codon/AA with a planted-root positive control (salvaged 3-char). R2 digraph→
codon controlled run (#4). R3 whole-unit→gene with a pre-registered prior (#7). R4 stop — declare
the substitution-mapping program closed under C1–C3 and write it up. R5 extend the structural
battery (#13).

**Recommendation: R1 — root→codon/AA, shipped with its own planted-root positive control.**
Rationale against the multivariable context: it is the *only* scenario that simultaneously (i) is
newly untested, (ii) is conceptually motivated rather than a fishing expedition, (iii) escapes the
parameter-explosion trap (C2) via the closed root vocabulary, (iv) reuses the app's existing root
segmentation and our convergence harness, and (v) is CPU-feasible. We attach the planted-root
positive control first so we never again interpret a null without knowing the instrument can fire.
If R1 also returns null, the substitution-mapping program is genuinely exhausted and we pivot to
R3 (bio-prior correspondence) or close it (R4). Note honestly: C1 makes a root-level *substitution*
null the most likely outcome — but R1 is the one remaining test that is worth our credibility to run.
