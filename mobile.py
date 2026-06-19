# -*- coding: utf-8 -*-
"""Mobile-first reading layer — market-grade typography + responsive CSS for the
verse / translations reading surface (Search · Ayah Browser · Āyah Deep-Dive).

>90% of use is on phones, so this targets iOS Safari + Android Chrome specifically:
real Qur'an webfonts (so Arabic/Urdu/Persian render the same on every device),
full-width single column, no nested scroll traps, generous tap targets, a calm
green-on-light palette like the best Qur'an apps. Desktop is unaffected except for
the nicer fonts. Inject once per page via `mobile.inject()`.
"""
import streamlit as st

# Brand palette (kept from the app, tuned for calm reading)
TEAL = "#0F6E56"      # primary accent
NAVY = "#1D3557"      # headers
INK = "#10243A"       # body text (never grey — locked rule)
PAPER = "#FFFFFF"
CARD = "#FBFCFE"
LINE = "#E6ECF3"

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Noto+Nastaliq+Urdu:wght@400;700&family=Vazirmatn:wght@400;500;600&family=Inter:wght@400;500;600;700&display=swap');

/* ---- iOS/Android base hardening ---- */
html{-webkit-text-size-adjust:100%;text-size-adjust:100%}
*{-webkit-tap-highlight-color:transparent}
:root{--teal:#0F6E56;--navy:#1D3557;--ink:#10243A;--line:#E6ECF3;--card:#FBFCFE}

/* ---- reading typography (all screens) ---- */
.qrow{margin:6px 0}
.qlab{display:inline-block;font-size:12px;font-weight:700;color:var(--teal);
  background:#EAF4F0;border-radius:999px;padding:1px 10px;margin-bottom:3px;font-family:'Inter',system-ui,sans-serif}
.qtxt{color:var(--ink);line-height:1.9;font-size:15.5px}
.qtxt.en{font-family:'Inter',system-ui,sans-serif}
.qtxt.ar{font-family:'Amiri','Noto Naskh Arabic',serif;font-size:18px;line-height:2.0}
.qtxt.ur{font-family:'Noto Nastaliq Urdu',serif;font-size:16px;line-height:2.4}
.qtxt.fa{font-family:'Vazirmatn','Noto Naskh Arabic',sans-serif;font-size:16px;line-height:2.05}
.qmean{direction:ltr;text-align:left;margin-top:8px;border-top:1px dashed #cfe0d9;padding-top:7px}
.qmean-h{font-size:13px;font-weight:800;color:var(--teal);margin-bottom:3px;font-family:'Inter',sans-serif}
/* the JS-free "+ more languages" reveal */
.qmore{margin-top:4px}
.qmore>summary{list-style:none;cursor:pointer;display:inline-block;font-size:12.5px;font-weight:700;
  color:var(--teal);background:#F1F7F4;border:1px solid #d7e8e0;border-radius:999px;padding:3px 12px;font-family:'Inter',sans-serif}
.qmore>summary::-webkit-details-marker{display:none}
.qmore[open]>summary{background:#E4F0EB;margin-bottom:4px}

/* the Arabic āyah HERO line (the verse itself) */
.qv-ar{font-family:'Amiri','Noto Naskh Arabic',serif}

/* ---- MOBILE (<=640px): the >90% case ---- */
@media (max-width:640px){
  section[data-testid='stMain'] .block-container{padding:0.55rem 0.7rem 3rem !important;max-width:100% !important}
  /* full-width single column; never trap scroll inside a box */
  .vscroll{max-height:none !important;overflow:visible !important;border:none !important;
    border-radius:0 !important;padding:0 !important}
  .vgrid{grid-template-columns:1fr !important}
  /* verse rows: bigger, finger-friendly */
  .vgrid details{padding:6px 4px !important}
  .vgrid summary{font-size:15px !important;line-height:1.8 !important;padding:8px 4px !important;min-height:44px}
  .vgrid details[open] summary .vtext{font-size:19px !important;line-height:2.05 !important}
  .qv-ar,.qtxt.ar{font-size:20px !important;line-height:2.1 !important}
  .qtxt{font-size:16.5px !important}
  .qtxt.ur{font-size:17px !important;line-height:2.5 !important}
  .qtxt.fa{font-size:17px !important}
  .qmean-h{font-size:14px !important}
  .qmore>summary{padding:7px 14px !important;font-size:13.5px !important}
  /* tame Streamlit chrome on phones */
  h1,h2{font-size:1.25rem !important}
  [data-testid='stMetricValue']{font-size:1.1rem !important}
  /* the page language selector: comfy tap height */
  [data-testid='stRadio'] label,[data-baseweb='radio']{min-height:40px}
  /* Ayah Browser cards: single column, larger Arabic on phones */
  .ayah-grid{grid-template-columns:1fr !important;gap:8px !important}
  .ayah-card{padding:10px 12px !important}
  .ayah-card .ar{font-size:20px !important;line-height:2.0 !important}
  .ayah-card .en{font-size:15px !important;line-height:1.7 !important}
}

/* hide the desktop "computing" ribbon text on tiny screens (keep the bar) */
@media (max-width:480px){ .stApp:has(div[data-testid='stStatusWidget'])::after{display:none} }
</style>
"""


def inject():
    """Inject the mobile reading CSS + webfonts. Must run every rerun (Streamlit
    rebuilds the DOM each time), so no cross-run guard here."""
    st.markdown(_CSS, unsafe_allow_html=True)
