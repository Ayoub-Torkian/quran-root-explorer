"""#64 — NETWORK view of the muqaṭṭaʿāt (multi-grain; network-first per DESIGN_STANCE).
(1) LETTER co-occurrence graph: hubs (م/ا/ل), isolate (ن), communities = traditional families.
(2) SŪRA content graph (root-cosine): do letter-families form content-COMMUNITIES? modularity vs label-shuffle.
RESULT: (1) designed combinatorial topology; (2) Q≈0 (z=+1.73, p=0.05) — letter-families are NOT content-
communities even in the network view → confirms #56 (not a linear-method artifact). Distinctive = position +
cardinality + letter-combinatorics, NOT content.
"""
import os, re, sys, warnings, itertools
import numpy as np, networkx as nx
warnings.filterwarnings("ignore")
from networkx.algorithms.community import greedy_modularity_communities, modularity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT); import analysis as A
from analysis import COL_ROOTS as R, COL_SURAH as S
rng = np.random.default_rng(7)
H = re.compile(r"[ً-ْٰـ]")
def rasm(t):
    t = H.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    return "".join(re.findall(r"[ء-ي]", t))
MUQ = {2:"الم",3:"الم",7:"المص",10:"الر",11:"الر",12:"الر",13:"المر",14:"الر",15:"الر",19:"كهيعص",20:"طه",
 26:"طسم",27:"طس",28:"طسم",29:"الم",30:"الم",31:"الم",32:"الم",36:"يس",38:"ص",40:"حم",41:"حم",42:"حمعسق",
 43:"حم",44:"حم",45:"حم",46:"حم",50:"ق",68:"ن"}
MUQ = {k: rasm(v) for k, v in MUQ.items()}

def main():
    G = nx.Graph()
    for letters in MUQ.values():
        for a, b in itertools.combinations(sorted(set(letters)), 2):
            G.add_edge(a, b, weight=(G[a][b]['weight'] + 1 if G.has_edge(a, b) else 1))
    for L in set("".join(MUQ.values())): G.add_node(L)
    print("(1) LETTER network — hubs:", ", ".join(f"{l}:{d}" for l, d in sorted(G.degree(weight='weight'), key=lambda x:-x[1])[:8]))
    print("    isolates:", [l for l in G.nodes if G.degree(l) == 0],
          "| communities:", ["".join(sorted(c)) for c in greedy_modularity_communities(G, weight='weight')])
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    sdoc = lambda s: " ".join(w for i in np.where(sur == s)[0] for w in str(df.iloc[i][R]).split() if w and w != 'nan')
    muq = sorted(MUQ); V = normalize(TfidfVectorizer(analyzer=str.split, min_df=2).fit_transform([sdoc(s) for s in muq]).toarray())
    Sim = V @ V.T; Gs = nx.Graph()
    for i in range(len(muq)):
        for j in range(i + 1, len(muq)):
            if Sim[i, j] > 0.3: Gs.add_edge(muq[i], muq[j], weight=float(Sim[i, j]))
    fam = {s: MUQ[s] for s in muq}; parts = {}
    for s in Gs.nodes: parts.setdefault(fam[s], set()).add(s)
    Q = modularity(Gs, list(parts.values()), weight='weight')
    labels = [fam[s] for s in Gs.nodes]; null = []
    for _ in range(2000):
        perm = list(labels); rng.shuffle(perm); p = {}
        for s, l in zip(Gs.nodes, perm): p.setdefault(l, set()).add(s)
        null.append(modularity(Gs, list(p.values()), weight='weight'))
    null = np.array(null)
    print(f"(2) content network: nodes={Gs.number_of_nodes()} edges={Gs.number_of_edges()} | letter-family Q={Q:.3f} z={(Q-null.mean())/null.std():+.2f} p={np.mean(null>=Q):.4f}")

if __name__ == "__main__":
    main()
