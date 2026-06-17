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

st.set_page_config(page_title="Search", page_icon="🔎", layout="wide")
log_page("search")
corpus = get_corpus()
INK = "#10243A"
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
    roots_norm = {norm(r): r for r in corpus.index_exact}
    root_idf = {r: math.log(N / max(1, len(corpus.index_exact.get(r, [])))) for r in corpus.index_exact}
    anorm = [math.sqrt(sum(root_idf.get(r, 0) ** 2 for r in rootset[i])) for i in range(N)]
    return refs, sname, disp, words, ntext, nwords, rootset, dict(nform2roots), dict(root2forms), roots_norm, root_idf, anorm

refs, sname, disp, words, ntext, nwords, rootset, nform2roots, root2forms, roots_norm, root_idf, anorm = build(id(corpus))
N = len(refs)

_PREF = sorted(["وبال", "فبال", "وكال", "فكال", "وال", "فال", "بال", "كال", "فلل", "ولل", "لل", "ال",
                "و", "ف", "ب", "ك", "ل", "س"], key=len, reverse=True)

def resolve(w):
    """Word -> root(s): try the form directly, else strip Arabic proclitics (ال، و، ف، ب، ك، ل ...)."""
    R = set()
    if w in roots_norm: R.add(roots_norm[w])
    if w in nform2roots: R |= nform2roots[w]
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
        sh = Rq & rootset[i]
        if not sh: continue
        cos = sum(root_idf.get(r, 0) ** 2 for r in sh) / (qn * (anorm[i] or 1.0))
        out.append((cos, i))
    out.sort(reverse=True)
    return out

def search(q):
    q = q.strip()
    m = re.match(r'^\s*(\d{1,3})\s*[:\-،]\s*(\d{1,3})\s*$', q)
    if m:
        s, a = int(m.group(1)), int(m.group(2))
        idx = [i for i, (ss, aa) in enumerate(refs) if ss == s and aa == a]
        return "reference", set(), set(), [("The verse", idx)]
    nq = norm(q); toks = [t for t in nq.split() if t]
    if not toks:
        return "empty", set(), set(), []
    if len(toks) >= 2:
        exact = [i for i, t in enumerate(ntext) if nq in t]
        eset = set(exact)
        hroots = query_roots(toks)                 # the PHRASE's own roots — for highlighting only (small)
        if 1 <= len(exact) <= 3:                    # one specific verse -> its curated roots drive similarity
            Rq = set().union(*[rootset[i] for i in exact])
        else:                                       # common phrase / no exact -> phrase's own roots
            Rq = hroots
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
        kind = "root" if t in roots_norm else "word"
        direct = [i for i in rootay if nq in nwords[i]]      # exact word form, WITHIN root verses
        if direct:
            dset = set(direct)
            other = [i for i in rootay if i not in dset]
            return kind, roots, {nq}, [("Verses with the exact word", direct), ("Other forms of the root", other)]
        return kind, roots, {nq}, [("Verses with this root", rootay)]
    direct = [i for i, tx in enumerate(ntext) if nq in tx]   # no root -> literal text match
    return "text", set(), {nq}, [("Text matches", direct)]

def related_roots(roots, topn=8):
    ay = set()
    for r in roots: ay.update(corpus.index_exact.get(r, []))
    cnt = Counter()
    for i in ay:
        for r in corpus.root_tokens[i]:
            if r not in roots: cnt[r] += 1
    return cnt.most_common(topn)

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

def verse_html(i, target, qwords):
    hl = hl_idx(i, target)
    out = []
    for k, w in enumerate(words[i][:50]):        # cap at first 50 words
        hit = (k in hl) or (qwords and norm(w) in qwords)   # root-aligned OR exact-word match
        out.append(f"<mark style='background:#FCEFB4'>{w}</mark>" if hit else w)
    return (f"<div style='direction:rtl;text-align:right;padding:1px 8px;border-bottom:1px solid #eef2f4;"
            f"font-size:13px;color:#10243A;line-height:1.65;white-space:nowrap;overflow:hidden;text-overflow:ellipsis'>"
            f"<b style='color:#0F6E56'>{refs[i][0]}:{refs[i][1]}</b> "
            f"<span style='color:#10243A'>{sname[i]}</span> &nbsp;{' '.join(out)}</div>")

hero("🔎 Search — anything, any form",
     "A root · a word · a phrase · an āyah · a reference (2:255). Paste a verse to find it AND similar ones.")

if "search_q" not in st.session_state:
    st.session_state.search_q = ""
if st.session_state.get("_pending_q"):
    st.session_state.search_q = st.session_state.pop("_pending_q")
q = st.text_input("Search the Qur'ān", key="search_q",
                  placeholder="مثال: كتب · الرحمن الرحيم · 2:255 · صلاة · أو الصق آية كاملة")
expand = st.checkbox("Concept expansion", value=True, help="For a single root/word, surface related roots (co-roots).")
st.markdown(
    "<style>.stButton button{padding:0 6px !important;min-height:0 !important;height:1.8em !important;"
    "font-size:12px !important;line-height:1.6 !important;border-radius:5px !important;}</style>",
    unsafe_allow_html=True)

if not q.strip():
    st.info("Type or paste anything. A single root expands to all its forms; a word resolves to its root; "
            "a pasted āyah finds the verse PLUS similar and partially-similar verses; diacritics and "
            "Qur'anic marks are ignored.")
    st.stop()

kind, roots, qwords, groups = search(q)
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
    if fcount:
        chips = " &nbsp; ".join(
            f"<span style='background:#eef4f1;border-radius:5px;padding:1px 7px;white-space:nowrap'>"
            f"<b>{f.replace(chr(1740),chr(1610)).replace(chr(1705),chr(1603))}</b> "
            f"<span style='color:#0F6E56'>{n}</span></span>" for f, n in fcount.most_common())
        st.markdown(
            f"<div style='font-size:13px;color:#10243A;margin:2px 0 8px;line-height:2'>"
            f"<b>Forms breakdown</b> ({len(fcount)} forms · {sum(fcount.values())} occurrences): &nbsp; {chips}</div>",
            unsafe_allow_html=True)

ln = 1
for lab, idx in groups:
    if not idx: continue
    layer(ln, f"{lab} ({len(idx)})"); ln += 1
    shown = idx[:300]
    cells = "".join(verse_html(i, roots, qwords) for i in shown)
    grid = f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:0 10px;direction:rtl'>{cells}</div>"
    if len(shown) > 30:                          # scrollable box for large groups
        grid = (f"<div style='max-height:560px;overflow-y:auto;border:1px solid #dbe6e0;"
                f"border-radius:6px;padding:2px 4px'>{grid}</div>")
    st.markdown(grid, unsafe_allow_html=True)
if total == 0:
    st.warning("No matches. Try the bare root, fewer words, or a reference like 2:255.")

if expand and kind in ("root", "word") and roots:
    rel = related_roots(roots, 30)
    if rel:
        layer(ln, "Related concepts / co-roots (click to explore)")
        st.caption("Roots that most co-occur with your query.")
        PC = 12
        for rs in range(0, len(rel), PC):
            cols = st.columns(PC, gap="small")
            for k, (r, n) in enumerate(rel[rs:rs + PC]):
                if cols[k].button(f"{r}·{n}", key=f"rel_{r}", use_container_width=True):
                    st.session_state._pending_q = r
                    st.rerun()
