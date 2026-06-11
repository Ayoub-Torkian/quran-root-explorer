"""Frequency control for within-verse synergy. Per-triple null (each root
independently circular-shifted -> preserves each root's exact rate+autocorr,
destroys cross-dependence). p per triple, then BH-FDR. Plus frequency
stratification: is synergy concentrated only in high-frequency triples?
"""
from __future__ import annotations
import sys, time, itertools
import numpy as np
from collections import Counter
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx"); K=normalize_letters
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),corpus.df[COL_SURAH].astype(int).to_numpy()))
rt=[[K(t) for t in corpus.root_tokens[i]] for i in order]; nA=len(order)
freq=Counter(r for toks in rt for r in set(toks))
T=[r for r,c in freq.most_common() if c>=100][:16]
B={r:np.zeros(nA,dtype=int) for r in T}
for k,toks in enumerate(rt):
    for r in set(toks):
        if r in B: B[r][k]=1
S=100
shifts={r:[np.roll(B[r],int(rng.integers(50,nA-50))) for _ in range(S)] for r in T}
def I2(x,y):
    n=x.size; p=(np.bincount(x*2+y,minlength=4).astype(float)/n).reshape(2,2)
    px=p.sum(1); py=p.sum(0); nz=p>0
    return float(np.sum(p[nz]*np.log2(p[nz]/np.outer(px,py)[nz])))
def I2c(x,y,z):
    t=0.0; n=x.size
    for zv in (0,1):
        m=z==zv; pz=m.sum()/n
        if pz>0: t+=pz*I2(x[m],y[m])
    return t
def II(x,y,z): return I2c(x,y,z)-I2(x,y)
def bh(p):
    p=np.asarray(p); m=p.size; o=np.argsort(p); q=p[o]*m/np.arange(1,m+1)
    q=np.minimum.accumulate(q[::-1])[::-1]; out=np.empty(m); out[o]=np.clip(q,0,1); return out

obs=[]; ps=[]; ftot=[]; combos=list(itertools.combinations(T,3))
for a,b,c in combos:
    o=II(B[a],B[b],B[c]); obs.append(o)
    nd=np.array([II(shifts[a][k],shifts[b][k],shifts[c][k]) for k in range(S)])
    ps.append((np.sum(nd>=o)+1)/(S+1))                       # one-sided: synergy
    ftot.append(freq[a]+freq[b]+freq[c])
obs=np.array(obs); ps=np.array(ps); ftot=np.array(ftot)
q=bh(ps)
sigF=ps<0.05; sigQ=q<0.10
print(f"[{time.time()-t0:.1f}s] roots={len(T)} triples={len(combos)} per-triple null S={S}")
print(f"  synergy p<0.05 (per-triple, freq-preserving): {sigF.sum()}/{len(combos)} ({100*sigF.mean():.0f}%)")
print(f"  survive BH-FDR q<0.10: {sigQ.sum()}")
# frequency stratification
med=np.median(ftot); lo=ftot<=med; hi=ftot>med
print(f"  frac significant — LOW-freq triples={sigF[lo].mean():.2f}  HIGH-freq triples={sigF[hi].mean():.2f}")
print(f"     (similar => NOT just a high-frequency artifact)")
idx=np.argsort(ps)[:6]
print("  top synergy triples after frequency control:")
for i in idx:
    a,b,c=combos[i]; print(f"    {a}+{b}+{c}: II={obs[i]:+.5f} p={ps[i]:.3g} q={q[i]:.3g}")
print(f"\n[total {time.time()-t0:.1f}s]")
