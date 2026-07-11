# -*- coding: utf-8 -*-
"""Why not the emphatic 'innā naḥnu + verb' (15:9) in 108:1? Unicode-safe."""
import json, re
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
DIAC=re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]'); strip=lambda s:DIAC.sub('',s)
NAHNU='نَحْنُ'

# all verses with the separate pronoun naḥnu
keys=[k for k,t in a.items() if NAHNU in t]
print("total verses with naḥnu (نحن):", len(keys))

# 'innā naḥnu' (doubled emphatic) specifically
dbl=[k for k in keys if 'إِنَّا نَحْنُ' in a[k] or 'إِنَّا لَنَحْنُ' in a[k]]
print("'innā naḥnu' / 'innā la-naḥnu' verses:", dbl)

# classify naḥnu contexts by contrast/exclusivity cues in the gloss
contrast=re.compile(r'\b(it is We|We who|We (alone|indeed)|We are the|than We|not you|are you the|did you|'
                    r'who creates|bring (it )?down|give life|cause.*die|inherit|guardian|sent (it )?down)\b',re.I)
vs_you=re.compile(r'\b(you|your)\b',re.I)
c=0; examples=[]
for k in keys:
    g=m.get(k,{}).get('en','')
    if contrast.search(g): c+=1
    if len(examples)<14: examples.append((k,g[:95]))
print(f"naḥnu verses whose gloss shows exclusivity/contrast cue: {c}/{len(keys)}")
print("\n== sample naḥnu contexts ==")
for k,g in examples: print(k,'|',g)
print("\n== the classic doubled cases ==")
for k in ['15:9','15:23','76:23','56:57','56:58','56:59','56:63','56:64','56:68','56:69','50:43','67:?']:
    if k in a: print(k, strip(a[k])[:60],'| EN:',m.get(k,{}).get('en','')[:80])
