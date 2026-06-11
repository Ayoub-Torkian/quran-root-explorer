#!/usr/bin/env python3
"""Fold the Qur'an-derived proteins and compare to shuffled controls.

Folds each short sura-protein with the ESMFold web API (the GPU work happens
remotely — no local GPU needed), then folds a SHUFFLED version of the same
protein beside it. Reports mean pLDDT (fold confidence, 0-100): real proteins
fold confidently (high pLDDT); most random/shuffled sequences do not.

HONEST TEST: does the Qur'an-protein fold better than its own shuffle? Our six
CPU scenarios predict NO (the proteins aren't specially protein-like). Folding
them confirms or refutes that on the strongest oracle. A null is the finding.

RUN ON YOUR MACHINE:  python fold_proteins.py
Dependencies: requests.   (ESMFold API limits length ~400 aa and rate-limits;
the script folds only the short suras and pauses between calls.)
"""
import os, re, time, random
import requests
random.seed(0)
HERE=os.path.dirname(__file__)
FASTA=os.path.join(HERE,"..","generated_proteins","quran_proteins_by_sura.fasta")
OUT=os.path.join(HERE,"..","generated_proteins","folds"); os.makedirs(OUT,exist_ok=True)
API="https://api.esmatlas.com/foldSequence/v1/pdb/"
MIN_AA, MAX_AA = 40, 400   # foldable size, within API limit

def read_fasta(p):
    name=None; seq=""; out=[]
    for ln in open(p):
        if ln.startswith(">"):
            if name: out.append((name,seq))
            name=ln[1:].strip().split()[0]; seq=""
        else: seq+=ln.strip()
    if name: out.append((name,seq))
    return out

def fold(seq, tries=3):
    """POST to ESMFold with SHORT timeouts so it fails fast when the (community-run,
    frequently-down) API is unavailable — instead of hanging for many minutes."""
    last=None
    for k in range(tries):
        try:
            r=requests.post(API, data=seq, timeout=45,
                            headers={"Content-Type":"text/plain","User-Agent":"foldscript/1.0"})
            if r.status_code==200 and r.text.lstrip().startswith(("HEADER","ATOM","MODEL","REMARK","PARENT")):
                return r.text
            last=f"HTTP {r.status_code}"
        except Exception as e:
            last=str(e)[:80]
        time.sleep(4*(k+1))   # 4s, 8s backoff
    raise RuntimeError(f"ESMFold API unavailable ({last})")

def mean_plddt(pdb):
    vals=[]
    for ln in pdb.splitlines():
        if ln.startswith("ATOM") and ln[12:16].strip()=="CA":
            try: vals.append(float(ln[60:66]))
            except: pass
    return sum(vals)/len(vals) if vals else float("nan")

def shuffle(s):
    l=list(s); random.shuffle(l); return "".join(l)

def main():
    prots=[(n,s) for n,s in read_fasta(FASTA) if MIN_AA<=len(s)<=MAX_AA]
    prots.sort(key=lambda x: len(x[1]))   # shortest first — most likely to get through a busy API
    print(f"Folding {len(prots)} short sura-proteins + a shuffled control each (shortest first).")
    print(f"{'sura':28}{'len':>5}{'pLDDT real':>12}{'pLDDT shuffled':>16}{'verdict':>10}")
    real_hi=ctrl_hi=0
    for name,seq in prots:
        try:
            pdb=fold(seq); pr=mean_plddt(pdb)
            open(os.path.join(OUT,name+".pdb"),"w").write(pdb)   # save structure (view in PyMOL/Mol*)
            time.sleep(1.0)
            ps=mean_plddt(fold(shuffle(seq))); time.sleep(1.0)
        except Exception as e:
            print(f"{name:28}{len(seq):>5}   error: {e}"); continue
        v="real>shuf" if pr>ps else "shuf>=real"
        real_hi+=pr>ps; ctrl_hi+=ps>=pr
        print(f"{name:28}{len(seq):>5}{pr:>12.1f}{ps:>16.1f}{v:>10}")
    print(f"\nReal folded better in {real_hi}/{real_hi+ctrl_hi}. For a genuine signal, the "
          "Qur'an-proteins should fold clearly and consistently above their shuffles AND "
          "above other languages' proteins (run those too). Otherwise: honest null.")
    print("Note pLDDT > ~70 = confident fold; random sequences usually score low.")

if __name__=="__main__":
    main()
