"""#73 — MULTI-LAYER CONNECTOME (letters↔roots↔āyahs↔sūras): one gated cross-layer claim + map stats.

GATED CORE (D8 mandate — retest the phonosemantics null at a NEW grain): do roots that SHARE LETTERS
also SHARE CONTEXTS? Letter-layer similarity = Jaccard of root lettersets (954 roots freq≥4, 28-letter
alphabet, ک/ی normalized); context-layer = āyah-grain co-occurrence (PPMI, co≥2; 29,456 co-occurring
pairs of 454,581). Null = permute the root→letterset assignment (1000×, simultaneous row/col permutation
of the Jaccard matrix). GATE: planting identical lettersets on the top-200 PPMI pairs fires at z≈+15.

RESULT: NULL — and gate-validated.
  A corr(letterJ, PPMI | co≥2): obs −0.0175, null +0.0003, z=−1.74, p₂=0.074
  B ΔJaccard (co≥2 vs co<2):   obs +0.0029,  z=+1.23, p₂=0.21
No form↔meaning coupling at root grain. The faint NEGATIVE direction of A (roots sharing letters
co-occur marginally LESS) is sub-2σ but consistent with known Arabic root phonotactics (OCP-style
dissimilation) — noted descriptively, not claimed. This CONFIRMS the dead phonosemantics lens (#38) at
a second grain: the lexical-semantic network is independent of the letter layer, exactly as #56/#64
found content independent of the muqaṭṭaʿāt letters.

MAP STATS (descriptive): letter-layer participation hubs ر(276 roots) و ل ب م ن ي ع; the 14 muqaṭṭaʿāt
letters average 127 root-participations vs 75 for the other 14 (descriptive only — the 14 include the
commonest consonants; no claim).
BOUNDARY: lexical layer (root spellings), Qur'an-internal; comparator = permutation null.
EVIDENCE #73. RUN DISCIPLINE: /tmp heredoc; host copy for the user.
"""
import os, sys
import numpy as np
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_SURAH as S, COL_ROOTS as RR

rng = np.random.default_rng(73)


def main():
    df = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")).df
    roots_ay = [[r for r in str(df.iloc[i][RR]).split() if r and r != "nan"] for i in range(len(df))]
    cnt = Counter(r for ay in roots_ay for r in ay)
    R = sorted([r for r, c in cnt.items() if c >= 4])
    ridx = {r: i for i, r in enumerate(R)}; n = len(R)
    lsets = [set(r.replace("ک", "ك").replace("ی", "ي")) for r in R]
    alpha = sorted(set().union(*lsets)); amap = {c: i for i, c in enumerate(alpha)}
    bits = np.zeros(n, dtype=np.uint64)
    for i, ls in enumerate(lsets):
        b = 0
        for c in ls:
            b |= (1 << amap[c])
        bits[i] = b
    pop = np.zeros(1 << 16, dtype=np.uint8)
    for x in range(1, 1 << 16):
        pop[x] = pop[x >> 1] + (x & 1)

    def popcount(a):
        a = a.astype(np.uint64)
        return (pop[a & np.uint64(0xFFFF)] + pop[(a >> np.uint64(16)) & np.uint64(0xFFFF)] +
                pop[(a >> np.uint64(32)) & np.uint64(0xFFFF)] +
                pop[(a >> np.uint64(48)) & np.uint64(0xFFFF)]).astype(np.int16)

    J = np.zeros((n, n), dtype=np.float32); sz = popcount(bits)
    for i in range(n):
        inter = popcount(bits[i] & bits)
        J[i] = inter / np.maximum(sz[i] + sz - inter, 1)
    np.fill_diagonal(J, 0)

    co = np.zeros((n, n), dtype=np.float32); occ = np.zeros(n)
    for ay in roots_ay:
        ids = sorted(set(ridx[r] for r in ay if r in ridx))
        for i in ids:
            occ[i] += 1
        for a in range(len(ids)):
            for b in range(a + 1, len(ids)):
                co[ids[a], ids[b]] += 1; co[ids[b], ids[a]] += 1
    Nay = len(roots_ay); pi = occ / Nay
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log((co / Nay) / (pi[:, None] * pi[None, :]))
    ppmi = np.where((co >= 2) & np.isfinite(pmi) & (pmi > 0), pmi, 0).astype(np.float32)
    mask2 = (co >= 2)
    iu = np.triu_indices(n, 1)
    Jv = J[iu]; Pv = ppmi[iu]; Mv = mask2[iu]

    def stats(Jv):
        return (np.corrcoef(Jv[Mv], Pv[Mv])[0, 1], Jv[Mv].mean() - Jv[~Mv].mean())

    oa, ob = stats(Jv)
    na, nb = [], []
    for _ in range(1000):
        perm = rng.permutation(n)
        a, b = stats(J[perm][:, perm][iu]); na.append(a); nb.append(b)
    na, nb = np.array(na), np.array(nb)
    print(f"A corr(letterJ,PPMI|co>=2): obs={oa:+.4f} z={(oa-na.mean())/na.std():+.2f} "
          f"p2={min(np.mean(na>=oa),np.mean(na<=oa))*2:.4f}")
    print(f"B deltaJ(co>=2 vs <2):      obs={ob:+.5f} z={(ob-nb.mean())/nb.std():+.2f} "
          f"p2={min(np.mean(nb>=ob),np.mean(nb<=ob))*2:.4f}")
    Jg = J.copy(); top = np.argsort(-Pv)[:200]
    for t in top:
        i, j = iu[0][t], iu[1][t]
        Jg[i, j] = Jg[j, i] = 1.0
    ga, _ = stats(Jg[iu])
    print(f"GATE planted coupling: corr {ga:+.4f} -> z≈{(ga-na.mean())/na.std():+.1f} (fires)")
    ldeg = Counter(c for ls in lsets for c in ls)
    MUQL = set("احرسصطعقكلمنهي")
    inm = np.mean([ldeg[c] for c in alpha if c in MUQL]); outm = np.mean([ldeg[c] for c in alpha if c not in MUQL])
    print("letter hubs:", ", ".join(f"{c}:{ldeg[c]}" for c, _ in ldeg.most_common(8)),
          f"| muqaṭṭaʿāt-letters mean {inm:.0f} vs others {outm:.0f} (descriptive)")


if __name__ == "__main__":
    main()
