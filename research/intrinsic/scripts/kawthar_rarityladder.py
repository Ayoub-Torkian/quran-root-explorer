# -*- coding: utf-8 -*-
"""RARITY LADDER: climb spread k=1,2,3,...  At each k: #roots, mean idf (specificity), and how the rare-root
inter-sura graph PERCOLATES (cumulative spread 2..k) -> giant-component fraction of 114 suras. Where al-Kawthar's roots sit."""
import collections, math
import networkx as nx
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
vr={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); vr[k]=[fa(x) for x in rs.split()]
Nv=len(vr)
rootsuras=collections.defaultdict(set); df=collections.Counter()
for k,rs in vr.items():
    s=int(k.split(':')[0])
    for r in set(rs): df[r]+=1; rootsuras[r].add(s)
spread={r:len(rootsuras[r]) for r in rootsuras}
byk=collections.defaultdict(list)
for r,k in spread.items(): byk[k].append(r)
idf=lambda r: math.log(Nv/df[r])
allsuras=set(s for ss in rootsuras.values() for s in ss)
print("k | #roots | %roots | mean_idf | cum inter-sura edges | giant-comp suras | %114 connected")
G=nx.Graph(); G.add_nodes_from(range(1,115))
import itertools
cum_roots=0
for k in range(1,21):
    rs=byk.get(k,[]); cum_roots+=len(rs)
    if k>=2:
        for r in rs:
            for a,b in itertools.combinations(sorted(rootsuras[r]),2): G.add_edge(a,b)
    gc=max((len(c) for c in nx.connected_components(G)),default=0) if G.number_of_edges() else 0
    mi=sum(idf(r) for r in rs)/len(rs) if rs else 0
    print(f"{k:2d} | {len(rs):5d} | {100*len(rs)/len(spread):4.1f} | {mi:5.2f} | {G.number_of_edges():5d} | {gc:3d} | {100*gc/114:4.0f}%")
# specificity drift: sample roots at each rarity tier
print("\nsemantic character by tier (sample roots):")
for k in [1,2,3,5,10]:
    samp=sorted(byk.get(k,[]),key=lambda r:-idf(r))[:8]
    print(f"  k={k}: {samp}")
# where al-Kawthar's 7 roots sit on the ladder
KW=[fa(x) for x in ['عطو','کثر','صلو','ربب','نحر','شنء','بتر']]
print("\nal-Kawthar roots on the rarity ladder (root: spread k, #verses df):")
for r in KW: print(f"  {r}: k={spread[r]} suras, df={df[r]} verses, idf={idf(r):.1f}")
