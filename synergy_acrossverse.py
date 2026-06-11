"""Across-verse (surah-level) synergy — the latent-motif domain. Root present in
a surah = binary over 114 surahs. II per triple vs per-triple permutation null
(independent shuffle of each root's surah vector), then BH-FDR.
"""
from __future__ import annotations
import sys, time, itertools
import numpy as np
from collections import Counter
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx"); K=normalize_letters
su=corpus.df[COL_SURAH].astype(int).to_numpy()
rt=[[K(t) for t in corpus.root_tokens[i]] for i in range(len(corpus.df))]
freq=Counter(r for toks in rt for r in set(toks))
sl=sorted(set(su.tolist())); si={s:i for i,s in enumerate(sl)}; nS=len(sl)
T=[r for r,c in freq.most_common() if c>=100][:16]
P={r:np.zeros(nS,dtype=int) for r in T}
for i,toks in enumerate(rt):
    s=si[int(su[i])]
    for r in set(toks):
        if r in P: P[r][s]=1
def I2(x,y):
    n=x.size; p=(np.bincount(x*2+y,minlength=4).astype(float)/n).reshape(2,2)
    px=p.sum(1); py=p.sum(0); nz=p>0
    return float(np.sum(p[nz]*np.log2(p[nz]/np.outer(px,py)[nz])))
def I2c(x,y,z):
    t=0.0;n=x.size
    for zv in (0,1):
        m=z==zv; pz=m.sum()/n
        if pz>0: t+=pz*I2(x[m],y[m])
    return t
def II(x,y,z): return I2c(x,y,z)-I2(x,y)
def bh(p):
    p=np.asarray(p); m=p.size; o=np.argsort(p); q=p[o]*m/np.arange(1,m+1)
    q=np.minimum.accumulate(q[::-1])[::-1]; out=np.empty(m); out[o]=np.clip(q,0,1); return out
S=300
perms={r:[P[r][rng.permutation(nS)] for _ in range(S)] for r in T}
obs=[];ps=[];combos=list(itertools.combinations(T,3))
for a,b,c in combos:
    o=II(P[a],P[b],P[c]); obs.append(o)
    nd=np.array([II(perms[a][k],perms[b][k],perms[c][k]) for k in range(S)])
    ps.append((np.sum(nd>=o)+1)/(S+1))
obs=np.array(obs); ps=np.array(ps); q=bh(ps)
print(f"[{time.time()-t0:.1f}s] surah-level (nS={nS}) roots={len(T)} triples={len(combos)}")
print(f"  synergy p<0.05: {(ps<0.05).sum()}/{len(combos)} ({100*(ps<0.05).mean():.0f}%)  (5% = chance)")
print(f"  survive BH-FDR q<0.10: {(q<0.10).sum()}")
idx=np.argsort(ps)[:6]
for i in idx:
    a,b,c=combos[i]; print(f"    {a}+{b}+{c}: II={obs[i]:+.4f} p={ps[i]:.3g} q={q[i]:.3g}")
print(f"\n[total {time.time()-t0:.1f}s]")
