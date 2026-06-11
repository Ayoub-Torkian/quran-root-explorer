import re, sys, time, gzip
import numpy as np
from collections import Counter
t0=time.time(); W=re.compile(r"[a-zA-Z]+")
def load(p):
    sents=[]; lab="?"
    for ln in open(p,encoding="utf-8",errors="ignore"):
        s=ln.strip()
        if lab=="?":
            m=re.search(r"gutenberg.org/(?:files|cache/epub)/(\d+)",s)
            if m: lab=m.group(1)
        if not s or s.startswith(("[","http","→","---","meta-","Content-","```","!")) or "GUTENBERG" in s.upper(): continue
        for se in re.split(r"[.!?]+",s):
            w=[x.lower() for x in W.findall(se)]
            if len(w)>=2: sents.append(w)
    return lab,sents
def charMI(words):
    s=" ".join(words); al=sorted(set(s)); vm={c:i for i,c in enumerate(al)}
    a=np.array([vm[c] for c in s]); K=len(al)
    def mi(d):
        x=a[:-d];y=a[d:]; j=np.bincount(x*K+y,minlength=K*K).astype(float)/x.size; pj=j.reshape(K,K)
        px=pj.sum(1);py=pj.sum(0);nz=pj>0; return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
    return mi(1)+mi(2)
def crep(words,n=8):
    s=" ".join(words); 
    g=Counter(s[i:i+n] for i in range(len(s)-n)); return 1-len(g)/max(len(s)-n,1)
def gz(words):
    b=" ".join(words).encode(); return len(gzip.compress(b))/max(len(b),1)
def yuleK(words):
    c=Counter(words); N=len(words); vi=Counter(c.values())
    return 1e4*(sum(v*(i*i) for i,v in vi.items())-N)/(N*N+1e-9)
def measures(win_words, win_sents):
    types=set(win_words); N=len(win_words); wl=np.array([len(w) for w in win_words])
    fc=Counter(win_words); hap=sum(1 for w,c in fc.items() if c==1)
    wp=np.array(list(fc.values()),float)/N; went=-np.sum(wp*np.log2(wp))
    sl=np.array([len(s) for s in win_sents]) if win_sents else np.array([1])
    return dict(
        ttr=len(types)/N, hapax=hap/max(len(types),1), yuleK=yuleK(win_words),
        mean_wl=wl.mean(), std_wl=wl.std(), frac_long=np.mean(wl>=8), word_ent=went,
        sent_mean=sl.mean(), sent_cv=sl.std()/(sl.mean()+1e-9),
        charMI=charMI(win_words), crep8=crep(win_words), gz=gz(win_words))
def windows(sents,N=1500,step=1500,maxw=30):
    flat=[(w,si) for si,s in enumerate(sents) for w in s]
    rows=[]
    for c in range(0,max(1,len(flat)-N+1),step):
        seg=flat[c:c+N]
        if len(seg)<N*0.8: break
        ww=[w for w,_ in seg]; sids=sorted(set(si for _,si in seg)); ws=[sents[i] for i in sids]
        rows.append(measures(ww,ws))
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}, len(rows)
NAME={"100":"SHAKESPEARE","1342":"Austen","1661":"Doyle","11339":"Aesop","10":"Bible","19942":"Candide","2000":"Quijote"}
import glob
data={}
for p in sorted(glob.glob("corpus/src_*.txt")):
    lab,sents=load(p)
    if lab in NAME and sum(len(s) for s in sents)>9000: data[NAME[lab]]=windows(sents)[0]
ks=list(next(iter(data.values())).keys())
sh=data["SHAKESPEARE"]; others=[k for k in data if k!="SHAKESPEARE"]
# pooled ordinary English (exclude Bible as it's scripture-register; keep secular)
ordkeys=[k for k in ["Austen","Doyle","Aesop","Candide","Quijote"] if k in data]
print(f"[{time.time()-t0:.1f}s] WHAT SEPARATES SHAKESPEARE? equal-N 1500w windows")
print(f"  Shakespeare windows={len(sh['ttr'])}; ordinary English={ordkeys}")
print(f"\n  {'measure':10s}{'Shakesp':>10}{'ordEN':>10}{'sd-gap':>9}   separates?")
rows=[]
for k in ks:
    pool=np.concatenate([data[o][k] for o in ordkeys])
    g=(sh[k].mean()-pool.mean())/(np.sqrt((sh[k].var()+pool.var())/2)+1e-9)
    rows.append((abs(g),k,sh[k].mean(),pool.mean(),g))
for ag,k,sm,om,g in sorted(rows,reverse=True):
    sep="*** YES" if ag>2 else ("~ weak" if ag>1 else "no")
    print(f"  {k:10s}{sm:10.3f}{om:10.3f}{g:+9.1f}   {sep}")
print(f"\n[total {time.time()-t0:.1f}s]")
