"""Close-up · Map — index of deep-dive investigations, placed on the north-star territory."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Map", page_icon="🔎", layout="wide")
if S:
    try:
        S.log_page("closeup_index")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()

st.markdown(
    "<div class='cu-wrap'><div style='font-size:27px;font-weight:800;color:#1D3557'>🔎 Close-up</div>"
    "<div class='cu-lede'><b>What this is.</b> A close-up zooms into one structural question about the "
    "Qur'ān's text, runs it through a battery of instruments, and reports an <b>honest verdict</b> — including "
    "the times a promising signal collapsed under a tougher control. Each card below carries a status badge so "
    "nothing reads as more than it is. Every result is measured against the text's own shuffle, on the bare "
    "consonantal skeleton (rasm).</div></div>", unsafe_allow_html=True)

# ---- north-star spine ----------------------------------------------------
PILLARS = [
    ("📐 ĀYAH — the verse as a unit", [
        ("pages/28_Closeup_Ayah.py", "The Āyah, defined", "DEFINED", 78,
         "Recoverable from the rasm as a connective-opened, grammatically-complete, fāṣila-closed clause-span."),
        (None, "Inter-Āyah order (frozen binomials)", "REDUCES-TO-KNOWN", 65,
         "Fixed conceptual pairs (سماء→أرض, دنيا→آخرة) — real, but the universal frozen-binomial effect."),
    ]),
    ("📜 SŪRA — the chapter as a unit", [
        (None, "The Sūra, defined", "CANDIDATE", "—",
         "Next program — onset register, internal cohesion, closure. Drops into this same frame."),
    ]),
    ("🗺️ ARRANGEMENT — why this order", [
        ("pages/29_Closeup_InterSura.py", "Inter-Sūra coherence (munāsabāt)", "REFUTED-ARTIFACT", 30,
         "Looked like the muṣḥaf groups similar sūras (z up to 9.8) — then collapsed under nonlinear size."),
    ]),
]
for title, items in PILLARS:
    st.markdown(f"<div class='cu-wrap'><div class='cu-sec'>{title}</div></div>", unsafe_allow_html=True)
    for path, name, status, grade, blurb in items:
        col = C.STATUS.get(status, (C.SLATE, ""))[0]
        st.markdown(
            f"<div class='cu-wrap cu-card' style='border-left:5px solid {col}'>"
            f"<span class='cu-badge' style='background:{col};font-size:11px'>{status}</span>"
            f"<span class='cu-grade'>grade {grade}</span>"
            f"<div style='font-size:16px;font-weight:800;color:#1D3557;margin-top:4px'>{name}</div>"
            f"<div style='font-size:13.5px;color:#475569;margin-top:2px'>{blurb}</div></div>",
            unsafe_allow_html=True)
        if path:
            st.page_link(path, label=f"Open · {name}", icon="→")

# ---- journey line --------------------------------------------------------
st.markdown("<div class='cu-wrap'><div class='cu-sec'>The journey so far</div>"
            "<div style='font-size:14px;color:#475569;line-height:1.7'>"
            "ledger cards (scoreboard) → graded ledger (two-tier, provisional) → <b>close-ups (the method &amp; the "
            "story)</b>. The Āyah is <b>defined to necessity</b>; the inter-Sūra arrangement was pushed hard and "
            "<b>honestly refuted</b> as a size artifact; the Sūra is next, in the same frame. Close-ups are living "
            "— a refuted finding can revive if a better instrument arrives.</div></div>", unsafe_allow_html=True)
