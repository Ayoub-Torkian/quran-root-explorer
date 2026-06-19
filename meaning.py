# -*- coding: utf-8 -*-
"""Meaning layer (Tier A) — per-āyah translations in 4 languages, keyed "S:A".

Source: fawazahmed0/quran-api (open, no key). One frozen edition per language,
chosen to fit this app's al-Mizan (Shia scholarly) orientation:
  • English — Ali Quli Qarai (scholarly, al-Mizan tradition)
  • العربية — Tafsīr al-Jalālayn (the classic concise per-āyah Arabic gloss)
  • اردو   — Sayyid Zeeshan Haider Jawadi
  • فارسی  — Naser Makarem Shirazi
All four cover every one of the 6,236 āyāt (verified 1:1 against Book6). To swap a
translator later, re-bundle meaning.json from a different edition id — nothing else
changes. This is translation (the MEANING layer), NOT tafsīr; al-Mizan tafsīr is Tier B.
"""
from __future__ import annotations
import json, os

_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meaning.json")

# code -> (short label, author, text-direction, font-family-or-None)
_AR_FONT = "'Amiri','Amiri Quran','Noto Naskh Arabic',serif"
EDITIONS = {
    "en": ("English", "Ali Quli Qarai", "ltr", None),
    "ar": ("العربية · تفسير الجلالين", "Jalālayn (gloss)", "rtl", _AR_FONT),
    "ur": ("اردو", "Zeeshan Haider Jawadi", "rtl", "'Noto Nastaliq Urdu','Jameel Noori Nastaleeq',serif"),
    "fa": ("فارسی", "Makarem Shirazi", "rtl", "'Vazirmatn','Noto Naskh Arabic',serif"),
}
LANGS = ("en", "ar", "ur", "fa")
INK = "#10243A"
TEAL = "#0F6E56"

_MEANING = None


def _load():
    global _MEANING
    if _MEANING is None:
        try:
            with open(_PATH, encoding="utf-8") as fh:
                _MEANING = json.load(fh)
        except Exception:
            _MEANING = {}
    return _MEANING


def available() -> bool:
    """True if the bundled meaning data loaded and is non-empty."""
    return bool(_load())


def get(ref: str):
    """Return {'en':.., 'ar':.., 'ur':.., 'fa':..} for 'S:A', or None if absent."""
    return _load().get(ref)


def gloss(ref: str, lang: str = "en", limit: int = 0) -> str:
    """One-language string for compact rows (e.g. browser cards). '' if absent."""
    d = get(ref)
    if not d:
        return ""
    t = (d.get(lang) or "").strip()
    return (t[:limit] + "…") if (limit and len(t) > limit) else t


def meaning_block_html(ref: str, langs=LANGS, title: str = "💬 Meaning",
                       source_note: bool = True) -> str:
    """Self-contained HTML card with the four translations (inline styles only, so it
    renders identically inside an RTL <details> body or a standalone st.markdown)."""
    d = get(ref)
    if not d:
        return ""
    rows = []
    for code in langs:
        txt = (d.get(code) or "").strip()
        if not txt:
            continue
        label, author, direction, font = EDITIONS[code]
        align = "right" if direction == "rtl" else "left"
        fam = f"font-family:{font};" if font else ""
        rows.append(
            f"<div style='margin:5px 0;direction:{direction};text-align:{align}'>"
            f"<span style='display:inline-block;font-size:12px;font-weight:700;color:{TEAL};"
            f"background:#EAF4F0;border-radius:6px;padding:0 8px;margin-bottom:2px'>{label}</span>"
            f"<div style='font-size:15px;color:{INK};line-height:1.85;{fam}'>{txt}</div></div>")
    if not rows:
        return ""
    note = ("<div style='font-size:12px;color:%s;margin-top:6px'>Translations (the meaning layer). "
            "Arabic row is Tafsīr al-Jalālayn's concise gloss. al-Mizan tafsīr is the next tier.</div>"
            % INK) if source_note else ""
    return (
        "<div style='direction:ltr;text-align:left;margin-top:8px;border-top:1px dashed #cfe0d9;"
        "padding-top:6px'>"
        f"<div style='font-size:13px;font-weight:800;color:{TEAL};margin-bottom:2px'>{title} "
        f"<span style='font-size:12px;font-weight:600;color:{INK}'>· {ref}</span></div>"
        + "".join(rows) + note + "</div>")


def render(ref: str, expanded: bool = False, title: str = "💬 Meaning · 4 languages"):
    """Streamlit helper: an expander holding the four translations for one āyah."""
    import streamlit as st
    html = meaning_block_html(ref, title="💬 Meaning")
    if not html:
        return
    with st.expander(f"{title}  ·  {ref}", expanded=expanded):
        st.markdown(html, unsafe_allow_html=True)
