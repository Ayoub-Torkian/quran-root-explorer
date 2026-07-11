# -*- coding: utf-8 -*-
"""Instrument 11b: MATHĀNĪ as SURFACE REFRAIN (the correct level — exact phrase doubling, not blurred content).
Within each sūra, detect near-duplicate āyāt (refrains) by rasm word-set Jaccard; measure refrain density vs a
length-matched random-sūra null built from corpus āyāt (does the canonical sūra REPEAT its own lines far above a
random bag of āyāt?). Reports the known refrain sūras. MEASURED, rasm surface, divine substrate."""
import numpy as np, statistics as st, openpyxl
np.random.seed(3)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
sura=[]; rasm=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    sura.append(s); rasm.append(set(str(r[10] or "").split()))
n=len(sura)
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def jac(x,y):
    if not x or not y: return 0.0
    return len(x&y)/len(x|y)
def refrain_density(idxs):  # fraction of āyāt that have a near-twin (Jaccard>=0.6) elsewhere in the set
    L=len(idxs); hit=0
    for p in range(L):
        for q in range(L):
            if p!=q and jac(rasm[idxs[p]],rasm[idxs[q]])>=0.6: hit+=1; break
    return hit/L if L else 0.0
allidx=list(range(n))
rows=[]
for s,(a,b) in bounds.items():
    L=b-a
    if L<4: continue
    rd=refrain_density(list(range(a,b)))
    nl=[refrain_density(list(np.random.choice(allidx,L,replace=False))) for _ in range(40)]
    z=(rd-st.mean(nl))/(st.pstdev(nl) or 1e-9)
    rows.append((rd,z,s,L))
rds=[r[0] for r in rows]; zs=[r[1] for r in rows]
import math
print("=== Instrument 11b: mathānī as SURFACE refrain (rasm) ===")
print(f"suras (L>=4): {len(rows)}")
print(f"  mean within-sūra refrain density = {st.mean(rds):.3f} | suras with ANY refrain: {100*sum(r>0 for r in rds)/len(rds):.0f}%")
print(f"  vs length-matched random-āyāt null: mean z={st.mean(zs):+.2f} | {100*sum(z>2 for z in zs)/len(zs):.0f}% z>2 | Stouffer Z={sum(zs)/math.sqrt(len(zs)):+.0f}")
rows.sort(key=lambda r:-r[0])
print("  top refrain sūras (density, z, sūra, L):", [(round(d,2),round(z,1),s,L) for d,z,s,L in rows[:8]])
print("DONE")
