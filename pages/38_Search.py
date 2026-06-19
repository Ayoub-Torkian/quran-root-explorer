"""Search — universal, linguistically-intelligent. Type ANYTHING: a root, a word, a phrase,
an āyah (whole or partial), or a reference (2:255). Normalised to letters only (diacritics +
Qur'anic marks stripped, variants folded), type detected, searched accordingly:
  • single ROOT  → all its forms + related concepts
  • single WORD  → resolves to its root + direct hits
  • PHRASE/ĀYAH  → finds THE verse, then SIMILAR and PARTIALLY-SIMILAR verses
                   (IDF-weighted shared-root similarity; rare shared roots weighted highest)
  • REFERENCE    → jumps to the verse."""
from __future__ import annotations
import re, math
from collections import defaultdict, Counter
import streamlit as st
from analysis import COL_SURAH, COL_AYAH, COL_SURAH_NAME, COL_DIACRITIZED, normalize_letters
from state import get_corpus, hero, layer, log_page
import meaning as _MEAN
import mobile as _MOB

st.set_page_config(page_title="Search", page_icon="🔎", layout="wide")
log_page("search")
_MOB.inject()                       # mobile-first reading CSS + Qur'an webfonts
corpus = get_corpus()
INK = "#10243A"
_MP = ()                            # translation language(s); Off by default, set from the selector each run
_NONLETTER = re.compile(r"[^ء-ي ]")

def norm(s):
    s = normalize_letters(str(s)); s = _NONLETTER.sub(" ", s)
    return re.sub(r"\s+", " ", s).strip()

@st.cache_data(show_spinner=False)
def build(_cid):
    df = corpus.df.reset_index(drop=True)
    N = len(df)
    refs = [(int(df[COL_SURAH][i]), int(df[COL_AYAH][i])) for i in range(N)]
    sname = [str(df[COL_SURAH_NAME][i]) if COL_SURAH_NAME in df.columns else "" for i in range(N)]
    disp = [str(df[COL_DIACRITIZED][i]) for i in range(N)]
    words = [d.split() for d in disp]
    ntext = [norm(d) for d in disp]
    nwords = [set(t.split()) for t in ntext]
    rootset = [set(corpus.root_tokens[i]) for i in range(N)]
    nform2roots = defaultdict(set); root2forms = defaultdict(set)
    for i in range(N):
        for r, sf in zip(corpus.root_tokens[i], corpus.surface_tokens[i]):
            nform2roots[norm(sf)].add(r); root2forms[r].add(sf)
    # full INFLECTED words -> root, via the same alignment the highlighter uses, so a typed
    # word like "يمشون" (stem یمش + ون suffix) or "الارض" resolves to its root (مشی / ءرض)
    # even though only the segmented stem is stored. This is what makes phrase "similar" work.
    def _dd(t):
        o = []
        for ch in t:
            if not o or o[-1] != ch: o.append(ch)
        return "".join(o)
    nword2roots = defaultdict(set)
    for i in range(N):
        dwords = ntext[i].split()
        content = [(_dd(norm(sf)), r) for r, sf in zip(corpus.root_tokens[i], corpus.surface_tokens[i])
                   if r and r != "-" and len(norm(sf)) >= 2]
        di = 0
        for cm, r in content:
            k = di
            while k < len(dwords) and cm not in _dd(dwords[k]): k += 1
            if k < len(dwords):
                nword2roots[dwords[k]].add(r); di = k + 1
    roots_norm = {norm(r): r for r in corpus.index_exact}
    root_idf = {r: math.log(N / max(1, len(corpus.index_exact.get(r, [])))) for r in corpus.index_exact}
    anorm = [math.sqrt(sum(root_idf.get(r, 0) ** 2 for r in rootset[i])) for i in range(N)]
    sura_nuzul = {}
    for i in range(N):
        ssn = int(df[COL_SURAH][i])
        if ssn not in sura_nuzul:
            try: sura_nuzul[ssn] = int(df["ترتیب نزول"][i])
            except Exception: pass
    return refs, sname, disp, words, ntext, nwords, rootset, dict(nform2roots), dict(nword2roots), dict(root2forms), roots_norm, root_idf, anorm, sura_nuzul

refs, sname, disp, words, ntext, nwords, rootset, nform2roots, nword2roots, root2forms, roots_norm, root_idf, anorm, sura_nuzul = build(id(corpus))
N = len(refs)

