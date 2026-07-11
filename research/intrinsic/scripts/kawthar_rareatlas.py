# -*- coding: utf-8 -*-
"""PRE-REGISTERED rare-root atlas (internal pilot). Stratify roots by surah-spread s.
k=1 HAPAX layer: count, %, per-sura density, null-test al-Kawthar's density.
k=2 BRIDGE layer: roots in exactly 2 suras -> unique surah-pair welds (shaniʾ is one).
Decision: a sura's hapax-density is a 'hotspot' if >95th pct of a length-matched null."""
import collections, random, statistics as st
random.seed(11)
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
verse_roots={}  # key 's:a' -> list of roots
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line:
        k,rs=line.split('\t',1); verse_roots[k]=[fa(x) for x in rs.split()]
# root -> total count, set of suras, set of verses
cnt=collections.Counter(); rootsuras=collections.defaultdict(set); rootverses=collections.defaultdict(set)
for k,rs in verse_roots.items():
    s=int(k.split(':')[0])
    for r in rs: cnt[r]+=1; rootsuras[r].add(s); rootverses[r].add(k)
Nroots=len(cnt)
hapax={r for r,c in cnt.items() if c==1}          # total count == 1 (true once-only)
spread1={r for r in cnt if len(rootsuras[r])==1}    # appears in exactly 1 sura (may repeat in it)
spread2={r for r in cnt if len(rootsuras[r])==2}
print("="*64); print("RARITY SPECTRUM"); print("="*64)
print(f"distinct roots: {Nroots}")
print(f"k=1 HAPAX (total count==1): {len(hapax)}  = {100*len(hapax)/Nroots:.1f}% of roots")
print(f"roots confined to ONE sura (spread=1): {len(spread1)} = {100*len(spread1)/Nroots:.1f}%")
print(f"roots in exactly TWO suras (spread=2, bridge layer): {len(spread2)} = {100*len(spread2)/Nroots:.1f}%")
sp=collections.Counter(len(rootsuras[r]) for r in cnt)
print("spread histogram (suras: #roots):", {k:sp[k] for k in sorted(sp)[:8]})

print("\n"+"="*64); print("HAPAX LAYER: per-sura singularity density"); print("="*64)
# verses & content-roots per sura
sura_verses=collections.defaultdict(set); sura_hapax=collections.Counter(); sura_roottok=collections.Counter()
for k,rs in verse_roots.items():
    s=int(k.split(':')[0]); sura_verses[s].add(k)
    for r in rs:
        sura_roottok[s]+=1
        if r in hapax: sura_hapax[s]+=1
dens={s: sura_hapax[s]/len(sura_verses[s]) for s in sura_verses}  # hapax per verse
top=sorted(dens, key=lambda s:-dens[s])[:12]
for s in top:
    print(f"  sura {s:3d}: {sura_hapax[s]} hapax / {len(sura_verses[s])} verses = {dens[s]:.2f}/verse  ({'108=al-Kawthar' if s==108 else ''})")
# null test for al-Kawthar: draw 3 random verses, count hapax roots, dens
allk=list(verse_roots)
def draw_dens(nv):
    vs=random.sample(allk,nv); h=sum(1 for v in vs for r in verse_roots[v] if r in hapax); return h/nv
nv108=len(sura_verses[108]); obs=dens[108]
nulls=[draw_dens(nv108) for _ in range(10000)]
pct=100*sum(1 for x in nulls if x<obs)/len(nulls)
print(f"\n  al-Kawthar hapax-density {obs:.2f}/verse vs 3-random-verse null: pct={pct:.1f}, null-mean={st.mean(nulls):.2f}")

print("\n"+"="*64); print("BRIDGE LAYER (spread=2): unique rare welds between sura-pairs"); print("="*64)
pairbridges=collections.defaultdict(list)
for r in spread2:
    a,b=sorted(rootsuras[r]); pairbridges[(a,b)].append(r)
print(f"sura-pairs welded by >=1 spread-2 root: {len(pairbridges)}")
deg=collections.Counter()
for (a,b) in pairbridges: deg[a]+=1; deg[b]+=1
topw=sorted(pairbridges, key=lambda p:-len(pairbridges[p]))[:6]
print("most rare-bridged sura-pairs:")
for p in topw: print(f"  {p}: {len(pairbridges[p])} shared rare roots")
print("108's spread-2 bridges:", {p:[r for r in v] for p,v in pairbridges.items() if 108 in p})
print("top suras by # rare-bridge partners (degree):", deg.most_common(6))

print("\n"+"="*64); print("REFINEMENT: is al-Kawthar special AMONG short suras, or is density a short-sura class trait?"); print("="*64)
# (a) contiguous 3-verse window null (controls for local clustering within a sura)
ordered=sorted(verse_roots, key=lambda k:(int(k.split(':')[0]),int(k.split(':')[1])))
def window_dens():
    i=random.randint(0,len(ordered)-3); ws=ordered[i:i+3]
    h=sum(1 for v in ws for r in verse_roots[v] if r in hapax); return h/3
wn=[window_dens() for _ in range(10000)]
pw=100*sum(1 for x in wn if x<dens[108])/len(wn)
print(f"  contiguous-3-verse-window null: al-Kawthar pct={pw:.1f} (mean={st.mean(wn):.2f})")
# (b) rank among short suras (<=7 verses) by hapax/verse
short=[s for s in sura_verses if len(sura_verses[s])<=7]
rank=sorted(short,key=lambda s:-dens[s])
pos=rank.index(108)+1
print(f"  among {len(short)} short suras (<=7 verses), al-Kawthar ranks #{pos} by hapax/verse")
print("  top short suras:", [(s,round(dens[s],2)) for s in rank[:6]])
# (c) per-verse expected hapax by sura position (Meccan-ish early/late) - quick: corpus mean hapax/verse
allmean=sum(1 for v in verse_roots for r in verse_roots[v] if r in hapax)/len(verse_roots)
print(f"  corpus mean hapax/verse = {allmean:.3f}; al-Kawthar = {dens[108]:.3f} ({dens[108]/allmean:.1f}x)")
