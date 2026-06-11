"""#68 — WITHIN-OPENING LETTER ORDER vs known keys (rasm only; D9 follow-up to #67's one-directionality).

QUESTION (CROSS_IMPACT D9): is the letter ORDER inside each muqaṭṭaʿāt opening correlated with a known
key — the modern hijāʾī alphabet, the ABJADĪ order (the ancient Semitic letter sequence, prior to the
hijāʾī shape-resorting), or corpus body-frequency rank? ORDERS only — no numerology (no abjad VALUES used).

RESULT: STRONG POSITIVE for the ABJADĪ (ancient-alphabet) order.
  distinct combos (11 multi-letter): concordance 0.889 (40/45 pairs), z=+4.32, p<1e-4;
  SELECTION-CORRECTED over all 6 keys (max-null): p=0.00005;
  per-sūra weighted robustness: 0.925 (74/80 pairs), z=+6.60, p<1e-5.
  hijāʾī ~chance (0.578, z=+0.86); frequency weak (0.644, z=+1.60, sub-2σ).
  Violations (5): كهيعص (ك first, vs ه/ي), طه, طسم (س before م), حمعسق (ع before س).
  NOTE: transition graph is NOT a global DAG — one 3-cycle م→ع→س→م — so no total order can sort all
  openings; abjadī is the best key, strong but not perfect. Explains #67's one-directionality finding:
  pairs never reverse because openings are (mostly) sorted by one ancient key.

GATE: planted abjadī-sorted sequences read 1.000; random key ~0.4–0.5; null = within-sequence shuffle
(multiset & length preserved). Sui generis / Qur'an-internal (randomization-null comparator per #50/#51).
RUN DISCIPLINE: author/run in /tmp via heredoc (mount lag); this host copy is for the user. EVIDENCE #68.
"""
import re, os, sys, itertools
import numpy as np
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import analysis as A
from analysis import COL_DIACRITIZED as D, COL_SURAH as S

rng = np.random.default_rng(68)
HARAKAT = re.compile(r"[ً-ْٰـٕ-ٟ]")


def rasm(t):
    t = HARAKAT.sub("", str(t)); t = re.sub(r"[آأإٱ]", "ا", t); t = re.sub(r"[ىئ]", "ي", t)
    t = re.sub("ة", "ه", t).replace("ؤ", "و")
    return "".join(re.findall(r"[ء-ي]", t))


MUQ_RAW = {2: "الم", 3: "الم", 7: "المص", 10: "الر", 11: "الر", 12: "الر", 13: "المر", 14: "الر",
           15: "الر", 19: "كهيعص", 20: "طه", 26: "طسم", 27: "طس", 28: "طسم", 29: "الم", 30: "الم",
           31: "الم", 32: "الم", 36: "يس", 38: "ص", 40: "حم", 41: "حم", 42: "حمعسق", 43: "حم",
           44: "حم", 45: "حم", 46: "حم", 50: "ق", 68: "ن"}
COMBOS = sorted(set(rasm(v) for v in MUQ_RAW.values()))
SEQS = [list(c) for c in COMBOS if len(c) >= 2]

HIJA = list("ابتثجحخدذرزسشصضطظعغفقكلمنهوي")   # modern (shape-sorted) order
ABJD = list("ابجدهوزحطيكلمنسعفصقرشتثخذضظغ")   # ancient Semitic order (ابجد هوز حطي كلمن سعفص قرشت ...)


def key_rank(order):
    return {l: i for i, l in enumerate(order)}


def concordance(seqs, rank, direction=+1):
    good = tot = 0
    for s in seqs:
        for a, b in itertools.combinations(s, 2):
            if rank[a] == rank[b]:
                continue
            tot += 1
            if direction * (rank[b] - rank[a]) > 0:
                good += 1
    return (good / tot if tot else 0.0), tot


