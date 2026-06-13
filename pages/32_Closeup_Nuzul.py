"""Close-up · Revelation order & the verse-length clock (Bazargan), reviewed — CANDIDATE. Credit-forward."""
import os
import streamlit as st

try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Revelation order", page_icon="🕰️", layout="wide")
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

# ── 1 · PROBLEM ──
C.hero("Revelation order & the verse-length clock (Bazargan), reviewed",
       "Can the Qur'ān's chapters be ordered in time from the text itself — and may we date the pieces inside a sūra?",
       "CANDIDATE", 70, "rasm-WORD", "DIVINE-ALT (revelation order, col 8)")
st.markdown(
    "<div style='display:flex;justify-content:flex-end;gap:9px;margin:7px 0 2px;flex-wrap:wrap'>"
    "<a href='#nz-fa' style='text-decoration:none'><div style='background:linear-gradient(135deg,#138A74,#10243A);"
    "color:#fff;border-radius:9px;padding:7px 13px;font-weight:800;font-size:13px;border:1px solid "
    "rgba(255,255,255,.3)'>📄 Persian abstract · خلاصهٔ فارسی ↓</div></a>"
    "<a href='#nz-ar' style='text-decoration:none'><div style='background:linear-gradient(135deg,#4E6E92,#10243A);"
    "color:#fff;border-radius:9px;padding:7px 13px;font-weight:800;font-size:13px;border:1px solid "
    "rgba(255,255,255,.3)'>📄 Arabic abstract · الملخّص العربي ↓</div></a></div>", unsafe_allow_html=True)
C.story(
    "Bazargan's quantitative insight is <b>real and measurable</b>: mean verse length grows over the revelation "
    "period, and that trend orders the sūras and confirms the traditional sequence. The one over-reach is using it "
    "to date arbitrary <i>passages</i> cut from inside a sūra.",
    "Revelation order is a legitimate (divine‑alternative) arrangement, and Bazargan pioneered data‑driven Qur'ānic "
    "study decades before stylometry — a program later <b>vindicated</b> by Behnam Sadeghi (2011). We credit it, and "
    "scope the single criticism precisely.", accent=C.TEAL)
C.kpis([
    ("r = 0.66", "length ↔ time", "Mean āyah length vs the traditional revelation order (col 8) — a real trend", C.TEAL),
    ("R² 0.44", "variance explained", "By verse length alone; broadly confirms the traditional sequence", C.TEAL),
    ("→ 0.49", "multivariate", "Adding word-length features — a modest, honest gain", C.INK),
    ("8.5 ≈ 11.1", "within ≈ between", "Verse-length spread INSIDE a sūra ≈ the spread ACROSS sūras", C.GOLD),
    ("2–74%", "change-point band", "Sūras with a detectable internal break — wildly method-dependent", C.GOLD),
    ("✓ Sadeghi", "program vindicated", "2011 stylometry confirmed the broader chronology Bazargan pioneered", C.TEAL),
    ("70", "grade", "CANDIDATE — sūra-level signal real; only passage-level dating overreaches", C.GOLD),
])

# ── 2 · HYPOTHESIS ──
C.section("Hypothesis")
C.callout("If verse length is a chronological clock, it makes three predictions — two for it, one against over-reach",
          "<b>(1) Correlation.</b> Mean verse length should track the revelation order. <b>(2) Recovery.</b> "
          "Ordering the sūras by length alone should approximate the traditional sequence. <b>(3) The boundary "
          "test.</b> One may date <i>passages</i> inside a sūra by length only if sūras actually contain "
          "<b>detectable internal style-breaks</b> — otherwise the 'passages' are drawn by the analyst, not the "
          "text. Predictions 1–2 vindicate Bazargan; prediction 3 is where passage-level dating must earn its keep.",
          accent=C.SLATE)

# ── 3 · METHOD & INSTRUMENTS ──
C.section("Method & instruments")
C.callout("The apparatus",
          "<b>Substrate</b> — rasm-WORD (Book6 col 6); āyah length in words. <b>Arrangement</b> — the divine-"
          "alternative: the traditional revelation order (col 8, sūra granularity), the standard reference. "
          "<b>Tests</b> — (a) Pearson/Spearman of mean āyah length vs revelation rank; (b) a multivariate clock "
          "(length + letters-per-word + letter-length); (c) the boundary test: detect an internal verse-length "
          "change-point in each sūra, run across <i>several</i> thresholds and a multiple-comparison-corrected "
          "t-test so the result can't be tuned; (d) within-sūra vs between-sūra length variance. <b>Note</b> — our "
          "normalised rasm differs from Bazargan's own counts; we test his <i>method</i>, not reproduce his figures.",
          accent=C.SLATE)

