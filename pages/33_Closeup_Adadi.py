"""Close-up · The numerical-word-count miracle (al-iʿjāz al-ʿadadī), reviewed — REFUTED-ARTIFACT.
Comprehensive, fair, data-driven review of the equal-frequency claims (Nawfal et al.). Sibling of Code 19.
All counts MEASURED on Book6 rasm tokens; the null and orthographic tests are measured; the Uthmānī-substrate
limitation is stated honestly."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Word-count miracle", page_icon="🧮", layout="wide")
if S:
    try:
        S.log_page("closeup_adadi")
    except Exception:
        pass
    for fn in ("inject_css", "render_grouped_nav"):
        try:
            getattr(S, fn)()
        except Exception:
            pass
C.inject()
Y, Pr, No = "✔ holds", "~ near", "✗ fails"

# ── 1 · PROBLEM ──
C.hero("The word-count miracle (al-iʿjāz al-ʿadadī), reviewed",
       "Do paired words — day/month, life/death, men/women, dunyā/ākhira — occur an EQUAL number of times in the "
       "Qur'ān by design, or is 'equal frequency' what counting freedom and chance produce anyway?",
       "REFUTED-ARTIFACT", 35, "rasm-WORD tokens (Book6 col 6)", "DIVINE-DEFAULT · RANDOM null")
st.markdown(
    "<div style='display:flex;justify-content:flex-end;gap:9px;margin:7px 0 2px;flex-wrap:wrap'>"
    "<a href='#ad-fa' style='text-decoration:none'>"
    "<div style='background:linear-gradient(135deg,#138A74,#10243A);color:#fff;border-radius:9px;padding:7px 13px;"
    "font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(16,36,58,.25);border:1px solid rgba(255,255,255,.3)'>"
    "📄 Persian abstract · خلاصهٔ فارسی ↓</div></a>"
    "<a href='#ad-ar' style='text-decoration:none'>"
    "<div style='background:linear-gradient(135deg,#4E6E92,#10243A);color:#fff;border-radius:9px;padding:7px 13px;"
    "font-weight:800;font-size:13px;box-shadow:0 2px 8px rgba(16,36,58,.25);border:1px solid rgba(255,255,255,.3)'>"
    "📄 Arabic abstract · الملخّص العربي ↓</div></a></div>", unsafe_allow_html=True)
C.onpage(["① Problem", "② Hypothesis", "③ Method",
          "<b>④ Results Part 1</b> the claims, counted (scorecards)",
          "<b>⑤ Results Part 2</b> the mechanism (null + orthography, 4 charts)",
          "⑥ Gating", "⑦ Interpretation", "⑧ Caveats", "⑨ Verdict"], fa="ad-fa", ar="ad-ar",
         closers="<b>Path forward</b> (what would settle it) · Reflection · Summary · Lessons · Takeaway")
C.story(
    "The claim — popularised by ʿAbd al-Razzāq Nawfal — is a <b>pervasive system of equal word-frequencies</b> as a "
    "numerical miracle: dunyā = ākhira, life = death, angels = devils, day = 365. Counted on the text under one fixed "
    "rule, the result splits exactly like <b>Code 19</b>: a few pairs genuinely match (dunyā = ākhira = 114; "
    "Ādam = ʿĪsā = 25), but most do not — and every count rides on a spelling choice.",
    "A sibling of the Code 19 review, held to the same gates. مقبول for the general reader (a clear scorecard), "
    "مطلوب for the specialist (every count, the null, the orthographic test). It <b>credits the genuine "
    "coincidences fairly</b> and refutes only the <i>pervasive</i> miracle. A methodological verdict, not a "
    "theological one.", accent=C.CORAL)
C.kpis([
    ("dunyā = ākhira", "114 = 114 ✓", "The flagship pair: both 114 on our rasm (claim 115 each) — genuinely equal; credited", C.TEAL),
    ("Ādam = ʿĪsā", "25 = 25 ✓", "Both exactly 25 — and the Qur'ān itself parallels them (Q 3:59); credited", C.TEAL),
    ("life ≠ death", "74 vs 51", "Claimed equal at 145; under one fixed rule they are not", C.CORAL),
    ("angels ≠ devils", "73 vs 17", "Claimed 88 each; measured wildly unequal", C.CORAL),
    ("114 → 0", "spelling swing", "ākhira = 114 as آخرة, but 0 as اخرة / الآخرة — counts ride on orthography", C.CORAL),
    ("2.9%", "chance equal-rate", "Two content-words (freq ≥ 10) share an exact count 2.9% of the time", C.GOLD),
    ("35", "grade", "REFUTED-ARTIFACT — real anchors, but no pervasive numerical law", C.CORAL),
])

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If equal frequencies are a designed miracle, three things must ALL hold",
          "Two claims are blurred, and we separate them. The <i>weak</i> claim: some word pairs happen to have "
          "equal counts — easy, and partly true. The <i>strong</i> claim: the text <b>encodes</b> a pervasive "
          "system of equalities. We test the strong one through three predictions.<br>"
          "&nbsp;&nbsp;<b>(1) The pair must actually be equal</b> under a single, fixed counting rule — member-1 = "
          "member-2, not merely each near some quoted number.<br>"
          "&nbsp;&nbsp;<b>(2) Robustness.</b> The count must survive a change of spelling and word-form; a law of "
          "the text cannot hinge on whether one writes آخرة or اخرة, or counts the plural.<br>"
          "&nbsp;&nbsp;<b>(3) Above chance, not cherry-picked.</b> Equal counts must occur <i>more</i> than chance "
          "gives for the relevant frequency, and the reported pairs must not be a selection from a far larger pool "
          "of misses.<br>"
          "The null is mundane: with thousands of word-types, many spellings per concept, and a free choice of which "
          "'opposite' to pair, <b>some</b> equalities are guaranteed. We let the data choose.", accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus — one fixed rule, a real null, and an orthographic stress-test",
          "<b>Substrate.</b> rasm-WORD tokens (Book6 col 6): 135,366 tokens, 7,236 distinct types, counted by exact "
          "token match — one fixed, declared rule, applied to every claim alike.<br>"
          "&nbsp;&nbsp;<b>Three tests.</b> (a) <i>Verification</i> — count each claimed word/pair directly. (b) "
          "<i>The null</i> — for each claimed count, how many other word-types share it exactly, how many fall "
          "within ±5%, and how often two random content-words are equal at all. (c) <i>Robustness</i> — re-count "
          "each concept under its spelling/word-form variants, to see whether the number is stable or an artefact "
          "of one orthographic choice.<br>"
          "&nbsp;&nbsp;<b>The honest limitation — stated up front.</b> Our rasm is morphologically segmented and "
          "mixed in orthography (dunyā is written with an Arabic yāʾ while most of the corpus uses the Persian "
          "form), so our absolute numbers are <i>not</i> the standard Uthmānī whole-word tallies the claims use — "
          "on a clean Uthmānī text dunyā and ākhira are classically 115 each. We therefore test <b>robustness and "
          "mechanism</b>, not the 'true' tally: a claim whose count flips with the convention was never a law of "
          "the text. (The same limitation we declared for Code 19.)", accent=C.SLATE)

# ── 4 · RESULTS · PART 1 — THE CLAIMS, COUNTED ──
C.section("Results · Part 1 — the claims, counted (our data)")
C.note("MEASURED. The famous claims, each counted under the one fixed rule. Read the EQUAL-PAIR claims by whether "
       "the two members actually equal each other — not whether each is near a quoted number.")
cP, cS = st.columns(2, gap="medium")
with cP:
    C.note("A · Equal-pair claims — is member-1 = member-2?")
    C.table(["Pair (claim = N each)", "m₁", "m₂", "v"], [
        [C.ar("الدنیا") + " / " + C.ar("آخرة") + " · 115", "114", "114", Y],
        [C.ar("آدم") + " / " + C.ar("عیسى") + " · 25", "25", "25", Y],
        [C.ar("حیاة") + " / " + C.ar("موت") + " · 145", "74", "51", No],
        [C.ar("ملائکة") + " / " + C.ar("شیاطین") + " · 88", "73", "17", No],
        [C.ar("رجال") + " / " + C.ar("نساء") + " · 24", "19", "52", No],
    ])
with cS:
    C.note("B · Single-count & ratio claims.")
    C.table(["Claim", "claim", "meas.", "v"], [
        [C.ar("إبلیس") + " (Iblīs)", "11", "11", Y],
        [C.ar("بحر") + " (sea)", "32", "33", Pr],
        [C.ar("شهر") + " (month)", "12", "10", Pr],
        [C.ar("یوم") + " (day, sing.)", "365", "420", No],
        [C.ar("بر") + " (land)", "13", "21", No],
        [C.ar("نساء") + " (women)", "24", "52", No],
    ])
C.note("① Equal-pair reality — the two actual counts of each famous pair, side by side. Two pairs land together "
       "(teal: dunyā/ākhira, Ādam/ʿĪsā); three are plainly unequal (coral). 'Equal frequency' is the exception "
       "here, not the rule.")
C.vbars([(C.ar("الدنیا", 19) + " world", 114, C.TEAL, "dunyā = 114"),
         (C.ar("آخرة", 19) + " hereafter", 114, C.TEAL, "ākhira = 114 — equal ✓"),
         (C.ar("آدم", 19) + " Adam", 25, C.TEAL, "Ādam = 25"),
         (C.ar("عیسى", 19) + " Jesus", 25, C.TEAL, "ʿĪsā = 25 — equal ✓"),
         (C.ar("حیاة", 19) + " life", 74, C.CORAL, "life = 74"),
         (C.ar("موت", 19) + " death", 51, C.CORAL, "death = 51 — NOT equal"),
         (C.ar("ملائکة", 19) + " angels", 73, C.CORAL, "angels = 73"),
         (C.ar("شیاطین", 19) + " devils", 17, C.CORAL, "devils = 17 — NOT equal")],
        ymax=125, fmt="{:.0f}")
C.note("Of the five famous EQUAL-PAIRS, <b>2 are internally equal</b> (dunyā/ākhira, Ādam/ʿĪsā) and 3 are not. The "
       "two that hold are real and creditable — and Ādam/ʿĪsā even has the Qur'ān's own warrant (Q 3:59, "
       "“the likeness of Jesus … is as the likeness of Adam”). The pervasive system, though, is already breaking.")

# ── 5 · RESULTS · PART 2 — THE MECHANISM ──
C.section("Results · Part 2 — why equal counts appear (the null & orthography)")
C.note("② Orthographic fragility — the same concept under different spellings/forms gives wildly different counts. "
       "‘Hereafter’ is 114 as آخرة but 0 as اخرة or الآخرة; ‘angels’ is 73 as ملائکة but 0 as ملئکة. A genuine "
       "numerical law is indifferent to spelling; a counting artefact lives precisely there — the Code 19 lesson, "
       "reproduced for words.")
C.vbars([(C.ar("آخرة", 19) + " (madda)", 114, C.TEAL, "آخرة = 114"),
         (C.ar("آخر", 19) + " (no -a)", 45, C.SLATE, "آخر = 45"),
         (C.ar("اخرة", 19) + " (plain alif)", 0, C.CORAL, "اخرة = 0"),
         (C.ar("الآخرة", 19) + " (+article)", 0, C.CORAL, "الآخرة = 0 (article split off)")],
        ymax=125, fmt="{:.0f}")
C.note("③ The null · partner abundance — how many OTHER word-types share each claimed count exactly. At the low "
       "counts many claims use, partners are everywhere (66 share the count 11; 23 share 24); at high counts they "
       "are scarce (0 share 88 or 115). So a low-count 'match' is trivially findable, while the high-count matches "
       "(dunyā/ākhira) are genuinely rarer — and duly credited.")
C.hist([66, 64, 23, 15, 12, 0, 0, 0], ["11", "12", "24", "25", "32", "88", "115", "365"], highlight=0, color=C.SLATE)
C.note("④ The null · ±5% band — how many word-types fall within ±5% of each target. With even a little tolerance, "
       "the low-count bands are crowded (204 types near 11; ~100 near 24–25), so 'approximately equal' is almost "
       "guaranteed for the small numbers many claims invoke.")
C.vbars([("near 11 (±5%)", 204, C.SLATE, "204 types within 10–12"),
         ("near 24", 101, C.SLATE, "101 types within 22–26"),
         ("near 25", 99, C.SLATE, "99 types within 23–27"),
         ("near 88", 15, C.GOLD, "15 types within 83–93"),
         ("near 115", 10, C.GOLD, "10 types within 109–121"),
         ("near 365", 6, C.GOLD, "6 types within 346–384")], ymax=220, fmt="{:.0f}")
C.note("⑤ The null · how often ANY two words are equal — by frequency floor. Among all types it is 24% (the corpus "
       "is full of rare words); among real content-words (freq ≥ 10) it settles to ~3%. So equal frequency is "
       "common for small words and merely uncommon — not miraculous — for larger ones, before any counting freedom "
       "is added.")
C.vbars([("all types", 0.240, C.CORAL, "P(two random types share a count) = 24%"),
         ("freq ≥ 10", 0.029, C.GOLD, "content-words: 2.9%"),
         ("freq ≥ 20", 0.017, C.GOLD, "1.7%"),
         ("freq ≥ 50", 0.004, C.INK, "0.4%")], ymax=0.28, fmt="{:.1%}")

# ── 6 · GATING CHAIN ──
C.section("Gating chain — striking, then ordinary")
C.para("<b>Naive look</b> — dunyā = ākhira = 114, Ādam = ʿĪsā = 25: arresting, and genuinely real. <b>Control 1 · "
       "the pair test</b> — most famous pairs are <i>not</i> internally equal (life 74 ≠ death 51; angels 73 ≠ "
       "devils 17; men 19 ≠ women 52). <b>Control 2 · spelling</b> — the matches that hold ride on one orthographic "
       "form (ākhira 114 → 0 under اخرة; angels 73 → 0 under ملئکة). <b>Control 3 · the null</b> — at the low counts "
       "many claims use, dozens-to-hundreds of partner words sit within ±5%, so 'a match' is almost free; equal "
       "frequency among content-words is ~3% even before counting freedom. <b>Control 4 · degrees of freedom</b> — "
       "choose the spelling, choose whether to add the article or the plural, choose which 'opposite' to pair, and "
       "select the hits from a large pool of attempts: that supplies every match needed. The <i>pervasive</i> "
       "miracle collapses; a small real cluster (dunyā/ākhira, Ādam/ʿĪsā) remains a genuine curiosity.")

# ── 7 · INTERPRETATION ──
C.section("Interpretation")
C.para("<b>The split is the same as Code 19, now for words instead of letters.</b> Sort each claim by one question "
       "— does its count depend on a spelling or word-form choice? — and the verdicts sort with it. The claims that "
       "hold do so for counts that happen to be stable on our rasm; the claims that fail are exactly those whose "
       "count moves when the spelling, the article, or the plural is counted differently. A genuine numerical law "
       "could not care how a scribe spells a word — arithmetic is indifferent to orthography — whereas a counting "
       "artefact lives precisely in that freedom.<br><br>"
       "<b>Why equal counts appear at all.</b> The Qur'ān has thousands of word-types, most of them infrequent; "
       "two random words share a count about a quarter of the time, and a fifth of content-words sit within a few "
       "of any small target. Give a counter several spellings per concept and a free choice of which words count as "
       "‘a pair’, and matches assemble themselves out of selection. The reported equalities are the hits; the far "
       "larger set of misses — which we counted — goes unreported. This is the multiple-comparisons trap that also "
       "drives <b>Code 19</b>, and from the inside it is invisible.<br><br>"
       "<b>In fairness, the anchors are real.</b> dunyā = ākhira = 114 and Ādam = ʿĪsā = 25 are not spelling-fragile "
       "coincidences of the trivial kind — at those frequencies, exact equality is genuinely uncommon (Control 3), "
       "and Ādam/ʿĪsā is a parallel the Qur'ān itself draws. We credit them as a small, real cluster — exactly as "
       "we credited the stable-letter facts in Code 19 — while refuting the claim that the <i>whole</i> lexicon is "
       "an equal-frequency system.")

# ── 8 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>On our instrument — the central caveat.</b> Our rasm is segmented and mixed in orthography, so our "
       "absolute counts are not the Uthmānī whole-word tallies the claims are built on; on a clean Uthmānī text "
       "some counts (dunyā, ākhira) classically reach 115. We do not adjudicate the 'true' Uthmānī number "
       "word-by-word. What we show is precise and convention-independent: (i) most famous pairs are <i>not</i> "
       "internally equal under any single rule, (ii) the counts that do match are spelling-fragile, and (iii) equal "
       "frequency is what chance plus counting freedom produce anyway. Each of these would have to be overturned on "
       "a clean corpus for the pervasive claim to stand — and a pre-registered, fixed-rule recount is the way to "
       "do it.<br><br>"
       "<b>In fairness — what we are NOT claiming.</b> We do not say every count is wrong, nor that those moved by "
       "dunyā = ākhira are careless: that pair, and Ādam = ʿĪsā, are real and striking. We refute the <i>pervasive "
       "numerical miracle</i>, not the existence of a small real cluster. <b>Same gate on ourselves.</b> The very "
       "null and robustness tests applied here also refuted one of our own findings (the inter-sūra coherence, a "
       "size artefact) — rigour without favour. <b>This is a statistical and methodological verdict, not a "
       "theological one.</b>")

# ── 9 · VERDICT ──
C.section("Verdict")
C.verdict("REFUTED-ARTIFACT",
          "A small, genuine cluster of equal counts exists — dunyā = ākhira = 114 and Ādam = ʿĪsā = 25 (the latter "
          "with the Qur'ān's own parallel) — fairly credited. But the <b>pervasive</b> equal-frequency miracle "
          "fails: most famous pairs are not internally equal under a fixed rule (life ≠ death, angels ≠ devils, "
          "men ≠ women), the matches that hold are spelling-fragile (114 → 0 with one form), and equal frequency is "
          "what chance plus counting freedom produce — partners crowd every low target. Not a governing system.",
          "~80% the pervasive miracle is selection + counting freedom; the dunyā/ākhira & Ādam/ʿĪsā anchors are real",
          "a pre-registered, spelling-fixed scheme on a clean Uthmānī text showing the pairs equal far above chance",
          "such a recount, if it held across the full pair-list, would reopen it — none has survived to date")

# ── PATH FORWARD ──
C.section("The path forward — what would settle the word-count claim, ranked by decisiveness")
C.note("Not generic advice. The text is not the limit here — our substrate is; so this lists, ranked by probability "
       "of <b>decisively settling</b> the claim, the moves <b>grounded in what we measured</b>. Each amplifies a "
       "control that worked or retires a freedom that manufactured the matches. One move (row 4) could even <b>raise "
       "the standing of the real anchors</b>. Bases MEASURED; probabilities INFERRED over them.")
gA, gD = st.columns(2, gap="medium")
with gA:
    C.table(["▲ Amplify — what a decisive test keeps"], tight=False, rows=[
        ["The high-count anchors (dunyā/ākhira, Ādam/ʿĪsā) — rare-by-chance, worth a clean test"],
        ["A clean Uthmānī whole-word corpus + pre-registered per-concept counting rules"],
        ["The FULL published pair-list + a proper null — hits AND misses"],
        ["A single fixed orthography — counts collapse to 0 without it"],
    ])
with gD:
    C.table(["▼ Demote — the freedoms that made the matches"], tight=False, rows=[
        ["Spelling / word-form flexibility (ākhira 114 → 0; angels 73 → 0)"],
        ["Free choice of which ‘opposite’ counts as the pair"],
        ["Reporting the matches, dropping the misses"],
        ["Counting on a segmented, mixed-orthography substrate (our own caveat)"],
    ])
C.note("The program, ranked by P(decisively settles the claim). #1 is the verdict's own ‘flip’ test; #4 is the fair "
       "move that could credit the genuine cluster.")
C.table(["#", "Move — grounded & testable", "Built on (MEASURED)", "Retires", "P→settle"], tight=False, rows=[
    ["1", "Clean Uthmānī whole-word corpus + pre-register ONE counting rule per concept (forms/article/plural), fixed before counting", "orthographic fragility (counts → 0) + the substrate caveat", "segmented/mixed-orthography ambiguity & post-hoc form choice", "0.80"],
    ["2", "Test the FULL published pair-list (Nawfal's roster), report every match AND miss", "the 2-of-5 hit pattern + the multiple-comparisons null", "cherry-picking", "0.78"],
    ["3", "Null per frequency: P(a random opposite matches within tolerance) at each claimed count", "partner-abundance (66 at 11; 0 at 88/115); equal-rate 2.9–24%", "‘equal = miraculous’ without a baseline", "0.72"],
    ["4", "Isolate & pre-register the anchors (dunyā/ākhira, Ādam/ʿĪsā) on the clean corpus; if exact, credit a small genuine feature", "measured 114/114, 25/25 + their rarity-by-chance", "lumping the anchors with the failed pervasive claim", "0.60"],
    ["5", "Independent replication under the protocol", "none has survived to date", "in-house counts", "0.50"],
])
C.vbars([("① clean-corpus fixed-rule recount", 0.80, C.TEAL, "removes the convention-freedom that drives it"),
         ("② full pair-list (hits+misses)", 0.78, C.TEAL, "the measured 2-of-5 pattern + null decide it"),
         ("③ null per frequency", 0.72, C.TEAL, "is 'equal' above chance at THAT frequency?"),
         ("④ isolate the real anchors", 0.60, C.GOLD, "fair move — could RAISE the anchors' standing"),
         ("⑤ independent replication", 0.50, C.GOLD, "none to date")],
        ymax=1.0, fmt="{:.0%}")
C.callout("The recommendation — the one test that decides it",
          "Run <b>#1</b>: a pre-registered fixed-rule count on a clean Uthmānī whole-word corpus, with one declared "
          "rule per concept and the full pair-list. The measured <b>orthographic fragility</b> (counts → 0 with a "
          "spelling change) shows the entire dispute lives in counting convention — fix it, count everything, and the "
          "pervasive claim either clears the null (it has not) or is settled. Pair it with <b>#4</b> to give the real "
          "anchors (dunyā = ākhira, Ādam = ʿĪsā) the clean, fair test they deserve.", accent=C.CORAL)

# ── REFLECTION ──
C.section("Reflection")
C.para("This is Code 19's twin, and the same three lessons hold.<br><br>"
       "<b>The pull is real.</b> dunyā = ākhira and Ādam = ʿĪsā genuinely match, and the mind is built to read "
       "design into such coincidence. An honest review begins by granting them — and even noting that one is a "
       "parallel the text itself draws.<br><br>"
       "<b>The over-reach is equally real.</b> A lexicon of thousands of words, most of them rare, with several "
       "spellings each and a free hand in pairing 'opposites', will hand a determined counter all the equalities "
       "they want. Report the hits, drop the misses, and a 'numerical miracle' assembles itself out of selection.<br><br>"
       "<b>The cure is the same: count everything, fix the rule, keep the spelling honest.</b> When we did, most "
       "pairs were unequal, the matches rode on orthography, and equal frequency turned out to be ordinary. A "
       "pattern is worth exactly as much as the null it was tested against — letters in Code 19, words here.")

# ── SUMMARY ──
C.section("Summary — what holds, what fails")
C.note("In the plainest terms — the genuine equalities on the left, the claims that do not survive a fixed-rule "
       "count on the right.")
C.table(["✔ Holds — credited", "✗ Fails — under a fixed rule"], tight=False, rows=[
    ["dunyā = ākhira = 114 (claim 115 each)", "life 74 ≠ death 51 · angels 73 ≠ devils 17"],
    ["Ādam = ʿĪsā = 25 — with Q 3:59's own parallel", "men 19 ≠ women 52 · day 420 ≠ 365"],
    ["Iblīs = 11 · baḥr ≈ 32 (33)", "the matches flip to 0 under a spelling change"],
    ["— a small, real cluster —", "equal frequency is ~3–24% by chance; partners crowd every low target"],
])

# ── LESSONS LEARNED ──
C.section("Lessons learned — for every numerical claim about the Book")
C.para("The same template as Code 19, applied without favour. Each principle earned its place here too.")
C.table(["Principle", "What it caught in this review"], tight=False, rows=[
    ["Test the pair, not the quoted number", "most 'equal' pairs are not internally equal (life ≠ death, angels ≠ devils)"],
    ["Robust — survive spelling & word-form", "ākhira 114 → 0 under اخرة; angels 73 → 0 under ملئکة"],
    ["A proper null — vs chance at that frequency", "equal counts are ~3% (freq ≥ 10) to 24% (all) by chance; partners crowd low targets"],
    ["No degrees of freedom — fix the rule first", "spelling + article + plural + free pairing supply every match needed"],
    ["Count everything, not just the hits", "the unreported misses outnumber the reported equalities"],
    ["Credit the genuine anchors fairly", "dunyā/ākhira & Ādam/ʿĪsā are real — refute the pervasive code, not the cluster"],
])
C.callout("The discipline, in plain terms",
          "An equality earns belief by surviving a <b>fixed rule, a spelling change, and a proper null</b> — not by "
          "being striking or paired with its semantic opposite. It must be <b>methodologically sound and "
          "statistically valid</b>, never " + C.ar("عوام گرایی", 17) + " or " + C.ar("عوام پسند", 17) + " "
          "(crowd-pleasing). The same gates that refuted this also refuted one of <i>our own</i> findings — rigour "
          "without favour, for claims we dislike and claims we would love to be true alike.", accent=C.SLATE)

# ── TAKEAWAY ──
C.section("Takeaway")
C.callout("In one line — for every reader",
          "A few word-counts in the Qur'ān really are equal — dunyā = ākhira, Ādam = ʿĪsā — and those are worth "
          "marvelling at. But there is <b>no pervasive equal-frequency code</b>: most famous pairs are unequal, the "
          "matches depend on a spelling, and 'equal counts' are what chance and counting freedom produce. Credit the "
          "cluster; retire the miracle. See also the <b>Code 19</b> review — the same mechanism, for letters.",
          accent=C.CORAL)

# ── PERSIAN ABSTRACT ──
C.section("خلاصهٔ کامل — Persian abstract")
st.markdown(
    "<div dir='rtl' id='ad-fa' style='font-family:Vazirmatn,Tahoma,\"Segoe UI\",sans-serif;font-size:15px;"
    "line-height:1.85;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #DD5A47;"
    "border-radius:11px;padding:16px 20px'>"
    "<b>ادعا.</b> «اعجازِ عددی» (که عبدالرزاق نوفل و دیگران رواج دادند) می‌گوید واژه‌های متناظر در قرآن به‌شمارِ "
    "برابر آمده‌اند — دنیا و آخرت، حیات و موت، مرد و زن، فرشتگان و شیاطین، روز = ۳۶۵ — و این را معجزه‌ای عددی "
    "می‌شمارد.<br><br>"
    "<b>روش.</b> همهٔ ادعاهای مشهور را با یک قاعدهٔ ثابت بر متن (رسمِ توکن‌شده؛ ۱۳۵٬۳۶۶ توکن، ۷٬۲۳۶ نوع) شمردیم و سه "
    "آزمون زدیم: (۱) آیا دو عضوِ هر جفت واقعاً با هم برابرند؟ (۲) آیا شمار با تغییرِ املا پایدار می‌ماند؟ (۳) در "
    "برابرِ «شانس» چه‌قدر برابریِ عددی خود‌به‌خود رخ می‌دهد؟<br><br>"
    "<b>یافتهٔ مثبت (به‌انصاف).</b> دو جفتِ مشهور واقعاً برابرند: <b>دنیا = آخرت = ۱۱۴</b> (ادعا ۱۱۵) و "
    "<b>آدم = عیسی = ۲۵</b> — و این دومی را خودِ قرآن قرینه کرده است (آل‌عمران ۳:۵۹). این‌ها را می‌پذیریم؛ ابلیس=۱۱ و "
    "بحر≈۳۲ نیز نزدیک‌اند.<br><br>"
    "<b>یافتهٔ منفی.</b> اما بیشترِ جفت‌ها <b>برابر نیستند</b>: حیات ۷۴ ≠ موت ۵۱، فرشتگان ۷۳ ≠ شیاطین ۱۷، رجال ۱۹ ≠ "
    "نساء ۵۲، روز ۴۲۰ ≠ ۳۶۵. از پنج جفتِ مشهور تنها دو تا درست درمی‌آید.<br><br>"
    "<b>شکنندگیِ املایی.</b> همان شمارها وابسته به املایند: «آخرة» ۱۱۴ است اما «اخرة» یا «الآخرة» صفر؛ «ملائکة» ۷۳ "
    "است اما «ملئکة» صفر. قانونی عددی به املا بی‌اعتناست؛ پس این نشانهٔ «مصنوعِ شمارش» است، نه قانون.<br><br>"
    "<b>چرا برابری پدید می‌آید.</b> قرآن هزاران نوع واژه دارد که بیشترشان کم‌بسامدند. دو واژهٔ تصادفی حدودِ ۲۴٪ مواقع "
    "هم‌شمارند و میانِ واژه‌های پربسامد (≥۱۰) ~۳٪. برای عددهای کوچک، ده‌ها تا صدها واژه در باندِ ±۵٪ هستند (۲۰۴ نوع "
    "نزدیکِ ۱۱، ۱۰۱ نوع نزدیکِ ۲۴). با چند املا برای هر مفهوم و آزادی در انتخابِ «جفتِ متضاد» و گزینشِ اصابت‌ها، "
    "برابری‌ها از دلِ گزینش ساخته می‌شوند — همان «تلهٔ مقایسه‌های چندگانه» که در رمزِ ۱۹ نیز کار می‌کند.<br><br>"
    "<b>تذکّرِ روشی (مهم).</b> رسمِ ما تجزیه‌شده و آمیخته‌املاست و عددهای آن همان شمارشِ کلمه‌ایِ مصحفِ عثمانی نیست "
    "(در مصحف، دنیا و آخرت کلاسیک ۱۱۵‌اند). پس ما <b>پایداری و ساز‌و‌کار</b> را می‌سنجیم، نه «شمارِ حقیقی» را؛ ادعایی "
    "که با قراردادِ شمارش جابه‌جا شود از آغاز قانون نبوده است.<br><br>"
    "<b>نتیجه.</b> خوشه‌ای کوچک و واقعی از برابری‌ها هست (دنیا/آخرت، آدم/عیسی) و آن را به‌انصاف می‌پذیریم؛ اما «نظامی "
    "فراگیر از برابریِ بسامد» در کار نیست. این داوری <b>آماری و روش‌شناختی</b> است، نه کلامی — و خواهرِ بررسیِ رمزِ "
    "۱۹ است: همان ساز‌و‌کار، این بار برای واژه‌ها.<br><br>"
    "<b>درس.</b> هر ادعای عددی دربارهٔ قرآن — از جمله ادعاهای خودِ ما — باید داده‌محور، با قاعدهٔ ثابت، مقاوم در برابرِ "
    "املا، و دارای آزمونِ پوچِ درست باشد؛ نه عوام‌گرایانه و عوام‌پسند.</div>", unsafe_allow_html=True)

# ── ARABIC ABSTRACT ──
C.section("الملخّص الكامل — Arabic abstract")
st.markdown(
    "<div dir='rtl' id='ad-ar' style='font-family:Amiri,\"Scheherazade New\",Tahoma,serif;font-size:15.5px;"
    "line-height:1.9;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;"
    "border-radius:11px;padding:16px 20px'>"
    "<b>الدعوى.</b> «الإعجاز العددي» (الذي روّج له عبد الرزاق نوفل وغيره) يزعم أنّ الكلمات المتقابلة في القرآن ترد "
    "بأعدادٍ متساوية — الدنيا والآخرة، الحياة والموت، الرجال والنساء، الملائكة والشياطين، اليوم = ٣٦٥ — ويعدّ ذلك "
    "معجزةً عددية.<br><br>"
    "<b>المنهج.</b> عددنا كلَّ دعوى مشهورة بقاعدةٍ واحدة ثابتة على النصّ (الرسم المُجزّأ؛ ١٣٥٬٣٦٦ مفردة، ٧٬٢٣٦ نوعاً) "
    "وأجرينا ثلاثة اختبارات: (١) هل عضوا كلّ زوجٍ متساويان فعلاً؟ (٢) هل يثبت العدد عند تغيّر الرسم؟ (٣) كم تقع "
    "المساواةُ العددية بالصدفة؟<br><br>"
    "<b>النتيجة الإيجابية (بإنصاف).</b> زوجان مشهوران متساويان حقاً: <b>الدنيا = الآخرة = ١١٤</b> (الدعوى ١١٥)، "
    "و<b>آدم = عيسى = ٢٥</b> — وهذا الأخير قرينةٌ يعقدها القرآن نفسُه (آل عمران ٣:٥٩). نعترف بهما؛ وإبليس=١١ والبحر≈٣٢ "
    "قريبان أيضاً.<br><br>"
    "<b>النتيجة السلبية.</b> لكنّ أكثر الأزواج <b>غير متساوية</b>: الحياة ٧٤ ≠ الموت ٥١، والملائكة ٧٣ ≠ الشياطين ١٧، "
    "والرجال ١٩ ≠ النساء ٥٢، واليوم ٤٢٠ ≠ ٣٦٥. فمن خمسة أزواجٍ مشهورة لا يصحّ إلّا اثنان.<br><br>"
    "<b>الهشاشة الإملائية.</b> الأعدادُ نفسُها رهينةُ الرسم: «آخرة» ١١٤ لكن «اخرة» أو «الآخرة» صفر؛ «ملائكة» ٧٣ لكن "
    "«ملئكة» صفر. والقانونُ العدديّ لا يبالي بالرسم؛ فهذه علامةُ «مصنوعٍ إحصائيّ» لا قانون.<br><br>"
    "<b>لماذا تظهر المساواة.</b> في القرآن آلافُ الأنواع، أكثرها نادر. ويتشارك لفظان عشوائيان العددَ نفسَه نحو ٢٤٪، "
    "وبين الكلمات المضمونية (تكرار ≥ ١٠) نحو ٣٪. وللأعداد الصغيرة عشراتٌ إلى مئاتٌ من الكلمات ضمن هامش ±٥٪ (٢٠٤ نوعاً "
    "قرب ١١، و١٠١ قرب ٢٤). فمع تعدّد الرسوم لكلّ مفهوم، وحرية اختيار «الضدّ»، وانتقاء الإصابات، تُصنع المساواةُ من "
    "محض الاختيار — وهي «مغالطةُ المقارنات المتعدّدة» نفسُها العاملة في رمز ١٩.<br><br>"
    "<b>تنبيهٌ منهجيّ (مهمّ).</b> رسمُنا مُجزّأٌ ومختلطُ الإملاء، وأعدادُه ليست عدّ الكلمات في المصحف العثماني الذي "
    "تُبنى عليه الدعاوى (وفيه الدنيا والآخرة ١١٥ كلاسيكياً). فنحن نختبر <b>الثبات والآلية</b> لا «العدد الحقيقيّ»؛ "
    "ودعوى ينتقل عددُها بتغيّر العُرف لم تكن قانوناً قطّ.<br><br>"
    "<b>الخلاصة.</b> ثمّة عنقودٌ صغيرٌ حقيقيّ من المساواة (الدنيا/الآخرة، آدم/عيسى) نعترف به بإنصاف؛ لكن لا «نظامَ "
    "تساوٍ شاملاً». وهذا حكمٌ <b>إحصائيّ ومنهجيّ</b> لا لاهوتيّ — وهو شقيقُ مراجعة رمز ١٩: الآليةُ نفسُها، لكن "
    "للكلمات.<br><br>"
    "<b>الدرس.</b> كلُّ دعوى عددية عن القرآن — بما فيها دعاوانا — يجب أن تكون قائمةً على البيانات، بقاعدةٍ ثابتة، "
    "صامدةً أمام الرسم، وذاتَ اختبارٍ عدميٍّ سليم؛ لا تملّقاً للعامّة (عوام‌گرایی / عوام‌پسند).</div>", unsafe_allow_html=True)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
