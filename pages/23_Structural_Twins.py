"""Structural Twins (مثاني) — verses sharing >=50% of roots, gated vs a null.
Dense + self-contained: serves a precomputed concordance (mathani_twins.json);
does NOT load the live corpus, so it cannot break other pages. Computed index, not tafsir."""
import json
from collections import Counter, defaultdict
from pathlib import Path
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Structural Twins", page_icon="♊", layout="wide")
try:
    from state import hero, log_page, inject_css, render_grouped_nav
    log_page("mathani_twins")
    # Restore the custom grouped sidebar nav + global CSS WITHOUT loading the
    # live corpus (this page stays self-contained). get_corpus() normally does
    # this for other pages; here we call the two pieces directly, like Lens Lab.
    try:
        inject_css()
    except Exception:
        pass
    try:
        render_grouped_nav()
    except Exception:
        pass
except Exception:
    def hero(t, s=""):
        st.title(t)
        if s: st.caption(s)

NAVY, TEAL, GRAY, ORANGE, RED, PURPLE = "#1d3557", "#1d9e75", "#c7c5bc", "#ef9f27", "#e63946", "#6a4c93"
DATA = Path(__file__).resolve().parent.parent / "mathani_twins.json"

SURA = ["", "Al-Fatihah","Al-Baqarah","Aal-Imran","An-Nisa","Al-Ma'idah","Al-An'am","Al-A'raf",
"Al-Anfal","At-Tawbah","Yunus","Hud","Yusuf","Ar-Ra'd","Ibrahim","Al-Hijr","An-Nahl","Al-Isra",
"Al-Kahf","Maryam","Ta-Ha","Al-Anbiya","Al-Hajj","Al-Mu'minun","An-Nur","Al-Furqan","Ash-Shu'ara",
"An-Naml","Al-Qasas","Al-Ankabut","Ar-Rum","Luqman","As-Sajdah","Al-Ahzab","Saba","Fatir","Ya-Sin",
"As-Saffat","Sad","Az-Zumar","Ghafir","Fussilat","Ash-Shura","Az-Zukhruf","Ad-Dukhan","Al-Jathiyah",
"Al-Ahqaf","Muhammad","Al-Fath","Al-Hujurat","Qaf","Adh-Dhariyat","At-Tur","An-Najm","Al-Qamar",
"Ar-Rahman","Al-Waqi'ah","Al-Hadid","Al-Mujadila","Al-Hashr","Al-Mumtahanah","As-Saff","Al-Jumu'ah",
"Al-Munafiqun","At-Taghabun","At-Talaq","At-Tahrim","Al-Mulk","Al-Qalam","Al-Haqqah","Al-Ma'arij",
"Nuh","Al-Jinn","Al-Muzzammil","Al-Muddaththir","Al-Qiyamah","Al-Insan","Al-Mursalat","An-Naba",
"An-Nazi'at","Abasa","At-Takwir","Al-Infitar","Al-Mutaffifin","Al-Inshiqaq","Al-Buruj","At-Tariq",
"Al-A'la","Al-Ghashiyah","Al-Fajr","Al-Balad","Ash-Shams","Al-Layl","Ad-Duha","Ash-Sharh","At-Tin",
"Al-Alaq","Al-Qadr","Al-Bayyinah","Az-Zalzalah","Al-Adiyat","Al-Qari'ah","At-Takathur","Al-Asr",
"Al-Humazah","Al-Fil","Quraysh","Al-Ma'un","Al-Kawthar","Al-Kafirun","An-Nasr","Al-Masad",
"Al-Ikhlas","Al-Falaq","An-Nas"]
def sname(s): return SURA[s] if 0 < s < len(SURA) else str(s)

@st.cache_data(show_spinner=False)
def load():
    return json.loads(DATA.read_text(encoding="utf-8"))

@st.cache_data(show_spinner=False)
def agg(_tw):
    pairs=set(); same=cross=strong=0; hub=Counter()
    for ref, lst in _tw.items():
        s=int(ref.split(":")[0])
        for t in lst:
            key=tuple(sorted([ref, t["ref"]]))
            if key in pairs: continue
            pairs.add(key); s2=int(t["ref"].split(":")[0])
            if s==s2: same+=1
            else: cross+=1
            hub[s]+=1; hub[s2]+=1
            if t["jaccard"]>=0.66: strong+=1
    return same, cross, strong, hub.most_common(10)

