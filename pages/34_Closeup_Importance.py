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
def scatter(pts, cloud, xr, yr, xlab, ylab, regline=None, kindcol=None, arabic=True, note_quad=None):
    W, H, L, B, Tp, Rr = 1000, 560, 76, 64, 36, 26
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
    for row in pts:
        lab, cx, cy = row[0], row[1], row[2]; kind = row[3] if len(row) > 3 else "other"
        col = kc.get(kind, SLATE) if isinstance(kind, str) else SLATE
        p.append(f"<circle cx='{X(cx):.1f}' cy='{Y(cy):.1f}' r='5.5' fill='{col}' stroke='#fff' stroke-width='1.4'/>")
        if arabic:
            p.append(f"<text x='{X(cx)+8:.1f}' y='{Y(cy)+4:.1f}' font-family='Amiri,serif' font-size='14' "
                     f"font-weight='700' fill='{INK}'>{lab}</text>")
        else:
            p.append(f"<text x='{X(cx)+7:.1f}' y='{Y(cy)+4:.1f}' font-size='12.5' fill='{INK}'>{lab}</text>")
    p.append(f"<text x='{L+pw/2:.0f}' y='{H-6}' text-anchor='middle' font-size='13.5' font-weight='700' fill='{INK}'>{xlab}</text>")
    p.append(f"<text x='18' y='{Tp+ph/2:.0f}' transform='rotate(-90 18,{Tp+ph/2:.0f})' text-anchor='middle' "
             f"font-size='13.5' font-weight='700' fill='{INK}'>{ylab}</text>")
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)


# ════════ custom schematic: احسن تقویم — necessity + sufficiency ════════
def ahsan():
    W, H = 1000, 360
    cx, cy = 500, 185
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>"]
    # ring of roles around a hub
    import math as _m
    ring = [("referent\n(hub)", CORAL, 0), ("connector", TEAL, 60), ("connector", TEAL, 120),
            ("specialist", SLATE, 180), ("unit-definer", GOLD, 240), ("specialist", SLATE, 300)]
    pos = []
    for i, (lab, col, ang) in enumerate(ring):
        a = _m.radians(ang); x = cx + 165 * _m.cos(a); y = cy + 120 * _m.sin(a); pos.append((x, y, lab, col))
    # edges hub->all + a few cross
    hub = pos[0]
    for x, y, lab, col in pos[1:]:
        p.append(f"<line x1='{hub[0]:.0f}' y1='{hub[1]:.0f}' x2='{x:.0f}' y2='{y:.0f}' stroke='#9FB4C8' stroke-width='1.5'/>")
    for a, b in [(1, 2), (2, 3), (4, 5), (3, 4), (5, 1)]:
        p.append(f"<line x1='{pos[a][0]:.0f}' y1='{pos[a][1]:.0f}' x2='{pos[b][0]:.0f}' y2='{pos[b][1]:.0f}' "
                 f"stroke='#C4D2DF' stroke-width='1'/>")
    for x, y, lab, col in pos:
        r = 30 if "hub" in lab else 21
        p.append(f"<circle cx='{x:.0f}' cy='{y:.0f}' r='{r}' fill='{col}' stroke='#fff' stroke-width='2'/>")
        parts = lab.split("\n")
        yoff = -7 if len(parts) > 1 else 0
        for k, ln in enumerate(parts):
            yy = y + 4 + 14 * k + yoff
            p.append(f"<text x='{x:.0f}' y='{yy:.0f}' text-anchor='middle' "
                     f"font-size='12.5' font-weight='700' fill='#fff'>{ln}</text>")
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
    scatter(mpts, sm.get("cloud", []), (0, 3.5), (0, 1.8),
            "log10 frequency  →  (how often)", "log10 (forms)  →  (how many shapes)",
            regline=(sm.get("slope"), sm.get("intercept")),
            kindcol={"living": TEAL, "frozen": CORAL})
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
            kindcol={"system": CORAL, "unit": TEAL, "other": SLATE}, note_quad=True)
C.note("Right (coral) = system-critical hubs · top (teal) = unit-definers · centre cloud = supporting concepts. "
       "The two clusters are the two registers of importance — pervasive vs defining.")

# ╔══════════════ 5 · NECESSITY ══════════════╗
C.section("Necessity — “cannot delete” (every part is load-bearing)")
C.note("⑥ The master deletion test. Scramble the arrangement (the One-Law shuffle) and the role structure "
       "collapses: modularity falls from its real value to chance. You <b>cannot delete the arrangement</b> "
       "without destroying the system — the order is necessary, not decorative.")
