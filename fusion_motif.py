"""COMBINE motif (within-verse co-occurrence, higher-order) with consensus
(cross-modal bonds). Find consensus TRIANGLES (distributed motifs), then split by
whether their 3 members ever co-occur in ONE verse:
  REALIZED  = consensus clique AND members co-occur in verses (validation).
  LATENT    = consensus clique whose 3 members NEVER share a verse (new object:
              a theme woven across the corpus but never locally assembled).
"""
import time
from collections import defaultdict
from itertools import combinations
import numpy as np
import networkx as nx
import analysis as A
import spatial_patterns as SP

t0 = time.time()
c = A.load_corpus("Book6.xlsx")
emb = SP.multiview_embeddings(c, True, unit="surah", min_freq=8)
roots = emb["roots"]; D = emb["distrib"]; L = emb["coloc"]; S = emb["spatial"]
n = len(roots); K = A.normalize_letters


def rowz(M):
    G = M @ M.T; sq = np.diag(G).copy()
    sim = -(sq[:, None] + sq[None, :] - 2 * G); np.fill_diagonal(sim, np.nan)
    mu = np.nanmean(sim, 1, keepdims=True); sd = np.nanstd(sim, 1, keepdims=True); sd[sd == 0] = 1
    z = (sim - mu) / sd; np.fill_diagonal(z, -9.0); return z


ZD, ZL, ZS = rowz(D), rowz(L), rowz(S)
cons = ((ZD >= 1).astype(int) + (ZL >= 1).astype(int) + (ZS >= 1).astype(int)) >= 2
mutual = cons & cons.T
G = nx.Graph()
for i in range(n):
    for j in range(i + 1, n):
        if mutual[i, j]:
            G.add_edge(i, j, weight=float(ZD[i, j] + ZL[i, j] + ZS[i, j]))

ayahset = defaultdict(set)
for i, toks in enumerate(c.root_tokens):
    for t in {K(x) for x in toks}:
        ayahset[t].add(i)

# enumerate consensus triangles
tris = []
for a, b, d in (combinations(sorted(G.nodes()), 3)):
    pass  # too slow; use neighbour-based triangle finding instead
tris = []
adj = {u: set(G.neighbors(u)) for u in G.nodes()}
for u in G.nodes():
    nb = sorted(adj[u])
    for ii in range(len(nb)):
        for jj in range(ii + 1, len(nb)):
            v, w = nb[ii], nb[jj]
            if v > u and w > u and w in adj[v]:
                tris.append((u, v, w))

def triple_cooc(t):
    a, b, d = (roots[x] for x in t)
    return len(ayahset[a] & ayahset[b] & ayahset[d])

def strength(t):
    return sum(G[x][y]["weight"] for x, y in combinations(t, 2))

scored = [(strength(t), triple_cooc(t), t) for t in tris]
realized = sorted([s for s in scored if s[1] >= 3], reverse=True)
latent = sorted([s for s in scored if s[1] == 0], reverse=True)
print(f"consensus triangles={len(tris)}  realized(co-occur≥3)={len(realized)}  latent(co-occur=0)={len(latent)}  ({time.time()-t0:.1f}s)")
print("\n=== REALIZED motifs (consensus AND co-occur in verses) — validation ===")
for s, co, t in realized[:8]:
    print(f"   {' · '.join(roots[x] for x in t):28} Σz={s:.1f}  triple-co-occur={co}")
print("\n=== LATENT motifs (consensus clique, members NEVER share a verse) — the new object ===")
for s, co, t in latent[:18]:
    print(f"   {' · '.join(roots[x] for x in t):28} Σz={s:.1f}")
print(f"\ntotal {time.time()-t0:.1f}s")
