#!/usr/bin/env python3
# P2 — Sūra sufficiency on the RASM. Does adding a rasm CONTENT channel (skeleton
# content words) to the symbol+wave MDL raise sūra-boundary PRECISION above 0.45?
# Self-consistent Bernoulli boundary code (lambda derived). All channels rasm-only.
import glob,unicodedata,numpy as np
from collections import Counter
from scipy.special import gammaln
LN2=np.log(2.0)
DATA=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv')[0]
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
sura=[];fin=[];nw=[];words=[];ALL=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);su=int(sa.split(':')[0]);w=skel(tx)
    sura.append(su);fin.append(w[-1][-1] if w and w[-1] else '');nw.append(len(w));words.append(w);ALL+=w
N=len(sura);sura=np.array(sura);truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)]);tset=set(np.where(truth)[0])
fa=sorted(set(fin));fid={c:i for i,c in enumerate(fa)};FL=np.array([fid[c] for c in fin]);Afl=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]);LB=np.digitize(np.array(nw),edges)-1;Alb=LB.max()+1
stop=set(w for w,_ in Counter(ALL).most_common(40));V=300
top=[w for w,_ in Counter([w for w in ALL if w not in stop]).most_common(V)];lid={w:i for i,w in enumerate(top)}
vlx=[[lid.get(w,V) for w in ws if w not in stop] for ws in words];Alx=V+1
def pref(ids,A,multi=False):
    P=np.zeros((N+1,A),np.int64)
    if not multi: P[1:]=np.cumsum(np.eye(A,dtype=np.int64)[ids],0)
    else:
        for k in range(N):
            P[k+1]=P[k]
            for x in ids[k]: P[k+1,x]+=1
    return P
Pfl=pref(FL,Afl);Plb=pref(LB,Alb);Plx=pref(vlx,Alx,True);Pw=Plx.sum(1)
ALPHA=0.5;MAXSEG=160;mc=max(N,int(Pw[-1]))+5
G=gammaln(np.arange(mc)+ALPHA);Ffl=gammaln(np.arange(mc)+Afl*ALPHA);Flb=gammaln(np.arange(mc)+Alb*ALPHA);Flx=gammaln(np.arange(mc)+Alx*ALPHA)
cfl=gammaln(Afl*ALPHA)-Afl*gammaln(ALPHA);clb=gammaln(Alb*ALPHA)-Alb*gammaln(ALPHA);clx=gammaln(Alx*ALPHA)-Alx*gammaln(ALPHA)
def cc(c,n,Ft,k):return -(G[c].sum(axis=1)+k-Ft[n])/LN2
def run(use_lx,iters=6):
    k=113
    for _ in range(iters):
        p=min(max(k/(N-1),1e-6),0.5);lam=-np.log2(p)
        cost=np.full(N+1,1e18);cost[0]=0;back=np.full(N+1,-1,np.int64)
        for j in range(1,N+1):
            lo=max(0,j-MAXSEG);starts=np.arange(lo,j);n=j-starts
            tot=cc(Pfl[j]-Pfl[lo:j],n,Ffl,cfl)+cc(Plb[j]-Plb[lo:j],n,Flb,clb)
            if use_lx: tot=tot+cc(Plx[j]-Plx[lo:j],Pw[j]-Pw[lo:j],Flx,clx)
            cand=cost[lo:j]+tot+lam;a=np.argmin(cand);cost[j]=cand[a];back[j]=lo+a
        b=[];j=N
        while j>0:
            i=back[j]
            if i>0: b.append(i)
            j=i
        k=len(b)
    pr=set(x-1 for x in b)
    P=len(pr&tset)/len(pr) if pr else 0; R=len(pr&tset)/len(tset)
    P1=sum(1 for q in pr if any((q+d) in tset for d in(-1,0,1)))/len(pr) if pr else 0
    return len(b)+1,P,R,P1
for lab,lx in [("symbol+wave (rasm)",False),("symbol+wave+CONTENT (rasm)",True)]:
    segs,P,R,P1=run(lx)
    print(f"{lab:30s} segs={segs:4d}  precision={P:.3f}  recall={R:.3f}  precision±1={P1:.3f}")
