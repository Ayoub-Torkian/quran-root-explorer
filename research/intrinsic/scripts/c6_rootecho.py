#!/usr/bin/env python3
# C6 — cognate accusative / root-echo. A root repeated within one verse. Two NEW channels:
# (2) adjacency: the two occurrences are consecutive tokens (verb+maṣdar) above within-verse shuffle.
# (3) verse-final: the echoed root lands on the last (emphasis/rhyme) position above shuffle.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
verses=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.rstrip('\n').split('\t',1);verses.append([x for x in r.split() if x and x!='NA'])
verses=[v for v in verses if len(v)>=3]
rng=np.random.default_rng(0)
def has_adjacent_repeat(v):
    return any(v[i]==v[i+1] for i in range(len(v)-1))
def has_repeat(v):
    return len(set(v))<len(v)
def final_is_repeated(v):
    last=v[-1];return v.count(last)>=2
# (1) repeat-rate baseline
rep=[has_repeat(v) for v in verses]; print("verses with a repeated root: %.1f%% (%d/%d)"%(100*np.mean(rep),sum(rep),len(verses)))
reps=[v for v in verses if has_repeat(v)]
# (2) adjacency among repeat-verses, real vs within-verse shuffle
real_adj=np.mean([has_adjacent_repeat(v) for v in reps])
fl=[]
for _ in range(200):
    fl.append(np.mean([has_adjacent_repeat(list(rng.permutation(v))) for v in reps]))
fl=np.array(fl); print("(2) adjacency of the echo: real %.3f vs within-verse shuffle %.3f  z=%+.1f"%(real_adj,fl.mean(),(real_adj-fl.mean())/fl.std()))
# (3) echoed root at verse-final, real vs shuffle
real_fin=np.mean([final_is_repeated(v) for v in reps])
fl2=[]
for _ in range(200):
    fl2.append(np.mean([final_is_repeated(list(rng.permutation(v))) for v in reps]))
fl2=np.array(fl2); print("(3) echo lands verse-final: real %.3f vs shuffle %.3f  z=%+.1f"%(real_fin,fl2.mean(),(real_fin-fl2.mean())/fl2.std()))
# examples of adjacent echoes
ex=[v for v in reps if has_adjacent_repeat(v)][:6]
print("examples (adjacent root-echo):",[ [x for x in v] for v in ex][:4])
