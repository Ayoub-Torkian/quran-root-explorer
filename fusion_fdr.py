"""FDR-gated LATENT MOTIFS. A latent motif = a consensus triangle (3 concepts
mutually bonded across >=2 of semantic/co-location/spatial) whose 3 members NEVER
share a verse. Test each triangle's tri-modal coherence against a cross-modal-
ALIGNMENT null (permute co-location & spatial candidate axes), pool the null
triangle-strengths, compute an empirical right-tail p per real latent triangle,
then Benjamini-Hochberg at q=0.05. Output = the ranked, GATED list (real evidence)."""
import time, bisect
from collections import defaultdict
import numpy as np
import analysis as A
import spatial_patterns as SP

t0 = time.time()
c = A.load_corpus("Book6.xlsx")
emb = SP.multiview_embeddings(c, True, unit="surah", min_freq=8)
roots = emb["roots"]; D = emb["distrib"]; L = emb["coloc"]; S = emb["spatial"]
n = len(roots); K = A.normalize_letters; freq = c.freq_norm


def rowz(M):
    G = M @ M.T; sq = np.diag(G).copy()
    sim = -(sq[:, None] + sq[None, :] - 2 * G); np.fill_diagonal(sim, np.nan)
    mu = np.nanmean(sim, 1, keepdims=True); sd = np.nanstd(sim, 1, keepdims=True); sd[sd == 0] = 1
    z = (sim - mu) / sd; np.fill_diagonal(z, -9.0); return z


ZD, ZL, ZS = rowz(D), rowz(L), rowz(S)
ayahset = defaultdict(set)
for i, toks in enumerate(c.root_tokens):
    for t in {K(x) for x in toks}:
        ayahset[t].add(i)


def triangles(zd, zl, zs):
    cons = ((zd >= 1).astype(int) + (zl >= 1).astype(int) + (zs >= 1).astype(int)) >= 2
    mutual = cons & cons.T
    adj = [set(np.where(mutual[u])[0].tolist()) for u in range(n)]
    out = []
    for u in range(n):
        nb = sorted(x for x in adj[u] if x > u)
        for ii in range(len(nb)):
            v = nb[ii]
            for jj in range(ii + 1, len(nb)):
                w = nb[jj]
                if w in adj[v]:
                    sdef = (zd[u, v] + zl[u, v] + zs[u, v] + zd[u, w] + zl[u, w]
                            + zs[u, w] + zd[v, w] + zl[v, w] + zs[v, w])
                    out.append((float(sdef), (u, v, w)))
    return out


real = triangles(ZD, ZL, ZS)
def tco(t): a, b, d = (roots[x] for x in t); return len(ayahset[a] & ayahset[b] & ayahset[d])
latent = [(s, t) for (s, t) in real if tco(t) == 0]
print(f"consensus triangles={len(real)}  latent(co-occur=0)={len(latent)}  ({time.time()-t0:.1f}s build)")

rng = np.random.default_rng(0)
null_s = []
B = 6
for _ in range(B):
    nt = triangles(ZD, ZL[:, rng.permutation(n)], ZS[:, rng.permutation(n)])
    null_s.extend(s for s, _ in nt)
null_s = np.sort(np.array(null_s)); Nn = len(null_s)
print(f"null pool={Nn} triangles over {B} draws  (null strength: mean={null_s.mean():.1f} 99pct={np.percentile(null_s,99):.1f} max={null_s.max():.1f})")

def pval(s):
    return (Nn - bisect.bisect_left(null_s, s) + 1) / (Nn + 1)

scored = sorted(((pval(s), s, t) for s, t in latent))
m = len(scored); q = 0.05
ksig = 0
for k in range(m, 0, -1):
    if scored[k - 1][0] <= k / m * q:
        ksig = k; break
print(f"\nFDR q=0.05 → {ksig} of {m} latent motifs SURVIVE (beyond the alignment null).")
print("rank  Σz     p         latent motif (3 roots that never share a verse)   [min pairwise co-occur]")
seen = set(); shown = 0
for p, s, t in sorted(scored, key=lambda x: -x[1]):
    key = tuple(sorted(t))
    if key in seen:
        continue
    seen.add(key)
    a, b, d = (roots[x] for x in t)
    mn = min(len(ayahset[a] & ayahset[b]), len(ayahset[a] & ayahset[d]), len(ayahset[b] & ayahset[d]))
    shown += 1
    print(f"  {shown:>2}  {s:5.1f}  {p:.2e}   {a} · {b} · {d:8}   [{mn}]")
    if shown >= 22:
        break
print(f"\ntotal {time.time()-t0:.1f}s")
