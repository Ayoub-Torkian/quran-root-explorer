# -*- coding: utf-8 -*-
"""V4 Task 3 — cross-text generalisation. Comparable lexical fingerprint for the compact early
suras al-Asr(103), al-Ikhlas(112), al-Nasr(110) vs al-Kawthar(108): is dense-singularity +
fittingness PARTICULAR to al-Kawthar or GENERAL to compact suras?"""
import collections, itertools, math, random
import numpy as np
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
sura_ayahs=collections.defaultdict(list); sura_roots=collections.defaultdict(list); ayahs=[]
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    ref,rs=line.split('\t',1); su=int(ref.split(':')[0]); rl=[fa(x) for x in rs.split()]
    ayahs.append(set(rl)); sura_ayahs[su].append(rl)
    for r in rl: sura_roots[su].append(r)
N=len(ayahs); cnt=collections.Counter(); co=collections.Counter(); spread=collections.defaultdict(set)
for su in sura_ayahs:
    for rl in sura_ayahs[su]:
        for r in rl: spread[r].add(su)
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
def pair(a,b): return co[(a,b)] if (a,b) in co else co[(b,a)]
def assoc(a,b):
    c=pair(a,b); return max(0.0,math.log2(c*N/(cnt[a]*cnt[b]))) if c>0 and a!=b else 0.0
idf=lambda r: math.log(114/len(spread[r]))
import bisect; byc=collections.defaultdict(list)
for r,c in cnt.items(): byc[c].append(r)
cs=sorted(byc); _pc={}
def matched(r,rng):
    c=cnt[r]
    if c not in _pc:
        lo=bisect.bisect_left(cs,max(1,int(c*0.5))); hi=bisect.bisect_right(cs,int(c*2)+1)
        _pc[c]=[x for k in cs[lo:hi] for x in byc[k]] or [r]
    return rng.choice(_pc[c])
def cohesion(rs):
    rs=[r for r in rs if r in cnt]
    return float(np.mean([assoc(a,b) for a,b in itertools.combinations(rs,2)])) if len(rs)>1 else 0.0

def features(su,rng):
    toks=sura_roots[su]; uniq=sorted(set(toks)); nv=len(sura_ayahs[su])
    hapax=[r for r in uniq if cnt[r]==1]
    hd=len(hapax)/nv
    mean_idf=float(np.mean([idf(r) for r in uniq]))
    Ca=cohesion(uniq); nl=[cohesion([matched(r,rng) for r in uniq]) for _ in range(200)]
    mu,sd=np.mean(nl),np.std(nl); fz=(Ca-mu)/sd if sd>0 else 0.0
    return dict(nv=nv,nroots=len(uniq),hapax=len(hapax),hd=hd,mean_idf=mean_idf,fit_z=fz)

# corpus percentiles for hapax-density across all 114
rng=random.Random(9)
HD={};
for su in range(1,115):
    toks=set(sura_roots[su]); nv=len(sura_ayahs[su])
    if nv==0: continue
    HD[su]=sum(1 for r in toks if cnt[r]==1)/nv
def pct(val,d): vals=list(d.values()); return 100.0*sum(1 for x in vals if x<val)/len(vals)

print("sura  name        nv  roots  hapax  hd(=hapax/verse)  hd_pct  mean_idf  fit_z")
names={108:'al-Kawthar',103:'al-ʿAsr  ',112:'al-Ikhlas',110:'al-Nasr  '}
for su in [108,103,112,110]:
    f=features(su,rng);
    print("%4d  %-10s %3d  %4d   %4d   %.3f            %5.0f    %.2f      %.2f"%(
        su,names[su],f['nv'],f['nroots'],f['hapax'],f['hd'],pct(f['hd'],HD),f['mean_idf'],f['fit_z']))
print("\n[interpretation] compare al-Kawthar's dense-singularity + fittingness to the other compact early suras.")
print("hd corpus median=%.3f ; suras with hd>0 (any hapax): %d/114"%(np.median(list(HD.values())),sum(1 for v in HD.values() if v>0)))