C.cascade([("designed order", f"{N.get('modularity_obs','—')}", N.get("modularity_z", 0), True),
           ("shuffle order", f"{N.get('modularity_null','—')}", 0.2, False)], zmax=40)
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
C.note("⑨ Robustness — fewer breakpoints than chance. The real network has " + str(N.get("cut_obs", "—")) +
       " cut-nodes vs " + str(N.get("cut_null", "—")) + " in a degree-matched random graph (z=" +
       str(N.get("cut_z", "—")) + "). It is built <b>not to fall apart</b> — redundancy without waste. There is no "
       "missing brace to add.")
C.scale("random graph", N.get("cut_null", 50), "Qur'ān network", N.get("cut_obs", 38), "fragile ← more cut-nodes", 60)
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
C.table(["✔ Holds (measured)", "✗ Does not / not claimed"], tight=False, rows=[
    ["importance is ≥2-D — a linear ranking discards " + f"{pv[1]}%" + " (PC2)", "‘ءله is a single point of failure’ (degree-explained, z=+2.3)"],
    ["role structure beats degree-null (z=+" + str(N.get("modularity_z", "—")) + ")", "a single scalar ‘importance’ that ranks صمد vs ءله"],
    ["necessity: shuffle collapse + " + str(g("root_sig", "—")) + "/" + str(g("word_sig", "—")) + " unit-definers", "theological weight (semantic — out of substrate)"],
    ["sufficiency: 2 axes=92%, robust, one whole", "full ‘sufficiency’ proof (partially operationalised)"],
    ["form AND content both required (کوثر needs WORD)", "frequency as evidence (only " + f"{w[0]}%" + " unique)"],
])

# ╔══════════════ LESSONS ══════════════╗
C.section("Lessons learned")
C.table(["Principle", "What it caught here"], tight=False, rows=[
    ["Check if your ‘criteria’ are independent first", "freq/spread/morphology are one axis (0.79–0.94)"],
    ["Credit unique information, not raw size", "frequency = " + f"{w[0]}%" + " unique; concentration = " + f"{w[3]}%"],
    ["When a scalar misbehaves, the order may be partial", "every forced ranking put a hapax/verb above ءله"],
    ["Reframe linear → network when structure is relational", "roles beat degree-null (z=+" + str(N.get("modularity_z", "—")) + ")"],
    ["Use form AND content", "کوثر invisible on root, recovered on word substrate"],
    ["Demote what the null explains", "hub criticality is degree-explained — dropped"],
])

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
    "<b>مسئله.</b> «کدام مفهوم در قرآن مهم‌تر است؟» این پرسش فرض می‌گیرد که اهمیت یک <b>نردبانِ خطی</b> است و پلهٔ آن "
    "را <b>بسامد</b> تعیین می‌کند. داده‌ها هر دو فرض را رد می‌کنند: بسامد، گستره و تنوعِ صرفی تقریباً یک محورند (همبستگی "
    "۰٫۷۹ تا ۰٫۹۴)، و سهمِ <b>یکتای</b> بسامد تنها " + f"{w[0]}" + "٪ است.<br><br>"
    "<b>بازقالب‌بندی (هستهٔ کار).</b> به‌جای رتبه‌بندی، می‌پرسیم هر مفهوم چه <b>نقشی</b> در شبکهٔ هم‌آیی دارد: "
    "اَبَرگره (ءله، قول، ربب)، رابط، متخصص، یا <b>تعریف‌گرِ واحد</b>. ساختارِ نقش‌ها در برابرِ نُلِ هم‌درجه واقعی است "
    "(z=+" + str(N.get("modularity_z", "—")) + ").<br><br>"
    "<b>احسن تقویم.</b> نظام در بهترین تناسب است: <b>نه می‌توان افزود چون بسنده است، نه کاست چون لازم است</b>. "
    "<b>ضرورت (حذف‌ناپذیری):</b> برهم‌زدنِ ترتیب، ساختار را فرومی‌پاشد؛ و " + str(g("root_sig", "—")) + " ریشه و " +
    str(g("word_sig", "—")) + " واژه، سورهٔ خود را بالاتر از شانس «در تملک» دارند (صمد، کوثر، نحر…). "
    "<b>کفایت (افزودن‌ناپذیری):</b> دو محور ۹۲٪ ساختار را نگه می‌دارند، شبکه یک‌پارچه است (۹۹٫۸٪) و از تصادف "
    "مقاوم‌تر است.<br><br>"
    "<b>صورت و محتوا.</b> هم ریشه (محتوا)، هم واژهٔ رسمی (صورت)، هم صرف لازم‌اند: «کوثر» در سطحِ ریشه در «کثر» گم "
    "می‌شود اما در سطحِ واژه به‌عنوان تعریف‌گرِ سورهٔ کوثر بازمی‌گردد؛ «محمد» پراکنده می‌ماند. <b>هیچ‌چیز بی‌اهمیت "
    "نیست</b> — اما نه به یک اندازه و نه روی یک خط‌کش.<br><br>"
    "<b>انصاف و حد.</b> بحرانی‌بودنِ اَبَرگره با درجه توضیح داده می‌شود (z=+" + str(N.get("hub_knockout_z", "—")) +
    ")، پس ادعای «نقطهٔ شکستِ یگانه» را وامی‌نهیم؛ و وزنِ کلامیِ مفاهیم (معنا) بیرون از این ابزار است. این داوری "
    "<b>ساختاری و روش‌شناختی</b> است (درجه ۷۲، نامزد)، نه کلامی.</div>", unsafe_allow_html=True)

