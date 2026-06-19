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

    def coher(assign):
        cent = collections.defaultdict(collections.Counter)
        for s, S in assign:
            for r in S:
                cent[s][r] += 1
        tot = 0.0; cnt = 0
        for s, S in assign:
            c = cent[s]
            sc = sum((c[r] - 1) * idf[r] for r in S)
            tot += sc / (len(S) or 1); cnt += 1
        return tot / max(cnt, 1)

    base = [(suras[i], vroots[i]) for i in range(N)]
    obs = coher(base)
    sizes = [suras[i] for i in range(N)]
    nulls = []
    for _ in range(n_null):
        perm = sizes[:]; random.shuffle(perm)
        nulls.append(coher([(perm[i], vroots[i]) for i in range(N)]))
    mu = sum(nulls) / len(nulls)
    sd = (sum((x - mu) ** 2 for x in nulls) / len(nulls)) ** 0.5 or 1.0
    return {"obs": obs, "mu": mu, "sd": sd, "z": (obs - mu) / sd}


def quran_themes(corpus, K=12):
    """Global thematic architecture: NMF on the root×sūra TF-IDF matrix. Returns sūra list,
    per-theme top roots + dominant sūras, the sūra×theme loading matrix (themes ordered by
    mean canonical position), and the arrangement-localization stat (real vs shuffled spread)."""
    import random
    random.seed(0)
    from sklearn.decomposition import NMF
    from sklearn.feature_extraction.text import TfidfTransformer
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
    X = TfidfTransformer().fit_transform(M)
    model = NMF(n_components=K, init="nndsvd", max_iter=400, random_state=0)
    W = model.fit_transform(X); H = model.components_
    inv = {i: r for r, i in vi.items()}
    meanpos = [float(np.average(range(len(susort)), weights=W[:, t] + 1e-9)) for t in range(K)]
    order = list(np.argsort(meanpos))
    Wo = W[:, order]
    themes = []
    for t in order:
        toproots = [inv[i] for i in np.argsort(-H[t])[:6]]
        domsuras = [susort[i] for i in np.argsort(-W[:, t])[:3]]
        themes.append({"roots": toproots, "suras": domsuras})
    # arrangement: within-theme position spread (real) vs shuffled labels
    dom = np.argmax(Wo, axis=1)
    real = [np.std([i for i in range(len(susort)) if dom[i] == t])
            for t in range(K) if list(dom).count(t) >= 3]
    real_spread = float(np.mean(real)) if real else 0.0
    rand = []
    allpos = list(range(len(susort)))
    for _ in range(100):
        random.shuffle(allpos)
        s = 0.0; c = 0
        for t in range(K):
            cnt = list(dom).count(t)
            if cnt >= 3:
                s += np.std(allpos[:cnt]); c += 1
        rand.append(s / max(c, 1))
    rand_spread = float(np.mean(rand)) if rand else 0.0
    return {"suras": susort, "themes": themes, "W": Wo,
            "real_spread": real_spread, "rand_spread": rand_spread}
