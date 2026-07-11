# -*- coding: utf-8 -*-
"""Graph-theoretic analysis: al-Kawthar's roots in the Qurʾanic co-occurrence web. Unicode-safe."""
import json, collections, itertools
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np, networkx as nx
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
OUT=f"{R}/research/intrinsic/kawthar_figs"
fa=lambda s:s.replace('ك','ک').replace('ي','ی').replace('ى','ی').replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا')

# transliteration of rasm consonants -> Latin (for ALL node labels)
TR={'ا':'ʾ','ب':'b','ت':'t','ث':'th','ج':'j','ح':'ḥ','خ':'kh','د':'d','ذ':'dh','ر':'r','ز':'z',
    'س':'s','ش':'sh','ص':'ṣ','ض':'ḍ','ط':'ṭ','ظ':'ẓ','ع':'ʿ','غ':'gh','ف':'f','ق':'q','ک':'k',
    'ل':'l','م':'m','ن':'n','ه':'h','و':'w','ی':'y','ء':'ʾ','ة':'h'}
def tr(root):
    if root=='ءله': return 'Allah'
    return '-'.join(TR.get(c,c) for c in root)

roots={}
for line in open(f"{R}/research/two_books_genome/roots_by_ayah.tsv",encoding='utf-8'):
    line=line.rstrip('\n')
    if '\t' in line: k,rs=line.split('\t',1); roots[k]=[fa(x) for x in rs.split()]

G=nx.Graph(); deg=collections.Counter(); pair=collections.Counter()
for k,rs in roots.items():
    u=sorted(set(rs))
    for r in u: deg[r]+=1
    for a,b in itertools.combinations(u,2): pair[(a,b)]+=1
for (a,b),w in pair.items(): G.add_edge(a,b,weight=w)
print("graph: nodes",G.number_of_nodes(),"edges",G.number_of_edges())

INK='#10243A'; NAVY='#1D3557'; GREEN='#1D9E75'; RED='#E63946'; BORD='#E2E8F1'; BTINT='#D7E6F7'; BORDEM='#C9D6E8'
S=['عطو','کثر','صلو','ربب','نحر','شنء','بتر']; HAPAX={'نحر','بتر'}

gdeg={r:(G.degree(r) if r in G else 0) for r in S}
wdeg={r:(G.degree(r,weight='weight') if r in G else 0) for r in S}
clust=nx.clustering(G, nodes=[r for r in S if r in G])
alldeg=sorted([G.degree(n) for n in G])
pct=lambda r: round(100*sum(1 for x in alldeg if x<gdeg[r])/len(alldeg),1)
metrics={}
print("\n== graph metrics for the 7 surah roots ==")
for r in S:
    metrics[tr(r)]=dict(degree=gdeg[r], wdegree=wdeg[r], clustering=round(clust.get(r,0),3), pctile=pct(r))
    print(f"  {tr(r):7s} degree={gdeg[r]:4d} wdeg={wdeg[r]:5d} clustering={clust.get(r,0):.3f} pct={pct(r)}")
json.dump(metrics, open(f"{R}/research/intrinsic/scripts/kawthar_graph_metrics.json",'w'), ensure_ascii=False, indent=1)

plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','text.color':INK})

# ================= FIG 11: ego network =================
ego=nx.Graph()
for r in S: ego.add_node(r, kind=('hapax' if r in HAPAX else 'surah'))
for r in S:
    if r not in G: continue
    for nb,d in sorted(G[r].items(), key=lambda kv:-kv[1]['weight'])[:6]:
        if nb not in ego: ego.add_node(nb, kind='neighbour')
        ego.add_edge(r,nb,weight=d['weight'])
for a,b in itertools.combinations(S,2):
    if G.has_edge(a,b): ego.add_edge(a,b,weight=G[a][b]['weight'])

fig,ax=plt.subplots(figsize=(11,7.6)); ax.axis('off'); ax.margins(0.12)
pos=nx.spring_layout(ego, k=1.1, seed=3, weight='weight', iterations=300)
sizes=[]; colors=[]
for n in ego.nodes():
    kind=ego.nodes[n].get('kind'); d=G.degree(n) if n in G else 1
    sizes.append((520 if kind=='surah' else 360 if kind=='hapax' else 90+min(d,300)*3))
    colors.append(RED if kind=='hapax' else (NAVY if kind=='surah' else BTINT))
ew=[0.5+0.12*ego[u][v]['weight'] for u,v in ego.edges()]
nx.draw_networkx_edges(ego,pos,width=ew,edge_color=BORDEM,alpha=0.75,ax=ax)
nx.draw_networkx_nodes(ego,pos,node_size=sizes,node_color=colors,edgecolors='white',linewidths=1.3,ax=ax)
for n,(x,y) in pos.items():
    kind=ego.nodes[n].get('kind')
    if kind=='surah':
        ax.text(x,y-0.085,tr(n),ha='center',va='top',fontsize=13,color=NAVY,fontweight='bold',zorder=6)
    elif kind=='hapax':
        ax.text(x,y-0.085,tr(n)+'  (hapax)',ha='center',va='top',fontsize=12.5,color=RED,fontweight='bold',zorder=6)
    else:
        ax.text(x,y+0.06,tr(n),ha='center',va='bottom',fontsize=10.5,color=INK,zorder=6)
ax.set_title("Figure 11.  al-Kawthar as a sub-graph of the Qurʾanic root co-occurrence web\n"
             "navy = the surah's 7 roots · red = the two hapax (near-isolates) · pale = strongest corpus neighbours · node size ∝ degree",
             loc='left',fontsize=13.5,color=NAVY,fontweight='bold')
fig.tight_layout(); fig.savefig(f"{OUT}/fig11_network.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig11_network.svg",bbox_inches='tight'); plt.close(fig)
print("saved fig11_network")

# ================= FIG 12: degree bars =================
fig,ax=plt.subplots(figsize=(8.8,4.8))
order=sorted(S, key=lambda r:gdeg[r]); y=np.arange(len(order))
vals=[max(gdeg[r],0.6) for r in order]
cols=[RED if r in HAPAX else (GREEN if r=='کثر' else NAVY) for r in order]
ax.barh(y,vals,color=cols,edgecolor='white',height=0.62,zorder=3)
ax.set_yticks(y); ax.set_yticklabels([tr(r) for r in order],fontsize=12.5)
ax.set_xscale('log'); ax.set_xlim(0.6, max(vals)*2.0)
for yi,r in zip(y,order):
    t=(f"{gdeg[r]} — near-isolate · {pct(r):.0f}th pct" if r in HAPAX
       else f"{gdeg[r]} co-occurring roots · {pct(r):.0f}th pct")
    ax.text(max(gdeg[r],0.6)*1.12, yi, t, va='center', fontsize=11.5,
            color=RED if r in HAPAX else INK, fontweight='bold' if r in HAPAX else 'normal')
ax.set_xlabel("Degree = number of distinct roots it ever shares a verse with (log scale)",fontsize=12.5)
ax.set_title("Figure 12.  Network degree confirms the fingerprint: the two hapax are\nnear-isolate nodes; r-b-b and k-th-r are hubs (94th–99.8th percentile)",loc='left',fontsize=13.5,color=NAVY,fontweight='bold')
for s in ['top','right']: ax.spines[s].set_visible(False)
ax.grid(axis='x',color=BORD,lw=0.8,zorder=0)
fig.tight_layout(); fig.savefig(f"{OUT}/fig12_degree.png",dpi=150,bbox_inches='tight'); fig.savefig(f"{OUT}/fig12_degree.svg",bbox_inches='tight'); plt.close(fig)
print("saved fig12_degree")
