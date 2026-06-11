# -*- coding: utf-8 -*-
"""
Morpho-syntactic (iltifat) tagger — 7th modality.
Tags grammatical PERSON / NUMBER / TENSE per text-unit from RAW Arabic text,
so the SAME tagger applies to Qur'an (de-diacritized) AND the unsegmented
comparison corpora (ordinary prose / poetry / saj').

Calibrated against the Qur'an's gold morphological segmentation (seg_tokens),
where clitic pronouns and verb-person affixes are split into separate tokens.
"""
import re

# ---- normalizer: strip diacritics + tatweel, fold alef/ya/hamza, fold ك,
#      but KEEP taa-marbuta (ة) distinct from haa (ه) so the 3ms clitic ـه
#      is not confused with the ubiquitous feminine ending ة. ----
_DIA = re.compile(r"[ً-ْٰـۖ-ࣰۭ-ࣿ]")
def norm(t):
    t = _DIA.sub("", str(t))
    t = re.sub(r"[آأإٱ]", "ا", t)
    t = re.sub(r"[ىیﻯ]", "ي", t)
    t = t.replace("ک", "ك").replace("ؤ", "ء").replace("ئ", "ء")
    return t.strip()

STRICT_CLITICS = False   # robustness flag: True drops noisy single-letter ك/ه clitics
WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
def words(s):
    return [w for w in WORD.findall(norm(s)) if w]

# ============================================================
#  RAW-TEXT tagger  (works on any Arabic word list)
# ============================================================
# Independent / clearly person-bearing whole words (high precision)
INDEP = {
    "انا": 1, "نحن": 1, "ايانا": 1, "اننا": 1, "اني": 1, "انني": 1,
    "انت": 2, "انتم": 2, "انتما": 2, "انتن": 2, "انتي": 2,
    "اياك": 2, "اياكم": 2, "ايها": 2, "ايتها": 2,
    "هو": 3, "هي": 3, "هم": 3, "هن": 3, "هما": 3, "اياه": 3, "اياهم": 3,
    "الذي": 3, "الذين": 3, "التي": 3, "اللاتي": 3, "اللذان": 3, "اولئك": 3,
}
# vocative particle => 2nd person addressee
VOC = {"يا"}

# clitic suffixes (checked on word end). Order longest-first.
SUF2 = ("كموها","كموه","كموني","كم","كما","كن","ك")    # 2nd person object/possessive
SUF3 = ("هموها","هما","هم","هن","ها","ه","هما")          # 3rd person
SUF1 = ("نا","ني","نيه")                                   # 1st person (us / me)

# present-tense verb prefixes -> person   (only when word "looks verbal")
PREF = {"ي": 3, "ت": 2, "ن": 1, "ا": 1}   # ا = first-sg أ after alef-fold (noisy; low weight)

# past-tense person suffixes on verbs (suffix conjugation)
PAST2 = ("تم","تما","تن","ت")     # fa3al-ta/-tum...  2nd
PAST1 = ("نا","ت")                # fa3al-naa (1pl) / fa3al-tu (1s) -- ت overlaps 2nd; resolved by context
PAST3 = ("وا","ون","ت","تا","نا") # fa3al-uu (3mp) etc (very noisy)

# multi-letter clitics are high-precision (weight 1.0); single-letter ك/ه are
# common as root letters so they get a low weight (0.4).
MULTI2 = ("كموها","كموه","كموني","كما","كم","كن")
MULTI1 = ("نا","ني","نيه")
MULTI3 = ("هموها","هما","هم","هن","ها")
def _suffix_person(w):
    """Return list of (person, weight) from clitic/agreement suffixes."""
    if len(w) < 4:
        return []
    for s in MULTI2:
        if w.endswith(s) and len(w) - len(s) >= 2:
            return [(2, 1.0)]
    for s in MULTI1:
        if w.endswith(s) and len(w) - len(s) >= 2:
            return [(1, 1.0)]
    for s in MULTI3:
        if w.endswith(s) and len(w) - len(s) >= 2:
            return [(3, 1.0)]
    # single-letter clitics (lower confidence)
    if STRICT_CLITICS:
        return []
    if w.endswith("ك") and len(w) >= 4:
        return [(2, 0.4)]
    if w.endswith("ه") and len(w) >= 4:
        return [(3, 0.4)]
    return []

