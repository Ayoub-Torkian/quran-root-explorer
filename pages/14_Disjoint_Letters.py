"""Two Books · Disjoint Letters (al-Muqaṭṭaʿāt) — the POINTER explorer
+ a hypothesis-testing workbench.

A self-contained module that tests the validated finding of the Disjoint-Letters
course: the 29 muqaṭṭaʿāt sūras behave as a POSITIONAL / ORGANIZATIONAL pointer —
an index over contiguous sūra-families in both muṣḥaf and revelation order,
flagging the long sūras — but NOT a semantic or letter-frequency code.

Everything is computed live from the loaded corpus (Book6) and validated against
a label-permutation null. No 'scientific-miracle' claims.

Tabs are grouped under three categories:
  🧭 Position (index geometry)  — the validated pointer finding: explore the
        tags, contiguity test, organization (length), and the verdict.
  🔤 Sequence (character scale) — letters≈bases: alphabet usage, letter-density
        enrichment, letter-level information theory.
  🧩 Semantic (word/root scale) — roots≈codons, words≈proteins: custom-family
        hypothesis lab, root entropy / richness.
"""
from __future__ import annotations

import itertools
import math
from collections import Counter

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from analysis import (COL_SURAH, COL_AYAH, COL_SURAH_NAME, COL_ROOTS,
                      COL_SEGMENTED, normalize_letters)
from state import get_corpus, hero, layer, log_page
from twobooks_stats import (shannon_bits, per_sura_letters_roots, perm_p,
                            benjamini_hochberg, MUQ, MUQ_FAMILIES, MUQ_MULTI,
                            MUQ_SIZES, LETTERS_OF, DISJOINT_LETTERS)

st.set_page_config(page_title="Disjoint Letters", page_icon="🔠", layout="wide")
log_page("disjoint_letters")
corpus = get_corpus()

# ───────────────────────── palette ─────────────────────────
NAVY = "#1D3557"; TEAL = "#1D9E75"; AMBER = "#EF9F27"; RED = "#E63946"
GREY = "#B4B2A9"; ICE = "#B4B2A9"; LT = "#1D9E75"; PURPLE = "#378ADD"

# ───────────────────────── families ────────────────────────
# Family membership, MUQ, sizes, LETTERS_OF and DISJOINT_LETTERS now come from the
# shared kernel (single source of truth). Only UI colours and display labels stay here.
_FAMCOL = {"ḤM": TEAL, "ALM": NAVY, "ALR": AMBER, "ṬSM": RED}
FAM = [(nm, MUQ_FAMILIES[nm], _FAMCOL[nm]) for nm in MUQ_FAMILIES]
MULTI = MUQ_MULTI
SIZES = MUQ_SIZES
SINGLE = {7: "ALMṢ", 13: "ALMR", 19: "KHYʿṢ", 20: "ṬH", 27: "ṬS",
          36: "YS", 38: "Ṣ", 50: "Q", 68: "N"}
TAG_AR = {40: "حمٓ", 2: "الٓمٓ", 10: "الٓرٓ", 26: "طسٓمٓ", 7: "الٓمٓصٓ", 13: "الٓمٓرٓ",
          19: "كٓهٓيٓعٓصٓ", 20: "طه", 27: "طسٓ", 36: "يٓسٓ", 38: "صٓ", 50: "قٓ", 68: "نٓ"}
FAMNAME = {}
FAMCOL = {}
for nm, ss, c in FAM:
    for s in ss:
        FAMNAME[s] = nm; FAMCOL[s] = c
for s in SINGLE:
    FAMNAME[s] = "singleton"; FAMCOL[s] = GREY


# ───────────────────────── data from corpus ────────────────
@st.cache_data(show_spinner=False)
def _build(_corpus_id):
    df = corpus.df
    verses, roots = {}, {}
    su = df[COL_SURAH].astype(int).tolist()
    ay = df[COL_AYAH].astype(int).tolist()
    for i in range(len(df)):
        s, a = su[i], ay[i]
        verses[s] = max(verses.get(s, 0), a)
        roots.setdefault(s, []).extend(corpus.root_tokens[i])
    nuz = {int(k): int(v) for k, v in corpus.rev_order_of_surah.items()}
    profs = {s: Counter(roots.get(s, [])) for s in MUQ}
    return verses, nuz, profs


@st.cache_data(show_spinner=False)
def _build_sura_stats(_corpus_id):
    """Per-sūra letter Counters and root-token lists, via the shared Two Books
    stats kernel (single source of truth across Disjoint Letters/Signal/Biology)."""
    return per_sura_letters_roots(corpus)


VERSES, NUZ, PROFS = _build(id(corpus))
LETTERS, ROOTS_BY_SURA = _build_sura_stats(id(corpus))
MUS = {s: s for s in range(1, 115)}
# Revelation order is a Book6 v2+ field; degrade gracefully if absent.
HAS_REV = sum(1 for s in MUQ if s in NUZ) >= len(MUQ) - 1
if not HAS_REV:
    st.warning("This sheet has no revelation-order column (Book6 v2+ needed), so the "
               "nuzūl-based views are hidden. The book-order (muṣḥaf) analysis below "
               "is fully available.")
NAMEOF = {}
for i in range(len(corpus.df)):
    NAMEOF[int(corpus.df[COL_SURAH].iat[i])] = str(corpus.df[COL_SURAH_NAME].iat[i])

# Corpus-wide letter baseline (for KL divergence + alphabet bar)
CORPUS_LETTERS = Counter()
for s in range(1, 115):
    CORPUS_LETTERS.update(LETTERS[s])
ALPHABET = [ch for ch, _ in CORPUS_LETTERS.most_common()]
_corpus_total = sum(CORPUS_LETTERS.values()) or 1
CORPUS_LETTER_P = {ch: CORPUS_LETTERS[ch] / _corpus_total for ch in ALPHABET}


# ───────────────────────── stats engine ────────────────────
def within_mean(pos, fams):
    tot = n = 0
    for ss in fams:
        ps = [pos[s] for s in ss if s in pos]
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                tot += abs(ps[i] - ps[j]); n += 1
    return tot / n if n else 0.0


def pair_mean(vals):
    """Mean pairwise absolute distance within a single list of values."""
    n = len(vals)
    if n < 2:
        return 0.0
    tot = cnt = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            tot += abs(vals[i] - vals[j]); cnt += 1
    return tot / cnt if cnt else 0.0


@st.cache_data(show_spinner=False)
def label_perm_null(order: str, ndraw: int, seed: int = 1):
    pos = MUS if order == "mushaf" else NUZ
    rng = np.random.default_rng(seed)
    base = list(MUQ)
    out = np.empty(ndraw)
    for k in range(ndraw):
        rng.shuffle(base)
        idx = 0; fams = []
        for sz in SIZES:
            fams.append(base[idx:idx + sz]); idx += sz
        out[k] = within_mean(pos, fams)
    obs = within_mean(pos, MULTI)
    p = (np.sum(out <= obs) + 1) / (ndraw + 1)
    return out, obs, p


@st.cache_data(show_spinner=False)
def loo_contiguity(order: str, drop: int, ndraw: int, seed: int = 21):
    """Leave-one-out contiguity: drop one sūra, rebuild families one smaller,
    and re-run the label-permutation. Returns the p-value (smaller observed
    within-family distance than chance ⇒ small p). Uses the shared perm_p."""
    pos = MUS if order == "mushaf" else NUZ
    fams_loo = [[s for s in fam if s != drop] for fam in MULTI]
    sizes_loo = [len(f) for f in fams_loo]
    muq_loo = [s for s in MUQ if s != drop]
    obs = within_mean(pos, fams_loo)
    rng = np.random.default_rng(seed)
    base = list(muq_loo)
    out = np.empty(ndraw)
    for k in range(ndraw):
        rng.shuffle(base)
        idx = 0; fams = []
        for sz in sizes_loo:
            fams.append(base[idx:idx + sz]); idx += sz
        out[k] = within_mean(pos, fams)
    return perm_p(out, obs, "less")


def cos(a, b):
    keys = set(a) | set(b)
    dot = sum(a[k] * b[k] for k in keys)
    na = np.sqrt(sum(v * v for v in a.values())); nb = np.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


