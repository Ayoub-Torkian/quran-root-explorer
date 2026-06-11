#!/usr/bin/env python3
# C-twins CONTROL — does the multimodal convergence survive when EXACT-duplicate verses are
# removed (refrains/formulae trivially share rhyme+length)? And among CROSS-sūra pairs only?
import glob,unicodedata,numpy as np
from collections import defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=set(x for x in r.split() if x and x!='NA')
fin=[];ln_=[];rs=[];txt=[];su=[]
for L in open(DATA,encoding='utf-8'):
    if '\t' not in L:continue
    sa,tx=L.split('\t',1); w=skel(tx); fin.append(w[-1][-1] if w and w[-1] else ''); ln_.append(len(w))
    rs.append(roots.get(sa.strip(),set())); txt.append(' '.join(w)); su.append(int(sa.split(':')[0]))
N=len(fin); ln_=np.array(ln_)
inv=defaultdict(list)
for i,s in enumerate(rs):
    for r in s: inv[r].append(i)
def collect(excl_dup,cross_only):
    P=[]
    for i in range(N):
        if len(rs[i])<2: continue
        cand=set()
        for r in rs[i]:
            if len(inv[r])<400: cand.update(inv[r])
        for j in cand:
            if j<=i: continue
            u=len(rs[i]|rs[j])
            if not u or len(rs[i]&rs[j])/u<0.5: continue
            if excl_dup and txt[i]==txt[j]: continue
            if cross_only and su[i]==su[j]: continue
            P.append((i,j))
    return np.array(P)
rng=np.random.default_rng(0)
def stats(P,label):
    if len(P)==0: print(f"  {label}: none"); return
    rm=np.mean([fin[a]==fin[b] for a,b in P]); ls=np.mean([abs(ln_[a]-ln_[b]) for a,b in P])
    rnd=np.array([(rng.integers(N),rng.integers(N)) for _ in range(4000)])
    rmr=np.mean([fin[a]==fin[b] for a,b in rnd]); lsr=np.mean([abs(ln_[a]-ln_[b]) for a,b in rnd])
    print(f"  {label}: n={len(P):5d}  rhyme {rm*100:.1f}% (rand {rmr*100:.1f}%)  |Δlen| {ls:.1f} (rand {lsr:.1f})")
print("structural-twin convergence under controls (root-Jaccard ≥0.5):")
stats(collect(False,False),"all twins                 ")
stats(collect(True ,False),"exact-duplicates REMOVED  ")
stats(collect(True ,True ),"duplicates removed + CROSS-sūra only")
