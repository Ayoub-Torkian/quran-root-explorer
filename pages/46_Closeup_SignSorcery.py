"""Close-up · Sign & Sorcery — āyah/burhān vs siḥr, and the missing word 'muʿjiza'.
A REVIEWED-CLAIM page: it corrects the folk assumption that the Qurʾān says 'muʿjiza' (it never does),
and reads siḥr as the counterfeit/mirror of the divine sign. All counts are rasm-WORD lexical counts on
Book6, tagged MEASURED vs INFERRED; external theology flagged [REPORT]."""
import streamlit as st
try:
    import state as S
except Exception:
    S = None
import closeup as C

st.set_page_config(page_title="Close-up · Sign & Sorcery", page_icon="✨", layout="wide")
if S:
    try: S.log_page("closeup_sign_sorcery")
    except Exception: pass
    for fn in ("inject_css", "render_grouped_nav"):
        try: getattr(S, fn)()
        except Exception: pass
C.inject()

# ── 1 · PROBLEM ──
C.hero("Sign & Sorcery — الآية والسحر",
       "What is siḥr, how does the Qurʾān separate it from a true sign — and does the Qurʾān actually use the "
       "word 'muʿjiza' (miracle) that everyone attaches to it?",
       "REVIEWED", "—", "rasm-WORD (Book6) — lexical counts", "DIVINE-DEFAULT · muṣḥaf order")
st.markdown(
    "<div style='display:flex;justify-content:flex-end;gap:9px;margin:7px 0 2px;flex-wrap:wrap'>"
    "<a href='#ss-fa' style='text-decoration:none'><div style='background:linear-gradient(135deg,#138A74,#10243A);"
    "color:#fff;border-radius:9px;padding:7px 13px;font-weight:800;font-size:13px;border:1px solid rgba(255,255,255,.3)'>"
    "📄 Persian abstract · خلاصهٔ فارسی ↓</div></a>"
    "<a href='#ss-ar' style='text-decoration:none'><div style='background:linear-gradient(135deg,#4E6E92,#10243A);"
    "color:#fff;border-radius:9px;padding:7px 13px;font-weight:800;font-size:13px;border:1px solid rgba(255,255,255,.3)'>"
    "📄 Arabic abstract · الملخّص العربي ↓</div></a></div>", unsafe_allow_html=True)
C.story(
    "The word everyone reaches for — <b>معجزة (muʿjiza, 'miracle')</b> — <b>never occurs in the Qurʾān</b> (0×). Its "
    "root عجز only means <i>to frustrate / escape</i>. The Qurʾān's own words for the authenticating wonder are "
    "<b>آية</b> (sign, 382), <b>بيّنة</b> (clear proof, 523) and <b>برهان</b> (8). So the real Qurʾānic pair is "
    "<b>āyah (sign) ↔ siḥr (sorcery)</b> — and siḥr turns out to be, above all, <b>what deniers *say*</b>: 44 of 59 "
    "sorcery-verses are speech-acts, and the phrase <b>سِحْرٌ مُبِين 'clear sorcery' (9×)</b> is thrown at Moses, "
    "Jesus and Muhammad alike — the exact mirror of <i>bayyina, 'clear proof.'</i>",
    "Naming matters: treating a post-Qurʾānic term (muʿjiza) as if it were Qurʾānic quietly reshapes the concept. "
    "Reading the text's own words shows siḥr is the <b>counterfeit</b> of the sign — built to be confusable — and "
    "that the Qurʾān separates them by source, ontology, outcome, and the verdict of the experts themselves.", accent=C.SLATE)
