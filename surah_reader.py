# -*- coding: utf-8 -*-
"""Whole-sūra reader — from any āyah under study, open the full sūra and read it
beginning→end, auto-positioned at the current āyah.

Rendered as a self-contained iframe (st.components.v1.html) so it scrolls on its own
and a tiny script can centre the current āyah on open. Honors the page's translation
choice (tr_lang) and text-size setting (qfs_lbl).
"""
import html as _html
import streamlit as st
import streamlit.components.v1 as components
from analysis import COL_SURAH, COL_AYAH, COL_SURAH_NAME, COL_DIACRITIZED
import meaning as _MEAN

_FS = {"A−": 0.9, "A": 1.0, "A+": 1.2, "A++": 1.45}


def _scale():
    return _FS.get(st.session_state.get("qfs_lbl", "A"), 1.0)


def _langs():
    return _MEAN._CHOICE2LANGS.get(st.session_state.get("tr_lang", "Off"), ())


def build_html(corpus, surah: int, cur_ayah: int, langs, fs: float, height: int) -> str:
    df = corpus.df
    sub = df[df[COL_SURAH].astype(int) == int(surah)].copy()
    sub["__a"] = sub[COL_AYAH].astype(float).astype(int)
    sub = sub.sort_values("__a")
    name = str(sub[COL_SURAH_NAME].iloc[0]) if COL_SURAH_NAME in df.columns and len(sub) else ""
    ar_px = round(20 * fs, 1); tr_px = round(15.5 * fs, 1)
    rows = []
    for _, r in sub.iterrows():
        a = int(r["__a"]); ar = str(r[COL_DIACRITIZED])
        cur = (a == int(cur_ayah))
        tr = _MEAN.meaning_block_html(f"{int(surah)}:{a}", langs=langs) if langs else ""
        rows.append(
            f"<div {'id=cur' if cur else ''} class='ay{' cur' if cur else ''}'>"
            f"<div class='hd'><span class='num'>{int(surah)}:{a}</span>"
            f"{'<span class=here>• reading from here</span>' if cur else ''}</div>"
            f"<div class='ar' dir='rtl'>{ar}</div>{tr}</div>")
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Amiri&family=Noto+Nastaliq+Urdu&family=Vazirmatn&family=Inter:wght@400;600;700&display=swap');
    *{{box-sizing:border-box;-webkit-text-size-adjust:100%}}
    body{{margin:0;font-family:'Inter',system-ui,sans-serif;color:#10243A;background:#FFFFFF}}
    .bar{{position:sticky;top:0;background:#1D3557;color:#fff;padding:8px 12px;font-weight:700;
      font-size:14px;z-index:9;box-shadow:0 1px 4px rgba(0,0,0,.15)}}
    .ay{{padding:9px 12px;border-bottom:1px solid #eef2f4}}
    .ay.cur{{background:#FFF6DA;border-radius:10px;box-shadow:inset 0 0 0 2px #EAD9A0;margin:4px 6px}}
    .hd{{display:flex;align-items:center;gap:10px}}
    .hd .num{{font-size:12.5px;font-weight:800;color:#0F6E56}}
    .hd .here{{font-size:11.5px;font-weight:700;color:#B07A1A}}
    .ar{{font-family:'Amiri','Noto Naskh Arabic',serif;font-size:{ar_px}px;line-height:2.05;
      color:#10243A;text-align:right;margin-top:4px}}
    .qmean{{margin-top:6px;border-top:1px dashed #cfe0d9;padding-top:6px}}
    .qmean-h{{font-size:13px;font-weight:800;color:#0F6E56;margin-bottom:2px}}
    .qrow{{margin:4px 0}}
    .qlab{{display:inline-block;font-size:12px;font-weight:700;color:#0F6E56;background:#EAF4F0;
      border-radius:999px;padding:1px 10px;margin-bottom:2px}}
    .qtxt{{font-size:{tr_px}px;line-height:1.85;color:#10243A}}
    .qtxt.ar{{font-family:'Amiri',serif;font-size:{round(17*fs,1)}px}}
    .qtxt.ur{{font-family:'Noto Nastaliq Urdu',serif;font-size:{round(17*fs,1)}px;line-height:2.4}}
    .qtxt.fa{{font-family:'Vazirmatn',sans-serif;font-size:{round(16.5*fs,1)}px}}
    """
    bar = (f"📖 Sūra {int(surah)} · {_html.escape(name)} — {len(sub)} āyāt"
           "  ·  scroll ↑ to the start, ↓ to the end")
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<style>{css}</style></head><body>"
        f"<div class='bar'>{bar}</div>"
        f"{''.join(rows)}"
        "<script>function ctr(){var c=document.getElementById('cur');"
        "if(c){c.scrollIntoView({block:'center'});}}"
        "window.addEventListener('load',ctr);setTimeout(ctr,80);setTimeout(ctr,300);</script>"
        "</body></html>")


def render(corpus, surah: int, cur_ayah: int, langs=None, height: int = 560):
    """Show the whole-sūra reader, scrolled to the current āyah."""
    if langs is None:
        langs = _langs()
    components.html(build_html(corpus, surah, cur_ayah, langs, _scale(), height),
                    height=height, scrolling=True)
