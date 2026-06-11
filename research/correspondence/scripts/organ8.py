#!/usr/bin/env python3
# More body<->sura correspondences: circulation, integration, pairing, vasculature hubs, scaling.
import collections, random
import numpy as np
random.seed(1)
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
# CIRCULATION: do high-freq roots perfuse ALL suras (the blood/vasculature)?
top=[r for r,_ in df.most_common(8)]
print("CIRCULATION — top roots present in % of suras (the shared 'blood supply'):")
for r in top:
    pct=sum(1 for s in suras if r in sur[s])/S
    print(f"   {r:5s}: in {pct:.0%} of suras (df={df[r]} verses)")
# INTEGRATION: rare-root sura graph — one connected body?
rare=[r for r,d in df.items() if 2<=d<=60]
adjset=collections.defaultdict(set)
for r in rare:
    h=[s for s in suras if r in sur[s]]
    for a in h:
        for b in h:
            if a!=b: adjset[a].add(b)
# BFS connected component
seen={suras[0]}; st=[suras[0]]
while st:
    u=st.pop()
    for v in adjset[u]:
        if v not in seen: seen.add(v); st.append(v)
deg=np.mean([len(adjset[s]) for s in suras])
print(f"\nINTEGRATION — rare-root graph: {len(seen)}/{S} suras in ONE connected body; mean partners/sura={deg:.0f}")
# PAIRING (bilateral): does each sura have a STRONG partner?
M=np.zeros((S,S))
for r in rare:
    h=[idx[s] for s in suras if r in sur[s]]
    for a in range(len(h)):
        for b in range(a+1,len(h)): M[h[a],h[b]]+=1; M[h[b],h[a]]+=1
dg=M.sum(1)+1e-9; A=M/np.sqrt(np.outer(dg,dg))
allv=A[np.triu_indices(S,1)]; thr=np.quantile(allv,0.90)
haspair=sum(1 for i in range(S) if A[i].max()>thr)
print(f"PAIRING — {haspair}/{S} suras ({haspair/S:.0%}) have >=1 strong partner (assoc in top 10% of all pairs)")
# SCALING (allometry): sura sizes power-law-ish?
sizes=np.array([sum(sur[s].values()) for s in suras])
print(f"SCALING — sura sizes span {sizes.min()}–{sizes.max()} root-tokens ({sizes.max()/sizes.min():.0f}x); scale-free family (L05)")
