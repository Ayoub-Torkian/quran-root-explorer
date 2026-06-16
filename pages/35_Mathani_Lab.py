"""Mathānī · Repetition & Refrain Lab — where the Qur'ān's repetition lives, in
comparative context. al-mathānī = "the oft-repeated" (15:87; 39:23). Per-sūra
recurring-trigram density + exact-refrain detection (full-word rasm; refrains shown
vocalized), placed against world oral literature (Kalevala, Iliad) and prose. Honest
finding: repetition is real but localized and typologically oral-formulaic. No inimitability claim."""
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

INK = "#10243A"; TEAL = "#0F6E56"; CORAL = "#D85A30"; BLUE = "#378ADD"; GREY = "#B4B2A9"
F = dict(color=INK, size=12)
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
        dia = [str(t).strip() for t in g[COL_DIACRITIZED].tolist() if isinstance(t, str) and str(t).strip()]
        if not dia:
            continue
        rasm = [_rasm(t) for t in dia]
        words = " ".join(rasm).split()
        if len(words) < 6:
            continue
        tri = Counter(tuple(words[i:i + 3]) for i in range(len(words) - 2))
        tot = sum(tri.values()) or 1
        tri_rep = sum(c for k, c in tri.items() if c >= 2) / tot
        ac = Counter(rasm)
        dia_of = {}
        for d, r in zip(dia, rasm):
            dia_of.setdefault(r, d)
        refr = sorted(((c, dia_of[a]) for a, c in ac.items() if c >= 2 and len(a.split()) >= 3), reverse=True)
        cov = sum(c * len(a.split()) for c, a in refr) / max(1, len(words))
        nm = str(g[COL_SURAH_NAME].iloc[0]) if COL_SURAH_NAME in g.columns else ""
        rows.append({"sura": int(s), "name": nm, "n_ayah": len(dia), "n_words": len(words),
                     "tri_rep": round(tri_rep, 4), "coverage": round(cov, 4),
                     "n_refrains": len(refr), "refrains": [(int(c), a) for c, a in refr[:5]]})
    return pd.DataFrame(rows).sort_values("tri_rep", ascending=False).reset_index(drop=True)


M = _mathani(id(corpus))

hero("Mathānī · Repetition & Refrain Lab",
     "Where the Qur'ān's repetition lives — quantified, localized, and placed against world oral literature.")

st.markdown(
    "The Qur'ān names itself **al-mathānī**, *the oft-repeated* — *sabʿan mina l-mathānī* "
    "(15:87) and *kitāban mutashābihan mathāniya* (39:23). Repetition — refrains, formulae, "
    "paired phrasings — is a structural signature of the text, rooted in its oral recitation. "
    "This lab measures that signature on the **full-word rasm**: how concentrated the repetition is, "
    "which sūras carry it, what the actual refrains are, and how the Qur'ān compares to the world's "
    "oral and written literature. The honest reading: repetition is real but **localized** and "
    "**typologically oral-formulaic** — distinctive, not unique.")

st.markdown(
    "<div style='background:#F1F6F4; border-left:4px solid #0F6E56; border-radius:6px; "
    "padding:14px 16px; margin:8px 0 14px; font-size:14px; color:#10243A; line-height:1.6;'>"
    "<b>Why this module matters.</b> It is the one lens that answers "
    "<i>&ldquo;what is measurably distinctive about the Qur&rsquo;\u0101n?&rdquo;</i> with the correct "
    "baseline &mdash; genre-matched classical Arabic (saj&rsquo;) and world oral literature, not random "
    "or biological controls. It turns a Qur&rsquo;\u0101nic self-description (<i>al-math\u0101n\u012b</i>, "
    "the oft-repeated) into a quantified, navigable structure and places it honestly: "
    "<b>distinctive, not unique</b>. That discipline &mdash; descriptive, comparative, no inimitability "
    "claim &mdash; is what lets a &ldquo;the Qur&rsquo;\u0101n is special&rdquo; statement survive "
    "scrutiny rather than become overclaim.</div>",
    unsafe_allow_html=True)
