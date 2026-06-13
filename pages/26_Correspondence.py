# Correspondence Ledger — the Qur'an as a designed system (native, interactive).
import json
import os

import streamlit as st

try:
    import state as S
except Exception:
    S = None

st.set_page_config(page_title="Correspondence Ledger", page_icon="🫀", layout="wide")
if S:
    try:
        S.log_page("correspondence")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    VZ = json.load(open(os.path.join(HERE, "research", "correspondence", "correspondence_viz.json"), encoding="utf-8"))
except Exception:
    VZ = {}

st.markdown(
    "<style>"
    ".block-container{max-width:1200px;padding-top:1rem}"
    ".cl-h1{font-size:30px;font-weight:800;color:#16243B;margin:0 0 2px}"
    ".cl-sub{font-size:14px;color:#10243A;line-height:1.55;margin:0 0 6px;max-width:920px}"
    ".cl-why{background:#F5F8FC;border-left:4px solid #1D3557;border-radius:8px;padding:10px 14px;"
    "font-size:14px;line-height:1.55;color:#16243B;margin:6px 0 10px;max-width:980px}"
    ".cl-sec{font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.8px;color:#1D3557;"
    "margin:22px 0 8px;border-bottom:2px solid #E7ECF3;padding-bottom:5px}"
    ".cl-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:2px 0}"
    "@media(max-width:820px){.cl-grid{grid-template-columns:1fr}}"
    ".cl-card{background:#fff;border:1px solid #E7ECF3;border-left:4px solid #1D9E75;border-radius:7px;padding:6px 11px;margin:0}"
    ".cl-card.b{border-left-color:#7FB069}.cl-card.d{border-left-color:#C4CBD3;background:#f7f8f9}"
    ".cl-ct{font-size:13px;font-weight:800;color:#16243B;margin:0 0 1px}"
    ".cl-look{font-size:12.5px;color:#10243A;line-height:1.35;margin:0}.cl-look b{color:#1D3557}"
    ".cl-found{font-size:12.5px;color:#0B3F2A;line-height:1.35;margin:1px 0 0}.cl-found b{color:#13592a}"
    ".cl-rej{font-size:12.5px;color:#9a4a4a;line-height:1.35;margin:1px 0 0}.cl-rej b{color:#7a2a2a}"
    "</style>",
    unsafe_allow_html=True,
)

st.markdown('<div class="cl-h1">🫀 Correspondence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="cl-sub">The <b>body</b> is the benchmark: for each property a body has, we test whether the '
    "Qurʾān measurably has it — and on which sūras, āyāt and roots — using only the "
    "text’s own shuffle as the null.</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="cl-why"><b>The idea &amp; what we got.</b> A designed system — a body, but equally a society, a '
    "genome, a geography — is recognisable by a fixed set of structural properties: parts with a unique "
    "<b>identity</b>, sealed by <b>membranes</b>, joined by specific <b>wiring</b>, paced by a <b>rhythm</b>, "
    "some arriving as matched <b>pairs</b>. The body is our <b>benchmark</b>: for each such property we ask, "
    "one-directionally, whether the Qurʾān measurably has it — and on which sūras, āyāt and roots — never "
    "reading a Qurʾān feature and retrofitting a body label. A property counts as <b>found</b> only with a "
    "proper null (the text’s own shuffle), an honest effect size, and a re-runnable script; a failed test "
    "indicts the <i>instrument</i>, not the text (all-or-none — refine, never declare it absent). After "
    "<b>7 scrutiny passes</b> the yield is a <b>7-property form-level core</b> that survives proper nulls, "
    "length de-confounding <i>and</i> split-half replication — shown below with its actual sūras, roots and "
    "charts. The headline is the synthesis: scattered, separately-known measures cohere as one "
    "<b>designed-system signature</b>.</div>",
    unsafe_allow_html=True,
)

m = st.columns(6)
m[0].metric("Bedrock (A)", "7", help="survived every scrutiny pass")
m[1].metric("Second tier (B)", "6", help="real but modest")
m[2].metric("Tested & rejected", "5", help="filed honestly, not disproof")
m[3].metric("Attributes tested", "34", help="across 7 scrutiny passes")
m[4].metric("Sūras in the system", "114")
m[5].metric("Strongest effect", "z = 125", help="propagation / self-replicating formulae")

# ---------------- discovery-visual builders (self-contained, used by the hero section) ----------------
def _dv_line(series, color="#1D9E75"):
    s = series
    if len(s) > 160:
        stp = len(s) / 160.0
        s = [s[int(i * stp)] for i in range(160)]
    mx = max(s) or 1.0
    n = len(s)
    pts = []
    for i, v in enumerate(s):
        x = 4.0 + (i / (n - 1.0)) * 316.0
        y = 70.0 - (v / mx) * 58.0
        pts.append("%.1f,%.1f" % (x, y))
    return ('<svg viewBox="0 0 320 76" width="100%%" height="74" preserveAspectRatio="none" role="img">'
            '<path d="M%s" fill="none" stroke="%s" stroke-width="1.3"/></svg>' % (" L".join(pts), color))

def _dv_bars(items, color="#1D9E75"):
    mx = max(v for _, v in items) or 1
    rows = ""
    for lab, v in items:
        w = max(4, int(v / float(mx) * 100))
        rows += ('<div style="display:flex;align-items:center;gap:6px;font-size:11px;margin:2px 0">'
                 '<span style="width:104px;flex:none;color:#10243A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">%s</span>'
                 '<span style="flex:1;height:9px;background:#ECEFF3;border-radius:3px;overflow:hidden">'
                 '<i style="display:block;height:100%%;width:%d%%;background:%s"></i></span>'
                 '<span style="width:36px;flex:none;text-align:right;font-weight:700;color:#16243B">%s</span></div>'
                 % (lab, w, color, v))
    return rows

