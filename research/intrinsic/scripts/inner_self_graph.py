# -*- coding: utf-8 -*-
"""Inner-self graph from the corpus (Book6 co-occurrence), PPMI-weighted. Full metric suite (all 25 nodes) +
graph-level stats + degree-preserving null for modularity + a COMMUNITY-CLUSTERED layout (communities as
separated blobs, for an explainable picture). Output: anatomy_figs/inner_self_graph_metrics.json.
MEASURED: edges/weights/metrics. INTERPRETIVE: node selection + role colours."""
import openpyxl, itertools, math, json, random
import networkx as nx
import networkx.algorithms.community as nxc
random.seed(17)
ROOT="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2/research/intrinsic"
wb=openpyxl.load_workbook(ROOT+"/../../Book6.xlsx", read_only=True, data_only=True); ws=wb.active
ayah=[set(str(r[8] or "").split()) for r in ws.iter_rows(min_row=9, values_only=True) if r[5] is not None]
Nv=len(ayah)
NODES={
 'الله':(['ءله'],'root'),'نفس':(['نفس'],'self'),'صدر':(['صدر'],'self'),'قلب':(['قلب'],'self'),'فؤاد':(['فءد'],'self'),
 'علم·عقل':(['علم','عقل'],'cog'),'عمل صالح':(['عمل','صلح'],'act'),'ظنّ':(['ظنن'],'down'),'هوی':(['هوی'],'down'),
 'ذکر':(['ذکر'],'up'),'تقوی':(['وقی'],'up'),'إیمان':(['ءمن'],'up'),'هدی':(['هدی'],'up'),'لهو·لعب':(['لهو','لعب'],'down'),
 'وسواس·شیطان':(['وسوس','شطن'],'down'),'تسویل':(['سول'],'down'),'مرض':(['مرض'],'down'),'طبع·ختم':(['طبع','ختم'],'down'),
 'زاد':(['زید'],'amp'),'برزخ':(['برزخ'],'bound'),'غطاء':(['غطو'],'bound'),'دنیا':(['دنو'],'dom'),'آخرة':(['ءخر','حیی'],'dom'),
 'کوثر':(['کثر'],'out_g'),'أبتر':(['بتر'],'out_r'),
}
names=list(NODES)
pres={n:[any(rt in s for rt in NODES[n][0]) for s in ayah] for n in names}
df={n:sum(pres[n]) for n in names}
def co(a,b): return sum(1 for i in range(Nv) if pres[a][i] and pres[b][i])
G=nx.Graph()
for n in names: G.add_node(n)
edges=[]
for a,b in itertools.combinations(names,2):
    c=co(a,b)
    if c==0: continue
    pab=c/Nv; pa=df[a]/Nv; pb=df[b]/Nv
    ppmi=math.log2(pab/(pa*pb)) if pab>0 and pa*pb>0 else 0.0
    if ppmi>0:
        G.add_edge(a,b,weight=round(ppmi,3)); edges.append([a,b,round(ppmi,3)])
# per-node metrics (ALL nodes)
deg=dict(G.degree())
strg={n:round(sum(d['weight'] for _,_,d in G.edges(n,data=True)),3) for n in G}
btw=nx.betweenness_centrality(G,weight=None)
try: eig=nx.eigenvector_centrality(G,max_iter=3000,weight='weight')
except Exception: eig={n:0 for n in G}
clo=nx.closeness_centrality(G)
pr=nx.pagerank(G,weight='weight')
clus=nx.clustering(G,weight='weight')
comms=list(nxc.greedy_modularity_communities(G,weight='weight'))
comm_of={n:i for i,c in enumerate(comms) for n in c}
mod=nxc.modularity(G,comms,weight='weight')
realmod_bin=nxc.modularity(G,list(nxc.greedy_modularity_communities(G)))
def null_mod(g,iters=300):
    import statistics as st; vals=[]
    for _ in range(iters):
        h=g.copy()
        try: nx.double_edge_swap(h,nswap=h.number_of_edges()*2,max_tries=h.number_of_edges()*20,seed=random.randint(0,1<<30))
        except Exception: pass
        vals.append(nxc.modularity(h,list(nxc.greedy_modularity_communities(h))))
    return st.mean(vals), (st.pstdev(vals) or 1e-9)
