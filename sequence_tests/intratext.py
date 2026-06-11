# -*- coding: utf-8 -*-
"""
INTRATEXTUAL NARRATIVE RECURRENCE (9th modality).
Tests the Qur'an's signature of RETELLING the same stories across DISTANT passages
with variation. Signature = a heavy upper tail of LONG-RANGE passage similarity
(a few far-apart passages spike) ABOVE the far-pair median — distinguishing genuine
recurrence from mere topical homogeneity (uniformly high similarity).

Fairness: EQUAL passage count P per corpus via bootstrap subsampling (controls the
77k-vs-3k size asymmetry & multiple-comparison inflation). Content-word cosine.
Gate-first: plant near-duplicate distant passages -> detector fires.
"""
import re, sys, time
import numpy as np
from collections import Counter
sys.path.insert(0, "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
sys.path.insert(0, "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/sequence_tests")
import analysis as A
from analysis import COL_DIACRITIZED as D
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(42); t0 = time.time()
_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t)
    t = re.sub(r"[ةھ]", "ه", t); return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()
# FIX (firming #43): normalize (strip harakat) FIRST, THEN tokenize. The old order
# [nl(x) for x in WA.findall(text)] shattered the DIACRITIZED Qur'an at every harakat
# into sub-word fragments (37.7k) while plain comparators stayed whole — an asymmetric
# tokenization confound. tok_text() yields real words (77.7k, the intended apples count).
def tok_text(s):
    return [w for w in WA.findall(nl(s)) if len(w) > 1]
# Arabic function words to drop (so similarity rides on CONTENT); normalized to match tokens
STOP = {nl(w) for w in ("في من الى على عن مع و ف ب ك ل ال هذا هذه ذلك التي الذي الذين ما لا ان انه اذا قد كان"
           " هو هي هم انت انا نحن كل بعض غير عند او ثم حتى يا اي بين لم لن لو ولا فلا وما وان به له لهم"
           " هنا هناك كما لقد وقد منه منها فيها فيه عليه عليها اليه اليها").split()}
def content_words(toklist):
    return [w for w in toklist if w not in STOP and len(w) > 1]

def passages(words, K=50):
    cw = content_words(words)
    return [cw[i:i + K] for i in range(0, len(cw) - K + 1, K)]

def tf_cosine_matrix(passlist):
    vocab = {}
    for p in passlist:
        for w in p: vocab.setdefault(w, len(vocab))
    V = np.zeros((len(passlist), len(vocab)))
    for i, p in enumerate(passlist):
        for w, ct in Counter(p).items(): V[i, vocab[w]] = ct
    # tf-idf-ish: idf weighting
    df = (V > 0).sum(0); idf = np.log((len(passlist) + 1) / (df + 1)) + 1
    V = V * idf
    nrm = np.linalg.norm(V, axis=1, keepdims=True); nrm[nrm == 0] = 1
    Vn = V / nrm
    return Vn @ Vn.T

def _excess_one(passlist, gapfrac=0.25, topq=0.95):
    P = len(passlist)
    Cm = tf_cosine_matrix(passlist)
    gap = max(1, int(P * gapfrac))
    far = np.array([Cm[i, j] for i in range(P) for j in range(i + gap, P)])
    if len(far) < 10: return None
    return np.quantile(far, topq) - np.median(far)

def recurrence_excess(passlist, P=40, gapfrac=0.25, topq=0.95, B=40):
    """equal-P bootstrap: mean over B subsamples of
       (top-quantile far-pair cosine) - (median far-pair cosine)."""
    if len(passlist) < P:
        return None
    vals = []
    for _ in range(B):
        idx = np.sort(rng.choice(len(passlist), P, replace=False))
        e = _excess_one([passlist[i] for i in idx], gapfrac, topq)
        if e is not None: vals.append(e)
    return np.array(vals)

def word_shuffle_passages(words, K=50):
    """destroy passage-level recurrence/coherence, PRESERVE unigram frequency."""
    cw = content_words(words)
    sh = list(cw); rng.shuffle(sh)
    return [sh[i:i + K] for i in range(0, len(sh) - K + 1, K)]

