"""Two Books · Signal — the Qur'an as a one-dimensional signal.

A companion to the Disjoint-Letters workbench. Here we treat the corpus as an
ordered SIGNAL and apply signal-processing tools — autocorrelation, dispersion,
and spectral analysis — each validated against a permutation / Poisson null so
no apparent structure is taken at face value.

Exploratory scaffold: these are honest, reproducible analyses over the loaded
corpus, not 'miracle' claims. Everything is computed live and guarded with
HAS_REV so the nuzūl (revelation-order) views degrade gracefully.
"""
from __future__ import annotations

import math
from collections import Counter

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from analysis import (COL_SURAH, COL_AYAH, COL_SURAH_NAME, COL_ROOTS,
                      COL_SEGMENTED, normalize_letters)
from state import get_corpus, hero, layer, log_page
from twobooks_stats import shannon_bits

st.set_page_config(page_title="Signal", page_icon="📡", layout="wide")
log_page("signal")
corpus = get_corpus()

NAVY = "#1D3557"; TEAL = "#1D9E75"; AMBER = "#EF9F27"; RED = "#E63946"
GREY = "#B4B2A9"; ICE = "#B4B2A9"; PURPLE = "#378ADD"


# ───────────────────────── data ─────────────────────────
@st.cache_data(show_spinner=False)
def _signal_data(_corpus_id):
    df = corpus.df
    su = df[COL_SURAH].astype(int).tolist()
    ay = df[COL_AYAH].astype(int).tolist()
    verses = {}
    ayah_token_len = []          # tokens per ayah, in mushaf order
    letters = {s: Counter() for s in range(1, 115)}
    for i in range(len(df)):
        s = su[i]
        verses[s] = max(verses.get(s, 0), ay[i])
        toks = corpus.seg_tokens[i]
        ayah_token_len.append(len(toks))
        for t in toks:
            nt = normalize_letters(t)
            for ch in nt:
                if ch.strip():
                    letters[s][ch] += 1
    nuz = {int(k): int(v) for k, v in corpus.rev_order_of_surah.items()}
    return verses, ayah_token_len, letters, nuz


VERSES, AYAH_LEN, LETTERS, NUZ = _signal_data(id(corpus))
HAS_REV = len(NUZ) >= 113
if not HAS_REV:
    st.warning("No revelation-order column in this sheet — nuzūl views are hidden; "
               "muṣḥaf-order analyses are fully available.")
NAMEOF = {int(corpus.df[COL_SURAH].iat[i]): str(corpus.df[COL_SURAH_NAME].iat[i])
          for i in range(len(corpus.df))}


def autocorr(x, max_lag):
    x = np.asarray(x, dtype=float)
    x = x - x.mean()
    denom = np.dot(x, x)
    if denom == 0:
        return np.zeros(max_lag + 1)
    out = np.array([np.dot(x[:len(x) - k], x[k:]) / denom
                    for k in range(max_lag + 1)])
    return out


# ───────────────────────── hero ─────────────────────────
hero("📡 Two Books · Signal",
     "Treat the text as an ordered signal — autocorrelation, dispersion, and "
     "spectra — each checked against a permutation/Poisson null.")

st.markdown(
    "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;"
    "padding:9px 14px;margin:6px 0 14px;font-size:13.5px;color:#1D3557;'>"
    "A <b>signal</b> is just a sequence of numbers in order. The Qur'an gives several: "
    "verse counts per sūra, token lengths per āyah, entropy per sūra. Signal tools ask "
    "whether the ordering carries structure — periodicity, memory, clustering — beyond "
    "what a reshuffled version would show.</div>", unsafe_allow_html=True)

