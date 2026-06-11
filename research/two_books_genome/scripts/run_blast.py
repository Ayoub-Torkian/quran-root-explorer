#!/usr/bin/env python3
"""REAL-BLAST run (faithful to the paper) with the control floor built in.

For each Qur'an unit: generate N frequency-sampled char->codon mappings (Monte-Carlo),
write the mapped DNA as FASTA, BLAST it (tblastx) against a LOCAL CCDS database, and take
the best bit-score / e-value per mapping. Do the IDENTICAL thing for a COMPOSITION CONTROL
(random sequences matched to the Qur'an's letter frequencies). The result is meaningful only
as: best-score(real) vs best-score(control). If real >> control, signal; if real ~ control, null.

Prereqs (see RUN_BLAST.md): install BLAST+, build the DB once:
    makeblastdb -in data/genome/ccds_cds.fasta -dbtype nucl -out data/genome/blastdb/ccds -parse_seqids
Run:  python run_blast.py
The Qur'an text files are READ-ONLY; controls are random freq-matched sequences (never the verses).
"""
import os, re, subprocess, unicodedata, json, time
import numpy as np
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,"..")
DB=os.path.join(ROOT,"data","genome","blastdb","ccds")
WORK=os.path.join(HERE,"blast_work"); os.makedirs(WORK,exist_ok=True)
N=20            # mappings per unit
EVALUE="10"     # permissive, like the paper; we judge real-vs-control, not raw e-value
SURAS=[112,108,103,110,114,1]   # short suras (edit/extend)

bases="TCAG"
codons=[a+b+c for a in bases for b in bases for c in bases]
STOP={"TAA","TAG","TGA"}
SENSE=[c for c in codons if c not in STOP]   # 61 sense codons (swap in codon-usage weights if desired)

def skel(t):
    t=unicodedata.normalize("NFD",t); t="".join(c for c in t if not unicodedata.combining(c))
    return "".join(c for c in t if "ء"<=c<="ي" and c!="ـ")
def sura_text(n):
    out=""
    for line in open(os.path.join(ROOT,"data","quran","quran_arabic_verses.tsv"),encoding="utf-8"):  # READ-ONLY
        if "\t" in line and line.split(":")[0]==str(n): out+=skel(line.split("\t",1)[1])
    return out

def gen_dna(letters, rng):
    uniq=sorted(set(letters)); m={c:SENSE[rng.integers(len(SENSE))] for c in uniq}
    return "".join(m[c] for c in letters)

def write_fasta(path, named):
    with open(path,"w") as f:
        for name,seq in named: f.write(f">{name}\n{seq}\n")

def tblastx(query):
    out=query+".tsv"
    try:
        subprocess.run(["tblastx","-query",query,"-db",DB,"-evalue",EVALUE,
                        "-outfmt","6","-max_target_seqs","5","-out",out],check=True)
    except FileNotFoundError:
        raise SystemExit("tblastx not found — install BLAST+ and build the DB (see RUN_BLAST.md).")
    return out

def best_bits(tsv):
    best={}
    if not os.path.exists(tsv): return best
    for ln in open(tsv):
        p=ln.split("\t")
        if len(p)<12: continue
        q=p[0]; bit=float(p[11])
        best[q]=max(best.get(q,0.0),bit)
    return best

def batch(label, units, rng):
    named=[]
    for uname,letters in units:
        for i in range(N):
            named.append((f"{label}_{uname}_m{i}", gen_dna(letters, rng)))
    fa=os.path.join(WORK,f"{label}.fasta"); write_fasta(fa,named)
    bb=best_bits(tblastx(fa))
    vals=np.array(list(bb.values())) if bb else np.array([0.0])
    return vals

def main():
    rng=np.random.default_rng(0)
    units=[(f"sura{n}", sura_text(n)) for n in SURAS]
    lens={u:len(s) for u,s in units}
    # composition control: freq-matched random letter sequences, same lengths (Qur'an NOT rearranged)
    allskel="".join(skel(open(os.path.join(ROOT,"data","quran","quran_arabic_concat.txt"),encoding="utf-8").read()))
    al=sorted(set(allskel)); fr=np.array([allskel.count(c) for c in al],float); fr/=fr.sum()
    ctrl=[(u, "".join(np.random.default_rng(7+i).choice(al,size=lens[u],p=fr))) for i,(u,_) in enumerate(units)]
    print("Running tblastx on REAL Qur'an mappings ...")
    real=batch("real", units, rng)
    print("Running tblastx on COMPOSITION CONTROL ...")
    ctl =batch("ctrl", ctrl, np.random.default_rng(1))
    row={"ts":time.strftime("%Y-%m-%d %H:%M"),"objective":"tblastx best bit-score vs CCDS","N":N,"suras":SURAS,
         "real_bits_mean":round(float(real.mean()),2),"real_bits_max":round(float(real.max()),2),
         "ctrl_bits_mean":round(float(ctl.mean()),2),"ctrl_bits_max":round(float(ctl.max()),2),
         "delta_mean":round(float(real.mean()-ctl.mean()),2)}
    print(json.dumps(row,indent=2))
    print("\nReal >> control (mean & max bit-score) => signal. Real ~ control => null (expected).")
    led=os.path.join(HERE,"ledger.json"); cur=json.load(open(led)) if os.path.exists(led) else []
    cur.append(row); json.dump(cur,open(led,"w"),indent=2)

if __name__=="__main__": main()
