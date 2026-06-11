# Structural Twins — Session Handoff
_Last worked: 2026-06-08. Scope: the Structural Twins (Mathāni) app page._

## What this feature is
`pages/23_Structural_Twins.py` — a Streamlit page serving the **mathani** finding:
verses that share ≥50% of their distinct roots (set-Jaccard) are "structural twins."
It is the research probe `research/nuance/mathani_39_23/` shipped as a feature.

**Self-contained by design:** the page loads ONLY `mathani_twins.json` (repo root),
never the live corpus/Book6. This is deliberate — it cannot break other pages.
Do NOT wire it to the live corpus.

## Key numbers (fixed; from the json)
- 3,523 twin pairs vs ~2,118 expected under a vocab/length-matched scramble null → z = +6.5
- ~60% is a vocabulary artifact; the +66% excess is the genuine structure (state this honestly)
- 34.5% of 6,236 verses have ≥1 twin; 4,084 have none (distinctive)
- 1,320 "strong" pairs (≥66%); 74% of twins span different surahs
- Top echo hub: Ar-Rahman (55) — 1,003 links, heavy self-refrain
- Most-linked verse: 37:167 (33 twins)

## Page structure (zoom-out narrative)
1. Header + 9 compact KPI chips (hover = definition; teal ⓘ cue + "hover" hint line)
2. **Verse level** — Surah/Ayah dropdowns (narrow) → selected verse + twin list
   (one line each: `ref · name  %  shared-roots  Arabic`) + twin-strength chart.
   If the selected verse has NO twin → success message + `st.stop()` (clean page).
3. **Surah level** — uses the chosen surah: chips (verses w/ twin, internal/external
   links, top partner) + "surahs that echo it most" bar + internal-vs-external donut.
4. **Whole-Qur'an statistics** (outlined navy box + "how to read the five"): gauge vs
   null, twin strength, echo hubs, where-twins-live donut, twins-per-verse.
5. **More granular cuts** (green concept box): threshold sensitivity, surah-distance,
   roots-that-drive-twinning (ربب/كذب/قول/إله), surah↔surah echo MATRIX (heatmap;
   diagonal = self-refrain), roots-shared-per-pair.

Arabic root labels in Plotly use `arabic_reshaper`+`bidi` (present in the live app;
absent in the sandbox — `shape()` degrades gracefully).

## Not a duplicate
The surah↔surah matrix is verse-twin structure, distinct from existing app heatmaps
(5_Compare_Heatmaps = surah×root; 2_Network = root co-occurrence; 18_Spatial = concept).

## Nav / icon
Listed under Lens Lab in `state.py` with icon `♊`. It is NOT the 19th lens — it shares
only the gate methodology (observed vs null, z). If reclassifying, it can get its own group.

## Deploy
The sandbox CANNOT run git here (`.git/config` is unreadable over the mount) and must NOT
edit large existing files like `state.py` (mount writes corrupt them — took the app down once;
recovered via `git checkout`). Edit `pages/23_Structural_Twins.py` via bash heredoc + verify
with `streamlit.testing.v1.AppTest`, then the USER deploys from their machine:

    cd C:\Users\torki\Downloads\Quran_Root_Explorer_Web_v1.2
    .\deploy.bat   # stages all, commits, pushes origin(GitHub) + hf(Hugging Face)

## State / pending
- Page edited + AppTest-verified clean. **User must run `deploy.bat`** to push the latest.
- AppMastery course: NO changes needed — M05/M07/M10/COURSE_INDEX still accurate (numbers
  unchanged; today's work is visualization depth, not a new finding). Optional one-liner:
  note the surah-echo map rediscovers Ar-Rahman's self-refrain.

## Shipped 2026-06-08 (this session, verified via AppTest; pending deploy.bat push)
- Per-verse twin-map: "where {verse}'s twins land (by surah)", gated to >=5 twins (verse level)
- Root as connector: "Shared root" selectbox (top 30 by reach) -> surahs it links + example pairs (root level)
- Revelation-era flow: donut of Meccan/Medinan/cross twin pairs. NOTE: MEDINAN set (28 surahs)
  is the traditional scholarly classification, NOT computed, disputed for several surahs — caveat
  is shown in-page. Defined as `MEDINAN = {...}` near the top of the file.
- Page now has 3 selectboxes (Surah, Ayah, Shared root) and the zoom order:
  verse -> surah -> root -> whole-Qur'an stats -> granular cuts -> revelation-era flow.

## Possible next (not built)
- Per-verse twin-map could become a mini surah×ayah heatmap for very high-twin refrain verses
- Root-connector: add a cross-book vs local ratio metric per root
- Sankey for revelation-era flow instead of donut (if richer breakdown wanted)
