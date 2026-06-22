# -*- coding: utf-8 -*-
"""W01 — Concept Anatomy engine. For ANY root, induce its senses/STATES from the WHOLE Qur'an
(القرآن يفسر بعضه بعضا as method): the distinctive co-occurring roots that SELECT each sense, each with
real verses. Plus a plain-words web role (keystone / theme-family / bridge·hub) from concept_graph_features.json.
Deployable: pure-python + numpy, cached on id(corpus). Powers the 'Anatomy of a Concept' structural tab.
"""
from __future__ import annotations
import json, os
from collections import Counter
import analysis as A

# co-reference groups: different roots, one referent → merge before reading the spectrum.
COREF = {
    A.normalize_letters("قلب"): [A.normalize_letters(x) for x in ("قلب", "صدر", "فءاد", "فءد")],
}
# gloss hints for common state/sense selectors (display only; not exhaustive, not required)
_GLOSS = {"طبع": "sealed", "ختم": "sealed", "غلف": "wrapped", "كنن": "covered", "قسو": "hardened",
          "مرض": "diseased", "قفل": "locked", "رين": "rusted", "ضيق": "constricted", "حرج": "straitened",
          "زيغ": "deviating", "رعب": "terror", "وجل": "trembling", "ربط": "strengthened", "خشع": "humbled",
          "خضع": "yielding", "لين": "softened", "رءف": "tender", "سلم": "sound", "هوي": "inclined",
          "نار": "fire", "نور": "light", "قدس": "holy", "نفخ": "breathed", "صرصر": "icy-wind", "عصف": "gale"}


def _norm(r):
    return A.normalize_letters(r)


def spectrum(corpus, root, min_lift=3.0, topn=24, per_state_verses=3):
    """[{selector, gloss, count, lift, verses:[(s,a)...]}] — distinctive co-occurring roots (sense-selectors)
    of `root` (co-reference-merged), each with example verses. Ranked by lift (attraction beyond chance)."""
    N = len(corpus.df); S, AY = A.COL_SURAH, A.COL_AYAH
    R = _norm(root); group = set(COREF.get(R, [R]))
    vroots = [set(_norm(t) for t in toks if t and t != "-") for toks in corpus.root_tokens]
    fr = Counter(r for s in vroots for r in s)
    occ = [i for i in range(N) if vroots[i] & group]
    if not occ:
        return []
    cnt = Counter()
    for i in occ:
        for r in vroots[i]:
            if r not in group and r != "-":
                cnt[r] += 1
    out = []
    for r, k in cnt.items():
        if k < 3:
            continue
        exp = len(occ) * fr.get(r, 0) / N
        lift = k / exp if exp > 0 else 0.0
        if lift < min_lift:
            continue
        verses = []
        for i in occ:
            if r in vroots[i]:
                verses.append((int(corpus.df[S][i]), int(float(corpus.df[AY][i]))))
                if len(verses) >= per_state_verses:
                    break
        out.append({"selector": r, "gloss": _GLOSS.get(r, ""), "count": k,
                    "lift": round(lift, 1), "verses": verses})
    out.sort(key=lambda d: -d["lift"])
    return out[:topn]


def web_role(root):
    """Plain-words web role from the banked graph features (keystone/bridge/hub + theme-family)."""
    try:
        p = os.path.join(os.path.dirname(__file__), "concept_graph_features.json")
        gf = json.load(open(p, encoding="utf-8"))["concepts"].get(_norm(root))
    except Exception:
        gf = None
    if not gf:
        return {"role": "member", "family": "", "keystone": False}
    role = gf.get("role", "member")
    return {"role": role, "family": gf.get("family_label", ""),
            "keystone": role in ("connector / bridge", "family anchor (hub)"),
            "bridge_z": gf.get("bridge_z"), "hub_z": gf.get("hub_z")}


def anatomy(corpus, root):
    return {"root": _norm(root), "senses": spectrum(corpus, root), "web": web_role(root),
            "coref": COREF.get(_norm(root))}