# ── SŪRA STRUCTURE & ORDER (Latent Features L11–L19) — self-contained, reads viz_data.json ──
try:
    import os as _os
    import json as _json
    _vz = _json.load(open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                                        "research", "intrinsic", "viz_data.json"), encoding="utf-8"))
    layer(1, "SŪRA STRUCTURE & ORDER — the ledger findings (Latent Features L11–L19)")
    st.caption("Where sūra boundaries are, how the order is arranged, and how each is marked. "
               "Open the 🧬 Latent Feature Ledger for the full critical review of each.")

    def _mini(fig, h=210):
        fig.update_layout(height=h, margin=dict(l=6, r=6, t=8, b=6), plot_bgcolor="white",
                          paper_bgcolor="white", font=dict(size=11, color="#1D3557"))
        return fig
    _c1, _c2 = st.columns(2)
    with _c1:
        if _vz.get("disc_hist"):
            st.markdown("**Boundary detection (L11)** — discontinuity at real seams (orange) vs ordinary (grey)")
            _dh = _vz["disc_hist"]; _f = go.Figure()
            _f.add_trace(go.Scatter(x=_dh["centers"], y=_dh["internal"], mode="lines", fill="tozeroy", name="ordinary", line=dict(color="#B7C0CC")))
            _f.add_trace(go.Scatter(x=_dh["centers"], y=_dh["boundary"], mode="lines", fill="tozeroy", name="boundary", line=dict(color="#E76F51")))
            _f.update_xaxes(title="discontinuity signal", showgrid=True, gridcolor="#EEF1F6"); _f.update_yaxes(showticklabels=False)
            st.plotly_chart(_mini(_f), width="stretch", key="sig_disc_L11")
        if _vz.get("order_bits"):
            st.markdown("**Order-load axis (L14/L19)** — canonical sits between random & sorted")
            _ob = _vz["order_bits"]; _ordk = ["length-sorted", "rhyme-sorted", "canonical", "random"]
            _f = go.Figure(go.Scatter(x=[_ob[k] for k in _ordk], y=[0] * 4, mode="markers+text",
                marker=dict(size=14, color=["#B7C0CC", "#B7C0CC", "#E63946", "#B7C0CC"], line=dict(width=1, color="#fff")),
                text=_ordk, textposition="top center"))
            _f.update_xaxes(title="MDL bits — lower = more compressible", showgrid=True, gridcolor="#EEF1F6"); _f.update_yaxes(visible=False, range=[-1, 1])
            st.plotly_chart(_mini(_f, 150), width="stretch", key="sig_order_L14")
    with _c2:
        if _vz.get("disc_offset"):
            st.markdown("**Boundary is a local peak (L12)** — signal vs offset from the true seam")
            _oc = _vz["disc_offset"]
            _f = go.Figure(go.Scatter(x=[p[0] for p in _oc], y=[p[1] for p in _oc], mode="lines+markers", line=dict(color="#2B9348", width=1.6), marker=dict(size=6)))
            _f.update_xaxes(title="verses off true boundary", showgrid=True, gridcolor="#EEF1F6"); _f.update_yaxes(title="signal", showgrid=True, gridcolor="#EEF1F6")
            st.plotly_chart(_mini(_f), width="stretch", key="sig_offset_L12")
        if _vz.get("onset_words"):
            st.markdown("**Sūra openings (L18)** — the actual opening words")
            _chips = "".join("<span style='display:inline-block;font-size:20px;background:#EEF3FB;border:1px solid #DEE7F2;border-radius:8px;padding:1px 11px;margin:3px;font-family:\"Traditional Arabic\",Amiri,serif'>%s<sub style='font-size:12px;color:#10243A'>%d</sub></span>" % (w, c) for w, c in _vz["onset_words"][:10])
            st.markdown("<div dir='rtl'>%s</div>" % _chips, unsafe_allow_html=True)
    if _vz.get("chaining"):
        _ch = _vz["chaining"]
        st.markdown("**The verse weave (L22)** — consecutive verses share roots above the order-shuffle floor (dashed); the bond fades with distance. Reorder verses within a sūra and it collapses to chance (z=%.0f)." % _ch["adj_z"])
        _cw1, _cw2 = st.columns([3, 2])
        with _cw1:
            _f = go.Figure(go.Scatter(x=_ch["gaps"], y=_ch["sharing"], mode="lines+markers",
                line=dict(color="#2A9D8F", width=2.4), marker=dict(size=10),
                text=["%.0f%%" % (v * 100) for v in _ch["sharing"]], textposition="top center"))
            _f.add_hline(y=_ch["floor"], line_dash="dash", line_color="#C1121F",
                         annotation_text="within-sūra order shuffle", annotation_position="bottom right", annotation_font_size=9)
            _f.update_xaxes(title="verse distance (gap)", dtick=1, showgrid=True, gridcolor="#EEF1F6")
            _f.update_yaxes(title="% pairs sharing a root", showgrid=True, gridcolor="#EEF1F6")
            st.plotly_chart(_mini(_f, 170), width="stretch", key="sig_chain_L22")
        with _cw2:
            _sp = _ch["split"]
            st.markdown("<div style='font-size:13px;color:#10181F;padding-top:18px'>The order of verses is <b>information-bearing</b>. Adjacent pairs share roots <b>49%%</b> of the time vs <b>39%%</b> under a within-sūra order shuffle — and it replicates in both halves of the book on their own (odd sūras z=%.0f, even z=%.0f).</div>" % (_sp["odd_z"], _sp["even_z"]), unsafe_allow_html=True)
    if _vz.get("granularity"):
        _gr = _vz["granularity"]
        st.markdown("**Multi-scale order (L23)** — the weave isn't only verse-to-verse. Shuffle passages of size b *within* a sūra (vocabulary fixed) and adjacent passages are still more similar than reshuffled ones at every scale — so whole paragraphs are arranged, not just neighbours.")
        _cg1, _cg2 = st.columns([3, 2])
        with _cg1:
            _f = go.Figure(go.Bar(x=["%d-verse" % b for b in _gr["b"]], y=_gr["z"],
                marker=dict(color="#F4A261", line=dict(color="rgba(0,0,0,.12)", width=1)),
                text=["z=%.1f" % z for z in _gr["z"]], textposition="outside"))
            _f.add_hline(y=2.0, line_dash="dash", line_color="#C1121F", annotation_text="significance", annotation_font_size=9)
            _f.update_xaxes(title="passage block size (within-sūra control)", showgrid=False)
            _f.update_yaxes(title="z (per-sūra paired)", showgrid=True, gridcolor="#EEF1F6", range=[0, 14])
            st.plotly_chart(_mini(_f, 170), width="stretch", key="sig_gran_L23")
        with _cg2:
            st.markdown("<div style='font-size:13px;color:#10181F;padding-top:18px'>Globally the order is non-random from single verses up to <b>100-verse sections</b> (z 73→8). The text is sequenced as <b>nested units</b>: words in verses, verses in passages, passages in sūras.</div>", unsafe_allow_html=True)
    # ── The order ladder continues: L24 (sūra-sequence), L25 (information flow), L26 (closing cadence) ──
    _ladder = [
        ("l24_controls", "Sūra-sequence order (L24)", "The arrangement reaches the **chapter** scale: adjacent sūras share vocabulary above a length-matched shuffle and the signal survives removing the muqaṭṭaʿāt groups — bearing on the muṣḥaf order itself.", "#6A4C93"),
        ("l25_controls", "Information flow is smoothed (L25)", "Adjacent verses carry similar information-per-word (root surprisal) — the text regulates information **flow**, a layer beyond lexical weaving. Beats the shuffle and a length-matched control; confirmed by surprisal autocorrelation.", "#2A9D8F"),
        ("l26_controls", "Closing cadence (L26)", "Sūras **resolve**: the final verse drops to lighter, more familiar vocabulary than the interior — and it is not the rhyme word (the effect strengthens once that is removed). Chapters are framed at both ends (onset L18 + close L26).", "#E76F51"),
    ]
    if any(_vz.get(k) for k, *_ in _ladder):
        st.markdown("**The order ladder — chapter scale, flow, and closing.** Three more findings on how the Qur'ān is arranged. Each bar is a per-sūra paired test vs a successive null (dashed = significance).")
        _lc = st.columns(3)
        for _i, (_k, _ttl, _desc, _col) in enumerate(_ladder):
            if not _vz.get(_k):
                continue
            with _lc[_i]:
                _cb = _vz[_k]
                st.markdown("**%s**" % _ttl)
                _f = go.Figure(go.Bar(x=_cb["labels"], y=_cb["vals"], marker=dict(color=_col, line=dict(color="rgba(0,0,0,.12)", width=1)),
                    text=["%.1f" % v for v in _cb["vals"]], textposition="outside"))
                _f.add_hline(y=2.0, line_dash="dash", line_color="#C1121F")
                _f.update_xaxes(showgrid=False, tickfont=dict(size=10))
                _f.update_yaxes(title=_cb["stat"], showgrid=True, gridcolor="#EEF1F6", range=[0, max(_cb["vals"]) * 1.25])
                st.plotly_chart(_mini(_f, 165), width="stretch", key="sig_%s" % _k)
                st.caption(_desc)
    # ── Per-sūra weave picker (L22, interactive) ──
    try:
        _wv = _json.load(open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                                            "research", "intrinsic", "sura_weave.json"), encoding="utf-8"))["suras"]
        st.markdown("**Per-sūra weave (L22)** — pick any sūra to see its actual root-chain, its score, and where it ranks.")
        _opts = sorted(_wv.values(), key=lambda o: o["n"])
        _lbl = {("%d · %s  (%s)" % (o["n"], o["name"], o["mode"])): str(o["n"]) for o in _opts}
        _pick = st.selectbox("sūra", list(_lbl.keys()), index=66, label_visibility="collapsed", key="weave_pick")
        _o = _wv[_lbl[_pick]]
        _m1, _m2, _m3, _m4 = st.columns(4)
        _m1.metric("neighbour-sharing", "%.2f" % _o["score"])
        _m2.metric("lift vs own shuffle", "%+.2f" % _o["lift"])
        _m3.metric("rank (of 95)", ("#%d" % _o["rank"]) if "rank" in _o else "—")
        _m4.metric("verses", _o["nv"])
        st.caption("**%s.** %s" % (_o["mode"].capitalize(),
                   "Reorder its verses and the chain measurably loosens." if _o["lift"] >= 0.05
                   else ("Cohesion is near-saturated — almost every neighbour shares a root regardless of order." if _o["score"] >= 0.55 and _o["lift"] < 0.03
                   else ("Too short for the corpus statistic; read its head/foot anchors instead." if _o["nv"] < 10
                   else "The weave is weak here — verses progress by shifting vocabulary."))))
        _shared_any = set(r for lk in _o["links"] for r in lk["s"])
        _rows = ""
        for i, v in enumerate(_o["verses"]):
            _lk = _o["links"][i - 1]["s"] if i > 0 else []
            _bridge = ("<span style='color:#2A9D8F;font-size:12px'>↑ shares %s</span>" %
                       " ".join("<b>%s</b>" % r for r in _lk)) if _lk else ("<span style='color:#10243A;font-size:12px'>↑ —</span>" if i > 0 else "")
            _rows += ("<div style='display:flex;gap:8px;align-items:baseline;padding:1px 0'>"
                      "<span style='color:#10243A;font-size:12px;min-width:46px'>%s</span>"
                      "<span dir='rtl' style='font-family:\"Traditional Arabic\",Amiri,serif;font-size:18px;color:#10171F;flex:1'>%s</span>"
                      "<span style='min-width:120px'>%s</span></div>") % (v["ref"], v["t"], _bridge)
        st.markdown("<div style='max-height:300px;overflow-y:auto;border:1px solid #E6EBF2;border-radius:8px;padding:6px 10px'>%s</div>" % _rows, unsafe_allow_html=True)
        st.caption("Green ↑ = this verse shares a root with the one above it (a live link in the weave). Grey ↑ = no shared root.")
    except Exception:
        pass
    if _vz.get("seams"):
        st.markdown("**The 113 sūra seams (L16)** — <span style='color:#C1121F'>■</span> sound-marked · <span style='color:#B7C0CC'>■</span> meaning-marked")
        st.markdown("<div style='line-height:1'>%s</div>" % "".join("<span style='display:inline-block;width:8px;height:15px;margin:1px;border-radius:2px;background:%s'></span>" % ("#C1121F" if s else "#B7C0CC") for s in _vz["seams"]), unsafe_allow_html=True)
    try:
        st.page_link("pages/25_Latent_Features.py", label="See L11–L19 · L22–L26 in the Latent Feature Ledger", icon="🧬")
    except Exception:
        pass
