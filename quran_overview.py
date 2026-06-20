# -*- coding: utf-8 -*-
"""Compact whole-Qur'an summary for the Home welcome screen. Source: Book6 corpus.
Two side-by-side boxes (corpus text columns + frequent roots), everything visible at once."""
from collections import Counter
import streamlit as st
import analysis as A

_GLOSS = {"ءله": "God", "قول": "to say", "كون": "to be", "ربب": "Lord",
          "ءمن": "to believe", "علم": "to know", "قوم": "people", "ءتی": "to come",
          "كفر": "to disbelieve", "بین": "between / clear", "رحم": "mercy"}


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
    letters = sum(len(strip(t).replace("ـ", "").replace(" ", "")) for ay in surftok for t in ay)
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
    top = [(rt, _GLOSS.get(rt, "—"), c, 100.0 * c / T) for rt, c in fc.most_common(6)]
    cov = lambda n: round(100 * sum(c for _, c in fc.most_common(n)) / T)
    hapax = sum(1 for v in fc.values() if v == 1)
    su = df[S].astype(int)
    cnt = su.value_counts()
    longest_s = int(cnt.idxmax()); longest_n = int(cnt.max()); shortest_n = int(cnt.min())
    nmap = {}
    if A.COL_SURAH_NAME in df.columns:
        for sv, nm in zip(su, df[A.COL_SURAH_NAME]):
            nmap.setdefault(int(sv), str(nm))
    wc = [len(str(v).split()) for v in df[A.COL_DIACRITIZED]] if A.COL_DIACRITIZED in df.columns \
        else [len(t) for t in surftok]
    li = max(range(len(wc)), key=lambda i: wc[i])
    long_ay = "%d:%d" % (int(df[S].iloc[li]), int(df[AY].iloc[li]))
    return dict(cols=cols, top=top, surahs=114, ayahs=NA, letters=letters,
                cov100=cov(100), cov500=cov(500), hapax=hapax, n_roots=len(fc),
                longest_s=longest_s, longest_name=nmap.get(longest_s, ""), longest_n=longest_n,
                shortest_n=shortest_n, avg_ayah=NA / 114.0, long_ay=long_ay, long_ay_w=wc[li])


