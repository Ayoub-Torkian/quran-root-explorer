# -*- coding: utf-8 -*-
"""Multimodal fusion v2 — add contextual-embedding tiling, rhyme run-length, windowed length-rhythm, 2nd-person
address shift to the 6 prior modes. 5-fold CV logistic; necessity (AUC/z) + sufficiency (recovery@113/F1/g_seg),
intrinsic-only vs full. All rasm, basmala excluded, window-based (no boundary leakage). MEASURED."""
import openpyxl, math, statistics as st
import numpy as np
np.random.seed(17)
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
for a in range(V):
    row=M[a]
    for b in np.nonzero(row)[0]:
        v=math.log2(row[b]*Nn/(df[VOC[a]]*df[VOC[b]])); Pm[a,b]=v if v>0 else 0
Uu,Sg,_=np.linalg.svd(Pm, full_matrices=False); EMB=Uu[:,:100]*np.sqrt(Sg[:100])
def vv(i):
    ids=[vi[x] for x in roots[i] if x in vi]; return EMB[ids].mean(0) if ids else np.zeros(100)
VVx=np.array([vv(i) for i in range(n)])
def cos(u,v):
    a=np.linalg.norm(u); b=np.linalg.norm(v); return float(u@v/(a*b)) if a and b else 0.0
def blockvec(lo,hi):
    seg=[VVx[t] for t in range(max(0,lo),min(n,hi))]; return np.mean(seg,0) if seg else np.zeros(100)
W=3; Wt=4
def btf(lo,hi):
    c=Counter()
    for t in range(max(0,lo),min(n,hi)):
        for x in roots[t]:
            if x in vi: c[x]+=1
    return c
def ctf(a,b):
    cm=set(a)&set(b); num=sum(a[x]*b[x] for x in cm); na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values())); return num/(na*nb) if na and nb else 0.0
rhyme=[ (tok[i][-1][-2:] if tok[i] else "") for i in range(n)]
def has2p(i): return 1.0 if any(t.endswith("ك") or t.endswith("کم") or t.endswith("کن") or t in ("انت","انتم","انتما") for t in tok[i]) else 0.0
H2=[has2p(i) for i in range(n)]
OPEN={"قل","یا","الم","الر","حم","طه","یس","ص","ق","ن","سبح","یسبح","الحمد","تبارک","ویل","إذا","عبس","اقرا","ال","ألم","أرءیت"}
DIV={"ءله","رحم","غفر","عزز","حکم","علم","ربب","قدر","کبر","حمد","سمع","بصر"}
def feats(i):
    emb=1-cos(VVx[i],VVx[i+1])
    embtile=1-cos(blockvec(i-Wt+1,i+1), blockvec(i+1,i+1+Wt))
    tile=1-ctf(btf(i-W+1,i+1), btf(i+1,i+1+W))
    rh=1.0 if rhyme[i]!=rhyme[i+1] else 0.0
    run=0
    for q in range(i,-1,-1):
        if rhyme[q]==rhyme[i]: run+=1
        else: break
    runf=min(run,25)/25.0
    lj=abs(len(roots[i])-len(roots[i+1]))/(len(roots[i])+len(roots[i+1])+1)
    prev=[len(roots[t]) for t in range(max(0,i-3),i+1)]; pm=sum(prev)/len(prev)
    lenwin=abs(len(roots[i+1])-pm)/(pm+1)
    p2=abs(H2[i+1]-H2[i])
    first=tok[i+1][0] if tok[i+1] else ""; op=1.0 if first in OPEN else 0.0
    dv=sum(1 for x in roots[i] if x in DIV)/(len(roots[i])+1)
    return [emb,embtile,tile,rh,runf,lj,lenwin,p2,op,dv]
NAMES=["emb","embtile","tile","rhyme","rhyme_run","len_jump","len_win","p2_shift","opener","divname"]
X=np.array([feats(i) for i in range(G)]); y=np.array([1.0 if sura[i]!=sura[i+1] else 0.0 for i in range(G)])
nb=int(y.sum()); X=(X-X.mean(0))/(X.std(0)+1e-9)
def cvlog(Xf,folds=5):
    idx=np.arange(G); np.random.shuffle(idx); oof=np.zeros(G); wp=(G-nb)/nb
    for f in range(folds):
        te=idx[f::folds]; tr=np.setdiff1d(idx,te)
        Xt=np.c_[np.ones(len(tr)),Xf[tr]]; yt=y[tr]; w=np.ones(len(tr)); w[yt==1]=wp; beta=np.zeros(Xt.shape[1])
        for _ in range(250):
            p=1/(1+np.exp(-Xt@beta)); g=Xt.T@(w*(p-yt))/len(tr); Hh=(Xt.T*(w*p*(1-p)))@Xt/len(tr)+1e-4*np.eye(Xt.shape[1]); beta-=np.linalg.solve(Hh,g)
        Xe=np.c_[np.ones(len(te)),Xf[te]]; oof[te]=1/(1+np.exp(-Xe@beta))
    return oof,beta
import bisect
def ev(oof,nm):
    bi=set(np.where(y==1)[0]); sw=sorted(oof[i] for i in range(G) if y[i]==0); sb=[oof[i] for i in range(G) if y[i]==1]
    A=sum(bisect.bisect_left(sw,v)+(bisect.bisect_right(sw,v)-bisect.bisect_left(sw,v))/2 for v in sb)/(len(sb)*len(sw))
    order=sorted(range(G),key=lambda i:-oof[i]); rec=len(set(order[:nb])&bi)/nb; best=0
    for t in np.quantile(oof,np.linspace(0.5,0.999,150)):
        pred=set(i for i in range(G) if oof[i]>=t)
        if pred:
            tp=len(pred&bi); P=tp/len(pred); Rc=tp/nb; F=2*P*Rc/(P+Rc) if P+Rc else 0; best=max(best,F)
    opt=st.mean(sorted(oof,reverse=True)[:nb]); canon=st.mean(oof[i] for i in bi); rnd=st.mean(oof); g=(opt-canon)/(opt-rnd+1e-9)
    print(f"  [{nm}] CV-AUC={A:.3f} rec@113={rec:.0%} bestF1={best:.2f} g_seg={g:.2f}"); return A
of,beta=cvlog(X); print("FULL (10 modes):"); ev(of,"full")
print("  coef:",{NAMES[k]:round(float(beta[k+1]),2) for k in range(len(NAMES))})
intr=[0,1,2,3,4,5,6,7]  # exclude opener,divname
ofi,_=cvlog(X[:,intr]); print("INTRINSIC-only (8 modes, no opener/divname):"); ev(ofi,"intrinsic")
print("DONE")
