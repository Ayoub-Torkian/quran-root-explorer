# Deep-Dive Report Generator — Hand-off

## What this is
The "Deep Dives" subsystem of the Qur'an Root Explorer produces three-register
reports (technical / plain English / plain Persian) for two kinds of target:
a **concept** (a triliteral root, e.g. قلب) and an **ayah** (e.g. 2:255).

- **`deep_dive.py`** — the analysis. `concept_deep_dive(target, unit, normalize)`
  and `ayah_deep_dive([(surah,ayah)], ...)` return a `res` dict.
- **`report_dive.py`** — builds the `.docx` reports from `res`.
- Both are in the deploy manifest (`deploy_git.py`), so deploying pushes them.

## In-app generation path (what the user actually uses)
```
docx_bytes_from_result(res, register)          # register in {technical, plain_en, plain_fa}
  → _ayah_paper / _concept_paper               # dispatcher
     → technical: _ayah_tech / _concept_tech   # IMRaD, with figures
     → plain:     _ayah_plain / _concept_plain  # plain language
```
Pages `19_Concept_Deep_Dive.py` / `20_Ayah_Deep_Dive.py` call
`RP.docx_bytes_from_result(...)` — unchanged, no edits needed there.

## What is DONE and verified
1. **Ayah = one context entity** (`deep_dive.py`). The seed verse is an
   idf-weighted centroid of its roots, so distinctive concepts define its
   signature. **All roots enter the analysis** regardless of UI display
   (full root sets drive the lexical lens & evidence; embeddable subset drives
   the meaning/territory centroids).
2. **No Qur'anic text reproduced.** Verified `verse_text_reproduced=False` on all
   six papers. Verses are cited by number; evidence is a shared-root **count**,
   not the text or a root dump.
3. **Technical papers = standard IMRaD**: Abstract · Keywords · 1 Introduction ·
   2 Materials and Methods · 3 Results · 4 Discussion · 5 Limitations ·
   6 Conclusion · References. **Figures**: 7 (concept), 6 (ayah), each with a
   numbered caption AND a discussion paragraph, inline in Results.
4. **Page numbers** in the footer of every paper (`_page_number_footer`).
5. **Arabic box bug fixed at source**: `_has_arabic()` + `_pin_cs()` pin the
   complex-script font on every run with Arabic, in LTR paragraphs and table
   cells. Applied inside `H`, `P`, `TABLE`.
