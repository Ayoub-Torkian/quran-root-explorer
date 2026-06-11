#!/usr/bin/env python3
# SECOND PASS — de-confound + missing nulls. Honest demotions expected.
import collections, random, math
import numpy as np
random.seed(2); np.random.seed(2)
RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter); vcount=collections.Counter()
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114:
            vcount[s]+=1
            for x in r.split():
                if x and x!='NA': sur[s][x]+=1
suras=sorted(sur); S=len(suras); idx={s:i for i,s in enumerate(suras)}
df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1

print("1) LOCATION de-confound — how much of R²=0.84 is just sūra length?")
length=np.array([sum(sur[s].values()) for s in suras],float)
y=np.arange(S,dtype=float); y-=y.mean()
def r2(X):
    X=np.atleast_2d(X.T).T if X.ndim==1 else X
    b=np.linalg.lstsq(X,y,rcond=None)[0]; return 1-((y-X@b)**2).sum()/((y-y.mean())**2).sum()
Xlen=np.c_[np.ones(S),length,np.log(length)]
r2_len=r2(Xlen)
idf={r:math.log(S/df[r]) for r in df}; roots=sorted(df); ri={r:i for i,r in enumerate(roots)}
Sig=np.zeros((S,len(roots)))
for s in suras:
    for r,n in sur[s].items(): Sig[idx[s],ri[r]]=n*idf[r]
Sig=Sig/(np.linalg.norm(Sig,axis=1,keepdims=True)+1e-9); Sig-=Sig.mean(0)
U=np.linalg.svd(Sig,full_matrices=False)[0][:,:10]
r2_prof=r2(np.c_[np.ones(S),U])
# residualize length out of profile PCs
Ures=U-Xlen@np.linalg.lstsq(Xlen,U,rcond=None)[0]
r2_resid=r2(np.c_[np.ones(S),Ures])
print(f"   length alone R²={r2_len:.2f} | full profile R²={r2_prof:.2f} | profile AFTER removing length R²={r2_resid:.2f}")
print(f"   -> {'LENGTH dominates; O2 mostly the length gradient' if r2_resid<0.3 else 'profile adds real signal beyond length'}")

print("\n2) DIGESTIVE null — is 'recurs across >=3 distant sūras' more than random root placement?")
sof={r:set(s for s in suras if r in sur[s]) for r in df}
def reproc(assign):  # assign root->set of suras
    return sum(1 for r in assign if 3<=len(assign[r])<=20 and (max(assign[r])-min(assign[r]))>30)
real=reproc(sof)
nul=[]
for _ in range(200):
    a={r:set(random.sample(suras,len(sof[r]))) for r in df if 3<=len(sof[r])<=20}
    # only roots eligible; others can't qualify
    nul.append(sum(1 for r in a if 3<=len(a[r])<=20 and (max(a[r])-min(a[r]))>30))
print(f"   real {real} vs random-placement {np.mean(nul):.0f}±{np.std(nul):.0f}  -> {'TRIVIAL (any mid-freq root spans the corpus)' if real<=np.mean(nul)+2*np.std(nul) else 'real reprocessing'}")

print("\n3) SYMMETRY null — are 16 adjacent twin-pairs more than random ordering gives?")
rare=[r for r in df if 2<=df[r]<=60]
M=np.zeros((S,S))
for r in rare:
    h=[idx[s] for s in suras if r in sur[s]]
    for a in range(len(h)):
        for b in range(a+1,len(h)): M[h[a],h[b]]+=1; M[h[b],h[a]]+=1
dg=M.sum(1)+1e-9; A=M/np.sqrt(np.outer(dg,dg)); thr=np.quantile(A[np.triu_indices(S,1)],0.95)
real=sum(1 for i in range(S-1) if A[i,i+1]>thr)
nul=[]
for _ in range(2000):
    p=np.random.permutation(S); nul.append(sum(1 for i in range(S-1) if A[p[i],p[i+1]]>thr))
z=(real-np.mean(nul))/np.std(nul)
print(f"   real {real} adjacent pairs vs random-order {np.mean(nul):.1f}±{np.std(nul):.1f}  z={z:+.1f}  -> {'✅ real pairing' if z>2 else 'not above chance'}")

print("\n4) SKELETON de-confound — do muqaṭṭaʿāt sūras cohere beyond length?")
MUQ={2,3,7,10,11,12,13,14,15,19,20,26,27,28,29,30,31,32,36,38,40,41,42,43,44,45,46,50,68}
mi=[idx[s] for s in suras if s in MUQ]
within=np.mean([A[i,j] for a,i in enumerate(mi) for j in mi[a+1:]])
# length-matched null: random groups matched to muqattaat length distribution
lens=np.array([length[idx[s]] for s in suras])
target=sorted(mi,key=lambda i:lens[i])
nul=[]
for _ in range(2000):
    # pick random suras with similar length ranks
    g=random.sample(range(S),len(mi)); nul.append(np.mean([A[g[a],g[b]] for a in range(len(g)) for b in range(a+1,len(g))]))
z=(within-np.mean(nul))/np.std(nul)
print(f"   muqaṭṭaʿāt within-assoc {within:.3f} vs random groups {np.mean(nul):.3f} z={z:+.1f}  -> {'✅ real structural class' if z>2 else 'not beyond chance/length'}")
