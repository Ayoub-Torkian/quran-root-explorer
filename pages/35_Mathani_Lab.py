"""Mathānī · Repetition & Refrain Lab — where the Qur'ān's repetition lives, in
comparative context. al-mathānī = "the oft-repeated" (15:87; 39:23). Per-sūra
recurring-trigram density + exact-refrain detection (FULL-WORD rasm), placed against
world oral literature (Kalevala, Iliad) and prose. Honest finding: repetition is real
but localized and typologically oral-formulaic (below the Kalevala). No inimitability claim."""
from __future__ import annotations

from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from analysis import COL_SURAH, COL_AYAH, COL_SURAH_NAME, COL_DIACRITIZED
from state import get_corpus, hero, layer, log_page

st.set_page_config(page_title="Mathānī Lab", page_icon="🔁", layout="wide")
log_page("mathani_lab")
corpus = get_corpus()

INK = "#10243A"; TEAL = "#0F6E56"; CORAL = "#D85A30"; GREY = "#B4B2A9"
HARAKAT = set(chr(c) for c in list(range(0x0610, 0x061B)) + list(range(0x064B, 0x0660))
              + [0x0670, 0x0640] + list(range(0x06D6, 0x06DD)))


def _rasm(s):
    return "".join(c for c in str(s) if c not in HARAKAT).strip()


COMPARATIVE = [
    ("Finnish · Kalevala (oral epic)", 0.049, CORAL),
    ("Qur'ān", 0.029, TEAL),
    ("French · Les Misérables", 0.017, GREY),
    ("English · Moby-Dick", 0.011, GREY),
    ("Greek · Iliad", 0.006, GREY),
    ("German · Kafka", 0.006, GREY),
]


@st.cache_data(show_spinner=False)
def _mathani(_cid):
    df = corpus.df
    rows = []
    for s, g in df.groupby(COL_SURAH):
        ayahs = [_rasm(t) for t in g[COL_DIACRITIZED].tolist() if isinstance(t, str) and str(t).strip()]
        ayahs = [a for a in ayahs if a]
        if not ayahs:
            continue
        words = " ".join(ayahs).split()
        if len(words) < 6:
            continue
        tri = Counter(tuple(words[i:i + 3]) for i in range(len(words) - 2))
        tot = sum(tri.values()) or 1
        tri_rep = sum(c for k, c in tri.items() if c >= 2) / tot
        ac = Counter(ayahs)
        refr = sorted(((c, a) for a, c in ac.items() if c >= 2 and len(a.split()) >= 3), reverse=True)
        cov = sum(c * len(a.split()) for c, a in refr) / max(1, len(words))
        nm = g[COL_SURAH_NAME].iloc[0] if COL_SURAH_NAME in g.columns else ""
        rows.append({"sura": int(s), "name": nm, "n_ayah": len(ayahs), "n_words": len(words),
                     "tri_rep": round(tri_rep, 4), "coverage": round(cov, 4),
                     "n_refrains": len(refr), "refrains": [(int(c), a) for c, a in refr[:5]]})
    return pd.DataFrame(rows).sort_values("tri_rep", ascending=False).reset_index(drop=True)


M = _mathani(id(corpus))

hero("Mathānī · Repetition & Refrain Lab",
     "Where the Qur'ān's repetition lives — quantified, localized, and placed against world oral literature.")

# ── Introduction / conceptual foundation ──────────────────────────────────────
st.markdown(
    "The Qur'ān names itself **al-mathānī**, *the oft-repeated* — *sabʿan mina l-mathānī* "
    "(15:87) and *kitāban mutashābihan mathāniya* (39:23). Repetition — refrains, formulae, "
    "paired phrasings — is a structural signature of the text, rooted in its oral recitation. "
    "This lab measures that signature on the **full-word rasm**: how concentrated the repetition is, "
    "which sūras carry it, what the actual refrains are, and how the Qur'ān compares to the world's "
    "oral and written literature. The honest reading it arrives at: the repetition is real but "
    "**localized** and **typologically oral-formulaic** — distinctive, not unique.")
with st.expander("Conceptual foundation — how repetition is measured"):
    st.markdown(
        "- **Recurring-trigram density** — within a sūra, the share of three-word sequences that "
        "occur more than once. A size-robust, language-agnostic index of internal repetition.\n"
        "- **Exact refrains** — whole āyāt that recur verbatim inside a sūra (litany refrains).\n"
        "- **Comparative band** — the same density over 350-word chunks of other corpora, so the "
        "Qur'ān is placed against oral epic (Kalevala, Iliad) and prose rather than judged in isolation.\n"
        "- **Substrate** — full-word consonantal skeleton (rasm); diacritics stripped, demoted as a human layer.")

# ── Headline metrics (small boxes, hover for detail) ──────────────────────────
biggest_c, biggest_nm = 0, ""
for r in M.itertuples():
    if r.refrains and r.refrains[0][0] > biggest_c:
        biggest_c, biggest_nm = r.refrains[0][0], r.name
with_refr = int((M["n_refrains"] > 0).sum())
total_refr = int(M["n_refrains"].sum())
top10 = M.nlargest(10, "tri_rep").eval("tri_rep*n_words").sum() / (M.eval("tri_rep*n_words").sum() or 1)
med = float(M["tri_rep"].median())

