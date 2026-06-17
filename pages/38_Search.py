"""Search — universal, linguistically-intelligent. Type ANYTHING in any form: a root, a word,
a phrase, an āyah (whole or partial), or a reference (2:255). Input is normalised (diacritics
stripped, letter-variants folded), its type detected, and the Qur'ān searched accordingly:
a ROOT expands to all its surface/morphological forms; a WORD resolves to its root; a PHRASE
is matched in the text; a REFERENCE jumps to the verse. Plus concept expansion (related roots by
co-occurrence) — meaning-aware, not literal-only."""
from __future__ import annotations
import re
from collections import defaultdict, Counter
import streamlit as st
from analysis import COL_SURAH, COL_AYAH, COL_SURAH_NAME, COL_DIACRITIZED, normalize_letters
from state import get_corpus, hero, layer, log_page

st.set_page_config(page_title="Search", page_icon="🔎", layout="wide")
log_page("search")
corpus = get_corpus()
INK = "#10243A"

@st.cache_data(show_spinner=False)
def build(_cid):
    df = corpus.df.reset_index(drop=True)
    refs = [(int(df[COL_SURAH][i]), int(df[COL_AYAH][i])) for i in range(len(df))]
    sname = [str(df[COL_SURAH_NAME][i]) if COL_SURAH_NAME in df.columns else "" for i in range(len(df))]
    disp = [str(df[COL_DIACRITIZED][i]) for i in range(len(df))]
    words = [d.split() for d in disp]
    norm_text = [" ".join(normalize_letters(w) for w in ws) for ws in words]
    nform2roots = defaultdict(set); root2forms = defaultdict(set)
    for i in range(len(corpus.root_tokens)):
        for r, sf in zip(corpus.root_tokens[i], corpus.surface_tokens[i]):
            nform2roots[normalize_letters(sf)].add(r); root2forms[r].add(sf)
    roots_norm = {normalize_letters(r): r for r in corpus.index_exact}
    return refs, sname, disp, words, norm_text, dict(nform2roots), dict(root2forms), roots_norm

refs, sname, disp, words, norm_text, nform2roots, root2forms, roots_norm = build(id(corpus))

def search(q):
    q = q.strip()
    m = re.match(r'^\s*(\d{1,3})\s*[:\-،]\s*(\d{1,3})\s*$', q)
    if m:
        s, a = int(m.group(1)), int(m.group(2))
        return "reference", set(), [i for i, (ss, aa) in enumerate(refs) if ss == s and aa == a], []
    nq = normalize_letters(q); toks = [t for t in nq.split() if t]
    roots = set()
    for t in toks:
        if t in roots_norm: roots.add(roots_norm[t])
        elif t in nform2roots: roots |= nform2roots[t]
    direct = [i for i, nt in enumerate(norm_text) if nq and nq in nt]
    dset = set(direct)
    rootay = set()
    for r in roots:
        rootay.update(corpus.index_exact.get(r, []))
    forms = [i for i in sorted(rootay) if i not in dset]
    kind = "reference" if False else ("root" if roots else "phrase" if len(toks) > 1 else "text")
    return kind, roots, direct, forms

def related_roots(roots, topn=8):
    ay = set()
    for r in roots: ay.update(corpus.index_exact.get(r, []))
    cnt = Counter()
    for i in ay:
        for r in corpus.root_tokens[i]:
            if r not in roots: cnt[r] += 1
    return cnt.most_common(topn)

def highlight(i, nq, roots):
    out = []
    for w in words[i]:
        nw = normalize_letters(w)
        hit = (nq and nq in nw) or (roots and (nform2roots.get(nw, set()) & roots))
        out.append(f"<mark style='background:#FCEFB4;border-radius:3px;padding:0 2px'>{w}</mark>" if hit else w)
    return " ".join(out)

def card(i, nq, roots):
    st.markdown(
        f"<div style='border:1px solid #cfe0d9;border-radius:7px;padding:8px 14px;margin:5px 0'>"
        f"<span style='font-size:12px;color:#10243A'><b>{refs[i][0]}:{refs[i][1]}</b> · {sname[i]}</span>"
        f"<div dir='rtl' style='font-size:20px;color:#10243A;line-height:1.9;margin-top:3px'>{highlight(i,nq,roots)}</div></div>",
        unsafe_allow_html=True)

hero("🔎 Search — anything, any form",
     "A root · a word · a phrase · an āyah · a reference (2:255). With or without diacritics, any spelling.")

if "search_q" not in st.session_state:
    st.session_state.search_q = ""
q = st.text_input("Search the Qur'ān", key="search_q",
                  placeholder="مثال: كتب · الرحمن الرحيم · 2:255 · صلاة · ميثاق")
c = st.columns([1, 1, 2])
maxn = c[0].slider("Max results", 5, 100, 25)
expand = c[1].checkbox("Concept expansion", value=True, help="Also surface related roots (co-occurrence).")

if not q.strip():
    st.info("Type anything above. Roots expand to all their forms; words resolve to their root; "
            "phrases and partial āyāt are matched; diacritics are ignored.")
    st.stop()

kind, roots, direct, forms = search(q)
nq = normalize_letters(q)

# interpretation banner
interp = {"reference": "a verse reference", "root": "a root", "phrase": "a phrase", "text": "a word/text"}[kind]
forms_list = sorted({f for r in roots for f in root2forms[r]})
st.markdown(
    f"<div style='background:#F1F6F4;border-left:4px solid #0F6E56;border-radius:6px;padding:10px 14px;"
    f"font-size:14px;color:#10243A;margin:8px 0'>Interpreted as <b>{interp}</b>"
    + (f" → root(s) <b>{' · '.join(sorted(roots))}</b>; appears as: <b>{'، '.join(forms_list[:12])}</b>"
       if roots else "")
    + f". &nbsp; {len(direct)} direct match(es)"
    + (f", {len(forms)} more via root-forms" if forms else "") + ".</div>", unsafe_allow_html=True)

if direct:
    layer(1, f"Direct matches ({len(direct)})")
    for i in direct[:maxn]:
        card(i, nq, roots)
if forms:
    layer(2, f"Other forms of the root ({len(forms)})")
    st.caption("Verses with the same root in a different surface/morphological form.")
    for i in forms[:maxn]:
        card(i, nq, roots)
if not direct and not forms:
    st.warning("No matches. Try fewer letters, the bare root, or a reference like 2:255.")

if expand and roots:
    rel = related_roots(roots)
    if rel:
        layer(3, "Related concepts (smart expansion)")
        st.caption("Roots that most co-occur with your query — click to explore.")
        cols = st.columns(min(8, len(rel)))
        for k, (r, n) in enumerate(rel):
            if cols[k % len(cols)].button(f"{r} · {n}", key=f"rel_{r}"):
                st.session_state.search_q = r
                st.rerun()
