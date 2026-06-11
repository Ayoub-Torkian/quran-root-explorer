"""Extended statistical analytics for the Quran Root Explorer.

Appended into analysis.py. Functions in this module assume the Corpus dataclass
and helper functions (search_root, normalize_letters, COL_*) are already imported.
"""
from __future__ import annotations

import math
import statistics
from collections import Counter, defaultdict
from itertools import combinations

import networkx as nx
import pandas as pd


def _key_fn(normalize: bool):
    if normalize:
        from analysis import normalize_letters
        return normalize_letters
    return lambda t: t


# ---------------------------------------------------------------------------
# Frequency & dispersion
# ---------------------------------------------------------------------------
def frequency_analysis(corpus, input_roots, normalize):
    """Per-root frequency rank, percentile, TF, dispersion."""
    from analysis import search_root
    freqs = corpus.freq_norm if normalize else corpus.freq_exact
    sorted_counts = sorted(freqs.values(), reverse=True)
    total = sum(freqs.values())
    rank_of = {r: i + 1 for i, (r, _) in enumerate(
        sorted(freqs.items(), key=lambda kv: -kv[1]))}
    rows = []
    for q in input_roots:
        c = freqs.get(q, 0)
        ayahs = search_root(corpus, q, normalize)
        # surah-wise distribution
        surah_counts = Counter()
        for i in ayahs:
            surah_counts[int(corpus.df.iloc[i]["ش  سوره"])] += 1
        n_surahs = len(surah_counts)
        # Juilland's D dispersion
        if n_surahs >= 2:
            mean = sum(surah_counts.values()) / 114
            variance = sum((surah_counts.get(s, 0) - mean) ** 2 for s in range(1, 115)) / 114
            stdev = math.sqrt(variance)
            cv = stdev / mean if mean else 0
            juilland_d = max(0.0, 1 - cv / math.sqrt(114 - 1))
        else:
            juilland_d = 0.0
        # entropy across surahs (Shannon, base 2)
        ps = [v / c for v in surah_counts.values()] if c > 0 else []
        H = -sum(p * math.log2(p) for p in ps if p > 0)
        H_max = math.log2(n_surahs) if n_surahs > 1 else 1.0
        H_norm = H / H_max if H_max else 0.0
        rows.append({
            "Input Root": q,
            "Frequency": c,
            "Rank (1=top)": rank_of.get(q, "—"),
            "% of all root tokens": round(100 * c / max(total, 1), 4),
            "TF (per 1000 ayahs)": round(1000 * c / max(corpus.n_ayahs, 1), 2),
            "Surahs covered": n_surahs,
            "Juilland D (0–1)": round(juilland_d, 4),
            "Entropy (bits)": round(H, 3),
            "Entropy normalized": round(H_norm, 4),
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Surah importance & TF-IDF
# ---------------------------------------------------------------------------
def surah_tfidf(corpus, input_roots, normalize, top_per_root=10):
    """TF-IDF: which surahs are most characteristic for each input root.
    TF = root_count_in_surah / total_roots_in_surah
    IDF = log(total_surahs / surahs_with_root)
    """
    from analysis import search_root
    K = _key_fn(normalize)
    n_surahs_total = 114

    # corpus-wide: surah -> set of unique roots present, total root tokens
    surah_root_set = defaultdict(set)
    surah_total = defaultdict(int)
    for i, toks in enumerate(corpus.root_tokens):
        s = int(corpus.df.iloc[i]["ش  سوره"])
        surah_total[s] += len(toks)
        for t in toks:
            surah_root_set[s].add(K(t))

    rows = []
    for q in input_roots:
        # docs (surahs) that contain q
        surahs_with_q = sum(1 for s in range(1, n_surahs_total + 1)
                            if q in surah_root_set.get(s, set()))
        idf = math.log((n_surahs_total + 1) / max(surahs_with_q, 1) + 1)
        # count q per surah
        per_surah = Counter()
        for i in search_root(corpus, q, normalize):
            per_surah[int(corpus.df.iloc[i]["ش  سوره"])] += 1
        # TF-IDF per surah
        scored = []
        for s, cnt in per_surah.items():
            tf = cnt / max(surah_total.get(s, 1), 1)
            scored.append((s, cnt, round(tf * idf, 6)))
        scored.sort(key=lambda x: -x[2])
        for s, cnt, score in scored[:top_per_root]:
            name = corpus.df[corpus.df["ش  سوره"] == s]["اسم سوره"].iloc[0]
            rows.append({"Input Root": q, "Surah #": s, "Surah Name": name,
                         "Hits in surah": cnt, "TF-IDF": score, "IDF": round(idf, 3)})
    return pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=["Input Root", "Surah #", "Surah Name", "Hits in surah", "TF-IDF", "IDF"])


def surah_role(corpus, input_roots, normalize):
    """For each surah that contains at least one input root, score its
    role/importance for the query: how many input roots, how many hits,
    proportion of surah devoted to the query."""
    from analysis import search_root
    K = _key_fn(normalize)
    surah_total = defaultdict(int)
    for i, toks in enumerate(corpus.root_tokens):
        s = int(corpus.df.iloc[i]["ش  سوره"])
        surah_total[s] += len(toks)

    hits_per_surah = defaultdict(lambda: defaultdict(int))
    for q in input_roots:
        for i in search_root(corpus, q, normalize):
            s = int(corpus.df.iloc[i]["ش  سوره"])
            hits_per_surah[s][q] += 1

    rows = []
    for s, perq in hits_per_surah.items():
        name = corpus.df[corpus.df["ش  سوره"] == s]["اسم سوره"].iloc[0]
        n_input_roots = len(perq)
        total_hits = sum(perq.values())
        share = total_hits / max(surah_total[s], 1)
        rows.append({"Surah #": s, "Surah Name": name,
                     "Input roots present": n_input_roots,
                     "Total hits": total_hits,
                     "Surah length (root tokens)": surah_total[s],
                     "Share of surah from input roots": round(100 * share, 3),
                     "Importance score": round(n_input_roots * total_hits / max(surah_total[s], 1) * 100, 3)})
    df = pd.DataFrame(rows)
    return df.sort_values("Importance score", ascending=False).reset_index(drop=True) if not df.empty else df


# ---------------------------------------------------------------------------
# Pairwise: PMI, conditional probability, Jaccard, Dice
# ---------------------------------------------------------------------------
def _ayahs_per_root(corpus, input_roots, normalize):
    from analysis import search_root
    return {q: set(search_root(corpus, q, normalize)) for q in input_roots}


def pmi_matrix(corpus, input_roots, normalize):
    """Pointwise Mutual Information matrix between input roots.
    PMI(A,B) = log2( P(A,B) / (P(A)*P(B)) ).
    Computed over the ayah-occurrence space (N = corpus size).
    """
    ayahs = _ayahs_per_root(corpus, input_roots, normalize)
    N = corpus.n_ayahs
    m = pd.DataFrame(0.0, index=input_roots, columns=input_roots, dtype=float)
    for a in input_roots:
        for b in input_roots:
            pa = len(ayahs[a]) / N if N else 0
            pb = len(ayahs[b]) / N if N else 0
            pab = len(ayahs[a] & ayahs[b]) / N if N else 0
            if pab > 0 and pa > 0 and pb > 0:
                m.loc[a, b] = round(math.log2(pab / (pa * pb)), 4)
            else:
                m.loc[a, b] = float("nan")
    return m


def conditional_probability(corpus, input_roots, normalize):
    """P(B|A) — probability of root B given that A is in the ayah.
    Rows are 'given' root A, columns are B."""
    ayahs = _ayahs_per_root(corpus, input_roots, normalize)
    m = pd.DataFrame(0.0, index=input_roots, columns=input_roots, dtype=float)
    for a in input_roots:
        for b in input_roots:
            denom = len(ayahs[a])
            m.loc[a, b] = round(len(ayahs[a] & ayahs[b]) / denom, 4) if denom else 0.0
    return m


def jaccard_matrix(corpus, input_roots, normalize):
    ayahs = _ayahs_per_root(corpus, input_roots, normalize)
    m = pd.DataFrame(0.0, index=input_roots, columns=input_roots, dtype=float)
    for a in input_roots:
        for b in input_roots:
            u = len(ayahs[a] | ayahs[b])
            m.loc[a, b] = round(len(ayahs[a] & ayahs[b]) / u, 4) if u else 0.0
    return m


def dice_matrix(corpus, input_roots, normalize):
    ayahs = _ayahs_per_root(corpus, input_roots, normalize)
    m = pd.DataFrame(0.0, index=input_roots, columns=input_roots, dtype=float)
    for a in input_roots:
        for b in input_roots:
            denom = len(ayahs[a]) + len(ayahs[b])
            m.loc[a, b] = round(2 * len(ayahs[a] & ayahs[b]) / denom, 4) if denom else 0.0
    return m


# ---------------------------------------------------------------------------
# Hypergeometric enrichment per surah
# ---------------------------------------------------------------------------
def _log_binom(n, k):
    if k < 0 or k > n:
        return float("-inf")
    return (math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1))


