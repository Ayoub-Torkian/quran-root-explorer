# -*- coding: utf-8 -*-
"""
ILTIFAT — full axis sweep: PERSON + NUMBER + TENSE shift rates, the directional
transition-type profile (esp. the iltifat-ila-l-khitab asymmetry: shifts INTO 2nd
person), and an any-axis composite. Same gate-validated tagger, fixed-N windows,
two unitizations, quoted-speech control.
"""
import re, sys, time
import numpy as np
sys.path.insert(0, "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
sys.path.insert(0, "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/sequence_tests")
import analysis as A
from analysis import COL_DIACRITIZED as DCOL
import iltifat_tagger as T

ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(40); t0 = time.time()
SENT = re.compile(r"[.!?؟؛\n]+"); CLAUSE = re.compile(r"[.،؛:!؟]+")

def units_from(path, splitter, minw=2):
    txt = open(path, encoding="utf-8", errors="ignore").read()
    return [w for w in (T.words(c) for c in splitter.split(txt)) if len(w) >= minw]

def tag_all(units):
    p = [T.tag_person(u)[0] for u in units]
    n = [T.tag_number(u) for u in units]
    te = [T.tag_tense(u) for u in units]
    return p, n, te

def sr(seq, none_vals):
    s = [x for x in seq if x not in none_vals]
    if len(s) < 2: return None
    return sum(1 for i in range(len(s)-1) if s[i] != s[i+1]) / (len(s)-1)

def windows_axis(seq, none_vals, U=40, step=20, maxw=200):
    s = [x for x in seq if x not in none_vals]
    out = []
    for c in range(0, max(1, len(s)-U+1), step):
        seg = s[c:c+U]
        if len(seg) < U*0.8: break
        out.append(sum(1 for i in range(len(seg)-1) if seg[i]!=seg[i+1])/(len(seg)-1))
        if len(out) >= maxw: break
    return np.array(out)

def into2_asym(persons):
    """directional profile of person transitions; returns dict of counts and the
       into-2nd vs out-of-2nd asymmetry (classical iltifat ila l-khitab)."""
    s = [x for x in persons if x]
    trans = {}
    for i in range(len(s)-1):
        if s[i] != s[i+1]:
            trans[(s[i], s[i+1])] = trans.get((s[i], s[i+1]), 0) + 1
    into2 = sum(v for (a, b), v in trans.items() if b == 2)
    outof2 = sum(v for (a, b), v in trans.items() if a == 2)
    tot = sum(trans.values()) or 1
    asym = (into2 - outof2) / tot
    return trans, into2/tot, outof2/tot, asym

def g(a, b):
    if len(a) < 2 or len(b) < 2: return float("nan")
    return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
def boot_p(a, b, R=2000):
    if len(a)==0 or len(b)==0: return float("nan")
    ai=rng.integers(0,len(a),R); bi=rng.integers(0,len(b),R)
    return float(np.mean(a[ai]>b[bi])+0.5*np.mean(a[ai]==b[bi]))

# ---- load
c = A.load_corpus(ROOT+"/Book6.xlsx")
qu = [T.words(c.df.iloc[i][DCOL]) for i in range(len(c.df))]
corpora = {"QURAN": qu}
pu=[]
for f in ("ar_tabari","ar_classical2","ar_novel","ar_news"):
    pu += units_from(ROOT+f"/sequence_tests/corpus/{f}.txt", SENT)
corpora["ord-Arabic"]=pu
corpora["poetry(Mutanabbi)"]=units_from(ROOT+"/sequence_tests/corpus/ar_poetry.txt", re.compile(r"\n+"))
saj=[]
for f in ("ar_sajprose","ar_saj_hariri"):
    saj += units_from(ROOT+f"/sequence_tests/corpus/{f}.txt", CLAUSE)
corpora["saj'(Hamadhani+Hariri)"]=saj

print(f"[{time.time()-t0:.1f}s] ===== AXIS SHIFT RATES (natural units) =====")
print(f"   {'corpus':24s} {'person':>7s} {'number':>7s} {'tense':>7s} | {'into2':>6s} {'out2':>6s} {'asym':>6s}")
dists={}
for nm,(units) in corpora.items():
    p,n,te = tag_all(units)
    rp=sr(p,{0}); rn=sr(n,set()); rt=sr(te,{"?"})
    _,i2,o2,asym = into2_asym(p)
    dists[nm]=dict(p=windows_axis(p,{0}), n=windows_axis(n,set()), t=windows_axis(te,{"?"}))
    print(f"   {nm:24s} {rp:7.3f} {rn:7.3f} {rt:7.3f} | {i2:6.3f} {o2:6.3f} {asym:+6.3f}")

print(f"\n[{time.time()-t0:.1f}s] ===== Qur'an vs baselines, fixed-N=40 windows (Δsd, P) =====")
for ax,lab in [("p","PERSON"),("n","NUMBER"),("t","TENSE")]:
    q=dists["QURAN"][ax]
    print(f"  [{lab}] Qur'an mean={q.mean():.3f} (n={len(q)})")
    for nm in ("ord-Arabic","poetry(Mutanabbi)","saj'(Hamadhani+Hariri)"):
        b=dists[nm][ax]
        print(f"      vs {nm:24s} Δ={g(q,b):+5.2f}sd  P(Q>base)={boot_p(q,b):.2f}")

# directional transition profile detail for Qur'an vs ordinary
print(f"\n[{time.time()-t0:.1f}s] ===== PERSON transition profile (normalized) =====")
for nm in ("QURAN","ord-Arabic","poetry(Mutanabbi)","saj'(Hamadhani+Hariri)"):
    p,_,_ = tag_all(corpora[nm])
    trans,i2,o2,asym = into2_asym(p)
    tot=sum(trans.values()) or 1
    prof={f"{a}->{b}": round(v/tot,3) for (a,b),v in sorted(trans.items())}
    print(f"   {nm:24s} asym(into2-out2)={asym:+.3f}  {prof}")
print(f"\n[total {time.time()-t0:.1f}s]")
