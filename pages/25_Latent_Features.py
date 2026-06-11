"""Latent Feature Ledger — intrinsic, self-referential discoveries.

Single source of truth: research/intrinsic/latent_features.json
Weekly cadence. Every feature carries a four-question critical review with a
numeric grade (pass >= 90 + novelty gate), a plain-English conceptual
foundation, its utility, score bars, and an impact chart.
"""
import html as _html
import json
import os
from datetime import date, datetime

import streamlit as st

try:
    import state as S
except Exception:  # pragma: no cover
    S = None

st.set_page_config(page_title="Latent Feature Ledger", page_icon="🧬", layout="wide")
if S:
    try:
        S.log_page("latent_features")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "research", "intrinsic", "latent_features.json")


@st.cache_data(show_spinner=False)
def load_ledger(path, mtime):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


try:
    L = load_ledger(DATA, os.path.getmtime(DATA))
except Exception as e:
    st.error("Could not load latent_features.json: %s" % e)
    st.stop()

feats = L.get("features", [])
by_id = {f.get("id"): f for f in feats}
PASS = L.get("review_rubric", {}).get("pass", 90)
RUBRIC = L.get("review_rubric", {}).get("criteria", {})

CAT_COLORS = {
    "Lexical baselines": "#9AA4B2",
    "Rhythm / wave": "#2A9D8F",
    "Rhyme / sound": "#E76F51",
    "Self-reference / network": "#6A4C93",
    "Constellation / matrix": "#457B9D",
    "Sūra definition": "#1D3557",
    "Order / sequence": "#F4A261",
    "Optimality / perturbation": "#2B9348",
    "Āyah": "#C1121F",
}

# Vivid per-feature palette so each bar pops (bars are otherwise category-uniform).
PALETTE = [
    "#E63946", "#F4A261", "#2A9D8F", "#457B9D", "#6A4C93", "#E76F51", "#06AED5",
    "#F72585", "#7209B7", "#3A0CA3", "#4361EE", "#4CC9F0", "#80B918", "#FF9F1C",
    "#D00000", "#9D4EDD", "#2B9348", "#FB5607", "#FF006E", "#8338EC", "#3A86FF",
    "#FFBE0B", "#118AB2", "#EF476F", "#06D6A0", "#073B4C", "#C1121F",
]


def feat_color(f):
    # stable, vivid colour keyed to the feature id (L03 -> palette[3])
    try:
        idx = int(str(f.get("id", "L0"))[1:])
    except Exception:
        idx = 0
    return PALETTE[idx % len(PALETTE)]


def grade_of(f):
    return f.get("review", {}).get("grade", 0)


def grade_color(g):
    return "#1D9E75" if g >= PASS else ("#E9A23B" if g >= 80 else "#9AA4B2")


included = [f for f in feats if f.get("in_table")]
excluded = [f for f in feats if not f.get("in_table")]
cat_order = L.get("category_order", [])


def _hero(t, s=""):
    if S:
        try:
            S.hero(t, s)
            return
        except Exception:
            pass
    st.markdown('<div class="lf-h1">%s</div>' % t, unsafe_allow_html=True)
    if s:
        st.markdown('<div class="lf-law">%s</div>' % s, unsafe_allow_html=True)


def _layer(n, label):
    if S:
        try:
            S.layer(n, label)
            return
        except Exception:
            pass
    st.markdown('<div class="lf-sec">%s</div>' % label, unsafe_allow_html=True)

