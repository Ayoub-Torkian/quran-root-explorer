# -*- coding: utf-8 -*-
"""#2 Calibrate the relocation detector PER SURA against tanzil embedded-verse gold [REPORT].
For each flagged sura: precision (of flags, how many are gold) + recall (of gold, how many caught) -> trust tier."""
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
GOLD_MEC_in_MED={7:set(range(163,171)),6:{20,23,91,93,114,151,152,153},17:{26,32,33,57}|set(range(73,81)),
 10:{40,94,95,96},11:{12,17,114},12:{1,2,3,7},15:{87},31:{27,28,29},40:{56,57},42:{23,24,25,27},43:{54},
 45:{14},46:{10,15,35},18:{28}|set(range(83,102)),14:{28,29},32:set(range(16,21)),30:{17},29:set(range(1,12)),
 19:{58,71},20:{130,131},56:{81,82},26:{197,224,225,226,227},28:{52,53,54,55,85},25:{68,69,70},36:{45},53:{32},50:{38},54:{44,45,46},77:{48}}
def flag(su):
    ay=S[su]; P=pipe.predict_proba(np.array([af(d['roots'],d['surf']) for d in ay],float))[:,1]
    sm=np.convolve(P,np.ones(3)/3,mode='same')
    return set(ay[i]['ay'] for i in range(len(ay)) if sm[i]>0.55)
rows=[]
for su,gold in GOLD_MEC_in_MED.items():
    if su not in S: continue
    fl=flag(su); tp=len(fl&gold); prec=tp/len(fl) if fl else 0; rec=tp/len(gold)
    rows.append((su,len(gold),len(fl),tp,prec,rec))
def tier(prec,rec):
    if rec>=0.75 and prec>=0.5: return "HIGH"
    if rec>=0.5 or (tp_ok:=prec>=0.6): return "MED"
    return "LOW"
print(f"{'sura':>4} {'gold':>4} {'flag':>4} {'tp':>3} {'prec':>5} {'rec':>5}  tier")
for su,ng,nf,tp,prec,rec in sorted(rows,key=lambda r:-(r[5]+ (r[4]))):
    t="HIGH" if (rec>=0.75 and prec>=0.5) else ("MED" if (rec>=0.5 or prec>=0.6) else "LOW")
    print(f"{su:>4} {ng:>4} {nf:>4} {tp:>3} {prec:>5.2f} {rec:>5.2f}  {t}")
hi=[su for su,ng,nf,tp,prec,rec in rows if rec>=0.75 and prec>=0.5]
print("\nHIGH-trust suras (flag is reliable):",sorted(hi))
