# -*- coding: utf-8 -*-
"""V4 Task 4 — explicit openness gradient [HUMAN CONSTRUCT].
Per-sura openness score from three internal, measurable proxies (NOT a muhkam/mutashabih classifier):
 (1) specificity: mean idf of content roots (rarer => less anchored)
 (2) singularity: hapax density (unresolvable from own family)
 (3) low self-interpretation support: few/weak corpus co-occurrences to fix meaning => more open
openness = z1 + z2 - z3 ; ranks suras by how hard their vocabulary is to pin down INTERNALLY.
This LOCALISES/ranks openness; it never adjudicates the theological categories."""
import collections, itertools, math
import numpy as np
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
sura_ayahs=collections.defaultdict(list); ayahs=[]; spread=collections.defaultdict(set)
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    ref,rs=line.split('\t',1); su=int(ref.split(':')[0]); rl=[fa(x) for x in rs.split()]
    ayahs.append(set(rl)); sura_ayahs[su].append(rl)
    for r in rl: spread[r].add(su)
N=len(ayahs); cnt=collections.Counter(); co=collections.Counter()
for s in ayahs:
    for r in s: cnt[r]+=1
    for a,b in itertools.combinations(sorted(s),2): co[(a,b)]+=1
def pair(a,b): return co[(a,b)] if (a,b) in co else co[(b,a)]
idf=lambda r: math.log(114/len(spread[r]))
def support(r):  # self-interpretation support: # of distinct corpus co-occurring roots (capped) -> ability to fix meaning
    s=0
    for (a,b),c in co.items():
        if (a==r or b==r) and c>0: s+=1
    return s
# precompute support via degree
deg=collections.Counter()
for (a,b),c in co.items():
    deg[a]+=1; deg[b]+=1
feat={}
for su in range(1,115):
    uniq=sorted(set(r for rl in sura_ayahs[su] for r in rl))
    if not uniq: continue
    nv=len(sura_ayahs[su])
    spec=float(np.mean([idf(r) for r in uniq]))
    hd=sum(1 for r in uniq if cnt[r]==1)/nv
    sup=float(np.mean([deg[r] for r in uniq]))   # higher = more anchored
    feat[su]=(spec,hd,sup,len(uniq),nv)
S=np.array([feat[su] for su in feat]); sus=list(feat)
def z(col):
    v=S[:,col]; return (v-v.mean())/v.std()
zspec,zhd,zsup=z(0),z(1),z(2)
openness={su:(zspec[i]+zhd[i]-zsup[i]) for i,su in enumerate(sus)}
order=sorted(openness,key=lambda s:-openness[s])
print("[openness gradient — HUMAN CONSTRUCT ranking of all 114 suras]")
print("most-open top-8:", [(su,round(openness[su],2)) for su in order[:8]])
print("least-open bottom-5:", [(su,round(openness[su],2)) for su in order[-5:]])
rk=order.index(108)+1
print("al-Kawthar(108): openness=%.2f  -> rank %d of %d (percentile %.0f)"%(openness[108],rk,len(order),100*(len(order)-rk)/len(order)))
for su,nm in [(112,'al-Ikhlas'),(103,'al-ʿAsr'),(110,'al-Nasr'),(102,'al-Takathur')]:
    if su in openness: print("  %s(%d): openness=%.2f rank %d"%(nm,su,openness[su],order.index(su)+1))
print("\ndistribution: mean=%.2f sd=%.2f min=%.2f max=%.2f"%(np.mean(list(openness.values())),np.std(list(openness.values())),min(openness.values()),max(openness.values())))
print("[honest bound] this RANKS internal under-determination; it does NOT decide muhkam/mutashabih (taʾwil-humble).")
