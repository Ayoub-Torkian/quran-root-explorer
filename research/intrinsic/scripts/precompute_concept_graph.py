"""Precompute per-concept GRAPH features (the two results that survived scrutiny):
  bridge_z  = degree-NORMALISED betweenness (vs degree-preserving null) — true connector score
  family    = degree-corrected SBM block (spectral, row-normalised = frequency-corrected) + label
  hub_z     = within-family degree z — the family's anchor concepts
  partners  = top-3 PPMI co-occurrence partners
Writes concept_graph_features.json at repo root. App READS it (no networkx/sklearn at runtime)."""
import json, math, random
import pandas as pd, numpy as np, networkx as nx
from collections import Counter, defaultdict
from sklearn.cluster import KMeans
random.seed(1); np.random.seed(1)

df = pd.read_excel("Book6.xlsx", header=7); ROOTS = df.columns[8]
norm = lambda t: str(t).replace("ك","ک").replace("ي","ی")
vr = [set(r for r in norm(v).split() if r and r != "-") for v in df[ROOTS]]
N = len(vr); docf = Counter(r for s in vr for r in s)
drop = {r for r,_ in docf.most_common(12)}
nodes = [r for r,_ in docf.most_common() if r not in drop][:300]
nset = set(nodes); idx = {r:i for i,r in enumerate(nodes)}; n = len(nodes)

# co-occurrence + PPMI backbone (top-12 partners/node) + full adjacency for SBM
A = np.zeros((n,n)); co = Counter()
for s in vr:
    rs = sorted(s & nset)
    for i in range(len(rs)):
        for j in range(i+1,len(rs)):
            A[idx[rs[i]],idx[rs[j]]] += 1; A[idx[rs[j]],idx[rs[i]]] += 1
            co[(rs[i],rs[j])] += 1
def ppmi(a,b,w):
    pa,pb,pab = docf[a]/N, docf[b]/N, w/N
    return max(0.0, math.log(pab/(pa*pb))) if pa*pb*pab>0 else 0.0
adj = defaultdict(list)
for (a,b),w in co.items():
    pm = ppmi(a,b,w)
    if pm>0: adj[a].append((pm,b)); adj[b].append((pm,a))
G = nx.Graph(); G.add_nodes_from(nodes)
for nd in nodes:
    for pm,m in sorted(adj[nd],reverse=True)[:12]:
        G.add_edge(nd,m,weight=round(pm,3))
gc = max(nx.connected_components(G), key=len); H = G.subgraph(gc).copy()

# bridge_z: betweenness vs degree-preserving (double-edge-swap) null
bt = nx.betweenness_centrality(H, normalized=True)
order = list(H.nodes()); R = 40
null = np.zeros((R,len(H)))
for r in range(R):
    Hr = H.copy(); nx.double_edge_swap(Hr, nswap=H.number_of_edges()*5,
                                       max_tries=H.number_of_edges()*100, seed=r)
    b = nx.betweenness_centrality(Hr, normalized=True); null[r] = [b[x] for x in order]
mu, sd = null.mean(0), null.std(0)+1e-9
bridge_z = {x:(bt[x]-mu[i])/sd[i] for i,x in enumerate(order)}

# dcSBM family (regularised spectral, row-normalise = degree/freq correction) + within-family hub z
deg = A.sum(1); tau = deg.mean(); Dt = np.diag(1/np.sqrt(deg+tau)); L = Dt@A@Dt
w,V = np.linalg.eigh(L); K = 9
X = V[:, np.argsort(-np.abs(w))[:K]]; Xn = X/(np.linalg.norm(X,axis=1,keepdims=True)+1e-9)
lab = KMeans(K, n_init=10, random_state=1).fit_predict(Xn)
fam_label = {}
for c in range(K):
    mem = sorted([i for i in range(n) if lab[i]==c], key=lambda i:-docf[nodes[i]])
    fam_label[c] = " · ".join(nodes[i] for i in mem[:3])
hub_z = {}
for c in range(K):
    m = [i for i in range(n) if lab[i]==c]
    kin = A[np.ix_(m,m)].sum(1); mu2,sd2 = kin.mean(), kin.std()+1e-9
    for t,i in enumerate(m): hub_z[nodes[i]] = (kin[t]-mu2)/sd2

def role(r):
    bz = bridge_z.get(r, -9); hz = hub_z.get(r, -9)
    if bz >= 2.0: return "connector / bridge"
    if hz >= 2.0: return "family anchor (hub)"
    return "member"
partners = {nd: [m for _,m in sorted(adj[nd],reverse=True)[:3]] for nd in nodes}

out = {}
for nd in nodes:
    if nd not in H: continue
    out[nd] = dict(freq=int(docf[nd]),
                   bridge_z=round(float(bridge_z.get(nd,0)),2),
                   family=int(lab[idx[nd]]), family_label=fam_label[int(lab[idx[nd]])],
                   hub_z=round(float(hub_z.get(nd,0)),2),
                   role=role(nd), partners=partners[nd])
meta = dict(n_concepts=len(out), n_families=K, backbone_nodes=H.number_of_nodes(),
            backbone_edges=H.number_of_edges(), null_R=R,
            note="bridge_z=degree-normalised betweenness; family=dcSBM block; hub_z=within-family degree z")
json.dump({"meta":meta,"concepts":out}, open("concept_graph_features.json","w"),
          ensure_ascii=False, indent=0)
print("WROTE concept_graph_features.json :", len(out), "concepts,", K, "families")
print("families:", [fam_label[c] for c in range(K)])
print("sample bridges:", sorted(out, key=lambda r:-out[r]['bridge_z'])[:6])
