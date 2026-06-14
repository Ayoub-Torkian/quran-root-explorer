# re-deploy 1779671310
"""Topic Modeling v2 — probabilistic, visual, comprehensive.

Per input root R you get:
  1. Probability-calibrated membership table for the top-N nearest roots
     (combined S1 co-occurrence and S2 distributional signals).
  2. S1 x S2 scatter visualization with quadrant overlay — see ALL partners
     of R in a single 2D map (core / contrastive / synonyms / unrelated).
  3. Topic statistics: cohesion, distinctiveness, mean intra-topic similarity,
     mean external similarity, and the cohesion gap (intra - external).
  4. Distinctive features: which partners discriminate R most from its kin.
  5. Surface-form divergence (filtered to input roots).
  6. Advanced expander: full corpus topic map.
"""
from __future__ import annotations
import streamlit as st
import pandas as pd
import numpy as np

from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, log_page, per_root_hint, needs_recompute)
import topics as T
import surface_divergence as SD

import plotly.graph_objects as go


st.set_page_config(page_title="Topic Modeling", page_icon="map", layout="wide")
log_page("topic_modeling")
corpus = get_corpus()

hero("Topic Modeling",
     "Probabilistic semantic-neighbourhood analysis for your input roots, "
     "with 2D quadrant visualisation, topic cohesion stats, and "
     "distinctive-feature ranking.")

st.markdown(
    '<div class="landscape-hint">Rotate sideways for clearer charts.</div>',
    unsafe_allow_html=True,
)

with st.expander("📌 What topic modelling adds beyond the Network tab (1-min)", expanded=False):
    st.markdown(
        "**The Network tab** asks one question: *do these roots share verses?* "
        "That is the **S1** signal (co-occurrence stability).\n\n"
        "**Topic Modelling** asks a second, independent question: "
        "*do these roots appear in the same kinds of verses?* "
        "That is the **S2** signal — distributional similarity computed by "
        "PPMI + SVD on the partner-vectors. Two roots can be distributionally "
        "similar even if they never appear in the same verse.\n\n"
        "**Why it matters — the four quadrants:**\n\n"
        "- **Core** (high S1 + high S2) — roots that share verses AND share "
        "contexts. The strongest semantic kin.\n"
        "- **Contrastive** (high S1, low S2) — roots that share verses but "
        "live in different contexts overall. Often **antithetical pairings** "
        "(virtue vs. vice, mercy vs. wrath) that the text deliberately places "
        "side-by-side.\n"
        "- **Latent synonyms** (low S1, high S2) — roots that almost never "
        "share verses with yours yet inhabit the same contexts. "
        "**Invisible to verse-reading alone.** This is the most valuable "
        "output: hidden semantic kin you would not connect from co-occurrence.\n"
        "- **Unrelated** (low S1 + low S2) — neither share verses nor contexts.\n\n"
        "**Joint probability** in the table = (S1 + S2) / 2, a calibrated "
        "combined ranking. **Cohesion gap** = mean similarity inside the topic "
        "minus mean similarity outside — positive means the topic boundary "
        "is genuinely distinct in this corpus."
    )

raw, normalize, top_p, min_w, run = query_controls(corpus)
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

input_roots = R.get("input_roots") or []
if not input_roots:
    st.info("Type one or more roots above and press Enter.")
    st.stop()


# ─────────────────────────────────────────────────────────────────
# Focused compute with progress
# ─────────────────────────────────────────────────────────────────
cache_key = ("topic_focus_v4", tuple(input_roots), bool(R.get("normalize")))
if ("topic_cache" not in st.session_state
        or st.session_state.get("topic_cache_key") != cache_key):
    holder = st.empty()
    bar = holder.progress(0.0, text="Initialising topic modelling...")
    def cb(frac, text):
        try:
            bar.progress(min(max(float(frac), 0.0), 1.0), text=text)
        except Exception:
            pass
    cache = T.compute_for_roots(corpus, input_roots, progress_cb=cb)
    st.session_state["topic_cache"] = cache
    st.session_state["topic_cache_key"] = cache_key
    holder.empty()

cache = st.session_state["topic_cache"]


# ─────────────────────────────────────────────────────────────────
# Top-line stats card
# ─────────────────────────────────────────────────────────────────
nodes = cache.get("nodes", [])
emb = cache.get("embeddings")
idx = cache.get("embedding_idx", {})
stab = cache.get("stability", {})

