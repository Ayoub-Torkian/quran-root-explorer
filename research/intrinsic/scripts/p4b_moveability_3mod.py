#!/usr/bin/env python3
# C3 finish — per-verse moveability in 3 INDEPENDENT rasm modalities (rhyme, length, root).
# Each verse: is it more predictable in its TRUE place than at random spots, under each
# channel's LOCAL neighbourhood model (window ±W, verse excluded)? vs shuffled-order floor.
import glob,unicodedata,numpy as np
from collections import Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=[x for x in r.split() if x and x!='NA']
sura=[];fin=[];nw=[];vroots=[];ALLR=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su); fin.append(w[-1][-1] if w and w[-1] else ''); nw.append(len(w))
    rs=roots.get(sa.strip(),[]); vroots.append(rs); ALLR+=rs
N=len(fin); sura=np.array(sura)
fa=sorted(set(fin)); fid={c:i for i,c in enumerate(fa)}; FL=np.array([fid[c] for c in fin]); A=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]); LB=np.digitize(np.array(nw),edges)-1; B=LB.max()+1
Vr=500; topr=[r for r,_ in Counter(ALLR).most_common(Vr)]; rid={r:i for i,r in enumerate(topr)}
VR=[[rid.get(r,Vr) for r in rs] for rs in vroots]; Ar=Vr+1
W=12; AL=0.5
def loc(idx):
    return (np.bincount(FL[idx],minlength=A)+AL, np.bincount(LB[idx],minlength=B)+AL,
            np.bincount([x for k in idx for x in VR[k]],minlength=Ar)+AL)
def surp(vid,pos,order):
    lo=max(0,pos-W);hi=min(N,pos+W+1); idx=[order[k] for k in range(lo,hi) if k!=pos]
    if not idx: return 0,0,0
    fc,lc,rc=loc(idx)
    srh=-np.log2(fc[FL[vid]]/fc.sum()); sln=-np.log2(lc[LB[vid]]/lc.sum())
    srt=np.mean([-np.log2(rc[x]/rc.sum()) for x in VR[vid]]) if VR[vid] else 0.0
    return srh,sln,srt
rng=np.random.default_rng(0)
def run(order,label,nr=20):
    pos=np.empty(N,int);pos[order]=np.arange(N)
    win=np.zeros((N,3))
    for vid in range(N):
        si=surp(vid,pos[vid],order); rs=[surp(vid,int(r),order) for r in rng.integers(0,N,nr)]
        rs=np.array(rs)
        for c in range(3): win[vid,c]=np.mean(si[c]<rs[:,c])
    print(f"  {label:20s} rhyme={win[:,0].mean()*100:.1f}%  length={win[:,1].mean()*100:.1f}%  root={win[:,2].mean()*100:.1f}%  ALL3(mean)={win.mean()*100:.1f}%")
    return win
print(f"N={N} · window ±{W} · 3 rasm modalities · % of verses more predictable IN PLACE than a random spot")
w=run(np.arange(N),"true order")
run(rng.permutation(N),"shuffled (floor)")
allpass=(w[:,0]>0.5).mean(),(w[:,1]>0.5).mean(),(w[:,2]>0.5).mean()
print(f"\n  per-verse share locked-in (>50%) by channel: rhyme {allpass[0]*100:.0f}%, length {allpass[1]*100:.0f}%, root {allpass[2]*100:.0f}%")
