"""Ayah-content Deep-Dive — explain an ayah in light of the whole corpus.

A FIRST-CLASS endeavor distinct from Root Exploration (not a tab of it). Decomposes
an ayah into its concepts, then surfaces the corpus's most relevant OTHER ayahs,
each TYPED by how it relates on three INDEPENDENT axes (lexical / semantic-
distributional / spatial-territory):
  direct · resonant · co-located · consensus · orthogonal · divergent.

Computational cross-references with evidence (axis z-scores + shared roots), NOT
tafsir. The heavy full report (docx + pdf) is produced by the background worker
`deep_dive.py ayah <s:a>`, not on this page.
"""
from __future__ import annotations

import streamlit as st

import analysis as _A
import deep_dive as DD
import plotly_charts as PC
from state import get_corpus, hero, log_page

st.set_page_config(page_title="Ayah Deep-Dive", page_icon="🔭", layout="wide")
log_page("ayah_deep_dive")
corpus = get_corpus()
st.markdown("<style>section[data-testid='stMain'] [data-testid='stCaptionContainer'],"
            "section[data-testid='stMain'] [data-testid='stCaptionContainer'] *"
            "{color:#10243A !important;font-size:14px !important;}</style>",
            unsafe_allow_html=True)


def _show_chips(items, n=8):
    items = [str(x) for x in items]
    if not items:
        st.markdown("<span style='font-size:20px;color:#10243A'>—</span>",
                    unsafe_allow_html=True)
        return
    out = " ".join(
        "<span style='font-size:22px;color:#10243A;background:#EEF3FB;border-radius:7px;"
        "padding:3px 14px;margin:4px 3px;display:inline-block;font-weight:600'>" + r + "</span>"
        for r in items[:n])
    if len(items) > n:
        out += f" <span style='font-size:14px;color:#10243A'>+{len(items) - n} more</span>"
    st.markdown(out, unsafe_allow_html=True)

hero("🔭 Ayah-content Deep-Dive", "explain an ayah in light of all relevant ayahs")
st.caption("Distinct from Root Exploration: decompose an ayah into its concepts, then surface "
           "the corpus's most relevant OTHER ayahs — TYPED by how they relate. "
           "Computational cross-references, not tafsir.")

# ── SOUND ARCHITECTURE: rhyme & verse-endings (Latent Features L06/L17) — reads viz_data.json ──
try:
    import os as _os17
    import json as _json17
    _vz17 = _json17.load(open(_os17.path.join(_os17.path.dirname(_os17.path.dirname(_os17.path.abspath(__file__))),
                                              "research", "intrinsic", "viz_data.json"), encoding="utf-8"))
    with st.expander("🎵 Sound architecture — rhyme runs & verse-endings (Latent Features L06 · L17)"):
        st.caption("Every āyah ends on a rhyme (fāṣila). Adjacent verses share that ending far more than chance "
                   "(L06, 0.72 vs 0.30), and the rhyme lives in the vowels (L17). See the 🧬 Latent Feature Ledger.")
        if _vz17.get("rhyme_strip"):
            st.markdown("**A rhyme run** — final letter of 30 consecutive verses (Sūra 19); same colour = same rhyme:")
            _pal = {}; _cols = ["#E76F51", "#2A9D8F", "#457B9D", "#F4A261", "#6A4C93", "#C1121F", "#118AB2", "#80B918"]
            _out = ""
            for _r, _c in _vz17["rhyme_strip"]:
                if _c not in _pal:
                    _pal[_c] = _cols[len(_pal) % len(_cols)]
                _out += "<span style='display:inline-block;font-size:20px;color:#fff;border-radius:6px;padding:0 9px;margin:2px;font-family:\"Traditional Arabic\",Amiri,serif;background:%s'>%s</span>" % (_pal[_c], _c)
            st.markdown("<div dir='rtl'>%s</div>" % _out, unsafe_allow_html=True)
        if _vz17.get("fasila"):
            st.markdown("**The actual verse-endings** (fāṣila) with counts — the vowels (-ūna/-īna) are the rhyme:")
            _fc = "".join("<span style='display:inline-block;font-size:21px;background:#EEF3FB;border:1px solid #DEE7F2;border-radius:8px;padding:1px 12px;margin:3px;font-family:\"Traditional Arabic\",Amiri,serif'>%s<sub style='font-size:12px;color:#10243A'>%d</sub></span>" % (w, c) for w, c in _vz17["fasila"][:12])
            st.markdown("<div dir='rtl'>%s</div>" % _fc, unsafe_allow_html=True)
        try:
            st.page_link("pages/25_Latent_Features.py", label="See L06 · L17 in the Latent Feature Ledger", icon="🧬")
        except Exception:
            pass
