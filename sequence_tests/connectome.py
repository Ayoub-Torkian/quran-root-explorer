"""#65 — QUR'AN CONNECTOME, first layer: root co-occurrence network (ecosystem/connectome-first principle).
All roots retained (freq≥4); edges = co-occur in same āyah ≥2×. Topology + emergent communities + hubs, vs
a degree-matched random graph. RESULT: nodes 915, edges 29,374; clustering 0.364 > random 0.275 (small-world
tendency); hubs = theologically central roots (ءله/قول/کون/ءمن/ربب/علم); modularity Q=0.09 (LOW → integrated,
not siloed); 4 emergent communities ≈ creation/knowledge, revelation/speech, faith/ethics, disbelief/judgment.
Descriptive/internal (gated vs degree-null); cross-text distinctiveness untested. Divinely-rooted.
"""
import os, sys, warnings, itertools
import numpy as np, networkx as nx
warnings.filterwarnings("ignore")
from collections import Counter
from networkx.algorithms.community import greedy_modularity_communities, modularity
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R

def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    ar = [list({w for w in str(df.iloc[i][R]).split() if w and w != 'nan'}) for i in range(len(df))]
    freq = Counter(w for rs in ar for w in rs); keep = {w for w, n in freq.items() if n >= 4}
    ew = Counter()
    for rs in ar:
        rs = [w for w in rs if w in keep]
        for a, b in itertools.combinations(sorted(rs), 2): ew[(a, b)] += 1
    G = nx.Graph()
    for (a, b), w in ew.items():
        if w >= 2: G.add_edge(a, b, weight=w)
    deg = dict(G.degree())
    print(f"nodes={G.number_of_nodes()} edges={G.number_of_edges()} avg_deg={np.mean(list(deg.values())):.1f} "
          f"density={nx.density(G):.4f} clustering={nx.transitivity(G):.3f}")
    print("HUBS:", ", ".join(f"{r}({d})" for r, d in sorted(deg.items(), key=lambda x: -x[1])[:12]))
    Rg = nx.Graph(nx.configuration_model([d for _, d in G.degree()], seed=1)); Rg.remove_edges_from(nx.selfloop_edges(Rg))
    print(f"clustering real {nx.transitivity(G):.3f} vs degree-matched random {nx.transitivity(Rg):.3f}")
    comms = list(greedy_modularity_communities(G, weight='weight'))
    print(f"communities={len(comms)} modularity Q={modularity(G, comms, weight='weight'):.3f}")
    for comm in sorted(comms, key=len, reverse=True)[:5]:
        print(f"  ({len(comm)}): " + " ".join(sorted(comm, key=lambda r: -deg[r])[:7]))

if __name__ == "__main__":
    main()
