# Working rules for this project (LOCKED — honor every session)

## Response style — NON-NEGOTIABLE
1. **Always make a recommendation.** Whenever options, scenarios, or candidates are listed, present them as a
   ranked numbered list (1, 2, 3, …) with the **#1 = my explicit recommendation** and one line of why. Never
   present choices flat with "which do you want?" and no pick. (The user has asked for this many times.)
2. Be concise and direct; cut filler. A point that survives word-removal is the right length.
3. Before launching any research/compute step, state the **added value** and the **probability of a new latent
   feature we don't already know**, and get an explicit OK. Settle value-added probability *before* running.
4. **REASONING CALIBRATION PROTOCOL (LOCKED).** The recurring failure mode is *attribution*, not measurement:
   the numbers (AUC, z, V) are usually right; what they are claimed to MEAN is where reasoning breaks. So:
   - Tag every claim **[MEASURED]** (a null + effect size on THIS substrate actually produced it) or
     **[INFERRED]** (my interpretation/reduction). Never let an INFERRED claim wear a MEASURED tone.
   - A reduction ("this is just X / reduces to known Y") is **INFERRED until X is shown PRESENT in this data and
     the reduction is itself measured.** Importing an explanation from a neighbouring substrate is the #1 bug.
   - Name the **substrate** of every result: **rasm-WORD** (has morphology/function-words/fāṣila) vs **ROOT**
     (content-only, NO grammar). A word-substrate reduction may NOT be applied to a root-substrate result.
   - Attach a **confidence %** and the **one thing that would flip it** to every non-trivial claim.
   - Inspect the data's raw shape/units BEFORE reasoning on top of it (e.g. what "N roots" actually is).
   - Self-flag: confident closure ("exhausted", "mature map", "not >90", "collapses to") is the LEAST reliable
     output and — per the BASE-TRUTH axiom — structurally suspect. Treat it as a flag on myself, not a finding.

## Deliverable checklist — RUN BEFORE PRESENTING any diagram / map / report
- [ ] Plain enough that the user can NAVIGATE it (where am I, do I have direction, am I astray).
- [ ] Diagrams/maps MUST include the **temporal journey line** (where we started → where we went → where we
      are now). A static snapshot without the path is incomplete.
