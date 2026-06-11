#!/usr/bin/env python3
# READING-FRAME test (codon-periodicity analog). Is there a discrete short PERIOD in the
# rasm letter stream and the root stream — a 'frame' like DNA's 3-bp codon period?
# Method: autocorrelation of a letter/root indicator at lags 1..18 vs shuffle; look for peaks.
import glob,unicodedata,collections,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
# letter stream (whole Qurān)
letters=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' in ln: letters+= list(skel(ln.split('\t',1)[1].strip()))
# map each letter to its global frequency rank -> numeric signal; test autocorr of 'is long-vowel' indicator
longv=np.array([1.0 if c in ('ا','و','ي') else 0.0 for c in letters])
def acf(x,maxlag):
    x=x-x.mean(); d=np.dot(x,x)
    return np.array([np.dot(x[:len(x)-k],x[k:])/d for k in range(1,maxlag+1)])
real=acf(longv,18)
rng=np.random.default_rng(0)
fl=np.array([acf(rng.permutation(longv),18) for _ in range(50)])
z=(real-fl.mean(0))/(fl.std(0)+1e-9)
print("LETTER stream — autocorrelation of long-vowel indicator (ا/و/ي), lag : z-vs-shuffle")
for k in range(18):
    bar='#'*int(max(0,z[k])/3)
    print("  lag %2d : z=%+6.1f %s"%(k+1,z[k],bar))
# root stream: autocorr of root-length (consonant count) — any period?
roots=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln: roots+= [len(x) for x in ln.split('\t',1)[1].split() if x and x!='NA']
roots=np.array(roots,dtype=float)
rr=acf(roots,12); fr=np.array([acf(rng.permutation(roots),12) for _ in range(50)]); zr=(rr-fr.mean(0))/(fr.std(0)+1e-9)
print("\nROOT stream — autocorrelation of root-length, lag : z")
print("  "+" ".join("L%d:%+.0f"%(k+1,zr[k]) for k in range(12)))
