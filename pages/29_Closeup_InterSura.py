"""Close-up · Inter-Sūra coherence — REFUTED-ARTIFACT. The honest 'method catches a false positive' story."""
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

C.hero(
    title="Inter-Sūra coherence (munāsabāt)",
    question="Does the muṣḥaf place lexically-similar sūras next to each other — by design?",
    status="REFUTED-ARTIFACT", grade=30,
    substrate="ROOT (content roots)", arrangement="DIVINE-DEFAULT vs DIVINE-ALT (revelation) · RANDOM = null",
    plain=("This is a close-up that did <b>not</b> end in a discovery — and that's why it's here. The question: "
           "is the canonical order of chapters arranged so neighbouring sūras share vocabulary, beyond the obvious "
           "fact that it runs roughly longest-to-shortest? The signal looked <b>strong</b> and survived control "
           "after control. Then a tougher control — accounting for sheer chapter <i>size</i> properly — made it "
           "<b>vanish</b>. The apparent coherence was long chapters mechanically sharing more words. The method "
           "caught its own false positive; we recorded it as such."))

# ---- plain english -------------------------------------------------------
C.section("Plain English — what happened, step by step")
st.markdown(
    "<div class='cu-wrap'><div style='font-size:15px;line-height:1.7;color:#243b53;background:#fff;"
    "border:1px solid #E2E8F0;border-radius:12px;padding:16px 20px'>"
    "We measured how much neighbouring sūras share distinctive roots, then stripped away every ordinary "
    "explanation one at a time: random chance, similar length, same revelation era, the known letter-families "
    "(الم, حم…). After all of those, a real-looking signal remained. But two final checks broke it: the effect "
    "lived <b>only in the long chapters at the front</b> and was absent in the short second half — and when we "
    "controlled chapter <b>size</b> properly (not just linearly), it collapsed to nothing. Verdict: a "
    "<b>size artifact</b>, not design.</div></div>", unsafe_allow_html=True)

# ---- the signature: gating cascade --------------------------------------
C.section("The gating cascade — survival, then collapse")
st.markdown("<div class='cu-wrap'><div style='font-size:14px;color:#475569;margin-bottom:6px'>"
            "Each bar is one control. Green = the signal survived it; red = it died. Bar length ∝ strength (z) "
            "of the muṣḥaf vs the relevant null.</div></div>", unsafe_allow_html=True)
C.cascade([
    ("vs random shuffle",                "z = 11.1", 11.1, True),
    ("length-matched null",              "z = 3.4",  3.4,  True),
    ("period (revelation) control",      "z = 9.8",  9.8,  True),
    ("muqaṭṭaʿāt blocks removed",        "z = 8.7",  8.7,  True),
    ("absolute size — LINEAR",           "z = 5.8",  5.8,  True),
    ("held-out: 2nd half of muṣḥaf",     "z = 0.0",  0.0,  False),
    ("size — NONLINEAR + stratified",    "z = −0.7", 0.7,  False),
], zmax=12.0)

# ---- the apparent signal (real Arabic data) -----------------------------
C.section("What it looked like — and the tell")
st.markdown("<div class='cu-wrap'><div style='font-size:14px;color:#475569;margin-bottom:6px'>"
            "The strongest 'coherent' adjacencies — every one a pair of <b>long front sūras</b>. That clustering "
            "at the long end was the tell: size, not theme.</div></div>", unsafe_allow_html=True)
C.table(["Adjacent sūras", "№", "Apparent residual"], [
    [C.ar("البقرة – آل عمران"), "2–3", "+0.52"],
    [C.ar("آل عمران – النساء"), "3–4", "+0.51"],
    [C.ar("النساء – المائدة"), "4–5", "+0.47"],
    [C.ar("الأنعام – الأعراف"), "6–7", "+0.47"],
    [C.ar("المائدة – الأنعام"), "5–6", "+0.44"],
])
st.markdown("<div class='cu-wrap'><div style='font-size:14px;color:#475569;margin:14px 0 6px'>"
            "It even looked near-optimal: among orderings that share its length profile, the muṣḥaf sat at the "
            "ceiling of coherence (this is what the size control later explained away).</div></div>",
            unsafe_allow_html=True)
C.scale("random", 15.4, "muṣḥaf", 22.8, "lexical optimum", 32.1)

# ---- why it collapsed ----------------------------------------------------
C.section("Why it collapsed — the size control")
st.markdown(
    "<div class='cu-wrap cu-card'><div style='font-size:14.5px;line-height:1.66;color:#243b53'>"
    "Two long chapters share more distinctive roots <i>mechanically</i> — more text, more overlap — regardless of "
    "any thematic design. A <b>linear</b> size control left a residue (z = 5.8) that looked real. But adding "
    "<b>nonlinear</b> size terms and using a <b>size-stratified null</b> (orderings that match the muṣḥaf's size "
    "profile position-for-position) dropped the effect to <b>z = −0.7</b> — indistinguishable from chance, even "
    "slightly negative. The held-out split had already warned us: the signal sat only on the long first half "
    "(z = 2.5) and was absent in the short second half (z ≈ 0).</div></div>", unsafe_allow_html=True)

C.verdict("REFUTED-ARTIFACT",
          "The apparent inter-sūra coherence is a <b>chapter-size artifact</b>, not an arrangement design. "
          "Recorded honestly; <b>not</b> written to the discovery ledger. The muṣḥaf is really ordered — by "
          "length — but no extra lexical-coherence layer survives proper size control.",
          confidence="~85% size artifact (nonlinear + stratified controls agree)",
          flip="a genuinely size-free similarity instrument reviving the residual",
          revise="such an instrument (≈15% odds) would move this off REFUTED")

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
