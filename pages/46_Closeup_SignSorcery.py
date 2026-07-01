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
          "⑤ The taḥaddī", "⑥ Forms of the sign", "⑦ Signs today", "⑧ Type", "⑨ Caveats", "⑩ Verdict", "⑪ Takeaway"], fa="ss-fa", ar="ss-ar")

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
    ["Source", "taught by devils; kufr — يُعَلِّمُونَ النَّاسَ السِّحْرَ (2:102)", "only by God's leave — وَمَا كَانَ لِرَسُولٍ أَن يَأْتِيَ بِآيَةٍ إِلَّا بِإِذْنِ اللَّهِ (13:38)"],
    ["Nature", "illusion / takhyīl — يُخَيَّلُ إِلَيْهِ … أَنَّهَا تَسْعَىٰ (20:66)", "truth — فَوَقَعَ الْحَقُّ وَبَطَلَ مَا كَانُوا يَعْمَلُونَ (7:118); وَيُحِقُّ اللَّهُ الْحَقَّ (10:82)"],
    ["Acts on", "the eyes & senses — سَحَرُوا أَعْيُنَ النَّاسِ (7:116)", "the created order — the staff (7:117), the sea (7:136), the earth (28:81)"],
    ["Learnable / matchable?", "yes — taught & transmitted (2:102)", "no — cannot be reproduced: فَأْتُوا بِسُورَةٍ مِّن مِّثْلِهِ (2:23; the taḥaddī, §⑤)"],
    ["Outcome", "fails, nullified — لَا يُفْلِحُ السَّاحِرُ (20:69); سَيُبْطِلُهُ (10:81)", "prevails — تَلْقَفُ مَا يَأْفِكُونَ, swallows it (7:117)"],
    ["Moral status", "kufr; harms, benefits not — يَضُرُّهُمْ وَلَا يَنفَعُهُمْ (2:102)", "guidance & mercy — هُدًى وَرَحْمَةٌ (27:77); warns — تَخْوِيفًا (17:59)"],
    ["Effect sought", "to deceive & overawe — اسْتَرْهَبُوهُمْ (7:116)", "to authenticate the messenger — قَدْ جِئْتُكُم بِبَيِّنَةٍ مِّن رَّبِّكُمْ (7:105)"],
    ["What it is called", "the denier's verdict — سِحْرٌ مُبِين 'clear sorcery' (9×) [MEASURED]", "بَيِّنَة 'clear proof' (7:105) · بُرْهَان · آيَة"],
    ["The experts' verdict", "— (they are the ones exposed)", "the magicians themselves prostrate — فَأُلْقِيَ السَّحَرَةُ سَاجِدِين (26:46 · 7:120 · 20:70)"],
])
C.note("<b>Every cell is verse-anchored [TEXT]</b>; 'سِحْرٌ مُبِين ×9' is [MEASURED] (counted across the corpus). "
       "The <i>reading</i> that these features together make siḥr the <b>counterfeit</b> of the āyah is [INFERRED] — "
       "the citations are the data; the framing is the interpretation.")
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
C.section("⑥ The forms of the sign — every element & creature is His instrument (and why not today)")
C.para("The āyah takes several forms: an <b>evidentiary / power sign</b> handed to a messenger to authenticate him; "
       "a <b>sign of God's power & the Resurrection</b> shown as a wonder; the <b>standing sign</b> of the Book (§⑤); "
       "and — when the sign is denied — a <b>protective</b> or <b>punitive</b> event. Across all of them <b>the whole "
       "of creation, element and creature alike, is God's instrument</b> — <i>'to God belong the hosts (junūd) of the "
       "heavens and the earth'</i> (48:4·7; 74:31). Place-names shown with a verse are Qurʾānic ([TEXT]); those marked "
       "<i>·ext</i> are traditional identifications ([REPORT]); the ≈date column is external throughout ([REPORT]).")
