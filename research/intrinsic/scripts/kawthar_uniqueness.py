# -*- coding: utf-8 -*-
"""LEXICAL DISTINCTIVENESS as a positive attribute (not 'isolation'):
a hapax is DISTINCT if its host verse's RARE (non-ubiquitous) context is shared with no other hapax.
Study the attribute across the corpus; robustness over thresholds; where al-Kawthar's pair sits. No revelation-order."""
import collections, math, itertools
import networkx as nx
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')
vr={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); vr[k]=[fa(x) for x in rs.split()]
Nv=len(vr); df=collections.Counter()
for rs in vr.values():
    for r in set(rs): df[r]+=1
cnt=collections.Counter(r for rs in vr.values() for r in rs)
idf=lambda r: math.log(Nv/df[r])
hapax={r for r,c in cnt.items() if c==1}
host={r:k for k,rs in vr.items() for r in rs if r in hapax}
def graph(UBIQ,THRESH):
    ubiq={r for r in df if df[r]>UBIQ}
    ctx={h:set(r for r in vr[host[h]] if r not in ubiq and r not in hapax) for h in hapax}
    G=nx.Graph(); G.add_nodes_from(hapax)
    for h1,h2 in itertools.combinations(hapax,2):
        sh=ctx[h1]&ctx[h2]
        if sh and sum(idf(r) for r in sh)>=THRESH: G.add_edge(h1,h2)
    return G
print("DISTINCTIVE (solitary) hapax = share no rare context with any other hapax. Robustness:")
for UBIQ,TH in [(150,6.0),(100,6.0),(200,5.0),(150,7.0)]:
    G=graph(UBIQ,TH); solo=[h for h in hapax if G.degree(h)==0]
    print(f"  UBIQ>{UBIQ}, idf-thresh {TH}: distinct={len(solo)} ({100*len(solo)/len(hapax):.0f}%), clustered={len(hapax)-len(solo)}")
# fix a config and study
G=graph(150,6.0); solo=set(h for h in hapax if G.degree(h)==0)
print(f"\n[config UBIQ>150, thresh 6.0]  distinct hapax: {len(solo)} of {len(hapax)}")
# idf: are distinct hapax in rarer-context verses? compare mean host-verse rare-context idf
def vctx_idf(h):
    rs=[r for r in vr[host[h]] if r not in hapax and df[r]<=150]
    return sum(idf(r) for r in rs)/len(rs) if rs else 0
import statistics as st
mi_solo=st.mean([vctx_idf(h) for h in solo]); mi_cl=st.mean([vctx_idf(h) for h in hapax-solo])
print(f"  mean rare-context idf: distinct={mi_solo:.2f} vs clustered={mi_cl:.2f}")
# per-surah: how many DISTINCT hapax does each surah hold?
sur_solo=collections.Counter(int(host[h].split(':')[0]) for h in solo)
top=sur_solo.most_common(12)
print("\nsuras holding the most DISTINCT hapax:", top)
# al-Kawthar
kw_h=[h for h in hapax if int(host[h].split(':')[0])==108]
print(f"\nal-Kawthar hapax: {kw_h}; distinct? {[(h, h in solo) for h in kw_h]}")
nverses=len({k for k in vr if int(k.split(':')[0])==108})
print(f"  -> al-Kawthar packs {sum(1 for h in kw_h if h in solo)} DISTINCT hapax into {nverses} verses")
# null: how many 3-verse random draws contain >=2 distinct hapax?
import random; random.seed(11); allk=list(vr)
def draw(): 
    vs=random.sample(allk,3); return sum(1 for v in vs for r in vr[v] if r in solo)
nd=[draw() for _ in range(10000)]; ge2=100*sum(1 for x in nd if x>=2)/len(nd)
print(f"  null: P(a random 3-verse window holds >=2 distinct hapax) = {ge2:.2f}%  -> al-Kawthar's 2-in-3 is in the top {ge2:.1f}%")
