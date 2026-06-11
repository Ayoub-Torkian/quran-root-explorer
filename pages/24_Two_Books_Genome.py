"""Two Books · Language vs the Genome — a replicated structural comparison + a
controlled test of the letter->DNA correspondence. Self-contained: loads ONLY
two_books_lens.json (repo root); never touches the live corpus or BLAST, so it
cannot break other pages. Computed result, gated vs controls. Not tafsir."""
import json
from pathlib import Path
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Two Books · Genome", page_icon="🧬", layout="wide")
try:
    from state import hero, log_page, inject_css, render_grouped_nav
    log_page("two_books_genome")
    try: inject_css()
    except Exception: pass
    try: render_grouped_nav()
    except Exception: pass
except Exception:
    def hero(t, s=""):
        st.title(t)
        if s: st.caption(s)

NAVY, TEAL, GRAY, ORANGE, RED, PURPLE = "#1d3557", "#1d9e75", "#c7c5bc", "#ef9f27", "#e63946", "#6a4c93"
DATA = Path(__file__).resolve().parent.parent / "two_books_lens.json"

@st.cache_data(show_spinner=False)
def load():
    return json.loads(DATA.read_text(encoding="utf-8"))

D = load(); m = D["meta"]; rows = D["structural"]; scen = D["scenarios"]

st.markdown("""<style>
.block-container{padding-top:2.2rem;padding-bottom:1rem}
div[data-testid='stVerticalBlock']{gap:0.45rem}
hr{margin:0.45rem 0}
</style>""", unsafe_allow_html=True)

hero("🧬 " + m["title"], m["subtitle"])

# ── KPI chips ────────────────────────────────────────────────────────────────
def chip(lab, val, tip):
    return (f"<div title=\"{tip}\" style='flex:1 1 120px;min-width:115px;padding:5px 10px;cursor:help;"
            f"border:1px solid #e6e6e6;border-radius:7px;background:#fafbfc'>"
            f"<div style='font-size:0.72rem;color:#000;font-weight:600;text-transform:uppercase;"
            f"letter-spacing:.3px;border-bottom:1px dotted #9ec3b6;display:inline-block'>{lab}</div>"
            f"<div style='font-size:1.3rem;font-weight:800;color:{NAVY}'>{val}</div></div>")
chips = [
    ("Genome memory γ", f"{m['genome_gamma']:.2f}", "Mutual-information decay exponent of the human coding genome — lower = longer-range statistical memory. The genome is the outlier."),
    ("Language γ range", f"{m['lang_gamma_lo']:.1f}–{m['lang_gamma_hi']:.1f}", "All 8 human languages decay fast (short memory). The genome (0.92) sits far below every one of them."),
    ("Languages", f"{m['n_languages']}", f"Tested across {m['n_families']} language families: Germanic, Romance, Hellenic, Finno-Ugric, and Semitic (the Qur'an)."),
    ("Families", f"{m['n_families']}", "The contrast replicates across unrelated language families and scripts — not a quirk of one language."),
    ("Cipher tests", f"{m['n_scenarios']}", "Searches for a letter→DNA mapping that makes the Qur'an map onto real genes/proteins (forward, backward, several encodings)."),
    ("Held-out nulls", f"{m['n_nulls']}/{m['n_scenarios']}", "Every cipher search, judged on held-out data vs a control battery, returned a null. No hidden code found."),
]
st.markdown("<div style='font-size:0.8rem;color:#1d9e75;font-weight:600;margin:2px 0 4px'>"
            "&#9432; Hover any box for what it means</div>", unsafe_allow_html=True)
st.markdown("<div style='display:flex;flex-wrap:wrap;gap:7px;margin:2px 0 12px'>"
            + "".join(chip(l, v, t) for l, v, t in chips) + "</div>", unsafe_allow_html=True)

# ── How to read ──────────────────────────────────────────────────────────────
st.markdown(
    "<div style='border:2px solid #1d3557;border-left:9px solid #1d3557;border-radius:10px;"
    "padding:13px 18px;margin:6px 0 14px;background:#f4f8fc'>"
    "<div style='font-size:1.15rem;font-weight:800;color:#1d3557'>Finding 1 — the two books have different &ldquo;handwriting&rdquo;</div>"
    "<div style='font-size:0.97rem;color:#111;margin-top:6px;line-height:1.55'>"
    "We measured each text&rsquo;s structural &ldquo;texture&rdquo; with no mapping at all &mdash; how fast the "
    "statistical link between distant positions fades (the <b>MI-decay exponent γ</b>; lower = longer memory). "
    "On the <b>full human coding genome</b> and <b>eight languages across five families</b>, the result is unanimous: "
    "<b>every human language has short memory (γ ≈ 1.4&ndash;2.5); the genome alone has long memory (γ ≈ 0.92)</b>. "
    "The Qur&rsquo;an sits squarely inside the language cluster &mdash; no closer to the genome than Homer or Cervantes.</div></div>",
    unsafe_allow_html=True)

# ── chart: gamma by corpus ───────────────────────────────────────────────────
def sty(fig, title, h=320):
    fig.update_layout(title=dict(text=title, font=dict(size=15, color=NAVY)),
        height=h, margin=dict(l=6, r=10, t=36, b=6), plot_bgcolor="white",
        font=dict(size=12, color="#222"), showlegend=False)
    fig.update_xaxes(tickfont=dict(size=11), gridcolor="#eee")
    fig.update_yaxes(title_font=dict(size=12), tickfont=dict(size=11), gridcolor="#eee")
    return fig

