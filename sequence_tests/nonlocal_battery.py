import re, sys, time, gzip
import numpy as np
from collections import Counter, defaultdict
sys.path.insert(0,"/sessions/nice-jolly-hypatia/mnt/Quran_Root_Explorer_Web_v1.2")
import analysis as A
from analysis import normalize_letters
rng=np.random.default_rng(0); t0=time.time(); W=re.compile(r"[^\W\d_]+",re.UNICODE)
def encode(s):
    al=sorted(set(s)); vm={c:i for i,c in enumerate(al)}
    return np.array([vm[c] for c in s],dtype=np.int64), len(al)
def MIlag(a,K,d):
    if a.size<=d: return 0.0
    x=a[:-d];y=a[d:]; j=np.bincount(x*K+y,minlength=K*K).astype(float)/x.size; pj=j.reshape(K,K)
    px=pj.sum(1);py=pj.sum(0);nz=pj>0; return float(np.sum(pj[nz]*np.log2(pj[nz]/np.outer(px,py)[nz])))
def rep(a,n):
    if len(a)<=n: return 0.0
    g=Counter(a[i:i+n].tobytes() for i in range(len(a)-n)); return 1-len(g)/max(sum(g.values()),1)
def gz(a): return len(gzip.compress(a.astype(np.int16).tobytes()))/(2*max(len(a),1))
def dfa(a):
    x=np.cumsum(a-a.mean()); N=len(x)
    if N<400: return float('nan')
    scales=np.unique(np.floor(np.logspace(np.log10(16),np.log10(N//4),8)).astype(int)); F=[]
    for s in scales:
        nseg=N//s
        if nseg<2: continue
        seg=x[:nseg*s].reshape(nseg,s); t=np.arange(s); tt=t-t.mean()
        sl=(seg*tt).sum(1)/(tt*tt).sum(); fit=seg.mean(1)[:,None]+sl[:,None]*tt[None,:]
        F.append((s,np.sqrt(((seg-fit)**2).mean())))
    F=np.array([f for f in F if f[1]>0])
    return float(np.polyfit(np.log(F[:,0]),np.log(F[:,1]),1)[0]) if len(F)>=3 else float('nan')
def nonlocal_metrics(a,K):
    MI_long=sum(MIlag(a,K,d) for d in (64,128,256,512))   # dependence at LONG distances
    MI_mid =sum(MIlag(a,K,d) for d in (8,16,32))
    return dict(MI_mid=MI_mid, MI_long=MI_long, rep12=rep(a,12), rep20=rep(a,20),
                dfa=dfa(a), comp=gz(a))
def metrics_str(s):
    a,K=encode(s); return nonlocal_metrics(a,K)

# build rasm streams
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
print(f"[{time.time()-t0:.1f}s] Quran rasm={len(qs)}c  Tabari rasm={len(ts)}c")

# ---- NON-LOCALITY VALIDITY: ladder on a Quran 8000-char window ----
samp=qs[:8000]; a0,K=encode(samp)
def block_shuffle(a,B=200):
    nb=len(a)//B; blocks=[a[i*B:(i+1)*B] for i in range(nb)]; rng.shuffle(blocks)
    return np.concatenate(blocks+[a[nb*B:]])
def full_shuffle(a):
    b=a.copy(); rng.shuffle(b); return b
L0=nonlocal_metrics(a0,K)
Lblk=nonlocal_metrics(block_shuffle(a0),K)
Lful=nonlocal_metrics(full_shuffle(a0),K)
print("\n=== NON-LOCALITY LADDER (Quran 8k-char window) ===")
print("  metric    L0_orig  Lblock(order)  Lfull   | non-local? (L0>Lblock => yes)")
for k in ["MI_mid","MI_long","rep12","rep20","dfa","comp"]:
    nl = "NON-LOCAL" if (not np.isnan(L0[k]) and abs(L0[k]-Lblk[k])>0.05*abs(L0[k]+1e-9) and (L0[k]>Lblk[k])==(k!='comp')) else "local/flat"
    print(f"  {k:8s} {L0[k]:8.4f} {Lblk[k]:13.4f} {Lful[k]:8.4f}   {nl}")

# ---- equal-N (8000c) Quran vs Tabari + beyond own-Markov ----
def windows(s,N=8000,step=4000,maxw=12):
    a,K=encode(s); rows=[]
    for c in range(0,max(1,len(a)-N+1),step):
        sub=a[c:c+N]
        if sub.size<N*0.6: break
        rows.append(nonlocal_metrics(sub,K))
        if len(rows)>=maxw: break
    ks=rows[0].keys(); return {k:np.array([r[k] for r in rows]) for k in ks}, len(rows)
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
Q,nq=windows(qs); T,nt=windows(ts)
qa,K=encode(qs[:40000]); qmk_arr=char_markov(qa,K); inv={i:c for i,c in enumerate(sorted(set(qs[:40000])))}
Mk,nm=windows("".join(inv[int(x)] for x in qmk_arr))
print(f"\n=== EQUAL-N (8000c) Quran vs Tabari(ordinary) vs Quran-own-Markov  (Q n={nq}, Tabari n={nt}) ===")
print(f"  {'metric':8s}{'QURAN':>12}{'Tabari':>12}{'Q-Markov':>12}   Q-vs-Tabari   beyond-Markov?")
for k in ["MI_mid","MI_long","rep12","rep20","dfa","comp"]:
    qmu,qsd=Q[k].mean(),Q[k].std(); tmu=T[k].mean(); mmu=Mk[k].mean()
    g=(qmu-tmu)/(qsd+1e-9); bm = "yes" if (not np.isnan(qmu) and abs(qmu-mmu)>0.05*abs(mmu+1e-9)) else "no"
    print(f"  {k:8s}{qmu:12.4f}{tmu:12.4f}{mmu:12.4f}   {g:+6.1f}sd      {bm}")
print(f"\n[total {time.time()-t0:.1f}s]")
