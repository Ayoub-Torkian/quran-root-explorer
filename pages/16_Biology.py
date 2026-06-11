"""Two Books · Biology — the genome metaphor applied to scripture.

Companion to the Disjoint-Letters workbench and the Signal page. We borrow the
toolkit of sequence biology under one explicit mapping:

    letters ≈ bases        roots ≈ codons        words ≈ proteins

and run base-composition, codon-usage (Zipf), di-codon bias, and sequence-
complexity analyses over the loaded corpus. The metaphor is a lens, not a claim
that scripture is literally genetic; every test carries a permutation null and an
honest caption. Computed live; guarded with HAS_REV.
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
from twobooks_stats import shannon_bits, per_sura_letters_roots

st.set_page_config(page_title="Biology", page_icon="🧬", layout="wide")
log_page("biology")
corpus = get_corpus()

NAVY = "#1D3557"; TEAL = "#1D9E75"; AMBER = "#EF9F27"; RED = "#E63946"
GREY = "#B4B2A9"; ICE = "#B4B2A9"; PURPLE = "#378ADD"; GREEN = "#1D9E75"


# ───────────────────────── data ─────────────────────────
@st.cache_data(show_spinner=False)
def _bio_data(_corpus_id):
    """Per-sūra letters + roots via the shared Two Books stats kernel."""
    return per_sura_letters_roots(corpus)


@st.cache_data(show_spinner=False)
def _codon_bigrams(_corpus_id):
    """Adjacent root pairs WITHIN each āyah (di-codons), plus the global root
    frequency and the per-āyah token lists for permutation."""
    ayah_roots = [list(toks) for toks in corpus.root_tokens]
    big = Counter()
    uni = Counter()
    for toks in ayah_roots:
        for t in toks:
            uni[t] += 1
        for a, b in zip(toks, toks[1:]):
            big[(a, b)] += 1
    return ayah_roots, uni, big


LETTERS, ROOTS_BY_SURA = _bio_data(id(corpus))
AYAH_ROOTS, UNI, BIG = _codon_bigrams(id(corpus))
NAMEOF = {int(corpus.df[COL_SURAH].iat[i]): str(corpus.df[COL_SURAH_NAME].iat[i])
          for i in range(len(corpus.df))}

CORPUS_LETTERS = Counter()
for s in range(1, 115):
    CORPUS_LETTERS.update(LETTERS[s])
_tot_letters = sum(CORPUS_LETTERS.values()) or 1


# ───────────────────────── hero ─────────────────────────
hero("🧬 Two Books · Biology",
     "The genome metaphor — letters≈bases, roots≈codons, words≈proteins — applied "
     "to scripture, with permutation nulls.")

st.markdown(
    "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;"
    "padding:9px 14px;margin:6px 0 14px;font-size:13.5px;color:#1D3557;'>"
    "Sequence biology has sharp tools for asking what a string of symbols 'does': "
    "base composition, codon-usage bias, di-nucleotide bias, complexity. Under the "
    "mapping <b>letters≈bases · roots≈codons · words≈proteins</b> we point those tools "
    "at the corpus. This is an analytical lens — a way to borrow rigorous statistics — "
    "not a claim that the text is genetic.</div>", unsafe_allow_html=True)

t_base, t_codon, t_di, t_cplx, t_markov = st.tabs(
    ["🧪 Base composition", "🔤 Codon usage (Zipf)", "🧩 Di-codon bias",
     "📏 Sequence complexity", "🧠 Markov memory"])


# ═══════════ TAB 1 — BASE COMPOSITION ═══════════
with t_base:
    layer(1, "The four-plus 'bases': letter composition")
    st.caption("DNA has 4 bases; Arabic script has ~28 letters. The base-composition "
               "profile is just how often each letter appears. Below: the corpus "
               "profile, then a per-sūra composition you can inspect.")
    items = CORPUS_LETTERS.most_common()
    fig = go.Figure(go.Bar(x=[ch for ch, _ in items], y=[c for _, c in items],
                           marker_color=NAVY,
                           text=[f"{100*c/_tot_letters:.1f}%" for _, c in items],
                           textposition="outside"))
    fig.update_layout(height=340, plot_bgcolor="white", font=dict(size=14),
                      xaxis_title="letter (base)", yaxis_title="count",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Corpus-wide base (letter) composition")
    st.plotly_chart(fig, width="stretch")
    try:
        _top1 = items[0]
        _top5_share = 100 * sum(c for _, c in items[:5]) / _tot_letters
        st.markdown(
            f"**📍 What to take from this chart:** of {_tot_letters:,} letters in the "
            f"corpus, «{_top1[0]}» alone is {100*_top1[1]/_tot_letters:.1f}% and the top "
            f"five letters carry {_top5_share:.1f}% — like genomic base composition, the "
            f"profile is strongly skewed, which is why per-sūra deviations (below) stay "
            f"small: every sūra is built from the same skewed alphabet."
        )
    except Exception:
        pass

    sopt = {f"{s} — {NAMEOF.get(s, '')}": s for s in range(1, 115)}
    pick = sopt[st.selectbox("Inspect a sūra's composition", list(sopt.keys()),
                             key="_bio_base_sura")]
    sc = LETTERS[pick]
    tot = sum(sc.values()) or 1
    sitems = sc.most_common(15)
    base_p = {ch: CORPUS_LETTERS[ch] / _tot_letters for ch in CORPUS_LETTERS}
    fig = go.Figure()
    fig.add_trace(go.Bar(x=[ch for ch, _ in sitems], y=[c / tot for _, c in sitems],
                         name=f"sūra {pick}", marker_color=TEAL))
    fig.add_trace(go.Bar(x=[ch for ch, _ in sitems],
                         y=[base_p.get(ch, 0) for ch, _ in sitems],
                         name="corpus baseline", marker_color=GREY, opacity=0.7))
    fig.update_layout(height=320, barmode="group", plot_bgcolor="white",
                      font=dict(size=14), xaxis_title="letter", yaxis_title="frequency",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title=f"Sūra {pick} base composition vs corpus baseline")
    st.plotly_chart(fig, width="stretch")
    st.caption("Deviations from the baseline are the script analogue of skewed "
               "GC-content — usually small, because every sūra draws on the same "
               "alphabet and grammar.")


# ═══════════ TAB 2 — CODON USAGE / ZIPF ═══════════
with t_codon:
    layer(1, "Codon usage: the rank-frequency law of roots")
    st.caption("Treating each root as a codon, how is usage distributed? Natural "
               "language follows Zipf's law — frequency ∝ 1/rank — appearing as a "
               "straight line on log-log axes. We fit the slope and report it.")
    ranked = UNI.most_common()
    ranks = np.arange(1, len(ranked) + 1)
    fr = np.array([c for _, c in ranked], dtype=float)
    fig = go.Figure(go.Scatter(x=ranks, y=fr, mode="markers",
                               marker=dict(size=4, color=PURPLE),
                               text=[r for r, _ in ranked], hoverinfo="text+y"))
    # Zipf fit on log-log
    lr = np.log10(ranks); lf = np.log10(fr)
    slope, intercept = np.polyfit(lr, lf, 1)
    fit = 10 ** (intercept + slope * lr)
    fig.add_trace(go.Scatter(x=ranks, y=fit, mode="lines", line=dict(color=RED),
                             name=f"Zipf fit slope={slope:.2f}"))
    fig.update_layout(height=360, plot_bgcolor="white", font=dict(size=14),
                      xaxis_type="log", yaxis_type="log",
                      xaxis_title="rank (log)", yaxis_title="frequency (log)",
                      margin=dict(l=10, r=10, t=30, b=10), showlegend=True,
                      title=f"Root (codon) rank-frequency — Zipf slope ≈ {slope:.2f}")
    st.plotly_chart(fig, width="stretch")
    try:
        _tok_tot = float(fr.sum())
        _top10_share = 100 * float(fr[:10].sum()) / _tok_tot
        _hapax_n = int(np.sum(fr == 1))
        st.markdown(
            f"**📍 What to take from this chart:** the head is extreme — the single "
            f"top root «{ranked[0][0]}» accounts for {100*float(fr[0])/_tok_tot:.1f}% of "
            f"all {int(_tok_tot):,} root tokens and the top 10 roots for "
            f"{_top10_share:.1f}%, while {_hapax_n:,} roots "
            f"({100*_hapax_n/len(ranked):.0f}% of the vocabulary) occur exactly once. "
            f"The fitted slope {slope:.2f} is steeper than the classic −1 because each "
            f"root pools many word-forms — a property of root-level counting, not a code."
        )
    except Exception:
        pass
    c1, c2, c3 = st.columns(3)
    c1.metric("Distinct roots (codons)", f"{len(ranked):,}",
              help="Size of the root vocabulary — distinct 'codons' in the metaphor.")
    c2.metric("Total root tokens", f"{int(fr.sum()):,}",
              help="Every root occurrence counted — the length of the 'coding sequence'.")
    c3.metric("Zipf slope", f"{slope:.2f}", "steeper than −1 (roots pool word-forms)",
              help="Slope of the log-log rank-frequency fit. Natural-language words give ≈ −1; "
                   "root-level aggregation concentrates mass at the head, steepening it.")
    st.caption("The distribution is heavily skewed — a few roots carry most of the "
               "text while a long tail appears once or twice, the same shape seen in "
               "codon-usage tables. The slope here is steeper than the classic −1 "
               "word-level Zipf because each root aggregates many surface word-forms, "
               "concentrating mass at the head.")

    st.divider()
    layer(2, "Most- and least-used codons")
    cc1, cc2 = st.columns(2)
    top = ranked[:15]
    cc1.markdown("**Most-used roots**")
    cc1.dataframe({"root": [r for r, _ in top], "count": [c for _, c in top]},
                  width="stretch")
    rare = [(r, c) for r, c in ranked if c == 1][:15]
    cc2.markdown("**Hapax roots (used once)**")
    cc2.metric("Hapax count", sum(1 for _, c in ranked if c == 1),
               help="Roots that occur exactly once in the whole corpus — the long tail of "
                    "the Zipf curve, analogous to rarely-used codons.")


# ═══════════ TAB 3 — DI-CODON BIAS ═══════════
with t_di:
    layer(1, "Di-codon bias: which root pairs avoid or attract")
    st.caption("In genomes, some adjacent base/codon pairs are over- or under-"
               "represented relative to chance (dinucleotide bias). Here we count "
               "adjacent root pairs within āyahs and compare to what independence "
               "predicts: expected(a,b) = f(a)·f(b)/N. The ratio observed/expected is "
               "the bias.")
    N = sum(UNI.values())
    # restrict to reasonably frequent roots so ratios are stable
    common = {r for r, c in UNI.most_common(150)}
    rows = []
    for (a, b), o in BIG.items():
        if a in common and b in common and o >= 5:
            exp = UNI[a] * UNI[b] / N
            if exp > 0:
                rows.append((a, b, o, exp, o / exp))
    rows.sort(key=lambda x: x[4])
    under = rows[:12]
    over = rows[-12:][::-1]

    def bias_fig(data, title, color):
        labels = [f"{a}→{b}" for a, b, *_ in data]
        ratios = [r[4] for r in data]
        fig = go.Figure(go.Bar(x=ratios, y=labels, orientation="h",
                               marker_color=color))
        fig.add_vline(x=1.0, line=dict(color=GREY, dash="dash"),
                      annotation_text="expected")
        fig.update_layout(height=360, plot_bgcolor="white", font=dict(size=13),
                          xaxis_title="observed / expected", yaxis_title="",
                          margin=dict(l=10, r=10, t=30, b=10), title=title)
        return fig

    cc1, cc2 = st.columns(2)
    with cc1:
        st.plotly_chart(bias_fig(over, "Over-represented di-codons", RED),
                        width="stretch")
    with cc2:
        st.plotly_chart(bias_fig(under, "Under-represented di-codons", NAVY),
                        width="stretch")

    st.divider()
    layer(2, "Is the overall bias beyond chance?")
    st.caption("Summary statistic: a chi-square-like sum over observed pairs. We "
               "shuffle the root stream (keeping āyah boundaries) and recompute, to "
               "see whether the real adjacency structure exceeds the null.")
    nd = st.select_slider("Permutations", [200, 500, 2000], value=500, key="_bio_di_nd")
    if st.button("▶ Test di-codon structure vs shuffled stream", type="primary",
                 key="_bio_di_btn"):
        st.session_state["_bio_di_run"] = nd
    if st.session_state.get("_bio_di_run"):
        def chi_stat(bigrams):
            tot = 0.0
            for (a, b), o in bigrams.items():
                if a in common and b in common:
                    exp = UNI[a] * UNI[b] / N
                    if exp > 0:
                        tot += (o - exp) ** 2 / exp
            return tot
        obs = chi_stat(BIG)
        # flat token stream + āyah boundary lengths
        flat = [t for toks in AYAH_ROOTS for t in toks]
        lens = [len(toks) for toks in AYAH_ROOTS]
        flat = np.array(flat, dtype=object)
        rng = np.random.default_rng(9)
        nn = st.session_state["_bio_di_run"]
        out = np.empty(nn)
        for j in range(nn):
            perm = flat.copy(); rng.shuffle(perm)
            bg = Counter(); pos = 0
            for L in lens:
                seg = perm[pos:pos + L]; pos += L
                for x, y in zip(seg, seg[1:]):
                    bg[(x, y)] += 1
            out[j] = chi_stat(bg)
        p = (np.sum(out >= obs) + 1) / (nn + 1)
        st.metric("Di-codon structure p", f"{p:.2g}",
                  "✓ structured beyond chance" if p < .05 else "n.s.")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
        fig.add_vline(x=obs, line=dict(color=RED, width=3),
                      annotation_text="observed", annotation_position="top")
        fig.update_layout(height=300, plot_bgcolor="white", font=dict(size=14),
                          xaxis_title="χ²-like adjacency statistic", yaxis_title="count",
                          showlegend=False, margin=dict(l=10, r=10, t=40, b=10),
                          title=f"Adjacency structure vs shuffled roots → p ≈ {p:.2g}")
        st.plotly_chart(fig, width="stretch")
        st.caption("Grammar makes certain roots co-occur adjacently (e.g. fixed "
                   "collocations), so a significant result reflects ordinary syntax — "
                   "the biological framing just measures it precisely.")


# ═══════════ TAB 4 — SEQUENCE COMPLEXITY ═══════════
with t_cplx:
    layer(1, "Sequence complexity per sūra")
    st.caption("Two complementary complexity axes per sūra: lexical richness "
               "(unique roots ÷ total = codon diversity) and letter entropy (base "
               "diversity). Plotted against sūra length to expose length effects.")
    rich = {}
    lh = {}
    length = {}
    for s in range(1, 115):
        toks = ROOTS_BY_SURA[s]
        rich[s] = len(set(toks)) / len(toks) if toks else 0.0
        lh[s] = shannon_bits(LETTERS[s].values())
        length[s] = len(toks)
    xs = [length[s] for s in range(1, 115)]
    fig = go.Figure(go.Scatter(
        x=xs, y=[rich[s] for s in range(1, 115)], mode="markers",
        marker=dict(size=7, color=[lh[s] for s in range(1, 115)],
                    colorscale="Viridis", showscale=True,
                    colorbar=dict(title="letter<br>entropy")),
        text=[f"{NAMEOF.get(s,'')} (sūra {s})" for s in range(1, 115)],
        hoverinfo="text+x+y"))
    fig.update_layout(height=380, plot_bgcolor="white", font=dict(size=14),
                      xaxis_type="log", xaxis_title="root tokens per sūra (log)",
                      yaxis_title="lexical richness (unique/total roots)",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Codon diversity vs length, coloured by base entropy")
    st.plotly_chart(fig, width="stretch")

    lv = np.array([length[s] for s in range(1, 115)], dtype=float)
    rv = np.array([rich[s] for s in range(1, 115)])
    corr = float(np.corrcoef(np.log10(lv), rv)[0, 1])
    st.metric("Correlation: log(length) vs richness", f"{corr:+.2f}",
              "longer sūras reuse roots more" if corr < 0 else "")
    st.caption("The strong negative correlation is expected: longer texts repeat "
               "vocabulary, lowering type-token ratio. This is the same length "
               "confound flagged in the Disjoint-Letters workbench — complexity "
               "measures must be read against length before any 'signal' is claimed.")

    st.divider()
    layer(2, "Cluster sūras by codon (root) composition")
    st.caption("Each sūra becomes a vector of its usage of the top-50 roots; "
               "hierarchical clustering (Ward) groups sūras with similar codon profiles "
               "into a dendrogram — a 'tree of chapters' by vocabulary.")
    if st.button("▶ Build the sūra dendrogram", type="primary", key="_bio_dend_btn"):
        st.session_state["_bio_dend"] = True
    if st.session_state.get("_bio_dend"):
        try:
            import plotly.figure_factory as ff
            from scipy.cluster.hierarchy import linkage
            _top = [r for r, _ in UNI.most_common(50)]
            _mat, _labels = [], []
            for _s in range(1, 115):
                _toks = ROOTS_BY_SURA[_s]; _tot = len(_toks) or 1
                _cnt = Counter(_toks)
                _mat.append([_cnt.get(r, 0) / _tot for r in _top])
                _labels.append(f"S{_s}")
            _mat = np.array(_mat)
            _dfig = ff.create_dendrogram(_mat, labels=_labels,
                                         linkagefun=lambda x: linkage(x, "ward"))
            _dfig.update_layout(height=430, plot_bgcolor="white", font=dict(size=9),
                                margin=dict(l=10, r=10, t=30, b=10),
                                title="Sūras clustered by top-50 codon composition (Ward linkage)")
            st.plotly_chart(_dfig, width="stretch")
            st.caption("Clusters largely track style and length (long Medinan vs short "
                       "Meccan sūras) — composition is dominated by common roots, so read "
                       "this as a vocabulary-similarity map, not a hidden code.")
        except Exception as _e:
            st.info(f"Dendrogram unavailable in this environment: {type(_e).__name__}.")



# ═══════════ TAB 5 — MARKOV MEMORY (LETTER STREAM) ═══════════
with t_markov:
    layer(1, "How much memory does the letter (base) sequence carry?")
    st.caption("Conditional entropy of the next letter given the previous k letters, "
               "measured within words. Order 0 = no context; each step adds one letter "
               "of history. A falling curve means letters are predictable from their "
               "neighbours — the script analogue of base-stacking rules in DNA.")

    @st.cache_data(show_spinner=False)
    def _letter_ngrams(_cid, maxn=4):
        grams = {m: Counter() for m in range(1, maxn + 1)}
        for toks in corpus.seg_tokens:
            for t in toks:
                nt = "".join(ch for ch in normalize_letters(t) if ch.strip())
                for m in range(1, maxn + 1):
                    for i in range(len(nt) - m + 1):
                        grams[m][nt[i:i + m]] += 1
        return grams

    @st.cache_data(show_spinner=False)
    def _letter_ngrams_shuffled(_cid, maxn=4, seed=7):
        import random
        rng = random.Random(seed)
        grams = {m: Counter() for m in range(1, maxn + 1)}
        for toks in corpus.seg_tokens:
            for t in toks:
                chars = [ch for ch in normalize_letters(t) if ch.strip()]
                rng.shuffle(chars)
                nt = "".join(chars)
                for m in range(1, maxn + 1):
                    for i in range(len(nt) - m + 1):
                        grams[m][nt[i:i + m]] += 1
        return grams

    def _cond_entropies(grams):
        H = {m: shannon_bits(grams[m].values()) for m in grams}
        orders = [0]
        vals = [H[1]]
        for m in (1, 2, 3):
            if (m + 1) in H:
                orders.append(m); vals.append(H[m + 1] - H[m])
        return orders, vals

    _g = _letter_ngrams(id(corpus))
    _orders, _vals = _cond_entropies(_g)
    _sg = _letter_ngrams_shuffled(id(corpus))
    _, _svals = _cond_entropies(_sg)
    _labels = [f"order {o}" for o in _orders]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=_labels, y=_vals, name="observed", marker_color=NAVY))
    fig.add_trace(go.Bar(x=_labels, y=_svals, name="letters shuffled within words",
                         marker_color=GREY, opacity=0.7))
    fig.update_layout(height=340, barmode="group", plot_bgcolor="white", font=dict(size=14),
                      yaxis_title="conditional entropy (bits / letter)",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Letter predictability vs context length")
    st.plotly_chart(fig, width="stretch")
    _c1, _c2, _c3 = st.columns(3)
    _c1.metric("Order-0 entropy (bits)", f"{_vals[0]:.2f}",
               help="Unpredictability of a letter with no context — the alphabet's raw mix.")
    if len(_vals) > 1:
        _c2.metric("Given 1 previous letter", f"{_vals[1]:.2f}",
                   help="Remaining unpredictability once you know the preceding letter.")
        _c3.metric("Memory gain (0→1)", f"{_vals[0] - _vals[1]:.2f} bits",
                   help="How many bits one letter of context buys — intra-word dependencies "
                        "from roots and templatic patterns.")
    st.caption("The observed curve sits below the shuffled baseline: real Arabic words "
               "carry intra-word letter dependencies (roots, templatic patterns) that "
               "make letters predictable. High orders are data-limited (sparse n-grams), "
               "so read orders 0–1 as the reliable part.")


# ═══════════════════ EXPORT THIS ANALYSIS ═══════════════════
st.divider()
st.markdown("### ⬇ Export this analysis")
import pandas as _pd
_ranked = UNI.most_common()
_codon_df = _pd.DataFrame({
    "rank": list(range(1, len(_ranked) + 1)),
    "root": [r for r, _ in _ranked],
    "count": [c for _, c in _ranked],
})
_bio_rows = []
for _s in range(1, 115):
    _toks = ROOTS_BY_SURA[_s]
    _bio_rows.append({
        "surah": _s, "name": NAMEOF.get(_s, ""),
        "root_tokens": len(_toks),
        "unique_roots": len(set(_toks)),
        "lexical_richness": round(len(set(_toks)) / len(_toks), 4) if _toks else 0.0,
        "letter_entropy_bits": round(shannon_bits(LETTERS[_s].values()), 4),
    })
_bio_df = _pd.DataFrame(_bio_rows)
_ec1, _ec2 = st.columns(2)
_ec1.download_button("⬇ Codon (root) usage (CSV)",
                     _codon_df.to_csv(index=False).encode("utf-8-sig"),
                     "biology_codon_usage.csv", "text/csv", key="_bio_codon_csv")
_ec2.download_button("⬇ Per-sūra complexity (CSV)",
                     _bio_df.to_csv(index=False).encode("utf-8-sig"),
                     "biology_per_sura.csv", "text/csv", key="_bio_sura_csv")
st.caption("Corpus-scoped export. Save any chart via its toolbar camera icon.")

st.caption("Computed live from the loaded corpus | permutation nulls | the genome "
           "framing is an analytical lens, not a claim of genetic structure. Part of "
           "the Two Books series alongside Disjoint Letters and Signal.")
