# -*- coding: utf-8 -*-
"""Which LONG surah most elaborates the SHORT surah 108? Rarity-weighted, length-normalized. Unicode-safe."""
import json, csv, collections, math
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
names={}
for d in csv.DictReader(open(f"{R}/exports/surah_profile.csv",encoding='utf-8-sig')):
    pass
# per-ayah roots
ay_roots={}; sur_ayahs=collections.defaultdict(list); sur_roots=collections.defaultdict(collections.Counter)
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' not in line: continue
    k,rs=line.split('\t',1); rs=[fa(x) for x in rs.split()]
    ay_roots[k]=rs; s=int(k.split(':')[0]); sur_ayahs[s].append(k)
    for r in rs: sur_roots[s][r]+=1
# idf by ayah
N=len(ay_roots); ndoc=collections.Counter()
for k,rs in ay_roots.items():
    for r in set(rs): ndoc[r]+=1
idf=lambda r: math.log(N/ndoc[r]) if ndoc.get(r) else 0

S108=['عطو','کثر','صلو','ربب','نحر','شنء','بتر']
SAC=['نسک','ذبح','هدی','قرب','بدن']      # sacrifice field (interprets naHr)
SEV=['قطع','دبر','هلک','صرم','جذذ']      # severance field (interprets abtar)
INTERP = S108 + SAC + SEV
TR={'ا':'ʾ','ب':'b','ت':'t','ث':'th','ج':'j','ح':'ḥ','خ':'kh','د':'d','ذ':'dh','ر':'r','ز':'z','س':'s','ش':'sh','ص':'ṣ','ض':'ḍ','ط':'ṭ','ظ':'ẓ','ع':'ʿ','غ':'gh','ف':'f','ق':'q','ک':'k','ل':'l','م':'m','ن':'n','ه':'h','و':'w','ی':'y','ء':'ʾ'}
tr=lambda r:'-'.join(TR.get(c,c) for c in r)

# A. which surahs share the rare hate-root شنء?
print("surahs containing شنء (shāniʾ/shanaʾān):", sorted(set(int(k.split(':')[0]) for k,rs in ay_roots.items() if 'شنء' in rs)))

# B. elaboration score: sum idf(r)*count(r in surah) over interpreting set, normalized by surah #ayahs
score={}
for s in sur_roots:
    if s==108: continue
    raw=sum(idf(r)*sur_roots[s].get(r,0) for r in INTERP)
    nay=len(sur_ayahs[s])
    score[s]=dict(raw=raw, per_ayah=raw/nay, nay=nay)
rank=sorted(score, key=lambda s:-score[s]['per_ayah'])
print("\n== TOP surahs elaborating 108 (idf-weighted interpreting roots, per-ayah normalized) ==")
for s in rank[:10]:
    present=[tr(r) for r in INTERP if sur_roots[s].get(r,0)]
    print(f"  Sūra {s:3d}  per-ayah={score[s]['per_ayah']:.3f}  raw={score[s]['raw']:.1f}  (n={score[s]['nay']})  interp-roots: {', '.join(present[:12])}")
print("\nrank of Sūra 5 (al-Māʾida):", rank.index(5)+1, "of", len(rank), "| per-ayah", round(score[5]['per_ayah'],3), "raw", round(score[5]['raw'],1))

# C. what in al-Māʾida drives it? per-root contribution
print("\n== al-Māʾida (5): which interpreting roots contribute (idf*count) ==")
contrib=sorted(((idf(r)*sur_roots[5].get(r,0), r, sur_roots[5].get(r,0)) for r in INTERP if sur_roots[5].get(r,0)), reverse=True)
for v,r,c in contrib: print(f"   {tr(r):8s} count={c:2d}  idf={idf(r):.2f}  contribution={v:.2f}")

# D. the specific ayahs in al-Māʾida carrying 108's distinctive roots
print("\n== specific al-Māʾida ayahs carrying 108's distinctive roots (شنء + sacrifice field) ==")
targ=set(['شنء']+SAC+['صلو','نسک'])
for k in sur_ayahs[5]:
    hit=[tr(r) for r in set(ay_roots[k]) if r in targ]
    if hit:
        print(f"   {k}  [{', '.join(hit)}]  {m.get(k,{}).get('en','')[:90]}")
