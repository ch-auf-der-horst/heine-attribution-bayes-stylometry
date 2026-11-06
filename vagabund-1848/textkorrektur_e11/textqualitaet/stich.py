import re,glob,os,random,json,subprocess,sys
U='AuthorshipAttribution/'
src=open(U+'AuthorshipAttribution/Repositorium_Vorbereitung/Bayes_Arbeitsskripte/kal/e11prep.py').read()
src=src.split("def write(")[0].replace("import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py","").replace("S=str(pfade.ARBEIT)","S=''").replace("O=S+'/e11/texte'; os.makedirs(O,exist_ok=True)","")
ns={}; exec(src,ns); cleanpage=ns['cleanpage']
num=lambda f:int(re.findall(r'(\d+)\.(?:png|jpg)',os.path.basename(f))[0])
seiten={}
mu={num(f):f for f in glob.glob('ocr/e11/mu/*.ocr.txt')}
seiten['Mueller_WvK_1841']=[(n,cleanpage(open(mu[n]).read()),n) for n in sorted(mu) if 15<=n<=136]
sc={num(f):f for f in glob.glob('ocr/e11/sct/*.ocr.txt')}
seiten['Scherr_1842']=[(n,cleanpage(open(sc[n]).read()),n) for n in sorted(sc) if 9<=n<=116]
for a,n in [('St','Storm_1843'),('Th','ThMommsen_1843')]:
    raw=open(U+f'AuthorshipAttribution/Repositorium_Vorbereitung/Bayes_Arbeitsskripte/lb/out/{a}.txt').read()
    teile=re.split(r'#### S\.(\d+)\n?',raw)
    L=[]
    for i in range(1,len(teile),2):
        p=int(teile[i]); L.append((p,cleanpage(teile[i+1]),p+9+1))   # Bild i-(p+9) -> PDF-Seite p+10
    seiten[n]=L
# Kontrolle: Seiten zusammengesetzt == texte-Datei?
for n,L in seiten.items():
    t='\n\n'.join(c for _,c,_ in L if c)
    ref=open(U+f'AuthorshipAttribution/Repositorium_Vorbereitung/Bayes_Arbeitsskripte/e11/texte/{n}.txt').read()
    print(n,'identisch mit texte:',t.strip()==ref.strip(), len(re.findall(r"[^\W\d_]+",t)))
rng=random.Random(20261030)
PDF={'Mueller_WvK_1841':U+'Recherche_Heine_Nachahmungen_1830_1849/Beschaffung_Gedichtbaende/Mueller_Junge_Lieder_1841.pdf',
     'Scherr_1842':U+'Recherche_Heine_Nachahmungen_1830_1849/Beschaffung_Gedichtbaende/Scherr_Laute_und_leise_Lieder_1842.pdf',
     'Storm_1843':U+'A_Administration/Mommsen_Storm_Mommsen_Liederbuch_dreier_Freunde(1843).pdf',
     'ThMommsen_1843':U+'A_Administration/Mommsen_Storm_Mommsen_Liederbuch_dreier_Freunde(1843).pdf'}
auswahl={}
os.makedirs('bilder',exist_ok=True); os.makedirs('ocrseiten',exist_ok=True)
for n,L in seiten.items():
    kand=[x for x in L if len(re.findall(r"[^\W\d_]+",x[1]))>=60]
    s=rng.sample(kand,3); auswahl[n]=[(a,c) for a,_,c in s]
    for a,t,c in s:
        open(f'ocrseiten/{n}_{a}.txt','w').write(t)
json.dump({'seed':20261030,'auswahl':auswahl},open('auswahl.json','w'),indent=1)
print(json.dumps(auswahl))
