# -*- coding: utf-8 -*-
"""Mobile-first reading layer — market-grade typography + responsive CSS + reader
controls for the verse / translations surface (Search · Ayah Browser · Āyah Deep-Dive).

>90% of use is on phones, so this targets iOS Safari + Android Chrome: real Qur'an
webfonts (Arabic/Urdu/Persian render the same on every device), full-width single
column, no nested-scroll traps, big tap targets, a calm green-on-light palette.

Reader controls (JS-free, persist in session):
  • Text size — A− / A / A+ / A++  (the ORIGINAL ARABIC is the priority: it scales most)
  • Line spacing — Compact / Comfortable / Spacious
  • Accordion — opening one āyah collapses the others (native <details name=…>)

Usage per page (after st.set_page_config):
    import mobile as _MOB
    _MOB.inject()              # reads the size/spacing the reader picked, injects CSS
    ...
    _MOB.settings_controls(st) # renders the ⚙️ Reading panel somewhere on the page
"""
import streamlit as st

TEAL = "#0F6E56"; NAVY = "#1D3557"; INK = "#10243A"

# size / spacing steps (Arabic gets the largest base so it stays the hero)
_FS = {"A−": 0.88, "A": 1.0, "A+": 1.2, "A++": 1.45}
_LS = {"Compact": 0.9, "Comfortable": 1.0, "Spacious": 1.2}
ACCORDION = "ayahacc"           # shared <details name> → exclusive open (collapse others)


def _scale():
    fs = _FS.get(st.session_state.get("qfs_lbl", "A"), 1.0)
    lh = _LS.get(st.session_state.get("qls_lbl", "Comfortable"), 1.0)
    return fs, lh


def _css(fs: float, lh: float) -> str:
    # base px (mobile-tuned); Arabic hero is biggest. All scale with the size control.
    ar = round(20 * fs, 1)          # Arabic verse hero (expanded)
    arT = round(17 * fs, 1)         # Arabic translation row (Jalālayn)
    tr = round(16 * fs, 1)          # latin/translation rows
    ur = round(17 * fs, 1)          # urdu
    fa = round(16.5 * fs, 1)        # persian
    L = lambda base: round(base * lh, 2)
    return f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;700&family=Noto+Nastaliq+Urdu:wght@400;700&family=Vazirmatn:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');

html{{-webkit-text-size-adjust:100%;text-size-adjust:100%}}
*{{-webkit-tap-highlight-color:transparent}}

/* reading typography */
.qrow{{margin:6px 0}}
.qlab{{display:inline-block;font-size:12px;font-weight:700;color:{TEAL};background:#EAF4F0;
  border-radius:999px;padding:1px 10px;margin-bottom:3px;font-family:'Inter',system-ui,sans-serif}}
