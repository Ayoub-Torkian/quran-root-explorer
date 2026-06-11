#!/usr/bin/env python3
# EXPLICIT VERIFICATION: physically reorder verses within sūras and show neighbour cohesion collapse.
import glob,numpy as np
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=set(x for x in r.split() if x and x!='NA')
sura=[];vr=[];ref=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,_=ln.split('\t',1);sura.append(int(sa.split(':')[0]));vr.append(roots.get(sa.strip(),set()));ref.append(sa.strip())
sura=np.array(sura)
bnd={s:(np.where(sura==s)[0][0],np.where(sura==s)[0][-1]+1) for s in np.unique(sura)}
def adj_share(order):  # order = list of verse indices in sequence
    return np.mean([1 if vr[order[k]]&vr[order[k+1]] else 0 for k in range(len(order)-1)])
alls=[s for s in np.unique(sura) if bnd[s][1]-bnd[s][0]>=10]
# REAL sequence (canonical)
real_pairs=[(i,i+1) for s in alls for i in range(bnd[s][0],bnd[s][1]-1)]
real=np.mean([1 if vr[i]&vr[j] else 0 for i,j in real_pairs])
# REORDER: 5 independent full reshuffles of verse order within each sūra
rng=np.random.default_rng(42)
print("Canonical (real) neighbour-sharing: %.3f" % real)
print("After physically reordering verses within each sūra:")
vals=[]
for t in range(5):
    acc=[]
    for s in alls:
        a,b=bnd[s];p=list(rng.permutation(range(a,b)));acc.append(adj_share(p))
    v=np.mean(acc);vals.append(v);print("   reshuffle #%d: %.3f" % (t+1,v))
print("   reshuffle mean: %.3f   -> drop of %.3f (%.0f%% of the signal above floor)" %
      (np.mean(vals),real-np.mean(vals),100*(real-np.mean(vals))/(real-0.389)))
# CONCRETE EXAMPLE: one sūra, canonical vs one reshuffle, show which neighbours share
s=12  # Yusuf
a,b=bnd[s]
print("\nWorked example — Sūra %d (%d verses):" % (s,b-a))
can=list(range(a,b))
print("  canonical neighbour-sharing: %.3f" % adj_share(can))
sh=list(rng.permutation(range(a,b)))
print("  one reshuffle:               %.3f" % adj_share(sh))
# show first 6 canonical adjacent pairs and whether they share a root
print("  first canonical adjacencies (share? / shared roots):")
for i in range(a,a+6):
    sr=vr[i]&vr[i+1]
    print("    %s↔%s : %s  %s" % (ref[i],ref[i+1],'YES' if sr else 'no ',' '.join(list(sr)[:4])))
