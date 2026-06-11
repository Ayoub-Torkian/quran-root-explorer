"""#55 — is the muqaṭṭaʿāt cohesion anchored in the REVELATION / "the Book" theme the letters precede?

Tests whether muqaṭṭaʿāt sūras over-express a revelation/"the Book" root cluster, permutation-nulled.
REV cluster (corpus orthography): کتب nazzala/نزل قرء ءیی(āyah) وحی ذکر بین تلو حکم رسل نبء صدق هدی.
RESULT (positive):
  WHOLE-SŪRA revelation-root rate: muqaṭṭaʿāt 0.0706 vs others 0.0479, diff +0.0227, z=+3.55, p=0.0002.
  OPENING (āyāt 1-3): muqaṭṭaʿāt 0.308 vs others 0.060 — ~5x concentration right after the letters
     (quantifies the classical observation: disjoint letters -> immediate mention of the Book).
=> the root-space cohesion (#53/#54) is anchored, in part, in a shared theme: scripture announcing
   scripture. CAVEAT: this explains the COMMON revelation theme, not the DIFFERENCE between letter-groups
   (حم vs الر); cohesion z=6.9 > theme z=3.5, so theme is PART of the cohesion, not all. Divinely-rooted.
"""
import os, sys
import numpy as np
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S, COL_AYAH as AY
rng = np.random.default_rng(55)
REV = set("کتب نزل قرء ءیی وحی ذکر بین تلو حکم رسل نبء صدق هدی".split())
MUQ = set([2,3,7,10,11,12,13,14,15,19,20,26,27,28,29,30,31,32,36,38,40,41,42,43,44,45,46,50,68])

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    ay = np.array([float(df.iloc[i][AY]) for i in range(len(df))])
    roots_of = lambda i: [w for w in str(df.iloc[i][R]).split() if w and w != 'nan']
    def rate(su, opening=False):
        idx = np.where(sur == su)[0]
        if opening: idx = [i for i in idx if ay[i] <= 3]
        toks = [w for i in idx for w in roots_of(i)]
        return (sum(w in REV for w in toks) / len(toks)) if toks else np.nan
    sus = [s for s in range(1, 115) if not np.isnan(rate(s))]
    rt = {s: rate(s) for s in sus}
    muq = [s for s in sus if s in MUQ]; obs = np.mean([rt[s] for s in muq]) - np.mean([rt[s] for s in sus if s not in MUQ])
    null = np.array([(lambda Z: np.mean([rt[s] for s in Z]) - np.mean([rt[s] for s in sus if s not in Z]))(set(rng.choice(sus, len(muq), replace=False))) for _ in range(5000)])
    print(f"whole-sūra REV rate: muqaṭṭaʿāt {np.mean([rt[s] for s in muq]):.4f} vs others {np.mean([rt[s] for s in sus if s not in MUQ]):.4f} | z={(obs-null.mean())/null.std():+.2f} p={np.mean(null>=obs):.4f}")
    ro = {s: rate(s, True) for s in sus}
    print(f"opening (1-3) REV rate: muqaṭṭaʿāt {np.nanmean([ro[s] for s in muq]):.4f} vs others {np.nanmean([ro[s] for s in sus if s not in MUQ]):.4f}")

if __name__ == "__main__":
    main()
