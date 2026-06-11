#!/usr/bin/env python3
# RECONCILE sequence(surface) <-> network(body): does the 1D mushaf order FOLD into a body-like network?
# Like DNA->chromatin: local contacts (decay with sequence distance) + long-range loops.
import collections, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter)
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    if 1<=s<=114:
        for x in r.split():
            if x and x!='NA': sur[s][x]+=1
suras=sorted(sur); S=len(suras); idx={s:i for i,s in enumerate(suras)}
df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1
rare=[r for r,d in df.items() if 2<=d<=60]
M=np.zeros((S,S))
for r in rare:
    h=[idx[s] for s in suras if r in sur[s]]
    for a in range(len(h)):
        for b in range(a+1,len(h)): M[h[a],h[b]]+=1; M[h[b],h[a]]+=1
dg=M.sum(1)+1e-9; A=M/np.sqrt(np.outer(dg,dg)); np.fill_diagonal(A,0)
# (1) FOLDING: association vs sequence distance |i-j|
dist=[]; assoc=[]
for i in range(S):
    for j in range(i+1,S):
        dist.append(j-i); assoc.append(A[i,j])
dist=np.array(dist); assoc=np.array(assoc)
print("RECONCILIATION — does the 1D sequence fold into the network?")
for lo,hi in [(1,1),(2,3),(4,8),(9,20),(21,113)]:
    m=(dist>=lo)&(dist<=hi); print(f"   seq-distance {lo:>3}-{hi:<3}: mean association {assoc[m].mean():.4f}")
from numpy import corrcoef
print(f"   correlation(association, -seq_distance) = {corrcoef(assoc,-dist)[0,1]:+.2f}  (negative slope = LOCAL folding/contact)")
# (2) LONG-RANGE LOOPS: distant-in-sequence but strongly tied (chromatin-loop analog)
thr=np.quantile(assoc,0.95)
loops=[(suras[i],suras[j],A[i,j]) for i in range(S) for j in range(i+1,S) if A[i,j]>=thr and (j-i)>20]
loops.sort(key=lambda x:-x[2])
print(f"   LONG-RANGE loops (top-5% association, seq-distance >20): {len(loops)} contacts; strongest:")
for a,b,v in loops[:6]: print(f"     sura {a} <-> sura {b}  (assoc {v:.3f}, apart {abs(a-b)})")
# (3) the folded network is body-like: communities(organs) + hubs already shown; recap one stat
deg=A.sum(1); print(f"   folded network: degree spread (hub structure) max/median = {deg.max()/np.median(deg):.1f}x  (hubs exist, like organs of high connectivity)")
