# -*- coding: utf-8 -*-
"""#1 CHUNK-LEVEL multimodal fusion + cross-ref. Segment long suras by ayah-level P(Medinan); annotate
each chunk with dominant referents + yasalunaka topic + overlapping event-anchor date; flag multi-temporal."""
import openpyxl, numpy as np
from collections import defaultdict,Counter
def norm(s): return (s or '').replace('ي','ی').replace('ك','ک').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ة','ه')
wb=openpyxl.load_workbook("Book6.xlsx",read_only=True); ws=wb['Sheet1']
S=defaultdict(list); nuzul={}; names={}
for row in ws.iter_rows(min_row=9,values_only=True):
    try: su,ay=int(row[5]),int(row[6])
    except: continue
    S[su].append(dict(ay=ay,roots=[norm(r) for r in (row[8]or'').split()],toks=[norm(t) for t in (row[9]or'').split()],surf=[norm(t) for t in (row[10]or'').split()]))
    nuzul[su]=int(row[12]); names[su]=row[7]
MED={2,3,4,5,8,9,13,22,24,33,47,48,49,57,58,59,60,61,62,63,64,65,66,98,110}
DISP={6,14,16,22,28,29,34,35,42,55,76,98,99,103,109,110,13}
LEGAL=set(map(norm,['نفق','جهد','قتل','ربو','طلق','نکح','حدد','زکو','حلل','حرم','شهد','عقد','صوم','حجج','ورث']))
ESCH=set(map(norm,['قیم','بعث','جنن','نار','زلزل','قرع','هوی','طور']))
def vbel(s): return any(s[i]=='ای' and s[i+1]=='ها' and i+2<len(s) and s[i+2]=='الذین' for i in range(len(s)-2))
def af(roots,surf):
    nr=max(1,len(roots))
    return [len(surf),int(vbel(surf)),sum(r in LEGAL for r in roots)/nr,sum(r in ESCH for r in roots)/nr,sum(r=='نفق' for r in roots),sum(r=='کفر' for r in roots)]
Xtr=[];ytr=[]
for su,ay in S.items():
    if su in DISP: continue
    lab=1 if su in MED else 0
    for d in ay: Xtr.append(af(d['roots'],d['surf'])); ytr.append(lab)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
pipe=make_pipeline(StandardScaler(),LogisticRegression(max_iter=3000,class_weight='balanced')); pipe.fit(np.array(Xtr,float),np.array(ytr))
def hs(s,seq):
    L=len(seq); return any(s[i:i+L]==seq for i in range(len(s)-L+1))
def lem(tk,*p): return any(any(t.startswith(x) for x in p) for t in tk)
def refs(d):
    g=[];s=d['surf'];tk=d['toks']
    if hs(s,['الذین','امن']) or lem(tk,'مؤمن','مسلم'): g.append('believers')
    if lem(tk,'منافق') or hs(s,['قلوب','هم','مرض']): g.append('hypocrites')
    if hs(s,['اهل','ال','کتاب']) or hs(s,['الذین','هاد']) or lem(tk,'یهود','نصار'): g.append('people_of_book')
    if lem(tk,'مشرک'): g.append('polytheists')
    if hs(s,['الذین','کذب']) or lem(tk,'مکذب','مستکبر'): g.append('meccan_deniers')
    if lem(tk,'عیس','مریم'): g.append('jesus/mary')
    return g
# event anchors -> (host sura, ayah-set, date)
ANCH=[('Qibla',2,set(range(142,151)),'2 AH'),('Hajj/Umra',2,set(range(196,204)),'~6 AH'),
 ('Uhud',3,set(range(121,129))|set(range(140,176)),'3 AH'),('Najran/Mubahala',3,set(range(33,64)),'~9-10 AH'),
 ('Badr-spoils',8,set(range(41,45)),'2 AH'),('Tabuk',9,set(range(38,53)),'9 AH'),('Masjid Dirar',9,set(range(107,111)),'9 AH'),
 ('Muhajirun/Ansar',9,{100,117},'~Hijra'),('Ahzab',33,set(range(9,28)),'5 AH'),('Hudaybiyya',48,{1,10,18,27},'6 AH'),
 ('Hashr/Nadir',59,set(range(1,15)),'4 AH'),('Conquest',110,{1,2,3},'8 AH')]
def chunks(su):
    ay=S[su]; P=pipe.predict_proba(np.array([af(d['roots'],d['surf']) for d in ay],float))[:,1]
    sm=np.convolve(P,np.ones(5)/5,mode='same'); host=1 if su in MED else 0
    # segment by side of 0.5 with min length 4, merge short
    side=(sm>=0.5).astype(int); segs=[];i=0
    while i<len(side):
        j=i
        while j<len(side) and side[j]==side[i]: j+=1
        segs.append((i,j,side[i])); i=j
    # merge segments <3 into neighbor
    merged=[]
    for s0,s1,sd in segs:
        if s1-s0<3 and merged: merged[-1]=(merged[-1][0],s1,merged[-1][2])
        else: merged.append((s0,s1,sd))
    out=[]
    for s0,s1,sd in merged:
        a0,a1=ay[s0]['ay'],ay[s1-1]['ay']; mp=float(np.mean(sm[s0:s1]))
        rc=Counter(); 
        for d in ay[s0:s1]:
            for g in refs(d): rc[g]+=1
        anch=[(nm,dt) for nm,hsu,aset,dt in ANCH if hsu==su and any(a in aset for a in range(a0,a1+1))]
        out.append((a0,a1,s1-s0,mp,[g for g,_ in rc.most_common(2)],anch))
    return host,out
print("=== CHUNK MAP of long suras (era P=mean P(Medinan); anchors dated [REPORT]) ===")
LONG=[2,3,4,5,8,9,33,48,59,6,7]
multitemporal=[]
for su in LONG:
    host,ch=chunks(su); dates=set(d for _,_,_,_,_,an in ch for _,d in an)
    spread = len(dates)>1
    if spread: multitemporal.append((su,dates))
    print(f"\nSura {su} {names[su]} (nuzul {nuzul[su]}, baseline={'Medinan' if host else 'Meccan'}):"+("  *** MULTI-TEMPORAL ***" if spread else ""))
    for a0,a1,L,mp,rf,an in ch:
        era='Med' if mp>=0.5 else 'Mec'
        tag=f"  anchor={an}" if an else ""
        print(f"   {a0:>3}-{a1:<3} ({L:2d}) P(Med)={mp:.2f} [{era}] refs={rf}{tag}")
print("\n=== MULTI-TEMPORAL suras (chunks carry different anchor-dates) ===")
for su,dates in multitemporal: print(f"  Sura {su} {names[su]}: dates {sorted(dates)}")
