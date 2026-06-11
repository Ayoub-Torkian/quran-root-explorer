#!/usr/bin/env python3
# CANDIDATE — refrain architecture. The Qur'an exactly REPEATS some verses (Sūra 55 "fa-bi-
# ayyi ālāʾi..." 31×; Sūra 77 "wayl yawmaʔiḏin..." 10×). Test: are refrains REGULARLY spaced
# (architectural dividers) more than chance? Intrinsic, rasm, exact-match. 3 angles:
# (1) how widespread; (2) spacing regularity vs random placement; (3) do they bisect evenly.
import glob,unicodedata,numpy as np
from collections import Counter,defaultdict
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'
def norm(t):
    t=unicodedata.normalize('NFD',t);t=''.join(c for c in t if not unicodedata.combining(c))
    return ' '.join(''.join(c for c in tok if 'ء'<=c<='ي' and c!='ـ') for tok in t.split()).strip()
sur=defaultdict(list)
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,tx=ln.split('\t',1); su=int(sa.split(':')[0]); sur[su].append(norm(tx))
rng=np.random.default_rng(0)
refrain_suras=[]; cv_real=[]; cv_rand=[]
for su,vs in sur.items():
    n=len(vs); c=Counter(vs)
    # refrain = a verse repeated >=3 times (and not trivially short/empty)
    cand=[(v,k) for v,k in c.items() if k>=3 and len(v)>=6]
    if not cand: continue
    v,k=max(cand,key=lambda t:t[1])
    pos=[i for i,x in enumerate(vs) if x==v]
    gaps=np.diff(pos)
    if len(gaps)<3: continue
    cv=gaps.std()/(gaps.mean()+1e-9)
    # null: place k marks at random positions, CV of gaps
    rc=[]
    for _ in range(500):
        rp=np.sort(rng.choice(n,k,replace=False)); g=np.diff(rp); rc.append(g.std()/(g.mean()+1e-9))
    refrain_suras.append((su,k,n)); cv_real.append(cv); cv_rand.append(np.mean(rc))
cv_real=np.array(cv_real); cv_rand=np.array(cv_rand)
print(f"(1) sūras with a refrain (verse repeated ≥3×): {len(refrain_suras)}")
print(f"    e.g. {[(su,'%dx in %dv'%(k,n)) for su,k,n in sorted(refrain_suras,key=lambda t:-t[1])[:6]]}")
print(f"(2) spacing regularity (CV of gaps; LOWER=more regular):")
print(f"    real refrains   CV={cv_real.mean():.3f}")
print(f"    random placement CV={cv_rand.mean():.3f}")
print(f"    refrains more regular than random in {np.mean(cv_real<cv_rand)*100:.0f}% of sūras; mean Δ={cv_rand.mean()-cv_real.mean():+.3f}")
# paired significance
from numpy import sqrt
d=cv_rand-cv_real; t=d.mean()/(d.std()/sqrt(len(d))+1e-9)
print(f"    paired t≈{t:.1f}  (positive = refrains more regular than chance)")