def _net_svg():
    tw = VZ.get("twins", [])[:8]
    forms = [(26, 28, "ṬSM"), (25, 67, "Tabāraka"), (62, 64, "Yusabbiḥ"), (85, 86, "wa-l-samāʾ"), (113, 114, "ʿawḏ")]
    Y0 = 104.0
    def X(s):
        return 28.0 + (s - 1) / 113.0 * 626.0
    P = ['<line x1="28" y1="%g" x2="654" y2="%g" stroke="#D7DEE6" stroke-width="1.2"/>' % (Y0, Y0)]
    for s in (1, 30, 60, 90, 114):
        P.append('<text x="%.1f" y="%g" font-size="12" fill="#10243A" text-anchor="middle">%d</text>' % (X(s), Y0 + 17, s))
    nodes = set()
    if tw:
        mxn = max(t.get("n", 1) for t in tw)
        for t in tw:
            try:
                a, b = [int(x) for x in t["p"].split("·")]
            except Exception:
                continue
            nodes.update((a, b))
            xa, xb = X(a), X(b)
            mid = (xa + xb) / 2.0
            apex = Y0 - (22.0 + (t.get("n", 1) / float(mxn)) * 68.0)
            w = 1.4 + (t.get("n", 1) / float(mxn)) * 2.4
            P.append('<path d="M%.1f %g Q%.1f %.1f %.1f %g" fill="none" stroke="#1D9E75" stroke-width="%.1f" opacity="0.9"/>' % (xa, Y0, mid, apex, xb, Y0, w))
        t = tw[0]
        try:
            a, b = [int(x) for x in t["p"].split("·")]
            mid = (X(a) + X(b)) / 2.0
            P.append('<text x="%.1f" y="14" font-size="12" font-weight="700" fill="#0F6E56" text-anchor="start">%s &mdash; %d shared roots</text>' % (max(mid - 20.0, 30.0), t.get("nm", "").split(" (")[0], t.get("n", 0)))
        except Exception:
            pass
    for a, b, lab in forms:
        nodes.update((a, b))
        xa, xb = X(a), X(b)
        mid = (xa + xb) / 2.0
        apex = Y0 - (16.0 + min(62.0, abs(xb - xa) * 0.42))
        P.append('<path d="M%.1f %g Q%.1f %.1f %.1f %g" fill="none" stroke="#D85A30" stroke-width="1.7" stroke-dasharray="4,3"/>' % (xa, Y0, mid, apex, xb, Y0))
        P.append('<text x="%.1f" y="%.1f" font-size="10" fill="#A8542F" text-anchor="middle">%s</text>' % (mid, apex - 4, lab))
    for s in nodes:
        P.append('<circle cx="%.1f" cy="%g" r="3" fill="#16243B"/>' % (X(s), Y0))
    P.append('<line x1="500" y1="12" x2="524" y2="12" stroke="#1D9E75" stroke-width="2.6"/><text x="529" y="16" font-size="11" fill="#10243A">shared-root link</text>')
    P.append('<line x1="500" y1="28" x2="524" y2="28" stroke="#D85A30" stroke-width="1.7" stroke-dasharray="4,3"/><text x="529" y="32" font-size="11" fill="#10243A">form-twin (same opening)</text>')
    return '<svg viewBox="0 0 680 128" width="100%" preserveAspectRatio="xMidYMid meet" role="img">' + "".join(P) + '</svg>'

# ---------------- WHAT WE DISCOVERED — three results, each visualized ----------------
st.markdown('<div class="cl-sec">What we discovered — three results, each visualized</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:13px;color:#10243A;margin:-2px 0 8px;max-width:1050px">Three discoveries cover all seven bedrock features — each measured only against the text&#700;s own shuffle (the One Law).</div>', unsafe_allow_html=True)
st.markdown('<div style="font-size:15px;font-weight:700;color:#1D3557;margin:8px 0 3px">Discovery 1 — a Sūra is an integrated unit <span style="font-weight:400;color:#10243A">(A1 edge · A2 interior · A6 wiring)</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="background:#fff;border:1px solid #E7ECF3;border-radius:12px;padding:14px 18px;margin:2px 0 8px;max-width:1050px">'
    '<div style="font-size:14px;line-height:1.55;color:#16243B;margin-bottom:6px">'
    '<b>In plain terms:</b> whether a sūra has 5 verses or 286, every one tests as the '
    '<b style="color:#0F6E56">same kind of object</b> — a sealed edge, an ordered interior, and specific '
    'wiring to other sūras. Size, content and position change; the structure does not. Like organs in a body: '
    'a heart and a taste-bud differ wildly in size and place, yet each is a bounded, ordered, connected unit.</div>'
    '<svg viewBox="0 0 680 230" width="100%" preserveAspectRatio="xMidYMid meet" role="img">'
    '<defs><pattern id="wv" width="7" height="7" patternUnits="userSpaceOnUse">'
    '<path d="M0 3.5 H7 M3.5 0 V7" stroke="#BFE3D3" stroke-width="0.8"/></pattern></defs>'
    '<path d="M158 66 Q200 24 242 68" fill="none" stroke="#1D9E75" stroke-width="1.6"/>'
    '<text x="200" y="34" font-size="11" font-weight="600" fill="#0F6E56" text-anchor="middle">342 shared roots</text>'
    '<path d="M515 86 Q545 62 575 86" fill="none" stroke="#1D9E75" stroke-width="1.6"/>'
    '<text x="545" y="70" font-size="11" font-weight="600" fill="#0F6E56" text-anchor="middle">4 shared</text>'
    '<circle cx="110" cy="104" r="56" fill="#EAF6F0"/><circle cx="110" cy="104" r="56" fill="url(#wv)"/>'
    '<circle cx="110" cy="104" r="56" fill="none" stroke="#1D9E75" stroke-width="2.5"/>'
    '<circle cx="158" cy="66" r="3.2" fill="#1D9E75"/>'
    '<text x="110" y="186" font-size="12.5" font-weight="600" fill="#16243B" text-anchor="middle">al-Baqara</text>'
    '<text x="110" y="202" font-size="11" fill="#10243A" text-anchor="middle">286 verses</text>'
    '<circle cx="285" cy="104" r="48" fill="#EAF6F0"/><circle cx="285" cy="104" r="48" fill="url(#wv)"/>'
    '<circle cx="285" cy="104" r="48" fill="none" stroke="#1D9E75" stroke-width="2.5"/>'
    '<circle cx="242" cy="68" r="3.2" fill="#1D9E75"/>'
    '<text x="285" y="186" font-size="12.5" font-weight="600" fill="#16243B" text-anchor="middle">Āl-ʿImrān</text>'
    '<text x="285" y="202" font-size="11" fill="#10243A" text-anchor="middle">200 verses</text>'
    '<circle cx="500" cy="104" r="20" fill="#EAF6F0"/><circle cx="500" cy="104" r="20" fill="url(#wv)"/>'
    '<circle cx="500" cy="104" r="20" fill="none" stroke="#1D9E75" stroke-width="2.5"/>'
    '<circle cx="515" cy="86" r="3" fill="#1D9E75"/>'
    '<text x="500" y="150" font-size="12.5" font-weight="600" fill="#16243B" text-anchor="middle">al-Falaq</text>'
    '<text x="500" y="166" font-size="11" fill="#10243A" text-anchor="middle">5 verses</text>'
    '<circle cx="590" cy="104" r="20" fill="#EAF6F0"/><circle cx="590" cy="104" r="20" fill="url(#wv)"/>'
    '<circle cx="590" cy="104" r="20" fill="none" stroke="#1D9E75" stroke-width="2.5"/>'
    '<circle cx="575" cy="86" r="3" fill="#1D9E75"/>'
    '<text x="590" y="150" font-size="12.5" font-weight="600" fill="#16243B" text-anchor="middle">al-Nās</text>'
    '<text x="590" y="166" font-size="11" fill="#10243A" text-anchor="middle">6 verses</text>'
    '<text x="197" y="223" font-size="11" fill="#9AA4B2" text-anchor="middle">a giant pair</text>'
    '<text x="545" y="190" font-size="11" fill="#9AA4B2" text-anchor="middle">a tiny pair</text>'
    '</svg>'
    '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:10px">'
    '<div style="border:1px solid #E7ECF3;border-radius:9px;padding:9px 11px">'
    '<div style="font-size:12.5px;font-weight:700;color:#16243B;margin-bottom:2px">Edge &middot; the membrane</div>'
    '<div style="font-size:11.5px;color:#10243A;line-height:1.4">Like an organ&#700;s membrane — the boundary is '
    'detectable: root-overlap <b style="color:#0F6E56">0.87 inside &rarr; 0.28</b> at the seam.</div></div>'
    '<div style="border:1px solid #E7ECF3;border-radius:9px;padding:9px 11px">'
    '<div style="font-size:12.5px;font-weight:700;color:#16243B;margin-bottom:2px">Interior &middot; the weave</div>'
    '<div style="font-size:11.5px;color:#10243A;line-height:1.4">Like ordered tissue, not a cell-heap — shuffle the '
    'verses and cohesion drops <b style="color:#0F6E56">0.73 &rarr; 0.52</b>. The order is load-bearing.</div></div>'
    '<div style="border:1px solid #E7ECF3;border-radius:9px;padding:9px 11px">'
    '<div style="font-size:12.5px;font-weight:700;color:#16243B;margin-bottom:2px">Wiring &middot; the network</div>'
    '<div style="font-size:11.5px;color:#10243A;line-height:1.4">Like vessels between organs — '
    '<b style="color:#0F6E56">44% of sūra-pairs</b> link specifically (vs 1% by chance).</div></div>'
    '</div>'
    '<div style="background:#EAF6F0;border-radius:8px;padding:9px 13px;margin-top:10px;font-size:12.5px;'
    'line-height:1.5;color:#04342C">Size ranges from <b>5 to 286 verses</b>; content and muṣḥaf position differ '
    'entirely — yet each is the same kind of object: <b>bounded &middot; ordered &middot; connected</b>. '
    'That is what &#8220;integrated unit&#8221; means, measured only against the text&#700;s own shuffle.</div>'
    '</div>', unsafe_allow_html=True)

