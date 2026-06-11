"""#74 — TEMPORAL RE-AIMING SWEEP across the seal lexicon (second-tier endings; #71 control standard).

DESIGN: all āyah-final words with ≥35 occurrences beyond the #71 trio (12 classes: مبين العالمين عليم
رحيم عظيم الظالمين تعلمون يءمنون يعملون الحكيم العظيم قدير). Per class: 3 nuzūl waves (1D k-means,
pre-stated) → temporal content-separation with the DECISIVE control built in from the start (cross-sūra
pairs only + sūra-level permutation null, 2000×) → Bonferroni over the 12-class sweep.

RESULTS:
  SURVIVOR (Bonferroni-safe, p<0.0042): عليم  d=+0.0187  z=+3.52  p=0.0010.
  Nominal only: يعملون z=+2.22 (p=.024, fails ×12). All else null — incl. مبين (−0.72; its #70 marginal
  rate-wave carries NO content shift) and رحيم (+0.22: content-stable wherever it appears).

THE TWIST — rate-waves and content-re-aiming are DISSOCIABLE (2×2 typology with #70/#71):
  BOTH:          يعلمون · اليم          (waves in usage AND re-aimed content)
  RATE only:     تعملون                 (#70 wave, #71 content-shift fell to the sūra-block confound)
  CONTENT only:  عليم                   (register-only in rate (#70), yet re-aimed in content (#74))
  NEITHER:       مبين رحيم الظالمين قدير … (stable formulas)

عليم ARC (descriptive): Meccan wave = knowledge-CONTEST narratives (سحر حکم ربب — incl. the ساحر عليم
epithet verses 7:109/112, 26:34/37 where the ending describes the SORCERER) → early-Medinan = covenant/
legal audit (کتب 12, شهد 8, قتل, وعد) → late-Medinan = community purification & grace (زکو نور فضل هدی;
9:103). METHOD CATCH (filed to cross-impact): the ending-WORD class is REFERENT-MIXED — عليم caps both
divine-attribute seals and the sorcerer-epithet; part of its temporal shift is referent-class composition.
Future #62-style analyses should split ending-classes by referent before claiming seal semantics.

CAVEATS: k=3 pre-stated; nuzūl = traditional chronology; d magnitudes small (~0.02) though gated;
Qur'an-internal. EVIDENCE #74. RUN DISCIPLINE: /tmp heredoc; host copy for the user.
"""
import re, os, sys
import numpy as np
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_DIACRITIZED as D, COL_SURAH as S, COL_ROOTS as RR, COL_REV_ORDER as RO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans

rng = np.random.default_rng(74)
_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)


def nl(t):
    t = _DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t)
    t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()


GEN = {"ءله", "کون", "قول"}
OWN = {"مبين": {"بین"}, "العالمين": {"علم"}, "عليم": {"علم"}, "رحيم": {"رحم"}, "عظيم": {"عظم"},
       "الظالمين": {"ظلم"}, "تعلمون": {"علم"}, "يءمنون": {"ءمن"}, "يعملون": {"عمل"},
       "الحكيم": {"حکم"}, "العظيم": {"عظم"}, "قدير": {"قدر"}}


def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    nuz = {}
    for i in range(len(df)):
        try:
            nuz[int(df.iloc[i][S])] = int(float(df.iloc[i][RO]))
        except Exception:
            pass
    nuzr = np.array([nuz.get(s, 999) for s in sur])
    finals = []
    for i in range(len(df)):
        tt = WA.findall(nl(df.iloc[i][D]))
        finals.append(tt[-1] if tt else "")
    finals = np.array(finals)
    roots = [str(df.iloc[i][RR]).split() for i in range(len(df))]
    cnt = Counter(finals); DONE = {"تعملون", "يعلمون", "اليم", ""}
    SEALS = [w for w, c in cnt.most_common(40) if c >= 35 and w not in DONE]
    print("sweep:", SEALS, "| Bonferroni n =", len(SEALS))
    res = []
    for seal in SEALS:
        idxs = np.where(finals == seal)[0]; nz = nuzr[idxs]
        if len(np.unique(nz)) < 6:
            continue
        lab = KMeans(n_clusters=3, n_init=10, random_state=71).fit(nz.reshape(-1, 1)).labels_
        excl = GEN | OWN.get(seal, set())
        docs = [" ".join(r for r in roots[i] if r not in excl) for i in idxs]
        X = normalize(TfidfVectorizer(analyzer=str.split, min_df=1).fit_transform(docs))
        Sim = (X @ X.T).toarray()
        ss = sur[idxs]; same = ss[:, None] == ss[None, :]
        valid = np.triu(np.ones_like(Sim, dtype=bool), 1) & ~same

        def sep(lv):
            Wm = lv[:, None] == lv[None, :]
            wi = Sim[valid & Wm]; bt = Sim[valid & ~Wm]
            return wi.mean() - bt.mean() if len(wi) > 5 and len(bt) > 5 else np.nan

        obs = sep(lab)
        usuras = np.unique(ss); sl = {u: lab[ss == u][0] for u in usuras}
        null = []
        for _ in range(2000):
            perm = rng.permutation([sl[u] for u in usuras]); pl = dict(zip(usuras, perm))
            null.append(sep(np.array([pl[u] for u in ss])))
        null = np.array(null)
        z = (obs - null.mean()) / (null.std() + 1e-12); p = np.mean(null >= obs)
        res.append((seal, len(idxs), obs, z, p))
        print(f"{seal:12s} n={len(idxs):3d}  d={obs:+.4f}  z={z:+.2f}  p={p:.4f}")
    nb = len(res)
    print(f"Bonferroni-safe (p<{0.05/nb:.4f}):", [r[0] for r in res if r[4] < 0.05 / nb])


if __name__ == "__main__":
    main()
