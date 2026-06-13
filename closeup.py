"""Close-up module — compact, readable, graphically-rich components for deep-dive investigations. (v2)

Hand-built inline SVG/HTML so Arabic renders natively and visuals stay crisp with no chart dependency.
Charts use a ~1000px viewBox to render near 1:1 inside the page column, so fonts never go minute.

Public API: ar · inject · hero · story · headline · foundation · section · note · cascade · bars · scale
            · table · verdict.  Status (LOCKED): DEFINED · CANDIDATE · REDUCES-TO-KNOWN · REFUTED-ARTIFACT
"""
import html as _h
import streamlit as st

INK, MUTE = "#10243A", "#566B82"
TEAL, CORAL, GOLD, SLATE = "#138A74", "#DD5A47", "#CC8A3C", "#4E6E92"
GRID, PANEL = "#E4ECF3", "#F4F8FB"
GREEN, RED = TEAL, CORAL
STATUS = {
    "DEFINED":          (TEAL,  "characterised to necessity"),
    "CANDIDATE":        (GOLD,  "real, gated, still climbing"),
    "REDUCES-TO-KNOWN": (SLATE, "resolves to an existing feature"),
    "REFUTED-ARTIFACT": (CORAL, "killed by a later control"),
}


def _e(s):
    return _h.escape(str(s))


def ar(txt, size=26):
    return (f"<span dir='rtl' style='unicode-bidi:isolate;font-family:\"Amiri\",\"Scheherazade New\",serif;"
            f"font-size:{size}px;font-weight:700;color:{INK};line-height:1'>{_e(txt)}</span>")


def inject():
    st.markdown(f"""
    <style>
      .block-container,section.main .block-container,div[data-testid='stMainBlockContainer']{{
          max-width:1000px!important;padding-top:2rem!important;padding-bottom:1rem!important;margin:0 auto!important}}
      .cu-card{{background:#fff;border:1px solid #E7EEF5;border-radius:12px;padding:12px 15px;margin:6px 0;
               box-shadow:0 1px 2px rgba(16,36,58,.05)}}
      .cu-badge{{display:inline-block;padding:4px 12px;border-radius:999px;color:#fff;font-weight:800;
                font-size:12.5px;letter-spacing:.4px}}
      .cu-chip{{display:inline-block;padding:3px 10px;border-radius:7px;font-size:12.5px;font-weight:700;
               margin-right:7px}}
      .cu-q{{font-size:15.5px;opacity:.92;line-height:1.4}}
      .cu-sec{{display:flex;align-items:center;gap:10px;margin:16px 0 7px}}
      .cu-sec span.b{{width:6px;height:19px;border-radius:3px;background:{TEAL}}}
      .cu-sec b{{font-size:16px;font-weight:800;color:{INK};letter-spacing:.2px;
                background:linear-gradient(transparent 58%, {TEAL}30 0);padding:0 3px}}
      .cu-note{{font-size:14.5px;color:{MUTE};line-height:1.5;margin:1px 0 5px}}
      .cu-lede{{font-size:16px;line-height:1.62;color:#243b53}}
      .cu-eye{{font-size:12px;font-weight:800;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px}}
      table.cu-tbl{{border-collapse:separate;border-spacing:0;width:100%;font-size:12.5px;table-layout:auto;
                   border:1px solid #E7EEF5;border-radius:10px;overflow:hidden}}
      table.cu-tbl td,table.cu-tbl th{{padding:4px 8px;text-align:left;border-bottom:1px solid #EDF3F8;
                   vertical-align:top;line-height:1.3}}
      table.cu-tbl tr:last-child td{{border-bottom:none}}
      table.cu-tbl th{{background:{PANEL};color:{MUTE};font-size:10.5px;text-transform:uppercase;letter-spacing:.3px}}
      table.cu-tbl td:first-child{{font-weight:600}}
      table.cu-tbl td:last-child{{font-weight:800;color:{INK};font-variant-numeric:tabular-nums}}
    </style>""", unsafe_allow_html=True)


