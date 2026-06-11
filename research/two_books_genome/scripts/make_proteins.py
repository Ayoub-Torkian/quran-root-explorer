#!/usr/bin/env python3
"""Make proteins from characters — turn the Qur'an into amino-acid sequences.

Uses ONE fixed, principled, NON-searched mapping: rank the Arabic letters by their
frequency in the Qur'an, and map the i-th most frequent letter to the (i mod 20)-th
most frequent human amino acid. One illustrative choice — the protein depends on it.

Output (per-sura, one protein per chapter):
    generated_proteins/quran_proteins_by_sura.fasta
    generated_proteins/mapping_frequency_rank.txt

Then fold them with scripts/fold_proteins.py.  Run: python make_proteins.py
"""
import os, unicodedata
from collections import Counter
HERE=os.path.dirname(__file__); ROOT=os.path.join(HERE,"..")
OUT=os.path.join(ROOT,"generated_proteins"); os.makedirs(OUT,exist_ok=True)
TSV=os.path.join(ROOT,"data","quran","quran_arabic_verses.tsv")
AA_RANK="LAGSVEKITRDPNFQYHMCW"   # human amino acids, most -> least frequent

def skel(t):
    t=unicodedata.normalize("NFD",t); t="".join(c for c in t if not unicodedata.combining(c))
    return "".join(c for c in t if "ء"<=c<="ي" and c!="ـ")

def main():
    if not os.path.exists(TSV):
        print(f"Missing {TSV} — run fetch_parsquran.py first."); return
    sura={}
    for line in open(TSV,encoding="utf-8"):
        if "\t" not in line: continue
        ref,txt=line.rstrip("\n").split("\t",1); s=int(ref.split(":")[0])
        sura[s]=sura.get(s,"")+skel(txt)
    freq=Counter("".join(sura.values()))
    letters=[c for c,_ in freq.most_common()]
    cmap={c:AA_RANK[i%20] for i,c in enumerate(letters)}   # fixed frequency-rank mapping
    def protein(s): return "".join(cmap[c] for c in sura[s])
    with open(os.path.join(OUT,"quran_proteins_by_sura.fasta"),"w") as f:
        for s in range(1,115):
            p=protein(s); f.write(f">sura{s:03d} len={len(p)}aa\n")
            for i in range(0,len(p),60): f.write(p[i:i+60]+"\n")
    with open(os.path.join(OUT,"mapping_frequency_rank.txt"),"w",encoding="utf-8") as f:
        f.write("Fixed frequency-rank mapping (letter freq-rank -> amino-acid freq-rank):\n")
        for i,c in enumerate(letters): f.write(f"  {i+1:2d}. {c} -> {cmap[c]}\n")
    print(f"{len(letters)} letters mapped; 114 sura-proteins written to {OUT}")
    print("Short, foldable suras (e.g. 112, 108, 103, 110, 114) are the fold candidates.")

if __name__=="__main__":
    main()
