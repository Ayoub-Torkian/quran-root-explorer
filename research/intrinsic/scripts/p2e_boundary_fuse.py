#!/usr/bin/env python3
# Necessity (recall) for the sūra: fuse L11 multimodal DISCONTINUITY (the seam) with
# L18 ONSET asymmetry (the opening) into one per-transition boundary score. Evaluate at
# top-113 (matched count -> precision=recall=F). Cross-validated onset; verse-shuffle floor.
import glob,unicodedata,numpy as np
from collections import Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=set(x for x in r.split() if x and x!='NA')
sura=[];nw=[];fw=[];finL=[];vroots=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su);nw.append(len(w));fw.append(w[0] if w else '');finL.append(w[-1][-1] if w and w[-1] else '');vroots.append(roots.get(sa.strip(),set()))
N=len(sura);sura=np.array(sura);nw=np.array(nw,float)
truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)]);tset=set(np.where(truth)[0]);nb=truth.sum()
is_open=np.array([i==0 or sura[i]!=sura[i-1] for i in range(N)]); even=(sura%2==0);odd=(sura%2==1)
def modal(a):
    c=Counter(a); return c.most_common(1)[0][0] if c else ''
K=4
# discontinuity components at transition i (between verse i and i+1)
Drh=np.zeros(N-1);Dln=np.zeros(N-1);Drt=np.zeros(N-1)
for i in range(N-1):
    p=slice(max(0,i-K+1),i+1); q=slice(i+1,min(N,i+1+K))
    Drh[i]=0.0 if modal(finL[p])==modal(finL[q]) else 1.0
    Dln[i]=abs(nw[q].mean()-nw[p].mean())
    a=set().union(*vroots[p]) if vroots[p] else set(); b=set().union(*vroots[q]) if vroots[q] else set()
    Drt[i]=1-(len(a&b)/len(a|b) if (a|b) else 0)
def onset_lo(train):
    co=Counter(fw[i] for i in np.where(train&is_open)[0]);ci=Counter(fw[i] for i in np.where(train&~is_open)[0])
    no=max((train&is_open).sum(),1);ni=max((train&~is_open).sum(),1);base=np.log(no)-np.log(ni)
    so=((nw[train&is_open]<=4).mean()+1e-3);si=((nw[train&~is_open]<=4).mean()+1e-3)
    return np.array([base+np.log((co.get(fw[i],0)+.5)/no)-np.log((ci.get(fw[i],0)+.5)/ni)+(np.log(so)-np.log(si) if nw[i]<=4 else np.log(1-so)-np.log(1-si)) for i in range(N)])
z=lambda x:(x-x.mean())/(x.std()+1e-9)
# onset at transition i = onset of post-verse i+1 (cross-validated: train on opposite parity of the post-verse)
On=np.zeros(N)
On[odd]=onset_lo(even)[odd]; On[even]=onset_lo(odd)[even]
Onset_t=On[1:N]   # transition i -> post verse i+1
def topF(score):
    top=np.argsort(-score)[:nb]; tp=truth[top].sum(); return tp/nb   # P=R=F at matched count
disc=z(Drh)+z(Dln)+z(Drt)
print(f"N={N}  sūra boundaries={nb}   (top-{nb} matched -> precision=recall=F)")
print(f"  discontinuity only (L11: rhyme+len+root)   F={topF(disc):.3f}")
print(f"  onset only (L18)                           F={topF(Onset_t):.3f}")
for wfuse in (0.5,1.0,1.5,2.0):
    fuse=disc + wfuse*z(Onset_t)
    print(f"  FUSED disc + {wfuse}*onset                     F={topF(fuse):.3f}")
# shuffle floor
rng=np.random.default_rng(0)
fl=np.mean([topF(rng.permutation(disc+1.5*z(Onset_t))) for _ in range(20)])
print(f"  verse-shuffle floor                        F={fl:.3f}")
# AUC of fused
db=(disc+1.5*z(Onset_t))[truth]; di=(disc+1.5*z(Onset_t))[~truth]
auc=np.mean([(di<v).mean() for v in db]); d=(db.mean()-di.mean())/np.sqrt((db.var()+di.var())/2)
print(f"  FUSED AUC(boundary>internal)={auc:.3f}  Cohen d={d:.2f}")
