"""MODALITY 48 — DIRECTIONAL sub-unit lens (genuine, non-trivial) + root-grain positional profile.

Closes the user-mandated items from IDEA_SIGNALS_GEOMETRY.md §8 (the earlier posdir directionality demo
was trivially antisymmetric). RESULT: no new distinctive.

PART A (cross-corpus, equal-N, shuffle null) — TIME-IRREVERSIBILITY of the within-unit sub-unit-length
  series: signed skew of lag-1 increments. Reversing flips its SIGN, shuffling destroys it -> a real
  directional statistic. FINDING: all corpora mildly negative (sharp-rise/gradual-fall); poetry z=-2.06,
  saj' -1.80 show it most; the QUR'AN is the LEAST directional (-0.054, z=-1.23). NOT distinctive, sub-2sd.

PART B (Qur'an-internal, shuffle null) — corr(within-ayah position, root RARITY). FINDING: +0.072,
  z=+13.4 — rarer roots sit toward the ayah END (fasila). Strong & significant, BUT Qur'an-internal only
  (comparators lack root annotation) and CONFOUNDED: generic Arabic puts function words (common) first and
  content words (rarer) later, and the end is the rhyme position (Lens 3). So it is a real internal
  gradient, NOT a distinctiveness claim. To promote: a root/morph-annotated comparator + rhyme-residual.

RUN DISCIPLINE: author/run in /tmp via heredoc (mount read lags); this host copy is for the user.
"""
import re, os, sys
import numpy as np
from scipy.stats import skew
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_DIACRITIZED as D, COL_ROOTS as R
rng = np.random.default_rng(48)
ARLET = re.compile(r'[ء-ي]'); nlet = lambda s: len(ARLET.findall(str(s)))
words = lambda u: [w for w in re.split(r'\s+', str(u)) if nlet(w) > 0]

def len_series(units, kmin=6):
    out = []
    for u in units:
        L = [nlet(w) for w in words(u)]
        if len(L) >= kmin: out.append(np.array(L, float))
    return out
def signed_skew(seqs):
    vals = [skew(np.diff(L)) for L in seqs if np.diff(L).std() > 0]
    return np.nanmean(vals) if vals else np.nan
def dir_z(seqs, B=150):
    obs = signed_skew(seqs)
    null = np.array([signed_skew([rng.permutation(L) for L in seqs]) for _ in range(B)])
    return obs, (obs - np.nanmean(null)) / (np.nanstd(null) + 1e-9)

def part_A():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx"))
    q = [str(c.df.iloc[i][D]) for i in range(len(c.df))]
    SENT = re.compile(r"[.!؟?\n،؛:]+")
    def comp(paths):
        txt = "".join("\n" + open(os.path.join(ROOT, 'sequence_tests', 'corpus', p), encoding='utf-8', errors='ignore').read() for p in paths)
        return [s for s in SENT.split(txt) if len(words(s)) >= 6]
    corp = {"QURAN": q, "ord-Arabic": comp(["ar_tabari.txt","ar_classical2.txt","ar_novel.txt","ar_news.txt"]),
            "poetry": comp(["ar_poetry.txt"]), "saj'": comp(["ar_sajprose.txt","ar_saj_hariri.txt"])}
    seqs = {k: len_series(v) for k, v in corp.items()}
    N = min(len(s) for s in seqs.values())
    print("PART A directional irreversibility | equal-N =", N)
    for name, s in seqs.items():
        if name == 'QURAN':
            ss, zz = [], []
            for _ in range(3):
                sub = [s[i] for i in rng.choice(len(s), N, replace=False)]; o, z = dir_z(sub); ss.append(o); zz.append(z)
            print(f"   {name:11s} signed-skew={np.median(ss):+.3f}  z={np.median(zz):+.2f}")
        else:
            sub = [s[i] for i in rng.choice(len(s), N, replace=False)]; o, z = dir_z(sub)
            print(f"   {name:11s} signed-skew={o:+.3f}  z={z:+.2f}")

def part_B():
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx"))
    rows = [[w for w in str(c.df.iloc[i][R]).split() if w and w != 'nan'] for i in range(len(c.df))]
    freq = Counter(w for row in rows for w in row); Vv = len(freq) + 1
    def slope(rs):
        cs = []
        for row in rs:
            if len(row) < 5: continue
            rar = np.array([-np.log(freq[w] / Vv) for w in row]); p = np.arange(len(row)) / (len(row) - 1)
            if rar.std() > 0: cs.append(np.corrcoef(p, rar)[0, 1])
        return np.nanmean(cs) if cs else np.nan
    obs = slope(rows)
    null = np.array([slope([list(rng.permutation(r)) for r in rows]) for _ in range(150)])
    print(f"PART B root-rarity vs position (Qur'an-internal): {obs:+.3f}  z={ (obs-null.mean())/(null.std()+1e-9):+.2f}")

if __name__ == "__main__":
    part_A(); part_B()