def hero(title, question, status, grade, substrate, arrangement, plain=""):
    col, _ = STATUS.get(status, (SLATE, ""))
    chip = ("background:rgba(255,255,255,.16);color:#eef4fb;border:1px solid rgba(255,255,255,.34)")
    st.markdown(
        f"<div style='background:linear-gradient(120deg,{INK},#1B3E5B 60%,{col});border-radius:13px;"
        f"padding:15px 19px;color:#fff'>"
        f"<div style='display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap'>"
        f"<div style='font-size:24px;font-weight:800'>{_e(title)}</div>"
        f"<span class='cu-badge' style='background:rgba(255,255,255,.2);border:1px solid rgba(255,255,255,.5)'>"
        f"{_e(status)} · grade {grade}</span></div>"
        f"<div style='background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.26);border-radius:9px;"
        f"padding:9px 13px;margin-top:9px'>"
        f"<div style='font-size:11.5px;font-weight:800;letter-spacing:1.1px;color:#c6e4dc'>THE PROBLEM</div>"
        f"<div style='font-size:17px;font-weight:800;line-height:1.4;margin-top:2px'>{_e(question)}</div></div>"
        f"<div style='margin-top:9px'><span class='cu-chip' style='{chip}'>🧬 {_e(substrate)}</span>"
        f"<span class='cu-chip' style='{chip}'>🗺️ {_e(arrangement)}</span></div></div>", unsafe_allow_html=True)


def story(what, why, accent=TEAL):
    st.markdown(
        f"<div class='cu-card' style='border:none;border-left:6px solid {accent};"
        f"background:linear-gradient(135deg,{accent}16,#fff 58%);padding:14px 18px'>"
        f"<div style='font-size:18.5px;font-weight:800;color:{INK};line-height:1.42'>{what}</div>"
        f"<div style='margin-top:10px;display:flex;align-items:baseline;gap:10px;flex-wrap:wrap'>"
        f"<span style='flex:0 0 auto;font-size:11px;font-weight:800;letter-spacing:.6px;color:#fff;"
        f"background:{accent};padding:4px 10px;border-radius:6px'>WHY IT MATTERS</span>"
        f"<span style='font-size:14.5px;color:#283A4D;line-height:1.5;flex:1;min-width:240px'>{why}</span>"
        f"</div></div>", unsafe_allow_html=True)


def headline(items):
    n = len(items)
    cells = ""
    for i, (v, lab, c) in enumerate(items):
        bd = "" if i == n - 1 else f"border-right:1px solid {GRID}"
        cells += (f"<div style='flex:1;min-width:130px;padding:9px 16px;{bd}'>"
                  f"<div style='font-size:27px;font-weight:800;color:{c or INK};font-variant-numeric:tabular-nums;"
                  f"line-height:1.05'>{_e(v)}</div>"
                  f"<div style='font-size:12px;color:{MUTE};text-transform:uppercase;letter-spacing:.4px;"
                  f"margin-top:3px'>{_e(lab)}</div></div>")
    st.markdown(f"<div class='cu-card' style='display:flex;flex-wrap:wrap;padding:3px 0'>{cells}</div>",
                unsafe_allow_html=True)


def foundation(body):
    st.markdown(
        f"<div class='cu-card' style='background:{PANEL};border-left:6px solid {SLATE}'>"
        f"<div class='cu-eye' style='color:{SLATE}'>Conceptual foundation</div>"
        f"<div class='cu-lede'>{body}</div></div>", unsafe_allow_html=True)


def section(label):
    st.markdown(f"<div class='cu-sec'><span class='b'></span><b>{_e(label)}</b></div>", unsafe_allow_html=True)


def note(txt):
    st.markdown(f"<div class='cu-note'>{txt}</div>", unsafe_allow_html=True)


