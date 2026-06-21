"""Semantic design-feature engine — characterizes each root/verse's place in the Qur'an's
DESIGN (descriptive feature engineering, never a shuffle-null hunt). Built ON-CORPUS:
PPMI co-occurrence -> truncated SVD embedding (Levy-Goldberg ≈ word2vec), pure numpy,
deployable, cached. Powers: meaning-based related-verses + concept navigation (the network
as a guided study path). Instrument validated 2026-06-21 (sensible neighbours: زکو≈صلو,
غفر≈رحم, سمو·ءرض·علق≈خلق); see GRADED_FINDINGS_LEDGER.md (semantic verse-order cohesion).
"""
from __future__ import annotations
from collections import Counter
import numpy as np
import analysis as A


def _norm(t):
    return A.normalize_letters(t)


def build(corpus, min_freq=5, k=100):
    """Return the design-feature engine dict. Heavy first call (~few s) -> CACHE it
    (@st.cache_resource keyed on id(corpus))."""
    rtok = corpus.root_tokens
    su = [int(x) for x in corpus.df[A.COL_SURAH].tolist()]
    ay = []
    for x in corpus.df[A.COL_AYAH].tolist():
        try:
            ay.append(int(float(x)))
        except Exception:
            ay.append(0)
    # per-verse normalized content-root sets
    vroots = []
    fr = Counter()
    for toks in rtok:
        s = set(_norm(t) for t in toks if t and t != "-")
        vroots.append(s)
        for r in s:
            fr[r] += 1
    vocab = [r for r, c in fr.items() if c >= min_freq]
    vi = {r: i for i, r in enumerate(vocab)}
    V = len(vocab)
    # symmetric within-verse co-occurrence
    co = np.zeros((V, V), dtype=np.float64)
    for s in vroots:
        idx = sorted(vi[r] for r in s if r in vi)
        for a in range(len(idx)):
            ia = idx[a]
            for b in range(a + 1, len(idx)):
                co[ia, idx[b]] += 1.0
                co[idx[b], ia] += 1.0
    tot = co.sum() or 1.0
    rs = co.sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((co / tot) / ((rs[:, None] / tot) * (rs[None, :] / tot)))
    ppmi = np.nan_to_num(np.maximum(pmi, 0.0))
    # truncated SVD -> k-dim root vectors (unit-normalized)
    U, Sg, _ = np.linalg.svd(ppmi)
    kk = min(k, U.shape[1])
    E = U[:, :kk] * np.sqrt(Sg[:kk])
    En = E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-9)
    # verse vectors = mean of their content-root vectors (unit-normalized)
    refs = [(su[i], ay[i]) for i in range(len(vroots))]
    vv = np.zeros((len(vroots), kk))
    for i, s in enumerate(vroots):
        ix = [vi[r] for r in s if r in vi]
        if ix:
            vv[i] = En[ix].mean(0)
    vvn = vv / (np.linalg.norm(vv, axis=1, keepdims=True) + 1e-9)
    return {
        "vocab": vocab, "vi": vi, "En": En, "k": kk,
        "refs": refs, "vvn": vvn, "vroots": vroots,
        "ref2i": {refs[i]: i for i in range(len(refs))},
        "freq": dict(fr),
    }


def relate(M, s, a, topn=8):
    """Verses nearest (s, a) in meaning, EACH with its DATA-DRIVEN reason so the claim is
    transparent and criticisable:
      (sura, ayah, similarity, shared_roots, bridge)
    where similarity = cosine of the two verses' embedding vectors (the ranking criterion),
    shared_roots = roots literally common to both, and bridge = the single most semantically
    aligned cross-pair (root_in_A, root_in_B, their cosine) — i.e. WHY they're linked even
    when no word is shared. Nothing arbitrary: every field is a measured number the user can check."""
    En, vi = M["En"], M["vi"]
    i = M["ref2i"].get((int(s), int(a)))
    if i is None or not M["vvn"][i].any():
        return []
    sims = M["vvn"] @ M["vvn"][i]
    order = np.argsort(-sims)
    ri = [r for r in M["vroots"][i] if r in vi]
    out = []
    for j in order:
        if j == i:
            continue
        rjset = M["vroots"][j]
        rj = [r for r in rjset if r in vi]
        shared = sorted(set(ri) & rjset)
        bridge = None
        best = -1.0
        for x in ri:
            vx = En[vi[x]]
            for y in rj:
                if y == x:
                    continue
                sc = float(vx @ En[vi[y]])
                if sc > best:
                    best, bridge = sc, (x, y, sc)
        out.append((M["refs"][j][0], M["refs"][j][1], float(sims[j]), shared, bridge))
        if len(out) >= topn:
            break
    return out


def root_neighbors(M, root, topn=12):
    """Meaning-relatives of a root: nearest roots in semantic space. -> [(root, sim), ...]."""
    vi = M["vi"]
    r = _norm(root)
    if r not in vi:
        return []
    v = M["En"][vi[r]]
    sims = M["En"] @ v
    order = np.argsort(-sims)
    out = []
    for j in order:
        if j == vi[r]:
            continue
        out.append((M["vocab"][j], float(sims[j])))
        if len(out) >= topn:
            break
    return out


def related_verses(M, s, a, topn=8):
    """Verses nearest IN MEANING to (s, a) — cross-references keyword search can't find.
    -> [(sura, ayah, sim), ...]."""
    i = M["ref2i"].get((int(s), int(a)))
    if i is None or not M["vvn"][i].any():
        return []
    sims = M["vvn"] @ M["vvn"][i]
    order = np.argsort(-sims)
    out = []
    for j in order:
        if j == i:
            continue
        sj = M["refs"][j]
        out.append((sj[0], sj[1], float(sims[j])))
        if len(out) >= topn:
            break
    return out


def verses_for_concept(M, roots, topn=10):
    """Verses nearest in meaning to a CONCEPT (centroid of one or more root vectors)."""
    vi = M["vi"]
    ix = [vi[_norm(r)] for r in roots if _norm(r) in vi]
    if not ix:
        return []
    c = M["En"][ix].mean(0)
    c = c / (np.linalg.norm(c) + 1e-9)
    sims = M["vvn"] @ c
    order = np.argsort(-sims)
    return [(M["refs"][j][0], M["refs"][j][1], float(sims[j])) for j in order[:topn]]
