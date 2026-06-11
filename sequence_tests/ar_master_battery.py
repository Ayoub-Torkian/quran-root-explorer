import re, sys, time
import numpy as np
import pandas as pd
from collections import Counter
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
WA = re.compile(r"[^\W\d_]+", re.UNICODE)
rng = np.random.default_rng(7); t0 = time.time()

_DIA = re.compile(r"[ً-ٰٟۖ-ۭ]")
_TAT = re.compile("ـ")
def strip_diacritics(t):
    if not isinstance(t, str): return ""
    return _TAT.sub("", _DIA.sub("", t)).strip()
def normalize_letters(t):
    if not isinstance(t, str): return ""
    t = strip_diacritics(t)
    t = re.sub(r"[آأإٱٲٳ]", "ا", t)  # alef
    t = re.sub(r"[یىێېۍؠ]", "ي", t)  # yeh
    t = re.sub(r"[ةھۀ]", "ه", t)                       # heh/ta-marbuta
    t = re.sub(r"[کڪګ]", "ك", t)                       # kaf
    t = re.sub(r"[ۆۇۈۉۋۅۥ]", "و", t)  # waw
    t = re.sub(r"[ؤئ]", "ء", t)                             # hamza
    t = t.replace("ٔ", "").replace("ٕ", "")
    t = t.translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    return t.strip()

def yuleK(words):
    c = Counter(words); N = len(words); vi = Counter(c.values())
    return 1e4 * (sum(v*(i*i) for i, v in vi.items()) - N) / (N*N + 1e-9)
def crep(s, n):
    if len(s) <= n: return 0.0
    g = Counter(s[i:i+n] for i in range(len(s)-n)); return 1 - len(g)/max(len(s)-n, 1)
def measures(words, topdrop):
    N = len(words); wl = np.array([len(w) for w in words]); fc = Counter(words)
    wp = np.array(list(fc.values()), float)/N
    top = set(w for w, _ in fc.most_common(topdrop)) if topdrop else set()
    s = " ".join(w for w in words if w not in top)
    return dict(yuleK=yuleK(words), ttr=len(fc)/N, word_ent=-np.sum(wp*np.log2(wp)),
                std_wl=wl.std(), mean_wl=wl.mean(), frac_long=float(np.mean(wl >= 7)),
                rep8=crep(s, 8), rep12=crep(s, 12))
def win(words, N=350, step=175, maxw=120, topdrop=20):
    rows = []
    for c in range(0, max(1, len(words)-N+1), step):
        w = words[c:c+N]
        if len(w) < N*0.8: break
        rows.append(measures(w, topdrop))
        if len(rows) >= maxw: break
    if not rows: rows = [measures(words, topdrop)]
    ks = rows[0].keys(); return {k: np.array([r[k] for r in rows]) for k in ks}
def load_ar(*paths):
    out = []
    for p in paths:
        for ln in open(p, encoding="utf-8", errors="ignore"):
            ss = ln.strip()
            if not ss: continue
            out += [normalize_letters(w) for w in WA.findall(ss) if normalize_letters(w)]
    return out

def _nl(x): return normalize_letters(str(x))
_raw = pd.read_excel(ROOT + "/Book6.xlsx", header=None, nrows=8)
_hdr = 0
for _i in range(len(_raw)):
    if _raw.iloc[_i].map(_nl).str.contains("حركت", regex=False).any():
        _hdr = _i; break
df = pd.read_excel(ROOT + "/Book6.xlsx", header=_hdr)
df.columns = [str(c).strip() for c in df.columns]
_cand = [c for c in df.columns if ("حركت" in _nl(c)) and ("بي" not in _nl(c))]
col = _cand[0]
print("diacritized column =", repr(col))
qw = [normalize_letters(w) for v in df[col].fillna("").astype(str).tolist()
      for w in v.split() if normalize_letters(w)]

C = "corpus/"
reg = {"Quran": qw, "Mutanabbi": load_ar(C+"ar_poetry.txt"),
       "Classical": load_ar(C+"ar_tabari.txt", C+"ar_classical2.txt"),
       "Novel": load_ar(C+"ar_novel.txt"), "News": load_ar(C+"ar_news.txt")}
D = {k: win(v) for k, v in reg.items()}
print("[%.1fs] words:" % (time.time()-t0), {k: len(v) for k, v in reg.items()})
print("windows:", {k: len(D[k]["ttr"]) for k in reg})

def gap(a, b): return (a.mean()-b.mean()) / (np.sqrt((a.var()+b.var())/2) + 1e-9)
def bp(a, b): return float(np.mean(rng.choice(a, 6000) > rng.choice(b, 6000)))
ords = ["Classical", "Novel", "News"]
metrics = ["rep8", "rep12", "std_wl", "frac_long", "yuleK", "ttr", "word_ent", "mean_wl"]
shdir = {"rep8": -1, "rep12": -1, "std_wl": -1, "frac_long": -1, "yuleK": -1, "ttr": 1, "word_ent": 1}
for focus in ["Mutanabbi", "Quran"]:
    print("\n==== %s vs ordinary Arabic (pooled) ====" % focus)
    pool = {m: np.concatenate([D[o][m] for o in ords]) for m in metrics}
    for m in metrics:
        g = gap(D[focus][m], pool[m]); P = bp(D[focus][m], pool[m])
        d = shdir.get(m); tag = "" if d is None else ("master-dir" if np.sign(g) == d else "OPPOSITE")
        print("  %-9s %s=%.4f ord=%.4f %+.1fsd P=%.2f %s" % (m, focus, D[focus][m].mean(), pool[m].mean(), g, P, tag))
print("\n==== Mutanabbi vs Quran (direct, same language) ====")
for m in ["rep8", "rep12", "std_wl", "frac_long", "yuleK", "ttr"]:
    g = gap(D["Mutanabbi"][m], D["Quran"][m]); P = bp(D["Mutanabbi"][m], D["Quran"][m])
    print("  %-9s Mut=%.4f Qur=%.4f %+.1fsd P(Mut>Qur)=%.2f" % (m, D["Mutanabbi"][m].mean(), D["Quran"][m].mean(), g, P))
print("\n==== rep12 robustness across content-drop ====")
for td in (0, 20, 50):
    Dt = {k: win(v, topdrop=td) for k, v in reg.items()}
    pool12 = np.concatenate([Dt[o]["rep12"] for o in ords])
    gM = gap(Dt["Mutanabbi"]["rep12"], pool12); gQ = gap(Dt["Quran"]["rep12"], pool12)
    print("  drop%2d: Mutanabbi %+.1fsd | Quran %+.1fsd" % (td, gM, gQ))
print("\n[total %.1fs]" % (time.time()-t0))
