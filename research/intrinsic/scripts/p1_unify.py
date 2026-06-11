#!/usr/bin/env python3
# P1 — cross-scale unification on the RASM. (A) MFDFA: is the verse-length signal
# MULTIFRACTAL (a spectrum of scaling exponents h(q), not one)? Multifractal width Δh>0
# vs shuffle ~0 is the signature of a system organized across ALL scales at once —
# unifying L03 (Hurst), L04 (1/f), L05 (scale-free sizes). (B) cross-scale coupling
# letter→word→verse→sūra co-vary beyond a structure-preserving null.
import glob,unicodedata,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
def skel(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
sura=[];wlen=[];llen=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx)
    sura.append(su); wlen.append(len(w)); llen.append(sum(len(x) for x in w))
sura=np.array(sura); wlen=np.array(wlen,float); llen=np.array(llen,float)
N=len(wlen)
def mfdfa(x,qs,scales):
    Y=np.cumsum(x-x.mean()); Nn=len(Y); Fq=np.full((len(qs),len(scales)),np.nan)
    for si,s in enumerate(scales):
        ns=Nn//s
        if ns<4: continue
        seg_var=[]
        for v in range(ns):
            for Yseg in (Y[v*s:(v+1)*s], Y[Nn-(v+1)*s:Nn-v*s]):
                t=np.arange(s); c=np.polyfit(t,Yseg,1); seg_var.append(np.mean((Yseg-np.polyval(c,t))**2))
        var=np.array(seg_var); var[var<1e-12]=1e-12
        for qi,q in enumerate(qs):
            Fq[qi,si]= np.exp(0.25*np.mean(np.log(var))) if abs(q)<1e-6 else (np.mean(var**(q/2.))) **(1./q)
    hq=np.array([np.polyfit(np.log(scales),np.log(Fq[qi]),1)[0] for qi in range(len(qs))])
    return hq
qs=np.array([-5,-3,-2,-1,0,1,2,3,5],float)
scales=np.array([8,16,24,32,48,64,96,128,192,256,384,512])
rng=np.random.default_rng(0)
def width(x):
    h=mfdfa(x,qs,scales); return h, h[0]-h[-1]   # Δh = h(-5)-h(5)
print("=== (A) MFDFA — is the verse-length signal multifractal? ===")
for name,x in [("verse length (words)",wlen),("verse size (letters)",llen)]:
    h,dh=width(x)
    sh=np.array([width(x[rng.permutation(N)])[1] for _ in range(8)])
    print(f"  {name:22s} h(q=2)={h[qs==2][0]:.2f}  Δh(real)={dh:.3f}  Δh(shuffle)={sh.mean():.3f}±{sh.std():.3f}  z={(dh-sh.mean())/sh.std():.1f}")
# ---- (B) cross-scale coupling across the 114 sūras ----
print("\n=== (B) cross-scale coupling (per-sūra scales co-vary vs structure-preserving null) ===")
S=np.unique(sura)
letpw=[];wpv=[];vps=[];lettot=[]
for s in S:
    m=sura==s
    vps.append(m.sum())                       # verses per sūra (verse->sūra)
    wpv.append(wlen[m].mean())                # words per verse (word->verse)
    letpw.append(llen[m].sum()/max(wlen[m].sum(),1))  # letters per word (letter->word)
letpw=np.array(letpw);wpv=np.array(wpv);vps=np.array(vps)
def corr(a,b): return np.corrcoef(a,b)[0,1]
# null: shuffle verses across sūras keeping sūra sizes -> recompute
def null_corr(pairfn,reps=200):
    out=[]
    for _ in range(reps):
        perm=rng.permutation(N); su2=sura.copy()  # keep sūra labels, shuffle verse contents
        lp=[];wv=[]
        wl2=wlen[perm];ll2=llen[perm]
        for s in S:
            m=sura==s; lp.append(ll2[m].sum()/max(wl2[m].sum(),1)); wv.append(wl2[m].mean())
        out.append(pairfn(np.array(lp),np.array(wv),vps))
    return np.mean(out),np.std(out)
pairs=[("letters/word ↔ words/verse", lambda lp,wv,vp: corr(lp,wv)),
       ("words/verse ↔ verses/sūra",  lambda lp,wv,vp: corr(wv,vp)),
       ("letters/word ↔ verses/sūra", lambda lp,wv,vp: corr(lp,vp))]
for name,fn in pairs:
    real=fn(letpw,wpv,vps); m,sd=null_corr(fn)
    print(f"  {name:30s} r={real:+.3f}   null={m:+.3f}±{sd:.3f}   z={(real-m)/ (sd+1e-9):+.1f}")
