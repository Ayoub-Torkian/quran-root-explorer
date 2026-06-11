# -*- coding: utf-8 -*-
"""Compact whole-Qur'an summary for the Home welcome screen. Source: Book6 corpus."""
from collections import Counter
import streamlit as st
import analysis as A

_NM = "اسم سوره"


@st.cache_data(show_spinner=False)
def _facts(_corpus, _cid):
    df = _corpus.df
    S, AY = A.COL_SURAH, A.COL_AYAH
    strip = A.strip_diacritics
    rtok, surftok, segtok = _corpus.root_tokens, _corpus.surface_tokens, _corpus.seg_tokens
    NA = len(df)
    roots = [A.normalize_letters(t) for ay in rtok for t in ay]
    fc = Counter(roots)
    di = [str(v).split() for v in df[A.COL_DIACRITIZED].tolist()] \
        if A.COL_DIACRITIZED in df.columns else [list(t) for t in surftok]
    words = sum(len(t) for t in di)
    letters = sum(len(strip(t).replace("ـ", "").replace(" ", "")) for ay in surftok for t in ay)
    # short sample verse: shortest with >=3 distinct roots (e.g. 1:4)
    pick = None
    for i in range(NA):
        nd = len(set(A.normalize_letters(t) for t in rtok[i]))
        if len(surftok[i]) >= 3 and nd >= 3 and (pick is None or len(surftok[i]) < pick[0]):
            pick = (len(surftok[i]), i)
    r0 = df.iloc[pick[1] if pick else 0]
    g = lambda col: str(r0[col]) if col in df.columns else ""
    ref = "%d:%d" % (int(r0[S]), int(float(r0[AY])))

    def tot(toks):
        return sum(len(t) for t in toks), len({w for t in toks for w in t})
    sf, sg, dz = tot(surftok), tot(segtok), tot(di)
    cols = [
        ("Roots · ریشه نحوی", sum(len(t) for t in rtok), len(fc), g(A.COL_ROOTS)),
        ("Word-forms · توکن ریشه نحوی", sf[0], sf[1], g(A.COL_SURFACE)),
        ("Rasm, segmented · بی حرکت", sg[0], sg[1], g(A.COL_SEGMENTED)),
        ("Diacritized · با حرکت", dz[0], dz[1], g(A.COL_DIACRITIZED)),
    ]
    return dict(cols=cols, ref=ref, ayahs=NA, words=words, letters=letters, uroots=len(fc))


def render_overview(corpus, source="Book6"):
    d = _facts(corpus, id(corpus))
    f = lambda n: format(int(n), ",")
    strip_line = ("114 sūras &middot; %s āyāt &middot; %s words &middot; %s letters &middot; %s roots"
                  % (f(d["ayahs"]), f(d["words"]), f(d["letters"]), f(d["uroots"])))
    crows = "".join(
        "<tr><td class='cc'>%s</td><td class='cn'>%s</td><td class='cn'>%s</td>"
        "<td class='cs' dir='rtl'>%s</td></tr>" % (lbl, f(t), f(u), s)
        for lbl, t, u, s in d["cols"])
    html = (
        "<style>.qcol{border-collapse:collapse;width:100%;margin:2px 0 4px}"
        ".qcol th{padding:5px 10px;font-size:11.5px;color:#46505F;font-weight:700;"
        "border-bottom:2px solid #1D3557;text-align:left}.qcol th.r{text-align:right}"
        ".qcol td{padding:6px 10px;border-bottom:1px solid #EEF2F7}"
        ".qcol td.cc{color:#46505F;font-weight:600;white-space:nowrap;font-size:13px}"
        ".qcol td.cn{color:#1D3557;font-weight:800;text-align:right;font-variant-numeric:tabular-nums}"
        ".qcol td.cs{color:#1D3557;font-weight:700;font-size:16px}</style>"
        "<div style='border:1px solid #E2E8F1;border-radius:11px;overflow:hidden;"
        "margin:2px 0 12px;background:#FBFCFE'>"
        "<div style='background:linear-gradient(90deg,#1D3557,#1D9E75);padding:11px 16px'>"
        "<span style='font-size:20px;font-weight:800;color:#fff'>📖 The Qur'an at a Glance</span>"
        "<span style='display:block;font-size:13px;color:#EAF6F1;margin-top:2px'>" + strip_line +
        " &middot; source: " + source + "</span></div>"
        "<div style='padding:8px 16px 12px'>"
        "<table class='qcol'><tr><th>Book6 column</th><th class='r'>total tokens</th>"
        "<th class='r'>unique</th><th>sample &middot; " + d["ref"] + "</th></tr>" + crows + "</table>"
        "<div style='font-size:11px;color:#7A8595'>Each verse is stored four ways: "
        "diacritized → rasm (segmented) → word-forms → roots.</div>"
        "</div></div>")
    st.markdown(html, unsafe_allow_html=True)
