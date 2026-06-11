import re, sys, time, gzip
import numpy as np
from collections import Counter, defaultdict
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
rng=np.random.default_rng(0); t0=time.time(); W=re.compile(r"[^\W\d_]+",re.UNICODE)
def encode(s):
    al=sorted(set(s)); vm={c:i for i,c in enumerate(al)}
    return np.frombuffer(bytes(vm[c] for c in s),dtype=np.uint8).astype(np.int64), len(al)
def H(keys):
    _,cnt=np.unique(keys,return_counts=True); p=cnt/cnt.sum(); return float(-np.sum(p*np.log2(p)))
def cond_entropy(a,K,n):
    if a.size<=n: return 0.0
    if n==0: return H(a)
    ctx=np.zeros(a.size-n,dtype=np.int64)
    for k in range(n): ctx=ctx*K+a[k:a.size-n+k]
    nxt=a[n:]; return H(ctx*K+nxt)-H(ctx)
def MIlag(a,K,d):
    if a.size<=d: return 0.0
    x=a[:-d];y=a[d:]; j=np.bincount(x*K+y,minlength=K*K).astype(float)/x.size; pj=j.reshape(K,K)
    px=pj.sum(1);py=pj.sum(0);nz=pj>0; return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
def ngram_rep(a,n):
    if len(a)<=n: return 0.0
    g=Counter(tuple(a[i:i+n].tolist()) for i in range(len(a)-n)); return 1-len(g)/max(sum(g.values()),1)
def comp_ratio(a): return len(gzip.compress(a.astype(np.int16).tobytes()))/(2*max(len(a),1))
def dfa(a):
    x=np.cumsum(a-a.mean()); N=len(x)
    if N<200: return float('nan')
    scales=np.unique(np.floor(np.logspace(np.log10(8),np.log10(N//4),7)).astype(int)); F=[]
    for s in scales:
        nseg=N//s
        if nseg<2: continue
        seg=x[:nseg*s].reshape(nseg,s); t=np.arange(s); tt=t-t.mean()
        sl=(seg*tt).sum(1)/(tt*tt).sum(); ic=seg.mean(1)
        fit=ic[:,None]+sl[:,None]*tt[None,:]; F.append((s,np.sqrt(((seg-fit)**2).mean())))
    F=np.array([f for f in F if f[1]>0])
    return float(np.polyfit(np.log(F[:,0]),np.log(F[:,1]),1)[0]) if len(F)>=3 else float('nan')
def metrics(a,K,with_dfa=False):
    m=dict(h1=cond_entropy(a,K,1),h2=cond_entropy(a,K,2),h3=cond_entropy(a,K,3),
           MI_near=MIlag(a,K,1)+MIlag(a,K,2), MI_far=MIlag(a,K,8)+MIlag(a,K,16)+MIlag(a,K,32),
           rep3=ngram_rep(a,3),rep5=ngram_rep(a,5),comp=comp_ratio(a))
    m["excessE"]=max(cond_entropy(a,K,1)-m["h2"],0)+max(m["h2"]-m["h3"],0)
    if with_dfa: m["dfa"]=dfa(a)
    return m
def char_markov(a,K):
    tr=defaultdict(Counter)
    for i in range(1,len(a)): tr[int(a[i-1])][int(a[i])]+=1
    succ={};cdf={}
    for st,c in tr.items():
        ks=np.array(list(c.keys()));vs=np.array(list(c.values()),float);succ[st]=ks;cdf[st]=np.cumsum(vs/vs.sum())
    out=a.copy()
    for i in range(1,len(a)):
        p=int(out[i-1]); out[i]=succ[p][np.searchsorted(cdf[p],rng.random())] if p in succ else rng.integers(K)
    return out
def win(s,N=4000,step=2000,maxw=10):
    a,K=encode(s); rows=[]
    for c in range(0,max(1,len(a)-N+1),step):
        sub=a[c:c+N]
        if sub.size<N*0.6: break
        rows.append(metrics(sub,K)); 
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}, len(rows)

corp=A.load_corpus("/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2/Book6.xlsx")
col='متن آیه با حرکت'
qwords=[normalize_letters(w) for i in range(len(corp.df)) for w in str(corp.df.iloc[i][col]).split() if normalize_letters(w)]
qs=" ".join(qwords)
tab=[]
for ln in open("corpus/ar_tabari.txt",encoding="utf-8",errors="ignore"):
    ss=ln.strip()
    if not ss or ss.startswith("صحيح"): continue
    tab+=[normalize_letters(w) for w in W.findall(ss) if normalize_letters(w)]
ts=" ".join(tab)
print(f"[{time.time()-t0:.1f}s] Quran rasm={len(qs)} chars  Tabari rasm={len(ts)} chars")

# ladder (validity) on one 8k-word Quran sample
def lad(words):
    w2=words.copy(); rng.shuffle(w2)
    ch=list(" ".join(words).replace(" ","")); rng.shuffle(ch)
    return {"L0":" ".join(words),
            "L1_inword":" ".join("".join(rng.permutation(list(w))) for w in words),
            "L2_wordord":" ".join(w2),
            "L4_scramble":"".join(ch)}
print("\n=== LADDER (Quran rasm 8k words): metric should move monotonically as structure is destroyed ===")
variants=lad(qwords[:8000]); mv={}
for n,s in variants.items(): a,K=encode(s); mv[n]=metrics(a,K,with_dfa=True)
ks=["h1","h2","h3","excessE","MI_near","MI_far","rep3","rep5","comp","dfa"]
print(f"  {'metric':9s}"+"".join(f"{n:>13}" for n in variants))
for k in ks: print(f"  {k:9s}"+"".join(f"{mv[n][k]:13.4f}" for n in variants))

print("\n=== EQUAL-N (4000c) Quran vs Tabari(ordinary) vs Quran-own-Markov ===")
qm,nq=win(qs); tm,nt=win(ts)
qa,K=encode(qs[:40000]); qmk="".join(chr(65+int(x)) for x in char_markov(qa,K)); mm,nm=win(qmk)
print(f"  windows: Q={nq} Tabari={nt} Q-Markov={nm}")
ks2=["h1","h2","h3","excessE","MI_near","MI_far","rep3","rep5","comp"]
print(f"  {'metric':9s}{'QURAN':>14}{'Tabari':>14}{'Q-Markov':>14}   Q-vs-Tabari")
for k in ks2:
    qmu,qsd=qm[k].mean(),qm[k].std(); tmu=tm[k].mean(); mmu=mm[k].mean()
    g=(qmu-tmu)/(qsd+1e-9); tag=f"{g:+.1f}sd" if not np.isnan(g) else ""
    print(f"  {k:9s}{qmu:14.4f}{tmu:14.4f}{mmu:14.4f}   {tag}")
print(f"\n[total {time.time()-t0:.1f}s]")
