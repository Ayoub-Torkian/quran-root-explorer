#!/usr/bin/env python3
# NOVELTY GATE for C7: is section-scale arrangement determined BEYOND sūra membership?
# Block-shuffle WITHIN each sūra (so sūra vocabulary is held fixed), at granularity b.
# Long sūras only (need many blocks). If adjacent blocks still beat within-sūra block-shuffle
# at b=5,10,20 -> genuine intra-sūra section order (NEW). If ~0 -> C7 adds nothing past L22+clustering.
import glob,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
import collections
bys=collections.defaultdict(list)
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);bys[int(sa.split(':')[0])].append(roots.get(sa.strip(),set()))
def jacc(a,b):
    u=a|b;return len(a&b)/len(u) if u else 0.0
rng=np.random.default_rng(9)
print("Within-sūra block-shuffle (sūra vocabulary held fixed):")
print(" b | n long sūras | real adj-Jacc | within-sūra shuffle | lift |  z")
for b in [2,5,10,20]:
    reals=[];flrs=[]
    longs=[s for s in bys if len(bys[s])>=b*4]   # need >=4 blocks
    for s in longs:
        V=bys[s];nb=len(V)//b
        blk=[set().union(*V[i*b:(i+1)*b]) for i in range(nb)]
        if nb<3:continue
        real=np.mean([jacc(blk[i],blk[i+1]) for i in range(nb-1)])
        fl=np.mean([np.mean([jacc(blk[p[i]],blk[p[i+1]]) for i in range(nb-1)]) for p in [rng.permutation(nb) for _ in range(60)]])
        reals.append(real);flrs.append(fl)
    reals=np.array(reals);flrs=np.array(flrs);d=reals-flrs
    z=d.mean()/(d.std(ddof=1)/np.sqrt(len(d))+1e-9)
    print(" %2d |     %3d      |    %.3f      |       %.3f         | %+.3f | %5.1f" %
          (b,len(reals),reals.mean(),flrs.mean(),d.mean(),z))
print("\n(z here is a per-sūra paired t across long sūras — each sūra one independent unit.)")
