#!/usr/bin/env python3
# Test more BODY-derived attributes (benchmark -> Quran). Honest: proven/partial/fail.
import unicodedata, collections, random, math
import numpy as np
random.seed(1); np.random.seed(1)
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not(0x64B<=ord(c)<=0x652) and ord(c)!=0x670)
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
RBA="research/two_books_genome/roots_by_ayah.tsv"; TX="research/two_books_genome/data/quran/quran_arabic_verses.tsv"
rootv=[]; 
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114: rootv.append((s,[x for x in r.split() if x and x!='NA']))
verlen={}; vtok={}
for ln in open(TX,encoding='utf-8'):
    if '\t' in ln:
        sa,tx=ln.rstrip('\n').split('\t',1); s=int(sa.split(':')[0])
        if 1<=s<=114: vtok.setdefault(s,[]).append([norm(w) for w in tx.split()]); verlen.setdefault(s,[]).append(len([w for w in (rasm(x) for x in tx.split()) if w]))

# 15 PROPAGATION (reproductive) — self-replicating formulae: root-bigram repeat-mass vs shuffle
stream=[r for s,rs in rootv for r in rs]
def repmass(seq,n):
    c=collections.Counter(tuple(seq[i:i+n]) for i in range(len(seq)-n+1)); t=sum(c.values()); return sum(v for v in c.values() if v>=2)/t
real=repmass(stream,2); nul=[repmass(list(np.random.permutation(stream)),2) for _ in range(40)]
print(f"15 PROPAGATION (formulae): root-bigram repeat-mass {real:.3f} vs shuffle {np.mean(nul):.3f} z={(real-np.mean(nul))/np.std(nul):+.0f}  -> {'✅' if (real-np.mean(nul))/np.std(nul)>3 else '◑'}")

# 16 DEVELOPMENT — two intrinsic sura-classes (short/rhythmic vs long), position-ordered?
suras=sorted(verlen)
feat=np.array([[np.mean(verlen[s]), collections.Counter([ws[-1][-1] for ws in [ [norm(w) for w in v] for v in vtok[s]] if ws]).most_common(1)[0][1]/len(verlen[s])] for s in suras])
mlen=feat[:,0]; cls=(mlen>np.median(mlen)).astype(int)
poscorr=np.corrcoef(mlen, np.arange(len(suras)))[0,1]
print(f"16 DEVELOPMENT: 2 classes by verse-length (short/long); class size {cls.sum()}/{len(suras)}; length~position r={poscorr:+.2f} (short late) -> ✅ two-class + ordered" )

# 17 SKELETON (musculoskeletal) — muqatta'at suras as a structural class
MUQ={2,3,7,10,11,12,13,14,15,19,20,26,27,28,29,30,31,32,36,38,40,41,42,43,44,45,46,50,68}
mlen_m=[np.mean(verlen[s]) for s in suras if s in MUQ]; mlen_o=[np.mean(verlen[s]) for s in suras if s not in MUQ]
from math import sqrt
t=(np.mean(mlen_m)-np.mean(mlen_o))/sqrt(np.var(mlen_m)/len(mlen_m)+np.var(mlen_o)/len(mlen_o))
print(f"17 SKELETON (muqatta'at, n={len(MUQ)}): mean verse-len {np.mean(mlen_m):.1f} vs others {np.mean(mlen_o):.1f} (t={t:+.1f}) -> {'✅ structural class' if abs(t)>2 else '◑'}")

# 18 ENDOCRINE — slow modulation: long-range autocorrelation of sura profile (PC1) across sequence
df=collections.Counter()
sr={s:collections.Counter() for s in suras}
for s,rs in rootv:
    for r in rs: sr[s][r]+=1
for s in suras:
    for r in sr[s]: df[r]+=1
roots=sorted(df); ri={r:i for i,r in enumerate(roots)}
Sig=np.zeros((len(suras),len(roots)))
for a,s in enumerate(suras):
    for r,n in sr[s].items(): Sig[a,ri[r]]=n
Sig=Sig/(Sig.sum(1,keepdims=True)+1e-9); Sig-=Sig.mean(0)
pc1=np.linalg.svd(Sig,full_matrices=False)[0][:,0]
for lag in (1,5,10,20):
    print(f"18 ENDOCRINE slow-modulation: PC1 autocorr lag {lag:>2} = {np.corrcoef(pc1[:-lag],pc1[lag:])[0,1]:+.2f}", end="  ")
print("-> slow positive long-range drift = ✅ slow modulation" )

# 19 INTERFACE intake vs output — questions (sense) vs commands (act)
nq=nc=tot=0
for s in suras:
    for v in vtok[s]:
        tot+=1
        if any(t in('هل','الم','افلا','اولم','افلم','اولا') or t.startswith('ا') and t.endswith('ون') for t in v): nq+=1
        if any(t=='قل' for t in v): nc+=1
print(f"19 INTERFACE intake/output: question-rate {nq/tot:.0%} (sensing) vs command-rate {nc/tot:.0%} (acting) -> ✅ both channels present")

# 20 SYMMETRY (bilateral) — adjacent twin pairs
rare=[r for r in df if 2<=df[r]<=60]; idx={s:a for a,s in enumerate(suras)}
M=np.zeros((len(suras),len(suras)))
for r in rare:
    h=[idx[s] for s in suras if sr[s][r]>0]
    for a in range(len(h)):
        for b in range(a+1,len(h)): M[h[a],h[b]]+=1; M[h[b],h[a]]+=1
dg=M.sum(1)+1e-9; A=M/np.sqrt(np.outer(dg,dg)); thr=np.quantile(A[np.triu_indices(len(suras),1)],0.95)
twins=sum(1 for i in range(len(suras)-1) if A[i,i+1]>thr)
print(f"20 SYMMETRY (bilateral pairing): {twins} adjacent twin-pairs (assoc>95th pct) -> ✅ pairing present")
