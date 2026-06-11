"""#58 — sūra-junction interlock (tanāsub al-suwar) under REARRANGEMENT scenarios (user-suggested).
Does end-of-sūra link to start-of-next in root-space, and is the CANONICAL order specially interlocked
vs the legitimate NUZŪL (revelation) order? Divinely-rooted (roots + canonical/chronological order).

RESULT: seam-interlock is REAL under both orderings (full-order-shuffle null 0.071):
  CANONICAL muṣḥaf  : junction 0.0911, z=+3.98, p<1e-4
  NUZŪL (revelation): junction 0.1009, z=+5.92, p<1e-4   (> canonical)
=> modest support for tanāsub al-suwar, BUT the canonical order is NOT specially optimized for it —
chronology interlocks more (same-period sūras share theme/register). Honest reading: the muṣḥaf sustains
significant seam-coherence DESPITE abandoning the chronological grouping that would maximize it (coherence
against the grain); seam-interlock is not evidence of unique canonical design. (Simple random-pairing null
gives canonical z=+2.47.) Length/period-locality is the main driver; overlaps #57.
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S, COL_AYAH as AY, COL_REV_ORDER as RO
rng = np.random.default_rng(58)

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    ay = np.array([float(df.iloc[i][AY]) for i in range(len(df))])
    rts = lambda i: [w for w in str(df.iloc[i][R]).split() if w and w != 'nan']
    W = 5; suras = [s for s in range(1, 115) if (sur == s).any()]
    nuz = {}
    for i in range(len(df)):
        try: nuz[int(df.iloc[i][S])] = int(float(df.iloc[i][RO]))
        except Exception: pass
    sd, ed = {}, {}
    for s in suras:
        idx = np.where(sur == s)[0]; o = idx[np.argsort(ay[idx])]
        sd[s] = " ".join(w for i in o[:W] for w in rts(i)); ed[s] = " ".join(w for i in o[-W:] for w in rts(i))
    keys = [("s", s) for s in suras] + [("e", s) for s in suras]
    docs = [({"s": sd, "e": ed}[k][s] or "x") for k, s in keys]
    V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([d if d.strip() else "x" for d in docs]).toarray())
    pos = {k: i for i, k in enumerate(keys)}; cos = lambda a, b: float(V[pos[a]] @ V[pos[b]])
    junction = lambda order: np.mean([cos(("e", order[i]), ("s", order[i + 1])) for i in range(len(order) - 1)])
    jc = junction(suras); jn = junction(sorted(suras, key=lambda s: nuz.get(s, 999)))
    null = np.array([junction(list(rng.permutation(suras))) for _ in range(2000)])
    z = lambda x: (x - null.mean()) / null.std()
    print(f"CANONICAL  junction {jc:.4f}  z={z(jc):+.2f}  p={np.mean(null>=jc):.4f}")
    print(f"NUZŪL      junction {jn:.4f}  z={z(jn):+.2f}  p={np.mean(null>=jn):.4f}")
    print(f"random null {null.mean():.4f} ± {null.std():.4f}  | canonical - nuzūl = {jc-jn:+.4f}")

if __name__ == "__main__":
    main()
