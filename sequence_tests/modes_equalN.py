import re, glob, time, sys, gzip
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
def rep(a,n): g=Counter(tuple(a[i:i+n]) for i in range(len(a)-n)); return 1-len(g)/max(sum(g.values()),1)
def gz(a): return 1-len(gzip.compress(a.astype(np.int16).tobytes()))/(2*max(len(a),1))
def REP(words):
    wa,K,_=enc(words,400); return (MI(wa,3,K)+rep(wa,4)+gz(wa))/3
def SYNT(words):
    top=set([w for w,_ in Counter(words).most_common(40)]); fw=[w for w in words if w in top]
    fa,K,_=enc(fw,40); return MI(fa,2,K)+rep(fa,3)
STOP_EN=set("the a an and or but of to in on at for with is are was were be it he she they we you i his her their its this that as by from not".split())
def NOV(content_words):
    seen=set(); per=[]; b=0
    for i,w in enumerate(content_words):
        if w not in seen: seen.add(w); b+=1
        if (i+1)%200==0: per.append(b); b=0
    per=np.array(per); return float(per.std()/(per.mean()+1e-9)) if len(per)>3 else 0.0
def markov(words,cap=400):
    a,K,inv=enc(words,cap); tr=defaultdict(Counter)
    for i in range(1,len(a)): tr[a[i-1]][a[i]]+=1
    succ={};cdf={}
    for s,c in tr.items():
        ks=np.array(list(c.keys()));vs=np.array(list(c.values()),float);succ[s]=ks;cdf[s]=np.cumsum(vs/vs.sum())
    s=a.copy()
    for i in range(1,len(a)): p=s[i-1]; s[i]=succ[p][np.searchsorted(cdf[p],rng.random())] if p in succ else rng.integers(K)
    return [inv.get(int(x),"O") for x in s]
def modedev(words, ndraw=2):
    """deviation of each mode from text's own Markov surrogate (ordinary-controlled)."""
    mks=[markov(words) for _ in range(ndraw)]
    rd=REP(words)-np.mean([REP(m) for m in mks])
    sd=SYNT(words)-np.mean([SYNT(m) for m in mks])
    cont=[x for x in words if x not in STOP_EN]
    nd=NOV(cont)-np.mean([NOV([x for x in m if x not in STOP_EN]) for m in mks])
    return rd,sd,nd
def windows(words,N=1500,step=750,maxw=24):
    out=[]
    for c in range(0,max(1,len(words)-N+1),step):
        w=words[c:c+N]
        if len(w)<N*0.6: break
        out.append(modedev(w))
        if len(out)>=maxw: break
    return np.array(out) if out else np.array([modedev(words)])
NAMES={"11339":"Aesop","10":"Bible","1342":"Austen","1661":"Doyle","19942":"Candide","21000":"Faust","2000":"Quijote","2388":"Gita","216":"Tao","2800":"Koran-EN"}
def load_g(p):
    lab="?"; words=[]
    for ln in open(p,encoding="utf-8",errors="ignore"):
        s=ln.strip()
        if lab=="?":
            m=re.search(r"gutenberg.org/(?:files|cache/epub)/(\d+)",s); 
            if m: lab=m.group(1)
        if not s or s.startswith(("[","http","→","---","meta-","Content-","```","!")) or "GUTENBERG" in s.upper(): continue
        words+=[w.lower() for w in W.findall(s)]
    return lab,words
data={}
for p in sorted(glob.glob("corpus/src_*.txt")):
    lab,w=load_g(p)
    if lab in NAMES and len(w)>9000: data[NAMES[lab]]=w
tab=[]
for ln in open("corpus/ar_tabari.txt",encoding="utf-8",errors="ignore"):
    s=ln.strip()
    if not s or s.startswith("صحيح"): continue
    tab+=[w for w in W.findall(s)]
data["Tabari(AR)"]=tab
corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
qw=[normalize_letters(x) for i in range(len(corp.df)) for x in corp.seg_tokens[i] if normalize_letters(x)]
data["QURAN(AR)"]=qw
modes=["REP_dev","SYNT_dev","NOV_dev"]
agg={}
for k,w in data.items():
    d=windows(w); agg[k]=(d.mean(0),d.std(0),len(d))
print(f"[{time.time()-t0:.1f}s] EQUAL-N (1500w) + own-Markov-controlled mode deviations")
for j,m in enumerate(modes):
    print(f"\n  --- {m} ---")
    order=sorted(agg,key=lambda t:-agg[t][0][j])
    for t in order:
        mu,sd,nw=agg[t]; star="  <<<" if "AR)" in t else ""
        print(f"    {t:12s} {mu[j]:+.3f} ± {sd[j]:.3f}{star}")
    print(f"    -> QURAN(AR) rank #{order.index('QURAN(AR)')+1}/{len(order)} ; Tabari(AR) #{order.index('Tabari(AR)')+1}")
print(f"\n[total {time.time()-t0:.1f}s]")
