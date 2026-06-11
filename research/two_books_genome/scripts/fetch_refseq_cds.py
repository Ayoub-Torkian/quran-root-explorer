#!/usr/bin/env python3
"""Download the full human coding-sequence corpus (the "Act of God" / expressed
genome side) for the two-books study.

We use **CCDS (Consensus CDS)** — the curated set of coding regions agreed by
NCBI/Ensembl/UCSC. It is exactly "expressed, translated coding sequence" (post-
splicing, in-frame), ~30-40k sequences, one clean nucleotide FASTA. This replaces
the 6-gene toy used in the pilot.

RUN ON YOUR MACHINE (needs open network; ~tens of MB download).

Output:
    data/genome/ccds_cds.fasta        # all consensus CDS, nucleotide
    data/genome/CCDS_nucleotide.current.fna.gz   # cached raw download

Dependencies: standard library only (urllib, gzip).

Alternative sources (if CCDS URL changes):
  - NCBI datasets CLI:  datasets download gene taxon human --include cds
  - RefSeq FTP mRNA:    ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/mRNA_Prot/  (then extract CDS via feature table)
  - Per-accession:      efetch -db nuccore -id <NM_...> -format fasta_cds_na
"""
import os, gzip, shutil, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "genome")
URL = "https://ftp.ncbi.nlm.nih.gov/pub/CCDS/current_human/CCDS_nucleotide.current.fna.gz"
GZ  = os.path.join(OUT, "CCDS_nucleotide.current.fna.gz")
FA  = os.path.join(OUT, "ccds_cds.fasta")

def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.exists(GZ):
        print(f"Downloading {URL} ...")
        req = urllib.request.Request(URL, headers={"User-Agent": "two-books-study/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(GZ, "wb") as f:
            shutil.copyfileobj(r, f)
        print(f"  saved {os.path.getsize(GZ)/1e6:.1f} MB -> {GZ}")
    else:
        print(f"Using cached {GZ}")
    print("Decompressing ...")
    nseq = nnt = 0
    with gzip.open(GZ, "rt") as g, open(FA, "w") as out:
        for line in g:
            out.write(line)
            if line.startswith(">"): nseq += 1
            else: nnt += len(line.strip())
    print(f"DONE. {nseq:,} consensus CDS, {nnt:,} nt -> {FA}")
    print("This is the genome corpus for run_pipeline.py.")

if __name__ == "__main__":
    main()
