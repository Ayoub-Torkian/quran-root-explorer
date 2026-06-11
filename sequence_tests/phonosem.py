import re, time, warnings
import numpy as np, pandas as pd
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
ROOT="/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2"
rng=np.random.default_rng(23); t0=time.time()
_DIA=re.compile(r"[ً-ٰٟۖ-ۭ]"); _TAT=re.compile("ـ"); WA=re.compile(r"[^\W\d_]+",re.UNICODE)
def nl(t):
    t=_TAT.sub("",_DIA.sub("",str(t)))
    t=re.sub(r"[آأإٱ]","ا",t); t=re.sub(r"[ىی]","ي",t); t=re.sub(r"[ةھ]","ه",t)
    return t.replace("ک","ك").replace("ؤ","ء").replace("ئ","ء").strip()
def words(s): return [w for w in WA.findall(nl(str(s))) if w]
# mutually-exclusive phonetic classes (place/manner): heavy<->smooth contrast
CLS={}
for ch in "صضطظ": CLS[ch]=0   # emphatics
for ch in "ق":   CLS[ch]=1   # uvular qaf
for ch in "ءهعحغخ": CLS[ch]=2 # gutturals
for ch in "بتدكج": CLS[ch]=3 # stops
for ch in "سشزثذف": CLS[ch]=4 # sibilants/fricatives
for ch in "لر":  CLS[ch]=5   # liquids
for ch in "من":  CLS[ch]=6   # nasals
for ch in "ويا": CLS[ch]=7   # glides/long vowels
NC=8
def phon_vec(ws):
    h=np.zeros(NC); n=0
    for w in ws:
        for ch in w:
            c=CLS.get(ch)
            if c is not None: h[c]+=1; n+=1
    return h/n if n else h

def units_to_arrays(units, k=50):
    units=[u for u in units if len(u)>=3]
    docs=[" ".join(u) for u in units]
    vec=TfidfVectorizer(analyzer=str.split,min_df=2); X=vec.fit_transform(docs)
    k=min(k,X.shape[1]-1,X.shape[0]-1)
    V=normalize(TruncatedSVD(n_components=k,random_state=0).fit_transform(X))   # semantic
    P=normalize(np.array([phon_vec(u) for u in units]))                          # phonetic
    S=[set(u) for u in units]                                                    # word-sets
    return V,P,S
def partial_corr(units, M=8000):
    V,P,S=units_to_arrays(units); n=len(S)
    if n<40: return None
    i=rng.integers(0,n,M); j=rng.integers(0,n,M); m=i!=j; i,j=i[m],j[m]
    sem=np.sum(V[i]*V[j],1); pho=np.sum(P[i]*P[j],1)
    lex=np.array([len(S[a]&S[b])/len(S[a]|S[b]) for a,b in zip(i,j)])
    # residualize sem and pho on lex (+intercept), correlate residuals
    A=np.c_[np.ones_like(lex),lex]
    def resid(y): 
        b=np.linalg.lstsq(A,y,rcond=None)[0]; return y-A@b
    rs,rp=resid(sem),resid(pho)
    pc=np.corrcoef(rs,rp)[0,1]
    # permutation null: shuffle pho residual
    nul=np.array([np.corrcoef(rs,rng.permutation(rp))[0,1] for _ in range(40)])
    z=(pc-nul.mean())/(nul.std()+1e-9)
    return pc,z,n

# ---- GATE: synthetic sound-meaning binding ----
def synth(bound=True, ndoc=400):
    # 6 latent classes; each has semantic markers + phonetic letter-bias
    smark=[["زهر%d"%c,"غصن%d"%c,"نهر%d"%c] for c in range(6)]
    heavy="صضطظقغخ"; smooth="لرمنويا"
    units=[]
    for d in range(ndoc):
        c=rng.integers(0,6)
        u=list(rng.choice(smark[c],2))                       # semantic markers (shared within class)
        pool=heavy if (c%2==0)==bound else (heavy if c%2==0 else smooth)
        pool=heavy if c%2==0 else smooth                      # class-specific phonetics
        if not bound: pool=heavy if rng.random()<0.5 else smooth  # break sound-meaning link
        for _ in range(6):
            u.append("".join(rng.choice(list(pool),rng.integers(3,6))))  # non-marker words follow class phonetics
        units.append(u)
    return units
print("[%.1fs] GATE:"%(time.time()-t0))
g_b=partial_corr(synth(True)); g_s=partial_corr(synth(False))
print("  bound synthetic   : partial_corr=%.3f z=%+.1f"%(g_b[0],g_b[1]))
print("  unbound synthetic : partial_corr=%.3f z=%+.1f"%(g_s[0],g_s[1]))

# ---- registers ----
raw=pd.read_excel(ROOT+"/Book6.xlsx",header=None,nrows=8); hdr=0
for i in range(len(raw)):
    if raw.iloc[i].map(lambda x: nl(x)).str.contains("سوره").any(): hdr=i;break
df=pd.read_excel(ROOT+"/Book6.xlsx",header=hdr); df.columns=[str(c).strip() for c in df.columns]
tcol=[c for c in df.columns if "متن" in nl(c) and "توكن" not in nl(c)][0]
qu=[words(t) for t in df[tcol].fillna("").astype(str).tolist() if len(words(t))>=3]
SENT=re.compile(r"[.!?؟؛\n]+")
prose=[words(x) for fn in ("ar_tabari","ar_classical2","ar_novel","ar_news")
       for x in SENT.split(open("corpus/%s.txt"%fn,encoding="utf-8",errors="ignore").read()) if len(words(x))>=3]
poet=[words(l) for l in open("corpus/ar_poetry.txt",encoding="utf-8",errors="ignore") if len(words(l))>=3]
saj=[words(x) for x in re.split(r"[،.؛:!؟]+",open("corpus/ar_sajprose.txt",encoding="utf-8").read()) if len(words(x))>=3]
print("\n[%.1fs] PHONO-SEMANTIC binding (partial corr sound~meaning | lexical overlap):"%(time.time()-t0))
for name,U in [("Quran",qu),("prose",prose),("poetry",poet),("saj",saj)]:
    r=partial_corr(U)
    if r: print("  %-7s n=%-5d partial_corr=%+.3f  z=%+.1f"%(name,r[2],r[0],r[1]))
print("\n[%.1fs]"%(time.time()-t0))