def _hypergeom_p_at_least(k, K, n, N):
    """P(X >= k) for hypergeometric Hypergeometric(N, K, n).
    Returns p-value. Computed via tail-sum of log-binomial. N=corpus, K=ayahs_with_root,
    n=surah ayah count, k=observed."""
    if k <= 0:
        return 1.0
    total = float("-inf")
    log_denom = _log_binom(N, n)
    for x in range(k, min(K, n) + 1):
        log_p = _log_binom(K, x) + _log_binom(N - K, n - x) - log_denom
        if total == float("-inf"):
            total = log_p
        else:
            # logaddexp
            a, b = max(total, log_p), min(total, log_p)
            total = a + math.log1p(math.exp(b - a))
    return math.exp(total) if total > float("-inf") else 0.0


def surah_enrichment(corpus, input_roots, normalize, max_p=0.5):
    """Hypergeometric enrichment: for each (root, surah) pair, is the root
    over-represented in that surah vs random? Returns rows with p-value.
    """
    from analysis import search_root
    N = corpus.n_ayahs
    # ayahs per surah
    surah_size = corpus.df.groupby("ش  سوره").size().to_dict()
    rows = []
    for q in input_roots:
        idx = search_root(corpus, q, normalize)
        K = len(idx)
        if K == 0:
            continue
        # observed in each surah
        per_surah = Counter()
        for i in idx:
            per_surah[int(corpus.df.iloc[i]["ش  سوره"])] += 1
        for s, k in per_surah.items():
            n = surah_size.get(s, 0)
            expected = K * n / N if N else 0
            p = _hypergeom_p_at_least(k, K, n, N)
            if p > max_p:
                continue
            name = corpus.df[corpus.df["ش  سوره"] == s]["اسم سوره"].iloc[0]
            rows.append({
                "Input Root": q, "Surah #": s, "Surah Name": name,
                "Observed": k, "Expected": round(expected, 2),
                "Enrichment (obs/exp)": round(k / expected, 3) if expected else float("inf"),
                "p-value": p,
                "-log10(p)": round(-math.log10(p), 3) if p > 0 else 99.0,
            })
    df = pd.DataFrame(rows)
    return df.sort_values("p-value").reset_index(drop=True) if not df.empty else df


