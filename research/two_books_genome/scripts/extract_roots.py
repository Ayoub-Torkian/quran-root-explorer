#!/usr/bin/env python3
"""Extract the Qur'an ROOT-token sequence from Book6.xlsx -> roots_seq.txt.

Run this LOCALLY (the real Book6.xlsx is a Git-LFS file, not present in the assistant's
sandbox). It writes research/two_books_genome/roots_seq.txt — a plain-text file (space-
separated root tokens, document order) that DOES sync, so the assistant can then run the
root-map test on it.

    # from the two_books_genome folder:
    python scripts/extract_roots.py "C:\\Users\\torki\\Downloads\\QuranProject\\quran-root-explorer\\data\\Book6.xlsx"

No data is modified; this only reads Book6.xlsx and writes one text file.
"""
import os, sys, unicodedata
HERE=os.path.dirname(__file__); REPO=os.path.abspath(os.path.join(HERE,"..","..",".."))
CANDS=[]
if len(sys.argv)>1: CANDS.append(sys.argv[1])
CANDS+= [r"C:\Users\torki\Downloads\QuranProject\quran-root-explorer\data\Book6.xlsx",
         os.path.join(REPO,"Book6.xlsx"), os.path.join(REPO,"book6.xlsx")]
XLSX=None
for p in CANDS:
    if p and os.path.exists(p) and os.path.getsize(p)>10000: XLSX=p; break
if not XLSX: raise SystemExit("Book6.xlsx not found (>10KB). Pass its path as the first argument, "
                              "or run `git lfs pull` so it is materialized.")
print("reading:",XLSX)

import openpyxl
COL_SURAH="ش  سوره"; COL_ROOTS="ریشه نحوی"
def strip(s):
    s=unicodedata.normalize("NFD",str(s)); return "".join(c for c in s if not unicodedata.combining(c))

wb=openpyxl.load_workbook(XLSX, read_only=True); ws=wb.active
rows=list(ws.iter_rows(values_only=True))
# detect header row (where both column names appear)
hr=11
for i,r in enumerate(rows[:25]):
    vals=[str(v) if v is not None else "" for v in r]
    if COL_SURAH in vals and COL_ROOTS in vals: hr=i; break
header=[str(v) if v is not None else "" for v in rows[hr]]
ci=header.index(COL_ROOTS)
COL_SU="ش  سوره"; COL_AY="ش  آیه"
si=header.index(COL_SU) if COL_SU in header else None
ai=header.index(COL_AY) if COL_AY in header else None
seq=[]
for r in rows[hr+1:]:
    if ci<len(r) and r[ci] is not None:
        for tok in strip(r[ci]).split():
            if tok and tok!="nan": seq.append(tok)
out=os.path.join(HERE,"..","roots_seq.txt")
open(out,"w",encoding="utf-8").write(" ".join(seq))
from collections import Counter
c=Counter(seq)
print(f"wrote {out}\n  root tokens={len(seq)}  distinct roots={len(c)}  "
      f"hapax={sum(1 for k,n in c.items() if n==1)}  ratio={len(seq)/max(len(c),1):.1f}")

# --- PER-ĀYAH roots (for the rasm topic channel; aligns to sura:ayah keys) ---
if si is not None and ai is not None:
    out2=os.path.join(HERE,"..","roots_by_ayah.tsv"); n=0
    with open(out2,"w",encoding="utf-8") as fh:
        for r in rows[hr+1:]:
            if si<len(r) and ai<len(r) and r[si] is not None and r[ai] is not None:
                try: key=f"{int(r[si])}:{int(r[ai])}"
                except Exception: continue
                toks=[t for t in (strip(r[ci]).split() if ci<len(r) and r[ci] is not None else []) if t and t!="nan"]
                fh.write(key+"\t"+" ".join(toks)+"\n"); n+=1
    print(f"wrote {out2}\n  ayah rows={n} (use this for the sūra topic channel; one line per āyah)")
else:
    print("WARN: surah/ayah columns not found; per-ayah file not written")
