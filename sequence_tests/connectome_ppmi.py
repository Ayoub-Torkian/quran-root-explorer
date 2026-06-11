"""#65(b) — NORMALIZED Qur'an connectome: PPMI edges (fix frequency bias). Hubs by association-strength,
emergent communities, strongest collocations. RESULT: raw hubs = most-frequent roots (artifact); PPMI hubs
shift; communities 4→12 (Q=0.248) reveal interpretable fields (creation/cosmos; faith/perception ءله-ءمن-
ربب-قلب-ءذن-ذکر-بصر; disbelief/punishment; social/law); strongest PPMI edges = genuine collocations
(لحم-خنزر-دمو-هلل forbidden foods; بکم-صمم deaf-dumb; قمص-قدد Yūsuf's shirt). ALWAYS normalize for frequency.
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
    N = len(ar); freq = Counter(w for rs in ar for w in rs); keep = {w for w, n in freq.items() if n >= 5}
    co = Counter()
    for rs in ar:
        rs = [w for w in rs if w in keep]
        for a, b in itertools.combinations(sorted(rs), 2): co[(a, b)] += 1
    G = nx.Graph()
    for (a, b), cab in co.items():
        if cab < 3: continue
        ppmi = np.log((cab / N) / ((freq[a] / N) * (freq[b] / N)))
        if ppmi > 0: G.add_edge(a, b, weight=ppmi)
    print(f"PPMI connectome: nodes={G.number_of_nodes()} edges={G.number_of_edges()}")
    strength = dict(G.degree(weight='weight')); rawdeg = dict(G.degree())
    print("RAW-freq hubs:", ", ".join(w for w, _ in sorted(rawdeg.items(), key=lambda x: -x[1])[:10]))
    print("PPMI hubs:    ", ", ".join(w for w, _ in sorted(strength.items(), key=lambda x: -x[1])[:10]))
    comms = list(greedy_modularity_communities(G, weight='weight'))
    print(f"communities={len(comms)} Q={modularity(G, comms, weight='weight'):.3f}")
    for comm in sorted(comms, key=len, reverse=True)[:6]:
        print("  (%d): %s" % (len(comm), " ".join(sorted(comm, key=lambda r: -strength[r])[:7])))
    edges = sorted(G.edges(data=True), key=lambda e: -e[2]['weight'])[:12]
    print("strongest PPMI edges:", ", ".join(f"{a}-{b}" for a, b, _ in edges))

if __name__ == "__main__":
    main()