C.para("<b>A · Evidentiary / power signs</b> — the created order bent to authenticate a prophet (direct signs):")
C.table(["Prophet", "The sign (Qurʾānic)", "Sūrah · verse", "≈ era", "Where"], tight=False, rows=[
    ["Mūsā", "staff → serpent, radiant hand — 'nine signs' (تِسْعَ آيَاتٍ)", "al-Isrāʾ 17:101 · al-Naml 27:12", "≈ 13th c. BCE?", "Egypt (43:51)"],
    ["Ṣāliḥ", "the she-camel, itself named a sign — نَاقَةُ اللَّهِ … آيَةً", "al-Aʿrāf 7:73 · al-Qamar 54:27", "≈ 1st mill. BCE", "al-Ḥijr (15:80)"],
    ["Ibrāhīm", "the fire made cool — يَا نَارُ كُونِي بَرْدًا وَسَلَامًا", "al-Anbiyāʾ 21:69", "≈ 2nd mill. BCE", "Babylon ·ext"],
    ["ʿĪsā", "clay bird given life, healing the blind & leper, raising the dead — بِإِذْنِ اللَّهِ", "Āl ʿImrān 3:49 · al-Māʾidah 5:110", "≈ 1st c. CE", "Palestine ·ext"],
    ["Sulaymān", "wind (a month each way); speech of birds; Bilqīs's throne in an instant — قَبْلَ أَن يَرْتَدَّ إِلَيْكَ طَرْفُكَ", "al-Naml 27:16·40 · Sabaʾ 34:12", "≈ 10th c. BCE", "Jerusalem ·ext ← Sabaʾ (27:22)"],
])
C.para("<b>Mūsā's nine signs (تِسْعُ آيَاتٍ)</b> — the count is stated (al-Isrāʾ 17:101 · al-Naml 27:12); the list below gathers the scattered mentions (mostly al-Aʿrāf 7:107–133). All in Egypt, ≈ 13th c. BCE?")
C.table(["#", "Sign", "Qurʾānic term", "Sūrah · verse"], tight=True, rows=[
    ["1", "staff → serpent", "الْعَصَا → ثُعْبَانٌ مُّبِين", "al-Aʿrāf 7:107 · al-Shuʿarāʾ 26:32"],
    ["2", "the radiant white hand", "الْيَدُ الْبَيْضَاء", "al-Aʿrāf 7:108 · Ṭā-Hā 20:22"],
    ["3", "years of drought", "السِّنِين", "al-Aʿrāf 7:130"],
    ["4", "shortage of crops", "نَقْصٌ مِّنَ الثَّمَرَات", "al-Aʿrāf 7:130"],
    ["5", "the flood", "الطُّوفَان", "al-Aʿrāf 7:133"],
    ["6", "the locusts", "الْجَرَاد", "al-Aʿrāf 7:133"],
    ["7", "the lice", "الْقُمَّل", "al-Aʿrāf 7:133"],
    ["8", "the frogs", "الضَّفَادِع", "al-Aʿrāf 7:133"],
    ["9", "the blood", "الدَّم", "al-Aʿrāf 7:133"],
])
C.note("The five of 7:133 (flood · locusts · lice · frogs · blood) are named آيَاتٍ مُّفَصَّلَات ('signs made distinct'). "
       "The Qurʾān <b>states 'nine' [TEXT]</b> but does not number them in one list; this enumeration is the traditional "
       "harmonisation <b>[INFERRED / REPORT]</b> — some scholars count differently (e.g. including the sea's parting).")