# ── 4 · RESULTS ──
C.section("Results — the clock works at sūra level")
C.note("The genuine trend, credited. Mean verse length rises with revelation order (r = 0.66, Spearman 0.69), "
       "broadly confirming the traditional sequence — and the extremes are exactly as expected.")
L, R = st.columns(2, gap="medium")
with L:
    C.table(["Shortest mean verse (early end)", "sūra"], [
        ["al-Ikhlāṣ — terse, hymnic", "112"], ["al-Nās", "114"], ["ʿAbasa", "80"], ["al-Ghāshiya", "88"],
    ])
with R:
    C.table(["Longest mean verse (late end)", "sūra"], [
        ["al-Baqara — long, legal", "2"], ["al-Māʾida", "5"], ["al-Mujādila", "58"], ["al-Ṭalāq", "65"],
    ])
C.note("A multivariate clock improves the fit only modestly — verse length already carries almost all the signal "
       "(letters-per-word alone correlates just 0.09). Honest gain, not transformative.")
C.vbars([("verse length", 0.44, C.TEAL, "length alone: R² 0.44"),
         ("+ letters/word", 0.46, C.TEAL, "+ word length"),
         ("+ letter length", 0.49, C.INK, "+ āyah length in letters")], ymax=0.6, fmt="{:.2f}")

# ── 5 · GATING CHAIN ──
C.section("The boundary test — where passage-dating fails")
C.note("Can one date a PASSAGE inside a sūra by its length? Only if sūras have detectable internal breaks. The "
       "fraction that do swings from 2% to 74% depending on the test — so 'is this sūra composite?' has no stable "
       "answer, and passage-level dating cannot be grounded. (We show the whole band, not a cherry-picked figure.)")
C.vbars([("Δ > 1.0σ", 33, C.SLATE, "mean-diff threshold 1.0×σ"), ("Δ > 1.25σ", 18, C.SLATE, "1.25×σ"),
         ("Δ > 1.5σ", 10, C.SLATE, "1.5×σ"), ("Δ > 2.0σ", 2, C.SLATE, "2.0×σ"),
         ("t-test p<.05", 74, C.GOLD, "uncorrected"), ("t-test Bonferroni", 38, C.GOLD, "multiplicity-corrected")],
        ymax=80, fmt="{:.0f}%")
C.para("And the deeper reason: the spread of verse length <b>inside</b> a single sūra (σ ≈ 8.5 words) is almost as "
       "large as the spread of sūra-means <b>across the whole corpus</b> (σ ≈ 11.1). So a passage's length carries "
       "little information about its date — the within‑sūra noise nearly swamps the between‑sūra signal.")

# ── 6 · INTERPRETATION ──
C.section("Interpretation")
C.para("The clock is <b>genuine at the level of the sūra</b> — the divine unit. Bazargan's central claim is correct, "
       "the traditional order is broadly confirmed, and the quantitative program he opened was <b>later vindicated "
       "by Sadeghi's (2011) stylometry</b>, which placed the chronology on a firm statistical footing. That is a "
       "real success and it is his.<br><br>"
       "It fails only at the level of the <b>passage</b> — a unit the analyst draws, not one the text marks. Internal "
       "length-variation is real but is not a datable boundary (it is method-dependent, 2–74%, and within ≈ between), "
       "so cutting a sūra into separately-dated passages over-reaches. This is the divine-division‑vs‑human-construct "
       "line, and the over-reach is shared with <b>Richard Bell and Blachère</b>, who re-ordered the text at "
       "passage/verse level — it is not unique to Bazargan, nor a flaw in his core insight.")

# ── 7 · CAVEATS & CONFOUNDS ──
C.section("Caveats & confounds")
C.para("<b>Credit first, and in context.</b> Bazargan worked in the 1970s–80s, applying quantitative method to "
       "scripture before stylometry existed; he should be read as a pioneer whose central intuition the later, "
       "sharper tools confirmed — not judged anachronistically against them. <b>The critique is narrow and shared.</b> "
       "It targets only passage-level <i>dating precision</i>, a move common to the whole chronological-rearrangement "
       "tradition (Bell, Blachère), not Bazargan's integrity or his sūra-level result. <b>On our instrument.</b> We "
       "count on a normalised rasm and the traditional order (col 8), not his exact figures; and we deliberately "
       "report the full 2–74% change-point band so the criticism cannot be tuned to indict him — the same gate we "
       "turned on one of our own findings.")

