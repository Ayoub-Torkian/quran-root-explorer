import re, time
import numpy as np, pandas as pd
from collections import Counter
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(9); t0 = time.time()
_DIA = re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT = re.compile("ـ"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _TAT.sub("", _DIA.sub("", str(t)))
    t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()
def end2(unit_tokens):
    if not unit_tokens: return ""
    w = unit_tokens[-1]
    return w[-2:] if len(w) >= 2 else w

def metrics(endings):
    n = len(endings)
    if n < 4: return None
    c = Counter(endings); fr = np.array(list(c.values()), float) / n
    dom = fr.max()                                  # dominant-rhyme share
    chance = float(np.sum(fr ** 2))                 # expected adjacency if i.i.d.
    adj = np.mean([endings[i] == endings[i + 1] for i in range(n - 1)])
    excess = adj - chance                           # run structure beyond frequency
    return dom, excess, chance, n

# ---- Quran: per-surah ayah endings (de-diacritized segmented col) ----
raw = pd.read_excel(ROOT + "/Book6.xlsx", header=None, nrows=8); hdr = 0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr = i; break
df = pd.read_excel(ROOT + "/Book6.xlsx", header=hdr); df.columns = [str(c).strip() for c in df.columns]
scol = [c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
tcol = [c for c in df.columns if "متن" in nl(c) and "بي" in nl(c)][0]
sur = {}
for s, txt in zip(df[scol].tolist(), df[tcol].tolist()):
    try: si = int(float(s))
    except Exception: continue
    if 1 <= si <= 114:
        sur.setdefault(si, []).append(end2([nl(w) for w in WA.findall(str(txt)) if nl(w)]))

# ---- ordinary prose: pseudo-ayat of ~8 words, endings = last word ----
def prose_endings(fns, k=8):
    toks = []
    for fn in fns:
        for ln in open("corpus/%s.txt" % fn, encoding="utf-8", errors="ignore"):
            toks += [nl(x) for x in WA.findall(ln) if nl(x)]
    return [end2(toks[i:i+k]) for i in range(0, len(toks)-k, k)]
prose = prose_endings(["ar_tabari", "ar_classical2", "ar_novel", "ar_news"])
# poetry: per-line endings (each line = hemistich)
_pl = []
for ln in open("corpus/ar_poetry.txt", encoding="utf-8", errors="ignore"):
    w = [nl(x) for x in WA.findall(ln) if nl(x)]
    if w: _pl.append(end2(w))
poet_lines = _pl[1::2]  # bayt-final hemistich only (the rhyme-bearing one)

# ============ GATE ============
print("[%.1fs] ===== RHYME DETECTOR GATE =====" % (time.time()-t0))
synth = ["ون"] * 30                                   # perfect monorhyme
m = metrics(synth); print("  (1) synthetic monorhyme: dom=%.2f excess=%+.2f [expect dom~1, excess~+1]" % (m[0], m[1]))
print("  (2) degradation (replace endings with random):")
for frac in (0.0, 0.5, 1.0):
    s = synth.copy(); k = int(frac*len(s)); idx = rng.choice(len(s), k, replace=False)
    for i in idx: s[i] = "r%d" % rng.integers(1e6)
    m = metrics(s); print("        random %3d%%: dom=%.2f excess=%+.2f" % (int(frac*100), m[0], m[1]))
mp = metrics(prose[:200]); print("  (3) ordinary prose (chunked): dom=%.2f excess=%+.2f [expect low]" % (mp[0], mp[1]))

# ============ COMPARE: Quran surahs vs prose chunks vs poetry ============
print("\n===== FASILA (verse-end rhyme) ACROSS REGISTERS =====")
QD = [metrics(sur[s]) for s in sorted(sur) if metrics(sur[s])]
Qdom = np.array([m[0] for m in QD]); Qexc = np.array([m[1] for m in QD])
PD = [metrics(prose[i:i+40]) for i in range(0, len(prose)-40, 40)]; PD = [m for m in PD if m]
Pdom = np.array([m[0] for m in PD]); Pexc = np.array([m[1] for m in PD])
poemchunks = [poet_lines[i:i+40] for i in range(0, len(poet_lines)-40, 40)]
LD = [metrics(c) for c in poemchunks]; LD = [m for m in LD if m]
Ldom = np.array([m[0] for m in LD]); Lexc = np.array([m[1] for m in LD])
def g(a, b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
print("  register      | dom-rhyme share | run-excess | (n)")
print("  Quran  surahs | %.2f            | %+.2f      | %d" % (Qdom.mean(), Qexc.mean(), len(QD)))
print("  Arabic poetry | %.2f            | %+.2f      | %d" % (Ldom.mean(), Lexc.mean(), len(LD)))
print("  ordinary prose| %.2f            | %+.2f      | %d" % (Pdom.mean(), Pexc.mean(), len(PD)))
print("  Quran vs prose: dom %+.1fsd | excess %+.1fsd" % (g(Qdom, Pdom), g(Qexc, Pexc)))
print("  Quran vs poetry: dom %+.1fsd | excess %+.1fsd" % (g(Qdom, Ldom), g(Qexc, Lexc)))
print("  frac Quran surahs dom>0.5: %.0f%% | prose: %.0f%%" % (100*np.mean(Qdom>0.5), 100*np.mean(Pdom>0.5)))
print("\n[total %.1fs]" % (time.time()-t0))
