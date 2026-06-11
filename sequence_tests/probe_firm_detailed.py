# PROBE C — firm-then-detailed direction (11:1; P3 / course M04). Pre-stated, run 2026-06-07,
# PYTHONHASHSEED=0, seed 0. Replicates #61 extraction (K=30 root windows, tf-idf cosine,
# cross-sura band 0.60-0.95): 17 pairs (vs #61's 19; verbatim band 0, consistent).
# RESULT: NULL both orders. Canonical: earlier-longer 11/17 z=+1.21 p_perm=.316; rare/hapax/TTR ~0.
# Nuzul (control-only): 9/17 z=+0.24. No measurable compact->expanded direction at this grain/N.
# Honest negative, filed in COURSE_FEASIBILITY + index P3. Underpowered (n=17) — caveat stands.
import sys, re, math, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import analysis as A
import numpy as np
from collections import Counter
rng=np.random.default_rng(0)
c=A.load_corpus(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Book6.xlsx"))
df=c.df; nl=A.normalize_letters
WA=re.compile(r"[^\W\d_]+", re.UNICODE)

# build per-sura root stream with verse refs + word counts + rev order
stream={}  # sura -> list of (root, verse_idx)
vwords={}; rev={}
for i in range(len(df)):
    r=df.iloc[i]; s=int(r[A.COL_SURAH]); a=int(r[A.COL_AYAH])
    roots=str(r[A.COL_ROOTS]).split()
    stream.setdefault(s,[]).extend((x,(s,a)) for x in roots)
    vwords[(s,a)]=len(WA.findall(nl(str(r[A.COL_DIACRITIZED]))))
    rev[s]=int(r[A.COL_REV_ORDER])
freq=Counter(x for s in stream for x,_ in stream[s])

K=30
wins=[]  # (sura, start_global, roots list, verse set)
g=0
for s in sorted(stream):
    seq=stream[s]
    for i0 in range(0,len(seq)-K+1,K):
        chunk=seq[i0:i0+K]
        wins.append(dict(sura=s, gpos=g, roots=[x for x,_ in chunk], verses={v for _,v in chunk}))
        g+=1
print("windows:",len(wins))
# tf-idf cosine
vocab={}
for w in wins:
    for x in w["roots"]: vocab.setdefault(x,len(vocab))
M=np.zeros((len(wins),len(vocab)))
for i,w in enumerate(wins):
    for x,ct in Counter(w["roots"]).items(): M[i,vocab[x]]=ct
dfreq=(M>0).sum(0); idf=np.log((len(wins)+1)/(dfreq+1))+1
M=M*idf; nrm=np.linalg.norm(M,axis=1,keepdims=True); nrm[nrm==0]=1
S=(M/nrm)@(M/nrm).T
pairs=[]
for i in range(len(wins)):
    for j in range(i+1,len(wins)):
        if wins[i]["sura"]!=wins[j]["sura"] and 0.6<=S[i,j]<0.95:
            pairs.append((i,j,S[i,j]))
print("recurrence-band pairs (0.60-0.95, cross-sura):",len(pairs))
nverb=sum(1 for i in range(len(wins)) for j in range(i+1,len(wins)) if wins[i]["sura"]!=wins[j]["sura"] and S[i,j]>=0.95)
print("verbatim-band (excluded):",nverb)

def feats(w):
    L=sum(vwords[v] for v in w["verses"])
    rare=sum(1 for x in w["roots"] if freq[x]<=5)/K
    hap=sum(1 for x in w["roots"] if freq[x]==1)/K
    ttr=len(set(w["roots"]))/K
    return L,rare,hap,ttr

def signtest(pairs,orderkey,label):
    # orderkey(i,j) -> (early_idx, late_idx) or None (tie/skip)
    names=["span-words L","rare-density","hapax-density","root-TTR"]
    used=0; wins_ct=[0,0,0,0]; diffs=[[],[],[],[]]
    for i,j,_ in pairs:
        o=orderkey(i,j)
        if o is None: continue
        e,l=o; used+=1
        fe,fl=feats(wins[e]),feats(wins[l])
        for m in range(4):
            if fe[m]>fl[m]: wins_ct[m]+=1
            diffs[m].append(fe[m]-fl[m])
    print(f"--- {label} (n={used} pairs) ---")
    for m,nm in enumerate(names):
        k=wins_ct[m]; n=used
        ties=sum(1 for d in diffs[m] if d==0); neff=n-ties
        z=(k-neff/2)/math.sqrt(neff/4) if neff>0 else float('nan')
        # rearrangement null (1000 random flips)
        null=rng.binomial(neff,0.5,1000)
        p_emp=float(np.mean(np.abs(null-neff/2)>=abs(k-neff/2)))
        print(f"  {nm:14s} earlier-greater {k}/{neff} (ties {ties})  z={z:+.2f}  p_perm={p_emp:.3f}  mean(early-late)={np.mean(diffs[m]):+.3f}")
canon=lambda i,j:(i,j) if wins[i]["gpos"]<wins[j]["gpos"] else (j,i)
def nuzul(i,j):
    ri,rj=rev[wins[i]["sura"]],rev[wins[j]["sura"]]
    if ri==rj: return None
    return (i,j) if ri<rj else (j,i)
signtest(pairs,canon,"CANONICAL muṣḥaf order")
signtest(pairs,nuzul,"NUZŪL order (Egyptian standard; control-only)")
# pair listing
print("--- pairs ---")
for i,j,cs in sorted(pairs,key=lambda t:-t[2]):
    wi,wj=wins[i],wins[j]
    print(f"  cos={cs:.3f}  {wi['sura']}:{sorted(wi['verses'])[0][1]}-{sorted(wi['verses'])[-1][1]}  <->  {wj['sura']}:{sorted(wj['verses'])[0][1]}-{sorted(wj['verses'])[-1][1]}  L={feats(wi)[0]}/{feats(wj)[0]}")
