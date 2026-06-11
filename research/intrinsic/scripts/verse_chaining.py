#!/usr/bin/env python3
# CANDIDATE — sequential lexical chaining. Adjacent verses share roots above a within-sūra
# ORDER shuffle. 3 modalities: (A) adjacency lift vs order-null; (B) distance decay (local?);
# (C) split-half stability (odd vs even sūras).
import glob,numpy as np
from collections import defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
sura=[];vr=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);sura.append(int(sa.split(':')[0]));vr.append(roots.get(sa.strip(),set()))
sura=np.array(sura)
bnd={s:(np.where(sura==s)[0][0],np.where(sura==s)[0][-1]+1) for s in np.unique(sura)}
def share(i,j):return 1 if vr[i]&vr[j] else 0
# (B) distance decay within sūra
def decay(suras):
    out={k:[] for k in range(1,6)}
    for s in suras:
        a,b=bnd[s]
        for i in range(a,b):
            for k in range(1,6):
                if i+k<b:out[k].append(share(i,i+k))
    return {k:np.mean(v) for k,v in out.items()}
alls=[s for s in np.unique(sura) if bnd[s][1]-bnd[s][0]>=10]
dc=decay(alls)
print("(B) root-sharing vs verse distance (local chaining if it decays):")
for k in range(1,6):print(f"    gap {k}: {dc[k]:.3f}")
# (A) adjacency lift vs within-sūra order shuffle, pooled
rng=np.random.default_rng(11)
real=np.mean([share(i,i+1) for s in alls for i in range(bnd[s][0],bnd[s][1]-1)])
fl=[]
for _ in range(300):
    acc=[]
    for s in alls:
        a,b=bnd[s];p=rng.permutation(range(a,b))
        acc+=[share(p[k],p[k+1]) for k in range(len(p)-1)]
    fl.append(np.mean(acc))
fl=np.array(fl);print(f"\n(A) adjacent (gap1) {real:.3f} vs within-sūra order-shuffle {fl.mean():.3f}±{fl.std():.4f}  z={(real-fl.mean())/fl.std():.1f}  lift={real/fl.mean():.2f}x")
# (C) split-half: odd vs even sūra ids
for name,sub in [('odd sūras',[s for s in alls if s%2==1]),('even sūras',[s for s in alls if s%2==0])]:
    r=np.mean([share(i,i+1) for s in sub for i in range(bnd[s][0],bnd[s][1]-1)])
    f=[]
    for _ in range(150):
        acc=[]
        for s in sub:
            a,b=bnd[s];p=rng.permutation(range(a,b));acc+=[share(p[k],p[k+1]) for k in range(len(p)-1)]
        f.append(np.mean(acc))
    f=np.array(f);print(f"(C) {name}: real {r:.3f} vs shuffle {f.mean():.3f}  z={(r-f.mean())/f.std():.1f}")