C.kpis([
    ("0×", "the word muʿjiza", "معجزة / معجزات never occurs; root عجز = 'to frustrate/escape' (مُعْجِزِين 9×). "
     "'muʿjiza' is post-Qurʾānic. [TEXT]", C.CORAL),
    ("382 · 523 · 8", "āyah · bayyina · burhān", "the Qurʾān's actual sign-vocabulary — sign, clear proof, proof. [TEXT]", C.TEAL),
    ("63", "siḥr occurrences", "~60 in the sorcery sense; 34 of them clustered in the Moses–Pharaoh sūras (7·10·20·26). [TEXT]", C.SLATE),
    ("44 / 59", "siḥr = a speech-act", "carry قول 'to say' — siḥr is mostly the denier's LABEL for a sign, not a description. [MEASURED]", C.SLATE),
    ("9×", "'سِحْرٌ مُبِين'", "'clear sorcery' — hurled at Moses (10:76,27:13), Jesus (5:110,61:6), Muhammad (46:7,37:15). Mirror of بيّنة. [MEASURED]", C.CORAL),
])
C.onpage(["① The problem", "② No 'muʿjiza'", "③ siḥr = what deniers say", "④ Four differentiators",
          "⑤ The taḥaddī", "⑥ Forms of the sign", "⑦ Type", "⑧ Caveats", "⑨ Verdict"], fa="ss-fa", ar="ss-ar")

# ── 2 · FOUNDATION ──
C.foundation(
    "A prophet's wonder is asked to prove something. The mature theology calls the proof a <b>muʿjiza</b> — 'that "
    "which renders opponents *incapable* (aʿjaza) of matching it.' That is a sound reading of the <i>challenge</i> "
    "(taḥaddī) verses — but it is a <b>later word</b>. The Qurʾān names the wonder an <b>āyah</b> (a sign that "
    "points beyond itself) and its counterfeit a <b>siḥr</b>. Reading the pair in the text's own terms is the task.")

# ── 3 · NO MUʿJIZA ──
C.section("① The vocabulary — what the Qurʾān actually says")
C.table(["Term", "Root", "Occurrences", "Meaning in the Qurʾān"], tight=False, rows=[
    ["معجزة muʿjiza", "عجز", "0", "does NOT occur — the root means 'to frustrate / escape' (مُعْجِزِين 9×). Post-Qurʾānic term."],
    ["آية āyah", "ءيي", "382", "a SIGN that authenticates and points beyond itself — the Qurʾān's primary word"],
    ["بيّنة / مبين bayyina", "بين", "523", "a CLEAR proof / self-evident"],
    ["برهان burhān", "برهن", "8", "a decisive PROOF"],
    ["سحر siḥr", "سحر", "63", "SORCERY — and, mostly, the denier's label for the sign (§③)"],
])
C.note("So the popular sentence 'the Qurʾān's muʿjiza' uses a word the Qurʾān never uses. The text frames the wonder "
       "as a <b>sign (āyah)</b>, whose authority is that it comes <i>bi-idhni-llāh</i> (by God's leave) and cannot be matched.")

# ── 4 · SIHR = SPEECH-ACT ──
C.section("② siḥr is, above all, what deniers SAY")
C.para("<b>44 of 59</b> sorcery-verses carry the root <b>قول 'to say'</b>: siḥr is overwhelmingly a <b>verdict thrown "
       "at a sign</b>, not a neutral description. The recurring formula <b>سِحْرٌ مُبِين 'clear sorcery' (9×)</b> is "
       "aimed at every messenger — and note the exact irony: the sign is a <b>بيّنة (clear proof)</b>; the denier "
       "calls it <b>سِحْرٌ مُبِين (clear sorcery)</b> — <i>same adjective 'clear / mubīn', opposite verdict.</i> The "
       "mirror-accusation <b>مسحور 'bewitched'</b> targets the prophet's person (17:47 · 25:8 · 17:101). "
       "<b>siḥr is the denier's name for the āyah.</b>")

