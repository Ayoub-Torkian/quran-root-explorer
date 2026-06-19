"""Ayah Browser — diacritized Quranic text first, then segmented + word-by-word."""
import streamlit as st

from state import (get_corpus, query_controls, compute_all, need_results,
                   hero, layer, highlight_text, render_quranic_verse, per_root_hint, log_page)
import meaning as _MEAN
import mobile as _MOB

st.set_page_config(page_title="Ayah Browser", page_icon="📖", layout="wide")
_MOB.inject()                       # mobile-first reading CSS + Qur'an webfonts (after set_page_config)
log_page("ayahs")
corpus = get_corpus()
raw, normalize, top_p, min_w, run = query_controls(corpus)
from state import needs_recompute
if run or needs_recompute():
    compute_all(corpus, raw, normalize, top_p, min_w)
R = need_results()

hero("📖 Ayah Browser",
     "Every matched ayah — full diacritized Quranic text, segmented form, and word-by-word alignment.")
per_root_hint(compact=True)
_MOB.settings_controls(st)          # ⚙️ text size (Arabic-first) + line spacing

occ = R["occurrences"]

layer(1, "How many ayahs match")
c1, c2, c3 = st.columns(3)
c1.metric("Total ayah hits", len(occ),
          help="One row per (root, ayah) match — an ayah containing 2 input roots counts twice here.")
c2.metric("Unique ayahs",
          occ[["Surah #", "Ayah #"]].drop_duplicates().shape[0] if not occ.empty else 0,
          help="Distinct verses matched, counted once each regardless of how many input roots they contain.")
c3.metric("Surahs covered", occ["Surah #"].nunique() if not occ.empty else 0,
          help="Distinct surahs (out of 114) containing at least one matched ayah.")

st.divider()
layer(2, "Filter & search")
c1, c2, c3 = st.columns(3)
with c1:
    root_pick = st.multiselect("Filter by input root", R["input_roots"],
                               default=R["input_roots"], key="ayah_root_pick")
with c2:
    available_surahs = sorted(occ["Surah #"].unique().tolist()) if not occ.empty else []
    surah_pick = st.multiselect("Filter by surah #", available_surahs,
                                default=available_surahs[:30] if len(available_surahs) > 30 else available_surahs,
                                key="ayah_surah_pick")
with c3:
    free_text = st.text_input("Search inside ayah text", key="ayah_search",
                              placeholder="type any Arabic chars…")

filtered = occ.copy()
if root_pick:
    filtered = filtered[filtered["Input Root"].isin(root_pick)]
if surah_pick:
    filtered = filtered[filtered["Surah #"].isin(surah_pick)]
if free_text:
    from analysis import strip_diacritics
    needle = strip_diacritics(free_text)
    filtered = filtered[filtered["Segmented Ayah"].str.contains(needle, na=False)]

st.caption(f"**{len(filtered)}** rows match.")

# ── Per-sūra profile of the filtered matches (Meccan/Medinan control frame) ──
try:
    import plotly.graph_objects as _go
    MEDINAN = {2, 3, 4, 5, 8, 9, 13, 22, 24, 33, 47, 48, 49, 55, 57, 58, 59, 60,
               61, 62, 63, 64, 65, 66, 76, 98, 99, 110}
    if not filtered.empty:
        _per_s = (filtered.drop_duplicates(["Surah #", "Ayah #"])
                          .groupby("Surah #").size())
        _ys = [int(_per_s.get(s, 0)) for s in range(1, 115)]
        _fig_b = _go.Figure(_go.Bar(
            x=list(range(1, 115)), y=_ys,
            marker_color=["#E63946" if s in MEDINAN else "#1D9E75" for s in range(1, 115)],
            hovertemplate="Surah %{x}<br>Matched ayahs: %{y}<extra></extra>"))
        _fig_b.update_layout(
            title=dict(text="<b>Matched ayahs per sūra — your current filter</b> "
                            "(🟩 Meccan · 🟥 Medinan — control-only)", x=0.5,
                       font=dict(size=14)),
            xaxis_title="sūra # (muṣḥaf order)", yaxis_title="matched ayahs",
            height=280, margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor="#FFFFFF", plot_bgcolor="#FAFBFD")
        st.plotly_chart(_fig_b, width='stretch')
        _uniq = int(_per_s.sum())
        _n_su = int((_per_s > 0).sum())
        _top_s = int(_per_s.idxmax()); _top_n = int(_per_s.max())
        _med_n = int(sum(v for s, v in _per_s.items() if int(s) in MEDINAN))
        _med_pct = round(100 * _med_n / max(_uniq, 1), 1)
        st.markdown(
            f"**📍 What to take from this chart:** your filter matches {_uniq} unique "
            f"ayahs spread over {_n_su} surahs; the densest is **S{_top_s}** with "
            f"{_top_n} matched ayahs, and {_med_pct}% of matches fall in Medinan sūras "
            f"(Meccan/Medinan is a human classification used as a control frame — "
            f"not a claim).")
