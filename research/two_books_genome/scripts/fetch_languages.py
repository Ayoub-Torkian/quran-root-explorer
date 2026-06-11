#!/usr/bin/env python3
"""Download public-domain texts in several languages (Project Gutenberg) as the
LANGUAGE-class replication set for the two-books study.

Goal: test whether *language as a class* — across families/scripts — sits apart
from the genome's structural signature, or whether the genome resembles some
languages. Each file is auto-included by run_pipeline.py.

RUN ON YOUR MACHINE (open network). Output: data/languages/<name>.txt
You can DROP ANY .txt into data/languages/ (e.g. Hebrew or non-Qur'an Arabic prose
for a Semitic replication) — run_pipeline.py picks it up automatically.

Dependencies: standard library only.
"""
import os, re, urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "languages")

# name -> Gutenberg plain-text URL. Edit/extend freely; failures are skipped.
BOOKS = {
    "english_moby_dick":   "https://www.gutenberg.org/cache/epub/2701/pg2701.txt",   # Germanic
    "english_pride":       "https://www.gutenberg.org/cache/epub/1342/pg1342.txt",
    "french_les_miserables":"https://www.gutenberg.org/cache/epub/135/pg135.txt",    # Romance
    "spanish_don_quijote": "https://www.gutenberg.org/cache/epub/2000/pg2000.txt",   # Romance
    "german_kafka":        "https://www.gutenberg.org/cache/epub/22367/pg22367.txt", # Germanic
    "finnish_kalevala":    "https://www.gutenberg.org/cache/epub/7000/pg7000.txt",   # Finno-Ugric
    "greek_iliad":         "https://www.gutenberg.org/cache/epub/6130/pg6130.txt",   # (translation; edit if you want Greek script)
}

START = re.compile(r"\*\*\*\s*START OF (THE|THIS) PROJECT GUTENBERG.*?\*\*\*", re.I|re.S)
END   = re.compile(r"\*\*\*\s*END OF (THE|THIS) PROJECT GUTENBERG.*", re.I|re.S)

def strip_gutenberg(t):
    m = START.search(t)
    if m: t = t[m.end():]
    m = END.search(t)
    if m: t = t[:m.start()]
    return t.strip()

def main():
    os.makedirs(OUT, exist_ok=True)
    ok = 0
    for name, url in BOOKS.items():
        dest = os.path.join(OUT, name + ".txt")
        if os.path.exists(dest):
            print(f"have   {name}"); ok += 1; continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "two-books-study/1.0"})
            raw = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
            body = strip_gutenberg(raw)
            if len(body) < 20000:
                print(f"SKIP   {name}: too short / unexpected ({len(body)} chars)"); continue
            open(dest, "w", encoding="utf-8").write(body)
            print(f"saved  {name}: {len(body):,} chars"); ok += 1
        except Exception as e:
            print(f"FAIL   {name}: {e}")
    print(f"\n{ok} language file(s) in {OUT}")
    print("Tip: drop any extra .txt here (Hebrew, Latin, non-Qur'an Arabic, ...) and re-run run_pipeline.py.")

if __name__ == "__main__":
    main()
