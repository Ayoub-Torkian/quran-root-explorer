# -*- coding: utf-8 -*-
"""
WAZN (8th modality) — morphological-template distribution.
Does the Qur'an's distribution over derivational templates (verb-form / participle
patterns) differ from ordinary Arabic, poetry, saj' beyond register noise?

Metric: per fixed-N word window, the wazn histogram; (a) JS-divergence from the
global ordinary-Arabic histogram, (b) per-bucket rate sd-gaps. Gate-first.
Positive-control: does poetry (Mutanabbi) itself diverge from ordinary?
"""
import re, sys, time
import numpy as np
sys.path.insert(0, "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
sys.path.insert(0, "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/sequence_tests")
import analysis as A
from analysis import COL_DIACRITIZED as D
import wazn_tagger as W
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(41); t0 = time.time()
SENT = re.compile(r"[.!?؟؛\n]+")

def js(p, q):
    p = np.asarray(p) + 1e-12; q = np.asarray(q) + 1e-12
    p /= p.sum(); q /= q.sum(); m = 0.5 * (p + q)
    def kl(a, b): return float(np.sum(a * np.log2(a / b)))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)

def hist_vec(word_list):
    h = W.hist(word_list)
    return np.array([h[b] for b in W.BUCKETS])

def fileW(p):
    return W.words(open(p, encoding="utf-8", errors="ignore").read())

def windows_js(words, ref, U=300, step=150, maxw=200):
    out = []
    for c in range(0, max(1, len(words) - U + 1), step):
        seg = words[c:c + U]
        if len(seg) < U * 0.8: break
        out.append(js(hist_vec(seg), ref))
        if len(out) >= maxw: break
    return np.array(out)

def windows_bucket(words, bi, U=300, step=150, maxw=200):
    out = []
    for c in range(0, max(1, len(words) - U + 1), step):
        seg = words[c:c + U]
        if len(seg) < U * 0.8: break
        out.append(hist_vec(seg)[bi])
        if len(out) >= maxw: break
    return np.array(out)

def g(a, b):
    if len(a) < 2 or len(b) < 2: return float("nan")
    return (a.mean() - b.mean()) / (np.sqrt((a.var() + b.var()) / 2) + 1e-9)
def boot_p(a, b, R=2000):
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5 * np.mean(a[ai] == b[bi]))

# ---------- load ----------
c = A.load_corpus(ROOT + "/Book6.xlsx")
qw = [w for i in range(len(c.df)) for w in W.words(c.df.iloc[i][D])]
ordw = []
for f in ("ar_tabari", "ar_classical2", "ar_novel", "ar_news"):
    ordw += fileW(ROOT + f"/sequence_tests/corpus/{f}.txt")
poet = fileW(ROOT + "/sequence_tests/corpus/ar_poetry.txt")
saj = fileW(ROOT + "/sequence_tests/corpus/ar_sajprose.txt") + fileW(ROOT + "/sequence_tests/corpus/ar_saj_hariri.txt")
corp = {"QURAN": qw, "ord-Arabic": ordw, "poetry(Mutanabbi)": poet, "saj'(Ham+Har)": saj}
ref = hist_vec(ordw)   # ordinary-Arabic reference distribution

# ---------- GATE ----------
print(f"[{time.time()-t0:.1f}s] ===== GATE (wazn JS-divergence detector) =====")
# planted: window where every word is a clear MU-participle form -> far from ordinary
planted = ["مفعول"] * 300
nullsamp = list(rng.choice(ordw, 300))          # drawn from ordinary itself
print(f"   planted(all-MU)  JS-from-ord = {js(hist_vec(planted), ref):.3f}  (expect HIGH)")
print(f"   null(ord sample) JS-from-ord = {js(hist_vec(nullsamp), ref):.3f}  (expect ~0)")
print("   --- degradation ladder (planted -> ordinary mix) ---")
for frac in (0.0, 0.25, 0.5, 0.75, 1.0):
    k = int(frac * 300)
    mix = planted[:300 - k] + list(rng.choice(ordw, k))
    print(f"     ord-fraction={frac:.2f}  JS-from-ord = {js(hist_vec(mix), ref):.3f}")

# ---------- positive control + cross-corpus ----------
print(f"\n[{time.time()-t0:.1f}s] ===== JS-from-ordinary, fixed-N=300-word windows =====")
djs = {nm: windows_js(w, ref) for nm, w in corp.items()}
base = djs["ord-Arabic"]
print(f"   {'corpus':20s} {'meanJS':>7s} {'nwin':>4s}  vs-ord(Δsd, P)")
for nm in corp:
    d = djs[nm]
    extra = "" if nm == "ord-Arabic" else f"  Δ={g(d,base):+5.2f}sd  P(>ord)={boot_p(d,base):.2f}"
    print(f"   {nm:20s} {d.mean():7.3f} {len(d):4d}{extra}")
print("   (positive-control read: poetry's Δ vs ord = is wazn mastery-bearing at all?)")

# ---------- per-bucket sd-gaps Qur'an vs ordinary ----------
print(f"\n[{time.time()-t0:.1f}s] ===== per-bucket rate, Qur'an vs ordinary (fixed-N=300) =====")
print(f"   {'bucket':6s} {'Quran':>7s} {'ord':>7s} {'poetry':>7s} {'saj':>7s} | {'Q-vs-ord':>9s} {'P':>5s}")
for bi, b in enumerate(W.BUCKETS):
    qv = windows_bucket(qw, bi); ov = windows_bucket(ordw, bi)
    pv = windows_bucket(poet, bi); sv = windows_bucket(saj, bi)
    print(f"   {b:6s} {qv.mean():7.3f} {ov.mean():7.3f} {pv.mean():7.3f} {sv.mean():7.3f} | "
          f"{g(qv,ov):+9.2f} {boot_p(qv,ov):5.2f}")
print(f"\n[total {time.time()-t0:.1f}s]")
