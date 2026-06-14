"""Close-up · Importance reframed — from a linear ranking to roles in a network (احسن تقویم).
CANDIDATE. The question "which concept is most important?" is shown to be ill-posed (a linear total order),
and replaced by a measured, null-validated framework: every concept has a ROLE in the co-occurrence system,
and the system is in best-proportion (احسن تقویم) — NECESSARY (cannot delete) and SUFFICIENT (cannot add).
All numbers MEASURED on Book6 rasm: ROOT (content), WORD (surface form) and MORPHOLOGY (forms) substrates,
each against the text's own shuffle (the One Law). Data file: closeup_importance_data.json (committed)."""
import os, json
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Importance as roles", page_icon="🕸️", layout="wide")
if S:
    try:
        S.log_page("closeup_importance")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()
INK, TEAL, CORAL, GOLD, SLATE = C.INK, C.TEAL, C.CORAL, C.GOLD, C.SLATE

# ── data (measured; shipped with repo) ──
_DP = os.path.join(os.path.dirname(__file__), "..", "closeup_importance_data.json")
try:
    D = json.load(open(_DP, encoding="utf-8"))
except Exception:
    D = {}
def g(k, d=None): return D.get(k, d)
N = g("nulls", {})

GLOSS = {"ءله": "God", "قول": "say", "کون": "be", "ربب": "Lord", "ءمن": "believe", "علم": "know",
         "قوم": "people", "عبد": "worship", "رحم": "mercy", "کثر": "abundance", "حمد": "praise",
         "وسی": "Mūsā", "رسل": "messenger", "کفر": "disbelieve", "صمد": "Eternal", "نحر": "sacrifice",
         "کفء": "equal", "لهب": "flame", "بتر": "cut-off", "ءلی": "bounties", "عصر": "epoch",
         "وسوس": "whisper", "قرع": "striking", "حسد": "envy", "ءرض": "earth", "فرعن": "Pharaoh",
         "برهم": "Abraham", "ءتی": "come", "لقی": "meet", "نهی": "forbid", "بین": "clarify"}
def gl(t): return GLOSS.get(t, "")


# ════════ custom dense SVG: NETWORK (the reframing centrepiece) ════════
def net(ko_hub=None, title=""):
    net = g("net", {})
    nodes = net.get("nodes", []); edges = net.get("edges", [])
    if not nodes:
        C.note("network data unavailable"); return
    W, H = 1000, 600
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"]
    for i, j, w in edges:
        xi, yi = nodes[i][1], nodes[i][2]; xj, yj = nodes[j][1], nodes[j][2]
        op = 0.08 + 0.42 * min(1.0, w / 3.0)
        p.append(f"<line x1='{xi:.0f}' y1='{yi:.0f}' x2='{xj:.0f}' y2='{yj:.0f}' "
                 f"stroke='#9FB4C8' stroke-width='1' stroke-opacity='{op:.2f}'/>")
    for (lab, x, y, role, deg, col) in nodes:
        r = 6 + 1.7 * (deg ** 0.5)
        faded = (ko_hub is not None and lab == ko_hub)
        fill = "#D7DEE6" if faded else col
        dash = "stroke-dasharray='3 3'" if faded else ""
        p.append(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{r:.1f}' fill='{fill}' stroke='#fff' "
                 f"stroke-width='1.6' {dash}/>")
        ty = y + r + 13 if y < H - 26 else y - r - 6
        p.append(f"<text x='{x:.0f}' y='{ty:.0f}' text-anchor='middle' "
                 f"font-family='Amiri,\"Scheherazade New\",serif' font-size='14.5' font-weight='700' "
                 f"fill='{INK}'>{lab}</text>")
    if ko_hub:
        p.append(f"<text x='{W/2:.0f}' y='24' text-anchor='middle' font-size='13.5' font-weight='800' "
                 f"fill='{CORAL}'>✂ remove hub {ko_hub} → network stays in ONE piece "
                 f"(robust, not a single point of failure)</text>")
    # legend
    leg = [("hub", CORAL), ("provincial-hub", GOLD), ("connector", TEAL), ("peripheral", SLATE)]
    lx = 40
    for name, c in leg:
        p.append(f"<circle cx='{lx}' cy='{H-12}' r='6' fill='{c}'/>"
                 f"<text x='{lx+11}' y='{H-7}' font-size='12.5' fill='{INK}'>{name}</text>")
        lx += 60 + 8 * len(name)
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)


# ════════ custom dense SVG: SCATTER ════════
def scatter(pts, cloud, xr, yr, xlab, ylab, regline=None, kindcol=None, arabic=True, note_quad=None,
            legend=None, regions=None):
    W, H, L, B, Tp, Rr = 1000, 588, 76, 92, 36, 26
    pw, ph = W - L - Rr, H - Tp - B
    (x0, x1), (y0, y1) = xr, yr
    X = lambda v: L + pw * (v - x0) / ((x1 - x0) or 1)
    Y = lambda v: Tp + ph * (1 - (v - y0) / ((y1 - y0) or 1))
    kc = kindcol or {"system": CORAL, "unit": TEAL, "other": SLATE}
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"]
    for t in range(5):
        gx = L + pw * t / 4; gy = Tp + ph * t / 4
        p.append(f"<line x1='{gx:.0f}' y1='{Tp}' x2='{gx:.0f}' y2='{Tp+ph}' stroke='#ECF1F6' stroke-width='1'/>")
        p.append(f"<line x1='{L}' y1='{gy:.0f}' x2='{L+pw}' y2='{gy:.0f}' stroke='#ECF1F6' stroke-width='1'/>")
        vx = x0 + (x1 - x0) * t / 4; vy = y1 - (y1 - y0) * t / 4
        p.append(f"<text x='{gx:.0f}' y='{Tp+ph+18:.0f}' text-anchor='middle' font-size='12.5' fill='{INK}'>{vx:.0f}</text>")
        p.append(f"<text x='{L-9}' y='{gy+4:.0f}' text-anchor='end' font-size='12.5' fill='{INK}'>{vy:.1f}</text>")
    if note_quad:
        p.append(f"<rect x='{X((x0+x1)/2):.0f}' y='{Tp}' width='{L+pw-X((x0+x1)/2):.0f}' "
                 f"height='{ph/2:.0f}' fill='{CORAL}' opacity='.04'/>")
        p.append(f"<rect x='{L}' y='{Tp}' width='{X((x0+x1)/2)-L:.0f}' height='{ph/2:.0f}' fill='{TEAL}' opacity='.04'/>")
    for cx, cy in cloud:
        p.append(f"<circle cx='{X(cx):.1f}' cy='{Y(cy):.1f}' r='2.6' fill='#B9C8D6' fill-opacity='.55'/>")
    if regline:
        b, a = regline
        xa, xb = x0, x1
        p.append(f"<line x1='{X(xa):.0f}' y1='{Y(a+b*xa):.0f}' x2='{X(xb):.0f}' y2='{Y(a+b*xb):.0f}' "
                 f"stroke='{SLATE}' stroke-width='1.6' stroke-dasharray='6 4'/>")
    if regions:
        for rx, ry, rtxt, rcol in regions:
            p.append(f"<text x='{X(rx):.0f}' y='{Y(ry):.0f}' text-anchor='middle' font-size='13' font-weight='800' "
                     f"fill='{rcol}' opacity='.85'>{rtxt}</text>")
    # labelled points with simple anti-overlap (place label on the open side, alternate vertical)
    for k, row in enumerate(pts):
        lab, cx, cy = row[0], row[1], row[2]; kind = row[3] if len(row) > 3 else "other"
        col = kc.get(kind, SLATE) if isinstance(kind, str) else SLATE
        px, py = X(cx), Y(cy)
        left = cx > (x0 + x1) * 0.62           # crowded right side → label to the LEFT
        dx = -9 if left else 9
        dy = 4 + (-11 if (k % 2) else 11) * 0  # keep baseline; reserve hook for future jitter
        anc = "end" if left else "start"
        p.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='5.5' fill='{col}' stroke='#fff' stroke-width='1.4'/>")
        fam = "font-family='Amiri,\"Scheherazade New\",serif' " if arabic else ""
        p.append(f"<text x='{px+dx:.1f}' y='{py+dy:.1f}' text-anchor='{anc}' {fam}font-size='14' "
                 f"font-weight='700' fill='{INK}'>{lab}</text>")
    p.append(f"<text x='{L+pw/2:.0f}' y='{Tp+ph+40:.0f}' text-anchor='middle' font-size='13.5' font-weight='700' "
             f"fill='{INK}'>{xlab}</text>")
    p.append(f"<text x='20' y='{Tp+ph/2:.0f}' transform='rotate(-90 20,{Tp+ph/2:.0f})' text-anchor='middle' "
             f"font-size='13.5' font-weight='700' fill='{INK}'>{ylab}</text>")
    if legend:
        lx = L
        for name, c in legend:
            p.append(f"<circle cx='{lx}' cy='{H-16}' r='6' fill='{c}'/>"
                     f"<text x='{lx+12}' y='{H-11}' font-size='12.5' fill='{INK}'>{name}</text>")
            lx += 40 + int(7.3 * len(name))
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)


