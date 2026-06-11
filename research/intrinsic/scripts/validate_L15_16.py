# Validity for L15 (movement scale) and L16 (boundary-load typology).
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
truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)])
fa=sorted(set(fin));fid={c:i for i,c in enumerate(fa)};FL=np.array([fid[c] for c in fin]);A_fl=len(fa)
edges=np.array([0,1,2,3,4,5,6,8,10,13,17,22,29,38,50,66,87,115,300,10**9]);LB=np.digitize(np.array(nw),edges)-1;A_lb=LB.max()+1
ALPHA=0.5;maxc=N+5
G=gammaln(np.arange(maxc)+ALPHA);Ffl=gammaln(np.arange(maxc)+A_fl*ALPHA);Flb=gammaln(np.arange(maxc)+A_lb*ALPHA)
cfl=gammaln(A_fl*ALPHA)-A_fl*gammaln(ALPHA);clb=gammaln(A_lb*ALPHA)-A_lb*gammaln(ALPHA)
def pref(ids,A):
    P=np.zeros((N+1,A),np.int64);P[1:]=np.cumsum(np.eye(A,dtype=np.int64)[ids],axis=0);return P
Pfl=pref(FL,A_fl);Plb=pref(LB,A_lb)
def seg(a,b):
    return float(-(G[Pfl[b]-Pfl[a]].sum()+cfl-Ffl[b-a])/LN2)+float(-(G[Plb[b]-Plb[a]].sum()+clb-Flb[b-a])/LN2)
lam=6.7
canon=list(np.where(truth)[0]+1)
# ---- L16: per-boundary local load (negative gain = load-bearing) ----
def share_loadbearing(starts):
    cuts=[0]+sorted(starts)+[N];s=0;tot=0
    for m in range(1,len(cuts)-1):
        a,x,b=cuts[m-1],cuts[m],cuts[m+1]
        g=(seg(a,x)+seg(x,b)+lam)-seg(a,b);s+=(g<0);tot+=1
    return s/tot
real_share=share_loadbearing(canon)
rng=np.random.default_rng(3)
null_shares=[]
for _ in range(200):
    rb=sorted(rng.choice(np.arange(1,N),len(canon),replace=False));null_shares.append(share_loadbearing(rb))
null_shares=np.array(null_shares)
z16=(real_share-null_shares.mean())/null_shares.std()
print(f"L16: canonical share load-bearing={real_share:.3f}  null(random cuts)={null_shares.mean():.3f}±{null_shares.std():.3f}  z={z16:.1f}")
# ---- L15: canonical 113-cut data-cost vs random 113-cut (significance of boundary placement) ----
def datacost(starts):
    cuts=[0]+sorted(starts)+[N];return sum(seg(a,b) for a,b in zip(cuts[:-1],cuts[1:]))
real_dc=datacost(canon)
rnd=np.array([datacost(sorted(rng.choice(np.arange(1,N),len(canon),replace=False))) for _ in range(200)])
z15=(rnd.mean()-real_dc)/rnd.std()
print(f"L15: canonical 113-cut data-cost={real_dc:,.0f}  random={rnd.mean():,.0f}±{rnd.std():,.0f}  advantage={rnd.mean()-real_dc:,.0f} bits  z={z15:.1f}")
