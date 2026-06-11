#!/usr/bin/env python3
"""STAGE C — reading-frame + ORF detection (the 'expression' checkpoint of PIPELINE.md).

Given char-derived DNA, scan all 6 reading frames for open reading frames
(ATG ... in-frame stop) and gate on ORF length / coverage. Real coding sequence
passes (the whole gene is one ORF, coverage ~1.0); shuffled/random DNA makes only
short ORFs by chance. Importable as a pipeline component; self-validating as a script.

Key discriminators (calibrated on real CDS vs shuffled/random, 2026-06-08):
  coverage    real ~1.00   vs  shuffled/random ~0.27
  longest ORF real ~328 aa vs  shuffled/random ~66-79 aa
A bare 50-aa gate is too lenient (random can throw a 50-126 aa ORF); use COVERAGE
and/or a length gate set at the null's upper tail.
"""
import os, re, random
from collections import Counter
import numpy as np
HERE = os.path.dirname(__file__)

COMP = {'A':'T','T':'A','C':'G','G':'C'}
STOPS = {'TAA','TAG','TGA'}
def revcomp(s): return ''.join(COMP.get(c,'N') for c in reversed(s))

def orfs_in_frame(seq, frame):
    res=[]; start=None; i=frame; n=len(seq)
    while i+3 <= n:
        c=seq[i:i+3]
        if start is None:
            if c=='ATG': start=i
        elif c in STOPS:
            res.append((i-start)//3); start=None
        i+=3
    return res

def all_orfs(dna):
    dna=re.sub('[^ACGT]','',dna.upper()); out=[]
    for s in (dna, revcomp(dna)):
        for f in (0,1,2): out+=orfs_in_frame(s,f)
    return out

def longest_orf(dna):
    o=all_orfs(dna); return max(o) if o else 0
def coverage(dna):
    dna=re.sub('[^ACGT]','',dna.upper())
    return (longest_orf(dna)*3)/len(dna) if dna else 0.0
def gate(dna, min_aa=100, min_cov=0.0):
    """Stage-C gate: pass if longest ORF >= min_aa (and coverage >= min_cov)."""
    return longest_orf(dna) >= min_aa and coverage(dna) >= min_cov

# ---------- self-validation ----------
def _load_cds(path):
    seqs=[]; cur=''
    for l in open(path):
        if l.startswith('>'):
            if cur: seqs.append(cur); cur=''
        else: cur+=l.strip().upper()
    if cur: seqs.append(cur)
    return [re.sub('[^ACGT]','',s) for s in seqs]
def _shuf(s): l=list(s); random.shuffle(l); return ''.join(l)
def _rand_comp(s):
    c=Counter(s); a=list(c); p=np.array([c[x] for x in a],float); p/=p.sum()
    return ''.join(np.random.choice(a,size=len(s),p=p))

if __name__=="__main__":
    random.seed(5); np.random.seed(5)
    base=os.path.join(HERE,"..","data","examples")
    cds=[]
    for f in os.listdir(base):
        if f.endswith(".fasta"): cds+=_load_cds(os.path.join(base,f))
    GATE=50
    def summarize(name, seqs):
        lo=[longest_orf(s) for s in seqs]; cov=[coverage(s) for s in seqs]
        print(f"{name:16} n={len(seqs):2d}  longestORF mean={sum(lo)/len(lo):6.1f} max={max(lo):4d}"
              f"  coverage mean={sum(cov)/len(cov):.2f}  pass(>={GATE}aa)={sum(x>=GATE for x in lo)}/{len(seqs)}")
    print(f"STAGE C ORF gate — real human CDS (n={len(cds)}) vs controls:")
    summarize("real CDS", cds)
    summarize("shuffled CDS", [_shuf(s) for s in cds])
    summarize("random matched", [_rand_comp(s) for s in cds])
    print("Coverage is the clean discriminator (real ~1.0 vs ~0.27). Calibrate the length")
    print("gate on the random/shuffled upper tail before judging any text-derived sequence.")
