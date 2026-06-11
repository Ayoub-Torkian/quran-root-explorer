#!/usr/bin/env python3
"""Scenario harness (CPU). Monitors PROGRESS / Δ of the Qur'an over the control battery
under an MC mapping search, against a real-protein objective. Folding (GPU) is deferred
until CPU progress reaches the gate (default 70%).

v0.2 objective = dipeptide-distance to real protein (KL to a large CCDS-derived reference).
NOTE: this objective punishes all natural-language order and may NOT track foldability —
see MONITOR.md; swapping the objective is a first-class re-steer.

Prereqs: data/genome/ccds_cds.fasta, data/quran/quran_arabic_concat.txt, a control text.
Usage: python scenario_harness.py [control_text.txt] [M]
"""
import os, re, sys, unicodedata, random
import numpy as np
random.seed(1); np.random.seed(1)
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,"..")
AA=20; CAP=150000; GATE=70.0
B="TCAG"; AAS="FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON={a+b+c:AAS[i] for i,(a,b,c) in enumerate((x,y,z) for x in B for y in B for z in B)}
AA20="ACDEFGHIKLMNPQRSTVWY"; A2I={a:i for i,a in enumerate(AA20)}
def translate(d):
    o=[]
    for k in range(0,len(d)-2,3):
        a=CODON.get(d[k:k+3],'X')
        if a=='*': continue
        if a in A2I: o.append(A2I[a])
    return o
def dip(p):
    c=np.bincount(p[:-1]*AA+p[1:],minlength=AA*AA).astype(float)+1.0; return c/c.sum()

def build_reference(maxrefseq=4800):
    ref=[]; test=[]; cur=''; n=0
    for line in open(os.path.join(ROOT,"data","genome","ccds_cds.fasta")):
        if line.startswith('>'):
            if cur:
                n+=1; (ref if n%6 else test).append(translate(re.sub('[^ACGT]','',cur))); cur=''
            if len(ref)>maxrefseq and len(test)>800: break
        else: cur+=line.strip().upper()
    R=np.array([a for s in ref for a in s]); T=np.array([a for s in test for a in s])
    return dip(R), T

def quran():
    t=open(os.path.join(ROOT,"data","quran","quran_arabic_concat.txt"),encoding="utf-8").read()
    t=unicodedata.normalize("NFD",t); t="".join(c for c in t if not unicodedata.combining(c))
    return "".join(c for c in t if "ء"<=c<="ي" and c!="ـ")[:CAP]
def lang(p):
    t=open(p,encoding="utf-8",errors="ignore").read().lower()
    t=unicodedata.normalize("NFD",t); t="".join(c for c in t if not unicodedata.combining(c))
    return "".join(c for c in t if c.isalpha())[:CAP]
def codes(s):
    al=sorted(set(s)); idx={c:i for i,c in enumerate(al)}; return np.array([idx[c] for c in s]),len(al)
def shuf(s): l=list(s); random.shuffle(l); return ''.join(l)

def search(seq, REF, M):
    cd,Asz=codes(seq); n=len(cd); tr,te=cd[:int(.7*n)],cd[int(.7*n):]
    def kl(p):
        if len(p)<50: return np.inf
        c=dip(p); return float(np.sum(c*np.log2(c/REF)))
    bk=np.inf; bm=None
    for _ in range(M):
        mp=np.random.randint(0,AA,size=Asz); k=kl(mp[tr])
        if k<bk: bk=k; bm=mp
    return kl(bm[te])

def main():
    ctrl_txt=sys.argv[1] if len(sys.argv)>1 else os.path.join(ROOT,"data","languages","english_moby_dick.txt")
    M=int(sys.argv[2]) if len(sys.argv)>2 else 300
    REF,T=build_reference()
    def kl(p): c=dip(p); return float(np.sum(c*np.log2(c/REF)))
    FLOOR=kl(T)
    qur=quran(); corp={"Quran":qur,"Quran_shuffled":shuf(qur),"control_lang":lang(ctrl_txt)}
    hk={n:search(s,REF,M) for n,s in corp.items()}
    base=min(hk["Quran_shuffled"],hk["control_lang"])
    prog=100*(base-hk["Quran"])/(base-FLOOR)
    print(f"FLOOR(real protein)={FLOOR:.4f}  M={M}")
    for n,v in hk.items(): print(f"  {n:16}{v:.4f}")
    print(f"Delta(control-Quran)={base-hk['Quran']:+.4f}  PROGRESS={prog:.1f}%  (GPU gate at {GATE}%)")
    return prog

if __name__=="__main__": main()
