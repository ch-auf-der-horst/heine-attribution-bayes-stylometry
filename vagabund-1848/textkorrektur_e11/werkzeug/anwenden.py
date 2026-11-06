"""Korrekturlisten (alt => neu je Seite) auf die bereinigte alte OCR anwenden; Protokoll schreiben."""
import sys,re,os,json
sys.path.insert(0,'arbeit/korr'); import werkzeug as w
def norm(t):
    t=t.replace('ſ','s')
    t=re.sub(r' +([,.;:!?])',r'\1',t)
    t=re.sub(r'„ +','„',t); t=re.sub(r' +“','“',t)
    t=re.sub(r' *(?:[=+]+-*|-+=+|-{2,}|=) *(?=[\s\w„“!?.,;:]|$)',' — ',t)
    t=re.sub(r'— *—',' — ',t)
    t=re.sub(r'(?m)(^|\s)[|)\]](?=\s|$)',r'\1',t)
    t=re.sub(r'([a-zäöüß])- *\n+ *([a-zäöüß])',r'\1\2',t)
    t=re.sub(r'[ \t]+',' ',t)
    return '\n'.join(l.strip() for l in t.split('\n'))
def lies(f):
    K={}; p=None
    for l in open(f).read().split('\n'):
        if l.startswith('@@ '):
            p=int(l.split()[1]); K.setdefault(p,{'ers':[],'voll':None,'notiz':[]})
            if 'VOLL' in l: K[p]['voll']=[]
        elif p is None or not l.strip(): 
            if p is not None and K[p]['voll'] is not None: K[p]['voll'].append('')
            continue
        elif l.startswith('#'): K[p]['notiz'].append(l[1:].strip())
        elif K[p]['voll'] is not None: K[p]['voll'].append(l)
        else:
            a,b=l.split(' => '); K[p]['ers'].append((a,b))
    return K
def bauen(d,seiten,kfile,outdir):
    K=lies(kfile); prot=[]
    os.makedirs(outdir,exist_ok=True)
    for p in seiten:
        k=K.get(p,{'ers':[],'voll':None,'notiz':[]})
        if k['voll'] is not None:
            t='\n'.join(k['voll']).strip(); prot.append((p,'Seite neu am Bild abgeschrieben','',''))
        else:
            t=w.alt_seite(d,p)[1]
            for a,b in k['ers']:
                assert a in t, (d,p,a)
                t=t.replace(a,b,1); prot.append((p,'Korrektur',a,b))
        for n in k['notiz']: prot.append((p,'Hinweis',n,''))
        open(f'{outdir}/{p}.txt','w').write(norm(t)+'\n')
    return prot
