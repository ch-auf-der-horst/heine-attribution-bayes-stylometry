import re,sys,glob,os,collections,unicodedata
B=os.environ.get('AA', 'AuthorshipAttribution')
R=B+'/Repositorium_Vorbereitung/Bayes_Arbeitsskripte'
K=B+'/corpus_diplomatisch'
F=[('Kandidat',K+'/Kandidat_Vagabund.txt'),
   ('Heine BdL 1827 (restituiert)',R+'/out/Heine_Buch_der_Lieder_1827_restituiert.txt'),
   ('Heine A2 (DHA I, Heine-Portal)',R+'/out/A2/Gedichte/*.txt')]
for n in ['Heine_Aurora','Heine_Biene','Heine_Almanach','Heine_Agrippina','Heine_Heimkehr','Heine_Kevlaar','Heine_DonnaClara','Heine_Ballade','Heine_Ratcliff',
          'Hektor_Vagabund','Hektor_Schilda','Steinmann_Lieder','Geibel_Lieder','Geibel_Junius','Geibel_Buecher','Mueller_1','Mueller_2','Wunderhorn_1806','Uhland_Lieder']:
    F.append((n,K+f'/{n}.txt'))
for n in ['Scherr_1842','Mueller_WvK_1841','Storm_1843','ThMommsen_1843']:
    F.append((n+' (E-11)',R+f'/e11/texte/{n}.txt'))
VERD={'fich','fie','ift','uud','nnd','iu','dcr','dic','dcs','uicht','nnr','fo','auf','tind','wic','fchon','bift','fpricht','ihu','uud','mid','nnb','unb','bcr','bie','ber','fey','feyn','fein'}
STARK={'fich','ift','uud','nnd','dcr','dic','dcs','uicht','nnr','tind','wic','fchon','bift','fpricht','ihu','nnb','unb','bcr'}
for name,pat in F:
    fs=sorted(glob.glob(pat))
    if not fs: print(name,'FEHLT',pat); continue
    t=unicodedata.normalize('NFC','\n'.join(open(f,encoding='utf-8').read() for f in fs))
    toks=re.findall(r"\S+",t)
    words=[re.sub(r"^[^\wäöüÄÖÜß]+|[^\wäöüÄÖÜß']+$","",x) for x in toks]; words=[w for w in words if w]
    lw=[w.lower() for w in words]
    a=sum(1 for w in words if re.search(r"[a-zäöüß][A-ZÄÖÜ]",w) and '-' not in w)
    b=sum(1 for w in words if re.search(r"[A-Za-zäöüß]\d|\d[A-Za-zäöüß]",w))
    c=sum(1 for w in lw if len(w)>=3 and re.fullmatch(r"[a-zß']+",w) and not re.search(r"[aeiouyäöü]",w))
    d=sum(1 for w in lw if w in STARK)
    e=collections.Counter(ch for ch in t if not re.match(r"[\w\s.,;:!?'\"„“”‚‘’»«›‹()\-—–]",ch))
    f=sum(1 for w in words if re.search(r"[^\wäöüÄÖÜß'\-]",w))
    tot=a+b+c+d+f
    print(f"{name:34s} Wörter {len(words):6d} | Großb.i.Wort {a:3d} Ziffer {b:3d} ohneVokal {c:3d} OCR-typisch {d:3d} Sonderz.i.Wort {f:3d} | auffällig/1000 {1000*tot/len(words):5.1f} | {dict(e.most_common(5))}")