# ════════ custom schematic: احسن تقویم — necessity + sufficiency ════════
def ahsan():
    W, H = 1000, 396
    cx, cy = 500, 190
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"]
    # ring of roles around a hub
    import math as _m
    ring = [("referent (hub)", CORAL, 0), ("connector", TEAL, 60), ("connector", TEAL, 120),
            ("specialist", SLATE, 180), ("unit-definer", GOLD, 240), ("specialist", SLATE, 300)]
    pos = []
    for i, (lab, col, ang) in enumerate(ring):
        a = _m.radians(ang); x = cx + 168 * _m.cos(a); y = cy + 110 * _m.sin(a); pos.append((x, y, lab, col))
    # edges hub->all + a few cross
    hub = pos[0]
    for x, y, lab, col in pos[1:]:
        p.append(f"<line x1='{hub[0]:.0f}' y1='{hub[1]:.0f}' x2='{x:.0f}' y2='{y:.0f}' stroke='#9FB4C8' stroke-width='1.5'/>")
    for a, b in [(1, 2), (2, 3), (4, 5), (3, 4), (5, 1)]:
        p.append(f"<line x1='{pos[a][0]:.0f}' y1='{pos[a][1]:.0f}' x2='{pos[b][0]:.0f}' y2='{pos[b][1]:.0f}' "
                 f"stroke='#C4D2DF' stroke-width='1'/>")
    for x, y, lab, col in pos:
        r = 26 if "hub" in lab else 18
        p.append(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{r}' fill='{col}' stroke='#fff' stroke-width='2'/>")
        ly = (y - r - 9) if y < cy - 5 else (y + r + 17)   # full label OUTSIDE node, in ink (never clipped)
        p.append(f"<text x='{x:.0f}' y='{ly:.0f}' text-anchor='middle' font-size='13' font-weight='800' "
                 f"fill='{INK}'>{lab}</text>")
    # left/right annotations
    p.append(f"<rect x='14' y='110' width='196' height='150' rx='10' fill='{TEAL}' opacity='.08'/>"
             f"<text x='28' y='138' font-size='14.5' font-weight='800' fill='{TEAL}'>CANNOT DELETE</text>"
             f"<text x='28' y='160' font-size='13' fill='{INK}'>= NECESSARY</text>"
             f"<text x='28' y='184' font-size='12.5' fill='{INK}'>every role is load-</text>"
             f"<text x='28' y='201' font-size='12.5' fill='{INK}'>bearing; remove it and</text>"
             f"<text x='28' y='218' font-size='12.5' fill='{INK}'>its unit/role degrades</text>"
             f"<text x='28' y='240' font-size='12' fill='{INK}'>(shuffle kills structure;</text>"
             f"<text x='28' y='256' font-size='12' fill='{INK}'>unit-definers q&lt;0.05)</text>")
    p.append(f"<rect x='790' y='110' width='196' height='150' rx='10' fill='{GOLD}' opacity='.10'/>"
             f"<text x='804' y='138' font-size='14.5' font-weight='800' fill='{GOLD}'>CANNOT ADD</text>"
             f"<text x='804' y='160' font-size='13' fill='{INK}'>= SUFFICIENT</text>"
             f"<text x='804' y='184' font-size='12.5' fill='{INK}'>the role-space is</text>"
             f"<text x='804' y='201' font-size='12.5' fill='{INK}'>saturated: 2 axes hold</text>"
             f"<text x='804' y='218' font-size='12.5' fill='{INK}'>92% of structure; one</text>"
             f"<text x='804' y='240' font-size='12' fill='{INK}'>connected whole (99.8%);</text>"
             f"<text x='804' y='256' font-size='12' fill='{INK}'>no empty role to fill</text>")
    p.append(f"<text x='{cx:.0f}' y='30' text-anchor='middle' font-size='15' font-weight='800' fill='{INK}'>"
             f"احسن تقویم — best proportion: necessary AND sufficient</text>")
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)


def pair_table(h1, h2, rows, c1=TEAL, c2=CORAL):
    """Two equal-width columns that fill the row (table-layout:fixed) — no wasted middle space."""
    thst = ("background:#F4F8FB;text-align:left;padding:5px 10px;font-size:12px;text-transform:uppercase;"
            "letter-spacing:.3px;border-bottom:1px solid #E1E9F1;width:50%")
    th = f"<tr><th style='{thst};color:{c1}'>{h1}</th><th style='{thst};color:{c2}'>{h2}</th></tr>"
    tdst = (f"padding:6px 10px;font-size:12.5px;color:{INK};vertical-align:top;border-bottom:1px solid #EDF3F8;"
            "line-height:1.42;width:50%")
    trs = "".join(f"<tr><td style='{tdst}'>{a}</td><td style='{tdst}'>{b}</td></tr>" for a, b in rows)
    st.markdown(f"<table style='border-collapse:separate;border-spacing:0;width:100%;table-layout:fixed;"
                f"border:1px solid #E7EEF5;border-radius:10px;overflow:hidden;margin:6px 0'>{th}{trs}</table>",
                unsafe_allow_html=True)


def curve(rc):
    """Attack-vs-random knockout curve: x = fraction of concepts removed, y = largest connected piece."""
    fr, at, rd = rc.get("fracs", []), rc.get("attack", []), rc.get("random", [])
    if not fr:
        return
    W, H, L, B, Tp, Rr = 1000, 430, 70, 76, 30, 216
    pw, ph = W - L - Rr, H - Tp - B
    fmax = max(fr) or 1
    X = lambda f: L + pw * f / fmax
    Y = lambda v: Tp + ph * (1 - v)
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"]
    for t in range(6):
        gy = Tp + ph * t / 5
        p.append(f"<line x1='{L}' y1='{gy:.0f}' x2='{L+pw}' y2='{gy:.0f}' stroke='#ECF1F6' stroke-width='1'/>"
                 f"<text x='{L-8}' y='{gy+4:.0f}' text-anchor='end' font-size='12.5' fill='{INK}'>{1-t/5:.0%}</text>")
    for t in range(6):
        f = fmax * t / 5
        p.append(f"<text x='{X(f):.0f}' y='{Tp+ph+18:.0f}' text-anchor='middle' font-size='12.5' fill='{INK}'>{f:.0%}</text>")

    def poly(vals, col):
        pts = " ".join(f"{X(f):.1f},{Y(v):.1f}" for f, v in zip(fr, vals))
        s = f"<polyline points='{pts}' fill='none' stroke='{col}' stroke-width='3' stroke-linejoin='round'/>"
        for f, v in zip(fr, vals):
            s += f"<circle cx='{X(f):.1f}' cy='{Y(v):.1f}' r='3.6' fill='{col}'/>"
        return s
    p.append(poly(rd, TEAL)); p.append(poly(at, CORAL))
    lx = L + pw + 18
    p.append(f"<rect x='{lx}' y='{Tp+8}' width='12' height='12' fill='{TEAL}'/>"
             f"<text x='{lx+16}' y='{Tp+18}' font-size='13' font-weight='700' fill='{INK}'>random failure</text>"
             f"<rect x='{lx}' y='{Tp+32}' width='12' height='12' fill='{CORAL}'/>"
             f"<text x='{lx+16}' y='{Tp+42}' font-size='13' font-weight='700' fill='{INK}'>targeted attack</text>")
    if len(rd) and len(at) > 1:
        p.append(f"<text x='{lx}' y='{Tp+76}' font-size='12.5' fill='{INK}'>50% gone →</text>"
                 f"<text x='{lx}' y='{Tp+94}' font-size='12.5' fill='{TEAL}'>random {rd[-1]:.0%} intact</text>"
                 f"<text x='{lx}' y='{Tp+118}' font-size='12.5' fill='{INK}'>30% gone →</text>"
                 f"<text x='{lx}' y='{Tp+136}' font-size='12.5' fill='{CORAL}'>attack {at[-2]:.0%} intact</text>")
    p.append(f"<text x='{L+pw/2:.0f}' y='{H-8}' text-anchor='middle' font-size='13.5' font-weight='700' "
             f"fill='{INK}'>fraction of concepts removed →</text>"
             f"<text x='22' y='{Tp+ph/2:.0f}' transform='rotate(-90 22,{Tp+ph/2:.0f})' text-anchor='middle' "
             f"font-size='13.5' font-weight='700' fill='{INK}'>largest connected piece</text>")
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)


# ╔══════════════ 1 · PROBLEM ══════════════╗
C.hero("Importance, reframed — from a ranking to roles in a network",
       "“Which concept is the most important in the Qur'ān?” Counting says ‘the most frequent’. But is "
       "importance a single ladder at all — or is the very question (one linear ranking) the wrong shape?",
       "CANDIDATE", 72, "rasm — ROOT (content) · WORD (form) · MORPHOLOGY", "DIVINE-DEFAULT · network + shuffle null")