# ---------------- Discovery 2: sūras form a modular network ----------------
st.markdown('<div style="font-size:15px;font-weight:700;color:#1D3557;margin:12px 0 3px">Discovery 2 — sūras form a modular network <span style="font-weight:400;color:#10243A">(A6 wiring · A7 twins)</span></div>', unsafe_allow_html=True)
st.markdown(
    '<div style="background:#fff;border:1px solid #E7ECF3;border-radius:12px;padding:13px 16px;margin:2px 0 8px;max-width:1050px">'
    '<div style="font-size:14px;line-height:1.55;color:#16243B;margin-bottom:6px">'
    'Sūras are <b>not</b> a bag of independent texts. Specific pairs share far more roots than a degree-matched '
    'shuffle would give (<b style="color:#0F6E56">teal arcs</b>, thicker = stronger — e.g. Baqara·Āl-ʿImrān 342), '
    'and <b style="color:#993C1D">form-twin</b> sūras that open with the same template pair up above chance '
    '(<b style="color:#993C1D">dashed arcs</b> — ṬSM 26·28, Tabāraka 25·67, wa-l-samāʾ 85·86). '
    'The whole book reads as a wired, modular system.</div>'
    + _net_svg() +
    '<div style="font-size:12px;color:#10243A;margin-top:4px">Horizontal axis = the 114 sūras in order · arch height = link strength · dashed = bilateral form-twins.</div>'
    '</div>', unsafe_allow_html=True)

# ---------------- Discovery 3: three confirming signatures ----------------
st.markdown('<div style="font-size:15px;font-weight:700;color:#1D3557;margin:12px 0 3px">Discovery 3 — three system signatures <span style="font-weight:400;color:#10243A">(A3 self-replication · A5 rhythm · A4 interface)</span></div>', unsafe_allow_html=True)
_ff = [(f["al"] + "·" + f["bl"], f["n"]) for f in VZ.get("formulae", [])[:6]]
st.markdown(
    '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:2px 0 8px;max-width:1050px">'
    '<div style="background:#fff;border:1px solid #E7ECF3;border-radius:11px;padding:11px 13px">'
    '<div style="font-size:14px;font-weight:700;color:#16243B">Self-replication <span style="color:#0F6E56">z=+125</span></div>'
    '<div style="font-size:12px;color:#10243A;line-height:1.45;margin:2px 0 6px">Fixed root-formulae recur far above chance, across every region — the text copies its own forms.</div>'
    + _dv_bars(_ff) +
    '</div>'
    '<div style="background:#fff;border:1px solid #E7ECF3;border-radius:11px;padding:11px 13px">'
    '<div style="font-size:14px;font-weight:700;color:#16243B">Rhythm <span style="color:#0F6E56">DFA 0.95</span></div>'
    '<div style="font-size:12px;color:#10243A;line-height:1.45;margin:2px 0 6px">Verse-lengths carry long-range 1/f memory across the whole book — a multi-scale pulse, not noise.</div>'
    + _dv_line(VZ.get("wave", [1, 1])) +
    '<div style="font-size:10px;color:#9AA4B2;margin-top:2px;text-align:center">words per verse · sūra 1 → 114</div>'
    '</div>'
    '<div style="background:#fff;border:1px solid #E7ECF3;border-radius:11px;padding:11px 13px">'
    '<div style="font-size:14px;font-weight:700;color:#16243B">Interface zones <span style="color:#0F6E56">z=+17.6</span></div>'
    '<div style="font-size:12px;color:#10243A;line-height:1.45;margin:2px 0 7px">Outward-address verses (qul, yā-ayyuhā) cluster into zones rather than scattering — an outward-facing surface.</div>'
    '<div style="display:flex;height:22px;border-radius:5px;overflow:hidden;font-size:10px;color:#fff;font-weight:700">'
    '<div style="width:28%;background:#1D9E75;display:flex;align-items:center;justify-content:center">28% out</div>'
    '<div style="width:72%;background:#C4CBD3;display:flex;align-items:center;justify-content:center;color:#10243A">72% inward</div></div>'
    '</div>'
    '</div>', unsafe_allow_html=True)

