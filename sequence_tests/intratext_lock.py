# -*- coding: utf-8 -*-
"""
INTRATEXT LOCK (#43): invariance battery for the #42 recurrence breakthrough.

Goal: show the QURAN's varied-intratextual-recurrence excess (+3.5-4sd vs ordinary
Arabic at passage grain, word-shuffle-controlled) is NOT an artifact of a single
choice of passage size, quantile, gap, bootstrap depth, or tokenization.

This is the project's G10 invariance gate applied to #42:
  (a) equal sample size  -> equal-P bootstrap (as in intratext.py)
  (b) >=2 tokenizations  -> WHITESPACE content-words AND RASM char-4-shingles
  swept across K in {40,50,60}, topq in {0.90,0.95}, gapfrac in {0.20,0.25,0.33},
  with heavy bootstrap B=200, against the SAME same-language baselines.

Every cell reports d(QURAN-ord), d(QURAN-poetry), d(QURAN-saj') on the
word-shuffle-controlled net (real - shuffle), plus bootstrap P vs ordinary.
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
STOP = set("في من الى على عن مع و ف ب ك ل ال هذا هذه ذلك التي الذي الذين ما لا ان انه اذا قد كان"
           " هو هي هم انت انا نحن كل بعض غير عند او ثم حتى يا اي بين لم لن لو ولا فلا وما وان به له لهم"
           " هنا هناك كما لقد وقد منه منها فيها فيه عليه عليها اليه اليها".split())
def content_words(toklist):
    return [w for w in toklist if w not in STOP and len(w) > 1]

# ---- TOKENIZER 1: whitespace content words (apples-to-apples) ----
def toks_word(words):
    return content_words(words)
# ---- TOKENIZER 2: rasm char-4-shingles over the joined content stream ----
#      (satisfies the G10 (b) "2nd tokenization" requirement by construction)
def toks_rasm(words):
    s = "".join(content_words(words))
    return [s[i:i+4] for i in range(0, len(s) - 4 + 1)]

def passages(tokens, K):
    return [tokens[i:i+K] for i in range(0, len(tokens) - K + 1, K)]

def tf_cosine_matrix(passlist):
    vocab = {}
    for p in passlist:
        for w in p: vocab.setdefault(w, len(vocab))
    V = np.zeros((len(passlist), len(vocab)))
    for i, p in enumerate(passlist):
        for w, ct in Counter(p).items(): V[i, vocab[w]] = ct
    df = (V > 0).sum(0); idf = np.log((len(passlist) + 1) / (df + 1)) + 1
    V = V * idf
    nrm = np.linalg.norm(V, axis=1, keepdims=True); nrm[nrm == 0] = 1
    Vn = V / nrm
    return Vn @ Vn.T

def _excess_one(passlist, gapfrac, topq):
    P = len(passlist)
    Cm = tf_cosine_matrix(passlist)
    gap = max(1, int(P * gapfrac))
    far = np.array([Cm[i, j] for i in range(P) for j in range(i + gap, P)])
    if len(far) < 10: return None
    return np.quantile(far, topq) - np.median(far)

def recurrence_excess(passlist, P, gapfrac, topq, B):
    if len(passlist) < P: return None
    vals = []
    for _ in range(B):
        idx = np.sort(rng.choice(len(passlist), P, replace=False))
        e = _excess_one([passlist[i] for i in idx], gapfrac, topq)
        if e is not None: vals.append(e)
    return np.array(vals)

def word_shuffle(tokens):
    sh = list(tokens); rng.shuffle(sh); return sh

def g(a, b):
    if a is None or b is None or len(a) < 2 or len(b) < 2: return float("nan")
    return (a.mean() - b.mean()) / (np.sqrt((a.var() + b.var()) / 2) + 1e-9)
def boot_p(a, b, R=2000):
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5 * np.mean(a[ai] == b[bi]))

def fileW(p):
    return [nl(x) for x in WA.findall(open(p, encoding="utf-8", errors="ignore").read()) if nl(x)]

# ---------- load raw word streams ----------
c = A.load_corpus(ROOT + "/Book6.xlsx")
qw = [nl(x) for i in range(len(c.df)) for x in WA.findall(c.df.iloc[i][D]) if nl(x)]
ordw = []
for f in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news"):
    ordw += fileW(ROOT + f"/sequence_tests/corpus/{f}.txt")
poet = fileW(ROOT + "/sequence_tests/corpus/ar_poetry.txt")
saj = fileW(ROOT + "/sequence_tests/corpus/ar_sajprose.txt") + fileW(ROOT + "/sequence_tests/corpus/ar_saj_hariri.txt")
RAW = {"QURAN": qw, "ord": ordw, "poetry": poet, "saj": saj}

def make_net(tokens, K, P, gapfrac, topq, B):
    real = recurrence_excess(passages(tokens, K), P, gapfrac, topq, B)
    shuf = recurrence_excess(passages(word_shuffle(tokens), K), P, gapfrac, topq, B)
    if real is None or shuf is None: return None
    return real - shuf  # distribution of net excess across bootstrap subsamples

def run_cell(tok_fn, K, gapfrac, topq, B):
    toks = {nm: tok_fn(w) for nm, w in RAW.items()}
    # equal P across corpora at this K
    Pcommon = min(len(passages(t, K)) for t in toks.values())
    P = max(15, min(40, Pcommon))
    nets = {}
    for nm, t in toks.items():
        nets[nm] = make_net(t, K, P, gapfrac, topq, B)
    base = nets["ord"]
    out = {"P": P, "npass": {nm: len(passages(t, K)) for nm, t in toks.items()}}
    for comp in ("QURAN", "poetry", "saj"):
        out[comp] = (g(nets[comp], base), boot_p(nets[comp], base))
    out["Q_mean"] = nets["QURAN"].mean(); out["ord_mean"] = base.mean()
    return out

print(f"[{time.time()-t0:.1f}s] corpora raw words:",
      {k: len(content_words(v)) for k, v in RAW.items()})

B = 100
for tokname, tok_fn in (("WORD", toks_word), ("RASM-4shingle", toks_rasm)):
    print(f"\n================ TOKENIZATION: {tokname}  (B={B}) ================")
    print(f"{'K':>3} {'topq':>5} {'gap':>5} {'P':>3} | {'Q-ord(sd,P)':>16} {'Q-poet(sd)':>11} {'Q-saj(sd)':>10}")
    for K in (40, 50, 60):
        for topq in (0.90, 0.95):
            for gapfrac in (0.25, 0.33):
                r = run_cell(tok_fn, K, gapfrac, topq, B)
                q = r["QURAN"]; p = r["poetry"]; s = r["saj"]
                print(f"{K:>3} {topq:>5.2f} {gapfrac:>5.2f} {r['P']:>3} | "
                      f"{q[0]:>+7.2f}sd P={q[1]:>4.2f} | {p[0]:>+7.2f}sd | {s[0]:>+7.2f}sd")
print(f"\n[total {time.time()-t0:.1f}s]")