except Exception:
    pass

with st.expander("📐 Method — the three axes & how this complements Motif analysis"):
    st.markdown(
        "Each candidate ayah is scored on **three INDEPENDENT axes**: **lexical** (shared "
        "roots), **semantic** (distributional closeness of meaning, even with NO shared "
        "words), **spatial** (shared territory). It is then typed: *consensus* (≥2 axes), "
        "*direct / resonant / co-located* (one), *orthogonal* (one, others independent), "
        "*divergent* (one high, another opposed).\n\n"
        "**Where this fits vs 🔺 Motifs:** Motif analysis is the *within-verse* lens "
        "(roots sharing a verse). This is the *across-verse* complement — it links ayahs "
        "by **resonance** (same meaning, different words) and **territory**, reaching the "
        "thematic/narrative ties co-occurrence cannot see (e.g. Yūsuf's grief ↔ his prison).")

@st.cache_data
def _surah_meta(_cid):
    df = corpus.df
    g = df.groupby(df[_A.COL_SURAH].astype(int))
    name = {int(s): str(sub[_A.COL_SURAH_NAME].iloc[0]) for s, sub in g}
    mx = {int(s): int(sub[_A.COL_AYAH].astype(int).max()) for s, sub in g}
    return name, mx


@st.cache_data(show_spinner="Matching against Book6…")
def _match(_cid, pasted):
    return DD.match_pasted_ayahs(corpus, pasted)


@st.cache_data
def _diac_text(_cid):
    df = corpus.df
    col = _A.COL_DIACRITIZED if _A.COL_DIACRITIZED in df.columns else _A.COL_SEGMENTED
    return {(int(s), int(a)): str(t) for s, a, t in
            zip(df[_A.COL_SURAH], df[_A.COL_AYAH], df[col])}


# ── Lens 17 / #66 panels: seal-class + formula-class (per-verse view; template = the 8:61 case study) ──
import re as _re17
_DIA17 = _re17.compile(r"[ً-ْٰـۖ-ۭ]")
_WA17 = _re17.compile(r"[^\W\d_]+", _re17.UNICODE)
_DIVRE = _re17.compile(r"^(الله|ولله|لله|بالله|فالله|والله|تالله|هو|وهو|انه|وانه|فانه)$|^رب(ي|ك|ه|ها|نا|كم|كما|هم|هن)?$")  # #78b: dual ربكما added


def _nl17(t):
    t = _DIA17.sub("", str(t)); t = _re17.sub(r"[آأإٱ]", "ا", t); t = _re17.sub(r"[ىیئ]", "ي", t)
    t = _re17.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").strip()


