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
    render_top_input_bar, log_page, log_search, chip_row,
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
    "🤲 Mercy":     ["رحم", "ءله", "ءمن"],
    "📚 Knowledge": ["علم", "حکم", "ذکر"],
    "⚖️ Justice":   ["عدل", "حقق", "قسط"],
    "🙏 Patience":  ["صبر", "شکر"],
    "🕋 Prayer":    ["صلو", "زکو", "صوم"],
    "👤 Soul":      ["نفس", "ءنس", "روح"],
    "🌍 Creation":  ["خلق", "حیی", "ربب"],
    "🔥 Reward":    ["عذب", "جزی", "جنن"],
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
    _multi = len(R["input_roots"]) >= 2
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
    if not _multi:        # pairwise charts are empty with a single root — hide rather than show a blank box
        catalogue = [(l, k) for l, k in catalogue if k != "over"]
        st.session_state.setdefault("show_charts", set()).discard("over")
        st.caption("Single root selected — the pairwise **Overlap matrix** is hidden (it needs ≥2 roots to compare).")
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
    # Render directly from the (freshly recomputed) results, with a stable key per chart.
    for k in [k for _, k in catalogue if k in sel]:
        try:
            st.plotly_chart(renderers[k](), width='stretch', key=f"vizchart_{k}")
        except Exception as _e:
            st.caption(f"(“{k}” unavailable: {type(_e).__name__})")


