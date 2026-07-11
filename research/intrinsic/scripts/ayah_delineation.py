# -*- coding: utf-8 -*-
"""GLOBAL āyah delineation (all 6236 verses): can label-free modalities recover WHERE verse boundaries fall in
each sūra's FROZEN word stream (no reordering)? Modalities: rhyme-match to sūra's dominant fāṣila (top1/top2 final
bigram, trigram), pausal end-letter, next-word-waw, word length, relative position. 5-fold CV logistic + GREEDY
forward selection -> minimal high-value modality set. MEASURED on rasm."""
import openpyxl, math, statistics as st
import numpy as np
from collections import Counter, defaultdict
np.random.seed(17)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
# per-sura ordered list of (word, is_verse_end)
sera=defaultdict(list)
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    toks=[t for t in str(r[10] or "").split() if t]
    for k,w in enumerate(toks):
        sera[s].append((w, k==len(toks)-1))   # True if last word of this āyah
PAUSAL=set("اىينمربدلهوقعكست")
feats=[]; ys=[]
for s,seq in sera.items():
    words=[w for w,_ in seq]
    end2=Counter(w[-2:] for w in words if len(w)>=2); end3=Counter(w[-3:] for w in words if len(w)>=3)
    top2=set([x for x,_ in end2.most_common(2)]); top1=set([x for x,_ in end2.most_common(1)]); t3=set([x for x,_ in end3.most_common(1)])
    L=len(words)
    for i,(w,isend) in enumerate(seq):
        if i==L-1: continue                     # last gap of sura = sura boundary, not an internal verse cut
        nxt=seq[i+1][0]
        f=[1.0 if w[-2:] in top1 else 0.0,      # rhyme top-1 bigram
           1.0 if w[-2:] in top2 else 0.0,      # rhyme top-2
           1.0 if (len(w)>=3 and w[-3:] in t3) else 0.0,  # rhyme top-1 trigram
           1.0 if (w and w[-1] in PAUSAL) else 0.0,       # pausal end-letter
           1.0 if nxt.startswith("و") else 0.0,           # next word starts with waw
           float(len(w)),                                  # word length
           i/max(1,L-1)]                                    # relative position
        feats.append(f); ys.append(1.0 if isend else 0.0)
X=np.array(feats); y=np.array(ys); G=len(y); nb=int(y.sum())
names=["rhyme_top1","rhyme_top2","rhyme3","pausal","next_waw","wlen","relpos"]
X=(X-X.mean(0))/(X.std(0)+1e-9)
def cv_auc(cols):
    Xf=X[:,cols]; idx=np.arange(G); np.random.shuffle(idx); oof=np.zeros(G); wpos=(G-nb)/nb
    for f in range(5):
        te=idx[f::5]; tr=np.setdiff1d(idx,te)
        Xt=np.c_[np.ones(len(tr)),Xf[tr]]; yt=y[tr]; w=np.ones(len(tr)); w[yt==1]=wpos; beta=np.zeros(Xt.shape[1])
        for _ in range(30):
            p=1/(1+np.exp(-np.clip(Xt@beta,-30,30))); g=Xt.T@(w*(p-yt))/len(tr)
            H=(Xt.T*(w*p*(1-p)))@Xt/len(tr)+1e-4*np.eye(Xt.shape[1]); beta-=np.linalg.solve(H,g)
        Xe=np.c_[np.ones(len(te)),Xf[te]]; oof[te]=1/(1+np.exp(-np.clip(Xe@beta,-30,30)))
    import bisect; sw=sorted(oof[y==0]); sb=oof[y==1]
    A=sum(bisect.bisect_left(sw,v)+(bisect.bisect_right(sw,v)-bisect.bisect_left(sw,v))/2 for v in sb)/(len(sb)*len(sw))
    order=np.argsort(-oof); rec=y[order[:nb]].sum()/nb
    best=0
    for t in np.quantile(oof,np.linspace(0.3,0.999,40)):
        pred=oof>=t; tp=y[pred].sum()
        if pred.sum()==0: continue
        P=tp/pred.sum(); Rc=tp/nb; F=2*P*Rc/(P+Rc) if P+Rc else 0; best=max(best,F)
    return A,rec,best
import sys
print("word-gaps:",G," verse-end gaps:",nb,f" (base rate {nb/G:.1%})")
print("single-modality CV-AUC:")
for c in range(len(names)):
    A,rec,F=cv_auc([c]); print(f"  {names[c]:11} AUC={A:.3f} rec={rec:.0%} F1={F:.2f}")
# greedy forward selection
chosen=[]; rem=list(range(len(names))); prevA=0.5
print("greedy forward selection (stop when ΔAUC<0.01):")
while rem:
    best=None
    for c in rem:
        A,_,_=cv_auc(chosen+[c])
        if best is None or A>best[1]: best=(c,A)
    if best[1]-prevA<0.01 and chosen: break
    chosen.append(best[0]); rem.remove(best[0]); 
    A,rec,F=cv_auc(chosen); print(f"  + {names[best[0]]:11} -> AUC={A:.3f} rec={rec:.0%} F1={F:.2f}"); prevA=best[1]
Afull,recf,Ff=cv_auc(list(range(len(names))))
print(f"ALL features: AUC={Afull:.3f} rec={recf:.0%} F1={Ff:.2f}")
print("minimal high-value set:", [names[c] for c in chosen])
print("DONE")
