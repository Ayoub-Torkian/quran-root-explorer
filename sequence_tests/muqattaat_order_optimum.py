"""#69 — calibrating #68: how good is the abjadī key, absolutely? + secondary-key sweep (rasm only).

THREE QUESTIONS, all data-driven (no storytelling about the violations):
 (1) CEILING: what is the maximum concordance ANY total order of the 14 letters could achieve on the
     muqaṭṭaʿāt openings? (exact, via bitmask DP over all orderings — the m→ʿ→s→m 3-cycle caps it.)
 (2) RANK: where does the a-priori abjadī key sit among ALL total orders? (1e6 random permutations.)
 (3) SECONDARY KEY: do the 5 violating pairs follow the makhārij (articulation-point) order instead?

RESULTS:
  CEILING: 0.978 (44/45) distinct / 0.975 per-sūra — exactly one pair is unsortable by ANY order (the
    3-cycle); the optimal orders themselves are overfit strings (e.g. احطلمركهيعسصقن), not a known key.
  ABJADĪ: 0.889 — only 4 pairs below the absolute ceiling; rank ~436/1e6 ≈ TOP 0.04% of all total orders
    (per-sūra: 0.925, top ~0.05%). An a-priori historical key sitting near the data-fit optimum.
  MAKHĀRIJ: 0.644 asc / 0.738 per-sūra — sub-significant; articulation is NOT the secondary key.
  VIOLATION ANATOMY (descriptive): every deviating combo is exactly ONE local move from its abjadī-sorted
    form — حمعسق: adjacent swap (ع↔س); طسم: swap at distance 2 (س↔م); طه: swap (ط↔ه); كهيعص: a single
    fronting of ك (sorted form هيكعص). Deviations are local perturbations of the key, not a rival system.
    The كهيعص fronted-ك remains UNEXPLAINED (no gated secondary key); filed as the open outlier.

GATE: planted abjadī-sorted input -> DP optimum reads 1.000. Sui generis / Qur'an-internal.
RUN DISCIPLINE: author/run in /tmp (mount lag); host copy for the user. EVIDENCE #69.
"""
import re, itertools
import numpy as np

rng = np.random.default_rng(69)


def rasm(t):
    t = re.sub(r"[ً-ْٰـٕ-ٟ]", "", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    return "".join(re.findall(r"[ء-ي]", t))


MUQ_RAW = {2: "الم", 3: "الم", 7: "المص", 10: "الر", 11: "الر", 12: "الر", 13: "المر", 14: "الر",
           15: "الر", 19: "كهيعص", 20: "طه", 26: "طسم", 27: "طس", 28: "طسم", 29: "الم", 30: "الم",
           31: "الم", 32: "الم", 36: "يس", 38: "ص", 40: "حم", 41: "حم", 42: "حمعسق", 43: "حم",
           44: "حم", 45: "حم", 46: "حم", 50: "ق", 68: "ن"}
COMBOS = sorted(set(rasm(v) for v in MUQ_RAW.values()))
SEQS = [list(c) for c in COMBOS if len(c) >= 2]
SEQS_W = [list(rasm(v)) for v in MUQ_RAW.values() if len(rasm(v)) >= 2]
L = sorted(set("".join(COMBOS))); idx = {l: i for i, l in enumerate(L)}; n = len(L)

ABJD = [l for l in "ابجدهوزحطيكلمنسعفصقرشتثخذضظغ" if l in idx]
MAKH = [l for l in "اهعحقكيصسرنطلم" if l in idx]  # articulation deepest-first, restricted


def W_of(seqs):
    W = np.zeros((n, n))
    for s in seqs:
        for a, b in itertools.combinations(s, 2):
            if a != b:
                W[idx[a], idx[b]] += 1
    return W


def conc_of_order(order, W):
    r = {l: i for i, l in enumerate(order)}
    good = sum(W[idx[a], idx[b]] for a in L for b in L if a != b and r[a] < r[b])
    return good / W.sum()


def optimal(W):
    full = 1 << n
    g = np.zeros((n, full))
    for j in range(n):
        for S in range(1, full):
            low = (S & -S).bit_length() - 1
            g[j][S] = g[j][S ^ (1 << low)] + W[low, j]
    dp = np.full(full, -1.0); dp[0] = 0.0; par = np.zeros(full, dtype=int)
    for S in range(full):
        if dp[S] < 0:
            continue
        for j in range(n):
            if S >> j & 1:
                continue
            T = S | (1 << j); v = dp[S] + g[j][S]
            if v > dp[T]:
                dp[T] = v; par[T] = j
    order = []; S = full - 1
    while S:
        j = par[S]; order.append(L[j]); S ^= (1 << j)
    return dp[full - 1] / W.sum(), order[::-1]


def main():
    for name, seqs in (("distinct-combos", SEQS), ("per-sura", SEQS_W)):
        W = W_of(seqs); tot = int(W.sum())
        if name == "distinct-combos":
            r = {l: i for i, l in enumerate(ABJD)}
            Wp = W_of([sorted(s, key=lambda l: r[l]) for s in seqs])
            print(f"GATE planted optimum = {optimal(Wp)[0]:.3f} (need 1.0)")
        best, order = optimal(W)
        abj = conc_of_order(ABJD, W)
        mak = conc_of_order(MAKH, W); makr = conc_of_order(MAKH[::-1], W)
        pairs = [(idx[a], idx[b], W[idx[a], idx[b]]) for a in L for b in L
                 if a != b and W[idx[a], idx[b]] > 0]
        A = np.array([p[0] for p in pairs]); B = np.array([p[1] for p in pairs])
        wts = np.array([p[2] for p in pairs])
        cnt_ge = cnt_opt = 0
        for _ in range(20):
            ranks = np.argsort(rng.random((50000, n)), axis=1).argsort(axis=1)
            sc = ((ranks[:, A] < ranks[:, B]) * wts).sum(axis=1) / wts.sum()
            cnt_ge += int((sc >= abj - 1e-12).sum()); cnt_opt += int((sc >= best - 1e-12).sum())
        print(f"\n[{name}] pairs={tot}")
        print(f"  OPTIMAL order : {''.join(order)}  conc={best:.3f}")
        print(f"  abjadi        : conc={abj:.3f}  gap={int(round((best - abj) * tot))} pairs  "
              f"rank: {cnt_ge}/1e6 >= abjadi; {cnt_opt}/1e6 >= optimum")
        print(f"  makharij      : asc {mak:.3f} / desc {makr:.3f}")
    r = {l: i for i, l in enumerate(ABJD)}
    print("\nviolating pairs (abjadi, distinct):")
    for s in SEQS:
        v = [(a, b) for a, b in itertools.combinations(s, 2) if a != b and r[a] > r[b]]
        if v:
            adjz = ["ADJACENT-rank-swap" if abs(ABJD.index(a) - ABJD.index(b)) == 1
                    else f"dist={abs(ABJD.index(a) - ABJD.index(b))}" for a, b in v]
            print(f"  {''.join(s)}: {v} {adjz}")


if __name__ == "__main__":
    main()
