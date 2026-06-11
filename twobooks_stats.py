"""twobooks_stats.py — shared statistical kernel for the Two Books pages
(Disjoint Letters · Signal · Biology).

Pure functions + reference data, no Streamlit dependency, so they can be unit-
tested and reused without import side effects. Centralizing these guarantees the
pages and the global FDR dashboard compute entropy, permutation p-values, the
muqaṭṭaʿāt membership, and the cross-domain test battery identically — one source
of truth.
"""
from __future__ import annotations

import itertools
import math
from collections import Counter

import numpy as np

from analysis import COL_SURAH, COL_AYAH, normalize_letters


# ───────────────────────── primitives ─────────────────────────
def shannon_bits(counts) -> float:
    """Shannon entropy (bits) of an iterable of counts."""
    total = sum(counts)
    if total <= 0:
        return 0.0
    h = 0.0
    for c in counts:
        if c > 0:
            p = c / total
            h -= p * math.log2(p)
    return h


def perm_p(null, observed, direction="greater") -> float:
    """Permutation p-value with +1 smoothing.
    direction='greater' → P(null >= observed); 'less' → P(null <= observed)."""
    null = np.asarray(null)
    n = null.size
    if direction == "greater":
        hits = int(np.sum(null >= observed))
    elif direction == "less":
        hits = int(np.sum(null <= observed))
    else:
        raise ValueError("direction must be 'greater' or 'less'")
    return (hits + 1) / (n + 1)


def benjamini_hochberg(pvals):
    """Benjamini–Hochberg FDR adjustment. Returns q-values in input order.
    Controls the false-discovery rate across a battery — NOT confounding."""
    p = np.asarray(pvals, dtype=float)
    m = p.size
    if m == 0:
        return np.array([])
    order = np.argsort(p)
    ranked = p[order]
    q = ranked * m / np.arange(1, m + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0.0, 1.0)
    out = np.empty(m)
    out[order] = q
    return out


def per_sura_letters_roots(corpus):
    """Per-sūra normalized-letter Counters and root-token lists, keyed 1..114."""
    df = corpus.df
    su = df[COL_SURAH].astype(int).tolist()
    letters = {s: Counter() for s in range(1, 115)}
    roots = {s: [] for s in range(1, 115)}
    for i in range(len(df)):
        s = su[i]
        for t in corpus.seg_tokens[i]:
            nt = normalize_letters(t)
            if not nt:
                continue
            for ch in nt:
                if ch.strip():
                    letters[s][ch] += 1
        roots[s].extend(corpus.root_tokens[i])
    return letters, roots


# ──────────────── muqaṭṭaʿāt reference data (single source) ────────────────
# Membership only (no UI colours). Verified against the corpus text:
# 28/29 openings appear in āyah 1; sūra 42's second set عسق is in āyah 2.
MUQ_FAMILIES = {
    "ḤM": [40, 41, 42, 43, 44, 45, 46],
    "ALM": [2, 3, 29, 30, 31, 32],
    "ALR": [10, 11, 12, 14, 15],
    "ṬSM": [26, 28],
}
MUQ_SINGLETONS = [7, 13, 19, 20, 27, 36, 38, 50, 68]
MUQ = sorted(sum(MUQ_FAMILIES.values(), []) + MUQ_SINGLETONS)
MUQ_MULTI = list(MUQ_FAMILIES.values())
MUQ_SIZES = [len(x) for x in MUQ_MULTI]

LETTERS_OF = {}
for _s in [2, 3, 29, 30, 31, 32]:
    LETTERS_OF[_s] = set("الم")
for _s in [10, 11, 12, 14, 15]:
    LETTERS_OF[_s] = set("الر")
for _s in [40, 41, 43, 44, 45, 46]:
    LETTERS_OF[_s] = set("حم")
LETTERS_OF[42] = set("حمعسق")
for _s in [26, 28]:
    LETTERS_OF[_s] = set("طسم")
LETTERS_OF[7] = set("المص")
LETTERS_OF[13] = set("المر")
LETTERS_OF[19] = set("كهيعص")
LETTERS_OF[20] = set("طه")
LETTERS_OF[27] = set("طس")
LETTERS_OF[36] = set("يس")
LETTERS_OF[38] = set("ص")
LETTERS_OF[50] = set("ق")
LETTERS_OF[68] = set("ن")
DISJOINT_LETTERS = sorted(set().union(*LETTERS_OF.values()))


def _verses(corpus):
    su = corpus.df[COL_SURAH].astype(int).tolist()
    ay = corpus.df[COL_AYAH].astype(int).tolist()
    v = {}
    for i in range(len(corpus.df)):
        v[su[i]] = max(v.get(su[i], 0), ay[i])
    return v


def _within_mean(posmap, fams):
    tot = n = 0
    for ss in fams:
        ps = [posmap[s] for s in ss if s in posmap]
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                tot += abs(ps[i] - ps[j]); n += 1
    return tot / n if n else 0.0