@st.cache_resource(show_spinner="Indexing seals & formulas…")
def _seal_index(_cid):
    """sklearn-FREE TF-IDF (scipy.sparse) — matches TfidfVectorizer(min_df=2, smooth_idf, l2)."""
    import numpy as _np
    import scipy.sparse as _sp
    df = corpus.df
    sur = df[_A.COL_SURAH].astype(int).to_numpy()
    ay = df[_A.COL_AYAH].astype(int).to_numpy()
    surf = [_WA17.findall(_nl17(t)) for t in df[_A.COL_DIACRITIZED]]
    roots = [str(t).split() for t in df[_A.COL_ROOTS]]
    finals = [w[-1] if w else "" for w in surf]
    classes = {}
    for i, f in enumerate(finals):
        classes.setdefault(f, []).append(i)
    body = [" ".join(r for r in rr[:-1] if r != rr[-1]) if len(rr) > 1 else "x" for rr in roots]
    docs = [(b if b.strip() else "x").split() for b in body]
    n_docs = len(docs)
    dfc = {}
    for d in docs:
        for w in set(d):
            dfc[w] = dfc.get(w, 0) + 1
    vocab = {w: j for j, w in enumerate(sorted(w for w, c in dfc.items() if c >= 2))}
    idf = _np.zeros(len(vocab))
    for w, j in vocab.items():
        idf[j] = _np.log((1.0 + n_docs) / (1.0 + dfc[w])) + 1.0
    rows, cols, vals = [], [], []
    for i, d in enumerate(docs):
        cnt = {}
        for w in d:
            j = vocab.get(w)
            if j is not None:
                cnt[j] = cnt.get(j, 0) + 1
        for j, c in cnt.items():
            rows.append(i); cols.append(j); vals.append(c * idf[j])
    V = _sp.csr_matrix((vals, (rows, cols)), shape=(n_docs, max(len(vocab), 1)))
    _l2 = _np.sqrt(_np.asarray(V.multiply(V).sum(axis=1)).ravel())
    _l2[_l2 == 0] = 1.0
    V = _sp.diags(1.0 / _l2) @ V
    V = V.tocsr()
    occ, spr = {}, {}
    for i, rr in enumerate(roots):
        for r in set(rr):
            occ[r] = occ.get(r, 0) + 1
            spr.setdefault(r, set()).add(int(sur[i]))
    spread = {r: len(s) for r, s in spr.items()}
    div = [any(_DIVRE.match(w) for w in s[-6:]) for s in surf]
    pos = {(int(sur[i]), int(ay[i])): i for i in range(len(df))}
    return dict(finals=finals, classes=classes, V=V, occ=occ, spread=spread, div=div,
                roots=roots, pos=pos)


@st.cache_data(show_spinner=False)
def _fit_z(_cid, ending):
    import numpy as _np
    SI = _seal_index(_cid)
    ix = SI["classes"].get(ending, []); V = SI["V"]
    if not (8 <= len(ix) <= 300):
        return None
    rng = _np.random.default_rng(62)

    def _coh(ii):
        M = (V[ii] @ V[ii].T).toarray(); iu = _np.triu_indices(len(ii), 1)
        return M[iu].mean()

    o = _coh(ix)
    null = _np.array([_coh(rng.choice(V.shape[0], len(ix), replace=False)) for _ in range(150)])
    return float((o - null.mean()) / null.std())