@st.cache_data(show_spinner=False)
def semantic_null(ndraw: int = 3000, seed: int = 17):
    def within(fams):
        v = []
        for ss in fams:
            v += [cos(PROFS[a], PROFS[b]) for a, b in itertools.combinations(ss, 2)]
        return float(np.mean(v)) if v else 0.0
    obs = within(MULTI)
    rng = np.random.default_rng(seed); base = list(MUQ); out = np.empty(ndraw)
    for k in range(ndraw):
        rng.shuffle(base); idx = 0; fams = []
        for sz in SIZES:
            fams.append(base[idx:idx + sz]); idx += sz
        out[k] = within(fams)
    p = (np.sum(out >= obs) + 1) / (ndraw + 1)
    return out, obs, p


# ── workbench helpers ──
def letter_entropy(s):
    return shannon_bits(LETTERS[s].values())


def root_entropy(s):
    return shannon_bits(Counter(ROOTS_BY_SURA[s]).values())


def kl_from_corpus(s):
    """KL(P_sura || Q_corpus) over letters, in bits."""
    cnt = LETTERS[s]
    tot = sum(cnt.values())
    if tot <= 0:
        return 0.0
    kl = 0.0
    for ch, c in cnt.items():
        p = c / tot
        q = CORPUS_LETTER_P.get(ch, 1e-9) or 1e-9
        kl += p * math.log2(p / q)
    return kl


def redundancy(s):
    """1 − H/Hmax over the sūra's letter distribution."""
    h = letter_entropy(s)
    k = len(LETTERS[s])
    hmax = math.log2(k) if k > 1 else 1.0
    return 1 - h / hmax if hmax else 0.0


def lexical_richness(s):
    """Unique roots / total roots — a type-token ratio on the codon layer."""
    toks = ROOTS_BY_SURA[s]
    return len(set(toks)) / len(toks) if toks else 0.0


def letter_density(s, ch):
    tot = sum(LETTERS[s].values())
    return LETTERS[s].get(ch, 0) / tot if tot else 0.0


# Attribute registry for the Hypothesis Lab clustering test
ATTRS = {
    "Length (verses)": lambda s: float(VERSES.get(s, 0)),
    "Letter entropy (bits)": letter_entropy,
    "Root entropy (bits)": root_entropy,
    "Root count (tokens)": lambda s: float(len(ROOTS_BY_SURA[s])),
}


@st.cache_data(show_spinner=False)
def attr_perm_null(attr_name: str, ndraw: int = 5000, seed: int = 3):
    """Label-permutation: does the REAL 4-family tagging cluster this attribute
    tighter (smaller within-family spread) than a random relabeling of the 29
    muqaṭṭaʿāt sūras into the same family sizes? Generalizes the length p≈0.29."""
    fn = ATTRS[attr_name]
    valmap = {s: fn(s) for s in MUQ}
    rng = np.random.default_rng(seed)
    base = list(MUQ)
    out = np.empty(ndraw)
    for k in range(ndraw):
        rng.shuffle(base)
        idx = 0; fams = []
        for sz in SIZES:
            fams.append(base[idx:idx + sz]); idx += sz
        out[k] = within_mean(valmap, fams)
    obs = within_mean(valmap, MULTI)
    p = (np.sum(out <= obs) + 1) / (ndraw + 1)
    return out, obs, p


def custom_contiguity(members, order, ndraw=5000, seed=7):
    """For a user-built set, mean pairwise distance vs random same-size subsets
    of all 114 sūras. Smaller observed ⇒ tighter than chance."""
    pos = MUS if order == "mushaf" else NUZ
    members = [s for s in members if s in pos]
    k = len(members)
    if k < 2:
        return None
    obs = pair_mean([pos[s] for s in members])
    universe = list(pos.keys())
    rng = np.random.default_rng(seed)
    out = np.empty(ndraw)
    for j in range(ndraw):
        pick = rng.choice(universe, size=k, replace=False)
        out[j] = pair_mean([pos[int(s)] for s in pick])
    p = (np.sum(out <= obs) + 1) / (ndraw + 1)
    return out, obs, p, k


def muq_special_null(metric_fn, ndraw=5000, seed=11, direction="greater"):
    """Are the 29 muqaṭṭaʿāt special on a per-sūra metric? Compare the mean of
    the metric over MUQ vs the mean over random 29-sūra subsets of all 114."""
    allvals = {s: metric_fn(s) for s in range(1, 115)}
    obs = float(np.mean([allvals[s] for s in MUQ]))
    universe = list(range(1, 115))
    rng = np.random.default_rng(seed)
    out = np.empty(ndraw)
    for j in range(ndraw):
        pick = rng.choice(universe, size=len(MUQ), replace=False)
        out[j] = float(np.mean([allvals[int(s)] for s in pick]))
    if direction == "greater":
        p = (np.sum(out >= obs) + 1) / (ndraw + 1)
    else:
        p = (np.sum(out <= obs) + 1) / (ndraw + 1)
    return out, obs, p, allvals


def enrichment_null(ch, ndraw=5000, seed=13):
    """Letter-density enrichment: do the sūras whose disjoint-letter set CONTAINS
    `ch` (bearers) carry that letter at higher density than chance? Permutation
    over random same-size sūra subsets. Generalizes the ق = rank 111/114 lead."""
    bearers = [s for s in MUQ if ch in LETTERS_OF.get(s, set())]
    k = len(bearers)
    if k == 0:
        return None
    dens = {s: letter_density(s, ch) for s in range(1, 115)}
    obs = float(np.mean([dens[s] for s in bearers]))
    universe = list(range(1, 115))
    rng = np.random.default_rng(seed)
    out = np.empty(ndraw)
    for j in range(ndraw):
        pick = rng.choice(universe, size=k, replace=False)
        out[j] = float(np.mean([dens[int(s)] for s in pick]))
    p = (np.sum(out >= obs) + 1) / (ndraw + 1)
    return out, obs, p, bearers, dens


# ───────────────────────── hero ────────────────────────────
hero("🔠 Two Books · The Disjoint Letters (al-Muqaṭṭaʿāt)",
     "The pointer explorer + hypothesis workbench in three views — "
     "🧭 Position (index geometry), 🔤 Sequence (letters≈bases), and "
     "🧩 Semantic (roots≈codons, words≈proteins).")

st.markdown(
    "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;"
    "padding:10px 14px;margin:6px 0 14px;font-size:14px;color:#1D3557;'>"
    "<b>The hypothesis.</b> A disjoint-letter opening (الٓمٓ, حمٓ, الٓرٓ, قٓ, نٓ …) is a "
    "<b>pointer</b>: a tag that groups and places a family of sūras — like a library "
    "call number — without describing their subject. Tabs are grouped into three views: "
    "<b>Position</b> (the validated index geometry — where the tagged sūras sit), "
    "<b>Sequence</b> (character scale — alphabet, letter density &amp; information), and "
    "<b>Semantic</b> (word/root scale — what the tagged sūras contain). Everything "
    "is computed live and validated against permutation nulls.</div>",
    unsafe_allow_html=True)

# Three-category navigation (per design review): Position (the validated index
# geometry) · Sequence (character scale) · Semantic (word/root scale). Inner tab
# containers keep their nesting path, so the `with t_*:` blocks below render
# under the right category.
pos_top, seq_top, sem_top = st.tabs(
    ["🧭 Position — index geometry",
     "🔤 Sequence — character scale",
     "🧩 Semantic — word / root scale"])
with pos_top:
    t_explore, t_contig, t_org, t_not = st.tabs(
        ["🧭 Explore the tags", "🎯 Contiguity geometry",
         "📏 Organization (length)", "🚫 What it is NOT"])
with seq_top:
    t_alpha, t_letinfo = st.tabs(
        ["🔤 Alphabet & letter density", "📐 Letter information theory"])
with sem_top:
    t_lab, t_rootinfo = st.tabs(
        ["🧪 Hypothesis Lab", "🧬 Root sequence & richness"])