# Layer-2/3 similarity is CONTENT-root based: drop the most ubiquitous (function/grammatical) roots
# (ءله، کون، قول …) so verses aren't matched on "kāna…" type formulas, only on meaningful shared roots.
DROP_SIM = {r for r, _v in sorted(corpus.index_exact.items(), key=lambda kv: -len(kv[1]))[:12]}
crootset = [rootset[i] - DROP_SIM for i in range(N)]
canorm = [math.sqrt(sum(root_idf.get(r, 0) ** 2 for r in crootset[i])) for i in range(N)]
_STOP = {"اذ", "اذا", "التي", "الذي", "الذين", "الي", "اليه", "اليوم", "ان", "انا", "او", "بل", "به",
         "بين", "ثم", "حتي", "ذلك", "علي", "عليه", "عن", "عند", "في", "فيه", "قد", "كل", "لا", "لكن",
         "لم", "لن", "له", "ما", "من", "منه", "هذا", "هذه", "هم", "هن", "هو", "هي", "و"}  # never highlight function words

_PREF = sorted(["وبال", "فبال", "وكال", "فكال", "وال", "فال", "بال", "كال", "فلل", "ولل", "لل", "ال",
                "و", "ف", "ب", "ك", "ل", "س"], key=len, reverse=True)

def resolve(w):
    """Word -> root(s): try the form directly, else strip Arabic proclitics (ال، و، ف، ب، ك، ل ...)."""
    R = set()
    if w in roots_norm: R.add(roots_norm[w])
    if w in nform2roots: R |= nform2roots[w]
    if w in nword2roots: R |= nword2roots[w]        # full inflected word (e.g. يمشون, الارض)
    if R: return R
    for pre in _PREF:
        if w.startswith(pre) and len(w) - len(pre) >= 2:
            stem = w[len(pre):]
            if stem in nform2roots: R |= nform2roots[stem]
            if stem in roots_norm: R.add(roots_norm[stem])
            if R: return R
    return R

def query_roots(toks):
    R = set()
    for t in toks:
        R |= resolve(t)
    return R

def similar_verses(Rq, exclude):
    """Rank verses by IDF-weighted COSINE of root vectors (query vs verse)."""
    if not Rq: return []
    qn = math.sqrt(sum(root_idf.get(r, 0) ** 2 for r in Rq)) or 1.0
    out = []
    for i in range(N):
        if i in exclude: continue
        sh = Rq & crootset[i]
        if not sh: continue
        cos = sum(root_idf.get(r, 0) ** 2 for r in sh) / (qn * (canorm[i] or 1.0))
        out.append((cos, i))
    out.sort(reverse=True)
    return out

_DIG = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹",
                     "01234567890123456789")
REFPOS = {(ss, aa): i for i, (ss, aa) in enumerate(refs)}

def parse_refs(q):
    """Parse a verse reference / list / range into ordered verse indices, or None.
    Accepts ASCII + Arabic/Persian digits and these forms (comma/؛-separated, mixable):
      2:255 · 2:35-82 (range) · 2:285-2:286 (cross-sura) · 2 (whole sura)."""
    t = q.translate(_DIG).strip()
    if not re.search(r"\d", t) or not re.fullmatch(r"[\d\s:،,؛;\-–—]+", t):
        return None
    out, ok = [], False
    for part in re.split(r"[،,؛;]+", t):
        part = part.strip()
        if not part: continue
        m = re.fullmatch(r"(\d{1,3})\s*:\s*(\d{1,3})\s*[-–—]\s*(\d{1,3})\s*:\s*(\d{1,3})", part)
        if m:                                              # S1:A1 - S2:A2  (cross-sura span)
            i1, i2 = REFPOS.get((int(m[1]), int(m[2]))), REFPOS.get((int(m[3]), int(m[4])))
            if i1 is not None and i2 is not None:
                lo, hi = sorted((i1, i2)); out += list(range(lo, hi + 1)); ok = True
            continue
        m = re.fullmatch(r"(\d{1,3})\s*:\s*(\d{1,3})\s*[-–—]\s*(\d{1,3})", part)
        if m:                                              # S:A1 - A2  (range within sura)
            ssv, a1, a2 = int(m[1]), int(m[2]), int(m[3])
            if a2 < a1: a1, a2 = a2, a1
            out += [REFPOS[(ssv, a)] for a in range(a1, a2 + 1) if (ssv, a) in REFPOS]; ok = True
            continue
        m = re.fullmatch(r"(\d{1,3})\s*:\s*(\d{1,3})", part)
        if m:                                              # S:A
            key = (int(m[1]), int(m[2]))
            if key in REFPOS: out.append(REFPOS[key]); ok = True
            continue
        m = re.fullmatch(r"(\d{1,3})", part)
        if m:                                              # bare sura -> whole sura
            ssv = int(m[1]); whole = [i for i, (x, _a) in enumerate(refs) if x == ssv]
            if whole: out += whole; ok = True
            continue
        return None                                        # any unrecognised piece -> not a reference
    if not ok: return None
    seen = set(); res = []
    for i in out:
        if i not in seen: seen.add(i); res.append(i)
    return res