c1, c2, c3, c4 = st.columns(4)
c1.metric("Ego-network nodes", cache.get("n_nodes", 0),
          help="Roots in the neighbourhood graph built around your inputs (your roots + their partners).")
c2.metric("Ego-network edges", cache.get("n_edges", 0),
          help="Co-occurrence links between those roots that pass the stability threshold.")
c3.metric("Topics detected (>=2 members)", len(cache.get("topics", [])),
          help="Stable Louvain communities found across seeds and resolutions — clusters of roots "
               "that keep landing together.")
c4.metric("Compute time", f"{cache.get('compute_seconds', 0):.1f} s",
          help="Wall-clock time for the ego-network + embedding computation (cached per query).")

st.caption(
    f"Louvain stability across {cache.get('n_seeds', '?')} seeds x "
    f"{len(cache.get('resolutions', []))} resolutions; "
    f"PPMI + SVD distributional embeddings (50 dims); "
    f"co-membership threshold {cache.get('stability_threshold', 0)}."
)

st.divider()


# ─────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────
def _prob(s1: float, s2: float) -> float:
    """Calibrated joint membership probability in [0, 1]."""
    return float(min(max((s1 + s2) / 2.0, 0.0), 1.0))


def _quadrant(s1: float, s2: float, hi: float = 0.5) -> str:
    if s1 >= hi and s2 >= hi:
        return "Core"
    if s1 >= hi and s2 < hi:
        return "Contrastive"
    if s1 < hi and s2 >= hi:
        return "Synonym"
    return "Unrelated"


def _build_neighbor_df(root: str) -> pd.DataFrame:
    """Every node (except root) with S1, S2, prob, quadrant."""
    if root not in idx or emb is None:
        return pd.DataFrame()
    i = idx[root]
    v = emb[i]
    cos = emb @ v
    rows = []
    for j, other in enumerate(nodes):
        if other == root:
            continue
        key = (root, other) if (root, other) in stab else (other, root)
        s1 = float(stab.get(key, 0.0))
        s2 = float(cos[j])
        rows.append({
            "root": other,
            "S1 (co-occurrence)": round(s1, 3),
            "S2 (context)": round(s2, 3),
            "Joint probability": round(_prob(s1, s2), 3),
            "Quadrant": _quadrant(s1, s2),
        })
    df = pd.DataFrame(rows).sort_values("Joint probability", ascending=False)
    return df


def _topic_stats(root: str) -> dict:
    """Cohesion, distinctiveness, gap, mean external similarity."""
    if root not in idx or emb is None:
        return {}
    ti, members, mean_s1 = T.get_topic_for_root(cache, root)
    out = {"in_topic": ti >= 0, "topic_size": len(members) if ti >= 0 else 0,
           "mean_S1_in_topic": round(mean_s1, 3) if ti >= 0 else None}
    # Mean S2 cohesion: average cosine to other topic members
    if ti >= 0 and emb is not None:
        i = idx[root]
        member_idxs = [idx[m] for m in members if m in idx and m != root]
        if member_idxs:
            sims_in = np.array([float(emb[m_idx] @ emb[i]) for m_idx in member_idxs])
            out["mean_S2_in_topic"] = round(float(sims_in.mean()), 3)
        # Mean S2 to nodes OUTSIDE the topic
        outside_idxs = [j for j in range(len(nodes))
                        if nodes[j] not in members and j != i]
        if outside_idxs:
            sims_out = np.array([float(emb[j] @ emb[i]) for j in outside_idxs])
            out["mean_S2_external"] = round(float(sims_out.mean()), 3)
            if "mean_S2_in_topic" in out:
                out["cohesion_gap"] = round(
                    out["mean_S2_in_topic"] - out["mean_S2_external"], 3)
    return out


