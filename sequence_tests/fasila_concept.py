"""#60 / DoE E2 — fāṣila-CONCEPT stream: does meaning chain at the verse-ends beyond chance?
Root embedding from āyah-level co-occurrence (PPMI + TruncatedSVD-50); for each āyah pick the end / start /
random root; mean cosine of consecutive picks within sūra vs within-sūra shuffle null. Divinely-rooted.
RESULT (negative for the special hypothesis): all positions chain strongly (general adjacency continuity),
but the fāṣila (end) chains LEAST — start z=+17.6, random z=+10.0, end z=+7.2. Meaning does NOT specially
chain at verse-ends; m2 ordering mechanism not privileged. NUANCE: the rhyme-constrained end-word partially
decouples its concept from the semantic flow (rhyme vs continuity trade-off at the fāṣila; links Lens 3 × 16).
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from collections import Counter, defaultdict
import scipy.sparse as sp
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S, COL_AYAH as AY
rng = np.random.default_rng(59)

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    ay = np.array([float(df.iloc[i][AY]) for i in range(len(df))])
    rl = [[w for w in str(df.iloc[i][R]).split() if w and w != 'nan'] for i in range(len(df))]
    vocab = sorted({w for r in rl for w in r}); vi = {w: k for k, w in enumerate(vocab)}
    cnt = Counter(); co = defaultdict(float); tot = 0.0
    for r in rl:
        u = set(r)
        for w in u: cnt[w] += 1
        for a in u:
            for b in u:
                if a < b: co[(a, b)] += 1; tot += 1
    rows, cols, vals = [], [], []
    for (a, b), v in co.items():
        pmi = np.log((v * tot) / (cnt[a] * cnt[b] + 1e-9) + 1e-12)
        if pmi > 0: rows += [vi[a], vi[b]]; cols += [vi[b], vi[a]]; vals += [pmi, pmi]
    M = sp.csr_matrix((vals, (rows, cols)), shape=(len(vocab), len(vocab)))
    E = normalize(TruncatedSVD(n_components=50, random_state=0).fit_transform(M))
    vec = {w: E[vi[w]] for w in vocab}
    def stream(which):
        return [None if not r else (r[-1] if which == 'end' else r[0] if which == 'start' else r[rng.integers(len(r))]) for r in rl]
    def mc(assign):
        cs = []
        for s in range(1, 115):
            idx = np.where(sur == s)[0]; idx = idx[np.argsort(ay[idx])]
            p = [assign[i] for i in idx if assign[i] is not None]
            cs += [float(vec[p[j]] @ vec[p[j + 1]]) for j in range(len(p) - 1)]
        return np.mean(cs)
    for w in ('end', 'start', 'rand'):
        st = stream(w); obs = mc(st)
        null = np.empty(300)
        for b in range(300):
            sh = list(st)
            for s in range(1, 115):
                idx = [i for i in np.where(sur == s)[0]]; v = [sh[i] for i in idx]; rng.shuffle(v)
                for i, x in zip(idx, v): sh[i] = x
            null[b] = mc(sh)
        print(f"  {w:5s}: mean-cos={obs:.4f} z={(obs-null.mean())/null.std():+.2f} p={np.mean(null>=obs):.4f}")

if __name__ == "__main__":
    main()