C.para("<b>B · Signs of God's power & the Resurrection</b> — wonders shown as āyāt, not tied to a contest (indirect):")
C.table(["Sign", "What (Qurʾānic)", "Sūrah · verse", "≈ date", "Where"], tight=False, rows=[
    ["Aṣḥāb al-Kahf (the Cave)", "the sleepers preserved ~309 yrs, called a sign — كَانُوا مِنْ آيَاتِنَا عَجَبًا", "al-Kahf 18:9 (·25)", "≈ 3rd c. CE? ·ext", "a cave ·ext"],
    ["The man & the ruined town", "made to die 100 years, then revived — فَأَمَاتَهُ اللَّهُ مِئَةَ عَامٍ ثُمَّ بَعَثَهُ", "al-Baqarah 2:259", "≈ 6th c. BCE? ·ext", "a town ·ext"],
    ["Ibrāhīm's four birds", "revived to answer 'how do You give life?' — كَيْفَ تُحْيِي الْمَوْتَىٰ", "al-Baqarah 2:260", "≈ early 2nd mill. BCE", "—"],
])
C.para("<b>C · Protective & punitive signs</b> — a different element (or creature) strikes when the sign is denied; and once, birds defend the Sanctuary:")
C.table(["People / event", "Element", "Mechanism (Qurʾānic)", "Sūrah · verse", "≈ date", "Where"], tight=False, rows=[
    ["Aṣḥāb al-Fīl (Elephant)", "birds + stones", "طَيْرًا أَبَابِيلَ · بِحِجَارَةٍ مِّن سِجِّيل", "al-Fīl 105:3–4", "≈ 570 CE", "Mecca ·ext"],
    ["Nūḥ's people", "water", "flood / drowning — الطوفان · أغرقنا", "al-ʿAnkabūt 29:14 · al-Aʿrāf 7:64", "prehistoric", "ark on al-Jūdī (11:44)"],
    ["ʿĀd", "wind", "howling wind — رِيحٌ صَرْصَرٌ عَاتِيَة", "al-Ḥāqqah 69:6 · al-Qamar 54:19", "ancient", "al-Aḥqāf (46:21)"],
    ["Thamūd", "sky / earth", "the Cry · bolt · quake — الصَّيْحَة · الصَّاعِقَة · الرَّجْفَة", "Hūd 11:67 · al-Aʿrāf 7:78", "≈ 1st mill. BCE", "al-Ḥijr (15:80)"],
    ["Pharaoh & host", "sea", "drowned — أَغْرَقْنَاهُم فِي الْيَمّ", "al-Aʿrāf 7:136 · Yūnus 10:90", "≈ 13th c. BCE?", "Egypt (43:51)"],
    ["Qārūn", "earth", "swallowed — فَخَسَفْنَا بِهِ وَبِدَارِهِ الْأَرْض", "al-Qaṣaṣ 28:81", "≈ 13th c. BCE?", "Egypt ·ext"],
    ["Lūṭ's people", "sky + earth", "stones + overturning — سِجِّيل · عَالِيَهَا سَافِلَهَا", "Hūd 11:82 · al-Ḥijr 15:74", "≈ early 2nd mill. BCE", "al-Muʾtafikāt (53:53)"],
    ["Madyan (Shuʿayb)", "sky / earth", "the Cry · the quake — الصَّيْحَة · الرَّجْفَة", "Hūd 11:94 · al-Aʿrāf 7:91", "2nd mill. BCE", "Madyan (7:85)"],
])
C.note("<b>Dates are external ([REPORT]) — the Qurʾān gives none;</b> '≈' is traditional/scholarly estimate, often "
       "legendary and debated (esp. Nūḥ, ʿĀd). <b>Locations differ:</b> those shown with a verse are named <b>in the "
       "text ([TEXT])</b> — al-Aḥqāf (46:21), al-Ḥijr (15:80), al-Jūdī where the ark rested (11:44), al-Muʾtafikāt "
       "(53:53), Madyan, Egypt (43:51); those marked <i>·ext</i> (Mecca, the cave's site, Sodom, Babylon) are "
       "traditional identifications ([REPORT]). What the text asserts ([TEXT]) is the event, its instrument and any "
       "named place; the shared signature of the punitive class is measured: sudden / unawares (وَهُمْ لَا "
       "يَشْعُرُونَ, 16:45), total (a whole qawm), and timed (لِكُلِّ أُمَّةٍ أَجَلٌ, 7:34).")
C.callout("The tools of the Maker — and why there is no punishment-sign today",
          "The point is the <b>single Author behind every instrument</b>: sea drowns, wind blasts, earth swallows, "
          "sky cries, stones fall, fire is made cool, sleepers are kept, the dead are raised, and <b>birds</b> defend "
          "— element and creature alike are <i>junūd</i> (hosts) of God (48:4). And the Qurʾān answers 'why not now?' "
          "— <b>وَمَا مَنَعَنَا أَن نُّرْسِلَ بِالْآيَاتِ إِلَّا أَن كَذَّبَ بِهَا الْأَوَّلُونَ</b> (17:59): the demanded "
          "punishment-signs were <b>withheld</b> from the final community, because the ancient pattern was sign → "
          "denial → annihilation. For this umma the sign <b>changed form, not substance</b>: the <b>standing sign</b> "
          "(the Book, §⑤) + <b>deferred judgment</b> (the reckoning is the Hour, not an immediate wipe-out) — "
          "<i>'We send not the signs except to warn'</i> (تَخْوِيفًا, 17:59). The <b>pattern is unchanged</b> — "
          "فَلَن تَجِدَ لِسُنَّةِ اللَّهِ تَبْدِيلًا (35:43); only its <b>mode</b> for the last people differs.", accent=C.TEAL)

# ── 6d · SIGNS TODAY ──
C.section("⑦ Do we still have signs — and why we may not notice them?")
C.para("Yes — but not as the sudden ʿadhāb of old (§⑥). The Qurʾān points to <b>ongoing, public signs</b> in three "
       "registers: the <b>standing sign</b> of the Book (the taḥaddī, §⑤); signs <b>in the horizons (āfāq)</b> — the "
       "cosmos and the alternation of night and day (<b>41:53</b>; 3:190; 51:20); and signs <b>in the selves "
       "(anfus)</b> — the human being itself (<b>41:53</b>; 51:21). Even a past judgment is left as a <b>lasting "
       "sign</b>: Pharaoh's body preserved <i>'as a sign for those after you'</i> (10:92).")