# ---------------- page-local styling ----------------
st.markdown(
    """
<style>
.block-container{padding-top:1.1rem;max-width:1180px;}
#lfwrap, #lfwrap *{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;}
/* ===== LEDGER DESIGN SYSTEM — one scale, one rhythm, one palette =====
   Tokens:  ink #16243B (primary) · slate #25364A (secondary, never gray)
            navy #1D3557 (headings) · teal #1D9E75 (accent) · line #E7ECF3
   Scale:   title 30 · section 13 · cat 15 · lead 15.5 · body 14.5 · micro 12
   Rhythm:  blocks 6–8px apart; line-height 1.55 body, 1.5 dense.            */
.lf-h1{font-size:30px;font-weight:800;letter-spacing:-.5px;color:#16243B;margin:0 0 2px;}
.lf-law{font-size:13.5px;line-height:1.5;color:#25364A;margin:0 0 14px;max-width:880px;font-weight:500;}
.lf-kpis{display:flex;gap:10px;flex-wrap:wrap;margin:2px 0 14px;}
.lf-kpi{flex:1 1 150px;background:#fff;border:1px solid #E7ECF3;border-left:4px solid #1D9E75;
  border-radius:10px;padding:10px 14px;box-shadow:0 1px 2px rgba(20,40,80,.04);}
.lf-kpi .n{font-size:26px;font-weight:800;color:#16243B;line-height:1;}
.lf-kpi .l{font-size:11.5px;text-transform:uppercase;letter-spacing:.6px;color:#34465B;margin-top:5px;font-weight:700;}
.lf-kpi.amber{border-left-color:#E9A23B;} .lf-kpi.grey{border-left-color:#9AA4B2;} .lf-kpi.navy{border-left-color:#1D3557;}
.lf-sec{font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.8px;color:#1D3557;
  margin:18px 0 8px;padding-bottom:5px;border-bottom:2px solid #E7ECF3;}
.lf-cat{font-size:15px;font-weight:800;color:#16243B;margin:14px 0 6px;display:flex;align-items:center;gap:8px;}
.lf-catdot{width:11px;height:11px;border-radius:3px;display:inline-block;}
.lf-chip{display:inline-block;font-size:10.5px;font-weight:700;color:#27384B;background:#EEF2F7;
  border-radius:20px;padding:2px 9px;margin:0 4px 4px 0;text-transform:uppercase;letter-spacing:.4px;}
.lf-badge{display:inline-block;font-size:12px;font-weight:800;color:#fff;border-radius:7px;padding:2px 9px;}
.lf-lead{font-size:15.5px;line-height:1.55;color:#16243B;margin:6px 0;font-weight:500;}
.lf-why{background:#E7F6EF;border-left:4px solid #1D9E75;border-radius:8px;padding:8px 12px;
  font-size:14.5px;line-height:1.5;color:#0B3F2A;margin:7px 0;}
.lf-meta{font-size:14.5px;line-height:1.5;color:#25364A;margin:4px 0;}
.lf-q{font-size:14.5px;line-height:1.5;color:#1F2D3D;margin:4px 0;}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p{color:#243039!important;}
.ectitle,.ectitle span{color:#243039!important;}
.lf-q b{color:#1D3557;}
[data-testid="stVerticalBlock"]{gap:.3rem!important;}
[data-testid="stExpander"] [data-testid="stVerticalBlock"]{gap:.15rem!important;}
.ar-wrap{margin:3px 0 10px;line-height:2;}
.ar-chip{display:inline-block;font-size:22px;color:#16365C;background:#EEF3FB;border:1px solid #DEE7F2;
  border-radius:9px;padding:2px 13px;margin:3px;font-family:"Traditional Arabic","Amiri","Scheherazade New",serif;}
.ar-chip sub{font-size:10px;color:#5A6573;font-weight:700;font-family:-apple-system,Segoe UI,sans-serif;}
.twinbox{background:#F5F8FC;border-left:4px solid #457B9D;border-radius:7px;padding:4px 11px;margin:3px 0;
  display:flex;align-items:center;gap:10px;}
.twinref{flex:0 0 auto;font-size:12px;font-weight:800;color:#1D3557;}
.twinar{flex:1 1 auto;font-size:16px;line-height:1.5;color:#10181F;white-space:nowrap;
  font-family:"Traditional Arabic","Amiri","Scheherazade New",serif;}
.rh-chip{display:inline-block;font-size:20px;color:#fff;border-radius:6px;padding:0 9px;margin:2px;font-family:"Traditional Arabic","Amiri",serif;}
.seam{display:inline-block;width:8px;height:15px;margin:1px;border-radius:2px;}
.seam-wrap{margin:4px 0 8px;line-height:1;}
.sbwrap{margin:8px 0 2px;}
.sbrow{display:flex;align-items:center;gap:8px;margin:2px 0;}
.sblabel{flex:0 0 150px;font-size:11px;color:#5B6675;text-align:right;}
.sbtrack{flex:1 1 auto;height:9px;border-radius:6px;overflow:hidden;background:
  linear-gradient(90deg,transparent calc(25% - 1px),#D5DDE8 25%,transparent calc(25% + 1px)),
  linear-gradient(90deg,transparent calc(50% - 1px),#D5DDE8 50%,transparent calc(50% + 1px)),
  linear-gradient(90deg,transparent calc(75% - 1px),#D5DDE8 75%,transparent calc(75% + 1px)),#EDF1F6;}
.sbfill{display:block;height:100%;background:linear-gradient(90deg,#2A9D8F,#1D9E75);}
.sbval{flex:0 0 42px;font-size:11px;color:#3D4757;font-weight:700;}
.lf-concept{font-size:16.5px;line-height:1.5;color:#13202E;background:#F5F8FC;
  border-left:4px solid #1D3557;border-radius:8px;padding:9px 13px;margin:4px 0 7px;}
.lf-concept .lab{display:block;font-size:10.5px;font-weight:800;letter-spacing:.6px;
  text-transform:uppercase;color:#1D3557;margin-bottom:2px;}
.ecwrap{margin:7px 0;}
.ectitle{font-size:12.5px;font-weight:700;color:#46505F;margin-bottom:4px;}
.ecrow{display:flex;align-items:center;gap:8px;margin:2px 0;}
.eclabel{flex:0 0 112px;font-size:12.5px;color:#46505F;text-align:right;}
.ectrack{flex:1 1 auto;height:9px;border-radius:5px;overflow:hidden;background:
  linear-gradient(90deg,transparent calc(25% - 1px),#D5DDE8 25%,transparent calc(25% + 1px)),
  linear-gradient(90deg,transparent calc(50% - 1px),#D5DDE8 50%,transparent calc(50% + 1px)),
  linear-gradient(90deg,transparent calc(75% - 1px),#D5DDE8 75%,transparent calc(75% + 1px)),#EDF1F6;}
.ecfill{display:block;height:100%;border-radius:5px;}
.ecval{flex:0 0 54px;font-size:12.5px;color:#16243B;font-weight:700;}
</style>
<div id="lfwrap"></div>
""",
    unsafe_allow_html=True,
)

_hero("🧬 Determinacy",
      "Intrinsic, self-referential discoveries — graded, novelty-gated, and surfaced live in the modules.")
st.markdown(
    "<div style='font-size:14.5px;color:#46505F;margin:2px 0 14px'>"
    "<b style='color:#16243B'>%d graded determinacy features (≥ 90)</b> — each found by measuring the "
    "text only against itself. Tap a card to explore.</div>" % len(included), unsafe_allow_html=True)

# det-journey: where this ledger started -> where we are
st.markdown(r'''<svg viewBox="0 0 1120 140" xmlns="http://www.w3.org/2000/svg" style="width:100%;background:#fff;border:1px solid #E7ECF3;border-radius:12px;margin:2px 0 14px" font-family="-apple-system,Segoe UI,Roboto,sans-serif">
 <line x1="70" y1="80" x2="1040" y2="80" stroke="#E7ECF3" stroke-width="3"/>
 <g text-anchor="middle">
  <g><circle cx="70" cy="80" r="8" fill="#9AA4B2"/><text x="70" y="42" font-size="11.5" font-weight="800" fill="#16243B">External sweep</text><text x="70" y="106" font-size="10" fill="#5B6675">is it distinctive?</text></g>
  <g><circle cx="232" cy="80" r="8" fill="#E9A23B"/><text x="232" y="42" font-size="11.5" font-weight="800" fill="#16243B">Jun 7 · One Law</text><text x="232" y="106" font-size="10" fill="#5B6675">internal only</text></g>
  <g><circle cx="394" cy="80" r="8" fill="#1D9E75"/><text x="394" y="42" font-size="11.5" font-weight="800" fill="#16243B">Wave &amp; rhyme</text><text x="394" y="106" font-size="10" fill="#5B6675">L01-07</text></g>
  <g><circle cx="556" cy="80" r="8" fill="#1D9E75"/><text x="556" y="42" font-size="11.5" font-weight="800" fill="#16243B">Self-ref · twins</text><text x="556" y="106" font-size="10" fill="#5B6675">L08·21</text></g>
  <g><circle cx="718" cy="80" r="8" fill="#1D9E75"/><text x="718" y="42" font-size="11.5" font-weight="800" fill="#16243B">Sūra &amp; Āyah</text><text x="718" y="106" font-size="10" fill="#5B6675">defined to necessity</text></g>
  <g><circle cx="880" cy="80" r="8" fill="#1D9E75"/><text x="880" y="42" font-size="11.5" font-weight="800" fill="#16243B">Arrangement</text><text x="880" y="106" font-size="10" fill="#5B6675">determined L14-26</text></g>
  <g><text x="1040" y="68" font-size="20" fill="#1D3557">★</text><text x="1040" y="42" font-size="11.5" font-weight="800" fill="#1D3557">NOW</text><text x="1040" y="106" font-size="10" fill="#1D3557">the wall: meaning</text></g>
 </g>
</svg>
''', unsafe_allow_html=True)