def _seal_panel(ref):
    SI = _seal_index(id(corpus))
    try:
        s_, a_ = (int(x) for x in ref.split(":"))
    except Exception:
        return
    i_ = SI["pos"].get((s_, a_))
    if i_ is None:
        return
    end_ = SI["finals"][i_]
    cls = SI["classes"].get(end_, [])
    with st.expander(f"🔏 Seal & formulas — Lens 17 / #66 panel  (ending: {end_} · class of {len(cls)})"):
        ref_flag = ("divine-marked context" if SI["div"][i_]
                    else "non-divine / other referent")
        st.markdown(f"- **Seal:** `{end_}` caps **{len(cls)}** āyahs across the muṣḥaf · "
                    f"this occurrence: *{ref_flag}* (pre-stated referent rule, EVIDENCE #77)")
        zz = _fit_z(id(corpus), end_)
        if zz is not None:
            st.markdown(f"- **Class content-fit (live #62 statistic):** z = **{zz:+.1f}** vs 150 same-N "
                        f"nulls — the ending predicts its class's body content (fit survives the "
                        f"referent split, #77)")
        else:
            st.markdown("- class too small (<8) or a bare-affix bucket (>300) for the live fit "
                        "statistic — see EVIDENCE #62/#77")
        st.caption("Boundary (honest): heavy ending-REUSE is the cross-text distinctive "
                   "(share 0.18 vs sajʿ 0.04, ord 0.10 — #63 as corrected by #76); the content-fit "
                   "itself is Qur'an-internal. The seal caps its OWN verse (#60).")
        rows = []
        for r in dict.fromkeys(SI["roots"][i_]):
            sp = SI["spread"].get(r, 0)
            klass = "GLOBAL motif" if sp >= 20 else ("LOCAL formula" if sp <= 3 else "mid")
            rows.append({"root": r, "āyahs": SI["occ"].get(r, 0), "sūras": sp, "#66 class": klass})
        if rows:
            import plotly.graph_objects as _goS
            _cmapS = {"GLOBAL motif": "#1D9E75", "mid": "#B4B2A9", "LOCAL formula": "#EF9F27"}
            _figS = _goS.Figure()
            for _klassS, _colS in _cmapS.items():
                _ptsS = [r for r in rows if r["#66 class"] == _klassS]
                if not _ptsS:
                    continue
                _figS.add_trace(_goS.Scatter(
                    x=[p["sūras"] for p in _ptsS], y=[max(p["āyahs"], 1) for p in _ptsS],
                    mode="markers+text", text=[p["root"] for p in _ptsS],
                    textposition="top center", name=_klassS,
                    marker=dict(size=12, color=_colS, line=dict(width=1, color="white")),
                    hovertemplate="%{text}: %{y} āyahs · %{x} sūras<extra></extra>"))
            _figS.add_vline(x=20, line_dash="dash", line_color="#1D9E75")
            _figS.add_vline(x=3, line_dash="dash", line_color="#EF9F27")
            _figS.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10),
                                title="this verse's concepts: reach vs frequency (#66 typing — "
                                      "right of green dash = GLOBAL, left of orange = LOCAL)",
                                xaxis_title="sūras reached", yaxis_title="āyahs (log)",
                                yaxis_type="log")
            st.plotly_chart(_figS, use_container_width=True)
            _ngS = sum(1 for r in rows if r["#66 class"] == "GLOBAL motif")
            _nlS = sum(1 for r in rows if r["#66 class"] == "LOCAL formula")
            _wdS = max(rows, key=lambda r: r["sūras"])
            st.markdown(
                f"**📍 What to take from this chart:** {_ngS}/{len(rows)} of this verse's "
                f"concepts are GLOBAL motifs — "
                + ("the verse is built almost entirely from the corpus's returned-to "
                   "vocabulary (the #42 mode): it speaks the book's recurring language."
                   if _ngS >= 0.7 * len(rows) else
                   f"a mixed build: {_nlS} passage-bound concept(s) anchor it locally while "
                   f"the global ones tie it into the corpus-wide weave.")
                + f" Widest reach here: **{_wdS['root']}** ({_wdS['sūras']} sūras, "
                  f"{_wdS['āyahs']} āyahs).")
            import pandas as _pd17
            with st.expander("data behind the chart (per-root table)"):
                st.dataframe(_pd17.DataFrame(rows), hide_index=True, use_container_width=True)
            st.caption("#66 axes per root: GLOBAL = spread ≥20 sūras (the returned-to class, the "
                       "conceptual face of #42); LOCAL = ≤3 sūras (passage-bound formulae); "
                       "frequencies unnormalized — association needs PPMI (see Network page).")


# ── v2.0 phase 3: ĀYAH-HERO strip (the seed through every lens) + mask/filter ──
_MUQ = {2, 3, 7, 10, 11, 12, 13, 14, 15, 19, 20, 26, 27, 28, 29, 30, 31, 32, 36, 38,
        40, 41, 42, 43, 44, 45, 46, 50, 68}  # 29 muqaṭṭaʿāt sūras (Lens 15)
_MED = {2, 3, 4, 5, 8, 9, 13, 22, 24, 33, 47, 48, 49, 55, 57, 58, 59, 60, 61, 62, 63,
        64, 65, 66, 76, 98, 99, 110}  # traditional cut — CONTROL-ONLY (human frame)
_SEAL_TYPE = [("يعلمون", "wave + re-aimed (#70/#71 'both')"),
              ("تعملون", "rate-wave only (#70/#74)"),
              ("اليم", "wave + re-aimed (#70/#71 'both')"),
              ("عليم", "content re-aimed only (#74)")]


