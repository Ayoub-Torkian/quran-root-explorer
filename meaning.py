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

Display: a `primary` language (the reader's pick) shows immediately under each āyah;
the rest sit behind a JS-free "+ more languages" reveal — the market-app pattern.
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
LANGS = ("en", "ar", "ur", "fa")          # all bundled editions
DISPLAY = ("en", "ar", "ur", "fa")        # shown by default — all four (ar = Tafsīr al-Jalālayn concise gloss)
LANG_LABEL = {"en": "English", "ar": "العربية", "ur": "اردو", "fa": "فارسی"}
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


def _row(code: str, txt: str) -> str:
    """One translation row. Uses CSS classes (mobile.py) for typography, with inline
    direction/align/font so it still looks right if the mobile CSS isn't injected."""
    label, author, direction, font = EDITIONS[code]
    align = "right" if direction == "rtl" else "left"
    fam = f"font-family:{font};" if font else ""
    return (f"<div class='qrow' style='direction:{direction};text-align:{align}'>"
            f"<span class='qlab'>{label}</span>"
            f"<div class='qtxt {code}' style='color:{INK};{fam}'>{txt}</div></div>")


def meaning_block_html(ref: str, primary=("en",), title: str = "💬 Meaning",
                       more_toggle: bool = True) -> str:
    """Self-contained HTML meaning card. `primary` = the language(s) shown immediately;
    the remaining languages sit behind a JS-free '+ more languages' reveal (the
    market-app pattern). If more_toggle is False, all selected languages show inline."""
    d = get(ref)
    if not d:
        return ""
    prim = [c for c in DISPLAY if c in primary] or ["en"]
    rest = [c for c in DISPLAY if c not in prim]
    prim_rows = "".join(_row(c, t) for c in prim if (t := (d.get(c) or "").strip()))
    rest_rows = "".join(_row(c, t) for c in rest if (t := (d.get(c) or "").strip()))
    if not prim_rows and not rest_rows:
        return ""
    more = ""
    if rest_rows and more_toggle:
        n = sum(1 for c in rest if (d.get(c) or "").strip())
        more = (f"<details class='qmore'><summary>＋ {n} more language"
                f"{'s' if n != 1 else ''}</summary>{rest_rows}</details>")
    elif rest_rows:
        prim_rows += rest_rows
    head = (f"<div class='qmean-h'>{title} "
            f"<span style='font-weight:600;color:{INK}'>· {ref}</span></div>")
    return "<div class='qmean'>" + head + prim_rows + more + "</div>"


def language_selector(st, key: str = "meaning_langs", default=("en",)):
    """Compact language picker for the top of a reading surface. Returns the chosen
    primary language codes (tuple); the rest appear behind '+ more' under each āyah."""
    if key not in st.session_state:
        st.session_state[key] = list(default)
    sel = st.multiselect(
        "🌐 Show translation", list(DISPLAY), format_func=lambda c: LANG_LABEL[c], key=key,
        help="Pick your language(s). The others stay one tap away under each āyah.")
    return tuple(sel) if sel else default


def render(ref: str, primary=("en",), expanded: bool = False, title: str = "💬 Meaning"):
    """Streamlit helper: an expander holding the translations for one āyah."""
    import streamlit as st
    html = meaning_block_html(ref, primary=primary, title="💬 Meaning")
    if not html:
        return
    with st.expander(f"{title}  ·  {ref}", expanded=expanded):
        st.markdown(html, unsafe_allow_html=True)
