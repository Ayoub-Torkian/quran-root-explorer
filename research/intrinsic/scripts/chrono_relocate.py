# -*- coding: utf-8 -*-
"""RELOCATION engine (baseline=revelation order; move only sustained anomalies).
Per-ayah era fingerprint -> segment long suras -> flag contiguous chunks whose fingerprint contradicts
the host sura. Coarse target (era), confidence per move. History = corroboration only."""
import openpyxl, numpy as np
from collections import defaultdict
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
S=defaultdict(list); nuzul={}; names={}
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    S[su].append((ay,[norm(r) for r in (row[8]or'').split()],[norm(t) for t in (row[10]or'').split()]))
    nuzul[su]=int(row[12]); names[su]=row[7]
MED={2,3,4,5,8,9,13,22,24,33,47,48,49,55,57,58,59,60,61,62,63,64,65,66,76,98,99,110}
DISPUTED={6,14,16,22,28,29,34,35,42,55,76,98,99,103,109,110,13}
LEGAL=set(map(norm,['نفق','جهد','قتل','ربو','طلق','نکح','یتم','وصی','حدد','غنم','اسر','صدق','زکو','حلل','حرم','شهد','عقد','جزی','صوم','حجج','دین','فرض','ورث']))
ESCH=set(map(norm,['قیم','بعث','جنن','نور','نار','حسب','وزن','صور','زلزل','قرع','سعر','هوی','طور']))
def vbel(s):
 for i in range(len(s)-2):
  if s[i]=='ای' and s[i+1]=='ها' and i+2<len(s) and s[i+2]=='الذین': return 1
 return 0
def vnas(s):
 for i in range(len(s)-3):
  if s[i]=='ای' and s[i+1]=='ها' and s[i+2:i+4]==['ال','ناس']: return 1
 return 0
def af(roots,surf):
 nr=max(1,len(roots))
 return [len(surf),vbel(surf),vnas(surf),sum(r in LEGAL for r in roots)/nr,sum(r in ESCH for r in roots)/nr,
         sum(r=='نفق' for r in roots),sum(r=='شرک' for r in roots),sum(r=='کفر' for r in roots)]
Xtr=[];ytr=[];grp=[]
for su,ay in S.items():
 if su in DISPUTED: continue
 lab=1 if su in MED else 0
 for a,r,s in ay: Xtr.append(af(r,s)); ytr.append(lab); grp.append(su)
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
pipe=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced'))
pipe.fit(np.array(Xtr,float),np.array(ytr))
def runs_against_host(su,minlen=4,margin=0.25):
 ay=S[su]; P=pipe.predict_proba(np.array([af(r,s) for _,r,s in ay],float))[:,1]
 sm=np.convolve(P,np.ones(5)/5,mode='same')
 host=1 if su in MED else 0
 # opposite-era = (host Medinan & sm<0.5-margin) or (host Meccan & sm>0.5+margin)
 opp=(sm< .5-margin) if host==1 else (sm> .5+margin)
 out=[];i=0
 while i<len(opp):
  if opp[i]:
   j=i
   while j<len(opp) and opp[j]: j+=1
   if j-i>=minlen:
    ays=[ay[k][0] for k in range(i,j)]
    out.append((ays[0],ays[-1],j-i,float(np.mean(sm[i:j]))))
   i=j
  else: i+=1
 return host,out
print("Relocation candidates: sustained off-era chunks (len>=4) in long suras (n_ayat>=60)")
print("host: M=Medinan baseline, m=Meccan baseline; chunk P=mean P(Medinan)")
REP={2:"trad: a few Baqara verses reported late/displaced",6:"trad: 6 verses of al-Anʿam reported Medinan",
     7:"trad: 7:163-170 reported Medinan",73:"trad: 73:20 reported Medinan",8:"trad: late-Meccan/Badr parts"}
cands=[]
for su,ay in S.items():
 if len(ay)<60: continue
 host,out=runs_against_host(su)
 for a0,a1,L,mp in out:
  tag = ('Meccan-like in MEDINAN '+names[su]) if host==1 else ('Medinan-like in MECCAN '+names[su])
  cands.append((L*abs(mp-0.5),su,a0,a1,L,mp,host,tag))
for score,su,a0,a1,L,mp,host,tag in sorted(cands,reverse=True)[:18]:
 r=REP.get(su,"")
 print(f"  {su}:{a0}-{a1}  len={L:2d}  P(Med)={mp:.2f}  host={'M' if host else 'm'}  {tag}   {('['+r+']') if r else ''}")
print(f"\ntotal sustained relocation candidates corpus-wide (long suras): {len(cands)}")
