import re,sys,glob,json
LEX={}
for l in open('AuthorshipAttribution/Heine_Nachahmer_Gedichtbaende/Explorativ_E11_Gaudy_Beck/arbeit/lexikon.tsv'):
    w,n=l.rstrip('\n').split('\t'); LEX[w]=int(n)
REG=[('k','tz'),('g','tz'),('&','ck'),('c','ch'),('t','tz'),('ß','ss'),('ä','ü'),('h','ch'),('ß','tz'),('k','ck'),('E','ck'),('F','ck'),('8',''),('ü','ück'),('i','ic'),('z','tz'),('t','ckt'),('e','ec')]
def cand(w):
    s=set()
    for a,b in REG:
        for m in re.finditer(re.escape(a),w): s.add(w[:m.start()]+b+w[m.end():])
    s|={x.replace('ß','tz') for x in list(s)}
    s|={x.replace('h','ch') if 'ch' not in x else x for x in list(s)}
    return s
d=sys.argv[1]; log=[]
for f in glob.glob(f'{d}/*.txt'):
    p=int(re.findall(r'(\d+)\.txt',f)[0]); t=open(f).read()
    t=re.sub(r'(?m)^\s*[«»]?\s*[IVXLC1]{1,6}[.,]?\s*$','',t)
    t=re.sub(r'» ?','„',t); t=re.sub(r' ?«','“',t)
    t=re.sub(r'Sc(?=[a-zäöü])(?!h)','Sch',t); t=re.sub(r'(?<=[a-zäöü])sc(?=[a-zäöü])(?!h)','sch',t)
    t=re.sub(r'chh','ch',t); t=re.sub(r'(?<=[a-zäöü])hh','h',t); t=re.sub(r'kk','ck',t)
    t=re.sub(r"(?<=[a-zäöü])\*(?=[\s,.;:!?])","'",t)
    for a,b in {'Do':'Doch','Mid':'Mich','mic':'mich','nac':'nach','Bu':'Buch','iz':'ich','Dur':'Durch','ichh':'ich','jekt':'jetzt','Jekt':'Jetzt','Nutr':'Nur','Snell':'Schnell','dochh':'doch','dichh':'dich'}.items():
        t=re.sub(r'(?<![\wäöüß])'+a+r'(?![\wäöüß])',b,t)
    t=re.sub(r'(\w)\? (?=[a-zäöü])',r"\1' ",t)   # wagt? ich -> wagt' ich
    t=re.sub(r'(\w)" (?=[a-zäöü])',r"\1' ",t)
    def f2(m):
        w=m.group(0)
        if w.lower() in LEX or len(w)<3: return w
        b=None
        for c in cand(w):
            if c.lower() in LEX and (b is None or LEX[c.lower()]>LEX[b.lower()]): b=c
        if b: log.append((p,w,b)); return b
        return w
    t=re.sub(r"[A-Za-zÄÖÜäöüß8]+",f2,t)
    t=re.sub(r'\n{3,}','\n\n',t).strip()+'\n'
    open(f,'w').write(t)
json.dump(log,open(f'{d}/log2.json','w'),ensure_ascii=False)
print(len(log)); print(' | '.join(f'{p}:{a}>{b}' for p,a,b in sorted(log)))
