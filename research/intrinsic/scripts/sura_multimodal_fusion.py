# -*- coding: utf-8 -*-
"""MULTIMODAL FUSION sufficiency: do fused boundary cues re-derive the canonical 113 sūra cuts?
Features (rasm, basmala excluded): semantic-cohesion drop (SVD emb), lexical TextTiling, rhyme change, length jump,
opening-formula(i+1)[recovers-known], closing divine-name(i). 5-fold CV logistic; AUC/F1/recovery@113/g_seg.
Run with all features and WITHOUT the recovers-known markers. MEASURED."""
import openpyxl, math, random, statistics as st
import numpy as np
random.seed(17); np.random.seed(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]; tok=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(str(r[8] or "").split()); tok.append(str(r[10] or "").split())
n=len(sura); G=n-1
from collections import Counter
df=Counter()
for rr in roots:
    for x in set(rr): df[x]+=1
VOC=[r for r in df if df[r]>=5]; vi={r:k for k,r in enumerate(VOC)}; V=len(VOC); Nn=n
M=np.zeros((V,V))
for rr in roots:
    ids=[vi[x] for x in set(rr) if x in vi]
    for a in ids:
        for b in ids:
            if a!=b: M[a,b]+=1
Pm=np.zeros((V,V))
nz=M>0
for a in range(V):
    for b in range(V):
        if M[a,b]>0:
            v=math.log2(M[a,b]*Nn/(df[VOC[a]]*df[VOC[b]])); Pm[a,b]=v if v>0 else 0
U,Sg,_=np.linalg.svd(Pm, full_matrices=False); EMB=U[:,:100]*np.sqrt(Sg[:100])
def vv(i):
    ids=[vi[x] for x in roots[i] if x in vi]; return EMB[ids].mean(0) if ids else np.zeros(100)
VVx=np.array([vv(i) for i in range(n)])
def cos(u,v):
    a=np.linalg.norm(u); b=np.linalg.norm(v); return float(u@v/(a*b)) if a and b else 0.0
W=3
def btf(lo,hi):
    c=Counter()
    for t in range(max(0,lo),min(n,hi)):
        for x in roots[t]:
            if x in vi: c[x]+=1
    return c
def ctf(a,b):
    cm=set(a)&set(b); num=sum(a[x]*b[x] for x in cm); na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values())); return num/(na*nb) if na and nb else 0.0
OPEN={"قل","یا","الم","الر","حم","طه","یس","ص","ق","ن","سبح","یسبح","الحمد","تبارک","ویل","إذا","عبس","اقرا","الحاقه","ال"}
DIV={"ءله","رحم","غفر","عزز","حکم","علم","ربب","قدر","رحیم","کبر","حمد"}
def feats(i):
    emb=1-cos(VVx[i],VVx[i+1])
    tile=1-ctf(btf(i-W+1,i+1), btf(i+1,i+1+W))
    last=tok[i][-1] if tok[i] else ""; nxt=tok[i+1][-1] if tok[i+1] else ""
    rhy=1.0 if last[-2:]!=nxt[-2:] else 0.0
    lj=abs(len(roots[i])-len(roots[i+1]))/ (len(roots[i])+len(roots[i+1])+1)
    first=tok[i+1][0] if tok[i+1] else ""
    op=1.0 if first in OPEN else 0.0
    dv=sum(1 for x in roots[i] if x in DIV)/(len(roots[i])+1)
    return [emb,tile,rhy,lj,op,dv]
X=np.array([feats(i) for i in range(G)]); y=np.array([1.0 if sura[i]!=sura[i+1] else 0.0 for i in range(G)])
nb=int(y.sum())
# standardize
X=(X-X.mean(0))/(X.std(0)+1e-9)
def logistic_cv(Xf, folds=5):
    idx=np.arange(G); np.random.shuffle(idx); oof=np.zeros(G)
    w_pos=(G-nb)/nb
    for f in range(folds):
        te=idx[f::folds]; tr=np.setdiff1d(idx,te)
        Xt=np.c_[np.ones(len(tr)),Xf[tr]]; yt=y[tr]; w=np.ones(len(tr)); w[yt==1]=w_pos
        beta=np.zeros(Xt.shape[1])
        for _ in range(300):
            p=1/(1+np.exp(-Xt@beta)); g=Xt.T@(w*(p-yt))/len(tr); 
            H=(Xt.T*(w*p*(1-p)))@Xt/len(tr)+1e-4*np.eye(Xt.shape[1])
            beta-=np.linalg.solve(H,g)
        Xe=np.c_[np.ones(len(te)),Xf[te]]; oof[te]=1/(1+np.exp(-Xe@beta))
    return oof, beta
def evalsc(oof,nm):
    bi=set(np.where(y==1)[0]); 
    import bisect; sw=sorted(oof[i] for i in range(G) if y[i]==0); sb=[oof[i] for i in range(G) if y[i]==1]
    A=sum(bisect.bisect_left(sw,v)+(bisect.bisect_right(sw,v)-bisect.bisect_left(sw,v))/2 for v in sb)/(len(sb)*len(sw))
    order=sorted(range(G),key=lambda i:-oof[i]); rec=len(set(order[:nb])&bi)/nb
    best=0
    for t in np.quantile(oof,np.linspace(0.5,0.999,120)):
        pred=set(i for i in range(G) if oof[i]>=t)
        if not pred: continue
        tp=len(pred&bi); P=tp/len(pred); Rc=tp/nb; F=2*P*Rc/(P+Rc) if P+Rc else 0; best=max(best,F)
    opt=st.mean(sorted(oof,reverse=True)[:nb]); canon=st.mean(oof[i] for i in bi); rnd=st.mean(oof); g=(opt-canon)/(opt-rnd+1e-9)
    print(f"  [{nm}] CV-AUC={A:.3f}  rec@113={rec:.0%}  bestF1={best:.2f}  g_seg={g:.2f}")
    return A
oofF,betaF=logistic_cv(X); 
print("FULL fusion (emb,tile,rhyme,len,OPENER,divname):"); evalsc(oofF,"full")
print("  coef:", {n_:round(float(b),2) for n_,b in zip(["emb","tile","rhyme","len","opener","divname"],betaF[1:])})
oofI,_=logistic_cv(X[:,:4]); 
print("INTRINSIC-only (emb,tile,rhyme,len — NO opener/divname):"); evalsc(oofI,"intrinsic")
print("DONE")
