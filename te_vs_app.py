"""Does transfer entropy add anything over the app's existing measures?
Compare, per root pair, on real ayah-level signals:
  - SYMMETRIC co-location: mutual information I(X;Y) at same position (= what
    cooccurrence/PMI/overlap capture, symmetric).
  - DIRECTIONAL lead-lag (app's directed_lead_lag_graph idea): P(Y at t+-1 | X) asym.
  - TRANSFER ENTROPY asym: TE(X->Y)-TE(Y->X), which conditions on Y's OWN past.
Key questions: is TE-asym just symmetric co-location? is it just the lead-lag?
"""
from __future__ import annotations
import sys, time, itertools
import numpy as np
from collections import Counter
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
t0=time.time(); corpus=A.load_corpus("Book6.xlsx"); K=normalize_letters
su=corpus.df[COL_SURAH].astype(int).to_numpy()
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),su))
rt=[[K(t) for t in corpus.root_tokens[i]] for i in order]; nA=len(order)
freq=Counter(r for toks in rt for r in set(toks))
T=[r for r,c in freq.items() if c>=80][:12]
B={r:np.zeros(nA) for r in T}
for k,toks in enumerate(rt):
    for r in set(toks):
        if r in B: B[r][k]=1
def symMI(x,y):
    n=x.size; xi=x.astype(int); yi=y.astype(int)
    p=(np.bincount(xi*2+yi,minlength=4).astype(float)/n).reshape(2,2)
    px=p.sum(1); py=p.sum(0); nz=p>0
    return float(np.sum(p[nz]*np.log2(p[nz]/np.outer(px,py)[nz])))
def leadlag(x,y):  # P(Y present at t-1 or t+1 | X at t)
    idx=np.where(x>0)[0]; hit=0
    for i in idx:
        if (i>0 and y[i-1]>0) or (i<nA-1 and y[i+1]>0): hit+=1
    return hit/max(len(idx),1)
def TE(x,y):  # x->y
    yn=y[1:].astype(int); yt=y[:-1].astype(int); xt=x[:-1].astype(int)
    p=(np.bincount(yn*4+yt*2+xt,minlength=8).astype(float)+1e-9); p/=p.sum(); p=p.reshape(2,2,2)
    te=0.0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                pj=p[a,b,c]; den=p[a,b,:].sum()*p[:,b,c].sum()
                if pj>0 and den>0: te+=pj*np.log2(pj*p[:,b,:].sum()/den)
    return te
sym=[]; ll_asym=[]; te_asym=[]; pairs=[]
for a,b in itertools.combinations(T,2):
    x,y=B[a],B[b]
    sym.append(symMI(x,y))
    ll_asym.append(leadlag(x,y)-leadlag(y,x))
    te_asym.append(TE(x,y)-TE(y,x))
    pairs.append((a,b))
sym=np.array(sym); ll_asym=np.array(ll_asym); te_asym=np.array(te_asym)
def cc(a,b): return float(np.corrcoef(a,b)[0,1])
print(f"[{time.time()-t0:.1f}s] pairs={len(pairs)} (roots freq>=80, top 12)")
print(f"  corr( symmetric co-location , |TE asym| )   = {cc(sym,np.abs(te_asym)):+.3f}")
print(f"     -> near 0 means TE-asymmetry is NOT explained by symmetric co-location")
print(f"  corr( lead-lag asym , TE asym )             = {cc(ll_asym,te_asym):+.3f}")
print(f"     -> how much TE just reproduces the app's existing directional measure")
# do they rank pairs differently?
oll=set(np.argsort(-np.abs(ll_asym))[:5]); ote=set(np.argsort(-np.abs(te_asym))[:5])
print(f"  top-5 directional pairs overlap (lead-lag vs TE): {len(oll&ote)}/5")
print("\n  example pairs where TE and lead-lag DISAGREE on direction:")
shown=0
for i in range(len(pairs)):
    if np.sign(ll_asym[i])!=np.sign(te_asym[i]) and abs(te_asym[i])>1e-4 and shown<4:
        print(f"    {pairs[i][0]}~{pairs[i][1]}: lead-lag={ll_asym[i]:+.3f}  TE-asym={te_asym[i]:+.5f}")
        shown+=1
print(f"\n[total {time.time()-t0:.1f}s]")