mu,sd=null_mod(G); zmod=(realmod_bin-mu)/sd
# graph-level stats
conn=nx.is_connected(G)
stats={'nodes':G.number_of_nodes(),'edges':G.number_of_edges(),'density':round(nx.density(G),3),
 'avg_degree':round(2*G.number_of_edges()/G.number_of_nodes(),2),'components':nx.number_connected_components(G),
 'cycles':len(nx.cycle_basis(G)),'transitivity':round(nx.transitivity(G),3),
 'avg_clustering':round(nx.average_clustering(G,weight=None),3),
 'diameter':(nx.diameter(G) if conn else None),
 'avg_path':(round(nx.average_shortest_path_length(G),2) if conn else None),
 'assortativity':round(nx.degree_assortativity_coefficient(G),3),
 'modularity_ppmi':round(mod,3),'modularity_z':round(zmod,2),'n_communities':len(comms)}
# COMMUNITY-CLUSTERED layout: communities as separated blobs
K=len(comms); Rout=4.6; rin=0.82
pos={}
order_comm=sorted(range(K), key=lambda i:-len(comms[i]))
for slot,ci in enumerate(order_comm):
    ang=math.pi/2 - 2*math.pi*slot/K
    cx,cy=Rout*math.cos(ang),Rout*math.sin(ang)
    mem=sorted(comms[ci],key=lambda n:-strg[n]); m=len(mem)
    if m==1: pos[mem[0]]=[cx,cy]
    else:
        sub=G.subgraph(comms[ci])
        try: sp=nx.spring_layout(sub,weight='weight',seed=7,k=1.0,iterations=300)
        except Exception: sp={n:[math.cos(2*math.pi*j/m),math.sin(2*math.pi*j/m)] for j,n in enumerate(mem)}
        xs=[p[0] for p in sp.values()]; ys=[p[1] for p in sp.values()]
        x0,x1=min(xs),max(xs); y0,y1=min(ys),max(ys); sx=(x1-x0) or 1; sy=(y1-y0) or 1
        for n,(x,y) in sp.items():
            pos[n]=[round(cx+((x-x0)/sx-0.5)*2*rin,4), round(cy+((y-y0)/sy-0.5)*2*rin,4)]
pos={n:pos[n] for n in names}
# backbone for drawing (intra dense + each node's top edge), tag inter/intra-community
THR=1.0; bb={}
for a,b,w in edges:
    if w>=THR: bb[(a,b)]=w
for n in G:
    nb=[(m,G[n][m]['weight']) for m in G[n]]
    if nb and not any(n in k for k in bb):
        m,w=max(nb,key=lambda t:t[1]); bb[(min(n,m),max(n,m))]=w
backbone=[[a,b,w,(comm_of[a]!=comm_of[b])] for (a,b),w in bb.items()]  # 4th = is_bridge
out={'N':Nv,'nodes':names,'roles':{n:NODES[n][1] for n in names},'df':df,
 'edges':edges,'deg':deg,'strength':strg,
 'betweenness':{k:round(v,4) for k,v in btw.items()},'eigenvector':{k:round(v,4) for k,v in eig.items()},
 'closeness':{k:round(v,4) for k,v in clo.items()},'pagerank':{k:round(v,4) for k,v in pr.items()},
 'clustering':{k:round(v,3) for k,v in clus.items()},'community':comm_of,
 'communities':[sorted(c) for c in comms],'stats':stats,'pos':pos,'backbone':backbone,'backbone_thr':THR}
