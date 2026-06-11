# Real-BLAST run — setup & run (your machine)

The faithful version of the paper's objective: `tblastx` of mapped Qur'an sequences against a
local human coding-sequence database — with the control floor built in. Runs locally (the NCBI
web API is rate-limited/down; local BLAST+ is the way). Qur'an files are read-only; controls are
frequency-matched random sequences (the verses are never rearranged).

## 1. Install BLAST+
Easiest (cross-platform), via conda/mamba:
```bash
conda install -c bioconda blast        # provides makeblastdb, tblastx, blastn
```
Or on Windows without conda: download "BLAST+ executables" from
https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ (the win64 installer), and make sure
`makeblastdb.exe` and `tblastx.exe` are on your PATH.

## 2. Build the database (once)
From `research/two_books_genome/` (after `python scripts/fetch_refseq_cds.py` has produced the CCDS):
```bash
mkdir -p data/genome/blastdb
makeblastdb -in data/genome/ccds_cds.fasta -dbtype nucl -out data/genome/blastdb/ccds -parse_seqids
```

## 3. Run
```bash
python scripts/run_blast.py
```
It generates N=20 frequency-sampled char→codon mappings for several short sūras, BLASTs them with
`tblastx`, and does the identical thing for a composition control. It prints and logs (to
`scripts/ledger.json`):
```
real_bits_mean / real_bits_max   vs   ctrl_bits_mean / ctrl_bits_max   and   delta_mean
```

## 4. How to read it (the only honest read)
A `tblastx` hit against this database is **expected for almost any sequence** — so the raw bit-score
or e-value means nothing on its own. The signal is the **comparison to the control**:
- **real ≫ control** (mean *and* max bit-score clearly higher) → a genuine effect. Then replicate
  across many sūras/seeds and test significance before any claim.
- **real ≈ control** → null (the prior, after everything else).

## Notes / knobs
- `SURAS`, `N`, `EVALUE` are at the top of `run_blast.py`.
- The char→codon draw is uniform over the 61 sense codons; to match the paper exactly, swap in a
  human codon-usage frequency table (genscript) where `SENSE` is sampled.
- `tblastx` is slow (6-frame translated search). Short sūras keep it tractable; scale up gradually.
- This is the one objective we had not run faithfully; honest prior from Steps 0–8, Route B, and the
  folding null is that it returns the same null — but it closes the loop on the paper's own method.