def search(q, mode="auto"):
    q = q.strip()
    if mode in ("auto", "reference"):
        ref = parse_refs(q)
        if ref is not None:
            label = "The verse" if len(ref) == 1 else f"The verses ({len(ref)})"
            return "reference", set(), set(), [(label, ref)]
        if mode == "reference":
            return "noref", set(), set(), []
    nq = norm(q); toks = [t for t in nq.split() if t]
    if not toks:
        return "empty", set(), set(), []
    if mode == "phrase" or (mode == "auto" and len(toks) >= 2):
        nqs = nq.replace(" ", "")                  # space-INSENSITIVE: robust to word-split/paste typos
        exact = [i for i, t in enumerate(ntext) if nqs in t.replace(" ", "")]
        eset = set(exact)
        hroots = query_roots(toks)                 # the PHRASE's own content roots drive similarity
        Rq = hroots - DROP_SIM                      # similar = verses sharing the TYPED phrase's roots …
        if not Rq and exact:                        # … fall back to the matched verse only if nothing resolved
            Rq = set().union(*[crootset[i] for i in exact])
        sims = similar_verses(Rq, eset)
        maxc = sims[0][0] if sims else 0.0
        sim_thr = max(0.15, 0.55 * maxc)
        par_thr = max(0.10, 0.30 * maxc)
        similar = [i for cos, i in sims if cos >= sim_thr]
        partial = [i for cos, i in sims if par_thr <= cos < sim_thr]
        groups = [("The verse(s)", exact), ("Similar verses", similar), ("Partially similar", partial)]
        return "phrase", hroots, set(toks), groups   # highlight by phrase words + phrase roots only
    # single token — word / root
    t = toks[0]
    roots = resolve(t)
    if roots:                                    # CURATED root index — no substring pollution
        rootay = sorted({i for r in roots for i in corpus.index_exact.get(r, [])})
        kind = mode if mode in ("root", "word") else ("root" if t in roots_norm else "word")
        direct = [i for i in rootay if nq in nwords[i]]      # exact word form, WITHIN root verses
        if direct:
            dset = set(direct)
            other = [i for i in rootay if i not in dset]
            return kind, roots, {nq}, [("Verses with the exact word", direct), ("Other forms of the root", other)]
        return kind, roots, {nq}, [("Verses with this root", rootay)]
    if mode == "root":
        return "noroot", set(), set(), []
    direct = [i for i, tx in enumerate(ntext) if nq in tx]   # no root -> literal text match
    return "text", set(), {nq}, [("Text matches", direct)]

def nuzul_timeline(roots):
    """Small SVG: where the query's occurrences fall along revelation (nuzul) order, early->late.
    nuzul order is a scholarly RECONSTRUCTION (labelled as such); divine-ALT arrangement."""
    rs = set(roots)
    from collections import Counter
    cnt = Counter()
    for i in range(N):
        cnt[refs[i][0]] += sum(1 for r in corpus.root_tokens[i] if r in rs)
    items = sorted((sura_nuzul.get(ssn, 0), ssn, cnt.get(ssn, 0)) for ssn in sura_nuzul)
    counts = [c for _, _, c in items]
    total = sum(counts); mx = max(counts) if counts else 0
    if not total: return ""
    wmean = sum(nz * c for nz, _, c in items) / total
    skew = ("earlier-revealed (Meccan-period)" if wmean < 50
            else "later-revealed (Medinan-leaning)" if wmean > 66 else "spread across the revelation")
    W, H = 700, 42; bw = W / 114.0; bars = ""
    for k, (nz, ssn, c) in enumerate(items):
        h = (c / mx) * (H - 8) if mx else 0
        bars += f"<rect x='{k*bw:.1f}' y='{H-h-2:.1f}' width='{max(1.0,bw-0.6):.1f}' height='{h:.1f}' fill='#0F6E56'/>"
    n_suras = sum(1 for _, _, c in items if c)
    svg = (f"<svg viewBox='0 0 {W} {H}' width='100%' style='max-width:720px;display:block'>"
           f"<line x1='0' y1='{H-2}' x2='{W}' y2='{H-2}' stroke='#dbe6e0' stroke-width='1'/>{bars}</svg>")
    txt = (f"<div style='font-size:12px;color:#10243A;margin:1px 0 3px'><b>Revelation timeline</b> "
           f"(sūra nuzūl order, early→late · reconstructed): in {n_suras} sūras · "
           f"weighted-mean rank {wmean:.0f}/114 → <b>{skew}</b>.</div>")
    return f"<div style='margin:2px 0 8px'>{txt}{svg}</div>"

