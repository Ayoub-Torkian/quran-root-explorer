#!/usr/bin/env python3
# FRESH PROBE — closing cadence. Is the LAST verse of a sūra systematically distinct from
# its interior (length, information-density)? Complements L18 (onset). Per-sūra paired:
# compare first & last verse to the sūra's interior mean, across all sūras.
import glob,unicodedata,numpy as np,collections,math
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B))
skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
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
    sa,tx=ln.split('\t',1);s=int(sa.split(':')[0]);bys[s].append((len(skel(tx.strip())),sur(roots.get(sa.strip(),[]))))
dLfirst=[];dLlast=[];dSfirst=[];dSlast=[]
for s,V in bys.items():
    if len(V)<6:continue
    L=[v[0] for v in V];Sv=[v[1] for v in V]
    intL=np.mean(L[1:-1]); intS=np.mean([x for x in Sv[1:-1] if x is not None])
    dLfirst.append(L[0]-intL); dLlast.append(L[-1]-intL)
    if Sv[0] is not None:dSfirst.append(Sv[0]-intS)
    if Sv[-1] is not None:dSlast.append(Sv[-1]-intS)
def rep(name,d):
    d=np.array(d);t=d.mean()/(d.std(ddof=1)/np.sqrt(len(d)));print("  %-26s mean Δ=%+.2f  t=%+.1f  (n=%d)"%(name,d.mean(),t,len(d)))
print("LENGTH (verse vs sūra interior mean, rasm letters):")
rep("first verse",dLfirst); rep("LAST verse",dLlast)
print("INFORMATION DENSITY (root surprisal vs interior):")
rep("first verse",dSfirst); rep("LAST verse",dSlast)
