"""HOME — Quran Explorer command center (Module 1 active).

v4: Prominent top input bar + highly visible menu items.
"""
from __future__ import annotations

import io
import tempfile
import zipfile
from pathlib import Path

import pandas as pd
import streamlit as st

import analysis as A
import plotly_charts as PC
from state import (
    compute_all, get_corpus, hero, layer, need_results, query_controls,
    render_top_input_bar, log_page, log_search,
)


st.set_page_config(page_title="Quran Explorer", page_icon="📖",
                   layout="wide", initial_sidebar_state="expanded")
log_page("home")


MODULES = [
    {"id": "roots",   "icon": "🌱", "name": "Root Exploration", "status": "active"},
    {"id": "topics",  "icon": "🧭", "name": "Topic Exploration", "status": "planned"},
    {"id": "motifs",  "icon": "🔺", "name": "Motif Analysis",    "status": "planned"},
    {"id": "kwic",    "icon": "🔎", "name": "Concordance (KWIC)", "status": "idea"},
    {"id": "stylo",   "icon": "🎨", "name": "Stylometry",        "status": "idea"},
    {"id": "compare", "icon": "⚖️", "name": "Cross-corpus",      "status": "idea"},
]


def _render_module_bar():
    st.markdown(
        "<div style='display:flex; gap:6px; flex-wrap:wrap; margin-bottom:10px;'>"
        + "".join(
            f"<span style='padding:6px 12px; border-radius:18px; font-size:13px; "
            f"background:{'#1D3557' if m['status']=='active' else '#E2E8F1'}; "
            f"color:{'white' if m['status']=='active' else '#10243A'}; "
            f"font-weight:{'700' if m['status']=='active' else '500'};'>"
            f"{m['icon']} {m['name']}"
            f"{'  ✓' if m['status']=='active' else '  · ' + m['status']}</span>"
            for m in MODULES
        )
        + "</div>",
        unsafe_allow_html=True,
    )


SAMPLE_QUERIES = {
    "🤲 Mercy & faith":         ["رحم", "ءله", "ءمن"],
    "📚 Knowledge cluster":     ["علم", "حکم", "ذکر"],
    "⚖️ Justice & truth":       ["عدل", "حقق", "قسط"],
    "🙏 Patience & gratitude":  ["صبر", "شکر"],
    "🕋 Prayer & charity":      ["صلو", "زکو", "صوم"],
    "👤 Human & soul":          ["نفس", "ءنس", "روح"],
    "🌍 Creation & life":       ["خلق", "حیی", "ربب"],
    "🔥 Punishment & reward":   ["عذب", "جزی", "جنن"],
}


def _set_query(roots):
    st.session_state.query_roots = list(roots)
    st.session_state["_force_rerun"] = True


def _add_root_to_query(r):
    if r and r not in st.session_state.get("query_roots", []):
        st.session_state.query_roots.append(r)
        st.session_state["_force_rerun"] = True


