"""Per-Root Profile — drill into a single input root, or the COMBINED view.

The COMBINED view has 3 sub-modes (chosen via radio):
  1. Co-present in surah (default) — how many input roots appear in each surah.
  2. At least k of N — slider for ayah-level intersection strictness (k=2…N).
  3. Overlay across surahs — semi-transparent overlay of each root's surah
     distribution, falling back to small-multiples when N >= 5.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import plotly_charts as PC
import analysis as _A
from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, highlight_text, log_page)

st.set_page_config(page_title="Per-Root Profile", page_icon="🔍", layout="wide")
log_page("per_root")

corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

# ── Surface-form divergence banner ──
# (placed AFTER corpus/R exist — previously this block ran before they were
#  defined, so the NameError was silently swallowed and the banner never showed)
try:
    import surface_divergence as _SD
    _sd_cache = _SD.compute(corpus)
    _split_roots = [r for r in R.get("input_roots", []) if _SD.is_split(_sd_cache, r)]
    if _split_roots:
        _sd_names = ", ".join(f"`{r}`" for r in _split_roots)
        st.warning(
            f"🔬 **Surface-form divergence detected for {_sd_names}.** "
            f"This root's surface forms split into statistically distinct "
            f"partner profiles. See **🔬 Surface Divergence** page for the breakdown."
        )
except Exception:
    pass

hero("🔍 Per-Root Profile",
     "Click any root for its dedicated breakdown — or pick 🔗 ALL TOGETHER for a "
     "combined view across input roots.")

if not R["input_roots"]:
    st.warning("No roots selected.")
    st.stop()

ALL_KEY = "__ALL_TOGETHER__"
n_inputs = len(R["input_roots"])

# Big prominent root-picker
st.markdown(
    """
    <div style='background:#EEF3FB;
                border-left:5px solid #1D3557; border-radius:14px;
                padding:12px 16px; margin-bottom:10px;
                box-shadow:0 1px 4px rgba(0,0,0,0.06);'>
      <div style='font-size:17px; font-weight:700; color:#1D3557;
                  margin-bottom:6px; letter-spacing:0.5px;'>
        👇 PICK A VIEW: INDIVIDUAL ROOT  OR  🔗 ALL TOGETHER
      </div>
      <div style='font-size:13.5px; color:#243447; line-height:1.5;'>
        Each input root has its own dedicated view.  Pick
        <b style='background:#1D3557;color:#fff;padding:1px 8px;border-radius:5px;'>🔗 ALL TOGETHER</b>
        for the combined view — three sub-modes inside (default is surah-level
        co-presence, which is the most informative because ayah-level intersection
        is often empty).
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

valid = list(R["input_roots"]) + ([ALL_KEY] if n_inputs >= 2 else [])
if st.session_state.get("profile_root") not in valid:
    st.session_state.profile_root = R["input_roots"][0]

button_labels = list(R["input_roots"])
if n_inputs >= 2:
    button_labels.append(ALL_KEY)
cols = st.columns(min(len(button_labels), 6))
for i, r in enumerate(button_labels):
    is_active = (r == st.session_state.profile_root)
    if r == ALL_KEY:
        text = "🔗 ALL TOGETHER"
        if is_active:
            text = "✓  🔗 ALL TOGETHER"
    else:
        text = f"✓  {r}" if is_active else r
    btn_type = "primary" if is_active else "secondary"
    if cols[i % len(cols)].button(text, key=f"prr_{r}",
                                   width='stretch',
                                   type=btn_type):
        st.session_state.profile_root = r
        st.rerun()

root = st.session_state.profile_root
combined_mode = (root == ALL_KEY)

