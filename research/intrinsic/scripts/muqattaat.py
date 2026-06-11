#!/usr/bin/env python3
# CANDIDATE — muqaṭṭaʿāt: are a sūra's opening disjoint letters over-represented in its OWN
# text? Intrinsic, rasm, letter-scale. Tested 3 ways: (1) z-score vs corpus baseline,
# (2) vs a random-letter null (real letters vs matched random letters), (3) rank of the
# disjoint letter among the sūra's letters. The text against itself.
import glob,unicodedata,numpy as np
from collections import Counter
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
def norm(s):
    s=unicodedata.normalize('NFD',s); return ''.join(c for c in s if 'ء'<=c<='ي' and c!='ـ')
MQ={2:'الم',3:'الم',7:'المص',10:'الر',11:'الر',12:'الر',13:'المر',14:'الر',15:'الر',19:'كهيعص',20:'طه',
    26:'طسم',27:'طس',28:'طسم',29:'الم',30:'الم',31:'الم',32:'الم',36:'يس',38:'ص',40:'حم',41:'حم',
    42:'حمعسق',43:'حم',44:'حم',45:'حم',46:'حم',50:'ق',68:'ن'}
MQ={k:list(dict.fromkeys(norm(v))) for k,v in MQ.items()}
# per-sura letter strings (EXCLUDING the opening disjoint 'verse' = ayah 1 of MQ suras)
body=Counter(); persura=Counter(); suratext={}; corpus=Counter()
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su,ay=map(int,sa.split(':')); s=norm(tx)
    if su in MQ and ay==1: continue        # skip the opening letters themselves
    suratext[su]=suratext.get(su,'')+s; corpus.update(s)
TOT=sum(corpus.values()); pc={c:corpus[c]/TOT for c in corpus}
alpha=list(corpus.keys())
rng=np.random.default_rng(0)
zs=[]; real_over=[]; rand_over=[]; ranks=[]
for su,letters in MQ.items():
    t=suratext.get(su,''); n=len(t); cnt=Counter(t)
    if n<50: continue
    # sura letter ranking
    order=[c for c,_ in cnt.most_common()]
    for d in letters:
        p=pc.get(d,1e-9); obs=cnt.get(d,0); exp=n*p
        z=(obs-exp)/np.sqrt(n*p*(1-p)+1e-9)
        zs.append(z); real_over.append(obs/n/p if p>0 else 0)
        ranks.append((order.index(d)+1) if d in order else len(alpha))
    # random-letter null: pick len(letters) random letters (corpus-freq weighted), their over-rep
    rl=rng.choice(alpha,len(letters),replace=False,p=[pc[c] for c in alpha])
    for d in rl:
        p=pc.get(d,1e-9); obs=cnt.get(d,0); rand_over.append(obs/n/p if p>0 else 0)
zs=np.array(zs); real_over=np.array(real_over); rand_over=np.array(rand_over); ranks=np.array(ranks)
print(f"muqaṭṭaʿāt: {len(MQ)} sūras, {len(zs)} (sūra,letter) pairs")
print(f"(1) vs CORPUS baseline: mean z={zs.mean():.2f}  median over-rep ratio={np.median(real_over):.2f}×  share over-rep(>1)={np.mean(real_over>1)*100:.0f}%")
print(f"(2) vs RANDOM-letter null: real over-rep={real_over.mean():.3f}  random={rand_over.mean():.3f}  (real>random if >)")
from numpy import mean
# permutation p: is real mean over-rep > random?
diff=real_over.mean()-rand_over.mean()
print(f"    difference real-random = {diff:+.3f}")
print(f"(3) RANK of disjoint letter among sūra's letters: median rank={np.median(ranks):.0f} of {len(alpha)}  (top-5 share={np.mean(ranks<=5)*100:.0f}%)")
