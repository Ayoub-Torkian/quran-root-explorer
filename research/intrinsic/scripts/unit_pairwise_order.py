# -*- coding: utf-8 -*-
"""Instrument 6: PAIRWISE directed recovery (what a per-āyah gradient can't capture). Build a directed precedence
graph per sūra from sequential-dependency votes, recover order by net-flow (row-sum) sort with jittered ties,
score directed Kendall τ vs canonical. CLEAN null = τ of random orders (~0) and direction-shuffled-edges.
Votes (content/rasm only): (A) reuse-flow: shared roots & the āyah adding MORE unshared roots tends later;
(B) specificity-increase: rarer-root āyāt tend later (given->new). MEASURED — honest test of the directed hypothesis."""
import numpy as np, statistics as st, openpyxl
from collections import Counter
np.random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(str(r[8] or "").split())
n=len(sura); df=Counter()
for rr in roots:
    for x in set(rr): df[x]+=1
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def kendall(a,b):
    L=len(a); ra={v:i for i,v in enumerate(a)}; rb={v:i for i,v in enumerate(b)}; c=di=0
    for i in range(L):
        for j in range(i+1,L):
            sgn=(ra[a[i]]-ra[a[j]])*(rb[a[i]]-rb[a[j]])
            if sgn>0:c+=1
            elif sgn<0:di+=1
    return (c-di)/(c+di) if (c+di) else 0.0
def recover(s):
    a,b=bounds[s]; L=b-a; sets=[set(roots[a+k]) for k in range(L)]
    rare=[np.mean([df[x]<=3 for x in roots[a+k]]) if roots[a+k] else 0 for k in range(L)]
    A=np.zeros((L,L))  # A[i,j]=vote i before j
    for x in range(L):
        for yk in range(L):
            if x==yk: continue
            sh=sets[x]&sets[yk]
            if sh:
                ux=len(sets[x]-sets[yk]); uy=len(sets[yk]-sets[x])
                A[x,yk]+= (uy-ux)/max(1,ux+uy)        # reuse-flow: more-adding later
            A[x,yk]+= 0.5*np.sign(rare[yk]-rare[x])    # specificity-increase
    net=A.sum(1)-A.sum(0)                              # net "precedes" flow
    order=list(np.argsort(net+1e-6*np.random.randn(L)))
    can=list(range(L))
    # null: direction-shuffled edges
    As=A*np.random.choice([-1,1],size=A.shape); nets=As.sum(1)-As.sum(0)
    onull=list(np.argsort(nets+1e-6*np.random.randn(L)))
    return kendall(order,can), kendall(onull,can)
taus=[]; nulls=[]
for s,(a,b) in bounds.items():
    if b-a<4: continue
    t,nl=recover(s); taus.append(t); nulls.append(nl)
N=len(taus)
print("=== Instrument 6: pairwise directed sequential recovery ===")
print(f"suras (L>=4): {N}")
print(f"  directed τ (net-flow) = {st.mean(taus):+.3f} | median {st.median(taus):+.3f} | {100*sum(t>=0.5 for t in taus)/N:.0f}% τ>=0.5")
print(f"  direction-shuffled-edges null τ = {st.mean(nulls):+.3f}  | random-order τ ≈ 0")
print(f"  baselines: undirected seriation +0.16 ; directed per-āyah gradient +0.10")
print("DONE")
