#!/usr/bin/env python3
# Promote C2 — sūra-onset. (A) signal in 4 independent rasm modalities (cross-val AUC vs 0.5 floor).
# (B) constrained-count MDL (exactly 114 segs) with onset -> recover recall (necessity).
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
sura=[];nw=[];fw=[];finL=[];vroots=[];ALLR=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su);nw.append(len(w));fw.append(w[0] if w else '');finL.append(w[-1][-1] if w and w[-1] else '')
    rs=roots.get(sa.strip(),[]); vroots.append(rs); ALLR+=rs
N=len(sura);sura=np.array(sura);nw=np.array(nw)
is_open=np.array([i==0 or sura[i]!=sura[i-1] for i in range(N)]); even=(sura%2==0);odd=(sura%2==1)
rng=np.random.default_rng(0)
def auc(s1,s0):
    if len(s1)==0 or len(s0)==0:return .5
    return np.mean([(s0<v).mean()+0.5*(s0==v).mean() for v in s1])
flo=[w[0] if w else '' for w in fw]
def lo_word(arr,train):
    co=Counter(arr[i] for i in np.where(train&is_open)[0]); ci=Counter(arr[i] for i in np.where(train&~is_open)[0])
    no=max((train&is_open).sum(),1);ni=max((train&~is_open).sum(),1)
    return np.array([np.log((co.get(arr[i],0)+.5)/no)-np.log((ci.get(arr[i],0)+.5)/ni) for i in range(N)])
recent=Counter();nov=np.zeros(N);from collections import deque;win=deque()
for i in range(N):
    rs=set(vroots[i]); nov[i]=(len([r for r in rs if recent[r]==0])/max(len(rs),1)) if rs else .5
    for r in vroots[i]: recent[r]+=1;win.append(r)
    while len(win)>200: recent[win.popleft()]-=1
print("=== (A) onset across rasm modalities (cross-val AUC, opening vs interior; floor 0.5) ===")
mods=[("symbol: first-letter", lambda tr: lo_word(flo,tr)),
      ("lexical: first-word",   lambda tr: lo_word(fw,tr)),
      ("wave: shortness",       lambda tr: (-nw).astype(float)),
      ("network: root-novelty", lambda tr: nov)]
for name,fn in mods:
    se=fn(even);so=fn(odd)
    a=(auc(se[odd&is_open],se[odd&~is_open])+auc(so[even&is_open],so[even&~is_open]))/2
    fll=auc(se[odd][rng.permutation(odd.sum())][:odd.sum()//20], se[odd])
    print(f"  {name:26s} AUC={a:.3f}  (floor 0.50)")
# ---- (B) constrained-count MDL ----
fa=sorted(set(finL));fid={c:i for i,c in enumerate(fa)};FL=np.array([fid[c] for c in finL]);Afl=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]);LB=np.digitize(nw,edges)-1;Alb=LB.max()+1
Vr=400;topr=[r for r,_ in Counter(ALLR).most_common(Vr)];rid={r:i for i,r in enumerate(topr)}
vrt=[[rid.get(r,Vr) for r in rs] for rs in vroots];Art=Vr+1
def pref(ids,A,multi=False):
    P=np.zeros((N+1,A),np.int64)
    if not multi:P[1:]=np.cumsum(np.eye(A,dtype=np.int64)[ids],0)
    else:
        for k in range(N):
            P[k+1]=P[k]
            for x in ids[k]:P[k+1,x]+=1
    return P
Pfl=pref(FL,Afl);Plb=pref(LB,Alb);Prt=pref(vrt,Art,True);Pw=Prt.sum(1)
A2=.5;mc=max(N,int(Pw[-1]))+5
G=gammaln(np.arange(mc)+A2);Ffl=gammaln(np.arange(mc)+Afl*A2);Flb=gammaln(np.arange(mc)+Alb*A2);Frt=gammaln(np.arange(mc)+Art*A2)
cfl=gammaln(Afl*A2)-Afl*gammaln(A2);clb=gammaln(Alb*A2)-Alb*gammaln(A2);crt=gammaln(Art*A2)-Art*gammaln(A2)
def cc(c,n,Ft,k):return -(G[c].sum(axis=1)+k-Ft[n])/LN2
truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)]);tset=set(np.where(truth)[0])
def onset_lo():
    tr=np.ones(N,bool); co=Counter(fw[i] for i in np.where(tr&is_open)[0]);ci=Counter(fw[i] for i in np.where(tr&~is_open)[0])
    no=is_open.sum();ni=(~is_open).sum();base=np.log(no)-np.log(ni)
    so=((nw[is_open]<=4).mean()+1e-3);si=((nw[~is_open]<=4).mean()+1e-3)
    return np.array([base+np.log((co.get(fw[i],0)+.5)/no)-np.log((ci.get(fw[i],0)+.5)/ni)+(np.log(so)-np.log(si) if nw[i]<=4 else np.log(1-so)-np.log(1-si)) for i in range(N)])
def kseg(onset,beta,K=114,L=130):
    INF=1e18;C=np.full((N+1,K+1),INF);C[0,0]=0.0;Ar=np.full((N+1,K+1),-1,np.int64)
    for j in range(1,N+1):
        lo=max(0,j-L);st=np.arange(lo,j);n=j-st
        sc=cc(Pfl[j]-Pfl[lo:j],n,Ffl,cfl)+cc(Plb[j]-Plb[lo:j],n,Flb,clb)+cc(Prt[j]-Prt[lo:j],Pw[j]-Pw[lo:j],Frt,crt)
        sc=sc+np.where(st>0,-beta*onset[st],0.0)
        cand=C[lo:j,0:K]+sc[:,None]            # (L,K)
        am=np.argmin(cand,axis=0)
        C[j,1:K+1]=cand[am,np.arange(K)];Ar[j,1:K+1]=lo+am
    bnds=[];j=N;m=K
    while m>0:
        a=Ar[j,m]
        if a>0:bnds.append(a)
        j=a;m-=1
    pr=set(x-1 for x in bnds);P=len(pr&tset)/len(pr) if pr else 0;Rr=len(pr&tset)/len(tset)
    return len(bnds)+1,P,Rr
print("\n=== (B) constrained-count MDL (exactly 114 segments) ===")
o=onset_lo()
for beta in (0.0,2.0):
    segs,P,Rr=kseg(o,beta)
    print(f"  K=114 β={beta}:  segs={segs}  precision={P:.3f}  recall={Rr:.3f}  F={2*P*Rr/(P+Rr) if P+Rr else 0:.3f}")
