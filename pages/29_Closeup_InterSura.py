"""Close-up · Inter-Sūra coherence — REFUTED-ARTIFACT. Story-first, full-width, readable."""
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

C.headline([("9.8", "peak survival z", C.TEAL), ("−0.7", "after size control", C.CORAL),
            ("0.45", "optimality fraction", C.INK), ("30", "grade", C.CORAL)])

C.foundation(
    "If the chapter order is designed, neighbours should be more alike than chance — and more alike than ordinary "
    "causes (length, era, sheer size) predict. We measure that surplus against the text's own shuffle, then strip "
    "each mundane cause in turn. What survives every control would be design; what dies under one was never design.")

C.section("The gating cascade — survival, then collapse")
C.note("Each point is one control. Green = the signal survived it; red = it died. Height = strength (z) vs the relevant null.")
C.cascade([
    ("vs random", "11.1", 11.1, True), ("length", "3.4", 3.4, True), ("period", "9.8", 9.8, True),
    ("blocks", "8.7", 8.7, True), ("size · linear", "5.8", 5.8, True),
    ("split · 2nd half", "0.0", 0.0, False), ("size · nonlinear", "−0.7", -0.7, False),
], zmax=12.0)

C.section("What it looked like — and the tell")
C.note("The strongest 'coherent' adjacencies — every one a pair of long front sūras. That clustering at the long end was the tell: size, not theme.")
C.table(["Adjacent sūras", "№", "residual"], [
    [C.ar("البقرة — آل عمران"), "2 – 3", "+0.52"],
    [C.ar("آل عمران — النساء"), "3 – 4", "+0.51"],
    [C.ar("النساء — المائدة"), "4 – 5", "+0.47"],
    [C.ar("الأنعام — الأعراف"), "6 – 7", "+0.47"],
    [C.ar("المائدة — الأنعام"), "5 – 6", "+0.44"],
])

C.section("It even looked near-optimal")
C.note("Among orderings that share its length profile, the muṣḥaf sat at the ceiling of coherence — which the size control later explained away.")
C.scale("random", 15.4, "muṣḥaf", 22.8, "lexical optimum", 32.1)

C.section("Why it collapsed — the size control")
C.note("Two long chapters share more distinctive roots mechanically — more text, more overlap. A LINEAR size control "
       "left a residue (z 5.8) that looked real. Adding NONLINEAR size terms and a SIZE-STRATIFIED null dropped it "
       "to z −0.7 — chance. The held-out split had already warned us: the signal sat only in the long first half.")

C.verdict("REFUTED-ARTIFACT",
          "The apparent inter-sūra coherence is a <b>chapter-size artifact</b>, not design — recorded honestly, "
          "<b>not</b> written to the discovery ledger. The muṣḥaf is really ordered (by length); no extra "
          "lexical-coherence layer survives proper size control.",
          "~85% size artifact (nonlinear + stratified agree)",
          "a genuinely size-free similarity instrument reviving the residual",
          "such an instrument (≈15% odds) moves this off REFUTED")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
