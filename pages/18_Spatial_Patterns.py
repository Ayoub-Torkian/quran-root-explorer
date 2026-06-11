"""Spatial Patterns — the Qur'an as a GIS point/area landscape.

Treats every root (or letter) occurrence as a 2-D point — x = position within the
ayah, y = global ayah index under a chosen *rearrangement* of the text — and runs
the classic point-pattern and areal (lattice) statistics of ecology / geography,
each judged against a Complete-Spatial-Randomness (CSR) null.

  TREE   = one concept (single root/letter): point pattern + area pattern.
  FOREST = the whole corpus: classify every root above a frequency floor.

Rearrangements ("بازآرایی") re-fold the text: muṣḥaf (surah→ayah), the ayah-major
TRANSPOSE (286 ayah-bands), or revelation order. Honest by construction: every
verdict is a CSR/permutation comparison, and a critique panel states plainly where
the paper's headline reproduces and where it does not.
"""
from __future__ import annotations

import json
import os

import numpy as np
import pandas as pd
import streamlit as st

import analysis as _A
import spatial_patterns as SP
import plotly_charts as PC
from state import (get_corpus, query_controls, hero, layer, log_page,
                   _add_root, _remove_root)

st.set_page_config(page_title="Spatial Patterns", page_icon="🗺️", layout="wide")
log_page("spatial_patterns")
corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
# Parse the queried roots directly — do NOT run the heavy compute_all pipeline,
# which hard-stops with "No valid roots parsed." on an empty query and would kick
# the user out of Forest/Archetypes (which need no root at all). Tree/Series guard
# the empty case gracefully below.
input_roots = _A.parse_input_roots(raw, normalize)

HAS_REV = getattr(corpus, "has_rev_order", False)
_FOREST_PATH = os.path.join(os.path.dirname(__file__), "..", "spatial_forest.json")


@st.cache_data(show_spinner=True)
def _coloc(_cid, roots, normalize, unit, n_perm):
    return SP.colocation_matrix(corpus, list(roots), normalize, unit=unit, n_perm=n_perm)


@st.cache_data(show_spinner=True)
def _multiview_emb(_cid, normalize, unit, min_freq):
    return SP.multiview_embeddings(corpus, normalize, unit=unit, min_freq=min_freq)


@st.cache_data(show_spinner=True)
def _coloc_field(_cid, normalize, unit, min_freq, feature="root"):
    return SP.colocation_field(corpus, normalize, unit=unit, min_freq=min_freq,
                               feature=feature)


@st.cache_data(show_spinner=True)
def _coloc_net(_cid, seeds, normalize, unit):
    return SP.colocation_network(corpus, list(seeds), normalize, unit=unit,
                                 top_per_seed=5, thr=0.5)


@st.cache_data(show_spinner=True)
def _control(_cid, normalize, order, unit, min_freq, n_seeds):
    return SP.control_comparison(corpus, normalize, order=order, unit=unit,
                                 min_freq=min_freq, n_seeds=n_seeds)


@st.cache_data(show_spinner=False)
def _forest(_cid):
    try:
        with open(_FOREST_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


@st.cache_data(show_spinner=True)
def _series(_cid, target, normalize, order, feature):
    return SP.concept_series_profile(corpus, target, normalize, order=order,
                                     feature=feature)


@st.cache_data(show_spinner=True)
def _archetypes(_cid, normalize, order, unit, min_freq, k, feature):
    return SP.archetype_analysis(corpus, normalize, order=order, unit=unit,
                                 min_freq=min_freq, k=k, feature=feature)


@st.cache_data(show_spinner=True)
def _kscan(_cid, normalize, order, unit, min_freq, feature):
    res = SP.archetype_analysis(corpus, normalize, order=order, unit=unit,
                                min_freq=min_freq, k=3, feature=feature)
    return SP.archetype_k_scan(res["Z"]) if res else []


@st.cache_data(show_spinner=True)
def _profile(_cid, target, normalize, order, unit, feature, position, n_mc):
    return SP.root_spatial_profile(corpus, target, normalize, order=order,
                                   unit=unit, feature=feature, position=position,
                                   n_mc=n_mc)


hero("🗺️ Two Books · Spatial Patterns",
     "The Qur'an as a point/area landscape — Ripley K, Clark-Evans R, Moran's I, "
     "LISA & Getis-Ord G*, each vs a random (CSR) null.")

st.markdown(
    "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;"
    "padding:9px 14px;margin:6px 0 12px;font-size:13.5px;color:#1D3557;'>"
    "Every occurrence is a point: <b>x = position inside the ayah</b>, "
    "<b>y = ayah index</b> in a chosen ordering. <b>Point</b> stats ask <i>how is a "
    "concept arranged?</i> (clustered / random / regular). <b>Area</b> stats ask "
    "<i>which regions are hot, cold, or autocorrelated?</i> A <b>rearrangement</b> "
    "re-folds the text (muṣḥaf · ayah-major transpose · revelation) so the same "
    "concept can be read as different geographies.</div>",
    unsafe_allow_html=True)

# ── SŪRA CONSTELLATION (Latent Feature L09/L10) — self-contained, reads viz_data.json ──
try:
    import json as _json
    _vzp = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "research", "intrinsic", "viz_data.json")
    _vz = _json.load(open(_vzp, encoding="utf-8"))
    _land = _vz.get("landscape", [])
    if _land:
        layer(1, "SŪRA CONSTELLATION — the 114 sūras as a landscape")
        st.caption("Each dot is a sūra placed by 100 intrinsic features; the main axis tracks the "
                   "canonical order (r = %.2f, Latent Feature L09); colour = unsupervised type — "
                   "short/dense vs long/rich (L10). Open the 🧬 Latent Feature Ledger for the full review."
                   % _vz.get("pc1_order_r", 0))
        import plotly.graph_objects as _go
        _cc = ["#E76F51", "#2A9D8F"]
        _fig = _go.Figure(_go.Scatter(
            x=[p[1] for p in _land], y=[p[2] for p in _land], mode="markers",
            marker=dict(size=[max(6, min(20, p[3] ** 0.5 + 4)) for p in _land],
                        color=[_cc[p[4]] if len(p) > 4 else "#457B9D" for p in _land],
                        line=dict(width=.5, color="#fff")),
            text=["sūra %d · %d verses · %s" % (p[0], p[3], ("short/dense" if (len(p) > 4 and p[4] == 0) else "long/rich")) for p in _land],
            hoverinfo="text"))
        _fig.update_layout(height=400, margin=dict(l=6, r=6, t=8, b=6), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="PC1 — size / richness (tracks canonical order)", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="PC2", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=11))
        st.plotly_chart(_fig, use_container_width=True, key="spatial_sura_constellation")
        try:
            st.page_link("pages/25_Latent_Features.py", label="See L09 · L10 in the Latent Feature Ledger", icon="🧬")
        except Exception:
            pass
