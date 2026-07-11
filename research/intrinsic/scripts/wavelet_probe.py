# -*- coding: utf-8 -*-
"""Wavelet exploration. (1-D) per-ayah signals along the canonical sequence: scale spectrum (scale-free?) +
boundary alignment (do transitions land on sura seams?). (2-D) ayah×ayah recurrence wavelet for ring/refrain.
Nulls: phase-randomized surrogate (1-D spectrum), circular-shift (boundary), row/col shuffle (2-D). MEASURED."""
import openpyxl, math, random
import numpy as np
random.seed(17); np.random.seed(17)
try:
    import pywt; HAVE=True
except Exception: HAVE=False
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
wb=openpyxl.load_workbook(R+"/Book6.xlsx", read_only=True, data_only=True); ws=wb.active
roots=[]; sura=[]
for r in ws.iter_rows(min_row=9, values_only=True):
    try: s=int(r[5])
    except (TypeError,ValueError): continue
    roots.append(str(r[8] or "").split()); sura.append(s)
n=len(roots)
from collections import Counter
df=Counter()
for rr in roots:
    for x in set(rr): df[x]+=1
# signals
length=np.array([len(rr) for rr in roots],dtype=float)
idf={x:math.log(n/df[x]) for x in df}
rare=np.array([ (sum(idf[x] for x in set(rr))/max(1,len(set(rr)))) for rr in roots])  # mean idf per ayah
# novelty: fraction of roots not in previous 20 ayat
nov=np.zeros(n); from collections import deque
win=deque(); seen=Counter()
for i,rr in enumerate(roots):
    s=set(rr); new=sum(1 for x in s if seen[x]==0); nov[i]=new/max(1,len(s))
    win.append(s); 
    for x in s: seen[x]+=1
    if len(win)>20:
        old=win.popleft()
        for x in old: seen[x]-=1
def haar_levels(x):
    x=x-x.mean(); L=int(math.floor(math.log2(len(x)))); cur=x[:2**L].copy(); var=[]
    for lev in range(L):
        a=(cur[0::2]+cur[1::2])/math.sqrt(2); d=(cur[0::2]-cur[1::2])/math.sqrt(2)
        var.append(np.var(d)); cur=a
    return np.array(var)
def spectrum_slope(x):
    v=haar_levels(x); sc=np.arange(1,len(v)+1)
    # log-log slope of detail variance vs scale (1/f -> slope ~ +1 in variance-vs-scale)
    m=np.polyfit(np.log(sc[:8]), np.log(v[:8]+1e-12),1)[0]; return m,v
print("pywt available:",HAVE,"| ayat:",n)
for name,sig in [("ayah-length",length),("rare-density(idf)",rare),("novelty",nov)]:
    m,v=spectrum_slope(sig)
    # phase-randomized surrogate slope
    sl=[]
    for _ in range(60):
        F=np.fft.rfft(sig-sig.mean()); ph=np.exp(1j*np.random.uniform(0,2*np.pi,len(F))); ph[0]=1
        sur=np.fft.irfft(np.abs(F)*ph, n=len(sig)); sl.append(spectrum_slope(sur)[0])
    z=(m-np.mean(sl))/(np.std(sl)+1e-9)
    print(f"  [{name}] scale-energy log-log slope {m:+.2f} (1/f≈+1) vs phase-surrogate {np.mean(sl):+.2f}±{np.std(sl):.2f} -> z={z:+.1f}")
# boundary alignment: level-1 Haar detail (|first diff|) at sura seams vs interior, using novelty (non-trivial)
seam=np.zeros(n,bool)
for i in range(1,n):
    if sura[i]!=sura[i-1]: seam[i]=True
d1=np.abs(np.diff(np.concatenate([[nov[0]],nov])))
real=d1[seam].mean()/ (d1[~seam].mean()+1e-9)
nul=[]
for _ in range(500):
    sh=np.roll(seam, np.random.randint(1,n-1)); nul.append(d1[sh].mean()/(d1[~sh].mean()+1e-9))
zb=(real-np.mean(nul))/(np.std(nul)+1e-9)
print(f"  [boundary] novelty-jump at sura seams vs interior ratio {real:.2f} vs shift-null {np.mean(nul):.2f}±{np.std(nul):.2f} -> z={zb:+.1f}")
# (2-D) recurrence wavelet on a mid sura: ring (anti-diagonal) energy vs row/col shuffle
def recur(sidx):
    ix=[i for i in range(n) if sura[i]==sidx]; m=len(ix)
    Rm=np.zeros((m,m))
    for p in range(m):
        sp=set(roots[ix[p]])
        for q in range(m):
            sq=set(roots[ix[q]]); u=sp|sq; Rm[p,q]=len(sp&sq)/len(u) if u else 0
    return Rm,m
for sidx in [55,2,19]:   # ar-Rahman (refrain!), al-Baqara, Maryam
    Rm,m=recur(sidx)
    if m<8: continue
    # anti-diagonal (ring) energy = mean similarity of mirror pairs (i, m-1-i) excluding center
    anti=np.mean([Rm[i,m-1-i] for i in range(m) if i!=m-1-i])
    offdiag=(Rm.sum()-np.trace(Rm))/(m*m-m)
    ratio=anti/(offdiag+1e-9)
    nl=[]
    for _ in range(300):
        perm=np.random.permutation(m); P=Rm[perm][:,perm]
        a2=np.mean([P[i,m-1-i] for i in range(m) if i!=m-1-i]); nl.append(a2/(offdiag+1e-9))
    z2=(ratio-np.mean(nl))/(np.std(nl)+1e-9)
    print(f"  [2D ring] sura {sidx} (m={m}): anti-diagonal/offdiag {ratio:.2f} vs shuffle {np.mean(nl):.2f}±{np.std(nl):.2f} -> z={z2:+.1f}")
print("DONE")