st.markdown(
    "<div style='display:flex;justify-content:flex-end;gap:9px;margin:7px 0 2px;flex-wrap:wrap'>"
    "<a href='#im-fa' style='text-decoration:none'><div style='background:linear-gradient(135deg,#138A74,#10243A);"
    "color:#fff;border-radius:9px;padding:7px 13px;font-weight:800;font-size:13px;border:1px solid rgba(255,255,255,.3)'>"
    "📄 خلاصهٔ فارسی ↓</div></a>"
    "<a href='#im-ar' style='text-decoration:none'><div style='background:linear-gradient(135deg,#4E6E92,#10243A);"
    "color:#fff;border-radius:9px;padding:7px 13px;font-weight:800;font-size:13px;border:1px solid rgba(255,255,255,.3)'>"
    "📄 الملخّص العربي ↓</div></a></div>", unsafe_allow_html=True)
C.onpage(["① Problem", "② Hypothesis", "③ Method",
          "<b>④ Results · the network & roles</b>", "<b>⑤ Necessity</b> (cannot delete)",
          "<b>⑥ Sufficiency</b> (cannot add)", "<b>⑫ What if?</b> (ablation)", "⑦ Gating",
          "⑧ Interpretation", "⑨ Caveats", "⑩ Verdict"],
         fa="im-fa", ar="im-ar",
         closers="<b>Path forward</b> · Reflection · Summary · Lessons · Takeaway")
C.story(
    "Asking <b>“which word matters most”</b> assumes importance is one ladder — a linear total order — and that "
    "the rung is set by <b>frequency</b>. Both assumptions fail on the data. Frequency, morphological richness and "
    "spread are the <b>same</b> axis (they agree ~0.8–0.94), so the famous ‘most-repeated-words’ list is almost all "
    "redundancy; once you credit each criterion only for what it <i>uniquely</i> adds, raw count is worth "
    f"<b>{g('weights',[7])[0]}%</b>. The fix is to stop ranking and ask a different question: <b>what ROLE does each "
    "concept play in the system, and could the system work without it?</b>",
    "This operationalises <b>احسن تقویم</b> (Q 95:4, best proportion): a designed whole where <b>nothing can be "
    "added because it is sufficient, and nothing deleted because it is necessary</b>. Every concept — pervasive "
    "hub or rare unit-definer — has a measured, null-validated role. <b>Nothing is unimportant.</b>", accent=TEAL)

# ── epigraph: Ḥāfeẓ — "everything good in its own place" = each concept in its role ──
st.markdown(
    "<div style='background:linear-gradient(135deg,#10243A,#1B3E5B);border-radius:13px;padding:15px 20px;"
    "margin:8px 0;text-align:center;color:#fff'>"
    "<div dir='rtl' style='font-family:Vazirmatn,\"Scheherazade New\",Amiri,serif;font-size:20px;font-weight:700;"
    "line-height:2'>جهان چون خط و خال و چشم و ابروست &nbsp;/&nbsp; که هر چیزی به جای خویش نیکوست</div>"
    "<div style='font-size:13.5px;color:#c6e4dc;margin-top:7px;line-height:1.5'>"
    "“The world is like script and mole and eye and brow — for <b>each thing is beautiful in its own place</b>.” "
    "— Ḥāfeẓ</div>"
    "<div style='font-size:12.5px;color:#eef4fb;margin-top:4px'>The thesis in one line: importance is not a rank — "
    "it is <b>being in one's place</b> (role) within a proportioned whole (احسن تقویم).</div></div>",
    unsafe_allow_html=True)

top = g("top", [])
w = g("weights", [7, 22, 8, 63])
C.headline([
    (str(g("root_types", "—")), "root concepts", INK),
    (str(g("word_types", "—")), "surface words", SLATE),
    (f"{w[0]}%", "unique info in FREQUENCY", CORAL),
    (f"+{N.get('modularity_z','—')}", "z · role structure is real", TEAL),
    (f"{N.get('giant_frac',0)*100:.1f}%", "one connected whole", TEAL),
])
C.kpis([
    ("0.81–0.94", "freq ≈ forms ≈ spread", "The three ‘criteria’ correlate 0.79–0.94 — they are ONE axis (prominence), so ranking by any of them is the same list", SLATE),
    (f"{w[0]}% / {w[3]}%", "freq vs concentration (unique)", "Credited for non-redundant information only: frequency 7%, concentration 63% — the loud signal is the least informative", CORAL),
    (f"+{N.get('modularity_z','—')} z", "roles are real", "Modularity 0.134 vs degree-matched null 0.043 — the network has genuine role structure, not chance", TEAL),
    (f"{N.get('cut_z','—')} z", "built robust", "Fewer single-points-of-failure than a random graph of the same degrees — engineered redundancy", TEAL),
    (str(g("root_sig", "—")) + " / " + str(g("word_sig", "—")), "unit-definers (root/word)", "Concepts that non-randomly OWN a sūra (FDR q<0.05): rare but necessary to their unit — صمد, کوثر, نحر …", GOLD),
    ("92%", "structure in 2 axes", "PCA: prominence + concentration capture 92% of the importance variance — the space is essentially 2-D and saturated", TEAL),
    ("72", "grade", "CANDIDATE — the reframe is defensible and null-validated; not yet discovery-tier (≥90)", GOLD),
])

# ── survey of schools ──
C.section("Problem — three schools, one hidden assumption")
C.callout("How importance has been argued — and where each falls short",
          "<b>1 · Thematic / maqāṣid (classical & modern).</b> Ranks concepts by doctrinal weight (tawḥīd, ʿibāda, "
          "ʿadl…). Insightful, but <b>not measured</b> — it reads importance in, it does not derive it from the text.<br>"
          "&nbsp;&nbsp;<b>2 · Numerical (iʿjāz ʿadadī).</b> Counts words and reads design into the totals. We showed "
          "in the sibling close-up that <b>counts ride on spelling</b> and equal-frequency is mostly chance. Counting "
          "answers ‘how many’, never ‘what role’.<br>"
          "&nbsp;&nbsp;<b>3 · Computational keyword / concordance.</b> Ranks by frequency or TF-IDF. Modern, but "
          f"inherits the <b>linear-ranking</b> assumption — and on this corpus frequency is only <b>{w[0]}%</b> "
          "unique information.<br>"
          "<b>The shared flaw:</b> all three assume importance is a <b>single ladder</b>. The data says it is not. "
          "We replace the ladder with a <b>network of roles</b> — and that reframing is the contribution.", accent=SLATE)

C.note("① The loud signal. Top concepts by raw frequency (ROOT substrate). Real, but — as the next chart shows — "
       "frequency mostly duplicates spread and morphology; it is not independent evidence of importance.")
C.vbars([(C.ar(t[0], 19) + " " + gl(t[0]), t[1], TEAL, f"{t[0]} = {t[1]}") for t in top[:8]],
        fmt="{:.0f}")
C.note("② The redundancy verdict. Each criterion credited only for the information it adds that the others do NOT. "
       "Frequency, spread and morphology overlap heavily, so frequency’s unique share is tiny; <b>concentration</b> "
       "(owning a place) is the most non-redundant signal. This is why ‘count the words’ is the weakest method.")
C.vbars([("frequency", w[0]/100, CORAL, "raw count — mostly duplicated by spread/forms"),
         ("spread (sūras)", w[2]/100, SLATE, "where it appears — overlaps frequency"),
         ("morphology (forms)", w[1]/100, GOLD, "derivational life — partly independent"),
         ("concentration", w[3]/100, TEAL, "owns a place — the most unique signal")],
        ymax=0.8, fmt="{:.0%}")

# ── morphology scatter (form vs content) ──
sm = g("scatter_morph", {})
C.note("③ Form vs content — morphology adds what frequency cannot. Each dot a root: x = log frequency, y = number "
       "of distinct surface forms. Above the line = <b>living</b> concepts that spawn many forms (قوم 45, لقی 33); "
       "below = <b>frozen</b> proper-nouns dense but inert (ءله, موسى, فرعون). Same count, different life.")
if sm:
    mpts = [[r[0], r[1], __import__("math").log10(r[2] + 1), ("living" if r[3] else "frozen")] for r in sm.get("pts", [])]
    scatter(mpts, sm.get("cloud", []), (0, 3.6), (0, 1.85),
            "log10 frequency  →  (how often a root occurs)", "log10 (number of distinct forms)",
            regline=(sm.get("slope"), sm.get("intercept")),
            kindcol={"living": TEAL, "frozen": CORAL},
            legend=[("living (above fit)", TEAL), ("frozen (below fit)", CORAL),
                    ("all roots", "#B9C8D6"), ("expected by frequency", SLATE)],
            regions=[(0.95, 1.72, "↑ LIVING — more forms than frequency predicts", TEAL),
                     (2.7, 0.12, "FROZEN — proper-nouns, dense but inert ↓", CORAL)])
C.note("Living vs frozen — a few examples by raw form-count. A proper noun can be frequent yet morphologically "
       "frozen; a verb can be modest yet generative. Frequency cannot see this difference; morphology can.")
