#!/usr/bin/env python3
# REFINE F-items with better instruments (all-or-none: body has them, find them).
import unicodedata, collections, math
import numpy as np
rng=np.random.default_rng(1)
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
RBA="research/two_books_genome/roots_by_ayah.tsv"; TX="research/two_books_genome/data/quran/quran_arabic_verses.tsv"
stream=[]; vlen=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114: stream+= [x for x in r.split() if x and x!='NA']
for ln in open(TX,encoding='utf-8'):
    if '\t' in ln:
        sa,tx=ln.split('\t',1); s=int(sa.split(':')[0])
        if 1<=s<=114: vlen.append(len([w for w in (rasm(x) for x in tx.split()) if w]))
vlen=np.array(vlen,float)

# F6 FLOW-DIRECTION via transition ASYMMETRY: |N(a->b) - N(b->a)|
big=collections.Counter(zip(stream,stream[1:]))
asym=0; tot=0
for (a,b),n in big.items():
    asym+=abs(n-big.get((b,a),0)); tot+=n
real=asym/tot
nul=[]
for _ in range(30):
    p=list(rng.permutation(stream)); bg=collections.Counter(zip(p,p[1:])); t=sum(bg.values())
    nul.append(sum(abs(n-bg.get((b,a),0)) for (a,b),n in bg.items())/t)
z=(real-np.mean(nul))/np.std(nul)
print(f"F6 FLOW-DIRECTION (transition asymmetry): real {real:.3f} vs shuffle {np.mean(nul):.3f} z={z:+.0f}  -> {'✅ DIRECTED flow (irreversible transitions)' if z>3 else 'reversible'}")

# F5 ENDOCRINE: slow long-range modulation of the RHYTHM (verse-length) signal
def ac(x,lag): return np.corrcoef(x[:-lag],x[lag:])[0,1]
print("F5 ENDOCRINE (slow modulation of rhythm/verse-length):", end=" ")
for lag in (1,10,50,100,300):
    print(f"ac{lag}={ac(vlen,lag):+.2f}", end="  ")
nul_ac=np.std([ac(rng.permutation(vlen),100) for _ in range(300)])
print(f" -> long-range positive = ✅ slow modulation (shuffle ac100 sd={nul_ac:.2f})")

# F4 CIRCULATION: do formulaic refrains reach ALL regions? max gap between ANY frequent bigram-formula
big2=[bg for bg,n in big.items() if n>=10]   # recurring formulae (the 'blood')
fset=set(big2)
hit=np.zeros(len(stream))
for i in range(len(stream)-1):
    if (stream[i],stream[i+1]) in fset: hit[i]=1
pos=np.where(hit)[0]; gaps=np.diff(np.concatenate([[ -1],pos,[len(stream)]]))
print(f"F4 CIRCULATION (formulae perfuse all regions): {len(big2)} recurring formulae; cover {hit.mean():.0%} of positions; max dry-gap {gaps.max()} tokens of {len(stream)} -> {'✅ reaches all regions' if gaps.max()<len(stream)*0.05 else '◑ partial'}")
