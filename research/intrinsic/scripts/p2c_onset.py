#!/usr/bin/env python3
# P2c — close the Sūra (necessary AND sufficient) by adding a rasm SŪRA-ONSET term.
# Sūras BEGIN distinctively (opening words: muqaṭṭaʿāt الم/حم/الر, الحمد, يا…; short first verse).
# Onset is a POSITIONAL boundary prior the marginal channels can't see. Trained
# cross-validated by sūra parity (held out), folded into symbol+wave+root MDL.
import glob,unicodedata,numpy as np
from collections import Counter
from scipy.special import gammaln
LN2=np.log(2.0)
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); roots[k]=[x for x in r.split() if x and x!='NA']
sura=[];fin=[];nw=[];fw=[];vroots=[];ALLR=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su);fin.append(w[-1][-1] if w and w[-1] else '');nw.append(len(w));fw.append(w[0] if w else '')
    rs=roots.get(sa.strip(),[]); vroots.append(rs); ALLR+=rs
N=len(sura);sura=np.array(sura);nw=np.array(nw)
truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)]);tset=set(np.where(truth)[0])
is_open=np.array([i==0 or sura[i]!=sura[i-1] for i in range(N)])   # verse i starts a sūra
fa=sorted(set(fin));fid={c:i for i,c in enumerate(fa)};FL=np.array([fid[c] for c in fin]);Afl=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]);LB=np.digitize(nw,edges)-1;Alb=LB.max()+1
Vr=400; topr=[r for r,_ in Counter(ALLR).most_common(Vr)]; rid={r:i for i,r in enumerate(topr)}
vrt=[[rid.get(r,Vr) for r in rs] for rs in vroots]; Art=Vr+1
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
def onset_logodds(train):
    # first-word log-odds + short-verse log-odds, from TRAIN sūra openings
    op=train&is_open; ot=train&~is_open
    cw_o=Counter(fw[i] for i in np.where(op)[0]); cw_i=Counter(fw[i] for i in np.where(ot)[0])
    no=max(op.sum(),1); ni=max(ot.sum(),1)
    def wlo(w):
        po=(cw_o.get(w,0)+0.5)/(no+0.5*len(cw_o)+1); pi=(cw_i.get(w,0)+0.5)/(ni+0.5*len(cw_i)+1)
        return np.log(po)-np.log(pi)
    # length: openings shorter; two-bin (<=4 short)
    so=( (nw[op]<=4).mean()+1e-3 ); si=( (nw[ot]<=4).mean()+1e-3 )
    llo_short=np.log(so)-np.log(si); llo_long=np.log(1-so)-np.log(1-si)
    base=np.log(no)-np.log(ni)
    out=np.zeros(N)
    for i in range(N):
        out[i]=base+wlo(fw[i])+(llo_short if nw[i]<=4 else llo_long)
    return out
def run(onset,beta,eval_mask):
    k=113
    for _ in range(6):
        p=min(max(k/(N-1),1e-6),0.5);lam=-np.log2(p)
        cost=np.full(N+1,1e18);cost[0]=0;back=np.full(N+1,-1,np.int64)
        for j in range(1,N+1):
            lo=max(0,j-MAXSEG);st=np.arange(lo,j);n=j-st
            tot=cc(Pfl[j]-Pfl[lo:j],n,Ffl,cfl)+cc(Plb[j]-Plb[lo:j],n,Flb,clb)+cc(Prt[j]-Prt[lo:j],Pw[j]-Pw[lo:j],Frt,crt)
            ob=np.where(st>0, -beta*onset[st], 0.0)   # reward starting a segment at an opening-looking verse
            cand=cost[lo:j]+tot+lam+ob;a=np.argmin(cand);cost[j]=cand[a];back[j]=lo+a
        b=[];j=N
        while j>0:
            i=back[j]
            if i>0: b.append(i)
            j=i
        k=len(b)
    pr=set(x-1 for x in b)
    # evaluate only on held-out boundaries (transitions whose post-verse is in eval_mask)
    ev=set(t for t in tset if eval_mask[t+1])
    prh=set(q for q in pr if eval_mask[q+1])
    tp=len(prh&ev); P=tp/len(prh) if prh else 0; R=tp/len(ev) if ev else 0
    P1=sum(1 for q in prh if any((q+d) in ev for d in(-1,0,1)))/len(prh) if prh else 0
    return len(b)+1,P,R,P1
odd=(sura%2==1); even=(sura%2==0)
print(f"N={N}  (cross-validated by sūra parity; onset trained on the OTHER half)")
for beta in (0.0,1.0,2.0,3.0):
    o_e=onset_logodds(even); s1,P1,R1,Pp1=run(o_e,beta,odd)
    o_o=onset_logodds(odd);  s2,P2,R2,Pp2=run(o_o,beta,even)
    P=(P1+P2)/2;Rr=(R1+R2)/2;Pp=(Pp1+Pp2)/2
    tag="(baseline, no onset)" if beta==0 else ""
    print(f" beta={beta:<4}  precision={P:.3f}  recall={Rr:.3f}  P±1={Pp:.3f}  {tag}")
