#!/usr/bin/env python3
# CHAR-scale point pattern. Each rasm letter = point (y=āyah index, x=position in āyah's letter stream).
# (A) per-letter position bias (verse-initial vs verse-final); (B) drift through book.
import glob,unicodedata,collections,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
pts=collections.defaultdict(list); yi=0; names={'ا':'alif','ل':'lam','ن':'nun','م':'mim','ر':'ra','ي':'ya','و':'waw','ب':'ba','ه':'ha','د':'dal','ت':'ta','ف':'fa'}
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    _,tx=ln.split('\t',1); sk=skel(tx.strip()); L=len(sk)
    if L<3:continue
    for i,ch in enumerate(sk): pts[ch].append((yi, i/(L-1)))
    yi+=1
common=[c for c in pts if len(pts[c])>=200]
rng=np.random.default_rng(0)
stats=[]
for c in common:
    P=np.array(pts[c]); x=P[:,1]; y=P[:,0]/yi
    rc=np.corrcoef(x,y)[0,1]; fl=[np.corrcoef(rng.permutation(x),y)[0,1] for _ in range(60)]
    zdrift=(rc-np.mean(fl))/(np.std(fl)+1e-9)
    stats.append((c,x.mean(),len(P),zdrift))
stats.sort(key=lambda t:t[1])
print("per-letter mean position (0=verse-initial, 1=verse-final):")
print("  most VERSE-INITIAL:", [(names.get(c,c),round(m,2)) for c,m,n,z in stats[:6]])
print("  most VERSE-FINAL:  ", [(names.get(c,c),round(m,2)) for c,m,n,z in stats[-6:]])
nd=sum(1 for c,m,n,z in stats if abs(z)>3)
print("letters with through-book position DRIFT (|z|>3): %d/%d"%(nd,len(stats)))
