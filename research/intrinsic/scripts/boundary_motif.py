#!/usr/bin/env python3
# BOUNDARY MOTIF (splice-site / promoter analog). Build a position-specific letter logo for
# the FIRST letters of sūras (the 'start') and compare conservation (information content, bits)
# to ordinary (non-first) verse-starts. A real motif = higher per-position info at the boundary.
import glob,unicodedata,collections,math,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
AR=set(chr(c) for c in range(0x621,0x64B)); skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
rows=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); s,a=sa.split(':'); rows.append((int(s),int(a),skel(tx.strip())))
# background letter freq
allc=collections.Counter(ch for _,_,t in rows for ch in t); tot=sum(allc.values())
bg={c:allc[c]/tot for c in allc}
K=5
sura_starts=[t[:K] for s,a,t in rows if a==1 and len(t)>=K]
other_starts=[t[:K] for s,a,t in rows if a>1 and len(t)>=K]
rng=np.random.default_rng(0); other_sample=[other_starts[i] for i in rng.choice(len(other_starts),len(sura_starts),replace=False)]
def info_per_pos(seqs):
    out=[]
    for p in range(K):
        col=collections.Counter(s[p] for s in seqs); n=sum(col.values())
        ic=sum((col[c]/n)*math.log2((col[c]/n)/bg.get(c,1e-9)) for c in col)  # KL info in bits
        cons=col.most_common(1)[0]; out.append((ic,cons[0],100*cons[1]/n))
    return out
S=info_per_pos(sura_starts); O=info_per_pos(other_sample)
print("n sūra-starts=%d (vs %d matched random verse-starts)"%(len(sura_starts),len(other_sample)))
print("pos | sūra-start info(bits) consensus%  | random-start info | lift")
for p in range(K):
    print("  %d | %.2f bits  '%s' %.0f%%        | %.2f bits  '%s' %.0f%%   | %.1fx"%(p+1,S[p][0],S[p][1],S[p][2],O[p][0],O[p][1],O[p][2],S[p][0]/(O[p][0]+1e-9)))
print("total motif info: sūra-start %.2f bits vs random %.2f bits"%(sum(x[0] for x in S),sum(x[0] for x in O)))
