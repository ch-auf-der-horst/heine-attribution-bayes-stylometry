import re,sys,glob,collections
LEX=set(l.split('\t')[0] for l in open('AuthorshipAttribution/Heine_Nachahmer_Gedichtbaende/Explorativ_E11_Gaudy_Beck/arbeit/lexikon.tsv'))
d=sys.argv[1]; out=[]
for f in sorted(glob.glob(f'{d}/*.txt'),key=lambda x:int(re.findall(r'(\d+)\.txt',x)[0])):
    p=re.findall(r'(\d+)\.txt',f)[0]
    t=open(f).read()
    for w in re.findall(r"[^\s]+",t):
        k=re.sub(r"^[„“\"'(]+|[,.;:!?“\"')—-]+$","",w)
        if re.search(r"[^A-Za-zÄÖÜäöüß'’-]",k) or (k and k.lower().strip("'") not in LEX and not re.fullmatch(r"[A-Za-zÄÖÜäöüß]+'?s?",k.lower()) ) : out.append((p,w))
        elif k and k.lower() not in LEX: out.append((p,k))
print(len(out)); print(' '.join(f'{p}:{w}' for p,w in out))