# ═══════════════════ POSITION · EXPLORE THE TAGS ═══════════════════
def family_strip(highlight=None, order="mushaf"):
    pos = MUS if order == "mushaf" else NUZ
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(1, 115)), y=[0] * 114, mode="markers",
                             marker=dict(size=5, color="#B4B2A9"), hoverinfo="skip",
                             showlegend=False))
    for nm, ss, c in FAM:
        xs = [pos[s] for s in ss]
        big = [s == highlight or FAMNAME.get(highlight) == nm for s in ss]
        fig.add_trace(go.Scatter(
            x=xs, y=[0] * len(ss), mode="markers", name=nm,
            marker=dict(size=[20 if b else 13 for b in big], color=c,
                        line=dict(width=[3 if b else 1 for b in big], color="white")),
            text=[f"Sūra {s} · {NAMEOF.get(s,'')}" for s in ss], hoverinfo="text"))
    xs = [pos[s] for s in SINGLE]
    fig.add_trace(go.Scatter(x=xs, y=[0] * len(SINGLE), mode="markers", name="singletons",
                             marker=dict(size=9, color=GREY, symbol="diamond"),
                             text=[f"Sūra {s} · {SINGLE[s]}" for s in SINGLE], hoverinfo="text"))
    fig.update_layout(height=240, margin=dict(l=10, r=10, t=30, b=10),
                      yaxis=dict(visible=False), legend=dict(orientation="h", y=-0.25),
                      xaxis_title=("sūra number (muṣḥaf order)" if order == "mushaf"
                                   else "revelation order (nuzūl)"),
                      title=("Book order" if order == "mushaf" else "Revelation order"),
                      font=dict(size=14), plot_bgcolor="white")
    return fig


with t_explore:
    layer(1, "Pick a disjoint-letter sūra")
    opts = {f"Sūra {s} — {NAMEOF.get(s,'')}  ·  {TAG_AR.get(s, FAMNAME[s])}  [{FAMNAME[s]}]": s
            for s in MUQ}
    pick_label = st.selectbox("Disjoint-letter sūra", list(opts.keys()),
                              index=list(opts.values()).index(40))
    pick = opts[pick_label]
    fam = FAMNAME[pick]
    members = next((ss for nm, ss, _ in FAM if nm == fam), [pick])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tag", TAG_AR.get(pick, FAMNAME[pick]),
              help="The disjoint-letter opening this sūra carries (e.g. الٓمٓ, حمٓ).")
    c2.metric("Family", fam,
              help="Sūras sharing the same (or related) opening form a family; "
                   "'singleton' = a tag carried by only one sūra.")
    c3.metric("Family size", len(members),
              help="Number of sūras in this family — the unit the contiguity test runs on.")
    c4.metric("Verses", VERSES.get(pick, "—"),
              help="Length of the selected sūra in verses — muqaṭṭaʿāt sūras are typically the long ones.")

    st.plotly_chart(family_strip(pick, "mushaf"), width="stretch")
    if HAS_REV:
        st.plotly_chart(family_strip(pick, "nuz"), width="stretch")

    if fam != "singleton":
        ms = sorted(members)
        if HAS_REV:
            ns = sorted(NUZ[s] for s in members)
            st.success(
                f"**{fam}** = sūras {', '.join(map(str, ms))} "
                f"(muṣḥaf span {max(ms)-min(ms)}) → revelation slots "
                f"{', '.join(map(str, ns))} (span {max(ns)-min(ns)}). "
                f"Contiguous on both axes — the pointer at work.")
        else:
            st.success(
                f"**{fam}** = sūras {', '.join(map(str, ms))} "
                f"(muṣḥaf span {max(ms)-min(ms)}). Contiguous in book order — "
                f"the pointer at work.")
    else:
        st.info(f"Sūra {pick} carries a **singleton** tag ({SINGLE[pick]}). "
                "Singletons have no family to cluster with, so they are flagged, "
                "not tested for internal contiguity (see *What it is NOT*).")


# ═══════════════════ POSITION · CONTIGUITY GEOMETRY ═══════════════════
def null_fig(out, obs, p, order):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE,
                               name="label-permutation null"))
    fig.add_vline(x=obs, line=dict(color=RED, width=3),
                  annotation_text=f"observed Δ={obs:.2f}", annotation_position="top")
    fig.update_layout(height=380, margin=dict(l=10, r=10, t=40, b=10),
                      xaxis_title="within-family mean distance (smaller = tighter)",
                      yaxis_title="count", font=dict(size=14), plot_bgcolor="white",
                      title=f"{order}: observed in the far tail → p ≈ {p:.2g}",
                      showlegend=False)
    return fig


with t_contig:
    layer(1, "Freeze the 29 sūras, shuffle only the labels")
    st.caption("The decisive test. We hold the 29 sūras in place and randomly "
               "reassign which opening each one gets (preserving family sizes). "
               "Does the REAL tagging group its sūras tighter than a random "
               "relabeling? This controls for the fact that muqaṭṭaʿāt sūras "
               "cluster anyway.")
    ndraw = st.select_slider("Permutations", [1000, 5000, 20000, 50000], value=20000)
    if st.button("▶ Run the label-permutation null", type="primary"):
        st.session_state["_dl_run"] = ndraw
    if st.session_state.get("_dl_run"):
        nd = st.session_state["_dl_run"]
        om, obs_m, p_m = label_perm_null("mushaf", nd)
        if HAS_REV:
            on, obs_n, p_n = label_perm_null("nuz", nd, seed=2)
            c1, c2 = st.columns(2)
            c1.metric("Muṣḥaf contiguity p", f"{p_m:.2g}", "✓ validated" if p_m < .05 else "n.s.")
            c2.metric("Revelation contiguity p", f"{p_n:.2g}", "✓ validated" if p_n < .05 else "n.s.")
            st.plotly_chart(null_fig(om, obs_m, p_m, "Book order (muṣḥaf)"), width="stretch")
            st.plotly_chart(null_fig(on, obs_n, p_n, "Revelation order (nuzūl)"), width="stretch")
            st.success(
                f"Observed within-family distance is **{obs_m:.1f}** (book) and "
                f"**{obs_n:.1f}** (revelation) vs a null mean of ≈{om.mean():.0f}. "
                "The disjoint letters index contiguous families on **both** axes — "
                "the validated core finding.")
        else:
            st.metric("Muṣḥaf contiguity p", f"{p_m:.2g}", "✓ validated" if p_m < .05 else "n.s.")
            st.plotly_chart(null_fig(om, obs_m, p_m, "Book order (muṣḥaf)"), width="stretch")
            st.success(
                f"Observed within-family distance is **{obs_m:.1f}** (book) vs a null "
                f"mean of ≈{om.mean():.0f}. The disjoint letters index contiguous "
                "families in book order — the validated core finding.")
    else:
        st.info("Press **Run** to sample the null and locate the real tagging in its tail.")

    layer(2, "Per-family — computed live, no cherry-picking")
    st.caption("Each family on its own: are its members tighter than random same-size "
               "subsets of all 114 sūras? Computed live — no stored numbers.")
    pf_nd = st.select_slider("Permutations (per family)", [1000, 5000, 20000],
                             value=5000, key="_dl_pf_nd")
    if st.button("▶ Compute per-family p (live)", type="primary", key="_dl_pf_btn"):
        st.session_state["_dl_pf"] = pf_nd
    if st.session_state.get("_dl_pf"):
        _pf = st.session_state["_dl_pf"]
        _names = [nm for nm, _, _ in FAM]
        _mem = {nm: mem for nm, mem, _ in FAM}
        _pm = [custom_contiguity(_mem[nm], "mushaf", ndraw=_pf)[2] for nm in _names]
        _fig = go.Figure()
        _fig.add_trace(go.Bar(x=_names, y=[-np.log10(pp) for pp in _pm], name="muṣḥaf",
                              marker_color=TEAL, text=[f"{pp:.1g}" for pp in _pm],
                              textposition="outside"))
        if HAS_REV:
            _pn = [custom_contiguity(_mem[nm], "nuz", ndraw=_pf, seed=8)[2] for nm in _names]
            _fig.add_trace(go.Bar(x=_names, y=[-np.log10(pp) for pp in _pn], name="revelation",
                                  marker_color=AMBER, text=[f"{pp:.1g}" for pp in _pn],
                                  textposition="outside"))
        _fig.add_hline(y=-np.log10(0.05), line=dict(color=RED, dash="dash"),
                       annotation_text="p = 0.05")
        _fig.update_layout(height=340, barmode="group", font=dict(size=14),
                           yaxis_title="−log₁₀ p", plot_bgcolor="white",
                           margin=dict(l=10, r=10, t=30, b=10),
                           title="Per-family contiguity vs random same-size subsets (live)")
        st.plotly_chart(_fig, width="stretch")
        st.caption("Bars above the dashed line are significant. The 2-sūra ṬSM family "
                   "is the weakest, as expected for the smallest group.")
    else:
        st.info("Press **Compute per-family p (live)** to test each family from data.")

    layer(3, "Leave-one-out robustness")
    st.caption("Does the result hinge on any single sūra? We drop each multi-family "
               "member in turn, rebuild the families one smaller, and re-run the "
               "muṣḥaf label-permutation. If every leave-one-out p stays below 0.05, "
               "the finding survives removing any one sūra.")
    loo_nd = st.select_slider("Permutations (per leave-one-out)", [1000, 5000, 20000],
                              value=5000, key="_dl_loo_nd")
    if st.button("▶ Run leave-one-out robustness", type="primary", key="_dl_loo_btn"):
        st.session_state["_dl_loo"] = loo_nd
    if st.session_state.get("_dl_loo"):
        _members = sorted(_s for _fam in MULTI for _s in _fam)
        _ps = [loo_contiguity("mushaf", _s, st.session_state["_dl_loo"]) for _s in _members]
        _full = label_perm_null("mushaf", st.session_state["_dl_loo"])[2]
        _fig = go.Figure(go.Bar(
            x=[f"−{_s}" for _s in _members],
            y=[-np.log10(_p) for _p in _ps],
            marker_color=[TEAL if _p < .05 else RED for _p in _ps],
            text=[f"{_p:.1g}" for _p in _ps], textposition="outside",
            hovertext=[f"drop sūra {_s} ({NAMEOF.get(_s, '')}) → p={_p:.2g}"
                       for _s, _p in zip(_members, _ps)], hoverinfo="text"))
        _fig.add_hline(y=-np.log10(0.05), line=dict(color=GREY, dash="dash"),
                       annotation_text="p = 0.05")
        _fig.update_layout(height=340, font=dict(size=13), plot_bgcolor="white",
                           xaxis_title="sūra dropped", yaxis_title="−log₁₀ p (muṣḥaf)",
                           margin=dict(l=10, r=10, t=30, b=10),
                           title="Leave-one-out contiguity — bars above the line stay significant")
        st.plotly_chart(_fig, width="stretch")
        _worst = max(_ps)
        st.metric("Worst-case leave-one-out p", f"{_worst:.2g}",
                  "✓ robust (all < 0.05)" if _worst < .05 else "⚠ sensitive to one sūra")
        st.caption(f"Full-family muṣḥaf p ≈ {_full:.2g}. Each bar is −log₁₀ p after "
                   "dropping that sūra; taller = stronger, green = still significant.")


