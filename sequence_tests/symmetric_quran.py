import re, sys, time, gzip
import numpy as np
from collections import Counter
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
t0=time.time(); WA=re.compile(r"[^\W\d_]+",re.UNICODE)
def yuleK(words):
    c=Counter(words); N=len(words); vi=Counter(c.values())
    return 1e4*(sum(v*(i*i) for i,v in vi.items())-N)/(N*N+1e-9)
def crep(words,n):
    s=" ".join(words); 
    if len(s)<=n: return 0.0
    g=Counter(s[i:i+n] for i in range(len(s)-n)); return 1-len(g)/max(len(s)-n,1)
def charMI(words):
    s=" ".join(words); al=sorted(set(s)); vm={c:i for i,c in enumerate(al)}
    a=np.array([vm[c] for c in s]); K=len(al)
    def mi(d):
        x=a[:-d];y=a[d:]; j=np.bincount(x*K+y,minlength=K*K).astype(float)/x.size; pj=j.reshape(K,K)
        px=pj.sum(1);py=pj.sum(0);nz=pj>0; return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
    return mi(1)+mi(2)
def contentrep(words,n,topn=20):
    top=set(w for w,_ in Counter(words).most_common(topn)); cw=[w for w in words if w not in top]
    return crep(cw,n)
def measures(words):
    N=len(words); wl=np.array([len(w) for w in words]); fc=Counter(words)
    wp=np.array(list(fc.values()),float)/N
    return dict(yuleK=yuleK(words), word_ent=-np.sum(wp*np.log2(wp)), ttr=len(fc)/N,
                hapax=sum(1 for c in fc.values() if c==1)/max(len(fc),1),
                mean_wl=wl.mean(), std_wl=wl.std(), frac_long=np.mean(wl>=8),
                charMI=charMI(words), crep8=crep(words,8), crep12=crep(words,12),
                contrep8=contentrep(words,8), contrep12=contentrep(words,12),
                gz=len(gzip.compress((" ".join(words)).encode()))/max(len(" ".join(words)),1))
def windows(words,N=800,step=300,maxw=120):
    rows=[]
    for c in range(0,max(1,len(words)-N+1),step):
        w=words[c:c+N]
        if len(w)<N*0.8: break
        rows.append(measures(w))
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}
def load_ar(p):
    out=[]
    for ln in open(p,encoding="utf-8",errors="ignore"):
        ss=ln.strip()
        if not ss or ss.startswith(("صحيح","أرض السافلين","نص إخباري")): continue
        out+=[normalize_letters(w) for w in WA.findall(ss) if normalize_letters(w)]
    return out
corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
col='متن آیه با حرکت'
qw=[normalize_letters(w) for i in range(len(corp.df)) for w in str(corp.df.iloc[i][col]).split() if normalize_letters(w)]
ar = load_ar("corpus/ar_tabari.txt")+load_ar("corpus/ar_novel.txt")+load_ar("corpus/ar_news.txt")
Q=windows(qw); 
# ordinary Arabic: window each register then pool
ordw={}
for nm,p in [("Tabari","corpus/ar_tabari.txt"),("Novel","corpus/ar_novel.txt"),("News","corpus/ar_news.txt")]:
    ordw[nm]=windows(load_ar(p))
ks=list(Q.keys())
print(f"[{time.time()-t0:.1f}s] SYMMETRIC SEARCH: what separates the QURAN from ordinary Arabic?")
print(f"  Quran windows={len(Q['ttr'])}; ordinary: "+", ".join(f"{k}={len(ordw[k]['ttr'])}" for k in ordw))
print(f"\n  {'measure':10s}{'QURAN':>9}{'ordAR':>9}{'sd-gap':>8}  separates?   (Shakespeare had:)")
shk={"yuleK":-2.6,"word_ent":+2.5,"std_wl":-2.8,"frac_long":-2.1,"ttr":+1.0,"charMI":+0.3,"gz":+0.9,
     "hapax":+0.2,"mean_wl":-0.5,"crep8":-1.8,"crep12":None,"contrep8":None,"contrep12":None}
rows=[]
for k in ks:
    pool=np.concatenate([ordw[o][k] for o in ordw])
    g=(Q[k].mean()-pool.mean())/(np.sqrt((Q[k].var()+pool.var())/2)+1e-9)
    rows.append((abs(g),k,Q[k].mean(),pool.mean(),g))
for ag,k,qm,om,g in sorted(rows,reverse=True):
    sep="*** YES" if ag>2 else ("~ weak" if ag>1 else "no")
    sh=shk.get(k); sht=f"Shake {sh:+.1f}sd" if isinstance(sh,(int,float)) else "(Quran-only)"
    print(f"  {k:10s}{qm:9.3f}{om:9.3f}{g:+8.1f}  {sep:9s}   {sht}")
print(f"\n[total {time.time()-t0:.1f}s]")

print("\n=== Quran vs NEAREST register (Tabari classical) — the hard comparison ===")
T=ordw["Tabari"]
for k in ["contrep8","contrep12","crep8","crep12","yuleK","word_ent","std_wl","ttr","gz"]:
    q=Q[k]; r=T[k]; g=(q.mean()-r.mean())/(np.sqrt((q.var()+r.var())/2)+1e-9)
    print(f"   {k:10s} Quran={q.mean():.3f} Tabari={r.mean():.3f}  {g:+.1f}sd")
