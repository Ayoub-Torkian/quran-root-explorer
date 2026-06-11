#!/usr/bin/env python3
# Phase B4 — Āyah by MDL on the WORD stream. Same self-consistent Bernoulli boundary
# code; channels = word-final-letter (rhyme/cadence) + word-length(letters).
# Test: does the text's own surface model recover āyah ends? Compare to a positional
# cadence test (is the āyah-end word an MDL-load-bearing cut far more than interior?).
import glob, unicodedata, numpy as np
from collections import Counter
from scipy.special import gammaln
LN2=np.log(2.0)
DATA=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv')[0]
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
W=[]; end=[]   # word stream; end[i]=True if word i is the last word of its āyah
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln: continue
    _,tx=ln.split('\t',1); ws=skel(tx)
    for k,w in enumerate(ws):
        W.append(w); end.append(k==len(ws)-1)
M=len(W); end=np.array(end)
fin=[w[-1] for w in W]; wl=np.array([len(w) for w in W])
fa=sorted(set(fin)); fid={c:i for i,c in enumerate(fa)}; FL=np.array([fid[c] for c in fin]); A_fl=len(fa)
edges=np.array([0,1,2,3,4,5,6,7,8,10,12,15,100]); LB=np.digitize(wl,edges)-1; A_lb=LB.max()+1
true_idx=set(np.where(end[:-1])[0])   # transition i is an āyah end
print(f"words={M}  āyāt(end markers)={end.sum()}  mean āyah length={M/end.sum():.1f} words  A_fl={A_fl} A_lb={A_lb}")

def prefix1(ids,A):
    P=np.zeros((M+1,A),np.int64); P[1:]=np.cumsum(np.eye(A,dtype=np.int64)[ids],axis=0); return P
Pfl=prefix1(FL,A_fl); Plb=prefix1(LB,A_lb)
ALPHA=0.5; MAXSEG=60; maxc=M+5
G=gammaln(np.arange(maxc)+ALPHA); Ffl=gammaln(np.arange(maxc)+A_fl*ALPHA); Flb=gammaln(np.arange(maxc)+A_lb*ALPHA)
cfl=gammaln(A_fl*ALPHA)-A_fl*gammaln(ALPHA); clb=gammaln(A_lb*ALPHA)-A_lb*gammaln(ALPHA)
def cc(counts,n,Ftab,const): return -(G[counts].sum(axis=1)+const-Ftab[n])/LN2
def run_dp(lam):
    INF=1e18; cost=np.full(M+1,INF); cost[0]=0; back=np.full(M+1,-1,np.int64)
    for j in range(1,M+1):
        lo=max(0,j-MAXSEG); n=j-np.arange(lo,j)
        tot=cc(Pfl[j]-Pfl[lo:j],n,Ffl,cfl)+cc(Plb[j]-Plb[lo:j],n,Flb,clb)
        cand=cost[lo:j]+tot+lam; k=np.argmin(cand); cost[j]=cand[k]; back[j]=lo+k
    b=[]; j=M
    while j>0:
        i=back[j]
        if i>0: b.append(i)
        j=i
    return sorted(b)
k=end.sum()
for _ in range(8):
    p=min(max(k/(M-1),1e-6),0.5); lam=-np.log2(p); bnds=run_dp(lam); k=len(bnds)
pr=set(int(b)-1 for b in bnds)
tp0=len(pr & true_idx); tp1=sum(1 for q in pr if any((q+d) in true_idx for d in (-1,0,1)))
P0=tp0/len(pr); R0=tp0/len(true_idx); P1=tp1/len(pr); R1=tp1/len(true_idx)
print(f"MDL word-stream: segs={k+1} lam={lam:.1f}b  P0={P0:.3f} R0={R0:.3f} F0={2*P0*R0/(P0+R0):.3f} | P1={P1:.3f} R1={R1:.3f} F1={2*P1*R1/(P1+R1):.3f}")

# positional cadence test: local MDL gain of cutting at a true āyah end vs interior word
def seg_code(a,b):
    return float(cc((Pfl[b]-Pfl[a])[None,:],np.array([b-a]),Ffl,cfl)[0])+float(cc((Plb[b]-Plb[a])[None,:],np.array([b-a]),Flb,clb)[0])
ends=np.where(end[:-1])[0]
np.random.seed(0); rng=np.random.choice(np.where(~end[:-1])[0], size=4000, replace=False)
def localgain(pos,half=8):
    a=max(0,pos-half); b=min(M,pos+half+1); x=pos+1
    return (seg_code(a,x)+seg_code(x,b)+lam)-seg_code(a,b)
ge=np.array([localgain(p) for p in np.random.choice(ends,4000,replace=False)])
gi=np.array([localgain(p) for p in rng])
print(f"local cadence gain (neg=cut pays off): āyah-end mean={ge.mean():.2f}  interior mean={gi.mean():.2f}  "
      f"share end load-bearing={np.mean(ge<0):.2f} vs interior {np.mean(gi<0):.2f}")
d=(gi.mean()-ge.mean())/np.sqrt((ge.var()+gi.var())/2)
print(f"Cohen d (end more compressive than interior)={d:.2f}")
# shuffle floor on word-final letters
o=np.random.permutation(M); FLs=FL[o]
Pfls=prefix1(FLs,A_fl)
def seg_code_s(a,b): return float(cc((Pfls[b]-Pfls[a])[None,:],np.array([b-a]),Ffl,cfl)[0])
ge_s=np.array([ (seg_code_s(max(0,p-8),p+1)+seg_code_s(p+1,min(M,p+9))+lam)-seg_code_s(max(0,p-8),min(M,p+9)) for p in np.random.choice(ends,2000,replace=False)])
print(f"shuffle floor: end-position gain on shuffled stream mean={ge_s.mean():.2f} (real end mean={ge.mean():.2f})")
