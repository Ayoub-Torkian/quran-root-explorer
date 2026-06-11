# Internal referee report — MANUSCRIPT_DRAFT.md (v2, methods/perspective)

_Adversarial self-review, 2026-06-09. Role: skeptical reviewer at a methods/stats or
computational-biology venue. Goal: find every reason to reject, then say what fixes it.
Recorded per the publication-grade record-keeping policy._

## Summary judgment
The reframe is the right move and the draft is honest, reproducible, and well-controlled.
But as written it is **not yet acceptable** at a serious venue, for one structural reason
above all: **a framework paper must demonstrate the framework can return a POSITIVE, not only
a null.** Everything else is fixable polish. Verdict: *major revision.*

## Major concerns (would block acceptance)

**M1 — No positive control; sensitivity is untested (the big one).**
The paper proposes a framework and exercises it once, on a hypothesis that returns null at
every stage. A reviewer's first question: *would your framework ever say yes?* As it stands,
a framework that rejects everything is indistinguishable from one whose search is simply too
weak. **Fix:** plant a known mapping into a synthetic text (encode a real CDS via a fixed
char→codon table, embed it in carrier text), then show the pipeline (a) recovers the planted
map via convergence, (b) clears the floor, (c) survives replication. A clean positive on the
planted case + the clean null on the Qur'ān is a *complete* demonstration. Without it, M1 sinks
the paper.

**M2 — The convergence null may be a search-power null, not a true null.**
Simulated annealing over 64^31 is not guaranteed to find the optimum; "independent runs don't
agree" can mean "no universal map exists" OR "the optimizer can't find it." The draft's
"search-effort-invariant" claim (Limitations) is asserted, not shown. **Fix:** same planted-map
control as M1 doubles as the search-adequacy check — if SA recovers a planted map at this M,
the negative is about the data, not the search.

**M3 — Centerpiece statistics are underpowered; "real = shuffled (z=0.00)" is absence of
evidence, not evidence of absence.**
n=5 pairs, real 0.22±0.13 vs shuffled 0.22±0.16. z=0.00 is striking but n=5 cannot exclude a
moderate order effect. A referee will demand an **equivalence test** (e.g., TOST) with a
pre-stated margin, or a proper power statement, and more pairs. **Fix:** raise to n≥20 pairs,
report an equivalence interval, not just a non-significant difference.

**M4 — Cross-alphabet γ comparison confound (28 vs 4 symbols).**
Fig 1 leans on MI-γ to compare a 4-letter genome with ~28-letter scripts. RESULTS.md already
concedes this confound; the manuscript underplays it. The *direction* (genome = longer memory)
is defensible and matches DNA long-range-correlation literature, but a genomics reviewer will
press. **Fix:** add a within-alphabet check (e.g., recode text to 4 symbols, or compare γ on
matched alphabet sizes) and state the confound explicitly in the caption.

**M5 — BLAST comparison has no significance test.**
Δmean 0.74 bits with N=20×6 and uniform (not human-codon-usage) draws, no CI, no null
distribution, no multiplicity handling. "Real ≈ control" is the right read, but a reviewer
wants the distribution and a test, plus codon-usage-weighted draws to match the paper's own
stated method. **Fix:** report the full bit-score distributions + a permutation test; rerun with
a human codon-usage table.

## Minor concerns (revise)

- **m1 Novelty framing.** Floor/held-out/replication/multiplicity are standard good practice;
  only the *convergence test as the operational definition of "a correct mapping exists"* and
  the *synthesis for cross-domain cipher claims* are novel. Say so plainly — claim the synthesis
  + the worked cautionary example, not new statistics. Overclaiming invites a harsh review.
- **m2 Folding (F5) is n=2, one fixed mapping.** Keep it explicitly as a supporting/orthogonal
  check, not evidence; the draft mostly does this.
- **m3 F3 trajectory is illustrative.** Already labeled; consider logging real annealing traces
  so nothing in the figures is schematic.
- **m4 Venue realism.** This is not a Nature paper as a null on a fringe hypothesis. Honest
  homes: a methods/stats venue, a computational-humanities/biology methods journal, or a
  preprint first. The framework + positive control (M1) is what could lift it.
- **m5 Tone/scope.** The theology disclaimer is good; keep the Qur'ān as one instance of a
  general class throughout so the paper reads as method, not apologetics or debunking.

## What is already strong (keep)
Reproducibility (seeds, ledger, scripts, provenance); the discipline of catching and walking
back the 0.58 false positive; the mapping-invariant pre-check as a cheap whole-class refutation;
honest null reporting.

## The decisive next step
M1 (planted-mapping positive control) resolves M1 **and** M2 at once and is the single highest-
leverage addition. Everything else is revision around it.

## Routes (LOCKED protocol: 3–5, recommend 1)
1. **Build the planted-mapping positive control** (resolves M1+M2). CPU-feasible: encode a real
   CDS with a fixed table, embed in carrier text, run the full convergence+floor+replication
   pipeline, show recovery. *Pro:* turns the paper from "rejects one thing" into "validated
   instrument"; directly answers the first referee question. *Con:* a few hours of new code/runs.
2. **Strengthen the centerpiece stats** (M3): n≥20 pairs + equivalence test. *Pro:* hardens the
   headline. *Con:* doesn't address the fatal M1; polishing a result whose instrument is
   unvalidated.
3. **Fix the γ confound** (M4): within-alphabet recoding. *Pro:* closes a genomics-referee
   attack. *Con:* secondary; Fig 1 is already only the pre-check, not the main result.
4. **Rerun BLAST properly** (M5): codon-usage draws + permutation test + distributions. *Pro:*
   faithful to the paper's own objective. *Con:* the loop is already closed; lower marginal value.
5. **Stop and submit as a null/preprint now.** *Pro:* fast. *Con:* M1 means likely desk-reject or
   harsh review at anything but a preprint server.

**Recommendation: Route 1 — build the planted-mapping positive control next.** It is the one
change that converts the manuscript from "a framework that only ever says no" into "a validated
framework that correctly says yes to a true signal and no to this one," and it simultaneously
proves the null is about the data rather than a weak search (M2). Multivariable context favors it:
CPU-only and self-contained (no GPU, no flaky NCBI API), it reuses the existing SA/convergence
harness, and it answers the very first question every reviewer will ask. M3–M5 are revision passes
to run *after* the instrument is validated.
