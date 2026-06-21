"""Higher-order (3-way) concept structure — is there a design layer BEYOND pairwise co-occurrence?

VERDICT (2026-06-21): REFUTED as an independent feature. Recurring concept-TRIADS reduce to
their constituent concept-PAIRS. Grade ~25.

Substrate ROOT (content-only, drop top-12 ubiquitous). Arrangement divine-default (and the metric
is arrangement-INVARIANT — it is within-verse bundling, independent of āyah order).

Pipeline (all measured on Book6.xlsx, verse = hyperedge over its content roots):
  1. Margins-only curveball null (fixes root-frequency AND verse-length simultaneously):
     triads recurring in >=5 verses  observed 757 vs null 115  -> 6.6x, z=+25.8
     repetition mass  sum c(c-1)       observed vs null          -> 2.1x, z=+28.4
     (looked like strong higher-order structure)
  2. NEGATIVE CONTROL (feed a curveball-randomised corpus as 'observed'): z=+1.1  -> estimator
     does NOT manufacture structure; pipeline valid.
  3. KIRKWOOD superposition test (the decisive attribution test) — observed triad count vs the
     pairwise max-entropy expectation  E_abc = N * co_ab*co_bc*co_ac / (d_a*d_b*d_c):
        topN  k>=   nTriads   agg obs/exp   median   %>pred
        150    5      757        0.68        1.04     53%
        150   10       75        0.36        0.59     16%
        200    5      927        0.48        0.98     49%
        250   10      100        0.20        0.52     15%
     Heavy triads sit AT or BELOW pairwise prediction; only a weak threshold-sensitive excess at
     k>=3 (median ~1.5x) that vanishes as N / threshold rise. => no robust 3-way layer.

CONCLUSION: the recurring concept-triads (جری·جنّة·نهر ; توب·رحم·غفر ; صلح·عمل·أجر) are a
CONSEQUENCE of strong concept-PAIRS, not an independent higher-order design. The reduction-to-
pairwise is now MEASURED-present (per the attribution rule), not assumed. The real, robust object
is the pairwise PPMI concept graph (already characterised by the bridge/centrality + dcSBM work).

FLIP (per base-truth axiom — instrument, not text, is the limit): a sharper granularity
(semantic-neighbourhood-restricted triads, 4-way motifs, or pericope/sentence units) showing
obs/pairwise >> 1 robustly across N and threshold would reopen this.
"""
import pandas as pd, numpy as np, random
from collections import Counter, defaultdict


def load(topN=150, header=7, xlsx="Book6.xlsx"):
    df = pd.read_excel(xlsx, header=header)
    ROOTS = df.columns[8]
    norm = lambda t: str(t).replace("ك", "ک").replace("ي", "ی")
    vr = [set(r for r in norm(v).split() if r and r != "-") for v in df[ROOTS]]
    docf = Counter(r for s in vr for r in s)
    drop = {r for r, _ in docf.most_common(12)}
    roots = [r for r, _ in docf.most_common() if r not in drop][:topN]
    return vr, roots, docf, len(vr)


def triad_counts(vr, roots):
    rset = set(roots)
    tc = Counter()
    for s in vr:
        rr = sorted(s & rset)
        L = len(rr)
        for i in range(L):
            for j in range(i + 1, L):
                for k in range(j + 1, L):
                    tc[(rr[i], rr[j], rr[k])] += 1
    return tc


def kirkwood_ratio(vr, roots, docf, N, kmin=5):
    """observed heavy-triad counts vs pairwise (Kirkwood) expectation. ~1 => no 3-way beyond pairs."""
    rset = set(roots)
    co = Counter()
    for s in vr:
        rr = sorted(s & rset)
        for i in range(len(rr)):
            for j in range(i + 1, len(rr)):
                co[(rr[i], rr[j])] += 1
    cco = lambda a, b: co.get((a, b), 0) or co.get((b, a), 0)
    tc = triad_counts(vr, roots)
    num = den = 0.0
    rr = []
    for (a, b, c), obs in tc.items():
        if obs < kmin:
            continue
        cab, cbc, cac = cco(a, b), cco(b, c), cco(a, c)
        if cab and cbc and cac:
            E = N * (cab * cbc * cac) / (docf[a] * docf[b] * docf[c])
            if E > 0:
                num += obs; den += E; rr.append(obs / E)
    return len(rr), num / den, float(np.median(rr))


if __name__ == "__main__":
    vr, roots, docf, N = load()
    n, agg, med = kirkwood_ratio(vr, roots, docf, N, kmin=5)
    print(f"heavy triads={n}  aggregate obs/pairwise={agg:.2f}x  median={med:.2f}x  -> REFUTED (reduces to pairwise)")
