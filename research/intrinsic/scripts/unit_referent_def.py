# -*- coding: utf-8 -*-
"""Instrument 8: REFERENT-DEFINITENESS directional recovery — a fully INTERNAL asymmetric relation (no external
model). Linguistic principle: a referent is introduced INDEFINITE, then referred to DEFINITE (ال). So for a stem
appearing both bare and with ال across āyāt, the indefinite-occurrence āyah PRECEDES the definite-occurrence āyah.
Build a per-sūra directed precedence graph from these votes; recover order by net-flow (jittered ties); directed
Kendall τ vs canonical. Nulls: order-shuffle (~0), direction-shuffled edges. MEASURED, rasm-only, divine substrate."""
import numpy as np, statistics as st, openpyxl
np.random.seed(19)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; rasm=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); rasm.append(str(r[10] or "").split())
n=len(sura)
PRE=set("وفبكل")  # leading conjunction/preposition letters that may precede ال
def stem_def(w):
    x=w
    if x and x[0] in PRE and x[1:3]=="ال" and len(x)>4: return x[3:], True   # و/ف/ب/ك/ل + ال + stem
    if x[:2]=="ال" and len(x)>3: return x[2:], True                          # ال + stem
    # indefinite: strip a single leading prefix letter if present
    if x and x[0] in PRE and len(x)>3: x=x[1:]
    return x, False
# per āyah: dict stem-> (saw_indef, saw_def)
ayah_stems=[]
for ww in rasm:
    sd={}
    for w in ww:
        s,d=stem_def(w)
        if len(s)<3: continue
        a,b=sd.get(s,(False,False)); sd[s]=(a or (not d), b or d)
    ayah_stems.append(sd)
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def kendall(a,b):
    L=len(a); ra={v:i for i,v in enumerate(a)}; rb={v:i for i,v in enumerate(b)}; c=di=0
    for i in range(L):
        for j in range(i+1,L):
            sg=(ra[a[i]]-ra[a[j]])*(rb[a[i]]-rb[a[j]])
            c+=sg>0; di+=sg<0
    return (c-di)/(c+di) if (c+di) else 0.0
def build_A(a,b):
    L=b-a
    # collect per-stem sets of (indef āyāt, def āyāt), restrict to distinctive stems (2..8 āyāt)
    stems={}
    for k in range(L):
        for s,(ind,dfn) in ayah_stems[a+k].items():
            d=stems.setdefault(s,[set(),set()])
            if ind: d[0].add(k)
            if dfn: d[1].add(k)
    A=np.zeros((L,L)); votes=0
    for s,(I,D) in stems.items():
        tot=len(I|D)
        if tot<2 or tot>8: continue
        for x in I:
            for y in D:
                if x!=y: A[x,y]+=1; votes+=1
    return A,votes
taus=[]; nulls=[]; dnull=[]; totvotes=0
for s,(a,b) in bounds.items():
    if b-a<4: continue
    A,v=build_A(a,b); totvotes+=v; L=b-a
    net=A.sum(1)-A.sum(0)
    order=list(np.argsort(net+1e-6*np.random.randn(L))); taus.append(kendall(order,list(range(L))))
    sh=list(range(L)); np.random.shuffle(sh); nulls.append(kendall(sh,list(range(L))))
    As=A*np.random.choice([-1,1],size=A.shape); netS=As.sum(1)-As.sum(0)
    dnull.append(kendall(list(np.argsort(netS+1e-6*np.random.randn(L))),list(range(L))))
N=len(taus)
print("=== Instrument 8: referent-definiteness directional recovery (internal, rasm) ===")
print(f"suras (L>=4): {N} | total indef->def precedence votes: {totvotes}")
print(f"  directed τ (net-flow) = {st.mean(taus):+.3f} | median {st.median(taus):+.3f} | {100*sum(t>=0.5 for t in taus)/N:.0f}% τ>=0.5")
print(f"  order-shuffle null τ = {st.mean(nulls):+.3f} | direction-shuffled-edges null τ = {st.mean(dnull):+.3f}")
print(f"  baselines: undirected +0.16 / gradient +0.10 / pairwise-reuse -0.00 / rhet-form +0.07")
print("DONE")
