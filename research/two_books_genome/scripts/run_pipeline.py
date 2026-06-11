#!/usr/bin/env python3
"""End-to-end Route-B pipeline (mapping-free, confirmation-grade).

Ties the three corpora together and runs the structural comparison with formal
exponent fits + 95% CIs across ALL modalities in ONE table:
    genome (real CDS) vs its shuffle, and each LANGUAGE vs its shuffle.

Prereqs (build these first, on your machine):
    python fetch_refseq_cds.py      ->  data/genome/ccds_cds.fasta
    python fetch_parsquran.py       ->  data/quran/quran_arabic_concat.txt
    (English is optional; point ENGLISH at any large .txt for a language control.)

Run:
    python run_pipeline.py [chunkLen]

The decisive question (see CHALLENGES.md): do the LANGUAGE exponents (Hurst, MI_gamma)
overlap the REAL genome's CIs AND sit clearly apart from their shuffles? Overlap +
separation = shared long-range structural class. Different exponents = no shared
structure (the honest-null outcome). A null is a successful result.
"""
import os, re, sys, json, math, random, glob, unicodedata
import numpy as np
from route_b_confirm import load_fasta, chunk_stats, shuf   # reuse the validated kernel
random.seed(11); np.random.seed(11)

HERE = os.path.dirname(__file__)
CDS_FA   = os.path.join(HERE, "..", "data", "genome", "ccds_cds.fasta")
CDS_TOY  = os.path.join(HERE, "..", "data", "examples", "human_cds_set.fasta")
QURAN    = os.path.join(HERE, "..", "data", "quran", "quran_arabic_concat.txt")
LANGDIR  = os.path.join(HERE, "..", "data", "languages")   # any .txt here is auto-included
ENGLISH  = os.environ.get("ENGLISH", "")   # optional extra path to a large .txt
LANG_CAP = 2_000_000   # cap per language so runtime stays bounded (genome dominates anyway)

def load_language(path):
    """Script-agnostic letter skeleton: lowercase, strip combining marks (diacritics),
    keep only Unicode letters. Works for Latin/Greek/Cyrillic/etc. uniformly."""
    t = open(path, encoding="utf-8", errors="ignore").read().lower()
    t = unicodedata.normalize("NFD", t)
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = "".join(ch for ch in t if unicodedata.category(ch).startswith("L"))
    return t[:LANG_CAP]

# Arabic diacritics / marks to strip -> bare consonantal skeleton (see data/arabic_letters.md)
AR_DIACRITICS = "".join(chr(c) for c in list(range(0x064B,0x0653))+[0x0670,0x0640,0x06D6,0x06D7,0x06D8,0x06D9,0x06DA,0x06DB,0x06DC,0x06DF,0x06E0,0x06E1,0x06E2,0x06E5,0x06E6,0x06E7,0x06E8,0x06EA,0x06EB,0x06EC,0x06ED])
def load_arabic_skeleton(p):
    t = open(p, encoding="utf-8").read()
    t = t.translate({ord(c): None for c in AR_DIACRITICS})
    # fold common variants to a 28-letter skeleton; keep only Arabic consonant letters
    t = (t.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ٱ","ا")
           .replace("ؤ","و").replace("ئ","ي").replace("ى","ي").replace("ة","ه").replace("ء",""))
    return re.sub(r"[^ء-ي]", "", t)

def main():
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    cds_path = CDS_FA if os.path.exists(CDS_FA) else CDS_TOY
    if cds_path == CDS_TOY:
        print("WARNING: full CCDS not found; using the 6-gene TOY set. Run fetch_refseq_cds.py "
              "for a real genome corpus (the toy gives meaningless wide CIs).")
    cds = load_fasta(cds_path)

    sets = [("CDS_real", cds), ("CDS_shuffled", shuf(cds))]
    if os.path.exists(QURAN):
        ar = load_arabic_skeleton(QURAN)
        sets += [("Quran_arabic", ar), ("Quran_shuffled", shuf(ar))]
    else:
        print(f"NOTE: {QURAN} not found — run fetch_parsquran.py to add the Arabic arm.")
    # auto-include every language file in data/languages/ (run fetch_languages.py)
    for f in sorted(glob.glob(os.path.join(LANGDIR, "*.txt"))):
        name = os.path.splitext(os.path.basename(f))[0]
        s = load_language(f)
        sets += [(name, s), (name + "_shuffled", shuf(s))]
    if ENGLISH and os.path.exists(ENGLISH):
        sets += [("English_extra", load_language(ENGLISH)),
                 ("English_extra_shuffled", shuf(load_language(ENGLISH)))]

    print(f"chunkLen={L}")
    print(f"{'sequence':16}{'N':>9}{'chunks':>7}  gzip            Hurst(DFA)      MI_gamma")
    res = {}
    for name, s in sets:
        if len(s) < 3*L:
            print(f"{name:16}{len(s):9d}{'--':>7}  (too short for chunkLen={L})"); continue
        st, K = chunk_stats(s, L); res[name] = {"N": len(s), "chunks": K, "metrics": st}
        f = lambda m: f"{st[m][0]:.3f}±{st[m][1]:.3f}"
        print(f"{name:16}{len(s):9d}{K:7d}  {f('gzip'):15} {f('Hurst'):15} {f('MI_gamma'):15}")
    json.dump(res, open(os.path.join(HERE, "pipeline_results.json"), "w"), indent=2)
    print("\nwrote pipeline_results.json")
    print("Interpretation: compare each language's Hurst & MI_gamma CIs to CDS_real's, and")
    print("confirm both are separated from their shuffles. Different exponents => honest null.")

if __name__ == "__main__":
    main()
