# SCENARIOS — the multimodal sweep and what "improvement" must mean

_2026-06-08. The approach is a data-driven search over many scenarios (direction,
granularity, unit, mapping, context). This file defines the scenario space, the ONE
objective that may be monitored, and the discipline that keeps the sweep honest._

## The scenario space (all parameters, pre-declared)

| axis | options |
|---|---|
| **direction** | forward (char→protein), backward (protein→CDS→char, expressed-subspace), mixed |
| **granularity** | 1 char = codon · 2 chars = codon · 3 chars = codon (char=base) · … (k chars → m codons) |
| **unit** | āyah · multi-āyah block · sūra |
| **mapping** | Monte-Carlo search over char↔codon (or char↔AA) maps |
| **context** | reading frame · strand · start-site (āyah/sūra boundary) · splice rule · codon-usage rule (for reverse translation) |

Every point in this space is a *scenario*. The sweep tests many; that is fine — but the
number tested is part of the statistics (see Discipline).

## The objective you may monitor — and the one you may NOT

**MAY NOT monitor:** raw resemblance of the generated sequence to real proteins/genes.
Over this space, raw resemblance climbs by chance; "improving" it is overfitting +
optional stopping (the Bible-Code failure mode). Watching it go up proves nothing.

**MUST monitor — the margin Δ over the control battery, on held-out data:**

    Δ(scenario) = score(held-out Qur'an, scenario)  −  max_control score(control, scenario)

where `score` is the cascade outcome (Stage-C ORF pass-rate → proteome-match → foldability),
and the controls (shuffled Qur'an, other-language texts, random) are run through the
**identical** scenario. Δ is the only "improvement" that searching harder cannot inflate —
the controls are searched exactly as hard. Persevere while Δ rises AND holds out-of-sample;
a flat Δ≈0 across scenarios IS the result (null), not a reason to keep going.

## Discipline (non-negotiable — see CHALLENGES.md)

1. **Sweep inside the null.** Max-statistic taken across the whole scenario space, applied
   symmetrically to controls. Track the total scenarios evaluated; correct family-wise (FDR).
2. **Pre-set budget + stopping rule.** Fix the compute budget and stopping criterion before
   starting. No "keep trying until it works."
3. **Held-out validation of every winner.** The margin must survive on data the search never
   saw (train/test split frozen up front).
4. **Robustness.** Each candidate winner re-checked across ≥2 seeds and an alternate
   normalization. Fragile ⇒ rejected.

## Monitoring (the "improvement degree" dashboard)

A leaderboard, per scenario: Δ with its 95% CI, the raw scores (for diagnostics only,
never as the criterion), survival flags (held-out, robustness), and the running family-wise
threshold. "Improvement toward the objective" = Δ trending up and clearing the corrected
threshold on held-out data. Diagnostics (raw resemblance) are shown but explicitly labelled
non-evidential.

## Harness design (to build)

- `Scenario` config (direction, granularity, unit, mapping params, context).
- `run_scenario(scenario, corpus)` → cascade score (reuses stage_c_orf, translation,
  proteome-match; folding only for survivors).
- `evaluate(scenario)` → runs Qur'an + the full control battery, returns Δ and CI on the
  held-out split.
- `sweep(space, budget)` → iterates scenarios under the budget, logs the leaderboard,
  applies family-wise correction, flags survivors for the GPU folding confirmation.

## Honest expectation

Route B + structure-preservation predict Δ≈0 throughout (null). The harness is built so that
outcome is reported cleanly — and so that, if some scenario *does* produce a held-out,
control-beating, correction-surviving Δ, it is believable precisely because the monitor
tracked the calibrated margin, not the seductive raw fit.
