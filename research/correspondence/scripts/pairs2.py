#!/usr/bin/env python3
# BILATERAL PAIRS pass-2: (1) content pairs after LENGTH control; (2) STRUCTURAL-form twins (opening template).
import unicodedata, collections, math
import numpy as np
def norm(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if not(0x64B<=ord(c)<=0x65F) and ord(c)!=0x670)
    return s.replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا').replace('ئ','ي').replace('ؤ','و')
AR=set(chr(c) for c in range(0x621,0x64B))
def rasm(s): return ''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
TX="research/two_books_genome/data/quran/quran_arabic_verses.tsv"; RBA="research/two_books_genome/roots_by_ayah.tsv"
sur=collections.defaultdict(collections.Counter); opening={}; firstverse={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1); s=int(k.split(':')[0])
        if 1<=s<=114:
            for x in r.split():
                if x and x!='NA': sur[s][x]+=1
for ln in open(TX,encoding='utf-8'):
    if '\t' in ln:
        sa,tx=ln.rstrip('\n').split('\t',1); s,a=sa.split(':'); s=int(s)
        if int(a)==1: opening[s]=tuple(norm(w) for w in tx.split()[:3])
suras=sorted(sur); S=len(suras); idx={s:i for i,s in enumerate(suras)}
df=collections.Counter()
for s in suras:
    for r in sur[s]: df[r]+=1
length=np.array([sum(sur[s].values()) for s in suras],float); loglen=np.log(length)
roots=sorted(df); ri={r:i for i,r in enumerate(roots)}; idf={r:math.log(S/df[r]) for r in df}
X=np.zeros((S,len(roots)))
for s in suras:
    for r,n in sur[s].items(): X[idx[s],ri[r]]=n*idf[r]
X=X/(np.linalg.norm(X,axis=1,keepdims=True)+1e-9)
C=X@X.T
iu=np.triu_indices(S,1)
lsim=-np.abs(loglen[iu[0]]-loglen[iu[1]])
b=np.polyfit(lsim,C[iu],1); resid=C[iu]-np.polyval(b,lsim)
Cr=np.full((S,S),-9.0); Cr[iu]=resid; Cr=np.triu(Cr)+np.triu(Cr).T
np.fill_diagonal(Cr,-9)
nn=Cr.argmax(1); mu,sd=resid.mean(),resid.std()
print("(1) CONTENT pairs after LENGTH control — reciprocal near-duplicates:")
got=0
for i in range(S):
    j=nn[i]
    if nn[j]==i and i<j and (Cr[i,j]-mu)/sd>3:
        print(f"     {suras[i]} <-> {suras[j]}  z={(Cr[i,j]-mu)/sd:+.1f}"); got+=1
print(f"     length-robust content-twin pairs (z>3): {got}")
# (2) STRUCTURAL twins — shared opening template (first word identical AND parallel)
firstword=collections.defaultdict(list)
for s in suras:
    if s in opening and opening[s]: firstword[opening[s][0]].append(s)
print("\n(2) STRUCTURAL twins — sūras sharing an opening template (the muʿawwidhatān signature):")
for w,ss in sorted(firstword.items(),key=lambda x:-len(x[1])):
    if len(ss)>=2 and w not in ('',):
        # show only distinctive templates (not the ubiquitous bare openers)
        print(f"     opening '{w}': suras {ss}" if len(ss)<=8 else f"     opening '{w}': {len(ss)} suras (generic)")
