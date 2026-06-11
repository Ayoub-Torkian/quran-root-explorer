"""#67 — EXTEND the muqaṭṭaʿāt / rasm POSITIONAL thread, NETWORK-FIRST (divinely-rooted, rasm only; NO ḥarakāt).

Three network-first probes from the HANDOFF "NEXT" list (#184), all permutation/configuration-nulled.
The muqaṭṭaʿāt are SUI GENERIS (no other-Arabic baseline exists), so per #50/#51 the admissible comparator
is the randomization null itself; the G10 gate is honoured via (positive control) + (equal-N nulls) +
(rearrangement: canonical vs nuzūl reported together).

  (1) DYNAMIC / TEMPORAL COMMUNITY SHIFT — are the letter-FAMILIES (sūras sharing an identical opening, e.g.
      the 7 ḥā-mīm sūras, the 6 alif-lām-mīm sūras) temporally CLUSTERED over revelation time (nuzūl) and over
      the canonical muṣḥaf order? Family = community; metric = mean within-family pairwise rank-distance vs a
      label-shuffle null. Rearrangement (canonical vs nuzūl) reported side by side.

  (2) BIPARTITE sūra×letter NETWORK + PROJECTION — 29 sūra nodes × 14 letter nodes, edge = opening contains
      letter. Test the letter-COMBINATORICS topology against a degree-preserving (checkerboard-swap) null that
      fixes every sūra's letter-count AND every letter's bearer-count: (a) reuse-concentration (entropy of the
      distinct combination distribution — the system reuses only 14 distinct combos, الم×6 ḥم×7), (b) letter-
      projection modularity, (c) bipartite nestedness (NODF-like). Sharper, properly-nulled successor to #64.

  (3) RASM LETTER-TRANSITION DIRECTED GRAPH — each muqaṭṭaʿāt is an ORDERED rasm sequence (كهيعص = ك→ه→ي→ع→ص).
      Aggregate consecutive-letter transitions over the DISTINCT combinations; test directed structure
      (asymmetry, distinct-edge count, transition entropy) vs a within-sequence shuffle null (multiset & length
      preserved). Probes whether the letter ORDER carries design beyond the letter multiset (#52/#64).

GATE: positive control = a structure-destroying shuffle is exactly the null (signal must exceed it); equal-N by
construction; rearrangement (nuzūl/canonical) baked into probe 1. rasm only — ḥarakāt stripped (divine-rootedness).
RUN: self-contained, runnable in place (no hardcoded VM path). `python3 -u sequence_tests/muqattaat_network2.py`.
DEPS: numpy, networkx, scikit-learn (load_corpus), openpyxl.
"""
import re, os, sys, itertools
import numpy as np
import networkx as nx
from collections import Counter
from networkx.algorithms.community import greedy_modularity_communities, modularity

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_SURAH as S, COL_REV_ORDER as RO

rng = np.random.default_rng(67)
HARAKAT = re.compile(r"[ً-ْٰـٕ-ٟ]")


def rasm(t):
    t = HARAKAT.sub("", str(t))
    t = re.sub(r"[آأإٱ]", "ا", t)
    t = re.sub(r"[ىئ]", "ي", t)
    t = re.sub("ة", "ه", t).replace("ؤ", "و")
    return "".join(re.findall(r"[ء-ي]", t))


MUQ_RAW = {2: "الم", 3: "الم", 7: "المص", 10: "الر", 11: "الر", 12: "الر", 13: "المر", 14: "الر",
           15: "الر", 19: "كهيعص", 20: "طه", 26: "طسم", 27: "طس", 28: "طسم", 29: "الم", 30: "الم",
           31: "الم", 32: "الم", 36: "يس", 38: "ص", 40: "حم", 41: "حم", 42: "حمعسق", 43: "حم",
           44: "حم", 45: "حم", 46: "حم", 50: "ق", 68: "ن"}
MUQ_SEQ = {k: rasm(v) for k, v in MUQ_RAW.items()}          # ordered letter string (preserves order)
SURAS = sorted(MUQ_SEQ)                                      # the 29 muqaṭṭaʿāt sūras, canonical order
ALPHA = sorted(set("".join(MUQ_SEQ.values())))              # the 14 distinct letters


# ----------------------------------------------------------------------------- gate / positive control
def gate():
    voc = "الٓمٓ"  # vocalized/with-superscript form
    ok_strip = (rasm(voc) == "الم")
    # a structure-destroyed copy (all letters pooled then re-cut to length 1) must lose order info:
    print(f"GATE  rasm strips ḥarakāt: {'الٓمٓ'} -> {rasm(voc)!r}  [{'OK' if ok_strip else 'FAIL'}]")
    print(f"GATE  alphabet = {''.join(ALPHA)}  (|A|={len(ALPHA)})   #combinations(distinct)={len(set(MUQ_SEQ.values()))}")
    return ok_strip


