"""Qur'ān-explains-Qur'ān · Cross-Reference WALK. Pick an āyah, then FOLLOW a parallel to make it the
new focus and see ITS parallels — walking the Qur'ān's self-commentary (القرآن يفسّر بعضه بعضًا).
Ranked by IDF-weighted shared-root similarity (rare shared roots count most). Visited āyāt are excluded
so the walk explores outward (no ping-pong). A computed cross-reference index, not tafsīr."""
from __future__ import annotations
import math
from collections import Counter, defaultdict
import streamlit as st
from analysis import COL_SURAH, COL_AYAH, COL_SURAH_NAME, COL_DIACRITIZED, COL_ROOTS
from state import get_corpus, hero, layer, log_page

st.set_page_config(page_title="Cross-References", page_icon="🪢", layout="wide")
log_page("cross_references")
corpus = get_corpus()
INK = "#10243A"

@st.cache_data(show_spinner=False)
def build(_cid):
    df = corpus.df
    refs, rootsets, disp, sura, name = [], [], [], [], []
    for _, r in df.iterrows():
        rootsets.append(set(str(r[COL_ROOTS]).split()))
        refs.append(f"{int(r[COL_SURAH])}:{int(r[COL_AYAH])}")
        disp.append(str(r[COL_DIACRITIZED]).strip())
        sura.append(int(r[COL_SURAH]))
        name.append(str(r[COL_SURAH_NAME]) if COL_SURAH_NAME in df.columns else "")
    N = len(refs)
    dfreq = Counter(x for rs in rootsets for x in rs)
    idf = {x: math.log(N / dfreq[x]) for x in dfreq}
    norm = [math.sqrt(sum(idf[x] ** 2 for x in rs)) for rs in rootsets]
    inv = defaultdict(list)
    for i, rs in enumerate(rootsets):
        for x in rs:
            inv[x].append(i)
    return refs, rootsets, disp, sura, name, idf, norm, inv, N

refs, rootsets, disp, sura, name, idf, norm, inv, N = build(id(corpus))
ref2i = {r: i for i, r in enumerate(refs)}
sname = {s: nm for s, nm in zip(sura, name)}

def related(qi, k, exclude_same, visited=frozenset()):
    sc = defaultdict(float)
    for x in rootsets[qi]:
        w = idf[x] ** 2
        for j in inv[x]:
            sc[j] += w
    qn = norm[qi] or 1e-9
    out = []
    for j, s in sc.items():
        if j == qi or j in visited or not rootsets[j]:
            continue
        if exclude_same and sura[j] == sura[qi]:
            continue
        out.append((s / (qn * (norm[j] or 1e-9)), j))
    out.sort(reverse=True)
    return out[:k]

hero("🪢 Qur'ān-explains-Qur'ān — the cross-reference walk",
     "Pick an āyah, then FOLLOW a parallel to make it the new focus and see its parallels — walking the "
     "text's own commentary. Rare shared roots weighted highest; visited āyāt drop out so you keep moving.")

cc = st.columns([2, 2, 1, 1])
suras = sorted(set(sura))
with cc[0]:
    s_pick = st.selectbox("Start · Sūra", suras, format_func=lambda s: f"{s} · {sname.get(s,'')}".strip(" ·"))
ay_opts = [refs[i] for i in range(N) if sura[i] == s_pick]
with cc[1]:
    a_pick = st.selectbox("Start · Āyah", ay_opts)
with cc[2]:
    k = st.slider("Show", 3, 20, 8)
with cc[3]:
    excl = st.checkbox("Other sūras only", value=True)

# ── walk state machine ───────────────────────────────────────────────
qi_start = ref2i[a_pick]
if st.session_state.get("xref_start") != qi_start:           # new start chosen -> reset walk
    st.session_state.xref_start = qi_start
    st.session_state.xref_path = [qi_start]
if "xref_act" in st.session_state:
    act, idx = st.session_state.pop("xref_act")
    p = st.session_state.xref_path
    if act == "follow" and idx not in p:
        p.append(idx)
    elif act == "back" and idx in p:
        st.session_state.xref_path = p[:p.index(idx) + 1]
path = st.session_state.get("xref_path", [qi_start])
qi = path[-1]

# breadcrumb (click to walk back)
if len(path) > 1:
    st.markdown("<div style='font-size:12px;color:#10243A;margin-top:4px'><b>Your walk</b> "
                "(click to step back):</div>", unsafe_allow_html=True)
    bcols = st.columns(min(len(path), 10))
    for bi, pj in enumerate(path[:10]):
        mark = " ●" if bi == len(path) - 1 else ""
        if bcols[bi].button(refs[pj] + mark, key=f"bc_{bi}", use_container_width=True):
            st.session_state.xref_act = ("back", pj); st.rerun()

# current focus āyah
st.markdown(
    f"<div dir='rtl' style='background:#F1F6F4;border-right:4px solid #0F6E56;border-radius:6px;"
    f"padding:14px 16px;margin:10px 0;font-size:22px;color:#10243A;line-height:1.9'>"
    f"<span style='font-size:13px;color:#10243A'>{refs[qi]} · {sname.get(sura[qi],'')}</span><br>{disp[qi]}</div>",
    unsafe_allow_html=True)
st.caption("Roots: " + " · ".join(sorted(rootsets[qi])))

layer(1, "Follow a parallel to keep walking")
rel = related(qi, k, excl, frozenset(path))
if not rel:
    st.info("No further parallels (content roots exhausted on this walk). Step back in the breadcrumb.")
for score, j in rel:
    shared = sorted(rootsets[qi] & rootsets[j], key=lambda x: -idf[x])
    col = st.columns([6, 1])
    col[0].markdown(
        f"<div style='border:1px solid #cfe0d9;border-radius:7px;padding:10px 14px;margin:4px 0'>"
        f"<div style='font-size:13px;color:#10243A'><b>{refs[j]}</b> · {sname.get(sura[j],'')} "
        f"&nbsp;|&nbsp; similarity {score*100:.0f}% &nbsp;|&nbsp; shared roots: "
        f"<b>{' · '.join(shared)}</b></div>"
        f"<div dir='rtl' style='font-size:19px;color:#10243A;line-height:1.8;margin-top:4px'>{disp[j]}</div></div>",
        unsafe_allow_html=True)
    if col[1].button("follow →", key=f"fl_{j}", use_container_width=True):
        st.session_state.xref_act = ("follow", j); st.rerun()

st.caption(f"Index: {N} āyāt · {len(idf)} distinct roots · cosine over IDF-weighted root vectors.")