def g(a, b):
    if a is None or b is None or len(a) < 2 or len(b) < 2: return float("nan")
    return (a.mean() - b.mean()) / (np.sqrt((a.var() + b.var()) / 2) + 1e-9)
def boot_p(a, b, R=2000):
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5 * np.mean(a[ai] == b[bi]))

def fileW(p):
    return tok_text(open(p, encoding="utf-8", errors="ignore").read())

# ---------- load ----------
c = A.load_corpus(ROOT + "/Book6.xlsx")
qw = [w for i in range(len(c.df)) for w in tok_text(str(c.df.iloc[i][D]))]
ordw = []
for f in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"):
    ordw += fileW(ROOT + f"/sequence_tests/corpus/{f}.txt")
poet = fileW(ROOT + "/sequence_tests/corpus/ar_poetry.txt")
saj = fileW(ROOT + "/sequence_tests/corpus/ar_sajprose.txt") + fileW(ROOT + "/sequence_tests/corpus/ar_saj_hariri.txt")
corp = {"QURAN": qw, "ord-Arabic": ordw, "poetry(Mutanabbi)": poet, "saj'(Ham+Har)": saj}
for nm, w in corp.items():
    print(f"   {nm:20s} content-words={len(content_words(w)):6d}  passages(K=50)={len(passages(w))}")

# ---------- GATE (direct, on exactly-P synthetic sets; no subsample dilution) ----------
print(f"\n[{time.time()-t0:.1f}s] ===== GATE (recurrence detector) =====")
P0 = 40
distinct = passages(ordw)[:P0]                    # 40 distinct ordinary passages
twin = distinct[5]
def plant(n):
    pl = [list(p) for p in distinct]
    for pos in list(range(8, 8 + 8 * n, 8))[:n]:  # distant copies of one passage
        if pos < P0: pl[pos] = list(twin)
    return pl
print(f"   distinct (no recurrence)          excess = {_excess_one(distinct):.3f}")
print("   --- ladder: # planted distant twins ---")
for n in (0, 1, 2, 4, 6):
    print(f"     planted twins={n}  excess = {_excess_one(plant(n)):.3f}")
# null: word-shuffled distinct (should be ~ distinct, low)
print(f"   word-shuffled ordinary            excess = {_excess_one(word_shuffle_passages(ordw)[:P0]):.3f}  (expect low)")

# ---------- cross-corpus (equal P) + WORD-SHUFFLE control ----------
Pcommon = min(len(passages(w)) for w in corp.values())
Puse = max(20, min(40, Pcommon))
print(f"\n[{time.time()-t0:.1f}s] ===== recurrence excess, EQUAL P={Puse} (bootstrap) + word-shuffle control =====")
print(f"   {'corpus':20s} {'real':>6s} {'wshuf':>6s} {'real-shuf':>9s} | vs-ord on (real-shuf)")
rows = {}
for nm, w in corp.items():
    real = recurrence_excess(passages(w), P=Puse, B=80)
    shuf = recurrence_excess(word_shuffle_passages(w), P=Puse, B=80)
    net = real.mean() - shuf.mean()
    rows[nm] = (real, shuf, net)
basenet_dist = rows["ord-Arabic"][0] - rows["ord-Arabic"][1]
for nm in corp:
    real, shuf, net = rows[nm]
    netdist = real - shuf
    extra = "" if nm == "ord-Arabic" else f"  d={g(netdist, basenet_dist):+5.2f}sd  P={boot_p(netdist, basenet_dist):.2f}"
    print(f"   {nm:20s} {real.mean():6.3f} {shuf.mean():6.3f} {net:+9.3f} |{extra}")
print("   (real-shuf = recurrence BEYOND unigram repetitiveness; if Quran collapses to ~ord here,")
print("    the raw excess was just the #28 repetition signal re-expressed at passage scale.)")
print(f"\n[total {time.time()-t0:.1f}s]")
# (firming #43: tokenization fixed to normalize-then-split; see intratext_lock_fixed.py)
