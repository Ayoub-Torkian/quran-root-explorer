#!/usr/bin/env python3
# FRESH PROBE — Uniform Information Density (UID). Per verse, mean root surprisal
# = avg of -log2 p(root) (p from global root frequency) = information per content word.
# UID predicts LOCAL smoothing: adjacent verses have closer info-density than chance.
# Test |Δsurprisal| between neighbours vs a within-sūra verse-order shuffle. Per-sūra paired.
import glob,numpy as np,collections,math
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=[x for x in r.split() if x and x!='NA']
freq=collections.Counter()
for rs in roots.values():
    for r in rs:freq[r]+=1
tot=sum(freq.values())
def surprisal(rs):
    rs=[r for r in rs if r in freq]
    if not rs:return None
    return np.mean([-math.log2(freq[r]/tot) for r in rs])
sura=[];surp=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);sura.append(int(sa.split(':')[0]));surp.append(surprisal(roots.get(sa.strip(),[])))
sura=np.array(sura)
bys=collections.defaultdict(list)
for i in range(len(sura)):bys[sura[i]].append(surp[i])
def mad(seq):  # mean |Δ| between neighbours, ignoring None
    v=[x for x in seq];d=[abs(v[i]-v[i+1]) for i in range(len(v)-1) if v[i] is not None and v[i+1] is not None]
    return np.mean(d) if d else None
rng=np.random.default_rng(4)
diffs=[];wins=0;n=0
for s,seq in bys.items():
    vals=[x for x in seq if x is not None]
    if len(vals)<8:continue
    real=mad(seq)
    fl=np.mean([mad(list(rng.permutation(vals))) for _ in range(200)])
    diffs.append(real-fl);wins+=(real<fl);n+=1   # real SMOOTHER => real < shuffle
diffs=np.array(diffs);t=diffs.mean()/(diffs.std(ddof=1)/np.sqrt(len(diffs)))
print("sūras tested (>=8 verses): %d" % n)
print("mean(real - shuffle) of neighbour |Δ info-density|: %+.4f  (negative = SMOOTHER than chance)" % diffs.mean())
print("paired t (each sūra one unit): %.1f" % t)
print("sūras smoother than their own shuffle: %d / %d" % (wins,n))
