#!/usr/bin/env python3
# Fresh probe — BOOK-LEVEL RING. Are symmetric sūra pairs (k, 115-k) more root-similar than
# a shuffle of sūra order? Tests a chiastic macro-structure across the 114-chapter sequence.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
bys=collections.defaultdict(list)
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);bys[int(sa.split(':')[0])].append(roots.get(sa.strip(),set()))
S=sorted(bys); bag={s:set().union(*bys[s]) for s in S}; length={s:len(bys[s]) for s in S}
def jac(a,b):
    u=bag[a]|bag[b];return len(bag[a]&bag[b])/len(u) if u else 0
pairs=[(S[i],S[len(S)-1-i]) for i in range(len(S)//2)]
real=np.mean([jac(a,b) for a,b in pairs])
rng=np.random.default_rng(0)
# null: random pairing of sūras (shuffle which sūra mirrors which)
fl=[]
for _ in range(3000):
    p=list(rng.permutation(S));fl.append(np.mean([jac(p[2*i],p[2*i+1]) for i in range(len(p)//2)]))
fl=np.array(fl)
print("book-level ring (sūra k ↔ 115-k) mean root-Jaccard: %.3f" % real)
print("random sūra-pairing null: %.3f ± %.3f  -> z=%+.1f  (perm p: %d/3000 >= real)" % (fl.mean(),fl.std(),(real-fl.mean())/fl.std(),int((fl>=real).sum())))
# length-matched? symmetric pairs are length-mismatched (long↔short); report the famous pair
print("Fātiḥa(1)↔Nās(114) Jaccard: %.3f ; Baqara(2)↔Falaq(113): %.3f" % (jac(1,114),jac(2,113)))
