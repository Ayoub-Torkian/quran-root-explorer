import re, time
import numpy as np
from collections import Counter
WF = re.compile(r"[^\W\d_]+", re.UNICODE)
rng = np.random.default_rng(11); t0 = time.time()
def yuleK(w):
    c = Counter(w); N = len(w); vi = Counter(c.values())
    return 1e4 * (sum(v*(i*i) for i, v in vi.items()) - N) / (N*N + 1e-9)
def crep(w, n):
    s = " ".join(w)
    if len(s) <= n: return 0.0
    g = Counter(s[i:i+n] for i in range(len(s)-n)); return 1 - len(g)/max(len(s)-n, 1)
def meas(w):
    N = len(w); wl = np.array([len(x) for x in w]); fc = Counter(w)
    wp = np.array(list(fc.values()), float)/N
    return dict(yuleK=yuleK(w), word_ent=-np.sum(wp*np.log2(wp)), ttr=len(fc)/N,
                std_wl=wl.std(), mean_wl=wl.mean(), frac_long=float(np.mean(wl >= 7)),
                rep8=crep(w, 8), rep12=crep(w, 12))
def win(w, N=300, step=150, maxw=30):
    rows = []
    for c in range(0, max(1, len(w)-N+1), step):
        s = w[c:c+N]
        if len(s) < N*0.8: break
        rows.append(meas(s))
        if len(rows) >= maxw: break
    if not rows: rows = [meas(w)]
    ks = rows[0].keys(); return {k: np.array([r[k] for r in rows]) for k in ks}
def load(*ps):
    out = []
    for p in ps:
        for ln in open(p, encoding="utf-8", errors="ignore"):
            out += WF.findall(ln)
    return out
M = load("corpus/fa_poetry.txt")
O = load("corpus/fa_news.txt", "corpus/fa_prose.txt")
DM = win(M); DO = win(O)
print("[%.1fs] PERSIAN: masters(poetry) vs ordinary(news+esra-prose)" % (time.time()-t0))
print("  masters words=%d win=%d ; ordinary words=%d win=%d" % (len(M), len(DM["ttr"]), len(O), len(DO["ttr"])))
def gap(a, b): return (a.mean()-b.mean()) / (np.sqrt((a.var()+b.var())/2) + 1e-9)
def bp(a, b): return float(np.mean(rng.choice(a, 6000) > rng.choice(b, 6000)))
shdir = {"yuleK": -1, "word_ent": 1, "ttr": 1, "std_wl": -1, "frac_long": -1, "rep8": -1, "rep12": -1}
for k in ["rep8", "rep12", "std_wl", "frac_long", "yuleK", "ttr", "word_ent", "mean_wl"]:
    g = gap(DM[k], DO[k]); P = bp(DM[k], DO[k]); d = shdir.get(k)
    tag = "" if d is None else ("master-dir" if np.sign(g) == d else "OPPOSITE")
    print("  %-9s M=%.4f O=%.4f %+.1fsd P=%.2f %s" % (k, DM[k].mean(), DO[k].mean(), g, P, tag))
print("[total %.1fs]" % (time.time()-t0))
