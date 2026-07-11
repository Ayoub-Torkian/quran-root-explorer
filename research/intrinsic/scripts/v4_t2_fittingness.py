# -*- coding: utf-8 -*-
"""V4 Task 2 — pre-registered null for thematic 'fittingness'.
Operationalisation: does a sura's actual content roots COHERE better than count-matched
random substitutes (a word-by-word 'fittingness' z-score)? Tests whether al-Kawthar's word
choices are locally design-unique or ordinary. Plus a regulative-voice sub-test (#10)."""
import collections, itertools, math, random
import numpy as np
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
ayahs=[]; sura_roots=collections.defaultdict(list); sura_ayahs=collections.defaultdict(list)
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    ref,rs=line.split('\t',1); su=int(ref.split(':')[0]); rl=[fa(x) for x in rs.split()]
    ayahs.append(set(rl)); sura_ayahs[su].append(set(rl))
    for r in rl: sura_roots[su].append(r)
N=len(ayahs); cnt=collections.Counter(); co=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
def pair(a,b): return co[(a,b)] if (a,b) in co else co[(b,a)]
_ac={}
def assoc(a,b):
    if a==b: return 0.0
    k=(a,b) if a<b else (b,a)
    if k in _ac: return _ac[k]
    c=pair(a,b); v=max(0.0,math.log2(c*N/(cnt[a]*cnt[b]))) if c>0 else 0.0; _ac[k]=v; return v
allroots=list(cnt);
# count-band buckets for matched substitution
import bisect
byc=collections.defaultdict(list)
for r,c in cnt.items(): byc[c].append(r)
counts_sorted=sorted(byc)
_poolcache={}
def matched(r,rng):
    c=cnt[r]
    if c not in _poolcache:
        lo=bisect.bisect_left(counts_sorted,max(1,int(c*0.5))); hi=bisect.bisect_right(counts_sorted,int(c*2)+1)
        _poolcache[c]=[x for cc in counts_sorted[lo:hi] for x in byc[cc]] or [r]
    return rng.choice(_poolcache[c])
def cohesion(rootset):
    rs=[r for r in rootset if r in cnt]
    if len(rs)<2: return 0.0
    return float(np.mean([assoc(a,b) for a,b in itertools.combinations(rs,2)]))

print("[fittingness swap-test z across all 114 suras]")
rng=random.Random(13); res={}
for su in range(1,115):
    rs=sorted(set(sura_roots[su]))
    if len(rs)<3 or len(rs)>40: res[su]=None; continue
    Ca=cohesion(rs); nulls=[]
    for _ in range(200):
        sub=[matched(r,rng) for r in rs]; nulls.append(cohesion(sub))
    mu,sd=np.mean(nulls),np.std(nulls); z=(Ca-mu)/sd if sd>0 else 0.0
    pct=100.0*sum(1 for x in nulls if x<Ca)/len(nulls)
    res[su]=(Ca,z,pct,len(rs))
kw=res[108]
print("  al-Kawthar(108): cohesion=%.3f  z=%.2f  pct=%.0f  (n_roots=%d)"%kw)
valid=[(su,v) for su,v in res.items() if v]
byz=sorted(valid,key=lambda kv:-kv[1][1])
rank=[su for su,_ in byz].index(108)+1
print("  al-Kawthar fittingness-z rank: %d of %d suras"%(rank,len(valid)))
print("  top-5 by fittingness z:", [(su,round(v[1],2)) for su,v in byz[:5]])
# short suras only (<=15 roots)
shorts=[(su,v) for su,v in valid if v[3]<=15]
byzs=sorted(shorts,key=lambda kv:-kv[1][1]); rks=[su for su,_ in byzs].index(108)+1 if 108 in [s for s,_ in shorts] else -1
print("  among %d short suras (<=15 roots), al-Kawthar rank: %d ; top-5:"%(len(shorts),rks),[(su,round(v[1],2)) for su,v in byzs[:5]])

print("\n[regulative-voice sub-test #10]")
# easing/restraint roots; Prophet-address proxy = sura contains command 'قل' root (qwl as imperative is hard;
# use a conservative proxy: 2nd-person address suras = those with root 'نبا'/'رسل' addressing, OR contains 'قول' heavily)
ease={'یسر','خفف','حزن','عجل','شقی','وضع','صبر','ثبت'}
addr_marker={'نبا','رسل'}  # sura concerns the Prophet's office
def has(su,roots): return any(r in set(sura_roots[su]) for r in roots)
# rate of easing roots in 'prophet-address' suras vs others
pa=[su for su in range(1,115) if has(su,addr_marker)]
oth=[su for su in range(1,115) if su not in pa]
def ease_rate(suras):
    tot=0;e=0
    for su in suras:
        toks=sura_roots[su]; tot+=len(toks); e+=sum(1 for t in toks if t in ease)
    return e/tot if tot else 0
print("  easing-root rate: prophet-office suras=%.4f (n=%d)  others=%.4f (n=%d)"%(ease_rate(pa),len(pa),ease_rate(oth),len(oth)))
# permutation null
rng2=random.Random(5); obs=ease_rate(pa)-ease_rate(oth); allsu=list(range(1,115)); perm=[]
for _ in range(2000):
    rng2.shuffle(allsu); g=set(allsu[:len(pa)])
    perm.append(ease_rate([s for s in g])-ease_rate([s for s in allsu[len(pa):]]))
p=sum(1 for x in perm if x>=obs)/len(perm)
print("  obs diff=%.4f  permutation p=%.3f -> %s"%(obs,p,"above-baseline (regulative signal)" if p<0.05 else "NOT above baseline (no regulative signal)"))