def render_per_root_picker(R):
    """High-visibility per-root jump-card row. Rendered ABOVE the tabs so
    the user can immediately switch to any input root's dedicated page,
    regardless of which tab is currently active."""
    if not R.get("input_roots"):
        return
    layer(1, "Per-root breakdown — pick a root to deep-dive")
    st.markdown(
        """
        <div style="background: #EEF3FB;
                    border-left:5px solid #1D3557; border-radius:14px;
                    padding:14px 18px; margin:6px 0 14px 0;
                    box-shadow:0 1px 4px rgba(0,0,0,0.06);
                    animation: pulseHint 2.6s ease-in-out infinite;">
          <div style="font-size:17px; font-weight:700; color:#1D3557;
                      letter-spacing:0.4px; margin-bottom:6px;">
            👉 WANT THE FULL PROFILE OF JUST ONE ROOT?
          </div>
          <div style="font-size:14.5px; color:#243447; line-height:1.6;">
            Click the <b style="background:#1D9E75; color:#fff;
              padding:2px 10px; border-radius:6px;">🔍 Open in Per Root Profile →</b>
            button under any card below — or use
            <b style="background:#1D3557; color:#fff; padding:2px 10px;
                      border-radius:6px;">🔍 Per Root Profile</b>
            in the <b>left-sidebar navigation</b>. Every input root has its
            own dedicated page with full charts, ayahs, surface forms, and partners.
          </div>
        </div>
        <style>
          @keyframes pulseHint {
            0%,100% { box-shadow:0 1px 4px rgba(0,0,0,0.06); }
            50%     { box-shadow:0 1px 4px rgba(0,0,0,0.06); }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
    cards = st.columns(min(len(R["input_roots"]), 4))
    for i, root in enumerate(R["input_roots"]):
        sub = R["occurrences"][R["occurrences"]["Input Root"] == root]
        n_ayahs = sub[["Surah #", "Ayah #"]].drop_duplicates().shape[0]
        n_surahs = sub["Surah #"].nunique() if not sub.empty else 0
        rrow = R["rarity"][R["rarity"]["Input Root"] == root]
        tier = rrow["Tier"].iloc[0] if not rrow.empty else "—"
        pct = rrow["Percentile"].iloc[0] if not rrow.empty else 0
        pm = R["pmotifs"][R["pmotifs"]["Input Root"] == root].head(3)
        top_partners = " · ".join(pm["Partner Root"].tolist()) if not pm.empty else "—"
        tier_color = {"ultra-rare": "#378ADD", "rare": "#378ADD",
                      "common": "#1D9E75", "very common": "#EF9F27",
                      "ubiquitous": "#1D3557"}.get(tier, "#1D3557")
        with cards[i % len(cards)]:
            st.markdown(
                f"""
                <div style="border:1px solid #E2E8F1; border-radius:12px;
                            padding:10px 12px; background:#FFFFFF; margin-bottom:6px;">
                    <div style="font-size:22px; font-weight:700; color:#1D3557;
                                text-align:center; margin-bottom:4px;">{root}</div>
                    <div style="font-size:13px; color:#243447; line-height:1.55;">
                        <b>{n_ayahs}</b> ayahs · <b>{n_surahs}</b> surahs<br>
                        Tier: <span style="background:{tier_color}; color:white;
                            padding:1px 8px; border-radius:8px; font-weight:700;">{tier}</span>
                            (top {100-pct:.0f}%)<br>
                        Top partners: <b>{top_partners}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"🔍 Open '{root}' in Per Root Profile  →",
                         key=f"top_goto_prr_{root}",
                         width='stretch',
                         type="primary"):
                st.session_state.profile_root = root
                st.switch_page("pages/1_Per_Root_Profile.py")
    st.divider()