# THREE functional sub-graphs (relief from the dense combined graph) — each: induced PPMI edges + spring layout + top bridges out
GROUPS=[
 ('apparatus','Apparatus — the organs (+ cognition↔action)',['نفس','صدر','قلب','فؤاد','علم·عقل','عمل صالح']),
 ('drivers','Drivers — up-drivers · down-drivers · the زاد amplifier',['ذکر','تقوی','إیمان','هدی','ظنّ','هوی','لهو·لعب','وسواس·شیطان','تسویل','مرض','طبع·ختم','زاد']),
 ('orientation','Orientation & outcome — دنیا/آخرة → کوثر/أبتر',['دنیا','آخرة','غطاء','برزخ','کوثر','أبتر','الله']),
]
def _deoverlap(pos,n):
    # spread nodes so no two collide: normalize to unit box, then push apart any pair closer than min_d
    import math
    P={k:[float(v[0]),float(v[1])] for k,v in pos.items()}
    xs=[p[0] for p in P.values()]; ys=[p[1] for p in P.values()]
    x0,x1=min(xs),max(xs); y0,y1=min(ys),max(ys); sx=(x1-x0) or 1; sy=(y1-y0) or 1
    for k in P: P[k]=[(P[k][0]-x0)/sx*2-1,(P[k][1]-y0)/sy*2-1]   # -> [-1,1]^2
    min_d=max(0.42, 1.9/math.sqrt(max(1,n)))                    # required separation (scales with count)
    ks=list(P)
    for _ in range(220):
        moved=False
        for i in range(len(ks)):
            for j in range(i+1,len(ks)):
                a,b=ks[i],ks[j]; dx=P[a][0]-P[b][0]; dy=P[a][1]-P[b][1]
                d=math.hypot(dx,dy) or 1e-6
                if d<min_d:
                    push=(min_d-d)/2.0; ux,uy=dx/d,dy/d
                    P[a][0]+=ux*push; P[a][1]+=uy*push; P[b][0]-=ux*push; P[b][1]-=uy*push; moved=True
        if not moved: break
    return {k:[round(v[0],4),round(v[1],4)] for k,v in P.items()}
func_sub={}
for key,label,grp in GROUPS:
    Sg=set(grp); gnodes=[n for n in names if n in Sg]
    gint=[[x,y,w] for x,y,w in edges if x in Sg and y in Sg]
    Hg=nx.Graph(); Hg.add_nodes_from(gnodes)
    for x,y,w in gint: Hg.add_edge(x,y,weight=w)
    gp=nx.spring_layout(Hg,weight='weight',seed=11,k=1.4,iterations=400)
    gp=_deoverlap(gp,len(gnodes))
    # bridges OUT, deduped by external target (keep the strongest source→target), so no target repeats
    gext={}
    for x,y,w in edges:
        if (x in Sg)!=(y in Sg):
            ins_,ext_=(x,y) if x in Sg else (y,x)
            if w>gext.get(ext_,(None,0))[1]: gext[ext_]=(ins_,w)
    gbr=sorted([[i,o,round(w,3)] for o,(i,w) in gext.items()],key=lambda e:-e[2])[:5]
    func_sub[key]={'label':label,'nodes':gnodes,'edges':gint,'pos':gp,'bridges':gbr}
out['func_sub']=func_sub
# COMBINED-by-region layout: the 3 functional groups as 3 blobs (the "combined" of the 3 subgraphs)
REGION_CENTERS={'apparatus':(0.0,3.4),'drivers':(-3.7,-2.1),'orientation':(3.7,-2.1)}
region_pos={}; region_of={}
for key,label,grp in GROUPS:
    cx,cy=REGION_CENTERS[key]; sp=func_sub[key]['pos']
    xs=[p[0] for p in sp.values()]; ys=[p[1] for p in sp.values()]
    x0,x1=min(xs),max(xs); y0,y1=min(ys),max(ys); sx=(x1-x0) or 1; sy=(y1-y0) or 1
    rr=1.85 if key=='drivers' else 1.45
    for n,(x,y) in sp.items():
        region_pos[n]=[round(cx+((x-x0)/sx-0.5)*2*rr,4), round(cy+((y-y0)/sy-0.5)*2*rr,4)]
    for n in grp: region_of[n]=key
out['pos']=region_pos
out['regions']=[[k,l,g] for k,l,g in GROUPS]
out['region_of']=region_of
json.dump(out,open(ROOT+"/anatomy_figs/inner_self_graph_metrics.json","w",encoding='utf-8'),ensure_ascii=False,indent=1)
print("stats:",stats)
print("written; backbone",len(backbone),"edges")
