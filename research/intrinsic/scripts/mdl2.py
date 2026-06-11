#!/usr/bin/env python3
# Phase B (refined) — MDL self-segmentation with a PARAMETER-FREE boundary code.
# Boundary indicator over N-1 transitions ~ Bernoulli(p); its two-part code cost is
#   -k*log2(p) - (N-1-k)*log2(1-p),  p = k/(N-1)  (MLE, self-consistent).
# Per-boundary penalty lam = -log2(p) is therefore DERIVED, iterated to a fixed point,
# never hand-set. Segment data code = KT/Dirichlet-Multinomial marginal (alpha=0.5).
# Channels: symbol(final letter) + wave(length bin). Lexical kept as confirmation.
# The only null is the text's own shuffle.

import glob, unicodedata, numpy as np, json, os
from collections import Counter
from scipy.special import gammaln
LN2=np.log(2.0)
DATA=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv')[0]
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
sura=[];fin=[];nwords=[];words=[];ALL=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su); fin.append(w[-1][-1] if w and w[-1] else ''); nwords.append(len(w)); words.append(w); ALL+=w
N=len(sura); sura=np.array(sura)
truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)]); truth_idx=set(np.where(truth)[0])

fl_alpha=sorted(set(fin)); fl_id={c:i for i,c in enumerate(fl_alpha)}
FL=np.array([fl_id[c] for c in fin]); A_fl=len(fl_alpha)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9])
LB=np.digitize(np.array(nwords),edges)-1; A_lb=LB.max()+1

def prefix1(ids,A):
    P=np.zeros((N+1,A),dtype=np.int64)
    idx=np.eye(A,dtype=np.int64)[ids]; P[1:]=np.cumsum(idx,axis=0); return P
Pfl=prefix1(FL,A_fl); Plb=prefix1(LB,A_lb)

ALPHA=0.5; MAXSEG=300
maxc=N+5
G=gammaln(np.arange(maxc)+ALPHA)
Ffl=gammaln(np.arange(maxc)+A_fl*ALPHA); Flb=gammaln(np.arange(maxc)+A_lb*ALPHA)
cfl=gammaln(A_fl*ALPHA)-A_fl*gammaln(ALPHA); clb=gammaln(A_lb*ALPHA)-A_lb*gammaln(ALPHA)
def cc(counts,n,Ftab,const):           # channel code in bits
    return -(G[counts].sum(axis=1)+const-Ftab[n])/LN2

def run_dp(lam, use_fl=True, use_lb=True):
    INF=1e18; cost=np.full(N+1,INF); cost[0]=0.0; back=np.full(N+1,-1,np.int64)
    for j in range(1,N+1):
        lo=max(0,j-MAXSEG); starts=np.arange(lo,j); n=j-starts; tot=0.0
        if use_fl: tot=tot+cc(Pfl[j]-Pfl[lo:j],n,Ffl,cfl)
        if use_lb: tot=tot+cc(Plb[j]-Plb[lo:j],n,Flb,clb)
        cand=cost[lo:j]+tot+lam; k=np.argmin(cand); cost[j]=cand[k]; back[j]=lo+k
    bnds=[]; j=N
    while j>0:
        i=back[j]
        if i>0: bnds.append(i)
        j=i
    return cost[N], sorted(bnds)

def fit_selfconsistent(use_fl=True,use_lb=True,iters=12):
    """Iterate p=k/(N-1); lam=-log2 p. Return converged partition + full code length."""
    k=113
    for _ in range(iters):
        p=min(max(k/(N-1),1e-6),0.5); lam=-np.log2(p)
        data_cost,bnds=run_dp(lam,use_fl,use_lb); k=len(bnds)
    # full two-part code = data + boundary-indicator code (Bernoulli)
    bcode=-(k*np.log2(p)+(N-1-k)*np.log2(1-p))
    return bnds,data_cost,bcode,p,lam

def evalb(pred,tol=0):
    pr=set(int(b)-1 for b in pred)
    tp=sum(1 for q in pr if any((q+d) in truth_idx for d in range(-tol,tol+1)))
    P=tp/len(pr) if pr else 0; R=tp/len(truth_idx); F=2*P*R/(P+R) if P+R else 0
    return P,R,F,len(pr)

