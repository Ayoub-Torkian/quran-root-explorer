#!/usr/bin/env python3
import glob,json,numpy as np,collections
R=glob.glob('/sessions/*/mnt/Quran_Root_Explorer_Web_v1.2')[0]
DATA=R+'/research/two_books_genome/data/quran/quran_arabic_verses.tsv'; RBA=R+'/research/two_books_genome/roots_by_ayah.tsv'
NAMES=["Al-Fātiḥa","Al-Baqara","Āl ʿImrān","An-Nisāʾ","Al-Māʾida","Al-Anʿām","Al-Aʿrāf","Al-Anfāl","At-Tawba","Yūnus","Hūd","Yūsuf","Ar-Raʿd","Ibrāhīm","Al-Ḥijr","An-Naḥl","Al-Isrāʾ","Al-Kahf","Maryam","Ṭā Hā","Al-Anbiyāʾ","Al-Ḥajj","Al-Muʾminūn","An-Nūr","Al-Furqān","Ash-Shuʿarāʾ","An-Naml","Al-Qaṣaṣ","Al-ʿAnkabūt","Ar-Rūm","Luqmān","As-Sajda","Al-Aḥzāb","Sabaʾ","Fāṭir","Yā Sīn","Aṣ-Ṣāffāt","Ṣād","Az-Zumar","Ghāfir","Fuṣṣilat","Ash-Shūrā","Az-Zukhruf","Ad-Dukhān","Al-Jāthiya","Al-Aḥqāf","Muḥammad","Al-Fatḥ","Al-Ḥujurāt","Qāf","Adh-Dhāriyāt","Aṭ-Ṭūr","An-Najm","Al-Qamar","Ar-Raḥmān","Al-Wāqiʿa","Al-Ḥadīd","Al-Mujādila","Al-Ḥashr","Al-Mumtaḥana","Aṣ-Ṣaff","Al-Jumuʿa","Al-Munāfiqūn","At-Taghābun","Aṭ-Ṭalāq","At-Taḥrīm","Al-Mulk","Al-Qalam","Al-Ḥāqqa","Al-Maʿārij","Nūḥ","Al-Jinn","Al-Muzzammil","Al-Muddaththir","Al-Qiyāma","Al-Insān","Al-Mursalāt","An-Nabaʾ","An-Nāziʿāt","ʿAbasa","At-Takwīr","Al-Infiṭār","Al-Muṭaffifīn","Al-Inshiqāq","Al-Burūj","Aṭ-Ṭāriq","Al-Aʿlā","Al-Ghāshiya","Al-Fajr","Al-Balad","Ash-Shams","Al-Layl","Aḍ-Ḍuḥā","Ash-Sharḥ","At-Tīn","Al-ʿAlaq","Al-Qadr","Al-Bayyina","Az-Zalzala","Al-ʿĀdiyāt","Al-Qāriʿa","At-Takāthur","Al-ʿAṣr","Al-Humaza","Al-Fīl","Quraysh","Al-Māʿūn","Al-Kawthar","Al-Kāfirūn","An-Naṣr","Al-Masad","Al-Ikhlāṣ","Al-Falaq","An-Nās"]
roots={}
for ln in open(RBA,encoding='utf-8'):
    if '\t' in ln:k,r=ln.rstrip('\n').split('\t',1);roots[k]=[x for x in r.split() if x and x!='NA']
txt={};order=[]
for ln in open(DATA,encoding='utf-8'):
    if '\t' not in ln:continue
    sa,t=ln.split('\t',1);txt[sa.strip()]=t.strip();order.append(sa.strip())
bysura=collections.defaultdict(list)
for k in order:bysura[int(k.split(':')[0])].append(k)
def adjshare(ks):
    return np.mean([1 if set(roots.get(ks[i],[]))&set(roots.get(ks[i+1],[])) else 0 for i in range(len(ks)-1)]) if len(ks)>1 else 0.0
out={}
for s,ks in bysura.items():
    real=adjshare(ks); nv=len(ks)
    fl=np.mean([adjshare(list(np.random.default_rng(s*97+t).permutation(ks))) for t in range(120)]) if nv>2 else real
    lift=real-fl
    links=[]
    for i in range(len(ks)-1):
        sh=list(set(roots.get(ks[i],[]))&set(roots.get(ks[i+1],[])));links.append({'a':ks[i],'b':ks[i+1],'s':sh})
    out[s]={'n':int(s),'name':NAMES[s-1],'nv':nv,'score':round(float(real),3),'lift':round(float(lift),3),
            'links':links,'verses':[{'ref':k,'t':txt[k]} for k in ks]}
# ranks among nv>=10
rankable=[s for s in out if out[s]['nv']>=10]
for r,s in enumerate(sorted(rankable,key=lambda x:-out[x]['lift']),1):out[s]['rank']=r
NR=len(rankable)
def mode(o):
    if o['nv']<10:return 'too short — ring/anchor reading'
    if o['lift']>=0.08:return 'tightly woven (order-dependent)'
    if o['score']>=0.55 and o['lift']<0.03:return 'saturated cohesion (order-free)'
    if o['lift']>=0.03:return 'loosely woven'
    return 'stepwise / weak weave'
for s in out:out[s]['mode']=mode(out[s])
json.dump({'rankable':NR,'suras':out},open(R+'/research/intrinsic/sura_weave.json','w',encoding='utf-8'),ensure_ascii=False)
print('wrote sura_weave.json — %d sūras, %d rankable' % (len(out),NR))
top=sorted(rankable,key=lambda x:-out[x]['lift'])[:3];bot=sorted(rankable,key=lambda x:out[x]['lift'])[:3]
print('most woven:',[(out[s]['name'],out[s]['score'],out[s]['lift']) for s in top])
print('least:',[(out[s]['name'],out[s]['score'],out[s]['lift']) for s in bot])
print('Fātiḥa:',out[1]['score'],out[1]['mode'])
import os;print('size KB:',round(os.path.getsize(R+'/research/intrinsic/sura_weave.json')/1024))