C.vbars([(C.ar("قوم", 19) + " people", 45, TEAL, "living · 45 forms"),
         (C.ar("لقی", 19) + " meet", 33, TEAL, "living · 33 forms"),
         (C.ar("ءمن", 19) + " believe", 28, TEAL, "living · 28 forms"),
         (C.ar("ربب", 19) + " Lord", 8, CORAL, "frozen · 8"),
         (C.ar("ءله", 19) + " God", 6, CORAL, "frozen · 6 (the Name)"),
         (C.ar("وسی", 19) + " Mūsā", 1, CORAL, "frozen · 1 (proper noun)")],
        ymax=50, fmt="{:.0f}")

# ╔══════════════ 2 · HYPOTHESIS ══════════════╗
C.section("Hypothesis — roles, not ranks; and best-proportion")
C.callout("If the Qur'ān's concept-system is in احسن تقویم, three things should hold — and be measurable",
          "<b>(A) Importance is relational, not scalar.</b> Each concept's standing is its <b>role</b> in the "
          "co-occurrence network (hub · connector · specialist · unit-definer), and roles should beat a "
          "degree-matched null — otherwise ‘role’ is just frequency in disguise.<br>"
          "&nbsp;&nbsp;<b>(B) NECESSITY — cannot delete.</b> Remove a concept (or its arrangement) and the system "
          "must measurably degrade: scrambling the order should collapse the structure, and rare <b>unit-definers</b> "
          "must own their sūra above chance (FDR).<br>"
          "&nbsp;&nbsp;<b>(C) SUFFICIENCY — cannot add.</b> The system should be <b>saturated and complete</b>: a "
          "low-dimensional role-space that already explains the structure, one connected whole with no missing "
          "bridge, no empty role waiting to be filled.<br>"
          "Together (B)+(C) = <b>احسن تقویم</b>. And crucially — <b>nothing is unimportant</b>: pervasive hubs and "
          "lone unit-definers are important in <i>different registers</i>, neither reducible to the other.", accent=TEAL)

# ╔══════════════ 3 · METHOD ══════════════╗
C.section("Method & instruments")
C.callout("Three substrates, one network, two scales — all against the text's own shuffle (the One Law)",
          f"<b>Substrates (form AND content).</b> ROOT — content only ({g('root_types','—')} roots, "
          f"{g('root_tokens','—')} tokens); WORD — surface rasm form ({g('word_types','—')} words); MORPHOLOGY — "
          "distinct forms per root (from the lemma column). Diacritics excluded (human layer).<br>"
          "&nbsp;&nbsp;<b>The system.</b> A co-occurrence network: two roots linked when they share an āyah more than "
          "chance (PPMI &gt; 0). Roles are read by network cartography (within-module degree × participation).<br>"
          "&nbsp;&nbsp;<b>Criticality = knockout.</b> Remove a node, measure how much the connected whole shrinks "
          "(ΔGC) — the engineering test for ‘necessary part’.<br>"
          "&nbsp;&nbsp;<b>Two scales.</b> GLOBAL (whole Qur'ān = the network) and LOCAL (the sūra subsystem; a "
          "unit-definer ‘owns’ its sūra by a chi-square vs a length-matched shuffle, FDR-corrected).<br>"
          "&nbsp;&nbsp;<b>The One Law.</b> Every claim is scored against the text's <b>own</b> shuffle — nothing "
          "external is admitted as evidence.", accent=SLATE)

# ╔══════════════ 4 · RESULTS — network & roles ══════════════╗
C.section("Results · the system and its roles  (NETWORK)")
C.note("④ The concept-network — top 36 concepts by influence, laid out by who-occurs-with-whom. Node size = "
       "connections; colour = measured role. <b>ءله</b> sits where every region meets — the referent the whole "
       "Book wires to. This single picture is the reframe: importance is <i>position</i>, not a number.")
net(title="co-occurrence network")
roles = N.get("roles", {})
C.note("Role census of the full network (869 concepts). Most concepts are <b>peripheral specialists</b>; a small "
       "set of <b>hubs</b> and <b>connectors</b> integrate the whole — the signature of an organised system, not a heap.")
C.table(["role", "what it is (the car / body analogy)", "count"], [
    ["connector-hub", "the chassis/engine everything bolts to — ءله, قول, ربب", str(roles.get("connector-hub", "—"))],
    ["connector", "the wiring harness — bridges separate subsystems", str(roles.get("connector", "—"))],
    ["peripheral", "a specialised part — local, not load-bearing alone", str(roles.get("peripheral", "—"))],
    ["ultra-peripheral", "a leaf — appears in one tight context", str(roles.get("ultra-peripheral", "—"))],
])

# ── two-extreme scatter ──
se = g("scatter_extreme", {})
C.note("⑤ The two-extreme map — the heart of the reframe. x = GLOBAL system role (how central in the whole network); "
       "y = LOCAL ownership (how much it defines one sūra). <b>ءله</b> is far right (system hub, owns no single sūra); "
       "<b>صمد · کوثر · نحر</b> are high up (own their sūra, invisible globally). Asking ‘which is more important’ is "
       "like asking heart vs DNA — they live on different axes. Both essential; neither rankable against the other.")
if se:
    scatter(se.get("labeled", []), se.get("cloud", []), (0, 100), (0, 100),
            "GLOBAL — system centrality  (percentile)", "LOCAL — owns its sūra  (percentile)",
            kindcol={"system": CORAL, "unit": TEAL, "other": SLATE}, note_quad=True,
            legend=[("system-critical hub", CORAL), ("unit-definer", TEAL), ("supporting concept", "#B9C8D6")],
            regions=[(80, 44, "system-critical hubs →", CORAL), (26, 96, "↑ unit-definers", TEAL)])
C.note("Right (coral) = system-critical hubs · top (teal) = unit-definers · centre cloud = supporting concepts. "
       "The two clusters are the two registers of importance — pervasive vs defining.")

# ╔══════════════ 5 · NECESSITY ══════════════╗
C.section("Necessity — “cannot delete” (every part is load-bearing)")
C.note("⑥ The master deletion test. Scramble the arrangement (the One-Law shuffle) and the role structure "
       "collapses: modularity falls from its real value to chance. You <b>cannot delete the arrangement</b> "
       "without destroying the system — the order is necessary, not decorative.")
C.vbars([("designed order (real)", N.get("modularity_obs", 0.134), TEAL,
          "real role structure present — modularity 0.134"),
         ("shuffled order (null)", N.get("modularity_null", 0.043), CORAL,
          "scramble the arrangement → structure gone — modularity 0.043")],
        ymax=0.16, fmt="{:.3f}")
C.note("The gap is overwhelming: real modularity " + str(N.get("modularity_obs", "—")) + " vs shuffle " +
       str(N.get("modularity_null", "—")) + " — that is <b>z = +" + str(N.get("modularity_z", "—")) +
       "</b> above the degree-matched null. You cannot delete the arrangement without destroying the roles.")
C.note("⑦ Local necessity — unit-definers. Rare concepts that own their sūra far above chance (FDR q<0.05). Delete "
       "صمد and al-Ikhlāṣ loses its defining attribute; delete کوثر and al-Kawthar loses its name. Necessity is "
       "<b>scale-dependent</b>: globally distributed, locally razor-sharp. (ROOT and WORD substrates agree.)")
rc = g("root_conc", {}); wc = g("word_conc", {})
C.table(["concept", "gloss", "substrate", "freq", "owns sūra (q)", "necessary to its unit?"], [
    [C.ar("صمد"), "Eternal", "root+word", "1", f"{rc.get('صمد',['','',''])[2]}", "✔ al-Ikhlāṣ"],
    [C.ar("کوثر"), "abundance", "WORD only", "1", f"{wc.get('کوثر',['','',''])[2]}", "✔ al-Kawthar"],
    [C.ar("نحر"), "sacrifice", "root+word", "1", f"{rc.get('نحر',['','',''])[2]}", "✔ al-Kawthar"],
    [C.ar("کفء"), "equal", "root+word", "1", f"{rc.get('کفء',['','',''])[2]}", "✔ al-Ikhlāṣ"],
    [C.ar("لهب"), "flame", "root+word", "3", f"{rc.get('لهب',['','',''])[2]}", "✔ al-Masad"],
    [C.ar("ءلی"), "bounties (ālāʾ)", "root", "34", f"{rc.get('ءلی',['','',''])[2]}", "✔ al-Raḥmān refrain"],
])
C.note("The substrate matters (form AND content). At ROOT level <b>کوثر folds into کثر</b> (‘abundance’, common) and "
       "is lost; on the WORD substrate it re-appears as a unit-definer (q≈" + str(wc.get('کوثر', ['', '', '—'])[2]) +
       "). Conversely محمد stays <b>diffuse</b> (q≈" + str(wc.get('محمد', ['', '', '—'])[2]) + ") — referenced across "
       "sūras, owning none. Both facts are correct, and only visible because we use form and content together.")
C.note("⑧ Global criticality — knockout. Removing a hub shrinks the connected whole; ءله removes the most. But the "
       "effect is small and degree-explained (z≈" + str(N.get("hub_knockout_z", "—")) + ", within chance) — so we "
       "do NOT overclaim ‘ءله is a single point of failure’. Necessity here is <b>distributed</b>, the next chart's point.")
