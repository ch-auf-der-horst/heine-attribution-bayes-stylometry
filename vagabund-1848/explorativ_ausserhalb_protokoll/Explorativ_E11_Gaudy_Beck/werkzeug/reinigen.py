import re,sys,os,collections,json
LEX={}
for l in open('AuthorshipAttribution/Heine_Nachahmer_Gedichtbaende/Explorativ_E11_Gaudy_Beck/arbeit/lexikon.tsv'):
    w,n=l.rstrip('\n').split('\t'); LEX[w]=int(n)
def inlex(w): return w.lower() in LEX
FEST={'Ih':'Ich','ih':'ich','vaß':'daß','vem':'dem','ves':'des','vie':'die','ver':'der','vas':'das','fie':'sie','Fie':'Sie','ſie':'sie','iſt':'ist','Doh':'Doch','doh':'doch','no':'noch','au':'auch','dur':'durch','nict':'nicht','nit':'nicht','Lag':None,'noh':'noch','noH':'noch','Unv':'Und','unv':'und','vu':'du','E8':'Es','e8':'es'}
VERW=[('f','s'),('v','d'),('8','s'),('å','ä'),('ii','ü')]
def kandidaten(w):
    out=set()
    for a,b in VERW:
        i=w.find(a)
        while i>=0:
            out.add(w[:i]+b+w[i+len(a):]); i=w.find(a,i+1)
    return out
def reparatur(w):
    if w in FEST and FEST[w]: return FEST[w],'fest'
    if inlex(w) or len(w)<2: return w,None
    bes=None
    for k in kandidaten(w):
        if inlex(k):
            n=LEX[k.lower()]
            if not bes or n>bes[1]: bes=(k,n)
    if bes: return bes[0],'lex'
    return w,'unbekannt'
def zeile_ist_muell(l):
    s=l.strip()
    if not s: return False
    if re.search(r'Digitized|Google|BIBLIOTHE|MONACENS|Staatsbibl',s,re.I): return True
    b=len(re.findall(r'[A-Za-zÄÖÜäöüßſ]',s))
    if b<3: return True
    if b/len(s)<0.5 and len(s)<20: return True
    return False
def zeile(l,log,seite):
    l=l.replace('ſ','s').replace('ﬁ','fi')
    l=re.sub(r'c<','ch',l); l=re.sub(r'<<h|<h','ch',l); l=l.replace('<','ch')
    l=re.sub(r'c>','ck',l); l=re.sub(r'(?<=\w)>','ck',l)
    l=re.sub(r'[ ]*(=+-*|-{2,}|=)[ ]*',' — ',l)
    l=re.sub(r' +([,.;:!?])',r'\1',l)
    l=re.sub(r'([,.;:!?])(?:[ .,:;\-"“„\'*|/%]{1,})$',r'\1',l)
    l=re.sub(r'(?<=\w) z$',';',l)
    l=re.sub(r'[|"“\'*%]+\s*$','',l)
    l=re.sub(r'^[\-.,:;|\'"“ ]+(?=[A-ZÄÖÜa-zäöü])','',l)
    def f(m):
        w=m.group(0); n,a=reparatur(w)
        if a: log.append((seite,w,n,a))
        return n
    l=re.sub(r"[A-Za-zÄÖÜäöüßå8]+",f,l)
    l=re.sub(r'[ \t]+',' ',l).strip()
    return l
def seite(txt,log,p):
    zs=txt.split('\n'); out=[]
    for i,l in enumerate(zs):
        s=l.strip()
        if re.fullmatch(r'[-\d .,:]{1,6}',s): continue   # Seitenzahl
        if re.fullmatch(r'\d+\s*\*?|[IVXL]+\s*\*',s): continue
        if zeile_ist_muell(l): continue
        out.append(zeile(l,log,p))
    t='\n'.join(out)
    t=re.sub(r'([a-zäöüß])-\n+([a-zäöüß])',r'\1\2',t)
    t=re.sub(r'\n{3,}','\n\n',t)
    return t.strip()
if __name__=='__main__':
    d,von,bis,ziel=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
    os.makedirs(ziel,exist_ok=True); log=[]
    for p in range(von,bis+1):
        t=open(f'neu/{d}/{p}.txt').read()
        open(f'{ziel}/{p}.txt','w').write(seite(t,log,p)+'\n')
    json.dump(log,open(f'{ziel}/log.json','w'),ensure_ascii=False)
    c=collections.Counter(a for *_,a in log); print(c)
    unb=collections.Counter(w for s,w,n,a in log if a=='unbekannt'); print(len(unb)); print(unb.most_common(60))