except Exception:
    pass

# ───────────────────────── controls ─────────────────────────
c1, c2, c3, c4 = st.columns([1.3, 1.2, 1.2, 1.1])
with c1:
    scope = st.radio("Scope", ["🌳 Tree (one concept)", "🌲 Forest (whole corpus)",
                              "🧬 Archetypes (latent)", "📈 Spatial series",
                              "🔗 Co-location", "🧠 Connectome"], index=0)
with c2:
    order = st.selectbox("Rearrangement", SP.available_orders(corpus),
                         format_func=lambda o: SP.ORDER_LABELS.get(o, o))
with c3:
    unit = st.selectbox("Areal unit", SP.available_units(corpus),
                        format_func=lambda u: SP.UNIT_LABELS.get(u, u))
with c4:
    pos_choice = st.selectbox("Position-in-ayah filter",
                              ["Any", "First", "Last", "k-th"], index=0,
                              help="Restrict to a fixed slot, e.g. the FIRST "
                                   "root of every ayah.")
position = {"Any": None, "First": "first", "Last": "last"}.get(pos_choice, None)
if pos_choice == "k-th":
    position = int(st.number_input("k (1 = first)", min_value=1, max_value=60,
                                   value=1, step=1))

# The whole app is ROOT-input; surface forms are EXTRACTED from a root, never
# typed. feature defaults to 'root'; Tree offers an extracted surface drill-down,
# and Archetypes offers a corpus-wide population toggle (roots vs surface forms).
feature = "root"