def tab_process(corpus, R):
    # ─────────── COMBINED HEADLINE METRICS ───────────
    layer(1, "Status — combined across all input roots")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Input roots", len(R["input_roots"]))
    c2.metric("Ayahs matched", len(R["match_ayahs"]))
    c3.metric("Co-occurring roots", len(R["partners"]))
    c4.metric("Triangles", R["triad"]["triangles (closed triads)"])

    st.divider()
    layer(2, "Variations of your current query — one click")
    cur = R["input_roots"]
    partners = R["partners"]
    if not cur:
        st.caption("Add at least one root above to see related queries.")
    else:
        variations = []
        # Single-root drill-downs
        for r in cur:
            variations.append((f"🎯 Just  {r}", [r]))
        # Each input + top 1 partner
        top_p = [p for p, _ in partners.most_common(3)]
        for r in cur:
            for tp in top_p:
                if tp not in cur:
                    variations.append((f"➕ {r} + {tp}", [r, tp]))
                    break
        # Current + top-1 partner
        if top_p and top_p[0] not in cur:
            variations.append((f"📈 Current + {top_p[0]}", list(cur) + [top_p[0]]))
        # Current + top-3 partners
        new_top3 = [p for p in top_p if p not in cur][:3]
        if new_top3:
            variations.append((f"🌐 Current + top 3 partners", list(cur) + new_top3))
        # Strongest pair from current
        if len(cur) >= 2:
            from itertools import combinations
            best_pair, best_w = None, -1
            for a, b in combinations(cur, 2):
                w = R["overlap"].loc[a, b] if not R["overlap"].empty else 0
                if w > best_w:
                    best_w, best_pair = w, (a, b)
            if best_pair:
                variations.append((f"🤝 Strongest pair: {best_pair[0]} + {best_pair[1]}", list(best_pair)))

        # Render in 3-column grid
        cols = st.columns(3)
        for i, (label, roots) in enumerate(variations[:9]):
            with cols[i % 3]:
                if st.button(label, key=f"var_{i}", width='stretch'):
                    _set_query(roots); st.rerun()

    st.divider()
    layer(3, "One-click actions")
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("🚀 Re-run", width='stretch'):
        st.session_state["_force_rerun"] = True; st.rerun()
    if c2.button("🔁 Toggle exact↔normalized", width='stretch'):
        st.session_state.normalize = not R["normalize"]
        st.session_state["_force_rerun"] = True; st.rerun()
    if c3.button("🗑️ Clear roots", width='stretch'):
        st.session_state.query_roots = []; st.rerun()
    if c4.button("✨ Add top 5 partners", width='stretch'):
        for p, _ in R["partners"].most_common(5):
            _add_root_to_query(p)
        st.rerun()

    st.divider()
    layer(3, "Suggested partners — click to add")
    top15 = R["partners"].most_common(15)
    if not top15:
        st.caption("(no partners yet)")
    else:
        cols = st.columns(5)
        for i, (root, n) in enumerate(top15):
            with cols[i % 5]:
                if st.button(f"+ {root}  ({n})", key=f"addp_{root}",
                             width='stretch'):
                    _add_root_to_query(root); st.rerun()

    st.divider()
    layer(4, "Parameter tuning (advanced)")
    with st.expander("Edit thresholds and re-run"):
        nt = st.slider("Top partners", 5, 40, R["top_partners"], key="tune_top")
        nm = st.slider("Min edge weight", 1, 10, R["min_weight"], key="tune_min")
        if st.button("Apply", key="apply_tune"):
            st.session_state.top_partners = nt
            st.session_state.min_weight = nm
            st.session_state["_force_rerun"] = True; st.rerun()


def tab_visualize(R):
    layer(1, "Visualization catalogue — pick what to render")
    catalogue = [
        ("📊 Distribution across surahs",   "dist"),
        ("📈 Per-root summary",             "summ"),
        ("🏷️ Rarity vs corpus baseline",    "rare"),
        ("🌐 Co-occurrence network",        "net"),
        ("⭕ Communities treemap",          "tree"),
        ("📐 Centrality ranking",           "cent"),
        ("🔺 Motif summary",                "motif"),
        ("🥇 Top triangles",                "tri"),
        ("🔥 Surah × Root heatmap",         "heat"),
        ("🔀 Overlap matrix",               "over"),
        ("🧬 Morphology (all roots)",       "morph"),
    ]
    if "show_charts" not in st.session_state:
        st.session_state.show_charts = {"dist", "rare", "net"}
    cols = st.columns(3)
    for i, (label, key) in enumerate(catalogue):
        with cols[i % 3]:
            on = key in st.session_state.show_charts
            new = st.checkbox(label, value=on, key=f"chk_{key}")
            if new and not on:
                st.session_state.show_charts.add(key)
            elif not new and on:
                st.session_state.show_charts.discard(key)

    st.divider()
    layer(2, "Inline gallery")
    sel = st.session_state.show_charts
    renderers = {
        "dist": lambda: PC.chart_distribution_across_surahs(R["occurrences"]),
        "summ": lambda: PC.chart_summary_metric_bars(R["summary"]),
        "rare": lambda: PC.chart_rarity_tier(R["rarity"]),
        "net":  lambda: PC.chart_network(R["graph"], R["communities"]),
        "tree": lambda: PC.chart_communities_treemap(R["graph"], R["communities"]),
        "cent": lambda: PC.chart_centrality(R["centrality"]),
        "motif": lambda: PC.chart_motif_summary(R["triad"]),
        "tri": lambda: PC.chart_triangle_table_bar(R["triangles"]),
        "heat": lambda: PC.chart_surah_heatmap(R["heatmap"]),
        "over": lambda: PC.chart_overlap_heatmap(R["overlap"]),
        "morph": lambda: PC.chart_morphology(R["morphology"]),
    }
    for k in [k for _, k in catalogue if k in sel]:
        st.plotly_chart(renderers[k](), width='stretch')


