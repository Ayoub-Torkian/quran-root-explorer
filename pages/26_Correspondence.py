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
    ".cl-sub{font-size:14px;color:#46505F;line-height:1.55;margin:0 0 6px;max-width:920px}"
    ".cl-why{background:#F5F8FC;border-left:4px solid #1D3557;border-radius:8px;padding:10px 14px;"
    "font-size:14px;line-height:1.55;color:#16243B;margin:6px 0 10px;max-width:980px}"
    ".cl-sec{font-size:13px;font-weight:800;text-transform:uppercase;letter-spacing:.8px;color:#1D3557;"
    "margin:22px 0 8px;border-bottom:2px solid #E7ECF3;padding-bottom:5px}"
    ".cl-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin:2px 0}"
    "@media(max-width:820px){.cl-grid{grid-template-columns:1fr}}"
    ".cl-card{background:#fff;border:1px solid #E7ECF3;border-left:4px solid #1D9E75;border-radius:7px;padding:6px 11px;margin:0}"
    ".cl-card.b{border-left-color:#7FB069}.cl-card.d{border-left-color:#C4CBD3;background:#f7f8f9}"
    ".cl-ct{font-size:13px;font-weight:800;color:#16243B;margin:0 0 1px}"
    ".cl-look{font-size:12.5px;color:#46505F;line-height:1.35;margin:0}.cl-look b{color:#1D3557}"
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

m = st.columns(5)
m[0].metric("Bedrock (A)", "7", help="survived every scrutiny pass")
m[1].metric("Attributes tested", "34")
m[2].metric("Scrutiny passes", "7")
m[3].metric("Strongest effect", "z = 125", help="propagation / self-replicating formulae")
m[4].metric("Demoted (length)", "4", help="length-gradient artifacts, not real")

# ---------------- sortable master table ----------------
st.markdown('<div class="cl-sec">All correspondences — click a column to sort</div>', unsafe_allow_html=True)
try:
    import pandas as pd
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
    df = pd.DataFrame(ROWS, columns=["ID", "Correspondence", "What we did", "Why we did it (body)", "What we found (Qur'an)", "Key value", "Effect", "Grade"])
    cc = {
        "What we did": st.column_config.TextColumn(width="large"),
        "Why we did it (body)": st.column_config.TextColumn(width="large"),
        "What we found (Qur'an)": st.column_config.TextColumn(width="medium"),
    }
    try:
        st.dataframe(df, use_container_width=True, hide_index=True, height=520, column_config=cc)
    except Exception:
        st.dataframe(df, use_container_width=True, hide_index=True, height=520)
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

# ---------------- concept cards ----------------
def cards(title, items, cls=""):
    st.markdown('<div class="cl-sec">%s</div>' % title, unsafe_allow_html=True)
    parts = ['<div class="cl-grid">']
    for ct, look, found, fl in items:
        kind = "cl-found" if fl != "rej" else "cl-rej"
        lbl = "Found:" if fl != "rej" else "Rejected:"
        parts.append(
            '<div class="cl-card %s"><div class="cl-ct">%s</div>'
            '<div class="cl-look"><b>Looked for:</b> %s</div>'
            '<div class="%s"><b>%s</b> %s</div></div>' % (cls, ct, look, kind, lbl, found))
    parts.append('</div>')
    st.markdown("".join(parts), unsafe_allow_html=True)

cards("Bedrock (A) — concept &amp; result", [
    ("A1 · Membrane", "a real edge to each sura — a membrane that seals it from its neighbours.", "neighbouring verses share many roots inside a sura, and that sharing collapses at the boundary (0.28 vs 0.87, z=-5).", ""),
    ("A2 · Internal weave", "a woven tissue (ordered) vs a loose pile of verses.", "shuffle a sura's verse order and the weave drops 0.73 → 0.52 (t=10.9).", ""),
    ("A3 · Propagation", "self-replication — does the text copy its own forms, like cells copying code?", "fixed formulae recur far above chance and reach every region: samaʾ·ard x188 ('heavens & earth'), 'amal·salah x89 ('do righteous deeds'). z=+125.", ""),
    ("A4 · Interface-zones", "an outward-facing surface (sense organs / skin), localized.", "28% of verses face outward (qul x270, ya-ayyuha x153) and they cluster into zones, z=+17.6.", ""),
    ("A5 · Rhythm / pulse", "a multi-scale pulse, like a heartbeat.", "verse lengths show long memory across the whole book (DFA 0.95 vs 0.5); information flow is regulated (z=+20).", ""),
    ("A6 · Connectivity", "specific wiring between suras, like vessels between organs.", "44% of sura-pairs are specifically linked (vs 1% chance); Baqara·Al-'Imran share 342 roots; the twins survive length control.", ""),
    ("A7 · Bilateral pairs", "matched identical pairs, like two eyes or two ears.", "form-twin suras sharing an opening template: TSM → 26 & 28, Tabaraka → 25 & 67, wa-l-samaʾ → 85 & 86. z=+5.4.", ""),
])

cards("Second tier (B) — real but modest", [
    ("Identity", "a unique function per sura — no two organs do the same job.", "a held-out verse traces to its home sura (7.2% vs 4.9% arbitrary).", ""),
    ("Necessity", "irreplaceability — remove an organ and the body loses a function.", "Fatiha is the single most-isolated sura in function space (rank 1 of 114).", ""),
    ("Digestive loop", "ingest a claim → process → output a response.", "'ask' (sa'al) is answered by 'say' (qul) within 2 verses, 25% vs 4% base.", ""),
    ("Polarity", "a head-tail axis (anterior-posterior).", "a marked head (AUC 0.75), a faint tail (0.61).", ""),
    ("Error-correction", "redundancy that repairs a damaged part.", "73% of verse-endings recoverable from the rhyme code (vs 50%).", ""),
    ("Signal propagation", "content carrying verse → verse (a nervous signal).", "adjacent verses share content above chance (0.087 vs 0.009).", ""),
], cls="b")

cards("Tested &amp; rejected — what we looked for, why it failed", [
    ("Location", "a fixed position per sura, like the heart fixed in the chest.", "position is just the mushaf's long→short ordering — remove length and nothing is left (residual R2=0.03).", "rej"),
    ("Folding contact-decay", "the linear text folding into a network with a contact-decay curve, like the genome (Hi-C).", "the decay was a length artifact (residual r=-0.04); the network itself survives via Connectivity (A6).", "rej"),
    ("Development", "developmental classes (ontogeny — early vs late forms).", "the two 'classes' are just the length gradient again.", "rej"),
    ("Skeleton (muqatta'at)", "a structural frame — the disjoint-letter suras as a skeleton.", "strong in odd suras (t=10.3) but failed split-half replication (t=1.7 in even).", "rej"),
    ("Circulation (substance)", "a circulating substance reaching every region, like blood.", "the core message clumps (no perfusion). The real 'flow' is the recitation itself (= Rhythm + Propagation).", "rej"),
], cls="d")

st.caption("Method (locked): body = benchmark, one-directional · PROVEN needs a proper null + honest effect + reproducible script · all-or-none (refine the instrument, never 'void'). Full ledger & scripts: research/correspondence/.")