# ╔══════════════ ARABIC ABSTRACT ══════════════╗
C.section("الملخّص الكامل — Arabic abstract")
st.markdown(
    "<div dir='rtl' id='im-ar' style='font-family:Amiri,\"Scheherazade New\",Tahoma,serif;font-size:15.5px;"
    "line-height:1.9;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;"
    "border-radius:11px;padding:16px 20px'>"
    "<b>المسألة.</b> «أيُّ مفهومٍ أهمُّ في القرآن؟» يفترض السؤالُ أنّ الأهمية <b>سُلَّمٌ خطّيّ</b> دَرَجتُه "
    "<b>التكرار</b>. والبياناتُ تردُّ الفرضين: التكرار والانتشار والثراء الصرفيّ محورٌ واحد (ارتباط ٠٫٧٩–٠٫٩٤)، "
    "ونصيبُ التكرار <b>الفريد</b> " + f"{w[0]}" + "٪ فقط.<br><br>"
    "<b>إعادة التأطير (جوهر العمل).</b> بدل الترتيب، نسأل عن <b>الدور</b> في شبكة التلازم: محورٌ جامع (ءله، قول، ربب)، "
    "واصلٌ، متخصّصٌ، أو <b>مُعرِّفٌ للوحدة</b>. وبنيةُ الأدوار حقيقيةٌ تتجاوز نُلَّ الدرجات (z=+" +
    str(N.get("modularity_z", "—")) + ").<br><br>"
    "<b>أحسن تقويم.</b> النظامُ في أحسن تناسبٍ: <b>لا يُزاد لأنّه كافٍ، ولا يُنقَص لأنّه ضروريّ</b>. "
    "<b>الضرورة (تعذّر الحذف):</b> خلطُ الترتيب يُسقِط البنية؛ و" + str(g("root_sig", "—")) + " جذراً و" +
    str(g("word_sig", "—")) + " كلمةً تَملِك سورتَها فوق الصدفة (صمد، كوثر، نحر…). <b>الكفاية (تعذّر الزيادة):</b> "
    "محوران يحملان ٩٢٪ من البنية، والشبكةُ كلٌّ موصولٌ (٩٩٫٨٪)، أمتنُ من العشوائيّ.<br><br>"
    "<b>الصورة والمضمون.</b> الجذرُ (مضمون) والكلمةُ الرسميّة (صورة) والصرفُ كلُّها لازمة: «الكوثر» يذوب في «كثر» على "
    "مستوى الجذر، ويعود مُعرِّفاً لسورة الكوثر على مستوى الكلمة؛ و«محمد» يبقى منتشراً. <b>لا شيء عديمُ الأهمية</b> — "
    "لكن ليس بالتساوي ولا على مسطرةٍ واحدة.<br><br>"
    "<b>إنصافٌ وحدّ.</b> حَرِجِيّةُ المحور الجامع تفسّرها الدرجةُ (z=+" + str(N.get("hub_knockout_z", "—")) +
    ")، فنترك دعوى «نقطة الانهيار الوحيدة»؛ والوزنُ اللاهوتيُّ (المعنى) خارج هذه الأداة. حكمٌ <b>بنيويٌّ منهجيّ</b> "
    "(الدرجة ٧٢، مُرشَّح) لا لاهوتيّ.</div>", unsafe_allow_html=True)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
# end of close-up · importance reframed