def _scatter_quadrants(df: pd.DataFrame, root: str) -> go.Figure:
    """S1 vs S2 scatter with quadrant lines and root labels."""
    fig = go.Figure()
    color_map = {"Core": "#1D9E75", "Contrastive": "#E63946",
                 "Synonym": "#378ADD", "Unrelated": "#B4B2A9"}
    for q, color in color_map.items():
        sub = df[df["Quadrant"] == q]
        if len(sub) == 0:
            continue
        fig.add_trace(go.Scatter(
            x=sub["S1 (co-occurrence)"], y=sub["S2 (context)"],
            mode="markers+text", text=sub["root"], textposition="top center",
            marker=dict(size=12, color=color, line=dict(width=1, color="white")),
            name=q,
            hovertemplate=("<b>%{text}</b><br>S1: %{x:.2f}<br>"
                           "S2: %{y:.2f}<extra></extra>"),
        ))
    # Quadrant divider lines
    fig.add_hline(y=0.5, line_dash="dash", line_color="#B4B2A9",
                  annotation_text="S2 = 0.5", annotation_position="bottom right")
    fig.add_vline(x=0.5, line_dash="dash", line_color="#B4B2A9",
                  annotation_text="S1 = 0.5", annotation_position="top right")
    # Quadrant labels in corners
    fig.add_annotation(x=0.95, y=0.95, xref="paper", yref="paper",
                       text="<b>CORE</b><br>(high S1 + S2)", showarrow=False,
                       font=dict(size=11, color="#1D9E75"))
    fig.add_annotation(x=0.95, y=0.05, xref="paper", yref="paper",
                       text="<b>CONTRASTIVE</b><br>(high S1, low S2)",
                       showarrow=False, font=dict(size=11, color="#E63946"))
    fig.add_annotation(x=0.05, y=0.95, xref="paper", yref="paper",
                       text="<b>LATENT SYNONYMS</b><br>(low S1, high S2)",
                       showarrow=False, font=dict(size=11, color="#378ADD"))
    fig.add_annotation(x=0.05, y=0.05, xref="paper", yref="paper",
                       text="<b>UNRELATED</b><br>(low S1 + S2)", showarrow=False,
                       font=dict(size=11, color="#10243A"))
    fig.update_layout(
        title=f"Semantic-neighbourhood map of `{root}`",
        xaxis=dict(title="S1 — co-occurrence stability", range=[-0.05, 1.05]),
        yaxis=dict(title="S2 — distributional similarity (context)",
                   range=[-0.05, 1.05]),
        height=600, margin=dict(l=60, r=20, t=60, b=60),
        plot_bgcolor="#FAFBFD", paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="top", y=-0.12, xanchor="center", x=0.5),
    )
    return fig


def _distinctive_features(root: str, k: int = 5) -> list[tuple]:
    """Partners that most distinguish `root` from its kin — high S2 with `root`
    but low mean S2 with other input roots."""
    if root not in idx or emb is None or len(input_roots) < 2:
        return []
    i = idx[root]
    other_inputs = [r for r in input_roots if r != root and r in idx]
    if not other_inputs:
        return []
    other_idxs = [idx[r] for r in other_inputs]
    scores = []
    v = emb[i]
    for j, other in enumerate(nodes):
        if other == root or j == i:
            continue
        s_root = float(emb[j] @ v)
        s_others = float(np.mean([emb[j] @ emb[oi] for oi in other_idxs]))
        scores.append((other, round(s_root, 3), round(s_others, 3),
                       round(s_root - s_others, 3)))
    scores.sort(key=lambda x: -x[3])
    return scores[:k]


# ─────────────────────────────────────────────────────────────────
# Per-input-root sections
# ─────────────────────────────────────────────────────────────────
per_root_hint(compact=True)

