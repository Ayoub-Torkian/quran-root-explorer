import json,re,os,glob
D=os.environ['D']
def body(f):
    raw=open(f,encoding='utf-8',errors='replace').read()
    s=raw.lstrip()
    if s.startswith('['):
        try: arr=json.loads(raw); return ''.join(p.get('text','') for p in arr if isinstance(p,dict))
        except: return raw
    return raw
en={}
for f in glob.glob(os.path.join(D,'*.txt'))+glob.glob(os.path.join(D,'*.json')):
    t=body(f)
    if 'eng-ummmuhammad/' not in t: continue
    m=re.search(r'eng-ummmuhammad/(\d+)\.', t)
    if not m: continue
    i=t.find('{"chapter"')
    if i<0: i=t.find('{\n    "chapter"')
    if i<0: continue
    b=t[i:]
    try: d=json.loads(b)
    except:
        depth=0;end=-1
        for k,ch in enumerate(b):
            if ch=='{':depth+=1
            elif ch=='}':
                depth-=1
                if depth==0:end=k+1;break
        if end<0: continue
        try: d=json.loads(b[:end])
        except: continue
    for v in d['chapter']:
        en[(int(v['chapter']),int(v['verse']))]=v['text']
print('EN pairs collected:',len(en))
surs=sorted(set(s for s,a in en))
print('EN full-ish surahs:',surs)
json.dump({f"{s}:{a}":t for (s,a),t in en.items()}, open('.stage/en_collected.json','w'),ensure_ascii=False)
