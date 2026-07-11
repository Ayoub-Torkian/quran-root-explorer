# -*- coding: utf-8 -*-
"""Instrument 9: INTERNAL autoregressive seam-likelihood order recovery. Uses the ORDERED root stream (all prior
instruments discarded order). Trains the corpus's own cross-āyah transition statistics — root at end of one āyah
-> root at start of next — i.e. القرآن يفسر بعضه بعضا as a directional sequence law. LEAVE-ONE-SŪRA-OUT (held-out
sūra's own adjacencies removed from the model, so recovery is not circular). Recover each sūra's āyah order by
chaining max seam-likelihood; directed Kendall τ vs canonical. Null: shuffle. MEASURED, rasm/root, divine substrate."""
import numpy as np, statistics as st, openpyxl, math
from collections import defaultdict, Counter
np.random.seed(29)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(str(r[8] or "").split())
n=len(sura)
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def endtok(i):   return roots[i][-1] if roots[i] else None
def starttok(i): return roots[i][0]  if roots[i] else None
# global cross-āyah seam bigram counts (end-root -> start-root) over canonical adjacencies
BI=defaultdict(Counter); START=Counter(); V=set()
adj=[]
for s,(a,b) in bounds.items():
    for k in range(a,b-1):
        e=endtok(k); st0=starttok(k+1)
        if e and st0: BI[e][st0]+=1; START[st0]+=1; V.add(e); V.add(st0); adj.append((s,e,st0))
Vn=len(V)|1
def kendall(a,b):
    L=len(a); ra={v:i for i,v in enumerate(a)}; rb={v:i for i,v in enumerate(b)}; c=di=0
    for i in range(L):
        for j in range(i+1,L):
            sg=(ra[a[i]]-ra[a[j]])*(rb[a[i]]-rb[a[j]])
            c+=sg>0; di+=sg<0
    return (c-di)/(c+di) if (c+di) else 0.0
taus=[]; nulls=[]
for s,(a,b) in bounds.items():
    L=b-a
    if L<4: continue
    # leave-one-out: local copy of counts with this sūra's seams removed
    rem=Counter()
    for k in range(a,b-1):
        e=endtok(k); st0=starttok(k+1)
        if e and st0: rem[(e,st0)]+=1
    def seam(i,j):  # log P(start_j | end_i) add-1 smoothed, LOO
        e=endtok(i); st0=starttok(j)
        if not e or not st0: return math.log(1.0/Vn)
        cnt=BI[e][st0]-rem.get((e,st0),0); tot=sum(BI[e].values())-sum(rem[k] for k in rem if k[0]==e)
        return math.log((cnt+0.5)/(tot+0.5*Vn))
    items=list(range(a,b))
    # greedy chain: pick start = āyah whose start-root is globally most likely a beginner; then maximize seam
    cur0=max(items,key=lambda i:(START[starttok(i)] if starttok(i) else 0)+1e-6*np.random.randn())
    order=[cur0]; rema=[x for x in items if x!=cur0]
    while rema:
        nx=max(rema,key=lambda j: seam(order[-1],j)+1e-6*np.random.randn()); order.append(nx); rema.remove(nx)
    taus.append(kendall(order,items))
    sh=items[:]; np.random.shuffle(sh); nulls.append(kendall(sh,items))
N=len(taus)
print("=== Instrument 9: internal autoregressive seam-likelihood recovery (LOO) ===")
print(f"suras (L>=4): {N} | distinct seam-transition types: {sum(len(v) for v in BI.values())} over vocab {len(V)}")
print(f"  directed τ = {st.mean(taus):+.3f} | median {st.median(taus):+.3f} | {100*sum(t>=0.5 for t in taus)/N:.0f}% τ>=0.5")
print(f"  order-shuffle null τ = {st.mean(nulls):+.3f}")
print(f"  baselines: undirected +0.16 / gradient +0.10 / pairwise -0.00 / rhet-form +0.07")
print("DONE")
