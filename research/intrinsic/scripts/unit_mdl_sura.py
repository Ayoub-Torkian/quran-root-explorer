# -*- coding: utf-8 -*-
"""Instrument 1: sūra as MDL-extremal whole-entity. Optimal contiguous K-segmentation (vectorized SSE + DP) with
MDL penalty -> desc_eff=cost/āyah; sūra is 'self-optimal' if desc_eff is a LOCAL MINIMUM vs resize neighbours
([a±1,b],[a,b±1]) — can't grow into the neighbour or truncate without describing LESS efficiently. Fraction
local-min vs random contiguous-span null (NO rearrangement). + rhyme-run tiling (fāṣila). MEASURED."""
import numpy as np, json, statistics as st
from collections import Counter
np.random.seed(17)
d=np.load("/tmp/unit.npz"); VV=d["VV"].astype(np.float64); sura=d["sura"]; n=len(sura)
rh=json.load(open("/tmp/unit_rhyme.json",encoding='utf-8')); rasm=rh["rasm"]
gv=float(((VV-VV.mean(0))**2).sum(1).mean()); GAMMA=0.5*gv; KMAX=4
def desc(lo,hi):
    A=VV[lo:hi]; L=len(A)
    CS=np.zeros((L+1,80)); css=np.zeros(L+1); CS[1:]=np.cumsum(A,0); css[1:]=np.cumsum((A*A).sum(1))
    S=np.full((L+1,L+1),1e18)
    for i in range(L):
        m=np.arange(1,L-i+1); diff=CS[i+1:]-CS[i]; S[i,i+1:]=(css[i+1:]-css[i])-(diff*diff).sum(1)/m
    INF=1e18; dp=[[INF]*(KMAX+1) for _ in range(L+1)]; dp[0][0]=0.0
    for i in range(1,L+1):
        for k in range(1,min(KMAX,i)+1):
            b=INF
            for j in range(k-1,i):
                c=dp[j][k-1]+S[j,i]
                if c<b: b=c
            dp[i][k]=b
    c,K=min((dp[L][k]+GAMMA*k,k) for k in range(1,KMAX+1)); return c/L,K
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def localmin(a,b):
    base,K=desc(a,b); nb=[]
    if a-1>=0: nb.append(desc(a-1,b)[0])
    if b+1<=n: nb.append(desc(a,b+1)[0])
    if b-a>2: nb.append(desc(a+1,b)[0]); nb.append(desc(a,b-1)[0])
    return all(base<=x+1e-9 for x in nb), K
lm=0; tot=0; Ks=[]; kw=None
for s,(a,b) in bounds.items():
    if b-a<4: continue
    ok,K=localmin(a,b); lm+=ok; tot+=1; Ks.append(K)
    if s==108: kw=(ok,K)
realf=lm/tot
lens=[b-a for s,(a,b) in bounds.items() if b-a>=4]
nf=[]
for _ in range(6):
    c=0
    for L in lens:
        a=np.random.randint(1,n-L-1); c+=localmin(a,a+L)[0]
    nf.append(c/len(lens))
print("=== Instrument 1: sūra MDL-extremal whole-entity (no rearrangement) ===")
print(f"suras tested L>=4: {tot} | mean optimal sections K*={st.mean(Ks):.2f} (multi-uniform: %d%% have K>=2)"%int(100*sum(k>=2 for k in Ks)/tot))
print(f"sūras = MDL LOCAL MINIMA (self-optimal size): {realf:.0%} | random-span null {st.mean(nf):.0%}±{st.pstdev(nf):.0%} | z={(realf-st.mean(nf))/(st.pstdev(nf) or 1e-9):+.1f}")
print(f"al-Kawthar (108): local-min={kw[0]} K*={kw[1]}")
covs=[]; nr=[]
for s,(a,b) in bounds.items():
    if b-a<4: continue
    seq=[rasm[i] for i in range(a,b)]; L=len(seq)
    covs.append(Counter(seq).most_common(1)[0][1]/L)
    nr.append((1+sum(seq[i]!=seq[i-1] for i in range(1,L)))/L)
print("=== fāṣila rhyme-run tiling (rasm rawiyy) ===")
print(f"mean dominant-rhyme coverage {st.mean(covs):.2f} | rhyme-runs/āyah {st.mean(nr):.2f}")
print("DONE")
