"""Close-up module — reusable, self-contained UI components for deep-dive investigations.

Every close-up shares one anatomy so the collection is comparable and honesty is enforced by
structure (a status badge), not by narration. All rendering is inline HTML/CSS via st.markdown so
Arabic renders natively (RTL-isolated) and charts stay crisp without extra chart deps.

Status vocabulary (LOCKED): DEFINED · CANDIDATE · REDUCES-TO-KNOWN · REFUTED-ARTIFACT
"""
import html as _h
import streamlit as st

# ---- palette -------------------------------------------------------------
INK = "#1D3557"
STATUS = {
    "DEFINED":          ("#2A9D8F", "Characterised to necessity"),
    "CANDIDATE":        ("#E9C46A", "Real, gated, still climbing"),
    "REDUCES-TO-KNOWN": ("#457B9D", "Resolves to an existing feature"),
    "REFUTED-ARTIFACT": ("#E76F51", "Killed by a later control"),
}
GREEN, RED, SLATE, AMBER = "#2A9D8F", "#E76F51", "#457B9D", "#E9C46A"


def _esc(s):
    return _h.escape(str(s))


def ar(txt, size=20):
    """Inline Arabic span, bidi-isolated so it never reorders surrounding Latin/numbers."""
    return (f"<span dir='rtl' style='unicode-bidi:isolate;font-family:\"Scheherazade New\",\"Amiri\",serif;"
            f"font-size:{size}px;font-weight:600;color:{INK}'>{_esc(txt)}</span>")


def inject():
    st.markdown("""
    <style>
      .cu-wrap{max-width:1100px}
      .cu-badge{display:inline-block;padding:4px 12px;border-radius:999px;color:#fff;font-weight:800;
                font-size:12px;letter-spacing:.5px;vertical-align:middle}
      .cu-grade{display:inline-block;margin-left:8px;font-weight:800;color:#1D3557;font-size:13px}
      .cu-chip{display:inline-block;padding:3px 10px;border-radius:6px;background:#EEF2F6;color:#33415C;
               font-size:12px;font-weight:700;margin-right:6px;margin-top:4px}
      .cu-q{font-size:18px;font-weight:700;color:#1D3557;margin:6px 0 2px}
      .cu-lede{font-size:15.5px;line-height:1.62;color:#243b53;background:#F7FAFC;border-left:4px solid #2A9D8F;
               padding:13px 16px;border-radius:8px;margin:8px 0 4px}
      .cu-sec{font-size:12px;font-weight:800;letter-spacing:1.4px;color:#5B6B82;text-transform:uppercase;
              border-bottom:2px solid #E2E8F0;padding-bottom:5px;margin:26px 0 12px}
      .cu-row{display:flex;align-items:center;gap:10px;margin:5px 0}
      .cu-lab{flex:0 0 230px;font-size:13.5px;color:#243b53;text-align:right}
      .cu-track{flex:1;background:#EDF1F5;border-radius:6px;height:22px;position:relative;overflow:hidden}
      .cu-fill{height:100%;border-radius:6px}
      .cu-val{flex:0 0 84px;font-size:13px;font-weight:800;font-variant-numeric:tabular-nums}
      .cu-dot{flex:0 0 14px;height:14px;border-radius:50%}
      .cu-card{background:#fff;border:1px solid #E2E8F0;border-radius:12px;padding:16px 18px;margin:6px 0}
      .cu-verd{border-radius:12px;padding:15px 18px;margin:10px 0;color:#243b53;font-size:14.5px;line-height:1.6}
      table.cu-tbl{border-collapse:collapse;width:100%;font-size:13.5px}
      table.cu-tbl td,table.cu-tbl th{border-bottom:1px solid #EDF1F5;padding:7px 10px;text-align:left}
      table.cu-tbl th{color:#5B6B82;font-size:11px;text-transform:uppercase;letter-spacing:.6px}
      .cu-num{font-variant-numeric:tabular-nums;font-weight:800;color:#1D3557}
    </style>""", unsafe_allow_html=True)


def hero(title, question, status, grade, substrate, arrangement, plain):
    col, desc = STATUS.get(status, (SLATE, ""))
    st.markdown(
        f"<div class='cu-wrap'><div style='font-size:26px;font-weight:800;color:{INK}'>{_esc(title)}</div>"
        f"<div style='margin:8px 0 4px'><span class='cu-badge' style='background:{col}'>{_esc(status)}</span>"
        f"<span class='cu-grade'>grade {grade} · {_esc(desc)}</span></div>"
        f"<div class='cu-q'>❝ {_esc(question)} ❞</div>"
        f"<div><span class='cu-chip'>substrate · {_esc(substrate)}</span>"
        f"<span class='cu-chip'>arrangement · {_esc(arrangement)}</span></div>"
        f"<div class='cu-lede'><b>In plain English.</b> {plain}</div></div>",
        unsafe_allow_html=True)