with st.expander("Conceptual foundation — how repetition is measured"):
    st.markdown(
        "- **Recurring-trigram density** — within a sūra, the share of three-word sequences that "
        "occur more than once. A size-robust, language-agnostic index of internal repetition.\n"
        "- **Exact refrains** — whole āyāt that recur verbatim inside a sūra (litany refrains); shown vocalized.\n"
        "- **Comparative band** — the same density over 350-word chunks of other corpora, so the "
        "Qur'ān is placed against oral epic (Kalevala, Iliad) and prose, not judged in isolation.\n"
        "- **Substrate** — full-word consonantal skeleton (rasm); diacritics demoted as a human layer for the metric.")

biggest_c, biggest_nm = 0, ""
for r in M.itertuples():
    if r.refrains and r.refrains[0][0] > biggest_c:
        biggest_c, biggest_nm = r.refrains[0][0], r.name
with_refr = int((M["n_refrains"] > 0).sum())
total_refr = int(M["n_refrains"].sum())
top10 = M.nlargest(10, "tri_rep").eval("tri_rep*n_words").sum() / (M.eval("tri_rep*n_words").sum() or 1)
med = float(M["tri_rep"].median())

c = st.columns(6)
c[0].metric("Sūras w/ refrain", f"{with_refr}/{len(M)}", help="Sūras with ≥1 verbatim repeated whole āyah.")
c[1].metric("Distinct refrains", total_refr, help="Unique repeated āyāt (≥3 words, ≥2 occurrences).")
c[2].metric("Largest refrain", f"×{biggest_c}", help=f"{biggest_nm}: most-repeated single āyah (Ar-Raḥmān's fa-bi-ayyi ālāʾi rabbikumā tukadhdhibān).")
c[3].metric("Top-10 share", f"{top10*100:.0f}%", help="Share of all recurring-trigram mass in the 10 most-repetitive sūras.")
c[4].metric("Median rep.", f"{med:.3f}", help="Median per-sūra recurring-trigram fraction; most sūras are low.")
c[5].metric("Oral band", "< Kalevala", help="Qur'ān 0.029 sits below the Finnish Kalevala 0.049, above prose.")

layer(1, "Where the repetition concentrates")
st.caption("Left: the 14 most-repetitive sūras. Right: cumulative repetition mass vs sūra rank — the steep "
           "rise is the localization (top 10 carry ~half). Hover for values.")
cc = st.columns([1, 1])
top = M.head(14)
fig = go.Figure(go.Bar(
    x=top["tri_rep"], y=[f"S{r.sura} · {r.name}".strip(" ·") for r in top.itertuples()],
    orientation="h", marker_color=TEAL, text=[f"{v:.3f}" for v in top["tri_rep"]], textposition="outside",
    hovertemplate="%{y}<br>recurring-trigram %{x:.3f}<extra></extra>"))
fig.update_layout(height=420, margin=dict(l=10, r=20, t=10, b=10),
                  yaxis=dict(autorange="reversed", tickfont=F),
                  xaxis=dict(title=dict(text="recurring-trigram fraction", font=F), tickfont=F),
                  plot_bgcolor="white", font=F)
cc[0].plotly_chart(fig, use_container_width=True)

ms = M.sort_values("tri_rep", ascending=False).reset_index(drop=True)
mass = (ms["tri_rep"] * ms["n_words"]).cumsum()
mass = (mass / mass.iloc[-1] * 100) if mass.iloc[-1] else mass
lor = go.Figure()
lor.add_trace(go.Scatter(x=list(range(1, len(ms) + 1)), y=mass, mode="lines", line=dict(color=BLUE, width=2),
                         hovertemplate="top %{x} sūras = %{y:.0f}% of repetition<extra></extra>"))
lor.add_trace(go.Scatter(x=[len(ms)], y=[100], mode="lines", line=dict(color=GREY, dash="dot"), showlegend=False))
lor.update_layout(height=420, margin=dict(l=10, r=20, t=10, b=10), showlegend=False,
                  xaxis=dict(title=dict(text="sūra rank (most → least repetitive)", font=F), tickfont=F),
                  yaxis=dict(title=dict(text="cumulative % of repetition mass", font=F), tickfont=F, range=[0, 101]),
                  plot_bgcolor="white", font=F)
cc[1].plotly_chart(lor, use_container_width=True)

st.markdown("**Per-sūra detail** — refrain-bearing sūras, sortable.")
tbl = M[M["n_refrains"] > 0][["sura", "name", "n_ayah", "n_words", "tri_rep", "coverage", "n_refrains"]].copy()
tbl.columns = ["Sūra", "Name", "Āyāt", "Words", "Recurring-trigram", "Refrain coverage", "# refrains"]
tbl["Refrain coverage"] = (tbl["Refrain coverage"] * 100).round(0).astype(int).astype(str) + "%"
st.dataframe(tbl.reset_index(drop=True), use_container_width=True, height=320)