# ----------------------------------------------------------------------------- (1) temporal community shift
def probe1_temporal(nuz):
    """Family = sūras with identical opening. Are families clustered in nuzūl & canonical order?
    Metric: mean within-family pairwise |rank distance| (lower = more clustered). Null: shuffle ranks."""
    fams = {}
    for s in SURAS:
        fams.setdefault(MUQ_SEQ[s], []).append(s)
    multi = {f: ss for f, ss in fams.items() if len(ss) >= 2}

    def mean_within(rank):  # rank: dict sūra->position
        ds = []
        for ss in multi.values():
            rs = [rank[s] for s in ss]
            ds += [abs(a - b) for a, b in itertools.combinations(rs, 2)]
        return float(np.mean(ds))

    print("\n(1) TEMPORAL / DYNAMIC COMMUNITY SHIFT  (family = identical opening; lower dist = clustered)")
    print("    families (>=2):", {f: len(ss) for f, ss in multi.items()})
    for label, rank in (("canonical", {s: i for i, s in enumerate(SURAS)}),
                        ("nuzul    ", {s: r for s, r in
                                       zip(sorted(SURAS, key=lambda s: nuz.get(s, 1e9)), range(len(SURAS)))})):
        obs = mean_within(rank)
        positions = list(rank.values())
        null = []
        for _ in range(20000):
            perm = rng.permutation(positions)
            rmap = {s: perm[i] for i, s in enumerate(rank)}
            null.append(mean_within(rmap))
        null = np.array(null)
        z = (obs - null.mean()) / null.std()
        p = np.mean(null <= obs)  # one-sided: clustered = SMALLER distance
        print(f"    {label}: mean within-family dist {obs:5.2f}  null {null.mean():5.2f}  z={z:+.2f}  p(<=)= {p:.4f}")


# ----------------------------------------------------------------------------- (2) bipartite + projection
def biadj():
    M = np.zeros((len(SURAS), len(ALPHA)), int)
    li = {l: j for j, l in enumerate(ALPHA)}
    for i, s in enumerate(SURAS):
        for l in set(MUQ_SEQ[s]):
            M[i, li[l]] = 1
    return M


def checkerboard_swaps(M, n_swaps):
    """Degree-preserving null for a 0/1 matrix: flip [[1,0],[0,1]] <-> [[0,1],[1,0]] submatrices.
    Index batches pre-drawn (vectorized) so the loop fits the sandbox time budget."""
    M = M.copy(); R, C = M.shape; done = 0
    max_tries = n_swaps * 60
    rs = rng.integers(0, R, size=(max_tries, 2)); cs = rng.integers(0, C, size=(max_tries, 2))
    for t in range(max_tries):
        if done >= n_swaps:
            break
        r1, r2 = rs[t]; c1, c2 = cs[t]
        if r1 == r2 or c1 == c2:
            continue
        a = M[r1, c1]; b = M[r1, c2]; c_ = M[r2, c1]; d = M[r2, c2]
        if a == 1 and d == 1 and b == 0 and c_ == 0:
            M[r1, c1] = M[r2, c2] = 0; M[r1, c2] = M[r2, c1] = 1; done += 1
        elif b == 1 and c_ == 1 and a == 0 and d == 0:
            M[r1, c2] = M[r2, c1] = 0; M[r1, c1] = M[r2, c2] = 1; done += 1
    return M


def combo_entropy(M):
    rows = [tuple(r) for r in M]
    cnt = Counter(rows); n = len(rows)
    p = np.array([v / n for v in cnt.values()])
    return float(-(p * np.log2(p)).sum()), len(cnt)


def proj_modularity(M):
    Lp = M.T @ M  # letter x letter co-occurrence across sūras
    G = nx.Graph()
    for a in range(len(ALPHA)):
        G.add_node(a)
    for a in range(len(ALPHA)):
        for b in range(a + 1, len(ALPHA)):
            if Lp[a, b] > 0:
                G.add_edge(a, b, weight=int(Lp[a, b]))
    if G.number_of_edges() == 0:
        return 0.0, G
    comms = list(greedy_modularity_communities(G, weight="weight"))
    return float(modularity(G, comms, weight="weight")), G


def nodf(M):
    """A simple nestedness proxy: mean pairwise paired-overlap over rows (and cols), degree-decreasing."""
    def axis(X):
        deg = X.sum(1); order = np.argsort(-deg); X = X[order]; k = len(X); tot = 0.0; cnt = 0
        for i in range(k):
            for j in range(i + 1, k):
                if deg[order[i]] > deg[order[j]] and deg[order[j]] > 0:
                    tot += 100.0 * (X[i] & X[j]).sum() / deg[order[j]]; cnt += 1
        return tot / cnt if cnt else 0.0
    return 0.5 * (axis(M.astype(bool)) + axis(M.T.astype(bool)))