@st.cache_data(show_spinner=False)
def agg2(_tw):
    pairs=set(); gaps=[]; roots=Counter()
    for ref, lst in _tw.items():
        s=int(ref.split(":")[0])
        for t in lst:
            key=tuple(sorted([ref, t["ref"]]))
            if key in pairs: continue
            pairs.add(key); s2=int(t["ref"].split(":")[0])
            if s!=s2: gaps.append(abs(s-s2))
            for r in t["shared"]: roots[r]+=1
    return gaps, roots.most_common(14)

try:
    import arabic_reshaper as _arsh
    from bidi.algorithm import get_display as _bidi
    def shape(x): return _bidi(_arsh.reshape(x))
except Exception:
    def shape(x): return x

# Traditional (scholarly) revelation classification — NOT computed; several surahs disputed.
MEDINAN = {2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110}

@st.cache_data(show_spinner=False)
def agg4(_tw):
    root_pairs=defaultdict(list); rev=Counter(); seen=set()
    for ref, lst in _tw.items():
        s=int(ref.split(":")[0])
        for tt in lst:
            key=tuple(sorted([ref, tt["ref"]]))
            if key in seen: continue
            seen.add(key); s2=int(tt["ref"].split(":")[0])
            for r in tt["shared"]:
                root_pairs[r].append((key[0], key[1], tt["jaccard"], s, s2))
            c1 = "Medinan" if s in MEDINAN else "Meccan"
            c2 = "Medinan" if s2 in MEDINAN else "Meccan"
            if c1==c2=="Meccan":   rev["Meccan \u2194 Meccan"]+=1
            elif c1==c2=="Medinan": rev["Medinan \u2194 Medinan"]+=1
            else:                   rev["cross (Meccan \u2194 Medinan)"]+=1
    return {k:v for k,v in root_pairs.items()}, dict(rev)

@st.cache_data(show_spinner=False)
def agg3(_tw):
    surah_partners=defaultdict(Counter); twinverses=Counter()
    sp=Counter(); shared_n=Counter(); seen=set()
    for ref, lst in _tw.items():
        s=int(ref.split(":")[0])
        if lst: twinverses[s]+=1
        for tt in lst:
            s2=int(tt["ref"].split(":")[0])
            surah_partners[s][s2]+=1
            key=tuple(sorted([ref, tt["ref"]]))
            if key in seen: continue
            seen.add(key); sp[tuple(sorted((s,s2)))]+=1; shared_n[len(tt["shared"])]+=1
    return {k:dict(v) for k,v in surah_partners.items()}, dict(twinverses), sp.most_common(), dict(shared_n)

def sty(fig, title):
    fig.update_layout(title=dict(text=title, font=dict(size=15, color=NAVY)),
        height=230, margin=dict(l=6,r=6,t=34,b=6), plot_bgcolor="white",
        font=dict(size=13, color="#222"), showlegend=False)
    fig.update_xaxes(title_font=dict(size=12), tickfont=dict(size=11), gridcolor="#eee")
    fig.update_yaxes(title_font=dict(size=12), tickfont=dict(size=11), gridcolor="#eee")
    return fig

st.markdown("""<style>
.block-container{padding-top:2.2rem;padding-bottom:1rem}
div[data-testid='stVerticalBlock']{gap:0.45rem}
div[data-testid='stHorizontalBlock']{gap:0.6rem}
div[data-testid='stMetricValue']{font-size:1.6rem}
div[data-testid='stMetricLabel'] p{font-size:0.82rem}
div[data-testid='stMetric']{padding:2px 0}
hr{margin:0.45rem 0}
div[data-testid='stSelectbox'] label{font-size:0.8rem;margin-bottom:0}
</style>""", unsafe_allow_html=True)

def rtl(txt, size="1.2em", color=NAVY):
    st.markdown(f"<div dir='rtl' style='font-size:{size};line-height:1.7;color:{color};margin:2px 0;"
                f"font-family:\"Scheherazade New\",\"Amiri\",serif'>{txt}</div>", unsafe_allow_html=True)