# ---------------- what we got: the discovery payoff ----------------
st.markdown(
    '<div style="background:#F5F8FC;border-left:4px solid #1D3557;border-radius:8px;'
    'padding:12px 16px;font-size:13px;line-height:1.55;color:#16243B;margin:12px 0 6px;max-width:1050px">'
    '<b>What we got — the discovery payoff.</b> The question this ledger asked: treat the '
    'Qur&#700;ān as a designed system, benchmark it against the body, and see which of the body&#700;s '
    'organizational features it carries — each measured <b>only against the text&#700;s own shuffle</b> '
    '(the One Law, on the rasm).'
    '<br><br><b>The yield.</b> Seven features survive their own-shuffle null (grade A). Read against the '
    'north star — what a <b>Sūra</b> is and why the current arrangement — three are load-bearing: a Sūra has '
    'a detectable <b>edge</b> (A1, root-overlap collapses at the boundary), an ordered <b>interior</b> '
    '(A2, shuffling its verses destroys cohesion), and specific <b>wiring</b> to other sūras (A6, a modular '
    'network). Together: the Sūra is a <b>bounded, internally-ordered, specifically-connected unit</b> — the '
    'raw material a necessary-and-sufficient definition needs. Propagation (A3, z=+125), interface-zones (A4), '
    'rhythm (A5) and bilateral twins (A7) add self-replicating, outward-facing, pulse-like and paired structure.'
    '<br><br><b>What is genuinely new.</b> Rhythm, boundaries and order were already in the Determinacy ledger; '
    'this program&#700;s net-new contribution is the <b>network view</b> (A6 connectivity + A7 twins) and the '
    'explicit <b>unit-definition</b> framing (edge + interior + wiring).'
    '<br><br><b>What it ruled out</b> (equally a result). Five candidates failed: location, folding-decay and '
    'development are <b>length-gradient artifacts</b>; the muqaṭṭaʿāt skeleton fails split-half; circulation '
    'clumps instead of perfusing. Per the One Law a failed correspondence indicts the <i>instrument</i>, not the '
    'text — so we file them honestly as not-yet-captured, never as disproof.'
    '<br><br><b>Bottom line, ranked.</b> '
    '<b>1)</b> The Sūra is now a <b>definable unit</b> — edge (A1) + ordered interior (A2) + specific wiring (A6); '
    'this is the real advance toward the north star. '
    '<b>2)</b> The <b>modular sūra-network</b> (A6/A7) is the main feature this effort added beyond Determinacy. '
    '<b>3)</b> Five honest demotions map the text&#700;s limits — what it does <i>not</i> do. '
    'The effort did <i>not</i> prove &#8220;the Qur&#700;ān is a body&#8221;; it produced an intrinsically-'
    'validated catalogue of what the Sūra <i>is</i> structurally.</div>',
    unsafe_allow_html=True,
)

# ---------------- master table (full-width HTML: every column visible, text wraps) ----------------
st.markdown(
    "<style>"
    ".ct{width:100%;max-width:1060px;border-collapse:collapse;font-size:11.5px;line-height:1.3;table-layout:fixed;margin:2px 0 6px}"
    ".ct th{background:#1D3557;color:#fff;text-align:left;padding:4px 7px;font-size:11px;font-weight:700}"
    ".ct td{padding:4px 7px;border-bottom:1px solid #EDF1F6;color:#2B3440;vertical-align:top;word-wrap:break-word;overflow-wrap:anywhere}"
    ".ct .ct-id{width:40px;font-weight:800;color:#1D3557}"
    ".ct .ct-c{width:108px;font-weight:700;color:#16243B}"
    ".ct .ct-why{color:#10243A}.ct .ct-got{color:#0B3F2A}"
    ".ct .ct-g{width:50px;text-align:center}"
    "</style>", unsafe_allow_html=True)
st.markdown('<div class="cl-sec">All correspondences — what we did · why · what we got</div>', unsafe_allow_html=True)
try:
    ROWS = [
        ("A1", "Membrane", "measured adjacent-verse root overlap, inside a sura vs across its boundary", "organs are sealed by a membrane — a sura should have a real edge", "root-overlap collapses at the seam", "0.28 vs 0.87", "z=-5", "A"),
        ("A2", "Internal weave", "compared a sura's real verse order to its own shuffle", "tissue is ordered, not a loose pile of cells", "verses chained beyond vocabulary", "0.73 vs 0.52", "t=10.9", "A"),
        ("A3", "Propagation", "counted recurring root-formulae vs a shuffled stream", "designed systems copy their own forms (self-replication)", "formulae repeat (samaʾ-ard x188)", "575 formulae", "z=+125", "A"),
        ("A4", "Interface-zones", "located outward markers (qul, ya-ayyuha) and tested their clustering", "a body faces its environment through localized surfaces (skin, senses)", "outward address clusters (qul x270)", "28% of verses", "z=+17.6", "A"),
        ("A5", "Rhythm / pulse", "ran DFA / 1-f on the verse-length signal", "living systems have a multi-scale pulse (heartbeat)", "verse-length long memory", "DFA 0.95", "z~20", "A"),
        ("A6", "Connectivity", "associated all sura-pairs by shared roots vs a degree-preserving null", "organs wire to specific partners, not at random", "specific pairs (2.3 share 342 roots)", "44% of pairs", "vs 1%", "A"),
        ("A7", "Bilateral pairs", "searched for suras sharing a distinctive opening template", "bodies have matched identical pairs (two eyes, two ears)", "form-twins (TSM 26.28 ...)", "14 pairs vs 5.7", "z=+5.4", "A"),
        ("B", "Identity", "classified a held-out verse back to its home sura", "each organ has a unique, non-redundant function", "verse traces to home sura", "7.2% vs 4.9%", "z~7.7", "B"),
        ("B", "Necessity", "found each sura's nearest neighbour in a function space", "remove an organ and the body loses a function", "Fatiha most-isolated", "rank 1/114", "-", "B"),
        ("B", "Digestive loop", "tested whether 'ask' (sa'al) is answered by 'say' (qul)", "bodies ingest external material and process it", "'ask' -> 'say' within 2 verses", "25% vs 4%", "-", "B"),
        ("B", "Polarity", "detected the first vs last verse of each sura", "organs have a head-tail (anterior-posterior) axis", "marked head, faint tail", "0.75 / 0.61", "AUC", "B"),
        ("B", "Error-correction", "tested if a verse-ending is recoverable from the rhyme", "bodies carry redundancy for self-repair", "endings rhyme-recoverable", "73% vs 50%", "-", "B"),
        ("B", "Signal", "measured root-overlap between adjacent verses", "a nervous system propagates signals", "content carries verse->verse", "0.087 vs 0.009", "~10x", "B"),
        ("OUT", "Location", "predicted sura position from its profile, controlling for length", "organs sit in fixed anatomical positions", "just the length ordering", "resid R2=0.03", "OUT", "OUT"),
        ("OUT", "Folding-decay", "correlated sura association with sequence distance, minus length", "a 1-D genome folds into a 3-D contact map (Hi-C)", "a length artifact", "r=-0.04", "OUT", "OUT"),
        ("OUT", "Development", "clustered suras into two size/style classes", "bodies develop through ontogenetic stages", "the length gradient", "-", "OUT", "OUT"),
        ("OUT", "Skeleton", "tested if the muqatta'at suras cohere, split-half", "a body has a rigid structural frame", "fails split-half", "t=10.3 / 1.7", "OUT", "OUT"),
        ("OUT", "Circulation", "checked if a core root perfuses every region evenly", "blood circulates to every tissue", "message clumps, no perfusion", "gap-CV z=+63", "OUT", "OUT"),
    ]
    def _g(grade):
        c = {"A": "#1D9E75", "B": "#C9962B"}.get(grade, "#9AA4B2")
        return ('<span style="display:inline-block;min-width:28px;text-align:center;padding:1px 5px;'
                'border-radius:6px;background:%s;color:#fff;font-weight:800;font-size:11px">%s</span>' % (c, grade))
    rows_html = ""
    for _id, corr, did, why, found, key, eff, grade in ROWS:
        tone = "background:#f7f8f9;" if grade == "OUT" else ""
        got = found
        if key and key != "-":
            got += " — <b>%s</b>" % key
        if eff and eff not in ("-", "OUT"):
            got += " <span style='color:#6b7480'>(%s)</span>" % eff
        rows_html += ('<tr style="%s"><td class="ct-id">%s</td><td class="ct-c">%s</td>'
                      '<td>%s</td><td class="ct-why">%s</td><td class="ct-got">%s</td>'
                      '<td class="ct-g">%s</td></tr>' % (tone, _id, corr, did, why, got, _g(grade)))
    st.markdown(
        '<table class="ct"><colgroup>'
        '<col style="width:4%"><col style="width:12%"><col style="width:27%">'
        '<col style="width:25%"><col style="width:26%"><col style="width:6%">'
        '</colgroup><thead><tr><th>ID</th><th>Correspondence</th><th>What we did</th>'
        "<th>Why we did it (body)</th><th>What we got (Qur'an)</th><th>Grade</th></tr></thead><tbody>"
        + rows_html + "</tbody></table>", unsafe_allow_html=True)
