# -*- coding: utf-8 -*-
"""Same gift, opposite effect by the receiver — abundance as a valence-neutral instrument. Unicode-safe."""
import json
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
a=json.load(open(f"{R}/arabic.json",encoding='utf-8')); m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
def show(keys,label):
    print(f"\n== {label} ==")
    for k in keys: print(' ',k,'|',(m.get(k,{}).get('en','') or '')[:128])
show(['2:26'],"SAME parable: 'misguides MANY (kathīr) by it and guides MANY by it' — first occurrence of k-th-r (2:26)")
show(['17:82','41:44'],"SAME Qurʾān: mercy/healing to believers, only LOSS/ deafness to the deniers")
show(['2:264','2:265'],"RAIN parable: same downpour → barren rock vs garden yielding double (the soil decides)")
show(['14:24','14:26'],"good word = good tree (firm, fruitful) vs bad word = bad tree (uprooted)")
show(['3:178','9:55','23:55','23:56','68:44','7:182'],"abundance as SNARE (istidrāj): wealth/children given to the heedless is NOT good for them")
show(['89:15','89:16'],"both ease AND restriction are a TEST; the human misreads honor vs humiliation")
