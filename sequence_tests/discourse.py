# -*- coding: utf-8 -*-
"""
MODALITY 10 — DISCOURSE / RHETORICAL MACROSTRUCTURE (the macro-rhythm of genres).

Hypothesis (handoff option A): the Qur'an's distinctive structure may live not in any
single feature but in how it SEQUENCES speech-act MOVES — oath -> narrative -> judgment
-> address -> assertion — switching genre/register far more, and with more pattern, than
ordinary prose, poetry, or saj' (which stay in one register). Cleanest new text-computable
lens; no parser needed.

Method (mirrors the #42 shuffle-control logic, applied to MOVE-LABELS not words):
  1. Split each corpus into UNITS (Qur'an = ayah; comparators = punctuation/clause units).
  2. Tag each unit with one of 6 speech-act MOVES via general-Arabic lexical cues:
     OATH, ADDRESS/COMMAND, NARRATIVE, JUDGMENT/ESCHATOLOGY, INTERROGATION, ASSERTION.
  3. Two sequence-structure statistics on the move-label sequence:
       (a) SWITCH rate        = fraction of adjacent units with a DIFFERENT move
                                (genre-heterogeneity / register-mixing)
       (b) transition MI      = mutual information I(move_t ; move_{t+1}), normalized
                                (patterned, predictable macro-rhythm)
  4. SHUFFLE-CONTROL: compare each statistic to the SAME labels randomly reordered, so
     base-rate (topical) move frequencies cancel and only SEQUENCING structure remains.
  5. Equal-N windows + bootstrap; cross-corpus sd-gaps vs same-language ordinary baseline.
  6. GATE: a planted structured sequence (periodic blocks) must fire; random must null.
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

# ---------- speech-act MOVE lexicons (normalized, general Arabic) ----------
OATH_NOUNS = {nl(w) for w in "الشمس القمر الليل النهار الفجر العصر التين الزيتون السماء النجم الطور والعاديات الضحي القلم الفلق الناس الكتاب المرسلات النازعات الذاريات".split()}
OATH_CUE  = {nl(w) for w in "اقسم لاقسم قسم اولا فلا".split()}
ADDR_CUE  = {nl(w) for w in "يا ايها قل قلنا اتقوا اعبدوا امنوا اعلموا انفقوا اذكروا كلوا اشكروا فاعبدون يايها يا".split()}
NARR_CUE  = {nl(w) for w in "قال قالوا اذ فلما ارسلنا ارسل جاء جاءهم نوح موسي فرعون ابراهيم لوط عاد ثمود مريم يوسف اتينا وهبنا نادي".split()}
JUDG_CUE  = {nl(w) for w in "يوم القيامه النار الجنه الحساب جهنم عذاب يومئذ الاخره جزاء الصراط الميزان خالدين عقاب ثواب الساعه".split()}
INT_CUE   = {nl(w) for w in "هل افلا الم اولم اين كيف متي ايان لماذا اليس اءذا اءنا".split()}
ASSERT_CUE= {nl(w) for w in "ان الله ربكم رب العالمين لا اله سبحان الحمد تبارك انما".split()}
MOVES = ["OATH", "ADDR", "NARR", "JUDG", "INT", "ASSERT"]

def tag_unit(ws):
    if not ws: return "ASSERT"
    sw = set(ws)
    sc = {m: 0 for m in MOVES}
    # OATH: leading waw + cosmic/temporal noun, or explicit oath cue
    if (ws[0] == nl("و") or ws[0].startswith(nl("و"))) and (sw & OATH_NOUNS): sc["OATH"] += 3
    sc["OATH"] += len(sw & OATH_CUE)
    sc["ADDR"] += len(sw & ADDR_CUE)
    sc["NARR"] += len(sw & NARR_CUE)
    sc["JUDG"] += len(sw & JUDG_CUE)
    # interrogation: hamza-initial question or explicit interrogatives
    sc["INT"] += len(sw & INT_CUE) + (1 if ws[0][:1] == nl("ا") and len(ws[0]) <= 4 else 0) * 0
    sc["ASSERT"] += len(sw & ASSERT_CUE)
    best = max(MOVES, key=lambda m: sc[m])
    return best if sc[best] > 0 else "ASSERT"

# ---------- sequence-structure statistics ----------
def switch_rate(labels):
    if len(labels) < 2: return None
    return np.mean([labels[i] != labels[i+1] for i in range(len(labels)-1)])
def transition_mi(labels):
    """normalized MI between consecutive move-labels."""
    if len(labels) < 3: return None
    a = labels[:-1]; b = labels[1:]
    idx = {m: k for k, m in enumerate(MOVES)}
    M = np.zeros((len(MOVES), len(MOVES)))
    for x, y in zip(a, b): M[idx[x], idx[y]] += 1
    Pxy = M / M.sum()
    Px = Pxy.sum(1, keepdims=True); Py = Pxy.sum(0, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore"):
        mi = np.nansum(Pxy * np.log((Pxy + 1e-12) / (Px * Py + 1e-12)))
    Hx = -np.nansum(Px * np.log(Px + 1e-12))
    return mi / (Hx + 1e-12) if Hx > 0 else 0.0

def run_excess(labels):
    """mean run-length of move-labels: blocks coherent? (computed as a window stat)."""
    if len(labels) < 2: return None
    runs = 1
    for i in range(1, len(labels)):
        if labels[i] != labels[i-1]: runs += 1
    return len(labels) / runs   # mean run length
def move_entropy(labels):
    """base-rate DIVERSITY of moves in a window (NOT shuffle-controlled): genre richness."""
    if not labels: return None
    ct = Counter(labels); tot = len(labels)
    p = np.array([v/tot for v in ct.values()])
    return float(-(p*np.log(p)).sum())
def window_stat(labels, W, B, statfn):
    """raw per-window statistic (no shuffle control) for base-rate comparisons."""
    if len(labels) < W: return None
    vals = []
    for _ in range(B):
        s = rng.integers(0, len(labels)-W+1)
        v = statfn(labels[s:s+W])
        if v is not None: vals.append(v)
    return np.array(vals) if vals else None

def stat_excess(labels, W, B, statfn):
    """equal-N windows of W units; per window: stat(real) - stat(shuffled labels)."""
    if len(labels) < W: return None
    vals = []
    for _ in range(B):
        s = rng.integers(0, len(labels) - W + 1)
        win = labels[s:s+W]
        real = statfn(win)
        sh = list(win); rng.shuffle(sh)
        shuf = statfn(sh)
        if real is not None and shuf is not None: vals.append(real - shuf)
    return np.array(vals) if vals else None

def g(a, b):
    if a is None or b is None or len(a) < 2 or len(b) < 2: return float("nan")
    return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
def boot_p(a, b, R=2000):
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5*np.mean(a[ai] == b[bi]))

# ---------- load corpora as UNIT -> move-label sequences ----------
c = A.load_corpus(ROOT + "/Book6.xlsx")
q_labels = [tag_unit(words(str(c.df.iloc[i][D]))) for i in range(len(c.df))]

UNIT_SPLIT = re.compile(r"[.!؟?\n،؛:]+")  # clause/pause units for comparators
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
print(f"[{time.time()-t0:.1f}s] units per corpus:", {k: len(v) for k, v in corp.items()})
for k, v in corp.items():
    dist = Counter(v); tot = len(v)
    print(f"   {k:12s} move-mix: " + " ".join(f"{m}={dist.get(m,0)*100//tot}%" for m in MOVES))

# ---------- GATE ----------
print(f"\n[{time.time()-t0:.1f}s] ===== GATE (structured vs random move-sequences) =====")
struct = (MOVES * 200)[:600]                      # periodic ABCDEF blocks -> high MI, switch=1
blocks = sum([[m]*6 for m in MOVES]*20, [])[:600] # coherent runs -> low switch, high MI
randseq = [MOVES[rng.integers(0, 6)] for _ in range(600)]
for nm, seq in (("periodic", struct), ("block-runs", blocks), ("random", randseq)):
    sr = switch_rate(seq); mi = transition_mi(seq)
    ex_sr = stat_excess(seq, 60, 200, switch_rate); ex_mi = stat_excess(seq, 60, 200, transition_mi)
    print(f"   {nm:11s} switch={sr:.2f} MI={mi:.3f} | excess switch={ex_sr.mean():+.3f} MI={ex_mi.mean():+.3f}")

# ---------- cross-corpus, equal-N ----------
W = max(20, min(60, min(len(v) for v in corp.values()) // 2))
B = 400
print(f"\n[{time.time()-t0:.1f}s] ===== cross-corpus, equal-N window W={W}, shuffle-controlled =====")
print(f"   {'corpus':12s} {'switchEx':>9s} {'vs-ord':>14s} | {'MI-Ex':>8s} {'vs-ord':>14s}")
res = {}
for nm, lab in corp.items():
    res[nm] = (stat_excess(lab, W, B, switch_rate), stat_excess(lab, W, B, transition_mi))
bs, bm = res["ord-Arabic"]
for nm in corp:
    se, me = res[nm]
    s_extra = "" if nm == "ord-Arabic" else f"d={g(se,bs):+5.2f}sd P={boot_p(se,bs):.2f}"
    m_extra = "" if nm == "ord-Arabic" else f"d={g(me,bm):+5.2f}sd P={boot_p(me,bm):.2f}"
    print(f"   {nm:12s} {se.mean():>+9.3f} {s_extra:>14s} | {me.mean():>+8.3f} {m_extra:>14s}")
print("   (switchEx>0 = more register-switching than a reshuffle of the same moves;")
print("    MI-Ex>0 = more patterned move-to-move transitions than chance.)")

# ---------- robustness: run-length excess (sequencing) ----------
print(f"\n[{time.time()-t0:.1f}s] ===== robustness: RUN-LENGTH excess (block coherence) =====")
rl = {nm: stat_excess(lab, W, B, run_excess) for nm, lab in corp.items()}
brl = rl["ord-Arabic"]
for nm in corp:
    extra = "" if nm == "ord-Arabic" else f"d={g(rl[nm],brl):+5.2f}sd P={boot_p(rl[nm],brl):.2f}"
    print(f"   {nm:12s} runlenEx {rl[nm].mean():+6.3f}  {extra}")

# ---------- descriptive: move-DIVERSITY (base-rate genre richness, NOT shuffle-controlled) ----------
print(f"\n[{time.time()-t0:.1f}s] ===== descriptive: MOVE-ENTROPY (genre inventory diversity) =====")
me = {nm: window_stat(lab, W, B, move_entropy) for nm, lab in corp.items()}
bme = me["ord-Arabic"]
for nm in corp:
    extra = "" if nm == "ord-Arabic" else f"d={g(me[nm],bme):+5.2f}sd P={boot_p(me[nm],bme):.2f}"
    print(f"   {nm:12s} move-entropy {me[nm].mean():.3f}  {extra}")
print("   (this IS base-rate: more genres present per window. Distinctiveness here = register-level,")
print("    like #28 repetition; the SEQUENCING tests above are the structural ones.)")
print(f"\n[total {time.time()-t0:.1f}s]")
