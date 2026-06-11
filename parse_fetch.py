import json, re, os, glob, sys
D=os.environ['D']
def extract_body(path):
    raw=open(path,encoding='utf-8',errors='replace').read()
    # two file shapes: plain text with header lines, OR a JSON array [{"type":"text","text":"..."}]
    s=raw.lstrip()
    if s.startswith('['):
        try:
            arr=json.loads(raw)
            txt=''.join(p.get('text','') for p in arr if isinstance(p,dict))
        except Exception:
            txt=raw
    else:
        txt=raw
    return txt
def parse(txt):
    # find first URL line to know edition+surah
    m=re.search(r'editions/([a-z]+-[a-z]+)/(\d+)\.json', txt)
    if not m: return None
    ed, sur = m.group(1), int(m.group(2))
    # find the JSON object starting at first '{'
    i=txt.find('{"chapter"')
    if i<0: i=txt.find('{\n    "chapter"')
    if i<0:
        i=txt.find('{')
    body=txt[i:]
    # try progressively
    try:
        d=json.loads(body)
    except Exception:
        # body may have trailing junk; find matching close by scanning
        depth=0; end=-1
        for k,ch in enumerate(body):
            if ch=='{':depth+=1
            elif ch=='}':
                depth-=1
                if depth==0: end=k+1;break
        if end>0:
            try: d=json.loads(body[:end])
            except Exception: return ('PARTIAL',ed,sur,None)
        else:
            return ('PARTIAL',ed,sur,None)
    ch=d.get('chapter')
    if not ch: return ('PARTIAL',ed,sur,None)
    return ('OK',ed,sur,ch)
files=glob.glob(os.path.join(D,'*.txt'))+glob.glob(os.path.join(D,'*.json'))
got={}
for f in files:
    txt=extract_body(f)
    r=parse(txt)
    if not r: continue
    status,ed,sur,ch=r
    key=(ed,sur)
    if status=='OK':
        got[key]=len(ch)
have_en=sorted(s for (e,s) in got if e=='eng-ummmuhammad')
have_fa=sorted(s for (e,s) in got if e=='fas-hussainansarian')
print('EN surahs have:',len(have_en),have_en)
print('FA surahs have:',len(have_fa),have_fa)
