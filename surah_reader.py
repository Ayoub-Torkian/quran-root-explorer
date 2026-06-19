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
            f"<div class='ar' dir='rtl'><span class='num'>{int(surah)}:{a} · {name}</span> {ar}"
            f"{' <span class=here>◂ here</span>' if cur else ''}</div>{tr}</div>")
    css = f"""
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;700&family=Noto+Nastaliq+Urdu&family=Vazirmatn&family=Inter:wght@400;600;700&display=swap');
    *{{box-sizing:border-box;-webkit-text-size-adjust:100%}}
    body{{margin:0;font-family:'Inter',system-ui,sans-serif;color:#10243A;background:#FFFFFF}}
    .bar{{position:sticky;top:0;background:#1D3557;color:#fff;padding:8px 12px;font-weight:700;
      font-size:14px;z-index:9;box-shadow:0 1px 4px rgba(0,0,0,.15)}}
    .ay{{padding:9px 12px;border-bottom:1px solid #eef2f4}}
    .ay.cur{{background:#FFF6DA;border-radius:10px;box-shadow:inset 0 0 0 2px #EAD9A0;margin:4px 6px}}
    .ar .num{{font-size:0.6em;font-weight:800;color:#0F6E56;vertical-align:0.15em}}
    .ar .here{{font-size:0.5em;font-weight:700;color:#B07A1A;vertical-align:0.2em}}
    .ar{{font-family:'Tahoma','Noto Sans Arabic','Segoe UI',Arial,sans-serif;font-size:{ar_px}px;
      line-height:2.05;color:#10243A;text-align:right}}
    .qmean{{margin-top:6px;border-top:1px dashed #cfe0d9;padding-top:6px}}
    .qmean-h{{font-size:13px;font-weight:800;color:#0F6E56;margin-bottom:2px}}
    .qrow{{margin:4px 0}}
    .qlab{{display:inline-block;font-size:12px;font-weight:700;color:#0F6E56;background:#EAF4F0;
      border-radius:999px;padding:1px 10px;margin-bottom:2px}}
    .qtxt{{font-size:{tr_px}px;line-height:1.85;color:#10243A}}
    .qtxt.ar{{font-family:'Tahoma','Noto Sans Arabic',sans-serif;font-size:{round(17*fs,1)}px}}
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
    """Show the whole-sūra reader (iframe), scrolled to the current āyah. Best for a
    quick peek from a verse under study."""
    if langs is None:
        langs = _langs()
    components.html(build_html(corpus, surah, cur_ayah, langs, _scale(), height),
                    height=height, scrolling=True)


def peek(corpus, surah, ayah, height: int = 520, key: str = ""):
    """Reusable affordance — a '📖 Read a sūra' expander that opens the scrollable reader
    at this āyah, AND lets the reader switch to any other sūra (picker + ◀ ▶). Drop onto
    ANY surface that shows an āyah (Search, Āyah Deep-Dive, Cross-References, …)."""
    df = corpus.df
    with st.expander(f"📖 Read a sūra — opens at {int(surah)}:{int(ayah)} "
                     f"(pick any sūra below · scroll start → end)"):
        suras = sorted(set(df[COL_SURAH].astype(int)))
        names = {}
        _cn = COL_SURAH_NAME if COL_SURAH_NAME in df.columns else COL_SURAH
        for s, n in zip(df[COL_SURAH].astype(int), df[_cn]):
            names.setdefault(int(s), str(n))
        sk = "peeksel_" + (key or f"{int(surah)}_{int(ayah)}")
        if sk not in st.session_state:
            st.session_state[sk] = int(surah)
        c = st.columns([1, 5, 1])
        if c[0].button("◀", key=sk + "_p"):
            st.session_state[sk] = max(1, int(st.session_state[sk]) - 1)
        if c[2].button("▶", key=sk + "_n"):
            st.session_state[sk] = min(114, int(st.session_state[sk]) + 1)
        sel = c[1].selectbox("Sūra", suras, format_func=lambda s: f"{s} · {names.get(s, '')}", key=sk)
        cur = int(ayah) if int(sel) == int(surah) else 1   # open at the studied āyah, else at the top
        render(corpus, int(sel), cur, height=height)


def inline_html(corpus, surah: int, langs, cur=None) -> str:
    """Whole sūra as INLINE HTML (uses the app's .vitem/.qv-ar/.qmean classes so the
    page's fonts + text-size control apply, and the PAGE scrolls — no nested box).
    For the dedicated 📖 Read surface, read top→bottom on phone or computer."""
    df = corpus.df
    sub = df[df[COL_SURAH].astype(int) == int(surah)].copy()
    sub["__a"] = sub[COL_AYAH].astype(float).astype(int)
    sub = sub.sort_values("__a")
    name = str(sub[COL_SURAH_NAME].iloc[0]) if (COL_SURAH_NAME in df.columns and len(sub)) else ""
    head = (f"<div style='text-align:center;font-weight:800;color:#1D3557;font-size:16px;"
            f"background:#F4F9F7;border:1px solid #cfe4dc;border-radius:12px;padding:10px;margin:4px 0 8px'>"
            f"📖 Sūra {int(surah)} · {name} <span style='font-weight:600;color:#10243A'>· {len(sub)} āyāt</span></div>")
    rows = [head]
    for _, r in sub.iterrows():
        a = int(r["__a"]); ar = str(r[COL_DIACRITIZED])
        tr = _MEAN.meaning_block_html(f"{int(surah)}:{a}", langs=langs) if langs else ""
        hl = "background:#FFF6DA;border-radius:10px;" if (cur and a == int(cur)) else ""
        rows.append(
            f"<div class='vitem' style='border-bottom:1px solid #eef2f4;padding:9px 10px;{hl}'>"
            f"<div class='vtext qv-ar' dir='rtl' style='text-align:right;color:#10243A;line-height:2.05'>"
            f"<span style='color:#0F6E56;font-weight:800;font-size:0.6em;vertical-align:0.15em'>"
            f"{int(surah)}:{a} · {name}</span> {ar}</div>{tr}</div>")
    return ("<div style='max-width:820px;margin:0 auto'><div class='vgrid'>"
            + "".join(rows) + "</div></div>")
