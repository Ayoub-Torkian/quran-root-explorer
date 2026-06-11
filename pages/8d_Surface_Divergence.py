"""Surface-form Divergence — data-driven detection of semantically split roots."""
from __future__ import annotations
import streamlit as st
import pandas as pd

from state import get_corpus, hero, layer, log_page
import surface_divergence as SD

st.set_page_config(page_title="Surface Divergence", page_icon="🔬", layout="wide")
log_page("surface_divergence")
corpus = get_corpus()

hero("🔬 Surface-form Divergence",
     "Roots whose surface forms split into statistically distinct partner "
     "profiles. Detected with Jensen-Shannon divergence + bootstrap stability — "
     "no curated split list.")

st.markdown(
    '<div class="landscape-hint">📱 Rotate sideways for clearer tables.</div>',
    unsafe_allow_html=True,
)

with st.expander("📌 What this page tells you (1-min)", expanded=False):
    st.markdown(
        "Same triliteral root, but different morphological patterns can carry "
        "completely different meanings. كثر produces both كوثر (heavenly "
        "abundance, positive) and تكاثر (worldly accumulation, negative). "
        "Treating them as one node averages two distinct meanings.\n\n"
        "**Method.** For each root: (1) split its occurrences by surface form, "
        "(2) build a partner-distribution vector for each form, "
        "(3) measure pairwise Jensen-Shannon divergence between vectors, "
        "(4) hierarchical-cluster forms by divergence, "
        "(5) bootstrap-resample to confirm the split is stable.\n\n"
        "Only roots with stability ≥ 0.60 across 20 resamples are flagged."
    )

with st.spinner("Loading surface-divergence cache (first run: 2–5 min one-time)…"):
    cache = SD.compute(corpus)

c1, c2, c3 = st.columns(3)
c1.metric("Roots scanned", cache.get("n_roots_scanned", 0))
c2.metric("Roots flagged as split", cache.get("n_splits", 0))
c3.metric("JSD threshold", cache.get("jsd_threshold", 0))

splits = cache.get("splits", [])
if not splits:
    st.info("No roots crossed the divergence + stability thresholds.")
    st.stop()

st.divider()
layer(1, "Split roots (ranked by maximum divergence)")

rows = [
    {
        "Root": s["root"],
        "Forms": s["n_forms"],
        "Max JSD": round(s["max_jsd"], 3),
        "Stability": round(s["stability"], 3),
        "Clusters": " | ".join(
            ", ".join(forms) for forms in s["clusters"].values()
        ),
    }
    for s in splits
]
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

st.divider()
layer(2, "Inspect a split root")
options = [s["root"] for s in splits]
sel = st.selectbox("Pick a root", options, index=0)
sel_split = next(s for s in splits if s["root"] == sel)
st.markdown(f"**Root** `{sel_split['root']}` — "
            f"max JSD **{sel_split['max_jsd']:.3f}**, "
            f"stability **{sel_split['stability']:.2f}**")

for cl_id, forms in sel_split["clusters"].items():
    st.markdown(f"#### Cluster {cl_id}")
    st.markdown("**Surface forms:** " + ", ".join(forms))
    partners = sel_split["cluster_top_partners"].get(cl_id, [])
    if partners:
        st.markdown("**Top partner roots (with counts):**")
        st.dataframe(
            pd.DataFrame(partners, columns=["partner", "shared verses"]),
            use_container_width=True, hide_index=True,
        )
    st.markdown("")

st.caption(f"Method: Jensen-Shannon divergence between surface-form partner "
           f"distributions; hierarchical clustering at JSD threshold "
           f"{cache.get('jsd_threshold', 0)}; bootstrap stability across "
           f"20 resamples (≥ {cache.get('stability_threshold', 0)} required).")
