# -*- coding: utf-8 -*-
"""
ILTIFAT (7th modality) — morpho-syntactic person/number/tense shift detector.

Hypothesis (al-Zarkashi / al-Suyuti): the Qur'an deploys rule-governed shifts of
grammatical PERSON / NUMBER / TENSE between adjacent text-units at a higher rate /
distinctive pattern than ordinary Arabic, poetry, and saj'.

Pipeline (telescope rule + G10):
  GATE  : planted-shift synthetic fires; constant=null; shuffle=baseline; monotone ladder.
  RUN   : same tagger on Qur'an + ordinary Arabic + poetry + saj', two unitizations.
  CONTROL: quoted-speech (qaala-root) boundaries excluded; within-text shuffle null.
"""
import re, sys, time, glob
import numpy as np
sys.path.insert(0, "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
sys.path.insert(0, "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/sequence_tests")
import analysis as A
from analysis import COL_DIACRITIZED as DCOL
import iltifat_tagger as T

ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(40)
t0 = time.time()

# qaala-root (quotative) detector — marks reported-speech frames to control out
_QUOT = re.compile(r"^(و|ف|ل)?(قال|قالوا|قالت|قل|قلنا|قلتم|يقول|تقول|نقول|اقول|قيل|قائل|قول|قولوا|نادى|ينادي|ناد)")
def is_quot_unit(unit_words):
    return any(_QUOT.match(w) for w in unit_words)

# ---------------- metrics on a unit-tag sequence ----------------
def shift_rate(tags):
    """tags: list of person ints (1/2/3); fraction of adjacent pairs that differ."""
    t = [x for x in tags if x]            # drop untagged
    if len(t) < 2:
        return None
    d = sum(1 for i in range(len(t) - 1) if t[i] != t[i + 1])
    return d / (len(t) - 1)

def shuffle_z(tags, R=300):
    t = [x for x in tags if x]
    if len(t) < 4 or len(set(t)) < 2:
        return None
    real = shift_rate(t)
    nul = np.empty(R)
    arr = np.array(t)
    for r in range(R):
        p = rng.permutation(arr)
        nul[r] = sum(1 for i in range(len(p) - 1) if p[i] != p[i + 1]) / (len(p) - 1)
    sd = nul.std()
    if sd < 1e-9:
        return 0.0
    return (real - nul.mean()) / sd      # +z = MORE alternation than chance order

def shift_rate_quotctrl(tags, quot_flags):
    """shift rate excluding boundaries where either side is a quotative-framed unit."""
    pairs = []
    seq = [(t, q) for t, q in zip(tags, quot_flags) if t]
    for i in range(len(seq) - 1):
        (t0_, q0), (t1_, q1) = seq[i], seq[i + 1]
        if q0 or q1:
            continue
        pairs.append(t0_ != t1_)
    if len(pairs) < 2:
        return None
    return sum(pairs) / len(pairs)

# ---------------- unitization ----------------
SENT = re.compile(r"[.!?؟؛\n]+")
CLAUSE = re.compile(r"[.،؛:!؟]+")

def units_from_lines(path, splitter, minw=2):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    out = []
    for chunk in splitter.split(txt):
        w = T.words(chunk)
        if len(w) >= minw:
            out.append(w)
    return out

def fixed_chunks(all_words, k=8):
    return [all_words[i:i + k] for i in range(0, len(all_words) - k + 1, k)]

# ---------------- tag a list of units ----------------
def tag_units(units):
    tags = [T.tag_person(u)[0] for u in units]
    quot = [is_quot_unit(u) for u in units]
    return tags, quot

# ---------------- windowed cross-corpus ----------------
def windows_shift(tags, U=40, step=20, maxw=200):
    """fixed-N (U tagged units) windows -> per-window shift_rate + shuffle_z."""
    tt = [x for x in tags if x]
    srs, zs = [], []
    for c in range(0, max(1, len(tt) - U + 1), step):
        seg = tt[c:c + U]
        if len(seg) < U * 0.8:
            break
        sr = shift_rate(seg)
        z = shuffle_z(seg, R=120)
        if sr is not None: srs.append(sr)
        if z is not None: zs.append(z)
        if len(srs) >= maxw:
            break
    return np.array(srs), np.array(zs)

def g(a, b):
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    return (a.mean() - b.mean()) / (np.sqrt((a.var() + b.var()) / 2) + 1e-9)

def boot_p(a, b, R=2000):
    """P(random a-window shift > random b-window shift)."""
    if len(a) == 0 or len(b) == 0:
        return float("nan")
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5 * np.mean(a[ai] == b[bi]))


