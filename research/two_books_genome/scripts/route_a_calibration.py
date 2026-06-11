#!/usr/bin/env python3
"""Route-A benchmark calibration on known-answer REAL samples from BOTH ends.

  ACT end  = real proteins (translate real human CDS via the standard genetic code)
  WORD end = real text mapped to peptides (arbitrary char->AA, as a baseline)

Purpose: confirm the cheap CPU proxies separate real-protein ORDER from random/shuffled
BEFORE running any mapping search, and show where naive text-derived peptides land.
The PRIMARY oracle (foldability / ESMFold) is GPU and is NOT run here — this validates
the cheap stage-1 proxies and the pipeline mechanics on actual data.

Usage:  python route_a_calibration.py [text_file]
Reads data/examples/*.fasta for the ACT end; text_file (any language) for the WORD end.
"""
import os, re, math, random, sys
from collections import Counter
import numpy as np
random.seed(3); np.random.seed(3)
HERE = os.path.dirname(__file__)

B="TCAG"; AAS="FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON={a+b+c:AAS[i] for i,(a,b,c) in enumerate((x,y,z) for x in B for y in B for z in B)}
def translate(dna):
    p=[]
    for k in range(0,len(dna)-2,3):
        aa=CODON.get(dna[k:k+3],'X')
        if aa=='*': break
        p.append(aa)
    return ''.join(p)
def load_cds(path):
    seqs=[]; cur=''
    for l in open(path):
        if l.startswith('>'):
            if cur: seqs.append(cur); cur=''
        else: cur+=l.strip().upper()
    if cur: seqs.append(cur)
    return [re.sub('[^ACGT]','',s) for s in seqs]

AA20="ACDEFGHIKLMNPQRSTVWY"
def comp_kl_uniform(s):
    c=Counter(s); n=len(s)
    return sum((c.get(a,0)/n)*math.log2((c.get(a,0)/n)/(1/20)) for a in AA20 if c.get(a,0))
def adj_mi(s):
    idx={a:i for i,a in enumerate(AA20)}; x=np.array([idx[a] for a in s if a in idx])
    if len(x)<50: return float('nan')
    J=np.zeros((20,20)); np.add.at(J,(x[:-1],x[1:]),1.0); J/=J.sum()
    px=J.sum(1); py=J.sum(0); nz=J>0
    mi=float(np.sum(J[nz]*np.log2(J[nz]/np.outer(px,py)[nz])))
    return mi-(19*19)/(2*len(x)*math.log(2))
def dipep(s):
    idx={a:i for i,a in enumerate(AA20)}; x=[idx[a] for a in s if a in idx]
    J=np.zeros((20,20))
    for a,b in zip(x[:-1],x[1:]): J[a,b]+=1
    J+=1e-6; return J/J.sum()
def kl_to(ref,s):
    P=dipep(s); return float(np.sum(P*np.log2(P/ref)))
def shuf(s): l=list(s); random.shuffle(l); return ''.join(l)
def rand_uniform(n): return ''.join(random.choice(AA20) for _ in range(n))
def rand_comp(s):
    c=Counter(s); a=list(c); p=np.array([c[x] for x in a],float); p/=p.sum()
    return ''.join(np.random.choice(a,size=len(s),p=p))

def main():
    exdir=os.path.join(HERE,"..","data","examples")
    cds=[]
    for f in os.listdir(exdir):
        if f.endswith(".fasta"): cds+=load_cds(os.path.join(exdir,f))
    real=''.join(translate(d) for d in cds)
    REF=dipep(real)
    txtfile=sys.argv[1] if len(sys.argv)>1 else None
    rows=[("ACT real protein",real),("ACT shuffled",shuf(real)),
          ("ACT random uniform",rand_uniform(len(real))),("ACT random comp",rand_comp(real))]
    if txtfile and os.path.exists(txtfile):
        eng=re.sub('[^a-z]','',open(txtfile,encoding='utf-8',errors='ignore').read().lower())[:len(real)]
        letters=sorted(set(eng)); cmap={c:AA20[i%20] for i,c in enumerate(letters)}
        wp=''.join(cmap[c] for c in eng)
        rows+=[("WORD text->peptide",wp),("WORD shuffled",shuf(wp))]
    print(f"{'sample':22}{'len':>7}{'compKL_unif':>12}{'adjMI_bits':>11}{'dipepKL_to_real':>16}")
    for name,s in rows:
        print(f"{name:22}{len(s):7d}{comp_kl_uniform(s):12.3f}{adj_mi(s):11.4f}{kl_to(REF,s):16.3f}")
    print("\nReal protein: non-uniform comp + protein-specific dipeptide bias (dipepKL~0).")
    print("Shuffle keeps comp, loses order (dipepKL rises). Text->peptide has its OWN order")
    print("but UNLIKE protein (dipepKL highest). Cheap proxies discriminate; ESMFold (GPU) is")
    print("the primary oracle. This is calibration, NOT the search verdict.")

if __name__=="__main__": main()
