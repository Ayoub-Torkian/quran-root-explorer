# -*- coding: utf-8 -*-
"""Cross-validate the ayah-level Medinan detector against tanzil's traditional EXCEPTION lists [REPORT]:
Meccan suras that contain Medinan verses, and Medinan suras with Meccan verses."""
import openpyxl, numpy as np
from collections import defaultdict
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx",read_only=True); ws=wb['Sheet1']
S=defaultdict(list)
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    S[su].append(dict(ay=ay,roots=[norm(r) for r in (row[8]or'').split()],surf=[norm(t) for t in (row[10]or'').split()]))
MED={2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110}
DISP={6,14,16,22,28,29,34,35,42,55,76,98,99,103,109,110,13}
LEGAL=set(map(norm,['نفق','جهد','قتل','ربو','طلق','نکح','حدد','زکو','حلل','حرم','شهد','عقد','صوم','حجج','ورث']))
ESCH=set(map(norm,['قیم','بعث','جنن','نار','زلزل','قرع','هوی','طور']))
def vbel(s): return any(s[i]=='ای' and s[i+1]=='ها' and i+2<len(s) and s[i+2]=='الذین' for i in range(len(s)-2))
def af(roots,surf):
    nr=max(1,len(roots)); return [len(surf),int(vbel(surf)),sum(r in LEGAL for r in roots)/nr,sum(r in ESCH for r in roots)/nr,sum(r=='نفق' for r in roots),sum(r=='کفر' for r in roots)]
Xtr=[];ytr=[]
for su,ay in S.items():
    if su in DISP: continue
    lab=1 if su in MED else 0
    for d in ay: Xtr.append(af(d['roots'],d['surf'])); ytr.append(lab)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
pipe=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced')); pipe.fit(np.array(Xtr,float),np.array(ytr))
# tanzil exceptions: Meccan sura -> set of MEDINAN verse numbers (and a couple Medinan->Meccan)
MEC_with_MED={7:set(range(163,171)),6:{20,23,91,93,114,151,152,153},17:{26,32,33,57,73,74,75,76,77,78,79,80},
 10:{40,94,95,96},11:{12,17,114},12:{1,2,3,7},15:{87},31:{27,28,29},40:{56,57},42:{23,24,25,27},43:{54},
 45:{14},46:{10,15,35},18:{28}|set(range(83,102)),14:{28,29},32:set(range(16,21)),30:{17},29:set(range(1,12)),
 19:{58,71},20:{130,131},56:{81,82},26:{197,224,225,226,227},28:{52,53,54,55,85},25:{68,69,70},36:{45},53:{32},50:{38},54:{44,45,46},77:{48}}
MED_with_MEC={2:{281},8:set(range(30,37)),9:{128,129},5:{3},22:{52,53,54,55},47:{13}}
def flag_ayahs(su, want_med=True):
    ay=S[su]; P=pipe.predict_proba(np.array([af(d['roots'],d['surf']) for d in ay],float))[:,1]
    sm=np.convolve(P,np.ones(3)/3,mode='same')
    return set(ay[i]['ay'] for i in range(len(ay)) if (sm[i]>0.55 if want_med else sm[i]<0.45))
print("=== Meccan suras: detector's Medinan-like ayahs vs tanzil's Medinan exceptions ===")
tot_tp=tot_gold=tot_flag=0
for su,gold in sorted(MEC_with_MED.items()):
    if su not in S: continue
    fl=flag_ayahs(su,True); tp=len(fl&gold)
    tot_tp+=tp; tot_gold+=len(gold); tot_flag+=len(fl)
    if tp or su in (6,7,18,42): print(f"  sura {su:3d}: tanzil-Medinan={sorted(gold)[:6]}{'..' if len(gold)>6 else ''} | detector∩gold={sorted(fl&gold)} ({tp}/{len(gold)})")
print(f"\n  overlap: detector caught {tot_tp}/{tot_gold} traditional Medinan-exception verses (recall={tot_tp/tot_gold:.0%}); flagged {tot_flag} total")
print("\n=== Medinan suras: detector's Meccan-like ayahs vs tanzil's Meccan exceptions ===")
for su,gold in sorted(MED_with_MEC.items()):
    if su not in S: continue
    fl=flag_ayahs(su,False); print(f"  sura {su:3d}: tanzil-Meccan={sorted(gold)} | detector∩gold={sorted(fl&gold)}")
