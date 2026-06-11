# -*- coding: utf-8 -*-
"""Compact whole-Qur'an summary for the Home welcome screen. Source: Book6 corpus.
Two side-by-side boxes (corpus columns + frequent roots) so everything is visible at once."""
from collections import Counter
import streamlit as st
import analysis as A

_NM = "اسم سوره"
_GLOSS = {"ءله": "God", "قول": "to say", "كون": "to be", "ربب": "Lord",
          "ءمن": "to believe", "علم": "to know", "قوم": "people", "ءتی": "to come",
          "كفر": "to disbelieve", "بین": "between / clear", "رحم": "mercy",
          "سمو": "name / sky", "ملك": "to own / king", "یوم": "day", "دین": "religion"}


@st.cache_data(show_spinner=False)
def _facts(_corpus, _cid):
    df = _corpus.df
    S, AY = A.COL_SURAH, A.COL_AYAH
    strip = A.strip_diacritics
    rtok, surftok, segtok = _corpus.root_tokens, _corpus.surface_tokens, _corpus.seg_tokens
    NA = len(df)
    roots = [A.normalize_letters(t) for ay in rtok for t in ay]
    T = len(roots)
    fc = Counter(roots)
    di = [str(v).split() for v in df[A.COL_DIACRITIZED].tolist()] \
        if A.COL_DIACRITIZED in df.columns else [list(t) for t in surftok]
    words = sum(len(t) for t in di)
    letters = sum(len(strip(t).replace("ـ", "").replace(" ", "")) for ay in surftok for t in ay)

    # Bismillāh — Sūra 1, Āya 1 (al-Fātiḥa / Ḥamd)
    sub = df[(df[S].astype(int) == 1) & (df[AY].astype(float).astype(int) == 1)]
    r0 = sub.iloc[0] if len(sub) else df.iloc[0]
    g = lambda col: str(r0[col]) if col in df.columns else ""

    def tot(toks):
        return sum(len(t) for t in toks), len({w for t in toks for w in t})
    sf, sg, dz = tot(surftok), tot(segtok), tot(di)
    cols = [
        ("Roots · ریشه نحوی", sum(len(t) for t in rtok), len(fc), g(A.COL_ROOTS)),
        ("Word-forms · توکن ریشه", sf[0], sf[1], g(A.COL_SURFACE)),
        ("Rasm, segmented · بی حرکت", sg[0], sg[1], g(A.COL_SEGMENTED)),
        ("Diacritized · با حرکت", dz[0], dz[1], g(A.COL_DIACRITIZED)),
    ]
    top = [(rt, _GLOSS.get(rt, ""), c, 100.0 * c / T) for rt, c in fc.most_common(6)]
    cov = lambda n: round(100 * sum(c for _, c in fc.most_common(n)) / T)
    hapax = sum(1 for v in fc.values() if v == 1)
    return dict(cols=cols, ref="1:1", top=top, ayahs=NA, words=words, letters=letters,
                uroots=len(fc), cov100=cov(100), cov500=cov(500), hapax=hapax)


def render_overview(corpus, source="Book6"):
    d = _facts(corpus, id(corpus))
    f = lambda n: format(int(n), ",")
    strip_line = ("114 sūras &middot; %s āyāt &middot; %s words &middot; %s letters &middot; %s roots &middot; %s"
                  % (f(d["ayahs"]), f(d["words"]), f(d["letters"]), f(d["uroots"]), source))

    cgrp = ("<colgroup><col style='width:42%'><col style='width:17%'>"
            "<col style='width:15%'><col style='width:26%'></colgroup>")
    crows = "".join(
        "<tr><td class='cc'>%s</td><td class='cn'>%s</td><td class='cn'>%s</td>"
        "<td class='cs' dir='rtl'>%s</td></tr>" % (lbl, f(t), f(u), s)
        for lbl, t, u, s in d["cols"])
    box_a = (
        "<div class='ov-box'>"
        "<div class='ov-h'>The four text columns of Book6</div>"
        "<table class='ov-t'>" + cgrp +
        "<tr><th>column</th><th class='r'>tokens</th><th class='r'>unique</th>"
        "<th>sample · 1:1 (Bismillāh)</th></tr>" + crows + "</table>"
        "<div class='ov-c'>Each verse stored 4 ways: diacritized → rasm → word-forms → roots.</div>"
        "</div>")

    rgrp = "<colgroup><col style='width:30%'><col style='width:46%'><col style='width:24%'></colgroup>"
    rrows = "".join(
        "<tr><td class='rr' dir='rtl'>%s</td><td class='rg'>%s</td><td class='cn'>%.1f%%</td></tr>"
        % (rt, gl, p) for rt, gl, c, p in d["top"])
    box_b = (
        "<div class='ov-box'>"
        "<div class='ov-h'>Most frequent roots &amp; reach</div>"
        "<table class='ov-t'>" + rgrp +
        "<tr><th>root</th><th>meaning</th><th class='r'>share</th></tr>" + rrows + "</table>"
        "<div class='ov-c'>Learn the top 100 roots → <b>%d%%</b> of all words; top 500 → <b>%d%%</b>. "
        "%s roots appear only once.</div></div>" % (d["cov100"], d["cov500"], f(d["hapax"])))

    css = (
        "<style>"
        ".ov-card{border:1px solid #E2E8F1;border-radius:11px;overflow:hidden;margin:2px 0 12px;background:#FBFCFE}"
        ".ov-head{background:linear-gradient(90deg,#1D3557,#1D9E75);padding:9px 16px}"
        ".ov-head b{font-size:18px;font-weight:800;color:#fff}"
        ".ov-head span{font-size:12.5px;color:#EAF6F1;margin-left:8px}"
        ".ov-row{display:flex;gap:14px;flex-wrap:wrap;padding:10px 14px 12px}"
        ".ov-box{flex:1;min-width:330px}"
        ".ov-h{font-size:12.5px;font-weight:800;color:#1D3557;margin:0 0 3px}"
        ".ov-t{border-collapse:collapse;width:100%;table-layout:fixed}"
        ".ov-t th{padding:4px 8px;font-size:11px;color:#46505F;font-weight:700;"
        "border-bottom:2px solid #1D3557;text-align:left}.ov-t th.r{text-align:right}"
        ".ov-t td{padding:5px 8px;border-bottom:1px solid #EEF2F7;overflow:hidden;text-overflow:ellipsis}"
        ".ov-t td.cc{color:#46505F;font-weight:600;font-size:12.5px;white-space:nowrap}"
        ".ov-t td.cn{color:#1D3557;font-weight:800;text-align:right;font-variant-numeric:tabular-nums}"
        ".ov-t td.cs{color:#1D3557;font-weight:700;font-size:15px;white-space:nowrap}"
        ".ov-t td.rr{color:#1D3557;font-weight:800;font-size:16px}"
        ".ov-t td.rg{color:#46505F;font-size:12.5px}"
        ".ov-c{font-size:10.5px;color:#7A8595;margin-top:5px}"
        "</style>")
    html = (css + "<div class='ov-card'><div class='ov-head'>"
            "<b>📖 The Qur'an at a Glance</b><span>" + strip_line + "</span></div>"
            "<div class='ov-row'>" + box_a + box_b + "</div></div>")
    st.markdown(html, unsafe_allow_html=True)
