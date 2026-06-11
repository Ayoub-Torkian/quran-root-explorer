import re, time
import numpy as np
from collections import Counter
t0=time.time(); WF=re.compile(r"[^\W\d_]+",re.UNICODE)
def yuleK(words):
    c=Counter(words); N=len(words); vi=Counter(c.values())
    return 1e4*(sum(v*(i*i) for i,v in vi.items())-N)/(N*N+1e-9)
def crep(words,n):
    s=" ".join(words)
    if len(s)<=n: return 0.0
    g=Counter(s[i:i+n] for i in range(len(s)-n)); return 1-len(g)/max(len(s)-n,1)
def measures(words):
    N=len(words); wl=np.array([len(w) for w in words]); fc=Counter(words)
    wp=np.array(list(fc.values()),float)/N
    return dict(yuleK=yuleK(words),word_ent=-np.sum(wp*np.log2(wp)),ttr=len(fc)/N,
                std_wl=wl.std(),mean_wl=wl.mean(),frac_long=np.mean(wl>=7),
                rep8=crep(words,8),rep12=crep(words,12))
def win(words,N=350,step=150,maxw=20):
    rows=[]
    for c in range(0,max(1,len(words)-N+1),step):
        w=words[c:c+N]
        if len(w)<N*0.8: break
        rows.append(measures(w))
        if len(rows)>=maxw: break
    if not rows: rows=[measures(words)]
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}
def load(p):
    out=[]
    for ln in open(p,encoding="utf-8",errors="ignore"):
        out+=[w for w in WF.findall(ln)]
    return out
M=load("corpus/fa_poetry.txt"); O=load("corpus/fa_news.txt")
DM=win(M); DO=win(O)
print(f"[{time.time()-t0:.1f}s] PERSIAN positive control: masters(poetry) vs ordinary(news)")
print(f"  masters words={len(M)} win={len(DM['ttr'])}; ordinary words={len(O)} win={len(DO['ttr'])}")
shk={"yuleK":"-(richer)","word_ent":"+(richer)","std_wl":"-","frac_long":"-","ttr":"+","rep8":"-(less rep)","rep12":"-"}
print(f"\n  {'measure':9s}{'Masters':>10}{'Ordinary':>10}{'sd-gap':>8}   Shakespeare-dir? (Shk:{'  '})")
shdir={"yuleK":-1,"word_ent":+1,"std_wl":-1,"frac_long":-1,"ttr":+1,"rep8":-1,"rep12":-1}
for k in ["yuleK","word_ent","ttr","std_wl","frac_long","rep8","rep12","mean_wl"]:
    m=DM[k]; o=DO[k]; g=(m.mean()-o.mean())/(np.sqrt((m.var()+o.var())/2)+1e-9)
    d=shdir.get(k)
    tag = "" if d is None else ("MATCHES Shakespeare" if np.sign(g)==d else "opposite")
    print(f"  {k:9s}{m.mean():10.3f}{o.mean():10.3f}{g:+8.1f}   {tag}")
print(f"\n[total {time.time()-t0:.1f}s]")
