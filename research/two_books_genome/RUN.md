# How to run the study end-to-end

First `cd` into this folder (the scripts resolve their data paths relative to
themselves, so the working directory must be here). Steps 1–2 run on **your machine**
(open network; the Arabic step writes scripture to disk, which the assistant chat
cannot do). Step 3 is the analysis.

### Windows PowerShell
```powershell
cd C:\Users\torki\Downloads\Quran_Root_Explorer_Web_v1.2\research\two_books_genome
python -m pip install requests beautifulsoup4 numpy     # one-time

python scripts\fetch_refseq_cds.py     # 1. genome  -> data\genome\ccds_cds.fasta
python scripts\fetch_parsquran.py      # 2. Arabic  -> data\quran\quran_arabic_concat.txt (sanity: 6236 verses)
python scripts\fetch_languages.py      # 3. language-class set -> data\languages\*.txt
python scripts\run_pipeline.py 2000    # 4. analysis -> scripts\pipeline_results.json

# run_pipeline auto-includes EVERY .txt in data\languages\. Drop in your own
# (Hebrew, Latin, non-Qur'an Arabic, ...) and re-run -- no code changes needed.
```

### macOS / Linux (bash)
```bash
cd .../research/two_books_genome
pip install requests beautifulsoup4 numpy
python scripts/fetch_refseq_cds.py
python scripts/fetch_parsquran.py
python scripts/fetch_languages.py
python scripts/run_pipeline.py 2000
```

## What you get
One table comparing **CDS_real vs CDS_shuffled** and each **language vs its shuffle**
on: gzip redundancy, DFA Hurst, and MI-decay exponent γ — each with a 95% CI.

## How to read it (the decisive test — see CHALLENGES.md)
- First confirm the controls behave: every *shuffle* should lose the structure (gzip
  rises toward 1, MI_gamma degenerates, Hurst → ~0.5).
- Then the real question: do the **language** exponents (Hurst, MI_gamma) **overlap
  the real genome's CIs** *and* sit clearly **apart from their shuffles**?
  - Overlap + separation  → language and genome share a long-range structural class.
  - Different exponents    → **no** shared structure. This is the honest-null outcome
    and is a *successful* result, not a failure.
- Only a robust positive here justifies moving to **Route A** (the searched
  letter→codon BLAST test in METHODOLOGY.md), which carries the Bible-Code risk and
  must not be attempted before Route B shows something.

## Stages after this
- If Route B is positive: re-run with ≥2 more languages (replication), larger chunk
  lengths (true long-range scales), and bootstrap the exponents.
- Then, and only then, Route A with the full mandatory baseline battery.
