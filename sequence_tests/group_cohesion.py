"""#59 / CROSS-IMPACT D3 — is muqaṭṭaʿāt root-space cohesion SPECIAL, or do other named sūra-groups cohere too?
Applies the #53 cohesion test (sūra root-TF-IDF, mean pairwise cosine vs random same-N null) to several
traditional groups. RESULT: cohesion is a GENERAL property of length/topically-homogeneous groups
(al-sabʿ al-ṭiwāl cos 0.78 z=+5.4; Medinan z=+5.4) — comparable to or above muqaṭṭaʿāt (0.53, z=+6.8).
=> the muqaṭṭaʿāt CONTENT-cohesion leg (#53/#54) is not sui-generis; down-weight it. Position pointer
(#50/#51) + half-alphabet (#50) remain distinctive. Nuance: letter-defined group > several MEANING-defined
groups (Musabbiḥāt z=+1.5 n.s., ḥamdu-openers z=+1.5 n.s.), so not a mere shared-opening-word effect.
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S
rng = np.random.default_rng(59)
MED = {2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110}
GROUPS = {
 "muqaṭṭaʿāt (letters)": [2,3,7,10,11,12,13,14,15,19,20,26,27,28,29,30,31,32,36,38,40,41,42,43,44,45,46,50,68],
 "Ḥawāmīm": [40,41,42,43,44,45,46],
 "al-sabʿ al-ṭiwāl": [2,3,4,5,6,7,9],
 "Musabbiḥāt (sabbaḥa)": [17,57,59,61,62,64,87],
 "al-ḥamdu openers": [1,6,18,34,35],
 "closing quls": [109,112,113,114],
 "Medinan": sorted(MED),
}

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    sdoc = lambda s: " ".join(w for i in np.where(sur == s)[0] for w in str(df.iloc[i][R]).split() if w and w != 'nan')
    order = [s for s in range(1, 115) if sdoc(s).strip()]
    V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([sdoc(s) for s in order]).toarray())
    pos = {s: k for k, s in enumerate(order)}
    def coh(ss):
        ks = [pos[s] for s in ss if s in pos]
        if len(ks) < 2: return np.nan
        M = V[ks] @ V[ks].T; iu = np.triu_indices(len(ks), 1); return M[iu].mean()
    GROUPS["Meccan"] = [s for s in range(1, 115) if s not in MED]
    for label, ss in GROUPS.items():
        sel = [s for s in ss if s in pos]; n = len(sel); o = coh(sel)
        null = np.array([coh(rng.choice(order, n, replace=False)) for _ in range(4000)])
        print(f"  {label:22s} n={n:2d} cos={o:.3f} z={(o-null.mean())/null.std():+.2f} p={np.mean(null>=o):.4f}")

if __name__ == "__main__":
    main()
