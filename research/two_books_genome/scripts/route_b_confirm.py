#!/usr/bin/env python3
"""Route-B CONFIRMATION-grade structural comparison (mapping-free).

Formal exponent fits with error bars:
  - DFA Hurst alpha  (long-range correlation; ~0.5 = none)
  - MI-decay gamma   (I(d) ~ d^-gamma; small = long memory)
  - unigram redundancy, gzip ratio
Error bars: non-overlapping chunks of length L; report mean +- 95% CI across chunks.
Mapping-free: NO letter->codon cipher. The decisive question is whether language and
the REAL genome share a long-range structural CLASS (overlapping Hurst/MI_gamma CIs,
both separated from their shuffles) -- NOT just "both non-random".

Usage:  python route_b_confirm.py <cds.fasta> <language.txt> [chunkLen]
Swap the language file for data/quran/quran_arabic_concat.txt once built.
For the REAL run: use the WHOLE RefSeq CDS (this 6-gene set is far too small -- note
the wide CIs below), and uncap the language length.
"""
import re, zlib, math, json, random, sys
from collections import Counter
import numpy as np
random.seed(11); np.random.seed(11)

def load_fasta(p):
    s=''.join(l.strip() for l in open(p) if not l.startswith('>'))
    return re.sub('[^ACGT]','',s.upper())
def load_text(p):
    return re.sub('[^a-z]','',open(p,encoding='utf-8',errors='ignore').read().lower())
def codes(s):
    a=sorted(set(s)); idx={c:i for i,c in enumerate(a)}
    return np.array([idx[c] for c in s]), len(a)
def redundancy(s,A):
    c=Counter(s); n=len(s); H=-sum((v/n)*math.log2(v/n) for v in c.values())
    return 1-H/math.log2(A)
def gzipr(s): b=s.encode(); return len(zlib.compress(b,9))/len(b)
def mi(cd,A,d):
    x=cd[:-d]; y=cd[d:]; n=len(x); J=np.zeros((A,A)); np.add.at(J,(x,y),1.0); J/=n
    px=J.sum(1); py=J.sum(0); nz=J>0
    v=float(np.sum(J[nz]*np.log2(J[nz]/np.outer(px,py)[nz])))
    bias=((np.sum(px>0)-1)*(np.sum(py>0)-1))/(2*n*math.log(2))
    return max(v-bias,1e-12)
def mi_decay(s):
    cd,A=codes(s); ds=[d for d in [1,2,3,5,8,13,21] if d<len(s)//4]
    y=np.array([mi(cd,A,d) for d in ds]); x=np.log(ds); pos=y>1e-9
    if pos.sum()<3: return float('nan')
    return float(-np.polyfit(x[pos],np.log(y[pos]),1)[0])
def dfa(s):
    c=Counter(s); ranked=sorted(c,key=lambda k:-c[k]); top=set(ranked[:max(1,len(ranked)//2)])
    x=np.array([1.0 if ch in top else -1.0 for ch in s]); y=np.cumsum(x-x.mean()); N=len(y)
    ns=np.unique(np.logspace(np.log10(8),np.log10(max(16,N//4)),12).astype(int)); F=[]
    for n in ns:
        if n<4 or n>N//2: continue
        m=N//n; seg=y[:m*n].reshape(m,n); t=np.arange(n); Am=np.vstack([t,np.ones(n)]).T
        co,_,_,_=np.linalg.lstsq(Am,seg.T,rcond=None); tr=(Am@co).T
        F.append(math.sqrt(((seg-tr)**2).mean()))
    ns=ns[:len(F)]; return float(np.polyfit(np.log(ns),np.log(F),1)[0])
def chunk_stats(s,L=1000):
    K=len(s)//L; rows={'redundancy':[],'gzip':[],'Hurst':[],'MI_gamma':[]}
    for k in range(K):
        c=s[k*L:(k+1)*L]; cd,A=codes(c)
        rows['redundancy'].append(redundancy(c,A)); rows['gzip'].append(gzipr(c))
        rows['Hurst'].append(dfa(c)); rows['MI_gamma'].append(mi_decay(c))
    out={}
    for k,v in rows.items():
        v=np.array([x for x in v if np.isfinite(x)])
        ci=1.96*v.std(ddof=1)/math.sqrt(len(v)) if len(v)>1 else float('nan')
        out[k]=(float(v.mean()),float(ci),int(len(v)))
    return out,K
def shuf(s):
    l=list(s); random.shuffle(l); return ''.join(l)

if __name__=='__main__':
    CDS=sys.argv[1] if len(sys.argv)>1 else 'data/examples/human_cds_set.fasta'
    TXT=sys.argv[2] if len(sys.argv)>2 else 'english_raw.txt'
    L=int(sys.argv[3]) if len(sys.argv)>3 else 1000
    cds=load_fasta(CDS); txt=load_text(TXT)[:30000]
    sets=[('CDS_real',cds),('CDS_shuffled',shuf(cds)),('Lang',txt),('Lang_shuffled',shuf(txt))]
    res={}
    print(f"{'sequence':16}{'N':>7}{'chunks':>7}  redundancy      gzip            Hurst(DFA)      MI_gamma")
    for name,s in sets:
        st,K=chunk_stats(s,L); res[name]={'N':len(s),'chunks':K,'metrics':st}
        f=lambda m:(f"{st[m][0]:.3f}±{st[m][1]:.3f}")
        print(f"{name:16}{len(s):7d}{K:7d}  {f('redundancy'):15} {f('gzip'):15} {f('Hurst'):15} {f('MI_gamma'):15}")
    json.dump(res,open('confirm_results.json','w'),indent=2)
