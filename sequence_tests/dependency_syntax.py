"""MODALITY 47 — DEPENDENCY-SYNTAX COMPLEXITY (real embedding depth, not the parser-free proxy of #11).

STATUS: detector STAGED. It is parser-agnostic but needs an Arabic UD parser, which is TOOLING-BLOCKED
in the research sandbox (neural parsers need torch — CUDA wheels too large for the run window, CPU index
proxy-403; UDPipe installs but its model needs a disallowed URL fetch). Run this where a parser is
available — the user's local machine, or any torch-enabled env. See EVIDENCE #47.

WHAT IT MEASURES (the things #11's surface proxy could NOT reach):
  - mean DEPENDENCY DISTANCE  (avg |head_pos - dep_pos|; higher = more non-local linkage)
  - TREE DEPTH                (max & mean root-to-leaf path; the real embedding/hypotaxis signal)
  - LONG-DEP RATE             (share of dependencies spanning > 5 tokens)
  - HEAD-FINAL rate           (head after dependent; word-order regularity)
Each per-unit; then equal-N sample per corpus, g = sd-gap vs same-language comparators, bootstrap P.
GATE: (1) parse a known sentence and verify depth/distance compute; (2) DEGRADATION — word-scrambling a
unit must INCREASE mean dependency distance (real metric moves monotonically). Run before judging the Qur'an.

PARSER BACKENDS (auto-detected, in order):
  1. stanza  (pip install stanza; stanza.download('ar'))    -- preferred, UD-PADT
  2. spacy_udpipe ('ar')                                     -- lighter, no torch
Provide your own by implementing parse_unit(text) -> list[(idx, head_idx)] (1-based; head 0 = root).
"""
import re, os, sys, statistics
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
rng = np.random.default_rng(47)

# ----------------------------------------------------------------- parser backend
_NLP = None
_BACKEND = None
def _init_parser():
    global _NLP, _BACKEND
    if _NLP is not None: return _BACKEND
    try:
        import stanza
        _NLP = stanza.Pipeline('ar', processors='tokenize,pos,lemma,depparse', verbose=False)
        _BACKEND = 'stanza'; return _BACKEND
    except Exception:
        pass
    try:
        import spacy_udpipe
        try: _NLP = spacy_udpipe.load('ar')
        except Exception: spacy_udpipe.download('ar'); _NLP = spacy_udpipe.load('ar')
        _BACKEND = 'udpipe'; return _BACKEND
    except Exception:
        pass
    raise RuntimeError("No Arabic UD parser available. Install stanza (+stanza.download('ar')) "
                       "or spacy_udpipe, then re-run. Detector logic is ready.")

def parse_unit(text):
    """-> list of (token_index_1based, head_index_1based|0). One sentence == one unit."""
    b = _init_parser()
    if b == 'stanza':
        doc = _NLP(text)
        out = []
        for sent in doc.sentences:
            base = len(out)
            for w in sent.words:
                out.append((base + w.id, (base + w.head) if w.head != 0 else 0))
        return out
    else:  # udpipe (spaCy Doc)
        doc = _NLP(text)
        idx = {tok.i: k + 1 for k, tok in enumerate(doc)}
        out = []
        for tok in doc:
            head = 0 if tok.head.i == tok.i else idx[tok.head.i]
            out.append((idx[tok.i], head))
        return out

# ----------------------------------------------------------------- tree metrics
def _depth(edges):
    children = {}; root = None
    for i, h in edges:
        children.setdefault(h, []).append(i)
        if h == 0: root = i
    if root is None: return 0
    best = 0; stack = [(root, 1)]
    while stack:
        node, d = stack.pop(); best = max(best, d)
        for c in children.get(node, []): stack.append((c, d + 1))
    return best

def unit_metrics(edges):
    if len(edges) < 3: return None
    dists = [abs(i - h) for i, h in edges if h != 0]
    if not dists: return None
    return {
        "dep_dist": float(np.mean(dists)),
        "depth":    float(_depth(edges)),
        "long_rate": float(np.mean([d > 5 for d in dists])),
        "head_final": float(np.mean([h > i for i, h in edges if h != 0])),
    }

