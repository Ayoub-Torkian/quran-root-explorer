import re, sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
rng=np.random.default_rng(0); t0=time.time(); W=re.compile(r"[^\W\d_]+",re.UNICODE)
def repC(s,n):
    a=np.frombuffer(bytes(s,'utf-16-le'),dtype=np.uint16)  # char ids cheap
    if len(a)<=n: return 0.0
    g=Counter(a[i:i+n].tobytes() for i in range(len(a)-n)); return 1-len(g)/max(sum(g.values()),1)
def win_rep(s,N=2500,step=1000,maxw=60):
    out=[]
    for c in range(0,max(1,len(s)-N+1),step):
        sub=s[c:c+N]
        if len(sub)<N*0.8: break
        out.append([repC(sub,8),repC(sub,12),repC(sub,20)])
        if len(out)>=maxw: break
    return np.array(out) if out else np.array([[repC(s,8),repC(s,12),repC(s,20)]])
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
reg={"Quran":qw,"Tabari(classical)":load_ar("corpus/ar_tabari.txt"),
     "Novel(literary)":load_ar("corpus/ar_novel.txt"),"News(MSA)":load_ar("corpus/ar_news.txt")}
S={k:" ".join(v) for k,v in reg.items()}
D={k:win_rep(v) for k,v in S.items()}
names=["rep8","rep12","rep20"]
print(f"[{time.time()-t0:.1f}s] SCALED 3-register test — per-register windows & means")
for k in reg: print(f"   {k:20s} words={len(reg[k]):6d} windows={len(D[k])}")
print(f"\n  {'metric':7s}"+"".join(f"{k.split('(')[0]:>11}" for k in reg))
for j,m in enumerate(names):
    print(f"  {m:7s}"+"".join(f"{D[k][:,j].mean():11.4f}" for k in reg))
print("\n  Quran vs each register (Welch-style sd units) and bootstrap P(Quran>reg):")
for j,m in enumerate(names):
    q=D["Quran"][:,j]
    line=f"   {m:7s}"
    for k in ["Tabari(classical)","Novel(literary)","News(MSA)"]:
        r=D[k][:,j]; csd=np.sqrt((q.var()+r.var())/2)+1e-9; g=(q.mean()-r.mean())/csd
        # bootstrap P(quran window > reg window)
        bp=np.mean(rng.choice(q,4000)>rng.choice(r,4000))
        line+=f"  {k.split('(')[0][:6]}:{g:+.1f}sd/P={bp:.2f}"
    print(line)

# frequency control: rep on word-stream with top-20 most frequent WORDS removed (content-only)
print("\n  FREQUENCY CONTROL — char rep after removing top-20 frequent words (content-only stream):")
def content_stream(words,topn=20):
    top=set(w for w,_ in Counter(words).most_common(topn)); return " ".join(w for w in words if w not in top)
for k in ["Quran","Tabari(classical)","News(MSA)"]:
    cs=content_stream(reg[k]); d=win_rep(cs)
    print(f"   {k:20s} rep8={d[:,0].mean():.4f} rep12={d[:,1].mean():.4f} (content-only)")
print(f"\n[total {time.time()-t0:.1f}s]")
