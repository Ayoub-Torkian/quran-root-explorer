# PIPELINE — the gradual Word→Act transduction (stage by stage)

_2026-06-08. Refines ROUTE_A_SPEC.md. Principle (user): nature is gradual — do not jump
from characters to protein. Mirror the central dogma + processing as discrete stages,
each with its own transformation, its own free/fixed status, and its own checkpoint
validated against real biology. The end is a folded protein, but the path is the point._

## Why staged (not a single substitution)

A one-shot char→amino-acid map ignores everything biology actually does: transcription,
choosing a reading frame, finding an open reading frame (ORF), splicing/expression,
translation, folding, maturation. Each is a real step that a real gene passes and random
sequence usually fails. Staging turns a single fragile yes/no into a **cascade of
checkpoints** — far more diagnostic, far more faithful, far harder to fake.

## The stages

| # | Biology (Act) | Word-side analogue | Free / Fixed | Checkpoint (benchmark at this stage) |
|---|---|---|---|---|
| A | Genome (DNA) | char → nucleotides (3 nt/char) | **FREE**: char→codon map (MC-searched) | GC%, k-mer spectra, long-range structure, blastn vs genome (this is the Route-B level) |
| B | Transcription → pre-mRNA | T→U on the coding strand | FIXED | well-formed RNA; choose strand (1 of 2) |
| C | Processing / **expression** → mature mRNA | reading-frame + ORF selection (and, later, splice-motif intron removal) | **CONTEXT** (pre-declared) | does a valid ORF exist? start (AUG) … in-frame stop, ≥ length threshold. Real CDS pass; random rarely does |
| D | Translation → polypeptide | ORF → amino acids via the standard code | FIXED (the validated genetic code) | AA composition vs proteome; dipeptide bias; blastp vs SwissProt |
| E | Folding | polypeptide → 3-D structure | FIXED oracle (ESMFold/AlphaFold) | pLDDT / stable fold vs real-protein positives & random negatives |
| F | Maturation / PTM | signal-peptide cleavage, etc. | optional, pre-declared | functional plausibility (v2; skip in v1) |

Only **Stage A** carries the searched free parameter. **Stage C** carries the *context/
expression* freedom (which frame, which strand, ORF length, later splice rules) — and per
CHALLENGES.md these contexts are **enumerated in advance** and the family is corrected, so
"wrong context" can never become an unfalsifiable escape. Everything else is fixed biology.

## Start sites = Sūra/Āyah boundaries (pre-declared reading rule)

Rather than scanning for arbitrary ATG starts, anchor ORF start sites at the text's own
structure: **each Āyah (or Sūra) is a transcription/translation unit** — translation begins
at its boundary and runs to its end or the first in-frame stop. Mapping: Āyah ≈ gene/ORF,
Sūra ≈ operon / chromosomal region, the whole Qur'ān ≈ genome. This *reduces* degrees of
freedom (principled, pre-declared) instead of adding them, and is falsifiable.

**Depends on a decision we must make first:** is a character a **codon** (3 nt → frame is
already fixed, so this is purely a *start-site* rule) or a **base** (3 chars → codon, so the
frame genuinely has 3 options and the Sūra/Āyah boundary *chooses the frame*)? Decide and
pre-register char=codon vs char=base before using this rule.

Caveats (pre-registration): Āyah lengths (few words → long) mostly differ from protein
lengths (~50–1000s aa) — check first how many Āyāt even reach the ~50-aa ORF floor; the rest
are simply "not expressed" (too short), which is a real outcome. Pre-declare Sūra vs Āyah vs
both and correct across that family. Controls get the IDENTICAL segmentation (shuffle within
Āyah; segment control texts the same way).

## Expressibility — MEASURED (2026-06-08), `scripts/expressibility.py`

Data-driven, no mapping search, no a-priori granularity choice. From the actual Qur'an
(6,236 verses; consonantal alphabet = 31; āyah median 43 chars, sūra median ~1,451):

| option | peptide aa | %āyāt ≥50aa | %āyāt ≥100aa | %sūras ≥50aa |
|---|---|---|---|---|
| char = codon | N chars | **42.8** | 11.0 | 98.2 |
| 2 chars = codon | N/2 | 11.0 | 0.9 | 91.2 |
| char = base | N/3 | 2.6 | 0.1 | 86.0 |

**"Is all text expressible?" — measured: no.** Under char=codon ~43% of āyāt clear the
50-aa floor (~2,670 āyāt; ~686 reach 100 aa); the rest are too short → "not expressed"
(a real outcome). char=base nearly eliminates āyāt-level expressibility (2.6%) — only the
sūra level survives, but that is just 114 units (low power). 2-chars=codon sits between.
The data does **not** pick a granularity; it sizes the testable set for each, which is what
decides whether a route has enough units to ever reach high statistical confidence. All
options stay on the table and get run through the full cascade vs the control battery.

## The expression idea, placed correctly

"Not all of it is expressed; expression is contextual" lives at **Stage C**. In real cells
the same DNA yields different products by frame, strand, and splicing. So expression here =
the pre-declared set of reading rules under which a unit may (or may not) yield a viable
ORF. A unit that yields no ORF in any declared context is simply "not expressed" — which is
a real outcome, not a failure to be explained away.

