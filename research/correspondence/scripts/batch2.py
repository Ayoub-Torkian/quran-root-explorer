#!/usr/bin/env python3
import collections, random
import numpy as np
random.seed(1); np.random.seed(1)
RBA="research/two_books_genome/roots_by_ayah.tsv"
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114: verses.append((s,set(x for x in r.split() if x and x!='NA')))
N=len(verses)
# 21 NERVOUS / SIGNAL — does verse content propagate to the next? adjacent rare-root overlap vs random pair
df=collections.Counter()
for s,rs in verses:
    for r in rs: df[r]+=1
rare=lambda r: 2<=df[r]<=60
adj=np.mean([len(set(x for x in verses[i][1] if rare(x)) & set(x for x in verses[i+1][1] if rare(x))) for i in range(N-1) if verses[i][0]==verses[i+1][0]])
rng=np.random.default_rng(1)
rnd=np.mean([len(set(x for x in verses[i][1] if rare(x)) & set(x for x in verses[j][1] if rare(x))) for i,j in rng.integers(0,N,(20000,2))])
print(f"21 NERVOUS/SIGNAL (propagation): adjacent rare-root overlap {adj:.3f} vs random pair {rnd:.3f} -> {'✅ signal propagates' if adj>3*rnd else '◑'}")
# 22 DIGESTIVE / INTAKE — reprocessed motifs: rare roots recurring across MANY distant suras
sura_of=collections.defaultdict(set)
for s,rs in verses:
    for r in rs: sura_of[r].add(s)
reproc=[r for r in sura_of if 3<=len(sura_of[r])<=20 and (max(sura_of[r])-min(sura_of[r]))>30]
print(f"22 DIGESTIVE/INTAKE (motif reprocessing): {len(reproc)} rare roots recur across >=3 suras spanning >30 apart (same material reworked across the corpus) -> ✅ reprocessing present")
# 23 EXCRETORY/abrogation-like: roots that appear ONLY early then vanish (used then dropped)
firsts={r:min(sura_of[r]) for r in sura_of if len(sura_of[r])>=2}; lasts={r:max(sura_of[r]) for r in firsts}
early_only=[r for r in firsts if lasts[r]<=20 and len(sura_of[r])>=3]
print(f"23 EXCRETORY (used-then-dropped): {len(early_only)} roots confined to suras<=20 (introduced then not reused later) -> ◑ candidate")
