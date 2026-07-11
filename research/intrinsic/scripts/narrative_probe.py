# -*- coding: utf-8 -*-
"""NARRATIVE-internal temporal signals. (A) Moses-story deployment per sura (episode coverage + length)
vs nuzul. (B) tribal punishment-cycle density vs nuzul. ONE-LAW: episodes read from Quran's own telling."""
import openpyxl, numpy as np
from collections import defaultdict
from scipy.stats import spearmanr
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
S=defaultdict(list); nuzul={}; names={}
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    S[su].append(dict(ay=ay,roots=[norm(r) for r in (row[8]or'').split()],toks=[norm(t) for t in (row[9]or'').split()],surf=[norm(t) for t in (row[10]or'').split()]))
    nuzul[su]=int(row[12]); names[su]=row[7]
def has_root(ay,roots): 
    rs=set(r for d in ay for r in d['roots']); ts=[t for d in ay for t in d['toks']]
    return any(r in rs for r in roots) or any(any(t.startswith(r) for t in ts) for r in roots)
# ---- (A) MOSES episodes (markers read from the Quranic telling) ----
MOSES_EP={
 'call_at_Tur':['طور','نود','واد'],          # call at the valley/fire (نودی / طوی)
 'staff_signs':['عصو','سحر'],                 # staff vs magicians
 'pharaoh_court':['فرعون','هامان','ملا'],     # Pharaoh & court
 'sea_drowning':['غرق','يم'],                 # sea / drowning
 'calf_tablets':['عجل','لوح','سامری','میقات'],# golden calf / tablets
}
mos_suras=[su for su in S if has_root(S[su],['موسی','موس'])]
rows=[]
for su in mos_suras:
    ay=S[su]; mos_ayat=[d for d in ay if any(t.startswith('موس') for t in d['toks'])]
    cover=sum(has_root(ay,mk) for mk in MOSES_EP.values())
    rows.append((su,nuzul[su],len(mos_ayat),cover))
rows.sort(key=lambda r:r[1])
nz=np.array([r[1] for r in rows]); length=np.array([r[2] for r in rows]); cov=np.array([r[3] for r in rows])
print(f"=== (A) MOSES deployment across revelation ({len(rows)} suras mention Moses) ===")
print("  nuzul vs narrative-LENGTH (#Moses ayat)  Spearman=%.3f"%spearmanr(nz,length).correlation)
print("  nuzul vs episode-COVERAGE (0-5)          Spearman=%.3f"%spearmanr(nz,cov).correlation)
print("  early(nuzul<=38) mean: len=%.1f cover=%.2f | late(>77) mean: len=%.1f cover=%.2f"%(
    length[nz<=38].mean(),cov[nz<=38].mean(),length[nz>77].mean() if (nz>77).any() else 0,cov[nz>77].mean() if (nz>77).any() else 0))
print("  fullest tellings (len, cover):",[(su,names[su],l,c,n) for su,n,l,c in sorted(rows,key=lambda r:-r[2])[:6]])
# ---- (B) tribal punishment-cycle density ----
TRIBES={'Ad(Hud)':['عاد'],'Thamud(Salih)':['ثمود','نوق'],'Madyan(Shuayb)':['مدین','شعیب'],
        'Nuh':['نوح'],'Lut':['لوط'],'Pharaoh':['فرعون']}
print("\n=== (B) tribal punishment-cycle density per sura vs nuzul ===")
tr=[]
for su in S:
    cnt=sum(has_root(S[su],pats) for pats in TRIBES.values())
    if cnt>0: tr.append((su,nuzul[su],cnt))
tr.sort(key=lambda r:r[1])
tn=np.array([r[1] for r in tr]); tc=np.array([r[2] for r in tr])
print("  suras with >=1 punishment-tribe: %d"%len(tr))
print("  nuzul vs tribe-COUNT per sura  Spearman=%.3f"%spearmanr(tn,tc).correlation)
multi=[(su,n,c) for su,n,c in tr if c>=4]
print("  multi-tribe CYCLE suras (>=4 tribes):",[(su,names[su],c,'nz%d'%n) for su,n,c in sorted(multi,key=lambda r:r[1])])
print("  their nuzul: median=%d  (early%%=%.0f%%)"%(int(np.median([n for _,n,_ in multi])),100*np.mean([n<=77 for _,n,_ in multi])))