def collocations(roots, topn=12, cap=1500):
    """Recurring multi-word phrases (mathani) the query root appears in, ranked by frequency.
    Positions found via root alignment (handles clitics like الْحَمْدُ). Order-independent dedup
    drops a phrase contained in a longer phrase of comparable count."""
    rs = set(roots)
    ay = sorted({i for r in roots for i in corpus.index_exact.get(r, [])})[:cap]
    cnt = Counter(); rep = {}
    for i in ay:
        pos = hl_idx(i, rs)
        if not pos: continue
        dw = words[i]; nw = [norm(w) for w in dw]
        for n in (2, 3, 4):
            for k in range(len(nw) - n + 1):
                if not any(k <= q < k + n for q in pos): continue
                key = " ".join(nw[k:k + n]); cnt[key] += 1; rep.setdefault(key, " ".join(dw[k:k + n]))
    cand = {g: cc for g, cc in cnt.items() if cc >= 3}
    keep = []
    for g, cc in cand.items():
        if any((g in h) and (h != g) and (len(h) > len(g)) and (cand[h] >= 0.8 * cc) for h in cand):
            continue
        keep.append((g, cc))
    keep.sort(key=lambda x: -x[1])
    return [(rep[g], cc) for g, cc in keep[:topn]]

def related_roots(roots, topn=30, minco=3):
    """Co-roots ranked by ATTRACTION (co-occurrence beyond chance, z) — not raw count, which is
    dominated by ubiquitous roots. z = (observed - expected) / sd under an independence model."""
    rs = set(roots)
    ay = sorted({i for r in roots for i in corpus.index_exact.get(r, [])})
    nA = len(ay)
    co = Counter()
    for i in ay:
        for r in rootset[i]:
            if r not in rs and r and r != "-": co[r] += 1
    out = []
    for r, cc in co.items():
        if cc < minco: continue
        pr = len(corpus.index_exact.get(r, [])) / N
        mean = nA * pr; sd = math.sqrt(nA * pr * (1 - pr)) or 1.0
        out.append((r, cc, round((cc - mean) / sd, 1)))
    out.sort(key=lambda x: -x[2])
    return out[:topn]

def _dedup(t):
    o = []
    for ch in t:
        if not o or o[-1] != ch: o.append(ch)
    return "".join(o)

def hl_idx(i, target):
    """Indices of display words whose CORPUS root is in `target`. Forward-only two-pointer
    aligning each content lemma (root_tokens↔surface_tokens) to a display word; tolerant of
    proclitics, pronoun enclitics and gemination. Precise: disambiguates homographs that merely
    share letters (e.g. نَنسَخْ root نسخ is NOT highlighted for a نسى search)."""
    if not target: return set()
    content = [(_dedup(norm(sf)), r) for r, sf in zip(corpus.root_tokens[i], corpus.surface_tokens[i])
               if len(norm(sf)) >= 2]
    dn = [_dedup(norm(w)) for w in words[i]]
    res = set(); di = 0
    for cm, r in content:
        j = di
        while j < len(dn) and cm not in dn[j]: j += 1
        if j < len(dn):
            if r in target: res.add(j)
            di = j + 1
    return res

