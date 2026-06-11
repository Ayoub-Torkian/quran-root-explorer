"""Spatial pattern recognition for the Qur'an root landscape.

Every root (or letter) occurrence is a 2-D point: x = position within the ayah,
y = global ayah index in a chosen *rearrangement* of the text. From there we
apply the classic point-pattern and areal (lattice) statistics of ecology / GIS,
each judged against a Complete-Spatial-Randomness (CSR) null.

POINT PATTERN  (how are a concept's occurrences arranged?)
  Clark-Evans R, MeanNND, Ripley K/L (+K_Max), Getis-Ord G* (1-D), Fano burstiness.
AREA / LATTICE  (which regions are hot, cold, or autocorrelated?)
  Moran's I (global) + LISA (local) + Getis-Ord G*, choropleth counts.

REARRANGEMENTS (the y-axis ordering / areal partition - "بازآرایی")
  mushaf      surah-major (sort surah, then ayah)        -> 114 surah units
  ayah_major  ayah-number first, surah second (transpose)-> 286 ayah-band units
  revelation  surah-scale nuzul order                    (needs has_rev_order)

FEATURE MODES
  root    : each occurrence of a root (default)
  letter  : each occurrence of a single Arabic letter in the ayah letter-stream
A position filter (k-th token/letter in the ayah, or first / last) lets the user
ask e.g. "what sits in the FIRST position of every ayah?".

Everything is computed live: no number is hard-coded, every verdict is a CSR
comparison with a pseudo p-value. Dense patterns are Monte-Carlo subsampled (cap)
so the O(n^2) kernels stay tractable on a shared Space.
"""
from __future__ import annotations

import numpy as np

from analysis import (_root_positions, _fano_factor, _entropy, normalize_letters,
                      COL_SURAH, COL_AYAH, MECCAN_CUTOFF)

try:
    from scipy.spatial import cKDTree as _KDTree
except Exception:  # pragma: no cover
    _KDTree = None

# ───────────────────────── orderings / rearrangements ─────────────────────────

ORDER_LABELS = {
    "mushaf": "Mushaf (surah → ayah)",
    "ayah_major": "Ayah-major (ayah → surah, 286 bands)",
    "revelation": "Revelation order (nuzul)",
}

UNIT_LABELS = {
    "surah": "Surah (114 units)",
    "ayah_band": "Ayah band (286 units, transpose)",
    "revelation": "Revelation-order surah (114)",
}


def available_orders(corpus):
    orders = ["mushaf", "ayah_major"]
    if getattr(corpus, "has_rev_order", False):
        orders.append("revelation")
    return orders


def available_units(corpus):
    units = ["surah", "ayah_band"]
    if getattr(corpus, "has_rev_order", False):
        units.append("revelation")
    return units


def _order_index(corpus, order="mushaf"):
    """Map each df row -> its global position 0..N-1 under the chosen ordering."""
    df = corpus.df
    n = len(df)
    if order == "mushaf":
        return np.arange(n, dtype=int)
    if order == "revelation" and getattr(corpus, "has_rev_order", False):
        return np.asarray(corpus.rev_global_idx, dtype=int)
    if order == "ayah_major":
        su = df[COL_SURAH].astype(int).to_numpy()
        ay = df[COL_AYAH].astype(int).to_numpy()
        keyed = sorted(range(n), key=lambda i: (int(ay[i]), int(su[i])))
        out = np.empty(n, dtype=int)
        for new_i, orig in enumerate(keyed):
            out[orig] = new_i
        return out
    return np.arange(n, dtype=int)


# ───────────────────────── feature extraction (points) ─────────────────────────

def _letter_positions(corpus, target_letter, normalize, position=None):
    """For a single Arabic letter, list (row_i, char_index_in_ayah) occurrences.

    The ayah letter-stream is the normalised letters of its segmented tokens,
    concatenated (spaces dropped). position: None=all, int k (1-based) = only the
    k-th letter, 'first'/'last' shortcuts.
    """
    tgt = normalize_letters(target_letter) if normalize else target_letter
    tgt = tgt[:1]
    out = []
    for i in range(len(corpus.df)):
        toks = corpus.seg_tokens[i]
        seq = "".join(normalize_letters(t) if normalize else t for t in toks)
        seq = [ch for ch in seq if ch.strip()]
        if not seq:
            continue
        if position in ("first", 1):
            idxs = [0] if seq[0] == tgt else []
        elif position in ("last", -1):
            idxs = [len(seq) - 1] if seq[-1] == tgt else []
        elif isinstance(position, int):
            k = position - 1
            idxs = [k] if (0 <= k < len(seq) and seq[k] == tgt) else []
        else:
            idxs = [j for j, ch in enumerate(seq) if ch == tgt]
        for j in idxs:
            out.append((i, j))
    return out


def occ_points(corpus, target, normalize, order="mushaf",
               feature="root", position=None):
    """(n,2) array of occurrence points: col0 = x (position within the ayah),
    col1 = y (global ayah index under `order`). Sorted by y.

    feature='root'   -> root-token occurrences (x = token index in ayah)
    feature='letter' -> single-letter occurrences (x = char index in ayah)
    position filters root/letter occurrences to a fixed in-ayah slot.
    """
    oidx = _order_index(corpus, order)
    pts = []
    if feature == "letter":
        for (i, j) in _letter_positions(corpus, target, normalize, position):
            pts.append((j, int(oidx[i])))
    elif feature == "surface":
        Ksf = (normalize_letters if normalize else (lambda t: t))
        tsf = Ksf(target)
        for i in range(len(corpus.df)):
            toks = corpus.surface_tokens[i]
            m = len(toks)
            for j, t in enumerate(toks):
                if Ksf(t) != tsf:
                    continue
                if position in ("first", 1) and j != 0:
                    continue
                if position in ("last", -1) and j != m - 1:
                    continue
                if isinstance(position, int) and position not in ("first", "last") \
                        and j != position - 1:
                    continue
                pts.append((j, int(oidx[i])))
    else:
        pos = _root_positions(corpus, [target], normalize, "mushaf").get(target, [])
        for it in pos:  # (gidx, surah, ayah, token_idx, ayah_len, mushaf_idx, rev_idx)
            j, mu, alen = it[3], it[5], it[4]
            if position in ("first", 1) and j != 0:
                continue
            if position in ("last", -1) and j != alen - 1:
                continue
            if isinstance(position, int) and position not in ("first", "last") \
                    and j != position - 1:
                continue
            pts.append((j, int(oidx[mu])))
    if not pts:
        return np.empty((0, 2), dtype=float)
    xy = np.array(pts, dtype=float)
    return xy[np.argsort(xy[:, 1])]


# ───────────────────────── point-pattern kernels ─────────────────────────

def _mean_nnd(xy):
    """Mean nearest-neighbour distance (2-D). KDTree when available, else O(n^2)."""
    n = len(xy)
    if n < 2:
        return np.nan
    if _KDTree is not None:
        tree = _KDTree(xy)
        d, _ = tree.query(xy, k=2)
        return float(d[:, 1].mean())
    diff = xy[:, None, :] - xy[None, :, :]
    d = np.sqrt((diff * diff).sum(-1))
    np.fill_diagonal(d, np.inf)
    return float(d.min(axis=1).mean())


def _k_counts(xy, radii):
    """Sum_{i!=j} 1{d_ij <= r} for each r (KDTree count_neighbors when available)."""
    n = len(xy)
    if _KDTree is not None:
        tree = _KDTree(xy)
        cn = tree.count_neighbors(tree, radii)
        cn = np.atleast_1d(cn).astype(float) - n
        return cn
    diff = xy[:, None, :] - xy[None, :, :]
    d = np.sqrt((diff * diff).sum(-1))
    np.fill_diagonal(d, np.inf)
    return np.array([np.sum(d <= r) for r in radii], dtype=float)


def _window(xy):
    xmin, xmax = float(xy[:, 0].min()), float(xy[:, 0].max())
    ymin, ymax = float(xy[:, 1].min()), float(xy[:, 1].max())
    if xmax <= xmin:
        xmax = xmin + 1.0
    if ymax <= ymin:
        ymax = ymin + 1.0
    return xmin, xmax, ymin, ymax


def _csr(rng, n, win):
    xmin, xmax, ymin, ymax = win
    return np.column_stack([rng.uniform(xmin, xmax, n),
                            rng.uniform(ymin, ymax, n)])


