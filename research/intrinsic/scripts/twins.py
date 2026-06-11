#!/usr/bin/env python3
# CANDIDATE — structural twins (mathānī) MULTIMODAL test. Verse pairs sharing >=50% of roots
# are "twins" (known z=+6.5). Question for the ledger: does the twin bond CONVERGE across
# modalities — do root-twins ALSO share RHYME (final letter) and LENGTH more than chance?
# Intrinsic, rasm. Inverted index for speed.
import glob,unicodedata,numpy as np
from collections import defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=set(x for x in r.split() if x and x!='NA')
fin=[];ln_=[];rs=[]
for L in open(DATA,encoding='utf-8'):
    if '\t' not in L:continue
    sa,tx=L.split('\t',1); w=skel(tx); fin.append(w[-1][-1] if w and w[-1] else ''); ln_.append(len(w)); rs.append(roots.get(sa.strip(),set()))
N=len(fin); ln_=np.array(ln_)
inv=defaultdict(list)
for i,s in enumerate(rs):
    for r in s: inv[r].append(i)
# twin pairs: Jaccard>=0.5 via candidates sharing >=2 roots
seen=set(); twins=[]
for i in range(N):
    if len(rs[i])<2: continue
    cand=set()
    for r in rs[i]:
        if len(inv[r])<400: cand.update(inv[r])
    for j in cand:
        if j<=i: continue
        u=len(rs[i]|rs[j]); 
        if u and len(rs[i]&rs[j])/u>=0.5: twins.append((i,j))
twins=np.array(twins)
print(f"twin pairs (root-Jaccard ≥0.5): {len(twins)}")
rng=np.random.default_rng(0)
def rhyme_match(P): return np.mean([fin[a]==fin[b] for a,b in P])
def len_sim(P): return np.mean([abs(ln_[a]-ln_[b]) for a,b in P])
rnd=np.array([(rng.integers(N),rng.integers(N)) for _ in range(len(twins))])
print(f"(root) — established z=+6.5 vs vocab/length-matched null (mathani_twins.json)")
print(f"(rhyme) twins share final letter: {rhyme_match(twins)*100:.1f}%   random pairs: {rhyme_match(rnd)*100:.1f}%")
print(f"(length) mean |len diff|: twins {len_sim(twins):.1f}   random {len_sim(rnd):.1f}  (smaller=more similar)")
