#!/usr/bin/env python3
"""R1 — ROOT-level mapping test (the salvaged 3-char idea), with a planted-ROOT positive control.

Needs roots_seq.txt (produced by extract_roots.py; run that locally first).

Two parts, both using the validated convergence instrument (bijection/assignment swap-SA +
trigram log-lik; see positive_control_cipher.py):

  (A) PLANTED-ROOT POSITIVE CONTROL — encrypt the (language-structured) root sequence with a
      random bijection over the top-K roots, score vs the root text's OWN trigram model, crack,
      and check recovery + cross-portion convergence. Validates the instrument AT ROOT granularity.

  (B) REAL TEST root->codon vs the genome — search root->codon maps maximizing trigram log-lik of
      the decoded AA sequence vs the REAL CCDS amino-acid trigram model; report FLOOR (shuffled
      roots), CONVERGENCE (cross-portion), and REPLICATION (several disjoint pairs).

Prediction from C1 (flat genome target, a target-side property): (A) fires, (B) is null — root
granularity cannot make the genome less flat. Run records whichever the data says.
"""
import os, json, time
import numpy as np
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,"..")
RSEQ=os.path.join(ROOT,"roots_seq.txt")
B="TCAG"; AAS="FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
A2I={a:i for i,a in enumerate("ACDEFGHIKLMNPQRSTVWY")}

def load_roots():
    if not os.path.exists(RSEQ):
        raise SystemExit("roots_seq.txt missing — run scripts/extract_roots.py locally first.")
    toks=open(RSEQ,encoding="utf-8").read().split()
    uniq=sorted(set(toks)); idx={r:i for i,r in enumerate(uniq)}
    return np.array([idx[t] for t in toks]), len(uniq)

# ---------- generic trigram instrument ----------
def trimodel(x,K):
    i=x[:-2]*K*K+x[1:-1]*K+x[2:]; c=np.bincount(i,minlength=K**3).astype(float)+0.2
    return np.log(c/c.sum())
def trilik_K(x,K,LP):
    if len(x)<80: return -1e9
    i=x[:-2]*K*K+x[1:-1]*K+x[2:]; return float(LP[i].mean())

# ===== (A) planted-root positive control (bijection cipher over top-K roots) =====
def positive_control(R, topK=30, iters=40000, restarts=3):
    from collections import Counter
    common=[r for r,_ in Counter(R.tolist()).most_common(topK)]
    keep=np.array([r for r in R if r in set(common)])
    remap={r:i for i,r in enumerate(common)}; S=np.array([remap[r] for r in keep]); K=topK
    LP=trimodel(S,K); rng=np.random.default_rng(0)
    pi=rng.permutation(K); C=pi[S]; truth=np.argsort(pi)
    def crack(seg,seed):
        g=np.random.default_rng(seed).permutation(K); rr=np.random.default_rng(seed+1)
        cur=trilik_K(g[seg],K,LP); best=cur; bm=g.copy()
        for t in range(iters):
            T=0.4*(1-t/iters)+1e-3; i,j=int(rr.integers(K)),int(rr.integers(K))
            if i==j: continue
            g[i],g[j]=g[j],g[i]; e=trilik_K(g[seg],K,LP)
            if e>cur or rr.random()<np.exp((e-cur)/max(T,1e-6)):
                cur=e
                if e>best: best=e; bm=g.copy()
            else: g[i],g[j]=g[j],g[i]
        return bm
    n=len(C); h=min(8000,n//2)
    rec=float(np.mean(crack(C[:h],5)==truth))
    conv=float(np.mean(crack(C[:h],11)==crack(C[h:2*h],12)))
    return {"topK":K,"recovery":round(rec,3),"cross_portion":round(conv,3),"chance":round(1/K,3)}

# ===== (B) real root->codon vs genome =====
def genome_aa_trimodel(maxaa=300000):
    COD={(a+b+c):AAS[i] for i,(a,b,c) in enumerate((x,y,z) for x in B for y in B for z in B)}
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
    P=np.array(R[:maxaa]); return trimodel(P,20)

def real_test(R, V, LPg, pairs=5, iters=8000):
    """map g: root_id(0..V-1) -> codon(0..60 sense) -> AA(0..19); score decoded-AA trigram vs genome."""
    sense=[i for i in range(64) if AAS[i]!='*']; sense=np.array(sense)
    cod2aa=np.array([A2I.get(AAS[c],-1) for c in range(64)])
    def decode_aa(g_codon, seg):
        aa=cod2aa[g_codon[seg]]; return aa[aa>=0]
    def sa(seg,seed):
        rng=np.random.default_rng(seed); g=sense[rng.integers(0,len(sense),size=V)]
        cur=trilik_K(decode_aa(g,seg),20,LPg); best=cur; bm=g.copy()
        for t in range(iters):
            T=0.5*(1-t/iters)+1e-3; i=int(rng.integers(V)); old=g[i]
            g[i]=sense[int(rng.integers(len(sense)))]; e=trilik_K(decode_aa(g,seg),20,LPg)
            if e>cur or rng.random()<np.exp((e-cur)/max(T,1e-6)):
                cur=e
                if e>best: best=e; bm=g.copy()
            else: g[i]=old
        return best,bm
    ag=lambda a,b: float(np.mean(a==b))
    n=len(R); w=n//(pairs+1); conv=[]; floor=[]
    rng=np.random.default_rng(7); Rsh=R.copy(); rng.shuffle(Rsh)
    for p in range(pairs):
        a=R[p*w:(p+1)*w]; b=R[(p+1)*w:(p+2)*w]
        _,mA=sa(a,100+2*p); _,mB=sa(b,100+2*p+1); conv.append(ag(mA,mB))
        a2=Rsh[p*w:(p+1)*w]; b2=Rsh[(p+1)*w:(p+2)*w]
        _,sA=sa(a2,200+2*p); _,sB=sa(b2,200+2*p+1); floor.append(ag(sA,sB))
    chance=float(np.mean([ag(np.random.default_rng(900+i).integers(0,61,V),
                             np.random.default_rng(950+i).integers(0,61,V)) for i in range(30)]))
    conv=np.array(conv); floor=np.array(floor)
    return {"pairs":pairs,"real_cross_portion_mean":round(float(conv.mean()),3),
            "real_cross_portion_sd":round(float(conv.std()),3),
            "shuffled_floor_mean":round(float(floor.mean()),3),
            "chance":round(chance,3)}

def main():
    R,V=load_roots(); print(f"roots: {len(R)} tokens, {V} distinct")
    t=time.time()
    pc=positive_control(R)
    LPg=genome_aa_trimodel()
    rt=real_test(R,V,LPg)
    out={"ts":time.strftime("%Y-%m-%d %H:%M"),"root_tokens":int(len(R)),"distinct_roots":int(V),
         "A_planted_root_positive_control":pc,"B_real_root_to_codon_vs_genome":rt,
         "sec":round(time.time()-t,1)}
    print(json.dumps(out,indent=2))
    json.dump(out,open(os.path.join(HERE,"root_map_result.json"),"w"),indent=2)
    print("\nREAD: (A) recovery & cross_portion >> chance => instrument fires at ROOT granularity. "
          "(B) real_cross_portion ~ shuffled_floor ~ chance => null (flat genome target, C1).")

if __name__=="__main__": main()