# (meta stats, grade chart, coverage and freshness moved to the "Method & overview" tab —
#  the landing leads with the discoveries themselves.)
new_n = sum(1 for f in feats if f.get("status") == "new")

# ---------------- viz data (used by the feature cards) ----------------
try:
    VZ = json.load(open(os.path.join(os.path.dirname(DATA), "viz_data.json"), encoding="utf-8"))
except Exception:
    VZ = None

# landing carries no filter chrome; matches() defaults to all
sel_dim, query = [], ""


def matches(f):
    return (not sel_dim or any(d in sel_dim for d in f.get("dimensions", []))) and (
        query.lower() in (f.get("name", "") + f.get("plain", "") + f.get("user_value", "")).lower())


def _render_method():
    """Grades, coverage and text visuals — demoted off the landing into the Method tab."""
    try:
        import plotly.graph_objects as go
        cc1, cc2 = st.columns([3, 2])
        with cc1:
            st.markdown('<div class="lf-sec">Impact — critical-review grade by feature</div>', unsafe_allow_html=True)
            ordered = sorted(included, key=grade_of)
            fig = go.Figure(go.Bar(
                x=[grade_of(f) for f in ordered],
                y=["%s · %s" % (f["id"], f["name"][:26]) for f in ordered],
                orientation="h",
                marker=dict(color=[grade_color(grade_of(f)) for f in ordered],
                            line=dict(color="rgba(0,0,0,.10)", width=1)),
                text=[grade_of(f) for f in ordered], textposition="outside",
                hovertext=[f.get("plain", "") for f in ordered], hoverinfo="text"))
            fig.add_vline(x=PASS, line_dash="dash", line_color="#C1121F",
                          annotation_text="pass %d" % PASS, annotation_position="top")
            fig.update_layout(height=26 * len(ordered) + 60, margin=dict(l=4, r=24, t=8, b=20),
                              xaxis=dict(range=[60, 102], title=None, showgrid=True, gridcolor="#EEF1F6"),
                              yaxis=dict(title=None), plot_bgcolor="white", paper_bgcolor="white",
                              font=dict(size=11, color="#27313F"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="impact_chart")
        with cc2:
            st.markdown('<div class="lf-sec">Coverage across the text\'s axes</div>', unsafe_allow_html=True)
            cov = L.get("coverage", {})
            ax = list(cov.keys())
            figc = go.Figure(go.Bar(
                x=[cov[a] for a in ax], y=[a.title() for a in ax], orientation="h",
                marker=dict(color="#2A9D8F", line=dict(color="rgba(0,0,0,.10)", width=1)),
                text=[cov[a] for a in ax], textposition="outside"))
            figc.update_layout(height=26 * len(ax) + 60, margin=dict(l=4, r=24, t=8, b=20),
                               xaxis=dict(title=None, showgrid=True, gridcolor="#EEF1F6"),
                               yaxis=dict(title=None, autorange="reversed"),
                               plot_bgcolor="white", paper_bgcolor="white", font=dict(size=11, color="#27313F"))
            st.plotly_chart(figc, use_container_width=True, config={"displayModeBar": False}, key="coverage_chart")
    except Exception:
        st.bar_chart({f["id"]: grade_of(f) for f in included})
    if VZ:
        st.markdown('<div class="lf-sec">From the actual text</div>', unsafe_allow_html=True)
        try:
            import plotly.graph_objects as go
            v1, v2 = st.columns(2)
            with v1:
                st.caption("The 114 sūras as a landscape — each dot a sūra; the main axis tracks the canonical order (r = %.2f). L09." % VZ.get("pc1_order_r", 0))
                land = VZ["landscape"]
                xs = [p[1] for p in land]; ys = [p[2] for p in land]; sn = [p[0] for p in land]; sz = [p[3] for p in land]
                fig = go.Figure(go.Scatter(x=xs, y=ys, mode="markers",
                    marker=dict(size=[max(6, min(20, s ** 0.5 + 4)) for s in sz], color=sn, colorscale="Viridis",
                                showscale=True, colorbar=dict(title="sūra #"), line=dict(width=.5, color="#fff")),
                    text=["sūra %d · %d verses" % (n, s) for n, s in zip(sn, sz)], hoverinfo="text"))
                fig.update_layout(height=330, margin=dict(l=4, r=4, t=6, b=4), plot_bgcolor="white", paper_bgcolor="white",
                    xaxis=dict(title="PC1 — size / richness", showgrid=True, gridcolor="#EEF1F6"),
                    yaxis=dict(title="PC2", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=11))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="content_landscape")
            with v2:
                st.caption("Verse-length rhythm across the whole Qur'ān (the wave behind L03/L04) — words per verse, in order.")
                figw = go.Figure(go.Scatter(y=VZ["wave"], mode="lines", line=dict(color="#2A9D8F", width=.9)))
                figw.update_layout(height=110, margin=dict(l=4, r=4, t=4, b=4), plot_bgcolor="white", paper_bgcolor="white",
                    xaxis=dict(visible=False), yaxis=dict(title="words/verse", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=11))
                st.plotly_chart(figw, use_container_width=True, config={"displayModeBar": False}, key="content_wave")
                st.caption("Sūra openings (L18) — the actual opening words, with counts:")
                ow = "".join('<span class="ar-chip">%s<sub>%d</sub></span>' % (w, c) for w, c in VZ["onset_words"][:12])
                st.markdown('<div dir="rtl" class="ar-wrap">%s</div>' % ow, unsafe_allow_html=True)
        except Exception:
            pass
        st.caption("The vocabulary backbone — most frequent roots (behind the root channels of L15/L18/L20):")
        rr = "".join('<span class="ar-chip">%s<sub>%d</sub></span>' % (w, c) for w, c in VZ["top_roots"][:16])
        st.markdown('<div dir="rtl" class="ar-wrap">%s</div>' % rr, unsafe_allow_html=True)