def verse_html(i, target, qwords, substr=False):
    """Collapsed: ref + first 50 words FROM THE START of the āyah (one line). Click to expand the
    full āyah content (native <details>, no reload). Matches are highlighted throughout."""
    hl = hl_idx(i, target)
    W = words[i]
    marked = []
    for k, w in enumerate(W):
        nw = norm(w)
        qhit = any(qw in nw for qw in qwords) if substr else (nw in qwords)
        hit = (k in hl) or (qwords and qhit)
        marked.append(f"<mark style='background:#FCEFB4'>{w}</mark>" if hit else w)
    ref_lbl = (f"<b style='color:#0F6E56'>{refs[i][0]}:{refs[i][1]} {sname[i]}</b>")
    full = " ".join(marked)
    _mean = _MEAN.meaning_block_html(f"{refs[i][0]}:{refs[i][1]}", langs=_MP)  # chosen language(s)
    _ar = (f"<div class='vtext qv-ar' dir='rtl' style='text-align:right;color:#10243A;"
           f"line-height:2.0'>{full}</div>")
    if not _mean:                       # translations Off → nothing to collapse; show āyah only
        return ("<div class='vitem' style='border-bottom:1px solid #eef2f4;padding:8px'>"
                f"<div class='vhead' style='font-size:12.5px;margin-bottom:3px'>{ref_lbl}</div>"
                f"{_ar}</div>")
    # Translation is the <details> BODY, OPEN by default (visible). Tap the āyah (summary)
    # to collapse it. Non-empty body → iOS Safari toggles reliably (the empty-body version
    # was why collapse didn't work before). Āyah text shows full in both states.
    return (
        "<div class='vitem' style='border-bottom:1px solid #eef2f4;padding:8px'>"
        "<details class='vrow' open>"
        f"<summary><div class='vhead' style='font-size:12.5px;margin-bottom:3px'>"
        f"<span class='ex'>⌄</span> {ref_lbl}</div>{_ar}</summary>"
        f"{_mean}"
        "</details>"
        "</div>")

hero("🔎 Search — anything, any form",
     "A root · a word · a phrase · an āyah · a reference or range (2:255 · 2:35-82 · 1:1،112:1). Paste a verse to find it AND similar ones.")

MODES = [("✨ Auto", "auto"), ("🌱 Root", "root"), ("🔤 Word", "word"),
         ("📜 Phrase / āyah", "phrase"), ("🔢 Reference / range", "reference")]
_M = {l: v for l, v in MODES}
# Per-mode examples: plain AND diacritized samples (shows that pasting diacritized web text works)
EX = {"auto": ["كتب", "الرَّحْمَٰنِ الرَّحِيمِ", "2:255"],
      "root": ["حمد", "علم", "صور"],
      "word": ["محمد", "الصواعق", "نِسَاء"],
      "phrase": ["الرحمن الرحيم", "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"],
      "reference": ["2:255", "2:35-82", "1:1،112:1", "114"]}
HELP = {"auto": "Anything — type auto-detected (root · word · phrase · reference).",
        "root": "A triliteral root → all its surface forms across the Qur'ān.",
        "word": "A word → its root, split into exact-word and other-form verses.",
        "phrase": "Paste a phrase or whole āyah → the verse plus similar & partial.",
        "reference": "A verse, range (2:35-82), list (1:1،112:1) or whole sura (114)."}
# Bilingual placeholder inside the box; auto/phrase/word show a DIACRITIZED sample
PH = {"auto": "e.g.  كتب · الرَّحْمَٰنِ الرَّحِيمِ · 2:255   —  root, word, phrase, or reference",
      "root": "e.g.  حمد   —  a triliteral root (bare consonants)",
      "word": "e.g.  محمد  /  نِسَاء   —  a single word, with or without diacritics",
      "phrase": "e.g.  بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ   —  paste a phrase or full āyah",
      "reference": "e.g.  2:255 · 2:35-82 · 114   —  verse, range, list, or whole sura"}

# Hover tooltips over each mode option = its description + examples (replaces the separate chip row)
TIP = {v: (HELP[v] + r"\A" + "e.g.   " + "   ·   ".join(EX[v])) for _, v in MODES}
tip_css = "".join(
    f'div[role=radiogroup] label:nth-of-type({k + 1}):hover::after{{content:"{TIP[v]}"}} '
    for k, (l, v) in enumerate(MODES))