def tab_export(corpus, R):
    layer(1, "What an export contains")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Excel sheets", "13")
    c2.metric("Charts", "4")
    c3.metric("PDF pages", "4")
    total = (len(R["occurrences"]) + len(R["cooc_tbl"]) + len(R["sforms"])
             + len(R["pmotifs"]) + len(R["triangles"]))
    c4.metric("Data rows", total)

    st.divider()
    layer(2, "One-click downloads")
    meta = {
        "Input roots": " ".join(R["input_roots"]),
        "Normalization": "ON" if R["normalize"] else "OFF (exact)",
        "Co-occurrence scope": "same ayah",
        "Top partners": R["top_partners"],
        "Min edge weight": R["min_weight"],
        "Ayahs in corpus": corpus.n_ayahs,
        "Ayahs matched": len(R["match_ayahs"]),
    }
    figures = [
        ("01_summary_distribution.png", A.plot_surah_distribution(R["occurrences"])),
        ("02_top_partners.png", A.plot_top_partners(R["partners"], top=20)),
        ("03_network.png", A.plot_network(R["graph"], set(R["input_roots"]))),
        ("04_motif_summary.png", A.plot_triad_summary(R["triad"])),
    ]
    c1, c2, c3 = st.columns(3)
    with tempfile.TemporaryDirectory() as td:
        xlsx_out = Path(td) / "quran_root_analysis.xlsx"
        A.export_excel(xlsx_out, summary=R["summary"], occurrences=R["occurrences"],
            cooccurrence_tbl=R["cooc_tbl"], surface_forms=R["sforms"],
            partner_motifs_tbl=R["pmotifs"], triangles_tbl=R["triangles"],
            triad_summary=R["triad"], meta=meta, centrality=R["centrality"],
            heatmap=R["heatmap"], overlap=R["overlap"], morphology=R["morphology"],
            position=R["position"], rarity=R["rarity"], first_last=R["first_last"])
        xlsx_bytes = xlsx_out.read_bytes()
    c1.download_button("⬇️ Multi-sheet Excel", data=xlsx_bytes,
                       file_name="quran_root_analysis.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       width='stretch')
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as zf:
        for name, fig in figures:
            zf.writestr(name, A.figure_to_png_bytes(fig))
    c2.download_button("⬇️ Charts (PNG zip)", data=zip_buf.getvalue(),
                       file_name="quran_root_charts.zip", mime="application/zip",
                       width='stretch')
    with tempfile.TemporaryDirectory() as td:
        pdf_out = Path(td) / "quran_root_charts.pdf"
        A.figures_to_pdf([f for _, f in figures], pdf_out)
        pdf_bytes = pdf_out.read_bytes()
    c3.download_button("⬇️ Combined PDF", data=pdf_bytes,
                       file_name="quran_root_charts.pdf", mime="application/pdf",
                       width='stretch')


def tab_display(R):
    layer(1, "Display preferences")
    if "display" not in st.session_state:
        st.session_state.display = dict(density="comfortable", layers_open=2,
                                        show_ayah_text=True, color_mode="vibrant",
                                        expanders_default=False, table_height=380)
    D = st.session_state.display
    st.divider()
    layer(2, "Quick presets")
    c1, c2, c3 = st.columns(3)
    if c1.button("📰 Compact", width='stretch'):
        D.update(density="compact", layers_open=1, table_height=260); st.rerun()
    if c2.button("📖 Comfortable", width='stretch'):
        D.update(density="comfortable", layers_open=2, table_height=380); st.rerun()
    if c3.button("🔬 Deep dive", width='stretch'):
        D.update(density="comfortable", layers_open=4, table_height=520); st.rerun()


def tab_explore(corpus, R):
    layer(1, "Learn the corpus")
    c1, c2, c3 = st.columns(3)
    c1.metric("Ayahs in corpus", corpus.n_ayahs)
    c2.metric("Unique roots", corpus.n_unique_roots)
    avg = sum(len(t) for t in corpus.root_tokens) / max(corpus.n_ayahs, 1)
    c3.metric("Avg roots / ayah", f"{avg:.1f}")

    st.divider()
    layer(2, "Top corpus-wide roots — click to add to query")
    freq = corpus.freq_norm if R["normalize"] else corpus.freq_exact
    top = freq.most_common(20)
    cols = st.columns(5)
    for i, (r, n) in enumerate(top):
        with cols[i % 5]:
            if st.button(f"+ {r}  ({n})", key=f"explore_{r}",
                         width='stretch'):
                _add_root_to_query(r); st.rerun()


def main():
    corpus = get_corpus()
    # Sidebar still has full query controls
    raw, normalize, top_p, min_w, run = query_controls(corpus)
    # (Corpus totals live in the page header now — no duplicate sidebar metrics.)

    # ====== header — readable & bold, one accent rule, stats fill the right ======
    try:
        _nr = "%s" % format(corpus.n_unique_roots, ",")
    except Exception:
        _nr = "1,701"
    st.markdown(
        "<div style='display:flex;align-items:baseline;gap:13px;padding:10px 2px 5px;flex-wrap:wrap'>"
        "<span style='font-size:29px;font-weight:800;color:#1D3557;letter-spacing:-.3px'>📖 Quran Explorer</span>"
        "<span style='font-size:16px;font-weight:700;color:#1D9E75'>Root Exploration</span>"
        "<span style='margin-left:auto;font-size:13.5px;font-weight:700;color:#10243A'>"
        "114 sūras &middot; 6,236 āyāt &middot; %s roots</span>"
        "</div>"
        "<div style='height:3px;background:linear-gradient(90deg,#1D3557,#1D9E75 55%%,rgba(29,158,117,0));"
        "border-radius:3px;margin:0 0 16px'></div>" % _nr,
        unsafe_allow_html=True)
    # ====== ORIENTATION — distinct bordered panel (redundant "Read & explore" removed) ======
    with st.container(border=True):
        st.markdown("<div style='font-size:14px;color:#10243A;margin:0 0 4px'>"
                    "<b>🧭 New here? Start with what you want to do</b></div>", unsafe_allow_html=True)
        _oc = st.columns(3)
        _paths = [
            ("pages/38_Search.py", "🔎 Search anything", "A word, phrase, root, or verse (2:255) — any spelling, diacritics optional."),
            ("pages/37_Discovery_Map.py", "💡 See what was discovered", "The map of graded findings and how they connect."),
            ("pages/22_Lens_Lab.py", "🧪 Check the rigor / claims", "18 lenses, verdicts, and reviewed claims."),
        ]
        for _i, (_p, _lab, _h) in enumerate(_paths):
            try:
                _oc[_i].page_link(_p, label=_lab, help=_h)
            except Exception:
                pass
        st.caption("Four areas — 🔭 EXPLORE (use the text · you're here) · 💡 DISCOVER (findings) · "
                   "🧪 METHODS·LAB (rigor) · 🛠️ TOOLS")

    # ====== ROOT-EXPLORE section — distinct heading separating it from the orientation panel ======
    st.markdown("<div style='font-size:15px;color:#1D3557;margin:14px 0 2px'>"
                "<b>🌱 Explore the text — type or tap a root</b></div>", unsafe_allow_html=True)
    run_top = render_top_input_bar(corpus)

    # About / help tucked BELOW the action so it never pushes empty space up top.
    with st.expander("ℹ️  About this tool · page guide · new here?", expanded=False):
        st.markdown(
            "**What it does** — give it any Arabic root (or a list) and it scans all 6,236 ayahs "
            "for **where** the root appears, **what partners** it co-occurs with, **how tightly** they "
            "pair (PMI · Jaccard · P(B|A)), **what themes** cluster, and **when** in revelation order.\n\n"
            "| Page | What it tells you |\n|---|---|\n"
            "| 🔍 Per Root | each input's deep-dive |\n"
            "| 🌐 Network | graph visualisations |\n"
            "| 📖 Ayahs | every matched ayah |\n"
            "| 📈 Statistics | quantitative tiles |\n"
            "| 📡 Signal | the text as an ordered signal |\n"
            "| 🔭 Ayah Deep-Dive | a verse vs all relevant verses |\n"
            "| 🧬 Latent Feature Ledger | intrinsic, graded discoveries |\n\n"
            "**New here?** Domain terms (root · ayah · PMI · Jaccard · Louvain · TF-IDF) and the "
            "Position / Sequence / Semantic scales are all explained on the Help page — a few minutes "
            "there saves an hour of guessing.")
        try:
            st.page_link("pages/0_Help.py", label="Open the Help page", icon="❓")
        except Exception:
            pass

    # Recompute ONLY when there is something to compute. After START OVER the
    # query is intentionally empty and we land on a blank welcome screen — we
    # do NOT auto-fill defaults and we do NOT silently run an analysis.
    from state import needs_recompute as _need_recompute
    has_query = bool(st.session_state.get("query_roots"))
    if has_query and (run or run_top or _need_recompute()):
        raw_now = " ".join(st.session_state.query_roots)
        log_search(st.session_state.query_roots)
        compute_all(corpus, raw_now, normalize, top_p, min_w)

    # Empty-state — show the whole-Qur'an summary on the welcome screen
    if "results" not in st.session_state:
        try:
            import quran_overview
            quran_overview.render_overview(corpus, source="Book6")
        except Exception:
            pass
        return

    R = need_results()

    # Status banner under input
    st.info(
        f"📊 Currently analyzing **{len(R['input_roots'])} root(s)** · "
        f"**{len(R['match_ayahs'])}** ayahs matched · "
        f"matching: **{'normalized' if R['normalize'] else 'exact'}**"
    )

    # 🔔 PER-ROOT JUMP CARDS — TOP-LEVEL, ABOVE THE TABS
    # User can switch directly to any input root's dedicated page no matter
    # which tab they're looking at.
    render_per_root_picker(R)

    # ====== HIGHLY VISIBLE TABS ======
    tabs = st.tabs(["🔁  PROCESS", "📊  VISUALIZE", "⬇️  EXPORT",
                    "🎨  DISPLAY", "🧭  EXPLORE"])
    with tabs[0]: tab_process(corpus, R)
    with tabs[1]: tab_visualize(R)
    with tabs[2]: tab_export(corpus, R)
    with tabs[3]: tab_display(R)
    with tabs[4]: tab_explore(corpus, R)

    st.divider()
    st.caption(
        "📚 Use the **left navigation** for the eight deep-dive pages: "
        "Per-Root Profile · Network · Motifs · Ayah Browser · Compare & Heatmaps · "
        "Morphology · Statistics · Export."
    )


if __name__ == "__main__":
    main()