C.callout("Why they go unnoticed — the deficit is attention, not signs",
          "The Qurʾān locates the gap in the <b>beholder</b>, not the sign: people <b>pass them by, turning away</b> — "
          "وَكَأَيِّن مِّنْ آيَةٍ … يَمُرُّونَ عَلَيْهَا وَهُمْ عَنْهَا مُعْرِضُونَ (12:105); they <b>do not look</b> — "
          "أَفَلَا تُبْصِرُونَ (51:21); <b>hearts are locked</b> against reflection — أَفَلَا يَتَدَبَّرُونَ الْقُرْآنَ "
          "أَمْ عَلَىٰ قُلُوبٍ أَقْفَالُهَا (47:24); and the <b>arrogant</b> are turned from them — سَأَصْرِفُ عَنْ "
          "آيَاتِيَ الَّذِينَ يَتَكَبَّرُونَ (7:146). The signs are read only by <b>أُولُو الْأَلْبَاب</b> ('people of "
          "understanding', 3:190) and <b>الْمُوقِنِين</b> ('those of certainty', 51:20). So the sign is <b>ever-present "
          "and open; perceiving it needs تَدَبُّر · تَفَكُّر · يَقِين</b> — and its absence (heedlessness, turning "
          "away, arrogance, a closed heart) is why it goes unseen. <i>[verses TEXT; that this answers 'why we don't "
          "notice today' is INFERRED.]</i>", accent=C.TEAL)

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
C.section("Extended takeaway — the whole picture")
C.para("<b>The Qurʾān never says 'muʿjiza'; it says āyah</b> — a <i>sign</i> that points beyond itself. Around that "
       "one word the whole discussion organises: a mirror-concept, a family of forms, and a standing challenge.")
C.para("<b>1 · The mirror — siḥr.</b> Sorcery is the <b>counterfeit</b> of the sign: 'clear sorcery' (سِحْرٌ مُبِين) "
       "set against 'clear proof' (بيّنة), the same event read two opposite ways. It is told apart <b>not by the size "
       "of the spectacle</b> but by <b>source</b> (devil-taught vs by-God's-leave), <b>reality</b> (illusion vs ḥaqq), "
       "<b>outcome</b> (nullified vs prevailing), and — decisively — the <b>experts' own prostration</b> (26:46).")
C.para("<b>2 · The forms — every element & creature.</b> The sign comes as an <b>evidentiary</b> proof (Mūsā's nine, "
       "Ṣāliḥ's she-camel, Ibrāhīm's cooled fire, ʿĪsā's healing, Sulaymān's wind, birds and instant throne), as a "
       "<b>wonder of power & resurrection</b> (the Cave-sleepers 'from Our signs', the man revived after a century, "
       "Ibrāhīm's four birds), and — when denied — as a <b>punitive or protective event</b> in which sea, wind, earth, "
       "sky, stones and <b>birds</b> each act. The lesson is the <b>single Author behind every tool</b>: whether a "
       "staff, a flood, a cave, or a verse, creation is God's <i>junūd</i> (48:4).")
C.para("<b>3 · The standing sign & 'why not today'.</b> The <b>taḥaddī</b> — 'bring the like', never met, guaranteed "
       "never to be (2:24) — turns the Book <b>itself</b> into a permanent, open, falsifiable sign; and the ʿajz "
       "(inability) it asserts is where later theology coined 'muʿjiza'. And the Qurʾān answers <b>why no annihilating "
       "sign today (17:59)</b>: the form <b>changed</b> — from immediate collective destruction to the <b>standing "
       "Book</b> + <b>deferred judgment</b> — while the <b>pattern (sunnat Allāh) did not</b> (35:43).")
C.callout("In one line",
          "A true sign is <b>God authenticating His word through His creation</b>; the counterfeit (siḥr) mimics the "
          "wonder but fails the four tests; the standing sign is the Book, and the reckoning is now deferred rather "
          "than immediate. Everything above is kept honest — the <b>lexical facts measured</b>, the <b>readings "
          "inferred</b>, the <b>dates and site-identifications external</b>.", accent=C.TEAL)

