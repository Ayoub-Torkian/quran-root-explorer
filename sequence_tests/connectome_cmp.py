"""#65(a) — connectome topology COMPARATOR: is the Qur'an's network distinctive or generic language structure?
Surface-word co-occurrence networks, equal-N units, Qur'an vs ordinary Arabic. RESULT: small-world (clust>
degree-null) is GENERAL — ordinary Arabic MORE clustered (0.309 vs 0.149); ordinary raw hubs are FUNCTION
words (في/من/الي) = frequency artifact. So connectome TOPOLOGY is not a Qur'an distinctive; use it as a MAP,
and always normalize for frequency (see connectome_ppmi.py).
"""
import os, re, sys, warnings, itertools
import numpy as np, networkx as nx
warnings.filterwarnings("ignore")
from collections import Counter
from networkx.algorithms.community import greedy_modularity_communities, modularity
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_SURFACE as SF
rng = np.random.default_rng(7)
DIA = re.compile(r"[ً-ْٰـ]"); WA = re.compile(r"[^\W\d_]+", re.UNICODE)
def nrm(t):
    t = DIA.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    t = t.replace("ة", "ه").replace("ؤ", "و"); return WA.findall(t)
def build(units):
    units = [list(set(u)) for u in units if len(u) >= 3]
    freq = Counter(w for u in units for w in u); keep = {w for w, n in freq.items() if n >= 3}
    co = Counter()
    for u in units:
        u = [w for w in u if w in keep]
        for a, b in itertools.combinations(sorted(u), 2): co[(a, b)] += 1
    G = nx.Graph()
    for (a, b), w in co.items():
        if w >= 2: G.add_edge(a, b, weight=w)
    return G
def report(G, label):
    if G.number_of_nodes() < 20: print(f"  {label}: too small"); return
    deg = dict(G.degree()); Rg = nx.Graph(nx.configuration_model([d for _, d in G.degree()], seed=1)); Rg.remove_edges_from(nx.selfloop_edges(Rg))
    Q = modularity(G, list(greedy_modularity_communities(G, weight='weight')), weight='weight')
    print(f"  {label:11s} n={G.number_of_nodes()} e={G.number_of_edges()} clust={nx.transitivity(G):.3f}(rand {nx.transitivity(Rg):.3f}) Q={Q:.3f} hubs={','.join(w for w,_ in sorted(deg.items(),key=lambda x:-x[1])[:5])}")
def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    q = [nrm(df.iloc[i][SF]) for i in range(len(df))]
    SENT = re.compile(r"[.!؟?\n،؛:]+"); CP = os.path.join(ROOT, "sequence_tests", "corpus")
    txt = "".join("\n" + open(os.path.join(CP, n + ".txt"), encoding="utf-8", errors="ignore").read() for n in ["ar_tabari", "ar_classical2", "ar_novel", "ar_news", "ar_news2"] if os.path.exists(os.path.join(CP, n + ".txt")))
    ordr = [nrm(s) for s in SENT.split(txt)]
    N = min(len(q), len(ordr))
    report(build([q[i] for i in rng.choice(len(q), N, replace=False)]), "QURAN")
    report(build(ordr[:N]), "ord-Arabic")

if __name__ == "__main__":
    main()
