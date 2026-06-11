# re-deploy 1779671310
"""topics.py — corpus topic discovery, focused mode.

Two computation paths:

  • compute_for_roots(corpus, input_roots, progress_cb)
      Fast, per-query. Runs Louvain stability + PPMI/SVD on the ego-network
      AROUND the input roots (their partners + 2-hop neighbours). Typically
      ~10-30 seconds. Returns the topic each input root belongs to plus
      adjacent topics and quadrant lists.

  • compute(corpus)
      Full corpus pass (kept for backward compatibility and the "Advanced"
      view). Slow on first run (a few minutes); cached to disk.

Signals (same in both modes):
  S1 = co-clustering stability across N Louvain runs (resolution-mixed)
  S2 = cosine similarity in PPMI-SVD distributional space

Quadrant labels for the user's root R against another root X:
  high S1, high S2 = core      (shares verses AND contexts)
  high S1, low  S2 = contrastive  (shares verses, different contexts — antithetical)
  low  S1, high S2 = distributional synonym (latent semantic kin)
  low  S1, low  S2 = unrelated
"""
from __future__ import annotations

import math
import os
import pickle
import time
from collections import defaultdict
from pathlib import Path

import networkx as nx
import numpy as np


# ─── Config ────────────────────────────────────────────────────────────
CACHE_VERSION = 3

# Global (slow) compute config
N_SEEDS = int(os.environ.get("TOPICS_N_SEEDS", "30"))
RESOLUTIONS = [0.7, 1.0, 1.5]
STABILITY_THRESHOLD = 0.70
DIST_SVD_DIMS = 50
MIN_ROOT_FREQUENCY = 2

# Focused (fast, per-query) compute config
FOCUSED_N_SEEDS = 15
FOCUSED_RESOLUTIONS = [1.0, 1.5]
FOCUSED_STABILITY_THRESHOLD = 0.60
FOCUSED_MAX_NODES = 250          # cap ego-network size for speed
FOCUSED_TOP_PARTNERS = 30        # per-root direct partners
FOCUSED_HOP2_PARTNERS = 8        # per-partner second-hop expansion

_CACHE_DIR = Path(os.environ.get("ANALYTICS_DATA_DIR", "/data"))
try:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
except PermissionError:
    _CACHE_DIR = Path("./.topics_cache")
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_PATH = _CACHE_DIR / "topics_cache.pkl"


# ═══════════════════════════════════════════════════════════════════════
# Shared low-level helpers
# ═══════════════════════════════════════════════════════════════════════
def _build_index(corpus) -> tuple[dict, dict]:
    """Returns (ayah_to_roots: ayah_id -> set(root), root_freq: root -> count)."""
    from analysis import normalize_letters
    ayah_to_roots: dict[int, set[str]] = defaultdict(set)
    root_freq: dict[str, int] = defaultdict(int)
    root_tokens = getattr(corpus, "root_tokens", None) or []
    for i, toks in enumerate(root_tokens):
        seen: set[str] = set()
        for t in toks:
            if not t:
                continue
            r = normalize_letters(t)
            if r:
                seen.add(r)
        if seen:
            ayah_to_roots[i] = seen
            for r in seen:
                root_freq[r] += 1
    return dict(ayah_to_roots), dict(root_freq)


def _build_graph(ayah_to_roots: dict, root_freq: dict, kept_roots: set) -> nx.Graph:
    pair_weight: dict[tuple[str, str], int] = defaultdict(int)
    for roots_in_ayah in ayah_to_roots.values():
        rs = sorted(r for r in roots_in_ayah if r in kept_roots)
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                pair_weight[(rs[i], rs[j])] += 1
    g = nx.Graph()
    g.add_nodes_from(kept_roots)
    for (a, b), w in pair_weight.items():
        g.add_edge(a, b, weight=w)
    return g


