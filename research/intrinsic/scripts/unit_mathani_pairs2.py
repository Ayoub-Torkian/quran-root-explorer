# -*- coding: utf-8 -*-
"""Instrument 13: mathānī pairing, LENGTH-CONTROLLED + āyah-level. Sūra rep = TF-IDF over roots (not length-biased
mean vector). (A) is each sūra's top content-twin a canonical NEIGHBOR more than chance? (B) matched-pair canonical
distance vs length-stratified null. (C) ĀYAH level: within each sūra, match āyāt into resembling pairs — are matched
pairs ADJACENT (āyāt come in twos) beyond chance? -> mathānī as micro-structure that would shape local order."""
import numpy as np, statistics as st, openpyxl, math
from collections import Counter
np.random.seed(8)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; roots=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); roots.append(str(r[8] or "").split())
n=len(sura); bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
sids=sorted(bounds); m=len(sids); idx={s:k for k,s in enumerate(sids)}
# TF-IDF sūra vectors over roots
docdf=Counter()
sroots=[]
for s in sids:
    a,b=bounds[s]; c=Counter()
    for k in range(a,b):
        for x in roots[k]: c[x]+=1
    sroots.append(c)
    for x in c: docdf[x]+=1
VOC=sorted(docdf); vi={r:k for k,r in enumerate(VOC)}
SV=np.zeros((m,len(VOC)))
for k,c in enumerate(sroots):
    tot=sum(c.values()) or 1
    for x,f in c.items(): SV[k,vi[x]]=(f/tot)*math.log(m/docdf[x])
SV=SV/(np.linalg.norm(SV,axis=1,keepdims=True)+1e-12)
S=SV@SV.T; np.fill_diagonal(S,-9)
# (A) is canonical neighbor the top content-twin?
top1=[int(np.argmax(S[i])) for i in range(m)]
nb_top1=sum(abs(top1[i]-i)==1 for i in range(m))     # top twin is a canonical neighbor
print("=== Instrument 13: mathānī pairing, length-controlled (TF-IDF) ===")
print(f"  (A) sūras whose #1 content-twin is a canonical NEIGHBOR: {nb_top1}/{m} (chance≈{2*m/(m-1):.1f}) ")
# known pairs ranks now
for x,y in [(2,3),(113,114),(73,74),(8,9),(105,106),(93,94)]:
    i,j=idx[x],idx[y]; r=int((S[i]>S[i,j]).sum())+1
    print(f"    S{x}~S{y}: sim={S[i,j]:+.2f}, #{r} of {m-1}")
# (B) matched-pair distance vs LENGTH-STRATIFIED null (permute within length-rank bands of 10)
def greedy_pairs(M):
    M=M.copy(); used=set(); pairs=[]
    order=np.dstack(np.unravel_index(np.argsort(-M,axis=None),M.shape))[0]
    for i,j in order:
        if i in used or j in used or i==j: continue
        used.add(i);used.add(j);pairs.append((i,j))
    return pairs
pairs=greedy_pairs(S); dists=[abs(i-j) for i,j in pairs]
lens=np.array([bounds[s][1]-bounds[s][0] for s in sids]); rankL=np.argsort(np.argsort(lens))
nd=[]
for _ in range(300):
    # permute within length bands of width 12 (preserves the muṣḥaf's length-ordering)
    P=np.arange(m); 
    for lo in range(0,m,12):
        seg=P[lo:lo+12].copy(); np.random.shuffle(seg); P[lo:lo+12]=seg
    nd.append(np.mean([abs(P[i]-P[j]) for i,j in pairs]))
zc=(np.mean(dists)-np.mean(nd))/(np.std(nd) or 1e-9)
print(f"  (B) matched-pair canonical distance {np.mean(dists):.1f} vs LENGTH-STRATIFIED null {np.mean(nd):.1f}±{np.std(nd):.1f} -> z={zc:+.1f}")
# (C) āyah-level pairing: within sūra, greedy-match āyāt, are matched pairs adjacent?
d2=np.load("/tmp/unit.npz"); VV=d2["VV"].astype(np.float64)
Vn=VV/(np.linalg.norm(VV,axis=1,keepdims=True)+1e-12)
adjfrac=[]; nulls=[]
for s,(a,b) in bounds.items():
    L=b-a
    if L<6: continue
    C=Vn[a:b]@Vn[a:b].T; np.fill_diagonal(C,-9)
    pr=greedy_pairs(C); af=np.mean([abs(i-j)==1 for i,j in pr]); adjfrac.append(af)
    nl=[]
    for _ in range(60):
        P=list(range(L)); np.random.shuffle(P)
        nl.append(np.mean([abs(P[i]-P[j])==1 for i,j in pr]))
    nulls.append((af-np.mean(nl))/(np.std(nl) or 1e-9))
print(f"  (C) āyah-level: matched-pair ADJACENCY frac mean {np.mean(adjfrac):.2f} | vs shuffle z mean {np.mean(nulls):+.2f} | Stouffer Z={sum(nulls)/math.sqrt(len(nulls)):+.0f}")
print("DONE")
