"""Close-up · Inter-Sūra coherence — REFUTED-ARTIFACT. Dense, real-data charts."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Inter-Sūra", page_icon="🗺️", layout="wide")
if S:
    try:
        S.log_page("closeup_intersura")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()

C.hero("Inter-Sūra coherence (munāsabāt)",
       "Does the muṣḥaf place lexically-similar sūras side by side — by design?",
       "REFUTED-ARTIFACT", 30, "ROOT", "DIVINE-DEFAULT vs DIVINE-ALT · RANDOM null")

C.story(
    "The chapter order looked <b>designed</b> to seat similar sūras together — a strong signal that survived "
    "control after control. Then a tougher size control made it <b>vanish</b>.",
    "It shows the method refusing to fool itself: a compelling result, honestly refuted. That discipline — not "
    "the headline — is the whole point.", accent=C.CORAL)

C.kpis([
    ("11.1", "z · vs random", "Adjacency coherence vs random shuffle of the 114 sūras", C.TEAL),
    ("9.8", "z · period-ctrl", "Survives controlling revelation era", C.TEAL),
    ("5.8", "z · size-linear", "Still alive under a linear size control", C.GOLD),
    ("−0.7", "z · size-nonlin", "Collapses under nonlinear + stratified size", C.CORAL),
    ("0.45", "optimality", "Fraction from random to the lexical optimum", C.INK),
    ("61%", "pairs +", "Adjacencies above expectation (majority, but front-weighted)", C.INK),
    ("30", "grade", "REFUTED-ARTIFACT — recorded, not promoted", C.CORAL),
])

C.foundation(
    "If the chapter order is designed, neighbours should be more alike than chance — and more alike than ordinary "
    "causes (length, era, sheer size) predict. We measure that surplus against the text's own shuffle, then strip "
    "each mundane cause in turn. What survives every control would be design; what dies under one was never design.")

C.section("The gating cascade — survival, then collapse")
C.note("Each point is one control. Green = the signal survived it; red = it died. Height = strength (z) vs that null.")
C.cascade([
    ("vs random", "11.1", 11.1, True), ("length", "3.4", 3.4, True), ("period", "9.8", 9.8, True),
    ("blocks", "8.7", 8.7, True), ("size · linear", "5.8", 5.8, True),
    ("split · 2nd half", "0.0", 0.0, False), ("size · nonlinear", "−0.7", -0.7, False),
], zmax=12.0)

C.section("Two legitimate orders vs the null")
a, b = st.columns(2, gap="small")
with a:
    C.note("Adjacent-sūra lexical coherence (TF-IDF cosine) — higher = more alike")
    C.vbars([("muṣḥaf", 0.202, C.TEAL, "canonical order"),
             ("revelation", 0.190, C.GOLD, "chronological order"),
             ("random", 0.160, C.SLATE, "shuffle null")], ymax=0.24, fmt="{:.3f}")
with b:
    C.note("Length smoothness (mean |Δroots| between neighbours) — lower = smoother")
    C.vbars([("muṣḥaf", 161, C.TEAL, "near length-descending"),
             ("revelation", 352, C.GOLD, "chronological"),
             ("random", 550, C.SLATE, "shuffle null")], ymax=620, fmt="{:.0f}")

C.section("Stripping each cause — the residual shrinks, then dies")
c, d = st.columns(2, gap="small")
with c:
    C.note("What predicts adjacent similarity (regression β) — size dominates")
    C.vbars([("len-prox", -0.010, C.SLATE, "length proximity (after size)"),
             ("period", 0.013, C.GOLD, "revelation-era proximity"),
             ("size-sum", 0.033, C.CORAL, "both chapters' size"),
             ("size-min", 0.070, C.CORAL, "smaller chapter's size")], fmt="{:.3f}")
with d:
    C.note("Coherence residual after each control is removed")
    C.vbars([("+len/period", 0.066, C.TEAL, "beyond length + period"),
             ("+size", 0.027, C.GOLD, "beyond linear size"),
             ("+topic", 0.020, C.GOLD, "beyond topic membership"),
             ("+nonlin", -0.008, C.CORAL, "beyond nonlinear size — gone")], fmt="{:.3f}")

C.section("Robustness — what finally broke it")
e, f = st.columns(2, gap="small")
with e:
    C.note("Held-out split — signal lives only in the long first half")
    C.vbars([("1st half", 2.5, C.GOLD, "sūras 1–57 (long): z 2.5"),
             ("2nd half", 0.0, C.CORAL, "sūras 58–114 (short): z ≈ 0")], ymax=3.5, fmt="{:.1f}")
with f:
    C.note("Topic-control z across topic-model sizes k (pre-size-control)")
    C.vbars([("k5", 5.2, C.SLATE, "5 topics"), ("k8", 5.6, C.SLATE, "8"),
             ("k15", 4.3, C.SLATE, "15"), ("k20", 4.8, C.SLATE, "20"),
             ("k30", 6.2, C.SLATE, "30")], ymax=7, fmt="{:.1f}")

C.section("What it looked like — and the tell")
g, h = st.columns([3, 2], gap="small")
with g:
    C.note("Strongest 'coherent' adjacencies — every one a pair of long front sūras")
    C.table(["Adjacent sūras", "№", "residual"], [
        [C.ar("البقرة — آل عمران"), "2 – 3", "+0.52"],
        [C.ar("آل عمران — النساء"), "3 – 4", "+0.51"],
        [C.ar("النساء — المائدة"), "4 – 5", "+0.47"],
        [C.ar("الأنعام — الأعراف"), "6 – 7", "+0.47"],
    ])
with h:
    C.note("Optimality — near the ceiling, which size later explained")
    C.scale("random", 15.4, "muṣḥaf", 22.8, "optimum", 32.1)

C.verdict("REFUTED-ARTIFACT",
          "The apparent inter-sūra coherence is a <b>chapter-size artifact</b>, not design — recorded honestly, "
          "<b>not</b> written to the discovery ledger. The muṣḥaf is really ordered (by length); no extra "
          "lexical-coherence layer survives proper size control.",
          "~85% size artifact (nonlinear + stratified agree)",
          "a genuinely size-free similarity instrument reviving the residual",
          "such an instrument (≈15% odds) moves this off REFUTED")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