C.section("خلاصهٔ کامل — Persian abstract")
st.markdown('''<div dir="rtl" id="ss-fa" style="font-family:Vazirmatn,Tahoma,'Segoe UI',sans-serif;font-size:14.5px;line-height:2.0;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #138A74;border-radius:11px;padding:16px 22px"><p style='margin:9px 0 0'><b>۱) مسئله و واژگان.</b> پرسشِ رایجِ «معجزهٔ قرآن» بر واژه‌ای استوار است که <b>در قرآن هرگز نیامده</b>: «معجزة/معجزات» صفر بار؛ و ریشهٔ «عجز» تنها «ناتوان‌ساختن/گریختن» است (مُعجِزین ۹ بار). واژگانِ خودِ قرآن برای آن نشانهٔ تأییدکننده اینهاست: <b>آیة</b> (۳۸۲)، <b>بیّنة/مبین</b> (۵۲۳)، <b>برهان</b> (۸). «معجزه» ساختهٔ متکلمانِ پس از نزول است — درست، اما نه قرآنی. پس جفتِ حقیقیِ قرآنی نه «معجزه–سحر»، بلکه <b>آیه ↔ سحر</b> است.</p><p style='margin:9px 0 0'><b>۲) سحر در قرآن.</b> ریشهٔ «سحر» ۶۳ بار آمده (نزدیک ۶۰ بار به معنایِ جادو)، و ۳۴ مورد در رویاروییِ موسی و فرعون خوشه بسته (سوره‌هایِ ۷، ۱۰، ۲۰، ۲۶). نکتهٔ سنجیده: سحر بیش از همه <b>گفتهٔ منکران</b> است — ۴۴ از ۵۹ آیه فعلِ «قول» دارند؛ برچسبی که بر نشانه می‌زنند، نه توصیفی بی‌طرف. عبارتِ <b>«سِحرٌ مُبین»</b> (۹ بار) بر موسی (۱۰:۷۶، ۲۷:۱۳)، عیسی (۵:۱۱۰، ۶۱:۶) و محمد (۴۶:۷، ۳۷:۱۵) یکسان فرود می‌آید — آیینهٔ وارونهٔ «بیّنه». اتهامِ همتا، «مسحور» (جادوزده)، متوجهِ شخصِ پیامبر است (۱۷:۴۷، ۲۵:۸، ۱۷:۱۰۱).</p><p style='margin:9px 0 0'><b>۳) تمایزِ نشانه از سحر — نه با شکوهِ ظاهری، بلکه با ویژگی‌ها.</b> <b>خاستگاه:</b> سحر تعلیمِ شیاطین و کفر است (۲:۱۰۲) ← نشانه تنها به اذنِ خدا: «وما کان لرسولٍ أن یأتیَ بآیةٍ إلا بإذن الله» (۱۳:۳۸). <b>سرشت:</b> سحر خیال است، «یُخیَّلُ إلیه … أنها تسعی» (۲۰:۶۶) ← نشانه حق است، «فوقع الحق وبطل ما کانوا یعملون» (۷:۱۱۸). <b>محلِّ اثر:</b> سحر بر چشم‌هاست، «سحروا أعین الناس» (۷:۱۱۶) ← نشانه بر خودِ آفرینش (عصا، دریا، زمین). <b>آموختنی/همانندپذیر؟</b> سحر آموختنی است (۲:۱۰۲) ← نشانه همانندناپذیر، «فأتوا بسورةٍ من مثله» (۲:۲۳). <b>سرانجام:</b> سحر باطل می‌شود، «لا یفلح الساحر» (۲۰:۶۹) ← نشانه پیروز می‌شود و باطل را می‌بلعد (۷:۱۱۷). <b>جایگاهِ اخلاقی:</b> سحر کفر و زیان است (۲:۱۰۲) ← نشانه هدایت و رحمت، «هدًی ورحمة» (۲۷:۷۷)، و بیم‌دهنده (۱۷:۵۹). <b>گواهیِ متخصصان</b> — قاطع‌ترین نشانه: خودِ ساحرانِ فرعون چون نشانهٔ موسی را دیدند به سجده افتادند، «فأُلقی السحرة ساجدین» (۲۶:۴۶، ۷:۱۲۰، ۲۰:۷۰). تخصص در بدل، اصل را تصدیق می‌کند.</p><p style='margin:9px 0 0'><b>۴) اشکالِ نشانه و ابزارهایِ آفریدگار.</b> نشانه یک شکل ندارد: (الف) <b>نشانهٔ تأییدی/قدرت</b> برای تصدیقِ پیامبر — نُه نشانهٔ موسی (۱۷:۱۰۱)، ناقهٔ صالح که خود «آیة» خوانده شده (۷:۷۳)، سردشدنِ آتش بر ابراهیم (۲۱:۶۹)، آفرینشِ پرنده از گِل و زنده‌کردنِ مردگان به‌دستِ عیسی (۳:۴۹)، و سلیمان: رام‌شدنِ باد (۳۴:۱۲)، منطقِ پرندگان (۲۷:۱۶)، و آوردنِ تختِ بلقیس «در یک چشم‌برهم‌زدن» (۲۷:۴۰). (ب) <b>نشانهٔ قدرت و رستاخیز</b> — اصحابِ کهف که خود «مِن آیاتِنا» خوانده شده‌اند (۱۸:۹)، زنده‌شدنِ آن مرد پس از صد سال (۲:۲۵۹)، و پرندگانِ ابراهیم (۲:۲۶۰). (ج) <b>نشانهٔ ایستا</b> (کتاب). (د) — چون انکار شود — <b>نشانهٔ عذاب یا حمایت</b>؛ و در همهٔ اینها <b>همهٔ آفرینش — عنصر و جاندار — ابزارِ خداست</b>، «ولله جنودُ السماوات والأرض» (۴۸:۴، ۷۴:۳۱): آب (نوح و فرعون)، باد (عاد، ۶۹:۶)، صیحه/صاعقه (ثمود، ۱۱:۶۷)، زمین (قارون، ۲۸:۸۱)، سنگ (لوط، ۱۱:۸۲)، و پرندگانِ ابابیل در دفاعِ حرم (فیل، ۱۰۵:۳). نشانهٔ مشترک: ناگهانی («لا یشعرون»، ۱۶:۴۵)، فراگیر، و زمان‌دار («لکل أمةٍ أجل»، ۷:۳۴). برخی مکان‌ها در قرآن نام‌برده شده‌اند (الأحقاف ۴۶:۲۱، الحِجر ۱۵:۸۰، الجودی ۱۱:۴۴، مدین)؛ اما تاریخ‌گذاری بیرونی و نامطمئن است (گزارش)، نه قرآنی.</p><p style='margin:9px 0 0'><b>۵) چرا امروز عذابِ نشانه‌ای نداریم؟</b> قرآن خود پاسخ می‌دهد: «وما مَنَعَنا أن نُرسِلَ بالآیاتِ إلا أن کذّبَ بها الأوّلون» (۱۷:۵۹) — نشانه‌هایِ عذابِ درخواستی از امتِ آخر <b>بازداشته</b> شد، چون الگویِ پیشین «نشانه ← انکار ← نابودی» بود. پس <b>شکلِ</b> نشانه دگرگون شد نه جوهرِ آن: <b>نشانهٔ ایستا</b> (کتاب) + <b>داوریِ به‌تعویق‌افتاده</b> (حساب در قیامت، نه نابودیِ فوری) — «وما نرسل بالآیات إلا تخویفاً». و <b>سنتِ خدا دگرگون نمی‌شود</b> («فلن تجد لسنة الله تبدیلا»، ۳۵:۴۳)؛ تنها شیوهٔ آن دیگر است. پس آری، ما هنوز نشانه داریم — به شکلِ کتاب و مهلت — نه عذابِ ناگهانیِ گذشتگان.</p><p style='margin:9px 0 0'><b>۶) تحدّی — نشانهٔ ایستا.</b> اتهامِ «او ساخته» (افتراه، ۱۰:۳۸، ۱۱:۱۳) و «خود گفته» (تقوّله، ۵۲:۳۳) با یک پاسخ روبه‌روست: پس همانندش را بیاورید — در چهار مقیاس: کلِّ قرآن حتی انس و جن با هم (۱۷:۸۸)، ده سوره (۱۱:۱۳)، یک سوره (۲:۲۳، ۱۰:۳۸)، و صرفاً سخنی همانند (۵۲:۳۴). یگانه پیش‌بینیِ ابطال‌پذیرِ ایستا: «فإن لم تفعلوا ولن تفعلوا» (۲:۲۴). و از همین <b>عجزِ</b> مخالفان («لا یأتون بمثله») متکلمان واژهٔ «اعجاز/معجزه» را برساختند؛ واژه نیست، اما اندیشه از این آیات برآمده.</p><p style='margin:9px 0 0'><b>۷) گونهٔ ساختاری — بدلِ همانند.</b> در گونه‌شناسیِ مفاهیم (محور، میدان، افراز، نردبان، جفتِ منجمد)، «آیه↔سحر» شکلی دیگر است: <b>جفتِ بدلی/رقیب</b> — دو چیز که عمداً همانند و اشتباه‌شدنی‌اند (هر دو شگفت، هر دو «مبین») و کارِ مفهوم فراهم‌آوردنِ نشانگرهایِ پنهانِ تمییز است. معنا در معیارِ تشخیصِ اصل از بدل زندگی می‌کند. مفهومی واژه‌ای است، نه حرفی.</p><p style='margin:9px 0 0'><b>۸) امانتِ روش‌شناختی.</b> واقعیت‌هایِ واژگانی (نبودِ «معجزه»، شمارِ سحر، ۴۴/۵۹، سِحرٌ مُبین ۹ بار، جدولِ عناصر، مقیاس‌هایِ تحدّی) <b>سنجیده/متنی</b> است؛ خوانشِ «سحر همچون بدلِ نشانه» <b>استنباط</b> است؛ بسته‌بندیِ کلامیِ «معجزه» و پیوندِ رویدادها با مکان و تاریخِ معیّن <b>گزارشِ بیرونی</b> و ادعانشده است. اطمینان: ~۹۹٪ برای واژگان، ~۸۰٪ برای خوانشِ ساختاری.</p></div>''', unsafe_allow_html=True)

