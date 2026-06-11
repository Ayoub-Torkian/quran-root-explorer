"""MODALITY 50 / Lens 15 — MUQATTA'AT / RASM POINTER (divinely-rooted: consonantal skeleton only).

Per the divine-rootedness control (DESIGN_STANCE.md), this studies the REVEALED text: the disjoint
opening letters (al-muqaṭṭaʿāt), the rasm, and the canonical sūra order — NO ḥarakāt. Three gate-validated
structural tests on the 29 muqaṭṭaʿāt sūras (permutation nulls):

  A) BEARER ENRICHMENT — do a sūra's opening letters appear at an elevated rate in its OWN rasm body?
     null = random same-size letter sets per sūra.  RESULT: 1.064x, z=+2.17, p=0.024 (modest aggregate;
     concentrated in single-letter sūras: ق/S50=1.73x, ص/S38=1.46x, ن/S68=1.24x — the classic 'ق lead').
  B) HALF-ALPHABET — distinct letters across all muqaṭṭaʿāt = 14 of 28 (نصف الحروف). CONFIRMED.
  C) MUSHAF CONTIGUITY — are the 29 sūras clustered in canonical order beyond chance?
     null = random 29-subsets of 1..114.  RESULT: 19 adjacent pairs vs null 7.1, p<0.0001 (strong;
     reproduces the position-pointer headline, cf. app Disjoint-Letters p≈2e-5).
  GATE: positive control (most over-represented letter per sūra) fires at 1.49x; negative (random) 1.01x.

These are INTERNAL structural properties of the revealed text (sui generis — there is no 'ordinary-Arabic
muqaṭṭaʿāt' baseline), validated against permutation nulls. A second positive structural result alongside
#42 recurrence, and exactly the divinely-rooted kind of target.

RUN DISCIPLINE: author/run in /tmp via heredoc (mount read lags); this host copy is for the user.
"""
import re, os, sys
import numpy as np
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_DIACRITIZED as D, COL_SURAH as S
rng = np.random.default_rng(50)
HARAKAT = re.compile(r"[ً-ْٰـٕ-ٟ]")
def rasm(t):
    t = HARAKAT.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    t = re.sub("ة", "ه", t).replace("ؤ", "و")
    return "".join(re.findall(r"[ء-ي]", t))

MUQ_RAW = {2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",14:"الر",15:"الر",19:"كهيعص",
 20:"طه",26:"طسم",27:"طس",28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",38:"ص",40:"حم",
 41:"حم",42:"حمعسق",43:"حم",44:"حم",45:"حم",46:"حم",50:"ق",68:"ن"}

def main():
    MUQ = {k: set(rasm(v)) for k, v in MUQ_RAW.items()}
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    bodies = {}
    for su in np.unique(sur):
        idx = np.where(sur == su)[0]
        if su in MUQ: idx = idx[1:]               # drop the opening-letters ayah
        bodies[su] = "".join(rasm(df.iloc[i][D]) for i in idx)
    corpus = "".join(bodies.values()); cf = Counter(corpus); Ctot = len(corpus)
    rate = lambda t, L: (sum(Counter(t)[l] for l in L) / len(t)) if t else 0.0
    corp_rate = lambda L: sum(cf[l] for l in L) / Ctot
    enrich = lambda asg: np.mean([rate(bodies[su], L) / corp_rate(L) for su, L in asg.items() if corp_rate(L) > 0])

    allmuq = set().union(*MUQ.values())
    print(f"B) distinct muqaṭṭaʿāt letters = {len(allmuq)}/28 -> {'HALF-ALPHABET confirmed' if len(allmuq)==14 else 'NOT 14'}: {''.join(sorted(allmuq))}")

    ALPH = sorted(set(corpus)); obs = enrich(MUQ)
    null = np.array([enrich({su: set(rng.choice(ALPH, len(L), replace=False)) for su, L in MUQ.items()}) for _ in range(2000)])
    print(f"A) bearer enrichment = {obs:.3f}x | null {null.mean():.3f} | z={(obs-null.mean())/(null.std()+1e-9):+.2f} p={np.mean(null>=obs):.4f}")
    hi = sorted(((su, rate(bodies[su], L) / corp_rate(L)) for su, L in MUQ.items()), key=lambda x: -x[1])[:5]
    print("   top bearers:", ", ".join(f"S{su}={r:.2f}x" for su, r in hi))

    cont = lambda pos: int(np.sum(np.diff(sorted(pos)) == 1))
    obsc = cont(list(MUQ)); nullc = np.array([cont(rng.choice(np.arange(1, 115), 29, replace=False)) for _ in range(5000)])
    print(f"C) mushaf contiguity = {obsc} adjacent pairs | null {nullc.mean():.2f} | p={np.mean(nullc>=obsc):.4f}")

    planted = {su: {max(ALPH, key=lambda l: rate(bodies[su], {l}) / corp_rate({l}) if corp_rate({l}) > 0 else 0)}
               for su in MUQ if bodies[su]}
    print(f"GATE: positive control {enrich(planted):.3f}x (>>1) ; negative/random ~{null.mean():.3f}x (~1.0)")

if __name__ == "__main__":
    main()
