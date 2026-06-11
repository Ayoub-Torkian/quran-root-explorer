#!/usr/bin/env python3
# C8 control: does canonical order still lead on meaning-continuity once the rhyme-bearing
# (final) root is removed from every verse? Compare adjacent root-sharing across arrangements
# using roots MINUS the last root.
import glob,unicodedata,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
ordroots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);ordroots[k]=[x for x in r.split() if x and x!='NA']
rh=[];full=[];minus=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1);k=sa.strip();sk=skel(tx.strip());tr=ordroots.get(k,[])
    rh.append(sk[-2:] if len(sk)>=2 else sk);full.append(set(tr));minus.append(set(tr[:-1]))
N=len(full);rng=np.random.default_rng(0)
def adj(order,field):
    return np.mean([1 if field[order[i]]&field[order[i+1]] else 0 for i in range(N-1)])
canon=list(range(N)); byrh=sorted(range(N),key=lambda i:rh[i])
print("adjacent root-sharing — FULL verse roots:")
print("  canonical %.3f   by-rhyme %.3f" % (adj(canon,full),adj(byrh,full)))
print("adjacent root-sharing — MINUS the rhyme-bearing word (the control):")
cF=adj(canon,minus); bF=adj(byrh,minus)
rnd=np.mean([adj(list(rng.permutation(N)),minus) for _ in range(200)])
print("  canonical %.3f   by-rhyme %.3f   random %.3f" % (cF,bF,rnd))
print("  canonical lead over by-rhyme: %+.3f   (canonical %.0f%% above random margin)" % (cF-bF, 100*(cF-bF)/(cF-rnd+1e-9)))