ko = N.get("knockout", {})
C.vbars([(C.ar(k, 19) + " " + gl(k), ko[k], (CORAL if k == "ءله" else SLATE), f"remove {k} → −{ko[k]:.1%} of the whole")
         for k in ["ءله", "قول", "کون", "ربب"] if k in ko], ymax=0.05, fmt="{:.1%}")

# ╔══════════════ 6 · SUFFICIENCY ══════════════╗
C.section("Sufficiency — “cannot add” (the system is complete & saturated)")
rc = g("robust_curve", {})
_r50 = int(rc.get("random", [0.45])[-1] * 100) if rc.get("random") else 45
_a30 = int(rc.get("attack", [0, 0.02])[-2] * 100) if rc.get("attack") else 2
_t1 = int(rc.get("top1", 0.96) * 100); _t10 = int(rc.get("top10", 0.88) * 100)
C.note("⑨ Robustness — the knockout curve (actual data, " + str(rc.get("n", "—")) + " concepts). Remove concepts "
       "and watch the largest connected piece survive. Under <b>random failure</b> (teal) the system degrades "
       "gracefully — half the concepts gone, <b>" + str(_r50) + "%</b> still connected. Under <b>targeted attack</b> "
       "(coral, most-central first) it falls far faster — yet removing the single top hub ءله leaves <b>" + str(_t1) +
       "%</b> intact, and even the top 10 leave <b>" + str(_t10) + "%</b>. Robust to accident, with <b>no single "
       "keystone</b> — redundancy without waste.")
if rc:
    curve(rc)
C.note("As area-under-curve, random failure preserves <b>" + str(rc.get("auc_random", "—")) + "</b> of the system "
       "on average vs <b>" + str(rc.get("auc_attack", "—")) + "</b> under targeted attack — the textbook signature "
       "of a <b>robust-yet-economically-wired</b> system (the same shape seen in metabolic and neural networks). "
       "The cut-node census agrees: <b>" + str(N.get("cut_obs", "—")) + "</b> breakpoints vs <b>" +
       str(N.get("cut_null", "—")) + "</b> in a degree-matched random graph (z=" + str(N.get("cut_z", "—")) +
       ") — fewer, not more. There is no missing brace to add.")
C.note("⑩ Dimensional saturation. Four importance criteria collapse onto essentially <b>two</b> axes (prominence + "
       "concentration) that hold 92% of the variance; the 3rd and 4th carry almost nothing. The description is "
       "<b>complete in 2 axes</b> — there is no third kind of importance waiting to be added.")
pv = g("pca_var", [69, 23, 6, 2])
C.vbars([("PC1 · prominence", pv[0]/100, TEAL, f"{pv[0]}% of structure"),
         ("PC2 · concentration", pv[1]/100, GOLD, f"{pv[1]}% — the orthogonal axis"),
         ("PC3", pv[2]/100, SLATE, f"{pv[2]}% — negligible"),
         ("PC4", pv[3]/100, SLATE, f"{pv[3]}% — negligible")],
        ymax=0.8, fmt="{:.0%}")
C.note("⑪ احسن تقویم, drawn. The system as a designed whole: a referent-hub, connectors, specialists and "
       "unit-definers — <b>necessary</b> on the left (cannot delete), <b>sufficient</b> on the right (cannot add).")
ahsan()

# ╔══════════════ WHAT IF — ablation test ══════════════╗
C.section("⑫ What if? — the ablation test (delete · delete · add)")
C.note("The cleanest proof of necessity + sufficiency is to intervene: <b>remove</b> a concept and watch what "
       "breaks, or <b>insert</b> one that isn't there and watch it fail to attach. Three experiments, on real data.")
C.note("WHAT IF we delete ءله (the hub)? The connector-hub (2,848×, in 86 sūras) is greyed out. The network "
       "shrinks by 3.8% — yet stays in <b>one connected piece</b>. Global necessity is real but <b>distributed</b>: "
       "no single concept is a catastrophic point of failure. The Book degrades gracefully — a designed-system trait.")
net(ko_hub="ءله", title="knockout ءله")
C.table(["WHAT IF…", "what happens (measured)", "scale", "what it proves"], [
    ["✂ delete ءله (hub)", "whole shrinks 3.8% (ΔGC=0.038) but stays ONE piece — degree-explained, robust",
     "GLOBAL", "necessity is real but distributed (no single collapse)"],
    ["✂ delete صمد (unit-definer)", "0 effect on the network; al-Ikhlāṣ loses 1 of its only 2 exclusive definers "
     "(صمد · کفء) — the sūra's defining attribute ‘Eternal’ is gone", "LOCAL", "necessity is razor-sharp at the unit scale"],
    ["➕ add a root NOT in the Qur'ān", "frequency 0 → 0 co-occurrences → an isolated node, no role, outside the "
     "whole — nowhere to attach", "—", "SUFFICIENCY: there is no empty slot to fill"],
])
C.note("al-Ikhlāṣ in full (10 root-tokens): " + " · ".join(C.ar(t, 17) for t in
       ["قول", "ءله", "وحد", "صمد", "ولد", "کون", "کفء"]) + ". Two of these (صمد ‘Eternal’, کفء ‘equal’) occur almost "
       "nowhere else — delete either and the sūra that the Prophet called ‘a third of the Qur'ān’ loses the very "
       "attribute that defines it. That is necessity you can feel.")
C.callout("The ablation verdict — احسن تقویم, experimentally",
          "<b>Delete a hub</b> → the web thins but holds (global, distributed necessity). <b>Delete a unit-definer</b> "
          "→ a whole sūra loses its identity (local, sharp necessity). <b>Add a foreign concept</b> → it floats "
          "unconnected, with no role to play (sufficiency). Every direction you push, the system resists: "
          "<b>nothing can be deleted because it is necessary; nothing can be added because it is sufficient</b> — "
          "each thing already in its place, " + C.ar("نیکو", 17) + ".", accent=TEAL)

# ╔══════════════ GATING ══════════════╗
C.section("Gating chain — from a naive ranking to a validated role-map")
C.para("<b>Naive</b> — ‘most important = most frequent’: ءله, قول, کون… <b>Control 1 · collinearity</b> — frequency, "
       "spread and morphology correlate 0.79–0.94; they are one axis, so the ranking is not three witnesses but one. "
       "<b>Control 2 · unique information</b> — credited for non-redundant signal, frequency is " + f"{w[0]}%" +
       "; concentration " + f"{w[3]}%" + ". <b>Control 3 · the reframe</b> — model importance as network roles; the "
       "role structure beats a degree-matched null at z=+" + str(N.get("modularity_z", "—")) + " (real, not "
       "frequency in disguise). <b>Control 4 · necessity</b> — shuffle collapses the structure; "
       + str(g("root_sig", "—")) + " root + " + str(g("word_sig", "—")) + " word unit-definers own their sūra at "
       "FDR q<0.05. <b>Control 5 · sufficiency</b> — 2 axes hold 92%, the graph is one connected whole, robust "
       "beyond chance. <b>Honest demotion</b> — hub knockout-criticality is degree-explained (z=+" +
       str(N.get("hub_knockout_z", "—")) + "), so we keep ‘role structure’ and ‘robustness’, and drop ‘ءله is a "
       "single point of failure’.")

# ╔══════════════ INTERPRETATION ══════════════╗
C.section("Interpretation")
C.para("<b>The reframe is the result.</b> A linear ranking is not merely crude — it is <b>provably lossy</b>: it "
       "lives on one axis (PC1) and discards the orthogonal " + f"{pv[1]}%" + " (PC2) where the unit-definers live. "
       "So ‘which concept is most important’ has no single answer, the way ‘is the heart or the DNA more important’ "
       "has none — they are different roles at different scales. Replacing the ladder with a <b>network of roles</b> "
       "is what makes the question well-posed.<br><br>"
       "<b>احسن تقویم, operationalised.</b> Best-proportion becomes two measurements. <b>Necessity</b> (cannot "
       "delete): scrambling the order collapses the structure (modularity → chance), and every sūra has rare "
       "concepts that necessarily define it (FDR-significant) — at the local scale, sharp; at the global scale, "
       "distributed across a robust web. <b>Sufficiency</b> (cannot add): the importance-space is saturated in two "
       "axes, the network is a single connected whole, and it carries fewer breakpoints than chance — there is no "
       "empty role to fill, no missing brace. The Book is <b>neither padded nor deficient</b>.<br><br>"
       "<b>Nothing is unimportant — but not equally, and not on one ruler.</b> ءله is the referent-hub the whole "
       "system wires to; صمد is the lone attribute that defines a single sūra; قوم is a living, generative concept; "
       "موسى is a frozen proper-noun carried across narratives. Form (surface, morphology) and content (root) each "
       "reveal a role the other hides. The system uses <b>all</b> of them — which is exactly what aḥsan taqwīm "
       "predicts.")

