# -*- coding: utf-8 -*-
"""Surah al-Kawthar (108) internal study - al-Quran yufassiru ba'duhu ba'dan only.
Outputs research/intrinsic/scripts/kawthar_data.json for charts + paper."""
import json, csv, re, collections, statistics

ROOT = "/sessions/modest-relaxed-ritchie/mnt/Quran_Root_Explorer_Web_v1.2"

def fa(s):
    if s is None: return s
    return (s.replace('ك','ک').replace('ي','ی').replace('ى','ی')
             .replace('أ','ا').replace('إ','ا').replace('آ','ا').replace('ٱ','ا'))

# ---- load roots by ayah (Persian-normalized substrate) ----
roots_by_ayah = {}
with open(f"{ROOT}/research/two_books_genome/roots_by_ayah.tsv", encoding='utf-8') as f:
    for line in f:
        line=line.rstrip('\n')
        if not line or '\t' not in line: continue
        key, rs = line.split('\t',1)
        roots_by_ayah[key] = [fa(x) for x in rs.split()]

# ---- root dictionary (normalize root col to Persian) ----
rootdict = {}
with open(f"{ROOT}/exports/root_dictionary.csv", encoding='utf-8-sig') as f:
    for d in csv.DictReader(f):
        rootdict[fa(d['root'])] = d

arabic = json.load(open(f"{ROOT}/arabic.json", encoding='utf-8'))
meaning = json.load(open(f"{ROOT}/meaning.json", encoding='utf-8'))

DIAC = re.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭـ]')
def rasm(s):
    return fa(DIAC.sub('', s).replace('ـ',''))

# inverted index root -> list of ayah keys
root2ayat = collections.defaultdict(list)
for k, rs in roots_by_ayah.items():
    for r in set(rs):
        root2ayat[r].append(k)
def sortkey(k):
    s,a=k.split(':'); return (int(s),int(a))
for r in root2ayat: root2ayat[r].sort(key=sortkey)

out = {}
order = ['عطو','کثر','صلو','ربب','نحر','شنء','بتر']
# عطو کثر صلو ربب نحر شنء بتر

S108 = {f"108:{i}": roots_by_ayah.get(f"108:{i}",[]) for i in (1,2,3)}
out['s108_roots'] = S108
inv = []
for r in order:
    d = rootdict.get(r, {})
    inv.append({'root': r,'occ': int(d.get('total_occurrences',0) or 0),
        'n_ayahs': int(d.get('n_ayahs',0) or 0),'n_surahs': int(d.get('n_surahs',0) or 0),
        'hapax': (d.get('hapax','').strip().lower()=='yes'),
        'first': d.get('first_mushaf',''),'last': d.get('last_mushaf',''),
        'busiest': d.get('busiest_surah',''),
        'rate_per_1k_ayahs': float(d.get('rate_per_1k_ayahs',0) or 0)})
out['inventory'] = inv

allocc = sorted(int(d.get('total_occurrences',0) or 0) for d in rootdict.values())
out['corpus_root_stats'] = {'n_roots': len(allocc),'median_occ': statistics.median(allocc),
    'mean_occ': round(statistics.mean(allocc),1),
    'n_hapax': sum(1 for d in rootdict.values() if d.get('hapax','').strip().lower()=='yes')}

# ===== کثر abundance field — valence classification =====
KTHR='کثر'
kthr_ayat = root2ayat[KTHR]
neg_cue = re.compile(r'\b(most of (them|the people|mankind|men)|but most|yet most|do not know|do not believe|'
                     r'are ungrateful|ungrateful|ignorant|follow (but )?conjecture|turn away|wrongdoers|disbelieve|'
                     r'rivalry|vie|piling up|hoard|boast|abundance of|much wealth)\b', re.I)
val = {'most_negated':0,'rivalry_takathur':0,'other':0}
kthr_detail=[]
for k in kthr_ayat:
    g = meaning.get(k,{}).get('en','') or ''
    cat='other'
    if k.startswith('102:'): cat='rivalry_takathur'
    elif neg_cue.search(g): cat='most_negated'
    val[cat]+=1
    kthr_detail.append({'k':k,'cat':cat,'en':g[:160]})
out['kthr_field'] = {'total_ayahs':len(kthr_ayat),'valence':val}
out['kthr_detail'] = kthr_detail

# ===== severance field (interpreting بتر) =====
sever_roots = ['بتر','قطع','دبر','جذذ','صرم','بور','هلک']
out['severance_field'] = {r:{'occ':int(rootdict.get(r,{}).get('total_occurrences',0) or 0),
    'n_ayahs':int(rootdict.get(r,{}).get('n_ayahs',0) or 0),
    'hapax':rootdict.get(r,{}).get('hapax','').strip().lower()=='yes'} for r in sever_roots}

# ===== sacrifice / worship field (interpreting نحر) =====
sac_roots = ['نحر','نسک','ذبح','هدی','قرب','بدن','صلو']
out['sacrifice_field'] = {r:{'occ':int(rootdict.get(r,{}).get('total_occurrences',0) or 0),
    'n_ayahs':int(rootdict.get(r,{}).get('n_ayahs',0) or 0),
    'hapax':rootdict.get(r,{}).get('hapax','').strip().lower()=='yes'} for r in sac_roots}

