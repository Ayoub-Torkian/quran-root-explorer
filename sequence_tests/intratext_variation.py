# -*- coding: utf-8 -*-
"""
SURAH-AWARE VARIATION PROFILE (#42b) — CORRECTED TOKENIZATION.

Promotes #42 from "recurrence exists" to "characterise HOW the Qur'an retells the
same stories across distant surahs". Uses CHARACTER-ANCHORED narrative clusters
(Musa, Nuh, Ibrahim, Adam, Maryam, ...) instead of a blind giant component, and
the FIXED real-word tokenization (normalize-then-split; anchors actually appear).

For each anchor we take the passages that mention it, form CROSS-SURAH pairs
(two retellings in different surahs), and measure the VARIATION craft:
   content-Jaccard   shared vocabulary (same story?)
   reorder           frac. discordant order of shared words (HIGH = re-sequenced)
   verbatim-run      longest shared contiguous token run (LOW = NOT a refrain)
   length-ratio      expand / compress
Contrast vs POETRY (Mutanabbi reused-motif pairs) and ORDINARY pairs selected at
a MATCHED cosine similarity, so the comparison is "given equally-similar passages,
how does each corpus vary them?"  GATE: recover injected substitution/reorder.
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
STOP = {nl(w) for w in ("في من الى على عن مع و ف ب ك ل ال هذا هذه ذلك التي الذي الذين ما لا ان انه اذا قد كان"
        " هو هي هم انت انا نحن كل بعض غير عند او ثم حتى يا اي بين لم لن لو ولا فلا وما وان به له لهم"
        " هنا هناك كما لقد وقد منه منها فيها فيه عليه عليها اليه اليها علي الي ومن لكم اني قال قالوا").split()}
def tok_text(s): return [w for w in WA.findall(nl(s)) if len(w) > 1]
def cw(toklist): return [w for w in toklist if w not in STOP and len(w) > 1]

# ---- load Qur'an ordered content-words WITH surah tags (FIXED tokenization) ----
c = A.load_corpus(ROOT + "/Book6.xlsx")
SUR = "ش  سوره"; SNAME = "اسم سوره"
toks, surah_of, sur_name = [], [], {}
for i in range(len(c.df)):
    s = int(c.df.iloc[i][SUR]); sur_name[s] = str(c.df.iloc[i][SNAME])
    for w in cw(tok_text(str(c.df.iloc[i][D]))):
        toks.append(w); surah_of.append(s)
K = 50
n = (len(toks)//K)*K
PASS = [toks[i:i+K] for i in range(0, n, K)]
PSUR = [Counter(surah_of[i:i+K]).most_common(1)[0][0] for i in range(0, n, K)]
P = len(PASS)
print(f"[{time.time()-t0:.1f}s] Qur'an: {len(toks)} content-words -> {P} passages (K={K})")

def cosmat(passlist):
    vocab = {}
    for p in passlist:
        for w in p: vocab.setdefault(w, len(vocab))
    V = np.zeros((len(passlist), len(vocab)))
    for i, p in enumerate(passlist):
        for w, ct in Counter(p).items(): V[i, vocab[w]] = ct
    df = (V > 0).sum(0); idf = np.log((len(passlist)+1)/(df+1))+1
    V = V*idf; nrm = np.linalg.norm(V, axis=1, keepdims=True); nrm[nrm == 0] = 1
    Vn = V/nrm; return Vn @ Vn.T
Cm = cosmat(PASS)

# ---------- variation metrics ----------
def reorder_rate(a, b):
    sb = set(b)
    sa_seq = [w for w in a if w in sb]
    sb_seq = [w for w in b if w in set(a)]
    common = list(dict.fromkeys([w for w in sa_seq if w in set(sb_seq)]))
    if len(common) < 3: return None
    pa = {w: i for i, w in enumerate([w for w in a if w in common])}
    pb = {w: i for i, w in enumerate([w for w in b if w in common])}
    conc = disc = 0
    for x in range(len(common)):
        for y in range(x+1, len(common)):
            u, v = common[x], common[y]
            s = (pa[u]-pa[v])*(pb[u]-pb[v])
            if s > 0: conc += 1
            elif s < 0: disc += 1
    return None if conc+disc == 0 else disc/(conc+disc)
def longest_run(a, b):
    la, lb = len(a), len(b); prev = [0]*(lb+1); best = 0
    for x in range(1, la+1):
        curr = [0]*(lb+1)
        for y in range(1, lb+1):
            if a[x-1] == b[y-1]:
                curr[y] = prev[y-1]+1
                if curr[y] > best: best = curr[y]
        prev = curr
    return best
def metrics(a, b):
    sa, sb = set(a), set(b)
    jac = len(sa & sb)/len(sa | sb)
    return jac, reorder_rate(a, b), longest_run(a, b), min(len(a), len(b))/max(len(a), len(b))
def profile(pairs, passlist, cosfn=None):
    J, R, RUN, LR, COS = [], [], [], [], []
    for i, j in pairs:
        jac, ro, run, lr = metrics(passlist[i], passlist[j])
        J.append(jac); RUN.append(run); LR.append(lr)
        if ro is not None: R.append(ro)
        if cosfn is not None: COS.append(cosfn(i, j))
    f = lambda v: (float(np.mean(v)), float(np.std(v))) if v else (float("nan"), 0.0)
    out = {"n": len(pairs), "jaccard": f(J), "reorder": f(R), "run": f(RUN), "lenratio": f(LR)}
    if COS: out["cos"] = f(COS)
    return out

# ---------- CHARACTER-ANCHORED narrative story-clusters ----------
anchors = {"Musa(موسى)": "موسي", "Firaun(فرعون)": "فرعون", "Nuh(نوح)": "نوح",
           "Ibrahim(ابراهيم)": "ابراهيم", "Adam(آدم)": "ادم", "Maryam(مريم)": "مريم",
           "Yusuf(يوسف)": "يوسف", "Lut(لوط)": "لوط", "Sulayman(سليمان)": "سليمان",
           "Dawud(داود)": "داود"}
print(f"\n[{time.time()-t0:.1f}s] ===== CHARACTER-ANCHORED RETELLING CLUSTERS =====")
print(f"   {'anchor':16s} {'#pass':>5} {'#surahs':>7} {'surah-span':>10} {'xS-pairs':>8} {'medCos':>6}")
allnarr = []   # cross-surah narrative pairs (Qur'an)
for name, form in anchors.items():
    idxs = [i for i in range(P) if form in set(PASS[i])]
    surs = sorted({PSUR[i] for i in idxs})
    xpairs = [(i, j) for a in range(len(idxs)) for b in range(a+1, len(idxs))
              for i, j in [(idxs[a], idxs[b])] if PSUR[i] != PSUR[j]]
    if not idxs: continue
    medcos = np.median([Cm[i, j] for i, j in xpairs]) if xpairs else float("nan")
    span = (max(surs)-min(surs)) if surs else 0
    print(f"   {name:16s} {len(idxs):>5} {len(surs):>7} {span:>10} {len(xpairs):>8} {medcos:>6.3f}")
    allnarr += xpairs

qnarr = profile(allnarr, PASS, cosfn=lambda i, j: Cm[i, j])
print(f"\n   ALL cross-surah narrative pairs: n={qnarr['n']}  median cos={qnarr['cos'][0]:.3f}")
# the genuine SAME-EPISODE retellings = top-cosine decile of same-anchor cross-surah pairs
allnarr_sorted = sorted(allnarr, key=lambda ij: -Cm[ij[0], ij[1]])
topnarr = allnarr_sorted[:max(20, len(allnarr)//10)]
qepis = profile(topnarr, PASS, cosfn=lambda i, j: Cm[i, j])
print(f"   SAME-EPISODE subset (top-cos decile): n={qepis['n']}  median cos={qepis['cos'][0]:.3f}")

# ---------- comparators at MATCHED cosine ----------
def fileW(p): return tok_text(open(p, encoding="utf-8", errors="ignore").read())
def build(words, K=50):
    w = cw(words); m = (len(w)//K)*K; return [w[i:i+K] for i in range(0, m, K)]
def matched_pairs(passlist, target_cos, tol=0.08, far=0.10, cap=400):
    Pn = len(passlist)
    if Pn < 6: return [], None
    Cn = cosmat(passlist); gap = max(1, int(Pn*far))
    cand = [(i, j, Cn[i, j]) for i in range(Pn) for j in range(i+gap, Pn)]
    sel = [(i, j) for i, j, cc in cand if abs(cc-target_cos) <= tol]
    if len(sel) < 8:  # fall back: take the top-similarity far pairs
        cand.sort(key=lambda x: -x[2]); sel = [(i, j) for i, j, _ in cand[:max(8, cap//4)]]
    rng.shuffle(sel); sel = sel[:cap]
    mc = np.median([Cn[i, j] for i, j in sel])
    return sel, mc
tgt = qnarr["cos"][0]
poet = build(fileW(ROOT + "/sequence_tests/corpus/ar_poetry.txt"))
ordw = []
for f in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"):
    ordw += fileW(ROOT + f"/sequence_tests/corpus/{f}.txt")
ordp = build(ordw)
pp, pmc = matched_pairs(poet, tgt); op, omc = matched_pairs(ordp, tgt)
pprof = profile(pp, poet); oprof = profile(op, ordp)

# Qur'an refrain control: its OWN most-verbatim far pairs (should be long runs, low reorder)
gapq = max(1, int(P*0.10))
qfar = sorted([(i, j, Cm[i, j]) for i in range(P) for j in range(i+gapq, P)], key=lambda x:-x[2])
qref = profile([(i, j) for i, j, _ in qfar[:120]], PASS)

def show(name, pr, mc=None):
    extra = f" cos~{mc:.2f}" if mc is not None else (f" cos~{pr['cos'][0]:.2f}" if 'cos' in pr else "")
    print(f"  {name:22s} n={pr['n']:4d}{extra} | Jaccard {pr['jaccard'][0]:.3f} | "
          f"reorder {pr['reorder'][0]:.3f} | verbatim-run {pr['run'][0]:.2f} | lenratio {pr['lenratio'][0]:.3f}")
print(f"\n[{time.time()-t0:.1f}s] ===== VARIATION PROFILE (matched-similarity pairs) =====")
print("   high Jaccard + high reorder + SHORT verbatim-run = 'same story, re-sequenced & re-expressed'")
show("QURAN narrative xS", qnarr)
show("QURAN same-episode top", qepis)
show("QURAN top-sim (refrain ctl)", qref)
show("poetry reused", pprof, pmc)
show("ordinary", oprof, omc)

# ---------- GATE ----------
print(f"\n[{time.time()-t0:.1f}s] ===== GATE: recover injected variation =====")
base = PASS[100]; pool = [w for w in toks if w not in set(base)]
def retell(p, sub, reorder=True):
    q = list(p)
    for k in rng.choice(len(q), int(len(q)*sub), replace=False): q[k] = pool[rng.integers(0, len(pool))]
    if reorder: rng.shuffle(q)
    return q
for sr in (0.0, 0.25, 0.5):
    jac, ro, run, lr = metrics(base, retell(base, sr))
    print(f"   sub={sr:.2f} reorder=on  -> Jaccard={jac:.3f} reorder={ro:.3f}(hi) verbatim-run={run}")
jac, ro, run, lr = metrics(base, retell(base, 0.25, reorder=False))
print(f"   sub=0.25 reorder=off -> Jaccard={jac:.3f} reorder={ro:.3f}(~0) verbatim-run={run}(long)")
print(f"\n[total {time.time()-t0:.1f}s]")