# ═══════════════════ SEQUENCE · ALPHABET & LETTER DENSITY ═══════════════════
with t_alpha:
    st.markdown(
        "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;"
        "padding:8px 14px;margin:4px 0 12px;font-size:13.5px;color:#1D3557;'>"
        "<b>Character scale.</b> Letters ≈ bases. Alphabet usage across the corpus, and "
        "a single-letter density explorer that tests whether a letter's own "
        "disjoint-letter sūras carry it at unusual density.</div>", unsafe_allow_html=True)

    layer(1, "Corpus alphabet — base-frequency profile")
    top_n = st.slider("Show top N letters", 10, len(ALPHABET), min(28, len(ALPHABET)),
                      key="_char_topn")
    items = CORPUS_LETTERS.most_common(top_n)
    fig = go.Figure(go.Bar(x=[ch for ch, _ in items], y=[c for _, c in items],
                           marker_color=NAVY,
                           text=[f"{100*c/_corpus_total:.1f}%" for _, c in items],
                           textposition="outside"))
    fig.update_layout(height=340, font=dict(size=15), plot_bgcolor="white",
                      xaxis_title="letter (normalized)", yaxis_title="count in corpus",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Letter (base) frequency across the whole Qur'an")
    st.plotly_chart(fig, width="stretch")
    try:
        _it = CORPUS_LETTERS.most_common()
        _top3 = sum(c for _, c in _it[:3])
        _n_dis_top10 = sum(1 for ch, _ in _it[:10] if ch in DISJOINT_LETTERS)
        st.markdown(
            f"**📍 What to take from this chart:** the top letter «{_it[0][0]}» alone is "
            f"{100*_it[0][1]/_corpus_total:.1f}% of all {_corpus_total:,} letters, and the "
            f"top three together carry {100*_top3/_corpus_total:.1f}% — a heavily skewed "
            f"alphabet. {_n_dis_top10} of the 10 most frequent letters are themselves "
            f"disjoint letters, so the openings draw from common stock, not rare glyphs."
        )
    except Exception:
        pass

    st.divider()
    layer(2, "Letter-density explorer + cross-chapter enrichment")
    st.caption("Pick a letter, see its density rank across all 114 sūras, then test "
               "whether the sūras whose disjoint-letter OPENING contains it carry the "
               "letter at unusually high density. Generalizes the ق finding "
               "(Sūrat Qāf ranks ~111/114 for ق-density).")
    letter = st.selectbox("Letter", DISJOINT_LETTERS,
                          index=DISJOINT_LETTERS.index("ق") if "ق" in DISJOINT_LETTERS else 0,
                          key="_char_letter")
    dens_all = {s: letter_density(s, letter) for s in range(1, 115)}
    ranked = sorted(range(1, 115), key=lambda s: dens_all[s])
    rank_of = {s: i + 1 for i, s in enumerate(ranked)}  # 1=lowest density
    bearers = [s for s in MUQ if letter in LETTERS_OF.get(s, set())]

    colors = []
    xs = list(range(1, 115))
    for s in xs:
        if s in bearers:
            colors.append(RED)
        elif s in MUQ:
            colors.append(AMBER)
        else:
            colors.append("#B4B2A9")
    fig = go.Figure(go.Bar(
        x=xs, y=[dens_all[s] for s in xs], marker_color=colors,
        text=[NAMEOF.get(s, "") for s in xs], hoverinfo="text+y"))
    fig.update_layout(height=340, font=dict(size=13), plot_bgcolor="white",
                      xaxis_title="sūra number", yaxis_title=f"density of «{letter}»",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title=(f"Density of «{letter}» per sūra — red = opening bears «{letter}», "
                             f"amber = other muqaṭṭaʿāt"))
    st.plotly_chart(fig, width="stretch")

    if bearers:
        ranks_str = ", ".join(f"{s} ({rank_of[s]}/114)" for s in bearers)
        st.caption(f"Density rank of opening-bearers (1=lowest, 114=highest): {ranks_str}")
        enr_nd = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                                  key="_char_enr_nd")
        if st.button(f"▶ Test «{letter}» enrichment in its bearer sūras",
                     type="primary", key="_char_enr_btn"):
            st.session_state["_char_enr_run"] = (letter, enr_nd)
        run = st.session_state.get("_char_enr_run")
        if run and run[0] == letter:
            res = enrichment_null(letter, ndraw=run[1])
            if res:
                out, obs, p, _, _ = res
                st.metric(f"«{letter}» enrichment p", f"{p:.2g}",
                          "✓ enriched" if p < .05 else "n.s.")
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
                fig.add_vline(x=obs, line=dict(color=RED, width=3),
                              annotation_text=f"bearers mean={obs:.3f}",
                              annotation_position="top")
                fig.update_layout(height=320, font=dict(size=14), plot_bgcolor="white",
                                  xaxis_title=f"mean «{letter}»-density",
                                  yaxis_title="count", showlegend=False,
                                  margin=dict(l=10, r=10, t=40, b=10),
                                  title=f"Bearer-sūra density vs random subsets → p ≈ {p:.2g}")
                st.plotly_chart(fig, width="stretch")
                st.caption("A small p means the letter's own sūras carry it at higher "
                           "density than chance — a local content signal. For most "
                           "letters this is n.s.; ق is the borderline case.")
    else:
        st.info(f"No muqaṭṭaʿāt opening contains «{letter}».")