def evidence_chart(ch, measured_color="#1D9E75"):
    items = ch.get("items", [])
    if not items:
        return ""
    vmax = max(abs(v) for _, v, _ in items) or 1.0
    rows = ""
    for label, v, kind in items:
        pct = int(round(100.0 * abs(v) / vmax))
        col = measured_color if kind == "measured" else "#B7C0CC"
        disp = ("%.2f" % v) if abs(v) < 100 else "{:,}".format(int(v))
        rows += ('<div class="ecrow"><span class="eclabel">%s</span>'
                 '<span class="ectrack"><span class="ecfill" style="width:%d%%;background:%s"></span></span>'
                 '<span class="ecval">%s</span></div>') % (label, pct, col, disp)
    return '<div class="ecwrap"><div class="ectitle">%s &nbsp;<span style="color:#1D9E75">■</span>measured <span style="color:#B7C0CC">■</span>floor</div>%s</div>' % (ch.get("title", ""), rows)


def score_bars(scores, color="#1D9E75"):
    rows = ""
    for k, v in scores.items():
        m = RUBRIC.get(k, v) or v
        pct = int(round(100.0 * v / m)) if m else 0
        rows += ('<div class="sbrow"><span class="sblabel">%s</span>'
                 '<span class="sbtrack"><span class="sbfill" style="width:%d%%;'
                 'background:%s"></span></span><span class="sbval">%d/%d</span></div>') % (
            k.replace("_", " "), pct, color, v, m)
    return '<div class="sbwrap">%s</div>' % rows