def tag_person(unit_words):
    """Return (dominant_person in {1,2,3} or 0, score_vector dict)."""
    sc = {1: 0.0, 2: 0.0, 3: 0.0}
    voc_next = False
    for w in unit_words:
        if w in VOC:
            voc_next = True
            continue
        if w in INDEP:
            sc[INDEP[w]] += 3
            voc_next = False
            continue
        if voc_next:
            sc[2] += 3          # the noun after yaa = the one ADDRESSED (2nd)
            voc_next = False
        for p, wt in _suffix_person(w):
            sc[p] += wt
    tot = sum(sc.values())
    if tot == 0:
        return 0, sc
    dom = max(sc, key=lambda k: sc[k])
    return dom, sc

# ---- NUMBER (sing / dual / plur) ----
PLUR_INDEP = {"نحن","هم","هن","انتم","انتن","اولئك","الذين","اللاتي","ايانا"}
DUAL_INDEP = {"هما","انتما","اللذان"}
def tag_number(unit_words):
    sg = du = pl = 0
    for w in unit_words:
        if w in PLUR_INDEP: pl += 2
        elif w in DUAL_INDEP: du += 2
        if len(w) >= 5:
            if w.endswith(("ون","ين","ات")): pl += 1     # sound plural / oblique
            if w.endswith("كم") or w.endswith("هم") or w.endswith("نا"): pl += 1
        if len(w) >= 5 and w.endswith("ان"): du += 1
    if du == 0 and pl == 0:
        return "s"
    return "p" if pl >= du else "d"

# ---- TENSE (past / present / imperative-ish) on a per-unit basis ----
def tag_tense(unit_words):
    pres = past = 0
    for w in unit_words:
        if len(w) < 3:
            continue
        c0 = w[0]
        # present: starts with ي/ت/ن/ا AND not a known particle/noun marker (heuristic)
        if c0 in "يتنا" and not w.startswith("ال") and len(w) >= 3:
            pres += 1
        # past 2nd/1st agreement suffix (strong past signal)
        if w.endswith(("تم","تما","نا","تا")) and len(w) >= 5:
            past += 1
    if pres == 0 and past == 0:
        return "?"
    return "v" if pres >= past else "p"   # v=imperfect(present), p=perfect(past)


# ============================================================
#  GOLD tagger from Qur'an seg_tokens (clitics already split)
# ============================================================
GP1 = {"نا","ني","ي"}                 # but ي/نا as standalone seg tokens => 1st clitic
GP2 = {"ك","كم","كما","كن","تم","ت"}  # 2nd clitic / past-2 suffix tokens
GP3 = {"ه","ها","هم","هن","هما","وا"} # 3rd clitic / past-3
GINDEP = {"انا":1,"نحن":1,"انت":2,"انتم":2,"اياك":2,"هو":3,"هي":3,"هم":3,"هما":3,
          "الذي":3,"الذين":3,"التي":3,"اولئك":3,"اياه":3}
def tag_person_gold(seg_tokens):
    """Dominant person from the clean segmented clitic tokens."""
    sc = {1:0,2:0,3:0}
    for raw in seg_tokens:
        w = norm(raw)
        if w in GINDEP:
            sc[GINDEP[w]] += 3; continue
        if w in GP1: sc[1] += 2
        elif w in GP2: sc[2] += 2
        elif w in GP3: sc[3] += 2
        else:
            # verb prefix on a stem token
            if len(w) >= 3 and w[0] in "نيتا":
                pass  # too noisy at token grain; rely on clitics for gold
    tot = sum(sc.values())
    if tot == 0:
        return 0, sc
    return max(sc, key=lambda k: sc[k]), sc