c = st.columns(6)
c[0].metric("Sūras w/ refrain", f"{with_refr}/{len(M)}",
            help="Sūras containing at least one verbatim repeated whole āyah.")
c[1].metric("Distinct refrains", total_refr,
            help="Unique repeated āyāt across the whole Qur'ān (≥3 words, ≥2 occurrences).")
c[2].metric("Largest refrain", f"×{biggest_c}",
            help=f"{biggest_nm}: the most-repeated single āyah (e.g. Ar-Raḥmān's fa-bi-ayyi ālāʾi rabbikumā tukadhdhibān).")
c[3].metric("Top-10 share", f"{top10*100:.0f}%",
            help="Fraction of all recurring-trigram mass held by the 10 most-repetitive sūras (concentration).")
c[4].metric("Median rep.", f"{med:.3f}",
            help="Median per-sūra recurring-trigram fraction — most sūras are low; the refrain-sūras are the tail.")
c[5].metric("Oral band", "below Kalevala",
            help="On the comparative band the Qur'ān (0.029) sits below the Finnish Kalevala (0.049), above prose.")

layer(1, "Where the repetition concentrates")
st.caption("Recurring-trigram density per sūra (full-word rasm). Repetition is localized — a few "
           "refrain-sūras carry most of it; the rest is no more repetitive than ordinary prose. Hover a bar for the value.")
top = M.head(14)
fig = go.Figure(go.Bar(
    x=top["tri_rep"], y=[f"S{r.sura} · {r.name}".strip(" ·") for r in top.itertuples()],
    orientation="h", marker_color=TEAL,
    text=[f"{v:.3f}" for v in top["tri_rep"]], textposition="outside",
    hovertemplate="%{y}<br>recurring-trigram %{x:.3f}<extra></extra>"))
fig.update_layout(height=460, margin=dict(l=10, r=20, t=10, b=10),
                  yaxis=dict(autorange="reversed", tickfont=dict(size=12, color=INK)),
                  xaxis=dict(title=dict(text="recurring-trigram fraction", font=dict(size=12, color=INK)),
                            tickfont=dict(size=12, color=INK)),
                  plot_bgcolor="white", font=dict(color=INK, size=12))
st.plotly_chart(fig, use_container_width=True)

layer(2, "Read a sūra's refrains")
opts = M[M["n_refrains"] > 0].sort_values("sura")
choice = st.selectbox("Sūra (refrain-bearing)",
                      [f"S{r.sura} · {r.name}".strip(" ·") for r in opts.itertuples()])
sel = opts[opts.apply(lambda r: f"S{r.sura} · {r['name']}".strip(" ·") == choice, axis=1)].iloc[0]
st.markdown(f"**Sūra {sel.sura}** — {sel.n_ayah} āyāt · refrain coverage "
            f"**{sel.coverage*100:.0f}%** of words · {sel.n_refrains} repeated āyah(s)")
st.table(pd.DataFrame([{"×": c2, "refrain (rasm)": a} for c2, a in sel.refrains]))

layer(3, "Comparative context — the oral-formulaic band")
st.caption("Median recurring-trigram fraction over 350-word chunks. The Qur'ān sits in the "
           "oral-formulaic range — below the Finnish Kalevala, above written prose. Distinctive, not unique.")
labels = [x[0] for x in COMPARATIVE]; vals = [x[1] for x in COMPARATIVE]; cols = [x[2] for x in COMPARATIVE]
fig2 = go.Figure(go.Bar(x=vals, y=labels, orientation="h", marker_color=cols,
                        text=[f"{v:.3f}" for v in vals], textposition="outside",
                        hovertemplate="%{y}<br>median recurring-trigram %{x:.3f}<extra></extra>"))
fig2.update_layout(height=300, margin=dict(l=10, r=20, t=10, b=10),
                   yaxis=dict(autorange="reversed", tickfont=dict(size=12, color=INK)),
                   xaxis=dict(title=dict(text="median recurring-trigram fraction", font=dict(size=12, color=INK)),
                             tickfont=dict(size=12, color=INK)),
                   plot_bgcolor="white", font=dict(color=INK, size=12))
st.plotly_chart(fig2, use_container_width=True)

layer(4, "Reading")
st.markdown(
    "- **Localized, not uniform.** The top 10 of ~110 sūras hold roughly half of all recurring-trigram "
    "mass; outside the refrain-sūras the Qur'ān is unremarkable in repetition.\n"
    "- **Two repetition modes.** Whole-āyah litany refrains (Ar-Raḥmān's "
    "*fa-bi-ayyi ālāʾi rabbikumā tukadhdhibān* ×31; Al-Mursalāt ×10) versus formulaic phrases in "
    "legal/narrative sūras (Al-Baqarah, An-Nisāʾ) that recur without a whole-āyah refrain.\n"
    "- **Typologically oral-formulaic.** Below the Kalevala, above prose — consistent with an "
    "orally-recited mathānī text. A comparison, not an inimitability claim.\n"
    "- **Powered vs genre-matched saj'** (Nahj al-Balāgha, 152 chunks): the Qur'ān is measurably more "
    "repetitive (hapax d=−2.0, tight CI), even against rhymed-prose sermons.")
