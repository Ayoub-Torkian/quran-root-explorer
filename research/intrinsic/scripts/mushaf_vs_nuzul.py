#!/usr/bin/env python3
# Does the canonical MUṢḤAF order carry more inter-sūra lexical continuity than the
# chronological NUZŪL (revelation) order? Both are real orderings of the same 114 sūras.
# Compared against the same length-matched null. Neutral intrinsic measurement.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
# Egyptian-standard revelation rank for each sūra (sūra -> nth revealed)
NUZUL={1:5,2:87,3:89,4:92,5:112,6:55,7:39,8:88,9:113,10:51,11:52,12:53,13:96,14:72,15:54,16:70,17:50,18:69,19:44,20:45,21:73,22:103,23:74,24:102,25:42,26:47,27:48,28:49,29:85,30:84,31:57,32:75,33:90,34:58,35:43,36:41,37:56,38:38,39:59,40:60,41:61,42:62,43:63,44:64,45:65,46:66,47:95,48:111,49:106,50:34,51:67,52:76,53:23,54:37,55:97,56:46,57:94,58:105,59:101,60:91,61:109,62:110,63:104,64:108,65:99,66:107,67:77,68:2,69:78,70:79,71:71,72:40,73:3,74:4,75:31,76:98,77:33,78:80,79:81,80:24,81:7,82:82,83:86,84:83,85:27,86:36,87:8,88:68,89:10,90:35,91:26,92:9,93:11,94:12,95:28,96:1,97:25,98:100,99:93,100:14,101:30,102:16,103:13,104:32,105:19,106:29,107:17,108:15,109:18,110:114,111:6,112:22,113:20,114:21}
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
def adj(order):return np.mean([jac(order[i],order[i+1]) for i in range(len(order)-1)])
mushaf=S[:]                                   # 1..114
nuzul=sorted(S,key=lambda s:NUZUL[s])         # by revelation rank
rng=np.random.default_rng(3)
# length-matched null (same construction as L24)
B=12; ranks=sorted(S,key=lambda s:length[s]); bucket={s:(ranks.index(s)*B)//len(S) for s in S}
members=collections.defaultdict(list)
for s in S:members[bucket[s]].append(s)
def lmatch(order):
    cb=[bucket[s] for s in order];pools={b:list(rng.permutation(members[b])) for b in members}
    return [pools[cb[i]].pop() for i in range(len(cb))]
flo=np.array([adj(lmatch(mushaf)) for _ in range(2000)])
print("inter-sūra neighbour root-Jaccard (higher = more lexical continuity between adjacent chapters):")
print("  MUṢḤAF (canonical) order : %.3f   z vs length-matched null = %+.1f" % (adj(mushaf),(adj(mushaf)-flo.mean())/flo.std()))
print("  NUZŪL (revelation) order : %.3f   z vs length-matched null = %+.1f" % (adj(nuzul),(adj(nuzul)-flo.mean())/flo.std()))
print("  length-matched null mean : %.3f ± %.3f" % (flo.mean(),flo.std()))
print("  random sūra-order        : %.3f" % np.mean([adj(list(rng.permutation(S))) for _ in range(500)]))
