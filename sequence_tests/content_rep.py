import re, sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
rng=np.random.default_rng(1); t0=time.time(); W=re.compile(r"[^\W\d_]+",re.UNICODE)
def repC(s,n):
    a=np.frombuffer(bytes(s,'utf-16-le'),dtype=np.uint16)
    if len(a)<=n: return 0.0
    g=Counter(a[i:i+n].tobytes() for i in range(len(a)-n)); return 1-len(g)/max(sum(g.values()),1)
def win_rep(words,topn,N=2500,step=900,maxw=80):
    top=set(w for w,_ in Counter(words).most_common(topn)) if topn else set()
    stream=[w for w in words if w not in top]
    s=" ".join(stream); out=[]
    for c in range(0,max(1,len(s)-N+1),step):
        sub=s[c:c+N]
        if len(sub)<N*0.8: break
        out.append([repC(sub,8),repC(sub,12)])
        if len(out)>=maxw: break
    return np.array(out) if out else np.array([[repC(s,8),repC(s,12)]])
def load_ar(p):
    out=[]
    for ln in open(p,encoding="utf-8",errors="ignore"):
        ss=ln.strip()
        if not ss or ss.startswith(("صحيح","أرض السافلين","نص إخباري")): continue
        out+=[normalize_letters(w) for w in W.findall(ss) if normalize_letters(w)]
    return out
corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
col='متن آیه با حرکت'
qw=[normalize_letters(w) for i in range(len(corp.df)) for w in str(corp.df.iloc[i][col]).split() if normalize_letters(w)]
reg={"Quran":qw,"Tabari":load_ar("corpus/ar_tabari.txt"),"Novel":load_ar("corpus/ar_novel.txt"),"News":load_ar("corpus/ar_news.txt")}
for topn in (0,20,50):
    D={k:win_rep(v,topn) for k,v in reg.items()}
    tag={0:"RAW (all words)",20:"content-only (drop top20)",50:"content-only (drop top50)"}[topn]
    print(f"\n=== {tag} ===  windows: "+" ".join(f"{k}={len(D[k])}" for k in reg))
    for j,m in enumerate(["rep8","rep12"]):
        q=D["Quran"][:,j]
        s=f"  {m}: Quran={q.mean():.4f}"
        for k in ["Tabari","Novel","News"]:
            r=D[k][:,j]; csd=np.sqrt((q.var()+r.var())/2)+1e-9; g=(q.mean()-r.mean())/csd
            bp=np.mean(rng.choice(q,5000)>rng.choice(r,5000))
            s+=f" | {k}={r.mean():.4f}({g:+.1f}sd,P={bp:.2f})"
        print(s)
print(f"\n[total {time.time()-t0:.1f}s]")
