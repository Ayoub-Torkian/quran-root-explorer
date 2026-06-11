#!/usr/bin/env python3
# CANDIDATE — lexical front-loading. Within a sūra, are new (first-in-unit) roots introduced
# EARLY and then elaborated? Measure new-root rate first-half vs second-half; ratio vs random
# same-length windows. 3 angles: (A) half ratio; (B) Heaps exponent within-sūra vs window;
# (C) fraction of sūra's unique roots already seen by 50% of its length.
import glob,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=[x for x in r.split() if x and x!='NA']
sura=[];vr=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);sura.append(int(sa.split(':')[0]));vr.append(roots.get(sa.strip(),[]))
N=len(sura);sura=np.array(sura)
bounds={}
for s in np.unique(sura):
    idx=np.where(sura==s)[0];bounds[s]=(idx[0],idx[-1]+1)
def newroot_halves(a,b):
    seen=set();first=0;second=0;mid=a+(b-a)//2
    for i in range(a,b):
        for r in vr[i]:
            if r not in seen:
                seen.add(r)
                if i<mid:first+=1
                else:second+=1
    return first,second,len(seen)
def frac_seen_by_half(a,b):
    seen=set();mid=a+(b-a)//2;total=set(r for i in range(a,b) for r in vr[i])
    for i in range(a,mid):
        for r in vr[i]:seen.add(r)
    return len(seen)/len(total) if total else 0
rng=np.random.default_rng(1)
real_ratio=[];rand_ratio=[];real_fs=[];rand_fs=[]
for s,(a,b) in bounds.items():
    if b-a<8:continue
    f,sec,u=newroot_halves(a,b)
    if u<4:continue
    real_ratio.append(f/(f+sec));real_fs.append(frac_seen_by_half(a,b))
    L=b-a;rr=[];rf=[]
    for _ in range(40):
        st=rng.integers(0,N-L);f2,s2,u2=newroot_halves(st,st+L)
        if (f2+s2)>0:rr.append(f2/(f2+s2));rf.append(frac_seen_by_half(st,st+L))
    rand_ratio.append(np.mean(rr));rand_fs.append(np.mean(rf))
real_ratio=np.array(real_ratio);rand_ratio=np.array(rand_ratio);real_fs=np.array(real_fs);rand_fs=np.array(rand_fs)
print(f"sūras tested (>=8 verses): {len(real_ratio)}")
print(f"(A) share of new roots in FIRST half: sūra {real_ratio.mean():.3f} vs random-window {rand_ratio.mean():.3f}  "
      f"(sūra front-loads more in {np.mean(real_ratio>rand_ratio)*100:.0f}%; Δ={real_ratio.mean()-rand_ratio.mean():+.3f})")
d=real_ratio-rand_ratio;print(f"    paired t≈{d.mean()/(d.std()/np.sqrt(len(d))+1e-9):.1f}")
print(f"(C) fraction of unit's unique roots seen by 50% length: sūra {real_fs.mean():.3f} vs random {rand_fs.mean():.3f}  "
      f"(higher in {np.mean(real_fs>rand_fs)*100:.0f}%; Δ={real_fs.mean()-rand_fs.mean():+.3f})")
