"""Within-surah rasm letter-sequence structure (Tier-1, divine-attributable).
Does the letter order WITHIN a surah carry structure beyond (a) composition and
(b) order-2 Markov -- with NO cross-surah leakage? Contrast vs the cross-surah
(reading-order) version to see how much earlier 'long-range' was human arrangement.
Run against the go/abort gates.
"""
from __future__ import annotations
import sys, time
import numpy as np
from collections import defaultdict
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx")
su=corpus.df[COL_SURAH].astype(int).to_numpy()
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),su)); su2=su[order]
# per-surah letter arrays (rasm), and full reading-order array
per={}; full=[]
for k,i in enumerate(order):
    s=int(su2[k]); per.setdefault(s,[])
    for t in corpus.seg_tokens[i]:
        for ch in normalize_letters(t):
            if ch.strip(): per[s].append(ch); full.append(ch)
alpha=sorted(set(full)); aidx={c:j for j,c in enumerate(alpha)}; K=len(alpha)
per={s:np.array([aidx[c] for c in v],dtype=np.int64) for s,v in per.items()}
full=np.array([aidx[c] for c in full],dtype=np.int64); N=full.size
H1=-sum((np.bincount(full,minlength=K)/N)[p]*np.log2((np.bincount(full,minlength=K)/N)[p]) for p in range(K) if np.bincount(full,minlength=K)[p]>0)
print(f"[{time.time()-t0:.1f}s] N={N} K={K} surahs={len(per)} H1={H1:.3f}")

def mi_within(arrs,d):
    joint=np.zeros(K*K)
    n=0
    for a in arrs:
        if a.size>d:
            x=a[:-d]; y=a[d:]; joint+=np.bincount(x*K+y,minlength=K*K); n+=x.size
    if n==0: return 0.0
    pj=(joint/n).reshape(K,K); px=pj.sum(1); py=pj.sum(0); nz=pj>0
    return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
def shuffled_within(arrs):
    return [a.copy() for a in (rng.permutation(a) for a in arrs)]
def markov2_segmented(lengths):
    ctx=defaultdict(lambda: np.zeros(K))
    for i in range(2,N): ctx[(full[i-2],full[i-1])][full[i]]+=1
    pr={c:v/v.sum() for c,v in ctx.items()}; bo=np.bincount(full,minlength=K)/N
    out=[]
    for L in lengths:
        s=np.empty(L,dtype=np.int64)
        if L>0: s[0]=rng.integers(K)
        if L>1: s[1]=rng.integers(K)
        for i in range(2,L): s[i]=rng.choice(K,p=pr.get((s[i-2],s[i-1]),bo))
        out.append(s)
    return out

ds=[1,2,3,4,5,6,8,10,13,16,20,25,32,40,50]
arrs=list(per.values()); lengths=[a.size for a in arrs]
real=np.array([mi_within(arrs,d) for d in ds])
shuf=np.zeros(len(ds))
for _ in range(3):
    sh=[rng.permutation(a) for a in arrs]; shuf+=np.array([mi_within(sh,d) for d in ds])
shuf/=3
exc_w=real-shuf
# cross-surah (reading order) for contrast
realc=np.array([mi_within([full],d) for d in ds])
shc=np.zeros(len(ds))
for _ in range(3):
    shc+=np.array([mi_within([rng.permutation(full)],d) for d in ds])
shc/=3
exc_c=realc-shc
# markov-2 within-surah (beyond-order-2 test)
mk=markov2_segmented(lengths)
mkmi=np.array([mi_within(mk,d) for d in ds])
mksh=np.zeros(len(ds))
for _ in range(2):
    mksh+=np.array([mi_within([rng.permutation(a) for a in mk],d) for d in ds])
mksh/=2
exc_mk=mkmi-mksh

mask=np.array(ds)>=5
lr_w=exc_w[mask].clip(min=0).sum(); lr_c=exc_c[mask].clip(min=0).sum(); lr_mk=exc_mk[mask].clip(min=0).sum()
near_w=exc_w[:4].clip(min=0).sum()
print("\n  excess MI (bias-corrected) by distance:")
print(f"  {'d':>4} {'within-surah':>13} {'cross-surah':>12} {'markov2-within':>15}")
for j,d in enumerate(ds):
    if d in (1,2,3,5,10,20,50):
        print(f"  {d:>4} {exc_w[j]:>13.5f} {exc_c[j]:>12.5f} {exc_mk[j]:>15.5f}")
print(f"\n  NEAR (d=1..4) within-surah excess sum = {near_w:.4f}  ({100*near_w/H1:.1f}% of H1)")
print(f"  LONG-RANGE (d>=5): within-surah={lr_w:.5f}  cross-surah={lr_c:.5f}  markov2={lr_mk:.5f}")
print(f"  beyond-Markov LR ratio (within real / markov2) = {lr_w/max(lr_mk,1e-9):.2f}x")
print(f"  LR effect size (within LR / H1) = {100*lr_w/H1:.3f}% of marginal entropy")
print("\n  GATE READ:")
print(f"   G5 effect size: LR {100*lr_w/H1:.3f}% of H1 (floor 1%) -> {'PASS' if 100*lr_w/H1>=1 else 'FAIL'}")
print(f"   G4 confound: within-surah LR vs cross-surah LR = {lr_w:.4f} vs {lr_c:.4f} "
      f"({'survives' if lr_w>0.5*lr_c else 'mostly cross-surah (human arrangement)'})")
print(f"   beyond-Markov: {'PASS (>3x)' if lr_w/max(lr_mk,1e-9)>=3 else 'weak'}")
print(f"\n[total {time.time()-t0:.1f}s]")