def feature_content(fid):
    """Show real Qur'ānic content inside the feature that it instantiates."""
    if not VZ:
        return
    try:
        import plotly.graph_objects as go
    except Exception:
        go = None
    if fid == "L09" and go:
        st.markdown('<div class="lf-meta"><b>The actual landscape</b> — each dot a sūra (colour = sūra number); the main axis tracks the canonical order.</div>', unsafe_allow_html=True)
        land = VZ["landscape"]
        fig = go.Figure(go.Scatter(x=[p[1] for p in land], y=[p[2] for p in land], mode="markers",
            marker=dict(size=[max(5, min(16, p[3] ** 0.5 + 3)) for p in land], color=[p[0] for p in land],
                        colorscale="Viridis", showscale=True, colorbar=dict(title="sūra #", thickness=10),
                        line=dict(width=.4, color="#fff")),
            text=["sūra %d · %d v" % (p[0], p[3]) for p in land], hoverinfo="text"))
        fig.update_layout(height=190, margin=dict(l=4, r=4, t=6, b=4), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="PC1 — size / richness", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="PC2", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10, color="#1D3557"), showlegend=False)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key="fc_land_%s" % fid)
    elif fid == "L03" and go:
        st.markdown('<div class="lf-meta"><b>The actual verse-length signal</b> — words per verse, in order (the wave whose memory is L03).</div>', unsafe_allow_html=True)
        fw = go.Figure(go.Scatter(y=VZ["wave"], mode="lines", line=dict(color="#2A9D8F", width=.8)))
        fw.update_layout(height=105, margin=dict(l=4, r=4, t=4, b=4), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="verse (in order)", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="words / verse", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10, color="#1D3557"))
        st.plotly_chart(fw, use_container_width=True, config={"displayModeBar": False}, key="fc_wave_L03")
    elif fid == "L04" and go and VZ.get("spectrum"):
        st.markdown('<div class="lf-meta"><b>The actual power spectrum</b> (log–log) — energy falls as 1/f^%.2f; a straight downward line is the pink-noise fingerprint.</div>' % VZ.get("spectrum_slope", 0), unsafe_allow_html=True)
        sp = VZ["spectrum"]
        fs = go.Figure(go.Scatter(x=[p[0] for p in sp], y=[p[1] for p in sp], mode="lines+markers",
            line=dict(color="#E76F51", width=1.2), marker=dict(size=5, color="#E76F51")))
        fs.update_layout(height=110, margin=dict(l=2, r=2, t=2, b=2), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="log frequency", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="log power", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10))
        st.plotly_chart(fs, use_container_width=True, config={"displayModeBar": False}, key="fc_spec_L04")
    elif fid == "L18":
        st.markdown('<div class="lf-meta"><b>The actual opening words</b> (with counts):</div>', unsafe_allow_html=True)
        chips = "".join('<span class="ar-chip">%s<sub>%d</sub></span>' % (w, c) for w, c in VZ["onset_words"][:12])
        st.markdown('<div dir="rtl" class="ar-wrap">%s</div>' % chips, unsafe_allow_html=True)
    elif fid in ("L05", "L15", "L20"):
        st.markdown('<div class="lf-meta"><b>The actual roots</b> behind this channel (most frequent):</div>', unsafe_allow_html=True)
        chips = "".join('<span class="ar-chip">%s<sub>%d</sub></span>' % (w, c) for w, c in VZ["top_roots"][:12])
        st.markdown('<div dir="rtl" class="ar-wrap">%s</div>' % chips, unsafe_allow_html=True)
    elif fid == "L07" and go and VZ.get("l07_coupling"):
        cw = VZ["l07_coupling"]; labels = ["different", "same last", "same last 2", "same last 3"]
        st.markdown('<div class="lf-meta"><b>Rhyme predicts theme</b> — the more two verses share their ending, the more they share vocabulary roots. Sound and meaning rise together.</div>', unsafe_allow_html=True)
        f7 = go.Figure(go.Scatter(x=[labels[r[0]] for r in cw], y=[r[1] for r in cw], mode="lines+markers",
            line=dict(color="#F72585", width=2.2), marker=dict(size=10), text=["%.1f%%" % r[1] for r in cw], textposition="top center"))
        f7.update_layout(height=115, margin=dict(l=4, r=4, t=8, b=4), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="rhyme level (matching final letters)", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="% of pairs sharing a root", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10, color="#1D3557"))
        st.plotly_chart(f7, use_container_width=True, config={"displayModeBar": False}, key="fc_coup_L07")
    elif fid == "L21" and VZ.get("twin_pair"):
        tp = VZ["twin_pair"]
        st.markdown('<div class="lf-meta"><b>A real structural twin pair</b> — different sūras, sharing %d roots:</div>' % len(tp["shared_roots"]), unsafe_allow_html=True)
        for side in ("a", "b"):
            vv = tp[side]
            st.markdown('<div class="twinbox"><span class="twinref">%s</span><span dir="rtl" class="twinar">%s</span></div>' % (vv["ref"], vv["text"]), unsafe_allow_html=True)
        st.markdown('<div class="lf-meta">shared roots:</div><div dir="rtl" class="ar-wrap">%s</div>'
                    % "".join('<span class="ar-chip">%s</span>' % r for r in tp["shared_roots"]), unsafe_allow_html=True)
    elif fid == "L06" and VZ.get("rhyme_strip"):
        st.markdown('<div class="lf-meta"><b>A rhyme run</b> — final letter of 30 consecutive verses (Sūra 19); same colour = same rhyme:</div>', unsafe_allow_html=True)
        pal = {}; cols = ["#E76F51", "#2A9D8F", "#457B9D", "#F4A261", "#6A4C93", "#C1121F", "#118AB2", "#80B918"]
        out = ""
        for r, c in VZ["rhyme_strip"]:
            if c not in pal:
                pal[c] = cols[len(pal) % len(cols)]
            out += '<span class="rh-chip" style="background:%s">%s</span>' % (pal[c], c)
        st.markdown('<div dir="rtl" class="ar-wrap">%s</div>' % out, unsafe_allow_html=True)
    elif fid == "L17" and VZ.get("fasila"):
        st.markdown('<div class="lf-meta"><b>The actual verse endings</b> (fāṣila), with counts — the vowels (-ūna / -īna) are the rhyme:</div>', unsafe_allow_html=True)
        chips = "".join('<span class="ar-chip">%s<sub>%d</sub></span>' % (w, c) for w, c in VZ["fasila"][:12])
        st.markdown('<div dir="rtl" class="ar-wrap">%s</div>' % chips, unsafe_allow_html=True)
    elif fid == "L01" and go and VZ.get("zipf"):
        st.markdown('<div class="lf-meta"><b>The actual rank–frequency curve</b> (log–log) — the straight downward line is Zipf\'s −1 law:</div>', unsafe_allow_html=True)
        z = VZ["zipf"]
        fz = go.Figure(go.Scatter(x=[p[0] for p in z], y=[p[1] for p in z], mode="markers", marker=dict(size=3, color="#457B9D")))
        fz.update_layout(height=110, margin=dict(l=2, r=2, t=2, b=2), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="log rank", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="log frequency", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10))
        st.plotly_chart(fz, use_container_width=True, config={"displayModeBar": False}, key="fc_zipf_L01")
        st.markdown('<div class="lf-meta">most frequent words:</div><div dir="rtl" class="ar-wrap">%s</div>'
                    % "".join('<span class="ar-chip">%s<sub>%d</sub></span>' % (w, c) for w, c in VZ["zipf_top"][:12]), unsafe_allow_html=True)
    elif fid == "L13" and go and VZ.get("perturb"):
        p = VZ["perturb"]
        st.markdown('<div class="lf-meta"><b>Operator × invariant</b> — each edit breaks the patterns it touches (green=intact, red=destroyed):</div>', unsafe_allow_html=True)
        Z = [r[1:] for r in p["rows"]]; ops = [r[0] for r in p["rows"]]
        fh = go.Figure(go.Heatmap(z=Z, x=p["invariants"], y=ops, colorscale="RdYlGn", zmin=0, zmax=1,
            text=Z, texttemplate="%{text}", textfont=dict(size=11),
            colorbar=dict(title="intact→broken", thickness=10)))
        fh.update_layout(height=120, margin=dict(l=2, r=2, t=2, b=2), font=dict(size=11), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fh, use_container_width=True, config={"displayModeBar": False}, key="fc_pert_L13")
    elif fid == "L02" and go and VZ.get("heaps"):
        st.markdown('<div class="lf-meta"><b>The actual vocabulary-growth curve</b> — new words keep arriving but slow down (Heaps β = 0.74):</div>', unsafe_allow_html=True)
        h = VZ["heaps"]
        fh2 = go.Figure(go.Scatter(x=[p[0] for p in h], y=[p[1] for p in h], mode="lines", line=dict(color="#6A4C93", width=1.6)))
        fh2.update_layout(height=110, margin=dict(l=2, r=2, t=2, b=2), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="words read", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="distinct words", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10))
        st.plotly_chart(fh2, use_container_width=True, config={"displayModeBar": False}, key="fc_heaps_L02")
    elif fid == "L08" and go and VZ.get("recurrence2"):
        st.markdown('<div class="lf-meta"><b>Self-reference decays with distance</b> — recurrence over shuffle by window (1 = no clustering); locality fades by ~256:</div>', unsafe_allow_html=True)
        rc = VZ["recurrence2"]
        fr = go.Figure(go.Scatter(x=[p[0] for p in rc], y=[p[1] for p in rc], mode="lines+markers", line=dict(color="#118AB2", width=1.4), marker=dict(size=5)))
        fr.add_hline(y=1.0, line_dash="dash", line_color="#C1121F")
        fr.update_layout(height=110, margin=dict(l=2, r=2, t=2, b=2), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="window (tokens, log)", type="log", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="recurrence × shuffle", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10))
        st.plotly_chart(fr, use_container_width=True, config={"displayModeBar": False}, key="fc_recur_L08")
    elif fid == "L22" and go and VZ.get("chaining"):
        ch = VZ["chaining"]
        st.markdown('<div class="lf-meta"><b>The verse weave</b> — neighbouring verses share roots far above the order-shuffle floor (dashed); the bond fades smoothly as verses get farther apart. Reorder the verses and the weave collapses to the floor.</div>', unsafe_allow_html=True)
        fc22 = go.Figure(go.Scatter(x=ch["gaps"], y=ch["sharing"], mode="lines+markers",
            line=dict(color="#2A9D8F", width=2.4), marker=dict(size=10, color="#2A9D8F"),
            text=["%.0f%%" % (v * 100) for v in ch["sharing"]], textposition="top center",
            name="actual order"))
        fc22.add_hline(y=ch["floor"], line_dash="dash", line_color="#C1121F",
            annotation_text="within-sūra order shuffle (chance)", annotation_position="bottom right",
            annotation_font_size=9)
        fc22.update_layout(height=120, margin=dict(l=4, r=4, t=8, b=4), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="verse distance (gap)", dtick=1, showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="% pairs sharing a root", showgrid=True, gridcolor="#EEF1F6"),
            font=dict(size=10, color="#1D3557"), showlegend=False)
        st.plotly_chart(fc22, use_container_width=True, config={"displayModeBar": False}, key="fc_chain_L22")
        sp = ch["split"]
        st.markdown('<div class="lf-meta">adjacency lift <b>z=%.0f</b> · per-sūra paired <b>t=11.5</b> (83/95 sūras) · sign-test <b>p=3·10⁻¹⁴</b> · Cohen <b>d=1.18</b> · holds in both halves (odd z=%.0f, even z=%.0f).</div>'
                    % (ch["adj_z"], sp["odd_z"], sp["even_z"]), unsafe_allow_html=True)
        if VZ.get("fatiha_case"):
            fc = VZ["fatiha_case"]
            st.markdown('<div class="lf-meta" style="margin-top:6px"><b>Case study — Sūrat al-Fātiḥa (al-Ḥamd).</b> Only 2 of 6 neighbour-pairs share a root: <b>ءله</b> anchors the head (1–2), <b>صرط</b> anchors the foot (6–7). The middle moves by distinct fields (praise→mercy→sovereignty→worship→guidance). It is <b>ring-framed, not chained</b> — a different mode from the narrative weave, and far too short (6 pairs) to register the corpus statistic.</div>', unsafe_allow_html=True)
            anch = {"ءله", "صرط"}
            _rows = ""
            for v in fc["verses"]:
                _a = [r for r in v["roots"] if r in anch]
                _tag = ("<span style='color:#C77B1A;font-size:11px;font-weight:700;white-space:nowrap'>⚓ %s</span>" % " ".join(_a)) if _a else ""
                _rows += ("<div style='display:flex;align-items:center;gap:8px;padding:2px 0;border-bottom:1px solid #F0F3F8'>"
                          "<span style='color:#5A6573;font-size:11px;min-width:34px'>%s</span>"
                          "<span dir='rtl' style='flex:1;font-family:\"Traditional Arabic\",Amiri,serif;font-size:17px;color:#10171F'>%s</span>"
                          "%s</div>") % (v["ref"], v["text"], _tag)
            st.markdown("<div style='margin:2px 0 4px'>%s</div>" % _rows, unsafe_allow_html=True)
            st.markdown('<div class="lf-meta"><b>Critical review:</b> a 7-verse sūra is a category mismatch for a corpus-level statistic — al-Fātiḥa sits among the short sūras L22 does not resolve. The two anchor-links it does show are structurally real (head/foot inclusio), so the case illustrates the <b>scale boundary</b> of L22 rather than confirming or refuting it. The weave lives in longer sūras (al-Mulk 0.62, al-Naml 0.63).</div>', unsafe_allow_html=True)
    elif fid == "L23" and go and VZ.get("granularity"):
        gr = VZ["granularity"]
        st.markdown('<div class="lf-meta"><b>Order stays determined across granularity</b> — shuffle passages of size b <i>within</i> a sūra (vocabulary fixed); adjacent passages are still more similar than reshuffled ones at every scale (per-sūra paired z).</div>', unsafe_allow_html=True)
        _gb = gr.get("global_b", gr["b"]); _gz = gr.get("global_z", gr["z"])
        fg = go.Figure(go.Scatter(x=_gb, y=_gz, mode="lines+markers",
            line=dict(color="#F4A261", width=2.4), marker=dict(size=6, color="#F4A261"), fill="tozeroy",
            fillcolor="rgba(244,162,97,.12)"))
        fg.add_hline(y=2.0, line_dash="dash", line_color="#C1121F")
        fg.update_layout(height=150, margin=dict(l=6, r=10, t=14, b=6), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="passage size (verses, log)", type="log", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="significance z", showgrid=True, gridcolor="#EEF1F6"),
            font=dict(size=10, color="#1D3557"), showlegend=False)
        st.plotly_chart(fg, use_container_width=True, config={"displayModeBar": False}, key="fc_gran_L23")
        st.markdown('<div class="lf-meta">Globally the order is non-random from single verses up to 100-verse sections (z 73→8). The text is sequenced as <b>nested units</b>: words in verses, verses in passages, passages in sūras.</div>', unsafe_allow_html=True)
    elif fid == "L10" and go and VZ.get("landscape") and len(VZ["landscape"][0]) >= 5:
        st.markdown('<div class="lf-meta"><b>The two sūra-types in the landscape</b> — colour = unsupervised cluster (short/dense vs long/rich):</div>', unsafe_allow_html=True)
        land = VZ["landscape"]; cc = ["#E76F51", "#2A9D8F"]; names = ["short / dense", "long / rich"]
        f10 = go.Figure()
        for cl in (0, 1):
            pts = [p for p in land if len(p) > 4 and p[4] == cl]
            f10.add_trace(go.Scatter(x=[p[1] for p in pts], y=[p[2] for p in pts], mode="markers", name=names[cl],
                marker=dict(size=[max(5, min(15, p[3] ** 0.5 + 3)) for p in pts], color=cc[cl], line=dict(width=.4, color="#fff")),
                text=["sūra %d · %d v" % (p[0], p[3]) for p in pts], hoverinfo="text"))
        f10.update_layout(height=190, margin=dict(l=4, r=4, t=6, b=4), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="PC1 — size / richness", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="PC2", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10, color="#1D3557"),
            legend=dict(orientation="h", y=1.12, font=dict(size=10)))
        st.plotly_chart(f10, use_container_width=True, config={"displayModeBar": False}, key="fc_clust_L10")
    elif fid == "L11" and go and VZ.get("disc_hist"):
        dh = VZ["disc_hist"]
        st.markdown('<div class="lf-meta"><b>How the seam stands out</b> — the discontinuity signal at real boundaries (orange) vs ordinary transitions (grey). The gap is the AUC.</div>', unsafe_allow_html=True)
        f11 = go.Figure()
        f11.add_trace(go.Scatter(x=dh["centers"], y=dh["internal"], mode="lines", fill="tozeroy", name="ordinary", line=dict(color="#B7C0CC")))
        f11.add_trace(go.Scatter(x=dh["centers"], y=dh["boundary"], mode="lines", fill="tozeroy", name="boundary", line=dict(color="#E76F51")))
        f11.update_layout(height=115, margin=dict(l=2, r=2, t=2, b=2), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="discontinuity signal", showgrid=True, gridcolor="#EEF1F6"), yaxis=dict(showticklabels=False),
            font=dict(size=10), legend=dict(font=dict(size=10), orientation="h", y=1.1))
        st.plotly_chart(f11, use_container_width=True, config={"displayModeBar": False}, key="fc_disc_L11")
    elif fid == "L12" and go and VZ.get("disc_offset"):
        oc = VZ["disc_offset"]
        st.markdown('<div class="lf-meta"><b>The boundary sits on a peak</b> — discontinuity signal vs how many verses off the true seam; it maxes at 0:</div>', unsafe_allow_html=True)
        f12 = go.Figure(go.Scatter(x=[p[0] for p in oc], y=[p[1] for p in oc], mode="lines+markers", line=dict(color="#2B9348", width=1.6), marker=dict(size=5)))
        f12.update_layout(height=110, margin=dict(l=2, r=2, t=2, b=2), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="verses off true boundary", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title="signal", showgrid=True, gridcolor="#EEF1F6"), font=dict(size=10))
        st.plotly_chart(f12, use_container_width=True, config={"displayModeBar": False}, key="fc_offset_L12")
    elif fid == "L19" and go and VZ.get("band_positions"):
        bp = VZ["band_positions"]
        st.markdown('<div class="lf-meta"><b>The complexity spectrum</b> — where the canonical order sits between a sorted "crystal" (0) and a random "gas" (1), in each channel. It lands in the meaningful middle.</div>', unsafe_allow_html=True)
        chans = list(bp.keys()); xs = [bp[c] for c in chans]
        f19 = go.Figure()
        f19.add_vrect(x0=0.2, x1=0.8, fillcolor="#EAF7F1", opacity=.7, line_width=0)
        f19.add_trace(go.Scatter(x=xs, y=chans, mode="markers+text", marker=dict(size=14, color="#7209B7", line=dict(width=1, color="#fff")),
            text=["%.2f" % x for x in xs], textposition="middle right", hoverinfo="x+y"))
        f19.update_layout(height=110, margin=dict(l=4, r=4, t=18, b=4), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(range=[-0.05, 1.05], title="sorted ‹crystal›  0 ——— 1  ‹gas› random", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(title=None), font=dict(size=11, color="#1D3557"))
        st.plotly_chart(f19, use_container_width=True, config={"displayModeBar": False}, key="fc_band_L19")
    elif fid == "L14" and go and VZ.get("order_bits"):
        ob = VZ["order_bits"]; order = ["length-sorted", "rhyme-sorted", "canonical", "random"]
        st.markdown('<div class="lf-meta"><b>The order-load axis</b> (MDL bits — lower = more compressible). The canonical order sits between random (worse) and sorted (better): non-arbitrary, but deliberately not maximally compressible.</div>', unsafe_allow_html=True)
        xs = [ob[k] for k in order]; colr = ["#B7C0CC", "#B7C0CC", "#E63946", "#B7C0CC"]
        f14 = go.Figure(go.Scatter(x=xs, y=[0] * len(order), mode="markers+text", marker=dict(size=15, color=colr, line=dict(width=1, color="#fff")),
            text=order, textposition="top center", hoverinfo="x"))
        f14.update_layout(height=105, margin=dict(l=4, r=4, t=24, b=4), plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="MDL data-cost (bits) — lower = more compressible", showgrid=True, gridcolor="#EEF1F6"),
            yaxis=dict(visible=False, range=[-1, 1]), font=dict(size=11, color="#1D3557"))
        st.plotly_chart(f14, use_container_width=True, config={"displayModeBar": False}, key="fc_orderaxis_L14")
    elif fid == "L16" and VZ.get("seams"):
        st.markdown('<div class="lf-meta"><b>The 113 sūra seams</b> — each square one boundary: <span style="color:#C1121F">■</span> sound-marked (hard), <span style="color:#B7C0CC">■</span> meaning-marked (soft):</div>', unsafe_allow_html=True)
        strip = "".join('<span class="seam" style="background:%s"></span>' % ("#C1121F" if s else "#B7C0CC") for s in VZ["seams"])
        st.markdown('<div class="seam-wrap">%s</div>' % strip, unsafe_allow_html=True)


