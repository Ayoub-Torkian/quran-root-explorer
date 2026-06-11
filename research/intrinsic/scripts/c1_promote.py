#!/usr/bin/env python3
# Promote C1 — the arrangement "intermediate-complexity band". For each rasm modality,
# the canonical order must sit BETWEEN random (worse compression) and sorted (better):
# random > canonical > sorted in MDL data-cost. Show it in 3 modalities = the text is
# neither a random gas nor a sorted crystal — the regime of meaningful sequences.
import glob,unicodedata,numpy as np
from collections import Counter
from scipy.special import gammaln
LN2=np.log(2.0)
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=[x for x in r.split() if x and x!='NA']
fin=[];nw=[];vroots=[];ALLR=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); w=skel(tx)
    fin.append(w[-1][-1] if w and w[-1] else '');nw.append(len(w))
    rs=roots.get(sa.strip(),[]); vroots.append(rs); ALLR+=rs
N=len(fin)
fa=sorted(set(fin));fid={c:i for i,c in enumerate(fa)};FL0=np.array([fid[c] for c in fin]);Afl=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]);LB0=np.digitize(np.array(nw),edges)-1;Alb=LB0.max()+1
# dominant root per verse (single categorical for the root modality)
Vr=300;topr=[r for r,_ in Counter(ALLR).most_common(Vr)];rid={r:i for i,r in enumerate(topr)}
def domroot(rs):
    for r in rs:
        if r in rid: return rid[r]
    return Vr
RT0=np.array([domroot(rs) for rs in vroots]);Art=Vr+1
ALPHA=.5;MAXSEG=160;mc=N+5
G=gammaln(np.arange(mc)+ALPHA)
def opt_cost(ids,A):
    Ft=gammaln(np.arange(mc)+A*ALPHA);k0=gammaln(A*ALPHA)-A*gammaln(ALPHA)
    P=np.zeros((N+1,A),np.int64);P[1:]=np.cumsum(np.eye(A,dtype=np.int64)[ids],0)
    def cc(c,n):return -(G[c].sum(axis=1)+k0-Ft[n])/LN2
    k=113
    for _ in range(5):
        p=min(max(k/(N-1),1e-6),0.5);lam=-np.log2(p)
        cost=np.full(N+1,1e18);cost[0]=0;back=np.full(N+1,-1,np.int64)
        for j in range(1,N+1):
            lo=max(0,j-MAXSEG);n=j-np.arange(lo,j)
            cand=cost[lo:j]+cc(P[j]-P[lo:j],n)+lam;a=np.argmin(cand);cost[j]=cand[a];back[j]=lo+a
        kk=0;j=N
        while j>0:
            i=back[j];kk+=(i>0);j=i
        k=kk
    return cost[N]
rng=np.random.default_rng(0)
def band(ids,A,name):
    canon=opt_cost(ids,A)
    rnd=np.mean([opt_cost(ids[rng.permutation(N)],A) for _ in range(6)])
    srt=opt_cost(ids[np.argsort(ids,kind='stable')],A)   # sort by this feature (homogeneous blocks)
    pos=(canon-srt)/(rnd-srt) if rnd>srt else float('nan')   # 0=sorted,1=random; meaningful band ~ middle
    print(f"  {name:18s} random={rnd:,.0f} > canonical={canon:,.0f} > sorted={srt:,.0f} bits   "
          f"[{'BAND OK' if srt<canon<rnd else 'FAIL'}]  position={pos:.2f}")
    return srt<canon<rnd
print(f"N={N}  intermediate-complexity band test (random > canonical > sorted in EACH rasm modality)")
ok=[]
ok.append(band(FL0,Afl,"symbol: rhyme"))
ok.append(band(LB0,Alb,"wave: length"))
ok.append(band(RT0,Art,"root: theme"))
print(f"\n  modalities with the band confirmed: {sum(ok)}/3   -> {'PROMOTE C1' if sum(ok)>=3 else 'not yet'}")