def cascade(steps, zmax=12.0):
    """steps = [(label, value_str, z, ok_bool)] -> SVG survive→collapse trajectory (renders ~1:1, readable)."""
    zmin = -2.0
    W, H, L, R, T, B = 1000, 300, 60, 22, 34, 88
    pw, ph = W - L - R, H - T - B
    n = len(steps)
    X = (lambda i: L + (pw * (i / (n - 1)) if n > 1 else pw / 2))
    Y = (lambda z: T + ph * (1 - (max(zmin, min(zmax, z)) - zmin) / (zmax - zmin)))
    last_ok = max([i for i, s in enumerate(steps) if s[3]], default=0)
    split = last_ok / (n - 1) * 100 if n > 1 else 100
    pts = [(X(i), Y(s[2])) for i, s in enumerate(steps)]
    z0 = Y(0)
    g = ""
    for gz in (0, 4, 8, 12):
        if gz > zmax:
            continue
        y = Y(gz); bold = gz == 0
        dash = "" if bold else "stroke-dasharray='4 4'"
        stroke = "#9FB4C8" if bold else "#CFDBE6"
        g += (f"<line x1='{L}' y1='{y:.1f}' x2='{W-R}' y2='{y:.1f}' stroke='{stroke}' "
              f"stroke-width='{1.8 if bold else 1.1}' {dash}/>"
              f"<text x='{L-10}' y='{y+5:.1f}' text-anchor='end' font-size='13' fill='{MUTE}'>{gz}</text>")
    for gi in range(n):
        gx = X(gi)
        g += f"<line x1='{gx:.1f}' y1='{T}' x2='{gx:.1f}' y2='{T+ph}' stroke='#E1E9F1' stroke-width='1'/>"
    coll = ""
    if last_ok < n - 1:
        cx = (X(last_ok) + X(last_ok + 1)) / 2
        coll = (f"<rect x='{cx:.1f}' y='{T}' width='{W-R-cx:.1f}' height='{ph}' fill='{CORAL}' opacity='.07'/>"
                f"<text x='{(cx+W-R)/2:.1f}' y='{T+17}' text-anchor='middle' font-size='13' font-weight='800' "
                f"fill='{CORAL}' letter-spacing='1.5px'>COLLAPSE</text>")
    area = (f"M {pts[0][0]:.1f},{z0:.1f} " + " ".join(f"L {x:.1f},{y:.1f}" for x, y in pts) +
            f" L {pts[-1][0]:.1f},{z0:.1f} Z")
    poly = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    dots = ""
    for i, (lab, val, z, ok) in enumerate(steps):
        x, y = pts[i]; c = TEAL if ok else CORAL
        dots += (f"<circle cx='{x:.1f}' cy='{y:.1f}' r='6' fill='#fff' stroke='{c}' stroke-width='3'/>"
                 f"<text x='{x:.1f}' y='{y-13:.1f}' text-anchor='middle' font-size='14.5' font-weight='800' "
                 f"fill='{c}'>{_e(val)}</text>"
                 f"<text x='{x:.1f}' y='{H-B+20:.1f}' text-anchor='end' font-size='13' fill='#34506A' "
                 f"transform='rotate(-26 {x:.1f},{H-B+20:.1f})'>{_e(lab)}</text>")
    svg = (
        f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"
        f"<defs><linearGradient id='cuArea' x1='0' x2='1'>"
        f"<stop offset='0%' stop-color='{TEAL}' stop-opacity='.30'/>"
        f"<stop offset='{split:.0f}%' stop-color='{TEAL}' stop-opacity='.15'/>"
        f"<stop offset='{split:.0f}%' stop-color='{CORAL}' stop-opacity='.22'/>"
        f"<stop offset='100%' stop-color='{CORAL}' stop-opacity='.08'/></linearGradient></defs>"
        f"{coll}{g}<path d='{area}' fill='url(#cuArea)'/>"
        f"<polyline points='{poly}' fill='none' stroke='#33506A' stroke-width='2.6' "
        f"stroke-linejoin='round' stroke-linecap='round'/>{dots}"
        f"<text x='20' y='{T+ph/2}' transform='rotate(-90 20,{T+ph/2})' text-anchor='middle' "
        f"font-size='12.5' font-weight='700' fill='{MUTE}'>strength  z</text></svg>")
    st.markdown("<div class='cu-card'>" + svg + "</div>", unsafe_allow_html=True)