def clark_evans(xy, n_mc=99, seed=0, cap=1200, alpha=0.05):
    """Clark-Evans R via Monte-Carlo CSR in the actual window."""
    n = len(xy)
    if n < 3:
        return dict(R=np.nan, mnnd=np.nan, expected=np.nan, p_clustered=np.nan,
                    p_regular=np.nan, klass="n/a", n=n, n_used=n)
    rng = np.random.default_rng(seed)
    if n > cap:
        xy = xy[rng.choice(n, cap, replace=False)]
    n_used = len(xy)
    mnnd = _mean_nnd(xy)
    win = _window(xy)
    sims = np.array([_mean_nnd(_csr(rng, n_used, win)) for _ in range(n_mc)])
    exp = float(np.nanmean(sims))
    R = mnnd / exp if exp > 0 else np.nan
    p_clu = (np.sum(sims <= mnnd) + 1) / (n_mc + 1)
    p_reg = (np.sum(sims >= mnnd) + 1) / (n_mc + 1)
    if p_clu <= alpha and R < 1:
        klass = "clustered"
    elif p_reg <= alpha and R > 1:
        klass = "regular"
    else:
        klass = "random"
    return dict(R=round(float(R), 3), mnnd=round(float(mnnd), 3),
                expected=round(exp, 3), p_clustered=round(float(p_clu), 3),
                p_regular=round(float(p_reg), 3), klass=klass,
                n=n, n_used=n_used)


def ripley_kl(xy, n_radii=24, n_mc=39, seed=0, cap=800):
    """Ripley's K and L(r) = sqrt(K/pi) - r against a CSR envelope; K_Max deviation."""
    n = len(xy)
    if n < 4:
        return None
    rng = np.random.default_rng(seed)
    if n > cap:
        xy = xy[rng.choice(n, cap, replace=False)]
    n = len(xy)
    xmin, xmax, ymin, ymax = win = _window(xy)
    area = (xmax - xmin) * (ymax - ymin)
    rmax = 0.30 * (ymax - ymin)
    radii = np.linspace(rmax / n_radii, rmax, n_radii)

    def L_of(pts):
        cn = _k_counts(pts, radii)
        K = area * cn / (n * (n - 1))
        return np.sqrt(np.maximum(K, 0) / np.pi) - radii

    L_obs = L_of(xy)
    sims = np.array([L_of(_csr(rng, n, win)) for _ in range(n_mc)])
    L_mean = sims.mean(0)
    L_lo = np.percentile(sims, 2.5, axis=0)
    L_hi = np.percentile(sims, 97.5, axis=0)
    k_max = float(np.max(np.abs(L_obs - L_mean)))
    above = np.mean(L_obs > L_hi)
    below = np.mean(L_obs < L_lo)
    if above >= below and above > 0:
        kclass = "clustered"
    elif below > above:
        kclass = "regular"
    else:
        kclass = "random"
    return dict(radii=radii, L_obs=L_obs, L_mean=L_mean, L_lo=L_lo, L_hi=L_hi,
                k_max=round(k_max, 3), klass=kclass, n=n)


def fano_burstiness(xy):
    """Fano factor of the gaps between successive y-positions (>1 bursty)."""
    if len(xy) < 3:
        return 0.0
    y = np.sort(xy[:, 1])
    gaps = np.diff(y).tolist()
    return round(_fano_factor(gaps), 3)


def gstar_window_1d(xy, n_bins=120, window=5):
    """1-D Getis-Ord-style moving-window focal score along the y-sequence."""
    if len(xy) < 3:
        return None
    y = xy[:, 1]
    ymin, ymax = y.min(), y.max()
    edges = np.linspace(ymin, ymax, n_bins + 1)
    counts, _ = np.histogram(y, bins=edges)
    kern = np.ones(2 * window + 1)
    focal = np.convolve(counts.astype(float), kern, mode="same")
    mu, sd = focal.mean(), focal.std()
    z = (focal - mu) / sd if sd > 0 else np.zeros_like(focal)
    centres = 0.5 * (edges[:-1] + edges[1:])
    return dict(centres=centres, counts=counts, focal=focal, z=z)


# ───────────────────────── areal / lattice kernels ─────────────────────────

def areal_counts(corpus, target, normalize, unit="surah",
                 feature="root", position=None):
    """Ordered per-unit occurrence counts + integer labels."""
    df = corpus.df
    su = df[COL_SURAH].astype(int).to_numpy()
    ay = df[COL_AYAH].astype(int).to_numpy()
    if unit == "ayah_band":
        size = 286
        key = ay
    elif unit == "revelation" and getattr(corpus, "has_rev_order", False):
        size = 114
        rev = corpus.rev_order_of_surah
        key = np.array([rev.get(int(s), 999) for s in su])
    else:
        size = 114
        key = su
    labels = np.arange(1, size + 1)
    counts = np.zeros(size + 1, dtype=float)
    if feature == "letter":
        xy = occ_points(corpus, target, normalize, "mushaf",
                        feature="letter", position=position)
        # map each occurrence's row back through counts via key — recount directly
        tgt = normalize_letters(target) if normalize else target
        tgt = tgt[:1]
        for i in range(len(df)):
            toks = corpus.seg_tokens[i]
            seq = [ch for t in toks
                   for ch in (normalize_letters(t) if normalize else t)
                   if ch.strip()]
            if not seq:
                continue
            if position in ("first", 1):
                c = 1 if seq[0] == tgt else 0
            elif position in ("last", -1):
                c = 1 if seq[-1] == tgt else 0
            elif isinstance(position, int):
                k = position - 1
                c = 1 if (0 <= k < len(seq) and seq[k] == tgt) else 0
            else:
                c = sum(1 for ch in seq if ch == tgt)
            if c:
                k = int(key[i])
                if 1 <= k <= size:
                    counts[k] += c
    else:
        K = (normalize_letters if normalize else (lambda t: t))
        rk = K(target)
        _src = corpus.surface_tokens if feature == "surface" else corpus.root_tokens
        for i in range(len(df)):
            toks = _src[i]
            if not toks:
                continue
            if position in ("first", 1):
                c = 1 if (toks and K(toks[0]) == rk) else 0
            elif position in ("last", -1):
                c = 1 if (toks and K(toks[-1]) == rk) else 0
            elif isinstance(position, int):
                k = position - 1
                c = 1 if (0 <= k < len(toks) and K(toks[k]) == rk) else 0
            else:
                c = sum(1 for t in toks if K(t) == rk)
            if c:
                k = int(key[i])
                if 1 <= k <= size:
                    counts[k] += c
    return counts[1:], labels


def contiguity_W(n, standardize=True):
    """1-D rook contiguity over ordered units (i adjacent to i±1)."""
    W = np.zeros((n, n))
    for i in range(n):
        if i > 0:
            W[i, i - 1] = 1
        if i < n - 1:
            W[i, i + 1] = 1
    if standardize:
        rs = W.sum(1, keepdims=True)
        rs[rs == 0] = 1
        W = W / rs
    return W


def morans_I(values, W, n_perm=199, seed=0):
    """Global Moran's I with a conditional-permutation pseudo p-value."""
    x = np.asarray(values, float)
    n = len(x)
    z = x - x.mean()
    s2 = (z * z).sum()
    if s2 == 0 or n < 3:
        return dict(I=np.nan, EI=(-1.0 / (n - 1) if n > 1 else np.nan),
                    p=np.nan, klass="n/a", n=n)
    S0 = W.sum()
    I = (n / S0) * (z @ W @ z) / s2
    rng = np.random.default_rng(seed)
    sims = np.empty(n_perm)
    for k in range(n_perm):
        zp = rng.permutation(z)
        sims[k] = (n / S0) * (zp @ W @ zp) / s2
    p = (np.sum(np.abs(sims) >= abs(I)) + 1) / (n_perm + 1)
    EI = -1.0 / (n - 1)
    if p <= 0.05 and I > EI:
        klass = "clustered"
    elif p <= 0.05 and I < EI:
        klass = "regular"
    else:
        klass = "random"
    return dict(I=round(float(I), 4), EI=round(EI, 4), p=round(float(p), 3),
                klass=klass, n=n)