D=load(); m=D["meta"]; verses=D["verse_text"]
same, cross, strong, top_hubs = agg(D["twins"])
gaps, top_roots_shared = agg2(D["twins"])
surah_partners, twinverses, sp_list, shared_n = agg3(D["twins"])
root_pairs, revcounts = agg4(D["twins"])
excess=round(100*(m["n_pairs"]-m["null_mean"])/m["null_mean"])
nmin, nmax = min(m["null_T"]), max(m["null_T"])
hub_name, hub_links = sname(top_hubs[0][0]), top_hubs[0][1]

hero("♊ Mathāni (مثاني)",
     "Structural Twins — verses sharing at least half their roots. Computed concordance, gated vs chance. Not tafsir.")

st.success(
    "🧬 **Now multimodally validated (Latent Feature L21, grade 96).** The twin bond is not just shared vocabulary: "
    "even with exact duplicates removed and looking only at pairs in *different* sūras, twins end on the same rhyme "
    "**~2× more than chance (59.5% vs 31%)** and run **~4× closer in length (|Δ| 2.4 vs 9.4)** — three converging "
    "rasm channels (root + rhyme + length). See the **Latent Feature Ledger** for the full critical review.")
try:
    st.page_link("pages/25_Latent_Features.py", label="Open L21 in the Latent Feature Ledger", icon="🧬")
except Exception:
    pass

# ── compact KPI strip (small chips, many of them) ────────────────────────────
cross_pct  = round(100*cross/(same+cross))
distinctive = len(verses) - m["n_verses_with_twin"]
ml_ref, ml_n = max(m["twins_per_verse"].items(), key=lambda x: x[1])
chips = [
    ("Twin pairs", f"{m['n_pairs']:,}", "Verse pairs sharing at least 50% of their distinct roots (set-Jaccard). The full structural concordance."),
    ("vs chance", f"+{excess}%", f"How far the {m['n_pairs']:,} pairs exceed the ~{m['null_mean']:,} expected under a vocabulary/length-matched scramble null."),
    ("z-score", f"+{m['z']}", f"Standard deviations above the null mean — how unlikely this many pairs is by chance (B={m['B']} scrambles)."),
    ("Verses w/ twin", f"{m['pct_verses_with_twin']}%", f"Share of the {len(verses):,} verses that have at least one structural twin."),
    ("No twin", f"{distinctive:,}", "Verses with no twin at the 50% threshold — distinctive, often long or unique verses."),
    ("Strong >=66%", f"{strong:,}", "Twin pairs sharing two-thirds or more of their roots — the tightest echoes."),
    ("Across-book", f"{cross_pct}%", "Share of twins whose two verses sit in different surahs (rather than within one surah)."),
    ("Top hub", hub_name, f"Surah with the most twin links ({hub_links:,}) — the densest echo cluster; refrain surahs lead."),
    ("Most-linked", f"{ml_ref} ({ml_n})", f"The single verse with the most twins: {ml_ref} has {ml_n}."),
]
def _chip(lab, val, tip):
    return (f"<div title=\"{tip}\" style='position:relative;flex:1 1 110px;min-width:105px;padding:4px 9px;"
            f"cursor:help;border:1px solid #e6e6e6;border-radius:7px;background:#fafbfc'>"
            f"<span style='position:absolute;top:3px;right:5px;font-size:0.72rem;color:{TEAL};"
            f"font-weight:700'>&#9432;</span>"
            f"<div style='font-size:0.74rem;color:#000;font-weight:600;text-transform:uppercase;letter-spacing:.3px;"
            f"white-space:nowrap;border-bottom:1px dotted #9ec3b6;display:inline-block'>{lab}</div>"
            f"<div style='font-size:1.3rem;font-weight:800;color:{NAVY}'>{val}</div></div>")
st.markdown("<div style='font-size:0.8rem;color:#1d9e75;font-weight:600;margin:0 0 4px'>"
            "&#9432; Hover any box for what it means</div>", unsafe_allow_html=True)
