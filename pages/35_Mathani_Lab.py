"""Mathānī · Repetition & Refrain Lab — where the Qur'ān's repetition lives, in
comparative context.

The Qur'ān calls itself *al-mathānī*, "the oft-repeated" (15:87; 39:23). This page
measures that quantitatively: per-sūra recurring-trigram density and exact-refrain
detection, then places the result against world oral-formulaic literature (Kalevala,
Iliad) and written prose. The honest finding it surfaces: the Qur'ān's repetition is
real but localized (a handful of refrain-sūras carry most of it) and typologically
oral-formulaic — it sits *below* the Finnish Kalevala, not as a statistical outlier.
No inimitability claim; every number is a measurement with a stated comparator.

Computed live from the loaded corpus (rasm column). Comparative band values are a
fixed reference (350-word-chunk median recurring-trigram fraction).
"""
from __future__ import annotations

from collections import Counter

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from analysis import COL_SURAH, COL_AYAH, COL_SURAH_NAME, COL_SEGMENTED
from state import get_corpus, hero, layer, log_page

st.set_page_config(page_title="Mathānī Lab", page_icon="🔁", layout="wide")
log_page("mathani_lab")
corpus = get_corpus()

INK = "#10243A"; TEAL = "#0F6E56"; CORAL = "#D85A30"; BLUE = "#378ADD"
AMBER = "#BA7517"; GREY = "#B4B2A9"

# Fixed reference: 350-word-chunk median recurring-trigram fraction (higher = more
# repetitive). Computed once over each full text; see mathani_dataset.json.
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
        ayahs = [str(t) for t in g[COL_SEGMENTED].tolist() if isinstance(t, str) and t.strip()]
        if not ayahs:
            continue
        words = " ".join(ayahs).split()
        if len(words) < 6:
            continue
        tri = Counter(tuple(words[i:i + 3]) for i in range(len(words) - 2))
        tot = sum(tri.values()) or 1
        tri_rep = sum(c for k, c in tri.items() if c >= 2) / tot
        ac = Counter(ayahs)
        refr = sorted(((c, a) for a, c in ac.items() if c >= 2 and len(a.split()) >= 3),
                      reverse=True)
        cov = sum(c * len(a.split()) for c, a in refr) / max(1, len(words))
        nm = g[COL_SURAH_NAME].iloc[0] if COL_SURAH_NAME in g.columns else ""
        rows.append({"sura": int(s), "name": nm, "n_ayah": len(ayahs), "n_words": len(words),
                     "tri_rep": round(tri_rep, 4), "coverage": round(cov, 4),
                     "n_refrains": len(refr),
                     "refrains": [(int(c), a) for c, a in refr[:5]]})
    return pd.DataFrame(rows).sort_values("tri_rep", ascending=False).reset_index(drop=True)


M = _mathani(id(corpus))

hero("Mathānī · Repetition & Refrain Lab",
     "Where the Qur'ān's repetition lives — quantified, localized, and placed against world oral literature.")

with_refr = int((M["n_refrains"] > 0).sum())
total_refr = int(M["n_refrains"].sum())
top10_share = M.nlargest(10, "tri_rep").eval("tri_rep*n_words").sum() / (M.eval("tri_rep*n_words").sum() or 1)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Sūras carrying a refrain", f"{with_refr} / {len(M)}")
k2.metric("Distinct whole-āyah refrains", total_refr)
k3.metric("Repetition in top-10 sūras", f"{top10_share*100:.0f}%")
k4.metric("Qur'ān vs Kalevala (rep.)", "0.029 vs 0.049")

layer(1, "Where the repetition concentrates")
st.caption("Recurring-trigram density per sūra. Repetition is **localized** — a few "
           "refrain-sūras carry most of it; the rest of the Qur'ān is no more repetitive "
           "than ordinary prose.")
top = M.head(14)
fig = go.Figure(go.Bar(
    x=top["tri_rep"], y=[f"S{r.sura} · {r.name}".strip(" ·") for r in top.itertuples()],
    orientation="h", marker_color=TEAL,
    text=[f"{v:.2f}" for v in top["tri_rep"]], textposition="outside"))
fig.update_layout(height=460, margin=dict(l=10, r=20, t=10, b=10),
                  yaxis=dict(autorange="reversed", tickfont=dict(size=12, color=INK)),
                  xaxis=dict(title="recurring-trigram fraction", tickfont=dict(size=12, color=INK),
                            titlefont=dict(size=12, color=INK)),
                  plot_bgcolor="white", font=dict(color=INK, size=12))
st.plotly_chart(fig, use_container_width=True)

layer(2, "Read a sūra's refrains")
opts = M[M["n_refrains"] > 0].sort_values("sura")
choice = st.selectbox("Sūra (refrain-bearing)",
                      [f"S{r.sura} · {r.name}".strip(" ·") for r in opts.itertuples()])
sel = opts[opts.apply(lambda r: f"S{r.sura} · {r['name']}".strip(" ·") == choice, axis=1)].iloc[0]
st.markdown(f"**Sūra {sel.sura}** — {sel.n_ayah} āyāt · refrain coverage "
            f"**{sel.coverage*100:.0f}%** of words · {sel.n_refrains} repeated āyah(s)")
rt = pd.DataFrame([{"×": c, "refrain (rasm)": a} for c, a in sel.refrains])
st.table(rt)

layer(3, "Comparative context — the oral-formulaic band")
st.caption("Median recurring-trigram fraction over 350-word chunks. The Qur'ān sits in "
           "the **oral-formulaic range — below the Finnish Kalevala**, above written prose. "
           "Its refrain structure is the same measurable phenomenon found across oral epic; "
           "it is distinctive, not unique.")
labels = [c[0] for c in COMPARATIVE]; vals = [c[1] for c in COMPARATIVE]; cols = [c[2] for c in COMPARATIVE]
fig2 = go.Figure(go.Bar(x=vals, y=labels, orientation="h", marker_color=cols,
                        text=[f"{v:.3f}" for v in vals], textposition="outside"))
fig2.update_layout(height=300, margin=dict(l=10, r=20, t=10, b=10),
                   yaxis=dict(autorange="reversed", tickfont=dict(size=12, color=INK)),
                   xaxis=dict(title="median recurring-trigram fraction", tickfont=dict(size=12, color=INK),
                             titlefont=dict(size=12, color=INK)),
                   plot_bgcolor="white", font=dict(color=INK, size=12))
st.plotly_chart(fig2, use_container_width=True)

layer(4, "Reading")
st.markdown(
    "- **Localized, not uniform.** The top 10 of ~110 sūras hold roughly half of all "
    "recurring-trigram mass; outside the refrain-sūras the Qur'ān is unremarkable in repetition.\n"
    "- **Two repetition modes.** Whole-āyah *litany refrains* (Ar-Raḥmān's "
    "*fa-bi-ayyi ālāʾi rabbikumā tukadhdhibān* ×31; Al-Mursalāt ×10) versus *formulaic phrases* "
    "in legal/narrative sūras (Al-Baqarah, An-Nisāʾ) that recur without a whole-āyah refrain.\n"
    "- **Typologically oral-formulaic.** The magnitude places the Qur'ān in the band of the "
    "world's oral epics — below the Kalevala, above prose — consistent with an orally-recited, "
    "*mathānī* text. This is a comparison, not an inimitability claim.")
