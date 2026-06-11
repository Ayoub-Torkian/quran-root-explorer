#!/usr/bin/env python3
# CHIRALITY: (1) sequence irreversibility of the root stream — triple asymmetry n(ABC) vs n(CBA);
# (2) HOMOCHIRALITY: per-sūra polarity (closing lighter than opening, in root-surprisal) — is the
# SIGN the same across sūras (homochiral) or mixed (racemic)?
import glob,collections,math,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=[x for x in r.split() if x and x!='NA']
# (1) irreversibility on the global root stream
stream=[];bys=collections.defaultdict(list)
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);rs=roots.get(sa.strip(),[]);stream+=rs;bys[int(sa.split(':')[0])].append(rs)
tri=collections.Counter(tuple(stream[i:i+3]) for i in range(len(stream)-2))
asym=0;sym=0
for t,c in tri.items():
    rev=t[::-1]
    if t==rev:continue
    cr=tri.get(rev,0); asym+=abs(c-cr); sym+=c+cr
print("(1) sequence irreversibility: triple asymmetry index = %.3f (0=fully reversible/achiral, 1=fully chiral)"%(asym/sym if sym else 0))
# most directionally-fixed triples (occur forward but ~never reversed)
chiral=sorted([(t,c,tri.get(t[::-1],0)) for t,c in tri.items() if c>=15 and t!=t[::-1]],key=lambda x:-(x[1]-x[2]))[:5]
print("   strongly chiral triples (forward count vs reversed):")
for t,c,cr in chiral: print("     %s  fwd=%d rev=%d"%('→'.join(t),c,cr))
# (2) homochirality: per-sūra surprisal polarity (first third vs last third)
freq=collections.Counter(stream);tot=len(stream)
def sur(rs):
    rs=[r for r in rs if r in freq];return np.mean([-math.log2(freq[r]/tot) for r in rs]) if rs else None
pol=[]
for s,vs in bys.items():
    if len(vs)<9:continue
    k=len(vs)//3
    first=[sur(v) for v in vs[:k]];last=[sur(v) for v in vs[-k:]]
    f=np.nanmean([x for x in first if x is not None]);l=np.nanmean([x for x in last if x is not None])
    if not(np.isnan(f) or np.isnan(l)):pol.append(l-f)  # negative = closing lighter
pol=np.array(pol)
same=np.mean(pol<0)
print("(2) homochirality: sūras whose CLOSING is lighter than opening (one handedness): %.0f%% (%d/%d)  mean polarity %+.3f"%(100*same,int((pol<0).sum()),len(pol),pol.mean()))
