# -*- coding: utf-8 -*-
"""Instrument 5: DIRECTED multimodal āyah-order recovery (direction KEPT, no reflection). Tests whether a GLOBAL
content->position principle recovers the canonical order, and NAMES which directed modalities carry it.
Modalities (all rasm, content-derived, non-positional):
 f1 generality (given->new: mean log-df of roots, general early)   f2 specificity (frac rare roots, new/elaboration late)
 f3 definiteness (frac ال-tokens, resolved referents later)        f4 connective opener (ف/ثم consequent-late, و mid)
 f5 length (rhetorical contour)                                    f6 reuse-flow (pairwise: the āyah ADDING more unshared roots comes later)
Recovery: ridge regression of within-sūra normalized rank on features, 5-fold CV BY SŪRA (no leakage), sort
predicted -> directed Kendall τ vs canonical. Greedy forward-selection (parsimony). Nulls: undirected baseline
+0.16, order-permutation (~0), single-feature. MEASURED."""
import numpy as np, statistics as st, openpyxl
from collections import Counter
np.random.seed(7)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]; rasm=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(str(r[8] or "").split()); rasm.append(str(r[10] or "").split())
n=len(sura)
df=Counter()
for rr in roots:
    for x in set(rr): df[x]+=1
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def starts(w,p): return w.startswith(p)
f1=np.zeros(n); f2=np.zeros(n); f3=np.zeros(n); f4=np.zeros(n); f5=np.zeros(n); f6=np.zeros(n)
for i in range(n):
    rr=roots[i]; ww=rasm[i]
    f1[i]=np.mean([np.log1p(df[x]) for x in rr]) if rr else 0.0
    f2[i]=np.mean([df[x]<=3 for x in rr]) if rr else 0.0
    f3[i]=np.mean([starts(w,"ال") for w in ww]) if ww else 0.0
    fw=ww[0] if ww else ""
    f4[i]= 1.0 if (starts(fw,"ف") or fw=="ثم") else (0.3 if starts(fw,"و") else 0.0)
    f5[i]=len(ww)
# f6 reuse-flow: within sūra pairwise net precedence
for s,(a,b) in bounds.items():
    L=b-a; sets=[set(roots[a+k]) for k in range(L)]
    sc=np.zeros(L)
    for x in range(L):
        for y in range(x+1,L):
            sh=sets[x]&sets[y]
            if sh:
                ux=len(sets[x]-sets[y]); uy=len(sets[y]-sets[x])
                v=np.sign(uy-ux)  # the one adding more unshared roots tends later -> earlier index precedes
                sc[x]+=v; sc[y]-=v
    f6[a:b]=sc
F={"f1_general":f1,"f2_specific":f2,"f3_definite":f3,"f4_connective":f4,"f5_length":f5,"f6_reuseflow":f6}
# target: within-sūra normalized rank
y=np.zeros(n)
for s,(a,b) in bounds.items():
    L=b-a
    if L>1:
        y[a:b]=np.arange(L)/(L-1)
# standardize features globally
Z={k:(v-v.mean())/(v.std()+1e-9) for k,v in F.items()}
suras=[s for s,(a,b) in bounds.items() if b-a>=4]
np.random.shuffle(suras); folds=[suras[i::5] for i in range(5)]
def kendall(a,b):
    L=len(a); ra={v:i for i,v in enumerate(a)}; rb={v:i for i,v in enumerate(b)}; c=di=0
    for i in range(L):
        for j in range(i+1,L):
            sgn=(ra[a[i]]-ra[a[j]])*(rb[a[i]]-rb[a[j]])
            if sgn>0:c+=1
            elif sgn<0:di+=1
    return (c-di)/(c+di) if (c+di) else 0.0
def cv_tau(feats, perm=False):
    taus=[]
    for fo in range(5):
        test=set(folds[fo]); train=[s for s in suras if s not in test]
        Xtr=[]; ytr=[]
        for s in train:
            a,b=bounds[s]
            for k in range(b-a): Xtr.append([Z[f][a+k] for f in feats]); ytr.append(y[a+k])
        Xtr=np.array(Xtr); ytr=np.array(ytr)
        A=Xtr.T@Xtr+1e-2*np.eye(len(feats)); w=np.linalg.solve(A,Xtr.T@ytr)
        for s in test:
            a,b=bounds[s]; L=b-a
            pred=np.array([[Z[f][a+k] for f in feats] for k in range(L)])@w
            can=list(range(L))
            if perm:
                pr=can[:]; np.random.shuffle(pr); order=list(np.argsort([pred[k] for k in pr]))
                order=[pr[o] for o in order]
            else: order=list(np.argsort(pred+1e-6*np.random.randn(L)))
            taus.append(kendall(order,can))
    return st.mean(taus), 100*sum(t>=0.5 for t in taus)/len(taus)
print("=== Instrument 5: directed multimodal āyah-order recovery (direction kept) ===")
print("single-modality directed τ (CV by sūra):")
singles=[]
for f in F:
    t,_=cv_tau([f]); singles.append((t,f)); print(f"  {f:14s} τ={t:+.3f}")
# greedy forward selection
chosen=[]; rem=list(F); best=-9
while rem:
    cand=[]
    for f in rem:
        t,_=cv_tau(chosen+[f]); cand.append((t,f))
    cand.sort(reverse=True)
    if cand[0][0]>best+0.005:
        best=cand[0][0]; chosen.append(cand[0][1]); rem.remove(cand[0][1])
    else: break
tau_full,pct=cv_tau(chosen)
tau_perm,_=cv_tau(chosen,perm=True)
print(f"\nPARSIMONIOUS set (forward-selected): {chosen}")
print(f"  directed τ = {tau_full:+.3f} | {pct:.0f}% of sūras τ>=0.5 | permutation-null τ = {tau_perm:+.3f} | undirected baseline +0.16")
# fitted weights on full data
Xall=[]; yall=[]
for s in suras:
    a,b=bounds[s]
    for k in range(b-a): Xall.append([Z[f][a+k] for f in chosen]); yall.append(y[a+k])
Xall=np.array(Xall); yall=np.array(yall)
w=np.linalg.solve(Xall.T@Xall+1e-2*np.eye(len(chosen)),Xall.T@yall)
print("  fitted directed weights (sign=direction; +=>later in sūra):")
for f,wt in sorted(zip(chosen,w),key=lambda z:-abs(z[1])): print(f"    {f:14s} {wt:+.3f}")
a,b=bounds[108]; L=b-a
pred=np.array([[Z[f][a+k] for f in chosen] for k in range(L)])@w
print(f"al-Kawthar(108): predicted order {list(np.argsort(pred))} vs canonical {list(range(L))}")
print("DONE")