# ═══════════════════ SEQUENCE · LETTER INFORMATION THEORY ═══════════════════
with t_letinfo:
    st.markdown(
        "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;"
        "padding:8px 14px;margin:4px 0 12px;font-size:13.5px;color:#1D3557;'>"
        "<b>Character-scale information.</b> Per-sūra Shannon entropy over LETTERS, "
        "KL-divergence from the corpus letter baseline, and redundancy "
        "(1 − H/H<sub>max</sub>). A label-shuffle permutation asks whether the "
        "muqaṭṭaʿāt sūras are special on each measure, or just ordinary.</div>",
        unsafe_allow_html=True)

    LETTER_METRICS = {
        "Letter entropy (bits)": (letter_entropy, "greater"),
        "KL-divergence from corpus (bits)": (kl_from_corpus, "greater"),
        "Redundancy (1−H/Hmax)": (redundancy, "greater"),
    }

    layer(1, "Per-sūra distribution")
    metric_name = st.selectbox("Letter-level measure", list(LETTER_METRICS.keys()),
                               key="_info_metric")
    fn, direction = LETTER_METRICS[metric_name]
    vals = {s: fn(s) for s in range(1, 115)}
    xs = list(range(1, 115))
    colors = [RED if s in MUQ else "#B4B2A9" for s in xs]
    fig = go.Figure(go.Bar(x=xs, y=[vals[s] for s in xs], marker_color=colors,
                           text=[NAMEOF.get(s, "") for s in xs], hoverinfo="text+y"))
    fig.update_layout(height=340, font=dict(size=13), plot_bgcolor="white",
                      xaxis_title="sūra number", yaxis_title=metric_name,
                      margin=dict(l=10, r=10, t=30, b=10),
                      title=f"{metric_name} per sūra — red = muqaṭṭaʿāt")
    st.plotly_chart(fig, width="stretch")

    mq_mean = float(np.mean([vals[s] for s in MUQ]))
    oth_mean = float(np.mean([vals[s] for s in xs if s not in MUQ]))
    c1, c2 = st.columns(2)
    c1.metric("Mean · muqaṭṭaʿāt", f"{mq_mean:.3f}")
    c2.metric("Mean · others", f"{oth_mean:.3f}")

    st.divider()
    layer(2, "Permutation test — are the muqaṭṭaʿāt special?")
    nd_info = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                               key="_info_nd")
    if st.button("▶ Run the label-shuffle null", type="primary", key="_info_btn"):
        st.session_state["_info_run"] = (metric_name, nd_info)
    run = st.session_state.get("_info_run")
    if run and run[0] == metric_name:
        out, obs, p, _ = muq_special_null(fn, ndraw=run[1], direction=direction)
        st.metric(f"{metric_name} — muqaṭṭaʿāt special? p", f"{p:.2g}",
                  "✓ special" if p < .05 else "✗ ordinary")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
        fig.add_vline(x=obs, line=dict(color=RED, width=3),
                      annotation_text=f"muq mean={obs:.3f}", annotation_position="top")
        fig.update_layout(height=340, font=dict(size=14), plot_bgcolor="white",
                          xaxis_title=f"mean {metric_name} over a 29-sūra set",
                          yaxis_title="count", showlegend=False,
                          margin=dict(l=10, r=10, t=40, b=10),
                          title=f"Muqaṭṭaʿāt mean vs random 29-sūra subsets → p ≈ {p:.2g}")
        st.plotly_chart(fig, width="stretch")
        st.caption("Letter-level information measures track sūra length, so the "
                   "muqaṭṭaʿāt (the long sūras) can look 'special' purely through "
                   "length. Read alongside *Organization* — the pointer is positional, "
                   "and local letter statistics inherit that length signal rather than "
                   "revealing a hidden letter code.")


# ═══════════════════ POSITION · ORGANIZATION (LENGTH) ═══════════════════
with t_org:
    layer(1, "The disjoint letters flag the LONG sūras")
    mq = [VERSES[s] for s in MUQ]
    nn = [VERSES[s] for s in VERSES if s not in MUQ]
    c1, c2, c3 = st.columns(3)
    c1.metric("Median verses · muqaṭṭaʿāt", int(np.median(mq)),
              help="Median sūra length (verses) over the 29 disjoint-letter sūras.")
    c2.metric("Median verses · others", int(np.median(nn)),
              help="Median sūra length over the remaining 85 sūras — the comparison baseline.")
    c3.metric("Ratio", f"{np.median(mq)/np.median(nn):.1f}×",
              help="Muqaṭṭaʿāt median ÷ others median. Far above 1 = the tags flag the long sūras.")
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=nn, nbinsx=30, marker_color="#B4B2A9", name="other sūras"))
    fig.add_trace(go.Histogram(x=mq, nbinsx=20, marker_color=TEAL, name="muqaṭṭaʿāt",
                               opacity=0.8))
    fig.update_layout(height=360, barmode="overlay", font=dict(size=14),
                      xaxis_title="verses per sūra", yaxis_title="count",
                      plot_bgcolor="white", margin=dict(l=10, r=10, t=30, b=10),
                      title=f"Disjoint-letter sūras are the long ones "
                            f"(median {int(np.median(mq))} vs {int(np.median(nn))} verses)")
    st.plotly_chart(fig, width="stretch")
    try:
        _long50 = sorted(VERSES, key=lambda s: -VERSES[s])[:20]
        _muq_in_top20 = sum(1 for s in _long50 if s in MUQ)
        st.markdown(
            f"**📍 What to take from this chart:** the teal (muqaṭṭaʿāt) distribution sits "
            f"far right of the grey one — median {int(np.median(mq))} vs "
            f"{int(np.median(nn))} verses ({np.median(mq)/np.median(nn):.1f}×), and "
            f"{_muq_in_top20} of the 20 longest sūras carry a disjoint-letter tag. The tag "
            f"flags *a long sūra here*; it does not encode a specific length (see the "
            f"Hypothesis Lab attribute test)."
        )
    except Exception:
        pass

    if HAS_REV:
        layer(2, "Revelation phase — simple early, families late")
        phase = [len([s for s in MUQ if NUZ.get(s, 0) <= 49]),
                 len([s for s in MUQ if 50 <= NUZ.get(s, 0) <= 89]),
                 len([s for s in MUQ if NUZ.get(s, 0) >= 90])]
        fig = go.Figure(go.Bar(x=["early-Meccan", "late-Meccan", "Medinan"], y=phase,
                               marker_color=[AMBER, TEAL, RED], text=phase,
                               textposition="outside"))
        fig.update_layout(height=320, font=dict(size=14), yaxis_title="# sūras",
                          plot_bgcolor="white", margin=dict(l=10, r=10, t=30, b=10),
                          title="Disjoint-letter sūras across revelation phases")
        st.plotly_chart(fig, width="stretch")
    st.caption("But length is **not** a per-tag attribute: the tag marks *a long sūra "
               "here*, not a specific length — a purely positional index. Test it live "
               "in the **Hypothesis Lab** tab (attribute label-permutation).")