def main():
    print("=" * 78)
    print("#68  WITHIN-OPENING LETTER ORDER vs KEYS (rasm; null = within-seq shuffle)")
    print("=" * 78)
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx")); df = c.df
    sur = np.array([int(df.iloc[i][S]) for i in range(len(df))])
    MUQS = {k: rasm(v) for k, v in MUQ_RAW.items()}
    text = []
    for s in np.unique(sur):
        idx = np.where(sur == s)[0]
        if s in MUQS:
            idx = idx[1:]
        text.append("".join(rasm(df.iloc[i][D]) for i in idx))
    cf = Counter("".join(text))
    letters = sorted(set("".join(COMBOS)))
    FREQ = sorted(letters, key=lambda l: -cf[l])
    print("corpus-frequency order (desc):", "".join(FREQ))

    import networkx as nx
    G = nx.DiGraph()
    for s in SEQS:
        for a, b in zip(s, s[1:]):
            G.add_edge(a, b)
    print("transition graph DAG?", nx.is_directed_acyclic_graph(G),
          "| cycles:", list(nx.simple_cycles(G)))

    KEYS = {"hijai-asc": (key_rank(HIJA), +1), "hijai-desc": (key_rank(HIJA), -1),
            "abjadi-asc": (key_rank(ABJD), +1), "abjadi-desc": (key_rank(ABJD), -1),
            "freq-desc": (key_rank(FREQ), +1), "freq-asc": (key_rank(FREQ), -1)}

    planted = [sorted(s, key=lambda l: key_rank(ABJD)[l]) for s in SEQS]
    g1, _ = concordance(planted, key_rank(ABJD), +1)
    rk = list(letters); rng.shuffle(rk)
    g0, _ = concordance(SEQS, key_rank(rk), +1)
    print(f"GATE  planted-sorted: {g1:.3f} (need 1.0) | random key: {g0:.3f} (~0.5)")

    NS = 20000
    obs = {k: concordance(SEQS, r, d)[0] for k, (r, d) in KEYS.items()}
    nulls = {k: [] for k in KEYS}; maxnull = []
    for _ in range(NS):
        sh = []
        for s in SEQS:
            t = s[:]; rng.shuffle(t); sh.append(t)
        vals = {k: concordance(sh, r, d)[0] for k, (r, d) in KEYS.items()}
        for k in KEYS:
            nulls[k].append(vals[k])
        maxnull.append(max(vals.values()))
    maxnull = np.array(maxnull)
    for k in KEYS:
        nl = np.array(nulls[k]); z = (obs[k] - nl.mean()) / (nl.std() + 1e-12)
        print(f"  {k:12s} obs={obs[k]:.3f}  null={nl.mean():.3f}  z={z:+.2f}  p={np.mean(nl >= obs[k]):.4f}")
    best = max(obs, key=obs.get)
    print(f"SELECTION-CORRECTED: best={best} obs={obs[best]:.3f}  p(max-null>=obs)={np.mean(maxnull >= obs[best]):.5f}")
    r, d = KEYS[best]
    exc = [("".join(s), [(a, b) for a, b in itertools.combinations(s, 2)
                         if r[a] != r[b] and d * (r[b] - r[a]) < 0]) for s in SEQS]
    print("violations under best key:", [(cc, v) for cc, v in exc if v])

    # robustness: per-sūra weighting
    seqs_w = [list(rasm(v)) for v in MUQ_RAW.values() if len(rasm(v)) >= 2]
    ABJ = key_rank(ABJD)
    obs_w, np_w = concordance(seqs_w, ABJ, +1)
    null = []
    for _ in range(NS):
        sh = []
        for s in seqs_w:
            t = s[:]; rng.shuffle(t); sh.append(t)
        null.append(concordance(sh, ABJ, +1)[0])
    null = np.array(null)
    print(f"ROBUSTNESS per-sūra weighted: obs={obs_w:.3f} (pairs={np_w}) "
          f"z={(obs_w - null.mean()) / null.std():+.2f} p={np.mean(null >= obs_w):.5f}")


if __name__ == "__main__":
    main()