# ╔══════════════ CAVEATS ══════════════╗
C.section("Caveats & confounds")
C.para("<b>What we do NOT claim.</b> (1) Hub knockout-criticality is <b>degree-explained</b> (z=+" +
       str(N.get("hub_knockout_z", "—")) + "): ءله fragments the network most, but no more than its connectivity "
       "predicts — we do not call it a designed single-point-of-failure. The beyond-null claims are the <b>role "
       "structure</b> (z=+" + str(N.get("modularity_z", "—")) + ") and <b>robustness</b> (z=" +
       str(N.get("cut_z", "—")) + ").<br>"
       "&nbsp;&nbsp;(2) <b>Sufficiency is partially operationalised</b> — saturation, completeness and robustness "
       "are real proxies for ‘cannot add’, but ‘sufficiency’ in full is a stronger claim than any finite test "
       "settles.<br>"
       "&nbsp;&nbsp;(3) <b>Structural ≠ semantic.</b> The method measures structural roles; the <i>theological</i> "
       "weight of a concept (why صمد is supreme as a Name of God) is <b>meaning</b>, which is not in the token "
       "distribution and is inadmissible under the One Law. We flag this boundary rather than fake a number across "
       "it.<br>"
       "&nbsp;&nbsp;(4) <b>Grade.</b> CANDIDATE (72), not discovery-tier: the reframe and its null-validations are "
       "solid; promotion needs the per-node knockout null and a weighted-network community null (G9).")

# ╔══════════════ VERDICT ══════════════╗
C.section("Verdict")
C.verdict("CANDIDATE",
          "The linear ‘importance ranking’ is the wrong shape — it is one axis and discards the orthogonal " +
          f"{pv[1]}%" + " where unit-definers live. Replacing it with <b>roles in a co-occurrence network</b> is "
          "defensible and null-validated: the role structure beats degree-chance (z=+" +
          str(N.get("modularity_z", "—")) + "), the system is necessary (shuffle collapses it; " +
          str(g("root_sig", "—")) + "/" + str(g("word_sig", "—")) + " unit-definers own their sūra) and sufficient "
          "(2 axes = 92%, one robust connected whole) — an operational reading of <b>احسن تقویم</b>. Form and "
          "content together; nothing unimportant.",
          "~85% the reframe (roles>ranking) is correct; ~72% the full necessity+sufficiency claim",
          "if a single axis is shown to subsume the others (a true total order on the rasm) — not seen (concentration ⟂, ρ≈0.2)",
          "per-node knockout null + weighted-community null clearing FDR would raise it toward discovery-tier")

# ╔══════════════ PATH FORWARD ══════════════╗
C.section("The path forward — ranked by decisiveness")
C.note("Grounded in what was measured; probabilities INFERRED over MEASURED bases.")
C.table(["#", "Move — grounded & testable", "Built on (MEASURED)", "P→settle"], tight=False, rows=[
    ["1", "Per-node knockout vs configuration-model null (every node, not just hubs)", "hub z=+2.3 within chance; need full distribution", "0.80"],
    ["2", "Weighted-network community null (is modularity z robust to edge weights?)", "modularity z=+34.9 on unweighted", "0.74"],
    ["3", "Run the whole pipeline on the WORD + MORPHOLOGY networks, not just ROOT", "کوثر recovered only on WORD substrate", "0.70"],
    ["4", "Formalise ‘sufficiency’ — does adding a synthetic concept ever improve modularity/coverage?", "2-axis saturation + 99.8% giant component", "0.55"],
    ["5", "Cross-arrangement: do roles persist under revelation order (DIVINE-ALT)?", "roles measured on muṣḥaf order only", "0.50"],
])
C.vbars([("① per-node knockout null", 0.80, TEAL, "settles whether criticality beats degree"),
         ("② weighted-community null", 0.74, TEAL, "hardens the role-structure claim"),
         ("③ word + morphology networks", 0.70, TEAL, "form-substrate roles"),
         ("④ formalise sufficiency", 0.55, GOLD, "the harder half of aḥsan taqwīm"),
         ("⑤ revelation-order roles", 0.50, GOLD, "DIVINE-ALT arrangement")],
        ymax=1.0, fmt="{:.0%}")
C.callout("The recommendation",
          "Run <b>#1</b> — the per-node knockout null — first; it is the verdict's own ‘flip’ test and decides "
          "whether any criticality claim survives beyond degree. Pair with <b>#3</b> so the form substrates (word, "
          "morphology) get their own role-maps, since کوثر already proved a definer is invisible on content alone.",
          accent=TEAL)

# ╔══════════════ REFLECTION ══════════════╗
C.section("Reflection")
C.para("The instinct to rank is strong — we want a single ‘most important word’. But the data kept refusing the "
       "ladder: every time a scalar was forced, it put a hapax above the Name (بتر &gt; ءله) or a verb above it "
       "(قوم &gt; ءله). That is not a bug to tune away; it is the finding. Importance is not one quantity.<br><br>"
       "What replaced it is humbler and sturdier: <b>ask what each part does</b>. A bolt, oil, a tyre, a headlight — "
       "you do not rank them, you ask which role each plays and what fails without it. The Qur'ān's concepts behave "
       "the same way, and — measured against the text's own shuffle — they form a system that is hard to break and "
       "has no slack to add. That is what <b>احسن تقویم</b> means when you make it count.<br><br>"
       "Ḥāfeẓ said it long before the network was drawn: <b>" + C.ar("هر چیزی به جای خویش نیکوست", 17) + "</b> — "
       "<i>each thing is beautiful in its own place</i>. Not ranked above or below — <b>placed</b>. The ablation "
       "test is only the empirical echo of that line: move a thing out of its place, and the beauty (the function) "
       "is lost.")

# ╔══════════════ SUMMARY ══════════════╗
C.section("Summary — what holds")
pair_table("✔ Holds (measured)", "✗ Does not / not claimed", [
    ["importance is ≥2-D — a linear ranking discards " + f"{pv[1]}%" + " (PC2)", "‘ءله is a single point of failure’ (degree-explained, z=+2.3)"],
    ["role structure beats degree-null (z=+" + str(N.get("modularity_z", "—")) + ")", "a single scalar ‘importance’ that ranks صمد vs ءله"],
    ["necessity: shuffle collapse + " + str(g("root_sig", "—")) + "/" + str(g("word_sig", "—")) + " unit-definers", "theological weight (semantic — out of substrate)"],
    ["sufficiency: 2 axes = 92%, robust, one connected whole", "full ‘sufficiency’ proof (only partially operationalised)"],
    ["form AND content both required (کوثر needs the WORD substrate)", "frequency as evidence (only " + f"{w[0]}%" + " unique information)"],
])

# ╔══════════════ LESSONS ══════════════╗
C.section("Lessons learned")
pair_table("Principle", "What it caught here", [
    ["Check if your ‘criteria’ are independent first", "freq / spread / morphology are one axis (0.79–0.94)"],
    ["Credit unique information, not raw size", "frequency = " + f"{w[0]}%" + " unique; concentration = " + f"{w[3]}%"],
    ["When a scalar misbehaves, the order may be partial", "every forced ranking put a hapax/verb above ءله"],
    ["Reframe linear → network when structure is relational", "roles beat the degree-null (z = +" + str(N.get("modularity_z", "—")) + ")"],
    ["Use form AND content together", "کوثر invisible on root, recovered on the word substrate"],
    ["Demote what the null explains", "hub criticality is degree-explained — dropped"],
], c1=SLATE, c2=INK)

# ╔══════════════ TAKEAWAY ══════════════╗
C.section("Takeaway")
C.callout("In one line",
          "Don't ask <b>which</b> Qur'ānic concept is most important — that is the wrong shape of question. Ask "
          "<b>what role</b> each plays in the network: a few hubs integrate the whole, many specialists define their "
          "place, and — measured against the text's own shuffle — <b>nothing can be deleted (necessary) and nothing "
          "added (sufficient)</b>. That is احسن تقویم, made testable.", accent=TEAL)

