"""HIGHER-ORDER SYNERGY — interaction information on root TRIPLES, real data.
Pairwise PMI/co-occurrence cannot see 3-way structure. Co-information:
  II(X;Y;Z) = I(X;Y|Z) - I(X;Y)
  II < 0  -> REDUNDANCY (the three share overlapping info; pairwise already saw it)
  II > 0  -> SYNERGY   (the trio carries info NO pair does -> genuinely latent)
Null: independent circular shifts of each signal (kills cross-dependence, keeps
rate+autocorrelation). A real 3-way effect must beat it.
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
T=[r for r,c in freq.most_common() if c>=100][:24]
B={r:np.zeros(nA,dtype=int) for r in T}
for k,toks in enumerate(rt):
    for r in set(toks):
        if r in B: B[r][k]=1

def I2(x,y):
    n=x.size; p=(np.bincount(x*2+y,minlength=4).astype(float)/n).reshape(2,2)
    px=p.sum(1); py=p.sum(0); nz=p>0
    return float(np.sum(p[nz]*np.log2(p[nz]/np.outer(px,py)[nz])))
def I2_cond(x,y,z):  # I(X;Y|Z)
    tot=0.0; n=x.size
    for zv in (0,1):
        m=z==zv; pz=m.sum()/n
        if pz<=0: continue
        tot+=pz*I2(x[m],y[m])
    return tot
def II(x,y,z): return I2_cond(x,y,z)-I2(x,y)

# null threshold for |II| under independence (shifted signals)
def shifted(v): return np.roll(v, int(rng.integers(50,nA-50)))
nulls=[]
keys=list(T)
for _ in range(3000):
    a,b,c=[B[keys[i]] for i in rng.choice(len(keys),3,replace=False)]
    nulls.append(II(shifted(a),shifted(b),shifted(c)))
nulls=np.array(nulls); thr=np.percentile(np.abs(nulls),95)

vals=[]; syn=0; red=0; sig=0; tot=0
for a,b,c in itertools.combinations(T,3):
    v=II(B[a],B[b],B[c]); vals.append(v); tot+=1
    if abs(v)>thr:
        sig+=1
        if v>0: syn+=1
        else: red+=1
vals=np.array(vals)
print(f"[{time.time()-t0:.1f}s] roots={len(T)} triples={tot}")
print(f"  null |II| 95th pct threshold = {thr:.5f} bits")
print(f"  triples beyond null: {sig}/{tot} ({100*sig/tot:.0f}%)")
print(f"    of those: SYNERGY (II>0) = {syn} ; REDUNDANCY (II<0) = {red}")
print(f"  II distribution: mean={vals.mean():+.5f} min={vals.min():+.5f} max={vals.max():+.5f}")
# show a few strongest synergistic triples (the genuinely-latent ones)
idx=np.argsort(-vals)[:5]
combos=list(itertools.combinations(T,3))
print("  strongest SYNERGY triples (info no pair carries):")
for i in idx:
    a,b,c=combos[i]; print(f"    {a} + {b} + {c}: II=+{vals[i]:.5f}")
print(f"\n[total {time.time()-t0:.1f}s]")