except Exception:
    pass

t_len, t_recur, t_spec, t_rhythm, t_xcorr = st.tabs(
    ["📈 Length signal", "🔁 Root recurrence", "🌊 Entropy spectrum",
     "🥁 Verse rhythm", "🔗 Co-recurrence"])


# ═══════════ TAB 1 — LENGTH SIGNAL ═══════════
with t_len:
    layer(1, "Sūra-length sequence and its memory")
    st.caption("Verse counts read off in order form a signal. Its autocorrelation "
               "shows whether neighbouring sūras have related lengths (memory) or are "
               "effectively independent.")
    order = st.radio("Order", ["Muṣḥaf (book)"] + (["Nuzūl (revelation)"] if HAS_REV else []),
                     horizontal=True, key="_sig_len_order")
    if order.startswith("Nuzūl"):
        seq_suras = sorted(range(1, 115), key=lambda s: NUZ.get(s, 999))
        xlab = "revelation order"
    else:
        seq_suras = list(range(1, 115))
        xlab = "sūra number (muṣḥaf)"
    series = [VERSES.get(s, 0) for s in seq_suras]

    fig = go.Figure(go.Scatter(x=list(range(1, 115)), y=series, mode="lines+markers",
                               line=dict(color=NAVY), marker=dict(size=4, color=AMBER),
                               text=[NAMEOF.get(s, "") for s in seq_suras],
                               hoverinfo="text+y"))
    fig.update_layout(height=320, plot_bgcolor="white", font=dict(size=14),
                      xaxis_title=xlab, yaxis_title="verses",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Sūra-length signal")
    st.plotly_chart(fig, width="stretch")
    try:
        _imax = int(np.argmax(series)); _imin = int(np.argmin(series))
        _h1 = float(np.mean(series[:57])); _h2 = float(np.mean(series[57:]))
        st.markdown(
            f"**📍 What to take from this chart:** the signal swings from "
            f"{int(series[_imax])} verses ({NAMEOF.get(seq_suras[_imax], '')}, "
            f"sūra {seq_suras[_imax]}) down to {int(series[_imin])} "
            f"({NAMEOF.get(seq_suras[_imin], '')}, sūra {seq_suras[_imin]}); the first "
            f"half of this ordering averages {_h1:.0f} verses vs {_h2:.0f} in the second "
            f"— a {'falling' if _h1 > _h2 else 'rising'} envelope. The autocorrelation "
            f"below tests whether neighbouring-length 'memory' is real or noise."
        )
    except Exception:
        pass

    max_lag = 20
    acf = autocorr(series, max_lag)
    fig = go.Figure(go.Bar(x=list(range(max_lag + 1)), y=acf, marker_color=TEAL))
    ci = 1.96 / math.sqrt(len(series))
    fig.add_hline(y=ci, line=dict(color=RED, dash="dash"))
    fig.add_hline(y=-ci, line=dict(color=RED, dash="dash"),
                  annotation_text="95% white-noise band")
    fig.update_layout(height=300, plot_bgcolor="white", font=dict(size=14),
                      xaxis_title="lag (sūras)", yaxis_title="autocorrelation",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Autocorrelation — bars outside the band = real memory")
    st.plotly_chart(fig, width="stretch")
    lag1 = acf[1]
    st.metric("Lag-1 autocorrelation", f"{lag1:+.3f}",
              "outside white-noise band" if abs(lag1) > ci else "within noise band",
              help=f"Correlation between each sūra's length and its immediate neighbour's. "
                   f"The 95% white-noise band is ±{ci:.3f}; outside it = genuine adjacency memory.")
    st.caption("A positive lag-1 means long sūras tend to sit next to long ones — "
               "consistent with the muqaṭṭaʿāt clustering the long sūras into runs.")


# ═══════════ TAB 2 — ROOT RECURRENCE ═══════════
with t_recur:
    layer(1, "Is a root bursty or evenly spread?")
    st.caption("Mark every āyah where a chosen root occurs as a 1, else 0. The gaps "
               "between 1s reveal whether the root clusters (bursty) or spreads "
               "regularly. We compare the dispersion to a Poisson (memoryless) null.")
    freqs = corpus.freq_norm
    top_roots = [r for r, _ in freqs.most_common(400)]
    root = st.selectbox("Root (normalized, top-400 by frequency)", top_roots,
                        key="_sig_root")
    idx = sorted(corpus.index_norm.get(root, []))
    n_ayah = len(corpus.df)
    if len(idx) < 3:
        st.info("Too few occurrences to analyze dispersion.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Occurrences", len(idx),
                  help="Āyahs containing this root, marked as 1s in the 0/1 signal.")
        gaps = np.diff(idx)
        fano = gaps.var() / gaps.mean() if gaps.mean() else 0.0
        c2.metric("Fano factor (var/mean of gaps)", f"{fano:.2f}",
                  "bursty (>1)" if fano > 1.2 else "regular (<1)" if fano < 0.8 else "~Poisson",
                  help="Variance ÷ mean of the gaps between occurrences. >1 = clumped bursts "
                       "with long silences; ≈1 = memoryless (Poisson); <1 = evenly spaced.")
        c3.metric("Mean gap (āyahs)", f"{gaps.mean():.1f}",
                  help="Average distance between consecutive occurrences along the muṣḥaf.")

        raster = np.zeros(n_ayah)
        raster[idx] = 1
        fig = go.Figure(go.Scatter(x=idx, y=[1] * len(idx), mode="markers",
                                   marker=dict(size=4, color=PURPLE), hoverinfo="x"))
        fig.update_layout(height=180, plot_bgcolor="white", font=dict(size=13),
                          xaxis_title="āyah index (muṣḥaf)", yaxis=dict(visible=False),
                          margin=dict(l=10, r=10, t=30, b=10),
                          title=f"Occurrence raster of «{root}»")
        st.plotly_chart(fig, width="stretch")

        nd = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                              key="_sig_recur_nd")
        if st.button("▶ Test dispersion vs Poisson null", type="primary",
                     key="_sig_recur_btn"):
            st.session_state["_sig_recur_run"] = (root, nd)
        run = st.session_state.get("_sig_recur_run")
        if run and run[0] == root:
            k = len(idx); rng = np.random.default_rng(5)
            out = np.empty(run[1])
            for j in range(run[1]):
                pick = np.sort(rng.choice(n_ayah, size=k, replace=False))
                g = np.diff(pick)
                out[j] = g.var() / g.mean() if g.mean() else 0.0
            p = (np.sum(out >= fano) + 1) / (run[1] + 1)
            st.metric("Burstiness p (vs random placement)", f"{p:.2g}",
                      "✓ more clustered than chance" if p < .05 else "n.s.")
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
            fig.add_vline(x=fano, line=dict(color=RED, width=3),
                          annotation_text=f"observed Fano={fano:.2f}",
                          annotation_position="top")
            fig.update_layout(height=300, plot_bgcolor="white", font=dict(size=14),
                              xaxis_title="Fano factor", yaxis_title="count",
                              showlegend=False, margin=dict(l=10, r=10, t=40, b=10),
                              title=f"Dispersion of «{root}» vs random placement → p ≈ {p:.2g}")
            st.plotly_chart(fig, width="stretch")


# ═══════════ TAB 3 — ENTROPY SPECTRUM ═══════════
with t_spec:
    layer(1, "Spectral analysis of the per-sūra entropy series")
    st.caption("Compute each sūra's letter-entropy, read the 114 values in order, and "
               "take the power spectrum (FFT). A spike at some frequency would mean a "
               "repeating cycle in how 'mixed' sūras are. We compare the peak to a "
               "phase-shuffled null that destroys ordering but keeps the values.")
    order2 = st.radio("Order", ["Muṣḥaf (book)"] + (["Nuzūl (revelation)"] if HAS_REV else []),
                      horizontal=True, key="_sig_spec_order")
    if order2.startswith("Nuzūl"):
        seq_suras = sorted(range(1, 115), key=lambda s: NUZ.get(s, 999))
    else:
        seq_suras = list(range(1, 115))
    H = np.array([shannon_bits(LETTERS[s].values()) for s in seq_suras])

    Hd = H - H.mean()
    power = np.abs(np.fft.rfft(Hd)) ** 2
    freqs_axis = np.fft.rfftfreq(len(Hd), d=1.0)
    fig = go.Figure(go.Scatter(x=freqs_axis[1:], y=power[1:], mode="lines",
                               line=dict(color=TEAL)))
    fig.update_layout(height=320, plot_bgcolor="white", font=dict(size=14),
                      xaxis_title="frequency (cycles per sūra)", yaxis_title="power",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Power spectrum of the letter-entropy signal")
    st.plotly_chart(fig, width="stretch")

    peak_power = float(power[1:].max())
    _peak_i = int(np.argmax(power[1:])) + 1
    _peak_freq = float(freqs_axis[_peak_i])
    # lowest two non-DC bins = slow drift across the reading order, not a true cycle
    _is_trend = _peak_i <= 2
    nd = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                          key="_sig_spec_nd")
    if st.button("▶ Test spectral peak vs shuffled null", type="primary",
                 key="_sig_spec_btn"):
        st.session_state["_sig_spec_run"] = nd
    if st.session_state.get("_sig_spec_run"):
        rng = np.random.default_rng(7)
        nn = st.session_state["_sig_spec_run"]
        out = np.empty(nn)
        base = Hd.copy()
        for j in range(nn):
            rng.shuffle(base)
            out[j] = float((np.abs(np.fft.rfft(base)) ** 2)[1:].max())
        p = (np.sum(out >= peak_power) + 1) / (nn + 1)
        if p < .05:
            _verdict = ("✓ slow trend (low-frequency)" if _is_trend
                        else "✓ periodic cycle beyond chance")
        else:
            _verdict = "✗ no structure beyond chance"
        st.metric("Peak-power p (vs shuffled order)", f"{p:.2g}", _verdict)
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
        fig.add_vline(x=peak_power, line=dict(color=RED, width=3),
                      annotation_text="observed peak", annotation_position="top")
        fig.update_layout(height=300, plot_bgcolor="white", font=dict(size=14),
                          xaxis_title="max spectral power", yaxis_title="count",
                          showlegend=False, margin=dict(l=10, r=10, t=40, b=10),
                          title=f"Spectral peak vs shuffled order → p ≈ {p:.2g}")
        st.plotly_chart(fig, width="stretch")
        if p < .05 and _is_trend:
            st.caption("The surviving peak sits at the lowest frequency — this is a slow "
                       "trend across the reading order, not a repeating cycle. The entropy "
                       "of sūras drifts gradually; there is no fixed-period carrier wave.")
        elif p < .05:
            st.caption("A mid-band peak survives the shuffle — a genuine repeating cycle "
                       "in how 'mixed' sūras are. Read the peak frequency to find its period.")
        else:
            st.caption("No peak beats the shuffled null — the entropy series behaves like "
                       "ordered noise, not a carrier wave.")


    st.divider()
    layer(2, "Wavelet multiresolution (Haar)")
    st.caption("The FFT asks 'which fixed cycle lengths'; a wavelet decomposition asks "
               "'how much variation lives at each SCALE' (2, 4, 8 … sūras). Pure Haar "
               "transform, no external library. A shuffle null flags any scale carrying "
               "more energy than chance.")

    def _haar_levels(x):
        x = np.asarray(x, dtype=float).copy()
        det = []
        while len(x) > 1:
            a = (x[0::2] + x[1::2]) / np.sqrt(2.0)
            d = (x[0::2] - x[1::2]) / np.sqrt(2.0)
            det.append(d); x = a
        return det

    def _level_energy(series):
        v = np.asarray(series, dtype=float) - np.mean(series)
        n2 = 1 << int(np.ceil(np.log2(len(v))))
        vp = np.zeros(n2); vp[:len(v)] = v
        return np.array([float(np.sum(d * d)) for d in _haar_levels(vp)])

    _en = _level_energy(H)
    _scales = [2 ** (k + 1) for k in range(len(_en))]
    wav_nd = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                              key="_sig_wav_nd")
    if st.button("▶ Test scale energies vs shuffled null", type="primary",
                 key="_sig_wav_btn"):
        st.session_state["_sig_wav"] = wav_nd
    if st.session_state.get("_sig_wav"):
        _rng = np.random.default_rng(11); _nn = st.session_state["_sig_wav"]
        _base = np.asarray(H, dtype=float)
        _null = np.empty((_nn, len(_en)))
        for _j in range(_nn):
            _null[_j] = _level_energy(_rng.permutation(_base))
        _pv = [(np.sum(_null[:, k] >= _en[k]) + 1) / (_nn + 1) for k in range(len(_en))]
        _colors = [TEAL if pp < .05 else GREY for pp in _pv]
        _wfig = go.Figure(go.Bar(x=[str(sc) for sc in _scales], y=_en, marker_color=_colors,
                                 text=[f"p={pp:.2g}" for pp in _pv], textposition="outside"))
        _wfig.update_layout(height=340, plot_bgcolor="white", font=dict(size=13),
                            xaxis_title="scale (sūras per detail coefficient)",
                            yaxis_title="detail energy", margin=dict(l=10, r=10, t=30, b=10),
                            title="Haar wavelet energy by scale — green = beyond shuffle null")
        st.plotly_chart(_wfig, width="stretch")
        st.caption("Green bars carry significantly more energy than a shuffled series "
                   "at that scale (p on each bar); grey bars do not. Significant coarse "
                   "scales reflect a slow trend across the reading order; significant fine "
                   "scales would indicate local periodicity.")
    else:
        st.info("Press Run to compare each scale's energy to a shuffled-series null.")


    st.divider()
    layer(3, "Wavelet scalogram (Ricker CWT) — where the structure sits")
    st.caption("A continuous wavelet transform localizes variation in BOTH scale and "
               "position: the heatmap shows, for each scale (rows) and sūra (columns), "
               "how strongly the entropy series varies there. Pure-numpy Ricker wavelet.")
    if st.button("▶ Build the scalogram", type="primary", key="_sig_cwt_btn"):
        st.session_state["_sig_cwt"] = True
    if st.session_state.get("_sig_cwt"):
        def _ricker(points, a):
            t = np.arange(points) - (points - 1) / 2.0
            amp = 2.0 / (np.sqrt(3 * a) * np.pi ** 0.25)
            return amp * (1 - (t / a) ** 2) * np.exp(-(t ** 2) / (2 * a ** 2))
        _x = np.asarray(H, dtype=float) - float(np.mean(H))
        _scales = np.arange(1, 33)
        _cwt = np.zeros((len(_scales), len(_x)))
        for _i, _a in enumerate(_scales):
            _pts = min(int(10 * _a) + 1, len(_x))
            _cwt[_i] = np.convolve(_x, _ricker(_pts, _a), mode="same")
        _xlab = "sūra position (nuzūl)" if order2.startswith("Nuzūl") else "sūra position (muṣḥaf)"
        _cfig = go.Figure(go.Heatmap(z=np.abs(_cwt), x=list(range(1, len(_x) + 1)),
                                     y=[int(a) for a in _scales], colorscale="Viridis",
                                     colorbar=dict(title="|coef|")))
        _cfig.update_layout(height=420, font=dict(size=13), plot_bgcolor="white",
                            xaxis_title=_xlab, yaxis_title="scale (sūras)",
                            margin=dict(l=10, r=10, t=30, b=10),
                            title="Ricker-wavelet scalogram of the entropy series")
        st.plotly_chart(_cfig, width="stretch")
        st.caption("Broad bright bands at large scales spanning the x-axis = the slow "
                   "trend; an isolated bright spot would mark a localized burst of "
                   "variation at a particular place and scale.")