for root in input_roots:
    st.markdown(f"## `{root}`")
    if root not in idx:
        st.warning(f"`{root}` is too rare to appear in the ego-network "
                   f"(needs >= 2 corpus ayahs).")
        st.divider()
        continue

    # Stats
    s = _topic_stats(root)
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("In a topic?", "yes" if s.get("in_topic") else "no",
               help="Whether this root landed in a stable Louvain community (>=2 members).")
    sc2.metric("Topic size", s.get("topic_size", 0),
               help="Number of roots in its topic, including the root itself.")
    sc3.metric("Mean S2 inside topic",
               s.get("mean_S2_in_topic") if s.get("mean_S2_in_topic") is not None else "n/a",
               help="Average distributional (context) similarity to the other topic members — "
                    "how alike their verse-contexts are, on a 0–1 cosine scale.")
    sc4.metric("Cohesion gap (inside - outside)",
               s.get("cohesion_gap") if s.get("cohesion_gap") is not None else "n/a",
               help="Positive = topic is genuinely distinct from outside. "
                    "Close to 0 = topic boundary is fuzzy.")

    # Scatter plot
    df = _build_neighbor_df(root)
    if len(df) == 0:
        st.info("No neighbours to plot.")
    else:
        st.plotly_chart(_scatter_quadrants(df, root), width='stretch')
        try:
            _qc = df["Quadrant"].value_counts()
            _n_core = int(_qc.get("Core", 0)); _n_syn = int(_qc.get("Synonym", 0))
            _n_con = int(_qc.get("Contrastive", 0))
            _top_nb = df.iloc[0]
            _syn_df = df[df["Quadrant"] == "Synonym"]
            _syn_txt = (f"the top latent synonym is **{_syn_df.iloc[0]['root']}** "
                        f"(S2 {_syn_df.iloc[0]['S2 (context)']}, almost never in the "
                        f"same verse — invisible to verse-reading alone)"
                        if len(_syn_df) else "no latent synonyms cleared the 0.5 line")
            st.markdown(
                f"**📍 What to take from this chart:** around `{root}` sit "
                f"{_n_core} core kin, {_n_con} contrastive partners and {_n_syn} latent "
                f"synonyms; the strongest overall neighbour is **{_top_nb['root']}** "
                f"(joint probability {_top_nb['Joint probability']}), and {_syn_txt}. "
                f"Position encodes the two signals (x = shares verses, y = shares "
                f"contexts) — similarity here is distributional, not a meaning claim."
            )
        except Exception:
            pass

        layer(1, "Top 15 neighbours by joint probability")
        top15 = df.head(15)
        st.dataframe(top15, use_container_width=True, hide_index=True)

        # Per-quadrant breakdown
        layer(2, "Quadrant breakdown (top 5 each)")
        qcols = st.columns(4)
        for col, q, color in zip(
            qcols, ["Core", "Contrastive", "Synonym", "Unrelated"],
            ["#1D9E75", "#E63946", "#378ADD", "#10243A"]
        ):
            sub = df[df["Quadrant"] == q].head(5)
            col.markdown(
                f"<div style='background:{color};color:white;padding:4px 10px;"
                f"border-radius:6px;font-weight:700;font-size:13px;'>"
                f"{q.upper()} ({len(df[df['Quadrant']==q])})</div>",
                unsafe_allow_html=True,
            )
            if len(sub) > 0:
                col.dataframe(sub[["root", "Joint probability"]],
                              use_container_width=True, hide_index=True)
            else:
                col.caption("None.")

        # Distinctive features (vs other inputs)
        if len(input_roots) >= 2:
            layer(3, f"Distinctive features — what separates `{root}` from "
                     f"the other inputs")
            dist = _distinctive_features(root, k=8)
            if dist:
                dd = pd.DataFrame(dist, columns=[
                    "partner", f"S2 with `{root}`",
                    "S2 with other inputs", "Discrimination (gap)"
                ])
                st.dataframe(dd, use_container_width=True, hide_index=True)
                st.caption(
                    f"Positive gap = partner is more associated with `{root}` "
                    f"than with the other input roots. Use for contrastive analysis."
                )
            else:
                st.caption("No distinctive features to report.")

    st.divider()


# ─────────────────────────────────────────────────────────────────
# Surface-form divergence (filtered to input roots)
# ─────────────────────────────────────────────────────────────────
st.markdown("## Surface-form divergence (your roots only)")
holder_sd = st.empty()
bar_sd = holder_sd.progress(0.0, text="Loading surface-divergence cache...")
try:
    sd_cache = SD.compute(corpus)
    bar_sd.progress(1.0, text="loaded")
    holder_sd.empty()
except Exception as e:
    holder_sd.empty()
    sd_cache = None
    st.error(f"Could not load surface-divergence cache: {e}")

if sd_cache is not None:
    flagged = [SD.get_split(sd_cache, r) for r in input_roots]
    flagged = [s for s in flagged if s]
    if not flagged:
        st.info("None of your input roots were flagged as semantically split.")
    else:
        for s in flagged:
            with st.expander(f"`{s['root']}` is split — "
                             f"max JSD {s['max_jsd']:.2f}, "
                             f"stability {s['stability']:.2f}",
                             expanded=True):
                for cl_id, forms in s["clusters"].items():
                    st.markdown(f"**Cluster {cl_id}** -- " + ", ".join(forms))
                    partners = s["cluster_top_partners"].get(cl_id, [])
                    if partners:
                        col_tbl, col_pad = st.columns([1, 3])
                        with col_tbl:
                            st.dataframe(
                                pd.DataFrame(partners, columns=["partner", "shared verses"]),
                                hide_index=True, width=300,
                            )