# ── 5 · DIFFERENTIATORS ──
C.section("③ How to tell the sign from the sorcery — feature by feature")
C.table(["Feature", "Sorcery — siḥr", "Sign — āyah"], tight=False, rows=[
    ["Source", "taught by devils; learning it is kufr (2:102, Hārūt/Mārūt)", "from God — bi-idhni-llāh, 'by His leave'"],
    ["Nature", "illusion / takhyīl — it only *seems* (يُخَيَّلُ … أَنَّهَا تَسْعَىٰ, 20:66)", "reality / ḥaqq — it *is*, not merely seems"],
    ["Acts on", "the eyes & senses — سَحَرُوا أَعْيُنَ النَّاسِ (7:116)", "the truth itself; the created order (staff · sea · earth · wind)"],
    ["Can be learned / matched?", "yes — taught, transmitted, practised", "no — God-given; cannot be reproduced (the taḥaddī, §⑤)"],
    ["Outcome", "fails, nullified — لَا يُفْلِحُ السَّاحِرُ (20:69); سَيُبْطِلُهُ (10:81)", "prevails, endures — تَلْقَفُ مَا يَأْفِكُونَ, swallows it (7:117)"],
    ["Moral status", "kufr; harms, benefits not (2:102)", "guidance & mercy; warns — تَخْوِيفًا (17:59)"],
    ["Effect sought", "to deceive & overawe — اسْتَرْهَبُوهُمْ (7:116)", "to authenticate the messenger & call to God"],
    ["What it is called", "the denier's verdict: سِحْرٌ مُبِين 'clear sorcery' (9×)", "بيّنة 'clear proof' · برهان · آية"],
    ["The experts' verdict", "— (they are the ones exposed)", "the magicians themselves prostrate — فَأُلْقِيَ السَّحَرَةُ سَاجِدِين (26:46 · 7:120 · 20:70)"],
])
C.callout("The decisive tell",
          "The people who would know a trick best — Pharaoh's master magicians — are the <b>first to fall in "
          "prostration</b> when they see Moses' sign. <b>Expertise in the counterfeit is what certifies the genuine.</b> "
          "The Qurʾān does not separate sign from sorcery by the size of the spectacle, but by source, reality, "
          "outcome, and this expert recognition.", accent=C.TEAL)

# ── 6 · TYPE ──
C.section("④ The structural type — a counterfeit / adversarial mirror")
C.para("In the concept typology (axis · field · partition · ladder · frozen pair — see the <b>Shapes of a concept</b> "
       "close-up), siḥr↔āyah is a further shape: a <b>counterfeit pair.</b> The two are <b>built to be confusable</b> "
       "— both extraordinary, both called 'clear' — and the concept's whole work is supplying the <b>hidden "
       "differentiators</b> that separate the real from the mimic. The meaning lives neither in one pole nor in a "
       "clean contrast, but in <b>the criterion that tells look-alikes apart.</b> It is <b>word-level</b> (a lexical–"
       "narrative concept) — the opposite end from the muqaṭṭaʿāt's character-level letters.")

# ── 6b · TAḤADDĪ ──
C.section("⑤ The taḥaddī — the standing challenge, and where 'muʿjiza' comes from")
C.para("The accusation <b>'he forged it'</b> (أَمْ يَقُولُونَ افْتَرَاهُ, 10:38 · 11:13) and <b>'he said it himself'</b> "
       "(تَقَوَّلَهُ, 52:33) is met with one reply: <b>then produce the like.</b> The challenge is stated at four scopes:")
C.table(["Scope demanded", "Verse", "Words"], tight=False, rows=[
    ["the whole Qurʾān — even humans & jinn combined", "17:88", "لَا يَأْتُونَ بِمِثْلِهِ وَلَوْ كَانَ بَعْضُهُمْ لِبَعْضٍ ظَهِيرًا"],
    ["ten forged sūras", "11:13", "فَأْتُوا بِعَشْرِ سُوَرٍ مِّثْلِهِ مُفْتَرَيَاتٍ"],
    ["one sūra like it", "2:23 · 10:38", "فَأْتُوا بِسُورَةٍ مِّن مِّثْلِهِ"],
    ["merely a discourse like it", "52:34", "فَلْيَأْتُوا بِحَدِيثٍ مِّثْلِهِ"],
])
C.callout("The self-staking sign — and the missing word, found",
          "Alone among prophetic signs, the taḥaddī makes a <b>falsifiable, standing prediction</b>: not just 'you have "
          "not' but <b>فَإِن لَّمْ تَفْعَلُوا وَلَن تَفْعَلُوا</b> — 'and you will <b>NEVER</b>' (2:24). Other prophets' "
          "signs were one-time events; the Qurʾān's sign is <b>the text itself</b> — permanently present and openly "
          "challengeable. And this is where the missing word comes from: the challenge asserts the opponents' "
          "<b>عَجْز (inability)</b> — لَا يَأْتُونَ بِمِثْلِهِ — and from that عجز the theologians coined <b>iʿjāz / "
          "muʿjiza</b>. The word is absent; the idea is <i>derived</i> from these verses. The loop closes: they cry "
          "'sorcery / forgery' → the text says 'match it' → they cannot → the standing sign stands.", accent=C.TEAL)
