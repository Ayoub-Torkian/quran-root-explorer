# Validity battery for L14 (MDL order-load). Four tests:
#  (1) NULL DISTRIBUTION: many global shuffles -> mean,sd,z,p (not a single shuffle).
#  (2) MODALITY CONVERGENCE: symbol-only vs wave-only each show the gap (>=2 channels agree).
#  (3) BLOCK CONTROL: within-sūra shuffle (keeps sūra membership+lengths, scrambles order
#      inside each sūra) — isolates order-load BEYOND the trivial block/length effect.
#  (4) FAITHFUL MAGNITUDE: report per-verse bits and CI, never just the raw total.
import glob,unicodedata,numpy as np
from collections import Counter
from scipy.special import gammaln
LN2=np.log(2.0)
DATA=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv')[0]
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
sura=[];fin=[];nw=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);su=int(sa.split(':')[0]);w=skel(tx)
    sura.append(su);fin.append(w[-1][-1] if w and w[-1] else '');nw.append(len(w))
N=len(sura);sura=np.array(sura)
fa=sorted(set(fin));fid={c:i for i,c in enumerate(fa)};FL0=np.array([fid[c] for c in fin]);A_fl=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]);LB0=np.digitize(np.array(nw),edges)-1;A_lb=LB0.max()+1
ALPHA=0.5;MAXSEG=160;maxc=N+5
G=gammaln(np.arange(maxc)+ALPHA);Ffl=gammaln(np.arange(maxc)+A_fl*ALPHA);Flb=gammaln(np.arange(maxc)+A_lb*ALPHA)
cfl=gammaln(A_fl*ALPHA)-A_fl*gammaln(ALPHA);clb=gammaln(A_lb*ALPHA)-A_lb*gammaln(ALPHA)
def pref(ids,A):
    P=np.zeros((N+1,A),np.int64);P[1:]=np.cumsum(np.eye(A,dtype=np.int64)[ids],axis=0);return P
def cc(c,n,Ft,k):return -(G[c].sum(axis=1)+k-Ft[n])/LN2
def opt_cost(FL,LB,use_fl=True,use_lb=True):
    Pfl=pref(FL,A_fl) if use_fl else None;Plb=pref(LB,A_lb) if use_lb else None
    k=113
    for _ in range(6):
        p=min(max(k/(N-1),1e-6),0.5);lam=-np.log2(p)
        cost=np.full(N+1,1e18);cost[0]=0;back=np.full(N+1,-1,np.int64)
        for j in range(1,N+1):
            lo=max(0,j-MAXSEG);n=j-np.arange(lo,j);tot=0.0
            if use_fl:tot=tot+cc(Pfl[j]-Pfl[lo:j],n,Ffl,cfl)
            if use_lb:tot=tot+cc(Plb[j]-Plb[lo:j],n,Flb,clb)
            cand=cost[lo:j]+tot+lam;a=np.argmin(cand);cost[j]=cand[a];back[j]=lo+a
        k=0;j=N
        while j>0:
            i=back[j]; k+= (i>0); j=i
    return cost[N]
rng=np.random.default_rng(7)
real=opt_cost(FL0,LB0)
def gshuf():
    o=rng.permutation(N);return opt_cost(FL0[o],LB0[o])
def wshuf():
    o=np.arange(N)
    for s in np.unique(sura):
        idx=np.where(sura==s)[0];o[idx]=rng.permutation(idx)
    return opt_cost(FL0[o],LB0[o])
NS=12
gn=np.array([gshuf() for _ in range(NS)]);wn=np.array([wshuf() for _ in range(NS)])
def rep(name,null):
    load=null.mean()-real;z=(null.mean()-real)/null.std()
    print(f"{name:18s} real={real:,.0f}  null={null.mean():,.0f}±{null.std():,.0f}  order-load={load:,.0f} bits  z={z:.1f}")
print(f"N={N}  channels: symbol+wave  (MAXSEG={MAXSEG}, {NS} shuffles each)")
rep("(1) global shuffle",gn)
rep("(3) within-sūra ctrl",wn)
# modality convergence
rf=opt_cost(FL0,None,True,False);rl=opt_cost(None,LB0,False,True)
gf=np.mean([opt_cost(FL0[rng.permutation(N)],None,True,False) for _ in range(6)])
gl=np.mean([opt_cost(None,LB0[rng.permutation(N)],False,True) for _ in range(6)])
print(f"(2) symbol-only order-load = {gf-rf:,.0f} bits   |   wave-only order-load = {gl-rl:,.0f} bits  (both>0 => convergent)")
print(f"(4) faithful magnitude: {(gn.mean()-real)/N:.2f} bits/verse over global shuffle; "
      f"{(wn.mean()-real)/N:.2f} bits/verse beyond block structure")
