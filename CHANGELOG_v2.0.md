# CHANGELOG — v2.0 (Re-Spine, Phase 1)

## Phase 11 — surface-form input + hover form-tooltips (plan-first design honored)
- `state.py`: cached form↔root index from corpus.seg_tokens∥root_tokens (only verses with 1:1
  alignment — the honest subset); `_smart_lookup` now resolves typed SURFACE FORMS to roots
  (unambiguous = top root ≥2× runner-up; otherwise an explicit chooser — never silent).
  ANALYSIS REMAINS ROOT-BASED (standard NLP practice); transparency chips show every mapping
  ("عليم ⇒ root علم") the moment it happens.
- Suggestion chips: native hover tooltip lists the root's top surface forms with counts
  ("Surface forms: يعلم ×217 · علم ×151 …") — the "hover shows forms" request via the stable
  native mechanism (no custom JS).
- Also: top row fits one line (shorter pill labels + rebalanced columns); Start-over gets
  destructive CONTRAST (white/red outline, fills red on hover, via st-key scoped CSS);
  PLAN-FIRST locked as UI-standard rule 6 in APP_PLAN.md.

## Phase 9 — FACE-LIFT (critical review honored) + global readability sweep
Critical review findings → fixes, all in state.py/app.py (apply app-wide):
- Inverted hierarchy: three saturated red/orange gradient banners outshouted the actual input.
  → hero() is now a calm navy band; the giant gradient instruction banner is a one-line label
  ("🔎 Find roots — type… · Enter applies"); the INPUT is the visual hero.
- Broken button grammar: destructive START OVER shared loud red with Analyze.
  → app-wide: primary buttons = TEAL (go), START OVER demoted to quiet secondary "↺ Start over";
  red is reserved for destructive/danger semantics only.
- CSS leak: per-column gradient expander rules (nth-child) hit EVERY page's columns.
  → replaced with one quiet white-card expander style app-wide (navy text, teal hover).
- HELP appeared 3× on Home → once (page_link inside the New-here expander); 2-column pill row.
- Readability/space sweep (global, state.py): top padding halved, vertical gaps 0.55rem,
  compressed headings/dividers, captions ≥13.5px with higher contrast, metrics as compact
  white cards, slimmer expander headers/buttons, zero chart/table margins.

