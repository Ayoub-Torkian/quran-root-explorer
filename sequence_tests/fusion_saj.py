import re, time, warnings
import numpy as np, pandas as pd
from collections import Counter
warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score
ROOT = "/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng = np.random.default_rng(13); t0 = time.time()
_DIA = re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT = re.compile("ـ"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t = _TAT.sub("", _DIA.sub("", str(t)))
    t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىی]", "ي", t); t = re.sub(r"[ةھ]", "ه", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()
def words(s): return [w for w in WA.findall(nl(str(s))) if w]
def yuleK(w):
    c=Counter(w); N=len(w); vi=Counter(c.values()); return 1e4*(sum(v*(i*i) for i,v in vi.items())-N)/(N*N+1e-9)
def crep(toks,n=12):
    s=" ".join(toks)
    if len(s)<=n: return 0.0
    g=Counter(s[i:i+n] for i in range(len(s)-n)); return 1-len(g)/max(len(s)-n,1)
def feats(units):
    flat=[w for u in units for w in u]
    if len(flat)<25 or len(units)<4: return None
    ends=[u[-1][-2:] if u and len(u[-1])>=2 else (u[-1] if u else "") for u in units]
    ec=Counter([e for e in ends if e]); dom=max(ec.values())/len(ends) if ends else 0
    ulen=np.array([len(u) for u in units]); wl=np.array([len(w) for w in flat])
    top=set(w for w,_ in Counter(flat).most_common(15)); content=[w for w in flat if w not in top]
    return dict(rhyme=dom, unit_cv=ulen.std()/(ulen.mean()+1e-9), std_wl=wl.std(),
                frac_long=float(np.mean(wl>=7)), rep12=crep(content,12), yuleK=yuleK(flat))
FEATS=["rhyme","unit_cv","std_wl","frac_long","rep12","yuleK"]
def mat(rows): return np.array([[r[f] for f in FEATS] for r in rows])

# Quran ayat per surah
raw=pd.read_excel(ROOT+"/Book6.xlsx",header=None,nrows=8); hdr=0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr=i;break
df=pd.read_excel(ROOT+"/Book6.xlsx",header=hdr); df.columns=[str(c).strip() for c in df.columns]
scol=[c for c in df.columns if "سوره" in nl(c) and "اسم" not in nl(c)][0]
tcol=[c for c in df.columns if "متن" in nl(c) and "توكن" not in nl(c)][0]
sur={}
for s,txt in zip(df[scol].tolist(), df[tcol].tolist()):
    try: si=int(float(s))
    except: continue
    if 1<=si<=114: sur.setdefault(si,[]).append(words(txt))
Q=mat([r for r in (feats(ay) for ay in sur.values()) if r])

# poetry windows
pl=[words(ln) for ln in open("corpus/ar_poetry.txt",encoding="utf-8",errors="ignore") if words(ln)]
L=mat([r for r in (feats(pl[i:i+24]) for i in range(0,len(pl)-24,12)) if r])

# ordinary prose: natural sentences
SENT=re.compile(r"[.!?؟؛\n]+")
psent=[words(x) for fn in ("ar_tabari","ar_classical2","ar_novel","ar_news")
       for x in SENT.split(open("corpus/%s.txt"%fn,encoding="utf-8",errors="ignore").read()) if len(words(x))>=3]
P=mat([r for r in (feats(psent[i:i+16]) for i in range(0,len(psent)-16,8)) if r])

# SAJ' prose: clause units (saj'a boundaries ~ punctuation)
sclause=[words(x) for x in re.split(r"[،.؛:!؟]+", open("corpus/ar_sajprose.txt",encoding="utf-8").read()) if len(words(x))>=2]
S=mat([r for r in (feats(sclause[i:i+20]) for i in range(0,max(1,len(sclause)-20),6)) if r])

print("[%.1fs] windows: Quran=%d poetry=%d prose=%d SAJ=%d"%(time.time()-t0,len(Q),len(L),len(P),len(S)))
def g(a,b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9)
print("\nFeature means + Quran-vs-SAJ sd-gap (does any axis separate Quran from saj'?):")
print("  feature   | Quran  | poetry | prose  | SAJ    | Q-vs-SAJ")
for j,f in enumerate(FEATS):
    print("  %-9s | %6.3f | %6.3f | %6.3f | %6.3f | %+.1fsd"%(f,Q[:,j].mean(),L[:,j].mean(),P[:,j].mean(),S[:,j].mean(),g(Q[:,j],S[:,j])))

# Quran vs SAJ classifier
X=np.vstack([Q,S]); y=np.array([1]*len(Q)+[0]*len(S))
clf=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000,class_weight="balanced"))
cv=StratifiedKFold(5,shuffle=True,random_state=0)
auc=cross_val_score(clf,X,y,cv=cv,scoring="roc_auc")
print("\nQURAN vs SAJ' (the adversarial test):")
for j,f in enumerate(FEATS):
    print("   %-9s single AUC=%.3f"%(f,max(roc_auc_score(y,X[:,j]),roc_auc_score(y,-X[:,j]))))
print("   MULTIVARIATE AUC = %.3f +/- %.3f"%(auc.mean(),auc.std()))
nl_=[cross_val_score(clf,X,rng.permutation(y),cv=cv,scoring="roc_auc").mean() for _ in range(20)]
print("   label-shuffle null = %.3f"%np.mean(nl_))
# cell: rhyme>prose-median AND unit_cv>poetry-median
ri,ci=FEATS.index("rhyme"),FEATS.index("unit_cv"); rt=np.median(P[:,ri]); ct=np.median(L[:,ci])
def cell(M): return 100*np.mean((M[:,ri]>rt)&(M[:,ci]>ct))
print("\nCELL occupancy (rhyme>prose-med AND unit_cv>poetry-med): Quran %.0f%% | poetry %.0f%% | prose %.0f%% | SAJ %.0f%%"%(cell(Q),cell(L),cell(P),cell(S)))
print("[%.1fs]"%(time.time()-t0))