def render_overview(corpus, source="Book6"):
    d = _facts(corpus, id(corpus))
    f = lambda n: format(int(n), ",")
    strip_line = "%s letters &middot; %s root-tokens &middot; %s" % (
        f(d["letters"]), f(d["cols"][0][1]), source)

    cgrp = ("<colgroup><col style='width:38%'><col style='width:28%'>"
            "<col style='width:18%'><col style='width:16%'></colgroup>")
    crows = "".join(
        "<tr><td class='cc'>%s</td><td class='cs' dir='rtl'>%s</td>"
        "<td class='cn'>%s</td><td class='cn'>%s</td></tr>" % (lbl, s, f(t), f(u))
        for lbl, t, u, s in d["cols"])
    box_a = ("<div class='ov-box'><div class='ov-h'>The four text columns of Book6</div>"
             "<table class='ov-t'>" + cgrp +
             "<tr><th>column</th><th>sample · 1:1 (Bismillāh)</th>"
             "<th class='r'>tokens</th><th class='r'>unique</th></tr>" + crows + "</table>"
             "<div class='ov-c'>Each verse stored 4 ways: diacritized → rasm → word-forms → roots.</div>"
             "</div>")

    rgrp = ("<colgroup><col style='width:14%'><col style='width:22%'><col style='width:30%'>"
            "<col style='width:17%'><col style='width:17%'></colgroup>")
    mx = d["top"][0][3] if d["top"] else 1.0
    rrows = "".join(
        "<tr><td class='rr' dir='rtl'>%s</td><td class='rg'>%s</td>"
        "<td class='bw'><div class='bar' style='width:%d%%'></div></td>"
        "<td class='cn'>%s</td><td class='cn'>%.1f%%</td></tr>"
        % (rt, gl, max(6, int(round(p / mx * 100))), f(c), p)
        for rt, gl, c, p in d["top"])
    box_b = ("<div class='ov-box'><div class='ov-h'>Most frequent roots &amp; reach</div>"
             "<table class='ov-t'>" + rgrp +
             "<tr><th>root</th><th>meaning</th><th>frequency</th>"
             "<th class='r'>count</th><th class='r'>share</th></tr>" + rrows + "</table>"
             "<div class='ov-c'>Top 100 roots → <b>%d%%</b> of all words; top 500 → <b>%d%%</b>. "
             "%s roots appear only once.</div></div>" % (d["cov100"], d["cov500"], f(d["hapax"])))

    css = (
        "<style>"
        ".ov-card{border:1px solid #E2E8F1;border-radius:11px;overflow:hidden;margin:2px 0 12px;background:#FBFCFE}"
        ".ov-head{background:linear-gradient(90deg,#1D3557,#1D9E75);padding:10px 18px;"
        "display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 12px}"
        ".ov-head b{font-size:19px;font-weight:800;color:#fff}.ov-head span{font-size:14px;color:#EAF6F1}"
        ".ov-row{display:flex;gap:18px;flex-wrap:wrap;padding:10px 16px 12px}"
        ".ov-box{flex:1;min-width:300px}"
        ".ov-h{font-size:14px;font-weight:800;color:#1D3557;margin:0 0 4px}"
        ".ov-t{border-collapse:collapse;width:100%;table-layout:fixed}"
        ".ov-t th{padding:5px 9px;font-size:12.5px;color:#10243A;font-weight:700;"
        "border-bottom:2px solid #1D3557;text-align:left}.ov-t th.r{text-align:right}"
        ".ov-t td{padding:6px 9px;border-bottom:1px solid #EEF2F7;overflow:hidden}"
        ".ov-t td.cc{color:#10243A;font-weight:600;font-size:13.5px;white-space:nowrap}"
        ".ov-t td.cn{color:#1D3557;font-weight:800;text-align:right;font-size:14.5px;font-variant-numeric:tabular-nums}"
        ".ov-t td.cs{color:#1D3557;font-weight:700;font-size:16px;white-space:nowrap}"
        ".ov-t td.rr{color:#1D3557;font-weight:800;font-size:18px}"
        ".ov-t td.rg{color:#10243A;font-size:13.5px}"
        ".ov-t td.bw{padding:6px 9px}"
        ".bar{height:12px;border-radius:3px;background:#1D9E75}"
        ".ov-c{font-size:12.5px;color:#10243A;margin-top:6px}"
        ".ov-ins{display:flex;flex-wrap:wrap;gap:4px 18px;padding:8px 18px;border-bottom:1px solid #EEF2F7;"
        "font-size:12.5px;color:#10243A;background:#F4F9F7}.ov-ins b{color:#1D3557}"
        "</style>")
    insights = ("<div class='ov-ins'>"
                "<span>📏 <b>Longest sūra</b> %s · %s āyāt</span>"
                "<span><b>Shortest</b> %s āyāt</span>"
                "<span><b>Avg</b> %.0f āyāt / sūra</span>"
                "<span><b>Longest āyah</b> %s (%s words)</span>"
                "<span><b>%.0f%%</b> of roots appear once</span></div>") % (
        d["longest_name"] or d["longest_s"], f(d["longest_n"]), f(d["shortest_n"]),
        d["avg_ayah"], d["long_ay"], f(d["long_ay_w"]), 100 * d["hapax"] / max(1, d["n_roots"]))
    html = (css + "<div class='ov-card'><div class='ov-head'>"
            "<b>📖 The Qur'an at a Glance</b><span>" + strip_line + "</span></div>"
            + insights + "<div class='ov-row'>" + box_a + box_b + "</div></div>")
    st.markdown(html, unsafe_allow_html=True)