def render_card(f):
    g = grade_of(f)
    rv = f.get("review", {})
    badge = '<span class="lf-badge" style="background:%s">%d/100</span>' % (grade_color(g), g)
    chips = "".join('<span class="lf-chip">%s</span>' % d for d in f.get("dimensions", []))
    with st.expander("%s · %s    —    grade %d" % (f.get("id"), f.get("name"), g)):
        st.markdown('%s &nbsp; %s' % (badge, chips), unsafe_allow_html=True)
        st.markdown('<div class="lf-lead"><b>In plain English:</b> %s</div>' % f.get("plain", ""), unsafe_allow_html=True)
        st.markdown('<div class="lf-why"><b>Why it matters:</b> %s</div>' % f.get("user_value", ""),
                    unsafe_allow_html=True)
        # Real charts only — the two-bar "measured vs floor" readout is gone. Every feature shows
        # a real chart (feature_content) or, for the one holdout (L07), states its number inline.
        # Constrain to ~60% width so charts (esp. the heatmap) don't sprawl across the row.
        _cc, _ = st.columns([3, 2])
        with _cc:
            feature_content(f.get("id"))
        st.markdown('<div class="lf-meta"><b>Measurement:</b> %s &nbsp;·&nbsp; <b>Shuffle floor:</b> %s '
                    '&nbsp;·&nbsp; <b>Universe analog:</b> %s</div>'
                    % (f.get("value"), f.get("shuffle_floor"), f.get("universe_analog")),
                    unsafe_allow_html=True)
        ev = f.get("evidence", {})
        if ev:
            st.markdown('<div class="lf-meta"><b>Evidence (instantiated):</b> %s &nbsp;—&nbsp; '
                        '<code>%s</code></div>' % (ev.get("measured", ""), ev.get("script", "")),
                        unsafe_allow_html=True)
        sub = f.get("substrate")
        if sub == "diacritics":
            st.markdown('<div class="lf-meta" style="color:#B23B3B"><b>Substrate:</b> diacritics — '
                        'human layer, corroborative only (not the rasm/divine text).</div>', unsafe_allow_html=True)
        st.markdown('<div class="lf-concept"><span class="lab">Conceptual foundation — the full reasoning</span>%s</div>'
                    % f.get("conceptual_foundation", ""), unsafe_allow_html=True)
        c1, c2 = st.columns([3, 2])
        with c1:
            nk = rv.get("q0_new_knowledge", "")
            if rv.get("novelty_pass", True):
                st.markdown('<div class="lf-q"><b>What we now know:</b> %s</div>' % nk, unsafe_allow_html=True)
            else:
                st.markdown('<div class="lf-q" style="color:#B23B3B"><b>Novelty gate FAILED:</b> %s</div>' % nk,
                            unsafe_allow_html=True)
            st.markdown('<div class="lf-q"><b>Discovers:</b> %s</div>' % rv.get("q1_discovers", ""), unsafe_allow_html=True)
            st.markdown('<div class="lf-q"><b>Relations:</b> %s</div>' % rv.get("q3_relations", ""), unsafe_allow_html=True)
            st.markdown('<div class="lf-q"><b>Validity:</b> %s</div>' % rv.get("q4_validity", ""), unsafe_allow_html=True)
            refs = f.get("cross_refs", [])
            if refs:
                st.markdown('<div class="lf-meta"><b>Related:</b> %s</div>'
                            % " · ".join("%s (%s)" % (r, by_id.get(r, {}).get("name", "")) for r in refs),
                            unsafe_allow_html=True)
            _MOD_PAGES = {"Signal": "pages/15_Signal.py", "Mathāni": "pages/23_Structural_Twins.py",
                          "Network": "pages/2_Network.py", "Statistics": "pages/7_Statistics.py",
                          "Spatial": "pages/18_Spatial_Patterns.py", "Ayah": "pages/20_Ayah_Deep_Dive.py"}
            _asf = f.get("app_surface", {})
            _mod = (_asf.get("module_key") or _asf.get("module")) if isinstance(_asf, dict) else None
            if _mod and _mod in _MOD_PAGES:
                try:
                    st.page_link(_MOD_PAGES[_mod], label="See it live in the %s module" % _mod, icon="📡")
                except Exception:
                    pass
        with c2:
            st.markdown('<div class="lf-meta"><b>Review score profile</b></div>', unsafe_allow_html=True)
            st.markdown(score_bars(rv.get("scores", {}), feat_color(f)), unsafe_allow_html=True)


