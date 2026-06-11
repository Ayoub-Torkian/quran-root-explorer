# -*- coding: utf-8 -*-
"""Verification: (1) hand-check tagger on canonical iltifat passages;
(2) address-share (fraction of person-shifts involving 2nd person) windowed sd-gaps."""
import re, sys, time
import numpy as np
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/sequence_tests")
import analysis as A
from analysis import COL_DIACRITIZED as DCOL, COL_SURAH as SCOL, COL_AYAH as YCOL
import iltifat_tagger as T
ROOT="/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng=np.random.default_rng(7); t0=time.time()
SENT=re.compile(r"[.!?؟؛\n]+"); CLAUSE=re.compile(r"[.،؛:!؟]+")
def units_from(path,sp,minw=2):
    txt=open(path,encoding="utf-8",errors="ignore").read()
    return [w for w in (T.words(c) for c in sp.split(txt)) if len(w)>=minw]

c=A.load_corpus(ROOT+"/Book6.xlsx")

# (1) hand-check: Surah 1 (Fatiha) should read 3rd person (v2-4) then 2nd (v5-7)
print(f"[{time.time()-t0:.1f}s] === HAND-CHECK: tagger person per ayah ===")
def show(si):
    for i in range(len(c.df)):
        r=c.df.iloc[i]
        if int(r[SCOL])==si:
            p,sc=T.tag_person(T.words(r[DCOL]))
            print(f"   {si}:{int(r[YCOL])}  person={p}  {dict((k,round(v,1)) for k,v in sc.items())}  | {r[DCOL][:50]}")
show(1)
print("   expect: 1:2-4 -> 3 (about God) ; 1:5-7 -> 2 (direct address). A 3->2 iltifat at v4->v5.")

# (2) address-share windowed
def persons(units): return [T.tag_person(u)[0] for u in units]
def addr_share_windows(p, U=60, step=30, maxw=200):
    s=[x for x in p if x]; out=[]
    for cc in range(0,max(1,len(s)-U+1),step):
        seg=s[cc:cc+U]
        if len(seg)<U*0.8: break
        sh=[(seg[i],seg[i+1]) for i in range(len(seg)-1) if seg[i]!=seg[i+1]]
        if not sh: continue
        inv2=sum(1 for a,b in sh if a==2 or b==2)/len(sh)
        out.append(inv2)
        if len(out)>=maxw: break
    return np.array(out)
def g(a,b):
    if len(a)<2 or len(b)<2: return float("nan")
    return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
def boot_p(a,b,R=2000):
    ai=rng.integers(0,len(a),R); bi=rng.integers(0,len(b),R)
    return float(np.mean(a[ai]>b[bi])+0.5*np.mean(a[ai]==b[bi]))

corp={"QURAN":[T.words(c.df.iloc[i][DCOL]) for i in range(len(c.df))]}
pu=[]
for f in ("ar_tabari","ar_classical2","ar_novel","ar_news"): pu+=units_from(ROOT+f"/sequence_tests/corpus/{f}.txt",SENT)
corp["ord-Arabic"]=pu
corp["poetry(Mutanabbi)"]=units_from(ROOT+"/sequence_tests/corpus/ar_poetry.txt",re.compile(r"\n+"))
sj=[]
for f in ("ar_sajprose","ar_saj_hariri"): sj+=units_from(ROOT+f"/sequence_tests/corpus/{f}.txt",CLAUSE)
corp["saj'(Hamadhani+Hariri)"]=sj

print(f"\n[{time.time()-t0:.1f}s] === ADDRESS-SHARE (fraction of person-shifts involving 2nd person) ===")
d={nm:addr_share_windows(persons(u)) for nm,u in corp.items()}
q=d["QURAN"]
print(f"   QURAN mean={q.mean():.3f} (n={len(q)} windows)")
for nm in ("ord-Arabic","poetry(Mutanabbi)","saj'(Hamadhani+Hariri)"):
    b=d[nm]
    print(f"     vs {nm:24s} mean={b.mean():.3f}  Δ={g(q,b):+5.2f}sd  P(Q>base)={boot_p(q,b):.2f}")
print(f"\n[total {time.time()-t0:.1f}s]")
