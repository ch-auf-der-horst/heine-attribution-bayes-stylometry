"""E-11: OCR-Texte der Nachahmer bereinigen -> e11/texte/<Verfasser>.txt (keine inhaltliche Auswahl)."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, glob, os
S=str(pfade.ARBEIT)
# Historisches Aufbereitungsskript (nachträglich abgesichert, 6.11.2026). Es schreibt unkorrigierten OCR-Text nach
# e11/texte/ und würde die am Seitenbild korrigierten Texte überschreiben (s. textkorrektur_e11/). Bei der Nachrechnung
# wurde es nicht ausgeführt. Ein Neulauf ist nur bewusst möglich (E11PREP_NEU=1) und nur mit allen OCR-Eingaben.
if os.environ.get('E11PREP_NEU') != '1':
    raise SystemExit('Historisches Aufbereitungsskript, nicht für einen Neulauf; es würde e11/texte/ überschreiben. '
                     'Abbruch. Bewusster Neulauf nur mit E11PREP_NEU=1.')
_fehlt = [d for d in ('/e11/mu/*.ocr.txt', '/e11/sct/*.ocr.txt') if not glob.glob(S + d)]
_fehlt += [f for f in ('/lb/out/St.txt', '/lb/out/Th.txt') if not os.path.isfile(S + f)]
if _fehlt:
    raise SystemExit('Abbruch vor jedem Schreibzugriff, es fehlen OCR-Eingaben: ' + ', '.join(_fehlt))
O=S+'/e11/texte'; os.makedirs(O,exist_ok=True)
LET=re.compile(r'[A-Za-zÄÖÜäöüßſ]')
def fix(s):
    # feste Regeln für systematische Fraktur-OCR-Fehler (für alle Nachahmertexte gleich)
    s=s.replace('ſ','s')
    s=re.sub(r'\bI<','Ich',s); s=s.replace('c<','ch').replace('<h','ch').replace('<','ch')
    s=re.sub(r'(?<=[a-zäöü])>','ck',s)
    s=re.sub(r'^[^A-Za-zÄÖÜäöü„"»(]+','',s)          # Randschmutz am Zeilenanfang
    s=re.sub(r'\s+z\s*$',';',s); s=re.sub(r'(?<=\w) z;$',';',s)
    return s.strip()
def cleanpage(t, drop_head=True):
    lines=t.split('\n'); ne=[l for l in lines if l.strip()]
    if not ne: return ''
    if 'Digitized by' in t or 'Staatsbibliothek' in t: return ''
    if sum(bool(re.search(r'\d+\s*$',l)) for l in ne)/len(ne)>0.3: return ''
    out=[]
    for l in lines:
        s=fix(l.strip())
        if not s: out.append(''); continue
        if len(LET.findall(s))<3: continue
        out.append(s)
    return re.sub(r'\n{3,}','\n\n','\n'.join(out)).strip()
def write(name, files):
    txt='\n\n'.join(p for p in (cleanpage(open(f).read()) for f in files) if p)
    open(f'{O}/{name}.txt','w').write(txt); print(name, len(re.findall(r"[^\W\d_]+",txt)),'Wörter')
num=lambda f:int(re.findall(r'(\d+)',os.path.basename(f))[0])
mu=sorted(glob.glob(S+'/e11/mu/*.ocr.txt'),key=num); write('Mueller_WvK_1841',[f for f in mu if 15<=num(f)<=136])
sc=sorted(glob.glob(S+'/e11/sct/*.ocr.txt'),key=num); write('Scherr_1842',[f for f in sc if 9<=num(f)<=116])
# Liederbuch: Storm und Theodor Mommsen nach Inhaltsverzeichnis (lb/split.py), Seitenmarker entfernen, gleiche Regeln
for a,n in [('St','Storm_1843'),('Th','ThMommsen_1843')]:
    raw=open(S+f'/lb/out/{a}.txt').read()
    pages=[p for p in re.split(r'#### S\.\d+\n?',raw)]
    txt='\n\n'.join(c for c in (cleanpage(p) for p in pages) if c)
    open(f'{O}/{n}.txt','w').write(txt); print(n,len(re.findall(r"[^\W\d_]+",txt)),'Wörter')
