# -*- coding: utf-8 -*-
"""Multi-scale structure engine — the root as anchor, one robust method PER scale.

Co-occurrence SATURATES as the window grows (triad closure 53%→98%→100% from āyah→passage→
sūra), so a single instrument cannot span scales. Each scale here uses the operation that
survives it, each measured against the text's own shuffle (see research/intrinsic/
MULTISCALE_STRUCTURE.md):

  • āyah    → ayah_bonds()       frequency-controlled bond graph (NPMI)
  • passage → passage_weave()    sequential root-reuse vs verse-order shuffle (z)
  • sūra    → sura_signatures()  TF-IDF chapter signature + internal coherence (z)
  • Qur'ān  → quran_themes()     NMF block factorization (root×sūra) + arrangement

Pure functions (no Streamlit); the page wraps them in st.cache_data.
"""
import math
import collections
import numpy as np
import analysis as A


def _prep(corpus):
    norm = A.normalize_letters
    vroots = [set(norm(t) for t in toks if t and t != "-") for toks in corpus.root_tokens]
    N = len(vroots)
    fr = collections.Counter()
    for s in vroots:
        for x in s:
            fr[x] += 1
    suras = [int(x) for x in corpus.df[A.COL_SURAH].tolist()]
    return vroots, fr, suras, N


def _nmf(X, k, iters=250, seed=0):
    """Tiny multiplicative-update NMF (numpy only) — the HF Space has numpy/scipy, no sklearn."""
    rng = np.random.RandomState(seed)
    n, m = X.shape
    W = np.abs(rng.rand(n, k)) + 1e-3
    H = np.abs(rng.rand(k, m)) + 1e-3
    for _ in range(iters):
        H *= (W.T @ X) / (W.T @ (W @ H) + 1e-9)
        W *= (X @ H.T) / ((W @ H) @ H.T + 1e-9)
    return W, H


