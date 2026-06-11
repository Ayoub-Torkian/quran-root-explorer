# -*- coding: utf-8 -*-
"""
INTRATEXT LOCK (FIXED TOKENIZATION) — the real firming test for #42.

BUG FOUND: intratext.py tokenizes the DIACRITIZED Qur'an column by running the
word-regex BEFORE stripping harakat: [nl(x) for x in WA.findall(text)].  On the
vocalized Qur'an this SHATTERS words at every diacritic -> 37.7k sub-word
fragments ("ون","وا","الل"), while the plain-text comparators tokenize into real
words. That is an asymmetric tokenization confound under the #42 cross-corpus test.

FIX: normalize (strip diacritics) FIRST, then tokenize: WA.findall(nl(text)).
This yields 77.7k real words for the Qur'an (matching the handoff's stated
"apples-to-apples 77.7k"), with real anchors (موسي=128, فرعون=67, نوح=33).

This script re-runs the #42 recurrence-excess battery with the CORRECT
tokenization, equal-P bootstrap + word-shuffle control, swept over K and params,
to test whether the +3.5-4sd Qur'an recurrence breakthrough SURVIVES on real words.
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
           " هنا هناك كما لقد وقد منه منها فيها فيه عليه عليها اليه اليها"
           " علي الي ومن وما ولا لكم لهم انا اني".split())
# normalize STOP the same way tokens are normalized, so they actually match
STOP = {nl(w) for w in STOP}
def tok_text(s):  # FIXED: normalize FIRST, then split
    return [w for w in WA.findall(nl(s)) if len(w) > 1]
def content_words(toklist):
    return [w for w in toklist if w not in STOP and len(w) > 1]
def toks_word(words): return content_words(words)
def toks_rasm(words):
    s = "".join(content_words(words)); return [s[i:i+4] for i in range(0, len(s)-3)]

def passages(tokens, K): return [tokens[i:i+K] for i in range(0, len(tokens)-K+1, K)]
def tf_cosine_matrix(passlist):
    vocab = {}
    for p in passlist:
        for w in p: vocab.setdefault(w, len(vocab))
    V = np.zeros((len(passlist), len(vocab)))
    for i, p in enumerate(passlist):
        for w, ct in Counter(p).items(): V[i, vocab[w]] = ct
    df = (V > 0).sum(0); idf = np.log((len(passlist)+1)/(df+1))+1
    V = V*idf; nrm = np.linalg.norm(V, axis=1, keepdims=True); nrm[nrm == 0] = 1
    Vn = V/nrm; return Vn @ Vn.T
def _excess_one(passlist, gapfrac, topq):
    Pn = len(passlist); Cm = tf_cosine_matrix(passlist); gap = max(1, int(Pn*gapfrac))
    far = np.array([Cm[i, j] for i in range(Pn) for j in range(i+gap, Pn)])
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
    return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
def boot_p(a, b, R=2000):
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5*np.mean(a[ai] == b[bi]))

# ---- load with CORRECT tokenization ----
c = A.load_corpus(ROOT + "/Book6.xlsx")
qw = []
for i in range(len(c.df)): qw += tok_text(str(c.df.iloc[i][D]))
def fileW(p): return tok_text(open(p, encoding="utf-8", errors="ignore").read())
ordw = []
for f in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"):
    ordw += fileW(ROOT + f"/sequence_tests/corpus/{f}.txt")
poet = fileW(ROOT + "/sequence_tests/corpus/ar_poetry.txt")
saj = fileW(ROOT + "/sequence_tests/corpus/ar_sajprose.txt") + fileW(ROOT + "/sequence_tests/corpus/ar_saj_hariri.txt")
RAW = {"QURAN": qw, "ord": ordw, "poetry": poet, "saj": saj}
print(f"[{time.time()-t0:.1f}s] FIXED tokens (raw words):",
      {k: len(v) for k, v in RAW.items()})
print(f"           content-words:", {k: len(content_words(v)) for k, v in RAW.items()})

def make_net(tokens, K, P, gapfrac, topq, B):
    real = recurrence_excess(passages(tokens, K), P, gapfrac, topq, B)
    shuf = recurrence_excess(passages(word_shuffle(tokens), K), P, gapfrac, topq, B)
    if real is None or shuf is None: return None
    return real - shuf
def run_cell(tok_fn, K, gapfrac, topq, B):
    toks = {nm: tok_fn(w) for nm, w in RAW.items()}
    Pcommon = min(len(passages(t, K)) for t in toks.values())
    P = max(15, min(40, Pcommon))
    nets = {nm: make_net(t, K, P, gapfrac, topq, B) for nm, t in toks.items()}
    base = nets["ord"]
    out = {"P": P, "npass": {nm: len(passages(t, K)) for nm, t in toks.items()}}
    for comp in ("QURAN", "poetry", "saj"):
        out[comp] = (g(nets[comp], base), boot_p(nets[comp], base))
    return out

B = 100
for tokname, tok_fn in (("WORD", toks_word), ("RASM-4shingle", toks_rasm)):
    print(f"\n========= TOKENIZATION: {tokname} (B={B}, FIXED real-word base) =========")
    print(f"{'K':>3} {'topq':>5} {'gap':>5} {'P':>3} | {'Q-ord(sd,P)':>16} {'Q-poet':>8} {'Q-saj':>8}")
    for K in (40, 50, 60):
        for topq in (0.90, 0.95):
            for gapfrac in (0.25, 0.33):
                r = run_cell(tok_fn, K, gapfrac, topq, B)
                q, p, s = r["QURAN"], r["poetry"], r["saj"]
                print(f"{K:>3} {topq:>5.2f} {gapfrac:>5.2f} {r['P']:>3} | "
                      f"{q[0]:>+7.2f}sd P={q[1]:>4.2f} | {p[0]:>+6.2f}sd | {s[0]:>+6.2f}sd")
print(f"\n[total {time.time()-t0:.1f}s]")
