# -*- coding: utf-8 -*-
"""PHASE 1: seriate suras by INTERNAL features (style + referent densities) and validate the recovered
ORDER against Book6 revelation order (nuzul, col12) = held-out gold. ONE-LAW: features internal only.
Key question: is there a FINER-than-binary chronological signal (order WITHIN Meccan, WITHIN Medinan)?"""
import openpyxl, numpy as np
from collections import defaultdict
from scipy.stats import spearmanr
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
rows=defaultdict(list); nuzul={}; names={}
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    rows[su].append(dict(roots=[norm(r) for r in (row[8]or'').split()],surf=[norm(t) for t in (row[10]or'').split()]))
    nuzul[su]=int(row[12]); names[su]=row[7]
MED={2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110}
LEGAL=set(map(norm,['نفق','جهد','قتل','ربو','طلق','نکح','یتم','وصی','حدد','غنم','اسر','صدق','زکو','حلل','حرم','شهد','عقد','جزی','صوم','حجج','دین','فرض','ورث']))
ESCH=set(map(norm,['قیم','بعث','جنن','نور','نار','حسب','وزن','صور','جهنم','فرد','زلزل','قرع','صخخ']))  # eschatology (Meccan-heavy)
def vocative(surf,t):
    for i in range(len(surf)-2):
        if surf[i]=='ای' and surf[i+1]=='ها':
            if t=='bel' and i+2<len(surf) and surf[i+2]=='الذین': return True
            if t=='nas' and surf[i+2:i+4]==['ال','ناس']: return True
    return False
def dens(allr,roots): return sum(r in roots for r in allr)/max(1,len(allr))
feat={}
for su,ayat in rows.items():
    n=len(ayat); allr=[r for a in ayat for r in a['roots']]; nr=max(1,len(allr))
    feat[su]=dict(
      mean_len=np.mean([len(a['surf']) for a in ayat]),
      bel=sum(vocative(a['surf'],'bel') for a in ayat)/n,
      nas=sum(vocative(a['surf'],'nas') for a in ayat)/n,
      legal=dens(allr,LEGAL), esch=dens(allr,ESCH),
      munafiq=sum(r=='نفق' for r in allr)/nr,        # referent: hypocrites (late)
      kafir=sum(r=='کفر' for r in allr)/nr,           # referent: disbelievers
      mushrik=sum(r=='شرک' for r in allr)/nr,         # referent: polytheists (Meccan)
      kitab=sum(r=='کتب' for r in allr)/nr,           # ahl al-kitab proxy
      jihad=sum(r=='جهد' for r in allr)/nr,
      allah=sum(r in('اله','الله') for r in allr)/nr,
      rahman=sum(r=='رحم' for r in allr)/nr)
keys=['mean_len','bel','nas','legal','esch','munafiq','kafir','mushrik','kitab','jihad','allah','rahman']
sus=sorted(feat); X=np.array([[feat[s][k] for k in keys] for s in sus]); ny=np.array([nuzul[s] for s in sus])
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import LeaveOneOut,cross_val_predict
from sklearn.pipeline import make_pipeline
def evalmodel(name,model,X,ny,idx=None):
    pred=cross_val_predict(model,X,ny,cv=LeaveOneOut())
    rho=spearmanr(pred,ny).correlation
    # pairwise concordance (Kendall-based): fraction of sura-pairs ordered correctly
    from itertools import combinations
    c=t=0
    for i,j in combinations(range(len(ny)),2):
        if ny[i]==ny[j]:continue
        t+=1; c+= (pred[i]-pred[j])*(ny[i]-ny[j])>0
    print(f"  {name:14s} Spearman={rho:.3f}  pairwise={c/t:.3f}  (n={len(ny)})")
    return pred,rho
ridge=make_pipeline(StandardScaler(),RidgeCV(alphas=np.logspace(-2,3,30)))
gbr=GradientBoostingRegressor(n_estimators=200,max_depth=2,learning_rate=0.05,subsample=0.8,random_state=0)
print("=== ALL 114 suras: predict nuzul rank from internal features (LOO out-of-sample) ===")
predR,rhoR=evalmodel("Ridge",ridge,X,ny)
predG,rhoG=evalmodel("GradBoost",gbr,X,ny)
# shuffle null
rng=np.random.default_rng(0); nulls=[]
for _ in range(200):
    ys=rng.permutation(ny); nulls.append(spearmanr(cross_val_predict(ridge,X,ys,cv=5),ys).correlation)
nulls=np.array(nulls); print(f"  shuffle-null Spearman: mean={np.nanmean(nulls):.3f} 95pct={np.nanpercentile(nulls,95):.3f}")
# FINER test: within-Meccan and within-Medinan ordering (the hard, beyond-binary signal)
for label,mask in [("Meccan-only",~np.isin(sus,list(MED))),("Medinan-only",np.isin(sus,list(MED)))]:
    Xm=X[mask]; nym=ny[mask]
    pr=cross_val_predict(ridge,Xm,nym,cv=LeaveOneOut()); rho=spearmanr(pr,nym).correlation
    print(f"=== {label}: n={mask.sum()}  within-class Spearman={rho:.3f}")
