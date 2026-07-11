# -*- coding: utf-8 -*-
"""Multimodal feature-impact + PARSIMONY for boundary recovery, both units:
(A) SŪRA boundaries (āyah-gaps), (B) ĀYAH boundaries (word-gaps, all 6236 āyāt). Rank each modality by
standalone CV-AUC; forward-select the minimal high-value set. Rasm-grounded. MEASURED."""
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
n=len(sura)
def auc(score,y):
    import bisect; sw=sorted(score[i] for i in range(len(y)) if y[i]==0); sb=[score[i] for i in range(len(y)) if y[i]==1]
    if not sw or not sb: return 0.5
    return sum(bisect.bisect_left(sw,v)+(bisect.bisect_right(sw,v)-bisect.bisect_left(sw,v))/2 for v in sb)/(len(sb)*len(sw))
def cv_auc(X,y,cols,folds=4):
    m=len(y); idx=np.arange(m); np.random.shuffle(idx); oof=np.zeros(m); nb=int(y.sum()); wp=(m-nb)/max(nb,1)
    Xs=X[:,cols] if cols else np.zeros((m,1))
    for f in range(folds):
        te=idx[f::folds]; tr=np.setdiff1d(idx,te)
        Xt=np.c_[np.ones(len(tr)),Xs[tr]]; yt=y[tr]; w=np.ones(len(tr)); w[yt==1]=wp; beta=np.zeros(Xt.shape[1])
        for _ in range(60):
            p=1/(1+np.exp(-np.clip(Xt@beta,-30,30))); g=Xt.T@(w*(p-yt))/len(tr)
            H=(Xt.T*(w*p*(1-p)))@Xt/len(tr)+1e-3*np.eye(Xt.shape[1])
            beta-=np.linalg.solve(H,g)
        Xe=np.c_[np.ones(len(te)),Xs[te]]; oof[te]=1/(1+np.exp(-np.clip(Xe@beta,-30,30)))
    return auc(oof,y)
def analyze(X,y,names,title):
    X=(X-X.mean(0))/(X.std(0)+1e-9)
    print(f"\n=== {title}  (n={len(y)}, positives={int(y.sum())}) ===")
    singles=sorted(((cv_auc(X,y,[k]),names[k]) for k in range(len(names))), reverse=True)
    print("  standalone CV-AUC:", " · ".join(f"{nm} {a:.3f}" for a,nm in singles))
    full=cv_auc(X,y,list(range(len(names))))
    chosen=[]; cur=0.5; curve=[]
    rem=list(range(len(names)))
    while rem:
        best=None
        for k in rem:
            a=cv_auc(X,y,chosen+[k])
            if best is None or a>best[0]: best=(a,k)
        gain=best[0]-cur
        if gain<0.005 and chosen: break
        chosen.append(best[1]); cur=best[0]; rem.remove(best[1]); curve.append((names[best[1]],round(cur,3),round(gain,3)))
    print("  forward selection:", " → ".join(f"+{nm}({a})" for nm,a,g in curve))
    print(f"  MINIMAL set = [{', '.join(names[c] for c in chosen)}]  AUC={cur:.3f}  vs FULL({len(names)}) AUC={full:.3f}")
    return chosen,cur,full

# ---------- (A) SŪRA boundaries (āyah-gaps) ----------
G=n-1
OPEN={"قل","یا","الم","الر","حم","طه","یس","ص","ق","ن","سبح","یسبح","الحمد","تبارک","ویل","إذا","عبس","اقرا","ال"}
DIV={"ءله","رحم","غفر","عزز","حکم","علم","ربب","قدر","رحیم","کبر","حمد"}
PRON1={"نحن","انا","انی","نا"}; PRON2={"انت","انتم","ک","کم","تو"}
def jac(a,b):
    u=set(a)|set(b); return len(set(a)&set(b))/len(u) if u else 0.0
def block(lo,hi):
    s=set()
    for t in range(max(0,lo),min(n,hi)): s|=set(roots[t])
    return s
fA=[]; yA=[]
for i in range(G):
    last=tok[i][-1] if tok[i] else ""; nxt0=tok[i+1][0] if tok[i+1] else ""; nxtlast=tok[i+1][-1] if tok[i+1] else ""
    tile=1-jac(block(i-2,i+1),block(i+1,i+4))
    rhy=1.0 if last[-2:]!=nxtlast[-2:] else 0.0
    lj=abs(len(roots[i])-len(roots[i+1]))/(len(roots[i])+len(roots[i+1])+1)
    op=1.0 if nxt0 in OPEN else 0.0
    dv=sum(1 for x in roots[i] if x in DIV)/(len(roots[i])+1)
    # NEW modalities:
    short=1.0 if len(roots[i])<=4 else 0.0                       # closing short verse
    conj=1.0 if nxt0 in {"و","فـ","ف","ثم","إن","ان","بل","قل","یا"} else 0.0   # discourse opener
    fA.append([tile,rhy,lj,op,dv,short,conj]); yA.append(1.0 if sura[i]!=sura[i+1] else 0.0)
analyze(np.array(fA),np.array(yA),["tile","rhyme","lenjump","opener","divname","shortclose","conj"],"A · SŪRA boundaries")

# ---------- (B) ĀYAH boundaries (word-gaps) ----------
# build word stream + per-sura rhyme class (modal last-2 of ayah-final words) + mean ayah word-length
from collections import Counter, defaultdict
words=[]; wsura=[]; wend=[]; ayidx=[]
for i in range(n):
    T=tok[i]; 
    for j,wd in enumerate(T):
        words.append(wd); wsura.append(sura[i]); wend.append(1 if j==len(T)-1 else 0); ayidx.append(i)
W=len(words)
rhyme_class=defaultdict(Counter); alen=defaultdict(list)
for i in range(n):
    if tok[i]:
        rhyme_class[sura[i]][tok[i][-1][-2:]]+=1; alen[sura[i]].append(len(tok[i]))
rc={s:rhyme_class[s].most_common(1)[0][0] for s in rhyme_class}
ml={s:(sum(alen[s])/len(alen[s])) for s in alen}
CONN={"و","فـ","ف","ثم","إن","ان","قل","یا","الذ","الذین","بل","لا","ما"}
# gaps = after each word except the very last word of corpus
fB=[]; yB=[]
since=0
for k in range(W-1):
    wd=words[k]; nxt=words[k+1]; s=wsura[k]
    since+=1
    rhy=1.0 if wd[-2:]==rc.get(s,"") else 0.0                    # fāṣila/rhyme match
    morph=1.0 if (wd[-1:] in {"ن","ا","ه","ی","و","م"} or wd[-2:] in {"ون","ین","ها","ات","کم","هم"}) else 0.0
    rhythm=since/ (ml.get(s,10)+1e-9)                            # length rhythm (words since last end / typical)
    conj=1.0 if nxt in CONN else 0.0                             # next word a connective/opener
    wl=len(wd)/8.0                                               # word length
    boundary=1.0 if wend[k]==1 else 0.0
    fB.append([rhy,morph,rhythm,conj,wl]); yB.append(boundary)
    if wend[k]==1: since=0
analyze(np.array(fB),np.array(yB),["rhyme","endmorph","rhythm","conjnext","wordlen"],"B · ĀYAH boundaries (word-gaps)")
print("\nDONE")