# ======================================================================
#  GATE
# ======================================================================
def gate():
    print(f"[{time.time()-t0:.1f}s] ===== GATE (telescope rule + monotone ladder) =====")
    alt = [(1 + (i % 2)) for i in range(60)]          # 1,2,1,2,... strong iltifat
    alt3 = [(1 + (i % 3)) for i in range(60)]         # 1,2,3,1,2,3 cycle
    block = [1]*20 + [2]*20 + [3]*20                  # clustered narration
    const = [3]*60                                    # no shift
    randt = list(rng.integers(1, 4, 60))             # random
    for name, tg in [("alternating12", alt), ("cycle123", alt3),
                     ("blocked", block), ("constant", const), ("random", randt)]:
        sr = shift_rate(tg); z = shuffle_z(tg)
        srs = f"{sr:.3f}" if sr is not None else "  -  "
        zs = f"{z:+.2f}" if z is not None else "  -  "
        print(f"   {name:14s}  shift_rate={srs}   shuffle_z={zs}")
    # degradation ladder: start from a realistically-clustered tag stream, progressively scramble
    base = ([1]*4 + [2]*4 + [3]*4) * 8
    print("   --- degradation ladder (block stream, increasing scramble) ---")
    for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
        a = np.array(base).copy()
        idx = rng.choice(len(a), int(frac * len(a)), replace=False)
        a[idx] = rng.permutation(a[idx])
        print(f"     scramble={frac:.2f}  shift_rate={shift_rate(list(a)):.3f}  shuffle_z={shuffle_z(list(a)):+.2f}")


# ======================================================================
#  LOAD CORPORA
# ======================================================================
def load_quran_units():
    c = A.load_corpus(ROOT + "/Book6.xlsx")
    units = [T.words(c.df.iloc[i][DCOL]) for i in range(len(c.df))]
    allw = [w for u in units for w in u]
    return units, allw

def main():
    gate()
    print(f"\n[{time.time()-t0:.1f}s] ===== loading corpora =====")
    corpora = {}          # name -> (units_natural, all_words)
    qu, qallw = load_quran_units()
    corpora["QURAN"] = (qu, qallw)

    prose_files = ["ar_tabari", "ar_classical2", "ar_novel", "ar_news"]
    pu = []
    for f in prose_files:
        pu += units_from_lines(ROOT + f"/sequence_tests/corpus/{f}.txt", SENT)
    corpora["ord-Arabic"] = (pu, [w for u in pu for w in u])

    poet = units_from_lines(ROOT + "/sequence_tests/corpus/ar_poetry.txt", re.compile(r"\n+"))
    corpora["poetry(Mutanabbi)"] = (poet, [w for u in poet for w in u])

    saj = []
    for f in ("ar_sajprose", "ar_saj_hariri"):
        saj += units_from_lines(ROOT + f"/sequence_tests/corpus/{f}.txt", CLAUSE)
    corpora["saj'(Hamadhani+Hariri)"] = (saj, [w for u in saj for w in u])

    # ---------- summary table per corpus (natural units) ----------
    print(f"\n[{time.time()-t0:.1f}s] ===== NATURAL UNITS (ayah / sentence / line / saj-clause) =====")
    print(f"   {'corpus':24s} {'units':>6s} {'tag%':>5s} {'shift':>6s} {'shiftQC':>7s} {'shZ':>6s}")
    natdist = {}
    for nm, (units, allw) in corpora.items():
        tags, quot = tag_units(units)
        ntag = sum(1 for x in tags if x)
        sr = shift_rate(tags)
        qc = shift_rate_quotctrl(tags, quot)
        z = shuffle_z(tags, R=400)
        srs, zs = windows_shift(tags, U=40, step=20)
        natdist[nm] = (srs, zs)
        print(f"   {nm:24s} {len(units):6d} {100*ntag/max(len(units),1):4.0f}% "
              f"{sr:6.3f} {(qc if qc else float('nan')):7.3f} {(z if z is not None else float('nan')):+6.2f}")

    # ---------- fixed 8-word chunks (G10 tokenization #2) ----------
    print(f"\n[{time.time()-t0:.1f}s] ===== FIXED 8-WORD CHUNK UNITS (G10 tokenization #2) =====")
    print(f"   {'corpus':24s} {'chunks':>6s} {'shift':>6s} {'shZ':>6s}")
    fixdist = {}
    for nm, (units, allw) in corpora.items():
        ch = fixed_chunks(allw, 8)
        tags = [T.tag_person(u)[0] for u in ch]
        sr = shift_rate(tags); z = shuffle_z(tags, R=400)
        srs, zs = windows_shift(tags, U=40, step=20)
        fixdist[nm] = (srs, zs)
        print(f"   {nm:24s} {len(ch):6d} {sr:6.3f} {(z if z is not None else float('nan')):+6.2f}")

    # ---------- cross-corpus sd-gaps vs ordinary Arabic ----------
    print(f"\n[{time.time()-t0:.1f}s] ===== Qur'an vs baselines (fixed-N=40-unit windows) =====")
    for label, dist in [("NATURAL", natdist), ("FIXED8", fixdist)]:
        qsr, qz = dist["QURAN"]
        print(f"  [{label}]  Qur'an shift windows: n={len(qsr)} mean={qsr.mean():.3f}  shuffle_z windows: mean={qz.mean():+.2f}")
        for nm in ("ord-Arabic", "poetry(Mutanabbi)", "saj'(Hamadhani+Hariri)"):
            bsr, bz = dist[nm]
            print(f"     vs {nm:24s}  shift Δ={g(qsr,bsr):+5.2f}sd  P(Q>base)={boot_p(qsr,bsr):.2f}   shZ Δ={g(qz,bz):+5.2f}sd")
    print(f"\n[total {time.time()-t0:.1f}s]")


if __name__ == "__main__":
    main()
