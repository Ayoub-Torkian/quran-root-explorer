#!/usr/bin/env python3
import unicodedata, collections
import numpy as np
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not(0x64B<=ord(c)<=0x65F) and ord(c)!=0x670)
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا').replace('ئ','ي').replace('ؤ','و')
R="research/two_books_genome/data/quran/quran_arabic_verses.tsv"
V=[]; toks_all=[]
for ln in open(R,encoding='utf-8'):
    if '\t' in ln:
        sa,tx=ln.rstrip('\n').split('\t',1); s=int(sa.split(':')[0]); T=[norm(w) for w in tx.split()]
        V.append((s,T)); toks_all+=T
N=len(V); NT=len(toks_all)
# C3 RESPIRATORY/exchange — intake (question) vs output (command) both present + balance
q=np.mean([1 if any(t in('هل','الم','افلا','اولم','افلم') or ('ايها' in t) for t in T) else 0 for _,T in V])
c=np.mean([1 if any(t=='قل' for t in T) else 0 for _,T in V])
out=np.mean([1 if any(t=='يا' or 'ايها' in t or t.endswith('كم') for t in T) else 0 for _,T in V])
print(f"C3 RESPIRATORY/exchange: intake(question) {q:.0%}, output(command) {c:.0%}, exchange surface(2nd-person) {out:.0%} -> ◑ both channels present (= E interface, redundant)")
# C5 EXCRETORY — explicit rejection/expulsion of false claim: كلا ('Nay!'), بل ('rather')
kalla=sum(T.count('كلا') for _,T in V); bal=sum(T.count('بل') for _,T in V)
vk=np.mean([1 if ('كلا' in T or 'بل' in T) else 0 for _,T in V])
print(f"C5 EXCRETORY (reject/expel false claim): 'كلا'(Nay!)×{kalla} + 'بل'(rather)×{bal}; in {vk:.0%} of verses -> ◑ explicit rejection function exists (metaphor-stretch, honest)")
# C6 LYMPHATIC — pervasive connective tissue: function-word/particle fraction (short tokens)
short=sum(1 for t in toks_all if len(t)<=2)
print(f"C6 LYMPHATIC (connective tissue): {short/NT:.0%} of tokens are short particles (و/ف/في/من…) — pervasive connective fabric -> ◑ present but generic (weakest correspondence, honest)")
