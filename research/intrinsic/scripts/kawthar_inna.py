# -*- coding: utf-8 -*-
"""Why innā (We) not innī (I) in 108:1 — corpus evidence. Unicode-safe (run from file)."""
import json, re
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8'))
m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]')
def strip(s): return DIAC.sub('',s)

INNA  = 'إِنَّا'      # إِنَّا  inna+nā (We)
INNI  = 'إِنِّي'      # إِنِّي  inna+ī (I)
INNANI= 'إِنَّنِي'  # إِنَّنِي innanī (I)
NAHNU = 'نَحْنُ'      # نَحْنُ We
ANA   = 'أَنا'                  # أَنَا  I (pron)

cnt={'innā (We) إِنَّا':0,'innī (I) إِنِّي':0,'innanī (I) إِنَّنِي':0,'naḥnu (We) نَحْنُ':0,'anā (I) أَنَا':0}
inna_keys=[]; inni_keys=[]
for k,t in a.items():
    if INNA in t: cnt['innā (We) إِنَّا']+=t.count(INNA); inna_keys.append(k)
    if INNI in t: cnt['innī (I) إِنِّي']+=t.count(INNI); inni_keys.append(k)
    if INNANI in t: cnt['innanī (I) إِنَّنِي']+=t.count(INNANI)
    cnt['naḥnu (We) نَحْنُ']+=t.count(NAHNU)
    cnt['anā (I) أَنَا']+=t.count(ANA)
print("== FORM COUNTS (diacritized, whole Qurʾān) ==")
for f,c in cnt.items(): print(f"  {f:24s} {c}")

print("\n== 'innā + 1st-plural bestowal/act addressed to the Prophet' (parallels to 108:1) ==")
for k in ['108:1','48:1','15:87','94:1','94:5','94:6','108:2']:
    print(k, strip(a[k]))
    print('   EN:', m.get(k,{}).get('en','')[:110])

print("\n== 'innā + We sent down' (majesty register, common opening) ==")
for k in ['97:1','76:23','44:3','15:9','54:49','17:105','76:2','2:23']:
    if INNA in a[k]:
        print(k, strip(a[k])[:60], '| EN:', m.get(k,{}).get('en','')[:70])

print("\n== innī / innanī (singular): oneness, nearness, worship-of-Me ==")
for k in ['20:14','2:186','6:79','11:51','21:25','16:51','51:56']:
    print(k, strip(a[k])[:70])
    print('   EN:', m.get(k,{}).get('en','')[:110])

# does al-Kawthar say 'pray to US'? check 108:2 object of worship
print("\n== inside 108: who is worship directed to? ==")
print("108:2 contains 'rabbika' (your Lord, singular):", 'رَبِّكَ' in a['108:2'])