def bars(rows, fmt="{:.2f}", color=TEAL):
    """rows = [(label, value_0_1, note)] -> SVG horizontal bar chart, Arabic labels, readable."""
    pct = "%" in fmt
    mx = max([v for _, v, _ in rows] + [1e-9])
    top = 1.0 if pct else mx * 1.12
    rh, gap = 36, 11
    W, Lx, R = 1000, 150, 300
    H = 30 + len(rows) * (rh + gap)
    bw = W - Lx - R
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"]
    for f in (0, .25, .5, .75, 1):
        x = Lx + bw * f
        p.append(f"<line x1='{x:.0f}' y1='22' x2='{x:.0f}' y2='{H-8}' stroke='#CFDBE6' stroke-width='1' "
                 f"stroke-dasharray='4 4'/>")
        tk = ("{:.0%}".format(f * top)) if pct else ("{:.0f}".format(f * top))
        p.append(f"<text x='{x:.0f}' y='15' text-anchor='middle' font-size='12.5' fill='{MUTE}'>{tk}</text>")
    p.append(f"<defs><linearGradient id='cuBar' x1='0' x2='1'><stop offset='0' stop-color='{color}' "
             f"stop-opacity='.6'/><stop offset='1' stop-color='{color}'/></linearGradient></defs>")
    for i, (lab, v, ann) in enumerate(rows):
        y = 28 + i * (rh + gap)
        w = max(4, bw * (v / top))
        raw = lab
        if "<span" in str(lab):
            raw = str(lab).split(">", 1)[1].rsplit("</span>", 1)[0]
        inside = w > 86
        vx = (Lx + w - 11) if inside else (Lx + w + 7)
        p.append(
            f"<text x='{Lx-12}' y='{y+rh*0.68:.0f}' text-anchor='end' "
            f"font-family='Amiri,\"Scheherazade New\",serif' font-size='25' font-weight='700' fill='{INK}'>{_e(raw)}</text>"
            f"<rect x='{Lx}' y='{y:.0f}' width='{bw}' height='{rh}' rx='8' fill='{PANEL}'/>"
            f"<rect x='{Lx}' y='{y:.0f}' width='{w:.0f}' height='{rh}' rx='8' fill='url(#cuBar)'/>"
            f"<text x='{vx:.0f}' y='{y+rh*0.66:.0f}' text-anchor='{'end' if inside else 'start'}' font-size='14.5' "
            f"font-weight='800' fill='{'#fff' if inside else INK}'>{_e(fmt.format(v))}</text>"
            f"<text x='{Lx+bw+12}' y='{y+rh*0.66:.0f}' font-size='14' fill='{MUTE}'>{_e(ann)}</text>")
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)


def hist(values, labels, highlight=None, ref=None, reflabel="expected", color=SLATE, hcolor=CORAL):
    """Compact distribution histogram (many thin vertical bars). highlight one bar; optional reference line."""
    n = len(values)
    mx = (max(list(values) + ([ref] if ref else [])) or 1) * 1.18
    W, H, L, Rr, T, B = 960, 226, 50, 16, 28, 42
    pw, ph = W - L - Rr, H - T - B
    Y = (lambda v: T + ph * (1 - v / mx))
    bw = min(46, pw / n * 0.5)
    show = n <= 12
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"]
    p.append(f"<text x='{W-Rr}' y='13' text-anchor='end' font-size='11' fill='#9AAEC2'>ⓘ hover bars for exact counts</text>")
    for t in range(4):
        gv = mx * t / 3
        gy = Y(gv)
        p.append(f"<line x1='{L}' y1='{gy:.0f}' x2='{W-Rr}' y2='{gy:.0f}' stroke='#ECF1F6' stroke-width='1'/>"
                 f"<text x='{L-8}' y='{gy+4:.0f}' text-anchor='end' font-size='12' fill='{MUTE}'>{gv:.0f}</text>")
    if ref is not None:
        ry = Y(ref)
        lw = len(str(reflabel)) * 6.6 + 10
        p.append(f"<line x1='{L}' y1='{ry:.0f}' x2='{W-Rr}' y2='{ry:.0f}' stroke='{INK}' stroke-width='1.3' "
                 f"stroke-dasharray='5 4'/>"
                 f"<rect x='{L+5}' y='{ry-15:.0f}' width='{lw:.0f}' height='15' rx='3' fill='#fff' opacity='.92'/>"
                 f"<text x='{L+9}' y='{ry-4:.0f}' font-size='11.5' font-weight='700' fill='{INK}'>{_e(reflabel)}</text>")
    for i, (v, lab) in enumerate(zip(values, labels)):
        cx = L + pw * (i + 0.5) / n
        col = hcolor if i == highlight else color
        by = Y(v); bh = (T + ph) - by
        p.append(f"<g style='cursor:pointer'><title>{_e(lab)}: {_e(v)}</title>"
                 f"<rect x='{cx-bw/2:.1f}' y='{by:.1f}' width='{bw:.1f}' height='{bh:.1f}' rx='2' fill='{col}'/></g>"
                 f"<text x='{cx:.1f}' y='{H-B+17:.0f}' text-anchor='middle' font-size='12' "
                 f"fill='{INK if i==highlight else MUTE}'>{_e(lab)}</text>")
        if show or i == highlight:
            fs, fw = (13, 800) if i == highlight else (11, 700)
            fc = hcolor if i == highlight else INK
            p.append(f"<text x='{cx:.1f}' y='{by-5:.0f}' text-anchor='middle' font-size='{fs}' font-weight='{fw}' "
                     f"fill='{fc}'>{_e(v)}</text>")
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)


