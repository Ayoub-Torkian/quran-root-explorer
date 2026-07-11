# -*- coding: utf-8 -*-
"""PHASE 2: does the Meccan/Medinan signal exist at AYAH granularity? If yes, flag Meccan-like ayah
BLOCKS embedded in Medinan suras (and vice versa). Validation against a few well-attested traditional
embedded-verse reports (external [REPORT], used to CHECK only)."""
import openpyxl, numpy as np
from collections import defaultdict
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
A=defaultdict(list); nuzul={}; names={}
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    A[su].append((ay,[norm(r) for r in (row[8]or'').split()],[norm(t) for t in (row[10]or'').split()]))
    nuzul[su]=int(row[12]); names[su]=row[7]
MED={2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110}
# suras Phase-0 found ambiguous/disputed -> exclude from TRAINING (use only confident suras)
DISPUTED={6,14,16,22,28,29,34,35,42,55,76,98,99,103,109,110,13}
LEGAL=set(map(norm,['نفق','جهد','قتل','ربو','طلق','نکح','یتم','وصی','حدد','غنم','اسر','صدق','زکو','حلل','حرم','شهد','عقد','جزی','صوم','حجج','دین','فرض','ورث']))
ESCH=set(map(norm,['قیم','بعث','جنن','نور','نار','حسب','وزن','صور','زلزل','قرع']))
def vocbel(surf):
    for i in range(len(surf)-2):
        if surf[i]=='ای' and surf[i+1]=='ها' and i+2<len(surf) and surf[i+2]=='الذین': return 1
    return 0
def vocnas(surf):
    for i in range(len(surf)-3):
        if surf[i]=='ای' and surf[i+1]=='ها' and surf[i+2:i+4]==['ال','ناس']: return 1
    return 0
def afeat(roots,surf):
    nr=max(1,len(roots))
    return [len(surf), vocbel(surf), vocnas(surf),
            sum(r in LEGAL for r in roots)/nr, sum(r in ESCH for r in roots)/nr,
            sum(r=='نفق' for r in roots), sum(r=='شرک' for r in roots), sum(r=='کفر' for r in roots)]
KEYS=['len','bel','nas','legal','esch','munafiq','mushrik','kafir']
# build ayah-level dataset from CONFIDENT suras only
Xtr=[];ytr=[];grp=[]
for su,ayat in A.items():
    if su in DISPUTED: continue
    lab=1 if su in MED else 0
    for ay,roots,surf in ayat:
        Xtr.append(afeat(roots,surf)); ytr.append(lab); grp.append(su)
Xtr=np.array(Xtr,float);ytr=np.array(ytr);grp=np.array(grp)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GroupKFold,cross_val_predict
from sklearn.metrics import roc_auc_score
pipe=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced'))
# grouped CV by sura: test ayahs come from held-out suras -> honest ayah-level signal
prob=cross_val_predict(pipe,Xtr,ytr,cv=GroupKFold(10),groups=grp,method='predict_proba')[:,1]
print(f"AYAH-level (grouped-by-sura CV) AUC={roc_auc_score(ytr,prob):.3f}  n_ayat={len(ytr)}")
# fit on all confident ayahs, then scan Medinan suras for Meccan-like blocks
pipe.fit(Xtr,ytr)
def scan(su):
    ayat=A[su]; feats=np.array([afeat(r,s) for _,r,s in ayat],float)
    p=pipe.predict_proba(feats)[:,1]  # P(Medinan)
    # smoothed (3-ayah window) to find blocks
    sm=np.convolve(p,np.ones(3)/3,mode='same')
    return [(ay,round(float(pi),2),round(float(si),2)) for (ay,_,_),pi,si in zip(ayat,p,sm)]
print("\n--- scan: Meccan-like ayah blocks inside MEDINAN suras (P_Medinan low) ---")
# well-attested traditional embedded reports for a CHECK [REPORT]:
REP={8:"tradition: parts late-Meccan/Badr-era",2:"2:281 reportedly last revealed; some early blocks",
     9:"all Medinan but 9:128-129 reportedly Meccan-ish ending"}
for su in [2,8,9,4,5]:
    sc=scan(su); low=[t for t in sc if t[2]<0.35]
    print(f"\nSura {su} {names[su]} (nuzul {nuzul[su]}): {len(low)} low-P(Med) ayat of {len(sc)}; "+REP.get(su,""))
    # contiguous-ish low blocks
    print("   low ayat:", [a for a,_,_ in low][:30])
print("\n--- reverse: Medinan-like ayat inside clearly MECCAN suras (sanity, should be few) ---")
for su in [96,87,93,108]:
    sc=scan(su); hi=[a for a,p,s in sc if s>0.6]
    print(f"Sura {su} {names[su]} (nuzul {nuzul[su]}): {len(hi)} high-P(Med) of {len(sc)}")
