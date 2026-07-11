# -*- coding: utf-8 -*-
"""Desaturated sufficiency: can a RICHER discontinuity signal re-derive the 113 sūra cuts? Signals:
(a) TextTiling block cosine (W=3 root-bag windows), (b) corpus-internal SVD root-embedding verse cosine.
For each: saturation, necessity (z vs within, AUC), optimality, sufficiency (top-K recovery, best F1, g_seg). MEASURED."""
import openpyxl, math, random, statistics as st
import numpy as np
random.seed(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append([x for x in str(r[8] or "").split()])
n=len(sura); G=n-1
from collections import Counter
df=Counter()
for rr in roots:
    for x in set(rr): df[x]+=1
VOC=[r for r in df if df[r]>=5]; vi={r:k for k,r in enumerate(VOC)}; V=len(VOC)
N=n
# co-occurrence (verse-level) PPMI matrix
import numpy as np
M=np.zeros((V,V))
for rr in roots:
    ids=[vi[x] for x in set(rr) if x in vi]
    for a in ids:
        for b in ids:
            if a!=b: M[a,b]+=1
P=np.zeros((V,V))
for a in range(V):
    for b in range(V):
        if M[a,b]>0:
            v=math.log2(M[a,b]*N/(df[VOC[a]]*df[VOC[b]]))
            P[a,b]=v if v>0 else 0
# SVD embedding
U,Sg,Vt=np.linalg.svd(P, full_matrices=False)
k=100; EMB=U[:,:k]*np.sqrt(Sg[:k])
def vvec(i):
    ids=[vi[x] for x in roots[i] if x in vi]
    return EMB[ids].mean(0) if ids else np.zeros(k)
VV=np.array([vvec(i) for i in range(n)])
def cos(u,v):
    nu=np.linalg.norm(u); nv=np.linalg.norm(v)
    return float(u@v/(nu*nv)) if nu and nv else 0.0
emb=[1-cos(VV[i],VV[i+1]) for i in range(G)]
# TextTiling block cosine (W=3) on tf vectors
W=3
def block_tf(lo,hi):
    c=Counter()
    for t in range(max(0,lo),min(n,hi)):
        for x in roots[t]:
            if x in vi: c[x]+=1
    return c
def ctf(a,b):
    common=set(a)&set(b); num=sum(a[x]*b[x] for x in common)
    na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
    return num/(na*nb) if na and nb else 0.0
tile=[1-ctf(block_tf(i-W+1,i+1), block_tf(i+1,i+1+W)) for i in range(G)]
bset=set(i for i in range(G) if sura[i]!=sura[i+1]); nb=len(bset)
bi=[i for i in range(G) if i in bset]; wi=[i for i in range(G) if i not in bset]
def stats(score,nm):
    mx=max(score); sat=sum(1 for v in score if v>=mx-1e-6)/G
    real=st.mean(score[i] for i in bi)-st.mean(score[i] for i in wi)
    idx=list(range(G)); ds=[]
    for _ in range(500):
        random.shuffle(idx); ds.append(st.mean(score[i] for i in idx[:nb])-st.mean(score[i] for i in idx[nb:]))
    z=(real-st.mean(ds))/(st.pstdev(ds) or 1e-9)
    import bisect; sw=sorted(score[i] for i in wi); sb=[score[i] for i in bi]
    A=sum(bisect.bisect_left(sw,v)+(bisect.bisect_right(sw,v)-bisect.bisect_left(sw,v))/2 for v in sb)/(len(sb)*len(sw))
    order=sorted(range(G), key=lambda i:-score[i]); topK=set(order[:nb]); rec=len(topK&bset)/nb
    best=0
    for t in sorted(set(score))[::max(1,len(set(score))//200)]:
        pred=set(i for i in range(G) if score[i]>=t)
        if not pred: continue
        tp=len(pred&bset); Pr=tp/len(pred); Rc=tp/nb; F=2*Pr*Rc/(Pr+Rc) if Pr+Rc else 0
        best=max(best,F)
    opt=st.mean(score[i] for i in order[:nb]); canon=st.mean(score[i] for i in bi); rnd=st.mean(score)
    g=(opt-canon)/(opt-rnd+1e-9)
    print(f"  [{nm}] sat={sat:.0%}  necessity z={z:+.1f} AUC={A:.3f}  | sufficiency rec@113={rec:.0%} bestF1={best:.2f} g_seg={g:.2f}")
print("voc(df>=5):",V," ayat:",n," boundaries:",nb)
stats(emb,"SVD-embedding")
stats(tile,"TextTiling W3")
print("DONE")
