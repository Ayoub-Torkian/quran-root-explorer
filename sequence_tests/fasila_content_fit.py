"""#62 — fāṣila–CONTENT FIT (munāsabat al-fawāṣil): does the āyah-FINAL word predict the BODY content?
Group āyahs by their ending (ROOT grain and MORPHOLOGY grain — user: morphology is apt for the wordform);
body-cohesion (root-TF-IDF) vs random same-N null; strict control = strip the ending's ROOT from the body.
RESULT (strong, Qur'an-internal): ROOT grain mean z=+11.3 (13/14 z>2); MORPHOLOGY grain mean z=+12.1
(16/16 z>2: قدیر +32, رحیم +29, صادقین +27, حکیم +26, …). The ending predicts OTHER content (control barely
changes z) → genuine fit, not self-repetition. Reconciles with #60/E2 (caps own āyah, doesn't chain to next).
CAVEAT: Qur'an-internal; cross-text distinctiveness untested — NEXT: same test on comparators (rearrangement
protocol). Fuses rhyme (Lens 3) × meaning × wazn (Lens 8 faʿīl attributes).
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SEGMENTED as SEG
rng = np.random.default_rng(62)

def run(df, by):  # by = 'root' or 'morph'
    roots = [[w for w in str(df.iloc[i][R]).split() if w and w != 'nan'] for i in range(len(df))]
    segs = [[w for w in str(df.iloc[i][SEG]).split() if w] for i in range(len(df))]
    keep = [i for i in range(len(df)) if len(roots[i]) >= 4 and segs[i]]
    end = [(roots[i][-1] if by == 'root' else segs[i][-1]) for i in keep]
    body = [" ".join(w for w in roots[i][:-1] if w != roots[i][-1]) for i in keep]  # strip ending root
    V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([b if b.strip() else "x" for b in body]).toarray())
    coh = lambda ix: (lambda M, iu: M[iu].mean())(V[ix] @ V[ix].T, np.triu_indices(len(ix), 1)) if len(ix) > 1 else np.nan
    ec = Counter(end); top = [w for w, n in ec.most_common(60) if n >= 15][:16]
    allidx = np.arange(len(keep)); res = []
    for w in top:
        ix = [k for k in range(len(keep)) if end[k] == w]
        o = coh(ix); null = np.array([coh(rng.choice(allidx, len(ix), replace=False)) for _ in range(600)])
        res.append((w, len(ix), o, (o - null.mean()) / null.std()))
    print(f"\n[{by}] fāṣila → body-content cohesion:")
    for w, nn, o, z in sorted(res, key=lambda x: -x[3]):
        print(f"   end={w:10s} n={nn:4d} body-coh={o:.3f} z={z:+.2f}")
    zs = [z for *_, z in res]; print(f"  mean z = {np.mean(zs):+.2f} ({sum(z>2 for z in zs)}/{len(zs)} z>2)")

def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    run(df, 'root'); run(df, 'morph')

if __name__ == "__main__":
    main()