def _hero_strip(ref, res):
    """One row: the seed āyah read through Lens 17 · 9 · 15/16/18 · #66 at a glance."""
    SI = _seal_index(id(corpus))
    try:
        s_, a_ = (int(x) for x in ref.split(":"))
    except Exception:
        return
    i_ = SI["pos"].get((s_, a_))
    if i_ is None:
        return
    end_ = SI["finals"][i_]
    cls = SI["classes"].get(end_, [])
    zz = _fit_z(id(corpus), end_)
    rel = [d for lst in res["related_by_type"].values() for d in lst]
    rsur = {d["ref"].split(":")[0] for d in rel}
    stype = "stable formula (#74 'neither')"
    for k, v in _SEAL_TYPE:
        if end_.endswith(k):
            stype = v
            break
    n_glob = sum(1 for r in set(SI["roots"][i_]) if SI["spread"].get(r, 0) >= 20)
    n_loc = sum(1 for r in set(SI["roots"][i_]) if 0 < SI["spread"].get(r, 0) <= 3)
    cells = st.columns(4)
    cells[0].metric("🔏 seal · Lens 17", end_ or "—",
                    f"class {len(cls)}" + (f" · fit z={zz:+.1f}" if zz is not None else " · n/a"),
                    delta_color="off")
    cells[1].metric("↩ return · Lens 9", f"{len(rel)} āyāt",
                    f"echo-set spans {len(rsur)} sūras", delta_color="off")
    cells[2].metric("🧭 position · L15/18", f"sūra {s_}" + (" 🔠" if s_ in _MUQ else ""),
                    ("Medinan" if s_ in _MED else "Meccan") + " (control-only) · " + stype,
                    delta_color="off")
    cells[3].metric("🌱 roots · #66", f"{n_glob} global / {n_loc} local",
                    "returned-to motifs vs passage-bound", delta_color="off")


def _parse_refs(txt):
    out = []
    for tok in txt.replace(",", " ").split():
        if ":" not in tok:
            continue
        sp, a = tok.split(":", 1)
        try:
            sn = int(sp)
        except ValueError:
            continue
        if "-" in a:
            lo, _, hi = a.partition("-")
            try:
                out += [f"{sn}:{x}" for x in range(int(lo), int(hi) + 1)]
            except ValueError:
                pass
        else:
            try:
                out.append(f"{sn}:{int(a)}")
            except ValueError:
                pass
    return tuple(out)


_name, _mx = _surah_meta(id(corpus))
_surahs = sorted(_name)
if st.session_state.get("_scope_refs"):
    st.info(f"🔬 Form scope active — your scoped āyah(s) are loaded under "
            f"**⌨️ Type references** (selected automatically): "
            f"{st.session_state['_scope_refs'][:80]}"
            f"{'…' if len(st.session_state['_scope_refs']) > 80 else ''}")
mode = st.radio("Choose ayah(s) by", ["📖 Browse", "⌨️ Type references", "📋 Paste ayah text"],
                horizontal=True,
                index=(1 if st.session_state.get("_scope_refs") else 0))
refs_tuple = ()
if mode.startswith("📖"):
    cc = st.columns([3, 1, 1])
    su = cc[0].selectbox("Surah", _surahs, index=_surahs.index(2),
                         format_func=lambda s: f"{s} — {_name.get(s, '')}")
    amax = _mx.get(su, 1)
    a1 = cc[1].number_input("From ayah", 1, amax, min(255, amax) if su == 2 else 1)
    a2 = cc[2].number_input("To ayah", int(a1), amax, int(a1))
    refs_tuple = tuple(f"{su}:{a}" for a in range(int(a1), int(a2) + 1))
elif mode.startswith("⌨️"):
    _sc_refs = st.session_state.get("_scope_refs", "")
    typed = st.text_input("References — supports ranges & commas",
                          value=(_sc_refs or "2:255"),
                          help="e.g.  2:255  ·  2:255-257  ·  2:255, 2:256, 3:18 — "
                               "if a 🔬 form scope is active on Home, its āyahs are "
                               "prefilled here automatically")
    if _sc_refs:
        st.caption("🔬 prefilled from your active form scope — this deep-dive runs on "
                   "exactly that subset (echoes are still searched corpus-wide: that is "
                   "what a deep-dive is for)")
    refs_tuple = _parse_refs(typed)
else:
    pasted = st.text_area("Paste ayah text from any website — verse numbers, brackets and "
                          "translations are stripped automatically by matching against Book6",
                          height=130,
                          placeholder="اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ …")
    if pasted.strip():
        hits = _match(id(corpus), pasted)
        if hits:
            st.caption("Potential matches from Book6 — 90%+ are pre-ticked; tick the correct one(s):")
            _dt = _diac_text(id(corpus))
            _sel = []
            for _n, (s, a, conf) in enumerate(hits, 1):
                cb, txt = st.columns([1, 9])
                if cb.checkbox(f"{_n}", value=(conf >= 0.90), key=f"m_{s}_{a}"):
                    _sel.append(f"{s}:{a}")
                txt.markdown(
                    f"**{s}:{a}**  <span style='color:#10243A;font-size:12px'>"
                    f"({int(conf * 100)}%)</span><br>"
                    f"<span style='font-size:15px'>{_dt.get((s, a), '')[:140]}</span>",
                    unsafe_allow_html=True)
            refs_tuple = tuple(_sel)
        else:
            st.warning("No matching ayah found — check the text is Qur'anic Arabic.")

