#!/usr/bin/env python3
# ARRANGEMENT SCANNER — re-sort the 6236-verse stream by different RULES and measure structure.
# Each rule optimizes its own axis; the question is which arrangement carries ROOT-cohesion
# (adjacent verses sharing word-roots) — the semantic-continuity signal. Is canonical privileged?
import glob,unicodedata,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
AR=set(chr(c) for c in range(0x621,0x64B))
skel=lambda s:''.join(c for c in unicodedata.normalize('NFD',s) if c in AR)
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
vr=[];rh=[];ln_=[];pos=[];fr=[]
i=0
for line in open(DATA,encoding='utf-8'):
    if '\t' not in line:continue
    sa,tx=line.split('\t',1);k=sa.strip();sk=skel(tx.strip())
    vr.append(roots.get(k,set()));rh.append(sk[-2:] if len(sk)>=2 else sk);ln_.append(len(sk))
    pos.append(int(k.split(':')[1]));fr.append(min(roots.get(k,{'zzz'})) if roots.get(k) else 'zzz')
N=len(vr)
def metrics(order):
    rs=np.mean([1 if vr[order[i]]&vr[order[i+1]] else 0 for i in range(N-1)])           # root-share
    rm=np.mean([1 if rh[order[i]]==rh[order[i+1]] else 0 for i in range(N-1)])           # same-rhyme
    dl=np.mean([abs(ln_[order[i]]-ln_[order[i+1]]) for i in range(N-1)])                 # |Δ length|
    return rs,rm,dl
arr={}
arr['canonical']=list(range(N))
arr['reverse']=list(range(N))[::-1]
arr['by length']=sorted(range(N),key=lambda i:ln_[i])
arr['by rhyme']=sorted(range(N),key=lambda i:rh[i])
arr['by first-root']=sorted(range(N),key=lambda i:fr[i])
arr['transpose (pos,sūra)']=sorted(range(N),key=lambda i:(pos[i],i))
rng=np.random.default_rng(0)
randm=np.array([metrics(list(rng.permutation(N))) for _ in range(50)]).mean(0)
print("%-22s | root-share | same-rhyme | |Δlen|" % "ARRANGEMENT")
print("-"*60)
rows=[]
for name,o in arr.items():
    rs,rm,dl=metrics(o);rows.append((name,rs,rm,dl))
    print("%-22s |   %.3f    |   %.3f    |  %.2f" % (name,rs,rm,dl))
print("%-22s |   %.3f    |   %.3f    |  %.2f" % ("random (mean)",*randm))
print("\nRanked by ROOT-cohesion (the meaning-continuity axis):")
for name,rs,rm,dl in sorted(rows,key=lambda x:-x[1]):
    print("  %-22s %.3f" % (name,rs))
