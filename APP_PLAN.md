# APP PLAN — the app is the MAIN INSTRUMENT (co-priority with research)

**Mandate (user):** the app is not a side-deliverable. It is the primary tool for users to
**(1) READ** the Qur'an, **(2) TEST** different ideas/lenses live, **(3) give FEEDBACK** on novel
ideas, and **(4) report BUGS**. Research findings only matter if users can read, probe, and
challenge them in the app. This file keeps app design explicitly in scope as research progresses.

## LOCKED UI STANDARD (user-mandated, 2026-06-07 — apply to EVERY page, new and old)
1. **Comprehensive-summary headline metrics FIRST** in every section: a st.metric row opens the
   section before any detail (counts, key statistic, verdict), each metric with a `help=` tooltip.
2. **`help=` hover (?) everywhere** — every metric, chart and control gets a quick-explanation
   tooltip; assume the user meets the number cold.
3. **Charts over tables wherever a finding can be SHOWN**: primarily bar, scatter, pie/donut,
   network. Every filed claim that has numbers should have a visual.
4. **Interpretation sections are first-class**: data-driven, specific, deep — interpret THE numbers
   on screen (this run, this verse, this class), never generic/common-sense filler. Where output is
   dynamic, generate the interpretation from the computed values.
   4b. **Every chart carries a "📍 What to take from this" line** (user-mandated after the bond-map
   review): name the takeaway explicitly with the computed values; geometry must MEAN something
   (e.g. radial bond map: sector = type, distance = strength, size = frequency) — if a layout is
   arbitrary (spring/force), replace it with one whose position encodes the message.
5. **Help enrichment wherever help exists** (page-level expanders, the Help page): concrete
   examples, what-the-number-means, boundaries — same honesty rules as the paper.
6. **PLAN-FIRST (user-mandated, after the face-lift saga):** every new feature/page starts with
   a short written design — FORM (layout sketch, which DESIGN_SYSTEM.md tokens, type steps) and
   CONTENT (data shown, charts + their takeaways, edge cases) — presented for approval BEFORE
   code. No more style-by-iteration. DESIGN_SYSTEM.md governs all form decisions.

## v3 BACKLOG (LOCKED — user suggestion 2026-06-07, queued, NOT current work)
**Recitation/qirāʾah module**: user picks any sūrah/āyah, reads aloud, app corrects and GATES
progression until read correctly; live position tracking; sample recitations for practice.
Goal: customer-base growth → future monetization.
Market reality (researched): crowded + well-funded — Tarteel (leader, real-time word-level
error detection), Qari AI & Tilawa.ai (phonetic tajwīd, 16+ rules), TajweedMate, Quranly,
Thurayya (kids). Polished graphics/sound is table stakes, not differentiation.
WHAT IT TAKES TO DO IT AND WIN (the build plan, not a refusal):
1. **Wedge = KIDS** (5–12) — the least defended segment (only Thurayya plays there seriously,
   and weakly on gamification). Parents PAY for measurable Qur'an progress; kids pedagogy
   actually WANTS our strict mastery-gate ("level cleared only when read correctly") — it maps
   to game mechanics (levels, streaks, badges, a visible sūrah-map of "territory conquered").
   Adult market = fight Tarteel head-on; kids market = win a beachhead first, expand upward.
2. **Engine path (staged):** v3.0 = word-level accuracy gate via fine-tuned open ASR on Qur'anic
   audio (achievable solo/small team; explicitly not tajwīd-grade — honest scope) → v3.5 =
   license or partner for phonetic tajwīd scoring (Qari-AI-class) → v4 = own model only if
   revenue justifies the data program (thousands of hours of graded kid + qari recordings —
   note: kid-voice data is exactly what incumbents lack; collecting it WITH consent via the
   app is itself a moat).
3. **Chassis:** separate mobile-first client (Flutter/React-Native) talking to a scoring API;
   the Streamlit app stays the research/analytics instrument and feeds the insight layer.
