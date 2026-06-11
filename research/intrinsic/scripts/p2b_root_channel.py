#!/usr/bin/env python3
# P2b — Sūra sufficiency with a RASM ROOT topic channel. Roots (tri-literal,
# diacritics-stripped) are rasm-derived. Replace the failed bag-of-content channel
# with a per-verse ROOT distribution; re-run the sūra MDL; does precision clear 0.45?
import glob,unicodedata,numpy as np
from collections import Counter
from scipy.special import gammaln
LN2=np.log(2.0)
ROOT=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=ROOT+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
RBA =ROOT+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
# roots keyed by sura:ayah
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' not in ln: 
        k=ln.strip(); roots[k]=[]; continue
    k,r=ln.rstrip('\n').split('\t',1); roots[k]=[x for x in r.split() if x and x!='NA']
sura=[];fin=[];nw=[];vroots=[];ALLR=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su);fin.append(w[-1][-1] if w and w[-1] else '');nw.append(len(w))
    rs=roots.get(sa.strip(),[]); vroots.append(rs); ALLR+=rs
N=len(sura);sura=np.array(sura);truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)]);tset=set(np.where(truth)[0])
fa=sorted(set(fin));fid={c:i for i,c in enumerate(fa)};FL=np.array([fid[c] for c in fin]);Afl=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]);LB=np.digitize(np.array(nw),edges)-1;Alb=LB.max()+1
Vr=400; topr=[r for r,_ in Counter(ALLR).most_common(Vr)]; rid={r:i for i,r in enumerate(topr)}
vrt=[[rid.get(r,Vr) for r in rs] for rs in vroots]; Art=Vr+1
print(f"N={N} verses · root tokens={len(ALLR)} · distinct roots={len(set(ALLR))} · channel alphabet={Art}")
def pref(ids,A,multi=False):
    P=np.zeros((N+1,A),np.int64)
    if not multi: P[1:]=np.cumsum(np.eye(A,dtype=np.int64)[ids],0)
    else:
        for k in range(N):
            P[k+1]=P[k]
            for x in ids[k]: P[k+1,x]+=1
    return P
Pfl=pref(FL,Afl);Plb=pref(LB,Alb);Prt=pref(vrt,Art,True);Pw=Prt.sum(1)
ALPHA=0.5;MAXSEG=160;mc=max(N,int(Pw[-1]))+5
G=gammaln(np.arange(mc)+ALPHA);Ffl=gammaln(np.arange(mc)+Afl*ALPHA);Flb=gammaln(np.arange(mc)+Alb*ALPHA);Frt=gammaln(np.arange(mc)+Art*ALPHA)
cfl=gammaln(Afl*ALPHA)-Afl*gammaln(ALPHA);clb=gammaln(Alb*ALPHA)-Alb*gammaln(ALPHA);crt=gammaln(Art*ALPHA)-Art*gammaln(ALPHA)
def cc(c,n,Ft,k):return -(G[c].sum(axis=1)+k-Ft[n])/LN2
def run(use_rt,iters=6):
    k=113
    for _ in range(iters):
        p=min(max(k/(N-1),1e-6),0.5);lam=-np.log2(p)
        cost=np.full(N+1,1e18);cost[0]=0;back=np.full(N+1,-1,np.int64)
        for j in range(1,N+1):
            lo=max(0,j-MAXSEG);st=np.arange(lo,j);n=j-st
            tot=cc(Pfl[j]-Pfl[lo:j],n,Ffl,cfl)+cc(Plb[j]-Plb[lo:j],n,Flb,clb)
            if use_rt: tot=tot+cc(Prt[j]-Prt[lo:j],Pw[j]-Pw[lo:j],Frt,crt)
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
# root-only channel too (is theme alone enough?)
def run_rootonly(iters=6):
    k=113
    for _ in range(iters):
        p=min(max(k/(N-1),1e-6),0.5);lam=-np.log2(p)
        cost=np.full(N+1,1e18);cost[0]=0;back=np.full(N+1,-1,np.int64)
        for j in range(1,N+1):
            lo=max(0,j-MAXSEG);st=np.arange(lo,j)
            tot=cc(Prt[j]-Prt[lo:j],Pw[j]-Pw[lo:j],Frt,crt)
            cand=cost[lo:j]+tot+lam;a=np.argmin(cand);cost[j]=cand[a];back[j]=lo+a
        b=[];j=N
        while j>0:
            i=back[j]
            if i>0: b.append(i)
            j=i
        k=len(b)
    pr=set(x-1 for x in b)
    P=len(pr&tset)/len(pr) if pr else 0;R=len(pr&tset)/len(tset)
    return len(b)+1,P,R
for lab,rt in [("symbol+wave (rasm)",False),("symbol+wave+ROOT (rasm)",True)]:
    segs,P,R,P1=run(rt); print(f"{lab:28s} segs={segs:4d}  precision={P:.3f}  recall={R:.3f}  P±1={P1:.3f}")
s,P,R=run_rootonly(); print(f"{'ROOT-only (theme)':28s} segs={s:4d}  precision={P:.3f}  recall={R:.3f}")
