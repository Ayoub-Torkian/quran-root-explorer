#!/usr/bin/env python3
"""POSITIVE CONTROL (referee M1+M2): does the framework return a POSITIVE when a true
char->AA mapping exists by construction?

Construction: take a real CCDS protein P (codes 0..19), pick a random bijection sigma
(AA->symbol), and write the PLANTED TEXT as T = sigma(P). By construction a true latent
map m* = sigma^{-1} exists: m*(T) == P, whose dipeptide distribution matches the real
genome (KL ~ 0). We then run the SAME simulated-annealing optimizer + the SAME convergence
machinery used in the main experiment on (a) the planted text and (b) the real Qur'an, under
identical settings. A valid instrument must:
  - recover the planted map (agreement to ground truth -> ~1),
  - show cross-portion CONVERGENCE >> chance on the planted text,
  - clear the FLOOR (shuffled planted text loses it),
  while the Qur'an stays at chance (the established null).

This simultaneously answers M1 (can it ever say yes?) and M2 (is the Qur'an null a
search-power artifact? No -- same optimizer recovers a real map when one exists).

CPU only. Qur'an files are READ-ONLY; the planted text is synthetic; controls are shuffles.
"""
import os, json, time, unicodedata, random
import numpy as np
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,"..")
B="TCAG"; AAS="FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
A2I={a:i for i,a in enumerate("ACDEFGHIKLMNPQRSTVWY")}
COD={(a+b+c):AAS[i] for i,(a,b,c) in enumerate((x,y,z) for x in B for y in B for z in B)}

def translate_ccds(maxaa=400000):
    R=[]; cur=''
    for line in open(os.path.join(ROOT,"data","genome","ccds_cds.fasta")):
        if line.startswith('>'):
            if cur:
                d=''.join(ch for ch in cur.upper() if ch in 'ACGT')
                for k in range(0,len(d)-2,3):
                    a=COD.get(d[k:k+3],'X')
                    if a in A2I: R.append(A2I[a])
                cur=''
            if len(R)>maxaa: break
        else: cur+=line.strip()
    return np.array(R[:maxaa])

LP=None   # trigram log-prob table over 20 AAs (length 8000), built from CCDS
def build_trigram(P):
    idx=P[:-2]*400+P[1:-1]*20+P[2:]
    c=np.bincount(idx,minlength=8000).astype(float)+0.5
    return np.log(c/c.sum())

def score(codes):
    """Higher = better. Mean trigram log-prob of the decoded sequence vs the genome model.
    This is the standard substitution-cipher objective; bigram/KL was too weak (M2)."""
    if len(codes)<80: return -1e9
    idx=codes[:-2]*400+codes[1:-1]*20+codes[2:]
    return float(LP[idx].mean())

def sa(textcodes, nL, seed, iters=8000, T0=1.0, restarts=2):
    """Single-position reassignment SA, identical for planted & Qur'an. Keeps best over restarts."""
    rng=np.random.default_rng(seed); gbest=-1e9; gm=None
    for r in range(restarts):
        m=rng.integers(0,20,size=nL); cur=score(m[textcodes]); best=cur; bestm=m.copy()
        for t in range(iters):
            T=T0*(1-t/iters)+1e-3
            i=int(rng.integers(nL)); old=m[i]; nv=int(rng.integers(20))
            if nv==old: continue
            m[i]=nv; e=score(m[textcodes])
            if e>cur or rng.random()<np.exp((e-cur)/max(T,1e-6)):
                cur=e
                if e>best: best=e; bestm=m.copy()
            else: m[i]=old
        if best>gbest: gbest=best; gm=bestm
    return gbest,gm

def quran_codes():
    t=open(os.path.join(ROOT,"data","quran","quran_arabic_concat.txt"),encoding="utf-8").read()
    t=unicodedata.normalize("NFD",t); t="".join(c for c in t if not unicodedata.combining(c))
    s="".join(c for c in t if "ء"<=c<="ي" and c!="ـ")
    alpha=sorted(set(s)); idx={c:i for i,c in enumerate(alpha)}
    return np.array([idx[c] for c in s]), len(alpha)

def agree(a,b): return float(np.mean(a==b))

def chance_level(nL, iters=200, seed=999):
    rng=np.random.default_rng(seed)
    return float(np.mean([agree(rng.integers(0,20,nL),rng.integers(0,20,nL)) for _ in range(iters)]))

def convergence(textcodes, nL, pairs, iters, base=0):
    """cross-portion: split into 2 halves, SA each independently, measure map agreement."""
    n=len(textcodes); res=[]
    for p in range(pairs):
        # disjoint windows for each pair
        w=n//(pairs+1); a=textcodes[p*w:(p+1)*w]; b=textcodes[(p+1)*w:(p+2)*w]
        _,mA=sa(a,nL,seed=base+2*p,iters=iters); _,mB=sa(b,nL,seed=base+2*p+1,iters=iters)
        res.append(agree(mA,mB))
    return np.array(res)

def main():
    global LP
    print("translating CCDS ..."); P=translate_ccds(maxaa=300000)
    LP=build_trigram(P)
    ITERS=8000; PAIRS=5
    rng=np.random.default_rng(0)

    # ---- PLANTED TEXT: a true char->AA map exists by construction ----
    Pchunk=P[:15000]
    sigma=rng.permutation(20)               # AA -> symbol bijection (alphabet size 20)
    T=sigma[Pchunk]                         # planted text (symbol codes)
    inv=np.argsort(sigma)                   # ground-truth map symbol->AA
    nLp=20
    _,mhat=sa(T,nLp,seed=5,iters=ITERS)
    gt_recovery=agree(mhat,inv)
    conv_planted=convergence(T,nLp,PAIRS,ITERS,base=100)
    # floor: shuffle planted text (destroys order -> destroys the latent dipeptide structure)
    Tsh=T.copy(); rng.shuffle(Tsh)
    conv_planted_shuf=convergence(Tsh,nLp,PAIRS,ITERS,base=200)
    chance_p=chance_level(nLp)

    # ---- QURAN: the established null, SAME optimizer/settings ----
    Q,nLq=quran_codes()
    conv_quran=convergence(Q[:15000],nLq,PAIRS,ITERS,base=300)
    chance_q=chance_level(nLq)

    out={
      "ts":time.strftime("%Y-%m-%d %H:%M"),"objective":"dipeptide-KL","optimizer":"SA",
      "iters":ITERS,"pairs":PAIRS,
      "planted":{
        "ground_truth_recovery":round(gt_recovery,3),
        "cross_portion_mean":round(float(conv_planted.mean()),3),
        "cross_portion_sd":round(float(conv_planted.std()),3),
        "shuffled_floor_mean":round(float(conv_planted_shuf.mean()),3),
        "chance":round(chance_p,3)},
      "quran":{
        "cross_portion_mean":round(float(conv_quran.mean()),3),
        "cross_portion_sd":round(float(conv_quran.std()),3),
        "chance":round(chance_q,3)}
    }
    print(json.dumps(out,indent=2))
    json.dump(out,open(os.path.join(HERE,"positive_control_result.json"),"w"),indent=2)
    print("\nREAD: planted recovery/cross_portion >> chance AND >> shuffled floor => the "
          "instrument FIRES when a true map exists. Quran stays at chance under the SAME "
          "optimizer => its null is about the data, not a weak search.")

if __name__=="__main__": main()
