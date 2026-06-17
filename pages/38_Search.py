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

def query_roots(toks):
    R = set()
    for t in toks:
        R |= nform2roots.get(t, set())
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
        if exact:                                  # use the found verse's CURATED roots
            Rq = set().union(*[rootset[i] for i in exact])
        else:
            Rq = query_roots(toks)
        sims = similar_verses(Rq, eset)
        maxc = sims[0][0] if sims else 0.0
        sim_thr = max(0.15, 0.55 * maxc)           # adaptive to each query's scale
        par_thr = max(0.10, 0.30 * maxc)
        similar = [i for cos, i in sims if cos >= sim_thr]
        partial = [i for cos, i in sims if par_thr <= cos < sim_thr]
        groups = [("The verse(s)", exact), ("Similar verses", similar), ("Partially similar", partial)]
        return "phrase", Rq, set(toks), groups
    # single token
    t = toks[0]; roots = set()
    if t in roots_norm: roots.add(roots_norm[t])
    elif t in nform2roots: roots |= nform2roots[t]
    direct = [i for i, tx in enumerate(ntext) if nq in tx]
    dset = set(direct)
    forms = sorted({i for r in roots for i in corpus.index_exact.get(r, [])} - dset)
    return ("root" if roots else "text"), roots, {nq}, [("Direct matches", direct), ("Other forms of the root", forms)]

def related_roots(roots, topn=8):
    ay = set()
    for r in roots: ay.update(corpus.index_exact.get(r, []))
    cnt = Counter()
    for i in ay:
        for r in corpus.root_tokens[i]:
            if r not in roots: cnt[r] += 1
    return cnt.most_common(topn)

def card(i, qwords, roots):
    out = []
    for w in words[i]:
        nw = norm(w)
        hit = (nw and nw in qwords) or (roots and (nform2roots.get(nw, set()) & roots))
        out.append(f"<mark style='background:#FCEFB4;border-radius:3px;padding:0 2px'>{w}</mark>" if hit else w)
    st.markdown(
        f"<div dir='rtl' style='padding:2px 10px;border-bottom:1px solid #eef2f4;font-size:18px;"
        f"color:#10243A;line-height:1.6'>"
        f"<span style='font-size:12px;font-weight:700;color:#0F6E56'>{refs[i][0]}:{refs[i][1]}</span>"
        f"<span style='font-size:12px;color:#10243A'> · {sname[i]}</span>&nbsp; {' '.join(out)}</div>",
        unsafe_allow_html=True)

hero("🔎 Search — anything, any form",
     "A root · a word · a phrase · an āyah · a reference (2:255). Paste a verse to find it AND similar ones.")

if "search_q" not in st.session_state:
    st.session_state.search_q = ""
q = st.text_input("Search the Qur'ān", key="search_q",
                  placeholder="مثال: كتب · الرحمن الرحيم · 2:255 · صلاة · أو الصق آية كاملة")
c = st.columns([1, 1, 2])
maxn = c[0].slider("Max results per group", 10, 100, 30)
expand = c[1].checkbox("Concept expansion", value=True, help="For a single root, surface related roots.")

if not q.strip():
    st.info("Type or paste anything. A single root expands to all its forms; a word resolves to its root; "
            "a pasted āyah finds the verse PLUS similar and partially-similar verses; diacritics and "
            "Qur'anic marks are ignored.")
    st.stop()

kind, roots, qwords, groups = search(q)
labels = {"reference": "a verse reference", "root": "a root", "text": "a word", "phrase": "a phrase / āyah"}
forms_list = sorted({f for r in roots for f in root2forms[r]}) if kind in ("root", "text") else []
total = sum(len(idx) for _, idx in groups)
st.markdown(
    f"<div style='background:#F1F6F4;border-left:4px solid #0F6E56;border-radius:6px;padding:10px 14px;"
    f"font-size:14px;color:#10243A;margin:8px 0'>Interpreted as <b>{labels.get(kind, kind)}</b>"
    + (f" → root <b>{' · '.join(sorted(roots))}</b>; appears as: <b>{'، '.join(forms_list[:12])}</b>" if forms_list else "")
    + (f" → {len(roots)} content roots" if kind == "phrase" else "")
    + f". &nbsp; " + " · ".join(f"{lab}: <b>{len(idx)}</b>" for lab, idx in groups if idx) + ".</div>",
    unsafe_allow_html=True)

ln = 1
for lab, idx in groups:
    if not idx: continue
    layer(ln, f"{lab} ({len(idx)})"); ln += 1
    for i in idx[:maxn]:
        card(i, qwords, roots)
if total == 0:
    st.warning("No matches. Try the bare root, fewer words, or a reference like 2:255.")

if expand and kind == "root" and roots:
    rel = related_roots(roots)
    if rel:
        layer(ln, "Related concepts (smart expansion)")
        st.caption("Roots that most co-occur with your query — click to explore.")
        cols = st.columns(min(8, len(rel)))
        for k, (r, n) in enumerate(rel):
            if cols[k % len(cols)].button(f"{r} · {n}", key=f"rel_{r}"):
                st.session_state.search_q = r
                st.rerun()
