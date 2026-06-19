# -*- coding: utf-8 -*-
"""Meaning layer (Tier A) — per-āyah translations in 4 languages, keyed "S:A".

Source: fawazahmed0/quran-api (open, no key). One frozen edition per language,
chosen to fit this app's al-Mizan (Shia scholarly) orientation:
  • English — Ali Quli Qarai (scholarly, al-Mizan tradition)
  • العربية — Tafsīr al-Jalālayn (the classic concise per-āyah Arabic gloss)
  • اردو   — Sayyid Zeeshan Haider Jawadi
  • فارسی  — Naser Makarem Shirazi
All four cover every one of the 6,236 āyāt (verified 1:1 against Book6).

Display model (per the user): the reader picks ONE language (or Off, or All) from a
single control that persists across pages. The chosen translation is shown directly
under each āyah — not hidden behind an expansion — so it is always visible. Default
is one language (English), never the full four-at-once (which is opt-in via "All").
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
DISPLAY = ("en", "ar", "ur", "fa")

# the single translation control (one choice, persists across pages). Default = Off.
_CHOICES = ["Off", "English", "العربية", "اردو", "فارسی", "All languages"]
_CHOICE2LANGS = {
    "English": ("en",), "العربية": ("ar",), "اردو": ("ur",), "فارسی": ("fa",),
    "All languages": DISPLAY, "Off": (),
}
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


def translation_control(st, key: str = "tr_lang"):
    """Single-select translation control. Returns the language code tuple to show:
    () for Off, (code,) for one language, or DISPLAY for All. Persists across pages
    (shared session key) so the choice is global; each page can still change it."""
    if key not in st.session_state:
        st.session_state[key] = "Off"          # default: no translations until the reader picks one
    choice = st.selectbox(
        "🌐 Translation", _CHOICES, key=key,
        help="Off by default. Pick one language to show it under each āyah, 'All languages' "
             "for every translation, or leave Off. Your choice carries across pages.")
    return _CHOICE2LANGS.get(choice, ())


def _row(code: str, txt: str) -> str:
    label, author, direction, font = EDITIONS[code]
    align = "right" if direction == "rtl" else "left"
    fam = f"font-family:{font};" if font else ""
    return (f"<div class='qrow' style='direction:{direction};text-align:{align}'>"
            f"<span class='qlab'>{label}</span>"
            f"<div class='qtxt {code}' style='color:{INK};{fam}'>{txt}</div></div>")


def meaning_block_html(ref: str, langs=("en",), title: str = "💬 Meaning") -> str:
    """Self-contained meaning card showing exactly `langs` (in canonical order).
    Returns "" when langs is empty (Off) or the āyah/text is missing."""
    if not langs:
        return ""
    d = get(ref)
    if not d:
        return ""
    rows = "".join(_row(c, t) for c in DISPLAY if c in langs and (t := (d.get(c) or "").strip()))
    if not rows:
        return ""
    head = (f"<div class='qmean-h'>{title} "
            f"<span style='font-weight:600;color:{INK}'>· {ref}</span></div>")
    return "<div class='qmean'>" + head + rows + "</div>"


def render(ref: str, langs=("en",), expanded: bool = True, title: str = "💬 Meaning"):
    """Streamlit helper: show the translations for one āyah (default: open)."""
    import streamlit as st
    html = meaning_block_html(ref, langs=langs, title="💬 Meaning")
    if not html:
        return
    st.markdown(html, unsafe_allow_html=True)
