"""#56 — per-letter DISTINCTIVE root-signatures: are same-letter families separable from EACH OTHER in
root-space (beyond the shared 'Book' theme)? + top distinctive roots per family.

RESULT (nuanced):
  GLOBAL SEPARABILITY = NULL. within-group cos 0.574 vs between-group 0.570, diff +0.004, z=+0.30, p=0.37
    (permutation: shuffle family labels among grouped muqaṭṭaʿāt sūras, preserving sizes). The #53 cohesion
    is a SHARED-theme effect, not letter-specific separation; the shared revelation/register vocabulary
    dominates the full TF-IDF vector and swamps letter-specific differences.
  BUT per-family TOP DISTINCTIVE ROOTS are vividly thematic:
    الم -> legal/communal (شری trade, ربو ribā, طلق divorce, حجج pilgrimage) — Baqara/Āl-ʿImrān legislation
    الر -> Yūsuf narrative (سجن prison, کیل measure, سبع seven, کید scheming, ءبو father)
    طس -> Mūsā–Pharaoh cycle (سحر sorcery, فرعن Pharaoh, جند troops, مدن Madyan, شعر)
    حم -> dispute/judgment (فرعن, قضی decree, جوب response, کبر arrogance)
  CAVEAT: distinctive roots reflect WHICH NARRATIVES each group's sūras contain (الر holds Sūrat Yūsuf ->
    Yūsuf vocab); the 'signature' is confounded with narrative content and does NOT show a letter->theme
    cipher. Same-letter sūras share narrative vocabulary; nothing here demonstrates the letter causes it.
Divinely-rooted (roots, canonical grouping); Qur'an-internal.
"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S
rng = np.random.default_rng(56)
GROUPS = {"الم":[2,3,29,30,31,32], "حم":[40,41,42,43,44,45,46], "الر":[10,11,12,14,15], "طس":[26,27,28]}

def main():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    sdoc = lambda s: " ".join(w for i in np.where(sur == s)[0] for w in str(df.iloc[i][R]).split() if w and w != 'nan')
    allg = [s for g in GROUPS.values() for s in g]
    order = [s for s in range(1, 115) if sdoc(s).strip()]
    V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([sdoc(s) for s in order]).toarray())
    pos = {s: k for k, s in enumerate(order)}
    cos = lambda a, b: float(V[pos[a]] @ V[pos[b]])
    def wb(lab):
        wi, be = [], []
        for i in range(len(allg)):
            for j in range(i + 1, len(allg)):
                a, b = allg[i], allg[j]
                (wi if lab[a] == lab[b] else be).append(cos(a, b))
        return np.mean(wi), np.mean(be)
    lab = {s: g for g, ss in GROUPS.items() for s in ss}
    w, b = wb(lab); obs = w - b
    sizes = [len(v) for v in GROUPS.values()]; gn = list(GROUPS)
    null = []
    for _ in range(5000):
        perm = rng.permutation(allg); l2 = {}; idx = 0
        for g, sz in zip(gn, sizes):
            for s in perm[idx:idx + sz]: l2[s] = g
            idx += sz
        x, y = wb(l2); null.append(x - y)
    null = np.array(null)
    print(f"SEPARABILITY within {w:.3f} vs between {b:.3f} | diff {obs:+.3f} z={(obs-null.mean())/null.std():+.2f} p={np.mean(null>=obs):.4f}")
    allr = [w for s in order for w in sdoc(s).split()]; cf = Counter(allr); Ct = len(allr)
    print("TOP DISTINCTIVE ROOTS per family (rate-ratio vs corpus, min count 8):")
    for g, ss in GROUPS.items():
        toks = [w for s in ss for w in sdoc(s).split()]; gc = Counter(toks); gt = len(toks)
        cand = sorted([(r, (gc[r] / gt) / (cf[r] / Ct)) for r in gc if gc[r] >= 8], key=lambda x: -x[1])
        print(f"  {g}: " + ", ".join(f"{r}({ra:.1f}x)" for r, ra in cand[:8]))

if __name__ == "__main__":
    main()