Date: 2026-06-07. Gate: lens set stabilized at 18 (consolidation #77) → re-spine unblocked per APP_PLAN.

## Changed
- **Navigation re-spined** (`state.py` → `NAV_SECTIONS`). New primary axis:
  📖 READER (Ayah Browser · Āyah Deep-Dive hero · Concept Deep-Dive) ·
  🧪 LENS LAB · 🧭 POSITION scale (Disjoint Letters · Spatial Patterns · FDR Summary) ·
  🔤 SEQUENCE scale (Signal · Morphology) ·
  🧩 SEMANTIC scale (Roots & relations / Topics & themes / Interpret) ·
  🛠️ TOOLS & FEEDBACK (Statistics · Feedback & Bugs · Export · Usage · Help).
  Old build-history groups (EXPLORE / DEEP DIVES / TWO BOOKS) retired. Pages regrouped by the
  QUESTION they answer (UI_REORG_NOTES); no page moved or renamed — zero-risk regroup.

## Added
- **Lens Lab** (`pages/22_Lens_Lab.py`) — the app's evidence-instrument centerpiece:
  - 18 verdict cards (claim · statistic vs null · comparator boundary · gate verdict · EVIDENCE refs),
    grouped DISTINCTIVE / INTERNAL-ONLY / NULL-register / BLOCKED — honest nulls first-class.
  - Filters by verdict class and scale; Architecture-of-Return thesis banner; embedded COVERAGE_MAP.
  - Content mirrors FINDINGS_SYNTHESIS.md (single source of truth; #76/#77 corrections included,
    abjadī stance re-weight included).
- `VALUE_SINCE_V1.2.md` — one-page value brief (four gated findings · corrections · artifacts).

## Verified
- `py_compile` clean on `state.py` + `pages/22_Lens_Lab.py`; all nav targets exist (fallbacks honored).
- Mount-truncation GOTCHA hit again on `state.py` VM reads (stable cut at line ~1691) — host file
  confirmed complete via direct read; verification done on reconstructed copy. Host = source of truth.

## Phase 2 increment (same day) — LIVE LENS RUNS
- `lens_live.py` (new): cached quick runners reusing the EXACT filed instruments —
  Lens 9 (#42 recurrence: equal-P bootstrap, word-shuffle net, canonical cell K=50, B=60) and
  Lens 3 (rhyme persistence: #76 feature f1, K=25 windows, 60× unit-shuffle null).
  Locked tokenizer rule honored (nrm of COL_DIACRITIZED, normalize-then-split).
- Lens Lab cards 9 and 3 now carry a "Run this lens LIVE" expander: button → fresh run → bars +
  gate readout. Results cached per session.
- FUNCTIONALLY VERIFIED in sandbox (streamlit stubbed): rhyme means reproduce #76 exactly
  (Q 0.737 / ord 0.31 / sajʿ 0.34 / poetry 0.55, shuffle-z huge, g vs sajʿ +2.37); recurrence
  K=50/B=60 → Q +2.86σ vs filed +3.0σ (B=300). sajʿ net flagged unstable (small corpus) —
  honest caveat shown in the card caption. Warm runtime ≈0.5 s.

## Phase 3 increment (same day) — ĀYAH-HERO FUSION VIEW + MASK
`pages/20_Ayah_Deep_Dive.py`:
- **Hero strip** per seed āyah — one row, four lenses at a glance: 🔏 seal (ending · class size ·
  live #62 fit-z) · ↩ return (echo-set size · sūra span) · 🧭 position (sūra #, muqaṭṭaʿāt flag,
  Meccan/Medinan as control-only, seal temporal type from the #70/#74 2×2 typology) · 🌱 roots
  (#66 global-motif vs local-formula counts). Renders before the existing seal expander.
- **🎭 Mask control** on the echo-set (signal-geometry made tangible): none · cross-sūra only ·
  project out the seal class (the #33 rhyme-channel mask) · Meccan-only / Medinan-only
  (control-only, labeled). Applies to the fusion map, table and relation expanders; kept/total shown.
- Constants reuse the project's own lists (MED 28-set from group_cohesion.py; 29 muqaṭṭaʿāt sūras).
- Verified: full-file py_compile (reconstructed against the mount-truncation GOTCHA).

## Phase 4 increment (same day) — LOCKED UI STANDARD applied (user mandate)
Standard (APP_PLAN.md): summary-metrics-first · help= tooltips everywhere · charts for every
numeric claim (bar/scatter/pie/network) · data-driven interpretation, never generic.
- **Lens Lab**: 📌 comprehensive-summary metric row (5 metrics, deep help tooltips) + verdict
  donut + headline effect-size bar chart (σ/z labeled, 2σ reference line) above the cards.
- **Concept Deep-Dive** (user-flagged "one chart only, roots without context"): relation donut ·
  bond NETWORK graph (hub-spoke, edge width = strength, color = type) · semantic-field strength
  bars (z + frequency hover — context for the chips) · 114-sūra occurrence profile bar
  (Meccan/Medinan colored, control-only) · real-vs-scramble null bar (±2σ) · surface-form sense
  pie · 🧠 computed interpretation block (consensus share, dominance, concentration→#66 mode,
  āyah-final share→Lens-17 link) — all values from THIS run.
- Verified: all new blocks compile; mount-cache truncation now affects every previously-read file
  (verification via fresh-name snippets — host files remain the source of truth).

## Phase 5 increment — Āyah Deep-Dive echo charts (mask-aware) + radial bond map rework
- Concept Deep-Dive bond network REPLACED with a radial bond map (user review: geometry must mean
  something): sector = relation type (rim-labeled) · distance from hub = bond strength (dotted
  stronger/weaker rings) · node size = frequency · "📍 What to take from this map" computed line.
  Standard rule 4b added to APP_PLAN (every chart carries a computed takeaway; no arbitrary layouts).
- Per-form frequency-by-sūra bar inside each surface-form expander (clitic-aware matching) +
  computed caption (peak sūra, Medinan share, form-vs-root geography pointer).
- Āyah Deep-Dive: echo-composition donut + echo-geography 114-sūra bar (both react to the 🎭 mask)
  + computed 📍 takeaway (cross-sūra share → long-range vs local; resonant-vs-direct mode;
  consensus core; densest-return sūra; mask-survival note).

## Phase 6 increment — Motifs + Network brought to the UI standard
- **Motifs**: census metrics now carry deep help tooltips; computed 📍 takeaway after the census
  (closure rate → constellation vs parallel-strand reading) and after the triangle chart (names
  the strongest triad, weight≠similarity warning, PPMI pointer).
- **Network**: all 12 §1 stats get explanatory tooltips; computed 📍 takeaway (modularity verdict
  → which section to read next; load-bearing articulation/bridge count; #65 map-not-claim
  boundary); phase-diff 📍 takeaway (stable-spine share, Meccan/Medinan-only counts, #70 context).

## Phase 7 increment — Statistics page to the UI standard
- Headline metrics get deep tooltips (rank vs dispersion independence; entropy-vs-D disagreement
  as a lumpiness flag) + computed 📍 takeaway (workhorse / most-even / most-concentrated roots,
  GLOBAL-motif count via the ≥20-sūra #66 threshold, frequent≠spread warning).
- Tile 3 (position-in-āyah) now ROUTES into the research: computed 📍 takeaway flags any root
  ending its āyah ≥40% (vs ~33% chance) as seal-active with the Lens-17 numbers and a pointer
  to the Āyah Deep-Dive seal panel; or states the honest negative.

## Hotfix (user-reported) — sklearn crash + global progress ribbon
- 20_Ayah_Deep_Dive `_seal_index` rewritten sklearn-FREE (scipy.sparse TF-IDF, min_df=2,
  smooth-idf, l2 — verified numerically identical to TfidfVectorizer, gram diff ≈1e-16).
  sklearn was the ONLY missing-dep import in the whole app (grepped); requirements.txt
  unchanged — the app now runs on its declared deps.
- state.py: global PROGRESS RIBBON — animated color bar pinned to the top edge + a navy
  "⏳ computing…" pill (top-right), shown automatically whenever Streamlit is running
  (CSS :has() on the status widget). Appears on every page; no per-page code needed.

## Phase 7b — Concept Deep-Dive layers 2–3 charted (user example honored)
- Robust bonds: grouped two-axis bar (semantic z + co-location z per bond) — shows WHY each is
  robust; 📍 takeaway (both bars or it's modality-specific).
- Co-location territory: strength bar (z + frequency hover) + the narrative-companionship-vs-
  synonymy caption.
- Cross-granularity (layer 3): a root∥surface VENN (counts in each wing/overlap) + computed
  takeaway — overlap = the trustworthy core (relation-level G10 invariance); a dominant
  surface-only wing routes to layer 5's per-form charts; #76 tokenizer-rule echo.

## Next (v2.0 phase 8)
Help page enrichment (0_Help.py, 924 lines — own session) · relationships-surface consolidation
(UI_REORG_NOTES) · more live lenses · remaining pages (Compare/Morphology/Topic pages) to the
standard.

## Phase 8 — full-app chart sweep (agent)
13 remaining pages audited and brought to the LOCKED UI STANDARD (metrics-first · help= ·
charts over chips/tables · computed 📍 takeaways · try/except-guarded). Every new block
verified by snippet py_compile (host = source of truth; mount-truncation GOTCHA respected).

- **1_Per_Root_Profile** — help= on the Tier metric; 📍 takeaway after the layer-2/density-home
  charts (busiest surah + share, size-true density home, Gini reading); combined-mode co-presence
  metrics get help= and the stacked-bar gets a computed takeaway (peak surah, #surahs with ALL
  inputs). BUGFIX: the surface-divergence banner referenced `corpus`/`R` before they were defined
  (silent NameError → banner never showed); moved after `R = need_results()`.
- **4_Ayah_Browser** — help= on the 3 headline metrics; NEW 114-sūra matched-ayahs profile bar
  (🟩 Meccan · 🟥 Medinan — control-only, MEDINAN 28-set) reacting to the live filter, with a
  computed takeaway (unique ayahs, densest surah, Medinan share + control-frame caveat).
- **5_Compare_Heatmaps** — help= on the 3 glance metrics; 📍 takeaway after the surah×root heatmap
  (hottest column/row, touched surahs, empty-columns reading) and after the pair-overlap chart
  (top pair's surah-Jaccard vs ayah-shared, zero-ayah pair count, placement≠association caveat).
- **6_Morphology** — help= on all 4 summary metrics; NEW prefix-vs-suffix donut (BLUE/ORANGE) +
  computed takeaway (top particle + share, prefix/suffix dominance); per-root drill-down gets a
  computed takeaway (attachments, distinct particles, top companion).
- **9_Topic_Modeling** — help= on the 4 top-line cache metrics and the 3 per-root topic metrics;
  📍 takeaway after each quadrant scatter (core/contrastive/synonym counts, strongest neighbour,
  top latent synonym, x/y geometry legend + distributional-not-meaning caveat).
- **8a_Interpret** — was text-only: NEW headline metric row (roots · unique ayahs · surahs ·
  corpus share, all with help=) + NEW per-root ayah-footprint bar (TEAL) with computed takeaway
  (dominant vs rarest root, asymmetry ratio, frequency≠importance warning). Fully guarded.
- **8f_Practical_Lens** — was expander-only: NEW headline metric row (pairs · stipulative ·
  embedded · independent, with help=) + NEW horizontal lift-spectrum bar (tier-colored, chance
  line) with computed takeaway (strongest pair, tier counts, thresholds-are-mechanical note).
- **8e_Calibration** — NEW metrics-first row for "Your current pair(s)" (pairs tested · max lift ·
  tier · pairs above chance, with help=); 📍 takeaway after the lift-spectrum (your best pair vs
  the 12 reference dyads, span of the ruler; reference-only variant when no pair entered).
- **14_Disjoint_Letters** — already chart-rich; added help= to the Explore-tab metrics (tag/family/
  size/verses) and Organization medians; 📍 takeaways on the two always-visible charts: corpus
  alphabet bar (top-letter and top-3 share, disjoint letters = common stock) and the length
  histogram (median ratio, muq count among 20 longest, flags-position-not-length note).
- **15_Signal** — help= on lag-1 ACF (with the computed ±band), dispersion metrics (occurrences/
  Fano/mean gap) and rhythm metrics (median/mean/CV); 📍 takeaways on the sūra-length signal
  (max/min sūras, first- vs second-half mean envelope) and the mean-āyah-length-per-sūra bar
  (range ×, extremes, two-registers reading).
- **16_Biology** — 📍 takeaways on the base-composition bar (top letter, top-5 share, why per-sūra
  deviations stay small) and the Zipf scatter (top-root and top-10 token share, hapax % of
  vocabulary, why slope < −1 is a counting property, not a code); help= on the Zipf metric row,
  hapax count, and the 3 Markov-memory metrics.
- **18_Spatial_Patterns** — already heavily annotated; added help= to the 4 Forest headline metrics
  and a 📍 takeaway after the Forest charts (bursty % vs coverage, Moran split, route to the
  scramble control before reading either as real structure).
- **17_Two_Books_Summary** — 📍 takeaway after the FDR bar chart (names the surviving and dropped
  tests, strongest p/q, FDR-handles-multiplicity-not-confounds caveat); help= on the
  discoveries-surviving metric.

Conventions held throughout: f-string takeaways from live page variables only; new chart colors
from the locked palette (TEAL #1D9E75 / BLUE #378ADD / ORANGE #EF9F27 / GREY #B4B2A9 /
RED #E63946); MEDINAN 28-set for control-only coloring; every new block wrapped in try/except
so failures can never blank a page; no heavy new computation added.

## Phase 10 — palette + type-scale enforcement (agent)
Style-only sweep of app.py · state.py · feedback.py · pages/*.py against DESIGN_SYSTEM.md.
No logic, no data, no chart semantics, no wording changed. All edits are string-value swaps;
representative f-string/concatenation blocks snippet-py_compile'd (host = source of truth;
mount-truncation GOTCHA respected — all discovery/verification via host grep).

Per-file replacements (counts by category):
- **state.py** (~95 value swaps) — gradients→flat: 13 removed (hero banner, quranic-verse,
  insight-card, top-input + focus + JS applyStyle, chips + chip hover ×2, landscape-hint,
  per_root_hint compact+large, analyze-call-OLD, JS ribbon idle ×2 → flat #1D3557); KEPT the
  sanctioned progress-ribbon gradients (CSS dlribbon L139 + JS running-state shine L1004 — the
  running gradient is the animation carrier; flattening it would disable the state cue).
  Gold/red banners → BG-TINT #EEF3FB + navy border-left (sidebar nav box, per_root_hint ×2,
  landscape-hint, verse box). Cyan #06AED5 → #1D9E75 on nav border-lefts ×2 and links→#16365C.
  Red-as-decoration → NAVY (active nav pill, selected tab, metric value, pill-input, hint
  headlines, big-input border) or TEAL for GO (Analyze button, primary buttons ×2, focus ring).
  Gray text → tokens: #6B7280/#374151/#7B8AA0/#2C3E5C/#1B263B/#A8C3E8 → #3D4757/#243447/#16365C
  (12 spots). Pills: rare→#378ADD, common→#1D9E75, ubiq→#EF9F27. Stage chips: #2A9D8F→#1D9E75 ×2,
  red indexing→navy, gray pending→#E2E8F1/#3D4757. Borders #E5E7EB/#E8EDF4→#E2E8F1 (5). mark.hit
  gold→TEAL/white. text-shadow removed ×2 (hero h1, JS ribbon). box-shadows normalized to
  0 1px 4px rgba(0,0,0,0.06) (12, incl. pulse keyframes neutered). Type: weights 800/900→700
  (16); 10/11px→12, 12.5→13, 22-28px UI→17/19/23 (hero 24→17, metric 24→23, insight value
  28→23, h3 22→19, h4 18→17, Analyze 22/20→19, mobile hero 26/22→17); Arabic content sizes
  (26-28px verse/input) kept per spec.
- **app.py** (18) — module bar: active #E63946→#1D3557, inactive #E5E7EB/#6B7280→#E2E8F1/#3D4757;
  per-root banner → #EEF3FB + navy border-left, 900→700, red→navy/teal; pulseHint keyframes
  neutered; tier_color map → #378ADD/#1D9E75/#EF9F27/#1D3557; jump-card → white card #E2E8F1
  border, root title 26px/900/red → 22px/700/navy, body #1D3557→#243447.
- **pages/0_Help.py** (~60) — top banner gradient→flat navy band, 21px/900→17/700; 6 ov-card
  gradients→flat tokens (#1D3557/#1D9E75/#378ADD/#EF9F27); shared CSS: card borders→#E2E8F1,
  gold .how/.ana/.help-analogy→#EEF3FB+navy border, purple terms/red emphasis→navy, grays→
  #3D4757/#243447, .tab-back #06AED5→#1D9E75, weights 800/900→700 (9), 11px→12px (4);
  charts: raw-vs-density bars #FCBF49/#06AED5→#B4B2A9/#1D9E75, scatter #06A77D→#1D9E75 +
  outlines #1B263B→#1D3557, dyad edges #9CA3AF→#B4B2A9, triangle red edges→navy, metric bars
  →[navy, teal, red-if-neg, #B4B2A9], plot_bgcolor #F8FAFC→#FAFBFD (4).
- **pages/1_Per_Root_Profile.py** (14) — picker banner gradient→#EEF3FB+navy, 18px/900/red→
  17/700/navy, purple chip→navy; "currently viewing" grays→#3D4757, red/purple root→navy;
  ayah/kayah cards → #E2E8F1/#FFFFFF/#243447, meta 11px gray→12px #3D4757; plot bg ×5.
- **pages/2_Network.py** (6) — version banner gradient→flat navy; legend box gradient→#EEF3FB+
  navy border+#243447 text; legend chips ORANGE #F77F00→#EF9F27, BLUE #06AED5→#378ADD.
- **pages/3_Motifs.py** (6) — tri-card → BG-CARD #FFFFFF + #E2E8F1 border, ar #1B263B→#243447,
  meta 11px #6B7280→12px #3D4757; section header 800→700, #6B7280→#3D4757.
- **pages/4_Ayah_Browser.py** (6) — ayah-card same card treatment; plot bg →#FAFBFD.
- **pages/8_Export.py** (12) — HTML reading-guide styles: h1/h2 red/gold→navy, gradient→#EEF3FB,
  code/body/meta →#EEF3FB/#243447/#3D4757; xlsx export: Font E63946→1D3557, 6B7280→3D4757,
  PatternFill FFF8E1→EEF3FB.
- **pages/8a_Interpret.py / 8f_Practical_Lens.py** (1+1) — plot_bgcolor #F8FAFC→#FAFBFD.
- **pages/9_Topic_Modeling.py** (10) — quadrant palette: Core #2A9D8F→#1D9E75, Synonym #06AED5→
  #378ADD, Unrelated #9CA3AF→#B4B2A9 (chips #6B7280→#3D4757); guide lines→#B4B2A9; annotation
  colors matched; Contrastive RED kept (divergent semantics).
- **pages/9_Usage.py** (9) — bootstrap #198754/#dc3545→#1D9E75/#E63946 (status ok/fail);
  #555→#3D4757; #f8f9fa/#6c757d strip→#EEF3FB/#1D3557; map outlines #333/#666→#B4B2A9 (3);
  DAU line #E63946→#1D9E75; grid #eee→#E2E8F1.
- **pages/14_Disjoint_Letters.py** (16) — palette constants: TEAL→#1D9E75, AMBER #F77F00→#EF9F27,
  GREY #9CA3AF→#B4B2A9, ICE #CADCFC→#B4B2A9 (null histograms = comparators), LT→#1D9E75,
  PURPLE→#378ADD (propagates to all charts); 4 hint banners (#F1FAF9/#EAF6F4/#F4F0FB×2 + teal/
  purple borders) → #EEF3FB + navy; verdict box #FFF3B0→#EEF3FB+navy border-left; "other" series
  #D9DEE7×3/#E2E6EC→#B4B2A9; scorecard rows #E5E7EB→#E2E8F1, #6B7280→#3D4757.
- **pages/15_Signal.py / 16_Biology.py / 17_Two_Books_Summary.py** (7+9+5) — same constant
  remap (TEAL/AMBER/GREY/ICE/PURPLE/GREEN); purple hint banner in 16 → #EEF3FB + navy.
- **pages/18_Spatial_Patterns.py** (8) — caveat banner #FFF7ED/#F77F00/#7A3E00 → #EEF3FB/navy/
  #243447; archetype cards #F7F3FC/#7209B7/#5A2D8C → #EEF3FB/#1D3557/#243447; ambiguous-roots
  line #7A3E00→#3D4757.
- **pages/19_Concept_Deep_Dive.py** (16) — caption override #111111→#3D4757; chips #0B1320/
  #E8EEF6/#444 → #243447/#EEF3FB/#3D4757; _RELC: spatial #888780→#B4B2A9 (per spec — now shares
  GREY-DATA with orthogonal), divergent #E24B4A→#E63946; gray fallbacks #999/#888780/#666→
  #B4B2A9/#3D4757; guide rings #D7DEE8→#C9D6E8; ring labels #8A93A6→#3D4757; venn SURFACE
  labels #185FA5→#378ADD.
- **pages/20_Ayah_Deep_Dive.py** (14) — same caption/chip treatment; verse 29px #0B1320→#243447;
  _RELC9: co-located #888780→#B4B2A9, divergent #E24B4A→#E63946, fallback #888→#B4B2A9;
  match % #888→#3D4757; divergence list #111/#1B263B→#243447 (3).
- **pages/22_Lens_Lab.py** (9) — TEAL→#1D9E75, GREY→#B4B2A9 (verdict classes; AMBER #E9C46A
  already the spec token); card border #E5E7EB→#E2E8F1; metadata/boundary text {GREY}/#44546A→
  #3D4757; hbar track #F1F5F9→#E2E8F1; poetry comparator bars #5DCAA5→#B4B2A9 ×2.
- **feedback.py, 5_Compare, 7_Statistics, 8b, 8c, 8d, 21_Feedback** — already clean (0 hits).

Intentionally left (with reason):
- state.py L139 + L1004: the two progress-ribbon gradients (CSS dlribbon + JS running-state
  shine) — the sanctioned exception; the JS idle-state gradient WAS flattened to #1D3557.
- pages/8e_Calibration.py L180-182 tier vlines (#7209B7/#06AED5/#80B918): mirror the tier colors
  defined centrally in pair_classification.py (out of sweep scope, also feeds 8f marker colors);
  recoloring only the page literals would desync threshold lines from the data points.
- pages/2_Network.py L229 PURPLE legend chip (#7209B7): the legend names its colour in the text
  ("PURPLE"); recoloring the swatch without rewording (wording is frozen) would make the label
  false. ORANGE/BLUE chips were movable to #EF9F27/#378ADD without contradiction.
- Arabic content sizes 16-29px and emoji icon sizes (36px .ov-icon, 22px .insight-card .icon)
  kept per the spec's content-text allowance.

Verified: host-grep `F77F00|FCBF49|FFF3B0|FFF8E1|text-shadow|linear-gradient` → only the two
ribbon-gradient lines in state.py; `font-weight: 800/900` → zero hits anywhere; no font-size
below 12px remains; full hex inventory of all swept files is on-palette except the three
documented leftovers above. Snippet py_compile clean.

## Phase 12 — Help overhaul (agent)
pages/0_Help.py brought current with v2.0 and the LOCKED UI STANDARD (was pre-re-spine).
- **Structure**: help content data (CONCEPTS · GLOSSARY · CHART_GUIDES · PAGE_TOUR) hoisted
  above the tabs so the new 📌 "WHAT THIS HELP COVERS" metric row (rule 1) computes its counts
  from the page's own structures (pages toured = sum over PAGE_TOUR groups; glossary/concepts/
  chart-guide counts = len(); lenses = 18 mirroring Lens Lab); all five metrics carry deep help=.
  Tab "🧭 Two Books" renamed "🧭 Scales & Lens Lab". No new charts added (help page — the live
  case-study charts already carry the visual load); cross-ref scatter's gray vline → GREY-DATA.
- **Overview**: app-description analogy now covers READ + TEST + surface-form input; NEW
  sidebar-spine card documenting the six v2.0 nav groups (📖 READER · 🧪 LENS LAB · 🧭/🔤/🧩
  scales · 🛠️ TOOLS & FEEDBACK) with the "formerly Two Books → three scales, nothing renamed"
  note; section-card grid counts now computed (f-string) and the Two Books card replaced by a
  Scales & Lens Lab card; jump row extended to 5 (adds 🔭 Āyah Deep-Dive + 🧪 Lens Lab).
- **Concepts**: #11 reworded ("Two Books section" → the three sidebar scale groups); NEW #12
  "The gate — how a claim earns 'distinctive'" (equal-N + permutation null + comparators +
  positive control, drug-trial analogy) and NEW #13 "Roots in, surface forms welcome"
  (root-based analysis as standard practice, transparency chip, ambiguity chooser, hover forms).
- **Glossary**: deduped the double TF-IDF; Surface form expanded (typed-form→root mapping +
  chip); Meccan/Medinan marked control-only + a dedicated control-only entry; NEW entries:
  Fāṣila/seal (0.18 vs sajʿ 0.04 / ord 0.10, fit z≈+12), Echo-set/return (~+3σ, #42), Relation
  types (consensus·resonant·direct·co-located·orthogonal·divergent), Mask 🎭 (incl. what
  "project out the seal class" means), Hero strip, Verdict classes, Gate/equal-N, σ vs z,
  FDR/Benjamini–Hochberg, PPMI ("frequency ≠ association"), Juilland D, GLOBAL motif vs LOCAL
  formula (#66), 📍 takeaway line. Muqaṭṭaʿāt entry gains the Moran I +0.54 / p<10⁻⁴ anchor.
- **Chart reading**: NEW lead banner stating the two app-wide conventions (computed 📍
  takeaway on every chart, ❓ tooltip on every metric); NEW guides for the Āyah hero strip,
  the radial bond map (sector=type · distance=strength · size=frequency), and the
  null-histogram-+-observed-line idiom.
- **Page tour**: rebuilt as nav-mirroring groups (HOME / READER / LENS LAB / the three scales /
  TOOLS & FEEDBACK), now 24 pages: NEW entries for Āyah Deep-Dive (hero strip + 🎭 mask),
  Concept Deep-Dive, Lens Lab (verdict cards + Run-live on cards 3/9), Interpret, Practical
  Lens, Calibration, Feedback & Bugs, Usage, Help; "(Two Books)" suffixes → scale tags; Home
  entry updated (lowercased tab names; surface-form input noted).
- **Scales & Lens Lab tab** (ex Two Books): re-spine intro; NEW Lens Lab guide rows (card
  anatomy · the four verdict classes · what a GATE is · what ▶ Run-live does on cards 3 and 9 ·
  headline numbers matching FINDINGS_SYNTHESIS: #42 ~+3σ, seals 0.18 vs sajʿ 0.04 / ord 0.10,
  fit z≈+12, Moran I +0.54 p<10⁻⁴, coverage ~74%); the five ex-Two-Books page cards retagged
  with their scale; stats-reading rows kept.
- **Troubleshooting**: NEW items for the surface-form mapper ("typed عليم, analyzed علم"),
  the 🎭 mask removing rhyme-only echoes, and the read-the-📍-line/hover-❓ habit; stale "red
  button" wording and 🔄 START OVER label fixed (now ↺ Start over).
- Verified: mount copy is fresh-but-truncated at the old byte size (GOTCHA confirmed again) —
  lines 1–856 compiled directly from a fresh copy; all post-cut changed blocks re-emitted to
  /tmp/help/snip2.py and py_compile'd clean. Host-grep: `Two Books tab|EXPLORE|DEEP DIVES` →
  0 hits (remaining "Two Books" mentions are intentional "formerly" framings);
  `#F77F00|#FCBF49|#FFF3B0|#FFF8E1|linear-gradient|text-shadow` → 0 hits.
