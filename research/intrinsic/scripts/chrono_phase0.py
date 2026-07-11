# -*- coding: utf-8 -*-
"""PHASE 0: internal Meccan/Medinan classifier from rasm/morphology ONLY (ONE-LAW admissible).
Held-out validation = traditional Medinan sura list (external [REPORT], used to SCORE only, never as a feature)."""
import openpyxl, numpy as np
from collections import defaultdict
R="."
wb=openpyxl.load_workbook(f"{R}/Book6.xlsx",read_only=True); ws=wb['Sheet1']
rows=defaultdict(list); nuzul={}; names={}
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    d=dict(roots=(row[8]or'').split(),surf=(row[10]or'').split())
    rows[su].append(d); nuzul[su]=row[12]; names[su]=row[7]

# --- traditional Medinan gold (Egyptian standard; disputed: 13,55,76,98,99) ---
MED={2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110}

# --- community/legal roots (Medinan-leaning content), all from the rasm root column ---
LEGAL={'نفق','جهد','قتل','ربو','طلق','نکح','یتم','وصی','حدد','غنم','اسر','صدق','زکو','حلل','حرم',
       'شهد','عقد','کتب','جزی','عذر','صوم','صیم','حجج','قصص','دین','فرض','میراث','ورث'}
def vocative(surf,target):
    # contiguous 'أی','ها', then target-token sequence
    for i in range(len(surf)-2):
        if surf[i]=='أی' and surf[i+1]=='ها':
            tail=surf[i+2:i+4]
            if target=='believers' and surf[i+2]=='الذین': return True
            if target=='nas' and tail[:2]==['ال','ناس']: return True
    return False

feat={}; 
for su,ayat in rows.items():
    n=len(ayat)
    toklens=[len(a['surf']) for a in ayat]
    allroots=[r for a in ayat for r in a['roots']]
    nr=max(1,len(allroots))
    f={}
    f['mean_ayah_len']=float(np.mean(toklens))
    f['med_ayah_len']=float(np.median(toklens))
    f['believer_addr']=sum(vocative(a['surf'],'believers') for a in ayat)/n
    f['nas_addr']=sum(vocative(a['surf'],'nas') for a in ayat)/n
    f['legal_density']=sum(r in LEGAL for r in allroots)/nr
    f['has_munafiq']=1.0 if 'نفق' in allroots and sum(r=='نفق' for r in allroots)>=1 else 0.0
    f['allah_density']=sum(r in ('اله','الله') for r in allroots)/nr  # الله lemma often 'اله'
    feat[su]=f
keys=['mean_ayah_len','med_ayah_len','believer_addr','nas_addr','legal_density','has_munafiq','allah_density']
sus=sorted(feat)
X=np.array([[feat[s][k] for k in keys] for s in sus])
y=np.array([1 if s in MED else 0 for s in sus])
print("suras:",len(sus),"| Medinan gold:",int(y.sum()),"Meccan:",int((1-y).sum()))

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, accuracy_score, confusion_matrix
pipe=make_pipeline(StandardScaler(),LogisticRegression(max_iter=2000,class_weight='balanced'))
loo=LeaveOneOut()
prob=cross_val_predict(pipe,X,y,cv=loo,method='predict_proba')[:,1]
pred=(prob>=0.5).astype(int)
auc=roc_auc_score(y,prob); acc=accuracy_score(y,pred)
cm=confusion_matrix(y,pred)
print(f"\nLOO-CV  AUC={auc:.3f}  ACC={acc:.3f}")
print("confusion [ [TN FP],[FN TP] ]:\n",cm)
# feature direction (fit on all)
pipe.fit(X,y); coef=pipe.named_steps['logisticregression'].coef_[0]
print("\nstandardized coefficients (toward Medinan):")
for k,c in sorted(zip(keys,coef),key=lambda t:-abs(t[1])): print(f"  {k:16s} {c:+.2f}")
# misclassified suras
print("\nmisclassified:")
for s,p,pr in zip(sus,pred,prob):
    if p!=(1 if s in MED else 0):
        print(f"  {s:3d} {names[s]:18s} gold={'M' if s in MED else 'm'} pred_p={pr:.2f} nuzul={nuzul[s]}")
