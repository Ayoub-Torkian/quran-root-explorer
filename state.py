# re-deploy 1779770521
"""state.py — v4: simple, bright, always-visible menu."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

import analysis as A


HERE = Path(__file__).resolve().parent
# Try multiple capitalizations so the same code works on case-sensitive
# Linux (HF Spaces, Render) and case-insensitive Windows.
DEFAULT_XLSX = None
for candidate in ("book6.xlsx", "Book6.xlsx", "BOOK6.xlsx",
                  "book5.xlsx", "Book5.xlsx"):
    _p = HERE / candidate
    if _p.exists():
        DEFAULT_XLSX = _p
        break
if DEFAULT_XLSX is None:
    DEFAULT_XLSX = HERE / "book6.xlsx"  # fall through to original error path

# Bump this string any time analysis.normalize_letters / index-building logic
# changes so cached corpora are automatically rebuilt.
NORMALIZE_VERSION = "v4-full-unicode-fold-2026-05"


# v2.0 RE-SPINE (APP_PLAN.md): primary axis = READER + the three SCALES
# (🧭 Position · 🔤 Sequence · 🧩 Semantic) + LENS LAB; Tools/Feedback cross-cutting.
# Old build-history groups (EXPLORE / DEEP DIVES / TWO BOOKS) retired; every page
# now sits under the question it answers (UI_REORG_NOTES: consolidate by QUESTION).
NAV_SECTIONS = [
    (None, [(None, [("app.py", "Home", "🏠")])]),
    ("🔭 EXPLORE", [
        (None, [("pages/40_Read.py", "Read the Qur'an", "📖"),
                ("pages/38_Search.py", "Search", "🔎")]),
        ("Study an āyah", [
            ("pages/4_Ayah_Browser.py", "Matched Āyāt", "📑"),
            ("pages/20_Ayah_Deep_Dive.py", "Āyah Deep-Dive", "🔭"),
            ("pages/36_Cross_References.py", "Cross-References", "🔗"),
        ]),
        ("Roots & relations", [
            ("pages/1_Per_Root_Profile.py", "Per-Root Profile", "🔍"),
            ("pages/19_Concept_Deep_Dive.py", "Concept Deep-Dive", "🔬"),
            ("pages/2_Network.py", "Network", "🌐"),
            ("pages/3_Motifs.py", "Motifs", "🔺"),
            ("pages/5_Compare_Heatmaps.py", "Compare & Heatmaps", "📊"),
            ("pages/9_Topic_Modeling.py", "Topic Modeling", "🧩"),
            ("pages/8c_My_Topics.py", "My Topics", "📌"),
            ("pages/8e_Calibration.py", "Calibration", "🎚️"),
        ]),
        ("Morphology & interpret", [
            ("pages/6_Morphology.py", "Morphology", "🧬"),
            ("pages/8d_Surface_Divergence.py", "Surface Divergence", "🔀"),
            ("pages/8a_Interpret.py", "Interpret", "🧠"),
            ("pages/8f_Practical_Lens.py", "Practical Lens", "🔭"),
        ]),
    ]),
    ("💡 DISCOVER", [
        (None, [("pages/37_Discovery_Map.py", "Discovery Map · start here", "🧭"),
                ("pages/39_Concept_Atlas.py", "Concept Atlas · the concepts", "🗺️"),
                ("pages/41_Structure_Map.py", "Structure Map · the scales", "🪜"),
                ("pages/25_Latent_Features.py", "Latent Features", "🧬"),
                ("pages/26_Correspondence.py", "Correspondence", "🫀")]),
        ("Close-up essays", [
            ("pages/27_Closeup_Index.py", "Map · close-ups", "🗺️"),
            ("pages/28_Closeup_Ayah.py", "The Āyah", "📐"),
            ("pages/30_Closeup_Sura.py", "The Sūra", "📜"),
            ("pages/29_Closeup_InterSura.py", "Inter-Sūra", "⚠️"),
            ("pages/34_Closeup_Importance.py", "Importance as roles", "🕸️"),
            ("pages/35_Mathani_Lab.py", "Mathānī · refrains", "🔁"),
            ("pages/23_Structural_Twins.py", "Structural Twins", "♊"),
        ]),
        ("Claims reviewed", [
            ("pages/31_Closeup_Code19.py", "Code 19", "🔢"),
            ("pages/33_Closeup_Adadi.py", "Word-count miracle", "🧮"),
            ("pages/32_Closeup_Nuzul.py", "Revelation order", "🕰️"),
        ]),
    ]),
    ("🧪 METHODS · LAB", [
        (None, [
            ("pages/22_Lens_Lab.py", "18 Lenses · Verdicts", "🧪"),
            ("pages/24_Two_Books_Genome.py", "Two Books · Genome", "🧬"),
            ("pages/17_Two_Books_Summary.py", "Two Books · FDR Summary", "📋"),
        ]),
        ("Scale lenses", [
            ("pages/14_Disjoint_Letters.py", "Disjoint Letters", "🔠"),
            ("pages/18_Spatial_Patterns.py", "Spatial Patterns", "🗺️"),
            ("pages/15_Signal.py", "Signal", "📡"),
            ("pages/16_Biology.py", "Biology", "🧬"),
        ]),
    ]),
    ("🛠️ TOOLS", [
        (None, [
            ("pages/7_Statistics.py", "Statistics", "📈"),
            ("pages/8_Export.py", "Export", "⬇️"),
            ("pages/9_Usage.py", "Usage", "📊"),
            ("pages/21_Feedback_and_Bugs.py", "Feedback & Bugs", "🐞"),
            ("pages/0_Help.py", "Help", "❓"),
        ]),
    ]),
]


def _nav_is_current(path):
    """True if `path` is the page currently executing (matches a file in the call
    stack). Reliable across Streamlit versions; no dependency on DOM markup."""
    import os, inspect
    try:
        bases = {os.path.basename(p) for p in (path if isinstance(path, (list, tuple)) else [path])}
        for fr in inspect.stack():
            if os.path.basename(fr.filename) in bases:
                return True
    except Exception:
        pass
    return False


def render_grouped_nav():
    """Two-level grouped sidebar nav (L1 category → L2 sub-group → page links).
    Version-safe: if st.page_link is missing (<1.31) the default nav stays."""
    if not hasattr(st, "page_link"):
        return
    if not _once_per_run("nav"):
        return
    st.markdown(
        "<style>"
        # VERIFIED LIVE against the rendered DOM (overlap measured in px, not
        # eyeballed). Two root causes defeated every earlier attempt:
        #  (1) the negative margin lived on [data-testid=stElementContainer]
        #      (NOT stPageLink) — it pulled each card up onto its neighbour;
        #  (2) the L1/L2 header markdown OVERFLOWS its auto-sized container, so
        #      the next card began ABOVE the header text => masking.
        # FIX (structural, once and for all): zero the container margins; use ONE
        # small gap as the only row-spacing lever; and give the header containers
        # a real min-height via :has() so a label can never overflow into a card.
        "[data-testid='stSidebarNav']{display:none!important;}"
        "section[data-testid='stSidebar'] [data-testid='stElementContainer']{margin:0!important;}"
        # ROOT CAUSE of the nav overlap (confirmed via live DOM): Streamlit puts margin-bottom:-16px
        # on stMarkdownContainer, collapsing the label's box so the next link overlaps it. Zero it.
        "section[data-testid='stSidebar'] [data-testid='stMarkdownContainer']{margin:0!important;}"
        "section[data-testid='stSidebar'] div[data-testid='stVerticalBlock']{gap:0.45rem!important;}"
        "section[data-testid='stSidebar'] [data-testid='stPageLink']{margin:0!important;}"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a{"
        "border:0!important;border-radius:6px!important;"
        "background:transparent!important;padding:2px 9px 2px 18px!important;margin:0!important;"
        "line-height:1.3!important;box-shadow:none!important;}"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a:hover{"
        "background:#EEF3FB!important;}"
        # CONTRAST (user mandate: no gray text) — nav links in full navy, real weight
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a,"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a span,"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a p{"
        "color:#16365C!important;font-weight:600!important;font-size:14px!important;}"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a:hover,"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a:hover span{"
        "color:#0F6E56!important;}"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page']{"
        "background:#1D3557!important;box-shadow:inset 4px 0 0 0 #1D9E75!important;}"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page'],"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page'] span,"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page'] p{"
        "color:#FFFFFF!important;font-weight:700!important;}"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page']:hover{"
        "background:#22406A!important;}"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page']:hover span,"
        "section[data-testid='stSidebar'] [data-testid='stPageLink'] a[aria-current='page']:hover p{"
        "color:#FFFFFF!important;}"
        # SIDEBAR NAV — layout-driven, once and for all: every nav container auto-sizes to its
        # content and never clips (kills overlap), with ONE uniform flex gap (kills stray empty
        # space). No per-item min-height magic numbers — those were the cause of the back-and-forth.
        "section[data-testid='stSidebar'] [data-testid='stElementContainer']"
        "{min-height:0!important;height:auto!important;overflow:visible!important;margin:0!important;}"
        "section[data-testid='stSidebar'] [data-testid='stElementContainer']:empty{display:none!important;}"
        ".dlnav-active{background:#1D3557!important;color:#FFFFFF!important;font-weight:800!important;"
        "font-size:14px!important;border-radius:6px!important;padding:4px 9px 4px 14px!important;"
        "border-left:4px solid #1D9E75!important;margin:0!important;line-height:1.3!important;"
        "display:block!important;white-space:nowrap!important;overflow:hidden!important;"
        "text-overflow:ellipsis!important;}"
        ".dlnav-h1{font-size:12px!important;font-weight:700!important;letter-spacing:1px!important;"
        "color:#FFFFFF!important;text-transform:uppercase!important;background:#1D3557!important;"
        "border-radius:6px!important;padding:5px 10px!important;margin:6px 0 0!important;"
        "line-height:1.2!important;display:block!important;white-space:nowrap!important;"
        "overflow:hidden!important;text-overflow:ellipsis!important;}"
        ".dlnav-h2{font-size:12px!important;font-weight:800!important;letter-spacing:.6px!important;"
        "color:#10243A!important;text-transform:uppercase!important;margin:10px 0 2px 12px!important;"
        "background:none!important;border:none!important;padding:0 0 2px 6px!important;"
        "border-left:3px solid #C7D3E2!important;line-height:1.3!important;display:block!important;}"
        # v2.0: global PROGRESS RIBBON — animated bar pinned to the very top whenever the app
        # is computing (driven by the presence of Streamlit's status widget via :has()).
        "@keyframes dlribbon{0%{background-position:0 0}100%{background-position:300% 0}}"
        ".stApp:has(div[data-testid='stStatusWidget'])::before{content:'';position:fixed;"
        "top:0;left:0;right:0;height:5px;z-index:999999;"
        "background:linear-gradient(90deg,#E63946,#F77F00,#06AED5,#2A9D8F,#E63946);"
        "background-size:300% 100%;animation:dlribbon 1.1s linear infinite;}"
        ".stApp:has(div[data-testid='stStatusWidget'])::after{content:'⏳ computing…';"
        "position:fixed;top:7px;right:14px;z-index:999999;font-size:12px;font-weight:700;"
        "color:#fff;background:#1D3557;border-radius:10px;padding:2px 10px;opacity:.92;}"
        # COMPACT accordion: tighten the sidebar expanders (category 'ribbon tabs')
        "section[data-testid='stSidebar'] [data-testid='stExpander']{margin:1px 0!important;}"
        "section[data-testid='stSidebar'] [data-testid='stExpander'] details{"
        "border:1px solid #E3E9F0!important;border-radius:7px!important;background:#fff!important;}"
        "section[data-testid='stSidebar'] [data-testid='stExpander'] summary{"
        "padding:3px 9px!important;min-height:0!important;font-size:12.5px!important;"
        "font-weight:700!important;color:#1D3557!important;}"
        "section[data-testid='stSidebar'] [data-testid='stExpander'] summary p{"
        "font-size:12.5px!important;font-weight:700!important;}"
        "section[data-testid='stSidebar'] [data-testid='stExpander'] summary svg{height:14px;width:14px;}"
        "section[data-testid='stSidebar'] [data-testid='stExpander'] details>div{padding:2px 6px 4px!important;}"
        "</style>",
        unsafe_allow_html=True,
    )
    # Every category collapses like Word's ribbon tabs (Findings included, for consistency);
    # only the Home/NAVIGATION group stays always visible.
    ALWAYS_OPEN = {None}
    use_accordion = hasattr(st, "expander")
    with st.sidebar:
        def _render_items(subs):
            for l2, items in subs:
                if l2:
                    st.markdown(f"<div class='dlnav-h2'>{l2}</div>", unsafe_allow_html=True)
                for path, label, icon in items:
                    # Every item is the SAME st.page_link — the current page is auto-highlighted by
                    # Streamlit via a[aria-current='page'] (styled above). No custom taller element,
                    # so overlap/masking is structurally impossible. (Settled — do not reintroduce a
                    # bespoke active <div>.)
                    for _p in (path if isinstance(path, (list, tuple)) else [path]):
                        try:
                            st.page_link(_p, label=label, icon=icon)
                            break
                        except Exception:
                            continue

        for l1, subs in NAV_SECTIONS:
            if (l1 in ALWAYS_OPEN) or not use_accordion:
                if l1:
                    st.markdown(f"<div class='dlnav-h1'>{l1}</div>", unsafe_allow_html=True)
                _render_items(subs)
            else:
                with st.expander(l1, expanded=(l1 == "🧭 MAIN") or any(_nav_is_current(_pp) for _l2, _it in subs for _pp, _lb, _ic in _it)):
                    _render_items(subs)
        # Persistent resources link — papers · presentations · courses (every page, below the nav).
        # Native st.link_button: avoids the anchor-colour / HTML-sanitizer issues entirely.
        _resurl = "https://drive.google.com/drive/folders/1Iz34p_uD7tAL7To8HaVGPFoCJYpp3fPc"
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        try:
            st.link_button("📚 Papers · presentations · courses", _resurl,
                           width='stretch', type="primary")
        except Exception:
            try:
                st.link_button("📚 Papers · presentations · courses", _resurl)
            except Exception:
                st.markdown(f"[📚 Papers · presentations · courses]({_resurl})")
        # v2.1: per-page feedback widgets removed (Feedback page stays in the nav)


def inject_css():
    st.markdown("""
    <style>
    /* ===== APP BACKGROUND ===== */
    .stApp { background: #FAFBFD; }
    .main .block-container { padding-top: 1.6rem; padding-bottom: 4rem; max-width: 1400px; }

    /* ===== v2.0 GLOBAL READABILITY + SPACE-EFFICIENCY SWEEP (user-mandated) =====
       Goals: no dead vertical space, nothing below 13px, higher contrast for
       secondary text, tighter rhythm — applies to EVERY page from this one file. */
    section[data-testid="stMain"] .block-container {
        padding-top: 1.0rem !important; padding-bottom: 1.6rem !important;
        max-width: 1500px !important;
    }
    section[data-testid="stMain"] div[data-testid="stVerticalBlock"] { gap: 0.55rem !important; }
    section[data-testid="stMain"] hr { margin: 0.5rem 0 !important; }
    section[data-testid="stMain"] h1 { margin: 0.1rem 0 0.4rem !important; font-size: 30px !important; }
    section[data-testid="stMain"] h2 { margin: 0.4rem 0 0.3rem !important; font-size: 23px !important; }
    section[data-testid="stMain"] h3 { margin: 0.35rem 0 0.25rem !important; font-size: 19px !important; }
    section[data-testid="stMain"] [data-testid="stCaptionContainer"],
    section[data-testid="stMain"] [data-testid="stCaptionContainer"] * {
        font-size: 13.5px !important; color: #10243A !important; line-height: 1.45 !important;
    }
    section[data-testid="stMain"] [data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #E2E8F1; border-radius: 10px;
        padding: 6px 10px !important;
    }
    section[data-testid="stMain"] [data-testid="stMetricLabel"] p { font-size: 13px !important; }
    section[data-testid="stMain"] [data-testid="stMetricValue"] { font-size: 23px !important; }
    section[data-testid="stMain"] [data-testid="stMetricDelta"] { font-size: 13px !important; }
    section[data-testid="stMain"] [data-testid="stExpander"] details {
        border-radius: 10px !important;
    }
    section[data-testid="stMain"] [data-testid="stExpander"] summary {
        padding: 0.45rem 0.8rem !important; font-size: 14.5px !important;
    }
    section[data-testid="stMain"] .stPlotlyChart { margin: 0 !important; }
    section[data-testid="stMain"] [data-testid="stDataFrame"] { margin: 0.1rem 0 !important; }
    section[data-testid="stMain"] .stMarkdown p { line-height: 1.5; margin-bottom: 0.45rem; }
    section[data-testid="stMain"] .stButton button { padding: 0.3rem 0.9rem !important; }
    section[data-testid="stMain"] [data-testid="stRadio"] { margin-bottom: 0 !important; }
    section[data-testid="stMain"] [data-testid="stSelectbox"] label,
    section[data-testid="stMain"] [data-testid="stMultiSelect"] label,
    section[data-testid="stMain"] [data-testid="stSlider"] label {
        font-size: 13.5px !important; color: #10243A !important;
    }
    section[data-testid="stMain"] [data-testid="stAlert"] { padding: 0.5rem 0.9rem !important; }
    /* ===== CONTRAST SWEEP (user mandate: gray only masks readability) ===== */
    section[data-testid="stMain"] .stMarkdown,
    section[data-testid="stMain"] .stMarkdown p,
    section[data-testid="stMain"] .stMarkdown li { color: #10243A; }
    .stButton button:not([kind="primary"]) {
        color: #16365C !important; font-weight: 600 !important;
        background: #FFFFFF !important; border: 1px solid #C9D6E8 !important;
    }
    .stButton button:not([kind="primary"]):hover {
        border-color: #1D9E75 !important; color: #0F6E56 !important;
    }
    input::placeholder, textarea::placeholder { color: #10243A !important; opacity: 1 !important; }
    section[data-testid="stMain"] [data-testid="stWidgetLabel"] p { color: #10243A !important; }
    /* ===== ONE progress language app-wide (v2.0): slim ribbon + pill only ===== */
    div[data-testid="stStatusWidget"] { visibility: hidden !important; }
    @keyframes dlribbon2 { 0% {background-position:0 0} 100% {background-position:300% 0} }
    .stApp:has(div[data-testid="stStatusWidget"])::before {
        content:''; position:fixed; top:0; left:0; right:0; height:5px; z-index:999999;
        background:linear-gradient(90deg,#E63946,#EF9F27,#1D9E75,#378ADD,#E63946);
        background-size:300% 100%; animation:dlribbon2 1.1s linear infinite;
    }
    .stApp:has(div[data-testid="stStatusWidget"])::after {
        content:'⏳ computing…'; position:fixed; top:9px; right:14px; z-index:999999;
        font-size:12px; font-weight:700; color:#FFFFFF; background:#1D3557;
        border-radius:10px; padding:2px 10px;
    }
    /* st.progress bars join the same language: teal fill, slim track */
    [data-testid="stProgress"] div[role="progressbar"] > div,
    .stProgress > div > div > div > div { background-color: #1D9E75 !important; }
    [data-testid="stProgress"] { margin: 0.2rem 0 !important; }
    /* Inputs: WHITE, bordered, teal focus — no gray fields, no red focus ring */
    section[data-testid="stMain"] [data-testid="stTextInput"] input,
    section[data-testid="stMain"] [data-testid="stTextArea"] textarea,
    section[data-testid="stMain"] [data-testid="stNumberInput"] input {
        background: #FFFFFF !important;
        border: 1.5px solid #C9D6E8 !important;
        border-radius: 9px !important;
        color: #10243A !important;
    }
    section[data-testid="stMain"] [data-testid="stTextInput"] div[data-baseweb="input"],
    section[data-testid="stMain"] [data-testid="stTextArea"] div[data-baseweb="textarea"] {
        background: #FFFFFF !important; border-color: transparent !important;
    }
    section[data-testid="stMain"] [data-testid="stTextInput"] input:focus,
    section[data-testid="stMain"] [data-testid="stTextArea"] textarea:focus {
        border-color: #1D9E75 !important;
        box-shadow: 0 0 0 2px rgba(29, 158, 117, 0.25) !important;
    }

    /* ===== SIDEBAR: WIDER, WHITE, CLEAN ===== */
    [data-testid="stSidebar"] {
        background: #FFFFFF;
        min-width: 260px !important;
        max-width: 260px !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.5rem;
    }

    /* ===== SIDEBAR PAGE NAV — ALWAYS VISIBLE, BIG, READABLE ===== */
    [data-testid="stSidebarNav"] {
        background: #EEF3FB;
        border: 2px solid #E2E8F1;
        border-radius: 14px;
        padding: 6px 6px 8px 6px;
        margin: 0 2px 10px 2px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    [data-testid="stSidebarNav"]::before {
        content: "📚  PAGES";
        display: block;
        color: #1D3557;
        font-size: 12px !important;
        font-weight: 700;
        letter-spacing: 1.2px;
        padding: 4px 8px 6px 8px;
        border-bottom: 1px solid #E2E8F1;
        margin-bottom: 4px;
        text-align: center;
    }
    [data-testid="stSidebarNav"] ul { padding: 0 !important; margin: 0 !important; }
    [data-testid="stSidebarNav"] li { list-style: none !important; }
    [data-testid="stSidebarNav"] li a,
    [data-testid="stSidebarNav"] li a span {
        display: block !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        color: #1D3557 !important;
        text-decoration: none !important;
    }
    [data-testid="stSidebarNav"] li a {
        background: #FFFFFF !important;
        padding: 7px 10px !important;
        margin: 2px 0 !important;
        border-radius: 9px !important;
        border-left: 5px solid #1D9E75 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        transition: all 0.15s ease;
    }
    [data-testid="stSidebarNav"] li a:hover,
    [data-testid="stSidebarNav"] li a:hover span {
        background: #EEF3FB !important;
        color: #16365C !important;
        border-left-color: #1D3557 !important;
        transform: translateX(2px);
    }
    [data-testid="stSidebarNav"] li a[aria-current="page"],
    [data-testid="stSidebarNav"] li a[aria-current="page"] span {
        background: #1D3557 !important;
        color: #FFFFFF !important;
        border-left: none !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* ===== SIDEBAR HEADERS / LABELS ===== */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #1D3557;
        font-size: 15px !important;
        font-weight: 700 !important;
        margin: 14px 0 6px 0 !important;
        padding: 4px 8px;
        background: #EEF3FB;
        border-radius: 6px;
        border-left: 4px solid #1D3557;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] label {
        font-size: 13px !important;
        color: #10243A !important;
    }
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        font-size: 12px !important;
        color: #10243A !important;
    }

    /* ===== HERO BANNER ===== */
    .hero-banner {
      background: #1D3557;
      color: white; padding: 10px 20px; border-radius: 12px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.06);
      margin-bottom: 10px;
    }
    .hero-banner h1 { color: white !important; margin: 0; font-weight: 700; font-size: 17px !important; }
    .hero-banner p  { color: rgba(255,255,255,0.94); margin: 2px 0 0; font-size: 13px; }
    [data-testid="stMetricValue"] { color: #1D3557; font-weight: 700; font-size: 23px !important; }
    [data-testid="stMetricLabel"] { font-weight: 700; font-size: 12px !important; color: #1D3557 !important; }
    [data-testid="stMetric"] { padding: 6px 8px !important; }

    /* ===== QURANIC DIACRITIZED TEXT ===== */
    .quranic-verse {
        direction: rtl; text-align: center;
        font-family: 'Amiri Quran', 'Amiri', 'Scheherazade New', 'Noto Naskh Arabic',
                     'Traditional Arabic', serif;
        font-size: 26px; line-height: 2.1;
        color: #10243A;
        background: #EEF3FB;
        border: 1px solid #E2E8F1;
        border-left: 4px solid #1D3557;
        border-radius: 12px;
        padding: 18px 24px; margin: 12px 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .ayah-meta {
        font-size: 12px; color: #10243A; text-align: center;
        margin-top: -6px; margin-bottom: 12px;
        letter-spacing: 0.5px;
    }
    .arabic-text { direction: rtl; text-align: right; font-size: 19px;
                   font-family: 'Amiri', 'Noto Naskh Arabic', serif;
                   line-height: 1.9; }
    mark.hit { background: #1D9E75; color: #FFFFFF; padding: 0 4px;
               border-radius: 4px; font-weight: bold; }

    /* ===== LAYER LABELS ===== */
    .layer-label {
        display: inline-block; background: #1D3557; color: white;
        padding: 5px 16px; border-radius: 14px; font-size: 13px;
        font-weight: 700; margin: 10px 0 10px 0; letter-spacing: 0.8px;
        text-transform: uppercase;
    }

    /* ===== PILLS ===== */
    .pill { display:inline-block; padding:4px 14px; border-radius:14px;
            font-size:13px; font-weight:700; margin: 2px 4px 2px 0; }
    .pill-input { background: #1D3557; color:white; }
    .pill-rare { background: #378ADD; color:white; }
    .pill-common { background: #1D9E75; color:white; }
    .pill-ubiq { background: #EF9F27; color:#FFFFFF; }

    /* ===== TOP TABS — BIG, ALWAYS-VISIBLE ===== */
    [data-baseweb="tab-list"] {
        gap: 6px !important;
        background: #EEF3FB !important;
        padding: 8px !important;
        border-radius: 14px !important;
        margin-bottom: 14px;
    }
    [data-baseweb="tab"] {
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 11px 22px !important;
        border-radius: 10px !important;
        background: white !important;
        color: #1D3557 !important;
        border: 2px solid #E2E8F1 !important;
    }
    [data-baseweb="tab"]:hover {
        background: #EEF3FB !important;
        color: #16365C !important;
        border-color: #C9D6E8 !important;
    }
    [data-baseweb="tab"][aria-selected="true"] {
        background: #1D3557 !important;
        color: white !important;
        border-color: #1D3557 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* ===== TOP INPUT — COMPACT PILL ROW ===== */
    .top-input-box {
        background: transparent;
        padding: 0;
        max-width: 480px;
        margin: 0 auto 8px auto;
        border: none;
        box-shadow: none;
    }
    .top-input-pill {
        display: inline-block;
        background: #1D3557;
        color: white;
        padding: 6px 16px;
        border-radius: 18px;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.3px;
        margin-right: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .top-input-hint {
        display: inline-block;
        color: #10243A;
        font-size: 13px;
        font-weight: 600;
    }
    .top-input-hint b { color: #1D3557; }

    /* ===== BUTTONS ===== */
    .stButton button {
        font-weight: 600;
        border-radius: 10px;
    }
    .stButton button[kind="primary"] {
        background: #1D9E75 !important;
        border: none !important;
    }

    /* ===== EXPANDERS / TABLES ===== */
    [data-testid="stExpander"] {
        border: 1px solid #E2E8F1 !important;
        border-radius: 10px !important;
        background: white !important;
        margin: 6px 0 !important;
    }
    /* GLOBAL TABLE LAYOUT — every dataframe across the app is compact AND
       flows side-by-side when there is horizontal room, so narrow tables
       stop wasting vertical space and consecutive tables share one row. */
    [data-testid="stDataFrame"],
    [data-testid="stDataFrameResizable"] {
        border-radius: 10px;
        overflow: hidden;
        max-width: 460px !important;
        display: inline-block !important;
        vertical-align: top;
        margin: 4px 10px 4px 0 !important;
    }
    /* When tables are stacked inside columns we still want them tight */
    [data-testid="stVerticalBlock"] > [data-testid="stDataFrame"] {
        margin-bottom: 8px !important;
    }
    hr { margin: 1.2rem 0 !important; opacity: 0.4; }
    /* ===== INSIGHT CALLOUTS ===== */
    .insight-card {
        background: #EEF3FB;
        border-left: 5px solid #1D3557;
        border-radius: 10px;
        padding: 14px 20px;
        margin: 10px 0;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .insight-card .icon { font-size: 22px; }
    .insight-card .headline { font-size: 15px; color: #1D3557; font-weight: 700; margin-bottom: 4px; }
    .insight-card .value { font-size: 23px; color: #1D3557; font-weight: 700; line-height: 1.2; }
    .insight-card .sub { font-size: 13px; color: #10243A; margin-top: 2px; }

    /* ===== MAIN HEADINGS — bigger ===== */
    .main h3, .main .stMarkdown h3 { font-size: 19px !important; color: #1D3557; font-weight: 700; }
    .main h4, .main .stMarkdown h4 { font-size: 17px !important; color: #1D3557; }
    /* ===== BODY ===== */
    .main p, .main .stMarkdown p { font-size: 15px; line-height: 1.55; }

    /* ===== TIGHTER LAYOUTS ===== */
    /* Reduce gap between st.columns */
    [data-testid="stHorizontalBlock"] { gap: 8px !important; }
    /* Metric cards — less padding */
    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E2E8F1;
        border-radius: 10px;
        padding: 8px 12px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    [data-testid="stMetricValue"] { line-height: 1.1 !important; }
    /* Tighter divider */
    hr { margin: 0.7rem 0 !important; opacity: 0.35; }
    /* Tighter vertical block spacing */
    .element-container { margin-bottom: 0.3rem !important; }
    /* Tighter dataframes */
    [data-testid="stDataFrame"] { margin: 4px 0; }
    /* Smaller plotly chart margins */
    .stPlotlyChart { padding: 0 !important; margin: 4px 0 !important; }
    /* Tighter expanders */
    [data-testid="stExpander"] summary { padding: 6px 12px !important; }
    [data-testid="stExpander"] > div > div { padding: 6px 12px !important; }
    /* Caption tight */
    [data-testid="stCaptionContainer"] { margin: 2px 0 !important; }
    /* st.subheader tighter */
    .main h3 { margin: 6px 0 4px 0 !important; }
    /* Buttons tight rows */
    .stButton { margin: 1px 0 !important; }
    /* Chip rows tighter */
    .pill { margin: 1px 3px 1px 0 !important; padding: 3px 11px !important; }
    /* AGGRESSIVE selectors so Streamlit's own styles can't win */
    .top-input-box input,
    .top-input-box [data-testid="stTextInput"] input,
    .top-input-box [data-testid="stTextInputRootElement"] input,
    .top-input-box .stTextInput input,
    .top-input-box [class*="TextInput"] input {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #10243A !important;
        background: #FFFFFF !important;
        border: 3px solid #1D3557 !important;
        border-top: none !important;
        border-top-left-radius: 0 !important;
        border-top-right-radius: 0 !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
        padding: 14px 18px !important;
        text-align: left !important;
        height: 64px !important;
        min-height: 64px !important;
        line-height: 1.2 !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    }
    /* Zero-gap: kill any margins/padding between the banner header and the input wrapper */
    .top-input-box,
    .top-input-box > div,
    .top-input-box [data-testid="stTextInput"],
    .top-input-box [data-testid="stTextInput"] > div,
    .top-input-box [data-testid="stTextInputRootElement"] {
        margin-top: 0 !important; padding-top: 0 !important;
        margin-bottom: 0 !important;
    }
    /* The Streamlit input wrapper itself shouldn't add a border */
    .top-input-box [data-testid="stTextInputRootElement"] {
        border: none !important;
        background: transparent !important;
    }
    .top-input-box input::placeholder,
    .top-input-box [data-testid="stTextInput"] input::placeholder {
        color: #10243A !important;
        opacity: 0.45 !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        text-align: left !important;
    }
    .top-input-box [data-testid="stTextInput"] input:focus {
        border-color: #1D9E75 !important;
        background: #FFFFFF !important;
        box-shadow: 0 0 0 3px rgba(29,158,117,0.22) !important;
    }

    .analyze-call { display:none; }  /* deprecated — was wasting vertical space */
    .analyze-call-OLD {
        background: #EEF3FB;
        border: 2px dashed #1D3557;
        border-radius: 14px;
        text-align: center;
        font-size: 17px;
        font-weight: 700;
        color: #1D3557;
        padding: 10px 14px;
        margin: 6px auto 8px auto;
        max-width: 600px;
        animation: pulseGlow 2s ease-in-out infinite alternate;
    }
    @keyframes pulseGlow {
        from { box-shadow: 0 0 0 0 rgba(29,53,87,0.20); }
        to   { box-shadow: 0 0 0 8px rgba(29,53,87,0); }
    }

    /* Hide auto-generated "app" entry at top of sidebar nav (redundant) */
    [data-testid="stSidebarNav"] ul li:first-child {
        display: none !important;
    }

    /* ===== CLICKABILITY CUES ===== */
    .stButton button { cursor: pointer !important; }
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
        transition: all 0.12s ease;
    }
    /* COMPACT INPUT REGION — eliminate every wasted pixel */
    /* hero margin tighter */
    .hero-banner { margin-bottom: 2px !important; }
    /* Kill ALL element-container margins inside the home block container */
    .main .block-container > div .element-container {
        margin-bottom: 0 !important; padding-bottom: 0 !important;
        margin-top: 0 !important; padding-top: 0 !important;
    }
    /* Streamlit emits a wrapper around stMarkdown — reset it too */
    .main .block-container [data-testid="stMarkdown"] {
        margin: 0 !important; padding: 0 !important;
    }
    /* The label banner sits flush — collapse the wrapper around it */
    .main .block-container [data-testid="stMarkdown"] + [data-testid="stMarkdown"] {
        margin-top: 0 !important;
    }
    /* Empty paragraphs Streamlit sometimes inserts: hide them */
    .main .block-container p:empty { display: none !important; }
    .main .block-container div:empty { display: none !important; min-height: 0 !important; }
    /* v2.0 FACE-LIFT — one calm design language. Navy = identity, teal = go,
       red = destructive ONLY. Expanders everywhere become quiet white cards
       (the old per-column gradient rules leaked onto every page's columns). */
    .main [data-testid="stExpander"] { margin: 2px 4px 2px 0 !important; }
    .main [data-testid="stExpander"] summary {
        padding: 6px 12px !important;
        min-height: 38px !important;
        font-size: 14.5px !important;
        font-weight: 700 !important;
        border-radius: 9px !important;
        background: #FFFFFF !important;
        border: 1px solid #E2E8F1 !important;
        color: #1D3557 !important;
    }
    .main [data-testid="stExpander"] summary:hover { border-color: #1D9E75 !important; }
    .main [data-testid="stExpander"] summary p,
    .main [data-testid="stExpander"] summary span {
        font-size: 14.5px !important; font-weight: 700 !important; color: #1D3557 !important;
    }
    /* GO actions (type=primary) = teal, app-wide */
    .stButton button[kind="primary"] {
        background: #1D9E75 !important; border: 1px solid #0F6E56 !important;
        color: #FFFFFF !important; font-weight: 700 !important; border-radius: 9px !important;
    }
    .stButton button[kind="primary"]:hover { background: #0F6E56 !important; }
    /* DESTRUCTIVE start-over = quiet outline red (scoped by its column position
       next to the hero; it is the only primary button inside that 2-col strip) */
    .stButton button[kind="secondary"] { border-radius: 9px !important; }
    /* First-time banner / tip-line collapse */
    .top-input-box { margin: 0 !important; padding: 0 !important; }
    .top-input-box + div { margin-top: 0 !important; padding-top: 0 !important; }
    /* Suggestion-row gap and chip styling */
    .top-input-box ~ div [data-testid="stHorizontalBlock"] {
        gap: 2px !important; margin: 0 !important;
        line-height: 1 !important;
    }
    /* 4-pt vertical gap between the two chip rows */
    .top-input-box ~ div [data-testid="stHorizontalBlock"] + [data-testid="stHorizontalBlock"] {
        margin-top: 4px !important;
    }
    /* 4-pt vertical gap between the input row and the suggestions header */
    .top-input-box + div, .top-input-box ~ [data-testid="stMarkdown"]:first-of-type {
        margin-top: 4px !important;
    }
    .top-input-box ~ div .element-container { margin: 0 !important; padding: 0 !important; }
    .top-input-box ~ div .stButton { margin: 0 !important; padding: 0 !important; }
    /* Condensed chips — 20 per row, line-height 1, very tight */
    .top-input-box ~ div .stButton button {
        font-size: 13px !important;
        font-weight: 700 !important;
        padding: 2px 4px !important;
        min-height: 30px !important;
        height: 30px !important;
        line-height: 1 !important;
        background: #FFFFFF !important;
        color: #16365C !important;
        border: 1.5px solid #C9D6E8 !important;
        border-radius: 7px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
        letter-spacing: 0 !important;
    }
    .top-input-box ~ div .stButton button:hover {
        background: #EEF3FB !important;
        color: #0F6E56 !important;
        border-color: #1D9E75 !important;
        transform: translateY(-1px);
        transition: all 0.12s ease;
    }
    /* Reduce vertical block padding on home page */
    .main .block-container { padding-top: 0.8rem !important; }
    /* Kill the redundant "(empty)" + bottom info-callout */
        /* ===== HYPERLINK STYLING — distinguish real links from text ===== */
    .main a, .main a:link, .main a:visited {
        color: #16365C !important;
        text-decoration: underline !important;
        font-weight: 700;
    }
    .main a:hover {
        color: #1D3557 !important;
        text-decoration: underline !important;
    }
    /* ===== CONTRAST FIXES ===== */
    .layer-label {
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* Analyze button sized to match the bigger input */
    .top-input-box ~ div .stButton button[kind="primary"] {
        font-size: 19px !important;
        font-weight: 700 !important;
        height: 60px !important;
        min-height: 60px !important;
        border-radius: 12px !important;
        background: #1D9E75 !important;
        color: white !important;
        border: none !important;
        letter-spacing: 0.5px;
    }
    /* But keep suggestion chips at their compact 38px height (override the above) */
    .top-input-box ~ div div[data-testid="stHorizontalBlock"] .stButton button {
        font-size: 17px !important;
        font-weight: 700 !important;
        height: 38px !important;
        min-height: 38px !important;
        background: #FFFFFF !important;
        color: #16365C !important;
        border: 2px solid #C9D6E8 !important;
        border-radius: 9px !important;
    }

    /* ───── LANDSCAPE BANNER (portrait phones only) ───── */
    .landscape-hint { display: none; }
    @media (max-width: 700px) and (orientation: portrait) {
        .landscape-hint {
            display: block;
            background: #EEF3FB;
            border-left: 4px solid #1D3557;
            color: #1D3557;
            padding: 9px 12px;
            margin: 6px 0 10px 0;
            border-radius: 8px;
            font-weight: 700;
            font-size: 13.5px;
            text-align: center;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        }
    }
    /* ───── HORIZONTAL SCROLL FOR PLOTLY CHARTS ON SMALL SCREENS ─────
       Wraps any chart in a swipeable container so labels stop overlapping. */
    @media (max-width: 720px) {
        [data-testid="stPlotlyChart"] {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch;
        }
        [data-testid="stPlotlyChart"] > div {
            min-width: 720px !important;
        }
    }

    /* ───── MOBILE / TOUCH FRIENDLY (iPhone, iPad, Android) ───── */
    /* iOS HIG: minimum tap target is 44pt. Bump chips + button on small screens. */
    @media (max-width: 820px) {
        .top-input-box ~ div .stButton button {
            font-size: 15px !important;
            min-height: 44px !important;
            height: 44px !important;
            padding: 4px 8px !important;
            border-radius: 9px !important;
        }
        .top-input-box ~ div div[data-testid="stHorizontalBlock"] .stButton button {
            font-size: 17px !important;
            min-height: 44px !important;
            height: 44px !important;
        }
        .top-input-box ~ div .stButton button[kind="primary"] {
            font-size: 19px !important;
            min-height: 56px !important;
            height: 56px !important;
        }
        .top-input-box input {
            font-size: 22px !important;
            height: 56px !important;
            min-height: 56px !important;
        }
        .hero-banner h1 { font-size: 17px !important; line-height: 1.15 !important; }
        .hero-banner p  { font-size: 14px !important; }
    }
    @media (max-width: 420px) {
        .top-input-box input {
            font-size: 20px !important;
            height: 52px !important;
            min-height: 52px !important;
        }
        .hero-banner h1 { font-size: 17px !important; }
    }
    </style>
    <script>
    // Stop Streamlit's bare "C" hotkey (clear cache) from intercepting
    // anything the user might type — Ctrl+C copy must keep working.
    (function() {
        if (window.__keyShimInstalled) return;
        window.__keyShimInstalled = true;
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey || e.metaKey || e.altKey) return;
            if (e.key === 'c' || e.key === 'C') {
                e.stopPropagation();
            }
        }, true);
    })();

    // ── Force big-input styling after Streamlit renders (CSS may not win) ──
    // Responsive: pick font/height based on viewport so iPhone doesn't overflow.
    (function ensureBigInput() {
        function pickSizes() {
            const w = window.innerWidth || document.documentElement.clientWidth;
            if (w < 420)  return { font: '20px', height: '52px', pad: '10px 14px' };
            if (w < 820)  return { font: '22px', height: '56px', pad: '12px 16px' };
            return { font: '28px', height: '64px', pad: '14px 18px' };
        }
        function applyStyle() {
            const root = document.querySelector('.top-input-box');
            if (!root) return false;
            const inp = root.querySelector('input');
            if (!inp) return false;
            const sz = pickSizes();
            inp.style.setProperty('font-size', sz.font, 'important');
            inp.style.setProperty('font-weight', '700', 'important');
            inp.style.setProperty('height', sz.height, 'important');
            inp.style.setProperty('min-height', sz.height, 'important');
            inp.style.setProperty('text-align', 'left', 'important');
            inp.style.setProperty('padding', sz.pad, 'important');
            inp.style.setProperty('border', '3px solid #1D3557', 'important');
            inp.style.setProperty('border-top', 'none', 'important');
            inp.style.setProperty('border-radius', '0 0 12px 12px', 'important');
            inp.style.setProperty('background', '#FFFFFF', 'important');
            inp.style.setProperty('color', '#10243A', 'important');
            // wrapper should not add its own gap
            const wrap = inp.closest('[data-testid="stTextInput"]');
            if (wrap) {
                wrap.style.setProperty('margin', '0', 'important');
                wrap.style.setProperty('padding', '0', 'important');
            }
            // Mobile keyboard hints (Arabic-friendly)
            inp.setAttribute('autocapitalize', 'off');
            inp.setAttribute('autocorrect', 'off');
            inp.setAttribute('spellcheck', 'false');
            return true;
        }
        let tries = 0;
        const iv = setInterval(function() {
            tries++;
            if (applyStyle() || tries > 60) clearInterval(iv);
        }, 200);
        window.addEventListener('resize', applyStyle);
        window.addEventListener('orientationchange', applyStyle);
    })();

    // ── Anonymous visitor ID + country (for analytics) ──
    // Sets two URL query params on first load so Python can log a country-
    // level visit count. No PII, no cookies, no third-party trackers.
    //   • vid  — random UUID stored in localStorage (stable per browser)
    //   • cc   — two-letter ISO country code (from ipapi.co, cached 7 days)
    (function visitorIdentity() {
        // Streamlit's multipage sidebar strips query params on navigation,
        // so we re-inject vid+cc from localStorage on EVERY page load if
        // the URL is missing them.  One redirect per page nav, no loop:
        // after the redirect the URL has everything localStorage has, so
        // urlMissing* are both false.
        try {
            const params = new URLSearchParams(window.location.search);

            // ── 1. Stable visitor UUID (mint if first ever visit) ──
            let vid = localStorage.getItem('qr_vid');
            if (!vid || vid.length !== 32) {
                vid = (crypto && crypto.randomUUID)
                    ? crypto.randomUUID().replace(/-/g, '')
                    : (Math.random().toString(36) + Math.random().toString(36)).replace(/[^a-z0-9]/g, '').slice(0, 32);
                localStorage.setItem('qr_vid', vid);
            }

            // ── 2. Cached country (7-day TTL) ──
            const cc      = localStorage.getItem('qr_cc');
            const ccTs    = parseInt(localStorage.getItem('qr_cc_ts') || '0', 10);
            const ccFresh = !!(cc && ccTs && (Date.now() - ccTs < 7 * 24 * 3600 * 1000));

            // ── 3. If URL is missing what we have, redirect once ──
            const urlMissingVid = (params.get('vid') !== vid);
            const urlMissingCc  = ccFresh && (params.get('cc') !== cc);
            if (urlMissingVid || urlMissingCc) {
                const p = new URLSearchParams(window.location.search);
                p.set('vid', vid);
                if (ccFresh) p.set('cc', cc);
                const newUrl = window.location.pathname + '?' + p.toString() + window.location.hash;
                // location.replace doesn't pollute the back-stack
                window.location.replace(newUrl);
                return;     // page is being replaced, stop here
            }

            // ── 4. No cached country?  Fetch it now (fire-and-forget). ──
            //   The result lands in localStorage; the NEXT page navigation
            //   will redirect with ?cc=XX attached, and Python will log it.
            if (!ccFresh) {
                fetch('https://ipapi.co/country/', { cache: 'no-store' })
                    .then(function(r){ return r.text(); })
                    .then(function(c){
                        c = (c || '').trim().toUpperCase();
                        if (c.length === 2 && /^[A-Z]{2}$/.test(c)) {
                            localStorage.setItem('qr_cc', c);
                            localStorage.setItem('qr_cc_ts', String(Date.now()));
                            // Optional: also stick it on the current URL so
                            // a Streamlit rerun (e.g. clicking a button)
                            // picks it up without a full nav.
                            const p2 = new URLSearchParams(window.location.search);
                            p2.set('cc', c);
                            window.history.replaceState({}, '',
                                window.location.pathname + '?' + p2.toString() + window.location.hash);
                        }
                    })
                    .catch(function(){});
            }
        } catch (e) { /* analytics must never break the app */ }
    })();

    // ── Per-keystroke autocomplete shim ──
    // Streamlit's text_input only commits on Enter or blur.  On desktop we
    // hook the input element and force a blur + refocus 250 ms after the
    // last keystroke so suggestions update as the user types — no Enter.
    //
    // CRITICAL: On touch devices (iPhone, iPad, Android) blur dismisses the
    // soft keyboard, which makes typing impossible.  We detect touch devices
    // and skip the shim entirely — those users press Enter / Go on the
    // soft keyboard to commit, which is the iOS-native pattern anyway.
    (function installPerKeyShim() {
        const isTouchDevice = ('ontouchstart' in window) ||
                              (navigator.maxTouchPoints > 0) ||
                              (navigator.msMaxTouchPoints > 0);
        if (isTouchDevice) return;   // ← iOS / Android safety
        function findInputAndAttach() {
            const root = document.querySelector('.top-input-box');
            if (!root) return false;
            const inp = root.querySelector('input');
            if (!inp || inp.__perKey) return inp ? true : false;
            inp.__perKey = true;
            let lastCommit = inp.value;
            let timer = null;
            inp.addEventListener('input', function() {
                if (inp.value === lastCommit) return;
                clearTimeout(timer);
                timer = setTimeout(function() {
                    if (inp.value === lastCommit) return;
                    lastCommit = inp.value;
                    // Force Streamlit to commit by blurring then refocusing.
                    inp.blur();
                    setTimeout(function() { inp.focus(); }, 30);
                }, 250);
            });
            return true;
        }
        // Streamlit re-renders frequently; keep retrying until we attach.
        let tries = 0;
        const iv = setInterval(function() {
            tries++;
            if (findInputAndAttach() || tries > 40) clearInterval(iv);
        }, 200);
    })();

    // ── Sticky animated progress ribbon at the very top of the page ──
    // Visible whenever Streamlit is rendering/running anything.
    (function topProgressRibbon() {
        // v2.0 slim design: 5px animated bar + small pill, VISIBLE ONLY WHILE RUNNING.
        if (window.__tprInstalled) return;
        window.__tprInstalled = true;
        const bar = document.createElement('div');
        bar.id = '__tprBar';
        bar.style.cssText = 'position:fixed;top:0;left:0;right:0;height:5px;'
            + 'z-index:2147483647;display:none;pointer-events:none;'
            + 'background:linear-gradient(90deg,#E63946,#EF9F27,#1D9E75,#378ADD,#E63946);'
            + 'background-size:300% 100%;animation:tprShine 1.1s linear infinite;';
        const pill = document.createElement('div');
        pill.id = '__tprPill';
        pill.textContent = '⏳ computing…';
        pill.style.cssText = 'position:fixed;top:9px;right:14px;z-index:2147483647;'
            + 'display:none;pointer-events:none;font-size:12px;font-weight:700;'
            + 'color:#FFFFFF;background:#1D3557;border-radius:10px;padding:2px 10px;';
        (document.documentElement || document.body).appendChild(bar);
        (document.documentElement || document.body).appendChild(pill);
        const style = document.createElement('style');
        style.textContent = '@keyframes tprShine{0%{background-position:0 0;}'
            + '100%{background-position:300% 0;}}';
        document.head.appendChild(style);
        function check() {
            // PRESENCE of the status widget = running (Streamlit removes it when idle);
            // spinners and progress bars count too. No text matching (locale-proof).
            let running = !!document.querySelector('[data-testid="stStatusWidget"]');
            if (!running && document.querySelectorAll('.stSpinner').length > 0) running = true;
            if (!running && document.querySelector('[data-testid="stProgress"]')) running = true;
            bar.style.display = running ? 'block' : 'none';
            pill.style.display = running ? 'block' : 'none';
        }
        check();
        setInterval(check, 250);
    })();
    </script>
    """, unsafe_allow_html=True)


def hero(title, subtitle=""):
    # Single-line hero. No multi-line, no wasted vertical space.
    sub = (f" <span style='font-weight:500;color:rgba(255,255,255,0.85);font-size:13.5px;'>· {subtitle}</span>"
           if subtitle else "")
    st.markdown(
        f"<div style='background:#1D3557;color:#FFFFFF;padding:7px 16px;"
        f"border-radius:10px;margin:0 0 6px 0;font-size:17px;font-weight:700;"
        f"letter-spacing:0.2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;'>"
        f"{title}{sub}</div>",
        unsafe_allow_html=True,
    )


def reader_play_handoff():
    """Shared '▶ play in Reader' hand-off. Any page that shows āyāt can offer a link
    `<a href='?play=S:A'>▶</a>`; calling this near the top routes that click to the Read
    page at the āyah with autoplay. Read is the single recitation home, so analytic/result
    surfaces (Search, Matched Āyāt, …) hand off rather than embed a second player."""
    pl = st.query_params.get("play")
    if not pl:
        return
    import re as _re
    m = _re.match(r"^(\d+):(\d+)$", str(pl))
    if not m:
        return
    st.session_state["read_s"] = int(m.group(1))
    st.session_state["read_a"] = int(m.group(2))
    st.session_state["read_s_prev"] = int(m.group(1))
    st.session_state["read_autoplay"] = True
    try:
        del st.query_params["play"]
    except Exception:
        pass
    st.switch_page("pages/40_Read.py")


def play_link(surah, ayah) -> str:
    """The green ▶ 'play in Reader' affordance (HTML string) for an āyah card/row."""
    return (f"<a class='vp' href='?play={int(surah)}:{int(ayah)}' "
            f"title='Play in Reader'>▶</a>")


def layer(n, label):
    st.markdown(f"<span class='layer-label'>LAYER {n} · {label}</span>",
                unsafe_allow_html=True)

def insight(headline: str, value: str = "", sub: str = ""):
    """Big visual takeaway callout used at the top of each page/section."""
    v = f"<div class='value'>{value}</div>" if value else ""
    s = f"<div class='sub'>{sub}</div>" if sub else ""
    st.markdown(
        f"<div class='insight-card'><div class='headline'><span class='icon'>💡</span>  {headline}</div>{v}{s}</div>",
        unsafe_allow_html=True,
    )


def per_root_hint(input_roots=None, compact=False):
    """🔔 High-visibility banner reminding the user where to drill into ONE root.

    Used on the home page (large) and on every deep-dive page (compact).
    With input_roots provided AND not compact, also renders one-click jump
    buttons for each input root that navigate directly to Per Root Profile.
    """
    if compact:
        st.markdown(
            """
            <div style="background:#EEF3FB;
                        border-left:4px solid #1D3557; border-radius:10px;
                        padding:8px 14px; margin:6px 0 10px 0;
                        font-size:13.5px; color:#1D3557; line-height:1.5;">
              <b style="color:#1D3557;">👉 Want one root in full detail?</b>
              Open <b style="background:#1D3557; color:#fff; padding:1px 8px;
                            border-radius:5px;">🔍 Per Root Profile</b>
              (left sidebar) and pick the root — every input root has its own page.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    # Large pulsing callout for the home page
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
          <div style="font-size:14.5px; color:#10243A; line-height:1.6;">
            Click any per-root jump button below, or open
            <b style="background:#1D3557; color:#fff; padding:2px 10px;
                      border-radius:6px;">🔍 Per Root Profile</b>
            from the <b>left-sidebar navigation</b> — every input root has its
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

    if input_roots:
        cols = st.columns(min(len(input_roots), 6))
        for i, r in enumerate(input_roots):
            if cols[i % len(cols)].button(
                f"🔍 {r}",
                key=f"perroot_jump_{r}",
                width='stretch',
                help=f"Jump to the Per Root Profile page for '{r}'",
            ):
                st.session_state.profile_root = r
                st.switch_page("pages/1_Per_Root_Profile.py")



def render_quranic_verse(diacritized_text, surah_num=None, ayah_num=None, surah_name=None):
    if not diacritized_text:
        return
    st.markdown(f"<div class='quranic-verse'>{diacritized_text}</div>",
                unsafe_allow_html=True)
    if surah_num is not None:
        meta = f"Surah {surah_num}"
        if surah_name:
            meta += f" ({surah_name})"
        if ayah_num is not None:
            meta += f" · Ayah {ayah_num}"
        st.markdown(f"<div class='ayah-meta'>{meta}</div>", unsafe_allow_html=True)


@st.cache_resource(show_spinner="Loading corpus…")
def load(xlsx_path, _version: str = NORMALIZE_VERSION):
    # _version is part of the cache key, so bumping NORMALIZE_VERSION invalidates
    # any old cached corpus that was indexed with a different normalize_letters.
    return A.load_corpus(xlsx_path)


def get_corpus():
    if _once_per_run("corpus_sidebar"):
        inject_css()
        render_grouped_nav()
        _stages = None
        if "_app_ready" not in st.session_state:
            _stages = st.empty()
            _stages.markdown(
                '<div style="display:flex;gap:6px;margin:2px 0;flex-wrap:nowrap;font-size:13px;font-weight:700;">'
                '<span style="background:#1D9E75;color:#fff;padding:3px 10px;border-radius:6px;">✓ Booted</span>'
                '<span style="background:#1D9E75;color:#fff;padding:3px 10px;border-radius:6px;">✓ Started</span>'
                '<span style="background:#1D3557;color:#fff;padding:3px 10px;border-radius:6px;">~ Indexing...</span>'
                '<span style="background:#E2E8F1;color:#10243A;padding:3px 10px;border-radius:6px;">○ Ready</span>'
                '</div>',
                unsafe_allow_html=True,
            )
        render_start_over_button()
        default = str(DEFAULT_XLSX) if DEFAULT_XLSX.exists() else ""
        path = default  # v2.1: Data source picker removed; always use the default corpus
        st.session_state["_xlsx_path"] = path
        if not path or not Path(path).exists():
            st.warning("Set a valid path to book6.xlsx (or book5.xlsx) in the sidebar.")
            st.stop()
        c = load(path, NORMALIZE_VERSION)
        # Stages panel cleanup: mark ready, then briefly show final state, then clear
        if "_app_ready" not in st.session_state and _stages is not None:
            # Stages already complete — no value in showing them. Clear the panel.
            _stages.empty()
            st.session_state["_app_ready"] = True
        return c
    # later calls in the same run: data only, never re-draw the sidebar
    _p = st.session_state.get("_xlsx_path") or (str(DEFAULT_XLSX) if DEFAULT_XLSX.exists() else "")
    if not _p or not Path(_p).exists():
        st.warning("Set a valid path to book6.xlsx (or book5.xlsx) in the sidebar.")
        st.stop()
    return load(_p, NORMALIZE_VERSION)


def _once_per_run(key):
    """True only the first call with `key` in the current script run. Anchored on
    the per-run counter set by log_page(); if absent, never suppresses."""
    seq = st.session_state.get("_run_seq")
    if seq is None:
        return True
    if st.session_state.get("_once_" + key) == seq:
        return False
    st.session_state["_once_" + key] = seq
    return True


def corpus_data():
    """Cached corpus WITHOUT sidebar/UI side effects. Use for secondary data
    access; the sidebar is drawn once per run by get_corpus()."""
    _p = st.session_state.get("_xlsx_path")
    if not _p or not Path(_p).exists():
        _p = str(DEFAULT_XLSX) if DEFAULT_XLSX.exists() else ""
    if not _p or not Path(_p).exists():
        return get_corpus()
    return load(_p, NORMALIZE_VERSION)



@st.cache_data(show_spinner=False)
def _all_roots_sorted(corpus_id, normalize, _corpus):
    src = _corpus.index_norm.keys() if normalize else _corpus.index_exact.keys()
    return sorted(src)


def _add_root(r):
    if r and r not in st.session_state.query_roots:
        st.session_state.query_roots.append(r)
    st.session_state["_force_rerun"] = True


def _add_many(roots):
    added = 0
    for r in roots:
        if r and r not in st.session_state.query_roots:
            st.session_state.query_roots.append(r)
            added += 1
    st.session_state["_force_rerun"] = True
    return added


def _replace_with(roots):
    """Replace the entire current selection with a new set (used when user
    types/pastes new roots — old query is fully replaced)."""
    st.session_state.query_roots = list(roots)
    st.session_state["_force_rerun"] = True


def _remove_root(r):
    if r in st.session_state.query_roots:
        st.session_state.query_roots.remove(r)
    st.session_state["_force_rerun"] = True


def _prefix_expansions(p):
    """Return all prefix forms that a typed prefix should be checked against.
    Handles the Arabic surface-form → root-form mismatch where word-initial
    alef (ا) is often a written form of root hamza (ء)."""
    if not p:
        return [p]
    out = [p]
    # If first char is bare alef ا — also try with leading hamza ء
    if p[0] == "ا":
        out.append("ء" + p[1:])
    # If first char is hamza ء — also try with leading alef ا
    if p[0] == "ء":
        out.append("ا" + p[1:])
    return out


def _smart_lookup(prefix, all_roots, normalize, f2r=None):
    from analysis import strip_diacritics, normalize_letters
    p = strip_diacritics(prefix or "").strip()
    if not p:
        return [], ""
    if normalize:
        p = normalize_letters(p)
    tokens = p.split()
    aset = set(all_roots)
    if len(tokens) >= 2:
        full_matches, notes, ambigs = [], [], []
        for t in tokens:
            if t in aset:
                full_matches.append(t)
                continue
            if f2r:  # surface form? map to its root (analysis stays root-based)
                root, cands = _map_form_to_roots(t, f2r, aset)
                if root:
                    if root not in full_matches:
                        full_matches.append(root)
                    notes.append((t, root))
                elif cands:
                    ambigs.append((t, cands))
        st.session_state["_form_notes"] = notes
        st.session_state["_form_ambigs"] = ambigs
        return full_matches, "multi"
    # Try every alef↔hamza expansion of the typed prefix
    for cand in _prefix_expansions(p):
        if cand in aset:
            return [cand], "multi"
    # Single token, not a root: maybe a SURFACE FORM → map to root
    if f2r:
        root, cands = _map_form_to_roots(p, f2r, aset)
        if root:
            st.session_state["_form_notes"] = [(p, root)]
            return [root], "multi"
        if cands:
            st.session_state["_form_ambigs"] = [(p, cands)]
    matches = []
    seen = set()
    for cand in _prefix_expansions(p):
        for r in all_roots:
            if r.startswith(cand) and r not in seen:
                matches.append(r); seen.add(r)
                if len(matches) >= 12:
                    break
        if len(matches) >= 12:
            break
    return matches, "prefix"


def _random_samples(prefix, all_roots, normalize, k=20):
    """Return up to k random roots whose normalized form starts with `prefix`
    (or any roots if prefix is empty).  Deterministic per prefix so the
    sample doesn't reshuffle on every keystroke or rerun.  When the prefix
    begins with alef ا or hamza ء, both forms are tried (because Arabic
    surface ا is often the written form of root-initial hamza ء)."""
    import random
    from analysis import strip_diacritics, normalize_letters
    p = strip_diacritics(prefix or "").strip()
    if p and normalize:
        p = normalize_letters(p)
    if not p:
        pool = list(all_roots)
    else:
        seen = set()
        pool = []
        for cand in _prefix_expansions(p):
            for r in all_roots:
                if r.startswith(cand) and r not in seen:
                    pool.append(r); seen.add(r)
    if not pool:
        return []
    rng = random.Random(hash(p) ^ 0xA1B2C3)
    rng.shuffle(pool)
    return pool[:k]


@st.cache_resource(show_spinner=False)
def _form_root_index(corpus_id, _corpus):
    """form→{root:count} and root→{form:count}, built from verses where the
    segmented-surface and root token streams align 1:1 (the safe majority).
    Surface input maps to roots; ANALYSIS STAYS ROOT-BASED (NLP best practice)."""
    from analysis import normalize_letters as K
    f2r, r2f = {}, {}
    # root_tokens || surface_tokens align positionally (the surface_form_table
    # method) — verified on real corpus: 6099 forms / 1583 roots, 98 ambiguous.
    rf2ix = {}
    for i, (r_toks, s_toks) in enumerate(zip(_corpus.root_tokens, _corpus.surface_tokens)):
        for j, rt in enumerate(r_toks):
            if j >= len(s_toks):
                break
            s, r = K(str(s_toks[j])).strip(), K(str(rt)).strip()
            if not s or not r or s == r:
                continue
            f2r.setdefault(s, {}); f2r[s][r] = f2r[s].get(r, 0) + 1
            r2f.setdefault(r, {}); r2f[r][s] = r2f[r].get(s, 0) + 1
            rf2ix.setdefault((r, s), set()).add(i)
    return f2r, r2f, rf2ix


def _root_forms_tip(r2f, root, n=10):
    """Hover-tooltip text: the top surface forms of a root, with counts."""
    from analysis import normalize_letters as K
    d = r2f.get(K(root))
    if not d:
        return None
    top = sorted(d.items(), key=lambda t: -t[1])[:n]
    extra = f" (+{len(d) - n} more)" if len(d) > n else ""
    return "Surface forms: " + " · ".join(f"{f} ×{c}" for f, c in top) + extra


def _map_form_to_roots(tok, f2r, aset):
    """Resolve one typed surface form to root(s). Returns (resolved_root, candidates).
    Unambiguous = top root ≥2× the runner-up. Candidates filtered to known roots."""
    from analysis import normalize_letters as K
    d = f2r.get(K(str(tok)).strip())
    if not d:
        return None, []
    top = sorted(d.items(), key=lambda x: -x[1])
    cands = [r for r, _c in top[:4] if r in aset]
    if not cands:
        return None, []
    if len(top) == 1 or top[0][1] >= 2 * top[1][1]:
        return (top[0][0] if top[0][0] in aset else cands[0]), cands
    return None, cands


def query_controls(corpus):
    # No default-fill: a fresh session / post-reset starts EMPTY.
    if "query_roots" not in st.session_state:
        st.session_state.query_roots = []
    # Re-apply the 🔬 form scope on EVERY page (set on Home, honored everywhere)
    try:
        _sigp = st.session_state.get("_form_scope_last")
        if _sigp:
            _f2rq, _r2fq, _rf2q = _form_root_index(id(corpus), corpus)
            from analysis import normalize_letters as _Kq
            _ixq = _rf2q.get((_Kq(_sigp[0]), _sigp[1]))
            A.set_form_scope({_Kq(_sigp[0]): set(_ixq)} if _ixq else None)
        else:
            A.set_form_scope(None)
    except Exception:
        pass
    if "prefix_search" not in st.session_state:
        st.session_state.prefix_search = ""

    # Search, suggestions and paste all live in the top input bar — no duplicate
    # search panel here (it only read as redundant). The sidebar just holds the
    # current selection and the run settings.
    if st.session_state.query_roots:
        st.sidebar.markdown("**Selected roots:**")
        for r in list(st.session_state.query_roots):
            c1, c2 = st.sidebar.columns([4, 1])
            c1.markdown(f"<span class='pill pill-input'>{r}</span>",
                        unsafe_allow_html=True)
            c2.button("✕", key=f"rm_sb_{r}", on_click=_remove_root, args=(r,))
        if st.sidebar.button("🗑️ Clear all", key="clearall_sb"):
            st.session_state.query_roots = []
            st.rerun()

    st.sidebar.divider()
    # v2.1: Tolerant matching / Top partners / Min edge weight removed from sidebar -> defaults
    st.session_state["normalize"] = True
    normalize = True
    top_p = st.session_state.get("top_partners", 15)
    min_w = st.session_state.get("min_weight", 1)
    run = False  # v2.1: Analyze button removed; auto-recompute via needs_recompute()
    raw = " ".join(st.session_state.query_roots)
    return raw, normalize, top_p, min_w, run


def render_top_input_bar(corpus, empty_samples=True):
    # No default-fill: a fresh session / post-reset starts EMPTY so the user is
    # never presented with a query they didn't ask for.
    # empty_samples=False suppresses the random-root grid on EMPTY input (the caller
    # supplies its own meaningful starters); prefix-typed suggestions still show.
    if "query_roots" not in st.session_state:
        st.session_state.query_roots = []
    if "prefix_top" not in st.session_state:
        st.session_state.prefix_top = ""

    normalize_pre = st.session_state.get("normalize", False)
    all_roots = _all_roots_sorted(id(corpus), normalize_pre, corpus)

    # No label row — the hint lives INSIDE the input (zero dead vertical space)
    st.markdown("<div class='top-input-box'>", unsafe_allow_html=True)
    c1, c2 = st.columns([5, 1])
    def _on_input_change():
        # Force a fresh rerun so the suggestions panel reflects the new prefix.
        st.session_state.pop("_last_processed_top", None)

    with c1:
        st.text_input("input", key="prefix_top",
                      placeholder="🔎 Type Arabic letters to find a root — or paste a list",
                      label_visibility="collapsed",
                      on_change=_on_input_change)
    with c2:
        run_top = st.button("🚀 Analyze", key="run_top", type="primary",
                            width='stretch')
    # (Redundant affordance hint removed — the placeholder already explains usage;
    #  keeping the area clean per UI feedback.)

    # Auto-focus the input on first session load — cursor blinks immediately
    if not st.session_state.get("_autofocused"):
        st.markdown(
            """
            <script>
            setTimeout(() => {
                const doc = window.parent.document;
                const box = doc.querySelector('.top-input-box');
                if (box) {
                    const inp = box.querySelector('input');
                    if (inp) inp.focus();
                }
            }, 250);
            </script>
            """,
            unsafe_allow_html=True,
        )
        st.session_state["_autofocused"] = True

    _f2r, _r2f, _rf2ix = _form_root_index(id(corpus), corpus)

    prefix = st.session_state.prefix_top
    last_top = st.session_state.get("_last_processed_top", "")
    # Multi-token paste path — replace query immediately
    if prefix.strip() and prefix != last_top:
        matches, mode = _smart_lookup(prefix, all_roots, normalize_pre, f2r=_f2r)
        if mode == "multi" and matches:
            if list(matches) != st.session_state.query_roots:
                _replace_with(matches)
                st.session_state["_last_processed_top"] = prefix
                st.rerun()
            else:
                st.session_state["_last_processed_top"] = prefix

    # ─── Surface-form → root transparency chips (analysis stays root-based) ───
    _fn = st.session_state.pop("_form_notes", None)
    if _fn:
        st.markdown(
            "<div style='font-size:13.5px;color:#16365C;margin:2px 0;'>" + " ".join(
                f"<span style='background:#EEF3FB;border:1px solid #C9D6E8;"
                f"border-radius:6px;padding:2px 10px;margin-right:4px;"
                f"display:inline-block;'>{f} ⇒ root <b>{r}</b></span>"
                for f, r in _fn[:6])
            + " <span style='color:#10243A;'>surface form mapped — analysis is "
              "root-based (standard practice)</span></div>",
            unsafe_allow_html=True)
    _fa = st.session_state.pop("_form_ambigs", None)
    if _fa:
        for _ff, _cands in _fa[:2]:
            st.markdown(
                f"<span style='font-size:13.5px;color:#16365C;'>«{_ff}» serves "
                f"several roots — pick the one you mean:</span>",
                unsafe_allow_html=True)
            _ac = st.columns(min(len(_cands), 4))
            for _j, _rc in enumerate(_cands[:4]):
                with _ac[_j]:
                    if st.button(f"{_ff} ⇒ {_rc}", key=f"amb_{_ff}_{_rc}",
                                 help=_root_forms_tip(_r2f, _rc) or ""):
                        _add_root(_rc)
                        st.session_state["_last_processed_top"] = prefix
                        st.rerun()

    # ─── 🔬 SURFACE FORMS = CLICKABLE SCOPE CHIPS (user mandate: obvious, one gesture)
    if st.session_state.query_roots:
        from analysis import normalize_letters as _K9
        _cur = st.session_state.get("_form_scope_last")
        st.markdown(
            "<div style='font-size:13.5px;color:#16365C;margin:4px 0 0 2px;'>"
            "🔬 <b>Surface forms of your root(s)</b> — <b>click ONE form</b> to limit the "
            "entire analysis to ONLY its āyahs (the chip turns dark; click ✕ to release):"
            "</div>", unsafe_allow_html=True)
        for _qr in st.session_state.query_roots[:3]:
            _dd = _r2f.get(_K9(_qr))
            if not _dd:
                continue
            _forms = sorted(_dd.items(), key=lambda t: -t[1])  # NO cutoff
            st.markdown(f"<span style='color:#1D3557;font-size:15px;font-weight:700;'>"
                        f"{_qr}</span>", unsafe_allow_html=True)
            _ncol = 8
            for _rs in range(0, len(_forms), _ncol):
                _row = _forms[_rs:_rs + _ncol]
                _fcols = st.columns(_ncol)
                for _k, (_f9, _c9) in enumerate(_row):
                    _act = (_cur == (_qr, _f9))
                    _nay = len(_rf2ix.get((_K9(_qr), _f9), ()))
                    with _fcols[_k]:
                        if st.button(("✕ " if _act else "") + f"{_f9} ×{_c9}",
                                     key=f"fs_{_qr}_{_f9}", width='stretch',
                                     type=("primary" if _act else "secondary"),
                                     help=("SCOPED — click to release" if _act else
                                           f"analyze ONLY the {_nay} āyah(s) where "
                                           f"{_qr} appears as {_f9}")):
                            st.session_state["_form_scope_last"] = (None if _act
                                                                    else (_qr, _f9))
                            st.session_state.pop("results", None)
                            st.session_state["_force_rerun"] = True
                            st.rerun()
        _sigc = st.session_state.get("_form_scope_last")
        if _sigc:
            _ixs = _rf2ix.get((_K9(_sigc[0]), _sigc[1]))
            A.set_form_scope({_K9(_sigc[0]): set(_ixs)} if _ixs else None)
            if _ixs:
                st.markdown(
                    f"<div style='font-size:13.5px;color:#FFFFFF;background:#1D3557;"
                    f"display:inline-block;border-radius:8px;padding:3px 12px;margin:2px 0;'>"
                    f"🔬 SCOPED: root <b>{_sigc[0]}</b> as <b>{_sigc[1]}</b> — analysis runs on "
                    f"these {len(_ixs)} āyah(s) ONLY (all Root-Exploration pages)</div>",
                    unsafe_allow_html=True)
                _refs = " ".join(
                    f"{int(corpus.df.iloc[_i][A.COL_SURAH])}:{int(corpus.df.iloc[_i][A.COL_AYAH])}"
                    for _i in sorted(_ixs))
                st.session_state["_scope_refs"] = _refs
                st.caption(f"Boundary: the two Deep-Dive pages read the WHOLE corpus by design. "
                           f"To deep-dive ONLY this subset, open 🔭 Āyah Deep-Dive — the "
                           f"references are prefilled there ({_refs[:60]}"
                           f"{'…' if len(_refs) > 60 else ''}).")
        else:
            A.set_form_scope(None)
            st.session_state.pop("_scope_refs", None)
    else:
        A.set_form_scope(None)
        st.session_state.pop("_scope_refs", None)
        if st.session_state.pop("_form_scope_last", None):
            st.session_state.pop("results", None)

    # ─── ONE tight "Suggestions" panel directly under the input ─────
    # Always visible.  Empty input → 20 random roots.
    # As soon as the user types ≥1 char, the sample is filtered to roots
    # whose normalized form starts with that prefix (and reshuffled — but
    # stably, so re-running with the same prefix gives the same 20 picks).
    # Suggestions are an ENTRY aid — once root(s) are selected and the box is
    # empty, they are redundant (user mandate): hide them. They reappear the
    # moment the user types a new prefix.
    if not prefix.strip() and (not empty_samples or st.session_state.query_roots):
        samples = []                       # empty input → caller's themed starters replace random roots
    else:
        samples = _random_samples(prefix, all_roots, normalize_pre, k=30)
    if samples:
        if prefix.strip():
            _hdr = (f"«{prefix.strip()}» — {len(samples)} of "
                    f"{sum(1 for r in all_roots if r.startswith(prefix.strip()))} matches")
        else:
            _hdr = "Tap a root to start, or type to search"
        st.markdown(
            f"<div style='margin:-2px 0 1px 4px;font-size:13px;color:#1D3557;'>"
            f"{_hdr}</div>", unsafe_allow_html=True)
        # 15 columns × 2 rows of CONDENSED chips → all 30 fit in two lines
        n_cols = 15
        for row_start in range(0, len(samples), n_cols):
            row = samples[row_start:row_start + n_cols]
            scols = st.columns(len(row))
            for i, root in enumerate(row):
                with scols[i]:
                    if st.button(root, key=f"rnd_top_{root}_{row_start}",
                                 width='stretch',
                                 help=_root_forms_tip(_r2f, root)
                                      or "no aligned surface forms recorded"):
                        _add_root(root); st.rerun()

    # The input box at the top already shows what's being analysed.
    # We only render compact remove buttons when there are 2+ roots so the
    # user can drop one without retyping. Single-root queries get no extra UI.
    if len(st.session_state.query_roots) >= 2:
        cols = st.columns(min(8, len(st.session_state.query_roots)))
        for i, r in enumerate(list(st.session_state.query_roots)):
            with cols[i % len(cols)]:
                if st.button(f"✕ {r}", key=f"rm_top_{r}", width='stretch'):
                    _remove_root(r); st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    return run_top


def compute_all(corpus, raw_query, normalize, top_p, min_w):
    input_roots = A.parse_input_roots(raw_query, normalize)
    if not input_roots:
        st.error("No valid roots parsed.")
        st.stop()

    # Generic progress bar — backend computation is shared across pages, so
    # the label stays page-agnostic. Each page renders its OWN progress bar
    # for any page-specific work it does on top of this.
    _prog_holder = st.empty()
    _bar = _prog_holder.progress(0.0, text=f"Analyzing your input ({len(input_roots)} root(s))...")
    TOTAL_STEPS = 29
    _step = {"i": 0}
    def _tick(_label: str):
        _step["i"] += 1
        try:
            pct = int(round(100 * _step["i"] / TOTAL_STEPS))
            _bar.progress(min(_step["i"] / TOTAL_STEPS, 1.0),
                          text=f"Analyzing your input... {pct}%")
        except Exception:
            pass

    _tick("Finding occurrences"); occurrences = A.find_occurrences(corpus, input_roots, normalize)
    _tick("Co-occurrence search"); partners, match_ayahs = A.cooccurrence(corpus, input_roots, normalize)
    _tick("Co-occurrence table"); cooc_tbl = A.cooccurrence_table(partners)
    _tick("Surface forms"); sforms = A.surface_form_table(corpus, input_roots, normalize)
    _tick("Partner motifs"); pmotifs = A.partner_motifs(corpus, input_roots, normalize, top=20)
    _tick("Building network"); g = A.build_network(corpus, input_roots, normalize, top_partners=top_p, min_weight=min_w)
    _tick("Triad census"); triad = A.triad_census(g)
    _tick("Triangles"); tri_tbl = A.triangles_table(g)
    _tick("Summary statistics"); summary = A.summary_stats(corpus, input_roots, occurrences, partners)
    _tick("Centrality"); centrality = A.centrality_table(g)
    _tick("Communities"); communities = A.detect_communities(g)
    _tick("Surah heatmap"); heatmap = A.surah_heatmap(corpus, input_roots, normalize)
    _tick("Overlap matrix"); overlap = A.overlap_matrix(corpus, input_roots, normalize)
    _tick("Overlap by surah"); overlap_surah = A.overlap_matrix_surah(corpus, input_roots, normalize)
    _tick("Morphology"); morphology = A.morphology_breakdown(corpus, input_roots, normalize)
    _tick("Position stats"); position = A.position_stats(corpus, input_roots, normalize)
    _tick("Baseline rarity"); rarity = A.baseline_rarity(corpus, input_roots, normalize)
    _tick("First & last occurrence"); flast = A.first_last_occurrence(corpus, input_roots, normalize)
    # Enriched network attributes (positional, spatial, rhythm, lead-lag)
    _tick("Node attributes"); node_attrs = A.node_attributes(corpus, input_roots, normalize, order="mushaf")
    _tick("Edge attributes"); edge_attrs = A.edge_attributes(corpus, g, normalize)
    _tick("Spatial occurrences"); spatial = A.spatial_occurrences(corpus, input_roots, normalize, order="mushaf")
    _tick("Cumulative trajectories"); trajectories = A.cumulative_trajectories(corpus, input_roots, normalize, order="mushaf")
    _tick("Lead-lag matrix"); ll_matrix = A.lead_lag_matrix(corpus, input_roots, normalize, window=2)
    _tick("Fingerprints"); fingerprints = A.fingerprint_table(corpus, input_roots, normalize,
                                       node_attrs=node_attrs)
    _tick("Network stats"); net_stats = A.network_stats(g)
    _tick("Phase networks (Meccan/Medinan)"); g_meccan, g_medinan = A.phase_networks(corpus, input_roots, normalize,
                                           top_partners=top_p, min_weight=min_w)
    _tick("Graph diff")
    if g_meccan is not None:
        only_meccan, only_medinan, in_both = A.graph_diff(g_meccan, g_medinan)
    else:
        only_meccan, only_medinan, in_both = [], [], []
    _tick("Directed lead-lag graph"); dg_lead_lag = A.directed_lead_lag_graph(corpus, input_roots, normalize,
                                            window=2, min_strength=0.05)
    _tick("Meccan/Medinan pair matrix"); pair_phase = A.meccan_medinan_pair_matrix(corpus, input_roots, normalize)
    R = dict(
        input_roots=input_roots, normalize=normalize, raw_query=raw_query,
        top_partners=top_p, min_weight=min_w,
        occurrences=occurrences, partners=partners, cooc_tbl=cooc_tbl,
        sforms=sforms, pmotifs=pmotifs, graph=g, triad=triad,
        triangles=tri_tbl, summary=summary, match_ayahs=match_ayahs,
        centrality=centrality, communities=communities, heatmap=heatmap,
        overlap=overlap, overlap_surah=overlap_surah,
        morphology=morphology, position=position,
        rarity=rarity, first_last=flast,
        has_diacritized=corpus.has_diacritized,
        # Enriched network results
        node_attrs=node_attrs, edge_attrs=edge_attrs,
        spatial=spatial, trajectories=trajectories,
        lead_lag=ll_matrix, fingerprints=fingerprints,
        # Graph-native additions
        net_stats=net_stats,
        g_meccan=g_meccan, g_medinan=g_medinan,
        phase_only_meccan=only_meccan,
        phase_only_medinan=only_medinan,
        phase_in_both=in_both,
        dg_lead_lag=dg_lead_lag,
        pair_phase=pair_phase,
        has_rev_order=corpus.has_rev_order,
    )
    st.session_state.results = R
    try:
        _bar.progress(1.0, text="Done")
        _prog_holder.empty()
    except Exception:
        pass
    st.toast(f"Analysis complete - {len(input_roots)} root(s), {len(match_ayahs)} ayahs")
    return R




def needs_recompute() -> bool:
    """Strict: only recompute when there is NO results cache yet, or when
    something actively flipped the _force_rerun flag (user added/removed a
    root, clicked Analyze, toggled normalize). Plain page navigation never
    triggers a recompute, so going Network -> Topic Modeling -> Network
    is fast and the original computed R is preserved."""
    if "results" not in st.session_state:
        return True
    if st.session_state.pop("_force_rerun", False):
        return True
    return False


def need_results():
    if "results" not in st.session_state:
        st.info("Use the input bar at the top — add roots; results compute automatically.")
        st.stop()
    return st.session_state.results


def highlight_text(seg_text, surface_forms):
    if not seg_text:
        return ""
    toks = seg_text.split()
    sset = set(surface_forms)
    out = []
    for t in toks:
        if t in sset:
            out.append(f"<mark class='hit'>{t}</mark>")
        else:
            out.append(t)
    return "<span class='arabic-text'>" + " ".join(out) + "</span>"



def render_start_over_button():
    """Top-of-page "START OVER" button — visible on every page above the hero.
    Clears all session state and switches back to the home page (app.py)."""
    cols = st.columns([7, 2])
    with cols[1]:
        # Destructive contrast (user mandate): RED border/text. Version-proof:
        # a hidden marker in this column + :has() — no dependency on st-key classes.
        st.markdown(
            "<span class='dl-so-marker' style='display:none'></span>"
            "<style>"
            # Pull the whole row up so it stops reading as a wasted full-height band (app-wide).
            "div[data-testid='stHorizontalBlock']:has(.dl-so-marker){margin-bottom:-14px}"
            "div[data-testid='stColumn']:has(.dl-so-marker) .stButton button,"
            "div[data-testid='column']:has(.dl-so-marker) .stButton button{"
            "color:#E63946!important;border:1.5px solid #E63946!important;"
            "background:#FFFFFF!important;font-weight:700!important;"
            "font-size:13px!important;min-height:0!important;padding:2px 10px!important;}"
            "div[data-testid='stColumn']:has(.dl-so-marker) .stButton button p{"
            "color:#E63946!important;font-weight:700!important;font-size:13px!important;}"
            "div[data-testid='stColumn']:has(.dl-so-marker) .stButton button:hover,"
            "div[data-testid='column']:has(.dl-so-marker) .stButton button:hover{"
            "background:#E63946!important;color:#FFFFFF!important;"
            "border-color:#A32D2D!important;}"
            "</style>",
            unsafe_allow_html=True)
        if st.button("↺ Start over",
                     key="__start_over__",
                     width='stretch', type="secondary",
                     help="Clears your query, view state, and cache, then returns "
                          "to the home page. The most reliable way to begin fresh."):
            keys_to_clear = [
                "query_roots", "profile_root", "combined_submode",
                "prefix_top", "prefix_search", "_force_rerun",
                "_last_processed_top", "_last_processed_sb",
                "_autofocused", "results", "normalize",
                "top_partners", "min_weight",
                "kofn_slider", "show_charts", "display",
                "ayah_root_pick", "ayah_surah_pick", "ayah_search",
                "ayah_pgsize", "ayah_page", "tri_pick", "morph_pick",
                "pair_a", "pair_b", "cent_metric", "net_metric",
            ]
            for k in keys_to_clear:
                if k in st.session_state:
                    del st.session_state[k]
            try:
                st.cache_data.clear()
            except Exception:
                pass
            try:
                st.cache_resource.clear()
            except Exception:
                pass
            st.switch_page("app.py")


def render_top_nav(active="home"):
    pass


def _inject_visitor_shim():
    """Inject the visitor-identity JS via components.html so it actually
    executes.  st.markdown(unsafe_allow_html=True) silently drops <script>
    tags because the HTML is set via innerHTML — script tags added that way
    are inert per the HTML spec.  components.html renders an iframe whose
    scripts DO run; we use window.top to manipulate the parent page URL
    (same-origin, so cross-frame access is allowed)."""
    try:
        from streamlit.components.v1 import html as _components_html
        _components_html(
            """
            <script>
            (function visitorIdentity() {
                try {
                    var w = window.top || window.parent || window;
                    var ls = w.localStorage;
                    var params = new URLSearchParams(w.location.search);

                    // 1. Stable visitor UUID (mint if first ever visit)
                    var vid = ls.getItem('qr_vid');
                    if (!vid || vid.length !== 32) {
                        vid = (w.crypto && w.crypto.randomUUID)
                            ? w.crypto.randomUUID().replace(/-/g, '')
                            : (Math.random().toString(36) + Math.random().toString(36)).replace(/[^a-z0-9]/g, '').slice(0, 32);
                        ls.setItem('qr_vid', vid);
                    }

                    // 2. Cached country (7-day TTL)
                    var cc      = ls.getItem('qr_cc');
                    var ccTs    = parseInt(ls.getItem('qr_cc_ts') || '0', 10);
                    var ccFresh = !!(cc && ccTs && (Date.now() - ccTs < 7 * 24 * 3600 * 1000));

                    // 3. If parent URL is missing what we have, redirect once
                    var needVid = (params.get('vid') !== vid);
                    var needCc  = ccFresh && (params.get('cc') !== cc);
                    if (needVid || needCc) {
                        var p = new URLSearchParams(w.location.search);
                        p.set('vid', vid);
                        if (ccFresh) p.set('cc', cc);
                        w.location.replace(w.location.pathname + '?' + p.toString() + w.location.hash);
                        return;
                    }

                    // 4. Need a country?  Fetch in background — next nav picks it up.
                    if (!ccFresh) {
                        fetch('https://ipapi.co/country/', { cache: 'no-store' })
                            .then(function(r){ return r.text(); })
                            .then(function(c){
                                c = (c || '').trim().toUpperCase();
                                if (/^[A-Z]{2}$/.test(c)) {
                                    ls.setItem('qr_cc', c);
                                    ls.setItem('qr_cc_ts', String(Date.now()));
                                    var p2 = new URLSearchParams(w.location.search);
                                    p2.set('cc', c);
                                    w.history.replaceState({}, '',
                                        w.location.pathname + '?' + p2.toString() + w.location.hash);
                                }
                            })
                            .catch(function(){});
                    }
                } catch (e) { /* analytics must never break the app */ }
            })();
            </script>
            """,
            height=0,
        )
    except Exception:
        pass


def log_page(page_name):
    try:
        st.session_state["_page"] = page_name  # used by feedback sidebar widgets (v1.4)
        st.session_state["_run_seq"] = st.session_state.get("_run_seq", 0) + 1  # per-run nonce (sidebar de-dup)
    except Exception:
        pass
    _inject_visitor_shim()
    try:
        import analytics as _ana
        _ana.track_once_per_session("page_view", {"page": page_name})
    except Exception:
        pass


def log_search(roots):
    try:
        import analytics as _ana
        _ana.track("search", {"roots": [str(r) for r in roots[:8]]})
    except Exception:
        pass


def log_export(fmt):
    try:
        import analytics as _ana
        _ana.track("export", {"format": fmt})
    except Exception:
        pass
