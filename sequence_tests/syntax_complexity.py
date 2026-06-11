# -*- coding: utf-8 -*-
"""
MODALITY 11 — SHALLOW SYNTACTIC COMPLEXITY (parataxis vs hypotaxis).

Attacks the dependency-syntax region (~0% coverage) WITHOUT a parser, using surface
function-word cues that are identifiable from raw normalized text and applied
IDENTICALLY to every corpus (so tagger noise is symmetric and cancels in contrasts).

Stylometric axes (per fixed-N window, equal-N across corpora):
  HYPOTAXIS / embedding : subordinator density = (relatives الذي/التي + complementizers
                          + conditional/temporal subordinators) per 100 words.
  RELATIVE-clause density: الذي/التي/الذين ... per 100 words (a clean embedding marker).
  PARATAXIS proxy       : coordinating-waw rate = fraction of words beginning و- (noisy
                          but symmetric), plus standalone coordinators ثم/او/ام/بل/لكن.
  CLAUSE LENGTH         : mean words between pause/clause delimiters.
Hypothesis: is the Qur'an's clausal architecture (embedding depth, parataxis) distinctive
vs ordinary prose / poetry / saj'? GATE: inject subordinators -> density rises monotonically.
"""
import re, sys, time
import numpy as np
from collections import Counter
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
sys.path.insert(0, ROOT); sys.path.insert(0, ROOT + "/sequence_tests")
import analysis as A
from analysis import COL_DIACRITIZED as D
rng = np.random.default_rng(42); t0 = time.time()

_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t)
    t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()
def words(s): return [w for w in WA.findall(nl(s)) if w]

REL   = {nl(w) for w in "الذي التي الذين اللذان اللتان اللذين اللتين اللاتي اللواتي اللائي".split()}
SUBORD= REL | {nl(w) for w in "اذا لو لولا لما كلما حتي كي لكي حيث حين لان كان لعل ليت اذ ريثما عندما بينما".split()}
COORD = {nl(w) for w in "ثم او ام بل لكن".split()}
WAW = nl("و"); FA = nl("ف")

def feats(toklist):
    n = len(toklist)
    if n < 5: return None
    rel = sum(w in REL for w in toklist)
    sub = sum(w in SUBORD for w in toklist)
    crd = sum(w in COORD for w in toklist)
    waw = sum(w.startswith(WAW) for w in toklist)
    return dict(rel=100*rel/n, sub=100*sub/n, crd=100*crd/n, waw=100*waw/n)

def window_stat(units, W, B, key):
    """units = list of (toklist) per pause-unit; window = W units concatenated."""
    if len(units) < W: return None
    vals = []
    for _ in range(B):
        s = rng.integers(0, len(units)-W+1)
        toks = [w for u in units[s:s+W] for w in u]
        f = feats(toks)
        if f is not None: vals.append(f[key])
    return np.array(vals) if vals else None

def clause_len(units, W, B):
    if len(units) < W: return None
    vals = []
    for _ in range(B):
        s = rng.integers(0, len(units)-W+1)
        ln = [len(u) for u in units[s:s+W] if len(u) >= 1]
        if ln: vals.append(np.mean(ln))
    return np.array(vals) if vals else None

def g(a, b):
    if a is None or b is None or len(a) < 2 or len(b) < 2: return float("nan")
    return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
def boot_p(a, b, R=2000):
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5*np.mean(a[ai] == b[bi]))

# ---------- load as pause-units (uniform) ----------
c = A.load_corpus(ROOT + "/Book6.xlsx")
q_units = [words(str(c.df.iloc[i][D])) for i in range(len(c.df))]
q_units = [u for u in q_units if len(u) >= 2]
SPLIT = re.compile(r"[.!؟?\n،؛:]+")
def file_units(paths):
    txt = ""
    for p in paths: txt += "\n" + open(p, encoding="utf-8", errors="ignore").read()
    return [u for u in (words(x) for x in SPLIT.split(txt)) if len(u) >= 2]
CP = ROOT + "/sequence_tests/corpus/"
ord_units = file_units([CP+f+".txt" for f in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2")])
poet_units = file_units([CP+"ar_poetry.txt"])
saj_units = file_units([CP+"ar_sajprose.txt", CP+"ar_saj_hariri.txt"])
corp = {"QURAN": q_units, "ord-Arabic": ord_units, "poetry": poet_units, "saj'": saj_units}
print(f"[{time.time()-t0:.1f}s] pause-units:", {k: len(v) for k, v in corp.items()})
for k, v in corp.items():
    allt = [w for u in v for w in u]; f = feats(allt)
    print(f"   {k:12s} words={len(allt):6d}  rel/100={f['rel']:.2f} subord/100={f['sub']:.2f} "
          f"coord/100={f['crd']:.2f} waw-init%={f['waw']:.1f} mean-clause={np.mean([len(u) for u in v]):.1f}")

# ---------- GATE: inject subordinators, density must rise monotonically ----------
print(f"\n[{time.time()-t0:.1f}s] ===== GATE (recover injected subordination) =====")
base = [w for u in ord_units[:200] for w in u]; rel_word = nl("الذي")
for rate in (0.0, 0.05, 0.10, 0.20):
    seq = list(base)
    for k in rng.choice(len(seq), int(len(seq)*rate), replace=False): seq[k] = rel_word
    print(f"   injected rel-rate={rate:.2f} -> measured rel/100 = {feats(seq)['rel']:.2f} (expect ~{rate*100:.0f})")

# ---------- cross-corpus, equal-N ----------
W = max(15, min(40, min(len(v) for v in corp.values()) // 2)); B = 400
print(f"\n[{time.time()-t0:.1f}s] ===== cross-corpus syntactic profile, equal-N W={W} units =====")
print(f"   {'corpus':12s} {'subord':>18s} {'relative':>18s} {'coord':>18s} {'waw':>18s} {'clauseLen':>18s}")
def row(nm):
    out = {}
    for key in ("sub", "rel", "crd", "waw"):
        out[key] = window_stat(corp[nm], W, B, key)
    out["cl"] = clause_len(corp[nm], W, B)
    return out
R = {nm: row(nm) for nm in corp}
def cell(nm, key):
    a = R[nm][key]; b = R["ord-Arabic"][key]
    if nm == "ord-Arabic": return f"{a.mean():6.2f}"
    return f"{a.mean():6.2f} d={g(a,b):+5.2f}sd"
for nm in corp:
    print(f"   {nm:12s} {cell(nm,'sub'):>18s} {cell(nm,'rel'):>18s} {cell(nm,'crd'):>18s} "
          f"{cell(nm,'waw'):>18s} {cell(nm,'cl'):>18s}")
print(f"\n   P(Q>ord): subord {boot_p(R['QURAN']['sub'],R['ord-Arabic']['sub']):.2f} | "
      f"relative {boot_p(R['QURAN']['rel'],R['ord-Arabic']['rel']):.2f} | "
      f"coord {boot_p(R['QURAN']['crd'],R['ord-Arabic']['crd']):.2f} | "
      f"waw {boot_p(R['QURAN']['waw'],R['ord-Arabic']['waw']):.2f} | "
      f"clauseLen {boot_p(R['QURAN']['cl'],R['ord-Arabic']['cl']):.2f}")
print(f"\n[total {time.time()-t0:.1f}s]")