C.note("Sequencing note [REPORT]: the popular 'the challenge de-escalates (whole → ten → one)' is <b>not</b> cleanly "
       "borne out by revelation order here (17:88 whole, then 10:38 one sūra, then 11:13 ten sūras; 2:23–24 latest, "
       "Medinan). What is <b>measured</b>: the four scopes above, the humans+jinn maximum (17:88), and the never-clause (2:24).")

# ── 6c · FORMS OF THE SIGN ──
C.section("⑥ The forms of the sign — every element is His instrument (and why not today)")
C.para("The āyah is not one shape. It comes as an <b>evidentiary sign</b> given to a messenger (Moses' staff; "
       "Ṣāliḥ's she-camel, 'made visible' 17:59; Jesus' healing), as the <b>standing sign</b> of the Book (§⑤), and "
       "— when the sign is denied — as the <b>punishment-sign</b>: a sudden, total event that vindicates it. Across "
       "these, <b>the whole of creation is drawn on as God's instrument</b> — <i>'to God belong the hosts (junūd) of "
       "the heavens and the earth'</i> (48:4·7; 74:31). A different element strikes each nation:")
C.table(["People", "Element", "Mechanism (Qurʾānic)", "Verse"], tight=False, rows=[
    ["Nūḥ's people", "water", "the flood / drowning — الطوفان · أغرقنا", "29:14 · 7:64"],
    ["ʿĀd", "wind", "a howling wind — رِيحٌ صَرْصَرٌ عَاتِيَة", "69:6 · 41:16 · 54:19"],
    ["Thamūd", "sky / earth", "the Cry · bolt · quake — الصَّيْحَة · الصَّاعِقَة · الرَّجْفَة", "11:67 · 41:17 · 7:78"],
    ["Pharaoh & his host", "sea", "drowned in the sea — أَغْرَقْنَاهُم فِي الْيَمّ", "7:136 · 10:90"],
    ["Qārūn", "earth", "the earth swallowed him — فَخَسَفْنَا بِهِ وَبِدَارِهِ الْأَرْض", "28:81"],
    ["Lūṭ's people", "sky + earth", "stones + overturning — حِجَارَةٍ مِّن سِجِّيل · عَالِيَهَا سَافِلَهَا", "11:82 · 15:74"],
    ["Madyan (Shuʿayb)", "sky / earth", "the Cry · the quake — الصَّيْحَة · الرَّجْفَة", "11:94 · 7:91"],
])
C.note("<b>Historical tag.</b> The events are narrated in the text — <b>[TEXT]</b>; identifying each people with a "
       "specific archaeological site or date is external — <b>[REPORT]</b> — and is not asserted here. The shared "
       "signature is measured: each strike is <b>sudden / unawares</b> (وَهُمْ لَا يَشْعُرُونَ — e.g. 16:45, the earth "
       "swallowing), <b>total</b> (a whole qawm), and <b>timed</b> — 'every nation has a term' (لِكُلِّ أُمَّةٍ أَجَلٌ, 7:34).")
