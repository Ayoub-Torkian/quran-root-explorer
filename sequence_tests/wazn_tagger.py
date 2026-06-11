# -*- coding: utf-8 -*-
"""
Morphological-template (wazn) classifier for raw Arabic text.
Classifies each content word into a coarse DERIVATIONAL bucket from its
consonantal skeleton (de-diacritized) — applied identically to every corpus so
its noise is symmetric. Calibrated against the Qur'an gold seg_tokens.

Buckets (priority order; first match wins):
  X     form X / istif'al / mustaf'il    است / مست
  VII   form VII / infi'al               ان...  (len>=5)
  MU    mu-participle II-X (act/pass)     م...   (مفعل/متفعل/منفعل/مفعول...)
  AF    form IV / elative af'al           ا...   (was أ)
  FAIL  active participle fa'il           C-ا-C(-C)   (alif in 2nd slot)
  INT   intensive/attribute fa'il/fa''al/fa'ul  فعيل/فعول  (long ي or و in penult)
  PLUR  broken plural af'al/fu'ul/fi'al   افعال / فعول / فعال shapes
  BASE  bare triliteral form I            3 consonants, no derivation marker
  OTHER everything else
"""
import re

_DIA = re.compile(r"[ً-ْٰـۖ-ۭ]")
def norm(t):
    t = _DIA.sub("", str(t))
    t = re.sub(r"[آأإٱ]", "ا", t)
    t = re.sub(r"[ىیﻯ]", "ي", t)
    return t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء").strip()

WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
def words(s):
    return [w for w in WORD.findall(norm(s)) if w]

PROCLITIC = ("ال", "و", "ف", "ب", "ك", "ل")
ENCLITIC = ("هما", "كما", "هم", "هن", "كم", "نا", "ها", "ه", "ك", "ي",
            "ون", "ين", "ات", "ان", "وا")

def _strip(w):
    """strip a single leading proclitic (و/ف then ال) — minimal, to keep skeleton."""
    if w.startswith("وال") or w.startswith("فال"):
        return w[3:]
    if w.startswith("ال") and len(w) > 3:
        return w[2:]
    if w[:1] in ("و", "ف") and len(w) > 3:
        return w[1:]
    return w

VOWELS = set("اوي")
def bucket(w):
    s = _strip(w)
    n = len(s)
    if n < 3:
        return "OTHER"
    if s.startswith("است") or s.startswith("مست"):
        return "X"
    if s.startswith("ان") and n >= 5:
        return "VII"
    if s.startswith("م") and n >= 4:
        return "MU"
    if s.startswith("ا") and n >= 4:
        # af'al (form IV / elative) vs broken plural af'al (افعال) vs noun
        if re.match(r"^ا..ا.$", s):
            return "PLUR"
        return "AF"
    # active participle fa'il: alif in 2nd slot, 4 letters (C-ā-C-C)
    if n == 4 and s[1] == "ا" and s[0] not in VOWELS and s[2] not in VOWELS and s[3] not in VOWELS:
        return "FAIL"
    # intensive/attribute fa'il (فعيل) or fa'ul (فعول): long ي/و in penult of a 4-letter stem
    if n == 4 and s[2] in ("ي", "و") and s[0] not in VOWELS and s[1] not in VOWELS and s[3] not in VOWELS:
        return "INT"
    # broken plural fu'ul/fi'al shape (فعول/فعال): C-C-ā/ū-C
    if n == 4 and s[2] in ("و", "ا") and s[3] not in VOWELS and s[0] not in VOWELS and s[1] not in VOWELS:
        return "PLUR"
    if n == 3 and not (set(s) & VOWELS):
        return "BASE"
    return "OTHER"

BUCKETS = ["X", "VII", "MU", "AF", "FAIL", "INT", "PLUR", "BASE", "OTHER"]

def hist(word_list):
    from collections import Counter
    c = Counter(bucket(w) for w in word_list)
    tot = sum(c.values()) or 1
    return {b: c.get(b, 0) / tot for b in BUCKETS}