def section(label):
    st.markdown(f"<div class='cu-wrap'><div class='cu-sec'>{_esc(label)}</div></div>", unsafe_allow_html=True)


def cascade(steps, zmax=12.0):
    """Signature visual: gating cascade. steps = [(label, value_str, z, ok_bool), ...]."""
    rows = []
    for label, val, z, ok in steps:
        w = max(4, min(100, abs(z) / zmax * 100))
        col = GREEN if ok else RED
        rows.append(
            f"<div class='cu-row'><div class='cu-lab'>{_esc(label)}</div>"
            f"<div class='cu-track'><div class='cu-fill' style='width:{w:.0f}%;background:{col}'></div></div>"
            f"<div class='cu-val' style='color:{col}'>{_esc(val)}</div>"
            f"<div class='cu-dot' style='background:{col}'></div></div>")
    st.markdown("<div class='cu-wrap cu-card'>" + "".join(rows) + "</div>", unsafe_allow_html=True)


def bars(rows, fmt="{:.2f}", color=INK):
    """Horizontal value bars. rows = [(arabic_or_label, value_0_1, annotation), ...]."""
    out = []
    for lab, v, note in rows:
        w = max(2, min(100, v * 100))
        lab_html = lab if "<span" in lab else _esc(lab)
        out.append(
            f"<div class='cu-row'><div class='cu-lab'>{lab_html}</div>"
            f"<div class='cu-track'><div class='cu-fill' style='width:{w:.0f}%;background:{color}'></div></div>"
            f"<div class='cu-val'>{_esc(fmt.format(v))}</div>"
            f"<div style='flex:0 0 150px;font-size:12px;color:#5B6B82'>{_esc(note)}</div></div>")
    st.markdown("<div class='cu-wrap cu-card'>" + "".join(out) + "</div>", unsafe_allow_html=True)


def scale(lo_label, lo, mid_label, mid, hi_label, hi):
    """A 1-D positional scale: lo (random) … mid (observed) … hi (optimal)."""
    span = hi - lo
    pos = max(0, min(100, (mid - lo) / span * 100)) if span else 50
    st.markdown(
        f"<div class='cu-wrap cu-card'><div style='position:relative;height:54px'>"
        f"<div style='position:absolute;top:24px;left:0;right:0;height:6px;border-radius:6px;"
        f"background:linear-gradient(90deg,#EDF1F5,{AMBER},{GREEN})'></div>"
        f"<div style='position:absolute;top:14px;left:{pos:.0f}%;transform:translateX(-50%);width:3px;height:26px;"
        f"background:{INK}'></div>"
        f"<div style='position:absolute;top:0;left:{pos:.0f}%;transform:translateX(-50%);font-size:12px;"
        f"font-weight:800;color:{INK};white-space:nowrap'>{_esc(mid_label)} {mid:g}</div>"
        f"<div style='position:absolute;top:36px;left:0;font-size:11px;color:#5B6B82'>{_esc(lo_label)} {lo:g}</div>"
        f"<div style='position:absolute;top:36px;right:0;font-size:11px;color:#5B6B82'>{_esc(hi_label)} {hi:g}</div>"
        f"</div></div>", unsafe_allow_html=True)


def table(headers, rows):
    th = "".join(f"<th>{_esc(h)}</th>" for h in headers)
    trs = []
    for r in rows:
        tds = "".join(f"<td>{c if '<span' in str(c) else _esc(c)}</td>" for c in r)
        trs.append(f"<tr>{tds}</tr>")
    st.markdown(f"<div class='cu-wrap'><table class='cu-tbl'><tr>{th}</tr>{''.join(trs)}</table></div>",
                unsafe_allow_html=True)


def verdict(status, text, confidence, flip, revise):
    col = STATUS.get(status, (SLATE, ""))[0]
    st.markdown(
        f"<div class='cu-wrap cu-verd' style='background:{col}14;border:1px solid {col}55'>"
        f"<b style='color:{col}'>VERDICT — {_esc(status)}.</b> {text}<br>"
        f"<b>Confidence</b> {_esc(confidence)} &nbsp;·&nbsp; <b>Flips if</b> {_esc(flip)}<br>"
        f"<b>Revise-up trigger</b> {_esc(revise)}</div>", unsafe_allow_html=True)
