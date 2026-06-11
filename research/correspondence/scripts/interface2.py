#!/usr/bin/env python3
# E refined: surface = CORPUS boundaries + interface CLUSTERING (zones), not sura-onsets.
import unicodedata, collections, random
import numpy as np
random.seed(1); np.random.seed(1)
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not (0x64B<=ord(c)<=0x652) and ord(c)!=0x670)
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
R="research/two_books_genome/data/quran/quran_arabic_verses.tsv"
verses=[]
for ln in open(R,encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.rstrip('\n').split('\t',1); s=int(sa.split(':')[0])
    toks=[norm(w) for w in tx.split()]
    voc=any(t=='يا' or 'ايها' in t for t in toks); cmd=any(t=='قل' for t in toks)
    sec=any(t.endswith('كم') or t.endswith('كن') or t in('انت','انتم','انتما') for t in toks)
    verses.append((s,1 if (voc or cmd or sec) else 0))
suras=sorted(set(s for s,_ in verses))
out_by_sura={s:np.mean([o for ss,o in verses if ss==s]) for s in suras}
# (1) CORPUS-boundary elevation: first/last K suras vs middle
K=5
ends=[out_by_sura[s] for s in suras[:K]]+[out_by_sura[s] for s in suras[-K:]]
mid=[out_by_sura[s] for s in suras[K:-K]]
print("E refined · CORPUS surface (interface concentrated at the whole-book's ends?):")
print(f"   first/last {K} suras outward-rate {np.mean(ends):.0%} vs middle {np.mean(mid):.0%}")
for sx in [1,113,114,112,109]:
    print(f"     sura {sx}: outward {out_by_sura[sx]:.0%}")
# (2) CLUSTERING: do outward verses form ZONES (interface patches)?
seq=np.array([o for _,o in verses])
ac=np.corrcoef(seq[:-1],seq[1:])[0,1]
nul=[np.corrcoef(p[:-1],p[1:])[0,1] for p in (np.random.permutation(seq) for _ in range(1000))]
z=(ac-np.mean(nul))/np.std(nul)
print(f"   INTERFACE CLUSTERING — outward verses run together: lag-1 autocorr {ac:+.3f} vs shuffle {np.mean(nul):+.3f} (z={z:+.1f})")
print(f"   {'CONFIRMED: the interface is LOCALIZED in zones (patches), like sensory organs/skin regions' if z>3 else 'not clustered'}")