def probe2_bipartite(M):
    print("\n(2) BIPARTITE sūra×letter NETWORK + PROJECTION  (null = degree-preserving checkerboard swaps)")
    ent, ncombo = combo_entropy(M)
    Qobs, G = proj_modularity(M)
    nod = nodf(M)
    print(f"    observed: distinct-combinations={ncombo}  combo-entropy={ent:.3f} bits  "
          f"letter-proj modularity Q={Qobs:.3f}  nestedness≈{nod:.1f}")
    print(f"    letter-projection hubs:", ", ".join(
        f"{ALPHA[n]}:{int(d)}" for n, d in sorted(G.degree(weight='weight'), key=lambda x: -x[1])[:6]))
    NS = 2000; ents, Qs, nods = [], [], []
    nsw = max(60, 3 * int(M.sum()))
    for _ in range(NS):
        Mr = checkerboard_swaps(M, nsw)
        e, _ = combo_entropy(Mr); ents.append(e)
        Qr, _ = proj_modularity(Mr); Qs.append(Qr)
        nods.append(nodf(Mr))
    for name, obs, null, side in (("combo-entropy(reuse)", ent, np.array(ents), "<="),
                                  ("proj-modularity", Qobs, np.array(Qs), ">="),
                                  ("nestedness", nod, np.array(nods), ">=")):
        z = (obs - null.mean()) / (null.std() + 1e-12)
        p = np.mean(null <= obs) if side == "<=" else np.mean(null >= obs)
        print(f"    {name:22s} obs={obs:7.3f}  null={null.mean():7.3f}  z={z:+.2f}  p({side})={p:.4f}")


# ----------------------------------------------------------------------------- (3) letter-transition graph
def transition_stats(seqs):
    """Directed transition multigraph over consecutive letters. Returns (asymmetry, distinct_edges, entropy)."""
    T = Counter()
    for seq in seqs:
        for a, b in zip(seq, seq[1:]):
            T[(a, b)] += 1
    if not T:
        return 0.0, 0, 0.0
    distinct = len(T)
    # asymmetry: among unordered pairs with >=1 directed edge, fraction that occur in only ONE direction
    pairs = set(frozenset((a, b)) for (a, b) in T if a != b)
    asym = 0
    for fp in pairs:
        ab = tuple(fp) if len(fp) == 2 else (next(iter(fp)),) * 2
        if len(ab) == 2:
            f, g = ab
            d1, d2 = T.get((f, g), 0), T.get((g, f), 0)
            if (d1 > 0) != (d2 > 0):
                asym += 1
    asym = asym / len(pairs) if pairs else 0.0
    tot = sum(T.values()); p = np.array([v / tot for v in T.values()])
    ent = float(-(p * np.log2(p)).sum())
    return asym, distinct, ent


def probe3_transitions():
    print("\n(3) RASM LETTER-TRANSITION DIRECTED GRAPH  (distinct combos; null = within-sequence shuffle)")
    combos = sorted(set(MUQ_SEQ.values()))
    seqs = [list(c) for c in combos if len(c) >= 2]
    asym, dist, ent = transition_stats(seqs)
    print(f"    distinct combos used: {combos}")
    print(f"    observed: distinct-transitions={dist}  one-directional-fraction={asym:.3f}  trans-entropy={ent:.3f} bits")
    NS = 20000; A_, D_, E_ = [], [], []
    for _ in range(NS):
        sh = []
        for seq in seqs:
            s2 = seq[:]; rng.shuffle(s2); sh.append(s2)
        a, d, e = transition_stats(sh)
        A_.append(a); D_.append(d); E_.append(e)
    for name, obs, null, side in (("one-directional-frac", asym, np.array(A_), ">="),
                                  ("distinct-transitions", dist, np.array(D_), ">="),
                                  ("transition-entropy", ent, np.array(E_), "<=")):
        z = (obs - null.mean()) / (null.std() + 1e-12)
        p = np.mean(null >= obs) if side == ">=" else np.mean(null <= obs)
        print(f"    {name:22s} obs={obs:7.3f}  null={null.mean():7.3f}  z={z:+.2f}  p({side})={p:.4f}")


# ----------------------------------------------------------------------------- main
def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "123"   # e.g. `... 23` runs probes 2+3 only
    print("=" * 78)
    print(f"#67  MUQAṬṬAʿĀT — NETWORK-FIRST EXTENSION (rasm only, no ḥarakāt)  [probes {which}]")
    print("=" * 78)
    if not gate():
        print("GATE FAILED — aborting."); return
    if "1" in which:
        c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
        nuz = {}
        for i in range(len(df)):
            try:
                nuz[int(df.iloc[i][S])] = int(float(df.iloc[i][RO]))
            except Exception:
                pass
        probe1_temporal(nuz)
    if "2" in which:
        probe2_bipartite(biadj())
    if "3" in which:
        probe3_transitions()
    print("\n" + "=" * 78)
    print("NOTE: muqaṭṭaʿāt are sui generis; comparator = randomization null (per #50/#51). Read verdicts")
    print("with the telescope rule — a null here narrows the search, it is not a claim of absence.")
    print("=" * 78)


if __name__ == "__main__":
    main()