except Exception:
    pass

st.divider()
layer(3, "Summary table")
cols_for_table = ["Input Root", "Surah #", "Ayah #", "Surah Name",
                  "Surface Form(s)"]
if R.get("has_diacritized"):
    cols_for_table.append("Quranic Text (diacritized)")
st.dataframe(filtered[cols_for_table],
             width='content', hide_index=True, height=360)

st.divider()
layer(4, "Read each ayah — diacritized Quranic text + word-by-word")

page_size = st.select_slider("Rows per page", [10, 25, 50, 100], value=10,
                             key="ayah_pgsize")
total_pages = max(1, (len(filtered) + page_size - 1) // page_size)
page = st.number_input("Page", min_value=1, max_value=total_pages,
                       value=1, step=1, key="ayah_page")
start = (page - 1) * page_size
end = start + page_size
page_rows = filtered.iloc[start:end]

sf_for = {q: R["sforms"][R["sforms"]["Input Root"] == q]["Surface Form (col 5)"].tolist()
          for q in R["input_roots"]}

st.markdown("""
<style>
.ayah-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px 10px;}
.ayah-card{border:1px solid #E2E8F1;border-radius:10px;padding:8px 12px;background:#FFFFFF;}
.ayah-card .ar{direction:rtl;text-align:right;font-family:'Amiri','Amiri Quran','Noto Naskh Arabic',serif;font-size:18px;line-height:1.55;color:#243447;margin:0 0 4px 0;}
.ayah-card .en{font-size:13px;color:#10243A;line-height:1.6;margin:0 0 4px 0;}
.ayah-card .meta{font-size:12px;color:#10243A;margin:0;}
</style>
""", unsafe_allow_html=True)
# honor the global translation choice (set on Search/Deep-Dive; persists in session)
_trchoice = st.session_state.get("tr_lang", "Off")
_trlang = {"English": "en", "العربية": "ar", "اردو": "ur", "فارسی": "fa",
           "All languages": "en", "Off": None}.get(_trchoice, "en")
_trdir = "rtl" if _trlang in ("ar", "ur", "fa") else "ltr"
cards = []
for _, row in page_rows.iterrows():
    ar = ""
    if R.get("has_diacritized") and row.get("Quranic Text (diacritized)"):
        ar = row["Quranic Text (diacritized)"]
    else:
        ar = row["Segmented Ayah"]
    meta = (f"S{row['Surah #']}·A{row['Ayah #']} · {row['Surah Name']} · "
            f"input: <b>{row['Input Root']}</b> · surface: {row['Surface Form(s)']}")
    _en = _MEAN.gloss(f"{int(row['Surah #'])}:{int(row['Ayah #'])}", "en")
    _en_html = f"<div class='en'>{_en}</div>" if _en else ""
    cards.append(f"<div class='ayah-card'><div class='ar'>{ar}</div>{_en_html}<div class='meta'>{meta}</div></div>")
st.markdown(f"<div class='ayah-grid'>{''.join(cards)}</div>", unsafe_allow_html=True)
