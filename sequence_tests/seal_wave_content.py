"""#71 — ĀYAH-GRAIN WAVE CONTENT of the true-wave seals (تعملون/يعلمون/اليم) — follow-up to #70.

QUESTION: #70 found these three seal-classes deploy in nuzūl waves finer than the Meccan/Medinan split.
What does each seal DO inside its waves — same content throughout (usage-intensity phases), or does the
same cadence get RE-AIMED at new domains over revelation time?

METHOD: for each seal, take its āyahs (final-word match, nl-normalized per the #43 tokenizer rule),
cluster their nuzūl positions into 3 temporal waves (1D k-means, pre-stated), profile each wave's
distinctive roots (rate-ratio vs the other waves; generic roots ءله/کون/قول and the seal's own root
excluded), and test TEMPORAL CONTENT SEPARATION = mean within-wave − between-wave TF-IDF root-cosine.
GATE (positive control): a planted CONTENT split (k-means on the vectors) fires at z≈+5.5…+10.
CONFOUND CONTROL (decisive): same-sūra pairs share vocabulary and waves contain sūra blocks → recompute
separation on CROSS-SŪRA pairs only, with a SŪRA-LEVEL permutation null (whole sūras swap waves).

RESULTS:
  naive (āyah-perm, all pairs):  تعملون z=+2.39 p=.016 · يعلمون z=+3.91 p=.0015 · اليم z=+2.70 p=.005
  CONTROLLED (cross-sūra only, sūra-level perm):
    يعلمون  z=+3.38 p=0.0005  -> SURVIVES (gated)
    اليم    z=+2.48 p=0.012   -> SURVIVES (Bonferroni×3 ≈ .036)
    تعملون  z=+1.23 p=0.12    -> FALLS — its wave-content was substantially the al-Baqara sūra-block.
  CONTENT ARCS (descriptive, from the wave profiles):
    يعلمون: Meccan wave = creation-signs ignorance (جعل ءرض سمو رزق قدر: "most of them do not know" about
      creation/provision) → Medinan wave = scripture-community ignorance (ءمن کتب فرق کفر دین: People of
      the Book, dīn). The polemic's TARGET shifts from cosmos to kitāb.
    اليم: Meccan = punishment-stories of past nations (ءمم وعد ظلم ءیی) → early-Medinan = covenant-breach
      (شری "selling cheap", قتل, کفر) → late-Medinan = community-era warnings (رسل, ءذن, ءمن). The
      threat-seal moves from history to the living community.
VERDICT: for يعلمون and اليم the seal is RE-AIMED across revelation time — same cadence, evolving
referential domain — robust to the sūra-vocabulary confound; for تعملون the shift is confound-limited
(parked). RE-READS #62: the fāṣila content-fit has a TIME dimension — fit is to the mission-phase's
domain, not to one fixed topic. Qur'an-internal (nuzūl structure; no comparator exists).
CAVEATS: k=3 waves pre-stated; nuzūl order is the traditional chronology (used as the established
rearrangement frame); separation magnitudes modest (d≈0.01) though gated. EVIDENCE #71.
RUN DISCIPLINE: /tmp heredoc; host copy for the user.
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

rng = np.random.default_rng(71)
_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)


def nl(t):
    t = _DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t)
    t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()


GEN = {"ءله", "کون", "قول"}
EXCL = {"تعملون": {"عمل"}, "يعلمون": {"علم"}, "اليم": {"ءلم", "عذب"}}


def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    AY = [c for c in df.columns if "آیه" in c and "متن" not in c][0]
    ayn = np.array([int(df.iloc[i][AY]) for i in range(len(df))])
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

    def sep_stat(Sim, labels, mask_same=None):
        wi, bt = [], []
        n = len(labels)
        for i in range(n):
            for j in range(i + 1, n):
                if mask_same is not None and mask_same[i, j]:
                    continue
                (wi if labels[i] == labels[j] else bt).append(Sim[i, j])
        return float(np.mean(wi) - np.mean(bt))

    for seal in ["تعملون", "يعلمون", "اليم"]:
        idxs = np.where(finals == seal)[0]
        nz = nuzr[idxs]
        km = KMeans(n_clusters=3, n_init=10, random_state=71).fit(nz.reshape(-1, 1))
        lab = km.labels_
        order = np.argsort(km.cluster_centers_.ravel()); remap = {order[k]: k for k in range(3)}
        lab = np.array([remap[l] for l in lab])
        print("=" * 78)
        print(f"SEAL '{seal}' — {len(idxs)} āyahs | waves (nuzūl span, n):",
              [(int(nz[lab == k].min()), int(nz[lab == k].max()), int((lab == k).sum())) for k in range(3)])
        docs = [" ".join(r for r in roots[i] if r not in GEN | EXCL[seal]) for i in idxs]
        X = normalize(TfidfVectorizer(analyzer=str.split, min_df=1).fit_transform(docs))
        Sim = (X @ X.T).toarray()
        for k in range(3):
            ink = Counter(r for i, l in zip(idxs, lab) if l == k for r in roots[i] if r not in GEN | EXCL[seal])
            outk = Counter(r for i, l in zip(idxs, lab) if l != k for r in roots[i] if r not in GEN | EXCL[seal])
            Ni, No = sum(ink.values()) + 1, sum(outk.values()) + 1
            scor = {r: (ink[r] / Ni) / ((outk[r] + 0.5) / No) for r in ink if ink[r] >= 3}
            top = sorted(scor.items(), key=lambda x: -x[1])[:7]
            exi = [f"{sur[i]}:{ayn[i]}" for i, l in zip(idxs, lab) if l == k][:4]
            print(f"  wave{k+1}: n={(lab==k).sum():3d}  roots:", " ".join(f"{r}({ink[r]})" for r, _ in top), "| e.g.", exi)
        obs = sep_stat(Sim, lab)
        null = np.array([sep_stat(Sim, rng.permutation(lab)) for _ in range(2000)])
        z = (obs - null.mean()) / (null.std() + 1e-12)
        kc = KMeans(n_clusters=3, n_init=10, random_state=7).fit(X.toarray()).labels_
        zpc = (sep_stat(Sim, kc) - null.mean()) / (null.std() + 1e-12)
        print(f"  naive separation: d={obs:+.4f} z={z:+.2f} p={np.mean(null>=obs):.4f} | GATE planted-content z≈{zpc:+.1f}")
        # decisive control: cross-sūra pairs only + sūra-level permutation
        ss = sur[idxs]; same = ss[:, None] == ss[None, :]
        obs_c = sep_stat(Sim, lab, same)
        usuras = np.unique(ss); sura_lab = {u: lab[ss == u][0] for u in usuras}
        null_c = []
        for _ in range(2000):
            perm = rng.permutation([sura_lab[u] for u in usuras])
            pl = {u: p for u, p in zip(usuras, perm)}
            labp = np.array([pl[u] for u in ss])
            null_c.append(sep_stat(Sim, labp, same))
        null_c = np.array(null_c)
        zc = (obs_c - null_c.mean()) / (null_c.std() + 1e-12)
        print(f"  CONTROLLED (cross-sūra, sūra-perm): d={obs_c:+.4f} z={zc:+.2f} p={np.mean(null_c>=obs_c):.4f}")


if __name__ == "__main__":
    main()
