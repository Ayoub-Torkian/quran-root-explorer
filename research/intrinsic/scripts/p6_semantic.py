#!/usr/bin/env python3
# FRONTIER — intrinsic semantic channel. The text is its own model: build root vectors
# from the Qur'an's OWN root co-occurrence (PPMI -> SVD), NO external corpus/embedding.
# Per-verse semantic vector; thematic-shift at sura seams. Test boundary detection +
# fuse with L11 discontinuity & L18 onset. Does it break the 0.27 recovery ceiling?
import glob,unicodedata,numpy as np
from collections import Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') if False else ''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: k,r=ln.rstrip('\n').split('\t',1); roots[k]=[x for x in r.split() if x and x!='NA']
sura=[];fin=[];nw=[];vroots=[];fw=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su);fin.append(w[-1][-1] if w and w[-1] else '');nw.append(len(w));fw.append(w[0] if w else '')
    vroots.append(roots.get(sa.strip(),[]))
N=len(sura);sura=np.array(sura);nw=np.array(nw,float)
truth=np.array([sura[i+1]!=sura[i] for i in range(N-1)]);tset=set(np.where(truth)[0]);nb=truth.sum()
# ---- build intrinsic root vectors from co-occurrence within +-1 verse ----
allr=[r for rs in vroots for r in rs]; V=[r for r,_ in Counter(allr).most_common(1500)]; ridx={r:i for i,r in enumerate(V)}; nv=len(V)
Co=np.zeros((nv,nv))
for i in range(N):
    ctx=set()
    for j in (i-1,i,i+1):
        if 0<=j<N: ctx|=set(vroots[j])
    cs=[ridx[r] for r in ctx if r in ridx]
    for a in cs:
        for b in cs:
            if a!=b: Co[a,b]+=1
rsum=Co.sum(1,keepdims=True)+1e-9; tot=Co.sum()
P=Co/tot; pr=rsum/tot
PMI=np.log((P+1e-12)/(pr*pr.T+1e-12)); PPMI=np.maximum(PMI,0)
U,S,Vt=np.linalg.svd(PPMI,full_matrices=False)
D=50; EMB=U[:,:D]*S[:D]   # root vectors
EMB=EMB/ (np.linalg.norm(EMB,axis=1,keepdims=True)+1e-9)
def vec(rs):
    v=[EMB[ridx[r]] for r in rs if r in ridx]
    return np.mean(v,axis=0) if v else np.zeros(D)
VV=np.array([vec(rs) for rs in vroots])
# ---- semantic-shift at each transition (cosine distance across a +-K window) ----
K=4
def wmean(a,b):
    s=VV[a:b]; n=np.linalg.norm(s,axis=1); s=s[n>0]
    return s.mean(0) if len(s) else np.zeros(D)
sem=np.zeros(N-1)
for i in range(N-1):
    p=wmean(max(0,i-K+1),i+1); q=wmean(i+1,min(N,i+1+K))
    sem[i]=1-np.dot(p,q)/((np.linalg.norm(p)*np.linalg.norm(q))+1e-9)
def auc(s):
    b=s[truth];i=s[~truth]; return np.mean([(i<v).mean() for v in b])
def topF(s): top=np.argsort(-s)[:nb]; return truth[top].sum()/nb
print(f"N={N} sūra boundaries={nb} · intrinsic root vectors D={D} from own co-occurrence")
print(f"  semantic-shift alone:           AUC={auc(sem):.3f}  topF={topF(sem):.3f}")
# baselines + fusion
def modal(a):
    from collections import Counter as C; c=C(a); return c.most_common(1)[0][0] if c else ''
Drh=np.array([0.0 if modal(fin[max(0,i-K+1):i+1])==modal(fin[i+1:i+1+K]) else 1.0 for i in range(N-1)])
Dln=np.array([abs(nw[i+1:i+1+K].mean()-nw[max(0,i-K+1):i+1].mean()) for i in range(N-1)])
is_open=np.array([i==0 or sura[i]!=sura[i-1] for i in range(N)])
co=Counter(fw[i] for i in np.where(is_open)[0]);ci=Counter(fw[i] for i in np.where(~is_open)[0]);no=is_open.sum();ni=(~is_open).sum()
On=np.array([np.log((co.get(fw[i],0)+.5)/no)-np.log((ci.get(fw[i],0)+.5)/ni) for i in range(N)])
z=lambda x:(x-x.mean())/(x.std()+1e-9)
disc=z(Drh)+z(Dln)
fuse_no_sem=disc+1.5*z(On[1:])
fuse_sem=disc+1.5*z(On[1:])+1.5*z(sem)
print(f"  L11⊕L18 (no semantic):          AUC={auc(fuse_no_sem):.3f}  topF={topF(fuse_no_sem):.3f}")
print(f"  L11⊕L18 ⊕ INTRINSIC SEMANTIC:   AUC={auc(fuse_sem):.3f}  topF={topF(fuse_sem):.3f}")
rng=np.random.default_rng(0)
print(f"  semantic-shift shuffle floor topF={np.mean([topF(rng.permutation(sem)) for _ in range(20)]):.3f}")