# ╔══════════════ PERSIAN ABSTRACT ══════════════╗
C.section("خلاصهٔ کامل — Persian abstract")
st.markdown(
    "<div dir='rtl' id='im-fa' style='font-family:Vazirmatn,Tahoma,\"Segoe UI\",sans-serif;font-size:15px;"
    "line-height:1.85;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #138A74;"
    "border-radius:11px;padding:16px 20px'>"
    "<b>۱) مسئله.</b> پرسشِ آشنای «کدام مفهوم در قرآن مهم‌تر است؟» دو فرضِ پنهان دارد: نخست آنکه اهمیت یک "
    "<b>نردبانِ خطی</b> (ترتیبِ یک‌بُعدی) است، و دوم آنکه پلهٔ این نردبان را <b>بسامد</b> (شمارِ تکرار) تعیین می‌کند. "
    "هر دو فرض بر دادهٔ متن مردود می‌شوند، و نشان دادنِ همین نادرستی و جایگزینیِ آن، جانِ این بررسی است.<br><br>"
    "<b>۲) چرا بسامد کافی نیست.</b> بسامد، گستره (شمارِ سوره‌ها) و تنوعِ صرفی تقریباً <b>یک محور</b>اند (همبستگیِ "
    "۰٫۷۹ تا ۰٫۹۴)؛ پس فهرستِ مشهورِ «پرتکرارترین واژه‌ها» سه شاهد نیست، یک شاهد است که سه بار تکرار شده. وقتی هر "
    "معیار را تنها برای اطلاعِ <b>یکتای</b> خود (آنچه دیگران نمی‌گویند) ارزش‌گذاری کنیم، سهمِ بسامد تنها " +
    f"{w[0]}" + "٪، صرف ۲۲٪، گستره ۸٪، و <b>تمرکز</b> (در تملک داشتنِ یک جای‌گاه) ۶۳٪ است. یعنی بلندترین سیگنال، "
    "کم‌اطلاع‌ترین است.<br><br>"
    "<b>۳) صورت و محتوا — هر سه بستر.</b> بر <b>رسم</b> (بی‌حرکت؛ حرکات لایهٔ بشری و کنار گذاشته می‌شود) سه بستر را "
    "با هم به کار می‌بریم: <b>ریشه</b> (محتوا؛ " + str(g("root_types", "—")) + " ریشه)، <b>واژهٔ رسمی</b> (صورت؛ " +
    str(g("word_types", "—")) + " واژه) و <b>صرف</b> (شمارِ صورت‌های هر ریشه). صورت و محتوا یکدیگر را آشکار می‌کنند؛ "
    "هیچ‌یک به‌تنهایی بسنده نیست.<br><br>"
    "<b>۴) بازقالب‌بندی به شبکه (هستهٔ کار).</b> به‌جای رتبه‌بندی می‌پرسیم هر مفهوم چه <b>نقشی</b> در شبکهٔ هم‌آییِ "
    "واژگان دارد (دو ریشه به‌هم پیوند می‌خورند اگر بیش از شانس در یک آیه بیایند، PPMI&gt;۰). نقش‌ها با کارتوگرافیِ "
    "شبکه خوانده می‌شوند: <b>اَبَرگرهِ رابط</b> (ءله، قول، ربب — شاسیِ نظام)، <b>رابط</b> (پلِ زیرسامانه‌ها)، "
    "<b>متخصص</b>، و <b>تعریف‌گرِ واحد</b>. ساختارِ نقش‌ها در برابرِ نُلِ هم‌درجه <b>واقعی</b> است (z=+" +
    str(N.get("modularity_z", "—")) + "): پس «نقش» همان بسامد در لباسِ مبدل نیست.<br><br>"
    "<b>۵) دو مقیاس — جهانی تا محلی.</b> اهمیت در دو تراز سنجیده می‌شود: <b>جهانی</b> (کلِ قرآن = شبکه) و "
    "<b>محلی</b> (زیرسامانهٔ سوره؛ یک تعریف‌گر سورهٔ خود را با کای‌دو در برابرِ شافلِ هم‌طول، با تصحیحِ FDR، «در "
    "تملک» دارد). یک مفهوم می‌تواند در یک تراز کلیدی و در دیگری حاشیه‌ای باشد.<br><br>"
    "<b>۶) ضرورت — «نمی‌توان کاست».</b> آزمونِ مادرِ حذف: برهم‌زدنِ ترتیب (شافلِ قانونِ یگانه) ساختارِ نقش را "
    "فرومی‌پاشد — مدولاریتی از " + str(N.get("modularity_obs", "—")) + " به " + str(N.get("modularity_null", "—")) +
    " سقوط می‌کند (z=+" + str(N.get("modularity_z", "—")) + "). و در تراز محلی، " + str(g("root_sig", "—")) +
    " ریشه و " + str(g("word_sig", "—")) + " واژه سورهٔ خود را بالاتر از شانس در تملک دارند (صمد، کوثر، نحر، کفء، "
    "لهب، آلاء…). ضرورت <b>مقیاس‌وابسته</b> است: محلی تیز، جهانی توزیع‌شده.<br><br>"
    "<b>۷) آزمونِ «چه می‌شود اگر؟».</b> <b>حذفِ ءله</b> (اَبَرگره): شبکه ۳٫۸٪ کوچک می‌شود اما <b>یک‌پارچه</b> "
    "می‌ماند — ضرورتِ توزیع‌شده و تاب‌آور، نه نقطهٔ شکستِ یگانه. <b>حذفِ صمد</b>: بر شبکه بی‌اثر است، اما سورهٔ "
    "اخلاص یکی از تنها دو تعریف‌گرِ انحصاری‌اش (صمد، کفء) را از دست می‌دهد — ضرورتِ محلیِ تیز. <b>افزودنِ ریشه‌ای "
    "که در قرآن نیست</b>: بسامدِ صفر ← بی هیچ هم‌آیی ← گرهِ منفرد و بی‌نقش، بیرون از کل — هیچ جایی برای افزودن نیست "
    "(کفایت).<br><br>"
    "<b>۸) کفایت — «نمی‌توان افزود».</b> فضای اهمیت <b>اشباع</b> است: دو محور (برجستگی + تمرکز) ۹۲٪ ساختار را نگه "
    "می‌دارند و محورِ سوم و چهارم تقریباً هیچ. شبکه <b>یک‌پارچه</b> است (۹۹٫۸٪ در یک مؤلفه)، و از گرافِ تصادفیِ "
    "هم‌درجه <b>کم‌شکاف‌تر</b> (z=" + str(N.get("cut_z", "—")) + ") — یعنی برای فروپاشی ساخته نشده و افزونگیِ "
    "بی‌اسراف دارد. نه جای خالیِ نقشی هست و نه مهارِ گم‌شده‌ای.<br><br>"
    "<b>۹) احسن تقویم.</b> این همان «بهترین تناسب» (تین ۹۵:۴) است که عملیاتی شده: <b>نه می‌توان افزود چون بسنده "
    "است، نه کاست چون لازم است</b>. حافظ پیش از آنکه شبکه رسم شود گفت: <b>«جهان چون خط و خال و چشم و ابروست / که "
    "هر چیزی به جای خویش نیکوست»</b> — اهمیت رتبه نیست، <b>بودن در جای خود</b> (نقش) است؛ و آزمونِ حذف، پژواکِ "
    "تجربیِ همان مصراع است: چیزی را از جایش بردار، نیکویی (کارکرد) از میان می‌رود.<br><br>"
    "<b>۱۰) انصاف و حدود (آنچه ادعا نمی‌کنیم).</b> بحرانی‌بودنِ اَبَرگره با <b>درجه</b> توضیح داده می‌شود (z=+" +
    str(N.get("hub_knockout_z", "—")) + "، در محدودهٔ شانس)؛ پس ادعای «ءله نقطهٔ شکستِ یگانهٔ طراحی‌شده» را "
    "وامی‌نهیم — ادعاهای فراتر از نُل تنها <b>ساختارِ نقش</b> و <b>تاب‌آوری</b>اند. و <b>ساختاری ≠ معنایی</b>: وزنِ "
    "کلامیِ صمد (نامِ خداوند) <b>معنا</b>ست، نه آماری توزیعی، و طبقِ قانونِ یگانه به‌عنوان شاهد نامقبول است؛ این مرز "
    "را علامت می‌زنیم، نه آنکه عددی بر آن بسازیم.<br><br>"
    "<b>۱۱) نتیجه و درجه.</b> داوری <b>ساختاری و روش‌شناختی</b> است، نه کلامی: <b>نامزد (درجهٔ ۷۲)</b> — بازقالب‌بندی "
    "و نُل‌هایش استوارند، اما ارتقا به ترازِ کشف نیازمندِ نُلِ حذفِ تک‌گرهی و نُلِ جامعهٔ وزنی است.<br><br>"
    "<b>۱۲) راهِ پیش‌رو (به‌ترتیبِ قطعیت).</b> ۱) نُلِ حذفِ تک‌گرهی برای هر گره؛ ۲) نُلِ جامعهٔ شبکهٔ وزنی؛ ۳) "
    "اجرای کلِ خط‌لوله بر شبکهٔ <b>واژه و صرف</b> (نه فقط ریشه)؛ ۴) صورت‌بندیِ دقیقِ «کفایت»؛ ۵) پایداریِ نقش‌ها در "
    "<b>ترتیبِ نزول</b> (آرایشِ الهیِ بدیل).<br><br>"
    "<b>درس.</b> پیش از رتبه‌بندی، استقلالِ معیارها را بسنج؛ اطلاعِ یکتا را ارزش بنه نه حجمِ خام؛ هرگاه نردبان "
    "بدرفتاری کرد، شاید ترتیب <b>جزئی</b> باشد؛ صورت و محتوا را با هم به کار بر؛ و آنچه را نُل توضیح می‌دهد، "
    "فروبکاه.</div>", unsafe_allow_html=True)