# ===== صلو co-occurrence =====
SALA='صلو'
salat_ayat = set(root2ayat[SALA])
co = collections.Counter()
for k in salat_ayat:
    for r in set(roots_by_ayah.get(k,[])):
        if r!=SALA: co[r]+=1
out['salat_cooc_top'] = co.most_common(20)
out['salat_n_ayahs'] = len(salat_ayat)
out['salat_with'] = {r: co.get(r,0) for r in ['زکو','ربب','قوم','اتی','صبر','رکع','سجد','نسک','هدی']}

# ===== structure =====
def strip_basmala(t):
    toks = t.split()
    if toks and rasm(toks[0]).startswith('بسم'):
        toks = toks[4:]
    return ' '.join(toks).strip()
struct=[]
for i in (1,2,3):
    k=f"108:{i}"; t=arabic[k]
    if k=='108:1': t=strip_basmala(t)
    r=rasm(t)
    rwords=[w for w in r.split() if w.strip()]
    struct.append({'k':k,'display':t,'rasm':r,
        'n_words':len([w for w in t.split() if w.strip()]),
        'n_letters':len(r.replace(' ','')),
        'last_word_rasm':rwords[-1] if rwords else '',
        'starts_inna': r.startswith('انا') or r.startswith('ان'),
        'has_kaf_suffix': any(w.endswith('ک') and len(w)>1 for w in rwords),
        'roots':roots_by_ayah.get(k,[])})
out['structure']=struct
out['rhyme']=[s['last_word_rasm'] for s in struct]
out['rhyme_endings']=[s['last_word_rasm'][-2:] for s in struct]
out['inna_verses']=[s['k'] for s in struct if s['starts_inna']]
out['kaf_verses']=[s['k'] for s in struct if s['has_kaf_suffix']]

# hapax density
hapax_set=set(r for r,d in rootdict.items() if d.get('hapax','').strip().lower()=='yes')
dist=collections.Counter()
for k,rs in roots_by_ayah.items():
    h=sum(1 for x in set(rs) if x in hapax_set); dist[h]+=1
out['ayah_hapax_dist']=dict(sorted(dist.items()))
out['n_ayahs_2plus_hapax']=sum(v for h,v in dist.items() if h>=2)
out['s108_hapax_per_verse']={s['k']:[x for x in set(s['roots']) if x in hapax_set] for s in struct}
out['s108_total_hapax']=len(set(r for s in struct for r in s['roots'] if r in hapax_set))

# ===== surah length context =====
surah_letters=collections.Counter()
for k,t in arabic.items():
    s=int(k.split(':')[0]); tt=t
    if k.endswith(':1'): tt=strip_basmala(tt)
    surah_letters[s]+=len(rasm(tt).replace(' ',''))
lengths=sorted(((surah_letters[s],s) for s in surah_letters))
out['shortest_surahs']=[(s,l) for l,s in lengths[:6]]
out['s108_letters']=surah_letters[108]; out['s102_letters']=surah_letters[102]
out['s108_rank_by_length']=[s for l,s in lengths].index(108)+1
out['surah_lengths']={str(s):surah_letters[s] for s in surah_letters}
out['kthr_in_108']=(KTHR in roots_by_ayah.get('108:1',[]))
out['kthr_in_102']=any(KTHR in roots_by_ayah.get(f'102:{i}',[]) for i in range(1,9))

json.dump(out, open(f"{ROOT}/research/intrinsic/scripts/kawthar_data.json",'w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
print("WROTE kawthar_data.json")
print("inventory:")
for x in inv: print(' ', x['root'],'occ',x['occ'],'surahs',x['n_surahs'],'hapax',x['hapax'],'first',x['first'],'last',x['last'])
print("corpus stats:", out['corpus_root_stats'])
print("kthr valence:", out['kthr_field']['valence'], 'of', out['kthr_field']['total_ayahs'])
print("severance:", {k:v['occ'] for k,v in out['severance_field'].items()})
print("sacrifice:", {k:v['occ'] for k,v in out['sacrifice_field'].items()})
print("per-verse (k,words,letters,end,inna,kaf):", [(s['k'],s['n_words'],s['n_letters'],s['last_word_rasm'],s['starts_inna'],s['has_kaf_suffix']) for s in struct])
print("rhyme endings:", out['rhyme_endings'])
print("inna verses:", out['inna_verses'], "kaf verses:", out['kaf_verses'])
print("ayah hapax dist:", out['ayah_hapax_dist'], "#>=2:", out['n_ayahs_2plus_hapax'])
print("108 hapax/verse:", out['s108_hapax_per_verse'], "total:", out['s108_total_hapax'])
print("shortest:", out['shortest_surahs'], "| 108 rank", out['s108_rank_by_length'], "108L", out['s108_letters'], "102L", out['s102_letters'])
print("salat top:", out['salat_cooc_top'][:10])
print("salat_with:", out['salat_with'])
