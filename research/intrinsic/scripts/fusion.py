# -*- coding: utf-8 -*-
"""COMPOSITE vs MULTIMODAL FUSION, back to back. Modalities (all internal): style, referent-emergence,
prophet-deployment, deontic-stance. Compare a no-fit weighted COMPOSITE vs a fitted FUSION (GradBoost).
Honest note: LOO-Ridge shrink-to-mean gives a SPURIOUS ~-1 Spearman when features carry no signal."""
import openpyxl, numpy as np
from collections import defaultdict
from scipy.stats import spearmanr
from itertools import combinations
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
A=[]
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    A.append(dict(su=su,nuzul=int(row[12]),roots=[norm(r) for r in (row[8]or'').split()],
                  toks=[norm(t) for t in (row[9]or'').split()],surf=[norm(t) for t in (row[10]or'').split()]))
MED={2,3,4,5,8,9,13,22,24,33,47,48,49,57,58,59,60,61,62,63,64,65,66,98,110}
def hs(s,seq):
    L=len(seq); return any(s[i:i+L]==seq for i in range(len(s)-L+1))
def lem(tk,*p): return any(any(t.startswith(x) for x in p) for t in tk)
PROH=set(map(norm,['رجس','نتهی']))
def refs(d):
    g=set();s=d['surf'];tk=d['toks']
    if hs(s,['الذین','امن']) or lem(tk,'مؤمن','مومن','مسلم'): g.add('believers')
    if hs(s,['الذین','کفر']) or lem(tk,'کافر') or 'کفار' in tk: g.add('disbelievers')
    if lem(tk,'منافق') or hs(s,['قلوب','هم','مرض']): g.add('hypocrites')
    if lem(tk,'مشرک'): g.add('polytheists')
    if hs(s,['اهل','ال','کتاب']) or hs(s,['الذین','هاد']) or lem(tk,'یهود','نصار'): g.add('people_of_book')
    if hs(s,['الذین','کذب']) or lem(tk,'مکذب','مستکبر'): g.add('meccan_deniers')
    return g
occ=defaultdict(list)
for d in A:
    for g in refs(d): occ[g].append(d['nuzul'])
medn={g:np.median(v) for g,v in occ.items()}
suras=defaultdict(list)
for d in A: suras[d['su']].append(d)
def feat(su):
    ay=suras[su];n=len(ay);allr=[r for d in ay for r in d['roots']];tks=[t for d in ay for t in d['toks']];nr=max(1,len(allr))
    rc=defaultdict(int)
    for d in ay:
        for g in refs(d): rc[g]+=1
    F={}
    F.update({'ref_'+g:rc[g]/n for g in medn})
    F['mean_len']=np.mean([len(d['surf']) for d in ay])
    F['legal']=sum(r in set(map(norm,['نفق','جهد','قتل','ربو','طلق','نکح','حدد','زکو','حلل','حرم','ورث'])) for r in allr)/nr
    F['jesus']=sum(t.startswith('عیس') for t in tks)/n
    F['banuisr']=sum(hs(d['surf'],['بنی','اسرائیل']) for d in ay)/n
    F['deontic']=sum(r in PROH for r in allr)/nr
    F['composite']=(sum(rc[g]*medn[g] for g in rc)/sum(rc.values())) if sum(rc.values()) else np.nan
    return F
allk=sorted(suras); FE={s:feat(s) for s in allk}
ny={s:suras[s][0]['nuzul'] for s in allk}
def pairwise(pred,truth):
    c=t=0
    for i,j in combinations(range(len(truth)),2):
        if truth[i]==truth[j]:continue
        t+=1;c+=(pred[i]-pred[j])*(truth[i]-truth[j])>0
    return c/t
# ---- COMPOSITE (no fit) ----
def comp_eval(keys):
    ks=[k for k in keys if not np.isnan(FE[k]['composite'])] if False else keys
    sub=[s for s in keys]
    comp=np.array([FE[s]['composite'] for s in sub]); tr=np.array([ny[s] for s in sub])
    m=~np.isnan(comp); comp,tr=comp[m],tr[m]
    return spearmanr(comp,tr).correlation,pairwise(comp,tr),m.sum()
rc_all,pw_all,n_all=comp_eval(allk)
rc_med,pw_med,n_med=comp_eval(sorted(MED))
print("=== (A) COMPOSITE (referent corpus-median weights, NO fitting) ===")
print(f"  ALL-114 : Spearman={rc_all:.3f} pairwise={pw_all:.3f} (n={n_all})")
print(f"  within-Medinan: Spearman={rc_med:.3f} pairwise={pw_med:.3f} (n={n_med})")
# ---- MULTIMODAL FUSION (GradBoost, LOO) ----
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import LeaveOneOut,cross_val_predict
keys=[k for k in FE[allk[0]] if k!='composite']
X=np.array([[FE[s][k] for k in keys] for s in allk]); y=np.array([ny[s] for s in allk])
gbr=GradientBoostingRegressor(n_estimators=300,max_depth=2,learning_rate=0.03,subsample=0.8,random_state=0)
pred=cross_val_predict(gbr,X,y,cv=LeaveOneOut())
print("\n=== (B) MULTIMODAL FUSION (style+referent+prophet+deontic, GradBoost LOO) ===")
print(f"  ALL-114 : Spearman={spearmanr(pred,y).correlation:.3f} pairwise={pairwise(pred,y):.3f}")
rng=np.random.default_rng(1); nl=[spearmanr(cross_val_predict(gbr,X,rng.permutation(y),cv=5),y).correlation for _ in range(40)]
print(f"  shuffle null: mean={np.mean(nl):.3f} 95pct={np.percentile(nl,95):.3f}")
# within-Medinan via fusion: rank suras by fused prediction restricted to Medinan (train on all)
gbr.fit(X,y); pm=gbr.predict(np.array([[FE[s][k] for k in keys] for s in sorted(MED)]))
print(f"  within-Medinan (fusion, ranks among Medinan): Spearman={spearmanr(pm,[ny[s] for s in sorted(MED)]).correlation:.3f}")
# feature importance
imp=sorted(zip(keys,gbr.feature_importances_),key=lambda t:-t[1])[:8]
print("  top fused features:",[(k,round(v,2)) for k,v in imp])