go = st.button("Run deep-dive", type="primary")


def _ayah(refs_tuple, normalize):
    cache = st.session_state.setdefault("_ayah_cache", {})
    key = (refs_tuple, normalize)
    if key in cache:
        return cache[key]
    seeds = [(int(s), int(a)) for s, a in (r.split(":") for r in refs_tuple)]
    bar = st.progress(0.0, text="Starting deep-dive…")
    try:
        res = DD.ayah_deep_dive(seeds, normalize=normalize, corpus=corpus,
                                progress=lambda f, m: bar.progress(min(f, 1.0), text=m))
    finally:
        bar.empty()
    cache[key] = res
    return res


if not refs_tuple:
    st.info("Choose at least one ayah above (browse, type, or paste).")
    st.stop()
if go:
    st.session_state["ayah_go"] = refs_tuple
if st.session_state.get("ayah_go") != refs_tuple:
    st.info("Selection ready — click ▶ Run deep-dive to start "
            "(it re-confirms whenever you change the selection).")
    st.stop()
try:
    res = _ayah(refs_tuple, False)
except Exception as e:
    st.warning(f"⚠️  {e}")
    st.stop()

for sd in res["seed"]:
    st.markdown(f"### {sd['ref']}")
    st.markdown(f"<div style='font-size:29px;line-height:1.95;margin:6px 0 8px;"
                f"color:#10243A'>{sd['text']}</div>", unsafe_allow_html=True)
    st.markdown("**concepts:**")
    _show_chips(sd["roots"])
    _hero_strip(sd["ref"], res)
    _seal_panel(sd["ref"])

syn = res["synthesis"]
_bc = syn["by_relation"]
g = st.columns(6)
g[0].metric("candidates", syn["n_candidates"], help="related ayahs above the relevance threshold")
g[1].metric("consensus", _bc.get("consensus", 0), help="related on ≥2 independent axes (robust)")
g[2].metric("resonant", _bc.get("resonant", 0), help="distributionally close in meaning, even with NO shared words")
g[3].metric("direct", _bc.get("direct", 0), help="shares roots (lexical overlap)")
g[4].metric("co-located", _bc.get("co-located", 0), help="shares spatial territory")
g[5].metric("divergent", _bc.get("divergent", 0), help="tension: close on one axis, opposed on another")
g2 = st.columns(6)
g2[0].metric("orthogonal", _bc.get("orthogonal", 0), help="related on a single axis; independent on the rest")
g2[1].metric("seed concepts", len(res["seed_concepts"]), help="distinct roots in the seed ayah(s)")
g2[2].metric("seed ayahs", len(res["seed"]), help="number of seed ayahs analysed")

# ── v2.0 phase 3: MASK / FILTER the echo-set (signal-geometry made tangible) ──
_mask = st.selectbox(
    "🎭 Mask the echo-set — isolate or remove a channel before reading the map",
    ["none",
     "cross-sūra only (remove the seed's own sūra)",
     "project out the seal class (remove same-ending āyahs — the #33 rhyme-channel mask)",
     "Meccan sūras only (traditional cut — control-only)",
     "Medinan sūras only (traditional cut — control-only)"])
_seed_suras = {int(r.split(":")[0]) for r in refs_tuple}
_SIm = _seal_index(id(corpus))
_seed_ends = {_SIm["finals"][_SIm["pos"][(int(r.split(':')[0]), int(r.split(':')[1]))]]
              for r in refs_tuple if (int(r.split(':')[0]), int(r.split(':')[1])) in _SIm["pos"]}


