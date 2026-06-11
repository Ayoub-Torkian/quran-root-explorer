# MODALITY 46 (variant B, data-driven) — field clusters via per-corpus TF-IDF->SVD->KMeans(K=6).
# Every unit labeled (removes the seed-lexicon OTHER bias). Same shuffle-controlled sequencing +
# cohesion excess as variant A. Result: NULL (confirms variant A). See EVIDENCE #46.
# RUN DISCIPLINE: author/run in /tmp via heredoc (mount read lags); set ROOT to this session's mount.
import re, sys, os, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_DIACRITIZED as D
rng = np.random.default_rng(42)
_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nl(t):
    t=_DIA.sub("",str(t)); t=re.sub(r"[آأإٱ]","ا",t); t=re.sub(r"[ىی]","ي",t)
    t=re.sub(r"[ةھ]","ه",t); return t.replace("ک","ك").replace("ؤ","ء").replace("ئ","ء").strip()
def doc(s): return " ".join(w for w in WA.findall(nl(s)) if w)
K=6
def cluster_labels(docs):
    docs=[d if d.strip() else "x" for d in docs]
    X=TfidfVectorizer(analyzer=str.split,min_df=2).fit_transform(docs)
    k=min(50,X.shape[1]-1,X.shape[0]-1)
    if k<5: return None
    V=TruncatedSVD(n_components=k,random_state=0).fit_transform(X)
    return list(KMeans(n_clusters=K,n_init=4,random_state=0).fit_predict(V))
def switch_rate(lab): return float(np.mean([lab[i]!=lab[i+1] for i in range(len(lab)-1)])) if len(lab)>1 else None
def transition_mi(lab):
    if len(lab)<3: return None
    M=np.zeros((K,K))
    for x,y in zip(lab[:-1],lab[1:]): M[x,y]+=1
    P=M/M.sum(); Px=P.sum(1,keepdims=True); Py=P.sum(0,keepdims=True)
    with np.errstate(divide="ignore",invalid="ignore"): mi=np.nansum(P*np.log((P+1e-12)/(Px*Py+1e-12)))
    Hx=-np.nansum(Px*np.log(Px+1e-12)); return float(mi/(Hx+1e-12)) if Hx>0 else 0.0
def run_len(lab):
    if len(lab)<2: return None
    r=1
    for i in range(1,len(lab)):
        if lab[i]!=lab[i-1]: r+=1
    return len(lab)/r
def stat_excess(lab,W,B,fn):
    if len(lab)<W: return None
    v=[]
    for _ in range(B):
        s=rng.integers(0,len(lab)-W+1); win=lab[s:s+W]; a=fn(win); sh=list(win); rng.shuffle(sh); b=fn(sh)
        if a is not None and b is not None: v.append(a-b)
    return np.array(v) if v else None
def g(a,b): return (a.mean()-b.mean())/(np.sqrt((a.var()+b.var())/2)+1e-9) if (a is not None and b is not None and len(a)>1 and len(b)>1) else float("nan")
def boot_p(a,b,R=2000):
    ai=rng.integers(0,len(a),R); bi=rng.integers(0,len(b),R); return float(np.mean(a[ai]>b[bi])+0.5*np.mean(a[ai]==b[bi]))

def main():
    c=A.load_corpus(os.path.join(ROOT,"Book6.xlsx"))
    q=[doc(str(c.df.iloc[i][D])) for i in range(len(c.df))]
    US=re.compile(r"[.!؟?\n،؛:]+")
    def file_docs(paths):
        txt="".join("\n"+open(p,encoding="utf-8",errors="ignore").read() for p in paths)
        return [doc(u) for u in US.split(txt) if len(u.split())>=2]
    CP=os.path.join(ROOT,"sequence_tests","corpus")+"/"
    docs={"QURAN":q,
     "ord-Arabic":file_docs([CP+f+".txt" for f in("ar_tabari","ar_classical2","ar_novel","ar_news","ar_news2")]),
     "poetry":file_docs([CP+"ar_poetry.txt"]),
     "saj'":file_docs([CP+"ar_sajprose.txt",CP+"ar_saj_hariri.txt"])}
    corp={k:cluster_labels(v) for k,v in docs.items()}
    print("units:",{k:(len(v) if v else 0) for k,v in corp.items()})
    W,B=40,400
    EX={k:{s:stat_excess(corp[k],W,B,fn) for s,fn in [("switch",switch_rate),("MI",transition_mi),("run",run_len)]} for k in corp if corp[k]}
    for s in ("switch","MI","run"):
        print(f"\n-- {s} excess --")
        for k in EX: print(f"   {k:11s} mean={EX[k][s].mean():+.4f}")
        for comp in ("ord-Arabic","poetry","saj'"):
            if comp in EX: print(f"   QURAN vs {comp:11s}: g={g(EX['QURAN'][s],EX[comp][s]):+.2f}sd  P={boot_p(EX['QURAN'][s],EX[comp][s]):.2f}")

if __name__ == "__main__": main()