def local_morans(values, W, n_perm=199, seed=0):
    """LISA: per-unit local Moran's I_i, pseudo p, and HH/LL/HL/LH quadrant."""
    x = np.asarray(values, float)
    n = len(x)
    z = x - x.mean()
    s2 = (z * z).sum() / n
    if s2 == 0 or n < 3:
        return dict(Ii=np.zeros(n), p=np.ones(n),
                    quad=np.array(["ns"] * n, dtype=object), lag=np.zeros(n))
    lag = W @ z
    Ii = (z / s2) * lag
    rng = np.random.default_rng(seed)
    p = np.ones(n)
    wn = (W > 0).sum(1).astype(int)
    for i in range(n):
        ki = max(int(wn[i]), 1)
        others = np.delete(z, i)
        sims = np.empty(n_perm)
        for k in range(n_perm):
            samp = rng.choice(others, ki, replace=False)
            sims[k] = (z[i] / s2) * samp.mean() * ki
        p[i] = (np.sum(np.abs(sims) >= abs(Ii[i])) + 1) / (n_perm + 1)
    quad = np.array(["ns"] * n, dtype=object)
    for i in range(n):
        if p[i] > 0.05:
            continue
        if z[i] > 0 and lag[i] > 0:
            quad[i] = "HH"
        elif z[i] < 0 and lag[i] < 0:
            quad[i] = "LL"
        elif z[i] > 0 and lag[i] < 0:
            quad[i] = "HL"
        else:
            quad[i] = "LH"
    return dict(Ii=Ii, p=p, quad=quad, lag=lag)


def getis_g_star(values):
    """Getis-Ord G*_i hot/cold z-scores using contiguity incl. self-weight."""
    x = np.asarray(values, float)
    n = len(x)
    if n < 3 or x.std() == 0:
        return dict(z=np.zeros(n), hot=np.array([False] * n),
                    cold=np.array([False] * n))
    W = contiguity_W(n, standardize=False)
    np.fill_diagonal(W, 1)
    xbar = x.mean()
    S = x.std()
    z = np.empty(n)
    for i in range(n):
        wi = W[i]
        num = (wi * x).sum() - xbar * wi.sum()
        den = S * np.sqrt((n * (wi ** 2).sum() - wi.sum() ** 2) / (n - 1))
        z[i] = num / den if den > 0 else 0.0
    return dict(z=z, hot=z >= 1.96, cold=z <= -1.96)


# ───────────────────────── per-root profile & corpus classification ─────────────────────────

