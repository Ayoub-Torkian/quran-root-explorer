#!/usr/bin/env python3
# P1 stability — robust MFDFA. Δh=1.56 (word-count) was suspect: negative q amplifies
# tiny segment variances and verse word-counts are small integers (many ties). Here:
# q restricted to a stable range, q=0 formula fixed (exp(0.5*mean(log var))), >=8 segments
# per scale. Decide: real multifractal width vs shuffle over the STABLE q range.
import glob,unicodedata,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
wlen=[];llen=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    _,tx=ln.split('\t',1); w=skel(tx); wlen.append(len(w)); llen.append(sum(len(x) for x in w))
wlen=np.array(wlen,float); llen=np.array(llen,float); N=len(wlen)
def mfdfa(x,qs,scales,min_seg=8):
    Y=np.cumsum(x-x.mean()); Nn=len(Y); H={}
    Fq=np.full((len(qs),len(scales)),np.nan)
    for si,s in enumerate(scales):
        ns=Nn//s
        if ns<min_seg: continue
        var=[]
        for v in range(ns):
            for seg in (Y[v*s:(v+1)*s], Y[Nn-(v+1)*s:Nn-v*s]):
                t=np.arange(s); c=np.polyfit(t,seg,1); var.append(np.mean((seg-np.polyval(c,t))**2))
        var=np.array(var); var=var[var>0]                       # drop degenerate (tie) segments
        for qi,q in enumerate(qs):
            Fq[qi,si]= np.exp(0.5*np.mean(np.log(var))) if abs(q)<1e-9 else (np.mean(var**(q/2.)))**(1./q)
    hq=np.full(len(qs),np.nan)
    for qi in range(len(qs)):
        ok=~np.isnan(Fq[qi])
        if ok.sum()>=4: hq[qi]=np.polyfit(np.log(scales[ok]),np.log(Fq[qi][ok]),1)[0]
    return hq
scales=np.array([8,12,16,24,32,48,64,96,128,192,256])
rng=np.random.default_rng(1)
def report(name,x):
    for qr,lab in [((-5,5),"q∈[-5,5] (original)"),((-3,3),"q∈[-3,3]"),((-2,2),"q∈[-2,2] (stable)")]:
        qs=np.array([q for q in (-5,-3,-2,-1,0,1,2,3,5) if qr[0]<=q<=qr[1]],float)
        h=mfdfa(x,qs,scales); dh=np.nanmax(h)-np.nanmin(h)
        sh=np.array([ (lambda hh:np.nanmax(hh)-np.nanmin(hh))(mfdfa(x[rng.permutation(N)],qs,scales)) for _ in range(10)])
        z=(dh-sh.mean())/(sh.std()+1e-9)
        print(f"  {name:14s} {lab:22s} Δh(real)={dh:.3f}  Δh(shuffle)={sh.mean():.3f}±{sh.std():.3f}  z={z:.1f}")
print("=== robust MFDFA — multifractal width vs shuffle, by q range ===")
report("verse words",wlen)
report("verse letters",llen)