C.callout("The tools of the Maker — and why there is no punishment-sign today",
          "The point is not the variety of disasters but the <b>single Author behind every element</b>: earth "
          "swallows, sea drowns, wind blasts, sky cries, stones fall — each is a <i>jund</i> (soldier) of God (48:4). "
          "And the Qurʾān answers 'why not now?' directly — <b>وَمَا مَنَعَنَا أَن نُّرْسِلَ بِالْآيَاتِ إِلَّا أَن "
          "كَذَّبَ بِهَا الْأَوَّلُونَ</b> (17:59): the demanded punishment-signs were <b>withheld</b> from the final "
          "community, because the ancient pattern was sign → denial → annihilation. For this umma the sign "
          "<b>changed form, not substance</b>: the <b>standing sign</b> (the Book, §⑤) + <b>deferred judgment</b> (the "
          "reckoning is the Hour, not an immediate wipe-out) — <i>'We send not the signs except to warn'</i> "
          "(تَخْوِيفًا, 17:59). The <b>pattern is unchanged</b> — فَلَن تَجِدَ لِسُنَّةِ اللَّهِ تَبْدِيلًا (35:43); only "
          "its <b>mode</b> for the last people differs. So we <i>do</i> still have the sign — as the Book and the "
          "deferred term — just not as the sudden collective ʿadhāb of old.", accent=C.TEAL)

# ── 7 · CAVEATS ──
C.section("Caveats")
C.para("<b>'muʿjiza' is a legitimate idea, just a later word.</b> This close-up corrects the *lexical* claim (the "
       "Qurʾān doesn't use it), not the theology of inimitability, which grows soundly from the challenge (taḥaddī) "
       "verses. <b>Sense-resolution:</b> the homograph سَحَر 'pre-dawn' (أسحار, 3:17 · 51:18) is set aside. "
       "<b>Co-occurrence is not causation:</b> the 'counterfeit-mirror' reading is an interpretation of the four "
       "differentiators, tagged as such. The Bābil / Hārūt–Mārūt backstory beyond the verse's own words is [REPORT].")

# ── 8 · VERDICT ──
C.section("Verdict")
C.verdict("REVIEWED",
          "The Qurʾān has no word 'muʿjiza' (0×); it frames the authenticating wonder as an āyah (sign) and its "
          "counterfeit as siḥr. siḥr is overwhelmingly the denier's label (44/59 speech-acts; سِحْرٌ مُبِين 9×), and "
          "the text separates true from false by source, ontology, outcome, and the experts' own prostration — not "
          "by spectacle. The lexical facts are MEASURED; the counterfeit-mirror reading is INFERRED.",
          "~99% on the lexical facts (counting); ~80% on the counterfeit-mirror structural reading.",
          "a Qurʾānic occurrence of معجزة (there is none), or a sign the text validates by spectacle alone",
          "extend to the taḥaddī (challenge) verses — the seed the term 'muʿjiza' grew from")

# ── 9 · REFLECTION / SUMMARY / LESSONS ──
C.section("Reflection")
C.para("The instinct was to compare 'miracle vs magic' — but the data moved the question: the Qurʾān doesn't argue "
       "'miracle beats magic', it distinguishes <b>a sign you read rightly</b> from <b>a sign you dismiss as sorcery.</b> "
       "The same event divides belief from denial; the drama is epistemic, not pyrotechnic.")
C.section("Summary")
C.para("<b>Measured:</b> muʿjiza 0×; āyah/bayyina/burhān 382/523/8; siḥr 63, 44/59 as speech-acts, سِحْرٌ مُبِين 9×; the "
       "four differentiator verses; magicians prostrate (26:46·7:120·20:70). <b>Inferred:</b> siḥr as the counterfeit "
       "mirror of the sign. <b>Report (flagged):</b> muʿjiza as the mature theological packaging.")
C.section("Lessons")
C.para("① Check whether the key term is even Qurʾānic before building on it. ② A concept can be defined by its "
       "<b>counterfeit</b>, not only its opposite. ③ Tag MEASURED vs INFERRED vs REPORT at every step.")