labels = [r["corpus"] for r in rows]
gam = [r["mi_gamma"] for r in rows]
cols = [NAVY if r.get("is_genome") else (ORANGE if r.get("is_quran") else TEAL) for r in rows]
c1, c2 = st.columns([3, 1], gap="medium")
with c1:
    fig = go.Figure(go.Bar(x=labels, y=gam, marker_color=cols,
        text=[f"{g:.2f}" for g in gam], textposition="outside", textfont_size=11, cliponaxis=False))
    fig.add_hline(y=m["genome_gamma"], line=dict(color=NAVY, width=1, dash="dot"))
    st.plotly_chart(sty(fig, "Memory length by corpus (MI-decay γ — lower = longer memory)", 360)
        .update_yaxes(title_text="γ", range=[0, 2.8]).update_xaxes(tickangle=30), use_container_width=True)
with c2:
    st.markdown(
        "<div style='border:1px solid #cdd7e0;border-left:7px solid #1d3557;border-radius:9px;"
        "padding:11px 14px;margin:34px 0 0;background:#f6f9fc;font-size:0.92rem;color:#111;line-height:1.5'>"
        f"<b style='color:{NAVY}'>The genome stands alone.</b><br>"
        "Navy = genome. Amber = Qur&rsquo;an. Teal = other languages. The genome&rsquo;s bar is far below the "
        "whole language pack &mdash; it carries long-range memory that no human language does.</div>",
        unsafe_allow_html=True)
st.caption("How to read: each bar is one corpus. Shuffling any text destroys its structure (controls verified); "
           "these values are the genuine signal. Lower γ = correlations reach farther.")

st.divider()
# ── Finding 2: the cipher search ─────────────────────────────────────────────
st.markdown(
    "<div style='border:1px solid #cdd7e0;border-left:7px solid #ef9f27;border-radius:9px;"
    "padding:12px 16px;margin:4px 0 12px;background:#fcf8f1'>"
    "<div style='font-size:1.12rem;font-weight:800;color:#1d3557'>Finding 2 — no hidden code: six searches, six honest nulls</div>"
    "<div style='font-size:0.95rem;color:#111;margin-top:5px;line-height:1.55'>"
    "We then searched directly for a letter&rarr;DNA cipher that turns Qur&rsquo;anic text into real genes/proteins &mdash; "
    "forward and backward, characters as codons and as bases, even &ldquo;each verse is a gene&rdquo;. To avoid the "
    "<b>Bible-Code trap</b> (a flexible search always finds <i>something</i>), we monitored only the margin over a "
    "control battery (scrambled text, other languages, random) on <b>held-out</b> data &mdash; un-gameable by searching harder.</div></div>",
    unsafe_allow_html=True)

def line(idv, desc, delta, verdict, hi=False):
    bg = "background:#fff7e9;" if hi else ""
    vc = RED if "false" in verdict else "#555"
    st.markdown(
        f"<div style='display:flex;gap:14px;align-items:baseline;padding:4px 8px;border-bottom:1px solid #eee;{bg}'>"
        f"<span style='flex:0 0 38px;color:{NAVY};font-weight:700;font-size:0.85em'>{idv}</span>"
        f"<span style='flex:1 1 auto;color:#222;font-size:0.88em'>{desc}</span>"
        f"<span style='flex:0 0 120px;color:{NAVY};font-weight:700;font-size:0.85em;text-align:right'>{delta}</span>"
        f"<span style='flex:0 0 190px;color:{vc};font-size:0.82em;text-align:right'>{verdict}</span></div>",
        unsafe_allow_html=True)
line("#", "What we tried", "Held-out Δ", "Verdict")
for s in scen:
    line(s["id"], s["desc"], s["delta"], s["verdict"], hi=("false" in s["verdict"]))
st.caption("Δ = how much the Qur'an beats the controls on held-out data (Δ>0 = real lead). "
           "S3 flashed Δ=+0.13 in a small run, then collapsed to ≈0 under a bigger search and 3 seeds — "
           "a false positive caught in real time, the discipline working as intended.")

# ── honest caveat ────────────────────────────────────────────────────────────
st.markdown(
    "<div style='border:2px solid #1d9e75;border-left:9px solid #1d9e75;border-radius:10px;"
    "padding:13px 18px;margin:14px 0 6px;background:#f3faf6'>"
    "<div style='font-size:1.05rem;font-weight:800;color:#15795a'>What this does and doesn&rsquo;t say</div>"
    "<div style='font-size:0.95rem;color:#111;margin-top:5px;line-height:1.55'>"
    "<b>Does:</b> human language and the coding genome are measurably, reproducibly built on different structural "
    "principles, and the Qur&rsquo;an behaves exactly like human language. The specific <b>letter&rarr;DNA cipher</b>, "
    "tested in its strongest honest forms, <b>does not hold</b>. "
    "<b>Doesn&rsquo;t:</b> weigh in on the two-books idea as theology or metaphor &mdash; only on the one testable, "
    "sequence-level claim. This is the Bible-Code&rsquo;s mirror image: the same idea, pursued with pre-registration, "
    "symmetric controls, held-out validation, and an un-gameable scoreboard.</div></div>",
    unsafe_allow_html=True)

st.caption(f"Honest scope: structural signatures are mapping-free and replicate across {m['n_languages']} languages / "
           f"{m['n_families']} families on the full {m['genome_label']}. The cipher search returned {m['n_nulls']}/{m['n_scenarios']} "
           "held-out nulls. Full record, code & data: research/two_books_genome/ (METHODOLOGY, CHALLENGES, RESULTS, JOURNEY).")
