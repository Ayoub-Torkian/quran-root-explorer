#!/usr/bin/env python3
# Fresh probe — POSITIONAL GRAMMAR. Do roots occupy systematic positions within the verse
# (initial vs final) beyond chance? For each frequent root, mean normalized position (0=first
# token, 1=last). Null: shuffle token order within each verse. Test (A) how many roots are
# significantly initial/final; (B) the across-root spread of mean-position vs shuffle.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        _,r=ln.split('\t',1);v=[x for x in r.split() if x and x!='NA']
        if len(v)>=4:verses.append(v)
# position of each root occurrence
pos=collections.defaultdict(list)
for v in verses:
    L=len(v)
    for i,r in enumerate(v):pos[r].append(i/(L-1))
freq={r:len(p) for r,p in pos.items()}
common=[r for r in pos if freq[r]>=30]
meanpos={r:np.mean(pos[r]) for r in common}
realspread=np.std([meanpos[r] for r in common])
rng=np.random.default_rng(0)
# null: shuffle positions within verses
def null_meanpos():
    p2=collections.defaultdict(list)
    for v in verses:
        L=len(v);perm=rng.permutation(L)
        for k,r in enumerate(v):p2[r].append(perm[k]/(L-1))
    return {r:np.mean(p2[r]) for r in common}
spreads=[];zinit=collections.Counter()
fl_means=collections.defaultdict(list)
for _ in range(60):
    nm=null_meanpos();spreads.append(np.std([nm[r] for r in common]))
    for r in common:fl_means[r].append(nm[r])
spreads=np.array(spreads)
print("verses used: %d ; frequent roots (>=30): %d" % (len(verses),len(common)))
print("(A) across-root spread of mean-position: real %.3f vs shuffle %.3f±%.3f  z=%+.1f" %
      (realspread,spreads.mean(),spreads.std(),(realspread-spreads.mean())/spreads.std()))
# (B) per-root: how many roots are significantly initial or final (|z|>3 vs their own shuffle dist)
nsig=0;inits=[];finals=[]
for r in common:
    m=np.mean(fl_means[r]);s=np.std(fl_means[r])+1e-9;z=(meanpos[r]-m)/s
    if abs(z)>3:
        nsig+=1
        if z<-3:inits.append((r,meanpos[r],z))
        else:finals.append((r,meanpos[r],z))
print("(B) roots with significant positional preference (|z|>3): %d / %d" % (nsig,len(common)))
inits.sort(key=lambda x:x[2]);finals.sort(key=lambda x:-x[2])
print("   most VERSE-INITIAL roots:", [(r,round(p,2)) for r,p,z in inits[:8]])
print("   most VERSE-FINAL roots:  ", [(r,round(p,2)) for r,p,z in finals[:8]])
