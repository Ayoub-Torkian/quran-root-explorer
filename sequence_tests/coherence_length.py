"""DoE E1 — coherence-length / block-rearrangement curve: where (at what scale) does order carry structure?
(A) mean āyah root-cosine at lag L (within sūra) → coherence length; (B) adjacency cosine after within-block
shuffle of size b → scale at which order matters. Divinely-rooted; baseline-gated (Qur'an-internal).
RESULT: coherence strongest at lag-1 (~1.8× baseline), decays to chance by ~lag 8–13 (short, pericope-scale).
Adjacency degrades with block size (0.074→0.040), so order lives at the FINEST scale. Sharpens #57 (local).
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S, COL_AYAH as AY
rng = np.random.default_rng(1)

def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))]); ay = np.array([float(df.iloc[i][AY]) for i in range(len(df))])
    docs = [" ".join(w for w in str(df.iloc[i][R]).split() if w and w != 'nan') for i in range(len(df))]
    V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([d if d.strip() else "x" for d in docs]).toarray())
    obs = []
    for s in range(1, 115):
        idx = np.where(sur == s)[0]
        if len(idx): obs.append(idx[np.argsort(ay[idx])])
    print("(A) coherence length: mean root-cosine between āyāt L apart (within sūra)")
    for L in [1, 2, 3, 5, 8, 13, 21]:
        cs = [float(V[o[i]] @ V[o[i + L]]) for o in obs for i in range(len(o) - L)]
        if cs: print(f"   lag {L:3d}: cos={np.mean(cs):.4f}")
    base = [float(V[o[a]] @ V[o[b]]) for o in obs if len(o) >= 2 for a, b in [rng.choice(len(o), 2, replace=False)]]
    print(f"   random within-sūra baseline cos={np.mean(base):.4f}")
    def adj(b):
        cs = []
        for o in obs:
            p = o.copy()
            if b > 1:
                for st in range(0, len(p), b):
                    seg = p[st:st + b].copy(); rng.shuffle(seg); p[st:st + b] = seg
            cs += [float(V[p[i]] @ V[p[i + 1]]) for i in range(len(p) - 1)]
        return np.mean(cs)
    print("(B) adjacency cosine after within-block shuffle (size b):")
    for b in [1, 2, 3, 5, 8, 1000]:
        print(f"   b={'full' if b==1000 else b}: {adj(b):.4f}")

if __name__ == "__main__":
    main()