st.markdown("<div style='display:flex;flex-wrap:wrap;gap:7px;margin:2px 0 12px'>"
            + "".join(_chip(l, v, tip) for l, v, tip in chips) + "</div>", unsafe_allow_html=True)

# ── per-verse explorer ───────────────────────────────────────────────────────
_by={}
for _k in verses:
    _s,_a=_k.split(":"); _by.setdefault(int(_s),[]).append(int(_a))
for _s in _by: _by[_s].sort()
_surahs=sorted(_by)
c1,c2,_=st.columns([2,1,6])
surah=c1.selectbox("Surah", _surahs, index=(_surahs.index(112) if 112 in _surahs else 0),
                   format_func=lambda s: f"{s} · {sname(s)}")
ayah=c2.selectbox("Ayah", _by[surah], index=0)
ref=f"{surah}:{ayah}"
tw=D["twins"].get(ref, [])

def line(label, arabic, pct="", roots="", hi=False):
    bg = "background:#eaf3f9;" if hi else ""
    st.markdown(
        f"<div style='display:flex;gap:14px;align-items:baseline;padding:4px 8px;"
        f"border-bottom:1px solid #eee;{bg}'>"
        f"<span style='flex:0 0 150px;color:{NAVY};font-weight:600;font-size:0.85em;white-space:nowrap'>{label}</span>"
        f"<span style='flex:0 0 38px;color:{TEAL};font-weight:700;font-size:0.82em'>{pct}</span>"
        f"<span style='flex:0 0 130px;color:#333;font-size:0.82em;white-space:nowrap;overflow:hidden'>{roots}</span>"
        f"<span dir='rtl' style='flex:0 1 auto;color:{NAVY};font-size:1.25em;"
        f"font-family:\"Scheherazade New\",\"Amiri\",serif'>{arabic}</span>"
        f"</div>", unsafe_allow_html=True)

line(f"{ref} · {sname(surah)}", verses[ref], pct="this", hi=True)

if not tw:
    st.success(f"No structural twin at the {int(m['threshold']*100)}% threshold — a distinctive verse.")
    st.stop()

st.caption(f"{len(tw)} structural twins — verses sharing >= half of this verse's roots")
lc, rc = st.columns([3,2], gap="medium")
with lc:
    for t in tw:
        s2=int(t["ref"].split(":")[0])
        line(f"{t['ref']} · {sname(s2)}", t["text"], pct=f"{t['jaccard']:.0%}", roots=" · ".join(t["shared"]))
with rc:
    fig=go.Figure(go.Bar(x=[t["jaccard"] for t in tw][::-1], y=[t["ref"] for t in tw][::-1],
        orientation="h", marker=dict(color=[len(t["shared"]) for t in tw][::-1],
        colorscale=[[0,GRAY],[1,TEAL]], showscale=False),
        text=[f"{t['jaccard']:.0%}" for t in tw][::-1], textposition="outside",
        textfont_size=11, cliponaxis=False))
    st.plotly_chart(sty(fig, "Twin strength (root overlap)").update_layout(
        height=max(230, 32*len(tw)), margin=dict(l=6,r=28,t=34,b=6)).update_xaxes(
        title_text="", range=[0,1.12]), use_container_width=True)

if len(tw) >= 5:
    _ts = Counter(int(t["ref"].split(":")[0]) for t in tw).most_common()
    _n=[sname(s) for s,_ in _ts][::-1]; _v=[c for _,c in _ts][::-1]
    figm=go.Figure(go.Bar(x=_v, y=_n, orientation="h", marker_color=ORANGE,
        text=[f"{c}" for c in _v], textposition="outside", textfont_size=11, cliponaxis=False))
    st.plotly_chart(sty(figm, f"Where {ref}'s {len(tw)} twins land (by surah)").update_xaxes(
        title_text="# twins").update_layout(margin=dict(l=6,r=30,t=34,b=6)), use_container_width=True)
    st.caption("How to read: each bar = how many of this verse's twins sit in that surah. "
               "One tall bar = a local refrain; spread bars = the verse echoes across the book.")

st.divider()
# ── SURAH level: how the selected surah echoes (uses the chosen surah) ────────
st.markdown(f"<div style='font-weight:800;color:#1d3557;font-size:1.25rem;margin:2px 0 4px'>"
            f"Surah {surah} · {sname(surah)} — how it echoes</div>", unsafe_allow_html=True)