if combined_mode:
    st.markdown(
        "<div style='font-size:14px; color:#10243A; margin-bottom:8px;'>"
        "Currently viewing: "
        f"<b style='color:#1D3557; font-size:18px;'>🔗 ALL TOGETHER  ·  {' + '.join(R['input_roots'])}</b>"
        "</div>",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f"<div style='font-size:14px; color:#10243A; margin-bottom:8px;'>"
        f"Currently viewing: <b style='color:#1D3557; font-size:18px;'>{root}</b> "
        f"&nbsp;·&nbsp; click any other button above to switch."
        f"</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────
# SINGLE-ROOT MODE (unchanged from before)
# ─────────────────────────────────────────────────────────────────
if not combined_mode:
    sub = R["occurrences"][R["occurrences"]["Input Root"] == root]
    sforms = R["sforms"][R["sforms"]["Input Root"] == root]
    rarity_row = R["rarity"][R["rarity"]["Input Root"] == root]
    flast = R["first_last"][R["first_last"]["Input Root"] == root]

    layer(1, "Headline metrics")
    _ay   = sub[["Surah #", "Ayah #"]].drop_duplicates().shape[0] if not sub.empty else 0
    _su   = sub["Surah #"].nunique() if not sub.empty else 0
    _tot  = int(sub["Hit Count"].sum()) if not sub.empty else 0          # total occurrences (term-frequency)
    _N    = corpus.n_ayahs
    _TOK  = sum(len(t) for t in corpus.root_tokens)                      # total root-tokens in the corpus
    _r_ay = round(1000 * _ay / _N, 1) if _N else 0
    _r_rt = round(1000 * _tot / _TOK, 2) if _TOK else 0
    _mean = round(_ay / _su, 1) if _su else 0
    _pct  = f"{rarity_row['Percentile'].iloc[0]}%" if not rarity_row.empty else "—"
    _tier = rarity_row["Tier"].iloc[0] if not rarity_row.empty else "—"
    _first = f"{flast['First (S:A)'].iloc[0]}" if not flast.empty else "—"
    _last  = f"{flast['Last (S:A)'].iloc[0]}" if not flast.empty else "—"

    r1 = st.columns(6)
    r1[0].metric("Ayahs", _ay, help="Ayahs containing the root (document frequency — once per ayah).")
    r1[1].metric("Total freq", _tot, help="Total occurrences incl. repeats within an ayah (term-frequency).")
    r1[2].metric("Surahs", _su, help="Distinct surahs the root appears in.")
    r1[3].metric("Surface forms", len(sforms), help="Distinct spellings that reduce to this one root.")
    r1[4].metric("Percentile", _pct, help="How frequent this root is vs all roots.")
    r1[5].metric("Tier", _tier, help="Frequency band derived from the percentile rank among all roots in this corpus.")

    r2 = st.columns(6)
    r2[0].metric("Rate /1k ayahs", _r_ay, help="ayah-freq / 6,236 * 1000 — share of verses.")
    r2[1].metric("Rate /1k roots", _r_rt, help="total-freq / total root-tokens * 1000 — size-true.")
    r2[2].metric("Breadth", f"{_su}/114", help="Surahs touched, out of 114.")
    r2[3].metric("Mean/surah", _mean, help="Average ayah-hits per surah it appears in.")
    r2[4].metric("First (S:A)", _first, help="First occurrence in mushaf order.")
    r2[5].metric("Last (S:A)", _last, help="Last occurrence in mushaf order.")
    if not flast.empty:
        st.caption(
            f"First: **{flast['First (S:A)'].iloc[0]}** ({flast['First Surah Name'].iloc[0]}) · "
            f"Last: **{flast['Last (S:A)'].iloc[0]}** ({flast['Last Surah Name'].iloc[0]})"
        )

    # Row 3 — concentration & extra summary metrics
    _aps = corpus.df.groupby(_A.COL_SURAH).size().to_dict()
    _names = corpus.df.drop_duplicates(_A.COL_SURAH).set_index(_A.COL_SURAH)[_A.COL_SURAH_NAME].to_dict()
    _conc = _A.root_concentration(corpus, root, normalize)
    _rep = round(_tot / _ay, 2) if _ay else 0
    _dens = []
    for _sid, _h in sub.groupby("Surah #").size().items():
        _sz = int(_aps.get(int(_sid), 0))
        if _h >= 3 and _sz >= 10:
            _dens.append((int(_sid), round(1000 * _h / _sz, 1)))
    _dsurah, _ddens = (max(_dens, key=lambda x: x[1]) if _dens else (None, 0))
    _npart = int((R["pmotifs"]["Input Root"] == root).sum())
    r3 = st.columns(6)
    r3[0].metric("Gini", _conc["gini"], help="Concentration across surahs: 0 = even, 1 = piled in one surah.")
    r3[1].metric("Top-3 share", f"{_conc['top3_share']}%", help="% of ayah-hits in its 3 busiest surahs.")
    r3[2].metric("Repetition", _rep, help="term-freq / ayah-freq — average repeats within an ayah.")
    r3[3].metric("Densest surah", f"S{_dsurah}" if _dsurah else "—", help="Size-normalized home (floor: >=3 hits, >=10 ayahs).")
    r3[4].metric("Home /1k", _ddens, help="Density of the densest surah, per 1,000 ayahs.")
    r3[5].metric("Partners", _npart, help="Distinct co-occurring root partners found.")

    st.divider()
    layer(2, "Distribution & forms — primary charts")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(PC.chart_per_root_surah_strip(R["occurrences"], root), width='stretch')
        st.plotly_chart(PC.chart_position_histogram(R["position"], root), width='stretch')
    with c2:
        st.plotly_chart(PC.chart_surface_form_sunburst(R["sforms"], root), width='stretch')
        st.plotly_chart(PC.chart_ayah_length_hist(R["position"], root), width='stretch')

    st.plotly_chart(PC.chart_density_home_surahs(R["occurrences"], _aps, _names, root), width='stretch')
    st.caption("**Density home** is size-true: hits per 1,000 ayahs of each surah. Unlike the raw "
               "'ayah hits per surah' above (which favours long surahs), this shows where the root is "
               "genuinely concentrated. **All surahs are shown** — green bars clear the support floor "
               "(>=3 hits and >=10 ayahs); **grey bars fall below it**. A grey bar can top the chart "
               "(e.g. a single hit in a 3-ayah surah = 333/1k) but its tiny denominator makes the "
               "density **not statistically reliable** — read it as a notable usage, not a ranking. "
               "The 'Densest surah' metric above still reports only the floor-qualified home.")
    try:
        _hits_by_surah = sub.groupby("Surah #").size().sort_values(ascending=False)
        if not _hits_by_surah.empty:
            _top_sid = int(_hits_by_surah.index[0])
            _top_hits = int(_hits_by_surah.iloc[0])
            _top_share = round(100 * _top_hits / max(_ay, 1), 1)
            _home_txt = (f"S{_dsurah} at {_ddens}/1k ayahs" if _dsurah
                         else "below the support floor (no surah qualifies)")
            st.markdown(
                f"**📍 What to take from these charts:** `{root}` touches {_ay} ayahs across "
                f"{_su}/114 surahs. Its busiest surah by raw count is **S{_top_sid} "
                f"({_names.get(_top_sid, '')})** with {_top_hits} ayah-hits "
                f"({_top_share}% of all its hits), while the size-true density home is "
                f"**{_home_txt}**. Concentration Gini = {_conc['gini']} "
                f"(0 = spread evenly, 1 = piled in one surah)."
            )
    except Exception:
        pass

    st.divider()
    layer(3, "Partners & morphology — drill-down tables")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Top co-occurring partners")
        st.plotly_chart(PC.chart_partner_motifs(R["pmotifs"], root, top=15), width='stretch')
        pm_sub = R["pmotifs"][R["pmotifs"]["Input Root"] == root]
        st.dataframe(pm_sub, width='content', hide_index=True, height=300)
    with c2:
        st.subheader("Attached particles (col 6 morphology)")
        st.plotly_chart(PC.chart_morphology_per_root(R["morphology"], root), width='stretch')
        morph_sub = R["morphology"][R["morphology"]["Input Root"] == root]
        st.dataframe(morph_sub, width='content', hide_index=True, height=300)

    st.subheader("Top co-occurring SURFACE FORMS (by lift)")
    _spl = _A.surface_partner_lift(corpus, [root], normalize, top=15, min_co=4)
    st.plotly_chart(PC.chart_surface_partner_lift(_spl, root, top=15), width='stretch')
    st.caption("Surface-form collocates ranked by **lift** (co-occurrence vs. chance) — the root's own "
               "forms excluded, support floor >=4 shared ayahs. High lift = a word-form that travels with "
               "this root far more than its overall frequency predicts. Complements the root-partner view "
               "(themes) with a phraseological one (exact word-forms).")
    if not _spl.empty:
        st.dataframe(_spl[_spl["Input Root"] == root][
            ["Partner Surface", "Ayahs Together", "Global Ayahs", "Lift", "Affinity"]],
            width='content', hide_index=True, height=300)

    st.divider()
    layer(4, "Surface forms — every spelling found")
    sf = sforms.copy()
    if sf.empty:
        st.caption("No surface forms.")
    else:
        sf["%"] = (100 * sf["Occurrences"] / sf["Occurrences"].sum()).round(1)
        cols_to_show = ["Surface Form (col 5)", "Occurrences", "%"]
        text_col = None
        if "Example Diacritized (col 7)" in sf.columns:
            text_col = "Example Diacritized (col 7)"; cols_to_show.append(text_col)
        elif "Example Segmented (col 6)" in sf.columns:
            text_col = "Example Segmented (col 6)"; cols_to_show.append(text_col)
        col_cfg = {
            "Surface Form (col 5)": st.column_config.TextColumn("Surface", width="small"),
            "Occurrences": st.column_config.NumberColumn("Count", width="small"),
            "%": st.column_config.NumberColumn("%", width="small"),
        }
        if text_col:
            col_cfg[text_col] = st.column_config.TextColumn(
                "Example ayah (with diacritics)" if "Diacritized" in text_col else "Example ayah",
                width="large")
        st.dataframe(sf[cols_to_show], width='content', hide_index=True,
                     height=320, column_config=col_cfg)

    st.divider()
    layer(4, "Every ayah containing this root")
    st.caption(f"{len(sub)} rows — laid out in 2 columns to minimize scrolling.")
    st.markdown("""
<style>
.ayah-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;}
.ayah-row{border:1px solid #E2E8F1;border-radius:8px;padding:6px 10px;background:#FFFFFF;}
.ayah-row:hover{background:#EEF3FB;}
.ayah-row .ar{direction:rtl;text-align:right;font-family:'Amiri','Amiri Quran','Noto Naskh Arabic',serif;font-size:18px;line-height:1.5;color:#243447;margin:0;}
.ayah-row .meta{font-size:12px;color:#10243A;margin:0;line-height:1.2;}
</style>
""", unsafe_allow_html=True)
    has_dia = R.get("has_diacritized")
    rows_html = []
    for _, row in sub.iterrows():
        if has_dia and row.get("Quranic Text (diacritized)"):
            ar = row["Quranic Text (diacritized)"]
        else:
            ar = row["Segmented Ayah"]
        meta = f"S{row['Surah #']}·A{row['Ayah #']} · {row['Surah Name']} · {row['Surface Form(s)']}"
        rows_html.append(f"<div class='ayah-row'><div class='ar'>{ar}</div><div class='meta'>{meta}</div></div>")
    st.markdown(f"<div class='ayah-grid'>{''.join(rows_html)}</div>", unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────────────────────────
# COMBINED MODE — 3 sub-modes
# ─────────────────────────────────────────────────────────────────
occ = R["occurrences"]
ayah_keys = occ[["Surah #", "Ayah #"]].drop_duplicates()

# Map: ayah → set of input roots present
ayah_roots = (occ.groupby(["Surah #", "Ayah #"])["Input Root"]
                 .apply(set).reset_index().rename(columns={"Input Root": "RootsHere"}))
ayah_roots["NumInputs"] = ayah_roots["RootsHere"].apply(len)

# Map: surah → set of input roots present anywhere in that surah
surah_to_roots = (occ.groupby("Surah #")["Input Root"]
                     .apply(set).reset_index().rename(columns={"Input Root": "RootsInSurah"}))
surah_to_roots["NumInputsInSurah"] = surah_to_roots["RootsInSurah"].apply(len)
# Also compute total ayah hits per surah, broken down by input root
surah_root_hits = (occ.groupby(["Surah #", "Input Root"])
                      .size().reset_index(name="Hits"))

CAT_PAL = px.colors.qualitative.Vivid


def _render_co_present_in_surah():
    layer(1, "Co-present in surah — where ALL inputs share territory")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Surahs with ≥1 input", int((surah_to_roots["NumInputsInSurah"] >= 1).sum()),
              help="Surahs where at least one of your input roots appears somewhere.")
    c2.metric("Surahs with ≥2 inputs", int((surah_to_roots["NumInputsInSurah"] >= 2).sum()),
              help="Surahs where two or more input roots share territory — the loosest co-presence.")
    c3.metric("Surahs with ALL inputs",
              int((surah_to_roots["NumInputsInSurah"] >= n_inputs).sum()),
              help=f"Surahs containing every one of your {n_inputs} input roots — the strictest surah-level joint signal.")
    c4.metric("Avg inputs / surah",
              f"{surah_to_roots['NumInputsInSurah'].mean():.2f}" if not surah_to_roots.empty else "—",
              help="Mean number of input roots present per surah that has at least one hit.")

    st.divider()
    layer(2, "Each surah's contribution — stacked by input root")
    if surah_root_hits.empty:
        st.caption("No data.")
    else:
        fig = px.bar(surah_root_hits, x="Surah #", y="Hits", color="Input Root",
                     color_discrete_sequence=CAT_PAL, labels={"Hits": "Ayah hits"})
        fig.update_layout(barmode="stack",
                          title=dict(text="<b>Ayah hits per surah, stacked by input root</b>",
                                     x=0.5, font=dict(size=16)),
                          xaxis=dict(tickmode="linear", dtick=5),
                          paper_bgcolor="#FFFFFF", plot_bgcolor="#FAFBFD",
                          height=420, margin=dict(l=30, r=20, t=46, b=30))
        st.plotly_chart(fig, width='stretch')
        try:
            _tot_by_surah = surah_root_hits.groupby("Surah #")["Hits"].sum().sort_values(ascending=False)
            _ts = int(_tot_by_surah.index[0]); _th = int(_tot_by_surah.iloc[0])
            _n_all = int((surah_to_roots["NumInputsInSurah"] >= n_inputs).sum())
            st.markdown(
                f"**📍 What to take from this chart:** the joint activity peaks in "
                f"**S{_ts}** ({_th} ayah-hits across the stacked roots); "
                f"{_n_all} of 114 surahs contain **all {n_inputs}** input roots, so the "
                f"surah-level view is where the co-presence signal actually lives."
            )
        except Exception:
            pass

    st.divider()
    layer(3, "Heat strip — how many input roots appear in each surah")
    if surah_to_roots.empty:
        st.caption("No data.")
    else:
        heat_df = surah_to_roots.sort_values("Surah #").copy()
        # Plotly can't serialize Python sets — render as a sorted string for hover
        heat_df["RootsList"] = heat_df["RootsInSurah"].apply(
            lambda s: " · ".join(sorted(s)))
        fig2 = px.bar(heat_df, x="Surah #", y="NumInputsInSurah",
                      color="NumInputsInSurah", color_continuous_scale="Sunset",
                      labels={"NumInputsInSurah": "# inputs present"},
                      hover_data={"RootsList": True, "NumInputsInSurah": True})
        fig2.update_layout(coloraxis_colorbar=dict(title="# inputs", thickness=12),
                           xaxis=dict(tickmode="linear", dtick=5),
                           height=280, paper_bgcolor="#FFFFFF", plot_bgcolor="#FAFBFD",
                           margin=dict(l=30, r=20, t=20, b=30))
        st.plotly_chart(fig2, width='stretch')

    st.divider()
    layer(4, "Top surahs — ranked by density of joint activity")
    rank = surah_to_roots.copy()
    if not rank.empty:
        name_lookup = occ.drop_duplicates(["Surah #"]).set_index("Surah #")["Surah Name"]
        rank["Surah Name"] = rank["Surah #"].map(name_lookup)
        # Per-root hit counts per surah
        per_root_pivot = (surah_root_hits.pivot(index="Surah #", columns="Input Root",
                                                 values="Hits").fillna(0).astype(int))

        def _breakdown(sid):
            row = per_root_pivot.loc[sid] if sid in per_root_pivot.index else None
            if row is None:
                return ""
            items = sorted(
                [(r, int(c)) for r, c in row.items() if c > 0],
                key=lambda x: -x[1])
            return "  ·  ".join(f"{r}: {c}" for r, c in items)

        rank["Per-root hits"] = rank["Surah #"].apply(_breakdown)
        rank["Total joint hits"] = rank["Surah #"].apply(
            lambda sid: int(per_root_pivot.loc[sid].sum())
                        if sid in per_root_pivot.index else 0)
        # Surah size (total ayahs in the surah) and density %
        ayahs_per_surah = corpus.df.groupby(_A.COL_SURAH).size().to_dict()
        rank["Surah ayahs"] = rank["Surah #"].apply(lambda sid: int(ayahs_per_surah.get(sid, 0)))
        # Ayahs in this surah touched by at least one input root
        touched_per_surah = (occ.drop_duplicates(["Surah #", "Ayah #"])
                                .groupby("Surah #").size().to_dict())
        rank["Touched ayahs"] = rank["Surah #"].apply(lambda sid: int(touched_per_surah.get(sid, 0)))
        rank["Density %"] = (100.0 * rank["Touched ayahs"] /
                              rank["Surah ayahs"].replace(0, 1)).round(1)
        rank["# inputs"] = rank["NumInputsInSurah"].astype(str) + f"/{n_inputs}"

        # Sort by density desc, then total hits desc — most thematic surahs on top
        rank = rank.sort_values(["Density %", "Total joint hits", "Surah #"],
                                  ascending=[False, False, True])

        display = rank[["Surah #", "Surah Name", "# inputs", "Per-root hits",
                         "Total joint hits", "Surah ayahs", "Touched ayahs",
                         "Density %"]].head(30)
        st.dataframe(display, width='content', hide_index=True, height=440)
        st.caption(
            "**Density %** = ayahs in this surah that contain at least one of your input "
            "roots, divided by the total ayahs in the surah.  A high density means the "
            "surah is genuinely \"about\" your query."
        )


def _render_k_of_n():
    layer(1, "At least k of N inputs — adjust strictness")
    max_k = n_inputs
    k = st.slider("Require at least k of N inputs in the same ayah",
                  min_value=2, max_value=max_k, value=2,
                  help=f"k = {max_k} is the strict intersection (often empty for "
                       f"large N).  k = 2 is the most permissive.",
                  key="kofn_slider")

    qualified = ayah_roots[ayah_roots["NumInputs"] >= k]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Threshold k", k)
    c2.metric("Qualifying ayahs", len(qualified))
    c3.metric("Surahs covered", qualified["Surah #"].nunique() if not qualified.empty else 0)
    union_size = len(R["match_ayahs"]) if R["match_ayahs"] else 0
    pct = (100.0 * len(qualified) / max(union_size, 1)) if union_size else 0
    c4.metric("% of union ayahs", f"{pct:.1f}%")

    if qualified.empty:
        st.warning(f"No ayahs contain {k} or more of your input roots together.")
        return

    qualified_keys = set(map(tuple, qualified[["Surah #", "Ayah #"]].to_numpy()))
    sub_rows = occ[occ.apply(lambda r: (r["Surah #"], r["Ayah #"]) in qualified_keys, axis=1)]

    st.divider()
    layer(2, "Surah distribution of qualifying ayahs (stacked by input root)")
    g = sub_rows.groupby(["Surah #", "Input Root"]).size().reset_index(name="Hits")
    fig = px.bar(g, x="Surah #", y="Hits", color="Input Root",
                 color_discrete_sequence=CAT_PAL,
                 labels={"Hits": "Ayah hits"})
    fig.update_layout(barmode="stack",
                      title=dict(text=f"<b>Qualifying ayahs (k≥{k}) by surah</b>",
                                 x=0.5, font=dict(size=16)),
                      xaxis=dict(tickmode="linear", dtick=5),
                      paper_bgcolor="#FFFFFF", plot_bgcolor="#FAFBFD",
                      height=360, margin=dict(l=30, r=20, t=46, b=30))
    st.plotly_chart(fig, width='stretch')

    st.divider()
    layer(3, "The qualifying ayahs")
    st.caption(f"{len(qualified)} unique ayahs · 2-column layout.")
    st.markdown("""
<style>
.kayah-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;}
.kayah-row{border:1px solid #E2E8F1;border-radius:8px;padding:6px 10px;background:#FFFFFF;}
.kayah-row .ar{direction:rtl;text-align:right;font-family:'Amiri','Amiri Quran','Noto Naskh Arabic',serif;font-size:18px;line-height:1.5;color:#243447;margin:0;}
.kayah-row .meta{font-size:12px;color:#10243A;margin:0;line-height:1.2;}
</style>
""", unsafe_allow_html=True)
    has_dia = R.get("has_diacritized")
    cards = []
    # Render one card per unique ayah, listing which inputs it contains
    name_lookup = occ.drop_duplicates(["Surah #"]).set_index("Surah #")["Surah Name"]
    for _, row in qualified.iterrows():
        surah_n = int(row["Surah #"])
        ayah_n = int(row["Ayah #"])
        present = sorted(row["RootsHere"])
        # Find the matching row in occ for diacritized text
        match = occ[(occ["Surah #"] == surah_n) & (occ["Ayah #"] == ayah_n)].iloc[0]
        if has_dia and match.get("Quranic Text (diacritized)"):
            ar = match["Quranic Text (diacritized)"]
        else:
            ar = match["Segmented Ayah"]
        sname = name_lookup.get(surah_n, "")
        meta = (f"S{surah_n}·A{ayah_n} · {sname} · contains: "
                f"<b>{' + '.join(present)}</b> "
                f"({len(present)}/{n_inputs})")
        cards.append(f"<div class='kayah-row'><div class='ar'>{ar}</div><div class='meta'>{meta}</div></div>")
    st.markdown(f"<div class='kayah-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)


def _render_overlay():
    layer(1, "Overlay across surahs — each input root on the same axes")
    # Build per-(surah, input root) ayah counts (unique-ayah, not row count)
    per = (occ.drop_duplicates(["Surah #", "Ayah #", "Input Root"])
              .groupby(["Surah #", "Input Root"]).size().reset_index(name="Ayahs"))

    use_small_multiples = n_inputs >= 5
    if use_small_multiples:
        st.info(f"You have {n_inputs} input roots — overlay would be cluttered, "
                f"so we're using small-multiples (one panel per root) instead.")
        fig = px.bar(per, x="Surah #", y="Ayahs", color="Input Root",
                     facet_col="Input Root", facet_col_wrap=2,
                     color_discrete_sequence=CAT_PAL,
                     labels={"Ayahs": "Ayah hits"})
        fig.update_layout(showlegend=False,
                          title=dict(text="<b>Per-root surah distribution (small multiples)</b>",
                                     x=0.5, font=dict(size=16)),
                          paper_bgcolor="#FFFFFF", plot_bgcolor="#FAFBFD",
                          height=max(420, 220 * ((n_inputs + 1) // 2)),
                          margin=dict(l=30, r=20, t=46, b=30))
        fig.update_xaxes(matches=None, tickmode="linear", dtick=10)
        fig.update_yaxes(matches=None)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        st.plotly_chart(fig, width='stretch')
    else:
        # Semi-transparent overlay — area chart per root
        fig = go.Figure()
        for i, r in enumerate(R["input_roots"]):
            sub_r = per[per["Input Root"] == r].sort_values("Surah #")
            color = CAT_PAL[i % len(CAT_PAL)]
            fig.add_trace(go.Bar(
                x=sub_r["Surah #"], y=sub_r["Ayahs"],
                name=r, marker_color=color, opacity=0.55,
                hovertemplate=f"<b>{r}</b><br>Surah %{{x}}<br>Ayahs: %{{y}}<extra></extra>",
            ))
        fig.update_layout(barmode="overlay",
                          title=dict(text="<b>Surah distribution — overlay of input roots</b>",
                                     x=0.5, font=dict(size=16)),
                          xaxis=dict(title="Surah #", tickmode="linear", dtick=5),
                          yaxis=dict(title="Ayah hits"),
                          paper_bgcolor="#FFFFFF", plot_bgcolor="#FAFBFD",
                          legend=dict(orientation="h", yanchor="bottom", y=1.02),
                          height=420, margin=dict(l=30, r=20, t=66, b=30))
        st.plotly_chart(fig, width='stretch')

    st.divider()
    layer(2, "Side-by-side counts per surah (sortable)")
    pivot = per.pivot(index="Surah #", columns="Input Root", values="Ayahs").fillna(0).astype(int)
    pivot["Total"] = pivot.sum(axis=1)
    pivot["# Inputs present"] = (pivot.drop(columns=["Total"]) > 0).sum(axis=1)
    pivot = pivot.reset_index().sort_values("Total", ascending=False).head(40)
    st.dataframe(pivot, width='content', hide_index=True, height=480)


# Sub-mode picker
sub_modes = {
    "🟪 Co-present in surah": _render_co_present_in_surah,
    "🎚️ At least k of N (slider)": _render_k_of_n,
    "🔀 Overlay across surahs": _render_overlay,
}
mode = st.radio(
    "Combined-view sub-mode",
    list(sub_modes.keys()), index=0, horizontal=True,
    key="combined_submode",
    help=("Co-present: surah-level co-presence (most populated). "
          "k of N: ayah-level with adjustable strictness. "
          "Overlay: each root's surah distribution superimposed.")
)
st.divider()
sub_modes[mode]()
