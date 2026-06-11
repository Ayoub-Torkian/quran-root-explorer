#!/usr/bin/env python3
"""Download the Arabic Qur'an text from parsquran.com (the LOCKED source) and
build a clean corpus file for the two-books study.

RUN THIS ON YOUR OWN MACHINE (it needs open network + writes Arabic to disk,
which the assistant chat cannot do because scripture can't be echoed there).

Endpoint (verified 2026-06-08):
    http://www.parsquran.com/data/show.php?lang=ara&sura=S&ayat=0&user=eng&tran=1
returns the COMPLETE sura S: each Arabic verse ends in an ornate marker  ﴿N﴾
(Arabic-Indic digits inside U+FD3F…U+FD3E), followed by a Persian gloss that
ends in an ASCII "(N)". We extract the Arabic run that ends at each ﴿N﴾ marker.

Output:
    data/quran/quran_arabic_verses.tsv   # "sura:verse\t<arabic verse>"
    data/quran/quran_arabic_concat.txt   # all verses concatenated (for structural analysis)
    data/quran/raw/sura_S.html           # cached raw pages (so parsing can be re-run offline)

Dependencies:  pip install requests beautifulsoup4
"""
import os, re, time, sys
import requests
from bs4 import BeautifulSoup

OUT = os.path.join(os.path.dirname(__file__), "..", "data", "quran")
RAW = os.path.join(OUT, "raw")
URL = "http://www.parsquran.com/data/show.php?lang=ara&sura={s}&ayat=0&user=eng&tran=1"

ARABIC = r"؀-ۿݐ-ݿﭐ-﷿ﹰ-﻿"
DIGITS = r"٠-٩۰-۹"   # Arabic-Indic (U+0660-0669) AND Persian/Extended (U+06F0-06F9)
ORNATE_MARK = re.compile(r"[﴿]\s*[" + DIGITS + r"]+\s*[﴾]")   # ﴿ digits ﴾
# a verse = the maximal run of Arabic chars + spaces ending right before an ornate marker
VERSE = re.compile(r"([" + ARABIC + r"][" + ARABIC + r"\s]*?)\s*[﴿]\s*([" + DIGITS + r"]+)\s*[﴾]")

def fetch_sura(s):
    r = requests.get(URL.format(s=s), timeout=30)
    r.encoding = "utf-8"
    return r.text

def parse_verses(html):
    text = BeautifulSoup(html, "html.parser").get_text(" ")
    out = []
    for m in VERSE.finditer(text):
        arabic = re.sub(r"\s+", " ", m.group(1)).strip()
        # keep only Arabic-script + space (drops any stray latin/persian-gloss bleed)
        arabic = "".join(ch for ch in arabic if re.match("[" + ARABIC + r"\s]", ch)).strip()
        if arabic:
            out.append(arabic)
    return out

def main():
    os.makedirs(RAW, exist_ok=True)
    tsv = open(os.path.join(OUT, "quran_arabic_verses.tsv"), "w", encoding="utf-8")
    concat = open(os.path.join(OUT, "quran_arabic_concat.txt"), "w", encoding="utf-8")
    total = 0
    for s in range(1, 115):
        cache = os.path.join(RAW, f"sura_{s}.html")
        if os.path.exists(cache):
            html = open(cache, encoding="utf-8").read()
        else:
            html = fetch_sura(s)
            open(cache, "w", encoding="utf-8").write(html)
            time.sleep(0.7)   # be polite
        if s == 1:   # numbers-only diagnostic (no scripture echoed)
            text = BeautifulSoup(html, "html.parser").get_text(" ")
            print(f"  [diag sura1] html_len={len(html)} text_len={len(text)} "
                  f"ornate_open={text.count(chr(0xFD3F))} marker_matches={len(ORNATE_MARK.findall(text))} "
                  f"arabic_chars={len(re.findall('['+ARABIC+']', text))}")
        verses = parse_verses(html)
        for i, v in enumerate(verses, 1):
            tsv.write(f"{s}:{i}\t{v}\n")
            concat.write(v + " ")
        total += len(verses)
        print(f"sura {s:3d}: {len(verses)} verses")
    tsv.close(); concat.close()
    print(f"DONE. {total} verses written to {OUT}")
    print("Sanity check: total Qur'an verses should be 6236 (excl. basmalas).")
    print("If counts look off, inspect data/quran/raw/sura_1.html and adjust the VERSE regex.")

if __name__ == "__main__":
    main()