def _louvain_runs(g: nx.Graph, n_seeds: int, resolutions: list[float],
                  progress_cb=None, prog_start=0.0, prog_span=0.6):
    """Run Louvain x seeds x resolutions; optionally report progress."""
    from networkx.algorithms.community import louvain_communities
    partitions = []
    rng = np.random.default_rng(0)
    seeds = rng.integers(0, 2**31 - 1, size=n_seeds).tolist()
    total = len(seeds) * len(resolutions)
    done = 0
    for res in resolutions:
        for seed in seeds:
            try:
                comms = louvain_communities(
                    g, weight="weight", resolution=res, seed=int(seed))
            except Exception:
                continue
            part = {r: i for i, c in enumerate(comms) for r in c}
            partitions.append(part)
            done += 1
            if progress_cb and done % max(1, total // 20) == 0:
                frac = prog_start + prog_span * (done / total)
                progress_cb(frac, f"Louvain stability run {done}/{total}")
    return partitions


def _coclustering_stability(partitions, nodes: list[str]) -> dict[tuple[str, str], float]:
    n = len(nodes)
    idx = {r: i for i, r in enumerate(nodes)}
    arrs = []
    for part in partitions:
        a = np.full(n, -1, dtype=np.int32)
        for r, c in part.items():
            if r in idx:
                a[idx[r]] = c
        arrs.append(a)
    if not arrs:
        return {}
    stab: dict[tuple[str, str], float] = {}
    candidates = set()
    for a in arrs:
        bycomm = defaultdict(list)
        for i, c in enumerate(a):
            if c >= 0:
                bycomm[int(c)].append(i)
        for ids in bycomm.values():
            for i in range(len(ids)):
                for j in range(i + 1, len(ids)):
                    candidates.add((ids[i], ids[j]))
    for i, j in candidates:
        same = 0
        valid = 0
        for a in arrs:
            ai, aj = int(a[i]), int(a[j])
            if ai >= 0 and aj >= 0:
                valid += 1
                if ai == aj:
                    same += 1
        if valid > 0:
            stab[(nodes[i], nodes[j])] = same / valid
    return stab


def _topics_from_stability(stab: dict, nodes: list[str], threshold: float) -> list[set]:
    g = nx.Graph()
    g.add_nodes_from(nodes)
    for (a, b), s in stab.items():
        if s >= threshold:
            g.add_edge(a, b, weight=s)
    topics = [c for c in nx.connected_components(g) if len(c) >= 2]
    topics.sort(key=len, reverse=True)
    return topics


def _ppmi_distributional(g: nx.Graph, nodes: list[str], dims: int = DIST_SVD_DIMS):
    n = len(nodes)
    idx = {r: i for i, r in enumerate(nodes)}
    deg = np.zeros(n, dtype=np.float64)
    for u, v, d in g.edges(data=True):
        w = d.get("weight", 1)
        deg[idx[u]] += w
        deg[idx[v]] += w
    total = deg.sum()
    if total == 0:
        return np.zeros((n, dims)), idx
    rows, cols, vals = [], [], []
    for u, v, d in g.edges(data=True):
        w = d.get("weight", 1)
        i, j = idx[u], idx[v]
        if deg[i] == 0 or deg[j] == 0 or w == 0:
            continue
        p_ij = w / total
        p_i = deg[i] / total
        p_j = deg[j] / total
        pmi = math.log(p_ij / (p_i * p_j)) if (p_i > 0 and p_j > 0) else 0
        if pmi > 0:
            rows.extend([i, j])
            cols.extend([j, i])
            vals.extend([pmi, pmi])
    if not vals:
        return np.zeros((n, dims)), idx
    from scipy.sparse import csr_matrix
    from scipy.sparse.linalg import svds
    M = csr_matrix((vals, (rows, cols)), shape=(n, n))
    k = min(dims, min(M.shape) - 1)
    if k < 2:
        return np.zeros((n, dims)), idx
    try:
        U, S, _ = svds(M.astype(np.float32), k=k)
        emb = U * S
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        norms[norms == 0] = 1
        emb = emb / norms
        if emb.shape[1] < dims:
            pad = np.zeros((n, dims - emb.shape[1]), dtype=emb.dtype)
            emb = np.concatenate([emb, pad], axis=1)
        return emb, idx
    except Exception:
        return np.zeros((n, dims)), idx


# ═══════════════════════════════════════════════════════════════════════
# FOCUSED (fast, per-query) computation
# ═══════════════════════════════════════════════════════════════════════
def _ego_network_nodes(g_full: nx.Graph, input_roots: list[str],
                       top_partners: int, hop2_partners: int,
                       max_nodes: int) -> set[str]:
    """Walk out 2 hops from each input root, keeping top-weighted partners."""
    keep: set[str] = set()
    # Step 1: input roots that exist in the graph
    seeds = [r for r in input_roots if r in g_full.nodes]
    keep.update(seeds)
    if not seeds:
        return keep
    # Step 2: top-K partners per input root
    hop1 = set()
    for r in seeds:
        nbrs = sorted(g_full[r].items(),
                      key=lambda kv: -kv[1].get("weight", 0))[:top_partners]
        for n, _ in nbrs:
            hop1.add(n)
    keep.update(hop1)
    if len(keep) >= max_nodes:
        return keep
    # Step 3: top-M partners of hop-1 nodes (capped)
    hop2 = set()
    for r in hop1:
        nbrs = sorted(g_full[r].items(),
                      key=lambda kv: -kv[1].get("weight", 0))[:hop2_partners]
        for n, _ in nbrs:
            if n not in keep:
                hop2.add(n)
            if len(keep) + len(hop2) >= max_nodes:
                break
        if len(keep) + len(hop2) >= max_nodes:
            break
    keep.update(list(hop2)[: max(0, max_nodes - len(keep))])
    return keep


def compute_for_roots(corpus, input_roots: list[str], progress_cb=None) -> dict:
    """Fast per-query topic modelling on the ego-network around input_roots."""
    t0 = time.time()
    if progress_cb:
        progress_cb(0.03, "Reading corpus index")

    ayah_to_roots, root_freq = _build_index(corpus)
    kept = {r for r, c in root_freq.items() if c >= MIN_ROOT_FREQUENCY}

    if progress_cb:
        progress_cb(0.15, f"Building full corpus graph ({len(kept):,} roots)")
    g_full = _build_graph(ayah_to_roots, root_freq, kept)

    if progress_cb:
        progress_cb(0.30, f"Walking 2-hop neighbourhood around {', '.join(input_roots)}")
    ego_nodes = _ego_network_nodes(
        g_full, input_roots,
        top_partners=FOCUSED_TOP_PARTNERS,
        hop2_partners=FOCUSED_HOP2_PARTNERS,
        max_nodes=FOCUSED_MAX_NODES,
    )
    if not ego_nodes:
        return _empty_result(input_roots, t0)
    g = g_full.subgraph(ego_nodes).copy()
    nodes = sorted(g.nodes)

    if progress_cb:
        progress_cb(0.40, f"Louvain stability on {len(nodes)} nodes "
                          f"({FOCUSED_N_SEEDS}x{len(FOCUSED_RESOLUTIONS)} runs)")
    partitions = _louvain_runs(
        g, FOCUSED_N_SEEDS, FOCUSED_RESOLUTIONS,
        progress_cb=progress_cb, prog_start=0.40, prog_span=0.40,
    )

    if progress_cb:
        progress_cb(0.82, "Computing co-clustering stability")
    stab = _coclustering_stability(partitions, nodes)
    topics = _topics_from_stability(stab, nodes, FOCUSED_STABILITY_THRESHOLD)

    if progress_cb:
        progress_cb(0.92, "Distributional similarity (PPMI + SVD)")
    emb, idx = _ppmi_distributional(g, nodes, DIST_SVD_DIMS)

    if progress_cb:
        progress_cb(1.0, "Done")

    return {
        "mode": "focused",
        "version": CACHE_VERSION,
        "compute_seconds": time.time() - t0,
        "input_roots": list(input_roots),
        "n_seeds": FOCUSED_N_SEEDS,
        "resolutions": FOCUSED_RESOLUTIONS,
        "stability_threshold": FOCUSED_STABILITY_THRESHOLD,
        "n_nodes": len(nodes),
        "n_edges": g.number_of_edges(),
        "nodes": nodes,
        "stability": stab,
        "topics": [list(t) for t in topics],
        "embeddings": emb,
        "embedding_idx": idx,
    }


def _empty_result(input_roots, t0):
    return {
        "mode": "focused", "version": CACHE_VERSION,
        "compute_seconds": time.time() - t0,
        "input_roots": list(input_roots),
        "n_nodes": 0, "n_edges": 0, "nodes": [],
        "stability": {}, "topics": [], "embeddings": None, "embedding_idx": {},
        "stability_threshold": FOCUSED_STABILITY_THRESHOLD,
        "n_seeds": FOCUSED_N_SEEDS, "resolutions": FOCUSED_RESOLUTIONS,
    }


# ═══════════════════════════════════════════════════════════════════════
# GLOBAL compute (slow; kept for the optional Advanced view)
# ═══════════════════════════════════════════════════════════════════════
def compute(corpus, force: bool = False, progress_cb=None) -> dict:
    if CACHE_PATH.exists() and not force:
        try:
            with open(CACHE_PATH, "rb") as f:
                cached = pickle.load(f)
            if (cached.get("version") == CACHE_VERSION
                    and cached.get("n_nodes", 0) > 0):
                return cached
        except Exception:
            pass

    t0 = time.time()
    if progress_cb:
        progress_cb(0.05, "Reading corpus index")
    ayah_to_roots, root_freq = _build_index(corpus)
    kept = {r for r, c in root_freq.items() if c >= MIN_ROOT_FREQUENCY}

    if progress_cb:
        progress_cb(0.10, f"Building full corpus graph ({len(kept):,} roots)")
    g = _build_graph(ayah_to_roots, root_freq, kept)
    nodes = sorted(g.nodes)
    if not nodes:
        return _empty_result_global(t0)

    if progress_cb:
        progress_cb(0.20, f"Louvain ({N_SEEDS}x{len(RESOLUTIONS)} runs)")
    partitions = _louvain_runs(
        g, N_SEEDS, RESOLUTIONS,
        progress_cb=progress_cb, prog_start=0.20, prog_span=0.55,
    )

    if progress_cb:
        progress_cb(0.78, "Co-clustering stability")
    stab = _coclustering_stability(partitions, nodes)
    topics = _topics_from_stability(stab, nodes, STABILITY_THRESHOLD)

    if progress_cb:
        progress_cb(0.92, "PPMI + SVD")
    emb, idx = _ppmi_distributional(g, nodes, DIST_SVD_DIMS)

    cache = {
        "mode": "global",
        "version": CACHE_VERSION,
        "compute_seconds": time.time() - t0,
        "n_seeds": N_SEEDS, "resolutions": RESOLUTIONS,
        "stability_threshold": STABILITY_THRESHOLD,
        "n_nodes": len(nodes), "n_edges": g.number_of_edges(),
        "nodes": nodes, "root_freq": root_freq,
        "stability": stab, "topics": [list(t) for t in topics],
        "embeddings": emb, "embedding_idx": idx,
    }
    if progress_cb:
        progress_cb(1.0, "Done")
    try:
        with open(CACHE_PATH, "wb") as f:
            pickle.dump(cache, f)
    except Exception:
        pass
    return cache


def _empty_result_global(t0):
    return {
        "mode": "global", "version": CACHE_VERSION,
        "compute_seconds": time.time() - t0,
        "n_seeds": N_SEEDS, "resolutions": RESOLUTIONS,
        "stability_threshold": STABILITY_THRESHOLD,
        "n_nodes": 0, "n_edges": 0, "nodes": [], "root_freq": {},
        "stability": {}, "topics": [], "embeddings": None, "embedding_idx": {},
    }


# ═══════════════════════════════════════════════════════════════════════
# Query API (works on either cache shape)
# ═══════════════════════════════════════════════════════════════════════
def get_topic_for_root(cache: dict, root: str) -> tuple[int, list[str], float]:
    for i, members in enumerate(cache.get("topics", [])):
        if root in members:
            stab = cache.get("stability", {})
            vals = []
            for m in members:
                if m == root:
                    continue
                key = (root, m) if (root, m) in stab else (m, root)
                if key in stab:
                    vals.append(stab[key])
            mean_s = float(np.mean(vals)) if vals else 0.0
            return i, list(members), mean_s
    return -1, [], 0.0


def distributional_neighbours(cache: dict, root: str, k: int = 10) -> list[tuple[str, float]]:
    idx = cache.get("embedding_idx", {})
    emb = cache.get("embeddings")
    if emb is None or root not in idx:
        return []
    i = idx[root]
    v = emb[i]
    sims = emb @ v
    nodes = cache.get("nodes", [])
    out = []
    for j in np.argsort(-sims):
        if j == i:
            continue
        out.append((nodes[j], float(sims[j])))
        if len(out) >= k:
            break
    return out


def quadrant_lists(cache: dict, root: str, k: int = 8,
                   high_s1: float = 0.5, high_s2: float = 0.5) -> dict:
    stab = cache.get("stability", {})
    idx = cache.get("embedding_idx", {})
    emb = cache.get("embeddings")
    nodes = cache.get("nodes", [])
    if root not in idx or emb is None:
        return {"core": [], "contrastive": [], "distributional_synonym": [], "unrelated": []}
    i = idx[root]
    v = emb[i]
    cos = emb @ v
    out = {"core": [], "contrastive": [], "distributional_synonym": [], "unrelated": []}
    for j, other in enumerate(nodes):
        if other == root:
            continue
        key = (root, other) if (root, other) in stab else (other, root)
        s1 = stab.get(key, 0.0)
        s2 = float(cos[j])
        if s1 >= high_s1 and s2 >= high_s2:
            out["core"].append((other, s1, s2))
        elif s1 >= high_s1 and s2 < high_s2:
            out["contrastive"].append((other, s1, s2))
        elif s1 < high_s1 and s2 >= high_s2:
            out["distributional_synonym"].append((other, s1, s2))
        else:
            out["unrelated"].append((other, s1, s2))
    for q in out:
        out[q].sort(key=lambda t: -(t[1] + t[2]))
        out[q] = out[q][:k]
    return out
