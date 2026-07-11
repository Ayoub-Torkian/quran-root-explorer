# -*- coding: utf-8 -*-
"""Instrument 2: ĀYAH sequence-necessity. If several consecutive āyāt form ONE entity (a coherent block), the
canonical ORDER is necessary. Tests within each sūra, vs PERMUTATION-of-order null (the random shuffle is the
yardstick, never a proposed reordering):
 (a) adjacent cohesion = mean cos(v_i,v_{i+1}) — do neighbours bind?
 (b) block-segmentability = optimal few-block desc-cost/āyah — does the GIVEN order cut into coherent multi-āyah
     blocks better than shuffled orders? (the direct 'several āyāt = one entity' test)
 (c) rhyme adjacency = share of adjacent pairs with same fāṣila (rasm rawiyy) vs shuffled.
MEASURED. No content change; only the order is permuted to build the null."""
import numpy as np, json, statistics as st
from collections import Counter
np.random.seed(23)
d=np.load("/tmp/unit.npz"); VV=d["VV"].astype(np.float64); sura=d["sura"]; n=len(sura)
rh=json.load(open("/tmp/unit_rhyme.json",encoding='utf-8')); rasm=rh["rasm"]
gv=float(((VV-VV.mean(0))**2).sum(1).mean()); GAMMA=0.5*gv; KMAX=4
Vn=VV/ (np.linalg.norm(VV,axis=1,keepdims=True)+1e-12)
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def adjcoh(idx): return float(np.mean([Vn[idx[i]]@Vn[idx[i+1]] for i in range(len(idx)-1)]))
def descord(idx):
    A=VV[idx]; L=len(A); CS=np.zeros((L+1,80)); css=np.zeros(L+1)
    CS[1:]=np.cumsum(A,0); css[1:]=np.cumsum((A*A).sum(1)); S=np.full((L+1,L+1),1e18)
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
    return min(dp[L][k]+GAMMA*k for k in range(1,KMAX+1))/L
def rhyadj(idx): return float(np.mean([rasm[idx[i]]==rasm[idx[i+1]] for i in range(len(idx)-1)]))
za=[]; zr=[]; P=400
zb=[]; PB=60
for s,(a,b) in bounds.items():
    L=b-a
    if L<4: continue
    idx=list(range(a,b))
    c0=adjcoh(idx); r0=rhyadj(idx)
    cs=[]; rs=[]
    for _ in range(P):
        p=idx[:]; np.random.shuffle(p); cs.append(adjcoh(p)); rs.append(rhyadj(p))
    za.append((c0-st.mean(cs))/(st.pstdev(cs) or 1e-9)); zr.append((r0-st.mean(rs))/(st.pstdev(rs) or 1e-9))
    if L<=90:
        b0=descord(idx); bs=[]
        for _ in range(PB):
            p=idx[:]; np.random.shuffle(p); bs.append(descord(p))
        zb.append((st.mean(bs)-b0)/(st.pstdev(bs) or 1e-9))  # lower cost = better; positive z = canonical better
N=len(za)
def stouffer(z): return sum(z)/math.sqrt(len(z))
import math
print("=== Instrument 2: āyah sequence-necessity (permutation-of-order null) ===")
print(f"suras (L>=4): {N}")
print(f"(a) adjacent cohesion: mean z=+{st.mean(za):.1f} | %d%% of suras z>2 | Stouffer Z=+{stouffer(za):.0f}"%int(100*sum(z>2 for z in za)/N))
print(f"(b) block-segmentability (L<=90, {len(zb)} suras): mean z=+{st.mean(zb):.1f} | %d%% z>2 | Stouffer Z=+{stouffer(zb):.0f}"%int(100*sum(z>2 for z in zb)/len(zb)))
print(f"(c) rhyme(fāṣila) adjacency: mean z=+{st.mean(zr):.1f} | %d%% z>2 | Stouffer Z=+{stouffer(zr):.0f}"%int(100*sum(z>2 for z in zr)/N))
# al-Kawthar exact (L=3, 6 perms)
import itertools
a,b=bounds[108]; idx=list(range(a,b)); perms=list(itertools.permutations(idx))
c0=adjcoh(idx); cc=[adjcoh(list(p)) for p in perms]
print(f"al-Kawthar(108) L=3: canonical adj-cohesion {c0:.3f}, rank {sorted(cc,reverse=True).index(c0)+1}/6 among orderings")
print("DONE")
