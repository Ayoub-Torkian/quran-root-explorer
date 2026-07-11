# -*- coding: utf-8 -*-
"""#1: do REFERENT-emergence features crack the within-Medinan ordering (Phase-1 failure)?
Two non-overfit tests: (a) principled composite (referent weighted by its CORPUS median-nuzul, derived
independently of the within-Medinan target); (b) regularized Ridge LOO. Both vs shuffle null + style-only."""
import openpyxl, numpy as np
from collections import defaultdict
from scipy.stats import spearmanr
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
A=[]
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    A.append(dict(su=su,ay=ay,nuzul=int(row[12]),roots=[norm(r) for r in (row[8]or'').split()],
                  toks=[norm(t) for t in (row[9]or'').split()],surf=[norm(t) for t in (row[10]or'').split()]))
MED={2,3,4,5,8,9,13,22,24,33,47,48,49,57,58,59,60,61,62,63,64,65,66,98,110}  # cleaned (drop disputed 55,76,99)
def hs(s,seq):
    L=len(seq)
    return any(s[i:i+L]==seq for i in range(len(s)-L+1))
def refs(d):
    g=set();s=d['surf'];tk=d['toks']
    def lem(*p): return any(any(t.startswith(x) for x in p) for t in tk)
    if hs(s,['الذین','امن']) or lem('مؤمن','مومن','مسلم'): g.add('believers')
    if hs(s,['الذین','کفر']) or lem('کافر') or 'کفار' in tk: g.add('disbelievers')
    if lem('منافق') or hs(s,['الذین','نافق']) or hs(s,['قلوب','هم','مرض']): g.add('hypocrites')
    if hs(s,['الذین','اشرک']) or lem('مشرک'): g.add('polytheists')
    if hs(s,['اهل','ال','کتاب']) or hs(s,['الذین','اوت','ال','کتاب']) or hs(s,['الذین','هاد']) or lem('یهود','نصار'): g.add('people_of_book')
    if hs(s,['الذین','کذب']) or lem('مکذب','مستکبر') or hs(s,['الذین','استکبر']): g.add('meccan_deniers')
    if lem('جهد') or lem('قتل'): g.add('jihad_qital')
    if lem('عیسی','عیس'): g.add('jesus')
    return g
# corpus median-nuzul per referent (independent weight)
occ=defaultdict(list)
for d in A:
    for g in refs(d): occ[g].append(d['nuzul'])
medn={g:np.median(v) for g,v in occ.items()}
print("referent corpus median-nuzul (weights):",{g:int(m) for g,m in sorted(medn.items(),key=lambda t:t[1])})
# per-sura features
suras=defaultdict(list)
for d in A: suras[d['su']].append(d)
def feats(su):
    ay=suras[su]; n=len(ay); allr=[r for d in ay for r in d['roots']]; nr=max(1,len(allr))
    ref_counts=defaultdict(int)
    for d in ay:
        for g in refs(d): ref_counts[g]+=1
    f={g:ref_counts[g]/n for g in medn}
    f['mean_len']=np.mean([len(d['surf']) for d in ay])
    return f,ref_counts,n
# composite lateness score = mention-weighted mean of referent corpus-median-nuzul
def composite(su):
    f,rc,n=feats(su); num=den=0
    for g,c in rc.items(): num+=c*medn[g]; den+=c
    return num/den if den else np.nan
medlist=sorted(MED)
comp=np.array([composite(s) for s in medlist]); truth=np.array([ [d['nuzul'] for d in suras[s]][0] for s in medlist])
rho_c=spearmanr(comp,truth).correlation
print(f"\n(a) PRINCIPLED COMPOSITE within-Medinan (n={len(medlist)}): Spearman={rho_c:.3f}")
# shuffle null for composite
rng=np.random.default_rng(0); nl=[spearmanr(comp,rng.permutation(truth)).correlation for _ in range(2000)]
print(f"    shuffle null: mean={np.mean(nl):.3f}  95pct={np.percentile(nl,95):.3f}  p={(np.sum(np.array(nl)>=rho_c)+1)/2001:.3f}")
# (b) regularized Ridge LOO with referent features + style
keys=sorted(medn)+['mean_len']
X=np.array([[feats(s)[0][k] for k in keys] for s in medlist]); y=truth
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from sklearn.model_selection import LeaveOneOut,cross_val_predict
from sklearn.pipeline import make_pipeline
ridge=make_pipeline(StandardScaler(),RidgeCV(alphas=np.logspace(0,4,30)))
pred=cross_val_predict(ridge,X,y,cv=LeaveOneOut()); rho_r=spearmanr(pred,y).correlation
print(f"(b) RIDGE LOO (referent+style) within-Medinan: Spearman={rho_r:.3f}")
# style-only baseline within-Medinan
Xs=np.array([[feats(s)[0]['mean_len']] for s in medlist])
preds=cross_val_predict(ridge,Xs,y,cv=LeaveOneOut()); print(f"    style-only (mean_len) baseline: Spearman={spearmanr(preds,y).correlation:.3f}")
# also confirm referent features help on ALL 114 and within-Meccan
allk=sorted(suras); Xa=np.array([[feats(s)[0][k] for k in keys] for s in allk]); ya=np.array([[d['nuzul'] for d in suras[s]][0] for s in allk])
pa=cross_val_predict(ridge,Xa,ya,cv=LeaveOneOut()); print(f"\nALL 114 (referent+style) Spearman={spearmanr(pa,ya).correlation:.3f}")