.qtxt{{color:{INK};font-size:{tr}px;line-height:{L(1.85)}}}
.qtxt.en{{font-family:'Inter',system-ui,sans-serif}}
.qtxt.ar{{font-family:'Tahoma','Noto Sans Arabic','Segoe UI',Arial,sans-serif;font-size:{arT}px;line-height:{L(2.0)}}}
.qtxt.ur{{font-family:'Noto Nastaliq Urdu',serif;font-size:{ur}px;line-height:{L(2.4)}}}
.qtxt.fa{{font-family:'Vazirmatn','Noto Naskh Arabic',sans-serif;font-size:{fa}px;line-height:{L(2.05)}}}
.qmean{{direction:ltr;text-align:left;margin-top:8px;border-top:1px dashed #cfe0d9;padding-top:7px}}
.qmean-h{{font-size:13px;font-weight:800;color:{TEAL};margin-bottom:3px;font-family:'Inter',sans-serif}}
.qmore{{margin-top:4px}}
.qmore>summary{{list-style:none;cursor:pointer;display:inline-block;font-size:12.5px;font-weight:700;
  color:{TEAL};background:#F1F7F4;border:1px solid #d7e8e0;border-radius:999px;padding:3px 12px;font-family:'Inter',sans-serif}}
.qmore>summary::-webkit-details-marker{{display:none}}
.qmore[open]>summary{{background:#E4F0EB;margin-bottom:4px}}

/* the ORIGINAL ARABIC āyah — the hero. Pars Quran look: Tahoma / Noto Sans Arabic (clean,
   not calligraphic). Scales most; !important beats inline + page CSS. */
.qv-ar{{font-family:'Tahoma','Noto Sans Arabic','Segoe UI',Arial,sans-serif}}
.vitem .vtext{{font-size:{ar}px !important;line-height:{L(2.0)} !important}}
.dd-hero{{font-size:{round(22*fs,1)}px !important;line-height:{L(2.05)} !important}}
.ayah-card .ar{{font-size:{round(19*fs,1)}px !important;line-height:{L(1.9)} !important}}

/* MOBILE (<=640px): the >90% case */
@media (max-width:640px){{
  section[data-testid='stMain'] .block-container{{padding:0.55rem 0.7rem 3rem !important;max-width:100% !important}}
  .vscroll{{max-height:none !important;overflow:visible !important;border:none !important;border-radius:0 !important;padding:0 !important}}
  .vgrid{{grid-template-columns:1fr !important}}
  .vgrid details{{padding:6px 4px !important}}
  .vgrid summary{{font-size:15px !important;line-height:1.8 !important;padding:8px 4px !important;min-height:44px}}
  .ayah-grid{{grid-template-columns:1fr !important;gap:8px !important}}
  .ayah-card{{padding:10px 12px !important}}
  h1,h2{{font-size:1.25rem !important}}
  [data-testid='stMetricValue']{{font-size:1.1rem !important}}
}}
/* PHONES IN LANDSCAPE + small tablets (<=1024px): keep reading FULL-FLOW (no nested
   scroll box, single column, full width) so rotating portrait↔landscape just reflows
   the āyah width instead of trapping it in a boxed scroller. */
@media (max-width:1024px){{
  .vscroll{{max-height:none !important;overflow:visible !important;border:none !important;border-radius:0 !important;padding:0 !important}}
  .vgrid{{grid-template-columns:1fr !important}}
  .ayah-grid{{grid-template-columns:1fr !important}}
  section[data-testid='stMain'] .block-container{{max-width:100% !important}}
}}
@media (max-width:480px){{ .stApp:has(div[data-testid='stStatusWidget'])::after{{display:none}} }}
</style>
"""


def inject():
    """Inject reading CSS + webfonts every rerun (Streamlit rebuilds the DOM each time)."""
    fs, lh = _scale()
    st.markdown(_css(fs, lh), unsafe_allow_html=True)
    # Nudge Streamlit to re-measure on rotation: on orientationchange, fire a resize on the
    # parent so the layout reflows to the new width (otherwise it can stay at portrait width).
    try:
        import streamlit.components.v1 as _c
        _c.html(
            "<script>try{var w=window.parent||window;function p(){w.dispatchEvent(new Event('resize'));}"
            "w.addEventListener('orientationchange',function(){setTimeout(p,150);setTimeout(p,500);"
            "setTimeout(p,1000);});}catch(e){}</script>", height=0)
    except Exception:
        pass


def settings_controls(st_, expanded: bool = False):
    """Render the ⚙️ Reading panel (text size + line spacing). Values persist in session
    and are read by inject() on the next rerun (no lag — widget state is set before inject)."""
    with st_.expander("⚙️ Reading settings — text size & spacing", expanded=expanded):
        c1, c2 = st_.columns(2)
        c1.radio("Text size — original Arabic first", list(_FS), index=1,
                 horizontal=True, key="qfs_lbl")
        c2.radio("Line spacing", list(_LS), index=1, horizontal=True, key="qls_lbl")
        st_.caption("Bigger sizes enlarge the Arabic āyah most. Settings follow you across verses.")
