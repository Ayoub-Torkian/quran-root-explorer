#!/usr/bin/env python3
"""Alphabet-size control for the MI-γ structural contrast (addresses referee M4).

MI-γ compares a 4-symbol genome with ~28-symbol scripts; a skeptic asks whether the smaller
alphabet alone explains the genome's lower γ (= longer-range memory). We recompute γ at MATCHED
alphabet sizes, reusing the relabeling-agnostic kernel in route_b_confirm.py:
  - genome recoded to 64 CODON symbols,
  - a language recoded DOWN to 4 symbols.
If the genome stays well below language at a matched alphabet, the effect is real structure.

Result (2026-06-09): genome nt(4)=0.888, genome codons(64)=0.273; English letters=2.254,
English-4sym=1.752. Gap persists at matched 4 symbols (Δ≈0.86); enlarging the genome alphabet
pushes γ DOWN — opposite of an alphabet-size artifact. M4 refuted.
"""
import os, re, sys, glob, unicodedata
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.join(HERE,"..")
sys.path.insert(0,HERE)
import route_b_confirm as K   # kernel: codes/mi/mi_decay/chunk_stats (relabeling-agnostic)

def load_nt(p,cap=900000):
    s=''.join(l.strip() for l in open(p) if not l.startswith('>'))
    return re.sub('[^ACGT]','',s.upper())[:cap]
def codon_string(nt):
    out=[]
    for i in range(0,len(nt)-2,3):
        c=nt[i:i+3]
        out.append(chr(0x4E00+("ACGT".index(c[0])*16+"ACGT".index(c[1])*4+"ACGT".index(c[2]))))
    return ''.join(out)
def lang_letters(p,cap=900000):
    t=open(p,encoding='utf-8',errors='ignore').read().lower()
    t=unicodedata.normalize('NFD',t); t=''.join(ch for ch in t if not unicodedata.combining(ch))
    return ''.join(ch for ch in t if unicodedata.category(ch).startswith('L'))[:cap]
def to4(s):
    a=sorted(set(s)); grp={c:str(i%4) for i,c in enumerate(a)}
    return ''.join(grp[c] for c in s)
def gamma(s,L=2000):
    st,_=K.chunk_stats(s,L); return st['MI_gamma'][:2]

def main():
    nt=load_nt(os.path.join(ROOT,"data","genome","ccds_cds.fasta"))
    print("genome nt   (4 sym): γ=%.3f ± %.3f"%gamma(nt))
    print("genome codon(64sym): γ=%.3f ± %.3f"%gamma(codon_string(nt)))
    for f in sorted(glob.glob(os.path.join(ROOT,"data","languages","*.txt"))):
        s=lang_letters(f); a=gamma(s); b=gamma(to4(s))
        print("%-26s letters γ=%.3f±%.3f | 4-sym γ=%.3f±%.3f"%(os.path.basename(f),a[0],a[1],b[0],b[1]))

if __name__=="__main__": main()