# ---------------- bird's-eye → detail: the map, then banded drill-down ----------------
shown = [f for f in included if matches(f)]

# Conceptual order = the determinacy ladder by SCALE (broadest → finest), one consistent axis.
# Modalities (form · sound · content · order) live INSIDE each scale, not as their own bands.
_BANDS_DEF = [
    ("🌍 Whole book", "Universal laws that hold across all 6,236 verses — is this even a structured object?",
     ["Lexical baselines", "Rhythm / wave", "Optimality / perturbation"], "#3F7D6E"),
    ("🕸 Across sūras", "How the 114 chapters relate — self-reference and the geometry of the whole.",
     ["Self-reference / network", "Constellation / matrix"], "#6A4C93"),
    ("📖 One sūra", "What a chapter is, where its seams lie, and that its order is determined.",
     ["Sūra definition", "Order / sequence"], "#1D3557"),
    ("🔹 Verse", "The āyah — its sound, its rhyme, and its boundary.",
     ["Rhyme / sound", "Āyah"], "#C1121F"),
]
# Keep the conceptual (scale) order; drop only the bands that have no findings yet.
def _bcount(b):
    return [f for f in shown if f.get("category") in b[2]]
BANDS = [b for b in _BANDS_DEF if _bcount(b)]

# Tier 1 = band tabs · Tier 2 = category sub-tabs · Tier 3 = one-line finding cards.
_tabs = st.tabs([b[0] for b in BANDS] + ["🔬 More", "📊 Method"])
for _ti, (title, desc, cats, col) in enumerate(BANDS):
    with _tabs[_ti]:
        _fl = sorted([f for f in shown if f.get("category") in cats], key=grade_of, reverse=True)
        _cats_present = [c for c in ([cc for cc in cat_order if cc in cats] or list(cats))
                         if any(f.get("category") == c for f in _fl)]
        _multi = len(_cats_present) > 1
        for cat in _cats_present:
            if _multi:
                st.markdown("<div style='font-size:11.5px;font-weight:700;letter-spacing:.4px;"
                            "text-transform:uppercase;color:#5A6B82;margin:13px 0 3px'>%s</div>"
                            % _html.escape(cat), unsafe_allow_html=True)
            for f in sorted([f for f in _fl if f.get("category") == cat], key=grade_of, reverse=True):
                render_card(f)