def scale(lo_label, lo, mid_label, mid, hi_label, hi):
    W, H, L, R = 1000, 92, 26, 26
    bw = W - L - R
    span = (hi - lo) or 1
    mx = L + bw * max(0, min(1, (mid - lo) / span))
    svg = (
        f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"
        f"<defs><linearGradient id='cuSc' x1='0' x2='1'><stop offset='0' stop-color='{GRID}'/>"
        f"<stop offset='.5' stop-color='{GOLD}'/><stop offset='1' stop-color='{TEAL}'/></linearGradient></defs>"
        f"<rect x='{L}' y='46' width='{bw}' height='10' rx='5' fill='url(#cuSc)'/>"
        f"<text x='{L}' y='76' font-size='13.5' fill='{MUTE}'>{_e(lo_label)} · {lo:g}</text>"
        f"<text x='{W-R}' y='76' text-anchor='end' font-size='13.5' fill='{MUTE}'>{_e(hi_label)} · {hi:g}</text>"
        f"<polygon points='{mx:.0f},40 {mx-8:.0f},24 {mx+8:.0f},24' fill='{INK}'/>"
        f"<line x1='{mx:.0f}' y1='40' x2='{mx:.0f}' y2='60' stroke='{INK}' stroke-width='3'/>"
        f"<text x='{mx:.0f}' y='18' text-anchor='middle' font-size='14' font-weight='800' "
        f"fill='{INK}'>{_e(mid_label)} · {mid:g}</text></svg>")
    st.markdown("<div class='cu-card'>" + svg + "</div>", unsafe_allow_html=True)


def table(headers, rows, tight=True):
    cls = "cu-tbl cu-tight" if tight else "cu-tbl"
    th = "".join(f"<th>{_e(h)}</th>" for h in headers)
    trs = []
    for r in rows:
        tds = "".join(f"<td>{c if '<span' in str(c) else _e(c)}</td>" for c in r)
        trs.append(f"<tr>{tds}</tr>")
    st.markdown(f"<table class='{cls}'><tr>{th}</tr>{''.join(trs)}</table>", unsafe_allow_html=True)


def verdict(status, text, confidence, flip, revise):
    col = STATUS.get(status, (SLATE, ""))[0]
    st.markdown(
        f"<div class='cu-card' style='border:none;border-left:6px solid {col};"
        f"background:linear-gradient(90deg,{col}10,#fff 44%)'>"
        f"<div style='font-size:13px;font-weight:800;letter-spacing:.6px;color:{col}'>VERDICT — {_e(status)}</div>"
        f"<div style='font-size:14.5px;line-height:1.58;color:#283A4D;margin:6px 0'>{text}</div>"
        f"<div style='font-size:13.5px;color:{MUTE};line-height:1.7'>"
        f"<b style='color:{INK}'>Confidence</b> {_e(confidence)} &nbsp;·&nbsp; "
        f"<b style='color:{INK}'>Flips if</b> {_e(flip)} &nbsp;·&nbsp; "
        f"<b style='color:{INK}'>Revise-up</b> {_e(revise)}</div></div>", unsafe_allow_html=True)


def para(text):
    """Discussion prose paragraph."""
    st.markdown(f"<div style='font-size:14.5px;line-height:1.62;color:#283A4D;margin:3px 2px 9px'>{text}</div>",
                unsafe_allow_html=True)


def callout(label, text, accent=SLATE):
    """Labelled discussion block (Hypothesis / Method / Interpretation / Caveats)."""
    st.markdown(
        f"<div class='cu-card' style='border-left:5px solid {accent};background:{accent}0c'>"
        f"<div class='cu-eye' style='color:{accent}'>{_e(label)}</div>"
        f"<div style='font-size:14.5px;line-height:1.6;color:#283A4D'>{text}</div></div>", unsafe_allow_html=True)