def _mask_keep(d):
    try:
        s2, a2 = (int(x) for x in d["ref"].split(":"))
    except Exception:
        return True
    if _mask.startswith("cross"):
        return s2 not in _seed_suras
    if _mask.startswith("project"):
        j = _SIm["pos"].get((s2, a2))
        return j is None or _SIm["finals"][j] not in _seed_ends
    if _mask.startswith("Meccan"):
        return s2 not in _MED
    if _mask.startswith("Medinan"):
        return s2 in _MED
    return True


_rbt = {t: [d for d in lst if _mask_keep(d)] for t, lst in res["related_by_type"].items()}
if _mask != "none":
    _tot = sum(len(v) for v in res["related_by_type"].values())
    _kept = sum(len(v) for v in _rbt.values())
    st.caption(f"mask active: {_kept}/{_tot} echo āyahs kept — if a relation class survives the "
               f"seal-class mask, it is NOT just the rhyme channel (the #33 lesson); the "
               f"Meccan/Medinan cuts are human-frame controls, never claims.")

_pts = [dict(label=d["ref"], x=d["axes"]["semantic"], y=d["axes"]["lexical"],
             relation=t, size=d["axes"]["spatial"])
        for t, lst in _rbt.items() for d in lst]
if _pts:
    st.plotly_chart(PC.chart_fusion_scatter(_pts, "semantic", "lexical",
                    f"{', '.join(res['request']['seeds'])} — relational fusion map", zlab="spatial"),
                    use_container_width=True)
    import pandas as _pd
    _tbl = [{"ayah": d["ref"], "relation": t,
             "L": d["axes"]["lexical"], "S": d["axes"]["semantic"], "P": d["axes"]["spatial"],
             "shared roots": " ".join(d["shared_roots"]) or "—", "متن آیه با حرکت": d["text"]}
            for t, lst in _rbt.items() for d in lst]
    st.markdown("**Plotted ayahs — ID ↔ text (match the points on the map above):**")
    st.dataframe(_pd.DataFrame(_tbl).sort_values(["relation", "ayah"]),
                 use_container_width=True, hide_index=True, height=330)

# ── v2.0 phase 5: echo-set charts (mask-aware) + computed takeaway (LOCKED UI standard) ──
import plotly.graph_objects as _go9

_RELC9 = {"consensus": "#1D9E75", "resonant": "#378ADD", "direct": "#EF9F27",
          "co-located": "#B4B2A9", "orthogonal": "#B4B2A9", "divergent": "#E63946"}