def distribution_profiles(corpus, min_freq=20, K=15):
    """How each root is LAID OUT across the book. Per root: burstiness (gap-CV, local clumping),
    dispersion (Juilland D), coverage (frac of 114 sūras touched), partner-consistency (1 − entropy
    of companion roots = keeps the same company), positional trend. Rule-based archetype on coverage.
    Plus corpus-level z vs a frequency-preserving random-placement null (the 'characteristic' test).
    Returns (profiles, z_summary). Numpy only — no sklearn (HF Space)."""
    import random
    random.seed(7)
    vroots, fr, suras, N = _prep(corpus)
    drop = set(r for r, _ in fr.most_common(12))
    roots = [r for r, v in fr.items() if v >= min_freq and r not in drop]
    rset = set(roots)
    content = [s & rset for s in vroots]
    occ = {r: [i for i in range(N) if r in vroots[i]] for r in roots}
    M = 20; binsz = N / M

    def modes(p, comp):
        p = sorted(p)
        g = np.diff(np.array(p)) if len(p) > 1 else np.array([1.0])
        B = g.std() / g.mean() if g.mean() > 0 else 0.0
        bc = np.zeros(M)
        for x in p:
            bc[min(M - 1, int(x // binsz))] += 1
        D = 1 - (bc.std() / bc.mean()) / math.sqrt(M - 1) if bc.mean() > 0 else 0.0
        cov = len(set(suras[i] for i in p)) / 114.0
        cc = {}
        for i in p:
            for x in comp[i]:
                cc[x] = cc.get(x, 0) + 1
        tot = sum(cc.values())
        H = (-sum((c / tot) * math.log(c / tot) for c in cc.values()) / math.log(len(cc))
             if tot > 0 and len(cc) > 1 else 0.0)
        trend = 2 * abs((sum(p) / len(p)) / N - 0.5)
        return B, D, cov, H, trend

    profiles = []
    for r in roots:
        B, D, cov, H, trend = modes(occ[r], content)
        arch = ("Distributed core" if cov >= 0.33 else
                "Concentrated pocket" if cov <= 0.16 else "Broadly woven")
        profiles.append({"root": r, "freq": fr[r], "burstiness": round(B, 2),
                         "coverage": round(cov, 2), "dispersion": round(D, 3),
                         "partner_consistency": round(1 - H, 2), "trend": round(trend, 2),
                         "archetype": arch, "n_suras": int(round(cov * 114))})

    def cmeans(rand):
        vals = []
        for r in roots:
            p = random.sample(range(N), fr[r]) if rand else occ[r]
            B, D, cov, H, trend = modes(p, content)
            vals.append([B, D, cov, 1 - H, trend])
        return np.array(vals).mean(0)

    canon = cmeans(False)
    nulls = np.array([cmeans(True) for _ in range(K)])
    mu = nulls.mean(0); sd = nulls.std(0) + 1e-9
    nm = ["burstiness", "dispersion", "coverage", "partner-consistency", "trend"]
    zsum = [{"mode": nm[j], "canonical": round(float(canon[j]), 3),
             "random": round(float(mu[j]), 3), "z": round(float((canon[j] - mu[j]) / sd[j]))}
            for j in range(5)]
    return profiles, zsum


def _refs(corpus):
    su = [int(x) for x in corpus.df[A.COL_SURAH].tolist()]
    ay = []
    for x in corpus.df[A.COL_AYAH].tolist():
        try:
            ay.append(int(float(x)))
        except Exception:
            ay.append(0)
    return list(zip(su, ay))


def bond_verses(corpus, ra, rb, limit=20):
    """Original-text read-back for an āyah bond: the (sūra, āyah) refs where both roots occur."""
    norm = A.normalize_letters
    refs = _refs(corpus)
    out = []
    for i, toks in enumerate(corpus.root_tokens):
        s = set(norm(t) for t in toks if t and t != "-")
        if ra in s and rb in s:
            out.append(refs[i])
            if len(out) >= limit:
                break
    return out


def theme_exemplars(corpus, roots, limit=20, min_hits=2):
    """Original-text read-back for a theme: verses containing the most of the theme's top roots."""
    norm = A.normalize_letters
    rs = set(roots)
    refs = _refs(corpus)
    scored = []
    for i, toks in enumerate(corpus.root_tokens):
        s = set(norm(t) for t in toks if t and t != "-")
        h = len(s & rs)
        if h >= min_hits:
            scored.append((h, i))
    scored.sort(key=lambda x: -x[0])
    return [refs[i] for _h, i in scored[:limit]]


def bond_word_hits(corpus, ra, rb, limit=30):
    """Dense bond read-out: per co-occurring āyah, the actual surface WORDS whose root is ra or rb
    (so you see where the two roots meet, not a wall of full verses). Returns [(sūra, āyah, words)]."""
    norm = A.normalize_letters
    refs = _refs(corpus)
    out = []
    for i, (rts, sfs) in enumerate(zip(corpus.root_tokens, corpus.surface_tokens)):
        nr = [norm(r) for r in rts]
        if ra in nr and rb in nr:
            words = [sf for r, sf in zip(nr, sfs) if r in (ra, rb)]
            out.append((refs[i][0], refs[i][1], " · ".join(dict.fromkeys(words))))
            if len(out) >= limit:
                break
    return out


def theme_word_hits(corpus, roots, limit=30, min_hits=2):
    """Dense theme read-out: āyāt carrying the most of the theme's roots, with the actual words."""
    norm = A.normalize_letters
    rs = set(roots)
    refs = _refs(corpus)
    scored = []
    for i, (rts, sfs) in enumerate(zip(corpus.root_tokens, corpus.surface_tokens)):
        nr = [norm(r) for r in rts]
        words = [sf for r, sf in zip(nr, sfs) if r in rs]
        h = len(set(r for r in nr if r in rs))
        if h >= min_hits:
            scored.append((h, refs[i][0], refs[i][1], " · ".join(dict.fromkeys(words))))
    scored.sort(key=lambda x: -x[0])
    return [(s, a, w) for _h, s, a, w in scored[:limit]]


def sura_sig_hits(corpus, sura, roots, limit=15):
    """Āyāt of one sūra that carry its signature roots, with the actual words (compact)."""
    norm = A.normalize_letters
    rs = set(roots)
    refs = _refs(corpus)
    out = []
    for i, (rts, sfs) in enumerate(zip(corpus.root_tokens, corpus.surface_tokens)):
        if refs[i][0] != int(sura):
            continue
        nr = [norm(r) for r in rts]
        words = [sf for r, sf in zip(nr, sfs) if r in rs]
        if words:
            out.append((refs[i][0], refs[i][1], " · ".join(dict.fromkeys(words))))
            if len(out) >= limit:
                break
    return out


def template_families(corpus, min_support=3, min_suras=2, top=50, fmin=3, fmax=120):
    """Recurring multi-root TEMPLATES across the book (the mathānī, generalized from L21 verse-pairs
    to 3-root families): root-triples that co-occur in ≥min_support verses spanning ≥min_suras sūras.
    Frequent-itemset mining on mid/rare content roots; greedy-deduped by verse overlap so one formula
    isn't listed many times. Each family is a coherent, cross-chapter recurring template."""
    norm = A.normalize_letters
    su = [int(x) for x in corpus.df[A.COL_SURAH].tolist()]
    ay = []
    for x in corpus.df[A.COL_AYAH].tolist():
        try:
            ay.append(int(float(x)))
        except Exception:
            ay.append(0)
    fr = collections.Counter()
    rows = []
    for toks in corpus.root_tokens:
        s = set(norm(t) for t in toks if t and t != "-")
        rows.append(s)
        for r in s:
            fr[r] += 1
    TR = set(r for r, v in fr.items() if fmin <= v <= fmax)
    inc = [s & TR for s in rows]
    pair = collections.Counter()
    for s in inc:
        sl = sorted(s)
        for i in range(len(sl)):
            for j in range(i + 1, len(sl)):
                pair[(sl[i], sl[j])] += 1
    adj = collections.defaultdict(set)
    for (a, b), c in pair.items():
        if c >= min_support:
            adj[a].add(b); adj[b].add(a)
    tri = collections.defaultdict(list)
    for idx, s in enumerate(inc):
        sl = sorted(x for x in s if x in adj)
        for i in range(len(sl)):
            a = sl[i]
            for j in range(i + 1, len(sl)):
                b = sl[j]
                if b not in adj[a]:
                    continue
                for k in range(j + 1, len(sl)):
                    c = sl[k]
                    if c in adj[a] and c in adj[b]:
                        tri[(a, b, c)].append(idx)
    fams = []
    for trip, idxs in tri.items():
        if len(idxs) >= min_support:
            suras = set(su[i] for i in idxs)
            if len(suras) >= min_suras:
                fams.append({"roots": list(trip), "support": len(idxs), "n_suras": len(suras),
                             "verses": [(su[i], ay[i]) for i in idxs], "_v": set(idxs)})
    fams.sort(key=lambda f: (-f["n_suras"], -f["support"]))
    kept = []
    for f in fams:
        if any(len(f["_v"] & g["_v"]) / len(f["_v"] | g["_v"]) > 0.6 for g in kept):
            continue
        kept.append(f)
        if len(kept) >= top:
            break
    for f in kept:
        f.pop("_v", None)
    return kept


def read_context(corpus, npmi_min=0.30, min_co=5, tmpl_top=80):
    """Per-āyah structural context for the reader: strong concept-bonds (NPMI) among a verse's roots,
    and any recurring template (mathānī family) the verse instantiates. Computed once (cache it);
    lookup by (sūra, āyah) is instant. Pure-python / deployable."""
    norm = A.normalize_letters
    su = [int(x) for x in corpus.df[A.COL_SURAH].tolist()]
    ay = []
    for x in corpus.df[A.COL_AYAH].tolist():
        try:
            ay.append(int(float(x)))
        except Exception:
            ay.append(0)
    vroots = [set(norm(t) for t in toks if t and t != "-") for toks in corpus.root_tokens]
    N = len(vroots)
    fr = collections.Counter()
    for s in vroots:
        for r in s:
            fr[r] += 1
    drop = set(r for r, _ in fr.most_common(12))
    cand = [r for r, v in fr.items() if v >= 8 and r not in drop]
    cs = set(cand)
    rset = {r: set() for r in cand}
    for i, s in enumerate(vroots):
        for r in (s & cs):
            rset[r].add(i)
    rl = sorted(cand, key=lambda r: -fr[r])
    npmi = {}
    for i in range(len(rl)):
        a = rl[i]; Sa = rset[a]
        for j in range(i + 1, len(rl)):
            b = rl[j]; w = len(Sa & rset[b])
            if w >= min_co:
                pab = w / N
                v = math.log(pab / ((fr[a] / N) * (fr[b] / N))) / (-math.log(pab))
                if v >= npmi_min:
                    npmi[frozenset((a, b))] = round(v, 2)
    refs = {(su[i], ay[i]): i for i in range(N)}
    fams = template_families(corpus, top=tmpl_top)
    vt = collections.defaultdict(list)
    for f in fams:
        for (s, a) in f["verses"]:
            i = refs.get((s, a))
            if i is not None:
                vt[i].append({"roots": f["roots"], "n_suras": f["n_suras"], "support": f["support"]})
    # distribution character per content root (core vs pocket) — reuse the distribution engine
    dprof, _dz = distribution_profiles(corpus)
    dist = {p["root"]: {"arch": p["archetype"], "n_suras": p["n_suras"], "cov": p["coverage"]}
            for p in dprof}
    # this chapter's dominant global theme — reuse the NMF theme engine
    th = quran_themes(corpus)
    tsuras = th["suras"]; dps = th["dom_per_sura"]; thlist = th["themes"]
    sura_theme = {}
    for k, s in enumerate(tsuras):
        t = thlist[dps[k]]
        sura_theme[int(s)] = {"roots": t["roots"], "lo": t["lo"], "hi": t["hi"]}
    return {"refs": refs, "vroots": vroots, "drop": drop, "npmi": npmi,
            "vt": dict(vt), "dist": dist, "sura_theme": sura_theme}


def ayah_bonds(corpus, min_co=5, top=150):
    """Within-āyah concept bonds ranked by NPMI (frequency-controlled), not raw count."""
    vroots, fr, suras, N = _prep(corpus)
    drop = set(r for r, _ in fr.most_common(12))
    roots = [r for r, v in fr.items() if v >= 10 and r not in drop]
    rset = {r: set() for r in roots}
    for i, s in enumerate(vroots):
        for r in s:
            if r in rset:
                rset[r].add(i)
    rl = sorted(roots, key=lambda r: -fr[r])
    out = []
    for i in range(len(rl)):
        a = rl[i]; Sa = rset[a]
        for j in range(i + 1, len(rl)):
            b = rl[j]; w = len(Sa & rset[b])
            if w >= min_co:
                pab = w / N
                npmi = math.log(pab / ((fr[a] / N) * (fr[b] / N))) / (-math.log(pab))
                out.append((a, b, w, round(npmi, 3)))
    out.sort(key=lambda x: -x[3])
    n_strong = sum(1 for x in out if x[3] > 0.3)
    return out[:top], n_strong


def passage_weave(corpus, n_null=40, seed=7):
    """Sequential lexical weave: IDF-weighted root reuse between adjacent verses, vs a
    within-sūra verse-ORDER shuffle. Returns global z + per-sūra weave (per adjacent pair)."""
    import random
    random.seed(seed)
    vroots, fr, suras, N = _prep(corpus)
    drop = set(r for r, _ in fr.most_common(12))
    idf = {r: math.log(N / v) for r, v in fr.items()}
    bysu = collections.defaultdict(list)
    for i in range(N):
        bysu[suras[i]].append(vroots[i])

    def W(shuffle=False):
        tot = 0.0; per = {}
        for s, seq in bysu.items():
            q = seq[:]
            if shuffle:
                random.shuffle(q)
            st = 0.0
            for k in range(len(q) - 1):
                st += sum(idf[r] for r in (q[k] & q[k + 1]) if r not in drop)
            per[s] = st; tot += st
        return tot, per

    obs, per = W(False)
    nulls = [W(True)[0] for _ in range(n_null)]
    mu = sum(nulls) / len(nulls)
    sd = (sum((x - mu) ** 2 for x in nulls) / len(nulls)) ** 0.5 or 1.0
    perpair = sorted(((s, per[s] / max(len(bysu[s]) - 1, 1)) for s in per),
                     key=lambda x: -x[1])
    return {"obs": obs, "mu": mu, "sd": sd, "z": (obs - mu) / sd, "per": perpair}


def ayah_clusters(corpus, npmi_min=0.35, max_clusters=14):
    """Āyah-scale concept FAMILIES: connected components of the strong-NPMI bond graph
    (roots that bond together form coherent groups — sun/moon/night/day, buy/sell/price …)."""
    import networkx as nx
    vroots, fr, suras, N = _prep(corpus)
    drop = set(r for r, _ in fr.most_common(12))
    roots = [r for r, v in fr.items() if v >= 10 and r not in drop]
    rset = {r: set() for r in roots}
    for i, s in enumerate(vroots):
        for r in s:
            if r in rset:
                rset[r].add(i)
    rl = sorted(roots, key=lambda r: -fr[r])
    G = nx.Graph()
    for i in range(len(rl)):
        a = rl[i]; Sa = rset[a]
        for j in range(i + 1, len(rl)):
            b = rl[j]; w = len(Sa & rset[b])
            if w >= 5:
                pab = w / N
                npmi = math.log(pab / ((fr[a] / N) * (fr[b] / N))) / (-math.log(pab))
                if npmi >= npmi_min:
                    G.add_edge(a, b)
    comps = [sorted(c, key=lambda r: -fr[r]) for c in nx.connected_components(G) if len(c) >= 2]
    comps.sort(key=len, reverse=True)
    return comps[:max_clusters]


def weave_decay(corpus, maxd=12, seed=3):
    """Passage-scale cohesion DECAY: IDF-weighted root reuse between āyāt d apart (d=1..maxd),
    real vs within-sūra order-shuffle floor. Shows how far cohesion reaches (the passage size)."""
    import random
    random.seed(seed)
    vroots, fr, suras, N = _prep(corpus)
    drop = set(r for r, _ in fr.most_common(12))
    idf = {r: math.log(N / v) for r, v in fr.items()}
    bysu = collections.defaultdict(list)
    for i in range(N):
        bysu[suras[i]].append(vroots[i])
    seqs = list(bysu.values())

    def reuse(ss, d):
        tot = 0.0; npairs = 0
        for seq in ss:
            for k in range(len(seq) - d):
                tot += sum(idf[r] for r in (seq[k] & seq[k + d]) if r not in drop)
                npairs += 1
        return tot / max(npairs, 1)

    real = [reuse(seqs, d) for d in range(1, maxd + 1)]
    sh = []
    for s in seqs:
        c = s[:]; random.shuffle(c); sh.append(c)
    floor = [reuse(sh, d) for d in range(1, maxd + 1)]
    return {"d": list(range(1, maxd + 1)), "real": real, "floor": floor}


def sura_signatures(corpus, k=6):
    """Per-sūra TF-IDF signature roots (chapter identity)."""
    vroots, fr, suras, N = _prep(corpus)
    drop = set(r for r, _ in fr.most_common(12))
    idf = {r: math.log(N / v) for r, v in fr.items()}
    scnt = collections.defaultdict(collections.Counter)
    for i in range(N):
        for r in vroots[i]:
            scnt[suras[i]][r] += 1
    sig = {}
    for s, c in scnt.items():
        tot = sum(c.values()) or 1
        sc = {r: (c[r] / tot) * idf[r] for r in c if r not in drop and fr[r] >= 5}
        sig[s] = [r for r, _ in sorted(sc.items(), key=lambda x: -x[1])[:k]]
    return sig


def sura_coherence(corpus, n_null=40, seed=11):
    """Internal coherence: each verse vs its own sūra's leave-one-out IDF profile, vs a
    verse→sūra reassignment null. Returns z."""
    import random
    random.seed(seed)
    vroots, fr, suras, N = _prep(corpus)
    idf = {r: math.log(N / v) for r, v in fr.items()}

    def coher(assign, want_per=False):
        cent = collections.defaultdict(collections.Counter)
        for s, S in assign:
            for r in S:
                cent[s][r] += 1
        tot = 0.0; cnt = 0
        per = collections.defaultdict(lambda: [0.0, 0])
        for s, S in assign:
            c = cent[s]
            v = sum((c[r] - 1) * idf[r] for r in S) / (len(S) or 1)
            tot += v; cnt += 1
            if want_per:
                per[s][0] += v; per[s][1] += 1
        m = tot / max(cnt, 1)
        if want_per:
            return m, {s: per[s][0] / per[s][1] for s in per if per[s][1]}
        return m

    base = [(suras[i], vroots[i]) for i in range(N)]
    obs, per = coher(base, want_per=True)
    sizes = [suras[i] for i in range(N)]
    nulls = []
    for _ in range(n_null):
        perm = sizes[:]; random.shuffle(perm)
        nulls.append(coher([(perm[i], vroots[i]) for i in range(N)]))
    mu = sum(nulls) / len(nulls)
    sd = (sum((x - mu) ** 2 for x in nulls) / len(nulls)) ** 0.5 or 1.0
    return {"obs": obs, "mu": mu, "sd": sd, "z": (obs - mu) / sd, "per": sorted(per.items())}


def quran_themes(corpus, K=12):
    """Global thematic architecture: NMF on the root×sūra TF-IDF matrix. Returns sūra list,
    per-theme top roots + dominant sūras, the sūra×theme loading matrix (themes ordered by
    mean canonical position), and the arrangement-localization stat (real vs shuffled spread)."""
    import random
    random.seed(0)
    vroots, fr, suras, N = _prep(corpus)
    drop = set(r for r, _ in fr.most_common(12))
    susort = sorted(set(suras)); si = {s: i for i, s in enumerate(susort)}
    vocab = [r for r, v in fr.items() if v >= 8 and r not in drop]
    vi = {r: i for i, r in enumerate(vocab)}
    M = np.zeros((len(susort), len(vocab)))
    for i in range(N):
        for r in vroots[i]:
            if r in vi:
                M[si[suras[i]], vi[r]] += 1
    # TF-IDF (numpy only — no sklearn)
    df = (M > 0).sum(axis=0)
    idf = np.log((M.shape[0] + 1.0) / (df + 1.0)) + 1.0
    X = M * idf
    nrm = np.sqrt((X ** 2).sum(axis=1, keepdims=True)) + 1e-9
    X = X / nrm
    W, H = _nmf(X, K, iters=250, seed=0)
    inv = {i: r for r, i in vi.items()}
    positions = np.arange(len(susort))
    sunum = np.array(susort, dtype=float)
    meanpos = [float(np.average(positions, weights=W[:, t] + 1e-9)) for t in range(K)]
    order = list(np.argsort(meanpos))
    Wo = W[:, order]
    rev = getattr(corpus, "rev_order_of_surah", {}) or {}

    def _meccan(s):
        ro = rev.get(s)
        return ro is not None and ro <= A.MECCAN_CUTOFF

    def _wpct(w, q):
        o = np.argsort(positions); cw = np.cumsum(w[o])
        if cw[-1] <= 0:
            return int(susort[0])
        cw = cw / cw[-1]
        idx = min(int(np.searchsorted(cw, q)), len(positions) - 1)
        return int(susort[o[idx]])

    themes = []
    for t in order:
        w = W[:, t] + 1e-9
        toproots = [inv[i] for i in np.argsort(-H[t])[:6]]
        domsuras = [int(susort[i]) for i in np.argsort(-W[:, t])[:3]]
        tot = float(W[:, t].sum()) + 1e-9
        mfrac = float(sum(W[i, t] for i in range(len(susort)) if _meccan(susort[i])) / tot)
        themes.append({"roots": toproots, "suras": domsuras,
                       "meanpos": float(np.average(sunum, weights=w)),
                       "lo": _wpct(w, 0.10), "hi": _wpct(w, 0.90), "meccan_frac": mfrac})
    dom = np.argmax(Wo, axis=1)
    dom_per_sura = [int(d) for d in dom]
    real = [np.std([i for i in range(len(susort)) if dom[i] == t])
            for t in range(len(order)) if list(dom).count(t) >= 3]
    real_spread = float(np.mean(real)) if real else 0.0
    rand = []
    allpos = list(range(len(susort)))
    for _ in range(100):
        random.shuffle(allpos)
        s = 0.0; c = 0
        for t in range(len(order)):
            cnt = list(dom).count(t)
            if cnt >= 3:
                s += np.std(allpos[:cnt]); c += 1
        rand.append(s / max(c, 1))
    rand_spread = float(np.mean(rand)) if rand else 0.0
    return {"suras": susort, "themes": themes, "W": Wo, "dom_per_sura": dom_per_sura,
            "real_spread": real_spread, "rand_spread": rand_spread}