def kpis(items):
    """items = [(value, label, tip, color_or_None)] -> compact KPI boxes with hover tooltips."""
    cells = ""
    for v, lab, tip, c in items:
        cells += (f"<div title='{_e(tip)}' style='position:relative;flex:1 1 96px;min-width:96px;background:#fff;"
                  f"border:1px solid #E7EEF5;border-radius:9px;padding:6px 10px 7px;cursor:help'>"
                  f"<div style='position:absolute;top:4px;right:6px;width:14px;height:14px;border-radius:50%;"
                  f"background:#EEF3F8;color:#8FA6BC;font-size:10px;font-weight:800;text-align:center;"
                  f"line-height:14px'>i</div>"
                  f"<div style='font-size:19px;font-weight:800;color:{c or INK};line-height:1.05;"
                  f"font-variant-numeric:tabular-nums'>{_e(v)}</div>"
                  f"<div style='font-size:11px;color:{MUTE};line-height:1.18;margin-top:1px;display:inline;"
                  f"border-bottom:1px dotted #B9C8D6'>{_e(lab)}</div></div>")
    st.markdown(f"<div style='font-size:10.5px;color:#8FA6BC;margin:2px 2px 0;font-weight:700;"
                f"letter-spacing:.3px'>ⓘ hover any box for its definition</div>"
                f"<div style='display:flex;flex-wrap:wrap;gap:6px;margin:3px 0 5px'>{cells}</div>",
                unsafe_allow_html=True)


def vbars(rows, ymax=None, ymin=None, fmt="{:.2f}", color=TEAL):
    """Clean editorial HORIZONTAL comparison bars. rows = [(label, value, color_or_None, tip)]."""
    vals = [r[1] for r in rows]
    hi = ymax if ymax is not None else max(vals + [0]) * 1.04
    lo = ymin if ymin is not None else min(vals + [0])
    if lo > 0:
        lo = 0
    n = len(rows)
    W = 960
    rowh, barh, padT, padB = 40, 22, 28, 10
    labelW, valW = 176, 54
    tx, tw = labelW, W - labelW - valW
    span = (hi - lo) or 1
    H = padT + n * rowh + padB
    X = (lambda v: tx + tw * (v - lo) / span)
    x0 = X(0)
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"]
    for t in range(5):
        gv = lo + span * t / 4
        gx = X(gv)
        p.append(f"<line x1='{gx:.0f}' y1='{padT-5}' x2='{gx:.0f}' y2='{H-padB}' stroke='#ECF1F6' stroke-width='1'/>"
                 f"<text x='{gx:.0f}' y='{padT-11}' text-anchor='middle' font-size='12' fill='{MUTE}'>{gv:.2g}</text>")
    if lo < 0:
        p.append(f"<line x1='{x0:.0f}' y1='{padT-5}' x2='{x0:.0f}' y2='{H-padB}' stroke='#9FB4C8' stroke-width='1.3'/>")
    for i, (lab, v, c, tip) in enumerate(rows):
        cy = padT + i * rowh + rowh / 2
        col = c or color
        bx = min(x0, X(v)); bw = max(2, abs(X(v) - x0))
        vstr = fmt.format(v)
        p.append(f"<text x='{labelW-13}' y='{cy+5:.0f}' text-anchor='end' font-size='14' font-weight='600' "
                 f"fill='{INK}'>{_e(lab)}</text>"
                 f"<rect x='{tx}' y='{cy-barh/2:.0f}' width='{tw}' height='{barh}' rx='3' fill='{PANEL}'/>"
                 f"<g><title>{_e(tip)}</title><rect x='{bx:.0f}' y='{cy-barh/2:.0f}' width='{bw:.0f}' height='{barh}' "
                 f"rx='3' fill='{col}'/></g>")
        if bw > 50 and v >= 0:
            p.append(f"<text x='{X(v)-10:.0f}' y='{cy+5:.0f}' text-anchor='end' font-size='13.5' font-weight='800' "
                     f"fill='#fff'>{_e(vstr)}</text>")
        else:
            vx = X(v) + (9 if v >= 0 else -9)
            anc = "start" if v >= 0 else "end"
            p.append(f"<text x='{vx:.0f}' y='{cy+5:.0f}' text-anchor='{anc}' font-size='13.5' font-weight='800' "
                     f"fill='{INK}'>{_e(vstr)}</text>")
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)
