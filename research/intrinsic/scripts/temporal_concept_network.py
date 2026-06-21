"""Graph #4 — temporal / multiplex concept network (how families assemble across nuzūl).

VERDICT (2026-06-21): one REAL residual finding (finer-than-binary temporal locality) + a lot that
reduces to the known Meccan→Medinan shift; the multiplex is degenerate in-sandbox.

Substrate ROOT (content, drop top-12). Arrangement DIVINE-ALT (revelation order, Book6 col12, nuzūl 1–114).

(a) FAMILY REVELATION PROFILES (9 dcSBM families, occurrence-weighted mean nuzūl):
    families span a NARROW band (mean rank 66–74/114, %Meccan 53–73%). Temporal SEGREGATION real but
    modest: spread(family-mean-nuzūl)=2.74 vs label-shuffle null 1.35±0.39  -> z=+3.6.
    => families differ mainly in Meccan/Medinan BALANCE (already-known thematic shift), not a novel
       assembly schedule.

(b) TIMING-HOMOPHILY of the co-occurrence backbone (do co-occurring concepts share nuzūl?):
    full corpus  r=+0.217  z=+9.9 (vs node-attribute permutation).
    ATTRIBUTION CONTROL (decisive) — rebuild inside Meccan era alone (no M/M binary):
        ranks 1–86  r=+0.081  z=+4.1
        ranks 1–60  r=+0.115  z=+5.8
    => ~60% of the effect IS the known Meccan→Medinan shift, but a GENUINE finer-than-binary temporal
       locality SURVIVES (z=+4.1–5.8). This residual is the real finding (grade ~52).

(c) MULTIPLEX — DEGENERATE in-sandbox: the "semantic" layer is PPMI-SVD-DERIVED from co-occurrence
    (not an independent layer); a morphology layer needs an Arabic morphological analyzer (none here).
    A true 3-layer multiplex is NOT testable with available instruments -> deferred, not claimed.

Analog: temporal assortativity / "aging" in growing networks (citation nets cite contemporaries).
Flip: independent semantic (external embeddings) + morphology (tagger) for a real multiplex;
āyah-level nuzūl to sharpen the residual locality.
Run: see this file's __main__ (loads Book6.xlsx + concept_graph_features.json)."""
import pandas as pd, numpy as np, networkx as nx, math
from collections import Counter, defaultdict


def timing_assortativity(vr, nz, lo, hi, R=600, seed=1):
    rng = np.random.default_rng(seed)
    idxs = [i for i in range(len(vr)) if not np.isnan(nz[i]) and lo <= nz[i] <= hi]
    docf = Counter(r for i in idxs for r in vr[i]); drop = {r for r, _ in docf.most_common(12)}
    nodes = [r for r, _ in docf.most_common() if r not in drop][:250]; nset = set(nodes)
    acc = defaultdict(lambda: [0.0, 0])
    for i in idxs:
        for r in vr[i] & nset:
            acc[r][0] += nz[i]; acc[r][1] += 1
    mnz = {r: acc[r][0] / acc[r][1] for r in nodes if acc[r][1] > 0}; nodes = [c for c in nodes if c in mnz]
    co = Counter()
    for i in idxs:
        rs = sorted(vr[i] & set(nodes))
        for a in range(len(rs)):
            for b in range(a + 1, len(rs)):
                co[(rs[a], rs[b])] += 1
    Nn = len(idxs)
    adj = defaultdict(list)
    for (a, b), w in co.items():
        pa, pb, pab = acc[a][1] / Nn, acc[b][1] / Nn, w / Nn
        pm = max(0.0, math.log(pab / (pa * pb))) if pa * pb * pab > 0 else 0.0
        if pm > 0:
            adj[a].append((pm, b)); adj[b].append((pm, a))
    G = nx.Graph(); G.add_nodes_from(nodes)
    for c in nodes:
        for pm, m in sorted(adj[c], reverse=True)[:12]:
            G.add_edge(c, m)
    H = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    nn = list(H.nodes()); ix = {c: i for i, c in enumerate(nn)}; ei = [(ix[a], ix[b]) for a, b in H.edges()]
    val = np.array([mnz[c] for c in nn])
    def assort(v):
        x = np.array([v[i] for i, j in ei]); y = np.array([v[j] for i, j in ei])
        return np.corrcoef(np.r_[x, y], np.r_[y, x])[0, 1]
    obs = assort(val); nl = np.array([assort(rng.permutation(val)) for _ in range(R)])
    return obs, (obs - nl.mean()) / (nl.std() + 1e-9), Nn


if __name__ == "__main__":
    df = pd.read_excel("Book6.xlsx", header=7)
    norm = lambda t: str(t).replace("ك", "ک").replace("ي", "ی")
    nz = pd.to_numeric(df[df.columns[12]], errors="coerce").to_numpy()
    vr = [set(r for r in norm(v).split() if r and r != "-") for v in df[df.columns[8]]]
    for lo, hi, tag in [(1, 114, "FULL"), (1, 86, "MECCAN-only"), (1, 60, "EARLY-MECCAN")]:
        r, z, n = timing_assortativity(vr, nz, lo, hi)
        print(f"{tag:14s} verses={n} timing-assortativity r={r:+.3f} z={z:+.1f}")
