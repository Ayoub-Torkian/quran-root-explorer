#!/usr/bin/env python3
# Positional grammar at SŪRA and BOOK scale (compositional, not syntactic).
# Sūra: mean normalized verse-position-within-sūra per root, spread vs within-sūra verse shuffle.
# Book: mean normalized global verse-position per root, spread vs global verse shuffle.
import glob,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
sura=[];rootsv=[]
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:
        k,r=ln.split('\t',1);sura.append(int(k.split(':')[0]));rootsv.append([x for x in r.split() if x and x!='NA'])
N=len(rootsv);sura=np.array(sura)
bounds={s:(np.where(sura==s)[0][0],np.where(sura==s)[0][-1]+1) for s in np.unique(sura)}
# per-occurrence positions
def collect(posfn):
    pos=collections.defaultdict(list)
    for i in range(N):
        p=posfn(i)
        for r in set(rootsv[i]):pos[r].append(p)
    return pos
def sura_pos(i):
    s=sura[i];a,b=bounds[s];return (i-a)/(b-a-1) if b-a>1 else 0.5
def book_pos(i):return i/(N-1)
rng=np.random.default_rng(0)
def run(name,posfn,shuffle):
    pos=collect(posfn);common=[r for r in pos if len(pos[r])>=30]
    meanp={r:np.mean(pos[r]) for r in common};real=np.std([meanp[r] for r in common])
    sp=[]
    for _ in range(40):
        order=shuffle();p2=collections.defaultdict(list)
        # recompute positions under shuffled verse order
        inv=np.empty(N,dtype=int);inv[order]=np.arange(N)
        for i in range(N):
            # position of verse i is its rank in shuffled order
            pass
        sp.append(None)
    return name,real,common,meanp,pos
# simpler: null = assign each root's occurrences random positions from U(0,1), matched count
def run2(name,posfn):
    pos=collect(posfn);common=[r for r in pos if len(pos[r])>=30]
    meanp={r:np.mean(pos[r]) for r in common};real=np.std([meanp[r] for r in common])
    allp=np.array([p for r in common for p in pos[r]])
    sp=[]
    for _ in range(200):
        sh=rng.permutation(allp);idx=0;mm=[]
        for r in common:
            n=len(pos[r]);mm.append(np.mean(sh[idx:idx+n]));idx+=n
        sp.append(np.std(mm))
    sp=np.array(sp);z=(real-sp.mean())/sp.std()
    nsig=0;early=[];late=[]
    for r in common:
        m=allp.mean();s=allp.std()/np.sqrt(len(pos[r]));zz=(meanp[r]-m)/s
        if abs(zz)>3:
            nsig+=1
            (early if zz<0 else late).append((r,round(meanp[r],2),zz))
    early.sort(key=lambda x:x[2]);late.sort(key=lambda x:-x[2])
    print("%s: spread real %.3f vs shuffle %.3f±%.3f  z=%+.1f ; %d/%d roots positionally biased (|z|>3)"%(name,real,sp.mean(),sp.std(),z,nsig,len(common)))
    print("   EARLY:",[r for r,p,zz in early[:7]],"| LATE:",[r for r,p,zz in late[:7]])
run2("SŪRA-scale (verse within sūra)",sura_pos)
run2("BOOK-scale (verse within Qurān)",book_pos)