# ---------------------------------------------------------------------------
# Position categorization
# ---------------------------------------------------------------------------
def position_categorization(corpus, input_roots, normalize):
    """Categorize each occurrence into start/middle/end thirds of the ayah."""
    from analysis import search_root
    K = _key_fn(normalize)
    rows = []
    for q in input_roots:
        counts = {"start (0–33%)": 0, "middle (33–66%)": 0, "end (66–100%)": 0}
        for i in search_root(corpus, q, normalize):
            toks = corpus.root_tokens[i]
            n = len(toks)
            for j, t in enumerate(toks):
                if K(t) == q:
                    rel = j / max(n - 1, 1) if n > 1 else 0.5
                    if rel < 1/3:
                        counts["start (0–33%)"] += 1
                    elif rel < 2/3:
                        counts["middle (33–66%)"] += 1
                    else:
                        counts["end (66–100%)"] += 1
        total = sum(counts.values()) or 1
        rows.append({
            "Input Root": q,
            "Start %": round(100 * counts["start (0–33%)"] / total, 1),
            "Middle %": round(100 * counts["middle (33–66%)"] / total, 1),
            "End %": round(100 * counts["end (66–100%)"] / total, 1),
            "Start count": counts["start (0–33%)"],
            "Middle count": counts["middle (33–66%)"],
            "End count": counts["end (66–100%)"],
        })
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Exclusive / hapax partners
# ---------------------------------------------------------------------------
def exclusive_partners(corpus, input_roots, normalize, max_other=0):
    """Partners that co-occur with input roots but almost nowhere else.
    max_other = how many ayahs OUTSIDE the input-root ayahs the partner may appear in."""
    from analysis import search_root
    K = _key_fn(normalize)
    matched = set()
    for q in input_roots:
        matched.update(search_root(corpus, q, normalize))
    # Count each non-input root's total ayahs vs its in-matched-set ayahs
    total_in = Counter()
    total_corpus = Counter()
    input_set = set(input_roots)
    for i, toks in enumerate(corpus.root_tokens):
        keys = {K(t) for t in toks} - input_set
        for k in keys:
            total_corpus[k] += 1
            if i in matched:
                total_in[k] += 1
    rows = []
    for partner, in_count in total_in.items():
        out_count = total_corpus[partner] - in_count
        if out_count <= max_other and in_count >= 2:
            rows.append({"Exclusive Partner": partner, "Ayahs with input": in_count,
                         "Other ayahs": out_count, "Exclusivity": round(in_count / (in_count + out_count), 4)})
    df = pd.DataFrame(rows)
    return df.sort_values("Ayahs with input", ascending=False).reset_index(drop=True) if not df.empty else df