# ── Arabic abstract ──
C.section("الملخّص الكامل — Arabic abstract")
st.markdown('''<div dir="rtl" id="ss-ar" style="font-family:Amiri,'Scheherazade New',Tahoma,serif;font-size:15.5px;line-height:2.05;color:#10243A;text-align:right;background:#F6F9FC;border-right:5px solid #4E6E92;border-radius:11px;padding:16px 22px"><p style='margin:9px 0 0'><b>١) المسألة والألفاظ.</b> السؤال الشائع عن «معجزة القرآن» مبنيٌّ على لفظٍ <b>لا يرد في القرآن قطّ</b>: «معجزة/معجزات» صفر مرّة، وجذر «عجز» إنّما يعني الإعجازَ عن الإدراك والإفلات (مُعجِزين ٩ مرّات). وألفاظ القرآن للآية المصدِّقة: <b>آية</b> (٣٨٢)، <b>بيّنة/مبين</b> (٥٢٣)، <b>برهان</b> (٨). فـ«المعجزة» صناعةٌ كلاميّة متأخّرة — صحيحةٌ لكن غير قرآنيّة. فالثنائيّ القرآنيّ الحقّ ليس «معجزة–سحر» بل <b>الآية ↔ السحر</b>.</p><p style='margin:9px 0 0'><b>٢) السحر في القرآن.</b> ورد جذر «سحر» ٦٣ مرّة (نحو ٦٠ بمعنى السحر)، و٣٤ منها متجمّعةٌ في مواجهة موسى وفرعون (السور ٧، ١٠، ٢٠، ٢٦). والمقيس: السحر قبل كلّ شيء <b>ما يقوله المكذِّبون</b> — ٤٤ من ٥٩ آيةً فيها فعل «قال»؛ وسمٌ يُلقى على الآية لا وصفٌ محايد. وصيغة <b>«سِحرٌ مُبين»</b> (٩ مرّات) تُرمى على موسى (١٠:٧٦، ٢٧:١٣) وعيسى (٥:١١٠، ٦١:٦) ومحمّد (٤٦:٧، ٣٧:١٥) سواءً — مرآةُ «بيّنة» المقابِلة. والتهمة النظيرة «مسحور» تستهدف شخص النبيّ (١٧:٤٧، ٢٥:٨، ١٧:١٠١).</p><p style='margin:9px 0 0'><b>٣) التمييز بين الآية والسحر — لا بالبهرَج بل بالخصائص.</b> <b>المصدر:</b> السحر تعليمُ الشياطين وكفر (٢:١٠٢) ← الآية بإذن الله، «وما كان لرسولٍ أن يأتيَ بآيةٍ إلا بإذن الله» (١٣:٣٨). <b>الحقيقة:</b> السحر تخييل، «يُخيَّلُ إليه … أنّها تسعى» (٢٠:٦٦) ← الآية حقّ، «فوقع الحقّ وبطل ما كانوا يعملون» (٧:١١٨). <b>محلّ الأثر:</b> السحر على الأعين، «سحروا أعين الناس» (٧:١١٦) ← الآية على الخلق (العصا، البحر، الأرض). <b>هل يُتعلَّم/يُحاكى؟</b> السحر يُتعلَّم (٢:١٠٢) ← الآية لا تُحاكى، «فأتوا بسورةٍ من مثله» (٢:٢٣). <b>المآل:</b> السحر يُبطَل، «لا يفلح الساحر» (٢٠:٦٩) ← الآية تغلب وتلقف الباطل (٧:١١٧). <b>الحكم:</b> السحر كفرٌ يضرّ ولا ينفع (٢:١٠٢) ← الآية هدًى ورحمة (٢٧:٧٧) وتخويف (١٧:٥٩). <b>شهادة الخبراء</b> — أقطعُها: سحرةُ فرعون خرّوا سُجّدًا لمّا رأوا آية موسى، «فأُلقي السحرة ساجدين» (٢٦:٤٦، ٧:١٢٠، ٢٠:٧٠). فالخبرةُ بالمزيَّف تصدّق الأصل.</p><p style='margin:9px 0 0'><b>٤) صور الآية وجنودُ الخالق.</b> ليست الآية صورةً واحدة: (أ) <b>آيةٌ مصدِّقة/آيةُ قدرة</b> لتصديق النبيّ — تسعُ آيات موسى (١٧:١٠١)، وناقةُ صالح «آية» (٧:٧٣)، وبردُ النار على إبراهيم (٢١:٦٩)، وخلقُ عيسى الطيرَ وإحياؤه الموتى (٣:٤٩)، وسليمانُ: تسخيرُ الريح (٣٤:١٢)، ومنطقُ الطير (٢٧:١٦)، وإحضارُ عرش بلقيس «قبل أن يرتدَّ إليك طرفُك» (٢٧:٤٠). (ب) <b>آيةُ القدرة والبعث</b> — أصحابُ الكهف المسمّون «من آياتنا» (١٨:٩)، وإماتةُ الرجل مئةَ عامٍ ثمّ بعثُه (٢:٢٥٩)، وطيرُ إبراهيم (٢:٢٦٠). (ج) <b>الآية القائمة</b> (الكتاب). (د) — عند التكذيب — <b>آيةُ عذابٍ أو حماية</b>؛ وفي هذا كلّه <b>الخلقُ كلُّه — عنصرًا وحيًّا — أداةٌ لله</b>، «ولله جنودُ السماوات والأرض» (٤٨:٤، ٧٤:٣١): الماء (نوح وفرعون)، الريح (عاد، ٦٩:٦)، الصيحة/الصاعقة (ثمود، ١١:٦٧)، الأرض (قارون، ٢٨:٨١)، الحجارة (لوط، ١١:٨٢)، وطيرُ الأبابيل دفاعًا عن الحرم (الفيل، ١٠٥:٣). التوقيعُ المشترك: مفاجئٌ («لا يشعرون»، ١٦:٤٥)، شاملٌ، ومؤقَّت («لكلّ أمّةٍ أجل»، ٧:٣٤). وبعضُ المواضع مُسمّاةٌ في القرآن (الأحقاف ٤٦:٢١، الحِجر ١٥:٨٠، الجوديّ ١١:٤٤، مدين)؛ أمّا التأريخُ فخارجيٌّ غيرُ مؤكَّد (تقرير) لا قرآنيّ.</p><p style='margin:9px 0 0'><b>٥) لماذا لا عذابَ آيةٍ اليوم؟</b> القرآن يجيب: «وما مَنَعَنا أن نُرسِلَ بالآياتِ إلا أن كذّبَ بها الأوّلون» (١٧:٥٩) — حُبِست آياتُ العذاب المطلوبة عن الأمّة الأخيرة، لأنّ السنّة الماضية: آية ← تكذيب ← إهلاك. فتبدّلت <b>صورةُ</b> الآية لا جوهرُها: <b>الآية القائمة</b> (الكتاب) مع <b>تأجيل الحساب</b> (الجزاء يوم القيامة لا استئصالٌ فوريّ) — «وما نرسل بالآيات إلا تخويفًا». و<b>سنّةُ الله لا تتبدّل</b> («فلن تجد لسنّة الله تبديلًا»، ٣٥:٤٣)؛ إنّما اختلف نمطُها. فنعم، ما زالت لنا الآية — كتابًا وأجلًا — لا عذابًا مفاجئًا كالأوّلين.</p><p style='margin:9px 0 0'><b>٦) التحدّي — الآية القائمة.</b> تهمةُ «افتراه» (١٠:٣٨، ١١:١٣) و«تقوّله» (٥٢:٣٣) تُقابَل بجواب واحد: فأتوا بمثله — في أربعة مقاديرَ: القرآنُ كلُّه ولو اجتمع الإنس والجنّ (١٧:٨٨)، عشرُ سور (١١:١٣)، سورةٌ واحدة (٢:٢٣، ١٠:٣٨)، بل حديثٌ مثلُه (٥٢:٣٤). وتنبّؤٌ قائمٌ قابلٌ للإبطال: «فإن لم تفعلوا ولن تفعلوا» (٢:٢٤). ومن هذا <b>العجزِ</b> عينِه («لا يأتون بمثله») اشتقّ المتكلّمون «الإعجاز/المعجزة»؛ اللفظ غائب، والفكرة مستمَدّةٌ من هذه الآيات.</p><p style='margin:9px 0 0'><b>٧) النوع البنيويّ — النظير المزيَّف.</b> في تصنيف المفاهيم (محور، حقل، قِسمة، سُلَّم، ثنائيّ جامد)، «الآية↔السحر» شكلٌ آخر: <b>ثنائيٌّ مزيَّف/مضادّ</b> — شيئان يُقصَد التباسُهما (كلاهما عجيب، كلاهما «مبين») وعملُ المفهوم تقديمُ علاماتِ التمييز الخفيّة. فالمعنى في معيار تمييز الأصل من المزيَّف. وهو مفهومٌ كلميّ لا حرفيّ.</p><p style='margin:9px 0 0'><b>٨) الأمانة العلميّة.</b> الحقائق اللفظيّة (غيابُ «معجزة»، عددُ السحر، ٤٤/٥٩، سِحرٌ مُبين ٩ مرّات، جدولُ العناصر، مقاديرُ التحدّي) <b>مقيسة/نصّيّة</b>؛ وقراءةُ «السحر نظيرٌ مزيَّف للآية» <b>استنباط</b>؛ وتغليفُ «المعجزة» الكلاميّ وربطُ الأحداث بمواقعَ وتواريخَ معيّنة <b>تقريرٌ خارجيّ</b> غيرُ مُدَّعًى. الثقة: ~٩٩٪ للألفاظ، ~٨٠٪ للقراءة البنيويّة.</p></div>''', unsafe_allow_html=True)
