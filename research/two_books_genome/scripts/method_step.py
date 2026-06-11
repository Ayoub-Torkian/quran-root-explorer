#!/usr/bin/env python3
"""METHOD HARNESS — run ONE step/scenario of the mapping program and log it.

Ties together everything we have (Qur'an corpus + real CCDS genome + scoring + the
floor & convergence checks) into one runnable model. Each run = one step: it searches
for the best char->AA (or char->codon) mapping under the objective, measures it against
the FLOOR (random/shuffled) and its IDENTIFIABILITY (self-consistency, cross-portion),
and appends a row to scripts/ledger.json. Climb Delta-over-floor, not raw similarity.

Objective is pluggable: default = proxy (-dipeptide-KL to real protein, CPU).
Swap in real BLAST/tblastx at the marked hook for fidelity to the paper.

Usage examples:
  python method_step.py --text full   --gran aa --M 2000 --label "M2000 proxy"
  python method_step.py --text half1  --gran aa --M 5000 --label "half1 M5000"
  python method_step.py --text sura:112 --gran codon --M 3000 --label "ikhlas codon"
"""
import os, re, json, time, argparse, unicodedata
import numpy as np
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,"..")
LEDGER=os.path.join(HERE,"ledger.json")
B="TCAG"; AAS="FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
A2I={a:i for i,a in enumerate("ACDEFGHIKLMNPQRSTVWY")}
COD={(a+b+c):AAS[i] for i,(a,b,c) in enumerate((x,y,z) for x in B for y in B for z in B)}

def _trd(d):
    o=[]
    for k in range(0,len(d)-2,3):
        a=COD.get(d[k:k+3],'X')
        if a in A2I:o.append(A2I[a])
    return o
def ref_dipeptide(maxaa=1500000):
    R=[];cur=''
    for line in open(os.path.join(ROOT,"data","genome","ccds_cds.fasta")):
        if line.startswith('>'):
            if cur:R+=_trd(re.sub('[^ACGT]','',cur));cur=''
            if len(R)>maxaa:break
        else:cur+=line.strip().upper()
    R=np.array(R); c=np.bincount(R[:-1]*20+R[1:],minlength=400).astype(float)+1.0
    return c/c.sum()
def quran():
    t=open(os.path.join(ROOT,"data","quran","quran_arabic_concat.txt"),encoding="utf-8").read()
    t=unicodedata.normalize("NFD",t);t="".join(c for c in t if not unicodedata.combining(c))
    return "".join(c for c in t if "ء"<=c<="ي" and c!="ـ")
def sura_text(n):
    out=""
    for line in open(os.path.join(ROOT,"data","quran","quran_arabic_verses.tsv"),encoding="utf-8"):
        if "\t" in line and line.split(":")[0]==str(n):
            a=unicodedata.normalize("NFD",line.split("\t",1)[1]); a="".join(c for c in a if not unicodedata.combining(c))
            out+="".join(c for c in a if "ء"<=c<="ي" and c!="ـ")
    return out

REF=None
def similarity_floorunits(seq_codes):
    """OBJECTIVE HOOK. Returns a 'distance' (lower = more similar to real protein).
    Default proxy = dipeptide-KL. >>> Replace this body with a BLAST/tblastx call <<<
    (map codes->amino acids/codons, write FASTA, run blast vs RefSeq, return -bitscore)."""
    if len(seq_codes)<80: return 1e9
    c=np.bincount(seq_codes[:-1]*20+seq_codes[1:],minlength=400).astype(float)+1.0; c/=c.sum()
    return float(np.sum(c*np.log2(c/REF)))

def search(cd, nL, M, rng, gran):
    bk=1e9; bm=None
    for _ in range(M):
        if gran=="aa":
            m=rng.integers(0,20,size=nL); prot=m[cd]
        else:  # codon: letter->codon(0..63)->AA; sense only via map to 0..60 then translate
            mc=rng.integers(0,64,size=nL); aa=np.array([A2I.get(AAS[i],-1) for i in range(64)])[mc[cd]]
            prot=aa[aa>=0]
        k=similarity_floorunits(prot)
        if k<bk:bk=k;bm=(m if gran=="aa" else mc)
    return bk,bm

def run(text, gran, M, label):
    global REF; REF=ref_dipeptide()
    q=quran()
    if text=="full": s=q
    elif text=="half1": s=q[:len(q)//2]
    elif text=="half2": s=q[len(q)//2:]
    elif text.startswith("sura:"): s=sura_text(int(text.split(":")[1]))
    else: s=q
    ALPHA=sorted(set(q)); IDX={c:i for i,c in enumerate(ALPHA)}; nL=len(ALPHA)
    codes=lambda x: np.array([IDX[c] for c in x if c in IDX])
    rng=np.random.default_rng
    cd=codes(s)
    real,_=search(cd,nL,M,rng(10),gran)
    import random as _r; sh=list(s); _r.seed(1); _r.shuffle(sh); fl_sh,_=search(codes("".join(sh)),nL,M,rng(11),gran)
    rndstr="".join(rng(7).choice(ALPHA,size=len(s))); fl_rn,_=search(codes(rndstr),nL,M,rng(12),gran)
    floor=min(fl_sh,fl_rn); delta=round(floor-real,4)
    # identifiability (independent seeds)
    _,mA1=search(cd,nL,M,rng(1),gran); _,mA2=search(cd,nL,M,rng(2),gran)
    other=codes(q[len(q)//2:] if text!="half2" else q[:len(q)//2]); _,mB=search(other,nL,M,rng(3),gran)
    ag=lambda a,b: float(np.mean(a==b))
    chance=float(np.mean([ag(rng(40+i).integers(0,20 if gran=="aa" else 64,nL),
                             rng(140+i).integers(0,20 if gran=="aa" else 64,nL)) for i in range(30)]))
    row={"ts":time.strftime("%Y-%m-%d %H:%M"),"label":label,"text":text,"gran":gran,"M":M,
         "real":round(real,4),"floor":round(floor,4),"delta_over_floor":delta,
         "self_consistency":round(ag(mA1,mA2),3),"cross_portion":round(ag(mA1,mB),3),"chance":round(chance,3)}
    led=json.load(open(LEDGER)) if os.path.exists(LEDGER) else []
    led.append(row); json.dump(led,open(LEDGER,"w"),indent=2)
    print(json.dumps(row,indent=2))
    print(f"\nRead: Delta>0 means real beats floor (real signal). self_consistency -> ~1 and "
          f"cross_portion >> chance means a mapping is converging. Logged to {LEDGER}.")

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--text",default="full"); ap.add_argument("--gran",default="aa",choices=["aa","codon"])
    ap.add_argument("--M",type=int,default=2000); ap.add_argument("--label",default="")
    a=ap.parse_args(); run(a.text,a.gran,a.M,a.label or f"{a.text}-{a.gran}-M{a.M}")