st.markdown(
    "<style>div[role=radiogroup]{gap:2px 18px !important} "
    "div[role=radiogroup] label{margin:0 !important;position:relative} "
    "div[role=radiogroup] label:hover::after{position:absolute;top:135%;left:0;z-index:60;"
    "white-space:pre-line;width:max-content;max-width:380px;background:#10243A;color:#fff;"
    "padding:6px 10px;border-radius:6px;font-size:12px;line-height:1.6;"
    "box-shadow:0 3px 10px rgba(16,36,58,.25)} " + tip_css +
    ".stButton button{padding:2px 8px !important;min-height:1.8em !important;height:auto !important;"
    "font-size:12px !important;line-height:1.55 !important;border-radius:5px !important;}</style>",
    unsafe_allow_html=True)

if "search_q" not in st.session_state: st.session_state.search_q = ""
if "search_mode" not in st.session_state: st.session_state.search_mode = MODES[0][0]
if st.session_state.get("_pending_mode"):
    st.session_state.search_mode = st.session_state.pop("_pending_mode")
if st.session_state.get("_pending_q") is not None:
    st.session_state.search_q = st.session_state.pop("_pending_q")

sel = st.radio("type", [l for l, _ in MODES], horizontal=True,
               key="search_mode", label_visibility="collapsed")
mode = _M[sel]
st.markdown("<div style='font-size:12px;color:#10243A;margin:1px 0 2px'>"
            "Hover a type above for examples. Paste straight from any web page — diacritics, "
            "tatwīl and Qur'anic marks are stripped automatically.</div>", unsafe_allow_html=True)
q = st.text_input(HELP[mode], key="search_q", placeholder=PH[mode], label_visibility="collapsed")
expand = st.checkbox("Concept expansion", value=True,
                     help="For a single root/word, surface related roots (co-roots).") if mode in ("auto", "root", "word") else False

if not q.strip():
    st.stop()

kind, roots, qwords, groups = search(q, mode)
note = ""
if kind in ("noref", "noroot"):                  # input doesn't fit the chosen mode → auto-detect instead
    note = ("That's not a valid reference" if kind == "noref" else "No root matched that input") \
        + " — interpreted automatically instead."
    kind, roots, qwords, groups = search(q, "auto")
if note:
    st.markdown(f"<div style='font-size:12px;color:#10243A;margin:2px 0'>ℹ️ {note}</div>",
                unsafe_allow_html=True)
labels = {"reference": "a verse reference", "root": "a root", "word": "a word", "text": "text", "phrase": "a phrase / āyah"}
forms_list = sorted({f for r in roots for f in root2forms[r]}) if kind in ("root", "word") else []
total = sum(len(idx) for _, idx in groups)
st.markdown(
    f"<div style='background:#F1F6F4;border-left:4px solid #0F6E56;border-radius:6px;padding:10px 14px;"
    f"font-size:14px;color:#10243A;margin:8px 0'>Interpreted as <b>{labels.get(kind, kind)}</b>"
    + (f" → root <b>{' · '.join(sorted(roots))}</b>; appears as: <b>{'، '.join(forms_list[:12])}</b>" if forms_list else "")
    + f". &nbsp; " + " · ".join(f"{lab}: <b>{len(idx)}</b>" for lab, idx in groups if idx) + ".</div>",
    unsafe_allow_html=True)

