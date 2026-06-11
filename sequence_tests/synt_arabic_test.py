import re, glob, time, sys
import numpy as np
from collections import Counter, defaultdict
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
rng=np.random.default_rng(0); t0=time.time(); W=re.compile(r"[^\W\d_]+",re.UNICODE)
def enc(seq,cap):
    top=[w for w,_ in Counter(seq).most_common(cap)]; vm={w:i for i,w in enumerate(top)}
    return np.array([vm.get(w,cap) for w in seq]),cap+1,{i:w for w,i in vm.items()}
def MI(a,d,K):
    if a.size<=d: return 0.0
    x=a[:-d];y=a[d:]; j=np.bincount(x*K+y,minlength=K*K).astype(float)/x.size; pj=j.reshape(K,K)
    px=pj.sum(1);py=pj.sum(0);nz=pj>0; return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
def rep(a,n):
    g=Counter(tuple(a[i:i+n]) for i in range(len(a)-n)); return 1-len(g)/max(sum(g.values()),1)
def SYNT(words):
    top=set([w for w,_ in Counter(words).most_common(40)]); fw=[w for w in words if w in top]
    fa,K,_=enc(fw,40); return MI(fa,2,K)+rep(fa,3)
def markov(words):
    a,K,inv=enc(words,400); tr=defaultdict(Counter)
    for i in range(1,len(a)): tr[a[i-1]][a[i]]+=1
    succ={};cdf={}
    for s,c in tr.items():
        ks=np.array(list(c.keys()));vs=np.array(list(c.values()),float);succ[s]=ks;cdf[s]=np.cumsum(vs/vs.sum())
    s=a.copy()
    for i in range(1,len(a)): p=s[i-1]; s[i]=succ[p][np.searchsorted(cdf[p],rng.random())] if p in succ else rng.integers(K)
    return [inv.get(int(x),"O") for x in s]
def synt_dev_windows(words, N=1400, step=700, maxw=40):
    """windowed SYNT-deviation at fixed sample size N; returns array of per-window deviations."""
    out=[]
    for c in range(0, max(1,len(words)-N+1), step):
        w=words[c:c+N]
        if len(w)<N*0.6: break
        out.append(SYNT(w)-SYNT(markov(w)))
        if len(out)>=maxw: break
    return np.array(out) if out else np.array([SYNT(words)-SYNT(markov(words))])

# comparators
SCRIP={"10":"Bible(en)","2388":"Gita(en)","216":"Tao(en)","2800":"Koran-EN(tr)"}
SEC={"1342":"Austen(en)","1661":"Doyle(en)","11339":"Aesop(en)","19942":"Candide(fr)","21000":"Faust(de)","2000":"Quijote(es)"}
def load_g(p):
    lab="?"; ww=[]
    for ln in open(p,encoding="utf-8",errors="ignore"):
        s=ln.strip()
        if lab=="?":
            m=re.search(r"gutenberg.org/(?:files|cache/epub)/(\d+)",s)
            if m: lab=m.group(1)
        if not s or s.startswith(("[","http","→","---","meta-","Content-","```","!")) or "GUTENBERG" in s.upper(): continue
        ww+=[w.lower() for w in W.findall(s)]
    return lab,ww

texts={}
for p in sorted(glob.glob("corpus/src_*.txt")):
    lab,w=load_g(p)
    nm=SCRIP.get(lab,SEC.get(lab))
    if nm and len(w)>9000: texts[nm]=w
# Arabic ordinary (Tabari)
tab=[]
for ln in open("corpus/ar_tabari.txt",encoding="utf-8",errors="ignore"):
    s=ln.strip()
    if not s or s.startswith("صحيح وضعيف"): continue
    tab+=[w for w in W.findall(s)]
texts["Tabari(ar-ORD)"]=tab
# Quran
corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
qw=[normalize_letters(x) for i in range(len(corp.df)) for x in corp.seg_tokens[i] if normalize_letters(x)]
texts["QURAN(ar)"]=qw

print(f"[{time.time()-t0:.1f}s] EQUAL-SAMPLE windowed SYNTACTIC deviation-from-ordinary (N~1400 words/window)")
print(f"   {'text':16s} {'words':>7s}  {'mean dev':>9s} {'sd':>6s} {'nwin':>4s}")
rows=[]
for nm,w in texts.items():
    d=synt_dev_windows(w)
    rows.append((d.mean(),d.std(),len(d),len(w),nm))
for m,sd,nw,nwd,nm in sorted(rows,reverse=True):
    arabic = "AR" if "ar" in nm.lower() else "  "
    print(f"   {nm:16s} {nwd:7d}  {m:+9.3f} {sd:6.3f} {nw:4d}  {arabic}")
print(f"\n[total {time.time()-t0:.1f}s]")