except Exception as e:
    st.info("Table unavailable: %s" % e)

# ---------------- charts (rendered directly, no tabs; each isolated + native fallback) ----------------
st.markdown('<div class="cl-sec">The evidence — results &amp; charts</div>', unsafe_allow_html=True)
try:
    import plotly.graph_objects as go
    _PLOTLY = True
except Exception:
    _PLOTLY = False
GRID = "#E7ECF3"

def _style(fig, h=230, xt="", yt=""):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=8, b=8), plot_bgcolor="#fff",
                      paper_bgcolor="#fff", xaxis_title=xt, yaxis_title=yt,
                      font=dict(size=12), showlegend=False)
    fig.update_xaxes(gridcolor=GRID, zeroline=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    return fig

def _chart(caption, plotly_fn, fallback=None):
    st.caption(caption)
    try:
        if _PLOTLY:
            plotly_fn()
            return
    except Exception:
        pass
    if fallback is not None:
        try:
            fallback()
        except Exception as e:
            st.caption("chart unavailable (%s)" % e)

ca, cb = st.columns(2)
with ca:
    if VZ.get("wave"):
        def _w():
            f = go.Figure(go.Scatter(y=VZ["wave"], mode="lines", line=dict(color="#1D9E75", width=1),
                                     hovertemplate="verse %{x}<br>%{y} words<extra></extra>"))
            st.plotly_chart(_style(f, 230, "verse (1 → 114)", "words / verse"), use_container_width=True, config={"displayModeBar": False})
        _chart("A5 · Rhythm — words per verse across the whole book; short & long come in waves (DFA 0.95).",
               _w, lambda: st.line_chart(VZ["wave"], height=200))
    mb = VZ.get("membrane", {})
    if mb.get("overlap"):
        def _m():
            f = go.Figure(go.Scatter(y=mb["overlap"], mode="lines", line=dict(color="#1D3557", width=1.2),
                                     hovertemplate="pair %{x}<br>overlap %{y}<extra></extra>"))
            for b in mb.get("boundaries", []):
                f.add_vline(x=b, line_color="#E08A8A", line_width=1, line_dash="dot")
            st.plotly_chart(_style(f, 230, "adjacent verse pair", "shared-root overlap"), use_container_width=True, config={"displayModeBar": False})
        _chart("A1 · Membrane — adjacent-verse overlap; dips at every sūra seam (red lines).",
               _m, lambda: st.line_chart(mb["overlap"], height=200))
with cb:
    if VZ.get("heatmap"):
        def _h():
            f = go.Figure(go.Heatmap(z=VZ["heatmap"], x=VZ.get("suras"), y=VZ.get("suras"), colorscale="Tealgrn",
                                     hovertemplate="Sūra %{x} ↔ Sūra %{y}<br>wiring %{z}<extra></extra>", colorbar=dict(title="shared")))
            f.update_yaxes(autorange="reversed")
            st.plotly_chart(_style(f, 300, "sūra", "sūra"), use_container_width=True, config={"displayModeBar": False})
        _chart("A6 · Connectivity — 114×114 sūra wiring; hover a cell for the two sūras & strength.", _h)
    ff = VZ.get("formulae", [])
    if ff:
        def _f():
            f = go.Figure(go.Bar(x=[x["n"] for x in ff][::-1], y=[x["al"] + " · " + x["bl"] for x in ff][::-1],
                                 orientation="h", marker_color="#1D9E75", hovertemplate="%{y}: x%{x}<extra></extra>"))
            st.plotly_chart(_style(f, 300, "times repeated", ""), use_container_width=True, config={"displayModeBar": False})
        _chart("A3 · Propagation — most-repeated root-formulae (self-replicating phrases).",
               _f, lambda: st.bar_chart({x["al"] + "·" + x["bl"]: x["n"] for x in ff}))

# ---------------- correspondence panels (body <-> Qur'an, Arabic, mini-bars, objective meter) ----------------
st.markdown(
    "<style>"
    ".cp-wrap{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:2px 0 10px}"
    "@media(max-width:820px){.cp-wrap{grid-template-columns:1fr}}"
    ".cp{background:#fff;border:1px solid #E7ECF3;border-left:4px solid #1D9E75;border-radius:10px;padding:10px 13px}"
    ".cp-out{border-left-color:#C4CBD3;background:#FAFBFC}"
    ".cp-hd{display:flex;justify-content:space-between;align-items:center;gap:8px}"
    ".cp-ttl{font-size:14.5px;font-weight:800;color:#16243B}"
    ".cp-meter{display:flex;align-items:center;gap:5px;font-size:10.5px;color:#8A94A0;flex:none}"
    ".cp-track{width:58px;height:6px;background:#ECEFF3;border-radius:4px;overflow:hidden;display:inline-block}"
    ".cp-track>i{display:block;height:100%}"
    ".cp-grade{font-weight:800;font-size:10.5px}"
    ".cp-aspect{font-size:11.5px;color:#10243A;margin:5px 0 8px;line-height:1.35}"
    ".cp-corr{display:grid;grid-template-columns:1fr 22px 1fr;align-items:stretch;gap:5px}"
    ".cp-side{border-radius:7px;padding:6px 9px;font-size:12px;line-height:1.32}"
    ".cp-body{background:#F4F6F8;color:#2B3440}.cp-quran{background:#E6F4EE;color:#0B3F2A}"
    ".cp-slab{font-size:9.5px;text-transform:uppercase;letter-spacing:.05em;margin-bottom:2px}"
    ".cp-body .cp-slab{color:#10243A}.cp-quran .cp-slab{color:#0F6E56}"
    ".cp-arrow{display:flex;align-items:center;justify-content:center;font-size:14px;color:#1D9E75;font-weight:800}"
    ".cp-ar{text-align:center;font-size:18px;color:#16243B;margin:9px 0 7px;line-height:1.7;direction:rtl}"
    ".cp-ar small{font-size:11px;color:#8A94A0;direction:ltr;unicode-bidi:embed}"
    ".cp-chart{margin:7px 0 1px}"
    ".cp-nums{font-size:10px;color:#10243A;text-align:center;margin:0 0 1px}"
    ".cp-rk{display:flex;flex-direction:column;gap:2px;margin:6px 0 1px}"
    ".cp-rkrow{display:flex;align-items:center;gap:6px;font-size:10px}"
    ".cp-rklab{width:98px;flex:none;color:#10243A;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"
    ".cp-rkbt{flex:1;height:8px;background:#ECEFF3;border-radius:3px;overflow:hidden}"
    ".cp-rkbt>i{display:block;height:100%}"
    ".cp-rkv{width:34px;flex:none;text-align:right;font-weight:700;color:#16243B}"
    ".cp-insight{font-size:11.5px;color:#0B3F2A;background:#EAF6F0;border-radius:6px;padding:6px 9px;margin:7px 0 2px;line-height:1.4}"
    ".cp-out .cp-insight{background:#F4F1EC;color:#5E5340}"
    ".cp-bars{display:flex;flex-direction:column;gap:3px;margin-top:2px}"
    ".cp-bar{display:flex;align-items:center;gap:7px;font-size:11px}"
    ".cp-bar>span:first-child{width:74px;color:#10243A;flex:none}"
    ".cp-bt{flex:1;height:8px;background:#ECEFF3;border-radius:4px;overflow:hidden}"
    ".cp-bt>i{display:block;height:100%}"
    ".cp-bv{min-width:82px;text-align:right;font-weight:700;color:#16243B;flex:none}"
    ".cp-eff{font-size:10.5px;text-align:right;margin-top:3px;color:#0F6E56}"
    ".cp-out .cp-eff{color:#9A7B4F}"
    "</style>", unsafe_allow_html=True)

def _ds(series, target=120):
    if len(series) <= target:
        return list(series)
    step = len(series) / float(target)
    return [series[int(i * step)] for i in range(target)]

def _line_svg(series, color, boundaries=None):
    s = _ds(series, 120)
    mx = max(s) or 1.0
    n = len(s)
    pts = []
    for i, v in enumerate(s):
        x = 6.0 + (i / (n - 1.0)) * 240.0
        y = 44.0 - (v / mx) * 34.0
        pts.append("%.1f,%.1f" % (x, y))
    poly = "M" + " L".join(pts)
    bl = ""
    if boundaries:
        L = len(series)
        for b in boundaries:
            if 0 <= b < L:
                bx = 6.0 + (b / (L - 1.0)) * 240.0
                bl += ('<line x1="%.1f" y1="6" x2="%.1f" y2="44" stroke="#E08A8A" '
                       'stroke-width="1" stroke-dasharray="2,2"/>' % (bx, bx))
    return ('<svg viewBox="0 0 252 50" width="100%%" height="46" preserveAspectRatio="xMidYMid meet" role="img">'
            '<line x1="6" y1="44" x2="246" y2="44" stroke="#E7ECF3" stroke-width="1"/>'
            '%s<path d="%s" fill="none" stroke="%s" stroke-width="1.4"/></svg>' % (bl, poly, color))

def _ranked_html(items, color):
    mx = max(v for _, v in items) or 1
    rows = ""
    for lab, v in items:
        w = max(4, int(v / float(mx) * 100))
        rows += ('<div class="cp-rkrow"><span class="cp-rklab">%s</span>'
                 '<span class="cp-rkbt"><i style="width:%d%%;background:%s"></i></span>'
                 '<span class="cp-rkv">%s</span></div>' % (lab, w, color, v))
    return '<div class="cp-rk">%s</div>' % rows

def _arcs_svg(pairs, color):
    def _x(s):
        return 8.0 + (s - 1) / 113.0 * 236.0
    arcs = ""
    for a, b, lab in pairs:
        xa, xb = _x(a), _x(b)
        mid = (xa + xb) / 2.0
        apex = 44.0 - (6.0 + min(32.0, abs(xb - xa) * 0.45))
        arcs += ('<path d="M%.1f 44 Q%.1f %.1f %.1f 44" fill="none" stroke="%s" stroke-width="1.4"/>'
                 '<circle cx="%.1f" cy="44" r="2.2" fill="%s"/><circle cx="%.1f" cy="44" r="2.2" fill="%s"/>'
                 '<text x="%.1f" y="%.1f" font-size="7.5" fill="#0F6E56" text-anchor="middle">%s</text>'
                 % (xa, mid, apex - 3, xb, color, xa, color, xb, color, mid, apex - 5, lab))
    return ('<svg viewBox="0 0 252 50" width="100%%" height="46" role="img">'
            '<line x1="8" y1="44" x2="244" y2="44" stroke="#C4CBD3" stroke-width="1"/>'
            '<text x="8" y="50" font-size="7" fill="#9AA4B2">sūra 1</text>'
            '<text x="244" y="50" font-size="7" fill="#9AA4B2" text-anchor="end">114</text>'
            '%s</svg>' % arcs)

def _card_chart(d):
    name, col = d["name"], "#1D9E75"
    if name == "Rhythm / pulse" and VZ.get("wave"):
        return _line_svg(VZ["wave"], col)
    if name == "Membrane" and VZ.get("membrane", {}).get("overlap"):
        mb = VZ["membrane"]
        return _line_svg(mb["overlap"], col, mb.get("boundaries"))
    if name == "Propagation" and VZ.get("formulae"):
        ff = VZ["formulae"][:7]
        return _ranked_html([(f["al"] + "·" + f["bl"], f["n"]) for f in ff], col)
    if name == "Connectivity" and VZ.get("twins"):
        tw = VZ["twins"][:6]
        return _ranked_html([(t["nm"].split(" (")[0], t["n"]) for t in tw], col)
    if name == "Bilateral pairs":
        return _arcs_svg([(26, 28, "ṬSM"), (25, 67, "Tabāraka"), (62, 64, "Yusabbiḥ"), (85, 86, "wa-l-samāʾ")], col)
    return None

def _panel(d):
    is_out = d["grade"] == "OUT"
    cls = "cp cp-out" if is_out else "cp"
    gcolor = "#9A7B4F" if is_out else "#0F6E56"
    glabel = "instrument limit" if is_out else "grade %s" % d["grade"]
    mfill = "#C4CBD3" if is_out else "#1D9E75"
    chart = _card_chart(d)
    nums = " &nbsp;&middot;&nbsp; ".join("%s %s" % (b[0], b[3]) for b in d["bars"])
    ar = '<div class="cp-ar">%s</div>' % d["arabic"] if d.get("arabic") else ""
    if chart:
        evid = ('<div class="cp-chart">%s</div><div class="cp-nums">%s</div>'
                '<div class="cp-eff">%s</div>' % (chart, nums, d["eff"]))
    else:
        lbl = "Why it failed &mdash;" if is_out else "So what &mdash;"
        evid = ('<div class="cp-insight"><b>%s</b> %s</div>'
                '<div class="cp-nums">%s</div>' % (lbl, d["eff"], nums))
    return (
        '<div class="%s">'
        '<div class="cp-hd"><div class="cp-ttl">%s &middot; %s</div>'
        '<div class="cp-meter"><span>objective</span>'
        '<span class="cp-track"><i style="width:%d%%;background:%s"></i></span>'
        '<span class="cp-grade" style="color:%s">%s</span></div></div>'
        '<div class="cp-aspect">%s</div>'
        '<div class="cp-corr">'
        '<div class="cp-side cp-body"><div class="cp-slab">Body</div>%s</div>'
        '<div class="cp-arrow">&harr;</div>'
        '<div class="cp-side cp-quran"><div class="cp-slab">Qur&#700;ān</div>%s</div></div>'
        '%s%s'
        '</div>' % (cls, d["id"], d["name"], d["meter"], mfill, gcolor, glabel,
                    d["aspect"], d["body"], d["quran"], ar, evid))

def _section(title, items):
    st.markdown('<div class="cl-sec">%s</div>' % title, unsafe_allow_html=True)
    st.markdown('<div class="cp-wrap">' + "".join(_panel(d) for d in items) + "</div>", unsafe_allow_html=True)

_A_ITEMS = [
    dict(id="A1", name="Membrane", grade="A", meter=90,
         aspect="Does each sūra have a real edge that seals it from its neighbours?",
         body="a membrane seals each organ from the next",
         quran="shared roots collapse exactly at the sūra boundary",
         arabic="بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيم <small>— the seam marker between sūras</small>",
         bars=[("inside sūra", 87, "#1D9E75", "0.87 overlap"), ("at boundary", 28, "#D85A30", "0.28 overlap")],
         eff="effect z = −5 · the edge is real"),
    dict(id="A2", name="Internal weave", grade="A", meter=91,
         aspect="Is a sūra a woven tissue (ordered) or a loose pile of verses?",
         body="tissue is ordered, not a loose pile of cells",
         quran="verse order carries structure beyond shared vocabulary; shuffle it and the weave drops",
         arabic="ثُمَّ · فَ · وَ <small>— the connectives that chain āyāt in sequence</small>",
         bars=[("real order", 73, "#1D9E75", "0.73 weave"), ("shuffled", 52, "#B4B2A9", "0.52 weave")],
         eff="effect t = 10.9 · order is load-bearing"),
    dict(id="A3", name="Propagation", grade="A", meter=94,
         aspect="Does the text copy its own forms, like a system that self-replicates?",
         body="cells copy their own code to reproduce",
         quran="fixed root-formulae recur far above chance, reaching every region",
         arabic="سَمَاء · أَرْض <small>×188</small> &nbsp; عَمِلُوا ٱلصَّالِحَات <small>×89</small>",
         bars=[("observed", 96, "#1D9E75", "575 formulae"), ("shuffled", 7, "#B4B2A9", "chance")],
         eff="effect z = +125 · strongest of the ledger"),
    dict(id="A4", name="Interface-zones", grade="A", meter=88,
         aspect="Does the text face outward, like skin and sense-organs facing the world?",
         body="a body meets its environment through localized surfaces",
         quran="outward-address verses cluster into zones, not scattered",
         arabic="قُلْ <small>×270 “say”</small> &nbsp; يَا أَيُّهَا <small>×153 “O you…”</small>",
         bars=[("outward", 28, "#1D9E75", "28% face out"), ("inward", 72, "#B4B2A9", "72% inward")],
         eff="they cluster into zones · z = +17.6"),
    dict(id="A5", name="Rhythm / pulse", grade="A", meter=89,
         aspect="Is there a multi-scale pulse across the book, like a heartbeat?",
         body="living systems beat with long-range, multi-scale rhythm",
         quran="verse-lengths show long memory across all 114 sūras",
         arabic="مُدْهَامَّتَان <small>— a one-word āyah, against verses of 100+ words</small>",
         bars=[("Qur'ān (DFA)", 95, "#1D9E75", "0.95 memory"), ("random text", 50, "#B4B2A9", "0.50")],
         eff="effect ≈ z 20 · regulated, not noise"),
    dict(id="A6", name="Connectivity", grade="A", meter=90,
         aspect="Do sūras wire to specific partners, like vessels between organs?",
         body="organs connect to specific partners, not at random",
         quran="specific sūra-pairs share many roots beyond a degree-matched null",
         arabic="ٱلْبَقَرَة ↔ آل عِمْرَان <small>— 342 shared roots</small>",
         bars=[("linked pairs", 44, "#1D9E75", "44% specific"), ("chance", 1, "#B4B2A9", "1%")],
         eff="44× above chance · survives length control"),
    dict(id="A7", name="Bilateral pairs", grade="A", meter=86,
         aspect="Are there matched identical pairs, like two eyes or two ears?",
         body="bodies carry matched bilateral pairs",
         quran="form-twin sūras share a distinctive opening template",
         arabic="طسم → ٢٦ · ٢٨ &nbsp; تَبَارَكَ → ٢٥ · ٦٧ &nbsp; وَٱلسَّمَاء → ٨٥ · ٨٦",
         bars=[("observed twins", 100, "#1D9E75", "14 pairs"), ("expected", 41, "#B4B2A9", "5.7 pairs")],
         eff="effect z = +5.4"),
]

_B_ITEMS = [
    dict(id="B", name="Identity", grade="B", meter=62,
         aspect="Does each sūra have a unique, non-redundant function?",
         body="each organ does a job no other does",
         quran="a held-out āyah classifies back to its home sūra above chance",
         arabic="قُلْ هُوَ ٱللَّهُ أَحَد <small>— each sūra keeps its own fingerprint</small>",
         bars=[("traced home", 72, "#1D9E75", "7.2%"), ("arbitrary", 49, "#B4B2A9", "4.9%")],
         eff="real but modest · z ≈ 7.7"),
    dict(id="B", name="Necessity", grade="B", meter=60,
         aspect="Is any sūra irreplaceable — remove it and a function is lost?",
         body="remove an organ and the body loses a function",
         quran="al-Fātiḥa is the single most-isolated sūra in function space",
         arabic="ٱلْفَاتِحَة <small>— most isolated, rank 1 / 114</small>",
         bars=[("Fātiḥa isolation", 100, "#1D9E75", "rank 1 / 114")],
         eff="one clear case; not yet a general law"),
    dict(id="B", name="Digestive loop", grade="B", meter=58,
         aspect="Does the text ingest a claim and return a processed response?",
         body="a body ingests material and processes it",
         quran="“ask” is answered by “say” within two verses, far above base-rate",
         arabic="سَأَلَ ↔ قُلْ <small>— “ask” → “say”</small>",
         bars=[("ask→say", 25, "#1D9E75", "25%"), ("base rate", 4, "#B4B2A9", "4%")],
         eff="local loop · ~6× base"),
    dict(id="B", name="Polarity", grade="B", meter=52,
         aspect="Does a sūra have a head–tail (anterior–posterior) axis?",
         body="organs have a head–tail body axis",
         quran="the first verse is markedly detectable; the last only faintly",
         arabic="أَوَّل ↔ آخِر <small>— a marked head, a faint tail</small>",
         bars=[("head", 75, "#1D9E75", "AUC 0.75"), ("tail", 61, "#B4B2A9", "AUC 0.61")],
         eff="head strong, tail weak · partial"),
    dict(id="B", name="Error-correction", grade="B", meter=64,
         aspect="Is there redundancy that can repair a damaged line?",
         body="bodies carry redundancy for self-repair",
         quran="most verse-endings are recoverable from the rhyme code",
         arabic="ـِينَ · ـُونَ <small>— rhyme endings that recover the line</small>",
         bars=[("from rhyme", 73, "#1D9E75", "73%"), ("baseline", 50, "#B4B2A9", "50%")],
         eff="real redundancy · +23 pts"),
    dict(id="B", name="Signal", grade="B", meter=55,
         aspect="Does content carry verse-to-verse, like a nervous signal?",
         body="a nervous system propagates a signal along a path",
         quran="adjacent verses share content well above chance",
         arabic="ذٰلِكَ · هُمْ <small>— anaphora linking adjacent āyāt</small>",
         bars=[("adjacent", 87, "#1D9E75", "0.087"), ("distant", 9, "#B4B2A9", "0.009")],
         eff="~10× above chance"),
]

_OUT_ITEMS = [
    dict(id="OUT", name="Location", grade="OUT", meter=15,
         aspect="Does each sūra sit in a fixed position, like the heart in the chest?",
         body="organs sit in fixed anatomical positions",
         quran="position is just the mushaf’s long→short ordering — nothing left after length",
         arabic="ٱلطُّوَل ↔ ٱلْمُفَصَّل <small>— long sūras first, short last</small>",
         bars=[("after length", 3, "#B4B2A9", "R² 0.03")],
         eff="length artifact · refine the instrument"),
    dict(id="OUT", name="Folding contact-decay", grade="OUT", meter=14,
         aspect="Does the 1-D text fold into a 3-D contact map, like the genome (Hi-C)?",
         body="a 1-D genome folds into a 3-D contact map",
         quran="the contact-decay curve was a length artifact — the network itself survives as A6",
         arabic="",
         bars=[("decay signal", 4, "#B4B2A9", "r −0.04")],
         eff="length artifact · network lives in A6"),
    dict(id="OUT", name="Development", grade="OUT", meter=16,
         aspect="Do sūras fall into developmental classes (early vs late forms)?",
         body="bodies develop through ontogenetic stages",
         quran="the two “classes” are just the length gradient again",
         arabic="",
         bars=[("class signal", 6, "#B4B2A9", "= length")],
         eff="length artifact"),
    dict(id="OUT", name="Skeleton (muqaṭṭaʿāt)", grade="OUT", meter=22,
         aspect="Do the disjoint-letter sūras form a rigid structural frame?",
         body="a body has a rigid structural skeleton",
         quran="strong in one half, fails split-half replication",
         arabic="ٱلٓمٓ · طٰسٓ · حٰمٓ <small>— the muqaṭṭaʿāt</small>",
         bars=[("odd sūras", 100, "#B4B2A9", "t 10.3"), ("even sūras", 17, "#D85A30", "t 1.7")],
         eff="fails split-half · not reproducible"),
    dict(id="OUT", name="Circulation", grade="OUT", meter=18,
         aspect="Does a core substance perfuse every region evenly, like blood?",
         body="blood circulates evenly to every tissue",
         quran="the core message clumps; the real “flow” is recitation (= A5 + A3)",
         arabic="",
         bars=[("evenness", 10, "#D85A30", "gap-CV z +63")],
         eff="clumped, not perfused · re-framed as A5+A3"),
]

_section("Bedrock (A) — the seven that hold", _A_ITEMS)
_section("Second tier (B) — real but modest", _B_ITEMS)
_section("Tested &amp; rejected (OUT) — what we looked for, why it failed", _OUT_ITEMS)

st.caption("Method (locked): body = benchmark, one-directional · PROVEN needs a proper null + honest effect + reproducible script · all-or-none (refine the instrument, never 'void'). Full ledger & scripts: research/correspondence/.")
