# -*- coding: utf-8 -*-
"""Appendix A: cited verses, ONE line each, first <=30 words of the ayah, with surah no/name/ayah no. Not counted in word total."""
import json, re
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8'))
NAME={2:'al-Baqara',4:'al-Nisāʾ',5:'al-Māʾida',6:'al-Anʿām',7:'al-Aʿrāf',8:'al-Anfāl',9:'al-Tawba',11:'Hūd',
12:'Yūsuf',13:'al-Raʿd',14:'Ibrāhīm',15:'al-Ḥijr',16:'al-Naḥl',17:'al-Isrāʾ',20:'Ṭā Hā',21:'al-Anbiyāʾ',
22:'al-Ḥajj',23:'al-Muʾminūn',26:'al-Shuʿarāʾ',28:'al-Qaṣaṣ',34:'Sabaʾ',35:'Fāṭir',38:'Ṣād',39:'al-Zumar',
40:'Ghāfir',41:'Fuṣṣilat',42:'al-Shūrā',47:'Muḥammad',48:'al-Fatḥ',51:'al-Dhāriyāt',53:'al-Najm',54:'al-Qamar',
56:'al-Wāqiʿa',57:'al-Ḥadīd',64:'al-Taghābun',71:'Nūḥ',72:'al-Jinn',76:'al-Insān',89:'al-Fajr',93:'al-Ḍuḥā',
94:'al-Sharḥ',97:'al-Qadr',99:'al-Zalzala',102:'al-Takāthur',106:'Quraysh',108:'al-Kawthar',111:'al-Masad'}
BASMALA='بِسْمِ اللَّهِ الرَّحْمَنِ الرَّحِيمِ'

GROUPS=[
 ("The sūra itself", ["108:1","108:2","108:3"]),
 ("The two faces of k-th-r (abundance)", ["102:1","102:2","57:20","6:116","2:269","2:26"]),
 ("naḥr and the sacrifice field", ["6:162","22:37","22:36","5:27"]),
 ("abtar and the severance field", ["6:45","111:1","111:2"]),
 ("The divine 'We' / 'I' / 'naḥnu' (register)", ["48:1","15:87","94:1","76:23","15:9","56:59","20:14","2:186","51:56"]),
 ("The give / elect verb family", ["93:5","11:108","14:39","7:144","22:78"]),
 ("Given and earned; multiplied reward; the trade", ["2:286","53:39","6:160","2:261","4:40","9:111","35:29"]),
 ("The Lord who nurtures; collective abundance; gratitude-as-growth", ["26:18","7:96","72:16","14:7","34:13","8:53","35:2"]),
 ("The receiver decides; instrument-neutral gift", ["17:82","2:264","89:15","89:16"]),
 ("daʿwa, aḥsan, and 'repel with the better'", ["16:125","41:33","12:108","39:18","39:55","23:96","41:34","5:50"]),
 ("The hater (shāniʾ) and al-Māʾida's elaboration", ["5:2","5:8","5:3","5:6","5:55"]),
]
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]')
rasm=lambda x: DIAC.sub('',x).replace('ك','ک').replace('ي','ی')
def line(k):
    s,ay=k.split(':'); s=int(s); ay=int(ay)
    t=a.get(k,'').strip(); w=t.split()
    if ay==1 and s not in (1,9) and len(w)>4:  # drop the 4-word basmala on sūra-opening verses
        w=w[4:]
    short=' '.join(w[:30]) + (' …' if len(w)>30 else '')
    return f"- **Q {s}:{ay}** — Sūra {s} *{NAME.get(s,'?')}*, āyah {ay}: {short}"

out=["# Appendix A. Cited verses (first words)",
"",
"*Each verse cited as evidence is listed once, by sūra number, sūra name and āyah number, with the **first up to 30 words** of its Arabic (rasm). Full verses are in the standard text. This Arabic is **not counted** toward the word total.*",""]
n=0
for title,keys in GROUPS:
    out.append(f"**{title}**\n")
    for k in keys: out.append(line(k)); n+=1
    out.append("")
open(f"{R}/research/intrinsic/papers/kawthar_en_appendixA.md",'w',encoding='utf-8').write("\n".join(out))
print("wrote Appendix A:",n,"verses, one line each (<=30 words)")
print("\nsamples:")
for k in ['108:1','5:2','2:261']: print(line(k))
