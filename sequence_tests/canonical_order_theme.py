"""#57 — does the CANONICAL sūra order carry thematic coherence beyond the length gradient? + NMF themes.

Divinely-rooted (roots + canonical arrangement; NO ḥarakāt). Sūra root-TF-IDF vectors; adjacency statistic
= mean cosine between canonically-consecutive sūras; two nulls.
RESULT (positive, length-controlled):
  adjacency cosine = 0.3465
  vs FULL-shuffle null 0.2509 -> z=+10.6 (but muṣḥaf is length-ordered: position↔length r=-0.73, so most
     of this is the length/register gradient).
  vs LENGTH-BAND(6) null 0.3282 -> z=+3.14, p=0.0007: even preserving the length backbone (shuffle only
     within blocks of 6 consecutive sūras), neighbors are MORE root-similar than chance. Genuine LOCAL
     thematic coherence in the canonical arrangement beyond length. Generalizes the muqaṭṭaʿāt contiguity
     to the whole muṣḥaf. (Magnitude modest: +0.018 over the length-controlled baseline, but significant.)
NMF (8 themes) recovers interpretable axes incl. a clean refuge/Muʿawwidhāt cluster (شرر وسوس حسد عوذ زلزل)
and eschatology (یوم کذب ویل / علم یقن قبر) — descriptive validation that the decomposition finds real themes.
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.decomposition import NMF
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S
rng = np.random.default_rng(57)

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    sdoc = lambda s: " ".join(w for i in np.where(sur == s)[0] for w in str(df.iloc[i][R]).split() if w and w != 'nan')
    order = [s for s in range(1, 115) if sdoc(s).strip()]
    docs = [sdoc(s) for s in order]
    vec = TfidfVectorizer(analyzer=str.split, min_df=2); X = vec.fit_transform(docs)
    V = normalize(X.toarray()); length = np.array([len(d.split()) for d in docs]); canon = np.arange(len(order))
    adj = lambda p: np.mean([V[p[i]] @ V[p[i + 1]] for i in range(len(p) - 1)])
    obs = adj(canon)
    nullA = np.array([adj(rng.permutation(len(order))) for _ in range(3000)])
    def blk(b=6):
        p = canon.copy()
        for st in range(0, len(p), b):
            seg = p[st:st + b].copy(); rng.shuffle(seg); p[st:st + b] = seg
        return p
    nullB = np.array([adj(blk(6)) for _ in range(3000)])
    print(f"adjacency cosine = {obs:.4f}")
    print(f"  vs full-shuffle  {nullA.mean():.4f} z={(obs-nullA.mean())/nullA.std():+.2f} p={np.mean(nullA>=obs):.4f}")
    print(f"  vs length-band(6) {nullB.mean():.4f} z={(obs-nullB.mean())/nullB.std():+.2f} p={np.mean(nullB>=obs):.4f}")
    print(f"  position-length r = {np.corrcoef(canon, length)[0,1]:+.2f}")
    W = NMF(n_components=8, init='nndsvd', random_state=0, max_iter=400).fit(X)
    feat = np.array(vec.get_feature_names_out())
    print("NMF themes:")
    for k, comp in enumerate(W.components_):
        print(f"  T{k+1}: " + " ".join(feat[np.argsort(comp)[::-1][:8]]))

if __name__ == "__main__":
    main()