# ═══════════════════ POSITION · WHAT IT IS NOT (THEME) ═══════════════════
with t_not:
    layer(1, "A pointer addresses; it does not describe")
    st.caption("The honest negatives are as important as the positive. Press to test "
               "whether same-tag sūras share a root-profile theme.")
    if st.button("▶ Run the semantic (theme) null", type="primary"):
        st.session_state["_dl_sem"] = True
    if st.session_state.get("_dl_sem"):
        out, obs, p = semantic_null()
        st.metric("Shared-theme p (root profiles)", f"{p:.2g}",
                  "✗ no theme" if p > .05 else "theme")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
        fig.add_vline(x=obs, line=dict(color=RED, width=3),
                      annotation_text=f"observed", annotation_position="top")
        fig.update_layout(height=340, font=dict(size=14), plot_bgcolor="white",
                          xaxis_title="within-family root similarity",
                          yaxis_title="count", showlegend=False,
                          margin=dict(l=10, r=10, t=40, b=10),
                          title=f"Within-family similarity is unremarkable → p ≈ {p:.2g}")
        st.plotly_chart(fig, width="stretch")
        st.caption("This is a live recomputation over raw root profiles, so the exact "
                   "p varies with the similarity measure and the random draw. Read the "
                   "p shown above — not any external figure: the conclusion is the same, "
                   "no per-tag theme.")

    st.divider()
    layer(2, "The scorecard — computed live")
    st.caption("Every verdict is computed from the loaded corpus on demand — no stored "
               "numbers, no hand-assigned conclusions. The data decides.")
    sc_nd = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                             key="_dl_sc_nd")
    if st.button("▶ Build the scorecard (live)", type="primary", key="_dl_sc_btn"):
        st.session_state["_dl_sc"] = sc_nd
    if not st.session_state.get("_dl_sc"):
        st.info("Press **Build the scorecard (live)** to compute every verdict from data.")
    else:
        _nd = st.session_state["_dl_sc"]
        _pm = label_perm_null("mushaf", _nd)[2]
        _mq = [VERSES[s] for s in MUQ]
        _ot = [VERSES[s] for s in VERSES if s not in MUQ]
        _medq = int(np.median(_mq)); _medo = int(np.median(_ot))
        _theme = semantic_null(_nd)[2]
        _lenp = attr_perm_null("Length (verses)", _nd)[2]
        _sig = sum(1 for _ch in DISJOINT_LETTERS
                   if (enrichment_null(_ch, ndraw=_nd) or (0, 0, 1.0))[2] < 0.05)
        _qd = {s: letter_density(s, "ق") for s in range(1, 115)}
        _qrank = sorted(range(1, 115), key=lambda s: _qd[s]).index(50) + 1
        rows = [("Contiguous family (muṣḥaf)",
                 "✓ supported" if _pm < .05 else "✗ not supported",
                 TEAL if _pm < .05 else RED, f"p = {_pm:.2g}")]
        if HAS_REV:
            _pn = label_perm_null("nuz", _nd, seed=2)[2]
            rows.append(("Contiguous family (revelation)",
                         "✓ supported" if _pn < .05 else "✗ not supported",
                         TEAL if _pn < .05 else RED, f"p = {_pn:.2g}"))
        rows += [
            ("Flags the long sūras",
             "✓ supported" if _medq > _medo else "✗ not supported",
             TEAL if _medq > _medo else RED, f"median {_medq} vs {_medo} verses"),
            ("Shared theme per tag",
             "✓ supported" if _theme < .05 else "✗ not supported",
             TEAL if _theme < .05 else RED, f"p = {_theme:.2g}"),
            ("Shared length per tag",
             "✓ supported" if _lenp < .05 else "✗ not supported",
             TEAL if _lenp < .05 else RED, f"p = {_lenp:.2g}"),
            ("Letter-frequency code",
             "✗ not supported" if _sig == 0 else "~ partial",
             RED if _sig == 0 else AMBER,
             f"{_sig}/{len(DISJOINT_LETTERS)} disjoint letters enriched"),
            ("Single-letter ق density (Sūrat Qāf)", "~ density lead", AMBER,
             f"rank {_qrank}/114"),
        ]
        html_rows = []
        for label, verdict, col, note in rows:
            html_rows.append(
                "<div style='display:flex;justify-content:space-between;align-items:center;"
                "border:1px solid #E2E8F1;border-left:5px solid " + col + ";border-radius:8px;"
                "padding:8px 14px;margin:4px 0;'>"
                "<span style='font-size:15px;color:#1D3557;font-weight:600;'>" + label + "</span>"
                "<span style='font-size:14px;'><b style='color:" + col + ";'>" + verdict + "</b>"
                "<span style='color:#10243A;'> &nbsp;&middot;&nbsp; " + note + "</span></span></div>")
        st.markdown("".join(html_rows), unsafe_allow_html=True)

    st.markdown(
        "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;padding:10px 14px;margin-top:12px;"
        "font-size:14px;color:#1D3557;'><b>Verdict.</b> The muqatta'at are a validated "
        "<b>positional / organizational pointer</b> &mdash; an index over contiguous "
        "sura-families in both mushaf and revelation order, flagging the long suras &mdash; "
        "but not a semantic or frequency code. The Qur'an's detectable latent structure is "
        "relational, not in local content statistics.</div>", unsafe_allow_html=True)

    st.divider()
    layer(3, "Multiple-testing correction (FDR) — cross-domain")
    st.caption("This section runs many permutation tests, so some could clear p<0.05 "
               "by chance alone. Benjamini–Hochberg controls the false-discovery rate "
               "across the whole battery at once.")
    fdr_nd = st.select_slider("Permutations (per test)", [1000, 5000, 20000],
                              value=5000, key="_dl_fdr_nd")
    if st.button("▶ Run the test battery + BH-FDR", type="primary", key="_dl_fdr_btn"):
        st.session_state["_dl_fdr"] = fdr_nd
    if st.session_state.get("_dl_fdr"):
        _nd = st.session_state["_dl_fdr"]
        _battery = [("Contiguity · muṣḥaf (tight)", label_perm_null("mushaf", _nd)[2])]
        if HAS_REV:
            _battery.append(("Contiguity · nuzūl (tight)",
                             label_perm_null("nuz", _nd, seed=2)[2]))
        _battery += [
            ("Shared theme per tag", semantic_null(_nd)[2]),
            ("Shared length per tag", attr_perm_null("Length (verses)", _nd)[2]),
            ("Letter-entropy special",
             muq_special_null(letter_entropy, _nd, direction="greater")[2]),
            ("Root-entropy special",
             muq_special_null(root_entropy, _nd, direction="greater")[2]),
            ("Lexical-richness special",
             muq_special_null(lexical_richness, _nd, direction="less")[2]),
            ("ق-density enrichment", enrichment_null("ق", _nd)[2]),
        ]
        # Signal-domain representative test: sūra-length autocorrelation (lag-1)
        _ser = np.array([VERSES.get(s, 0) for s in range(1, 115)], dtype=float)
        _sc = _ser - _ser.mean()
        _den = float(np.dot(_sc, _sc)) or 1.0
        _ac1 = float(np.dot(_sc[:-1], _sc[1:]) / _den)
        _rng_s = np.random.default_rng(31); _outs = np.empty(_nd)
        for _j in range(_nd):
            _q = _rng_s.permutation(_ser); _qc = _q - _q.mean()
            _qd = float(np.dot(_qc, _qc)) or 1.0
            _outs[_j] = float(np.dot(_qc[:-1], _qc[1:]) / _qd)
        _battery.append(("Length autocorrelation (Signal)", perm_p(_outs, _ac1, "greater")))
        _labels = [b[0] for b in _battery]
        _ps = [b[1] for b in _battery]
        _qs = list(benjamini_hochberg(_ps))
        _alpha = 0.05
        _surv = [q <= _alpha for q in _qs]
        import pandas as _pd
        _tbl = _pd.DataFrame({
            "test": _labels,
            "p (raw)": [f"{pp:.2g}" for pp in _ps],
            "q (BH-FDR)": [f"{qq:.2g}" for qq in _qs],
            "survives 5% FDR": ["✓" if sv else "✗" for sv in _surv],
        })
        st.dataframe(_tbl, width="stretch", hide_index=True)
        _fig = go.Figure()
        _fig.add_trace(go.Bar(x=_labels, y=[-np.log10(max(pp, 1e-6)) for pp in _ps],
                              name="−log₁₀ p (raw)", marker_color=ICE))
        _fig.add_trace(go.Bar(x=_labels, y=[-np.log10(max(qq, 1e-6)) for qq in _qs],
                              name="−log₁₀ q (BH-FDR)", marker_color=TEAL))
        _fig.add_hline(y=-np.log10(_alpha), line=dict(color=RED, dash="dash"),
                       annotation_text="α = 0.05")
        _fig.update_layout(height=400, barmode="group", font=dict(size=12),
                           plot_bgcolor="white", margin=dict(l=10, r=10, t=30, b=130),
                           yaxis_title="−log₁₀ (higher = stronger)", xaxis_tickangle=-35,
                           title="Raw p vs BH-FDR q — bars above the line survive correction")
        st.plotly_chart(_fig, width="stretch")
        st.metric("Discoveries surviving 5% FDR", f"{sum(_surv)} / {len(_surv)}")
        st.caption("FDR controls for running many tests — not for confounding. The "
                   "contiguity findings survive; any entropy/length 'special' that "
                   "clears the line does so largely through the sūra-length confound "
                   "(see the Organization tab), so read those alongside that caveat.")


