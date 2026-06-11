"""Build on the POSITIVE finding (consensus, z=+27): turn the mutual consensus
bonds into a NETWORK, detect communities (emergent concept-fields), and surface
the NON-TRIVIAL bonds — coherent across all 3 modalities yet weak in raw
co-occurrence (the candidates for 'not already known')."""
import time
from collections import defaultdict
import numpy as np
import networkx as nx
import analysis as A
import spatial_patterns as SP

t0 = time.time()
c = A.load_corpus("Book6.xlsx")
emb = SP.multiview_embeddings(c, True, unit="surah", min_freq=8)
roots = emb["roots"]; D = emb["distrib"]; L = emb["coloc"]; S = emb["spatial"]
n = len(roots); freq = c.freq_norm
K = A.normalize_letters


def rowz(M):
    G = M @ M.T; sq = np.diag(G).copy()
    sim = -(sq[:, None] + sq[None, :] - 2 * G)
    np.fill_diagonal(sim, np.nan)
    mu = np.nanmean(sim, 1, keepdims=True); sd = np.nanstd(sim, 1, keepdims=True); sd[sd == 0] = 1
    z = (sim - mu) / sd; np.fill_diagonal(z, -9.0); return z


ZD, ZL, ZS = rowz(D), rowz(L), rowz(S)
HI = 1.0
cons = ((ZD >= HI).astype(int) + (ZL >= HI).astype(int) + (ZS >= HI).astype(int)) >= 2
mutual = cons & cons.T

# co-occurrence (ayahs containing both roots)
ayahset = defaultdict(set)
for i, toks in enumerate(c.root_tokens):
    for t in {K(x) for x in toks}:
        ayahset[t].add(i)

G = nx.Graph()
G.add_nodes_from(range(n))
bonds = []
for i in range(n):
    for j in range(i + 1, n):
        if mutual[i, j]:
            w = float(ZD[i, j] + ZL[i, j] + ZS[i, j] + ZD[j, i] + ZL[j, i] + ZS[j, i])
            G.add_edge(i, j, weight=w)
            co = len(ayahset[roots[i]] & ayahset[roots[j]])
            bonds.append((w, co, roots[i], roots[j]))

try:
    comms = nx.community.louvain_communities(G, weight="weight", seed=0)
except Exception:
    comms = list(nx.community.greedy_modularity_communities(G, weight="weight"))
comms = [com for com in comms if len(com) >= 4]
comms.sort(key=len, reverse=True)
print(f"n={n}  consensus edges={G.number_of_edges()}  communities(>=4)={len(comms)}  ({time.time()-t0:.1f}s)")
print("\n=== EMERGENT CONCEPT-FIELDS (top communities) ===")
for k, com in enumerate(comms[:10]):
    mem = sorted(com, key=lambda i: -G.degree(i, weight="weight"))
    label = " ".join(roots[i] for i in mem[:10])
    print(f"  C{k+1} (n={len(com)}): {label}")

print("\n=== NON-TRIVIAL bonds (high cross-modal Σz, LOW raw co-occurrence ≤2) ===")
nt = [b for b in bonds if b[1] <= 2]
nt.sort(reverse=True)
for w, co, a, b in nt[:20]:
    print(f"   {a} <-> {b}   Σz={w:.1f}  co-occur={co}")
print(f"\ntotal {time.time()-t0:.1f}s")