# ----------------------------------------------------------------- corpora
_DIAC = re.compile(r"[ً-ْٰـ]")  # harakat + dagger-alif + tatweel
def _strip(s):
    return _DIAC.sub("", str(s)).strip()

def load_units():
    # FAIRNESS: parse every corpus in the SAME orthographic condition (diacritics stripped),
    # since comparators are undiacritized and the parser is trained on undiacritized MSA.
    import analysis as A
    from analysis import COL_DIACRITIZED as D
    c = A.load_corpus(os.path.join(ROOT, "Book6.xlsx"))
    q = [_strip(c.df.iloc[i][D]) for i in range(len(c.df)) if len(str(c.df.iloc[i][D]).split()) >= 4]
    SENT = re.compile(r"[.!؟?\n]+")
    def comp(paths):
        txt = "".join("\n" + open(os.path.join(ROOT, 'sequence_tests', 'corpus', p), encoding='utf-8',
                                  errors='ignore').read() for p in paths)
        return [_strip(s) for s in SENT.split(txt) if len(s.split()) >= 4]
    return {
        "QURAN": q,
        "ord-Arabic": comp(["ar_tabari.txt", "ar_classical2.txt", "ar_novel.txt", "ar_news.txt"]),
        "poetry": comp(["ar_poetry.txt"]),
        "saj'": comp(["ar_sajprose.txt", "ar_saj_hariri.txt"]),
    }

def g(a, b):
    a, b = np.asarray(a), np.asarray(b)
    return (a.mean() - b.mean()) / (np.sqrt((a.var() + b.var()) / 2) + 1e-9)
def boot_p(a, b, R=2000):
    a, b = np.asarray(a), np.asarray(b)
    ai = rng.integers(0, len(a), R); bi = rng.integers(0, len(b), R)
    return float(np.mean(a[ai] > b[bi]) + 0.5 * np.mean(a[ai] == b[bi]))

# ----------------------------------------------------------------- gate
def gate():
    print("=== GATE ===")
    test = "الذي خلق السماوات والارض في ستة ايام ثم استوى على العرش"
    e = parse_unit(test); m = unit_metrics(e)
    assert m is not None, "gate: parser returned too few tokens"
    print(f"  parsed {len(e)} tokens; depth={m['depth']:.0f} dep_dist={m['dep_dist']:.2f}  [{_BACKEND}]")
    # degradation: scrambling words should raise mean dependency distance
    import random
    toks = test.split(); random.Random(0).shuffle(toks)
    e2 = parse_unit(" ".join(toks)); m2 = unit_metrics(e2)
    print(f"  scrambled dep_dist={m2['dep_dist']:.2f} (expect >= original {m['dep_dist']:.2f})")

# ----------------------------------------------------------------- main
def main(N_PER_CORPUS=250):
    _init_parser(); print("parser backend:", _BACKEND)
    gate()
    units = load_units()
    print("units:", {k: len(v) for k, v in units.items()})
    N = min(N_PER_CORPUS, *[len(v) for v in units.values()])
    print(f"equal-N per corpus = {N}")
    M = {}
    for name, us in units.items():
        idx = rng.choice(len(us), N, replace=False)
        rows = [unit_metrics(parse_unit(us[i])) for i in idx]
        rows = [r for r in rows if r]
        M[name] = {k: np.array([r[k] for r in rows]) for k in rows[0]}
    for feat in ("dep_dist", "depth", "long_rate", "head_final"):
        print(f"\n-- {feat} --")
        for name in units:
            print(f"   {name:11s} mean={M[name][feat].mean():.3f}")
        for comp in ("ord-Arabic", "poetry", "saj'"):
            print(f"   QURAN vs {comp:11s}: g={g(M['QURAN'][feat], M[comp][feat]):+.2f}sd  "
                  f"P={boot_p(M['QURAN'][feat], M[comp][feat]):.2f}")

if __name__ == "__main__":
    main()
