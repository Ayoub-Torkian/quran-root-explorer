#!/usr/bin/env python3
# GC-SKEW -> ORIGINS analog. Binary letter class b=+1 long-vowel(ا/و/ي), -1 consonant.
# Cumulative skew along the whole rasm stream; detrend; its turning points = candidate "origins".
# Test: do sūra boundaries sit at skew turning-points (slope sign-changes) above chance?
import glob,unicodedata,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
b=[]; bnd=[]  # boundary letter-index at each new sūra
prev=None; idx=0
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); s=int(sa.split(':')[0]); t=skel(tx.strip())
    if s!=prev: bnd.append(idx); prev=s
    for ch in t: b.append(1 if ch in ('ا','و','ي') else -1); idx+=1
b=np.array(b,float); C=np.cumsum(b - b.mean())  # detrended cumulative skew
# smooth and find turning points (local extrema of slope-sign of a smoothed C)
w=400
sm=np.convolve(C,np.ones(w)/w,mode='same')
slope=np.gradient(sm); sign=np.sign(slope)
turns=np.where(np.diff(sign)!=0)[0]   # slope sign-changes = extrema = candidate origins
print("letters: %d ; sūra boundaries: %d ; skew turning-points: %d"%(len(b),len(bnd),len(turns)))
# distance from each sūra boundary to nearest turning point
def mean_dist(bset):
    return np.mean([min(abs(np.array(turns)-x)) for x in bset])
real=mean_dist(bnd[1:])  # skip pos 0
rng=np.random.default_rng(0)
fl=[mean_dist(rng.integers(0,len(b),len(bnd)-1)) for _ in range(300)]
fl=np.array(fl)
print("mean letters from a sūra boundary to nearest skew-origin: real %.0f vs random %.0f±%.0f  z=%+.1f"%(real,fl.mean(),fl.std(),(real-fl.mean())/fl.std()))
print("(negative z = boundaries sit CLOSER to skew origins than chance)")
