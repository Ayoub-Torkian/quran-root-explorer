# re-deploy 1779671310
"""surface_divergence.py — detects roots whose surface forms have
statistically distinct partner-distributions (e.g. a root that produces
one positive form and one negative). Strictly data-driven; no curated
split list."""
from __future__ import annotations

import math
import os
import pickle
import time
from collections import defaultdict
from pathlib import Path

import numpy as np


CACHE_VERSION = 2
MIN_FORM_FREQUENCY = 4
JSD_SPLIT_THRESHOLD = 0.30
BOOTSTRAP_ROUNDS = 20
BOOTSTRAP_STABILITY = 0.60

_CACHE_DIR = Path(os.environ.get("ANALYTICS_DATA_DIR", "/data"))
try:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
except PermissionError:
    _CACHE_DIR = Path("./.topics_cache")
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_PATH = _CACHE_DIR / "surface_divergence_cache.pkl"


def _jsd(p: np.ndarray, q: np.ndarray) -> float:
    p = p / (p.sum() + 1e-12)
    q = q / (q.sum() + 1e-12)
    m = 0.5 * (p + q)
    def kl(a, b):
        mask = (a > 0) & (b > 0)
        return float(np.sum(a[mask] * np.log(a[mask] / b[mask])))
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)


def _build_indices(corpus):
    """Reads the real corpus structure (df + root_tokens + surface_tokens).
    Returns: ayah_to_roots, root_to_ayahs, form_ayahs[(root, sform)] = ayah list."""
    from analysis import normalize_letters

    ayah_to_roots: dict[int, set[str]] = defaultdict(set)
    root_to_ayahs: dict[str, set[int]] = defaultdict(set)
    form_ayahs: dict[tuple[str, str], list[int]] = defaultdict(list)

    root_tokens = getattr(corpus, "root_tokens", None) or []
    surface_tokens = getattr(corpus, "surface_tokens", None) or []

    for i, toks in enumerate(root_tokens):
        sf_list = surface_tokens[i] if i < len(surface_tokens) else []
        for j, t in enumerate(toks):
            if not t:
                continue
            r = normalize_letters(t)
            if not r:
                continue
            sf = sf_list[j] if j < len(sf_list) and sf_list[j] else r
            ayah_to_roots[i].add(r)
            root_to_ayahs[r].add(i)
            form_ayahs[(r, sf)].append(i)
    return ayah_to_roots, root_to_ayahs, form_ayahs


def _partner_vector(form_ayahs_list, ayah_to_roots, root_universe, self_root):
    idx = {r: i for i, r in enumerate(root_universe)}
    v = np.zeros(len(root_universe), dtype=np.float64)
    for a in form_ayahs_list:
        for partner in ayah_to_roots.get(a, ()):
            if partner == self_root:
                continue
            j = idx.get(partner)
            if j is not None:
                v[j] += 1.0
    return v


