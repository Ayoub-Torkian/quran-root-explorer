"""Topic Map — overview of corpus-wide topics discovered from two signals."""
from __future__ import annotations
import streamlit as st
import pandas as pd

from state import get_corpus, hero, layer, log_page
import topics as T

st.set_page_config(page_title="Topic Map", page_icon="🗺️", layout="wide")
log_page("topic_map")
corpus = get_corpus()

hero("🗺️ Topic Map",
     "Corpus-wide thematic clusters discovered from two independent signals: "
     "co-occurrence stability (who shares verses) and distributional similarity "
     "(who has similar partners). All numbers are computed from the data.")

st.markdown(
    '<div class="landscape-hint">📱 Rotate sideways for clearer tables.</div>',
    unsafe_allow_html=True,
)

with st.expander("📌 How topics are detected (1-min)", expanded=False):
    st.markdown(
        "**Signal 1 — co-occurrence stability.** Louvain community detection is "
        "run 30 times with different random seeds and 3 resolutions. A pair "
        "of roots lands in the same topic if they co-cluster in ≥70% of runs.\n\n"
        "**Signal 2 — distributional similarity.** PPMI-weighted co-occurrence "
        "matrix, reduced with SVD, cosine in the reduced space. Captures "
        "whether two roots appear in *similar contexts*, even if they never "
        "share a verse.\n\n"
        "Topics shown here are the connected components after applying the "
        "stability threshold. Topics with very few members or low stability "
        "are still listed but flagged."
    )

with st.spinner("Loading topic cache (first run: 5–10 min one-time)…"):
    cache = T.compute(corpus)

c1, c2, c3 = st.columns(3)
c1.metric("Nodes (roots)", cache.get("n_nodes", 0))
c2.metric("Edges (root pairs)", cache.get("n_edges", 0))
c3.metric("Topics detected", len(cache.get("topics", [])))

st.divider()
layer(1, "Topics by size")

topics = cache.get("topics", [])
stab = cache.get("stability", {})

def _mean_internal_stability(members):
    vals = []
    for i, a in enumerate(members):
        for b in members[i+1:]:
            key = (a, b) if (a, b) in stab else (b, a)
            if key in stab:
                vals.append(stab[key])
    if not vals:
        return 0.0
    return float(sum(vals) / len(vals))

rows = []
for idx, members in enumerate(topics):
    members = list(members)
    rows.append({
        "Topic #": idx + 1,
        "Size": len(members),
        "Mean stability": round(_mean_internal_stability(members), 3),
        "Members (first 6)": ", ".join(sorted(members)[:6]) +
                              ("…" if len(members) > 6 else ""),
    })
if rows:
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No topics passed the stability threshold yet — the cache may "
            "still be building. Refresh in a minute.")

st.divider()
layer(2, "Topic explorer")
if topics:
    options = [f"Topic {i+1} ({len(t)} members)" for i, t in enumerate(topics)]
    sel = st.selectbox("Pick a topic to inspect", options, index=0)
    sel_i = options.index(sel)
    members = sorted(topics[sel_i])
    st.markdown(f"**Members ({len(members)}):** " + ", ".join(members))
    mean_s = _mean_internal_stability(members)
    st.metric("Mean pairwise stability inside topic", round(mean_s, 3))

st.divider()
st.caption(
    f"Cache: {cache.get('n_seeds', 0)} seeds × {len(cache.get('resolutions', []))} "
    f"resolutions, stability threshold {cache.get('stability_threshold', 0)}. "
    f"Method: Louvain stability + PPMI/SVD distributional similarity. "
    f"Computed in {cache.get('compute_seconds', 0):.0f} seconds."
)