def root_spatial_profile(corpus, target, normalize, order="mushaf",
                         unit="surah", feature="root", position=None,
                         n_mc=99, seed=0):
    """One-stop profile for a single target under one rearrangement."""
    xy = occ_points(corpus, target, normalize, order, feature=feature,
                    position=position)
    ce = clark_evans(xy, n_mc=n_mc, seed=seed)
    kl = ripley_kl(xy, n_mc=max(19, n_mc // 3), seed=seed)
    vals, labels = areal_counts(corpus, target, normalize, unit=unit,
                                feature=feature, position=position)
    W = contiguity_W(len(vals))
    mi = morans_I(vals, W, seed=seed)
    lisa = local_morans(vals, W, n_perm=99, seed=seed)
    gstar = getis_g_star(vals)
    return dict(target=target, order=order, unit=unit, feature=feature,
                position=position, xy=xy, clark_evans=ce, ripley=kl,
                fano=fano_burstiness(xy), moran=mi, lisa=lisa, gstar=gstar,
                areal_values=vals, areal_labels=labels,
                k_max=(kl or {}).get("k_max", np.nan))


def _combined_verdict(ce_klass, mi_klass):
    """Fuse the global readings (R + I) into CLUS / RAND / REG (the macro claim)."""
    votes = [v for v in (ce_klass, mi_klass)
             if v in ("clustered", "regular", "random")]
    if not votes:
        return "random"
    if votes.count("regular") >= votes.count("clustered") and "regular" in votes:
        return "regular"
    if votes.count("clustered") > votes.count("regular"):
        return "clustered"
    return "random"


def classify_corpus(corpus, normalize, order="mushaf", unit="surah",
                    min_freq=8, n_mc=39, max_roots=None, seed=0):
    """Forest view: classify every root above a frequency floor and tally the
    CLUS / RAND / REG percentages — the corpus-wide headline."""
    freq = corpus.freq_norm if normalize else corpus.freq_exact
    roots = [r for r, c in freq.items() if c >= min_freq]
    roots.sort(key=lambda r: -freq[r])
    if max_roots:
        roots = roots[:max_roots]
    rows = []
    for r in roots:
        xy = occ_points(corpus, r, normalize, order)
        if len(xy) < 3:
            continue
        ce = clark_evans(xy, n_mc=n_mc, seed=seed, cap=600)
        kl = ripley_kl(xy, n_mc=max(15, n_mc // 3), seed=seed, cap=600)
        vals, _ = areal_counts(corpus, r, normalize, unit=unit)
        mi = morans_I(vals, contiguity_W(len(vals)), n_perm=99, seed=seed)
        k_klass = (kl or {}).get("klass", "n/a")
        rows.append(dict(
            root=r, freq=int(freq[r]),
            R=ce["R"], R_class=ce["klass"],
            I=mi["I"], I_class=mi["klass"],
            K_max=(kl or {}).get("k_max", np.nan), K_class=k_klass,
            verdict=_combined_verdict(ce["klass"], mi["klass"]),
        ))
    n = len(rows) or 1

    def pct(field, val):
        return round(100 * sum(1 for x in rows if x[field] == val) / n, 1)

    summary = dict(
        n_roots=len(rows), order=order, unit=unit, min_freq=min_freq,
        global_regular=pct("verdict", "regular"),
        global_clustered=pct("verdict", "clustered"),
        global_random=pct("verdict", "random"),
        local_clustered_K=pct("K_class", "clustered"),
        local_regular_K=pct("K_class", "regular"),
        R_regular=pct("R_class", "regular"),
        I_regular=pct("I_class", "regular"),
        I_clustered=pct("I_class", "clustered"),
    )
    return rows, summary


# ───────────────────────── two-scale signature (local vs global) ─────────────────────────

def two_scale_signature(xy, n_mc=39, seed=0, cap=800):
    """Read the SAME Ripley L(r) curve at small vs large radius — the paper's
    actual multiscale method for the 'locally clustered, globally regular' claim.

    local  = behaviour over the smallest third of radii  (clumping at short range)
    global = behaviour over the largest third of radii    (spacing at long range)
    Each is 'clustered' if L sits above the CSR 97.5% envelope, 'regular' if below
    the 2.5% envelope, else 'random'. Scores are mean signed (L_obs - L_csr_mean).
    """
    kl = ripley_kl(xy, n_mc=n_mc, seed=seed, cap=cap)
    if kl is None:
        return dict(local="n/a", global_="n/a", local_score=np.nan,
                    global_score=np.nan, kl=None)
    r = kl["radii"]
    m = len(r)
    lo_third = slice(0, max(1, m // 3))
    hi_third = slice(m - max(1, m // 3), m)

    def verdict(sl):
        obs = kl["L_obs"][sl]
        hi = kl["L_hi"][sl]
        lo = kl["L_lo"][sl]
        above = np.mean(obs > hi)
        below = np.mean(obs < lo)
        if above >= below and above > 0.34:
            return "clustered"
        if below > above and below > 0.34:
            return "regular"
        return "random"

    local_score = float(np.mean(kl["L_obs"][lo_third] - kl["L_mean"][lo_third]))
    global_score = float(np.mean(kl["L_obs"][hi_third] - kl["L_mean"][hi_third]))
    return dict(local=verdict(lo_third), global_=verdict(hi_third),
                local_score=round(local_score, 3),
                global_score=round(global_score, 3), kl=kl)


def coverage_index(corpus, target, normalize, unit="surah",
                   feature="root", position=None):
    """Fraction of areal units the target touches (1.0 = pervasive/unsaturated,
    near 0 = confined). A simple, frequency-aware 'global spread' reading."""
    vals, labels = areal_counts(corpus, target, normalize, unit=unit,
                                feature=feature, position=position)
    occupied = int((vals > 0).sum())
    return dict(occupied=occupied, total=len(vals),
                coverage=round(occupied / max(len(vals), 1), 3))


def classify_corpus_2scale(corpus, normalize, order="mushaf", unit="surah",
                           min_freq=8, n_mc=25, max_roots=None, seed=0):
    """Forest tally using the two-scale Ripley reading (local vs global) plus the
    areal Moran verdict, so the headline reports BOTH scales honestly."""
    freq = corpus.freq_norm if normalize else corpus.freq_exact
    roots = [r for r, c in freq.items() if c >= min_freq]
    roots.sort(key=lambda r: -freq[r])
    if max_roots:
        roots = roots[:max_roots]
    rows = []
    for r in roots:
        xy = occ_points(corpus, r, normalize, order)
        if len(xy) < 4:
            continue
        ts = two_scale_signature(xy, n_mc=n_mc, seed=seed, cap=500)
        cov = coverage_index(corpus, r, normalize, unit=unit)
        vals, _ = areal_counts(corpus, r, normalize, unit=unit)
        mi = morans_I(vals, contiguity_W(len(vals)), n_perm=99, seed=seed)
        rows.append(dict(
            root=r, freq=int(freq[r]),
            local=ts["local"], global_=ts["global_"],
            local_score=ts["local_score"], global_score=ts["global_score"],
            coverage=cov["coverage"], I=mi["I"], I_class=mi["klass"],
        ))
    n = len(rows) or 1

    def pct(field, val):
        return round(100 * sum(1 for x in rows if x[field] == val) / n, 1)

    summary = dict(
        n_roots=len(rows), order=order, unit=unit, min_freq=min_freq,
        local_clustered=pct("local", "clustered"),
        local_regular=pct("local", "regular"),
        local_random=pct("local", "random"),
        global_regular=pct("global_", "regular"),
        global_clustered=pct("global_", "clustered"),
        global_random=pct("global_", "random"),
        mean_coverage=round(float(np.mean([x["coverage"] for x in rows])), 3),
        I_regular=pct("I_class", "regular"),
        I_clustered=pct("I_class", "clustered"),
    )
    return rows, summary


# ───────────────────────── fast forest tally (no Monte-Carlo point kernels) ─────────────────────────

def classify_corpus_fast(corpus, normalize, order="mushaf", unit="surah",
                         min_freq=8, fano_clustered=1.5, n_perm=49,
                         max_roots=None, seed=0):
    """Corpus-wide tally using only CHEAP per-root statistics so it runs over the
    whole floor set in seconds (for the precomputed JSON the page loads):

      local clustering : Fano factor of y-gaps > `fano_clustered`  (bursty)
      global spread    : coverage = fraction of areal units occupied (unsaturation)
      areal autocorr   : Moran's I on per-unit counts (clustered / random / regular)

    Honest and fast; the heavy CSR two-scale kernels stay for live single-target use.
    """
    freq = corpus.freq_norm if normalize else corpus.freq_exact
    roots = [r for r, c in freq.items() if c >= min_freq]
    roots.sort(key=lambda r: -freq[r])
    if max_roots:
        roots = roots[:max_roots]
    rows = []
    for r in roots:
        xy = occ_points(corpus, r, normalize, order)
        if len(xy) < 4:
            continue
        fano = fano_burstiness(xy)
        vals, _ = areal_counts(corpus, r, normalize, unit=unit)
        occupied = int((vals > 0).sum())
        coverage = occupied / max(len(vals), 1)
        mi = morans_I(vals, contiguity_W(len(vals)), n_perm=n_perm, seed=seed)
        rows.append(dict(
            root=r, freq=int(freq[r]), fano=fano,
            local=("clustered" if fano > fano_clustered else "dispersed"),
            coverage=round(coverage, 3),
            I=mi["I"], I_class=mi["klass"],
        ))
    n = len(rows) or 1

    def pct(field, val):
        return round(100 * sum(1 for x in rows if x[field] == val) / n, 1)

    summary = dict(
        n_roots=len(rows), order=order, unit=unit, min_freq=min_freq,
        fano_threshold=fano_clustered,
        local_clustered=pct("local", "clustered"),
        mean_coverage=round(float(np.mean([x["coverage"] for x in rows])), 3),
        median_coverage=round(float(np.median([x["coverage"] for x in rows])), 3),
        max_coverage=round(float(np.max([x["coverage"] for x in rows])), 3),
        saturated_pct=pct("coverage", 1.0),
        I_clustered=pct("I_class", "clustered"),
        I_regular=pct("I_class", "regular"),
        I_random=pct("I_class", "random"),
    )
    return rows, summary


# ───────────────────────── analytic Moran's I (closed-form, for the forest) ─────────────────────────

def morans_I_analytic(values, W):
    """Global Moran's I with the closed-form randomization z-score / p-value.
    Deterministic and O(n) given W — used for the precomputed corpus tally."""
    import math
    x = np.asarray(values, float)
    n = len(x)
    z = x - x.mean()
    s2 = (z * z).sum()
    if s2 == 0 or n < 4:
        return dict(I=np.nan, z=np.nan, p=np.nan, klass="n/a", n=n)
    S0 = W.sum()
    I = (n / S0) * (z @ W @ z) / s2
    EI = -1.0 / (n - 1)
    S1 = 0.5 * np.sum((W + W.T) ** 2)
    rowsum = W.sum(1)
    colsum = W.sum(0)
    S2 = np.sum((rowsum + colsum) ** 2)
    b2 = (n * np.sum(z ** 4)) / (s2 ** 2)
    A = n * ((n * n - 3 * n + 3) * S1 - n * S2 + 3 * S0 * S0)
    B = b2 * ((n * n - n) * S1 - 2 * n * S2 + 6 * S0 * S0)
    C = (n - 1) * (n - 2) * (n - 3) * S0 * S0
    var = (A - B) / C - EI * EI if C > 0 else 0.0
    zsc = (I - EI) / math.sqrt(var) if var > 0 else 0.0
    p = math.erfc(abs(zsc) / math.sqrt(2))
    if p <= 0.05 and I > EI:
        klass = "clustered"
    elif p <= 0.05 and I < EI:
        klass = "regular"
    else:
        klass = "random"
    return dict(I=round(float(I), 4), z=round(float(zsc), 3),
                p=round(float(p), 4), klass=klass, n=n)


# ═══════════════════════════════════════════════════════════════════════════
# LATENT SPATIAL ARCHETYPES  (multivariate feature vectors → unsupervised)
# ═══════════════════════════════════════════════════════════════════════════

FEATURE_NAMES = [
    "log_freq", "fano", "coverage", "moran_I", "moran_z",
    "grav_center", "spread_entropy", "gap_cv", "peak_share",
    "mean_pos_ayah", "meccan_pct", "acf1", "lacunarity",
]


def build_feature_matrix(corpus, normalize, order="mushaf", unit="surah",
                         min_freq=8, feature="root"):
    """One corpus pass → a rich per-root spatial feature vector (all cheap, no
    Monte-Carlo). Returns (roots, X, feature_names). Features capture BOTH the
    local scale (burstiness, gap regularity, peak share) and the global scale
    (coverage, Moran, gravitational centre, spread)."""
    df = corpus.df
    n = len(df)
    su = df[COL_SURAH].astype(int).to_numpy()
    ay = df[COL_AYAH].astype(int).to_numpy()
    has_rev = getattr(corpus, "has_rev_order", False)
    oidx = _order_index(corpus, order)
    rev_of = corpus.rev_order_of_surah if has_rev else {}
    size = 286 if unit == "ayah_band" else 114
    if unit == "revelation" and not has_rev:
        unit = "surah"

    K = normalize_letters
    _src = corpus.surface_tokens if feature == "surface" else corpus.root_tokens
    ylists = {}
    counts = {}
    posfrac = {}   # sum of within-ayah position fraction
    meccan = {}
    for i in range(n):
        toks = _src[i]
        m = len(toks)
        if m == 0:
            continue
        s = int(su[i]); a = int(ay[i])
        yi = int(oidx[i])
        if unit == "ayah_band":
            key = a if a <= 286 else 0
        elif unit == "revelation":
            key = rev_of.get(s, 0)
        else:
            key = s
        is_mecc = (has_rev and rev_of.get(s, 999) <= MECCAN_CUTOFF)
        for j, t in enumerate(toks):
            r = K(t)
            ylists.setdefault(r, []).append(yi)
            cv = counts.setdefault(r, np.zeros(size + 1))
            if 1 <= key <= size:
                cv[key] += 1
            posfrac[r] = posfrac.get(r, 0.0) + (j / max(m - 1, 1) if m > 1 else 0.5)
            if is_mecc:
                meccan[r] = meccan.get(r, 0) + 1

    if feature == "surface":
        from collections import Counter as _C
        freq = _C()
        for i in range(n):
            seen = set()
            for t in _src[i]:
                kt = K(t)
                if kt not in seen:
                    seen.add(kt); freq[kt] += 1
    else:
        freq = corpus.freq_norm if normalize else corpus.freq_exact
    roots = [r for r in ylists if freq.get(r, 0) >= min_freq and len(ylists[r]) >= 4]
    Wsurah = contiguity_W(size)
    rows = []
    keep = []
    for r in roots:
        ys = sorted(ylists[r])
        tot = len(ys)
        gaps = np.diff(ys)
        fano = _fano_factor(gaps.tolist())
        gap_cv = (gaps.std() / gaps.mean()) if len(gaps) and gaps.mean() > 0 else 0.0
        vec = counts[r][1:size + 1]
        occ = int((vec > 0).sum())
        coverage = occ / size
        peak_share = float(vec.max() / vec.sum()) if vec.sum() else 0.0
        ent = _entropy(vec[vec > 0].tolist())
        mi = morans_I_analytic(vec, Wsurah)
        grav = float(np.mean(ys)) / max(n, 1)
        mean_pos = posfrac.get(r, 0.0) / tot
        mecc_pct = (meccan.get(r, 0) / tot) if has_rev else 0.0
        ser, _ = density_series(ys, n, n_bins=120)
        _ac = acf(ser, max_lag=1)
        acf1 = float(_ac[1]) if len(_ac) > 1 else 0.0
        _lac = lacunarity(ser, box=8)
        lac = float(np.log1p(_lac)) if np.isfinite(_lac) else 0.0
        rows.append([
            np.log1p(freq[r]), fano, coverage,
            mi["I"] if mi["I"] == mi["I"] else 0.0,
            mi["z"] if mi["z"] == mi["z"] else 0.0,
            grav, ent, gap_cv, peak_share, mean_pos, mecc_pct,
            acf1, lac,
        ])
        keep.append(r)
    X = np.array(rows, dtype=float)
    return keep, X, list(FEATURE_NAMES)


def _standardize(X):
    mu = X.mean(0); sd = X.std(0); sd[sd == 0] = 1.0
    return (X - mu) / sd, mu, sd


def _pca2(Z):
    Zc = Z - Z.mean(0)
    U, S, Vt = np.linalg.svd(Zc, full_matrices=False)
    emb = Zc @ Vt[:2].T
    var = (S[:2] ** 2) / (S ** 2).sum()
    return emb, Vt[:2], var


def _kmeans(Z, k, iters=100, seed=0):
    rng = np.random.default_rng(seed)
    n = Z.shape[0]
    centers = [Z[rng.integers(n)]]
    for _ in range(1, k):
        d2 = np.min([((Z - c) ** 2).sum(1) for c in centers], axis=0)
        s = d2.sum()
        p = d2 / s if s > 0 else None
        centers.append(Z[rng.choice(n, p=p)])
    C = np.array(centers)
    lab = np.zeros(n, int)
    for _ in range(iters):
        D = ((Z[:, None, :] - C[None, :, :]) ** 2).sum(-1)
        new = D.argmin(1)
        if (new == lab).all() and _ > 0:
            break
        lab = new
        C = np.array([Z[lab == j].mean(0) if (lab == j).any() else C[j]
                      for j in range(k)])
    return lab, C


def _name_archetype(centroid_z, feat_names):
    """Short descriptor from a cluster centroid's most distinctive z-features."""
    order = np.argsort(-np.abs(centroid_z))
    parts = []
    for idx in order[:3]:
        if abs(centroid_z[idx]) < 0.4:
            continue
        arrow = "↑" if centroid_z[idx] > 0 else "↓"
        parts.append(f"{arrow}{feat_names[idx]}")
    # friendly label heuristics
    cov = centroid_z[FEATURE_NAMES.index("coverage")]
    fano = centroid_z[FEATURE_NAMES.index("fano")]
    peak = centroid_z[FEATURE_NAMES.index("peak_share")]
    if cov > 0.5 and fano < 0.3:
        tag = "Pervasive pillar"
    elif cov < -0.3 and (fano > 0.4 or peak > 0.4):
        tag = "Focal / isolated signal"
    elif centroid_z[FEATURE_NAMES.index("moran_z")] > 0.6:
        tag = "Regional anchor"
    else:
        tag = "Mixed"
    return tag, "  ".join(parts) if parts else "near-average"


def archetype_analysis(corpus, normalize, order="mushaf", unit="surah",
                       min_freq=8, k=4, seed=0, feature="root"):
    """Unsupervised spatial archetypes: feature matrix → standardise → PCA(2) +
    k-means(k). Returns roots, embedding, labels, centroids, names, variance."""
    roots, X, names = build_feature_matrix(corpus, normalize, order, unit,
                                           min_freq, feature=feature)
    if len(roots) < k:
        return None
    Z, mu, sd = _standardize(X)
    emb, comps, var = _pca2(Z)
    lab, stab, mean_stab = archetype_stability(Z, k, n_boot=20, seed=seed)
    Cz = np.array([Z[lab == j].mean(0) if (lab == j).any() else np.zeros(Z.shape[1])
                   for j in range(k)])
    arche = []
    _seen = {}
    for j in range(k):
        members = [roots[i] for i in range(len(roots)) if lab[i] == j]
        tag, desc = _name_archetype(Cz[j], names)
        _seen[tag] = _seen.get(tag, 0) + 1
        if _seen[tag] > 1:
            tag = f"{tag} {_seen[tag]}"
        cl_stab = float(stab[lab == j].mean()) if (lab == j).any() else 0.0
        arche.append(dict(cluster=j, n=len(members), tag=tag, desc=desc,
                          stability=round(cl_stab, 3),
                          examples=sorted(members,
                                          key=lambda r: -(corpus.freq_norm.get(r, 0)
                                          if normalize else corpus.freq_exact.get(r, 0)))[:8]))
    return dict(roots=roots, X=X, Z=Z, feat_names=names, emb=emb, labels=lab,
                centroids_z=Cz, archetypes=arche, var=var, k=k,
                order=order, unit=unit, stability=stab, mean_stability=mean_stab,
                components=comps)


# ═══════════════════════════════════════════════════════════════════════════
# SPATIAL SERIES  (1-D series indexed by position — the time-series toolkit)
# ═══════════════════════════════════════════════════════════════════════════

def density_series(ys, n_total, n_bins=120):
    """Bin a concept's y-positions into a 1-D density series along the ordering."""
    ys = np.asarray(ys, float)
    edges = np.linspace(0, max(n_total, 1), n_bins + 1)
    counts, _ = np.histogram(ys, bins=edges)
    centres = 0.5 * (edges[:-1] + edges[1:])
    return counts.astype(float), centres


def acf(series, max_lag=40):
    """Autocorrelation function of a series (lag 0..max_lag)."""
    x = np.asarray(series, float)
    x = x - x.mean()
    denom = np.dot(x, x)
    if denom == 0:
        return np.zeros(max_lag + 1)
    return np.array([np.dot(x[:len(x) - k], x[k:]) / denom
                     for k in range(max_lag + 1)])


def periodogram(series):
    """FFT power spectrum. Returns (periods-in-bins, power, freqs)."""
    x = np.asarray(series, float) - np.mean(series)
    n = len(x)
    power = np.abs(np.fft.rfft(x)) ** 2
    freqs = np.fft.rfftfreq(n, d=1.0)
    with np.errstate(divide="ignore"):
        periods = np.where(freqs > 0, 1.0 / freqs, np.inf)
    return periods, power, freqs


def dominant_period(series):
    """Strongest non-DC spectral period (in bins) and its fraction of power."""
    periods, power, _ = periodogram(series)
    if len(power) <= 1 or power[1:].sum() == 0:
        return np.nan, 0.0
    idx = np.argmax(power[1:]) + 1
    return float(periods[idx]), float(power[idx] / power[1:].sum())


def lacunarity(series, box=8):
    """Gliding-box lacunarity Λ = 1 + Var/Mean² — texture/gappiness of the series."""
    x = np.asarray(series, float)
    if len(x) < box:
        return np.nan
    s = np.convolve(x, np.ones(box), mode="valid")
    m = s.mean()
    if m == 0:
        return np.nan
    return float(1.0 + s.var() / (m * m))


def cross_correlation(a, b, max_lag=40):
    """Normalised cross-correlation of two density series; peak lag = lead/lag.
    Positive lag means A leads B."""
    a = np.asarray(a, float) - np.mean(a)
    b = np.asarray(b, float) - np.mean(b)
    na = np.sqrt(np.dot(a, a)); nb = np.sqrt(np.dot(b, b))
    lags = np.arange(-max_lag, max_lag + 1)
    if na == 0 or nb == 0:
        return lags, np.zeros(len(lags))
    out = []
    for L in lags:
        if L < 0:
            v = np.dot(a[-L:], b[:len(b) + L])
        elif L > 0:
            v = np.dot(a[:len(a) - L], b[L:])
        else:
            v = np.dot(a, b)
        out.append(v / (na * nb))
    return lags, np.array(out)


def fractal_dimension(kl):
    """Correlation (fractal) dimension D from the Ripley curve: K = π(L+r)²,
    slope of log K vs log r. Returns D and the fit R². EXPLORATORY — the corpus
    is far too short (<3 decades) to claim true fractality; D is a texture descriptor."""
    if not kl:
        return dict(D=np.nan, r2=np.nan)
    r = np.asarray(kl["radii"], float)
    L = np.asarray(kl["L_obs"], float)
    K = np.pi * (L + r) ** 2
    mask = (r > 0) & (K > 0)
    lr = np.log(r[mask]); lk = np.log(K[mask])
    if len(lr) < 4:
        return dict(D=np.nan, r2=np.nan)
    A = np.vstack([lr, np.ones_like(lr)]).T
    coef = np.linalg.lstsq(A, lk, rcond=None)[0]
    pred = A @ coef
    ss = 1.0 - ((lk - pred) ** 2).sum() / (((lk - lk.mean()) ** 2).sum() + 1e-12)
    return dict(D=round(float(coef[0]), 3), r2=round(float(ss), 3))


def concept_series_profile(corpus, target, normalize, order="mushaf",
                           feature="root", n_bins=120, max_lag=40):
    """Full spatial-series profile for one concept under one rearrangement."""
    xy = occ_points(corpus, target, normalize, order, feature=feature)
    if len(xy) == 0:
        return None
    ser, centres = density_series(xy[:, 1], len(corpus.df), n_bins=n_bins)
    a = acf(ser, max_lag=max_lag)
    periods, power, freqs = periodogram(ser)
    dom_p, dom_frac = dominant_period(ser)
    kl = ripley_kl(xy, n_mc=19)
    return dict(target=target, order=order, series=ser, centres=centres,
                acf=a, periods=periods, power=power, freqs=freqs,
                dom_period=dom_p, dom_frac=dom_frac,
                lacunarity=lacunarity(ser), fractal=fractal_dimension(kl), xy=xy)


# ═══════════════════════════════════════════════════════════════════════════
# ARCHETYPE STABILITY  (bootstrap consensus — which roots have a robust archetype)
# ═══════════════════════════════════════════════════════════════════════════

def _align_labels(ref, lab, k):
    """Greedily map a run's cluster ids onto the reference ids by max overlap."""
    M = np.zeros((k, k), int)
    for a, b in zip(ref, lab):
        M[a, b] += 1
    pairs = sorted(((M[a, b], a, b) for a in range(k) for b in range(k)),
                   reverse=True)
    map_b = {}; used_a = set()
    for _, a, b in pairs:
        if b in map_b or a in used_a:
            continue
        map_b[b] = a; used_a.add(a)
    for b in range(k):
        if b not in map_b:
            rem = [a for a in range(k) if a not in used_a]
            map_b[b] = rem[0] if rem else 0
            if rem:
                used_a.add(rem[0])
    return np.array([map_b[x] for x in lab])


def archetype_stability(Z, k, n_boot=25, jitter=0.08, seed=0):
    """Per-root archetype-membership stability: refit k-means n_boot times with
    feature jitter, align labels to a reference, and record how often each root
    lands in its reference cluster. High = robust spatial fingerprint; low =
    sits ambiguously between archetypes."""
    ref, _ = _kmeans(Z, k, seed=seed)
    agree = np.zeros(len(Z))
    rng = np.random.default_rng(seed)
    for b in range(n_boot):
        Zb = Z + jitter * rng.standard_normal(Z.shape)
        lab, _ = _kmeans(Zb, k, seed=b + 1)
        agree += (_align_labels(ref, lab, k) == ref)
    stab = agree / n_boot
    return ref, stab, float(stab.mean())


def archetype_k_scan(Z, ks=(2, 3, 4, 5, 6, 7, 8), n_boot=12, seed=0):
    """Mean bootstrap stability per k — how many archetypes the data supports."""
    out = []
    for k in ks:
        if len(Z) < k:
            continue
        _, _, ms = archetype_stability(Z, k, n_boot=n_boot, seed=seed)
        out.append((int(k), round(ms, 3)))
    return out


# ═══════════════════════════════════════════════════════════════════════════
# SEMANTIC ALIGNMENT  (do spatial archetypes carry MEANING? — independent test)
# ═══════════════════════════════════════════════════════════════════════════

def semantic_alignment(corpus, res, normalize=True, n_perm=99, seed=0):
    """Test whether the spatial feature space aligns with an INDEPENDENT semantic
    space (root co-occurrence / distributional meaning — 'a word by the company it
    keeps'), which uses none of the spatial features.

    Builds a PPMI co-occurrence embedding, then a Mantel correlation between the
    spatial-feature distance matrix and the semantic-distance matrix, with a
    label-permutation null. Positive significant r => spatially-similar concepts
    are also semantically similar => the spatial archetype carries real meaning.
    Also reports within- vs between-archetype semantic cohesion.
    """
    roots = res["roots"]; Z = np.asarray(res["Z"]); lab = np.asarray(res["labels"])
    K = normalize_letters if normalize else (lambda t: t)
    idx = {r: i for i, r in enumerate(roots)}
    m = len(roots)
    if m < 8:
        return None
    C = np.zeros((m, m))
    for toks in corpus.root_tokens:
        present = sorted({idx[K(t)] for t in toks if K(t) in idx})
        for a in range(len(present)):
            ia = present[a]
            for b in range(a + 1, len(present)):
                ib = present[b]
                C[ia, ib] += 1; C[ib, ia] += 1
    total = C.sum()
    if total == 0:
        return None
    rs = C.sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        ppmi = np.log((C / total) / (np.outer(rs, rs) / total ** 2 + 1e-12) + 1e-12)
    ppmi = np.maximum(ppmi, 0.0)
    np.fill_diagonal(ppmi, 0.0)
    nrm = np.linalg.norm(ppmi, axis=1, keepdims=True); nrm[nrm == 0] = 1
    S = ppmi / nrm
    sim = S @ S.T
    Dsem = 1.0 - sim
    Zc = Z - Z.mean(0)
    Dspat = np.sqrt(((Zc[:, None, :] - Zc[None, :, :]) ** 2).sum(-1))
    iu = np.triu_indices(m, 1)
    a = Dspat[iu]; b = Dsem[iu]
    r = float(np.corrcoef(a, b)[0, 1])
    rng = np.random.default_rng(seed)
    cnt = 0
    for _ in range(n_perm):
        p = rng.permutation(m)
        rp = np.corrcoef(a, Dsem[np.ix_(p, p)][iu])[0, 1]
        if abs(rp) >= abs(r):
            cnt += 1
    pval = (cnt + 1) / (n_perm + 1)
    within = []; between = []
    for i in range(m):
        same = lab == lab[i]
        for j in range(i + 1, m):
            (within if same[j] else between).append(sim[i, j])
    return dict(mantel_r=round(r, 3), p=round(float(pval), 4),
                within_sim=round(float(np.mean(within)), 4),
                between_sim=round(float(np.mean(between)), 4),
                cohesion_ratio=round(float(np.mean(within) / (np.mean(between) + 1e-12)), 2),
                m=m)


def occ_surah_ayah(corpus, target, normalize, feature="root", position=None):
    """(surah[], ayah[]) for every occurrence — feeds the 2-D hotspot surface."""
    K = normalize_letters if normalize else (lambda t: t)
    tgt = K(target)
    df = corpus.df
    sarr = df[COL_SURAH].astype(int).to_numpy()
    aarr = df[COL_AYAH].astype(int).to_numpy()
    src = corpus.surface_tokens if feature == "surface" else corpus.root_tokens
    su = []; ay = []
    for i in range(len(df)):
        toks = src[i]; m = len(toks)
        for j, t in enumerate(toks):
            if K(t) != tgt:
                continue
            if position in ("first", 1) and j != 0:
                continue
            if position in ("last", -1) and j != m - 1:
                continue
            if isinstance(position, int) and position not in ("first", "last") \
                    and j != position - 1:
                continue
            su.append(int(sarr[i])); ay.append(int(aarr[i]))
    return np.array(su), np.array(ay)


# ═══════════════════════════════════════════════════════════════════════════
# CONTROL CORPUS  (frequency-matched scramble — is the structure beyond chance?)
# ═══════════════════════════════════════════════════════════════════════════

def _tally_fast(corpus, normalize, order="mushaf", unit="surah",
                min_freq=8, fano_clustered=1.5):
    """One corpus pass + analytic Moran → corpus-wide headline in ~2s. Used for
    the real-vs-scramble control where speed matters (no permutations)."""
    from collections import defaultdict, Counter
    df = corpus.df
    n = len(df)
    su = df[COL_SURAH].astype(int).to_numpy()
    ay = df[COL_AYAH].astype(int).to_numpy()
    oidx = _order_index(corpus, order)
    size = 286 if unit == "ayah_band" else 114
    rev = getattr(corpus, "rev_order_of_surah", {})
    K = normalize_letters
    ylists = defaultdict(list)
    counts = defaultdict(lambda: np.zeros(size + 1))
    freq = Counter()
    for i in range(n):
        toks = corpus.root_tokens[i]
        if not toks:
            continue
        if unit == "ayah_band":
            key = int(ay[i]) if ay[i] <= 286 else 0
        elif unit == "revelation":
            key = int(rev.get(int(su[i]), 0))
        else:
            key = int(su[i])
        seen = set()
        for t in toks:
            r = K(t)
            if r not in seen:
                seen.add(r); freq[r] += 1
            ylists[r].append(int(oidx[i]))
            if 1 <= key <= size:
                counts[r][key] += 1
    W = contiguity_W(size)
    rows = []
    for r, fr in freq.items():
        if fr < min_freq:
            continue
        ys = sorted(ylists[r])
        if len(ys) < 4:
            continue
        gaps = [ys[k + 1] - ys[k] for k in range(len(ys) - 1)]
        fano = _fano_factor(gaps)
        vec = counts[r][1:size + 1]
        cov = int((vec > 0).sum()) / size
        rows.append((fano, cov, morans_I_analytic(vec, W)["klass"]))
    m = len(rows) or 1
    def pct(pred):
        return round(100 * sum(1 for x in rows if pred(x)) / m, 1)
    return dict(n_roots=len(rows),
                local_clustered=pct(lambda x: x[0] > fano_clustered),
                mean_coverage=round(float(np.mean([x[1] for x in rows])), 3),
                I_clustered=pct(lambda x: x[2] == "clustered"),
                I_regular=pct(lambda x: x[2] == "regular"),
                I_random=pct(lambda x: x[2] == "random"))


def make_scramble(corpus, seed=0):
    """A frequency-matched null: globally permute all root tokens while keeping
    each ayah's length and every root's total count. Destroys real spatial /
    sequential structure but preserves the marginal frequency distribution."""
    import copy
    rng = np.random.default_rng(seed)
    flat = [t for toks in corpus.root_tokens for t in toks]
    rng.shuffle(flat)
    new = []
    k = 0
    for toks in corpus.root_tokens:
        n = len(toks)
        new.append(flat[k:k + n]); k += n
    sc = copy.copy(corpus)
    sc.root_tokens = new
    return sc


def control_comparison(corpus, normalize, order="mushaf", unit="surah",
                       min_freq=8, n_seeds=3, max_roots=None):
    """Run the corpus-wide headline on the real text and on `n_seeds`
    frequency-matched scrambles, and compare. Findings that survive the scramble
    are real spatial structure; findings that match it are frequency artifacts."""
    real = _tally_fast(corpus, normalize, order=order, unit=unit, min_freq=min_freq)
    keys = ["local_clustered", "mean_coverage", "I_clustered", "I_regular",
            "I_random"]
    sims = {k: [] for k in keys}
    for sd in range(n_seeds):
        summ = _tally_fast(make_scramble(corpus, seed=sd), normalize,
                           order=order, unit=unit, min_freq=min_freq)
        for k in keys:
            sims[k].append(summ[k])
    null = {k: (round(float(np.mean(v)), 2), round(float(np.std(v)), 2))
            for k, v in sims.items()}
    verdict = {}
    for k in keys:
        mu, sd = null[k]
        diff = real[k] - mu
        z = diff / sd if sd > 0 else (float("inf") if abs(diff) > 1e-6 else 0.0)
        verdict[k] = dict(real=real[k], null_mean=mu, null_sd=sd,
                          diff=round(diff, 2), z=round(z, 1) if np.isfinite(z) else None,
                          beyond_chance=bool(abs(z) >= 2) if np.isfinite(z) else True)
    return dict(real=real, null=null, verdict=verdict, n_seeds=n_seeds,
                n_roots=real["n_roots"])


# ═══════════════════════════════════════════════════════════════════════════
# CO-LOCATION  (bivariate: do two concepts share territory or avoid each other?)
# ═══════════════════════════════════════════════════════════════════════════

def colocation_matrix(corpus, roots, normalize, unit="surah", n_perm=199, seed=0):
    """Pairwise areal co-location of concepts. For each pair, the correlation of
    their per-unit (surah/band) count vectors: + = share territory, − = avoid.
    Significance from permuting one vector's unit labels (keeps marginals, breaks
    alignment). Returns the affinity matrix, p-values, and significant pairs —
    the orthogonal 'semantic geography' dimension (relationships, not magnitudes)."""
    roots = [r for r in roots][:14]
    vecs = []
    for r in roots:
        vals, _ = areal_counts(corpus, r, normalize, unit=unit)
        vecs.append(np.asarray(vals, float))
    V = np.array(vecs)
    R = len(roots)
    if R < 2:
        return None
    Vz = V - V.mean(1, keepdims=True)
    sd = Vz.std(1, keepdims=True); sd[sd == 0] = 1
    Vn = Vz / sd
    aff = (Vn @ Vn.T) / V.shape[1]
    np.fill_diagonal(aff, np.nan)
    rng = np.random.default_rng(seed)
    pvals = np.ones((R, R))
    for i in range(R):
        for j in range(i + 1, R):
            obs = aff[i, j]
            cnt = 0
            base = Vn[i]
            for _ in range(n_perm):
                perm = rng.permutation(Vn[j])
                if abs(np.dot(base, perm) / V.shape[1]) >= abs(obs):
                    cnt += 1
            p = (cnt + 1) / (n_perm + 1)
            pvals[i, j] = pvals[j, i] = p
    sig = []
    for i in range(R):
        for j in range(i + 1, R):
            if pvals[i, j] <= 0.05:
                sig.append((roots[i], roots[j], round(float(aff[i, j]), 3),
                            round(float(pvals[i, j]), 3),
                            "share" if aff[i, j] > 0 else "avoid"))
    sig.sort(key=lambda x: -abs(x[2]))
    return dict(roots=roots, affinity=aff, pvals=pvals, sig=sig, unit=unit)


def colocation_field(corpus, normalize, unit="surah", min_freq=8, feature="root"):
    """One pass → standardized per-unit count vectors for ALL roots (or surface
    forms) ≥ floor. Cache this; it powers fast corpus-wide co-locator lookups."""
    from collections import defaultdict, Counter
    df = corpus.df
    su = df[COL_SURAH].astype(int).to_numpy()
    ay = df[COL_AYAH].astype(int).to_numpy()
    size = 286 if unit == "ayah_band" else 114
    rev = getattr(corpus, "rev_order_of_surah", {})
    K = normalize_letters if normalize else (lambda t: t)
    _src = corpus.surface_tokens if feature == "surface" else corpus.root_tokens
    counts = defaultdict(lambda: np.zeros(size + 1))
    freq = Counter()
    for i in range(len(df)):
        toks = _src[i]
        if not toks:
            continue
        if unit == "ayah_band":
            key = int(ay[i]) if ay[i] <= 286 else 0
        elif unit == "revelation":
            key = int(rev.get(int(su[i]), 0))
        else:
            key = int(su[i])
        seen = set()
        for t in toks:
            r = K(t)
            if r not in seen:
                seen.add(r); freq[r] += 1
            if 1 <= key <= size:
                counts[r][key] += 1
    roots = [r for r, f in freq.items() if f >= min_freq]
    M = np.array([counts[r][1:size + 1] for r in roots])
    Mz = M - M.mean(1, keepdims=True)
    sd = Mz.std(1, keepdims=True); sd[sd == 0] = 1
    return dict(roots=roots, Mn=Mz / sd, size=size,
                index={r: i for i, r in enumerate(roots)})


def colocation_neighbors(corpus, target, normalize, unit="surah", top=15,
                         min_freq=8, n_perm=199, field=None, seed=0, feature="root"):
    """The corpus-wide co-locators of one concept (root OR surface form): the
    items that most SHARE its territory (and most AVOID it), each with a
    permutation p-value."""
    if field is None:
        field = colocation_field(corpus, normalize, unit, min_freq, feature=feature)
    K = normalize_letters if normalize else (lambda t: t)
    tk = K(target)
    if tk in field["index"]:
        tv = field["Mn"][field["index"][tk]]
    else:
        vals, _ = areal_counts(corpus, target, normalize, unit=unit, feature=feature)
        v = np.asarray(vals, float); vz = v - v.mean()
        tv = vz / (vz.std() or 1)
    Mn = field["Mn"]; sz = field["size"]
    aff = (Mn @ tv) / sz
    rng = np.random.default_rng(seed)

    def _withp(idxs):
        out = []
        for j in idxs:
            r = field["roots"][j]
            if r == tk:
                continue
            obs = float(aff[j])
            cnt = sum(1 for _ in range(n_perm)
                      if abs(np.dot(rng.permutation(tv), Mn[j]) / sz) >= abs(obs))
            out.append((r, round(obs, 3), round((cnt + 1) / (n_perm + 1), 3)))
            if len(out) >= top:
                break
        return out

    share = _withp(np.argsort(-aff))
    avoid = _withp(np.argsort(aff))
    return dict(target=target, share=share, avoid=avoid)


def colocation_network(corpus, seeds, normalize, unit="surah", top_per_seed=6,
                       min_freq=8, thr=0.45, max_edges=70, n_perm=99, field=None,
                       seed=0, feature="root"):
    """Expanding semantic-geography graph: start from `seeds`, pull each seed's
    top corpus co-locators in as nodes, then draw significant affinity edges among
    all of them. The seeds + their co-locators are a STARTING POINT to traverse
    outward, not a terminal list."""
    if field is None:
        field = colocation_field(corpus, normalize, unit, min_freq, feature=feature)
    K = normalize_letters if normalize else (lambda t: t)
    idx = field["index"]; roots = field["roots"]; Mn = field["Mn"]; sz = field["size"]
    seedset = set(K(s) for s in seeds)

    def _vec(tk, target):
        if tk in idx:
            return Mn[idx[tk]]
        vals, _ = areal_counts(corpus, target, normalize, unit=unit, feature=feature)
        v = np.asarray(vals, float); vz = v - v.mean()
        return vz / (vz.std() or 1.0)

    nodes, seen, vecmap = [], set(), {}
    for _s in seeds:                       # every seed becomes a node (even rare ones)
        tk = K(_s)
        if tk not in seen:
            nodes.append(tk); seen.add(tk); vecmap[tk] = _vec(tk, _s)
    for _s in seeds:                       # expand each seed's top corpus co-locators
        tk = K(_s)
        aff = (Mn @ vecmap[tk]) / sz
        added = 0
        for j in np.argsort(-aff):
            r = roots[j]
            if r == tk:
                continue
            if r not in seen:
                nodes.append(r); seen.add(r); vecmap[r] = Mn[j]
            added += 1
            if added >= top_per_seed:
                break
    if len(nodes) < 2:
        return None
    sub = np.array([vecmap[n] for n in nodes])
    P = (sub @ sub.T) / sz
    cand = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if abs(P[i, j]) >= thr:
                cand.append((i, j, float(P[i, j])))
    cand.sort(key=lambda e: -abs(e[2])); cand = cand[:max_edges]
    rng = np.random.default_rng(seed)
    edges = []
    for i, j, a in cand:
        cnt = sum(1 for _ in range(n_perm)
                  if abs(np.dot(rng.permutation(sub[i]), sub[j]) / sz) >= abs(a))
        edges.append((nodes[i], nodes[j], round(a, 3),
                      round((cnt + 1) / (n_perm + 1), 3),
                      "share" if a > 0 else "avoid"))
    roles = {n: ("seed" if n in seedset else "colocator") for n in nodes}
    return dict(nodes=nodes, edges=edges, roles=roles, seeds=list(seedset))


# ═══════════════════════════════════════════════════════════════════════════
# CONNECTOME — multi-view concept neighbours (semantic ∥ spatial ∥ co-location)
# ═══════════════════════════════════════════════════════════════════════════
# Tested finding: blended/concatenated fusion DILUTES meaning (semantic-NN
# coherence 0.36→0.22) because spatial/co-location are orthogonal to meaning.
# The three views barely overlap (Jaccard ≈0.03) → keep them SEPARATE and read
# CONSENSUS (a bond confirmed by ≥2 independent views = robust) and DIVERGENCE
# (semantic-but-not-spatial = same meaning, different deployment).

def multiview_embeddings(corpus, normalize, unit="surah", min_freq=8, dims=25):
    """Three orthogonal per-concept embeddings: semantic (PPMI-SVD co-occurrence),
    spatial (the GIS feature vector), co-location (areal-territory SVD)."""
    roots, X, _ = build_feature_matrix(corpus, normalize, "mushaf", unit, min_freq)
    idx = {r: i for i, r in enumerate(roots)}
    n = len(roots)
    Sz = (X - X.mean(0)) / (X.std(0) + 1e-9)
    fld = colocation_field(corpus, normalize, unit, min_freq)
    Ul, Sl, _ = np.linalg.svd(fld["Mn"], full_matrices=False)
    dl = min(dims, Ul.shape[1]); L = Ul[:, :dl] * Sl[:dl]
    Lz = (L - L.mean(0)) / (L.std(0) + 1e-9)
    K = normalize_letters if normalize else (lambda t: t)
    Co = np.zeros((n, n))
    for i in range(len(corpus.df)):
        pres = sorted({idx[K(t)] for t in corpus.root_tokens[i] if K(t) in idx})
        for a in range(len(pres)):
            ia = pres[a]
            for b in range(a + 1, len(pres)):
                ib = pres[b]; Co[ia, ib] += 1; Co[ib, ia] += 1
    tot = Co.sum(); rs = Co.sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        ppmi = np.maximum(np.log((Co / tot) / (np.outer(rs, rs) / tot ** 2 + 1e-12) + 1e-12), 0)
    np.fill_diagonal(ppmi, 0)
    Ud, Sd, _ = np.linalg.svd(ppmi, full_matrices=False)
    dd = min(dims, Ud.shape[1]); Dd = Ud[:, :dd] * Sd[:dd]
    Dz = (Dd - Dd.mean(0)) / (Dd.std(0) + 1e-9)
    return dict(roots=roots, index=idx, spatial=Sz, coloc=Lz, distrib=Dz)


def concept_multiview_neighbors(corpus, target, normalize, k=10, emb=None,
                                unit="surah", min_freq=8):
    """For one concept: its nearest neighbours in each of the 3 orthogonal views,
    plus CONSENSUS (bonds in ≥2 views) and view-specific DIVERGENCE."""
    if emb is None:
        emb = multiview_embeddings(corpus, normalize, unit=unit, min_freq=min_freq)
    idx = emb["index"]; roots = emb["roots"]
    K = normalize_letters if normalize else (lambda t: t)
    tk = K(target)
    if tk not in idx:
        return None

    def nn(M):
        v = M[idx[tk]]
        d = ((M - v) ** 2).sum(1)
        return [roots[j] for j in np.argsort(d) if roots[j] != tk][:k]

    views = {"semantic": nn(emb["distrib"]), "spatial": nn(emb["spatial"]),
             "co-location": nn(emb["coloc"])}
    from collections import Counter
    cnt = Counter()
    where = {}
    for vn, vs in views.items():
        for r in vs:
            cnt[r] += 1; where.setdefault(r, []).append(vn)
    consensus = sorted([(r, where[r]) for r in cnt if cnt[r] >= 2],
                       key=lambda x: -len(x[1]))
    sem_only = [r for r in views["semantic"] if cnt[r] == 1]      # meaning, not territory
    return dict(target=target, views=views, consensus=consensus, sem_only=sem_only)
