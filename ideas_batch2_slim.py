"""IDEAS SWEEP batch 2/2 (slim) — ideas 6-10, reduced params for time."""
from __future__ import annotations
import sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx")
K=normalize_letters
su=corpus.df[COL_SURAH].astype(int).to_numpy()
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),su)); su=su[order]
rt=[[K(t) for t in corpus.root_tokens[i]] for i in order]
nA=len(order); freq=Counter(r for toks in rt for r in set(toks)); res={}
def dfa(x):
    x=x-x.mean(); y=np.cumsum(x)
    sc=np.unique(np.logspace(np.log10(16),np.log10(len(x)//8),12).astype(int)); F=[]
    for s in sc:
        ns=len(y)//s
        if ns<1: continue
        g=y[:ns*s].reshape(ns,s); t=np.arange(s)
        c=np.linalg.lstsq(np.vstack([t,np.ones(s)]).T,g.T,rcond=None)[0]
        fit=(c[0][:,None]*t+c[1][:,None]); F.append(np.sqrt(np.mean((g-fit)**2)))
    F=np.array(F); sc=sc[:len(F)]
    return float(np.polyfit(np.log(sc),np.log(F),1)[0])

# 6 per-root occurrence DFA (theme memory)
tops=[r for r,c in freq.items() if c>=120]
sig={r:np.zeros(nA) for r in tops}
for k,toks in enumerate(rt):
    for r in set(toks):
        if r in sig: sig[r][k]=1
al=[dfa(sig[r]) for r in tops]
sh=[dfa(rng.permutation(sig[tops[0]])) for _ in range(6)]
res["6 per-root occurrence DFA (theme memory)"]=(f"median alpha={np.median(al):.3f}",f"shuffled~{np.mean(sh):.3f} n={len(tops)}")

# 7 Heaps + new-root burstiness
seen=set(); V=[]
for toks in rt:
    for r in toks:
        if r not in seen: seen.add(r)
    V.append(len(seen))
V=np.array(V); n=np.arange(1,nA+1)
beta=float(np.polyfit(np.log(n[10:]),np.log(V[10:]),1)[0])
flat=np.array([r for toks in rt for r in toks],dtype=object)
def nv(stream):
    s=set(); out=[]; b=0
    for i,r in enumerate(stream):
        if r not in s: s.add(r); b+=1
        if (i+1)%500==0: out.append(b); b=0
    return np.var(out)
v_real=nv(flat); v_sh=np.mean([nv(flat[rng.permutation(len(flat))]) for _ in range(3)])
res["7 Heaps vocab-growth exponent"]=(f"beta={beta:.3f}",f"new-root var real={v_real:.0f} shuf={v_sh:.0f}")

# 8 transfer-entropy directional asymmetry (8 roots)
T=[r for r,c in freq.items() if c>=80][:8]
B={}
for r in T:
    B[r]=sig[r] if r in sig else np.array([1.0 if r in set(toks) else 0.0 for toks in rt])
def TE(x,y):
    yn=y[1:].astype(int); yt=y[:-1].astype(int); xt=x[:-1].astype(int)
    p=(np.bincount(yn*4+yt*2+xt,minlength=8).astype(float)+1e-9); p/=p.sum(); p=p.reshape(2,2,2)
    te=0.0
    for a in range(2):
        for b in range(2):
            for c in range(2):
                pj=p[a,b,c]; den=p[a,b,:].sum()*p[:,b,c].sum()
                if pj>0 and den>0: te+=pj*np.log2(pj*p[:,b,:].sum()/den)
    return te
sigp=0; tested=0
for i in range(len(T)):
    for j in range(i+1,len(T)):
        x=B[T[i]]; y=B[T[j]]; d=abs(TE(x,y)-TE(y,x)); tested+=1
        nl=[abs(TE(np.roll(x,rng.integers(50,nA-50)),y)-TE(y,np.roll(x,rng.integers(50,nA-50)))) for _ in range(20)]
        if d>np.percentile(nl,95): sigp+=1
res["8 directional flow (transfer-entropy asym)"]=(f"{sigp}/{tested} pairs significant","shift null p<.05")

# 9 root->surah localization MI
import pandas as pd
rfl=[]; sfl=[]
for k,toks in enumerate(rt):
    for r in set(toks): rfl.append(r); sfl.append(su[k])
rf=np.array(pd.factorize(rfl)[0]); sf=np.array(pd.factorize(sfl)[0])
def MI(a,b):
    Kb=b.max()+1; nn=a.size
    pj=(np.bincount(a*Kb+b,minlength=(a.max()+1)*Kb).astype(float)/nn).reshape(a.max()+1,Kb)
    pa=pj.sum(1); pb=pj.sum(0); nz=pj>0
    return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(pa,pb)[nz])))
mr=MI(rf,sf); ms=np.mean([MI(rf,rng.permutation(sf)) for _ in range(6)])
res["9 root->surah localization (MI)"]=(f"MI={mr:.3f} shuffled={ms:.3f}",f"excess={mr-ms:.3f} bits")

# 10 revelation-order vs lexical richness
from scipy.stats import spearmanr
rev=corpus.rev_order_of_surah; tmp={}
for k,toks in enumerate(rt): tmp.setdefault(int(su[k]),[]).extend(toks)
S=[s for s in tmp if s in {int(x) for x in rev}]
x=[rev[s] for s in S]; y=[len(set(tmp[s]))/max(len(tmp[s]),1) for s in S]
rho,p=spearmanr(x,y)
res["10 revelation-order vs lexical richness"]=(f"rho={rho:.3f}",f"p={p:.4g} n={len(S)}")

print(f"[{time.time()-t0:.1f}s]")
print(f"{'idea':<46}{'result':<40}{'null/effect'}")
print("-"*112)
for k,(a,b) in res.items(): print(f"{k:<46}{a:<40}{b}")
print(f"[total {time.time()-t0:.1f}s]")
