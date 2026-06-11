#!/usr/bin/env python3
# C11 controls: (1) is the LAST verse's low surprisal beyond a RANDOM interior verse?
# (2) does it survive removing the final (rhyme-bearing) root? (3) rhyme-class change at the close.
import glob,unicodedata,numpy as np,collections,math
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=[x for x in r.split() if x and x!='NA']
freq=collections.Counter()
for rs in roots.values():
    for r in rs:freq[r]+=1
tot=sum(freq.values())
def sur(rs):
    rs=[r for r in rs if r in freq];return np.mean([-math.log2(freq[r]/tot) for r in rs]) if rs else None
bys=collections.defaultdict(list)
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);s=int(sa.split(':')[0]);bys[s].append(roots.get(sa.strip(),[]))
rng=np.random.default_rng(7)
# (1) last-verse surprisal vs interior, compared to a RANDOM non-edge verse vs interior
dlast=[];drand=[];dlast_norhyme=[]
for s,V in bys.items():
    if len(V)<7:continue
    S=[sur(v) for v in V]; interior=[x for x in S[1:-1] if x is not None]
    if len(interior)<3 or S[-1] is None:continue
    im=np.mean(interior)
    dlast.append(S[-1]-im)
    j=rng.integers(1,len(V)-1)
    if S[j] is not None:drand.append(S[j]-im)
    # remove final root from last verse
    lastr=V[-1][:-1] if len(V[-1])>1 else V[-1]
    sl=sur(lastr)
    if sl is not None:dlast_norhyme.append(sl-im)
def rep(n,d):
    d=np.array(d);t=d.mean()/(d.std(ddof=1)/np.sqrt(len(d)));print("  %-34s mean Δ=%+.3f  t=%+.1f  (n=%d)"%(n,d.mean(),t,len(d)))
print("Closing surprisal drop — controls:")
rep("LAST verse vs interior",dlast)
rep("random interior verse vs interior",drand)
rep("LAST verse MINUS final root",dlast_norhyme)
# paired: last vs random
m=min(len(dlast),len(drand)); d=np.array(dlast[:m])-np.array(drand[:m]); t=d.mean()/(d.std(ddof=1)/np.sqrt(len(d)))
print("  paired (last - random) t=%+.1f" % t)
