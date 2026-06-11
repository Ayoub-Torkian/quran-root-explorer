"""DoE E4 — Mantel test: does sūra position-distance track content-distance, canonical vs nuzūl?
Mantel r between |i−j| (position) and 1−root-cosine (content) over sūras; permutation null.
RESULT: CANONICAL r=+0.325 (z=+8.5), NUZŪL r=+0.290 (z=+7.6), both p<1e-4. Position tracks content in both;
canonical EDGES nuzūl (reverses #58 seam result) → muṣḥaf optimizes GLOBAL grouping over local seam-chronology.
CAVEATS: muṣḥaf length-ordering inflates canonical (content-by-length gradient; only length-controlled #57 is
the genuine thematic part); per E1-comparator this is Qur'an-INTERNAL, not a cross-text distinctive. Generalizes #57.
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S, COL_REV_ORDER as RO
rng = np.random.default_rng(4)

def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    sdoc = lambda s: " ".join(w for i in np.where(sur == s)[0] for w in str(df.iloc[i][R]).split() if w and w != 'nan')
    suras = [s for s in range(1, 115) if sdoc(s).strip()]
    V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([sdoc(s) for s in suras]).toarray())
    Dcon = 1 - (V @ V.T)
    nuz = {}
    for i in range(len(df)):
        try: nuz[int(df.iloc[i][S])] = int(float(df.iloc[i][RO]))
        except Exception: pass
    iu = np.triu_indices(len(suras), 1); b = Dcon[iu]
    def mantel(pv):
        D = np.abs(pv[:, None] - pv[None, :]); return np.corrcoef(D[iu], b)[0, 1]
    for lab, pv in [("CANONICAL", np.array([s for s in suras], float)),
                    ("NUZŪL", np.array([nuz.get(s, 999) for s in suras], float))]:
        obs = mantel(pv); null = np.array([mantel(pv[rng.permutation(len(suras))]) for _ in range(5000)])
        print(f"  {lab:10s} Mantel r={obs:+.3f} z={(obs-null.mean())/null.std():+.2f} p={np.mean(np.abs(null)>=abs(obs)):.4f}")

if __name__ == "__main__":
    main()
