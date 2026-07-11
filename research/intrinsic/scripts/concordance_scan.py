# -*- coding: utf-8 -*-
"""#1 MULTI-CLOCK CONCORDANCE scan for NEW chunk candidates. A candidate = a chunk whose era-classifier
signal is OFF its host baseline AND >=1 independent clock (referent-era / یسألونک-topic / bashīr-nadhīr /
legal) concurs in the same direction (>=2 clocks total). Tradition-known cases flagged separately."""
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
EARLY_REF=lambda d: lem(d['toks'],'مکذب','مستکبر','مشرک') or hs(d['surf'],['الذین','کذب'])
LATE_REF =lambda d: lem(d['toks'],'منافق','یهود','نصار') or hs(d['surf'],['اهل','ال','کتاب']) or hs(d['surf'],['قلوب','هم','مرض'])
def yasala(d):  # +1 legal(Medinan), -1 theological(Meccan), 0 none
    s=d['surf']
    if not any(w.startswith('یسل') or w.startswith('یسال') for w in s): return 0
    if any(r in LEGAL for r in d['roots']) or hs(s,['ال','محیض']) or lem(d['toks'],'یتم','اهله','انفال','خمر'): return 1
    if lem(d['toks'],'ساعه','روح','قیمه','جبال','قرنین'): return -1
    return 0
def bnr(d):  # +1 glad-tidings(later), -1 warning(earlier)
    g=lem(d['toks'],'بشیر','بشری','مبشر','یبشر'); w=lem(d['toks'],'نذیر','منذر','انذر','ینذر')
    return (1 if g else 0)-(1 if w else 0)
def legal_heavy(d): return sum(r in LEGAL for r in d['roots'])>=2
def chunks(su):
    ay=S[su]; P=pipe.predict_proba(np.array([af(d['roots'],d['surf']) for d in ay],float))[:,1]
    sm=np.convolve(P,np.ones(5)/5,mode='same'); side=(sm>=0.5).astype(int); segs=[];i=0
    while i<len(side):
        j=i
        while j<len(side) and side[j]==side[i]: j+=1
        segs.append((i,j)); i=j
    merged=[]
    for s0,s1 in segs:
        if s1-s0<4 and merged: merged[-1]=(merged[-1][0],s1)
        else: merged.append((s0,s1))
    for s0,s1 in merged:
        yield s0,s1,float(np.mean(sm[s0:s1])),ay[s0:s1]
KNOWN={(6,137,146),(7,155,170)}  # tradition-reported displaced
print("=== NEW multi-clock concordant chunk candidates (>=2 clocks off host) ===")
print("clocks: ERA(P) · REF(early/late referents) · ASK(یسألونک topic) · BNR(bashīr/nadhīr) · LEG(legal-heavy)")
cands=[]
for su,ay in S.items():
    if len(ay)<40: continue
    host=1 if su in MED else 0
    for s0,s1,mp,ch in chunks(su):
        a0,a1=ch[0]['ay'],ch[-1]['ay']
        # off-host era?
        era_off = (mp>0.62) if host==0 else (mp<0.38)
        if not era_off: continue
        offdir = 1 if host==0 else 0   # direction we're claiming (1=more Medinan/later, 0=more Meccan/earlier)
        votes=['ERA']
        ref=sum(LATE_REF(d) for d in ch)-sum(EARLY_REF(d) for d in ch)
        if (ref>0)==(offdir==1) and ref!=0: votes.append('REF')
        ask=sum(yasala(d) for d in ch)
        if (ask>0)==(offdir==1) and ask!=0: votes.append('ASK')
        b=sum(bnr(d) for d in ch)
        if (b>0)==(offdir==1) and b!=0: votes.append('BNR')
        lg=sum(legal_heavy(d) for d in ch)
        if lg>=2 and offdir==1: votes.append('LEG')
        if len(votes)>=2:
            known=any(su==k[0] and not (a1<k[1] or a0>k[2]) for k in KNOWN)
            cands.append((len(votes),su,a0,a1,s1-s0,mp,offdir,votes,known))
for n,su,a0,a1,L,mp,offdir,votes,known in sorted(cands,reverse=True):
    tag='[tradition-known]' if known else '[NEW]'
    direction='Medinan-like in Meccan' if offdir==1 else 'Meccan-like in Medinan'
    print(f"  {su}:{a0}-{a1} ({names[su]}) len={L} P(Med)={mp:.2f} clocks={'+'.join(votes)} ({len(votes)}) {direction} {tag}")
print(f"\ntotal concordant chunks: {len(cands)} | NEW: {sum(1 for c in cands if not c[8])}")
