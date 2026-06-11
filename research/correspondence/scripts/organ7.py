#!/usr/bin/env python3
# Small suras do NOT fail internal organization — wrong instrument. Scale-free test: internal RHYME cohesion.
import unicodedata, collections, random
import numpy as np
random.seed(1); np.random.seed(1)
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
R="research/two_books_genome/data/quran/quran_arabic_verses.tsv"
sur=collections.defaultdict(list)   # sura -> list of verse-final letters
allf=[]
for ln in open(R,encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.rstrip('\n').split('\t',1); s=int(sa.split(':')[0])
    ws=[w for w in (rasm(x) for x in tx.split()) if w]
    if ws: f=ws[-1][-1]; sur[s].append(f); allf.append(f)
allf=np.array(allf)
def cohesion(letters):  # fraction sharing the dominant final letter (rhyme strength)
    c=collections.Counter(letters); return max(c.values())/len(letters)
suras=sorted(sur)
zs=[]; small=[108,103,110,112,1,114,113,111,109]
print("INTERNAL RHYME COHESION per sura vs random same-size verse sets (scale-free):")
rec={}
for s in suras:
    L=sur[s]; n=len(L); real=cohesion(L)
    null=[cohesion(list(np.random.choice(allf,n))) for _ in range(400)]
    z=(real-np.mean(null))/(np.std(null)+1e-9); zs.append(z); rec[s]=(n,real,z)
zs=np.array(zs)
print(f"   {(zs>2).sum()}/{len(suras)} suras internally rhyme-cohesive beyond chance (z>2): {(zs>2).mean():.0%}")
print(f"   median z = {np.median(zs):.1f}")
print("   small suras (the 'pituitary' cases):")
for s in small:
    if s in rec:
        n,real,z=rec[s]; print(f"     sura {s:3d} ({n} verses): {real:.0%} share the rhyme, z={z:+.1f}")
