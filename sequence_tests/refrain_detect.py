import re, time
import numpy as np, pandas as pd
from collections import defaultdict
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(7); t0 = time.time()
_DIA = re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT = re.compile("ـ"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _TAT.sub("", _DIA.sub("", str(t)))
    t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()
def sig(s):  # normalized ayah signature for verbatim-refrain matching
    return " ".join(nl(w) for w in WA.findall(str(s)) if nl(w))

raw = pd.read_excel(ROOT + "/Book6.xlsx", header=None, nrows=8); hdr = 0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr = i; break
df = pd.read_excel(ROOT + "/Book6.xlsx", header=hdr); df.columns = [str(c).strip() for c in df.columns]
scol = [c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
# segmented (de-diacritized) ayah text col: has متن + بي(without) ; diacritized has با
tcol = [c for c in df.columns if "متن" in nl(c) and "بي" in nl(c)][0]
print("text col:", repr(tcol))
df = df[[scol, tcol]].copy()
sur = {}
for s, txt in zip(df[scol].tolist(), df[tcol].tolist()):
    try: si = int(float(s))
    except Exception: continue
    if 1 <= si <= 114: sur.setdefault(si, []).append(sig(txt))

def refrain_stat(seq):
    pos = defaultdict(list)
    for i, s in enumerate(seq):
        if s: pos[s].append(i)
    best, bc, bp = 0.0, 0, None
    for s, ps in pos.items():
        if len(ps) < 3: continue
        g = np.diff(ps); reg = 1.0 / (1.0 + g.std() / (g.mean() + 1e-9))
        if reg > best: best, bc, bp = reg, len(ps), s
    return best, bc, bp
def refrain_z(seq, R=500):
    real, c, s = refrain_stat(seq)
    if c < 3: return None
    arr = list(seq); nu = np.empty(R)
    for t in range(R):
        rng.shuffle(arr); nu[t] = refrain_stat(arr)[0]
    return real, c, (real - nu.mean()) / (nu.std() + 1e-9)

# ---- GATE: the Qur'an's own known refrain surahs must light up ----
print("[%.1fs] ===== REFRAIN DETECTOR GATE (known refrain surahs) =====" % (time.time() - t0))
known = {55: "ar-Rahman فبأي آلاء", 77: "al-Mursalat ويل يومئذ", 54: "al-Qamar", 26: "ash-Shu'ara", 56: "al-Waqi'a"}
for s in [55, 77, 54, 26, 56]:
    r = refrain_z(sur[s])
    if r: print("  S%-3d %-22s reg=%.2f count=%2d  z=%+.1f" % (s, known.get(s, ""), r[0], r[1], r[2]))
    else: print("  S%-3d %-22s no repeated ayah (count<3)" % (s, known.get(s, "")))

# ---- ALL surahs ----
print("\n[%.1fs] ===== ALL SURAHS =====" % (time.time() - t0))
res = []
for s, seq in sorted(sur.items()):
    r = refrain_z(seq)
    if r: res.append((s, r[0], r[1], r[2]))
nz = [x for x in res if x[3] is not None]
zz = np.array([x[3] for x in nz])
print("  surahs with a repeated-ayah (count>=3): %d / 114" % len(nz))
print("  of those: frac z>2 = %.0f%%  | frac z>3 = %.0f%%  | mean z = %+.2f"
      % (100*np.mean(zz > 2), 100*np.mean(zz > 3), zz.mean()))
print("  top periodic-refrain surahs (surah, reg, count, z):")
for s, reg, c, z in sorted(nz, key=lambda x: -x[3])[:15]:
    print("     S%-3d reg=%.2f count=%2d z=%+.1f" % (s, reg, c, z))

# ---- ordinary-Arabic control: pseudo-surahs of pseudo-ayat (6-word) ----
otoks = []
for fn in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news"):
    for ln in open("corpus/%s.txt" % fn, encoding="utf-8", errors="ignore"):
        otoks += [nl(x) for x in WA.findall(ln) if nl(x)]
opa = [" ".join(otoks[i:i+6]) for i in range(0, len(otoks) - 6, 6)]
ocount = 0; oz = []
for i in range(0, len(opa) - 80, 80):
    r = refrain_z(opa[i:i+80], R=300)
    if r: ocount += 1; oz.append(r[2])
print("\n  ordinary pseudo-surahs with repeated pseudo-ayah: %d (of %d) -> refrains essentially absent"
      % (ocount, len(opa)//80))
print("\n[total %.1fs]" % (time.time() - t0))