# ---------------------------------------------------------------------------
# Network: PageRank, k-core, ego density
# ---------------------------------------------------------------------------
def network_extras(g):
    if g.number_of_nodes() == 0:
        return pd.DataFrame(columns=["Root", "PageRank", "k-core", "Ego density", "Triangles@node"])
    try:
        pr = nx.pagerank(g, weight="weight")
    except Exception:
        pr = {n: 0.0 for n in g.nodes()}
    try:
        kc = nx.core_number(g)
    except Exception:
        kc = {n: 0 for n in g.nodes()}
    tri = nx.triangles(g)
    rows = []
    for n in g.nodes():
        ego = nx.ego_graph(g, n)
        ego_d = nx.density(ego) if ego.number_of_nodes() > 1 else 0.0
        rows.append({
            "Root": n,
            "PageRank": round(pr.get(n, 0), 5),
            "k-core": kc.get(n, 0),
            "Ego density": round(ego_d, 4),
            "Triangles@node": tri.get(n, 0),
            "Is Input": g.nodes[n].get("is_input", False),
        })
    return pd.DataFrame(rows).sort_values("PageRank", ascending=False).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Cumulative trajectory across surah order
# ---------------------------------------------------------------------------
def cumulative_trajectory(corpus, input_roots, normalize):
    """Cumulative ayah-hits across surah 1..114, per input root."""
    from analysis import search_root
    rows = []
    for q in input_roots:
        per_surah = Counter()
        for i in search_root(corpus, q, normalize):
            per_surah[int(corpus.df.iloc[i]["ش  سوره"])] += 1
        cumulative = 0
        for s in range(1, 115):
            cumulative += per_surah.get(s, 0)
            rows.append({"Input Root": q, "Surah #": s, "Cumulative hits": cumulative})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Hierarchical clustering of input roots (single-linkage over Jaccard distance)
# ---------------------------------------------------------------------------
def cluster_input_roots(jaccard_df):
    """Return a dendrogram-ready linkage matrix (list of merges)."""
    if jaccard_df.empty or len(jaccard_df) < 2:
        return None
    try:
        import numpy as np
        from scipy.cluster.hierarchy import linkage
        # distance = 1 - similarity
        dist = 1 - jaccard_df.values
        n = dist.shape[0]
        condensed = []
        for i in range(n):
            for j in range(i + 1, n):
                condensed.append(dist[i, j])
        Z = linkage(condensed, method="average")
        return Z
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Cross-validation summary
# ---------------------------------------------------------------------------
def cross_validation(corpus, input_roots, normalize, R):
    """Run consistency checks and return a table of findings."""
    from analysis import search_root
    findings = []
    # 1. total matched ayahs
    union_ayahs = set()
    for q in input_roots:
        union_ayahs.update(search_root(corpus, q, normalize))
    findings.append({"Check": "Ayahs matched (union of inputs)",
                     "Value": len(union_ayahs),
                     "Status": "✓" if len(union_ayahs) == len(R["match_ayahs"]) else "⚠"})
    # 2. per-root ayah count vs occurrences table
    for q in input_roots:
        from_search = len(search_root(corpus, q, normalize))
        sub = R["occurrences"][R["occurrences"]["Input Root"] == q]
        from_occ = sub[["Surah #", "Ayah #"]].drop_duplicates().shape[0]
        findings.append({
            "Check": f"Ayahs containing root '{q}'",
            "Value": f"{from_search} (index) vs {from_occ} (occurrences)",
            "Status": "✓" if from_search == from_occ else "⚠",
        })
    # 3. Sum of surface form occurrences should be >= ayah count
    sf = R["sforms"]
    for q in input_roots:
        sub = sf[sf["Input Root"] == q]
        total_sf = int(sub["Occurrences"].sum()) if not sub.empty else 0
        n_ayahs = len(search_root(corpus, q, normalize))
        findings.append({
            "Check": f"Surface-form total >= ayah count for '{q}'",
            "Value": f"{total_sf} surface vs {n_ayahs} ayahs",
            "Status": "✓" if total_sf >= n_ayahs else "⚠",
        })
    # 4. Co-occurrence partner consistency
    findings.append({
        "Check": "Unique partner count matches cooccurrence_table size",
        "Value": f"{len(R['partners'])} vs {len(R['cooc_tbl'])}",
        "Status": "✓" if len(R["partners"]) == len(R["cooc_tbl"]) else "⚠",
    })
    return pd.DataFrame(findings)