# ── Persian abstract ──
C.section("خلاصهٔ کامل — Persian abstract")
st.markdown('''<div dir="rtl" id="ss-fa" style="font-family:Vazirmatn,Tahoma,'Segoe UI',sans-serif;font-size:15px;line-height:1.95;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #138A74;border-radius:11px;padding:18px 22px">
<b>نشانه و سحر.</b> واژهٔ <b>معجزه</b> در قرآن <b>هرگز نیامده</b> است (۰ بار)؛ ریشهٔ «عجز» تنها به معنای «ناتوان‌کردن/گریختن» است (مُعجِزین ۹ بار). واژگانِ خودِ قرآن برای نشانهٔ تأییدکننده: <b>آیة</b> (۳۸۲)، <b>بیّنة</b> (۵۲۳)، <b>برهان</b> (۸). پس جفتِ حقیقیِ قرآنی <b>آیه ↔ سحر</b> است. <b>سحر (۶۳ بار، ۳۴ بار در داستان موسی‌–فرعون)</b> بیش از همه «چیزی است که منکران می‌گویند» — ۴۴ از ۵۹ آیه فعلِ «قول» دارند، و عبارتِ <b>«سِحْرٌ مُبِین»</b> (۹ بار) به موسی، عیسی و محمد نسبت داده می‌شود؛ آیینهٔ وارونهٔ «بیّنه». <b>تمایزها:</b> منشأ (تعلیمِ شیاطین، ۲:۱۰۲ ← به اذن خدا)، هستی (خیالِ چشم‌ها ۷:۱۱۶ و ۲۰:۶۶ ← حقیقی)، سرانجام («لا یفلح الساحر» ۲۰:۶۹؛ «سیبطله» ۱۰:۸۱ ← عصا فرو می‌بلعد ۷:۱۱۷)، و شناختِ متخصصان (خودِ ساحران سجده می‌کنند، ۲۶:۴۶). <b>گونهٔ ساختاری:</b> «بدلِ همانند» — دو چیزِ عمداً اشتباه‌شدنی که مفهوم، نشانگرهای پنهانِ تشخیص را فراهم می‌آورد. سطح: واژه‌ای. اطمینان: ۹۹٪ برای واژگان، ۸۰٪ برای خوانشِ «بدل/آینه».
</div>''', unsafe_allow_html=True)

# ── Arabic abstract ──
C.section("الملخّص الكامل — Arabic abstract")
st.markdown('''<div dir="rtl" id="ss-ar" style="font-family:Amiri,'Scheherazade New',Tahoma,serif;font-size:15.5px;line-height:2.0;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;border-radius:11px;padding:18px 22px">
<b>الآية والسحر.</b> لفظ <b>«معجزة» لا يرد في القرآن قطّ</b> (٠ مرّة)؛ وجذر «عجز» إنّما يعني الإفلاتَ والإعجازَ عن الإدراك (مُعجِزِين ٩ مرّات). وألفاظ القرآن للآيةِ المصدِّقة هي <b>آية</b> (٣٨٢)، و<b>بيّنة</b> (٥٢٣)، و<b>برهان</b> (٨). فالثنائيّ القرآنيّ الحقّ هو <b>الآية ↔ السحر</b>. و<b>السحر (٦٣ مرّة، ٣٤ منها في قصّة موسى وفرعون)</b> هو قبل كلّ شيء <b>ما يقوله المكذِّبون</b>: ٤٤ من ٥٩ آيةً فيها فعل «قال»، وصيغة <b>«سِحْرٌ مُبِين»</b> (٩ مرّات) تُرمى على موسى وعيسى ومحمّد — وهي المرآةُ المقابِلة لـ«بيّنة». <b>الفوارق:</b> المصدر (تعليمُ الشياطين ٢:١٠٢ ← بإذن الله)، والحقيقة (تخييلُ الأعين ٧:١١٦ و٢٠:٦٦ ← حقّ)، والمآل («لا يُفلِح الساحر» ٢٠:٦٩؛ «سيُبطِله» ١٠:٨١ ← والعصا «تَلْقَفُ ما يأفِكون» ٧:١١٧)، واعترافُ الخبراء (السحرةُ أنفسُهم يخرّون سُجّدًا ٢٦:٤٦). <b>النوع البنيويّ:</b> «نظيرٌ مزيَّف» — شيئان يُقصَد التباسُهما، والمفهومُ يُقدّم علاماتِ التمييز الخفيّة. المستوى: كلميّ. الثقة: ٩٩٪ للألفاظ، ٨٠٪ لقراءة «النظير المزيَّف».
</div>''', unsafe_allow_html=True)
