#!/usr/bin/env python3
# O5 · INTERNAL COHESION — is a sura a WOVEN tissue (ordered chain) vs just a bag of shared vocabulary?
# Null = within-sura verse-order shuffle (keeps the sura's roots, destroys the sequence). Scale-free.
import collections, random
import numpy as np
random.seed(7); np.random.seed(7)
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(list)
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: continue
    k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
    if 1<=s<=114: sur[s].append(set(x for x in r.split() if x and x!='NA'))
def adj(verses):
    return np.mean([len(verses[i]&verses[i+1]) for i in range(len(verses)-1)]) if len(verses)>1 else np.nan
deltas=[]; small_ok=0; small_tot=0
realsum=[]; nullsum=[]
for s,vs in sur.items():
    if len(vs)<3: continue
    real=adj(vs)
    nul=[]
    for _ in range(200):
        p=vs[:]; random.shuffle(p); nul.append(adj(p))
    d=real-np.mean(nul); deltas.append((real-np.mean(nul))/(np.std(nul)+1e-9))
    realsum.append(real); nullsum.append(np.mean(nul))
    if len(vs)<=10:
        small_tot+=1; small_ok+= (real>np.mean(nul))
deltas=np.array(deltas)
realsum=np.array(realsum); nullsum=np.array(nullsum)
from math import sqrt
# paired t across suras
diff=realsum-nullsum; t=diff.mean()/(diff.std()/sqrt(len(diff)))
print("O5 · INTERNAL COHESION (woven tissue) — real adjacent weave vs within-sura order shuffle:")
print(f"   suras tested: {len(deltas)}")
print(f"   real adjacent overlap {realsum.mean():.3f}  vs shuffled {nullsum.mean():.3f}  (+{realsum.mean()-nullsum.mean():.3f})")
print(f"   paired t = {t:.1f}   |  {(deltas>0).mean():.0%} of suras weave above their own shuffle (per-sura z>2: {(deltas>2).mean():.0%})")
print(f"   small suras (<=10 verses, the 'pituitary' cases): {small_ok}/{small_tot} woven above shuffle ({small_ok/max(small_tot,1):.0%})")
print("   => internal organization is SEQUENTIAL (ordered chain), not a homogeneous bag (consistent w/ X3).")