4. **Differentiators (in order):** ① mastery-gate-as-game (tunable strictness: kid/teacher
   modes — false rejections must never punish a 6-year-old); ② UNDERSTANDING layer no
   competitor has — after a verse is cleared, an age-tuned insight card from our 18-lens data
   (this verse's seal & what it means, where the verse returns, its concept constellation):
   "read it right, then know what you read"; ③ parent/teacher dashboard from our analytics
   DNA (real progress curves, weak-letter heatmaps — we are BETTER at charts than audio apps);
   ④ Lens-14 rhythm/isochrony practice once the recited layer unblocks (unique, research-backed).
5. **Monetization:** family subscription (per-child progress) + B2B licensing to madrasas/
   weekend schools (the dashboard sells it) + halal-strict no-ads stance as a trust signal.
6. **Success conditions to honor before building:** a licensed/partnered scorer OR a fine-tune
   hitting >95% word-accuracy on kid voices; one madrasa pilot committed; the insight-card
   content pipeline auto-generated from FINDINGS/EVIDENCE (cheap for us, impossible for them).

## Principle: the app is an EVIDENCE INSTRUMENT, not a claims engine
Every lens shown in the app displays — always — its **statistic + null + equal-N + comparator +
gate verdict**. No "miracle" claims; honest nulls are shown as first-class results (most modalities
ARE null — that is the finding). This mirrors the locked methodology (`DESIGN_STANCE.md`).

## The organizing model (already agreed): MODALITY × SCALE, on a shared index
- **Scales** (how we read): 🧭 Position · 🔤 Sequence (char) · 🧩 Semantic (root/word). Shipped in v1.3.
- **Modalities** (what we test): the 12 lenses + the signal-geometry/positional-directional lenses.
- **Fusion unit = the āyah** (the "sign"): click one āyah/passage → see it read through every
  available lens at once, each with its null. This is the app's hero interaction.

## Four surfaces to build
1. **Reader** — read the Qur'an (exists in part via root explorer); make the āyah the clickable hero.
2. **Lens Lab** — one card per modality/idea. Each card: short claim, live run on a chosen
   passage/corpus, the statistic vs its null, equal-N + comparator, GATE verdict (pass/null), and a
   link to the EVIDENCE entry. Surfaces #42 (the one distinctive) prominently; shows the rest as
   honest nulls. Reuses `sequence_tests/*` detectors (each runs in ~2s).
3. **Feedback loop** — per-lens 👍/👎 + free-text note; a "propose a new lens/idea" form. Captured to
   a local store (e.g. `feedback/feedback.jsonl`) for us to review and turn into new modalities.
4. **Bug report** — a always-visible "report a bug" widget logging page + state + user note to
   `feedback/bugs.jsonl`.

## Phasing (realistic, incremental — NOT a stop-the-world overhaul)
- **v1.4 (next app release, incremental):**
  - Add **Feedback** + **Bug report** widgets (cheap, high value, unblocks user signal immediately).
  - Add a first **Lens Lab** page: render the 12 modality verdicts from EVIDENCE/COVERAGE as cards;
    make 2–3 fast lenses runnable live (recurrence #42, rhyme persistence, field-dynamics #46).
  - Embed/link `COVERAGE_MAP.html` as the "where we are" view.
  - Finish the shipped Two Books 🔜 items (alt-chronology robustness, spatial autocorrelation).
- **v2.0 (re-spine, scheduled, not yet):** reorganize nav around MODALITY × SCALE; the āyah-hero
  fusion view; every lens live and interactive. Two Books folds in as the three scales.

## SHIPPED (v1.5 increment): per-verse Seal & Formula panel on Ayah Deep-Dive
The 🔭 Ayah Deep-Dive page now carries a **🔏 Seal & formulas (Lens 17 / #66)** expander per seed āyah
(template = the 8:61 bilingual case study in RootCourse): the ending-word and its class size, a LIVE
#62 content-fit z (150 same-N nulls, instant; verified on 8:61 → العليم, class 26, z=+11.6), the #77
referent flag (divine-marked / other), the honest cross-text boundary line (#63 as corrected by #76:
0.18 vs sajʿ 0.04), and a per-root #66 table (āyahs · sūras · GLOBAL motif / LOCAL formula / mid).
Combined with the page's existing typed echo-set, the per-verse view (echo-set · seal-class ·
formula-class) is now live; the bound-set remains a manual/scholarly layer.

## How current research ideas map to app surfaces (keep this current)
- #42 intratextual recurrence (DISTINCTIVE) → Lens Lab flagship card + āyah-hero "where else does
  this passage recur" view.
- Signal-geometry / pointer (`IDEA_SIGNALS_GEOMETRY.md`) → Position-scale lenses; wavelet/locality
  demos (record: largely #33, no credit — show as an honest null demo).
- Positional/directional sub-unit lens → an āyah-internal visualizer (sub-unit spectrum char→root→
  morph; R→L default, reverse toggle).
- Masking/filtering toolkit → a "mask/filter" control on the āyah-hero view (include only Meccan /
  narrative / a field; project out a known axis) — makes the methodology tangible to users.

## Open decisions (ask the user when we start building)
- v1.4 scope: feedback+bug only first, or feedback+bug + first Lens Lab page together?
- Feedback storage: local file (private) vs a shared collector (multi-user)?
- Which 2–3 lenses to make live first in Lens Lab?

## Information architecture — the growing-nav problem (user-flagged, IN SCOPE, postponed to v2.0)
The flat nav list is long and getting longer (now ~25 pages + Feedback). This is the core reason the
re-spine is needed, NOT a cosmetic tweak. Target structure when we do it:
- **Top level = the three SCALES** (🧭 Position · 🔤 Sequence · 🧩 Semantic) — the categories we already
  have in Two Books — promoted to the app's primary axis.
- **Within each scale = the relevant MODALITIES/lenses**, each a card (claim · live run · null · gate).
- Collapse today's ~25 ad-hoc pages into this MODALITY × SCALE grid; Reader + Lens Lab + Feedback are
  cross-cutting, not more list items.
- Decision deferred deliberately: finalize the lens set first (research is still adding/retiring lenses),
  so the IA is designed once around the true, stable set rather than reorganized repeatedly.
DO NOT start the re-spine until the research sweep is at a stable stopping point. Until then, new pages
go into the existing groups (as Feedback did).

## Status
v1.4 feedback + bug widgets SHIPPED (feedback.py, pages/21_Feedback_and_Bugs.py, sidebar hook in state.py).
v1.5 per-verse Seal & Formula panel SHIPPED (pages/20_Ayah_Deep_Dive.py).

**v2.0 RE-SPINE PHASE 1 — SHIPPED (this session; gate satisfied: lens set stable at 18).**
- NAV re-spined (state.py NAV_SECTIONS): primary axis = 📖 READER · 🧪 LENS LAB · the three SCALES
  (🧭 Position · 🔤 Sequence · 🧩 Semantic, with Semantic sub-grouped Roots/Topics/Interpret) ·
  🛠️ TOOLS & FEEDBACK. Old build-history groups (EXPLORE / DEEP DIVES / TWO BOOKS) retired; pages
  regrouped by QUESTION (UI_REORG_NOTES). No page was moved/renamed — zero-risk regroup.
- LENS LAB SHIPPED (pages/22_Lens_Lab.py): one card per lens for all 18 — claim · statistic-vs-null ·
  comparator boundary · gate verdict; verdict-class sections (DISTINCTIVE / INTERNAL-ONLY / NULL /
  BLOCKED); scale + verdict filters; thesis banner; embedded COVERAGE_MAP. Source of truth =
  FINDINGS_SYNTHESIS.md (update the LENSES table there when verdicts change).
- Verified: py_compile both files; every nav target exists (fallback lists honored).

**v2.0 phase 2 (next app steps):**
- Make 2–3 fast lenses runnable LIVE inside Lens Lab cards (#42 recurrence, rhyme persistence —
  reuse sequence_tests detectors, ~2s each).
- Āyah-hero FUSION view: extend 20_Ayah_Deep_Dive into "this āyah through every lens" (Seal &
  Formula panel = the shipped seed); add the mask/filter control (signal-geometry toolkit).
- UI_REORG_NOTES locked decision: consolidate the multi-root "relationships" surface
  (Motifs + consensus + synergy) into one leveled page.