def tab_export(corpus, R):
    # The full export logic lives on the dedicated Export page (8_Export.py), built ON DEMAND.
    # This tab used to eagerly rebuild an Excel workbook + PNG zip + PDF on EVERY home-page rerun
    # (Streamlit renders all tab bodies each run) — a real perf drag and a duplicate surface.
    # It's now a lightweight pointer, so the home page stays fast and there is ONE export surface.
    layer(1, "Export & download")
    with st.container(key="inputbar-export"):
        st.markdown(
            "<div class='t-body'>Full exports — every chart and table plus the Reading-Guide narrative, "
            "as <b>PDF</b> · interactive <b>HTML</b> · multi-sheet <b>Excel</b> — are built "
            "<b>on demand</b> on the dedicated Export page (kept off the home page so it stays fast).</div>",
            unsafe_allow_html=True)
        try:
            st.page_link("pages/8_Export.py", label="Open the full Export page", icon="⬇️")
        except Exception:
            if st.button("⬇️  Open the full Export page", key="go_export"):
                st.switch_page("pages/8_Export.py")
    st.caption(f"It bundles everything for your current roots ({' · '.join(R['input_roots']) or '—'}).")


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
        "<span style='font-size:16px;font-weight:700;color:#1D9E75'>Read &middot; Analyze &middot; Learn &middot; Reflect</span>"
        "<span style='margin-left:auto;font-size:13.5px;font-weight:700;color:#10243A'>"
        "114 sūras &middot; 6,236 āyāt &middot; %s roots</span>"
        "</div>"
        "<div style='font-size:14px;font-weight:500;color:#10243A;margin:2px 0 8px 2px'>"
        "Anchored in fact, not interpretation — every claim measured from the text itself.</div>"
        "<div style='height:3px;background:linear-gradient(90deg,#1D3557,#1D9E75 55%%,rgba(29,158,117,0));"
        "border-radius:3px;margin:0 0 14px'></div>" % _nr,
        unsafe_allow_html=True)

    # ====== COMMAND CENTER — ONE compact card: primary Read on the left, the three
    #        other entry paths as high-contrast buttons on the right (replaces the two
    #        stacked boxes + the faint page-links that read as clutter). ======
    with st.container(border=True):
        st.markdown(
            "<div style='display:flex;align-items:baseline;gap:9px;flex-wrap:wrap;margin:0 0 6px'>"
            "<span style='font-size:20px;font-weight:800;color:#1D3557'>📖 Read &amp; listen</span>"
            "<span style='font-size:13px;font-weight:700;color:#1D9E75'>start here</span>"
            "<span style='font-size:13px;color:#10243A;margin-left:4px'>— read any sūra with "
            "translation; tap an āyah's ▶ to hear it recited, the player follows along.</span>"
            "</div>", unsafe_allow_html=True)
        # Buttons hug their text and sit left-aligned (fit-row) — NO full-width stretch / empty bands.
        with st.container(key="fitrow-homecmd"):
            _b1, _b2, _b3, _b4 = st.columns(4)
            if _b1.button("📖 Open the Reader  →", type="primary", key="home_open_read"):
                st.switch_page("pages/40_Read.py")
            if _b2.button("🔎 Search", key="home_open_search",
                          help="A word, phrase, root, or verse (2:255) — any spelling, diacritics optional."):
                st.switch_page("pages/38_Search.py")
            if _b3.button("💡 Discovered", key="home_open_disc",
                          help="The map of graded findings and how they connect."):
                st.switch_page("pages/37_Discovery_Map.py")
            if _b4.button("🧪 Rigor / claims", key="home_open_rigor",
                          help="18 lenses, verdicts, and reviewed claims."):
                st.switch_page("pages/22_Lens_Lab.py")

    # ====== JUMP TO A DISCOVERY — surface the distinctive DISCOVER views (the concept map,
    #        the scales, network roles, correspondence, flagship close-ups) that otherwise sit
    #        2–3 levels deep in the side menu. Styled as a tinted green-bordered LAUNCHPAD so it
    #        visibly stands out; buttons stay content-sized (fit-row) so no full-width sprawl. ======
    st.markdown(
        "<style>"
        "div.st-key-fitrow-quickdisc{background:#F4F9F7;border:1px solid #cfe4dc;"
        "border-left:5px solid #1D9E75;border-radius:12px;padding:11px 16px 13px;margin:16px 0 4px;"
        "box-shadow:0 1px 4px rgba(16,36,58,.07)}"
        "div.st-key-fitrow-quickdisc button{border:1.5px solid #1D9E75 !important;background:#fff !important;"
        "color:#1D3557 !important;font-weight:700 !important}"
        "div.st-key-fitrow-quickdisc button:hover{background:#1D9E75 !important;border-color:#0F6E56 !important}"
        "div.st-key-fitrow-quickdisc button:hover p,div.st-key-fitrow-quickdisc button:hover span{color:#fff !important}"
        "</style>", unsafe_allow_html=True)
    with st.container(key="fitrow-quickdisc"):
        st.markdown("<div style='font-size:16px;font-weight:800;color:#1D3557;margin:0 0 8px'>"
                    "🧭 Jump to a discovery&nbsp; <span style='font-size:13px;font-weight:600;color:#0F6E56'>"
                    "— the distinctive views, otherwise tucked under the menus</span></div>",
                    unsafe_allow_html=True)
        _q = st.columns(6)
        if _q[0].button("🗺️ Concept Atlas", key="qs_atlas",
                        help="The whole text as one map — 1,701 roots grouped into themes, whole-Qur'ān or per sūra."):
            st.switch_page("pages/39_Concept_Atlas.py")
        if _q[1].button("🪜 Structure Map", key="qs_struct",
                        help="The nested scales — letter → word → āyah → sūra → whole."):
            st.switch_page("pages/41_Structure_Map.py")
        if _q[2].button("🌐 Network roles", key="qs_net",
                        help="Which roots bridge themes and which anchor a family — measured."):
            st.switch_page("pages/2_Network.py")
        if _q[3].button("🫀 Correspondence", key="qs_corr",
                        help="Where the text's structure mirrors that of other designed systems."):
            st.switch_page("pages/26_Correspondence.py")
        if _q[4].button("🧠 Inner-self anatomy", key="qs_inner",
                        help="The graded states of the heart — qalb · ṣadr · fuʾād."):
            st.switch_page("pages/42_Closeup_InnerSelf.py")
        if _q[5].button("🔢 Code 19", key="qs_code19",
                        help="The 19-based claim, reviewed and measured."):
            st.switch_page("pages/31_Closeup_Code19.py")

    # ====== ROOT-EXPLORE — research entry: input bar + MEANINGFUL themed starters
    #        (the old empty-state grid of 30 random roots was patchy/confusing). ======
    st.markdown("<div style='font-size:14.5px;color:#1D3557;margin:14px 0 2px'>"
                "<b>🌱 Explore by root</b> — type or paste Arabic root(s), or start from a theme below"
                "</div>", unsafe_allow_html=True)
    run_top = render_top_input_bar(corpus, empty_samples=False)
    if not st.session_state.get("query_roots") and not st.session_state.get("prefix_top", "").strip():
        # chip_row → small, content-sized, wrapping chips (compact on desktop, wraps on mobile
        # instead of 8 full-width stacked rows). No width='stretch'.
        with chip_row("themes"):
            _tc = st.columns(len(SAMPLE_QUERIES))
            for _i, (_lab, _rts) in enumerate(SAMPLE_QUERIES.items()):
                if _tc[_i].button(_lab, key=f"theme_{_i}"):
                    _set_query(_rts); st.rerun()

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
    st.markdown(
        "<div style='font-size:13.5px;color:#10243A;line-height:1.7'>"
        "📚 Use the <b>left navigation</b>, grouped into four areas:<br>"
        "<b>🔭 Explore</b> — Read · Search; Per-Root Profile · Concept Deep-Dive · Network · Motifs; "
        "Compare &amp; Heatmaps · Topic Modeling · My Topics · Calibration; Morphology · Surface Divergence; "
        "Reading Guide · Practical Lens · Statistics.<br>"
        "<b>💡 Discover</b> — Discovery Map · <b>Concept Atlas</b> · <b>Structure Map</b> · Latent Features · "
        "Correspondence; Structural units (Closeup Index · the Āyah · the Sūra · Inter-Sūra); "
        "Patterns &amp; roles (Importance as roles · Mathani · Structural Twins); Claims Reviewed (Code 19 · "
        "Word-count miracle · Revelation order).<br>"
        "<b>🧪 Methods · Lab</b> — Lens Lab · Two Books; Computational lenses (Disjoint Letters · Spatial Patterns · "
        "Signal · Biology).<br>"
        "<b>🛠️ Tools</b> — Export · Feedback · Help."
        "</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
