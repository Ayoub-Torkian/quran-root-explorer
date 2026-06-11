"""My Topics — for the user's input root: topic membership + quadrant lists."""
from __future__ import annotations
import streamlit as st
import pandas as pd

from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, log_page, per_root_hint)
import topics as T

st.set_page_config(page_title="My Topics", page_icon="🎯", layout="wide")
log_page("my_topics")
corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

hero("🎯 My Topics",
     "Topic membership for your input roots, plus the two latent-finding lists "
     "computed from the corpus.")
per_root_hint(compact=True)

st.markdown(
    '<div class="landscape-hint">📱 Rotate sideways for clearer tables.</div>',
    unsafe_allow_html=True,
)

with st.spinner("Loading topic cache…"):
    cache = T.compute(corpus)

roots = R.get("input_roots") or []
if not roots:
    st.info("Type one or more roots above and press Enter to see topic memberships.")
    st.stop()

for root in roots:
    st.markdown(f"### `{root}`")
    topic_i, members, mean_s = T.get_topic_for_root(cache, root)
    if topic_i < 0:
        st.warning(f"`{root}` is not assigned to any stable topic (stability "
                   f"threshold {cache.get('stability_threshold', 0)}).")
    else:
        st.markdown(
            f"**Belongs to Topic {topic_i + 1}** "
            f"({len(members)} members, mean internal stability **{mean_s:.3f}**)."
        )
        st.markdown("**Other members:** " +
                    ", ".join(sorted(m for m in members if m != root)))

    quad = T.quadrant_lists(cache, root, k=8)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔄 Contrastive partners** (high co-occurrence, low "
                    "distributional similarity — likely antithetical pairings):")
        if quad["contrastive"]:
            st.dataframe(
                pd.DataFrame(quad["contrastive"],
                             columns=["root", "co-occur stability", "distr. similarity"]),
                use_container_width=True, hide_index=True,
            )
        else:
            st.caption("None in this corpus.")
    with col2:
        st.markdown("**💡 Distributional synonyms** (low co-occurrence, high "
                    "distributional similarity — latent semantic neighbours, "
                    "not visible by reading verses alone):")
        if quad["distributional_synonym"]:
            st.dataframe(
                pd.DataFrame(quad["distributional_synonym"],
                             columns=["root", "co-occur stability", "distr. similarity"]),
                use_container_width=True, hide_index=True,
            )
        else:
            st.caption("None in this corpus.")

    st.divider()

st.caption("Both signals are computed from the corpus only. Every value above "
           "is a number, not an interpretation.")