if _pts:
    _cnt9 = {}
    for _t9, _lst9 in _rbt.items():
        for _d9 in _lst9:
            try:
                _s9 = int(_d9["ref"].split(":")[0])
            except Exception:
                continue
            _cnt9[_s9] = _cnt9.get(_s9, 0) + 1
    cQ1, cQ2 = st.columns([1, 2])
    with cQ1:
        _labs9 = [t for t, l in _rbt.items() if l]
        _figd9 = _go9.Figure(_go9.Pie(
            labels=_labs9, values=[len(_rbt[t]) for t in _labs9], hole=0.55,
            marker=dict(colors=[_RELC9.get(t, "#B4B2A9") for t in _labs9])))
        _figd9.update_layout(title="echo composition", height=290,
                             margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(_figd9, use_container_width=True)
        st.caption("❓ how the echoes relate — by meaning (resonant), shared roots (direct), "
                   "territory (co-located), or ≥2 axes at once (consensus). Reacts to the 🎭 mask.")
    with cQ2:
        _xs9 = list(range(1, 115))
        _figp9 = _go9.Figure(_go9.Bar(
            x=_xs9, y=[_cnt9.get(s, 0) for s in _xs9],
            marker_color=["#E63946" if s in _MED else "#1D9E75" for s in _xs9],
            hovertemplate="sūra %{x}: %{y} echo(es)<extra></extra>"))
        _figp9.update_layout(height=290, margin=dict(l=10, r=10, t=40, b=10),
                             title="echo geography — where the seed returns across the muṣḥaf "
                                   "(🟩 Meccan · 🟥 Medinan, control-only)",
                             xaxis_title="sūra (muṣḥaf order)", yaxis_title="echoes")
        st.plotly_chart(_figp9, use_container_width=True)
        st.caption("❓ a wide scatter of bars = LONG-RANGE return (the #42 signature); bars "
                   "hugging the seed's own sūra = local neighborhood. Reacts to the 🎭 mask.")
    _nres9 = len(_rbt.get("resonant") or []); _ndir9 = len(_rbt.get("direct") or [])
    _ncon9 = len(_rbt.get("consensus") or [])
    _tot9 = sum(_cnt9.values())
    _cross9 = sum(v for k, v in _cnt9.items() if k not in _seed_suras)
    _topS9 = max(_cnt9, key=_cnt9.get) if _cnt9 else None
    _mode9 = ("**resonant-led** — the verse returns by MEANING with different words "
              "(re-expression, the #42 mode)" if _nres9 > _ndir9 else
              "**direct-led** — shared roots carry the echo (lexical anchoring)"
              if _ndir9 > _nres9 else "**balanced** between meaning-echo and root-echo")
    st.markdown(
        f"**📍 What to take from the echo-set:** {_tot9} echoes, "
        f"**{100 * _cross9 / max(_tot9, 1):.0f}% outside the seed's own sūra** — "
        + ("long-range return, the corpus keeps coming back to this matter."
           if _cross9 > _tot9 * 0.6 else "mostly a local neighborhood around the seed.")
        + f" The set is {_mode9}; **{_ncon9} consensus** echoes are the core to read first"
        + (f"; densest return: sūra {_topS9} ({_cnt9[_topS9]} echoes)." if _topS9 else ".")
        + (" 🎭 A mask is active — if the set above survived 'project out the seal class', "
           "this return is NOT the rhyme channel." if _mask != "none" else ""))

TYPE_DESC = {
    "consensus": "≥2 axes high — robust, reinforcing",
    "resonant": "distributionally close (meaning, even without shared words)",
    "direct": "shares roots (lexical)",
    "co-located": "shares spatial territory",
    "orthogonal": "one axis only, independent on the rest",
    "divergent": "close on one axis, opposed on another (tension)",
}
for t in ["consensus", "resonant", "direct", "co-located", "orthogonal", "divergent"]:
    lst = _rbt.get(t, [])
    if not lst:
        continue
    with st.expander(f"{t.upper()}  ·  {TYPE_DESC[t]}  ({len(lst)})"):
        for d in lst[:8]:
            ax = d["axes"]
            st.markdown(
                f"<div style='margin:0 0 12px'>"
                f"<span style='color:#10243A;font-weight:700'>{d['ref']}</span> "
                f"<span style='color:#10243A'>· L={ax['lexical']:+.1f} S={ax['semantic']:+.1f} "
                f"P={ax['spatial']:+.1f} · shared: {' '.join(d['shared_roots']) or '—'}</span>"
                f"<div style='font-size:18px;color:#10243A;line-height:1.95;margin-top:2px'>"
                f"{d['text']}</div></div>",
                unsafe_allow_html=True)

st.divider()
st.markdown("#### 📄 Report  (Word · three registers)")
if st.button("Generate report", type="primary", key="gen_ayah"):
    try:
        import report_dive as RP
        _regs = ["technical", "plain_en", "plain_fa"]
        _b = st.progress(0.0, text="Generating report…")
        _docs = {}
        for _i, _reg in enumerate(_regs):
            _b.progress(_i / len(_regs), text=f"Generating {_reg.replace('_', ' ')}…")
            _docs[_reg] = RP.docx_bytes_from_result(res, _reg)
        _b.empty()
        st.session_state["ayah_report"] = {"seeds": res["request"]["seeds"], "docs": _docs}
    except Exception as e:
        st.warning(f"Report generation unavailable: {e}")
_rep = st.session_state.get("ayah_report")
if _rep and _rep.get("seeds") == res["request"]["seeds"]:
    _slug = "_".join(res["request"]["seeds"]).replace(":", "-")
    dl = st.columns(3)
    for col, (reg, label) in zip(dl, [("technical", "Technical"),
                                      ("plain_en", "Plain English"),
                                      ("plain_fa", "فارسی / Persian")]):
        col.download_button(f"⬇ {label}", _rep["docs"][reg],
                            file_name=f"ayah_{_slug}_{reg}.docx",
                            mime=("application/vnd.openxmlformats-officedocument"
                                  ".wordprocessingml.document"),
                            key=f"dl_ayah_{reg}", use_container_width=True)
    st.caption("Generated on demand. Matching PDFs come from the local worker: "
               "`python deep_dive.py ayah <s:a> --reports`.")
