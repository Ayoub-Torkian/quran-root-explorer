"""Close-up · Map — index of deep-dive investigations on the north-star territory (horizontal pillars)."""
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
    "<div style='font-size:24px;font-weight:800;color:#10243A'>🔎 Close-up</div>"
    "<div style='font-size:13px;color:#10243A;line-height:1.5;margin:2px 0 4px'>One structural question per card — "
    "run through a battery of instruments, badged with an <b>honest verdict</b> (including signals that collapsed). "
    "Everything measured against the text's own shuffle, on the bare consonantal skeleton (rasm).</div>",
    unsafe_allow_html=True)

PILLARS = [
    ("📐 ĀYAH", "the verse as a unit", [
        ("pages/28_Closeup_Ayah.py", "The Āyah, defined", "DEFINED", 78,
         "Rebuilt from the rasm: connective-opened, grammatically-complete, fāṣila-closed."),
        (None, "Inter-Āyah order", "REDUCES-TO-KNOWN", 65,
         "Frozen pairs (سماء→أرض, دنيا→آخرة) — real, but the universal binomial effect."),
    ]),
    ("📜 SŪRA", "the chapter as a unit", [
        ("pages/30_Closeup_Sura.py", "The Sūra, characterised", "CANDIDATE", 62,
         "A cohesive, register-bracketed block with soft seams — real, but softer than the āyah."),
    ]),
    ("🗺️ ARRANGEMENT", "why this order", [
        ("pages/29_Closeup_InterSura.py", "Inter-Sūra coherence", "REFUTED-ARTIFACT", 30,
         "Looked designed (z up to 9.8) — collapsed under nonlinear size control."),
    ]),
]

cols = st.columns(3, gap="small")
for (head, sub, items), cm in zip(PILLARS, cols):
    with cm:
        st.markdown(f"<div class='cu-sec'><span class='b'></span><b>{head}</b></div>"
                    f"<div style='font-size:13px;color:#10243A;margin:-2px 0 4px 16px'>{sub}</div>",
                    unsafe_allow_html=True)
        for path, name, status, grade, blurb in items:
            col = C.STATUS.get(status, (C.SLATE, ""))[0]
            st.markdown(
                f"<div class='cu-card' style='border-left:5px solid {col};min-height:128px'>"
                f"<span class='cu-badge' style='background:{col};font-size:12px'>{status}</span>"
                f"<span style='font-weight:800;color:#10243A;font-size:13px;margin-left:7px'>grade {grade}</span>"
                f"<div style='font-size:15.5px;font-weight:800;color:#10243A;margin-top:6px'>{name}</div>"
                f"<div style='font-size:13.5px;color:#10243A;margin-top:4px;line-height:1.5'>{blurb}</div></div>",
                unsafe_allow_html=True)
            if path:
                st.page_link(path, label=f"Open {name}")

st.markdown("<div class='cu-sec'><span class='b'></span><b>🔢 CLAIMS REVIEWED</b></div>"
            "<div style='font-size:13px;color:#10243A;margin:-2px 0 4px 16px'>famous numerical claims, "
            "held to the same gates</div>", unsafe_allow_html=True)
_col = C.STATUS["REFUTED-ARTIFACT"][0]
st.markdown(
    f"<div class='cu-card' style='border-left:5px solid {_col}'>"
    f"<span class='cu-badge' style='background:{_col};font-size:12px'>REFUTED-ARTIFACT</span>"
    f"<span style='font-weight:800;color:#10243A;font-size:13px;margin-left:7px'>grade 22</span>"
    f"<div style='font-size:15.5px;font-weight:800;color:#10243A;margin-top:6px'>Code 19 (Rashad Khalifa), reviewed</div>"
    f"<div style='font-size:13.5px;color:#10243A;margin-top:4px;line-height:1.5'>Across 1,202 natural counts, 19 "
    f"holds no statistical privilege (hit-rate 3.2% ≤ 5.3% chance, not above rival numbers). A multiple-comparisons "
    f"artifact — fair, measured, methodological.</div></div>", unsafe_allow_html=True)
st.page_link("pages/31_Closeup_Code19.py", label="Open Code 19, reviewed")
_c2 = C.STATUS["CANDIDATE"][0]
st.markdown(
    f"<div class='cu-card' style='border-left:5px solid {_c2}'>"
    f"<span class='cu-badge' style='background:{_c2};font-size:12px'>CANDIDATE</span>"
    f"<span style='font-weight:800;color:#10243A;font-size:13px;margin-left:7px'>grade 70</span>"
    f"<div style='font-size:15.5px;font-weight:800;color:#10243A;margin-top:6px'>Qur'ān chronology — dating the "
    f"revelation, reviewed</div>"
    f"<div style='font-size:13.5px;color:#10243A;margin-top:4px;line-height:1.5'>The whole field — tradition, "
    f"Nöldeke, Bazargan, Sadeghi — <b>converges</b>: verse length is a real clock (Meccan 14 → Medinan 30 "
    f"words/āyah, r = 0.66). Bazargan <b>credited</b>; only passage-level dating overreaches (2–74%, within ≈ "
    f"between).</div></div>", unsafe_allow_html=True)
st.page_link("pages/32_Closeup_Nuzul.py", label="Open Qur'ān chronology, reviewed")

st.markdown("<div class='cu-sec'><span class='b'></span><b>The journey</b></div>"
            "<div style='font-size:12.5px;color:#475569;line-height:1.6'>"
            "ledger cards (scoreboard) → graded ledger (provisional) → <b>close-ups (method &amp; story)</b>. "
            "The Āyah is <b>defined to necessity</b>; the inter-Sūra arrangement was pushed hard and <b>honestly "
            "refuted</b> as a size artifact; the Sūra is next. Close-ups are living — a refuted finding can revive "
            "if a better instrument arrives.</div>", unsafe_allow_html=True)