with _tabs[len(BANDS)]:
    st.markdown('<div class="lf-sec">Did not pass (< %d)</div>' % PASS, unsafe_allow_html=True)
    st.caption("Kept visible for honesty: baseline gates, soft claims awaiting stronger validation, and "
               "instrument-limited nulls (عدم الوجدان — absence of evidence is not evidence of absence).")
    for f in sorted([f for f in excluded if matches(f)], key=grade_of, reverse=True):
        render_card(f)
    cands = L.get("candidates", [])
    if cands:
        st.markdown('<div class="lf-sec">Candidates — not yet in the table</div>', unsafe_allow_html=True)
        for c in cands:
            with st.expander("🔎 %s · %s" % (c.get("id"), c.get("name"))):
                st.markdown('<div class="lf-meta"><b>Status:</b> %s</div>' % c.get("status", ""), unsafe_allow_html=True)
                st.markdown('<div class="lf-meta"><b>Evidence so far:</b> %s</div>' % c.get("evidence", c.get("result", "")), unsafe_allow_html=True)
                st.markdown('<div class="lf-why"><b>What would be new:</b> %s</div>' % c.get("why_new", c.get("extends", "")), unsafe_allow_html=True)
                st.markdown('<div class="lf-meta"><b>Universe analog:</b> %s</div>' % c.get("universe_analog", ""), unsafe_allow_html=True)
                st.markdown('<div class="lf-meta"><b>To promote:</b> %s</div>' % c.get("to_promote", ""), unsafe_allow_html=True)

with _tabs[-1]:
    st.markdown('<div class="lf-meta">Grades and coverage live here so the discoveries lead. '
                'The grade bar is a readout — the real evidence is inside each finding\'s card.</div>', unsafe_allow_html=True)
    _render_method()
    st.markdown('<div class="lf-sec">Critical-review rubric (pass ≥ %d)</div>' % PASS, unsafe_allow_html=True)
    st.markdown('<div class="lf-meta">%s &nbsp;·&nbsp; mandatory novelty gate.</div>'
                % " · ".join("%s %d" % (k.replace("_", " "), v) for k, v in RUBRIC.items()), unsafe_allow_html=True)
    if L.get("gaps"):
        st.markdown('<div class="lf-sec">Open research frontier</div>', unsafe_allow_html=True)
        st.markdown('<div class="lf-meta">%s</div>' % L["gaps"], unsafe_allow_html=True)
    try:
        due = datetime.strptime(L.get("next_update_due", ""), "%Y-%m-%d").date()
        st.caption("Source of truth: research/intrinsic/latent_features.json · last updated %s · weekly cadence." % L.get("last_updated"))
    except Exception:
        pass

st.divider()
st.markdown("<div style='font-size:12.5px;line-height:1.5;color:#34465B'>"
            "Every finding clears the critical-review rubric (pass ≥ %d) and a novelty gate. "
            "Open research frontiers and the full rubric live in the <b>Method</b> tab and the synthesis document.</div>" % PASS,
            unsafe_allow_html=True)
