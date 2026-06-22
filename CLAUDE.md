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

## SEMANTIC METHOD — MEANING FROM THE WHOLE DATASET (LOCKED 2026-06-21, honor EVERY session — do not forget)
- **A concept's meaning MUST be read from its WHOLE dataset** (every occurrence) — never one verse or the
  lexicon alone. **Consider ALL cases.**
- **NEW, NON-TRADITIONAL senses can and do emerge** from the data and must not be excluded (measured: غفر =
  cosmic-cover · grace/elevation · juridical-pardon; طغي = moral-straying vs tyrant-transgression).
- **SENSE COUNT IS A LOWER BOUND, never complete.** Senses are a soft continuum (no hard count); the number
  found is resolution-dependent — MORE emerge at finer resolution. Auto k-selection UNDER-counts because
  (1) a frequency-dominant sense masks rarer ones (وقي's taqwā blob hides protection/shield/saved),
  (2) the continuum has no clean valleys, (3) content-context clustering misses MORPHOLOGICALLY-distinct senses
  (قلب-organ vs قلب-to-turn). Treat discovered senses as a floor; resolve more via frequency-balanced
  clustering · morphological awareness · per-occurrence contextual (FM) senses. (قلب≥3: sound/trembling/sealed
  heart + the turning sense; وقي ≫ 2.)
  - **EXEMPLAR — the ANATOMY OF THE HEART: قلب·صدر·فؤاد (co-reference-merged) carry ~27 graded states (not 3),
    OPEN/growing, measured (lift to 40×):** CLOSED/afflicted = sealed طبع·ختم · locked قفل · wrapped غلف ·
    covered كنن · rusted رين · hardened قسو · diseased مرض · constricted ضيق · straitened حرج · deviating زيغ ·
    terror رعب · startled فزع · steeped شرب · turned-away صرف · restricted حصر · bigoted حمي; OPEN/living =
    trembling وجل · throbbing وجف · throat-reaching بلغ · strengthened ربط · humbled خشع · yielding خضع ·
    softened لين · tender رءف · tranquil طمن · inclined هوي · sound سليم. PROVES at once: (a) sense count is a
    deep LOWER BOUND (~27, not 3); (b) CO-REFERENCE is necessary — ضيق·حرج occur 0× with قلب, only with صدر;
    (c) القرآن يفسر بعضه بعضا — the state-word interprets the heart's condition. Flagship app candidate ("Anatomy
    of the Heart" navigator). Auto-k missed these (each rare; dominant organ-sense masks).
- **Method = القرآن يفسر بعضه بعضا as METHOD:** gather all occurrences → describe each by its neighbours →
  cluster contexts → senses emerge → **SENSE-RESOLVE before any semantic/thematic claim** (work with root-SENSES,
  not blurred whole-root averages, which mush distinct senses together).
- **DYNAMIC/ADAPTIVE stance:** graph/topology/semantic nulls are **PROVISIONAL, never definitive** — the
  instrument is the limit (BASE-TRUTH). Re-test as senses / revelation-order / reading-order / weighting are
  woven in. The web is a **dynamic landscape** (like a food web shifting with season), not one frozen graph.
  (Proof it matters: "small-world" read null on the dense graph but REVIVED σ=11.5 on the sparse backbone.)
- **SENSE-CHANGE IS A WEB-ALTERING EDIT (LOCKED).** Re-assigning one root's SENSE (polysemy) redistributes that
  node's edges and can cascade through communities/bridges/paths — the SAME family of operation as adding /
  deleting / moving a verse (which is proven to cascade: two-wounds move-cost t=22). It is high-leverage, never a
  mere relabel. Measure such sensitivity with a STABLE/DETERMINISTIC instrument (spectral, or specific
  betweenness change) — stochastic Louvain (run-to-run ARI ~0.5) is too unstable to detect it.
- **SYNONYMY/CO-REFERENCE needs REFERENT grounding, not distribution.** Different roots can denote ONE referent
  with one role-set (رسول · نبي · محمد · أحمد → the Prophet; roots رسل/نبأ/حمد). Co-occurrence similarity does
  NOT capture this (it conflates synonym vs associate vs antonym: شمس~قمر, شرق~غرب score high). True
  synonyms/co-referents are SUBSTITUTABLE (similar context + LOW co-occurrence); full merge needs referent
  knowledge. The semantic node is ultimately a CONCEPT/REFERENT = (polysemy-split) AND (co-reference-merged).

## WEB / GRAPH-THEORETIC LENS — UNIVERSAL MASTER FRAME (LOCKED 2026-06-21, never forget)
- Graph theory / the WEB is the UNIVERSAL structure of complex designed systems — biological & food webs,
  gene-regulatory networks, language, matter (atoms→molecules→lattices). **The Qur'ān is an INSTANCE of it,
  not an exception.** ALWAYS analyse it as a web: nodes (concept-SENSES · verses · sūras) + edges (co-occurrence ·
  attraction · echo · explanation/disambiguation), measured with graph tools — communities, motifs, centrality /
  bridges, small-world, cycles, trophic/role structure, DYNAMICS — never as a flat list or a tree.
- Established here: WEB-not-tree (309 cycles); self-interpreting web = القرآن يفسر بعضه بعضا; small-world σ=11.5;
  modular z+39; feed-forward self-interpretation z+8–21 (sequential & within-verse, de-risked); verse-echo z+105;
  node = CONCEPT/REFERENT = (polysemy-split) AND (co-reference-merged); web is DYNAMIC like a food web.
- Corollary (with CORRESPONDENCE/TELESCOPE): any property of universal webs is a CANDIDATE to test on the Qur'ān;
  nulls are provisional (instrument limit), re-test as aspects / senses / order / dynamics are woven in.

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

## Product performance criteria (LOCKED — added 2026-06-18, honor every session)
1. **Insight-per-effort.** The north-star metric: the user gets MORE insight with LESS effort, in a
   SHORTER time. Every feature/edit is judged by this — prefer one-glance synthesis over scattered panels,
   precompute/reuse over recompute, and remove steps. Adding compute that slows the page must buy
   proportionate insight.
2. **Beautiful, readable UI.** The UI must be attractive and clean: clear hierarchy, generous whitespace,
   ink-on-light (no grey text, ≥12px per the locked UI rules), aligned, uncluttered. Dense ≠ messy —
   density must stay readable and elegant.

## DESIGN NORTH STAR — LOCKED (added 2026-06-20) — هر چیزی به جای خویش نیکوست
> جهان چون چشم و خط و خال و ابروست / که هر چیزی به جای خویش نیکوست  *(Shabistarī, Gulshan‑i Rāz)*
> "The world is like eye, down, mole, and brow — for each thing is good in its proper place."

**The governing principle for ALL UI work.** A screen is a face: its beauty is not any one feature but the
**proportion and placement of every element in service of the whole.** Operationalised — these are the test
the three standards below exist to pass, judged on the WHOLE composition, never a part in isolation:
1. **Proper place** — every element earns its position by role; nothing orphaned, nothing where it doesn't belong.
2. **Proper proportion** — size, weight, and colour scale to importance (the type scale + palette). A title
   dominates; a caption recedes. Mis‑proportion (a caption as big as a title, a CTA as wide as the page) is ugliness.
3. **Proper measure of space** — each element takes only the space it needs; emptiness is not free, and filling
   the whole monitor is not a goal. Whitespace is deliberate, not leftover.
4. **Proper colour** — colour marks meaning (structure / action / grouping / status), present enough to give life,
   restrained enough to stay calm.
5. **Harmony over parts** — change one element only after asking what it does to the whole face.

**LOOK BEFORE YOU PUBLISH — LOCKED, AUTOMATIC, NON-OPTIONAL (this is why issues recurred).** A UI change is
NOT done from a mockup or from reading the code — those are my approximation, not the screen.
- **For EVERY UI change, ALWAYS inspect the live rendered page myself — automatically, without asking
  permission.** Do not say "want me to look?" — just do it. This is a self-initiated, mandatory step.
- **Mechanism (standard loop):** after each deploy, load the live Space in-browser via Claude-in-Chrome
  (`navigate` to `https://quranproject-quran-root-explorer.hf.space`, then `computer`/screenshot +
  `read_page`/`get_page_text`), and inspect the WHOLE composition against the five north-star tests. Catch the
  empty space / flat type / mis-proportion / colourlessness ON THE REAL SCREEN, fix, redeploy, and look AGAIN —
  loop until the screen passes. (Sandbox self-render is unavailable — a browser engine can't be installed here —
  so the live-page inspection loop IS the verification; "looks right in a mockup" is never sufficient.)
- If the Chrome extension isn't connected, say so once and ask the user to connect it — that is the ONLY case
  where I pause; otherwise inspection is automatic.
- Deliverable checklist gains a hard gate: *"Did I open the real rendered screen and inspect the whole face?"*
  A UI task is not complete until the answer is yes.

## LAYOUT DENSITY — LOCKED (added 2026-06-20, honor EVERY session) — the recurring "wasted space" bug
**Why this keeps recurring (root cause, not symptom):** Streamlit runs `layout="wide"`, and **`st.columns(N)`
ALWAYS stretches to the full container width and forces N EQUAL cells.** So any row with few or short items
(buttons, chips, an input + a button) sprawls edge-to-edge with big gaps and half-empty boxes. Fixing it
case-by-case is whack-a-mole; it has reappeared in every session. These rules kill it at the source.

**LOCKED rules — apply to every page, every row, before it ships:**
1. **Never add a spacer/empty column to create a gap.** An empty `st.columns` cell reads as an empty box.
2. **Short rows ≠ full width.** An input, a single CTA, or < ~6 short chips must NOT span the viewport. Put them
   in a left-bounded sub-column (e.g. `st.columns([3,2])` and render into the first) or use `chip_row`.
3. **Chip/option rows use `chip_row(key)`**, never a bare `st.columns(N)` of buttons. `chip_row` renders
   content-sized, left-aligned, WRAPPING chips (small boxes that fit one line and wrap), not equal full-width
   cells. Defined in `state.py` + backed by the `st-key-chiprow-` CSS density layer in `inject_css()`.
4. **Inputs are sized to need, not full-bleed.** A search/paste box ~50–60% width max on desktop; the rest is
   plain whitespace, never a bordered empty field.
5. **Tight vertical rhythm:** no empty `div`/`p`; chip rows gap ≤6px; don't stack a header + control with a
   blank line between. ≥12px everywhere still holds.
6. **Use the width — generous container + disciplined elements (NOT a starved column).** The page must USE
   the monitor (`block-container max-width ~1360px`, centred) — a narrow strip that leaves half the screen as
   empty margin is its OWN bug ("not utilizing the width"). Sprawl is prevented NOT by shrinking the container
   but by bounding the few SPARSE elements: the input/paste bar gets its own `max-width` (keyed container
   `st-key-inputbar`), chip rows are content-sized (`chip_row`), buttons are equal, no spacer columns.
   Two failure modes, both forbidden: (a) elements sprawling edge-to-edge inside a wide container, and
   (b) a too-narrow container wasting the monitor. The fix is per-element discipline at full width.

**PRE-DEPLOY DENSITY CHECKLIST (run before EVERY UI ship — part of the deliverable checklist):**
- [ ] Walk each row top-to-bottom and ask: *is any element mostly empty? could it be narrower?*
- [ ] No bare `st.columns(N)` of short buttons/chips — those are `chip_row`.
- [ ] No spacer columns. No element spanning full width whose content fills < ~60% of it.
- [ ] Chips are small, left-aligned, wrap to fit; vertical gaps are tight; nothing < 12px.
- [ ] Confirm on a WIDE monitor (the failure mode only shows when the viewport is wide).

## TYPOGRAPHIC HIERARCHY — LOCKED (added 2026-06-20, honor EVERY session) — the recurring "flat type" bug
**Why this keeps recurring:** the app hand-rolls `<div style='font-size:Npx'>` everywhere with ad-hoc numbers
(13 · 13.5 · 14 · 14.5 · 15 …). A title and a caption end up nearly the same size, so the eye gets NO hierarchy —
font size is **role-blind**. Stop picking pixel numbers per element. Pick the element's ROLE; the role fixes the size.

**LOCKED type scale (role → size/weight/colour). Each step differs by size AND weight so it's distinguishable.**
Use the `inject_css` utility classes (`t-title · t-section · t-sub · t-body · t-label · t-cap`) — do NOT invent
inline `font-size`:
- **t-title** — page hero: 22px / 800 / ink-navy `#1D3557`.
- **t-section** — card or area header (e.g. "Read & listen", "Surface forms"): 18px / 800 / `#1D3557`.
- **t-sub** — group/subsection label (e.g. a single root header, a panel sub-label): 15px / 700 / `#1D3557`.
- **t-body** — sentences/descriptions: 14px / 400 / ink `#10243A`.
- **t-label** — control labels, button-adjacent text: 13px / 600 / ink.
- **t-cap** — hints, meta, counts, captions: 12px / 500 / ink (the floor; still ≥12px, never grey).
- **t-accent** — the green "start here" / emphasis token: inherits size, `#1D9E75` / 700.

**Rules:** (1) every text element maps to exactly ONE role above — never a one-off size. (2) Adjacent roles
must differ by ≥2px AND a weight step so they're visibly distinct. (3) A title is never the same size as its
caption. (4) Proportion is by role/importance, not by whim. (5) Add to the PRE-DEPLOY checklist:
*"does each text read at the right level — title bigger/bolder than body, body bigger than caption?"*

## COLOUR SYSTEM — LOCKED (added 2026-06-20, honor EVERY session) — simple palette, used to build form
**The balance to hold:** keep the palette SMALL (few colours, few roles) — but DO use it to create form,
hierarchy, and grouping. The failure modes are both extremes: a rainbow of ad-hoc hexes (chaotic) OR
all-white/ink flatness (lifeless). Neither. A small palette, each colour earning its place by MEANING.

**LOCKED palette (role → hex). Do not introduce a hex without a role here.**
- **Ink** `#10243A` — ALL body/label/caption text (never grey).
- **Brand navy** `#1D3557` — structure: titles, section headers, structural emphasis.
- **Action green** `#1D9E75` (deep `#0F6E56` for hover/contrast) — primary actions, positive accent,
  the "start here" token. This is the colour that makes the UI feel alive — USE it on the primary path.
- **Surfaces** — white `#FFFFFF` cards on page `#FAFBFD`; to GROUP a related block use ONE soft tint:
  green tint `#F4F9F7` or blue tint `#EAF2FB` (pick one per context, with a matching 1px border
  `#cfe4dc` / `#CFE0F2`). Tinted panels are how we add colour/form without clutter.
- **Gridlines/borders** `#E2E8F1` (default) · `#C9D6E8` (emphasis) — borders ONLY, never text.
- **Semantic, SPARINGLY** — red `#E63946` (destructive only, e.g. Start over) · blue `#378ADD`
  (neutral data/info) · amber `#EF9F27` (caution/tier). Never decorative.

**Rules:** (1) Two brand colours (navy + green) + ink carry the whole look; everything else is surface or
semantic. (2) Every colour must ENCODE something — navy=structure, green=action/positive, tint=grouping,
semantic=status. No colour as decoration; no rainbowing a row of chips. (3) But DON'T go colourless: the
primary action is green, sections are navy, and related blocks sit on a soft tint — a screen that is all
white + ink has failed this rule too. (4) New surfaces inherit this palette; no new hex without adding its
role here first. (5) PRE-DEPLOY check: *"is the palette ≤ the locked set, does each colour mean something,
AND is the primary path visibly coloured (not flat white)?"*