_sp = surah_partners.get(surah, {})
_internal = _sp.get(surah, 0)
_external = sum(v for k, v in _sp.items() if k != surah)
_tv = twinverses.get(surah, 0); _tot = len(_by[surah])
_partlist = sorted(((k, v) for k, v in _sp.items() if k != surah), key=lambda x: -x[1])[:10]
schips = [
    ("Verses w/ twin", f"{_tv}/{_tot}", "Verses in this surah with at least one structural twin, out of its total verses."),
    ("Internal links", f"{_internal:,}", "Twin relations between two verses inside this same surah (refrain-type repetition)."),
    ("External links", f"{_external:,}", "Twin relations linking this surah's verses to verses in OTHER surahs."),
    ("Top partner", sname(_partlist[0][0]) if _partlist else "—", "The other surah this one twins with most often."),
]
st.markdown("<div style='display:flex;flex-wrap:wrap;gap:7px;margin:2px 0 12px'>"
            + "".join(_chip(l, v, tp) for l, v, tp in schips) + "</div>", unsafe_allow_html=True)
if _partlist:
    sc1, sc2 = st.columns([3, 2], gap="medium")
    with sc1:
        _nm = [sname(k) for k, _ in _partlist][::-1]; _vl = [v for _, v in _partlist][::-1]
        fig = go.Figure(go.Bar(x=_vl, y=_nm, orientation="h", marker_color=TEAL,
            text=[f"{v:,}" for v in _vl], textposition="outside", textfont_size=11, cliponaxis=False))
        st.plotly_chart(sty(fig, f"Surahs that echo {sname(surah)} most").update_xaxes(
            title_text="twin links").update_layout(margin=dict(l=6, r=34, t=34, b=6)),
            use_container_width=True)
    with sc2:
        fig = go.Figure(go.Pie(labels=["external", "internal"], values=[_external, _internal],
            hole=0.55, marker_colors=[NAVY, ORANGE], sort=False, textinfo="label+percent", textfont_size=12))
        fig.update_layout(height=max(230, 32 * len(_partlist)), margin=dict(l=6, r=6, t=34, b=6),
            title=dict(text="Internal vs external", font=dict(size=15, color=NAVY)), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.caption(f"{sname(surah)} has no within-corpus structural twins.")

st.divider()
# ── ROOT level: a shared root as a connector between verses ───────────────────
st.markdown("<div style='font-weight:800;color:#1d3557;font-size:1.25rem;margin:2px 0 4px'>"
            "Root as connector</div>", unsafe_allow_html=True)
st.markdown("<div style='border:1px solid #cdd7e0;border-left:7px solid #1d9e75;border-radius:9px;"
    "padding:9px 14px;margin:2px 0 10px;background:#f6faf8;font-size:0.95rem;color:#111;line-height:1.5'>"
    "<b>How to read.</b> Pick a shared root to see how it stitches the text together &mdash; how many "
    "twin pairs it appears in, which surahs it most links, and the strongest example pairs. A root that "
    "bridges distant surahs is a cross-book connector; one that stays local marks a refrain.</div>",
    unsafe_allow_html=True)
_toproots = sorted(root_pairs, key=lambda r: -len(root_pairs[r]))[:30]
rsel = st.selectbox("Shared root (top 30 by reach)", _toproots,
                    format_func=lambda r: f"{r}  —  {len(root_pairs[r]):,} pairs")
_pr = root_pairs[rsel]
rcl, rcr = st.columns([2,3], gap="medium")
with rcl:
    _sc = Counter()
    for a,b,j,sa,sb in _pr:
        _sc[sa]+=1; _sc[sb]+=1
    _tt = _sc.most_common(10)
    _nn=[sname(s) for s,_ in _tt][::-1]; _vv=[c for _,c in _tt][::-1]
    figr=go.Figure(go.Bar(x=_vv, y=_nn, orientation="h", marker_color=NAVY,
        text=[f"{c}" for c in _vv], textposition="outside", textfont_size=11, cliponaxis=False))
    st.plotly_chart(sty(figr, f"Surahs most linked by  {shape(rsel)}").update_xaxes(
        title_text="twin links").update_layout(margin=dict(l=6,r=30,t=34,b=6)), use_container_width=True)
with rcr:
    st.caption(f"This root bridges {len(_pr):,} twin pairs — strongest examples:")
    for a,b,j,sa,sb in sorted(_pr, key=lambda x:-x[2])[:8]:
        st.markdown(f"<div style='padding:2px 0;border-bottom:1px solid #eee;font-size:0.9em'>"
            f"<b>{a}</b> · {sname(sa)} &nbsp;&harr;&nbsp; <b>{b}</b> · {sname(sb)} "
            f"<span style='color:{TEAL};font-weight:700'>{j:.0%}</span></div>", unsafe_allow_html=True)

# ── corpus-level charts (only reached when the verse HAS twins) ───────────────
st.markdown(
    "<div style='border:2px solid #1d3557;border-left:9px solid #1d3557;border-radius:10px;"
    "padding:14px 18px;margin:30px 0 16px;background:#f4f8fc'>"
    "<div style='font-size:1.45rem;font-weight:800;color:#1d3557;letter-spacing:.2px'>"
    "Whole-Qur'an statistics</div>"
    "<div style='font-size:1.02rem;color:#111;margin-top:6px;line-height:1.55'>"
    f"The five charts below describe the <b>entire Qur'an</b> &mdash; all {m['n_pairs']:,} "
    f"structural-twin pairs across {len(verses):,} verses. They are fixed background context and "
    "<b>do NOT change</b> when you pick a different verse above. Your selected verse only drives "
    "the twin list and the chart beside it.</div>"
    "<div style='font-size:0.95rem;color:#111;margin-top:8px;line-height:1.55;"
    "border-top:1px dashed #c4d0db;padding-top:8px'>"
    "<b>How to read the five.</b> "
    "<b>Observed vs scramble null</b> &mdash; how many twin pairs really exist vs the ~"
    f"{m['null_mean']:,} chance would give. "
    "<b>Twin strength</b> &mdash; the overlap-% spread of all pairs (a spike at 100% = identical root sets). "
    "<b>Echo hubs by surah</b> &mdash; which surahs repeat the most (refrain surahs lead). "
    "<b>Where twins live</b> &mdash; share that links different surahs vs stays within one. "
    "<b>Twins per verse</b> &mdash; how many echoes each verse has."
    "</div></div>", unsafe_allow_html=True)
a1,a2,a3 = st.columns(3)
with a1:
    fig=go.Figure(go.Indicator(mode="gauge+number+delta", value=m["n_pairs"],
        number={"font":{"size":28,"color":RED}},
        delta={"reference":m["null_mean"],"increasing":{"color":TEAL},
               "font":{"size":13},"suffix":" vs chance"},
        gauge={"axis":{"range":[1900,3700],"tickfont":{"size":10}},"bar":{"color":RED,"thickness":0.32},
               "steps":[{"range":[nmin,nmax],"color":"#d9e8f0"}],
               "threshold":{"line":{"color":NAVY,"width":3},"thickness":0.85,"value":m["null_mean"]}}))
    fig.update_layout(height=230, margin=dict(l=18,r=18,t=36,b=4),
        title=dict(text="Observed vs scramble null", font=dict(size=15,color=NAVY)), font=dict(size=12))
    st.plotly_chart(fig, use_container_width=True)
with a2:
    fig=go.Figure(go.Histogram(x=m["pair_jaccards"], nbinsx=22, marker_color=TEAL,
                  marker_line_color="white", marker_line_width=0.5))
    fig.add_vline(x=0.66, line=dict(color=ORANGE,width=2,dash="dash"))
    st.plotly_chart(sty(fig,"Twin strength (overlap)").update_xaxes(
        title_text="set-Jaccard").update_yaxes(title_text="pairs"), use_container_width=True)
with a3:
    names=[sname(s) for s,_ in top_hubs][::-1]; vals=[c for _,c in top_hubs][::-1]
    fig=go.Figure(go.Bar(x=vals, y=names, orientation="h",
        marker=dict(color=vals, colorscale=[[0,TEAL],[1,NAVY]]),
        text=[f"{v:,}" for v in vals], textposition="outside", textfont_size=11, cliponaxis=False))
    st.plotly_chart(sty(fig,"Echo hubs by surah").update_xaxes(
        title_text="").update_layout(margin=dict(l=6,r=34,t=34,b=6)), use_container_width=True)

b1,b2 = st.columns([2,3])
with b1:
    fig=go.Figure(go.Pie(labels=["across book","within surah"], values=[cross,same],
        hole=0.55, marker_colors=[NAVY,ORANGE], sort=False, textinfo="label+percent", textfont_size=12))
    fig.update_layout(height=230, margin=dict(l=6,r=6,t=34,b=6),
        title=dict(text="Where twins live", font=dict(size=15,color=NAVY)), showlegend=False,
        annotations=[dict(text=f"{strong:,}<br>strong", x=0.5,y=0.5,showarrow=False,font_size=13)])
    st.plotly_chart(fig, use_container_width=True)
with b2:
    tpv=list(m["twins_per_verse"].values())
    fig=go.Figure(go.Histogram(x=tpv, marker_color=PURPLE, xbins=dict(start=0.5,size=1),
                  marker_line_color="white", marker_line_width=0.5))
    st.plotly_chart(sty(fig,"Twins per verse").update_xaxes(
        title_text="# twins").update_yaxes(title_text="verses (log)", type="log"), use_container_width=True)

st.markdown("<div style='font-weight:800;color:#1d3557;font-size:1.1rem;"
            "border-top:1px solid #d7dde3;padding-top:10px;margin:16px 0 2px'>"
            "More granular cuts</div>", unsafe_allow_html=True)
st.markdown(
    "<div style='border:1px solid #cdd7e0;border-left:7px solid #1d9e75;border-radius:9px;"
    "padding:11px 16px;margin:6px 0 12px;background:#f6faf8'>"
    "<div style='font-size:0.97rem;color:#111;line-height:1.55'>"
    "<b>How to read these five.</b> "
    "<b>(1) Pairs surviving a higher bar</b> &mdash; how fast the echo network thins as you demand "
    "stronger overlap; most twins sit at the 50% floor, but ~27% are near-identical. "
    "<b>(2) Distance between paired surahs</b> &mdash; whether echoes are local (neighbouring surahs) "
    "or span the whole book; the long tail means most echoes reach far. "
    "<b>(3) Roots that drive twinning</b> &mdash; which concepts actually generate the repetition: "
    "Lordship (ربب), denial (كذب), speech (قول), godhood (إله). ""<b>(4) Which surahs share near-identical verses</b> &mdash; a map of verse-twin links between ""surahs; the bright diagonal is a surah echoing itself (Ar-Rahman\u2019s refrain). ""<b>(5) Roots shared per twin pair</b> &mdash; most twins rest on just 2&ndash;3 shared roots.""</div></div>", unsafe_allow_html=True)
g1,g2,g3 = st.columns(3)
with g1:
    _THR=[0.5,0.6,0.66,0.75,0.9,1.0]
    _pj=m["pair_jaccards"]
    _cnt=[sum(1 for x in _pj if x>=th-1e-9) for th in _THR]
    fig=go.Figure(go.Bar(x=[f"{int(th*100)}%" for th in _THR], y=_cnt, marker_color=NAVY,
        text=[f"{c:,}" for c in _cnt], textposition="outside", textfont_size=10, cliponaxis=False))
    st.plotly_chart(sty(fig,"Pairs surviving a higher bar").update_xaxes(
        title_text="min overlap required").update_yaxes(title_text="pairs"), use_container_width=True)
with g2:
    fig=go.Figure(go.Histogram(x=gaps, marker_color=TEAL, nbinsx=28,
        marker_line_color="white", marker_line_width=0.5))
    st.plotly_chart(sty(fig,"Distance between paired surahs").update_xaxes(
        title_text="|surah gap| (cross-book twins)").update_yaxes(title_text="pairs"),
        use_container_width=True)
with g3:
    _rl=[shape(r) for r,_ in top_roots_shared][::-1]
    _rv=[c for _,c in top_roots_shared][::-1]
    fig=go.Figure(go.Bar(x=_rv, y=_rl, orientation="h", marker_color=ORANGE,
        text=[f"{v:,}" for v in _rv], textposition="outside", textfont_size=10, cliponaxis=False))
    st.plotly_chart(sty(fig,"Roots that drive twinning").update_xaxes(
        title_text="in N twin pairs").update_layout(margin=dict(l=6,r=36,t=34,b=6)),
        use_container_width=True)

g4, g5 = st.columns([3, 2], gap="medium")
with g4:
    _deg = Counter()
    for (a, b), c in sp_list:
        _deg[a] += c; _deg[b] += c
    _topS = [s for s, _ in _deg.most_common(16)]
    _spd = dict(sp_list)
    _Z = [[_spd.get(tuple(sorted((a, b))), 0) for b in _topS] for a in _topS]
    _labs = [sname(s) for s in _topS]
    fig = go.Figure(go.Heatmap(z=_Z, x=_labs, y=_labs, colorscale=[[0, "#ffffff"], [1, NAVY]],
        zmax=30, zmin=0, colorbar=dict(title="links", thickness=10),
        hovertemplate="%{y} ↔ %{x}: %{z} twin links<extra></extra>"))
    fig.update_layout(height=400, margin=dict(l=6, r=6, t=34, b=6), plot_bgcolor="white",
        title=dict(text="Which surahs share near-identical verses (diagonal = self-refrain)",
                   font=dict(size=15, color=NAVY)), font=dict(size=11))
    fig.update_xaxes(tickangle=45, tickfont=dict(size=10))
    fig.update_yaxes(tickfont=dict(size=10), autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
with g5:
    _it = sorted(shared_n.items())
    fig = go.Figure(go.Bar(x=[str(k) for k, _ in _it], y=[v for _, v in _it], marker_color=PURPLE,
        text=[f"{v:,}" for _, v in _it], textposition="outside", textfont_size=9, cliponaxis=False))
    st.plotly_chart(sty(fig, "Roots shared per twin pair").update_xaxes(
        title_text="# shared roots").update_yaxes(title_text="pairs"), use_container_width=True)

st.markdown("<div style='font-weight:800;color:#1d3557;font-size:1.1rem;"
            "border-top:1px solid #d7dde3;padding-top:10px;margin:16px 0 2px'>"
            "Revelation-era flow</div>", unsafe_allow_html=True)
g6, g7 = st.columns([2,3], gap="medium")
with g6:
    figmm=go.Figure(go.Pie(labels=list(revcounts.keys()), values=list(revcounts.values()),
        hole=0.5, marker_colors=[NAVY,ORANGE,TEAL], sort=False, textinfo="percent", textfont_size=12))
    figmm.update_layout(height=260, margin=dict(l=6,r=6,t=34,b=6),
        title=dict(text="Twin pairs by revelation class", font=dict(size=15,color=NAVY)),
        legend=dict(font=dict(size=10), orientation="h", y=-0.12))
    st.plotly_chart(figmm, use_container_width=True)
with g7:
    st.markdown("<div style='border:1px solid #cdd7e0;border-left:7px solid #ef9f27;border-radius:9px;"
        "padding:11px 16px;margin:20px 0 0;background:#fcf8f1;font-size:0.93rem;color:#111;line-height:1.55'>"
        "<b>How to read.</b> Each twin pair is classed by whether its two verses sit in Meccan or "
        "Medinan surahs. A large <b>cross</b> slice means structural echoes bridge the two revelation "
        "eras rather than repeating inside one. <b>Caveat:</b> Meccan/Medinan here is the traditional "
        "scholarly classification (<i>not</i> computed), and several surahs are disputed &mdash; treat "
        "this as context, not a measured finding.</div>", unsafe_allow_html=True)

st.caption(f"Honest scope: a vocabulary/length-matched scramble already makes ~{m['null_mean']:,} pairs "
           f"(~60% artifact); the +{excess}% excess (z=+{m['z']}, B={m['B']}) is genuine structure. "
           f"{round(100*cross/(same+cross))}% of twins span different surahs. "
           f"Twin = set-Jaccard >= {m['threshold']} of distinct roots (Book6). research/nuance/mathani_39_23/.")
