"""Corpus-wide MULTIMODAL FUSION scan with a cross-modal-alignment NULL.

For every concept, classify its relation to every other concept across the three
independent modalities (semantic ∥ co-location ∥ spatial), tally the six types,
and compare the REAL cross-modal structure to a null in which each modality's
neighbour-rankings are kept but their ALIGNMENT across modalities is randomised.
Finding survives only if real >> null. Honest by construction: prints the verdict
AND the stopping signal if the off-diagonal classes are at chance.
"""
import time
import numpy as np
import analysis as A
import spatial_patterns as SP

t0 = time.time()
c = A.load_corpus("Book6.xlsx")
emb = SP.multiview_embeddings(c, True, unit="surah", min_freq=8)
roots = emb["roots"]; D = emb["distrib"]; L = emb["coloc"]; S = emb["spatial"]
n = len(roots)
freq = c.freq_norm


def rowz(M):
    G = M @ M.T
    sq = np.diag(G).copy()
    d2 = sq[:, None] + sq[None, :] - 2 * G
    sim = -d2
    np.fill_diagonal(sim, np.nan)
    mu = np.nanmean(sim, 1, keepdims=True)
    sd = np.nanstd(sim, 1, keepdims=True); sd[sd == 0] = 1
    z = (sim - mu) / sd
    np.fill_diagonal(z, -9.0)
    return z


ZD, ZL, ZS = rowz(D), rowz(L), rowz(S)
HI, NEG, NEAR = 1.0, -1.0, 0.5


def classify(zd, zl, zs):
    hD, hL, hS = zd >= HI, zl >= HI, zs >= HI
    nh = hD.astype(int) + hL.astype(int) + hS.astype(int)
    anyneg = (zd <= NEG) | (zl <= NEG) | (zs <= NEG)
    consensus = nh >= 2
    one = nh == 1
    divergent = one & anyneg
    nearD = (~hD) & (np.abs(zd) < NEAR)
    nearL = (~hL) & (np.abs(zl) < NEAR)
    nearS = (~hS) & (np.abs(zs) < NEAR)
    # orthogonal: exactly one high, the other two within NEAR of 0
    nonhigh_near = (hD | nearD) & (hL | nearL) & (hS | nearS)
    orthogonal = one & (~anyneg) & nonhigh_near
    return dict(consensus=int(consensus.sum()), divergent=int(divergent.sum()),
                orthogonal=int(orthogonal.sum()), related=int((nh >= 1).sum()),
                consensus_per=consensus.sum(1), divergent_per=divergent.sum(1))


real = classify(ZD, ZL, ZS)

rng = np.random.default_rng(0)
keys = ["consensus", "divergent", "orthogonal", "related"]
null = {k: [] for k in keys}
for _ in range(6):
    pl = rng.permutation(n); ps = rng.permutation(n)
    nd = classify(ZD, ZL[:, pl], ZS[:, ps])
    for k in keys:
        null[k].append(nd[k])

print(f"n_concepts={n}   ({time.time()-t0:.1f}s to build)")
print(f"{'class':12} {'real':>8} {'null_mean':>10} {'null_sd':>8} {'z':>7}  verdict")
for k in keys:
    mu = float(np.mean(null[k])); sd = float(np.std(null[k]) or 1e-9)
    z = (real[k] - mu) / sd
    v = ("BEYOND CHANCE" if z >= 3 else "at chance" if abs(z) < 3 else "below chance")
    print(f"{k:12} {real[k]:>8} {mu:>10.1f} {sd:>8.1f} {z:>7.1f}  {v}")

# strongest MUTUAL consensus bonds (i in j's >=2-view neighbours AND vice versa)
hi2 = (ZD >= HI).astype(int) + (ZL >= HI).astype(int) + (ZS >= HI).astype(int)
cons = hi2 >= 2
mutual = cons & cons.T
pairs = []
for i in range(n):
    for j in range(i + 1, n):
        if mutual[i, j]:
            strength = float(ZD[i, j] + ZL[i, j] + ZS[i, j] + ZD[j, i] + ZL[j, i] + ZS[j, i])
            pairs.append((strength, roots[i], roots[j]))
pairs.sort(reverse=True)
print(f"\nMUTUAL consensus bonds (robust, both directions, >=2 views): {len(pairs)}")
for s, a, b in pairs[:15]:
    print(f"   {a} <-> {b}   (Σz={s:.1f})")

# top 'contested' concepts: most divergent partners
order = np.argsort(-real["divergent_per"])
print("\nMost-divergent concepts (deployment fights meaning) — real counts:")
for i in order[:12]:
    print(f"   {roots[i]:6} divergent={int(real['divergent_per'][i])}  consensus={int(real['consensus_per'][i])}  freq={int(freq.get(roots[i],0))}")
print(f"\ntotal {time.time()-t0:.1f}s")
