import unicodedata, numpy as np
from collections import Counter, defaultdict
def skel(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return [w for w in (''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()) if w]
suras=defaultdict(list); ALL=[]
for ln in open('/sessions/gifted-tender-cori/mnt/Quran_Root_Explorer_Web_v1.2/research/two_books_genome/data/quran/quran_arabic_verses.tsv',encoding='utf-8'):
    if '\t' not in ln: continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); w=skel(tx); ALL+=w; suras[su].append(w)
stop=set(w for w,_ in Counter(ALL).most_common(40))
jac=lambda a,b: len(a&b)/len(a|b) if (a|b) else 0.0
def win(verses,idx,k=2):
    s=set()
    for v in verses[idx:idx+k]:
        s|=set(x for x in v if x not in stop)
    return s
OC=[]; OM=[]; rhyme_close=[]; suralist=[]
data={}
for su,verses in suras.items():
    if len(verses)<6: continue
    O=win(verses,0); C=win(verses,len(verses)-2); m=len(verses)//2; M=win(verses,m)
    OC.append(jac(O,C)); OM.append(jac(O,M)); suralist.append(su); data[su]=(O,C)
    f0=verses[0][-1][-1] if verses[0] and verses[0][-1] else ''
    fL=verses[-1][-1][-1] if verses[-1] and verses[-1][-1] else ''
    rhyme_close.append(1.0 if f0==fL else 0.0)
OC=np.array(OC); OM=np.array(OM)
# cross-sura floor: O of one vs C of another
rng=np.random.default_rng(0); sl=list(data)
cross=[]
for _ in range(5000):
    a,b=rng.choice(sl,2,replace=False); cross.append(jac(data[a][0],data[b][1]))
cross=np.array(cross)
d=(OC.mean()-OM.mean())/np.sqrt((OC.var()+OM.var())/2)
print(f"suras tested (>=6 verses): {len(OC)}")
print(f"opening~closing  Jaccard mean = {OC.mean():.4f}")
print(f"opening~middle   Jaccard mean = {OM.mean():.4f}   (paired d={d:.2f}, OC>OM in {100*np.mean(OC>OM):.0f}% of suras)")
print(f"cross-sura floor (open_A~close_B) = {cross.mean():.4f}")
print(f"OC vs floor: ratio={OC.mean()/cross.mean():.2f}x  z={(OC.mean()-cross.mean())/cross.std():.1f}")
# permutation test on paired OC-OM
diff=OC-OM; obs=diff.mean()
perm=np.array([ (rng.permutation([1,-1]*len(diff))[:len(diff)]*np.abs(diff)).mean() for _ in range(2000)])
print(f"paired OC>OM permutation p = {(np.sum(perm>=obs)+1)/2001:.4f}")
print(f"rhyme closure (last verse final letter == first verse): {100*np.mean(rhyme_close):.0f}% of suras")
