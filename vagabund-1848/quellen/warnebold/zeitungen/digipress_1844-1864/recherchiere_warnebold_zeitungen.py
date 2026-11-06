"""Reproduzierbare digiPress-Recherche zu Ernst Warnebold.
Eingabe: öffentliche digiPress-Suche und BSB-IIIF/OCR-API, keine lokalen Korpora.
Ausgabe: Suchlisten, Fundseiten (JPG/hOCR/TXT), Quellen-Hashes, Suchprotokoll.
Nur Python-Standardbibliothek; Namenssuche beweist weder Vollständigkeit noch Autorschaft.
"""
from pathlib import Path
import urllib.request, urllib.parse, re, html, json, hashlib, datetime, time
ROOT=Path(__file__).resolve().parent
records=[]; searches=[]
def fetch(url,name):
    target=ROOT/name; target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists(): data=target.read_bytes()
    else:
        for attempt in range(3):
            try:
                data=urllib.request.urlopen(url,timeout=45).read();break
            except Exception:
                if attempt==2:raise
                time.sleep(1)
        target.write_bytes(data)
    records.append(dict(url=url,file=name,sha256=hashlib.sha256(data).hexdigest(),retrieved=datetime.datetime.now(datetime.timezone.utc).isoformat()))
    return data
queries=['Warnebold','Warneboldt','Warnebo*','Warn?bold*','Warne*bold*','W?rn?bo*','Warn*b*','"Warne bold"','"W arnebold"','Warmbold','Warnbold','"Ernst W"']
for title,lo,hi in [('Magdeburgische Zeitung',1848,1864),('Weser-Zeitung',1844,1846)]:
    for i,q in enumerate(queries):
        params=dict(citationtitleid=title,content=q,fromYear=lo,untilYear=hi)
        u='https://digipress.digitale-sammlungen.de/search/extended?'+urllib.parse.urlencode(params)
        prefix=('Magdeburg' if lo==1848 else 'Weser')+f'_{i+1:02}'
        raw=fetch(u,'suchlisten/'+prefix+'_1.html').decode()
        m=re.search(r'digiPress: ([0-9.,]+) Treffer',raw);n=int(re.sub(r'[^0-9]','',m.group(1))) if m else None
        searches.append(dict(title=title,fromYear=lo,untilYear=hi,query=q,hits=n,url=u))
        if n is not None and n<=200:
            for page in range(1,(n+9)//10):fetch(u+'&start='+str(page),'suchlisten/'+prefix+f'_{page+1}.html')
        print(title,q,n,flush=True)
items=[('1858-10-20','bsb10487689',239,'bsb10487689_00231_u001',9,'Bericht ueber Warnebold; Korrespondenzzeichen a ungeloest'),('1859-01-10','bsb10487690',101,'bsb10487690_00101_u001',1,'Bericht ueber Warnebold; keine gesicherte Eigenprosa'),('1859-05-06','bsb10487691',472,'bsb10487691_00461_u001',12,'Anzeige C. Warnebold; nicht Ernst zugeordnet'),('1859-05-07','bsb10487691',486,'bsb10487691_00477_u001',10,'Wiederholte Anzeige C. Warnebold; nicht Ernst zugeordnet')]
finds=[]
for date,vol,page,issue,vpage,status in items:
    prefix='fundseiten/Magdeburg_'+date
    ocrurl=f'https://api.digitale-sammlungen.de/ocr/{vol}/{page}'
    raw=fetch(ocrurl,prefix+'.hocr.html').decode()
    text=html.unescape(re.sub('<[^>]+>',' ',raw));(ROOT/(prefix+'.txt')).write_text(re.sub(r'\s+',' ',text),encoding='utf-8')
    imageurl=f'https://api.digitale-sammlungen.de/iiif/image/v2/{vol}_{page:05}/full/full/0/default.jpg'
    fetch(imageurl,prefix+'.jpg')
    finds.append(dict(date=date,status=status,viewer=f'https://digipress.digitale-sammlungen.de/view/{issue}?page={vpage}',ocr=ocrurl,image=imageurl))
(ROOT/'SUCHPROTOKOLL.json').write_text(json.dumps(searches,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'FUNDSTELLEN.json').write_text(json.dumps(finds,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'QUELLEN.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
