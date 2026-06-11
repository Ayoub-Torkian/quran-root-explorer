#!/usr/bin/env python3
# C9 CONTROL — does inter-sūra continuity survive (1) length-ordering and (2) muqaṭṭaʿāt grouping?
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
S=sorted(bys)
bag={s:set().union(*bys[s]) for s in S}
length={s:len(bys[s]) for s in S}                       # sūra length in verses
def jac(a,b):
    u=bag[a]|bag[b];return len(bag[a]&bag[b])/len(u) if u else 0
def adj(order,mask=None):
    v=[jac(order[i],order[i+1]) for i in range(len(order)-1)
       if (mask is None or (mask(order[i]) and mask(order[i+1])))]
    return np.mean(v),len(v)
rng=np.random.default_rng(11)
realA,_=adj(S)
# (1) LENGTH-MATCHED null: keep the muṣḥaf's length-bucket sequence, randomize sūra identity within bucket
B=12; ranks=sorted(S,key=lambda s:length[s]); bucket={s:(ranks.index(s)*B)//len(S) for s in S}
canbk=[bucket[s] for s in S]
members=collections.defaultdict(list)
for s in S:members[bucket[s]].append(s)
def length_matched_order():
    pools={b:list(rng.permutation(members[b])) for b in members}
    return [pools[canbk[i]].pop() for i in range(len(canbk))]
flL=np.array([adj(length_matched_order())[0] for _ in range(2000)])
# plain shuffle for reference
flR=np.array([adj(list(rng.permutation(S)))[0] for _ in range(2000)])
print("(A) whole-sūra neighbour Jaccard:")
print("    canonical                         %.3f" % realA)
print("    plain sūra-order shuffle          %.3f ± %.3f  -> z=%+.1f" % (flR.mean(),flR.std(),(realA-flR.mean())/flR.std()))
print("    LENGTH-MATCHED shuffle (control)  %.3f ± %.3f  -> z=%+.1f  (perm p: %d/2000 >= real)" %
      (flL.mean(),flL.std(),(realA-flL.mean())/flL.std(),int((flL>=realA).sum())))
# (2) muqaṭṭaʿāt grouping: exclude adjacencies where both sūras carry opening letters
MUQ={2,3,7,10,11,12,13,14,15,19,20,26,27,28,29,30,31,32,36,38,40,41,42,43,44,45,46,50,68}
realM,nM=adj(S,mask=lambda s:s not in MUQ)
flLM=np.array([adj(length_matched_order(),mask=lambda s:s not in MUQ)[0] for _ in range(1500)])
print("\n(B) excluding muqaṭṭaʿāt sūras (%d adjacencies of non-muq pairs):" % nM)
print("    canonical (non-muq)               %.3f" % realM)
print("    length-matched shuffle (non-muq)  %.3f ± %.3f  -> z=%+.1f  (p: %d/1500)" %
      (flLM.mean(),flLM.std(),(realM-flLM.mean())/flLM.std(),int((flLM>=realM).sum())))
