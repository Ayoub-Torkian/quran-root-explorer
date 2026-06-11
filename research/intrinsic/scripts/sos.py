import unicodedata, numpy as np
from collections import defaultdict, Counter
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
verses=[]; suras=defaultdict(list)
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.split('\t',1); s=int(sa.split(':')[0]); w=skel(tx); verses.append(w); suras[s].append(w)
vlen=np.array([len(v) for v in verses],float)        # verse-length signal, mushaf order
llen=np.array([sum(len(x) for x in v) for v in verses],float)  # letters per verse

def dfa(x):
    x=x-x.mean(); y=np.cumsum(x); N=len(y)
    scales=np.unique(np.floor(np.logspace(np.log10(8),np.log10(N//4),20)).astype(int))
    F=[]
    for n in scales:
        nseg=N//n; 
        if nseg<2: continue
        rms=[]
        for s in range(nseg):
            seg=y[s*n:(s+1)*n]; t=np.arange(n)
            c=np.polyfit(t,seg,1); fit=np.polyval(c,t); rms.append(np.sqrt(np.mean((seg-fit)**2)))
        F.append((n,np.mean(rms)))
    F=np.array(F); H=np.polyfit(np.log(F[:,0]),np.log(F[:,1]),1)[0]; return H
def specslope(x):
    x=x-x.mean(); f=np.fft.rfftfreq(len(x)); P=np.abs(np.fft.rfft(x))**2
    m=(f>0)&(f<0.1)  # low-freq band
    a,_=np.polyfit(np.log(f[m]),np.log(P[m]),1); return -a
rng=np.random.default_rng(0)
print("=== cross-scale memory on the verse-length signal (N=%d) ==="%len(vlen))
print(f"DFA Hurst  vlen : {dfa(vlen):.3f}   (shuffle {np.mean([dfa(rng.permutation(vlen)) for _ in range(5)]):.3f})   [0.5=white, >0.5=long-range]")
print(f"DFA Hurst  llen : {dfa(llen):.3f}   (shuffle {np.mean([dfa(rng.permutation(llen)) for _ in range(5)]):.3f})")
print(f"1/f slope  vlen : {specslope(vlen):.2f}  (shuffle {np.mean([specslope(rng.permutation(vlen)) for _ in range(5)]):.2f})   [0=white,1=pink]")
# self-similar size distributions across the scale ladder (tail exponent via MLE, xmin chosen modestly)
def plaw(vals,xmin):
    v=np.array([x for x in vals if x>=xmin],float)
    return 1+len(v)/np.sum(np.log(v/(xmin-0.5)))
wl=[len(w) for v in verses for w in v]
ul=[len(v) for v in verses]                          # verse = unit of words
sl=[sum(len(v) for v in suras[s]) for s in suras]     # sura length in words
print("\n=== self-similar size distributions (power-law tail exponent) ===")
print(f"word-length  (letters) : alpha={plaw(wl,2):.2f}  range {min(wl)}-{max(wl)}")
print(f"verse-length (words)   : alpha={plaw(ul,3):.2f}  range {min(ul)}-{max(ul)}")
print(f"sura-length  (words)   : alpha={plaw(sl,50):.2f}  range {min(sl)}-{max(sl)}")
