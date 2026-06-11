#!/usr/bin/env python3
# CANDIDATE — sūra internal thematic coherence. Is a sūra's content more self-coherent than
# a same-length window placed at a RANDOM OFFSET? 3 angles: (A) root co-occurrence within
# the sūra vs random window; (B) repeated-root density; (C) coherence DROPS across the seam.
# Intrinsic, rasm roots. The content-level test of "the sūra is a unit".
import glob,unicodedata,numpy as np
from collections import defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=set(x for x in r.split() if x and x!='NA')
sura=[];vr=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); sura.append(int(sa.split(':')[0])); vr.append(roots.get(sa.strip(),set()))
N=len(sura);sura=np.array(sura)
# verse index ranges per sura
bounds={}
for s in np.unique(sura):
    idx=np.where(sura==s)[0]; bounds[s]=(idx[0],idx[-1]+1)
def coherence(a,b):
    # fraction of verse-pairs in [a,b) sharing >=1 root (sampled if large)
    idx=list(range(a,b)); 
    if len(idx)<3: return None
    import random
    pairs=[(idx[i],idx[j]) for i in range(len(idx)) for j in range(i+1,len(idx))]
    if len(pairs)>2000:
        rng=np.random.default_rng(a); pairs=[pairs[k] for k in rng.choice(len(pairs),2000,replace=False)]
    sh=sum(1 for i,j in pairs if vr[i]&vr[j]); return sh/len(pairs)
def rep_density(a,b):
    from collections import Counter; c=Counter(r for i in range(a,b) for r in vr[i])
    tot=sum(c.values()); return (tot-len(c))/tot if tot else 0   # share of root-tokens that are repeats
rng=np.random.default_rng(0)
real_coh=[];rand_coh=[];real_rep=[];rand_rep=[]
for s,(a,b) in bounds.items():
    L=b-a
    if L<6: continue
    rc=coherence(a,b)
    if rc is None: continue
    real_coh.append(rc); real_rep.append(rep_density(a,b))
    # random-offset same-length windows
    rcs=[];rrs=[]
    for _ in range(30):
        st=rng.integers(0,N-L); rcs.append(coherence(st,st+L)); rrs.append(rep_density(st,st+L))
    rand_coh.append(np.mean([x for x in rcs if x is not None])); rand_rep.append(np.mean(rrs))
real_coh=np.array(real_coh);rand_coh=np.array(rand_coh);real_rep=np.array(real_rep);rand_rep=np.array(rand_rep)
print(f"sūras tested (>=6 verses): {len(real_coh)}")
print(f"(A) root co-occurrence within unit: sūra {real_coh.mean():.3f} vs random-window {rand_coh.mean():.3f}  "
      f"(sūra more coherent in {np.mean(real_coh>rand_coh)*100:.0f}%; mean Δ={real_coh.mean()-rand_coh.mean():+.3f})")
d=(real_coh-rand_coh); print(f"    paired t≈{d.mean()/(d.std()/np.sqrt(len(d))+1e-9):.1f}")
print(f"(B) repeated-root density: sūra {real_rep.mean():.3f} vs random-window {rand_rep.mean():.3f}  "
      f"(more in {np.mean(real_rep>rand_rep)*100:.0f}%)")
