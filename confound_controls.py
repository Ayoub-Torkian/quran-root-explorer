"""Confound controls for the two implementation front-runners, before recommending."""
from __future__ import annotations
import sys, time
import numpy as np
from collections import Counter
sys.path.insert(0,".")
import analysis as A
from analysis import COL_SURAH, COL_AYAH, normalize_letters
from scipy.stats import spearmanr, rankdata
rng=np.random.default_rng(0); t0=time.time()
corpus=A.load_corpus("Book6.xlsx")
K=normalize_letters
su=corpus.df[COL_SURAH].astype(int).to_numpy()
order=np.lexsort((corpus.df[COL_AYAH].astype(int).to_numpy(),su)); su=su[order]
vlen=np.array([sum(len(normalize_letters(t)) for t in corpus.seg_tokens[i]) for i in order],dtype=float)
rt=[[K(t) for t in corpus.root_tokens[i]] for i in order]
def dfa(x):
    x=x-x.mean(); y=np.cumsum(x)
    sc=np.unique(np.logspace(np.log10(16),np.log10(len(x)//8),16).astype(int)); F=[]
    for s in sc:
        ns=len(y)//s
        if ns<1: continue
        g=y[:ns*s].reshape(ns,s); t=np.arange(s)
        F.append(np.mean([np.sqrt(np.mean((r-np.polyval(np.polyfit(t,r,1),t))**2)) for r in g]))
    F=np.array(F); sc=sc[:len(F)]; return float(np.polyfit(np.log(sc),np.log(F),1)[0])

print("=== IDEA 1 control: is verse-length long memory genuine or surah-BLOCK structure? ===")
a_raw=dfa(vlen)
# within-surah detrend: subtract each surah's own mean -> removes block/level structure
det=vlen.copy()
for s in np.unique(su):
    m=su==s; det[m]=vlen[m]-vlen[m].mean()
a_det=dfa(det)
# also: shuffle surah blocks order (keep within-surah intact) -> across-surah only
print(f"  DFA raw verse-length            = {a_raw:.3f}")
print(f"  DFA within-surah detrended      = {a_det:.3f}   (if ~0.5 => was block structure)")
print(f"  verdict: {'GENUINE within-surah long memory' if a_det>0.6 else 'largely surah-block / level structure'}")

print("\n=== IDEA 10 control: is richness~revelation a CHRONOLOGY effect or a LENGTH artifact? ===")
rev=corpus.rev_order_of_surah
tmp={}
for k,toks in enumerate(rt): tmp.setdefault(int(su[k]),[]).extend(toks)
S=[s for s in tmp if s in {int(x) for x in rev}]
revv=np.array([rev[s] for s in S],dtype=float)
length=np.array([len(tmp[s]) for s in S],dtype=float)
ttr=np.array([len(set(tmp[s]))/max(len(tmp[s]),1) for s in S])     # type-token ratio (length-biased)
def shannon(c):
    p=np.array(list(Counter(c).values()),float); p/=p.sum(); return float(-(p*np.log2(p)).sum())
ent=np.array([shannon(tmp[s]) for s in S])                          # root entropy (less length-biased)
def pspear(a,b,c):  # partial spearman of a,b controlling c
    ra,rb,rc=rankdata(a),rankdata(b),rankdata(c)
    def resid(y,x):
        x1=np.vstack([x,np.ones_like(x)]).T
        beta=np.linalg.lstsq(x1,y,rcond=None)[0]; return y-x1@beta
    return float(np.corrcoef(resid(ra,rc),resid(rb,rc))[0,1])
print(f"  spearman(rev, type-token ratio)         = {spearmanr(revv,ttr)[0]:+.3f} p={spearmanr(revv,ttr)[1]:.2g}")
print(f"  spearman(rev, surah length)             = {spearmanr(revv,length)[0]:+.3f}")
print(f"  spearman(length, type-token ratio)      = {spearmanr(length,ttr)[0]:+.3f}  (mechanical: TTR falls with length)")
print(f"  PARTIAL spearman(rev, TTR | length)     = {pspear(revv,ttr,length):+.3f}  (chronology effect net of length)")
print(f"  spearman(rev, root ENTROPY)             = {spearmanr(revv,ent)[0]:+.3f} p={spearmanr(revv,ent)[1]:.2g}")
print(f"  PARTIAL spearman(rev, entropy | length) = {pspear(revv,ent,length):+.3f}")
print(f"\n[total {time.time()-t0:.1f}s]")
