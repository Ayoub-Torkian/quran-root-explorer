# -*- coding: utf-8 -*-
"""
MODALITY 10 — DISCOURSE / RHETORICAL MACROSTRUCTURE (complete run).
See discourse.py for the full docstring. Tags units by speech-act MOVE, then tests
whether the SEQUENCE of moves is distinctive (shuffle-controlled) vs ordinary/poetry/saj',
plus a base-rate move-DIVERSITY descriptive. Gate-validated.
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

OATH_NOUNS = {nl(w) for w in "الشمس القمر الليل النهار الفجر العصر التين الزيتون السماء النجم الطور والعاديات الضحي القلم الفلق الناس الكتاب المرسلات النازعات الذاريات".split()}
OATH_CUE  = {nl(w) for w in "اقسم لاقسم قسم".split()}
ADDR_CUE  = {nl(w) for w in "يا ايها قل قلنا اتقوا اعبدوا امنوا اعلموا انفقوا اذكروا كلوا اشكروا فاعبدون يايها".split()}
NARR_CUE  = {nl(w) for w in "قال قالوا اذ فلما ارسلنا ارسل جاء جاءهم نوح موسي فرعون ابراهيم لوط عاد ثمود مريم يوسف اتينا وهبنا نادي".split()}
JUDG_CUE  = {nl(w) for w in "يوم القيامه النار الجنه الحساب جهنم عذاب يومئذ الاخره جزاء الصراط الميزان خالدين عقاب ثواب الساعه".split()}
INT_CUE   = {nl(w) for w in "هل افلا الم اولم اين كيف متي ايان لماذا اليس".split()}
ASSERT_CUE= {nl(w) for w in "ان الله ربكم رب العالمين لا اله سبحان الحمد تبارك انما".split()}
MOVES = ["OATH", "ADDR", "NARR", "JUDG", "INT", "ASSERT"]

def tag_unit(ws):
    if not ws: return "ASSERT"
    sw = set(ws); sc = {m: 0 for m in MOVES}
    if ws[0].startswith(nl("و")) and (sw & OATH_NOUNS): sc["OATH"] += 3
    sc["OATH"] += len(sw & OATH_CUE)
    sc["ADDR"] += len(sw & ADDR_CUE)
    sc["NARR"] += len(sw & NARR_CUE)
    sc["JUDG"] += len(sw & JUDG_CUE)
    sc["INT"] += len(sw & INT_CUE)
    sc["ASSERT"] += len(sw & ASSERT_CUE)
    best = max(MOVES, key=lambda m: sc[m])
    return best if sc[best] > 0 else "ASSERT"

def switch_rate(labels):
    if len(labels) < 2: return None
    return np.mean([labels[i] != labels[i+1] for i in range(len(labels)-1)])
def transition_mi(labels):
    if len(labels) < 3: return None
    a = labels[:-1]; b = labels[1:]; idx = {m: k for k, m in enumerate(MOVES)}
    M = np.zeros((6, 6))
    for x, y in zip(a, b): M[idx[x], idx[y]] += 1
    Pxy = M / M.sum(); Px = Pxy.sum(1, keepdims=True); Py = Pxy.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        mi = np.nansum(Pxy * np.log((Pxy + 1e-12) / (Px * Py + 1e-12)))
    Hx = -np.nansum(Px * np.log(Px + 1e-12))
    return mi / (Hx + 1e-12) if Hx > 0 else 0.0
def run_excess(labels):
    if len(labels) < 2: return None
    runs = 1
    for i in range(1, len(labels)):
        if labels[i] != labels[i-1]: runs += 1
    return len(labels) / runs
def move_entropy(labels):
    if not labels: return None
    ct = Counter(labels); tot = len(labels)
    p = np.array([v/tot for v in ct.values()])
    return float(-(p*np.log(p)).sum())

def stat_excess(labels, W, B, statfn):
    if len(labels) < W: return None
    vals = []
    for _ in range(B):
        s = rng.integers(0, len(labels)-W+1); win = labels[s:s+W]
        real = statfn(win); sh = list(win); rng.shuffle(sh); shuf = statfn(sh)
        if real is not None and shuf is not None: vals.append(real - shuf)
    return np.array(vals) if vals else None
def window_stat(labels, W, B, statfn):
    if len(labels) < W: return None
    vals = []
    for _ in range(B):
        s = rng.integers(0, len(labels)-W+1); v = statfn(labels[s:s+W])
        if v is not None: vals.append(v)
    return np.array(vals) if vals else None
def g(a, b):
    if a is None or b is None or len(a) < 2 or len(b) < 2: return float("nan")
    return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
def boot_p(a, b, R=2000):
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5*np.mean(a[ai] == b[bi]))

c = A.load_corpus(ROOT + "/Book6.xlsx")
q_labels = [tag_unit(words(str(c.df.iloc[i][D]))) for i in range(len(c.df))]
UNIT_SPLIT = re.compile(r"[.!؟?\n،؛:]+")
def file_labels(paths):
    txt = ""
    for p in paths: txt += "\n" + open(p, encoding="utf-8", errors="ignore").read()
    labs = []
    for unit in UNIT_SPLIT.split(txt):
        ws = words(unit)
        if len(ws) >= 2: labs.append(tag_unit(ws))
    return labs
CP = ROOT + "/sequence_tests/corpus/"
ord_labels = file_labels([CP+f+".txt" for f in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2")])
poet_labels = file_labels([CP+"ar_poetry.txt"])
saj_labels = file_labels([CP+"ar_sajprose.txt", CP+"ar_saj_hariri.txt"])
corp = {"QURAN": q_labels, "ord-Arabic": ord_labels, "poetry": poet_labels, "saj'": saj_labels}
print(f"[{time.time()-t0:.1f}s] units:", {k: len(v) for k, v in corp.items()})

W = max(20, min(60, min(len(v) for v in corp.values()) // 2)); B = 400
print(f"\n=== SEQUENCING (shuffle-controlled, equal-N W={W}) ===")
print(f"   {'corpus':12s} {'switchEx':>9s} {'vs-ord':>14s} | {'MI-Ex':>7s} {'vs-ord':>14s} | {'runlenEx':>8s} {'vs-ord':>14s}")
sw = {nm: stat_excess(l, W, B, switch_rate) for nm, l in corp.items()}
miE = {nm: stat_excess(l, W, B, transition_mi) for nm, l in corp.items()}
rl = {nm: stat_excess(l, W, B, run_excess) for nm, l in corp.items()}
for nm in corp:
    e1 = "" if nm == "ord-Arabic" else f"d={g(sw[nm],sw['ord-Arabic']):+5.2f}sd P={boot_p(sw[nm],sw['ord-Arabic']):.2f}"
    e2 = "" if nm == "ord-Arabic" else f"d={g(miE[nm],miE['ord-Arabic']):+5.2f}sd P={boot_p(miE[nm],miE['ord-Arabic']):.2f}"
    e3 = "" if nm == "ord-Arabic" else f"d={g(rl[nm],rl['ord-Arabic']):+5.2f}sd P={boot_p(rl[nm],rl['ord-Arabic']):.2f}"
    print(f"   {nm:12s} {sw[nm].mean():>+9.3f} {e1:>14s} | {miE[nm].mean():>+7.3f} {e2:>14s} | {rl[nm].mean():>+8.3f} {e3:>14s}")

print(f"\n=== DESCRIPTIVE: MOVE-ENTROPY (genre-inventory diversity, base-rate, NOT shuffle-ctl) ===")
me = {nm: window_stat(l, W, B, move_entropy) for nm, l in corp.items()}
for nm in corp:
    extra = "" if nm == "ord-Arabic" else f"d={g(me[nm],me['ord-Arabic']):+5.2f}sd P={boot_p(me[nm],me['ord-Arabic']):.2f}"
    print(f"   {nm:12s} move-entropy {me[nm].mean():.3f}  {extra}")
print(f"\n[total {time.time()-t0:.1f}s]")
