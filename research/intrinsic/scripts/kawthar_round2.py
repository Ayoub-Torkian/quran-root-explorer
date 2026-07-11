# -*- coding: utf-8 -*-
"""Round-2 internal evidence: naḥr as anti-hoarding; shāniʾ's argument = takāthur-logic; knowledge cycle; relations."""
import json
R="/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"
m=json.load(open(f"{R}/meaning.json",encoding='utf-8'))
def show(keys,label):
    print("\n==",label,"==")
    for k in keys: print(" ",k,"|",(m.get(k,{}).get('en','') or '')[:150])
# A) naḥr / sacrifice as GIVING-BACK, anti-hoarding (vs takāthur)
show(['22:36','22:37','6:162','108:2'],"naḥr anchors")
show(['9:34','9:35','3:180','92:5','92:6','92:7','92:8','100:8','104:2'],"HOARDING condemned / give vs withhold (anti-takāthur)")
show(['2:261','2:262','2:245','63:10'],"spending from the gift multiplied")
# B) the shāniʾ's argument = worth by wealth+children (the takāthur metric), refuted
show(['34:35','34:36','34:37','18:34','71:21','19:77','9:55','23:55','68:14'],"opponents argue superiority by amwāl+awlād (takāthur-logic)")
# C) knowledge/act -> increase cycle (internal, not the hadith)
show(['29:69','47:17','2:282','20:114','12:22'],"use/act on guidance -> increase (the cycle)")
# D) relations: the consolation cluster (Duhā 93, Sharḥ 94), takāthur twin (102)
show(['93:3','93:5','93:11','94:1','94:5','94:7','94:8'],"al-Duhā / al-Sharḥ — the consolation-and-giving cluster")
