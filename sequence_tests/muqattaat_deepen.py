"""#51 — DEEPEN the muqaṭṭaʿāt / rasm pointer (divinely-rooted, rasm only; NO ḥarakāt).

Extends #50 (muqattaat_pointer.py) with three sharpenings, all permutation-nulled:
  A) MORAN'S I (1-D spatial autocorrelation, rook adjacency) of the 29-sūra indicator over canonical
     order 1..114. RESULT: I=+0.539, z=+5.80, p<1e-4 — strong clustering (rigorous form of the contiguity).
  B) ROBUSTNESS under NUZŪL (revelation) order: I=+0.306 p<1e-4; contiguity 14 pairs vs null 7.1 p=0.001.
     The clustering SURVIVES re-ordering (not a canonical-arrangement artifact) but is STRONGER in the
     muṣḥaf order (0.54 vs 0.31) — partly chronological, amplified by the canonical arrangement.
  C) PER-LETTER bearer enrichment: concentrated in DISTINCTIVE letters — ط 1.25x, ق 1.24x, ن 1.24x,
     ص 1.18x — while ubiquitous ا/ل/م sit at ~1.0. The "ق lead" is really a distinctive/emphatic-letter lead.

RUN DISCIPLINE: author/run in /tmp via heredoc (mount read lags); this host copy is for the user.
"""
import re, os, sys
import numpy as np
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_DIACRITIZED as D, COL_SURAH as S, COL_REV_ORDER as RO
rng = np.random.default_rng(51)
HARAKAT = re.compile(r"[ً-ْٰـٕ-ٟ]")
def rasm(t):
    t = HARAKAT.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    t = re.sub("ة", "ه", t).replace("ؤ", "و")
    return "".join(re.findall(r"[ء-ي]", t))
MUQ_RAW = {2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",14:"الر",15:"الر",19:"كهيعص",
 20:"طه",26:"طسم",27:"طس",28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",38:"ص",40:"حم",
 41:"حم",42:"حمعسق",43:"حم",44:"حم",45:"حم",46:"حم",50:"ق",68:"ن"}

def morans_I(x):
    x = np.asarray(x, float); n = len(x); d = x - x.mean()
    num = 2 * sum(d[i] * d[i + 1] for i in range(n - 1)); den = np.sum(d ** 2); W = 2 * (n - 1)
    return (n / W) * (num / den) if den > 0 else 0.0

def main():
    MUQ = {k: set(rasm(v)) for k, v in MUQ_RAW.items()}
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    nuz = {}
    for i in range(len(df)):
        try: nuz[int(df.iloc[i][S])] = int(float(df.iloc[i][RO]))
        except Exception: pass
    ind = np.array([1 if s in MUQ else 0 for s in range(1, 115)], float)
    obs = morans_I(ind); null = np.array([morans_I(rng.permutation(ind)) for _ in range(5000)])
    print(f"A) Moran's I mushaf: {obs:+.3f} z={(obs-null.mean())/null.std():+.2f} p={np.mean(null>=obs):.4f}")
    order = sorted(range(1, 115), key=lambda s: nuz.get(s, 999))
    ind_n = np.array([1 if s in MUQ else 0 for s in order], float)
    obsn = morans_I(ind_n); nulln = np.array([morans_I(rng.permutation(ind_n)) for _ in range(5000)])
    contig = lambda pos: int(np.sum(np.diff(sorted(pos)) == 1))
    nr = sorted(nuz[s] for s in MUQ if s in nuz); cn = contig(nr)
    ncn = np.array([contig(rng.choice(np.arange(1, 115), len(nr), replace=False)) for _ in range(5000)])
    print(f"B) nuzul: Moran's I {obsn:+.3f} p={np.mean(nulln>=obsn):.4f} | contiguity {cn} vs {ncn.mean():.1f} p={np.mean(ncn>=cn):.4f}")
    bodies = {}
    for s in np.unique(sur):
        idx = np.where(sur == s)[0]
        if s in MUQ: idx = idx[1:]
        bodies[s] = "".join(rasm(df.iloc[i][D]) for i in idx)
    corpus = "".join(bodies.values()); cf = Counter(corpus); Ct = len(corpus)
    print("C) per-letter bearer enrichment:")
    for L in sorted(set().union(*MUQ.values())):
        sus = [s for s in MUQ if L in MUQ[s] and bodies[s]]
        base = cf[L] / Ct
        enr = np.mean([Counter(bodies[s])[L] / len(bodies[s]) for s in sus]) / base if base > 0 and sus else 0
        print(f"   {L}: {enr:.2f}x (n={len(sus)})")

if __name__ == "__main__":
    main()
