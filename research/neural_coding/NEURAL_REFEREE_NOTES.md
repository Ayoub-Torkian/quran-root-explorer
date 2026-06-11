# Internal referee report — Neural pilot (NEURAL_PILOT.md)

_Adversarial self-review, 2026-06-09, in the same spirit as the genome `REFEREE_NOTES.md`. Role:
a skeptical reviewer at a computational-neuroimaging or methods venue. Goal: find every reason to
reject, then say what fixes it. Includes a self-critique of our own specificity claim._

## Summary judgment
The pilot is honest, well-controlled, and reproducible, and its *methodological* thesis (one
validated discipline yielding differentiated, trustworthy verdicts) is sound. But as an **empirical
neuroscience** contribution it is thin and rests on raw, un-preprocessed data, and one of our own
headline interpretations (the specificity "failure") is over-read. Verdict: **major revision**;
publishable as a *methods/registered-report-style* note, not as an empirical finding.

## Major concerns

**M1 — Novelty. The empirical effect is already known; the only new thing is the discipline.**
Speech-envelope tracking in auditory cortex is established (e.g., Ding & Simon; Hamilton et al.).
With content-specificity *failing* (§3.2/N6) and the dissociation inconclusive, there is no new
empirical claim. The paper must be framed honestly as a **methods demonstration** — porting the
genome programme's controls and showing they catch over-claims on real neural data — not as "the
brain tracks speech." Overclaiming empirical novelty would (rightly) draw rejection.

**M2 — Our specificity interpretation is over-read (self-critique).** We concluded the effect is
"not stimulus-specific" because a different story's envelope (tunnel) predicts Pieman BOLD equally
(real 0.0368 ≈ mismatch 0.0346, p = 0.49). A sharp reviewer will note two problems:
(a) **It is partly expected.** Any two speech envelopes share coarse spectro-temporal statistics, and
after HRF low-pass + TR downsampling the predictable BOLD component is dominated by *slow* structure
that a lag-optimized mismatch envelope can fit. So "predicts equally" does not cleanly establish
"no content-specific code" — it conflates content with the slow shared envelope.
(b) **It cuts deeper than we admitted.** If a mismatched story predicts as well as the real one,
the predictable signal may be largely coarse/slow shared structure (overall speech arc, intro,
arousal/drift), which would *temper even the real-vs-phase-floor positive* — the effect might not be
fine-grained auditory tracking at all. The honest statement is narrower: *the cross-run-predictable
component is not carried by Pieman-specific moment-to-moment envelope structure; its nature (slow
confound vs coarse auditory response) is unresolved on this data.* **Fix:** high-pass the
features/BOLD more aggressively and add motion/physio nuisance regressors (needs preprocessing);
report whether any prediction survives at faster timescales; and use a proper specificity design
(inter-subject: model predicts a held-out subject's BOLD on the *same* story but not on a *different*
story). Until then, the specificity section should be stated as a limitation, not a finding.

**M3 — Everything rests on raw, un-fMRIPrepped data.** No motion correction, no field-map/distortion
correction, no anatomical normalization; cross-run reliability is computed on unrealigned native
volumes (a conservative but noisy ceiling). The semantic null and the dissociation are explicitly
gated on this. **Fix:** fMRIPrep on the 14 subjects; re-run unchanged. This is the single highest-
value action and converts the pilot from "suggestive" to "submittable."

**M4 — Researcher degrees of freedom in the lag search.** A best-lag search per subject and per
feature set adds DOF; the phase-shuffle floor mitigates but does not eliminate it (the floor was not
itself lag-optimized — see genome-style fairness concerns). **Fix:** pre-register a single HRF lag
(or fit one lag on training data only) and report lag as a nuisance, not a tuned parameter.

**M5 — Ceiling and effect-size framing.** "% of ceiling variance" uses inter-run reliability on
unrealigned data as the denominator; this is rough and inflates apparent effect sizes when
reliability is low. **Fix:** estimate the ceiling after realignment, and report raw cross-run R²
alongside the normalized number.

## Minor
- Single dataset (Narratives Pieman), single stimulus; generalization untested.
- Crude 16-band acoustic features and word-level (not phoneme/spectrotemporal-receptive-field)
  features; an SRF or modern model would be the standard.
- Semantic features are GloVe→PCA-12; contemporary work uses contextual LLM embeddings.
- n = 14 (6 of 20 requested subjects lacked Pieman runs) — fine for a pilot, modest for a claim.
- Whisper word timings are unverified against a gold alignment.

## What is genuinely strong (keep)
The discipline and its honesty: a validated planted positive control (N1); a replicated effect with
a real significance test (N4); a robust *null* reported as such (N5); a reliability/margin gate that
**refused** a false-positive dissociation flag (§3.4); and — to our credit and our cost — a
specificity control that forced us to *narrow our own positive*. The reproducibility (scripts,
per-run JSON, figures) is complete.

## Routes (LOCKED protocol: 3–5, recommend 1)
1. **Reframe as a methods/registered-report note** (no new data): retitle to foreground the
   discipline; demote the acoustic result to "a real but coarse, non-content-specific effect";
   move the specificity section to Limitations with the M2 caveat; state the semantic null and the
   refused dissociation as demonstrations of the controls. *Pro:* honest, submittable now, costs
   nothing. *Con:* not an empirical neuro finding.
2. **fMRIPrep the 14 subjects, then re-run** (engines unchanged): gives content-specificity its
   fair test, the language-network semantic ROI test, and a trustworthy dissociation. *Pro:* turns
   it into a real empirical contribution. *Con:* hours of compute per subject; a deliberate project.
3. **Add an inter-subject specificity design** on the existing raw data (predict subject B's BOLD
   from subject A's envelope-model, same vs different story). *Pro:* cheap, sharpens M2. *Con:* still
   raw data; partial.
4. **Drop the empirical arc; fold the neural section into the genome methods paper** as a one-figure
   "the same discipline on a non-flat target" vignette. *Pro:* one clean paper. *Con:* loses detail.

**Recommendation: Route 1 now, Route 2 next.** Reframe the pilot honestly as a methods note (which
fixes M1 and M2 by stating them, and is submittable as-is), and schedule fMRIPrep (Route 2) as the
deliberate experiment that would make the empirical claims real. Route 3 is a worthwhile cheap
add-on to M2 if the appetite is to keep working on raw data. The throughline to protect at all
costs is the one the pilot already embodies: report exactly what the controls support — including
when, as in §3.2/N6, the control narrows our own result.