# ═══════════ TAB 4 — VERSE RHYTHM ═══════════
with t_rhythm:
    layer(1, "The rhythm of āyah lengths")
    st.caption("Each āyah has a token length. Their distribution and per-sūra "
               "variability describe the text's 'rhythm' — short staccato sūras vs "
               "long flowing ones.")
    arr = np.array(AYAH_LEN)
    c1, c2, c3 = st.columns(3)
    c1.metric("Median āyah length (tokens)", int(np.median(arr)),
              help="Half of all verses are shorter than this many tokens, half longer.")
    c2.metric("Mean", f"{arr.mean():.1f}",
              help="Average tokens per āyah over the whole corpus; above the median = "
                   "a long right tail of very long verses.")
    c3.metric("Coefficient of variation", f"{arr.std()/arr.mean():.2f}",
              help="Std ÷ mean — relative spread of verse lengths. Higher = more uneven rhythm.")
    fig = go.Figure(go.Histogram(x=arr, nbinsx=50, marker_color=NAVY))
    fig.update_layout(height=320, plot_bgcolor="white", font=dict(size=14),
                      xaxis_title="tokens per āyah", yaxis_title="count",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Distribution of āyah lengths across the whole corpus")
    st.plotly_chart(fig, width="stretch")

    su = corpus.df[COL_SURAH].astype(int).tolist()
    per_sura_mean = {}
    per_sura_vals = {}
    for i, s in enumerate(su):
        per_sura_vals.setdefault(s, []).append(AYAH_LEN[i])
    means = [np.mean(per_sura_vals[s]) for s in range(1, 115)]
    fig = go.Figure(go.Bar(x=list(range(1, 115)), y=means, marker_color=AMBER,
                           text=[NAMEOF.get(s, "") for s in range(1, 115)],
                           hoverinfo="text+y"))
    fig.update_layout(height=300, plot_bgcolor="white", font=dict(size=13),
                      xaxis_title="sūra number", yaxis_title="mean āyah length",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Mean āyah length per sūra")
    st.plotly_chart(fig, width="stretch")
    try:
        _mh = int(np.argmax(means)) + 1; _ml = int(np.argmin(means)) + 1
        st.markdown(
            f"**📍 What to take from this chart:** mean verse length spans a "
            f"{means[_mh-1]/max(means[_ml-1], 1e-9):.0f}× range — from "
            f"{means[_mh-1]:.1f} tokens/āyah in sūra {_mh} ({NAMEOF.get(_mh, '')}) down "
            f"to {means[_ml-1]:.1f} in sūra {_ml} ({NAMEOF.get(_ml, '')}). Corpus-wide "
            f"the median āyah is {int(np.median(arr))} tokens with CV "
            f"{arr.std()/arr.mean():.2f} — long flowing verses and short staccato ones "
            f"are both real registers, not noise around one typical length."
        )
    except Exception:
        pass



# ═══════════ TAB 5 — CO-RECURRENCE (CROSS-CORRELATION) ═══════════
with t_xcorr:
    layer(1, "Do two roots co-occur with a directional lag?")
    st.caption("Mark each root's āyahs as a 1/0 signal, then cross-correlate the two. "
               "A peak at lag 0 means they share āyahs; a peak off zero means one tends "
               "to appear a few āyahs before/after the other. A circular-shift null — "
               "which preserves each signal's own clustering — tests the peak.")
    _xr = [r for r, _ in corpus.freq_norm.most_common(400)]
    _c1, _c2 = st.columns(2)
    a = _c1.selectbox("Root A", _xr, key="_sig_xa")
    b = _c2.selectbox("Root B", _xr, index=min(1, len(_xr) - 1), key="_sig_xb")
    n_ayah = len(corpus.df)
    asig = np.zeros(n_ayah); asig[sorted(corpus.index_norm.get(a, []))] = 1
    bsig = np.zeros(n_ayah); bsig[sorted(corpus.index_norm.get(b, []))] = 1
    if asig.sum() < 3 or bsig.sum() < 3:
        st.info("Need at least 3 occurrences of each root.")
    else:
        av = asig - asig.mean(); bv = bsig - bsig.mean()
        denom = np.sqrt((av * av).sum() * (bv * bv).sum()) or 1.0
        L = 15
        def _xc_vec(x, y):
            full = np.correlate(x, y, mode="full")
            cidx = len(x) - 1
            return full[cidx - L:cidx + L + 1]
        lags = list(range(-L, L + 1))
        xc = list(_xc_vec(av, bv) / denom)
        peak_i = int(np.argmax(np.abs(xc))); peak_lag = lags[peak_i]
        obs = max(abs(v) for v in xc)
        _fig = go.Figure(go.Bar(x=lags, y=xc, marker_color=TEAL))
        _fig.add_vline(x=0, line=dict(color=GREY, dash="dot"))
        _fig.update_layout(height=320, plot_bgcolor="white", font=dict(size=14),
                           xaxis_title="relative lag (āyahs)",
                           yaxis_title="normalized cross-correlation",
                           margin=dict(l=10, r=10, t=30, b=10),
                           title=f"Cross-correlation «{a}» × «{b}»")
        st.plotly_chart(_fig, width="stretch")
        _m1, _m2 = st.columns(2)
        _m1.metric("Peak lag (āyahs)", f"{peak_lag:+d}")
        _m2.metric("Peak correlation", f"{xc[peak_i]:+.3f}")
        _nd = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                               key="_sig_xc_nd")
        if st.button("▶ Test the peak vs a circular-shift null", type="primary",
                     key="_sig_xc_btn"):
            st.session_state["_sig_xc"] = (a, b, _nd)
        _run = st.session_state.get("_sig_xc")
        if _run and _run[0] == a and _run[1] == b:
            rng = np.random.default_rng(3); _n = _run[2]
            out = np.empty(_n)
            for j in range(_n):
                sh = np.roll(bsig, int(rng.integers(1, n_ayah)))
                shv = sh - sh.mean()
                d2 = np.sqrt((av * av).sum() * (shv * shv).sum()) or 1.0
                out[j] = float(np.max(np.abs(_xc_vec(av, shv) / d2)))
            p_xc = (np.sum(out >= obs) + 1) / (_n + 1)
            st.metric("Peak |cross-correlation| p", f"{p_xc:.2g}",
                      "✓ beyond chance" if p_xc < .05 else "n.s.")
            _f2 = go.Figure()
            _f2.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
            _f2.add_vline(x=obs, line=dict(color=RED, width=3),
                          annotation_text=f"observed |peak|={obs:.3f}",
                          annotation_position="top")
            _f2.update_layout(height=300, plot_bgcolor="white", font=dict(size=14),
                              xaxis_title="max |cross-correlation| under circular shift",
                              yaxis_title="count", showlegend=False,
                              margin=dict(l=10, r=10, t=40, b=10),
                              title=f"Peak vs circular-shift null → p ≈ {p_xc:.2g}")
            st.plotly_chart(_f2, width="stretch")
            st.caption("A significant peak means the two roots' āyah positions are "
                       "correlated beyond chance — usually shared themes or fixed "
                       "collocations, not a hidden code.")


# ═══════════════════ EXPORT THIS ANALYSIS ═══════════════════
st.divider()
st.markdown("### ⬇ Export this analysis")
import pandas as _pd
_sig_rows = []
for _s in range(1, 115):
    _sig_rows.append({
        "surah": _s, "name": NAMEOF.get(_s, ""),
        "verses": VERSES.get(_s, 0),
        "revelation_order": NUZ.get(_s, ""),
        "letter_entropy_bits": round(shannon_bits(LETTERS[_s].values()), 4),
    })
_sig_df = _pd.DataFrame(_sig_rows)
st.download_button("⬇ Per-sūra signal series (CSV)",
                   _sig_df.to_csv(index=False).encode("utf-8-sig"),
                   "signal_per_sura.csv", "text/csv", key="_sig_export_csv")
st.caption("Corpus-scoped export. Save any chart via its toolbar camera icon.")

st.caption("Computed live from the loaded corpus | permutation / Poisson nulls | "
           "exploratory scaffold, no 'scientific-miracle' claims. Part of the Two Books "
           "series alongside Disjoint Letters and Biology.")
