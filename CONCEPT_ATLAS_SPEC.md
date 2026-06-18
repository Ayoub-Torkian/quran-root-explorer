# Concept Atlas — one-page SPEC (sign-off before deep dive)

## Purpose / gap filled
One corpus-wide **map of the conceptual territory** — the integrative surface the app lacks. The Network
page is query-restricted; Topic Map is a thin orphan; Discovery Map is about *findings*, not *concepts*.
The Atlas shows the WHOLE landscape at a glance and is the launch point into Search. Directly serves the
locked "map of the territory" + insight-per-effort rules, and it **reduces patchiness** (absorbs/retires
Topic Map + My Topics rather than adding a loose page).

## The object (precise definitions — so it's a map, not a hairball)
- **Nodes** = the top ~150 CONTENT roots (drop the ~10 ubiquitous ones: الله، قال، کون…). **Size** =
  importance (frequency, optionally eigen-centrality). **Label** = only the largest ~40 nodes (rest on hover)
  → readable, uncluttered.
- **Edges** = **attraction (PPMI)**, the validated metric — and only the **backbone**: each node keeps its
  top ~3 above-chance partners (sparse, legible), not all co-occurrences. This is the #1 anti-hairball rule.
- **Clusters = themes** = Louvain communities on the attraction graph; each cluster is a colour-bordered
  region with a 1–2 word auto-label (its highest-attraction roots). This *is* the topic layer, unified.
- **Colour** = revelation phase: each root's weighted-mean nuzūl rank → Meccan↔Medinan gradient (reuses the
  validated nuzūl logic). So the map carries the **temporal journey** (early→late) as colour, per the locked
  diagram rule.
- **Layout** = community-grouped (themes sit together); precomputed once, cached.

## Interaction (phased — ship value early, keep it actionable not decorative)
- **Phase 1 (MVP):** the static dense map + legend + a compact **theme index** (each theme = a row of its
  top roots as **clickable buttons** → jump to Search via the existing `_pending_q`/snapshot path). Even
  without graph-click, every concept is one click from its full profile. This alone is the flagship.
- **Phase 2:** click a node on the graph itself (Streamlit `st.plotly_chart` selection events) → inline
  concept snapshot (reuse the Search snapshot card) → "open in Search". Add a theme filter + a Meccan/Medinan
  toggle (reuses the phase split).

## Reuse (no new engines — all validated)
Attraction PPMI (Network), nuzūl skew + timeline (Search), importance/centrality (Network stats), Louvain
communities (Network), the snapshot card (Search). The Atlas is **synthesis, not new computation.**

## IA / sustainability
New page `pages/39_Concept_Atlas.py`, placed in **DISCOVER** (top, as "🗺️ Concept Atlas · the territory").
**Retire** Topic Map (8b) + My Topics (8c) into it (or fold their views in) so the nav gets *cleaner*, not
patchier. Update `NAV_SECTIONS`; remove the two orphans' nav entries.

## Performance (insight-per-effort)
All corpus-wide stats (co-occurrence, PPMI, communities, nuzūl means, importance, layout) computed **once**
in a `@st.cache_data` build; the page renders from the cache. Target: sub-second after first load.

## Honesty / watch-outs
- The map's value is **navigation + orientation**, not discovery — it shows known structure beautifully;
  it is NOT a new latent feature. [INFERRED]
- Failure mode = decorative hairball. Guardrails above (backbone edges, ≤40 labels, theme regions) are the
  contract; if Phase-1 doesn't read cleanly at a glance, we fix readability before adding interactivity.
- Themes from Louvain are descriptive, not canonical; label them as "auto-grouped."

## Value assessment (per locked criteria)
- Insight-per-effort: **HIGH** — whole landscape in one glance, one click to any concept's profile.
- Integration: **HIGH** — unifies Search + Network + topics + nuzūl; removes 2 orphan pages.
- Effort: **medium-high** (Phase 1 medium); Risk: **medium** (readability), mitigated by the backbone rules.

## Ranked recommendation
1. **(Recommend) Build Phase 1** (static territory map + clickable theme index + retire Topic Map/My Topics).
   Ships the flagship + cleans the IA. Validate readability on the real corpus before wiring interactivity.
2. Phase 2 (graph-click → inline snapshot → open in Search) once Phase 1 reads cleanly.
3. Defer the Meccan/Medinan animated journey until Phases 1–2 land.

**GATE: sign off on (a) node=top-150-content-roots, (b) edges=PPMI top-3 backbone, (c) themes=Louvain,
(d) colour=nuzūl phase, (e) retire Topic Map + My Topics into the Atlas. Then I build Phase 1.**