# ── 8 · VERDICT ──
C.section("Verdict")
C.verdict("CANDIDATE",
          "Bazargan's core claim holds: verse length tracks revelation time (r = 0.66), the sūra-level chronological "
          "signal is real, and the program he pioneered was vindicated by Sadeghi's stylometry. The single, scoped "
          "criticism — shared with Bell and Blachère — is that passage-level dating inside sūras is not justified by "
          "length (method-dependent 2–74%; within ≈ between). A genuine, partly-validated contribution; credit stands.",
          "sūra-level clock ~80% MEASURED · passage-level dating ~75% unjustified",
          "a stylometric feature that dates passages above chance and survives multiplicity correction",
          "richer features (function-word stylometry à la Sadeghi) at the passage level could revise this upward")

# ── REFLECTION ──
C.section("Reflection")
C.para("This is the mirror-image of the Code 19 case, and the contrast is the lesson. There, a striking pattern had "
       "<i>no</i> data support and earned a refutation. Here, a quantitative claim has <b>real</b> data support and "
       "earns credit — the same impartial gate produces opposite, deserved verdicts. The only fault is a unit error: "
       "applying a sūra-level signal to analyst-drawn passages. Respect the divine division as the atomic unit, and "
       "Bazargan's clock is a genuine, useful instrument; over-reach below it, and it becomes noise.")

# ── SUMMARY ──
C.section("Summary — what holds, what overreaches")
C.table(["✔ Holds — credited", "✗ Overreaches — scoped"], tight=False, rows=[
    ["Verse length tracks revelation time (r = 0.66)", "Dating arbitrary passages inside a sūra"],
    ["Sūra-order broadly confirms the tradition", "Within-sūra spread (8.5) ≈ between (11.1)"],
    ["Pioneering data method, vindicated by Sadeghi", "'Composite' is method-dependent (2–74%)"],
    ["Extremes sane (Meccan short, Medinan long)", "Over-reach shared with Bell / Blachère"],
])

# ── TAKEAWAY ──
C.section("Takeaway")
C.callout("In one line — for every reader",
          "Bazargan was <b>right</b> that verse length is a chronological clock for the Qur'ān's chapters — a real, "
          "pioneering, later-vindicated finding. The only correction: that clock works on the <b>sūra</b> (the "
          "text's own unit), not on passages the analyst slices out of it. Credit the insight; bound the over-reach.",
          accent=C.TEAL)

# ── PERSIAN ABSTRACT ──
C.section("خلاصهٔ کامل — Persian abstract")
st.markdown(
    "<div dir='rtl' id='nz-fa' style='font-family:Vazirmatn,Tahoma,\"Segoe UI\",sans-serif;font-size:15px;"
    "line-height:1.75;color:#243b53;text-align:right;background:#F6F9FC;border-right:5px solid #138A74;"
    "border-radius:11px;padding:15px 20px'>"
    "<b>زمینه.</b> مهدی بازرگان در «سیر تحولِ قرآن» با روشی کمّی نشان داد که <b>میانگینِ طولِ آیه‌ها در طولِ دورهٔ "
    "نزول افزایش می‌یابد</b> و از این «ساعتِ» سبکی برای ترتیبِ زمانیِ سوره‌ها بهره گرفت. این، کارِ پیشگامانه‌ای در "
    "قرآن‌پژوهیِ داده‌محور بود، دهه‌ها پیش از سبک‌سنجیِ نوین.<br><br>"
    "<b>یافتهٔ مثبت (اعتبارِ کار).</b> ادعای اصلیِ او <b>درست</b> است: طولِ آیه با ترتیبِ سنّتیِ نزول هم‌بستگی دارد "
    "(r = ۰٫۶۶؛ اسپیرمن ۰٫۶۹) و ترتیبِ سوره‌ها را تقریباً بازتولید می‌کند؛ سوره‌های کوتاهِ مکّی در یک سو و سوره‌های "
    "بلندِ مدنی در سوی دیگر. افزون بر این، بهنام صادقی (۲۰۱۱) با سبک‌سنجی همان گاه‌شماری را تأیید کرد — یعنی "
    "<b>برنامهٔ بازرگان موفق بود</b>.<br><br>"
    "<b>نقدِ محدود و منصفانه.</b> تنها اشکال، تاریخ‌گذاریِ «بخش‌ها» در درونِ یک سوره است. پراکندگیِ طولِ آیه در "
    "<i>درونِ</i> یک سوره (≈۸٫۵) تقریباً به‌اندازهٔ پراکندگیِ میانگین‌ها <i>میانِ</i> سوره‌هاست (≈۱۱٫۱)، و «آیا این "
    "سوره مرکّب است؟» بسته به آزمون از ۲٪ تا ۷۴٪ نوسان دارد — یعنی بی‌پاسخ. پس بریدنِ سوره به بخش‌ها و تاریخ‌گذاریِ "
    "جداگانهٔ آن‌ها از طریقِ طول، موجّه نیست. این خطا — که با ریچارد بل و بلاشر مشترک است — اشتباهی در «واحد» است: "
    "اعمالِ سیگنالی سوره‌ای بر بخش‌هایی که خودِ پژوهشگر می‌بُرد، نه متن.<br><br>"
    "<b>نتیجه.</b> ساعتِ سبکیِ بازرگان در سطحِ <b>سوره</b> (واحدِ متن) واقعی و سودمند است و به‌انصاف اعتبارش را "
    "می‌پذیریم؛ تنها در سطحِ «بخش» فروتر می‌رود. اعتبارِ کار بر جای می‌ماند و دامنهٔ زیاده‌روی روشن می‌شود.</div>",
    unsafe_allow_html=True)

