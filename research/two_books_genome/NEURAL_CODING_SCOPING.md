# Scoping the pivot: language ↔ neural code (and why it is real where text↔genome was not)

_2026-06-09. Critical scoping of the direction you raised: "language → electrochemical
transduction … both language and the genome emanate from that foundation." Written as peer
review — including where I push back. Citations are from memory and must be verified before any
manuscript use._

## The claim, split into a strong part and a weak part

You proposed a chain: **language → neurons → (eventually) genome**. These are not equal.

**Strong, real, and testable: language ↔ neural code.** Language is physically processed by neural
circuits; text/speech is transduced into spike trains and distributed cortical activity. There is a
genuine, measurable mapping from linguistic structure to neural activity, and a mature field already
quantifies it with *exactly the controls we just built*: held-out prediction, noise-ceiling floors,
and positive/negative region controls. Representative results (verify): Huth et al. 2016 (semantic
maps across cortex); Pereira et al. 2018 (decoding meaning from fMRI); Schrimpf et al. 2021
(LLM embeddings predict the language network near its noise ceiling); Goldstein et al. 2022 (ECoG
next-word prediction aligns with model surprisal); Caucheteux & King 2022; LeBel et al. 2023 and the
Narratives corpus (Nastase 2021) as open data. Crucially, **the target here is not statistically
flat** — neural responses to language carry rich, structured, predictable variance — so the
flat-target ceiling (C1) that nulled text↔genome does **not** apply.

**Weak, and I'd reject it as stated: language ↔ genome via neurons.** The inference "because both
emanate from biology, there is a road from language to the genome" does not hold at the sequence
level. The genome specifies a *developmental program* that builds language-capable brains; it does
not contain linguistic content, and there is no codon-like cipher from words to DNA. The
language↔genome relationship is **evolutionary/developmental, not a sequence correspondence** — the
same reason our text→genome mapping was null six different ways. So I would not pursue a
language→neuron→genome sequence bridge; it repeats the error we just documented. The honest, rich
object is the **language ↔ neural-representation** link, full stop.

## What a first falsifiable step looks like (and why our framework transfers)

The encoding-model paradigm maps onto our six controls almost one-to-one:

| our control | neural-encoding analogue |
|---|---|
| floor (1) | predict held-out neural responses; compare to a shuffled-feature / phase-randomized floor |
| out-of-sample (2) | fit weights on some stories, test on unseen stories |
| convergence (3) | do independent subjects/sessions yield the same feature→cortex mapping? |
| replication (4) | across subjects and datasets, with significance vs the noise ceiling |
| multiplicity (5) | whole-brain voxelwise FDR correction |
| **positive control (6)** | low-level acoustic/letter features must predict early sensory cortex; semantic features predict association cortex — a built-in "does the instrument fire" check |

That last row is why this is a good fit: the field already has a natural positive control, which is
precisely the thing whose absence sank our first genome attempt.

## Critical caveats (peer-review, before anyone gets excited)

1. **Predictivity ≠ "the brain computes the model."** Encoding-model fit shows shared variance, not
   mechanism; LLM-features-predict-cortex has been over-read. State it as representational
   alignment, not identity.
2. **Compute/data step up.** fMRI/ECoG datasets are GB-scale; ridge encoding models and noise-
   ceiling estimation are heavier than the CPU toys here (though still laptop-feasible on one
   subject). This is a new project, not an afternoon.
3. **No genome bridge.** Resist re-attaching the genome; that is the weak limb above.
4. **It's a different field with deep priors.** We would be entrants to a mature literature; the
   contribution must be methodological (e.g., porting the convergence + planted-positive-control
   discipline), not "we discovered language is in the brain."

## Routes (LOCKED protocol: 3–5, recommend 1)

1. **Replicate one published encoding result on one open dataset** (e.g., LLM-feature → language-
   network prediction on a single Narratives/LeBel subject), with our floor + held-out + positive-
   control discipline. *Pro:* concrete, falsifiable, non-flat target, reuses our framework, has a
   built-in positive control. *Con:* enters a crowded field; heavier data.
2. **Theory-only conceptual bridge** language→neural code (no genome). *Pro:* cheap. *Con:* adds
   little to an existing literature; no new evidence.
3. **Pursue the language→neuron→genome bridge.** *Pro:* matches the original "two books" intuition.
   *Con:* the weak limb — no sequence-level mechanism; would repeat the documented null. **Advised
   against.**
4. **Stay with the genome paper; treat neural coding as future work.** *Pro:* finishes what's done.
   *Con:* defers the one direction with a non-flat target.

**Recommendation: R1 — a single-dataset encoding-model replication, framed as porting our
controls (especially the planted positive control) to a target that actually carries signal.** It
is the only proposed direction that (i) has a real mechanism, (ii) faces a non-flat target where a
positive result is even possible, and (iii) reuses everything we built. I would explicitly *not*
carry the genome along (R3): the honest lesson of this whole program is that "both emanate from
biology" is not a sequence correspondence. If the goal right now is to *publish*, finish the genome
methods paper first and open R1 as the next project; if the goal is to *explore*, R1 is the door.