# ╔══════════════ ARABIC ABSTRACT ══════════════╗
C.section("الملخّص الكامل — Arabic abstract")
st.markdown(
    "<div dir='rtl' id='im-ar' style='font-family:Amiri,\"Scheherazade New\",Tahoma,serif;font-size:15.5px;"
    "line-height:1.9;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;"
    "border-radius:11px;padding:16px 20px'>"
    "<b>١) المسألة.</b> السؤالُ المألوف «أيُّ مفهومٍ أهمُّ في القرآن؟» يخفي فرضين: أوّلًا أنّ الأهمية <b>سُلَّمٌ "
    "خطّيّ</b> (ترتيبٌ أحاديُّ البُعد)، وثانيًا أنّ دَرَجتَه <b>التكرار</b>. والبياناتُ تردُّ الفرضين، وبيانُ ذلك "
    "واستبدالُه هو جوهرُ هذه المراجعة.<br><br>"
    "<b>٢) لماذا لا يكفي التكرار.</b> التكرارُ والانتشارُ (عددُ السور) والثراءُ الصرفيُّ <b>محورٌ واحد</b> (ارتباط "
    "٠٫٧٩–٠٫٩٤)؛ فقائمةُ «أكثر الكلمات تكرارًا» ليست ثلاثةَ شهودٍ بل شاهدٌ واحدٌ مكرَّرٌ ثلاثًا. وإذا كافأنا كلَّ "
    "معيارٍ على معلومته <b>الفريدة</b> فقط، كان نصيبُ التكرار " + f"{w[0]}" + "٪، والصرفِ ٢٢٪، والانتشارِ ٨٪، "
    "و<b>التركيزِ</b> (تملُّكِ موضعٍ) ٦٣٪. فأعلى إشارةٍ هي أقلُّها إفادةً.<br><br>"
    "<b>٣) الصورة والمضمون — ثلاثة أُسُس.</b> على <b>الرسم</b> (بلا حركات؛ الحركاتُ طبقةٌ بشرية مُستبعَدة) نستعمل "
    "ثلاثةَ أُسُسٍ معًا: <b>الجذر</b> (مضمون؛ " + str(g("root_types", "—")) + " جذرًا)، و<b>الكلمة الرسمية</b> "
    "(صورة؛ " + str(g("word_types", "—")) + " كلمة)، و<b>الصرف</b> (عددُ صيغ كلِّ جذر). الصورةُ والمضمونُ يكشف "
    "أحدُهما ما يخفيه الآخر؛ ولا يكفي واحدٌ وحدَه.<br><br>"
    "<b>٤) إعادة التأطير إلى شبكة (الجوهر).</b> بدل الترتيب نسأل عن <b>الدور</b> في شبكة التلازم (جذران يُوصَلان إن "
    "تلازما في آيةٍ فوق الصدفة، PPMI&gt;٠). وتُقرأ الأدوارُ بكارتوغرافيا الشبكة: <b>محورٌ جامع</b> (ءله، قول، ربب — "
    "هيكلُ النظام)، و<b>واصلٌ</b> (جسرُ الأنظمة الفرعية)، و<b>متخصّصٌ</b>، و<b>مُعرِّفٌ للوحدة</b>. وبنيةُ الأدوار "
    "<b>حقيقيةٌ</b> تتجاوز نُلَّ الدرجات (z=+" + str(N.get("modularity_z", "—")) + ")؛ فالدورُ ليس تكرارًا متنكِّرًا.<br><br>"
    "<b>٥) مقياسان — من العامّ إلى الخاصّ.</b> تُقاس الأهمية في مستويين: <b>عامّ</b> (القرآن كلُّه = الشبكة) "
    "و<b>محلّيّ</b> (نظامُ السورة الفرعيّ؛ يَملِك المُعرِّفُ سورتَه بمربّع كاي مقابل خلطٍ مُطابِقٍ للطول، مع تصحيح "
    "FDR). وقد يكون المفهومُ محوريًّا في مستوًى هامشيًّا في الآخر.<br><br>"
    "<b>٦) الضرورة — «تعذّر الحذف».</b> اختبارُ الحذف الأكبر: خلطُ الترتيب (خلطُ القانون الواحد) يُسقِط بنيةَ الدور — "
    "تهبط النمطيّةُ من " + str(N.get("modularity_obs", "—")) + " إلى " + str(N.get("modularity_null", "—")) +
    " (z=+" + str(N.get("modularity_z", "—")) + "). وفي المستوى المحلّيّ يَملِك " + str(g("root_sig", "—")) +
    " جذرًا و" + str(g("word_sig", "—")) + " كلمةً سورتَها فوق الصدفة (صمد، كوثر، نحر، كفء، لهب، آلاء…). والضرورةُ "
    "<b>تابعةٌ للمقياس</b>: محلّيًّا حادّة، عامًّا موزَّعة.<br><br>"
    "<b>٧) اختبار «ماذا لو؟».</b> <b>حذفُ ءله</b> (المحور الجامع): تنكمش الشبكةُ ٣٫٨٪ لكنّها تبقى <b>قطعةً واحدة</b> "
    "— ضرورةٌ موزَّعةٌ صامدة، لا نقطةَ انهيارٍ وحيدة. <b>حذفُ صمد</b>: لا أثرَ على الشبكة، لكنّ سورةَ الإخلاص تفقد "
    "أحدَ مُعرِّفَيها الحصريَّين (صمد، كفء) — ضرورةٌ محلّيةٌ حادّة. <b>إضافةُ جذرٍ ليس في القرآن</b>: تكرارُه صفرٌ ← "
    "بلا تلازمٍ ← عُقدةٌ معزولةٌ بلا دور، خارج الكلّ — لا موضعَ للإضافة (الكفاية).<br><br>"
    "<b>٨) الكفاية — «تعذّر الزيادة».</b> فضاءُ الأهمية <b>مُشبَع</b>: محوران (البروز + التركيز) يحملان ٩٢٪ من "
    "البنية، والثالثُ والرابعُ لا يكادان يحملان شيئًا. والشبكةُ <b>كلٌّ موصولٌ</b> (٩٩٫٨٪ في مكوِّنٍ واحد)، "
    "و<b>أقلُّ تصدُّعًا</b> من رسمٍ عشوائيٍّ مطابقِ الدرجات (z=" + str(N.get("cut_z", "—")) + ") — مبنيٌّ على ألّا "
    "ينهار، بفائضٍ بلا إسراف. فلا دورَ شاغرٌ ولا دعامةٌ مفقودة.<br><br>"
    "<b>٩) أحسن تقويم.</b> هذا هو «أحسن التناسب» (التين ٩٥:٤) مُفعَّلًا: <b>لا يُزاد لأنّه كافٍ، ولا يُنقَص لأنّه "
    "ضروريّ</b>. قال حافظٌ قبل أن تُرسَم الشبكة: <b>«جهان چون خط و خال و چشم و ابروست / که هر چیزی به جای خویش "
    "نیکوست»</b> — «كلُّ شيءٍ حَسَنٌ في موضعه»؛ فالأهميةُ ليست رتبةً بل <b>وجودًا في الموضع</b> (الدور)، واختبارُ "
    "الحذف صدًى تجريبيٌّ للبيت: انزِع شيئًا عن موضعه يَزُلِ الحُسن (الوظيفة).<br><br>"
    "<b>١٠) إنصافٌ وحدودٌ (ما لا نَدّعيه).</b> حَرِجِيّةُ المحور الجامع تفسّرها <b>الدرجةُ</b> (z=+" +
    str(N.get("hub_knockout_z", "—")) + "، ضمن الصدفة)؛ فنترك دعوى «ءله نقطةُ انهيارٍ مُصمَّمة» — والادّعاءاتُ "
    "المتجاوزةُ للنُلِّ هي <b>بنيةُ الدور</b> و<b>المتانة</b> فقط. و<b>البنيويُّ ≠ الدلاليّ</b>: الثقلُ اللاهوتيُّ "
    "لصمد (اسمٌ من أسماء الله) <b>معنًى</b> لا إحصاءٌ توزيعيّ، وهو غيرُ مقبولٍ شاهدًا بمقتضى القانون الواحد؛ نُعلِّم "
    "هذا الحدَّ ولا نصطنع عليه رقمًا.<br><br>"
    "<b>١١) النتيجة والدرجة.</b> حكمٌ <b>بنيويٌّ منهجيّ</b> لا لاهوتيّ: <b>مُرشَّح (الدرجة ٧٢)</b> — إعادةُ التأطير "
    "ونُلُّها متينة، لكنّ الترقيةَ إلى رتبة الاكتشاف تستلزم نُلَّ الحذف لكلِّ عُقدة ونُلَّ المجتمع الموزون.<br><br>"
    "<b>١٢) سبيلُ المضيّ (بترتيب الحسم).</b> ١) نُلُّ الحذف لكلِّ عُقدة؛ ٢) نُلُّ مجتمعِ الشبكة الموزونة؛ ٣) إجراءُ "
    "كامل المسار على شبكتَي <b>الكلمة والصرف</b> لا الجذر وحدَه؛ ٤) صياغةُ «الكفاية» صياغةً دقيقة؛ ٥) ثباتُ الأدوار "
    "في <b>ترتيب النزول</b> (ترتيبٌ إلهيٌّ بديل).<br><br>"
    "<b>الدرس.</b> تحقَّقْ أوّلًا من استقلال معاييرك؛ وكافِئِ المعلومةَ الفريدة لا الحجمَ الخامَّ؛ وإذا ساء السُّلَّمُ "
    "فقد يكون الترتيبُ <b>جزئيًّا</b>؛ واستعمِلِ الصورةَ والمضمونَ معًا؛ وأنزِلْ ما يفسّره النُّلُّ.</div>",
    unsafe_allow_html=True)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
# end of close-up · importance reframed