if kind in ("root", "word") and roots:
    fcount = Counter()
    for r in roots:
        for i in corpus.index_exact.get(r, []):
            for rt, sf in zip(corpus.root_tokens[i], corpus.surface_tokens[i]):
                if rt == r:
                    fcount[sf] += 1
    _rel = related_roots(roots, 30)            # computed ONCE — reused by the co-roots panel below
    _ph = collocations(roots)                  # computed ONCE — reused by the phrases panel below
    _rs = set(roots)
    _vset = sorted({i for r in roots for i in corpus.index_exact.get(r, [])})
    _per = Counter()
    for i in _vset: _per[refs[i][0]] += sum(1 for r in corpus.root_tokens[i] if r in _rs)
    _pit = [(sura_nuzul[s], c) for s, c in _per.items() if s in sura_nuzul]
    _tot = sum(c for _, c in _pit); _wm = (sum(nz * c for nz, c in _pit) / _tot) if _tot else 0
    _skew = "earlier-revealed" if _wm < 50 else ("later-revealed" if _wm > 66 else "spread across revelation")
    _bits = [f"<b>{sum(fcount.values())}</b>× · <b>{len(_vset)}</b> verses · <b>{len(fcount)}</b> forms",
             f"revelation <b>{_skew}</b> ({_wm:.0f}/114)"]
    if _rel: _bits.append(f"pairs with <b>{_rel[0][0]}</b> (z{_rel[0][2]:g})")
    if _ph: _bits.append(f"signature <b>{_ph[0][0]}</b>")
    st.markdown("<div style='background:#F4F9F7;border:1px solid #cfe4dc;border-radius:10px;"
                "padding:8px 14px;margin:6px 0 10px;font-size:13.5px;color:#10243A;line-height:1.75'>"
                "🌱 " + " &nbsp;·&nbsp; ".join(_bits) + "</div>", unsafe_allow_html=True)
    if fcount:
        st.markdown(f"<div style='font-size:13px;color:#10243A;margin:2px 0 2px'>"
                    f"<b>Forms breakdown</b> ({len(fcount)} forms · {sum(fcount.values())} occurrences) "
                    f"— click a form to search it</div>", unsafe_allow_html=True)
        _forms = [(f.replace(chr(1740), chr(1610)).replace(chr(1705), chr(1603)), n)
                  for f, n in fcount.most_common()]
        _PCF = 8
        for _rf in range(0, len(_forms), _PCF):
            _cf = st.columns(_PCF, gap="small")
            for _k, (f, n) in enumerate(_forms[_rf:_rf + _PCF]):
                if _cf[_k].button(f"{f}·{n}", key=f"fm_{_rf}_{_k}", use_container_width=True):
                    st.session_state._pending_q = f
                    st.rerun()

if kind in ("root", "word") and roots:
    _tl = nuzul_timeline(roots)
    if _tl: st.markdown(_tl, unsafe_allow_html=True)
    if _ph:
        st.markdown("<div style='font-size:13px;color:#10243A;margin:4px 0 2px'>"
                    "<b>Recurring phrases (mathānī)</b> — click to search the formula</div>",
                    unsafe_allow_html=True)
        _PCP = 2
        for _rp in range(0, len(_ph), _PCP):
            _cols = st.columns(_PCP, gap="small")
            for _k, (ph, cc) in enumerate(_ph[_rp:_rp + _PCP]):
                if _cols[_k].button(f"{ph}  ×{cc}", key=f"ph_{_rp}_{_k}", use_container_width=True):
                    st.session_state._pending_q = ph
                    st.rerun()

if kind == "phrase":                              # one-glance parallel snapshot (reuses groups+roots, no recompute)
    _ex = groups[0][1] if len(groups) > 0 else []
    _sim = groups[1][1] if len(groups) > 1 else []
    _par = groups[2][1] if len(groups) > 2 else []
    _bits = [f"<b>{len(_ex)}</b> exact · <b>{len(_sim)}</b> similar · <b>{len(_par)}</b> partial"]
    _tp = _sim or _par
    if _tp:
        _j = _tp[0]; _bits.append(f"closest parallel <b>{refs[_j][0]}:{refs[_j][1]}</b> ({sname[_j]})")
    if roots:
        _key = [r for r in sorted(roots, key=lambda r: -root_idf.get(r, 0)) if r not in DROP_SIM][:3]
        _bits.append("shared roots <b>" + " · ".join(_key) + "</b>")
    st.markdown("<div style='background:#F4F9F7;border:1px solid #cfe4dc;border-radius:10px;"
                "padding:8px 14px;margin:6px 0 10px;font-size:13.5px;color:#10243A;line-height:1.75'>"
                "🧩 " + " &nbsp;·&nbsp; ".join(_bits) + "</div>", unsafe_allow_html=True)

if kind == "reference" and groups and groups[0][1]:   # one-glance summary of the selected verse set
    _idxs = groups[0][1]
    _suras = sorted({refs[i][0] for i in _idxs})
    _drop = {r for r, _v in sorted(corpus.index_exact.items(), key=lambda kv: -len(kv[1]))[:10]}
    _cnt = Counter()
    for i in _idxs:
        for r in corpus.root_tokens[i]:
            if r and r != "-" and r not in _drop: _cnt[r] += 1
    _dom = [r for r, _v in _cnt.most_common(8)]
    _lw = max((len(words[i]), i) for i in _idxs)[1]
    _bits = [f"<b>{len(_idxs)}</b> āyāt · <b>{len(_suras)}</b> sūra(s)"]
    if len(_suras) == 1:
        _bits.append(f"<b>Sūra {_suras[0]} {sname[_idxs[0]]}</b> · nuzūl {sura_nuzul.get(_suras[0], '?')}/114")
    _bits.append(f"longest <b>{refs[_lw][0]}:{refs[_lw][1]}</b>")
    if _dom: _bits.append("themes <b>" + " · ".join(_dom) + "</b>")
    st.markdown("<div style='background:#F4F9F7;border:1px solid #cfe4dc;border-radius:10px;"
                "padding:8px 14px;margin:4px 0 10px;font-size:13.5px;color:#10243A;line-height:1.75'>"
                "📖 " + " &nbsp;·&nbsp; ".join(_bits) + "</div>", unsafe_allow_html=True)

