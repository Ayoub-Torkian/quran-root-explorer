#!/usr/bin/env python3
"""EXPRESSIBILITY test (data-driven, no mapping search, no a-priori choice).

Same text yields different peptide lengths under different char->nucleotide
granularities, so it clears the protein-length floor at different rates. This
measures, from the actual Qur'an, what fraction of units (ayah / sura) reach the
~50-aa and ~100-aa folding floors under each option. It does NOT decide the
granularity — it sizes the testable set for each, which determines whether a route
has enough units to reach high statistical confidence.

Outputs numbers only. Reads data/quran/quran_arabic_verses.tsv (built by
fetch_parsquran.py). Run after that exists.
"""
import os, unicodedata, statistics as st
from collections import defaultdict
HERE=os.path.dirname(__file__)
TSV=os.path.join(HERE,"..","data","quran","quran_arabic_verses.tsv")

def skeleton_len(txt):
    txt=unicodedata.normalize("NFD",txt)
    txt="".join(c for c in txt if not unicodedata.combining(c))
    return sum(1 for c in txt if "ء"<=c<="ي" and c!="ـ")

def main():
    if not os.path.exists(TSV):
        print(f"Missing {TSV} — run fetch_parsquran.py first."); return
    sura=defaultdict(int); ay=[]; alpha=set()
    for line in open(TSV,encoding="utf-8"):
        if "\t" not in line: continue
        ref,txt=line.rstrip("\n").split("\t",1); s=int(ref.split(":")[0])
        t=unicodedata.normalize("NFD",txt); t="".join(c for c in t if not unicodedata.combining(c))
        letters=[c for c in t if "ء"<=c<="ي" and c!="ـ"]
        alpha.update(letters); n=len(letters); ay.append(n); sura[s]+=n
    suras=[sura[k] for k in sorted(sura)]
    def frac(xs,thr): return 100*sum(1 for x in xs if x>=thr)/len(xs)
    print(f"verses={len(ay)} suras={len(suras)} consonantal_alphabet={len(alpha)}")
    print(f"AYAH chars: min={min(ay)} median={int(st.median(ay))} mean={st.mean(ay):.1f} max={max(ay)}")
    print(f"SURA chars: min={min(suras)} median={int(st.median(suras))} mean={st.mean(suras):.0f} max={max(suras)}")
    print(f"\n{'option':16}{'aa=':12}  %ayah>=50  %ayah>=100  %sura>=50  %sura>=100")
    for name,div in [("char=codon",1),("2chars=codon",2),("char=base",3)]:
        a50=frac(ay,50*div); a100=frac(ay,100*div); s50=frac(suras,50*div); s100=frac(suras,100*div)
        print(f"{name:16}{'N/'+str(div):12}  {a50:8.1f}  {a100:9.1f}  {s50:8.1f}  {s100:9.1f}")
    print("\nNot all text is expressible; the fraction depends on (granularity x unit).")
    print("This sizes the testable set per option — it does not pick one. Decide by which")
    print("route, once run through the full cascade, beats its control battery with power.")

if __name__=="__main__": main()
