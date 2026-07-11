# -*- coding: utf-8 -*-
"""Shared setup for the 3 unit-definition instruments: verse SVD-embeddings + proper fāṣila rhyme keys
(rasm rawiyy AND voweled ending). Saves /tmp/unit.npz (VV, sura, alen) and /tmp/unit_rhyme.json."""
import openpyxl, math, json
import numpy as np
from collections import Counter
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]; rasm=[]; vow=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(str(r[8] or "").split())
    rasm.append(str(r[10] or "").split()); vow.append(str(r[11] or "").split())
n=len(sura)
df=Counter()
for rr in roots:
    for x in set(rr): df[x]+=1
VOC=[r for r in df if df[r]>=5]; vi={r:k for k,r in enumerate(VOC)}; V=len(VOC)
M=np.zeros((V,V))
for rr in roots:
    ids=[vi[x] for x in set(rr) if x in vi]
    for a in ids:
        for b in ids:
            if a!=b: M[a,b]+=1
Pm=np.zeros((V,V))
for a in range(V):
    for b in range(V):
        if M[a,b]>0:
            v=math.log2(M[a,b]*n/(df[VOC[a]]*df[VOC[b]])); Pm[a,b]=v if v>0 else 0
U,Sg,_=np.linalg.svd(Pm,full_matrices=False); EMB=U[:,:80]*np.sqrt(Sg[:80])
VV=np.zeros((n,80))
for i in range(n):
    ids=[vi[x] for x in roots[i] if x in vi]
    if ids: VV[i]=EMB[ids].mean(0)
import re
HARAKAT=re.compile(r'[ً-ْٰ]')   # tanwin/harakat/sukun/dagger-alif
def rkey_rasm(words):                            # rawiyy proxy: last 2 consonantal letters of last word
    w=words[-1] if words else ""; return w[-2:]
def rkey_vow(words):                             # voweled ending: last 3 chars incl. harakat (DEMOTE: diacritic)
    w=words[-1] if words else ""; return w[-3:]
alen=[len(rr) for rr in roots]
np.savez("/tmp/unit.npz", VV=VV, sura=np.array(sura), alen=np.array(alen))
json.dump({"rasm":[rkey_rasm(rasm[i]) for i in range(n)], "vow":[rkey_vow(vow[i]) for i in range(n)]},
          open("/tmp/unit_rhyme.json","w",encoding='utf-8'), ensure_ascii=False)
print("setup done: n=%d, VV %s, voc=%d"%(n, VV.shape, V))