def compute(corpus, force: bool = False) -> dict:
    if CACHE_PATH.exists() and not force:
        try:
            with open(CACHE_PATH, "rb") as f:
                cached = pickle.load(f)
            if (cached.get("version") == CACHE_VERSION
                    and cached.get("n_roots_scanned", 0) > 0):
                return cached
        except Exception:
            pass

    t0 = time.time()
    ayah_to_roots, root_to_ayahs, form_ayahs = _build_indices(corpus)
    root_universe = sorted([r for r, ays in root_to_ayahs.items() if len(ays) >= 2])
    rng = np.random.default_rng(0)

    if not root_universe:
        return {
            "version": CACHE_VERSION, "computed_at": time.time(),
            "compute_seconds": time.time() - t0,
            "n_roots_scanned": 0, "n_splits": 0, "splits": [],
            "jsd_threshold": JSD_SPLIT_THRESHOLD,
            "stability_threshold": BOOTSTRAP_STABILITY,
            "min_form_frequency": MIN_FORM_FREQUENCY,
        }

    splits = []
    for root in root_universe:
        forms = [
            (sf, ayahs) for (rt, sf), ayahs in form_ayahs.items()
            if rt == root and len(ayahs) >= MIN_FORM_FREQUENCY
        ]
        if len(forms) < 2:
            continue
        vecs = {sf: _partner_vector(ays, ayah_to_roots, root_universe, root)
                for sf, ays in forms}
        sfs = list(vecs.keys())
        n = len(sfs)
        jsd_mat = np.zeros((n, n))
        for i in range(n):
            for j in range(i + 1, n):
                d = _jsd(vecs[sfs[i]], vecs[sfs[j]])
                jsd_mat[i, j] = jsd_mat[j, i] = d
        max_jsd = float(jsd_mat.max())
        if max_jsd < JSD_SPLIT_THRESHOLD:
            continue
        from scipy.cluster.hierarchy import linkage, fcluster
        from scipy.spatial.distance import squareform
        try:
            condensed = squareform(jsd_mat, checks=False)
            Z = linkage(condensed, method="average")
            labels = fcluster(Z, t=JSD_SPLIT_THRESHOLD, criterion="distance")
        except Exception:
            continue
        if len(set(labels)) < 2:
            continue
        stable_count = 0
        for _ in range(BOOTSTRAP_ROUNDS):
            try:
                vecs_b = {}
                for sf, ays in forms:
                    sampled = rng.choice(ays, size=len(ays), replace=True)
                    vecs_b[sf] = _partner_vector(list(sampled), ayah_to_roots,
                                                  root_universe, root)
                jsd_b = np.zeros((n, n))
                for i in range(n):
                    for j in range(i + 1, n):
                        d = _jsd(vecs_b[sfs[i]], vecs_b[sfs[j]])
                        jsd_b[i, j] = jsd_b[j, i] = d
                cond_b = squareform(jsd_b, checks=False)
                Z_b = linkage(cond_b, method="average")
                lab_b = fcluster(Z_b, t=JSD_SPLIT_THRESHOLD, criterion="distance")
                from collections import defaultdict as _dd
                pa, pb = _dd(set), _dd(set)
                for i, l in enumerate(labels):
                    pa[l].add(i)
                for i, l in enumerate(lab_b):
                    pb[l].add(i)
                pa_sets = {frozenset(s) for s in pa.values()}
                pb_sets = {frozenset(s) for s in pb.values()}
                if pa_sets == pb_sets:
                    stable_count += 1
            except Exception:
                continue
        stability = stable_count / BOOTSTRAP_ROUNDS
        if stability < BOOTSTRAP_STABILITY:
            continue
        clusters = defaultdict(list)
        for i, l in enumerate(labels):
            clusters[int(l)].append(sfs[i])
        cluster_top_partners = {}
        for cl_id, cl_forms in clusters.items():
            agg = np.zeros(len(root_universe))
            for sf in cl_forms:
                agg += vecs[sf]
            top_idx = np.argsort(-agg)[:8]
            cluster_top_partners[cl_id] = [
                (root_universe[i], int(agg[i])) for i in top_idx if agg[i] > 0
            ]
        splits.append({
            "root": root,
            "n_forms": n,
            "max_jsd": max_jsd,
            "stability": stability,
            "clusters": dict(clusters),
            "cluster_top_partners": cluster_top_partners,
        })

    splits.sort(key=lambda s: -s["max_jsd"])
    cache = {
        "version": CACHE_VERSION,
        "computed_at": time.time(),
        "compute_seconds": time.time() - t0,
        "n_roots_scanned": len(root_universe),
        "n_splits": len(splits),
        "splits": splits,
        "jsd_threshold": JSD_SPLIT_THRESHOLD,
        "stability_threshold": BOOTSTRAP_STABILITY,
        "min_form_frequency": MIN_FORM_FREQUENCY,
    }
    try:
        with open(CACHE_PATH, "wb") as f:
            pickle.dump(cache, f)
    except Exception:
        pass
    return cache


def is_split(cache: dict, root: str) -> bool:
    for s in cache.get("splits", []):
        if s["root"] == root:
            return True
    return False


def get_split(cache: dict, root: str) -> dict | None:
    for s in cache.get("splits", []):
        if s["root"] == root:
            return s
    return None