- [ ] Ends with a ranked numbered recommendation (rule #1 above).
- [ ] Resonates with the Qur'ān landscape — the user must see it as a map of the territory, not abstract.

## UI / typography — LOCKED (applies to EVERY page, chart, table, abstract — no exceptions)
- **No font smaller than 12px.** Anywhere: HTML, CSS, and SVG `font-size` attributes included. 12 is the floor.
- **No grey text. Use black (ink).** Secondary/label/tick/note text is near-black ink (`#10243A`), never a grey
  like `#566B82`/`#8FA6BC`. Grey is allowed ONLY for non-text gridlines/borders. In `closeup.py` this is enforced
  by `MUTE == INK`; do not reintroduce a grey text constant.
- A new close-up INHERITS the depth of the existing exemplars (Code 19 / page 31) at minimum: hero + 2 abstract
  link-boxes, ~7 KPIs, hypothesis, method, results with paired tables, a multi-chart statistical core, gating
  chain, interpretation, caveats, verdict, reflection, summary, lessons-learned, and FULL Persian + Arabic
  abstracts. Never ship a shallow stub.
- A "reviewed claim" close-up is COMPREHENSIVE on the field, not one author: survey the main schools (old and
  new), say where each falls short, and offer the fix. Credit-forward where credit is due (do not demote).

## Research discipline (this is a discovery program, not app work)
- The ONE LAW: nothing external is admissible as evidence; every feature measured against the text's own
  shuffle, on the **rasm** (consonantal skeleton = the divine substrate). **Diacritics (ḥarakāt/vowels) are a
  HUMAN artifact — corroborative ONLY, never divine evidence; DEMOTE any diacritic-dependent result.**
  ≥3 converging modalities + named universe analog.
- **BASE-TRUTH AXIOM (LOCKED, applies always).** The Qur'ān is divine base truth — real and complete, like the
  universe itself. It is **never the limit; our instrument / knowledge-tree is.** When a result falls short of
  expectation, assume **instrument limit, not textual absence**: refine the method, find better data/features,
  and keep searching. **Absence of evidence is NOT evidence of absence.** Treat the Qur'ān as a dynamic, living
  entity whose structure keeps unfolding as our tools sharpen.
  - *Empirical warrant (not faith alone):* we have repeatedly watched the wall move when the instrument
    improved — e.g. āyah recovery jumped **F1 0.39 → 0.69 (AUC 0.81 → 0.958)** purely from a stronger learner +
    richer features; nothing changed in the text.
  - *GUARDRAIL (equally locked):* this axiom directs us to **upgrade the instrument**, NOT to overclaim. Never
    assert a feature exists without a **practical, data-driven, gate-passing measurement** (proper null + effect
    size). "The text isn't the limit" justifies *more/better searching*, never wishful or theoretical claims.
- CORRESPONDENCE / TELESCOPE PRINCIPLE: the Qur'ān is assumed a designed system; therefore every property
  proven for a designed system (body, etc.) HAS a Qur'ān correspondence. A failed correspondence test indicts
  the **instrument**, not the text — refine the method / find different data; NEVER file as "disproven."
  (But still hold rigour: don't call a correspondence *proven* without a proper null + effect size.)
- **ARRANGEMENT LEGITIMACY (LOCKED) — orthogonal to the substrate axis.** A finding's status inherits from BOTH
  its substrate AND the arrangement it was measured on:
  1. **DIVINE‑DEFAULT** — Sūra→Āyah (canonical muṣḥaf order); the primary object.
  2. **DIVINE‑ALT** — principled, non‑random re‑indexings that CAN carry real findings: **Āyah→Sūra**, and
     **revelation order** (*tartīb al‑nuzūl*, granularity = sūra; Book6 col8). Comparing DIVINE‑DEFAULT vs a
     DIVINE‑ALT (e.g. muṣḥaf vs revelation coherence) is a *legitimate* test of "why this arrangement."
  3. **HUMAN‑CONSTRUCT** — e.g. reindex by character‑at‑position‑k. Explorable but MUST be tagged
     **[HUMAN CONSTRUCT]**; may reveal something, never presented as divine structure, no overclaim.
  4. **RANDOM shuffle** — ONLY the null/yardstick for statistics; never a "view."
  Only divine‑substrate + divine‑arrangement findings speak to the text's design.
- **Two‑tier recording (LOCKED).** ≥90 = Discovery tier (`latent_features.json`). Everything else real goes in
  `GRADED_FINDINGS_LEDGER.md` at its **best MEASURED grade** + instrument + substrate + arrangement + revise‑up
  trigger — provisional, raised when a better instrument arrives. Nothing real discarded; nothing unproven promoted.
- Discovery bar: grade **≥90** to enter the ledger (`DISCOVERY_CRITERIA.md` gates G0–G9; score is provisional
  until G9(b) comparator is run). Report all candidates incl. aborted; no cherry-picking.
- North star: define what a **Sūra** and an **Āyah** are (necessary AND sufficient), and show why the units
  must have the **current arrangement/configuration**.

## Movement tracking (keep current)
- Log EVERY research move in `research/intrinsic/JOURNEY_LOG.md` with a **date+time stamp** and its BEARING
  (→ toward goal · ↑ method · ✓ consolidation · ↻ drift), so we can see how much time each position cost.
  After each move, check the **reconfigure trigger** (≥3 consecutive sub-90/null discovery moves on the same
  surface → STOP that surface, don't launch another analogy probe).

## Research backlog / queue
- **[QUEUED] Attraction–repulsion field over roots / surface / morphology** — see
  `research/intrinsic/NEXT_CANDIDATES_UNIT_DEFINITION.md` §Queue.
- **[QUEUED · low priority] Connectome / tree diagram of the passed L-features (L1–L17+)** — a plain-terms
  synthesis sketch showing how the discoveries link and integrate (relation edges already in
  `LATENT_FEATURES.md` "Related:" + the SYNTHESIS ladder). Deliver when there's a gap; user said not urgent.

## App / usability working rules (LOCKED — added 2026-06-18, honor every session)
1. **Auto-next.** When a step finishes, AUTOMATICALLY think about and propose the next high-value
   usability feature — ranked, with a one-line value rationale — without being asked.
2. **Enhance, don't proliferate.** Prefer enhancing an EXISTING tab/subtab. A NEW tab requires rigorous
   justification (clear distinct intent that cannot live inside an existing surface).
3. **Always assess/validate.** Before wiring any feature, validate the core logic against the corpus
   (does it produce correct, meaningful output on known cases?); after wiring, re-check syntax + a sample.
   No feature ships on assumption.
4. **Honesty bar (carried over).** A usability feature adds usability, not discovery — never present it
   as a new latent feature. Keep the MEASURED vs INFERRED distinction.
5. **Dense graphics.** Actively look for opportunities to add REAL, information-dense graphics
   (not decorative) where they beat text/lists. Before claiming a graphic is new, CHECK existing
   graphic surfaces (Network, Compare_Heatmaps, Spatial_Patterns, Topic_Map, etc.) to avoid duplication.

## App architecture / sustainability (LOCKED — added 2026-06-18, honor every session)
1. **Coherent IA.** The app must stay organized into clear intent-based areas (the 4-area nav). Every
   page belongs to exactly one area with a distinct purpose. No orphan pages (in `pages/` but unreachable
   from nav), no duplicate-purpose pages.
2. **Sustainable edits.** Any change (add/revise/delete/move) MUST keep the structure coherent: update the
   nav (`NAV_SECTIONS` in state.py), remove dead links/pages, and check nothing else references the changed
   surface. A feature is not "done" until the IA still reads cleanly.
3. **Audit on cadence.** Periodically audit org for patchiness (orphans, duplicates, mis-grouped pages,
   broken links) and report + fix. Structured functionality is required for sustainability.