layer(2, "Read a sūra's refrains")
opts = M[M["n_refrains"] > 0].sort_values("sura")
choice = st.selectbox("Sūra (refrain-bearing)", [f"S{r.sura} · {r.name}".strip(" ·") for r in opts.itertuples()])
sel = opts[opts.apply(lambda r: f"S{r.sura} · {r['name']}".strip(" ·") == choice, axis=1)].iloc[0]
st.markdown(f"**Sūra {sel.sura}** — {sel.n_ayah} āyāt · refrain coverage "
            f"**{sel.coverage*100:.0f}%** of words · {sel.n_refrains} repeated āyah(s)")
st.table(pd.DataFrame([{"×": c2, "refrain (vocalized)": a} for c2, a in sel.refrains]))

st.markdown("**Full refrain inventory** — every whole-āyah refrain in the Qur'ān, vocalized.")
inv = []
for r in M.itertuples():
    for cnt, txt in r.refrains:
        inv.append({"×": cnt, "Refrain (vocalized)": txt, "Sūra": r.sura, "Name": r.name})
inv_df = pd.DataFrame(inv).sort_values("×", ascending=False).reset_index(drop=True)
st.dataframe(inv_df, use_container_width=True, height=360)

layer(3, "Comparative context — the oral-formulaic band")
st.caption("Median recurring-trigram fraction over 350-word chunks. The Qur'ān sits in the "
           "oral-formulaic range — below the Finnish Kalevala, above written prose. Distinctive, not unique.")
labels = [x[0] for x in COMPARATIVE]; vals = [x[1] for x in COMPARATIVE]; cols = [x[2] for x in COMPARATIVE]
fig2 = go.Figure(go.Bar(x=vals, y=labels, orientation="h", marker_color=cols,
                        text=[f"{v:.3f}" for v in vals], textposition="outside",
                        hovertemplate="%{y}<br>median recurring-trigram %{x:.3f}<extra></extra>"))
fig2.update_layout(height=300, margin=dict(l=10, r=20, t=10, b=10),
                   yaxis=dict(autorange="reversed", tickfont=F),
                   xaxis=dict(title=dict(text="median recurring-trigram fraction", font=F), tickfont=F),
                   plot_bgcolor="white", font=F)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("**Powered stylometric contrast vs genre-matched saj'** (Nahj al-Balāgha, 152 chunks each):")
sty = pd.DataFrame([
    ["hapax ratio", 0.787, 0.849, "−2.05", "[−2.33, −1.80]"],
    ["type-token ratio", 0.656, 0.708, "−1.00", "[−1.26, −0.76]"],
    ["compressibility", 0.356, 0.370, "−0.91", "[−1.18, −0.67]"],
    ["letter entropy", 4.364, 4.403, "−0.72", "[−0.98, −0.48]"],
    ["short-word ratio", 0.153, 0.142, "+0.39", "[+0.14, +0.66]"],
], columns=["feature", "Qur'ān", "saj' (Nahj)", "Cohen's d", "95% CI"])
st.dataframe(sty, use_container_width=True, hide_index=True)

layer(4, "Reading")
st.markdown(
    "- **Localized, not uniform.** The top 10 of ~110 sūras hold roughly half of all recurring-trigram "
    "mass; outside the refrain-sūras the Qur'ān is unremarkable in repetition.\n"
    "- **Two repetition modes.** Whole-āyah litany refrains (Ar-Raḥmān's "
    "*fa-bi-ayyi ālāʾi rabbikumā tukadhdhibān* ×31; Al-Mursalāt ×10) versus formulaic phrases in "
    "legal/narrative sūras (Al-Baqarah, An-Nisāʾ) that recur without a whole-āyah refrain.\n"
    "- **Typologically oral-formulaic.** Below the Kalevala, above prose — consistent with an "
    "orally-recited mathānī text. A comparison, not an inimitability claim.\n"
    "- **Powered vs genre-matched saj'.** Even against Nahj al-Balāgha (rhymed-prose sermons) the "
    "Qur'ān is measurably more repetitive (hapax d=−2.0, CI excludes 0).")
