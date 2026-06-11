"""#66 — LOCAL vs GLOBAL (multi-location) collocation. For root-pairs co-occurring in āyahs: PPMI = association
strength; sūra-SPREAD (# distinct sūras of co-occurrence) = local↔global. Two orthogonal axes.
RESULT: GLOBAL motif-pairs (high spread + high PPMI): ءرض-سمو (61 sūras, +2.20), شیء-کلل (51,+1.66),
ءمن-عمل (50,+1.02). Frequency co-occurrence (high spread, low PPMI): ءله-قول/علم/کون. LOCAL formulae
(high PPMI, ≤3 sūras): نسو-نکح, حرم-شهر, طلق-عرف, ءخو/ءبو-ءسف (Yūsuf). Global high-PPMI = conceptual face of #42.
"""
import os, sys, warnings, itertools
import numpy as np
warnings.filterwarnings("ignore")
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S

def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    N = len(df); sur = [int(df.iloc[i][S]) for i in range(N)]
    ar = [list({w for w in str(df.iloc[i][R]).split() if w and w != 'nan'}) for i in range(N)]
    freq = Counter(w for rs in ar for w in rs); keep = {w for w, n in freq.items() if n >= 8}
    cnt = Counter(); suras = defaultdict(set)
    for i, rs in enumerate(ar):
        rs = [w for w in rs if w in keep]
        for a, b in itertools.combinations(sorted(rs), 2):
            cnt[(a, b)] += 1; suras[(a, b)].add(sur[i])
    pairs = [(p, cnt[p], len(suras[p])) for p in cnt if cnt[p] >= 6]
    ppmi = lambda a, b, c: np.log((c / N) / ((freq[a] / N) * (freq[b] / N)))
    print("GLOBAL (multi-location) — most distinct sūras:")
    for (a, b), c, ns in sorted(pairs, key=lambda x: -x[2])[:12]:
        print(f"  {a}-{b:6s} sūras={ns:3d} āyahs={c:3d} ppmi={ppmi(a,b,c):+.2f}")
    print("LOCAL (concentrated, ≤3 sūras, high PPMI):")
    for (a, b), c, ns in sorted([p for p in pairs if p[2] <= 3], key=lambda x: -ppmi(x[0][0], x[0][1], x[1]))[:12]:
        print(f"  {a}-{b:6s} sūras={ns} āyahs={c:2d} ppmi={ppmi(a,b,c):+.2f}")
    sp = np.array([ns for _, _, ns in pairs])
    print(f"pairs={len(pairs)} spread median={np.median(sp):.0f} max={sp.max()} global(≥20)={np.sum(sp>=20)} local(≤3)={np.sum(sp<=3)}")

if __name__ == "__main__":
    main()