6. **Plain papers**: professional section titles. `_ayah_plain` is now full
   IMRaD (1 Introduction · 2 Method · 3 Results with ONE compact cross-reference
   table · 4 Discussion · 5 Limitations · 6 Conclusion). Findings are a single
   table (relation | verse | # shared | meaning | territory), not repeated lines.
7. **Mess cleaned**: removed 428 lines of stacked duplicate builders (kept the
   last/active definition of each). File went from ~1940 to ~1500 lines.

## IMMEDIATE NEXT TASK — DONE (2026-06-04)
**`_concept_plain` is now full IMRaD**, mirroring `_ayah_plain`:
Abstract · 1 Introduction · 2 Method (five lenses, kept apart) · 3 Results
(principal finding = meaning-mates ≠ territory-mates; the verified bond; the
frequency-control note; ONE compact companion table:
relation | concept | meaning | territory | shape) · 4 Discussion ·
5 Limitations · 6 Conclusion. Orphaned helpers `_concept_type_note` and
`_roots6` were pruned (call-graph verified single-use). All six papers verified:
concept tech 7 figs/6 tables, ayah tech 6 figs/6 tables, all four plain papers
1 compact table / 0 figs, `verse_text_reproduced=False` on every ayah paper.
`report_dive.py` compiles (1528 lines).

**Only remaining step: deploy.** The sandbox cannot reach huggingface.co, so run
the push from your own machine (PowerShell, from this folder):
```
python -m py_compile deep_dive.py report_dive.py ; python deploy_git.py
```
The commit message in `deploy_git.py` is already set for this change.

## (historical) original next task
### was:
**`_concept_plain` (in `report_dive.py`) is not yet in full IMRaD** like
`_ayah_plain`. Convert it to the same structure: Abstract · 1 Introduction ·
2 Method (five lenses, kept apart) · 3 Results (principal finding = meaning-mates
≠ territory-mates; the verified bond; the frequency-control note; ONE compact
companion table: relation | concept | meaning | territory | shape) ·
4 Discussion · 5 Limitations · 6 Conclusion. Mirror the plain-language tone of
`_ayah_plain`. Keep it tight — no filler, no repeated lines, no reproduced
content.

## Editing gotchas (important)
- **Always `python -m py_compile deep_dive.py report_dive.py` after every edit.**
- `report_dive.py` had a history of stacked appends; prefer **bash/python
  string-replace** with a `count==1` assertion, or AST-based splicing by
  `def` boundaries, over fragile line numbers.
- A long heredoc once **truncated mid-write** — verify `tail`/`wc -l` after big
  appends.
- There are still some likely-**unused helper functions** (e.g. `_plain_idea`,
  `_plain_lenses`, `_rel_analogy`, `_concept_figures`, `_ayah_figures`,
  `_ayah_type_prose`, `_concept_rel_prose`). They are harmless but could be
  pruned after a call-graph check. The old CLI builders
  (`_concept_technical`, `_concept_plain_en/_fa`, `_ayah_blocks`) are still used
  by `build_reports()` (the local CLI path) — do not delete without rewiring it.

## `res` data reference (for writing reports)
- Common: `res["request"]` (kind, target/seeds, unit, k, min_freq, n_scramble),
  `res["meta"]` (n_ayahs, code_version, elapsed_s).
- Concept: `field{semantic_field, co_location_neighbours}`,
  `distribution{frequency, n_surahs_present, hotspot_surahs, archetype, features{...}}`,
  `null{real, null_mean, null_sd, z, n_scramble, interpretation}` (Moran's I,
  frequency-controlled), `relations.related_by_type{type: [{root, axes{semantic,
  co-location, spatial}, relevance}]}`, `relations.by_relation{counts}`,
  `synthesis{cross_modal{convergence, divergence, verified_bonds}, modalities, reading}`,
  `cross_granularity{verified_both_levels, root_level_only, surface_level_only}`,
  `senses[{form, count, share}]`, `sequence{mean_within_ayah_position, ayah_final_share}`.
- Ayah: `seed[{ref, text, roots}]`, `seed_concepts`, `related_by_type{type:
  [{ref, axes{lexical, semantic, spatial}, shared_roots, relevance, text}]}`,
  `synthesis{by_relation, cross_modal{divergence}, ...}`.
  NOTE: `x["text"]` and `sd["text"]` are the verse texts — **never print them**;
  cite `ref` and use `len(shared_roots)`.

## Regenerate & inspect (test snippet)
```python
import deep_dive as DD, report_dive as RP, docx, io
res = DD.concept_deep_dive("قلب", unit="surah", normalize=True)
# res = DD.ayah_deep_dive([(2,255)], unit="surah", normalize=True)
for reg in ["technical","plain_en","plain_fa"]:
    b = RP.docx_bytes_from_result(res, reg)
    d = docx.Document(io.BytesIO(b))
    print(reg, "figs", len(d.inline_shapes), "tables", len(d.tables))
```

## Deploy (PowerShell, from this folder)
```
python -m py_compile deep_dive.py report_dive.py ; python deploy_git.py
```
Live URL: https://quranproject-quran-root-explorer.hf.space/

## UPDATE 2 (2026-06-04) — sense-cohesion line + ayah decision
- Added `_sense_cohesion(senses)` to `report_dive.py`: mean pairwise Jaccard of the
  per-surface-form significant co-locator sets → cohesive (J≥0.34) / mixed / split
  (J≤0.12). Gated on ≥2 forms (count≥5) each with ≥2 significant co-locators; returns
  None (no sentence) when too sparse. Reports only the verdict + the form-robust core,
  never per-form association lists (respects the surface-only="not asserted" epistemic).
- Wired into all THREE concept registers: one gated sentence in plain_en/plain_fa
  Results; a quantified (Jaccard) gated sentence in technical §3.5 Morphology.
- Verified: قلب → split (J=0.02). All six papers regenerate; counts unchanged
  (concept tech 7 figs/6 tables, ayah tech 6/6, plain papers 1 table/0 figs);
  verse_text_reproduced=False on all ayah papers; page-number footers intact.
- DECISION — **no surface forms in the ayah deep dive.** The ayah is analysed as a
  root-level, multi-root entity (idf-weighted centroid of its roots); surface forms
  are stripped at tokenisation and there is no single root whose morphology could be
  examined, so the concept-style cohesion signal has no analog. The only verse-level
  surface idea (cross-verse verbatim echo) duplicates the lexical axis, risks
  reproducing verse text, and is mostly empty. Rejected on data/architecture grounds.

# ============================================================================
# SESSION HANDOFF — 2026-06-04 (START HERE NEXT TIME)
# ============================================================================

## STATE: code complete & verified, NOT yet deployed
`report_dive.py` (1590 lines) and `deploy_git.py` compile clean. All six deep-dive
papers regenerate and were verified this session.

## #1 ACTIONABLE — DEPLOY (only thing left from this session's work)
The sandbox proxy blocks huggingface.co (HTTP 403), so the git push CANNOT run from
the agent. Run this on the user's machine (PowerShell, from this folder):
```
python -m py_compile deep_dive.py report_dive.py ; python deploy_git.py
```
`deploy_git.py` already has the correct commit message for this change. Live URL:
https://quranproject-quran-root-explorer.hf.space/

## WHAT SHIPPED THIS SESSION (in report_dive.py)
1. `_concept_plain` → full IMRaD, mirroring `_ayah_plain`: Abstract · 1 Intro ·
   2 Method · 3 Results (ONE compact table: relation|concept|meaning|territory|shape)
   · 4 Discussion · 5 Limitations · 6 Conclusion. Both plain registers (en/fa).
2. New `_sense_cohesion(senses)` helper: mean pairwise Jaccard of per-surface-form
   significant (p≤0.10) co-locator sets → cohesive (J≥0.34) / mixed / split (J≤0.12).
   Gated: ≥2 forms (count≥5) each with ≥2 sig co-locators, else returns None (silent).
   Reports verdict + form-robust core only; never per-form association lists.
   Wired into ALL THREE concept registers: one gated sentence in plain_en/plain_fa
   Results; a quantified (Jaccard) gated sentence in technical §3.5.
3. Pruned orphaned helpers `_concept_type_note`, `_roots6`.
   Worked examples: قلب → split (J=0.02); رود → split (J=0.013, راود=Joseph story
   vs یرید=legal contexts).

## DECISION LOG (don't re-litigate without new reason)
- **Ayah deep dive: NO surface forms.** Ayah is analysed as a root-level, multi-root
  centroid; surface forms are stripped at tokenisation; no single-root morphology
  anchor exists, so the concept-style cohesion signal has no analog. Rejected on
  data/architecture grounds, not preference.
- **No surface-form clone of the multimodal fusion map.** The map's x-axis is
  semantic, which is root-indexed (`multiview_embeddings` has NO surface mode) and is
  conceptually degenerate for forms (all forms of one root share a meaning
  neighbourhood → collinear → collapse on x). The 6-type typology is defined by
  semantic×co-location, so it's undefined for forms. A clone would be faithful in
  pixels, false in meaning. REJECTED.

## OPEN ITEM (user undecided; my lean = LOW PRIORITY)
A distinct, honest **"surface-form divergence" panel** for page 19, IF the user wants
it — the visual twin of the shipped cohesion line. Build rules if greenlit:
  - co-location modality primary (spatial optional). `colocation_field/neighbors`,
    `archetype_analysis`, `occ_surah_ayah` all support feature="surface".
  - NOT semantic (degenerate for forms). NOT the fusion-map typology.
  - Gated on ≥2 high-mass forms; badge "exploratory · co-location only".
  - **KEEP ARABIC LABELS** — the app renders Plotly (Arabic shows fine; the screenshot
    proves it). Transliteration was only a sandbox-matplotlib font gap; do NOT carry it
    into the app.
  - Adds "WHERE senses diverge" on top of the cohesion line's "THAT they diverge",
    only for the minority of multi-form roots; blank for monoform concepts.

## ENV GOTCHA (cost us time this session — avoid)
Editing files on the C:\Users\torki\Downloads mount via the Edit/Write FILE TOOLS
TRUNCATES large files mid-write (hit report_dive.py and deploy_git.py). WORKAROUND:
do all edits in the sandbox (python read→modify→write to /tmp, `ast.parse`, then
`cp /tmp/x.py <mount>`), then `py_compile`. `cp` and python writes do NOT truncate.
Use `PYTHONPYCACHEPREFIX=/sessions/.../outputs/pycache` (mount __pycache__ is RO-ish).
Deps to pip-install in a fresh sandbox: networkx (deep_dive import), and
arabic_reshaper/python-bidi only if rendering Arabic in matplotlib (app doesn't need).

## QUICK VERIFY SNIPPET (run after any report_dive change)
```python
import pickle, io, docx, report_dive as RP
for f in ["concept_res.pkl","ayah_res.pkl"]:  # cached this session in outputs/
    res=pickle.load(open(f,"rb"))
    for reg in ["technical","plain_en","plain_fa"]:
        d=docx.Document(io.BytesIO(RP.docx_bytes_from_result(res,reg)))
        print(reg, "figs",len(d.inline_shapes),"tables",len(d.tables))
```