# ═══════════════════════════ ARCHETYPES ═══════════════════════════
if scope.startswith("🧬"):
    a1, a2 = st.columns([1, 1])
    with a1:
        k = int(st.slider("Number of archetypes (k)", 2, 8, 3,
                          help="The k-scan below shows the data robustly supports "
                               "k≈3 (stability collapses past it)."))
    with a2:
        min_freq = int(st.slider("Min root frequency", 5, 50, 8, step=1))
    pop = st.radio("Population (corpus-wide — not a typed input)",
                   ["roots", "surface forms"], horizontal=True, index=0)
    afeat = "surface" if pop.startswith("surface") else "root"
    res = _archetypes(id(corpus), normalize, order, unit, min_freq, k, afeat)
    if not res:
        st.warning("Too few items for clustering at this floor.")
        st.stop()
    st.caption(f"Population: **{afeat}s** ({len(res['roots'])} above the floor).")
    layer(1, "LATENT ARCHETYPES — spatial behaviour, discovered unsupervised")
    g = st.columns(3)
    g[0].metric("Roots clustered", len(res["roots"]),
                f"{res['X'].shape[1]} features", delta_color="off",
                help="Each root is a 13-feature spatial vector (local: Fano, "
                     "gap-CV, peak share, lacunarity, ACF · global: coverage, "
                     "Moran, gravitational centre, spread) → standardised → PCA + k-means.")
    g[1].metric("PCA variance (2-D)",
                f"{(res['var'][0]+res['var'][1])*100:.0f}%", delta_color="off",
                help="Share of total variance captured by the two plotted axes.")
    g[2].metric("Mean stability", f"{res['mean_stability']:.2f}",
                "bootstrap consensus", delta_color="off",
                help="How often each root keeps its archetype under feature jitter "
                     "(20 refits). High = robust spatial fingerprint.")
    cc = st.columns([1.3, 1.0])
    with cc[0]:
        st.plotly_chart(PC.chart_archetype_embedding(res),
                        use_container_width=True)
    with cc[1]:
        st.plotly_chart(PC.chart_archetype_profiles(res),
                        use_container_width=True)
    kscan = _kscan(id(corpus), normalize, order, unit, min_freq, afeat)
    sc = st.columns([1.0, 1.0])
    with sc[0]:
        st.plotly_chart(PC.chart_k_scan(kscan), use_container_width=True)
    with sc[1]:
        import numpy as _np
        st_arr = _np.asarray(res["stability"]); rts = res["roots"]
        amb = [rts[i] for i in _np.argsort(st_arr)[:10]]
        st.markdown("**Stability read-out**")
        st.caption(
            "The k-scan shows how many archetypes survive resampling: stability "
            "stays high then collapses at the right k — pick the largest k still "
            "above ~0.9. Roots below pin to a robust archetype; the **ambiguous** "
            "ones below sit *between* archetypes (transitional spatial behaviour):")
        st.markdown(f"<div style='color:#3D4757;font-size:13.5px;'>"
                    f"{'  ·  '.join(amb)}</div>", unsafe_allow_html=True)
    if afeat == "root":
        sa = SP.semantic_alignment(corpus, res, n_perm=99)
        if sa:
            layer(2, "SEMANTIC VALIDATION — do spatial archetypes carry meaning?")
            q = st.columns(3)
            q[0].metric("Mantel r (spatial ↔ meaning)", sa["mantel_r"],
                        f"p={sa['p']}", delta_color="off",
                        help="Correlation between the spatial-feature distance and "
                             "an INDEPENDENT distributional-semantic distance "
                             "(co-occurrence / 'company a word keeps'). Permutation p.")
            q[1].metric("Within-archetype cohesion", f"{sa['cohesion_ratio']}×",
                        "vs between", delta_color="off",
                        help="Mean semantic similarity of same-archetype pairs ÷ "
                             "different-archetype pairs. >1 = archetypes are "
                             "semantically more alike than chance.")
            q[2].metric("Roots tested", sa["m"], delta_color="off")
            verdict = ("significant but weak" if sa["p"] <= 0.05 and sa["mantel_r"] < 0.3
                       else ("significant & moderate" if sa["p"] <= 0.05
                             else "not significant"))
            st.caption(
                f"Spatial archetype ↔ meaning is **{verdict}** (r={sa['mantel_r']}, "
                f"p={sa['p']}). Honest reading: how a concept is *distributed* is "
                f"**largely independent of what it means**, with a small shared "
                f"component — the spatial features are mostly a different, "
                f"complementary signal to lexical semantics, not a proxy for it.")
    st.markdown("**Archetypes found** (top members by frequency · cluster stability):")
    for a in res["archetypes"]:
        st.markdown(
            f"<div style='border-left:4px solid #1D3557;background:#EEF3FB;"
            f"border-radius:6px;padding:6px 12px;margin:4px 0;font-size:13.5px;'>"
            f"<b>{a['tag']}</b> · n={a['n']} · stability {a['stability']:.2f} · "
            f"<i>{a['desc']}</i><br>"
            f"<span style='color:#243447;'>{'  ·  '.join(a['examples'])}</span></div>",
            unsafe_allow_html=True)

    layer(2, "ROOT → CLUSTER ASSIGNMENT — which item is in which archetype")
    _tags = {a["cluster"]: a["tag"] for a in res["archetypes"]}
    _freq = corpus.freq_norm if normalize else corpus.freq_exact
    assign = pd.DataFrame({
        "Item": res["roots"],
        "Cluster k": res["labels"],
        "Archetype": [_tags.get(int(l), "?") for l in res["labels"]],
        "Freq": [int(_freq.get(r, 0)) for r in res["roots"]],
        "Stability": np.round(res["stability"], 2),
        "PC1": np.round(res["emb"][:, 0], 2),
        "PC2": np.round(res["emb"][:, 1], 2),
    })
    _fcol1, _fcol2 = st.columns([1, 3])
    with _fcol1:
        _pick = st.selectbox("Filter by archetype",
                             ["(all)"] + [a["tag"] for a in res["archetypes"]])
    _view = assign if _pick == "(all)" else assign[assign["Archetype"] == _pick]
    _view = _view.sort_values(["Cluster k", "Freq"], ascending=[True, False])
    st.dataframe(_view, hide_index=True, use_container_width=True, height=340)
    st.caption(f"{len(_view)} items · every queried/clustered item with its archetype "
               f"(cluster k), bootstrap stability, and PCA coordinates. Sort or filter "
               f"to see exactly which roots/forms fall in each cluster. Low-stability "
               f"rows sit ambiguously between clusters.")

