import re, sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
rng=np.random.default_rng(2); t0=time.time(); WA=re.compile(r"[^\W\d_]+",re.UNICODE)
def crepC(s,n):
    if len(s)<=n: return 0.0
    g=Counter(s[i:i+n] for i in range(len(s)-n)); return 1-len(g)/max(len(s)-n,1)
def win(words,topn,N=2000,step=700,maxw=120):
    top=set(w for w,_ in Counter(words).most_common(topn)) if topn else set()
    s=" ".join(w for w in words if w not in top); out=[]
    for c in range(0,max(1,len(s)-N+1),step):
        sub=s[c:c+N]
        if len(sub)<N*0.8: break
        out.append([crepC(sub,8),crepC(sub,12)]); 
        if len(out)>=maxw: break
    return np.array(out) if out else np.array([[crepC(s,8),crepC(s,12)]])
def load_ar(*ps):
    out=[]
    for p in ps:
        for ln in open(p,encoding="utf-8",errors="ignore"):
            ss=ln.strip()
            if not ss or ss.startswith(("صحيح","أرض","نص ")): continue
            out+=[normalize_letters(w) for w in WA.findall(ss) if normalize_letters(w)]
    return out
corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
col='متن آیه با حرکت'
qw=[normalize_letters(w) for i in range(len(corp.df)) for w in str(corp.df.iloc[i][col]).split() if normalize_letters(w)]
classical=load_ar("corpus/ar_tabari.txt","corpus/ar_classical2.txt")
print(f"[{time.time()-t0:.1f}s] FINAL TEST: Quran content-rep vs CLASSICAL Arabic at volume")
print(f"  classical words={len(classical)}")
for topn,tag in [(0,"RAW"),(20,"content drop20"),(50,"content drop50")]:
    Q=win(qw,topn); C=win(classical,topn)
    print(f"\n  {tag}: classical windows={len(C)}, Quran windows={len(Q)}")
    for j,m in enumerate(["rep8","rep12"]):
        q=Q[:,j]; c=C[:,j]; csd=np.sqrt((q.var()+c.var())/2)+1e-9; g=(q.mean()-c.mean())/csd
        bp=np.mean(rng.choice(q,6000)>rng.choice(c,6000))
        print(f"    {m}: Quran={q.mean():.4f} Classical={c.mean():.4f}  {g:+.1f}sd  P(Q>C)={bp:.2f}")
print(f"\n[total {time.time()-t0:.1f}s]")
