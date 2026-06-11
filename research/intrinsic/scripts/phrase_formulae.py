#!/usr/bin/env python3
# Fresh probe — FORMULAIC PHRASES. Does the Qur'ān reuse fixed root-SEQUENCES (bigrams/trigrams)
# far above a unigram-matched shuffle? Measures repeat-mass of n-grams vs a null that keeps the
# root-frequency distribution but destroys order (shuffle the whole root stream).
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
stream=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        _,r=ln.split('\t',1);stream+= [x for x in r.split() if x and x!='NA']
stream=np.array(stream,dtype=object); N=len(stream)
def ngram_repeatmass(seq,n):
    c=collections.Counter(tuple(seq[i:i+n]) for i in range(len(seq)-n+1))
    tot=sum(c.values()); rep=sum(v for v in c.values() if v>=2)
    return rep/tot, c
rng=np.random.default_rng(0)
for n in (2,3):
    real,c=ngram_repeatmass(stream,n)
    fl=[]
    for _ in range(80):
        fl.append(ngram_repeatmass(rng.permutation(stream),n)[0])
    fl=np.array(fl); z=(real-fl.mean())/fl.std()
    print("%d-gram repeat-mass: real %.3f vs shuffle %.3f±%.3f  z=%+.1f  lift=%.2fx" % (n,real,fl.mean(),fl.std(),z,real/fl.mean()))
    if n==2:
        print("   top recurring root-bigrams:", [(' '.join(k),v) for k,v in c.most_common(6)])