## Checkpoints are gated AND scored

Two readings at each stage:
- **Gate** (pass/fail): e.g. Stage C — is there an ORF ≥ threshold? No ORF ⇒ the unit drops
  out here (not expressed), exactly as for non-coding DNA.
- **Score** (continuous): e.g. Stage D blastp bit-score, Stage E pLDDT — carried forward for
  the statistical comparison.

A candidate that survives the whole cascade is rare and meaningful **only if** it survives
more often / scores higher than the identical pipeline run on the control battery.

## Validation on real samples at EVERY stage (both ends)

Before judging any Qur'an-derived sequence, run **known answers** through the same stages:
- **Act-end positive controls:** real human CDS → must pass Stage C (long ORF, by
  construction), translate to protein-like AA stats (Stage D), and fold (Stage E, high pLDDT).
- **Negative controls:** shuffled CDS / random DNA → should fail early (no clean long ORF) or
  mid (non-protein AA stats) or at folding.
- **Word-end baseline:** real text under a naive map → see where it drops out of the cascade.
This calibrates each checkpoint's threshold on real biology. (`route_a_calibration.py` does
the Stage-D part on CPU today; Stage C ORF-finding and Stage E folding extend it.)

## The null is run stage-aware

The symmetric control search (shuffled Qur'an, other-language texts, random) is pushed
through the **identical cascade**. Report, per stage: what fraction of units survive the
gate, and the score distribution of survivors — Qur'an vs each control. A real signal must
show up as Qur'an surviving/scoring above controls **at the late stages** (ORF→protein→fold),
not just stage A.

## Compute (per ROUTE_A_SPEC §11)
Stages A–D and the gates: CPU, offline (ORF scan, translation, DIAMOND/blastp, all stats).
Stage E folding: GPU, applied only to the small set of cascade survivors (Qur'an + control
+ held-out finalists). The cascade itself *shrinks* the GPU load — most candidates drop out
before folding, exactly as most DNA is never translated.

## Going backward: work in the EXPRESSED subspace (a simplification to test)

Reverse-translating a protein recovers the **CDS — the expressed coding portion only**
(introns/UTRs are unrecoverable). So working from the protein/CDS skips modeling
transcription, splicing, and ORF-finding — you are already in the expressed subspace.
Stage B becomes trivial, most of Stage C is bypassed.

Caveats to pre-register:
- **Reverse translation is non-unique** (degenerate code: 1 AA → up to 6 codons). Protein
  → DNA is a *set*. Fix it with a pre-declared codon rule (human codon-usage / most-frequent
  codon); do NOT search synonymous codons (that is a hidden data-dredge lever).
- **Tradeoff:** the expressed-subspace route *assumes* expression, so it gives up the
  Stage-C ORF gate (a strong, hard-to-fake checkpoint, coverage 1.00 vs 0.27). It leans more
  on folding / proteome-match. ⇒ keep BOTH routes and compare which carries signal:
  forward (char→codon→ORF→protein) vs backward (expressed-subspace, char↔AA direct).
- **Granularity it forces:** the natural unit becomes char↔amino-acid (1 char = 1 residue),
  many-to-one (31→20) — breaks one-to-one. Either accept many-to-one, or keep char→codon
  (one-to-one) and let the fixed code reduce to AA. Both stay on the table.
- **Bonus experiment:** start from REAL proteins (guaranteed expressed + foldable),
  reverse-translate (fixed codon rule) → CDS → chars, and test resemblance to Qur'an. The
  "Act" end is then unimpeachably real; same control battery applies.

## Stage C — BUILT & validated (2026-06-08), `scripts/stage_c_orf.py`

6-frame ORF scan (ATG…in-frame stop). Validated on real human CDS vs controls:

| input | longest ORF (aa) | coverage | pass ≥50aa |
|---|---|---|---|
| real CDS | mean 328 (max 609) | **1.00** | 6/6 |
| shuffled CDS | mean 66 | 0.27 | 5/6 |
| random matched | mean 79 (max 126) | 0.27 | 4/6 |

Clean separation. **Coverage** (longest ORF ÷ length) is the headline discriminator
(real ~1.00 vs ~0.27); the absolute longest ORF also separates (328 vs ~70). Lesson:
a bare 50-aa gate is too lenient — random DNA can throw a 50–126 aa ORF — so the length
gate must be set at the **null's upper tail** (calibrated on these shuffled/random
controls), and coverage used alongside. The component exposes `gate(dna, min_aa, min_cov)`
for the cascade.

## Build order (remaining)
1. ~~Stage C ORF engine + gate~~ DONE (above).
2. Wire A→B→C→D with the gates; run the control battery through it (CPU).
3. Plug Stage E (ESMFold) for survivors on a GPU box.
4. Train/held-out split + max-statistic null across the whole cascade.

## Honest prior (unchanged)
Route B + the structure-preservation argument still predict a calibrated null. But the
staged design is the faithful, falsifiable form of the idea, and a cascade of biological
checkpoints is exactly what would make a positive — if it came — hard to dismiss.
