#!/usr/bin/env python3
# Drive C10 (UID) toward promotion: 2 more modalities.
# (2) LENGTH-MATCHED control: is the smoothing an artifact of verse length? Shuffle within
#     length-bands (so neighbour length-gaps preserved) and re-test.
# (3) AUTOCORRELATION: does the surprisal series have positive lag-1 autocorrelation vs shuffle?
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
def surp(rs):
    rs=[r for r in rs if r in freq]
    return np.mean([-math.log2(freq[r]/tot) for r in rs]) if rs else None
sura=[];S=[];LN=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);sura.append(int(sa.split(':')[0]));rs=roots.get(sa.strip(),[]);S.append(surp(rs));LN.append(len(rs))
sura=np.array(sura)
bys=collections.defaultdict(list)
for i in range(len(sura)):bys[sura[i]].append((S[i],LN[i]))
rng=np.random.default_rng(8)
def madv(vals):
    d=[abs(vals[i]-vals[i+1]) for i in range(len(vals)-1)]
    return np.mean(d) if d else None
# (2) length-matched: shuffle within length terciles inside each sūra
d2=[];w2=0;n2=0
for s,seq in bys.items():
    vals=[v for v,l in seq if v is not None];lens=[l for v,l in seq if v is not None]
    if len(vals)<9:continue
    real=madv(vals)
    order=np.argsort(lens);band={order[i]:(i*3)//len(order) for i in range(len(order))}
    mem=collections.defaultdict(list)
    for i,b in band.items():mem[b].append(i)
    fl=[]
    for _ in range(200):
        pools={b:list(rng.permutation(mem[b])) for b in mem};idx=[pools[band[i]].pop() for i in range(len(vals))]
        fl.append(madv([vals[j] for j in idx]))
    d2.append(real-np.mean(fl));w2+=(real<np.mean(fl));n2+=1
d2=np.array(d2);t2=d2.mean()/(d2.std(ddof=1)/np.sqrt(len(d2)))
print("(2) LENGTH-MATCHED control: mean(real-shuffle) %+.4f  paired t=%.1f  smoother in %d/%d sūras" % (d2.mean(),t2,w2,n2))
# (3) lag-1 autocorrelation of surprisal vs within-sūra shuffle
d3=[];w3=0;n3=0
for s,seq in bys.items():
    vals=np.array([v for v,l in seq if v is not None])
    if len(vals)<10:continue
    def ac1(x):
        x=x-x.mean();d=np.dot(x,x);return np.dot(x[:-1],x[1:])/d if d>0 else 0
    real=ac1(vals);fl=np.mean([ac1(rng.permutation(vals)) for _ in range(200)])
    d3.append(real-fl);w3+=(real>fl);n3+=1
d3=np.array(d3);t3=d3.mean()/(d3.std(ddof=1)/np.sqrt(len(d3)))
print("(3) lag-1 AUTOCORRELATION: mean(real-shuffle) %+.4f  paired t=%.1f  positive in %d/%d sūras" % (d3.mean(),t3,w3,n3))