def two_books_battery(corpus, ndraw=5000, seed=0):
    """Run one representative permutation test per Two Books domain and return
    {test_name: p}. The single source for the cross-section FDR view, so the
    global dashboard never duplicates page logic."""
    rng = np.random.default_rng(seed)
    mus = {s: s for s in range(1, 115)}
    nuz = {int(k): int(v) for k, v in corpus.rev_order_of_surah.items()}
    has_rev = sum(1 for s in MUQ if s in nuz) >= len(MUQ) - 1
    verses = _verses(corpus)
    letters, roots = per_sura_letters_roots(corpus)
    profs = {s: Counter(roots[s]) for s in MUQ}
    res = {}

    def _fam_shuffle_p(valfn, observed_fams_fn, direction):
        obs = observed_fams_fn(MUQ_MULTI)
        base = list(MUQ); out = np.empty(ndraw)
        for k in range(ndraw):
            rng.shuffle(base); idx = 0; fams = []
            for sz in MUQ_SIZES:
                fams.append(base[idx:idx + sz]); idx += sz
            out[k] = observed_fams_fn(fams)
        return perm_p(out, obs, direction)

    # Position — contiguity
    res["Contiguity · muṣḥaf (Position)"] = _fam_shuffle_p(
        None, lambda f: _within_mean(mus, f), "less")
    if has_rev:
        res["Contiguity · nuzūl (Position)"] = _fam_shuffle_p(
            None, lambda f: _within_mean(nuz, f), "less")

    # Semantic — shared theme (cosine of root profiles)
    def _cos(a, b):
        keys = set(a) | set(b)
        dot = sum(a[k] * b[k] for k in keys)
        na = math.sqrt(sum(v * v for v in a.values()))
        nb = math.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb) if na and nb else 0.0

    def _theme(fams):
        v = []
        for ss in fams:
            v += [_cos(profs[a], profs[b]) for a, b in itertools.combinations(ss, 2)]
        return float(np.mean(v)) if v else 0.0
    res["Shared theme per tag (Semantic)"] = _fam_shuffle_p(None, _theme, "greater")

    # Position/Semantic — per-tag length spread
    lmap = {s: float(verses.get(s, 0)) for s in MUQ}
    res["Shared length per tag"] = _fam_shuffle_p(
        None, lambda f: _within_mean(lmap, f), "less")

    # muq-vs-random specials
    def _special(metric, direction):
        allv = {s: metric(s) for s in range(1, 115)}
        obs = float(np.mean([allv[s] for s in MUQ])); out = np.empty(ndraw)
        for j in range(ndraw):
            pick = rng.choice(range(1, 115), size=len(MUQ), replace=False)
            out[j] = float(np.mean([allv[int(x)] for x in pick]))
        return perm_p(out, obs, direction)
    res["Letter entropy special (Sequence)"] = _special(
        lambda s: shannon_bits(letters[s].values()), "greater")
    res["Root entropy special (Semantic)"] = _special(
        lambda s: shannon_bits(Counter(roots[s]).values()), "greater")

    # Signal — sūra-length autocorrelation (lag-1)
    ser = np.array([verses.get(s, 0) for s in range(1, 115)], dtype=float)
    sc = ser - ser.mean(); den = float(np.dot(sc, sc)) or 1.0
    ac1 = float(np.dot(sc[:-1], sc[1:]) / den); out = np.empty(ndraw)
    for j in range(ndraw):
        q = rng.permutation(ser); qc = q - q.mean(); qd = float(np.dot(qc, qc)) or 1.0
        out[j] = float(np.dot(qc[:-1], qc[1:]) / qd)
    res["Length autocorrelation (Signal)"] = perm_p(out, ac1, "greater")

    # Biology — di-codon adjacency structure (chi-square vs shuffled stream)
    ayah_roots = [list(t) for t in corpus.root_tokens]
    uni = Counter(); big = Counter()
    for toks in ayah_roots:
        for t in toks:
            uni[t] += 1
        for a, b in zip(toks, toks[1:]):
            big[(a, b)] += 1
    ntok = sum(uni.values()) or 1
    common = {r for r, _ in uni.most_common(150)}

    def _chi(bg):
        tot = 0.0
        for (a, b), o in bg.items():
            if a in common and b in common:
                exp = uni[a] * uni[b] / ntok
                if exp > 0:
                    tot += (o - exp) ** 2 / exp
        return tot
    obs = _chi(big)
    flat = np.array([t for toks in ayah_roots for t in toks], dtype=object)
    lens = [len(toks) for toks in ayah_roots]
    nd_bio = min(ndraw, 500)
    out = np.empty(nd_bio)
    for j in range(nd_bio):
        perm = flat.copy(); rng.shuffle(perm); bg = Counter(); pos = 0
        for L in lens:
            seg = perm[pos:pos + L]; pos += L
            for x, y in zip(seg, seg[1:]):
                bg[(x, y)] += 1
        out[j] = _chi(bg)
    res["Di-codon structure (Biology)"] = perm_p(out, obs, "greater")
    return res
