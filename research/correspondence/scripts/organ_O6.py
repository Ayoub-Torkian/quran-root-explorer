#!/usr/bin/env python3
# O6 · RHYTHM/COORDINATION (heartbeat) — do a sura's verses share the rhyme (fasila) far above chance?
import unicodedata, collections, random
import numpy as np
random.seed(7); np.random.seed(7)
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
R="research/two_books_genome/data/quran/quran_arabic_verses.tsv"
sur=collections.defaultdict(list)
for ln in open(R,encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.rstrip('\n').split('\t',1); s=int(sa.split(':')[0])
    ws=[w for w in (rasm(x) for x in tx.split()) if w]
    if ws: sur[s].append(ws[-1][-1])     # final rasm letter (the rhyme consonant)
suras=sorted(sur)
# within vs across same-final-letter probability
allf=[f for s in suras for f in sur[s]]
# within: sample pairs in same sura
def same_within(n=200000):
    hits=0;t=0
    ss=[s for s in suras if len(sur[s])>=2]
    for _ in range(n):
        s=random.choice(ss); a,b=random.sample(sur[s],2); hits+= (a==b); t+=1
    return hits/t
def same_across(n=200000):
    hits=0
    for _ in range(n):
        a,b=random.choice(allf),random.choice(allf); hits+= (a==b)
    return hits/n
w=same_within(); a=same_across()
print(f"O6 · RHYME COORDINATION — P(two verses share final letter):")
print(f"   within-sura {w:.3f}  vs  across-corpus {a:.3f}   ratio = {w/a:.2f}x  (the organ's verses beat to one rhyme)")
# per-sura significance vs random same-size sets (heartbeat is per-organ)
def dom(L): c=collections.Counter(L); return max(c.values())/len(L)
zs=[]; small=[108,103,112,114,111,109,1]
rec={}
for s in suras:
    L=sur[s]; n=len(L); real=dom(L)
    nul=[dom(list(np.random.choice(allf,n))) for _ in range(300)]
    z=(real-np.mean(nul))/(np.std(nul)+1e-9); zs.append(z); rec[s]=(n,real,z)
zs=np.array(zs)
print(f"   per-sura: {(zs>2).mean():.0%} of suras rhyme-cohesive beyond chance (z>2); median z={np.median(zs):.1f}")
print(f"   NOTE: rasm-only catches the CONSONANT rhyme; vowel-rhyme suras read lower -> rasm rhyme is PARTIAL.")
for s in small:
    if s in rec: n,real,z=rec[s]; print(f"     sura {s} ({n}v): {real:.0%} share rhyme, z={z:+.1f}")