# ── ARABIC ABSTRACT ──
C.section("الملخّص الكامل — Arabic abstract")
st.markdown(
    "<div dir='rtl' id='nz-ar' style='font-family:Amiri,\"Scheherazade New\",Tahoma,serif;font-size:15.5px;"
    "line-height:1.8;color:#243b53;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;"
    "border-radius:11px;padding:15px 20px'>"
    "<b>السياق.</b> أظهر مهدي بازركان في «سير تطوّر القرآن» بمنهجٍ كمّيّ أنّ <b>متوسّط طول الآيات يتزايد عبر مدّة "
    "النزول</b>، واتّخذ من هذه «الساعة» الأسلوبية ترتيباً زمنياً للسور؛ وهو عملٌ رائدٌ في الدراسة القرآنية القائمة "
    "على البيانات قبل علم الأسلوب الإحصائي بعقود.<br><br>"
    "<b>النتيجة الإيجابية (تقديرُ العمل).</b> دعواه الأساسية <b>صحيحة</b>: طولُ الآية يرتبط بالترتيب التقليديّ للنزول "
    "(r = ٠٫٦٦؛ سبيرمان ٠٫٦٩) ويعيد إنتاج تسلسل السور تقريباً؛ السورُ المكّيّة القصيرة في طرفٍ والمدنيّة الطويلة في "
    "طرف. كما أنّ بهنام صادقي (٢٠١١) أيّد بالأسلوب الإحصائيّ الترتيبَ نفسَه — أي أنّ <b>برنامج بازركان نجح</b>.<br><br>"
    "<b>النقد المحدود والمنصف.</b> العيبُ الوحيد هو تأريخُ «المقاطع» داخل السورة. فتشتّتُ طول الآية <i>داخل</i> السورة "
    "(≈٨٫٥) يقارب تشتّتَ المتوسّطات <i>بين</i> السور (≈١١٫١)، و«هل هذه السورة مركّبة؟» يتراوح حسب الاختبار من ٢٪ إلى "
    "٧٤٪ — أي بلا جواب. فتقطيعُ السورة إلى مقاطع وتأريخُ كلٍّ منها بالطول غيرُ مبرَّر. وهذا الخطأ — المشترَك مع ريتشارد "
    "بِل وبلاشير — خطأٌ في «الوحدة»: تطبيقُ إشارةٍ على مستوى السورة على مقاطعَ يرسمها الباحث لا النصّ.<br><br>"
    "<b>الخلاصة.</b> ساعةُ بازركان الأسلوبية حقيقيةٌ ونافعةٌ على مستوى <b>السورة</b> (وحدة النصّ) ونعترف بها بإنصاف؛ "
    "وإنّما تقصر على مستوى «المقطع». يبقى التقديرُ قائماً ويُحدَّد نطاقُ التجاوز.</div>", unsafe_allow_html=True)

st.page_link("pages/27_Closeup_Index.py", label="← Back to the Close-up map", icon="🔎")