# ── isolated, reliable "copy results" button (own component iframe — does NOT touch the verse grid) ──
_copy_idxs = [i for _lab, _idx in groups for i in _idx][:120]
if _copy_idxs:
    import json as _json
    _payload = _json.dumps("\n".join(f"{refs[i][0]}:{refs[i][1]}  {disp[i]}" for i in _copy_idxs))
    _btn = ("<button id='cpb' style='font-size:13px;border:1px solid #cfe4dc;background:#eef4f1;"
            "color:#0F6E56;border-radius:7px;padding:4px 12px;cursor:pointer;font-weight:700;"
            "font-family:sans-serif'>📋 Copy these verses</button>"
            "<script>const T=" + _payload + ";document.getElementById('cpb').onclick=function(){"
            "navigator.clipboard.writeText(T);this.textContent='✓ copied';"
            "setTimeout(function(){document.getElementById('cpb').textContent='📋 Copy these verses'},1200)};</script>")
    st.components.v1.html(_btn, height=40)

# ── translation control (one language / all / off — persists across pages) + reading settings ──
_MP = _MEAN.translation_control(st)
_MOB.settings_controls(st)          # ⚙️ text size (Arabic-first) + line spacing
# ── whole-sūra reader: open the full sūra from the first result, at that āyah ──
_all_shown = [i for _lab, _idx in groups for i in _idx]
if _all_shown:
    import surah_reader as _SR
    _SR.peek(corpus, refs[_all_shown[0]][0], refs[_all_shown[0]][1])
ln = 1
for lab, idx in groups:
    if not idx: continue
    layer(ln, f"{lab} ({len(idx)})"); ln += 1
    shown = idx[:300]
    _htarget = (roots - DROP_SIM) if kind == "phrase" else roots   # zoom highlight on CONTENT roots
    _hq = qwords - _STOP                                            # never highlight function words
    cells = "".join(verse_html(i, _htarget, _hq, kind == "text") for i in shown)
    grid = ("<style>"
            ".vgrid summary{display:block;list-style:none;cursor:pointer}"
            ".vgrid summary::-webkit-details-marker{display:none}"
            ".vgrid summary::marker{content:\"\"}"
            # āyah text stays full whether open or collapsed; only the translation toggles
            ".vgrid details[open]{background:#fbfdfc;border-radius:6px;box-shadow:inset 0 0 0 1px #eef4f1}"
            ".vgrid .ex{color:#0F6E56;font-weight:800;display:inline-block;transition:transform .15s}"
            ".vgrid details:not([open]) .ex{transform:rotate(-90deg)}"   # collapsed → chevron points in
            "</style>"
            "<div class='vgrid' style='display:grid;grid-template-columns:1fr;gap:0;direction:rtl'>"
            f"{cells}</div>")
    grid = (f"<div class='vscroll' style='max-height:560px;overflow-y:auto;border:1px solid #dbe6e0;"
            f"border-radius:6px;padding:2px 4px'>{grid}</div>")   # desktop: boxed; mobile: full-flow (vscroll)
    st.markdown(grid, unsafe_allow_html=True)
if total == 0:
    st.warning("No matches. Try the bare root, fewer words, or a reference like 2:255.")

if expand and kind in ("root", "word") and roots:
    rel = _rel
    if rel:
        layer(ln, "Related concepts / co-roots (click to explore)")
        st.caption("Roots that most distinctively PAIR with your query — attraction beyond chance (z).")
        PC = 12
        for rsx in range(0, len(rel), PC):
            cols = st.columns(PC, gap="small")
            for k, (r, cc, z) in enumerate(rel[rsx:rsx + PC]):
                if cols[k].button(f"{r}·{z:g}", key=f"rel_{r}", use_container_width=True):
                    st.session_state._pending_q = r
                    st.rerun()