print(f"N={N}  canonical internal boundaries={len(truth_idx)}  (self-consistent Bernoulli boundary code)")
print("="*78)
for name,kw in [("symbol(fin)",dict(use_fl=True,use_lb=False)),
                ("wave(len)",dict(use_fl=False,use_lb=True)),
                ("symbol+wave",dict(use_fl=True,use_lb=True))]:
    bnds,dc,bc,p,lam=fit_selfconsistent(**kw)
    P0,R0,F0,k=evalb(bnds,0); P1,R1,F1,_=evalb(bnds,1)
    print(f"{name:14s} segs={k+1:4d} lam={lam:4.1f}b p={p:.4f}  P0={P0:.3f} R0={R0:.3f} F0={F0:.3f} | P1={P1:.3f} R1={R1:.3f} F1={F1:.3f}")
print("="*78)

# ---- chosen model: symbol+wave ----
bnds,dc,bc,p,lam=fit_selfconsistent(True,True)
def total_cost(boundaries,use_fl=True,use_lb=True,lam=lam):
    cuts=[0]+list(boundaries)+[N]; tot=0.0
    for a,b in zip(cuts[:-1],cuts[1:]):
        if use_fl: tot+=float(cc((Pfl[b]-Pfl[a])[None,:],np.array([b-a]),Ffl,cfl)[0])
        if use_lb: tot+=float(cc((Plb[b]-Plb[a])[None,:],np.array([b-a]),Flb,clb)[0])
    tot+=lam*(len(cuts)-2)
    return tot
canon=list(np.where(truth)[0]+1)
print(f"\nMDL-optimal: {len(bnds)+1} segments (median len {np.median(np.diff([0]+bnds+[N])):.0f} verses)")
print(f"canonical partition data-cost vs MDL-optimal data-cost: {total_cost(canon):,.0f} vs {dc:,.0f} bits")

# ---- نull discipline: verse-shuffle floor ----
np.random.seed(1)
def shuffled_optimal():
    o=np.random.permutation(N)
    global Pfl,Plb
    Pfl_b,Plb_b=Pfl,Plb
    Pfl=prefix1(FL[o],A_fl); Plb=prefix1(LB[o],A_lb)
    bb,dcs,_,_,_=fit_selfconsistent(True,True,iters=8)
    Pfl,Plb=Pfl_b,Plb_b
    return len(bb)+1,dcs
sk,sdc=shuffled_optimal()
print(f"\nverse-shuffle floor: optimal segs={sk}  data-cost={sdc:,.0f}  (real data-cost={dc:,.0f}; gap={sdc-dc:,.0f} bits = recoverable order)")

# ---- per-boundary necessity map: local Δcode of each canonical boundary ----
# For each canonical boundary, compare code(merged neighbours) - code(split at true spot).
def seg_code(a,b):
    s=0.0
    s+=float(cc((Pfl[b]-Pfl[a])[None,:],np.array([b-a]),Ffl,cfl)[0])
    s+=float(cc((Plb[b]-Plb[a])[None,:],np.array([b-a]),Flb,clb)[0])
    return s
cuts=[0]+canon+[N]; gains=[]
for m in range(1,len(cuts)-1):
    a,x,b=cuts[m-1],cuts[m],cuts[m+1]
    g=(seg_code(a,x)+seg_code(x,b)+lam)-seg_code(a,b)   # negative = boundary pays for itself
    gains.append(g)
gains=np.array(gains)
print(f"\nper-boundary local MDL gain (negative=load-bearing): mean={gains.mean():.1f}b  "
      f"share load-bearing={np.mean(gains<0):.2f}  median={np.median(gains):.1f}b")
# shifted/random nulls on full partition
def jit(sh):
    cs=[]
    for _ in range(20):
        j=sorted(set(int(np.clip(b+np.random.randint(-sh,sh+1),1,N-1)) for b in canon)); cs.append(total_cost(j))
    return np.mean(cs)
cc0=total_cost(canon)
print(f"\ncanonical full code={cc0:,.0f}  jitter±5={jit(5):,.0f}  jitter±20={jit(20):,.0f}")
rc=[total_cost(sorted(np.random.choice(np.arange(1,N),113,replace=False))) for _ in range(40)]
print(f"random 113-cut={np.mean(rc):,.0f}±{np.std(rc):,.0f}  (canonical beats random by {np.mean(rc)-cc0:,.0f} bits)")

json.dump({"mdl_starts":[int(b) for b in bnds],"canonical_starts":[int(b) for b in canon],
           "per_boundary_gain":[float(g) for g in gains],"N":N,"p":float(p),"lam":float(lam)},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'mdl_boundaries.json'),'w'))
print(f"\nsaved -> mdl_boundaries.json")