# ═══════════════════════════ TREE ═══════════════════════════
elif scope.startswith("🌳"):
    if not input_roots:
        st.info("Type one or more roots in the 🔎 Query box in the sidebar (top-left) "
                "and press Enter — Spatial Patterns reads your query like every other page.")
        st.stop()
    tcol1, tcol2, tcol3 = st.columns([1.1, 1.6, 1.0])
    with tcol1:
        if len(input_roots) == 1:
            root_in = input_roots[0]
            st.caption("Root (from your query)")
            st.markdown(f"### {root_in}")
        else:
            root_in = st.selectbox("Root (from your query)", input_roots, index=0)
    feature = "root"; target = root_in
    with tcol2:
        _forms = _A.surface_form_table(corpus, [root_in], normalize)
        _forms = _forms[_forms["Input Root"] == root_in] if not _forms.empty else _forms
        opts = ["All occurrences (whole root)"]; fmap = {}
        if not _forms.empty:
            for _, rr in _forms.sort_values("Occurrences", ascending=False).head(30).iterrows():
                lbl = f"{rr['Surface Form (col 5)']}  ({int(rr['Occurrences'])})"
                opts.append(lbl); fmap[lbl] = rr["Surface Form (col 5)"]
        pick = st.selectbox(f"Surface form of «{root_in}» (extracted)", opts, index=0)
        if pick in fmap:
            feature = "surface"; target = fmap[pick]
    with tcol3:
        n_mc = st.slider("CSR sims", 19, 199, 99, step=20,
                         help="More = tighter envelope, slower.")

    prof = _profile(id(corpus), target, normalize, order, unit, feature,
                    position, n_mc)
    xy = prof["xy"]
    if len(xy) < 4:
        st.warning(f"Only {len(xy)} occurrences found for «{target}» under this "
                   f"filter — too few for a stable spatial verdict.")
        if len(xy) == 0:
            st.stop()

    ce = prof["clark_evans"]; kl = prof["ripley"]; mi = prof["moran"]
    ts = SP.two_scale_signature(xy, n_mc=max(19, n_mc // 3))
    cov = SP.coverage_index(corpus, target, normalize, unit=unit,
                            feature=feature, position=position)

    layer(1, "SUMMARY — hover each ? for what it means")
    m = st.columns(7)
    m[0].metric("Occurrences", f"{len(xy)}", f"{cov['occupied']}/{cov['total']} units",
                delta_color="off",
                help="Number of points (root or surface-form occurrences) under this filter, "
                     "and how many areal units they touch.")
    m[1].metric("Clark-Evans R", f"{ce['R']}", ce["klass"], delta_color="off",
                help="Nearest-neighbour ratio vs CSR: <1 clustered · ≈1 random · "
                     ">1 regular.")
    m[2].metric("Ripley K_Max", f"{kl['k_max'] if kl else '—'}", "multiscale",
                delta_color="off",
                help="Max deviation of L(r) from CSR across radii — overall "
                     "multiscale clustering strength.")
    m[3].metric("Local scale", ts["local"], f"score {ts['local_score']}",
                delta_color="off",
                help="Ripley verdict at SMALL radius (within-passage). "
                     "clustered = bursts of the concept.")
    m[4].metric("Global scale", ts["global_"], f"score {ts['global_score']}",
                delta_color="off",
                help="Ripley verdict at LARGE radius (whole text). The paper "
                     "claims 'regular' here; see the critique panel.")
    m[5].metric("Burstiness (Fano)", f"{prof['fano']}",
                "bursty" if prof["fano"] > 1 else "even", delta_color="off",
                help="Variance/mean of gaps between occurrences. >1 = bursty "
                     "(clumped), <1 = evenly spaced.")
    m[6].metric("Coverage", f"{cov['coverage']:.2f}", "unsaturation",
                delta_color="off",
                help="Fraction of areal units touched — global spread. High but "
                     "<1 = pervasive yet unsaturated.")
    m2 = st.columns(7)
    m2[0].metric("Moran's I", f"{mi['I']}", mi["klass"], delta_color="off",
                 help="Areal autocorrelation of per-unit counts: + clustered · "
                      "0 random · − regular. p=%s." % mi.get("p"))
    m2[1].metric("Mean NN dist", f"{ce['mnnd']}", f"CSR {ce['expected']}",
                 delta_color="off",
                 help="Observed mean nearest-neighbour distance vs the CSR "
                      "expectation that defines R.")

    t_point, t_area, t_map = st.tabs(["📍 Point pattern", "🗺️ Area pattern", "🌡️ Hotspot & growth"])
    with t_point:
        st.plotly_chart(PC.chart_point_pattern(xy, target,
                        SP.ORDER_LABELS.get(order, order), feature),
                        use_container_width=True)
        cc = st.columns(2)
        with cc[0]:
            st.plotly_chart(PC.chart_ripley_l(kl, target),
                            use_container_width=True)
        with cc[1]:
            gs = SP.gstar_window_1d(xy)
            st.plotly_chart(PC.chart_gstar_focal(gs, target),
                            use_container_width=True)
    with t_area:
        st.plotly_chart(PC.chart_areal_lattice(
            prof["areal_values"], prof["areal_labels"],
            SP.UNIT_LABELS.get(unit, unit).split(" (")[0],
            gstar=prof["gstar"], lisa=prof["lisa"], target=target),
            use_container_width=True)
        lq = prof["lisa"]["quad"]
        labs = prof["areal_labels"]; vals = prof["areal_values"]
        hot = [(int(labs[i]), int(vals[i]), lq[i])
               for i in range(len(labs)) if lq[i] in ("HH", "HL")]
        if hot:
            st.caption("**LISA / G\\* hot units** (significant high-value clusters):")
            st.dataframe(pd.DataFrame(hot, columns=["Unit", "Count", "LISA"]),
                         hide_index=True, use_container_width=True)
        else:
            st.caption("No significant LISA hot clusters at α=0.05 for this unit.")
    with t_map:
        _su, _ay = SP.occ_surah_ayah(corpus, target, normalize, feature, position)
        cc2 = st.columns(2)
        with cc2[0]:
            st.plotly_chart(PC.chart_density_surface(_su, _ay, target),
                            use_container_width=True)
        with cc2[1]:
            st.plotly_chart(PC.chart_cumulative_growth(
                xy, target, SP.ORDER_LABELS.get(order, order)),
                use_container_width=True)
        st.caption("Left: a 2-D **hotspot surface** over the muṣḥaf grid "
                   "(surah × ayah) — bright cells = where the concept piles up. "
                   "Right: cumulative **growth** along the ordering — steep = burst, "
                   "flat = silence.")

# ═══════════════════════════ FOREST ═══════════════════════════
elif scope.startswith("🌲"):
    fj = _forest(id(corpus))
    if not fj:
        st.error("Precomputed forest file `spatial_forest.json` not found. "
                 "Run `python precompute_spatial.py` in the app folder.")
        st.stop()
    scen_keys = list(fj["scenarios"].keys())
    def _flabel(k):
        sm = fj["scenarios"][k]["summary"]
        return (f"{sm.get('feature', 'root')}  ·  "
                f"{SP.ORDER_LABELS.get(sm['order'], sm['order'])}  ·  "
                f"{SP.UNIT_LABELS.get(sm['unit'], sm['unit'])}")
    pretty = {k: _flabel(k) for k in scen_keys}
    sk = st.selectbox("Rearrangement scenario", scen_keys,
                      format_func=lambda k: pretty[k])
    scen = fj["scenarios"][sk]
    summ = scen["summary"]; rows = scen["rows"]

    layer(1, "FOREST — corpus-wide headline")
    g = st.columns(4)
    g[0].metric("Roots classified", summ["n_roots"], f"freq ≥ {summ['min_freq']}",
                delta_color="off",
                help="Every root above the frequency floor, run through the full "
                     "point/area pipeline in this rearrangement scenario.")
    g[1].metric("Local clustered", f"{summ['local_clustered']:.0f}%",
                f"Fano > {summ['fano_threshold']}", delta_color="off",
                help="Share of roots whose occurrence gaps are bursty (Fano factor above "
                     "the threshold) — local clumping rather than even spacing.")
    g[2].metric("Mean coverage", f"{summ['mean_coverage']:.2f}",
                f"{summ['saturated_pct']:.0f}% saturate all units", delta_color="off",
                help="Average fraction of areal units a root touches. Well below 1 with 0% "
                     "saturation = pervasive-but-unsaturated spread.")
    g[3].metric("Areal Moran", f"clus {summ['I_clustered']:.0f}%",
                f"reg {summ['I_regular']:.0f}% · rand {summ['I_random']:.0f}%",
                delta_color="off",
                help="How per-unit counts autocorrelate across the lattice: % of roots "
                     "reading clustered / regular / random under Moran's I.")
    cc = st.columns([1.2, 1.4])
    with cc[0]:
        st.plotly_chart(PC.chart_forest_summary_bars(summ),
                        use_container_width=True)
    with cc[1]:
        st.plotly_chart(PC.chart_forest_fingerprint(rows, pretty[sk]),
                        use_container_width=True)
    try:
        st.markdown(
            f"**📍 What to take from these charts:** of {summ['n_roots']} roots, "
            f"{summ['local_clustered']:.0f}% are locally bursty yet mean coverage is only "
            f"{summ['mean_coverage']:.2f} with {summ['saturated_pct']:.0f}% saturating all "
            f"units — bursts spread thin rather than piling up. At the areal scale "
            f"{summ['I_clustered']:.0f}% read clustered vs {summ['I_regular']:.0f}% "
            f"regular; see the scramble control below before treating either as more than "
            f"a frequency artifact."
        )
    except Exception:
        pass

    with st.expander("🔬 All roots — sortable table", expanded=False):
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True,
                     height=320)

    with st.expander("🧪 Control — is this beyond chance? (vs scrambled scripture)",
                     expanded=False):
        st.caption("Re-run the headline on the REAL text vs 3 frequency-matched "
                   "scrambles (same root counts, same ayah lengths, roots reshuffled "
                   "across the text). A metric that MATCHES the scramble is a frequency "
                   "artifact; one that DIFFERS beyond the error bars is real structure. "
                   "(Root-based control.)")
        _co = summ.get("order", "mushaf")
        _cu = summ.get("unit", "surah") if summ.get("feature") == "root" else "surah"
        cc = _control(id(corpus), normalize, _co, _cu, int(summ.get("min_freq", 8)), 3)
        st.plotly_chart(PC.chart_control_comparison(cc), use_container_width=True)
        _lab = {"local_clustered": "Local clustered %", "mean_coverage": "Mean coverage",
                "I_clustered": "Moran clustered %", "I_regular": "Moran regular %",
                "I_random": "Moran random %"}
        trows = [{"Metric": _lab[k], "Real": v["real"], "Scramble μ": v["null_mean"],
                  "±σ": v["null_sd"], "z": v["z"],
                  "Verdict": "beyond chance" if v["beyond_chance"] else "frequency artifact"}
                 for k, v in cc["verdict"].items()]
        st.dataframe(pd.DataFrame(trows), hide_index=True, use_container_width=True)
        st.caption("Typical honest reading: **local clustering is a frequency artifact** "
                   "(the scramble clusters just as much), but the real text's **areal "
                   "distribution is significantly MORE even than chance** (fewer "
                   "Moran-clustered roots than the scramble) — real support for a "
                   "*global-uniformity* reading. A human-TEXT comparison still needs an "
                   "external root-annotated corpus; this scramble is the within-reach null.")

# ═══════════════════════════ SPATIAL SERIES ═══════════════════════════
elif scope.startswith("📈"):
    st.caption("Treat a concept's per-bin density as a 1-D **series indexed by "
               "position** (not time) under the chosen rearrangement — then the "
               "time-series toolkit applies: autocorrelation (memory), periodogram "
               "(recurrence wavelength), cross-correlation (which concept leads).")
    if not input_roots:
        st.info("Type roots in the 🔎 Query box in the sidebar — Series needs at least one.")
        st.stop()
    cs = st.columns(2)
    with cs[0]:
        ta = st.selectbox("Concept A (from your query)", input_roots, index=0)
    with cs[1]:
        _bopts = ["(none)"] + [r for r in input_roots if r != ta]
        tb_sel = st.selectbox("Concept B (optional, cross-correlation)", _bopts,
                              index=1 if len(_bopts) > 1 else 0)
        tb = "" if tb_sel == "(none)" else tb_sel
    feature = "root"
    spa = _series(id(corpus), ta, normalize, order, feature)
    if not spa:
        st.warning(f"No occurrences for «{ta}».")
        st.stop()
    ol = SP.ORDER_LABELS.get(order, order)
    layer(1, "SERIES SUMMARY — hover each ? for meaning")
    mm = st.columns(5)
    mm[0].metric("Dominant period", f"{spa['dom_period']:.0f} bins",
                 f"{spa['dom_frac']*100:.0f}% of power", delta_color="off",
                 help="Strongest recurrence wavelength from the FFT. Near the full "
                      "length = a broad trend, not true periodicity.")
    mm[1].metric("ACF lag-1", f"{spa['acf'][1]:.2f}" if len(spa['acf'])>1 else "—",
                 "memory", delta_color="off",
                 help="Short-range autocorrelation: high = a dense stretch tends to "
                      "be followed by another (persistence).")
    mm[2].metric("Lacunarity", f"{spa['lacunarity']:.2f}", "gappiness",
                 delta_color="off",
                 help="Gliding-box texture Λ=1+Var/Mean². High = clumpy/holey "
                      "(bursts + silences); ~1 = even.")
    mm[3].metric("Fractal D", f"{spa['fractal']['D']}", f"R²={spa['fractal']['r2']}",
                 delta_color="off",
                 help="Correlation dimension from log-log Ripley K. EXPLORATORY: "
                      "the corpus is too short to claim fractality; a near-perfect R² "
                      "mostly reflects the ~1-D window, not self-similarity.")
    mm[4].metric("Occurrences", f"{len(spa['xy'])}", delta_color="off",
                 help="Points in the series for concept A.")
    st.plotly_chart(PC.chart_density_series(spa, ol), use_container_width=True)
    cc = st.columns(2)
    with cc[0]:
        st.plotly_chart(PC.chart_acf(spa), use_container_width=True)
    with cc[1]:
        st.plotly_chart(PC.chart_periodogram(spa), use_container_width=True)
    if tb:
        spb = _series(id(corpus), tb, normalize, order, feature)
        if spb:
            lags, xc = SP.cross_correlation(spa["series"], spb["series"], max_lag=40)
            _n = len(spa["series"])
            st.plotly_chart(PC.chart_cross_correlation(lags, xc, ta, tb, n=_n),
                            use_container_width=True)
            import numpy as _np
            conf = 1.96 / _np.sqrt(max(_n, 2))
            peak = int(lags[int(_np.abs(xc).argmax())])
            if _np.abs(xc).max() > conf and peak != 0:
                lead = ta if peak > 0 else tb
                st.caption(f"Peak lag **{peak:+d} bins** clears the 95% band → "
                           f"**{lead}** tends to lead. A genuine latent sequencing signal.")
            else:
                st.caption("No lag clears the 95% noise band → **no robust lead-lag**; "
                           "the two concepts are roughly co-located. Honest null result.")
        else:
            st.warning(f"No occurrences for «{tb}».")

# ═══════════════════════════ CO-LOCATION ═══════════════════════════
elif scope.startswith("🔗"):
    if len(input_roots) < 1:
        st.info("Add one or more roots in the 🔎 Query box (sidebar) to map co-location.")
        st.stop()
    layer(1, "CO-LOCATION — semantic geography (share vs avoid territory)")
    st.caption("Do concepts SHARE the same surahs/bands (red) or AVOID each other (blue)? "
               "Correlation of per-unit count vectors vs a label-permutation null — the "
               "orthogonal latent dimension: relationships, not per-concept magnitudes.")
    if len(input_roots) >= 2:
        res = _coloc(id(corpus), tuple(input_roots), normalize, unit, 199)
        if res:
            aff = res["affinity"]
            off = aff[~np.eye(len(res["roots"]), dtype=bool)]
            npair = len(res["roots"]) * (len(res["roots"]) - 1) // 2
            shares = [x for x in res["sig"] if x[4] == "share"]
            avoids = [x for x in res["sig"] if x[4] == "avoid"]
            g = st.columns(4)
            g[0].metric("Concepts · pairs", f"{len(res['roots'])} · {npair}",
                        delta_color="off", help="Your queried roots and the number of pairs.")
            g[1].metric("Significant pairs", f"{len(res['sig'])}",
                        f"{round(100*len(res['sig'])/max(npair,1))}% · mean|aff| {np.nanmean(np.abs(off)):.2f}",
                        delta_color="off", help="Pairs whose co-location beats the permutation null (p≤0.05).")
            g[2].metric("Strongest share", f"{shares[0][2]}" if shares else "—",
                        f"{shares[0][0]} ↔ {shares[0][1]}" if shares else "none",
                        delta_color="off", help="Most territory-sharing pair.")
            g[3].metric("Strongest avoid", f"{avoids[0][2]}" if avoids else "—",
                        f"{avoids[0][0]} ↔ {avoids[0][1]}" if avoids else "none found",
                        delta_color="off", help="Most mutually-avoiding pair.")
            if len(res["roots"]) >= 3:
                st.plotly_chart(PC.chart_colocation_heatmap(res), use_container_width=True)
            if res["sig"]:
                st.markdown("**Significant pairs** (p ≤ 0.05, strongest first):")
                st.dataframe(pd.DataFrame(res["sig"],
                             columns=["A", "B", "Affinity", "p", "Relation"]),
                             hide_index=True, use_container_width=True)
    layer(2, "DEEP DIVE — corpus-wide co-locators per concept (one tab each)")
    gran = st.radio("Granularity", ["root", "surface forms"], horizontal=True,
                    help="Surface forms disaggregate a root's blurred geography into "
                         "FORM-specific co-locators (validated: عليم↔divine names vs "
                         "علم↔guidance) — same statistical power, finer meaning.")
    st.caption("Each tab = one queried concept · ✶ = significant (p≤0.05).")
    field = _coloc_field(id(corpus), normalize, unit, 8)
    _dd = input_roots[:6]
    for _tab, _pick in zip(st.tabs(_dd), _dd):
        with _tab:
            if gran == "surface forms":
                sfield = _coloc_field(id(corpus), normalize, unit, 8, "surface")
                _ft = _A.surface_form_table(corpus, [_pick], normalize)
                _ft = _ft[_ft["Input Root"] == _pick] if not _ft.empty else _ft
                _forms = [fm for fm in _ft.sort_values("Occurrences", ascending=False)
                          ["Surface Form (col 5)"].tolist()
                          if _A.normalize_letters(fm) in sfield["index"]][:6]
                if not _forms:
                    st.caption(f"No surface forms of «{_pick}» above the frequency floor.")
                else:
                    rows = []
                    for _fm in _forms:
                        co = SP.colocation_neighbors(corpus, _fm, normalize, unit=unit,
                                                     top=6, feature="surface", field=sfield)
                        rows.append({"Surface form": _fm,
                                     "Shares territory with":
                                     " · ".join(x[0] for x in co["share"][:6])})
                    st.dataframe(pd.DataFrame(rows), hide_index=True,
                                 use_container_width=True)
                    st.caption(f"Each surface form of «{_pick}» has a DISTINCT co-locator "
                               f"profile — the root view averages these together.")
            else:
                nbr = SP.colocation_neighbors(corpus, _pick, normalize, unit=unit,
                                              top=15, field=field)
                cN = st.columns([1.25, 1.0])
                with cN[0]:
                    st.plotly_chart(PC.chart_colocation_neighbors(nbr),
                                    use_container_width=True)
                with cN[1]:
                    st.markdown(f"**«{_pick}» shares with** (✶ p≤0.05):")
                    st.dataframe(pd.DataFrame(nbr["share"], columns=["Root", "Affinity", "p"]),
                                 hide_index=True, use_container_width=True, height=240)
                    st.markdown(f"**«{_pick}» avoids:**")
                    st.dataframe(pd.DataFrame(nbr["avoid"], columns=["Root", "Affinity", "p"]),
                                 hide_index=True, use_container_width=True, height=150)
                _cands = [r for r, a, p in nbr["share"] if r not in input_roots][:8]
                if _cands:
                    st.caption("➕ Add a co-locator as a new seed:")
                    bcols = st.columns(len(_cands))
                    for _bc, _r in zip(bcols, _cands):
                        _bc.button(f"➕ {_r}", key=f"add_{_pick}_{_r}",
                                   on_click=_add_root, args=(_r,))
    if len(input_roots) > 6:
        st.caption(f"(Co-locator tabs shown for the first 6 of {len(input_roots)} roots.)")

    layer(3, "EXPAND — launchpad, not endpoint")
    st.caption("➖ Remove a seed to refocus the map:")
    rcols = st.columns(min(len(input_roots), 8))
    for _i, _r in enumerate(input_roots):
        rcols[_i % len(rcols)].button(f"➖ {_r}", key=f"delcoloc_{_r}",
                                      on_click=_remove_root, args=(_r,))
    net = _coloc_net(id(corpus), tuple(input_roots), normalize, unit)
    if net and net.get("edges"):
        with st.expander("🔬 Co-location network — seeds → corpus co-locators "
                         "(collapse to save space)", expanded=True):
            st.plotly_chart(PC.chart_colocation_network(net), use_container_width=True)

# ═══════════════════════════ CONNECTOME ═══════════════════════════
elif scope.startswith("🧠"):
    if not input_roots:
        st.info("Add root(s) in the 🔎 Query box to view the connectome.")
        st.stop()
    layer(1, "CONNECTOME — one concept through 3 orthogonal views")
    st.caption("**Semantic** (what it MEANS · co-occurrence) ∥ **Spatial** (HOW it's "
               "deployed) ∥ **Co-location** (WHERE it lives). The three views barely "
               "overlap (Jaccard ≈0.03 — orthogonal). A bond in **≥2 views = robust "
               "(consensus)**; a **semantic-only** bond = same meaning, different "
               "deployment. (Tested: blending the views into one distance *dilutes* "
               "meaning 0.36→0.22, so they are kept separate.)")
    emb = _multiview_emb(id(corpus), normalize, unit, 8)
    for _tab, _pick in zip(st.tabs(input_roots[:6]), input_roots[:6]):
        with _tab:
            res = SP.concept_multiview_neighbors(corpus, _pick, normalize, k=10, emb=emb)
            if not res:
                st.caption(f"«{_pick}» is below the connectome floor (freq < 8).")
                continue
            cc = st.columns(3)
            _icon = {"semantic": "🧩 Semantic", "spatial": "🗺️ Spatial",
                     "co-location": "🔗 Co-location"}
            for _col, (_vn, _vs) in zip(cc, res["views"].items()):
                with _col:
                    st.markdown(f"**{_icon.get(_vn, _vn)}**")
                    st.markdown("　".join(_vs))
            if res["consensus"]:
                st.markdown("**🔗 Consensus bonds** (≥2 views — robust):")
                st.markdown("　".join(f"**{r}** _({'+'.join(w)})_"
                                      for r, w in res["consensus"]))
                _cz = [r for r, w in res["consensus"] if r not in input_roots][:8]
                if _cz:
                    bcols = st.columns(len(_cz))
                    for _bc, _r in zip(bcols, _cz):
                        _bc.button(f"➕ {_r}", key=f"cx_{_pick}_{_r}",
                                   on_click=_add_root, args=(_r,))
            if res["sem_only"]:
                st.caption("Pure-meaning (semantic-only — the axis spatial/territory miss): "
                           + " · ".join(res["sem_only"][:8]))

# ═══════════════════════════ CRITIQUE PANEL (always) ═══════════════════════════
layer(9, "Critical reading — does the paper's claim hold?")
st.markdown(
    "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;"
    "padding:11px 15px;font-size:13.5px;color:#243447;line-height:1.5;'>"
    "<b>What reproduces:</b> <b>local clustering</b> is robust — essentially every "
    "abundant root is bursty (Fano≫1) and its Ripley L sits above the CSR envelope at "
    "short range. This matches the paper's “locally clustered ~90%.”<br>"
    "<b>What does NOT reproduce:</b> the headline “<b>globally regular ~95%</b>.” Under a "
    "transparent CSR/areal-Moran test, frequent roots are clustered at <i>all</i> scales "
    "and <b>0%</b> read as areal-<i>regular</i>. The defensible global property is "
    "<b>unsaturated coverage</b> — no root saturates the text (mean coverage ≈0.13–0.21; "
    "0% saturate all units) while bursting locally.<br>"
    "<b>Caveats before any uniqueness claim:</b> (1) verdicts are method/scale-dependent; "
    "(2) regularity stats are frequency-confounded — rare roots look “regular” for lack of "
    "power; (3) the paper's cross-text comparison table is footnoted as taken from ChatGPT "
    "and unverified — “unique vs other texts” requires running this identical pipeline on "
    "those corpora; (4) no multiple-comparison (FDR) control; (5) results shift with "
    "tokenisation choices. <b>Fractals</b>: testable here (log-log K) but the corpus is far "
    "too short (&lt;3 decades) to support a fractal-dimension claim — exploratory only. "
    "<b>Origami</b>: a useful metaphor for the rearrangement/transpose folds, not a statistic."
    "</div>", unsafe_allow_html=True)
