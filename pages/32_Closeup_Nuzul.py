"""Close-up · Qur'ān chronology — dating the revelation, reviewed (CANDIDATE). Comprehensive across the
main schools (traditional, orientalist, modern/quantitative); credit-forward to Bazargan. All counts MEASURED
on Book6 (rasm-WORD, col 8 revelation order); the scholarship survey is tagged as such."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Qur'ān chronology", page_icon="🕰️", layout="wide")
if S:
    try:
        S.log_page("closeup_nuzul")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()
Y, P, N = "✔ holds", "~ partial", "✗ over-reach"

# ── 1 · PROBLEM ──
C.hero("Qur'ān chronology — dating the revelation, reviewed",
       "Can the Qur'ān's chapters be ordered in time from the text itself — and how far down may we date: "
       "the sūra, or the passages inside it?",
       "CANDIDATE", 70, "rasm-WORD (Book6 col 6)", "DIVINE-ALT · revelation order (col 8)")
st.markdown(
    "<div style='display:flex;justify-content:flex-end;gap:9px;margin:7px 0 2px;flex-wrap:wrap'>"
    "<a href='#nz-fa' style='text-decoration:none'>"
    "<div style='background:linear-gradient(135deg,#138A74,#10243A);color:#fff;border-radius:9px;padding:7px 13px;"
    "font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(16,36,58,.25);border:1px solid rgba(255,255,255,.3)'>"
    "📄 Persian abstract · خلاصهٔ فارسی ↓</div></a>"
    "<a href='#nz-ar' style='text-decoration:none'>"
    "<div style='background:linear-gradient(135deg,#4E6E92,#10243A);color:#fff;border-radius:9px;padding:7px 13px;"
    "font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(16,36,58,.25);border:1px solid rgba(255,255,255,.3)'>"
    "📄 Arabic abstract · الملخّص العربي ↓</div></a></div>", unsafe_allow_html=True)
C.story(
    "The chronology of the Qur'ān is a <b>real, measurable signal</b>: mean verse length climbs steadily from the "
    "short, rhymed Meccan sūras (≈ 14 words/āyah) to the long, legal Medinan ones (≈ 30) — and that single trend "
    "orders the sūras and broadly confirms the traditional sequence. Eleven centuries of scholars, from the "
    "tradition to Nöldeke to Bazargan to Sadeghi, <b>converge</b> on it. The one over-reach they also share is "
    "dating analyst-cut <i>passages</i> inside a sūra.",
    "Revelation order is a legitimate divine-<i>alternative</i> arrangement. This reviews the whole field — not one "
    "author — credits each where credit is due (Bazargan pioneered the quantitative clock; Sadeghi vindicated it), "
    "and scopes the single shared criticism precisely. مقبول for the general reader, مطلوب for the specialist.",
    accent=C.TEAL)
C.kpis([
    ("r = 0.66", "length ↔ time", "Mean āyah length (words) vs the traditional revelation order, col 8 — MEASURED on 114 sūras", C.TEAL),
    ("R² 0.44", "variance explained", "Verse length alone explains 44% of the revelation-order variance", C.TEAL),
    ("14 → 30", "Mecca → Medina", "Mean words/āyah: Meccan 14.0 (n=86) vs Medinan 29.7 (n=28) — the clock, plainly", C.TEAL),
    ("8.4 ≈ 11.1", "within ≈ between", "Verse-length spread INSIDE a sūra (8.4) ≈ the spread of sūra-means ACROSS the corpus (11.1)", C.GOLD),
    ("2–74%", "change-point band", "Share of sūras with a detectable internal break — wildly method-dependent", C.GOLD),
    ("✓ Sadeghi", "program vindicated", "2011 morphological stylometry confirmed the chronology the tradition & Bazargan drew", C.TEAL),
    ("70", "grade", "CANDIDATE — sūra-level clock real & converged; only passage-level dating over-reaches", C.GOLD),
])
st.markdown(
    "<div style='font-size:12.5px;color:#10243A;background:#EEF3F8;border:1px solid #DCE6F0;border-radius:9px;"
    "padding:8px 13px;margin:5px 0 2px;line-height:1.75'><b>On this page —</b> "
    "① Problem &nbsp;·&nbsp; ② Hypothesis &nbsp;·&nbsp; ③ Method &nbsp;·&nbsp; "
    "<b>④ Results Part 1</b> the measured clock (5 charts) &nbsp;·&nbsp; "
    "<b>⑤ Results Part 2</b> the field, school by school (timeline + 6 profiles) &nbsp;·&nbsp; "
    "⑥ Gating &nbsp;·&nbsp; ⑦ Interpretation &nbsp;·&nbsp; ⑧ Caveats &nbsp;·&nbsp; ⑨ Verdict &nbsp;→&nbsp; "
    "Reflection · Summary · Lessons · Takeaway · "
    "<a href='#nz-fa' style='color:#138A74;font-weight:700'>Persian</a> / "
    "<a href='#nz-ar' style='color:#138A74;font-weight:700'>Arabic</a> abstracts</div>", unsafe_allow_html=True)

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If verse length is a chronological clock, it makes three predictions — two FOR it, one against over-reach",
          "Two claims are routinely blurred, and we separate them. The <i>weak, true</i> claim: style drifts over "
          "the revelation period. The <i>strong</i> claim: that drift can <b>date</b> any slice of text. We test "
          "three predictions.<br>"
          "&nbsp;&nbsp;<b>(1) Correlation.</b> Mean verse length must track the revelation order. "
          "<br>&nbsp;&nbsp;<b>(2) Recovery.</b> Ordering the sūras by length alone must approximate the traditional "
          "sequence — and the independent scholarly chronologies must converge on the same shape. "
          "<br>&nbsp;&nbsp;<b>(3) The boundary test.</b> One may date a <i>passage</i> inside a sūra by length only "
          "if sūras carry <b>detectable internal style-breaks</b>; otherwise the 'passages' are drawn by the analyst, "
          "not the text.<br>"
          "Predictions 1–2 vindicate the tradition, Nöldeke and Bazargan alike; prediction 3 is where passage-level "
          "dating — Bell's, Blachère's, and Bazargan's finest-grained move — must earn its keep.",
          accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus — substrate, the divine-alternative order, and four tests",
          "<b>Substrate.</b> rasm-WORD (Book6 col 6): āyah length counted in whole word-tokens on the consonantal "
          "skeleton, diacritics demoted. <b>Arrangement.</b> the divine-<i>alternative</i>: the traditional "
          "revelation order (col 8, sūra granularity — the 1924 Cairo standard), the reference every modern study "
          "uses.<br>"
          "&nbsp;&nbsp;<b>Four tests.</b> (a) <i>Correlation</i> — Pearson/Spearman of mean āyah length vs "
          "revelation rank, across all 114 sūras. (b) <i>Multivariate clock</i> — length + letters-per-word + "
          "letter-length, to see how much more than raw length is carried. (c) <i>Convergence</i> — line up the "
          "main scholarly chronologies (traditional, orientalist, quantitative) and check they agree on the shape "
          "the data shows. (d) <i>Boundary test</i> — detect an internal verse-length change-point in each sūra "
          "across <i>several</i> thresholds and a multiplicity-corrected t-test, so 'is this sūra composite?' cannot "
          "be tuned; plus within-sūra vs between-sūra variance.<br>"
          "&nbsp;&nbsp;<b>MEASURED vs SCHOLARSHIP.</b> Every number below is MEASURED on Book6. The survey of who "
          "said what is historical scholarship, tagged as such — never dressed as our measurement. Our normalised "
          "rasm differs from Bazargan's own tallies; we test his <i>method</i>, not reproduce his figures.",
          accent=C.SLATE)

# ── 4 · RESULTS · PART 1 — THE MEASURED CLOCK (our data) ──
C.section("Results · Part 1 — the measured clock (our data)")
C.note("MEASURED. Mean verse length rises with revelation order (Pearson r = 0.66, Spearman 0.69, R² 0.44), broadly "
       "reproducing the traditional sequence — and the extremes are exactly where the tradition puts them.")
L, R = st.columns(2, gap="medium")
with L:
    C.table(["Shortest mean āyah — early/Meccan", "sūra", "w/āyah"], [
        ["al-Ikhlāṣ — terse, hymnic", "112", "4.8"], ["al-Nās", "114", "5.0"],
        ["ʿAbasa", "80", "5.1"], ["al-Ghāshiya", "88", "5.2"],
    ])
with R:
    C.table(["Longest mean āyah — late/Medinan", "sūra", "w/āyah"], [
        ["al-Mumtaḥina — long, legal", "60", "49.6"], ["al-Māʾida", "5", "41.1"],
        ["al-Ṭalāq", "65", "39.4"], ["al-Baqara", "2", "38.0"],
    ])

C.section("Statistical core — five measured views of the clock")

C.note("① The clock itself — mean words/āyah by revelation-order quintile (Q1 earliest → Q5 latest). The rise is "
       "real and large (7 → 29 words), but NOT perfectly monotonic: Q4 dips below Q3. The trend is a drift, not a "
       "metronome — already a caution against fine-grained dating.")
C.hist([7.3, 11.7, 22.0, 16.7, 29.3], ["Q1 early", "Q2", "Q3", "Q4", "Q5 late"], highlight=4, color=C.TEAL)

C.note("② The plainest cut — Meccan vs Medinan mean āyah length. The single fact under the whole chronology: "
       "Medinan verses are more than twice as long. MEASURED on the traditional Makkī/Madanī split.")
C.vbars([("Meccan (n=86)", 14.0, C.TEAL, "Mean 14.0 words/āyah across 86 Meccan sūras"),
         ("Medinan (n=28)", 29.7, C.INK, "Mean 29.7 words/āyah across 28 Medinan sūras")],
        ymax=34, fmt="{:.1f}")

C.note("③ A multivariate clock improves the fit only modestly — verse length already carries almost all the signal "
       "(letters-per-word alone correlates just ~0.09). An honest gain, not a transformation.")
C.vbars([("verse length", 0.44, C.TEAL, "length alone: R² 0.44"),
         ("+ letters/word", 0.46, C.TEAL, "+ word length"),
         ("+ letter length", 0.49, C.INK, "+ āyah length in letters: R² 0.49")], ymax=0.6, fmt="{:.2f}")

C.note("④ The boundary test — share of sūras with a 'detectable' internal break, by method. It swings from 2% to "
       "74%, so 'is this sūra composite?' has NO stable answer — and passage-level dating cannot be grounded. We "
       "show the whole band, never a cherry-picked figure.")
C.vbars([("Δ > 1.0σ", 33, C.SLATE, "mean-diff threshold 1.0×σ"), ("Δ > 1.25σ", 18, C.SLATE, "1.25×σ"),
         ("Δ > 1.5σ", 10, C.SLATE, "1.5×σ"), ("Δ > 2.0σ", 2, C.SLATE, "2.0×σ"),
         ("t-test p<.05", 74, C.GOLD, "uncorrected — inflated by multiplicity"),
         ("t-test Bonferroni", 38, C.GOLD, "multiplicity-corrected")], ymax=80, fmt="{:.0f}%")

C.note("⑤ The deepest reason passage-dating fails — the spread of verse length INSIDE one sūra (σ ≈ 8.4) is almost "
       "as large as the spread of sūra-means ACROSS the whole corpus (σ ≈ 11.1). A passage's length says little "
       "about its date: within-sūra noise nearly swamps the between-sūra signal.")
C.vbars([("within a sūra (σ)", 8.4, C.GOLD, "Mean within-sūra SD of āyah length ≈ 8.4 words"),
         ("between sūras (σ)", 11.1, C.INK, "SD of the 114 sūra-means ≈ 11.1 words")],
        ymax=13, fmt="{:.1f}")

# ── 5 · RESULTS · PART 2 — THE FIELD, REVIEWED SCHOOL BY SCHOOL ──
def _field(icon, label, txt, lc):
    return (f"<div style='background:#F6F9FC;border-radius:8px;padding:7px 10px'>"
            f"<div style='font-size:12px;font-weight:800;color:{lc};letter-spacing:.3px'>{icon} {label}</div>"
            f"<div style='font-size:13.5px;color:#10243A;line-height:1.5;margin-top:2px'>{txt}</div></div>")


def profile(name, era, gran, accent, did, strength, limit, got, weight, blind, xref):
    st.markdown(
        f"<div class='cu-card' style='border-left:6px solid {accent};padding:13px 16px'>"
        f"<div style='display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap'>"
        f"<div style='font-size:17px;font-weight:800;color:#10243A'>{name}</div>"
        f"<div style='display:flex;gap:6px;flex-wrap:wrap'>"
        f"<span style='font-size:12px;font-weight:700;color:#10243A;background:#EEF3F8;border-radius:6px;"
        f"padding:3px 9px'>{era}</span>"
        f"<span style='font-size:12px;font-weight:800;color:#fff;background:{accent};border-radius:6px;"
        f"padding:3px 9px'>{gran}</span></div></div>"
        f"<div style='font-size:14px;color:#10243A;line-height:1.55;margin:8px 0 9px'><b>What it did.</b> {did}</div>"
        f"<div style='display:grid;grid-template-columns:1fr 1fr;gap:8px'>"
        f"{_field('✓', 'STRENGTH', strength, '#138A74')}"
        f"{_field('✗', 'LIMIT', limit, '#C24230')}"
        f"{_field('📊', 'WHAT IT GOT', got, '#10243A')}"
        f"{_field('⚖', 'CONTRIBUTION', weight, '#10243A')}</div>"
        f"<div style='font-size:13.5px;color:#10243A;line-height:1.5;margin-top:9px;border-top:1px solid #E7EEF5;"
        f"padding-top:7px'><b>Did not consider.</b> {blind}</div>"
        f"<div style='font-size:12.5px;color:#10243A;line-height:1.45;margin-top:6px;background:#EEF3F8;"
        f"border-radius:7px;padding:6px 10px'><b>↔ Cross-reference.</b> {xref}</div></div>", unsafe_allow_html=True)


def timeline(nodes):
    W, H, L, Rr, y0 = 1000, 196, 46, 46, 104
    n = len(nodes); pw = W - L - Rr
    p = [f"<svg viewBox='0 0 {W} {H}' width='100%' style='width:100%;display:block'>",
         f"<line x1='{L}' y1='{y0}' x2='{W-Rr}' y2='{y0}' stroke='#9FB4C8' stroke-width='2'/>"]
    for i, (yr, nm, c) in enumerate(nodes):
        x = L + pw * (i / (n - 1)); up = (i % 2 == 0)
        stub = (y0 - 20) if up else (y0 + 20)
        nmY = (y0 - 30) if up else (y0 + 35)
        yrY = (y0 - 46) if up else (y0 + 51)
        p.append(f"<line x1='{x:.0f}' y1='{y0}' x2='{x:.0f}' y2='{stub:.0f}' stroke='{c}' stroke-width='2'/>"
                 f"<circle cx='{x:.0f}' cy='{y0}' r='6.5' fill='{c}' stroke='#fff' stroke-width='2'/>"
                 f"<text x='{x:.0f}' y='{nmY:.0f}' text-anchor='middle' font-size='13' font-weight='800' "
                 f"fill='#10243A'>{nm}</text>"
                 f"<text x='{x:.0f}' y='{yrY:.0f}' text-anchor='middle' font-size='12' fill='#10243A'>{yr}</text>")
    p.append("</svg>")
    st.markdown("<div class='cu-card'>" + "".join(p) + "</div>", unsafe_allow_html=True)


C.section("Results · Part 2 — the field, reviewed school by school")
C.para("This is the fair core of the review: not a verdict, but an account. Each school below gets its due — what it "
       "did, what it got right, what it missed, how much it moved the field, and what it could not yet see — before "
       "the one-line summary at the very end. Read top to bottom it is also the story of an <b>instrument "
       "sharpening</b>: from transmitted report, to stylistic intuition, to an explicit, falsifiable number.")

C.note("① The journey — eleven centuries of chronology, coloured by the resolution each aimed at. Sūra-level work "
       "(teal) lands on the data's sweet spot; passage/verse work (coral) reaches past it. Spacing is schematic, "
       "not linear in time.")
timeline([("7th c.", "Tradition", C.TEAL), ("1844", "Weil", C.SLATE), ("1860", "Nöldeke", C.TEAL),
          ("1861", "Muir", C.SLATE), ("1895", "Grimme", C.SLATE), ("1902", "Hirschfeld", C.GOLD),
          ("1937", "Bell", C.CORAL), ("1947", "Blachère", C.CORAL), ("1980s", "Bazargan", C.TEAL),
          ("2011", "Sadeghi", C.TEAL), ("2017", "Sinai", C.TEAL)])
st.markdown("<div style='font-size:12.5px;color:#10243A;margin:2px 2px 10px;display:flex;gap:16px;flex-wrap:wrap'>"
            "<span><b style='color:#138A74'>●</b> sūra-level (on the data's target)</span>"
            "<span><b style='color:#4E6E92'>●</b> period</span>"
            "<span><b style='color:#CC8A3C'>●</b> typology</span>"
            "<span><b style='color:#C24230'>●</b> passage / verse (over-reach)</span></div>", unsafe_allow_html=True)

profile("1 · The Islamic tradition — asbāb al-nuzūl, Ibn ʿAbbās, Cairo 1924", "7th–20th c.", "sūra level", C.TEAL,
        "Gathered the occasion-of-revelation reports, classified every sūra Meccan or Medinan from the text's own "
        "register-markers — address-forms (<i>yā ayyuhā l-nās</i> vs <i>yā ayyuhā lladhīna āmanū</i>), legal vs "
        "eschatological content — and fixed a full 114-sūra order, canonised in the 1924 Cairo edition (our col 8).",
        "Earliest and richest, anchored in transmitted memory and internal markers; still the reference axis every "
        "later study — including this one — tests against.",
        "Many asbāb reports are late, isnād-contested, or contradictory; the tradition itself concedes some sūras are "
        "composite (Medinan verses inside Meccan sūras).",
        "The broad Meccan→Medinan order — which our data independently confirms (verse length tracks it, r = 0.66).",
        "Foundational: it defines the very object and the order being tested.",
        "No quantitative control; the authenticity of a report, not measurement, decided placement.",
        "It supplies the col-8 order measured in <b>Results</b> above; the orientalists (Weil, Nöldeke) set out to "
        "<i>refine</i> it, and Bazargan/Sadeghi later <i>confirmed</i> it with numbers.")

profile("2 · Weil & Muir — the first Western chronologies", "1844 · 1861", "period", C.SLATE,
        "Weil first brought European source-criticism to the Qur'ān, proposing three Meccan periods + Medinan on "
        "tone and style; Muir extended it to five Meccan periods + Medinan, dating sūras by fit with the Prophet's "
        "biography and adding an early 'rhapsodic' phase.",
        "Broke from pure tradition and tied chronology to observable stylistic development — rising verse length, "
        "cooling fervour — the germ of the modern clock.",
        "Impressionistic and biography-driven; hard to replicate. Muir's earliest 'rhapsodies' are speculative.",
        "The period skeleton Nöldeke would refine; a broadly correct ordering.",
        "Pioneering but superseded within a generation.",
        "No formal, statable criterion — chronology read from subjective tone, with no null.",
        "Their 'rising verse length' intuition is exactly what the <b>clock chart</b> (②) later measures; Nöldeke "
        "systematised what they sketched.")

profile("3 · Nöldeke — the standard", "1860", "period (sūra-ranked)", C.TEAL,
        "In <i>Geschichte des Qorāns</i> fixed the canonical scheme — three Meccan periods + Medinan — judged by "
        "STYLE (verse length, rhyme, sentence structure) together with content and tradition, and ranked sūras "
        "within each period.",
        "The first rigorous, criterion-based chronology. Verse-length growth is essentially Nöldeke's observation — "
        "the exact signal our data measures (r = 0.66). Durable for 160 years.",
        "Treats period boundaries as sharp; the drift is in fact gradual (our quintiles rise but not monotonically — "
        "Q4 dips). Within-period order stays uncertain.",
        "The reference relative chronology of the entire field.",
        "The single most influential — the frame everyone, including this review, still uses.",
        "No statistical null; the three periods reified as discrete stages rather than a continuum.",
        "His verse-length criterion = the <b>r = 0.66 clock</b> measured here; Blachère refined him, and Sadeghi "
        "(2011) <i>vindicated</i> him statistically — see Profile 6.")

profile("4 · Grimme & Hirschfeld — variants & typology", "1895 · 1902", "typology", C.GOLD,
        "Grimme compressed the Meccan material to two periods on metrical-theological grounds; Hirschfeld set "
        "sequence aside for a typology — confirmatory, declamatory, narrative, descriptive, legislative, parabolic.",
        "Tested whether fewer or different categories fit, and Hirschfeld rightly foregrounded genre, which "
        "co-varies with date.",
        "Grimme's two periods are too coarse; a typology is not a chronology — genre is not time, though the two "
        "correlate.",
        "Useful cautions, not a new order.",
        "Secondary refinements to the Nöldeke frame.",
        "Conflated genre with chronology — the very confound that also caps a length-only clock (long = legal = "
        "late, but not always).",
        "Their genre↔time confound is the same one that holds Bazargan's R² to 0.44 (Profile 6) and that the "
        "<b>multivariate chart</b> (③) tries to break.")

profile("5 · Bell & Blachère — the radical re-daters", "1937 · 1947", "passage / verse", C.CORAL,
        "Bell re-dated at the PASSAGE and verse level, treating sūras as composite documents repeatedly edited and "
        "revised (the 'Bell hypothesis'); Blachère produced a chronologically-ordered French translation, refining "
        "Nöldeke but still re-sequencing the text.",
        "Rightly saw that a sūra is not always a single-session unit, and put the composite question on the table "
        "seriously.",
        "Passage-level dating is not robust: our change-point test gives a 2–74% 'composite' rate by threshold, and "
        "within-sūra spread (8.4) ≈ between-sūra spread (11.1). The cuts are analyst-drawn, not text-marked.",
        "A finer but unstable map; few of Bell's specific re-datings command consensus.",
        "An influential cautionary tale — the method reached below its evidence.",
        "No robustness check on the boundaries; assumed detectable seams where the statistics show mostly none.",
        "This is THE shared over-reach — the same unit-error Bazargan commits at the passage (Profile 6), exposed by "
        "the <b>change-point band</b> (④) and the <b>within ≈ between</b> chart (⑤).")

profile("6 · Bazargan, Sadeghi & Sinai — the quantitative turn", "1980s · 2011 · 2017", "sūra (statistical)", C.TEAL,
        "Bazargan computed mean verse length per sūra and ordered by it — the first explicit chronometer (our "
        "r = 0.66 clock). Sadeghi built a morphological / function-word stylometric program with a proper "
        "statistical frame, confirming gradual evolution and the broad order. Sinai joined verse-length metrics to "
        "text-criticism in support of Nöldeke.",
        "Reproducible, falsifiable, data-driven; Sadeghi supplied the null and effect-size rigour the field lacked. "
        "The convergence with tradition and Nöldeke is the strong triangulation.",
        "Bazargan leaned on ONE feature (length conflates with genre; R² 0.44); Sadeghi's power is sūra-level and "
        "feature-hungry; none reaches the passage safely.",
        "The r = 0.66 length-clock; Sadeghi's vindication; the modest multivariate gain 0.44 → 0.49.",
        "The modern backbone — credited, and still growing.",
        "Bazargan did not separate genre from time; and the clock tempts its users below the sūra — the same "
        "over-reach as Bell (Profile 5).",
        "Bazargan's clock IS the measured result of this whole page; Sadeghi vindicates Nöldeke (Profile 3); the "
        "discipline-without-favour echoes the <b>Code 19 review</b>, where the same gates refuted a claim instead.")

C.note("③ The crux, visualised — how well the data supports dating at each resolution. Support is high from "
       "whole-corpus down to the SŪRA, then falls off a cliff at the passage and verse. Every school's verdict "
       "tracks the resolution it aimed at — the timeline's colours, quantified. [INFERRED — a schematic of the "
       "measured results ②–⑤ above, not a separate measurement.]")
C.vbars([("Mecca/Medina split", 0.95, C.TEAL, "the whole-corpus split — essentially certain (14 vs 30 words/āyah)"),
         ("period (Nöldeke)", 0.85, C.TEAL, "three periods — well supported"),
         ("sūra — the clock", 0.80, C.TEAL, "r = 0.66; the sweet spot"),
         ("passage (Bell)", 0.25, C.CORAL, "2–74% composite rate — unstable"),
         ("verse", 0.10, C.CORAL, "within ≈ between; essentially no signal")], ymax=1.0, fmt="{:.0%}")

C.note("④ The instrument sharpening over time — each era brought a new feature to bear. The chronology was not so "
       "much overturned as BETTER MEASURED: the modern numbers confirmed what the tradition and Nöldeke had read "
       "from style. (This is the knowledge-tree growing, not the text changing.)")
C.table(["Era · school", "Features brought to bear", "What was new"], tight=False, rows=[
    ["7th–20th c. · tradition", "occasion-reports, address-form, legal vs eschatological content", "the object & the sūra-level order"],
    ["1844–61 · Weil, Muir", "tone, fervour, biographical fit", "Western source-criticism of the text"],
    ["1860 · Nöldeke", "verse length + rhyme + content + tradition", "a criterion-based relative chronology"],
    ["1895–1902 · Grimme, Hirschfeld", "metre; genre typology", "genre as a (confounding) axis"],
    ["1937–47 · Bell, Blachère", "composite-document analysis", "the passage as a unit — the over-reach"],
    ["1980s · Bazargan", "mean verse length, quantified", "an explicit, reproducible clock"],
    ["2011–17 · Sadeghi, Sinai", "morphology, function-words, a proper null", "statistical rigour & vindication"],
])

C.section("At a glance — the limit and the fix, in one row each")
C.note("Everything above, compressed: each school's single key limit and the remedy. The fix is almost always to "
       "respect the sūra as the atomic unit and ADD features — not to discard the approach.")
C.table(["Approach", "Where it falls short", "Suggested fix"], tight=False, rows=[
    ["Traditional asbāb al-nuzūl", "many occasion-reports are late, contested, or absent", "validate against the intrinsic stylometric signal — which broadly confirms the order"],
    ["Nöldeke — 3 sharp Meccan periods", "boundaries are gradiental, not discrete; periods blur", "read the drift as a continuum (as Sadeghi's gradual evolution shows)"],
    ["Weil / Muir — tone & content", "subjective, hard to replicate", "quantify: verse length + morphology give a reproducible proxy"],
    ["Bell — passage/verse re-dating", "not robust: composite-rate 2–74%; within ≈ between", "confine dating to the sūra; treat passage cuts as hypotheses, not dates"],
    ["Blachère — chronological translation", "inherits passage-level precision it can't support", "present sūra-level order; flag intra-sūra cuts as uncertain"],
    ["Bazargan — verse length only", "one feature; length conflates with genre/topic (R² 0.44)", "multivariate stylometry (the modest 0.44 → 0.49 gain, extended)"],
    ["Sadeghi — morphological stylometry", "powerful but sūra-level; needs many features", "the right tool to PROBE passages — only where a real style-break is detectable"],
])

# ── 6 · GATING CHAIN ──
C.section("Gating chain — strong at the sūra, weak at the passage")
C.para("<b>Naive look</b> — verse length climbs across the revelation; ordering by it reproduces the tradition. "
       "<b>Control 1 · convergence</b> — independent chronologies (tradition, Nöldeke, Bazargan, Sadeghi) agree on "
       "the same Mecca→Medina drift; the signal is not one analyst's artifact. <b>Control 2 · effect size</b> — the "
       "correlation is real and moderate (r = 0.66, R² 0.44); credited. <b>Control 3 · granularity</b> — push from "
       "sūra to passage and the ground gives way: the 'composite' rate is method-dependent (2–74%), and within-sūra "
       "spread (8.4) ≈ between-sūra spread (11.1). <b>Control 4 · degrees of freedom</b> — letting the analyst draw "
       "the passage boundaries supplies all the freedom needed to 'date' anything. The sūra-level clock survives "
       "every gate; passage-level dating fails at Control 3.")

# ── 7 · INTERPRETATION ──
C.section("Interpretation")
C.para("The clock is <b>genuine at the level of the sūra</b> — the divine unit. The traditional order is broadly "
       "confirmed from the text's own statistics; Nöldeke's stylistic reading, Bazargan's verse-length clock, and "
       "Sadeghi's morphological stylometry all <b>converge</b> on it. Bazargan's central claim is correct and "
       "pioneering, and Sadeghi's 2011 program vindicated the quantitative road he opened. That is a real, shared "
       "success — and the credit is genuinely distributed across the field.<br><br>"
       "It fails only at the level of the <b>passage</b> — a unit the analyst draws, not one the text marks. "
       "Internal length-variation is real but is not a datable boundary (method-dependent 2–74%, and within ≈ "
       "between), so cutting a sūra into separately-dated passages over-reaches. This is the divine-division-vs-"
       "human-construct line, and the over-reach is <b>shared</b> with Richard Bell and Blachère, who re-ordered the "
       "text at passage/verse level — it is not unique to Bazargan, nor a flaw in his core insight.")

# ── 8 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>Credit first, and in context.</b> Bazargan worked in the 1970s–80s, applying quantitative method to "
       "scripture before stylometry existed; he is a pioneer whose central intuition the later, sharper tools "
       "confirmed — not to be judged anachronistically against them. <b>The critique is narrow and shared.</b> It "
       "targets only passage-level <i>dating precision</i> — a move common to the whole chronological-rearrangement "
       "tradition (Bell, Blachère) — not anyone's integrity or the sūra-level result. <b>On our instrument.</b> We "
       "count on a normalised rasm and the traditional order (col 8), not any author's exact figures; the "
       "Makkī/Madanī split itself has a few contested sūras (we use the standard list). <b>Same gate on ourselves.</b> "
       "We deliberately report the full 2–74% change-point band so the criticism cannot be tuned to indict anyone — "
       "the very gate we turned on one of our own findings (the inter-sūra coherence), recorded honestly as a size "
       "artifact.")

# ── 9 · VERDICT ──
C.section("Verdict")
C.verdict("CANDIDATE",
          "The Qur'ān's chronology is a real, measurable property of the text: verse length tracks revelation time "
          "(r = 0.66; Meccan 14 → Medinan 30 words/āyah), and the traditional, orientalist and quantitative schools "
          "<b>converge</b> on it. Bazargan's clock is credited and Sadeghi's stylometry vindicates the program. The "
          "single, scoped criticism — shared with Bell and Blachère — is that passage-level dating inside sūras is "
          "not justified (method-dependent 2–74%; within ≈ between). A genuine, partly-validated contribution.",
          "sūra-level clock ~80% MEASURED · passage-level dating ~75% unjustified",
          "a stylometric feature that dates passages above chance and survives multiplicity correction",
          "richer function-word stylometry (à la Sadeghi) at the passage level could revise the boundary upward")

# ── REFLECTION ──
C.section("Reflection")
C.para("This is the mirror-image of the Code 19 case, and the contrast is the lesson. There, a striking pattern had "
       "<i>no</i> data support and earned a refutation. Here, a quantitative claim has <b>real</b> data support, "
       "<b>independent convergence</b> across eleven centuries of scholarship, and a later vindication — so it earns "
       "credit. The same impartial gate produces opposite, deserved verdicts. The only fault is a unit error: "
       "applying a sūra-level signal to analyst-drawn passages. Respect the divine division as the atomic unit, and "
       "the chronology is a genuine, useful instrument; over-reach below it, and it becomes noise.")

# ── SUMMARY ──
C.section("Summary — what holds, what over-reaches")
C.note("In the plainest terms — the credited, converged findings on the left; the single shared over-reach on the right.")
C.table(["✔ Holds — credited & converged", "✗ Over-reaches — scoped"], tight=False, rows=[
    ["Verse length tracks revelation time (r = 0.66)", "Dating arbitrary passages inside a sūra"],
    ["Meccan 14 → Medinan 30 words/āyah", "Within-sūra spread (8.4) ≈ between (11.1)"],
    ["Sūra-order broadly confirms the tradition", "'Composite?' is method-dependent (2–74%)"],
    ["Tradition + Nöldeke + Bazargan + Sadeghi converge", "Over-reach shared with Bell / Blachère"],
    ["Bazargan pioneered it; Sadeghi vindicated it", "One feature; length conflates with genre"],
])

# ── LESSONS LEARNED ──
C.section("Lessons learned — for every chronological claim")
C.para("A template, not a verdict on one person. Any dating claim — traditional, orientalist, or quantitative — must "
       "clear the same gates, applied without favour. Each principle below earned its place in this review.")
C.table(["Principle", "What it caught here"], tight=False, rows=[
    ["≥3 converging modalities, not one road", "tradition + style + numbers agree → the sūra-level clock is trustworthy"],
    ["Match the claim to the unit it can support", "length dates the sūra, not the analyst's passage"],
    ["Effect size, reported honestly (R², not a hit)", "r = 0.66 / R² 0.44 — real and moderate, neither hidden nor inflated"],
    ["Robustness — show the whole band", "composite-rate 2–74%; a single figure would mislead either way"],
    ["Credit pioneers in their context", "Bazargan judged as a 1980s pioneer, not against tools that postdate him"],
    ["Same gate on our own findings", "the change-point gate that scoped this also refuted our inter-sūra coherence"],
])
C.callout("The discipline, in plain terms",
          "A chronology earns belief by <b>convergence and proper effect sizes</b>, and by daring no finer than its "
          "instrument allows — not by the elegance of a single re-ordering. Credit the real signal generously; bound "
          "the over-reach precisely. The same gates that credit Bazargan also refuse passage-level dating, and also "
          "refuted one of <i>our own</i> findings. Rigour without favour.", accent=C.SLATE)

# ── TAKEAWAY ──
C.section("Takeaway")
C.callout("In one line — for every reader",
          "The Qur'ān's chapters <b>can</b> be ordered in time from the text itself — verse length is a real clock, "
          "and the tradition, Nöldeke, Bazargan and Sadeghi all agree on it. The only correction: that clock works "
          "on the <b>sūra</b> (the text's own unit), not on passages an analyst slices out of it. Credit the insight; "
          "bound the over-reach.", accent=C.TEAL)

# ── PERSIAN ABSTRACT ──
C.section("خلاصهٔ کامل — Persian abstract")
st.markdown(
    "<div dir='rtl' id='nz-fa' style='font-family:Vazirmatn,Tahoma,\"Segoe UI\",sans-serif;font-size:15px;"
    "line-height:1.85;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #138A74;"
    "border-radius:11px;padding:16px 20px'>"
    "<b>پرسش.</b> آیا می‌توان سوره‌های قرآن را از روی خودِ متن به‌ترتیبِ زمانِ نزول چید؟ و تا کجا می‌توان دقیق شد — "
    "تا سطحِ «سوره»، یا تا «بخش‌های» درونِ سوره؟<br><br>"
    "<b>چشم‌اندازِ پژوهش (نه فقط بازرگان).</b> این بررسی بر تمامِ میدان است. سنّتِ اسلامی (ترتیبِ نزولِ منسوب به ابن‌عباس "
    "و چاپِ استانداردِ قاهره ۱۹۲۴) بر پایهٔ اسبابِ نزول و روایات است. خاورشناسان نیز کوشیدند: <b>گوستاو وایل</b> "
    "(۱۸۴۴، نخستین گاه‌شماریِ غربی)، <b>تئودور نولدکه</b> (۱۸۶۰، سه دورهٔ مکّی + مدنی بر پایهٔ سبک و محتوا — معیارِ "
    "مرجع)، <b>ویلیام میور</b> (۱۸۶۱، شش دوره)، <b>گریمه</b> و <b>هیرشفلد</b>، و در سدهٔ بیستم <b>ریچارد بل</b> "
    "(۱۹۳۷) و <b>رژیس بلاشر</b> (۱۹۴۷). نکتهٔ مهم: همهٔ این‌ها بر یک «شکلِ کلان» هم‌داستان‌اند — سوره‌های کوتاه و "
    "مقفّای مکّی در آغاز، سوره‌های بلند و فقهیِ مدنی در پایان.<br><br>"
    "<b>پیشگامِ کمّی.</b> <b>مهدی بازرگان</b> در «سیر تحولِ قرآن» با روشی کمّی نشان داد که <b>میانگینِ طولِ آیه در طولِ "
    "دورهٔ نزول افزایش می‌یابد</b> و از این «ساعتِ» سبکی برای ترتیبِ سوره‌ها بهره گرفت — دهه‌ها پیش از سبک‌سنجیِ نوینِ "
    "غربی. این کارِ پیشگامانه را به‌تمامی به او نسبت می‌دهیم.<br><br>"
    "<b>یافتهٔ سنجیده (اعتبارِ کار).</b> ادعای اصلی <b>درست</b> است: طولِ آیه با ترتیبِ سنّتیِ نزول هم‌بستگی دارد "
    "(r = ۰٫۶۶؛ اسپیرمن ۰٫۶۹؛ R² = ۰٫۴۴). به‌زبانِ ساده: میانگینِ واژه در هر آیه از ۱۴ واژه در سوره‌های مکّی به ۲۹٫۷ "
    "واژه در سوره‌های مدنی می‌رسد — بیش از دو برابر. سوره‌های کوتاه (اخلاص، ناس، عبس) در یک سو و بلند (ممتحنه، مائده، "
    "طلاق، بقره) در سوی دیگرند. افزون بر این، <b>بهنام صادقی</b> (۲۰۱۱) با سبک‌سنجیِ صرفی همان گاه‌شماری را تأیید کرد — "
    "یعنی برنامهٔ بازرگان <b>موفق</b> بود. سه راهِ مستقل — روایات، سبکِ نولدکه، و اعدادِ بازرگان/صادقی — به یک نتیجه "
    "می‌رسند؛ این هم‌گرایی، بخشِ نیرومندِ گاه‌شماری است.<br><br>"
    "<b>نقدِ محدود و منصفانه.</b> تنها اشکال، تاریخ‌گذاریِ «بخش‌ها» در درونِ یک سوره است. پراکندگیِ طولِ آیه در "
    "<i>درونِ</i> یک سوره (≈۸٫۴) تقریباً به‌اندازهٔ پراکندگیِ میانگین‌ها <i>میانِ</i> سوره‌هاست (≈۱۱٫۱)، و «آیا این "
    "سوره مرکّب است؟» بسته به آزمون از ۲٪ تا ۷۴٪ نوسان دارد — یعنی بی‌پاسخ. پس بریدنِ سوره به بخش‌ها و تاریخ‌گذاریِ "
    "جداگانهٔ آن‌ها از راهِ طول موجّه نیست. این خطا — که با ریچارد بل و بلاشر مشترک است — خطایی در «واحد» است: اعمالِ "
    "سیگنالی سوره‌ای بر بخش‌هایی که خودِ پژوهشگر می‌بُرد، نه متن.<br><br>"
    "<b>کجا هر روش کم می‌آورد و راهِ بهبود.</b> اسبابِ نزولِ سنّتی گاه دیرهنگام و مورد اختلاف است → با سیگنالِ درونیِ "
    "سبک اعتبارسنجی شود (که ترتیبِ کلان را تأیید می‌کند). مرزهای تیزِ سه‌دورهٔ نولدکه پیوسته‌اند نه گسسته → آن‌ها را "
    "طیف ببینیم. روشِ ذوقیِ وایل/میور تکرارناپذیر است → کمّی شود. تاریخ‌گذاریِ بخش‌محورِ بل/بلاشر ناپایدار است → به سطحِ "
    "سوره محدود شود. تک‌ویژگیِ بازرگان (فقط طول) → سبک‌سنجیِ چندمتغیّره (همان بهبودِ ۰٫۴۴ به ۰٫۴۹). و سبک‌سنجیِ صادقی، "
    "ابزارِ درست برای کاوشِ بخش‌هاست — تنها آن‌جا که شکستِ سبکیِ واقعی آشکار باشد.<br><br>"
    "<b>انصافِ بی‌طرفانه.</b> این داوری از سرِ خصومت نیست؛ همان دروازه‌ای که تاریخ‌گذاریِ بخش‌ها را رد کرد، بر یافتهٔ "
    "خودِ ما (هم‌بستگیِ میان‌سوره‌ای) نیز اعمال شد و آن را «مصنوعِ اندازه» ثبت کردیم. باندِ کاملِ ۲–۷۴٪ را آگاهانه نشان "
    "می‌دهیم تا نقد قابلِ تنظیم نباشد.<br><br>"
    "<b>نتیجه.</b> گاه‌شماریِ قرآن خاصیتی واقعی و سنجش‌پذیرِ متن است؛ ساعتِ سبکی در سطحِ <b>سوره</b> (واحدِ متن) معتبر "
    "است و میدانِ سنّتی، خاورشناسانه و کمّی بر آن هم‌گرایند. اعتبارِ کارِ بازرگان بر جای می‌ماند؛ تنها در سطحِ «بخش» "
    "فروتر می‌رود.<br><br>"
    "<b>درس.</b> هر ادعای گاه‌شناختی — سنّتی، خاورشناسانه یا کمّی — باید بر هم‌گراییِ چند مدرک و اندازهٔ اثرِ صادقانه "
    "استوار باشد و از مرزِ ابزار فراتر نرود؛ سیگنالِ واقعی را سخاوتمندانه ارج نهیم و زیاده‌روی را دقیق محدود کنیم — نه "
    "عوام‌گرایانه و عوام‌پسند.</div>", unsafe_allow_html=True)

# ── ARABIC ABSTRACT ──
C.section("الملخّص الكامل — Arabic abstract")
st.markdown(
    "<div dir='rtl' id='nz-ar' style='font-family:Amiri,\"Scheherazade New\",Tahoma,serif;font-size:15.5px;"
    "line-height:1.9;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;"
    "border-radius:11px;padding:16px 20px'>"
    "<b>السؤال.</b> هل يمكن ترتيبُ سُوَر القرآن زمنياً من النصّ نفسِه؟ وإلى أيّ حدٍّ نُدقّق — إلى مستوى «السورة» أم إلى "
    "«المقاطع» داخلها؟<br><br>"
    "<b>مسحُ الميدان كلِّه (لا بازركان وحده).</b> التقليدُ الإسلاميّ (ترتيبُ النزول المنسوب إلى ابن عبّاس وطبعةُ القاهرة "
    "المعياريّة ١٩٢٤) يقوم على أسباب النزول والروايات. واجتهد المستشرقون: <b>غوستاف فايل</b> (١٨٤٤، أوّل ترتيب غربيّ)، "
    "و<b>تيودور نولدكه</b> (١٨٦٠، ثلاثُ مراحل مكّيّة + مدنيّة بناءً على الأسلوب والمضمون — وهو المرجع)، و<b>وليم ميور</b> "
    "(١٨٦١، ستُّ مراحل)، و<b>غريمه</b> و<b>هيرشفلد</b>، ثمّ في القرن العشرين <b>ريتشارد بِل</b> (١٩٣٧) و<b>ريجيس "
    "بلاشير</b> (١٩٤٧). والمهمّ أنّ هذه المدارس تتّفق على «الشكل العامّ»: سورٌ مكّيّةٌ قصيرةٌ مقفّاةٌ أوّلاً، ومدنيّةٌ "
    "طويلةٌ تشريعيّةٌ آخِراً.<br><br>"
    "<b>الرائد الكمّيّ.</b> أظهر <b>مهدي بازركان</b> في «سير تطوّر القرآن» بمنهجٍ كمّيّ أنّ <b>متوسّط طول الآية يتزايد "
    "عبر مدّة النزول</b>، واتّخذ من هذه «الساعة» الأسلوبية ترتيباً للسور — قبل علم الأسلوب الغربيّ بعقود. ننسب هذا "
    "الفضل إليه كاملاً.<br><br>"
    "<b>النتيجة المقيسة (تقديرُ العمل).</b> الدعوى الأساسية <b>صحيحة</b>: طولُ الآية يرتبط بترتيب النزول التقليديّ "
    "(r = ٠٫٦٦؛ سبيرمان ٠٫٦٩؛ R² = ٠٫٤٤). وببساطة: يرتفع متوسّطُ الكلمات في الآية من ١٤ كلمة في السور المكّيّة إلى ٢٩٫٧ "
    "في المدنيّة — أكثر من الضعف. القصارُ (الإخلاص، الناس، عبس) في طرفٍ والطوالُ (الممتحنة، المائدة، الطلاق، البقرة) في "
    "طرف. كما أيّد <b>بهنام صادقي</b> (٢٠١١) بالأسلوب الإحصائيّ الصرفيّ الترتيبَ نفسَه — أي أنّ برنامج بازركان <b>نجح</b>. "
    "ثلاثُ طرقٍ مستقلّة — الروايات، وأسلوبُ نولدكه، وأرقامُ بازركان/صادقي — تبلغ النتيجةَ نفسَها؛ وهذا التقاطعُ هو الجزءُ "
    "القويّ من التأريخ.<br><br>"
    "<b>النقد المحدود والمنصف.</b> العيبُ الوحيد هو تأريخُ «المقاطع» داخل السورة. فتشتّتُ طول الآية <i>داخل</i> السورة "
    "(≈٨٫٤) يقارب تشتّتَ المتوسّطات <i>بين</i> السور (≈١١٫١)، و«هل هذه السورة مركّبة؟» يتراوح حسب الاختبار من ٢٪ إلى "
    "٧٤٪ — أي بلا جواب. فتقطيعُ السورة وتأريخُ كلٍّ بالطول غيرُ مبرَّر. وهذا الخطأ — المشترَك مع بِل وبلاشير — خطأٌ في "
    "«الوحدة»: تطبيقُ إشارةٍ على مستوى السورة على مقاطعَ يرسمها الباحثُ لا النصّ.<br><br>"
    "<b>أين يقصر كلُّ منهجٍ وكيف يُصلَح.</b> أسبابُ النزول التقليديّة قد تكون متأخّرةً أو خلافيّة → تُعاضَد بالإشارة "
    "الأسلوبية الداخلية (التي تؤكّد الترتيبَ العامّ). وحدودُ مراحل نولدكه الثلاث متدرّجةٌ لا قاطعة → تُقرأ طيفاً. ومنهجُ "
    "فايل/ميور الذوقيّ غيرُ قابلٍ للتكرار → يُكمَّم. وتأريخُ بِل/بلاشير المقطعيّ غيرُ مستقرّ → يُقصَر على السورة. "
    "وأحاديّةُ بازركان (الطول فقط) → أسلوبٌ متعدّد المتغيّرات (تحسّنُ ٠٫٤٤ إلى ٠٫٤٩). وأسلوبُ صادقي هو الأداةُ الصحيحة "
    "لسبر المقاطع — حيث يظهر انكسارٌ أسلوبيٌّ حقيقيّ فقط.<br><br>"
    "<b>الإنصافُ بلا محاباة.</b> ليس هذا خصومةً؛ فالبوّابةُ نفسُها التي ردّت تأريخَ المقاطع طُبِّقت على اكتشافنا "
    "(التماسكِ بين السور) فسجّلناه «مصنوعَ حجمٍ». ونعرض نطاقَ ٢–٧٤٪ كاملاً عمداً كي لا يكون النقدُ قابلاً للضبط.<br><br>"
    "<b>الخلاصة.</b> تأريخُ القرآن خاصّيةٌ حقيقيّةٌ قابلةٌ للقياس؛ والساعةُ الأسلوبية صحيحةٌ على مستوى <b>السورة</b> "
    "(وحدة النصّ)، ويتقاطع عليها الميدانُ التقليديّ والاستشراقيّ والكمّيّ. يبقى تقديرُ عملِ بازركان قائماً؛ وإنّما يقصر "
    "على مستوى «المقطع».<br><br>"
    "<b>الدرس.</b> كلُّ دعوى تأريخيّة — تقليديّةً كانت أم استشراقيّةً أم كمّيّة — يجب أن تقوم على تقاطُع الأدلّة وحجمِ "
    "الأثر الصادق، وألّا تتجاوز حدَّ الأداة؛ نُقدّر الإشارةَ الحقيقيّة بسخاء ونحدّ التجاوزَ بدقّة — لا تملّقاً للعامّة "
    "(عوام‌گرایی / عوام‌پسند).</div>", unsafe_allow_html=True)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
