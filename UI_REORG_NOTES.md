# UI Reorganization — LIVE notes (deferred; do not act yet, do not forget)

Status: app organization kept LIVE/unchanged for now. These are locked decisions
for when reorg happens.

## LOCKED: the multi-root "relationships" surface
Motif, Consensus/Latent-motif, and Synergy answer ONE question — "how do >=2 roots
relate beyond pairwise?" — differing only by DOMAIN:
  - Motif            = within-verse co-occurrence (counts).            [pages/3_Motifs.py]
  - Consensus / Latent-motif = across-verse, >=2 modalities agree
    (meaning/territory/distribution).                                  [Deep Dives; deep_dive.py]
  - Synergy (interaction information) = true 3-way irreducibility
    (info no pair carries).                                           [NEW, not yet in app]
They share the same object (sets of roots) and question -> they belong in ONE place.
AGREED. Group them as one "Relationships / multi-root structure" surface, leveled:
pairwise strength -> within-verse motif -> across-verse latent -> 3-way synergy.

NOTE: per testing (EVIDENCE.md s13-15), synergy is a WEAK aggregate effect with no
FDR-surviving triads; if grouped, it enters as a minor diagnostic, not a headline.
The grouping rationale stands regardless of synergy's strength.

## Earlier finding (also locked): relational features are scattered by build-history
Same relational concept currently lives in >=4 places under >=4 names:
co-occurrence (Network+Home+Export), PMI/Jaccard/overlap (Compare&Heatmaps),
lead-lag/directional (buried as Network page section 4), co-location (Spatial
Patterns + Deep Dives), motifs (Motifs page). Consolidate by QUESTION, not artifact.
Make scale (sequence<->semantic) a toggle WITHIN each question, not separate page groups.
