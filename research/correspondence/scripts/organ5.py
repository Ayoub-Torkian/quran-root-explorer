#!/usr/bin/env python3
# SURA-as-ORGAN battery (relational, scale-free):
# (A) IDENTITY  — distinct function, unique markers ("don't merge heart & stomach")
# (B) CONNECTIVITY — specific partners, not uniform ("heart wires to lungs")
# (C) LOCATION  — position determined by wiring ("can't put heart in the leg")
import collections, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter); order=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    if s not in sur: order.append(s)
    for x in r.split():
        if x and x!='NA': sur[s][x]+=1
suras=order  # canonical order
S=len(suras); idx={s:i for i,s in enumerate(suras)}
df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1

# (A) IDENTITY: unique markers (roots in exactly ONE sura)
uniq=collections.Counter()
for r,d in df.items():
    if d==1:
        for s in suras:
            if r in sur[s]: uniq[s]+=1; break
has=sum(1 for s in suras if uniq[s]>0)
print("(A) IDENTITY — unique 'marker' roots (appear in ONE sura only):")
print(f"   {has}/{S} suras ({has/S:.0%}) carry >=1 unique marker — incl small ones?")
for sx in [108,103,110,112,1,114]:
    print(f"     sura {sx} (verses-roots {sum(sur[sx].values())}): {uniq[sx]} unique markers")

# inter-sura connectivity via shared RARE roots (2<=df<=80)
rare=[r for r,d in df.items() if 2<=d<=80]
M=np.zeros((S,S))
for r in rare:
    holders=[idx[s] for s in suras if r in sur[s]]
    for a in range(len(holders)):
        for b in range(a+1,len(holders)):
            M[holders[a],holders[b]]+=1; M[holders[b],holders[a]]+=1
deg=M.sum(1)
# (B) CONNECTIVITY specificity: is wiring concentrated on few partners (organ) vs uniform?
# Gini-like: top-5 partners' share of each sura's total connectivity
share=[]
for i in range(S):
    w=np.sort(M[i])[::-1]; 
    if w.sum()>0: share.append(w[:5].sum()/w.sum())
share=np.array(share)
print("\n(B) CONNECTIVITY — is each sura wired to SPECIFIC partners?")
print(f"   top-5 partners carry median {np.median(share):.0%} of a sura's connectivity (uniform would be 5/113=4%)")

# (C) LOCATION: are canonical NEIGHBORS a sura's real partners? (position follows wiring)
adj=np.mean([M[i,i+1] for i in range(S-1)])
nulls=[]
for _ in range(300):
    p=np.random.permutation(S); nulls.append(np.mean([M[p[i],p[i+1]] for i in range(S-1)]))
nulls=np.array(nulls); zc=(adj-nulls.mean())/nulls.std()
# is a sura's TOP partner near its canonical position?
near=0
for i in range(S):
    j=int(np.argmax(M[i])) if M[i].max()>0 else -1
    if j>=0 and abs(j-i)<=2: near+=1
print("\n(C) LOCATION — is position set by wiring? ('heart can't go in the leg')")
print(f"   canonical-neighbour connectivity {adj:.2f} vs random-order {nulls.mean():.2f}±{nulls.std():.2f}  z={zc:+.1f}")
print(f"   {near}/{S} suras have their STRONGEST partner within +/-2 positions ({near/S:.0%}; chance ~4/113=4%)")