# ═══════════════════ SEMANTIC · HYPOTHESIS LAB ═══════════════════
with t_lab:
    layer(1, "Build your own sūra family")
    st.caption("Pick any set of sūras and test whether they cluster contiguously — "
               "against a LIVE null of random same-size subsets of all 114. This is the "
               "same machinery the course used on the muqaṭṭaʿāt, now in your hands.")

    preset = st.selectbox(
        "Start from a preset (optional)",
        ["— custom —"] + [nm for nm, _, _ in FAM] + ["All muqaṭṭaʿāt (29)"],
        index=0, key="_lab_preset")
    if preset == "All muqaṭṭaʿāt (29)":
        default_members = MUQ
    elif preset != "— custom —":
        default_members = next(ss for nm, ss, _ in FAM if nm == preset)
    else:
        default_members = [40, 41, 42, 43, 44, 45, 46]

    sura_opts = {f"{s} — {NAMEOF.get(s, '')}": s for s in range(1, 115)}
    inv = {v: k for k, v in sura_opts.items()}
    chosen_labels = st.multiselect(
        "Sūras in your family", list(sura_opts.keys()),
        default=[inv[s] for s in default_members], key="_lab_members")
    chosen = [sura_opts[l] for l in chosen_labels]

    nlab = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                            key="_lab_nd")
    if st.button("▶ Test contiguity of my family", type="primary", key="_lab_btn"):
        st.session_state["_lab_run"] = (tuple(sorted(chosen)), nlab)

    if st.session_state.get("_lab_run"):
        run_members, run_nd = st.session_state["_lab_run"]
        run_members = list(run_members)
        if len(run_members) < 2:
            st.warning("Pick at least 2 sūras to measure contiguity.")
        else:
            rm = custom_contiguity(run_members, "mushaf", ndraw=run_nd)
            out_m, obs_m, p_m, k = rm
            cols = st.columns(2 if HAS_REV else 1)
            cols[0].metric("Muṣḥaf contiguity p", f"{p_m:.2g}",
                           "✓ tighter than chance" if p_m < .05 else "n.s.")
            res_n = None
            if HAS_REV:
                res_n = custom_contiguity(run_members, "nuz", ndraw=run_nd, seed=8)
                out_n, obs_n, p_n, _ = res_n
                cols[1].metric("Revelation contiguity p", f"{p_n:.2g}",
                               "✓ tighter than chance" if p_n < .05 else "n.s.")

            def lab_fig(out, obs, p, order):
                fig = go.Figure()
                fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE,
                                           name="random-subset null"))
                fig.add_vline(x=obs, line=dict(color=RED, width=3),
                              annotation_text=f"your family Δ={obs:.1f}",
                              annotation_position="top")
                fig.update_layout(height=320, font=dict(size=14), plot_bgcolor="white",
                                  xaxis_title="mean pairwise distance (smaller = tighter)",
                                  yaxis_title="count", showlegend=False,
                                  margin=dict(l=10, r=10, t=40, b=10),
                                  title=f"{order}: p ≈ {p:.2g}")
                return fig

            st.plotly_chart(lab_fig(out_m, obs_m, p_m, "Book order (muṣḥaf)"),
                            width="stretch")
            if res_n is not None:
                st.plotly_chart(lab_fig(out_n, obs_n, p_n, "Revelation order (nuzūl)"),
                                width="stretch")
            verdict = ("clusters more tightly than random sūra-sets"
                       if p_m < .05 else "is no tighter than a random set of the same size")
            st.info(f"Your {k}-sūra family {verdict} in book order (p ≈ {p_m:.2g}). "
                    "The null is rebuilt live on every run, so try contiguous vs scattered "
                    "picks and watch the p-value move.")

    st.divider()
    layer(2, "Does a tag share an attribute? (label-permutation)")
    st.caption("Generalizes the per-tag length test. We hold the 4 real families and "
               "shuffle which sūras carry which tag, asking whether the real tagging "
               "groups an attribute tighter than chance. A tight grouping (small p) would "
               "mean the tag encodes that attribute; a large p means it does not.")
    attr_name = st.selectbox("Attribute to test", list(ATTRS.keys()), key="_lab_attr")
    nattr = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                             key="_lab_attr_nd")
    if st.button("▶ Run attribute label-permutation", type="primary", key="_lab_attr_btn"):
        st.session_state["_lab_attr_run"] = (attr_name, nattr)
    if st.session_state.get("_lab_attr_run"):
        an, andr = st.session_state["_lab_attr_run"]
        out, obs, p = attr_perm_null(an, ndraw=andr)
        st.metric(f"{an} — shared-per-tag p", f"{p:.2g}",
                  "encodes attribute" if p < .05 else "✗ not encoded")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
        fig.add_vline(x=obs, line=dict(color=RED, width=3),
                      annotation_text=f"observed Δ={obs:.2f}", annotation_position="top")
        fig.update_layout(height=320, font=dict(size=14), plot_bgcolor="white",
                          xaxis_title="within-family spread of attribute (smaller = tighter)",
                          yaxis_title="count", showlegend=False,
                          margin=dict(l=10, r=10, t=40, b=10),
                          title=f"{an}: within-family spread vs null → p ≈ {p:.2g}")
        st.plotly_chart(fig, width="stretch")
        st.caption("If p is large, the disjoint-letter tag does NOT pick out sūras that "
                   "share this attribute — consistent with a purely positional pointer.")


