# -*- coding: utf-8 -*-
"""V4 Task 5 — is 'a long sura elaborates the short' SYSTEMATIC?
For each short sura s, rank every other sura t by a LENGTH-NORMALISED, rarity-weighted
co-thematic overlap elab(t->s)=sum_{shared roots} idf(r) / nroots(t). Find the top elaborator;
test whether top elaborators are systematically LONG vs a null. (Measures co-thematic density,
NOT demonstrated intent.)"""
import collections, itertools, math, random
import numpy as np
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
sura_roots=collections.defaultdict(set); spread=collections.defaultdict(set); nv=collections.Counter()
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    ref,rs=line.split('\t',1); su=int(ref.split(':')[0]); rl=[fa(x) for x in rs.split()]
    nv[su]+=1
    for r in rl: sura_roots[su].add(r); spread[r].add(su)
idf=lambda r: math.log(114/len(spread[r]))
nroots={su:len(sura_roots[su]) for su in sura_roots}
def elab(t,s):
    sh=sura_roots[t]&sura_roots[s]
    return sum(idf(r) for r in sh)/nroots[t] if nroots[t] else 0.0
shorts=[su for su in range(1,115) if nroots.get(su,0)<=15 and nroots.get(su,0)>=3]
print("[long->short elaboration]  %d short suras tested (<=15 roots)"%len(shorts))
names={108:'al-Kawthar',112:'al-Ikhlas',103:'al-ʿAsr',110:'al-Nasr',106:'Quraysh',105:'Fil',107:'Maʿun',111:'Masad'}
toplens=[]
for s in shorts:
    rank=sorted((t for t in range(1,115) if t!=s and nroots.get(t,0)>0), key=lambda t:-elab(t,s))
    top=rank[0]; toplens.append(nroots[top])
    if s in names or s in (108,112,103,110):
        print("  s=%-3d %-10s top elaborator=sura %d (%d roots, %d verses)  elab=%.3f"%(
            s,names.get(s,''),top,nroots[top],nv[top],elab(top,s)))
# null: are top elaborators longer than a random other-sura?
alllens=[nroots[t] for t in range(1,115) if nroots.get(t,0)>0]
obs=np.mean(toplens);
rng=random.Random(4); nullmeans=[np.mean([rng.choice(alllens) for _ in shorts]) for _ in range(5000)]
p=sum(1 for x in nullmeans if x>=obs)/len(nullmeans)
print("\n  mean #roots of TOP elaborators = %.0f ; random other-sura mean = %.0f ; corpus median sura roots=%.0f"%(obs,np.mean(alllens),np.median(alllens)))
print("  permutation p(top elaborators this long by chance) = %.4f -> %s"%(p,"SYSTEMATIC: long suras elaborate short (above chance)" if p<0.05 else "NOT systematic"))
# how often is the top elaborator a 'long' sura (>=100 roots)?
nlong=sum(1 for L in toplens if L>=100)
print("  top elaborator is a LONG sura (>=100 roots) for %d/%d short suras (%.0f%%)"%(nlong,len(shorts),100*nlong/len(shorts)))
