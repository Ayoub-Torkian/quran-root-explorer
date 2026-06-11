#!/usr/bin/env python3
# E · EXTERNAL INTERFACE — outward-facing markers (address/command/2nd-person). Prediction: concentrate at onsets.
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
    sa,tx=ln.rstrip('\n').split('\t',1); s,a=sa.split(':'); s=int(s);a=int(a)
    toks=[norm(w) for w in tx.split()]
    verses.append((s,a,toks))
def outward(toks):
    voc = any(t=='يا' or 'ايها' in t or t.startswith('يايها') for t in toks)
    cmd = any(t=='قل' for t in toks)
    sec = any(t.endswith('كم') or t.endswith('كن') or t in ('انت','انتم','انتما') for t in toks)
    return voc, cmd, sec, (voc or cmd or sec)
first=[]; interior=[]
nv=nc=ns=0; tot=0
for s,a,toks in verses:
    voc,cmd,sec,out=outward(toks); tot+=1; nv+=voc;nc+=cmd;ns+=sec
    (first if a==1 else interior).append(1 if out else 0)
print("E · EXTERNAL INTERFACE — outward-facing markers:")
print(f"   corpus interface size: vocative {nv/tot:.0%}, command(قل) {nc/tot:.0%}, 2nd-person {ns/tot:.0%}; ANY outward {np.mean([outward(t)[3] for _,_,t in verses]):.0%} of verses")
fa=np.mean(first); ia=np.mean(interior)
# significance: are first verses more outward-facing than interior? permutation
allv=np.array(first+interior); nf=len(first)
nul=[np.mean(np.random.choice(allv,nf,replace=False)) for _ in range(2000)]
z=(fa-np.mean(nul))/np.std(nul)
print(f"   PREDICTION test — outward-facing rate: sura ONSET (1st verse) {fa:.0%} vs interior {ia:.0%}  z={z:+.1f}")
print(f"   {'CONFIRMED: interface concentrates at the opening (surface), like sensory organs/orifices' if z>2 else 'NOT confirmed at onset'}")
# also: does it concentrate at sura ENDINGS (the other surface)?
last=[]; mid=[]
bys=collections.defaultdict(list)
for i,(s,a,t) in enumerate(verses): bys[s].append(i)
for s,ix in bys.items():
    for pos,i in enumerate(ix):
        o=outward(verses[i][2])[3]
        (last if pos==len(ix)-1 else mid).append(1 if o else 0)
zl=(np.mean(last)-np.mean(mid))/ (np.std([np.mean(np.random.choice(np.array(last+mid),len(last),replace=False)) for _ in range(1000)])+1e-9)
print(f"   sura END (last verse) {np.mean(last):.0%} vs middle {np.mean(mid):.0%}  z={zl:+.1f}")