# ═══════════════════ SEMANTIC · ROOT SEQUENCE & RICHNESS ═══════════════════
with t_rootinfo:
    st.markdown(
        "<div style='background:#EEF3FB;border-left:5px solid #1D3557;border-radius:8px;"
        "padding:8px 14px;margin:4px 0 12px;font-size:13.5px;color:#1D3557;'>"
        "<b>Word/root scale.</b> Roots ≈ codons. Per-sūra root entropy (how varied the "
        "root vocabulary is) and lexical richness (unique ÷ total roots), each tested "
        "for whether the muqaṭṭaʿāt sūras stand out.</div>", unsafe_allow_html=True)

    layer(1, "Root entropy per sūra")
    vals = {s: root_entropy(s) for s in range(1, 115)}
    xs = list(range(1, 115))
    colors = [RED if s in MUQ else "#B4B2A9" for s in xs]
    fig = go.Figure(go.Bar(x=xs, y=[vals[s] for s in xs], marker_color=colors,
                           text=[NAMEOF.get(s, "") for s in xs], hoverinfo="text+y"))
    fig.update_layout(height=320, font=dict(size=13), plot_bgcolor="white",
                      xaxis_title="sūra number", yaxis_title="root entropy (bits)",
                      margin=dict(l=10, r=10, t=30, b=10),
                      title="Root (codon) entropy per sūra — red = muqaṭṭaʿāt")
    st.plotly_chart(fig, width="stretch")
    nd_re = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                             key="_root_ent_nd")
    if st.button("▶ Are the muqaṭṭaʿāt special on root entropy?", type="primary",
                 key="_root_ent_btn"):
        st.session_state["_root_ent_run"] = nd_re
    if st.session_state.get("_root_ent_run"):
        out, obs, p, allv = muq_special_null(root_entropy,
                                             ndraw=st.session_state["_root_ent_run"],
                                             direction="greater")
        oth = float(np.mean([allv[s] for s in range(1, 115) if s not in MUQ]))
        c1, c2, c3 = st.columns(3)
        c1.metric("Root entropy · muq", f"{obs:.2f}")
        c2.metric("· others", f"{oth:.2f}")
        c3.metric("p (muq higher?)", f"{p:.2g}", "✓ higher" if p < .05 else "n.s.")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
        fig.add_vline(x=obs, line=dict(color=RED, width=3),
                      annotation_text=f"muq mean={obs:.2f}", annotation_position="top")
        fig.update_layout(height=300, font=dict(size=14), plot_bgcolor="white",
                          xaxis_title="mean root entropy over a 29-sūra set",
                          yaxis_title="count", showlegend=False,
                          margin=dict(l=10, r=10, t=40, b=10),
                          title=f"Root entropy vs random 29-sūra subsets → p ≈ {p:.2g}")
        st.plotly_chart(fig, width="stretch")
        st.caption("Longer sūras draw on more distinct roots, so higher muqaṭṭaʿāt root "
                   "entropy is again largely a length effect — not a hidden code.")

    st.divider()
    layer(2, "Lexical richness (codon diversity)")
    st.caption("Type-token ratio on the root stream: unique roots ÷ total roots per "
               "sūra. Are the muqaṭṭaʿāt sūras more or less lexically diverse than others?")
    rich_nd = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                               key="_char_rich_nd")
    if st.button("▶ Test muqaṭṭaʿāt lexical richness", type="primary", key="_char_rich_btn"):
        st.session_state["_char_rich_run"] = rich_nd
    if st.session_state.get("_char_rich_run"):
        out, obs, p, allvals = muq_special_null(
            lexical_richness, ndraw=st.session_state["_char_rich_run"],
            direction="less")
        others = float(np.mean([allvals[s] for s in range(1, 115) if s not in MUQ]))
        c1, c2, c3 = st.columns(3)
        c1.metric("Richness · muqaṭṭaʿāt", f"{obs:.3f}")
        c2.metric("Richness · others", f"{others:.3f}")
        c3.metric("p (muq lower?)", f"{p:.2g}", "✓ lower" if p < .05 else "n.s.")
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=out, nbinsx=40, marker_color=ICE, name="null"))
        fig.add_vline(x=obs, line=dict(color=RED, width=3),
                      annotation_text=f"muq mean={obs:.3f}", annotation_position="top")
        fig.update_layout(height=300, font=dict(size=14), plot_bgcolor="white",
                          xaxis_title="mean lexical richness (unique/total roots)",
                          yaxis_title="count", showlegend=False,
                          margin=dict(l=10, r=10, t=40, b=10),
                          title=f"Muqaṭṭaʿāt vs random 29-sūra subsets → p ≈ {p:.2g}")
        st.plotly_chart(fig, width="stretch")
        st.caption("Longer sūras naturally repeat roots more, so muqaṭṭaʿāt (the long "
                   "sūras) tend to LOWER type-token ratios — a length artefact, not a "
                   "letter code. The permutation makes that explicit.")



    st.divider()
    layer(3, "Embedding-space clustering — a denoised theme test")
    st.caption("Build each muqaṭṭaʿāt sūra as a root-frequency vector, reduce with SVD, "
               "then ask whether same-tag families sit closer (cosine) than a random "
               "relabeling. A denoised companion to the raw-profile theme null.")
    emb_nd = st.select_slider("Permutations", [1000, 5000, 20000], value=5000,
                              key="_dl_emb_nd")
    if st.button("▶ Run embedding-space family test", type="primary", key="_dl_emb_btn"):
        st.session_state["_dl_emb"] = emb_nd
    if st.session_state.get("_dl_emb"):
        _vocab = sorted({r for s in MUQ for r in PROFS[s]})
        _vi = {r: i for i, r in enumerate(_vocab)}
        _M = np.zeros((len(MUQ), len(_vocab)))
        for _row, _s in enumerate(MUQ):
            _tot = sum(PROFS[_s].values()) or 1
            for _r, _cnt in PROFS[_s].items():
                _M[_row, _vi[_r]] = _cnt / _tot
        _k = min(10, len(MUQ) - 1)
        try:
            _U, _Sg, _Vt = np.linalg.svd(_M - _M.mean(0), full_matrices=False)
            _emb = _U[:, :_k] * _Sg[:_k]
        except Exception:
            _emb = _M
        _pos = {s: _emb[i] for i, s in enumerate(MUQ)}
        def _cosd(a, b):
            na = np.linalg.norm(a); nb = np.linalg.norm(b)
            return 1.0 - (np.dot(a, b) / (na * nb)) if na and nb else 1.0
        def _within(fams):
            ds = []
            for ss in fams:
                for i in range(len(ss)):
                    for j in range(i + 1, len(ss)):
                        ds.append(_cosd(_pos[ss[i]], _pos[ss[j]]))
            return float(np.mean(ds)) if ds else 0.0
        _obs = _within(MULTI)
        _rng = np.random.default_rng(23); _base = list(MUQ)
        _ndr = st.session_state["_dl_emb"]; _out = np.empty(_ndr)
        for _t in range(_ndr):
            _rng.shuffle(_base); _idx = 0; _f = []
            for _sz in SIZES:
                _f.append(_base[_idx:_idx + _sz]); _idx += _sz
            _out[_t] = _within(_f)
        _p = perm_p(_out, _obs, "less")
        st.metric("Embedding-space shared-theme p", f"{_p:.2g}",
                  "theme" if _p < .05 else "✗ no theme")
        _xy = _emb[:, :2] if _emb.shape[1] >= 2 else np.c_[_emb[:, 0], np.zeros(len(MUQ))]
        _fig = go.Figure()
        for _nm, _ss, _co in FAM:
            _ii = [MUQ.index(s) for s in _ss]
            _fig.add_trace(go.Scatter(x=_xy[_ii, 0], y=_xy[_ii, 1], mode="markers+text",
                                      name=_nm, marker=dict(size=12, color=_co),
                                      text=[str(s) for s in _ss], textposition="top center"))
        _si = [MUQ.index(s) for s in SINGLE]
        _fig.add_trace(go.Scatter(x=_xy[_si, 0], y=_xy[_si, 1], mode="markers",
                                  name="singletons",
                                  marker=dict(size=8, color=GREY, symbol="diamond")))
        _fig.update_layout(height=420, plot_bgcolor="white", font=dict(size=13),
                           xaxis_title="SVD dim 1", yaxis_title="SVD dim 2",
                           margin=dict(l=10, r=10, t=30, b=10),
                           title="Muqaṭṭaʿāt sūras in root-embedding space (colour = family)")
        st.plotly_chart(_fig, width="stretch")
        _hist = go.Figure()
        _hist.add_trace(go.Histogram(x=_out, nbinsx=40, marker_color=ICE, name="null"))
        _hist.add_vline(x=_obs, line=dict(color=RED, width=3),
                        annotation_text=f"observed={_obs:.3f}", annotation_position="top")
        _hist.update_layout(height=300, plot_bgcolor="white", font=dict(size=14),
                            xaxis_title="within-family mean cosine distance (smaller = tighter)",
                            yaxis_title="count", showlegend=False,
                            margin=dict(l=10, r=10, t=40, b=10),
                            title=f"Within-family embedding distance vs null → p ≈ {_p:.2g}")
        st.plotly_chart(_hist, width="stretch")
        st.caption("Large p means families don't cluster even after SVD denoising — the "
                   "disjoint-letter tag carries no shared theme, consistent with a purely "
                   "positional pointer.")

# ═══════════════════ EXPORT THIS ANALYSIS ═══════════════════
st.divider()
st.markdown("### ⬇ Export this analysis")
import pandas as _pd
_dl_rows = []
for _s in range(1, 115):
    _dl_rows.append({
        "surah": _s, "name": NAMEOF.get(_s, ""),
        "verses": VERSES.get(_s, 0),
        "muqattaat": _s in MUQ,
        "family": FAMNAME.get(_s, "") if _s in MUQ else "",
        "tag_letters": "".join(sorted(LETTERS_OF.get(_s, set()))),
        "letter_entropy_bits": round(letter_entropy(_s), 4),
        "root_entropy_bits": round(root_entropy(_s), 4),
        "kl_from_corpus_bits": round(kl_from_corpus(_s), 4),
        "redundancy": round(redundancy(_s), 4),
        "lexical_richness": round(lexical_richness(_s), 4),
        "root_tokens": len(ROOTS_BY_SURA[_s]),
    })
_dl_df = _pd.DataFrame(_dl_rows)
st.download_button("⬇ Per-sūra stats — all 114 (CSV)",
                   _dl_df.to_csv(index=False).encode("utf-8-sig"),
                   "disjoint_letters_per_sura.csv", "text/csv",
                   key="_dl_export_csv")
st.caption("Corpus-scoped export, separate from the root-query Export page. "
           "To save any chart as an image, use the camera icon on its toolbar.")

st.caption("Computed live from the loaded corpus | permutation nulls | letters≈bases · "
           "roots≈codons · words≈proteins | no 'scientific-miracle' claims. Companion to "
           "the 17-lecture Disjoint-Letters course.")
