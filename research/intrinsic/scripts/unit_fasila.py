# -*- coding: utf-8 -*-
"""Instrument 3: proper fāṣila (rhyme) model. (i) does the fāṣila bind the āyah SEQUENCE — adjacent-āyah rhyme
agreement vs order-shuffle null — on the rasm rawiyy (DIVINE substrate) vs the voweled ending (HUMAN/diacritic,
DEMOTED); (ii) does it tile each sūra into few rhyme-sections (multi-uniform). MEASURED."""
import numpy as np, json, statistics as st, math
from collections import Counter
np.random.seed(31)
d=np.load("/tmp/unit.npz"); sura=d["sura"]; n=len(sura)
rh=json.load(open("/tmp/unit_rhyme.json",encoding='utf-8')); rasm=rh["rasm"]; vow=rh["vow"]
bounds={}; cur=sura[0]; start=0
for i in range(1,n):
    if sura[i]!=cur: bounds[int(cur)]=(start,i); cur=sura[i]; start=i
bounds[int(cur)]=(start,n)
def adjz(key):
    zs=[]; P=400
    for s,(a,b) in bounds.items():
        if b-a<4: continue
        idx=list(range(a,b)); r0=np.mean([key[idx[i]]==key[idx[i+1]] for i in range(len(idx)-1)])
        rs=[]
        for _ in range(P):
            p=idx[:]; np.random.shuffle(p); rs.append(np.mean([key[p[i]]==key[p[i+1]] for i in range(len(p)-1)]))
        zs.append((r0-st.mean(rs))/(st.pstdev(rs) or 1e-9))
    return zs
def tile(key):
    covs=[]; runs=[]
    for s,(a,b) in bounds.items():
        if b-a<4: continue
        seq=[key[i] for i in range(a,b)]; L=len(seq)
        covs.append(Counter(seq).most_common(1)[0][1]/L); runs.append((1+sum(seq[i]!=seq[i-1] for i in range(1,L)))/L)
    return st.mean(covs), st.mean(runs)
zr=adjz(rasm); zv=adjz(vow); N=len(zr)
cr,rr=tile(rasm); cv,rv=tile(vow)
print("=== Instrument 3: proper fāṣila (rhyme) model ===")
print(f"(i) sequence-binding (adjacent rhyme agreement vs shuffle), {N} suras:")
print(f"    rasm rawiyy [DIVINE]   mean z=+{st.mean(zr):.1f} | %d%% z>2 | Stouffer Z=+{sum(zr)/math.sqrt(N):.0f}"%int(100*sum(z>2 for z in zr)/N))
print(f"    voweled end [DEMOTED]  mean z=+{st.mean(zv):.1f} | %d%% z>2 | Stouffer Z=+{sum(zv)/math.sqrt(N):.0f}"%int(100*sum(z>2 for z in zv)/N))
print(f"(ii) sūra rhyme-tiling: rasm dom-coverage {cr:.2f}, runs/āyah {rr:.2f} | voweled dom-coverage {cv:.2f}, runs/āyah {rv:.2f}")
print("DONE")
