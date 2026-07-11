# -*- coding: utf-8 -*-
"""WHOLE-ENTITY sūra-hood as MULTI-UNIFORM SECTIONS: a sūra = a few coherent sections sharing a dominant theme.
Structural features per span (āyah embeddings): top-1 variance fraction (dominant theme), centroid-similarity,
best-2-block centroid relatedness, blocks-to-80%-variance, length-rhythm, internal-opener. Classify real-sūra vs
random same-length contiguous span (no reordering); 5-fold CV logistic + greedy selection. MEASURED."""
import openpyxl, math, statistics as st
import numpy as np
from collections import Counter, defaultdict
np.random.seed(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]; tok=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(str(r[8] or "").split()); tok.append(str(r[10] or "").split())
n=len(sura)
df=Counter()
for rr in roots:
    for x in set(rr): df[x]+=1
VOC=[r for r in df if df[r]>=5]; vi={r:k for k,r in enumerate(VOC)}; V=len(VOC)
M=np.zeros((V,V))
for rr in roots:
    ids=[vi[x] for x in set(rr) if x in vi]
    for a in ids:
        for b in ids:
            if a!=b: M[a,b]+=1
Pm=np.zeros((V,V))
for a in range(V):
    for b in range(V):
        if M[a,b]>0:
            v=math.log2(M[a,b]*n/(df[VOC[a]]*df[VOC[b]])); Pm[a,b]=v if v>0 else 0
U,Sg,_=np.linalg.svd(Pm,full_matrices=False); EMB=U[:,:80]*np.sqrt(Sg[:80])
def vec(i):
    ids=[vi[x] for x in roots[i] if x in vi]; return EMB[ids].mean(0) if ids else np.zeros(80)
VV=np.array([vec(i) for i in range(n)])
def unit(v):
    nv=np.linalg.norm(v,axis=1,keepdims=True); return v/(nv+1e-9)
OPEN=set("قل یا الم الر حم طه یس ص ق ن سبح یسبح الحمد تبارک ویل إذا اقرا".split())
def feats(lo,hi):
    A=VV[lo:hi]; L=hi-lo
    if L<3: return None
    An=unit(A); cen=A.mean(0); cs=float(np.mean(An@ (cen/(np.linalg.norm(cen)+1e-9))))   # centroid similarity
    Ac=A-A.mean(0); cov=Ac.T@Ac; ev=np.linalg.eigvalsh(cov)[::-1]; tot=ev.sum()+1e-9
    top1=float(ev[0]/tot); 
    cum=np.cumsum(ev)/tot; k80=int(np.searchsorted(cum,0.8)+1); blocks80=k80/L          # parsimony of sections
    # best 2-block contiguous split -> relatedness of the two section centroids
    bestrel=1.0
    for c in range(1,L):
        c1=A[:c].mean(0); c2=A[c:].mean(0); rel=float(c1@c2/((np.linalg.norm(c1)*np.linalg.norm(c2))+1e-9))
        bestrel=min(bestrel,rel)
    lens=[len(roots[i]) for i in range(lo,hi)]; lenreg=1/(1+(st.pstdev(lens)/(st.mean(lens)+1e-9)))
    inop=sum(1 for k in range(lo+1,hi) if tok[k] and tok[k][0] in OPEN)/L
    return [top1, cs, bestrel, blocks80, lenreg, inop]
names=["top1_var","centroid_sim","block2_relat","blocks80","len_reg","intl_opener"]
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[cur]=(start,i); cur=sura[i]; start=i
bounds[cur]=(start,n)
pos=[]; neg=[]
for s,(a,b) in bounds.items():
    f=feats(a,b)
    if f: pos.append(f)
    L=b-a
    if L<3: continue
    for _ in range(20):
        s0=np.random.randint(0,n-L+1); g=feats(s0,s0+L)
        if g: neg.append(g)
X=np.array(pos+neg); y=np.array([1.0]*len(pos)+[0.0]*len(neg)); G=len(y); nb=len(pos)
X=(X-X.mean(0))/(X.std(0)+1e-9)
def cvauc(cols):
    Xf=X[:,cols]; idx=np.arange(G); np.random.shuffle(idx); oof=np.zeros(G); wpos=(G-nb)/nb
    for f in range(5):
        te=idx[f::5]; tr=np.setdiff1d(idx,te); Xt=np.c_[np.ones(len(tr)),Xf[tr]]; yt=y[tr]; w=np.ones(len(tr)); w[yt==1]=wpos; beta=np.zeros(Xt.shape[1])
        for _ in range(40):
            p=1/(1+np.exp(-np.clip(Xt@beta,-30,30))); g=Xt.T@(w*(p-yt))/len(tr); H=(Xt.T*(w*p*(1-p)))@Xt/len(tr)+1e-4*np.eye(Xt.shape[1]); beta-=np.linalg.solve(H,g)
        Xe=np.c_[np.ones(len(te)),Xf[te]]; oof[te]=1/(1+np.exp(-np.clip(Xe@beta,-30,30)))
    import bisect; sw=sorted(oof[y==0]); sb=oof[y==1]
    return sum(bisect.bisect_left(sw,v)+(bisect.bisect_right(sw,v)-bisect.bisect_left(sw,v))/2 for v in sb)/(len(sb)*len(sw))
print("real sūra:",nb," random spans:",len(neg))
print("single-modality CV-AUC:")
for c in range(len(names)): print(f"  {names[c]:13} AUC={cvauc([c]):.3f}")
chosen=[]; rem=list(range(len(names))); prev=0.5
print("greedy forward selection:")
while rem:
    best=max(((c,cvauc(chosen+[c])) for c in rem), key=lambda t:t[1])
    if best[1]-prev<0.01 and chosen: break
    chosen.append(best[0]); rem.remove(best[0]); print(f"  + {names[best[0]]:13} -> AUC={best[1]:.3f}"); prev=best[1]
print("ALL:",round(cvauc(list(range(len(names)))),3)," | minimal:",[names[c] for c in chosen])
print("DONE")
