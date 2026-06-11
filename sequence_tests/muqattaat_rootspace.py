"""#53 — SIGNAL-GEOMETRY on ROOTS (divinely-rooted): is the muqaṭṭaʿāt grouping coherent in root-space?

Each sūra -> root-TF-IDF vector; cohesion = mean pairwise cosine; null = random sūra-subsets of same size.
RESULT (positive): the grouping is NOT merely positional — it is strongly coherent in root/semantic space.
  all 29 muqaṭṭaʿāt: cosine 0.530 vs null 0.251, z=+6.92, p<1e-4
  Ḥā-Mīm (7 consec.):       0.545 vs 0.253, z=+3.08, p=0.003
  Alif-Lām-Rā (5):          0.565 vs 0.252, z=+2.68, p=0.010
  Alif-Lām-Mīm (6):         0.599 vs 0.252, z=+3.27, p=0.003
=> opening letters track LEXICAL-THEMATIC families; same-letter sūras share root content.
CAVEAT: muqaṭṭaʿāt are mostly Meccan, so part of the 29-set cohesion is shared register; but the
same-letter subgroups being TIGHTER than the 29-set average argues for letter-specific structure beyond
register. Qur'an-internal (nulls = random sūra-subsets); divinely-rooted (roots, not ḥarakāt).
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S
rng = np.random.default_rng(53)

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    docs = {}
    for s in range(1, 115):
        toks = []
        for i in np.where(sur == s)[0]:
            toks += [w for w in str(df.iloc[i][R]).split() if w and w != 'nan']
        docs[s] = " ".join(toks)
    order = [s for s in range(1, 115) if docs[s].strip()]
    X = TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([docs[s] for s in order])
    V = normalize(X.toarray()); pos = {s: k for k, s in enumerate(order)}
    def cohesion(ss):
        ks = [pos[s] for s in ss if s in pos]
        if len(ks) < 2: return np.nan
        M = V[ks] @ V[ks].T; iu = np.triu_indices(len(ks), 1)
        return M[iu].mean()
    def test(ss, label):
        obs = cohesion(ss); n = len([s for s in ss if s in pos])
        null = np.array([cohesion(rng.choice(order, n, replace=False)) for _ in range(5000)])
        print(f"   {label:22s} n={n} cos={obs:.4f} | null {null.mean():.4f} | z={(obs-null.mean())/null.std():+.2f} p={np.mean(null>=obs):.4f}")
    MUQ = [2,3,7,10,11,12,13,14,15,19,20,26,27,28,29,30,31,32,36,38,40,41,42,43,44,45,46,50,68]
    print("ROOT-SPACE COHESION (mean pairwise cosine) vs random sūra-subsets:")
    test(MUQ, "all muqaṭṭaʿāt (29)")
    test([40,41,42,43,44,45,46], "Ḥā-Mīm group (7)")
    test([10,11,12,14,15], "Alif-Lām-Rā (5)")
    test([2,3,29,30,31,32], "Alif-Lām-Mīm (6)")

if __name__ == "__main__":
    main()
