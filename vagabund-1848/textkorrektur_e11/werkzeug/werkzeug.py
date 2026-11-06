"""Hilfen: alte OCR-Seite (bereinigt wie e11prep), neue Fraktur-OCR, Abweichungen markiert."""
import re,os,sys,difflib,glob
src=open('arbeit/korr/e11prep.py').read().split("def write(")[0]
src=src.replace("import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py","").replace("S=str(pfade.ARBEIT)","S=''").replace("O=S+'/e11/texte'; os.makedirs(O,exist_ok=True)","")
ns={}; exec(src,ns); cleanpage=ns['cleanpage']; fix=ns['fix']
K='arbeit/korr/'
def alt_seite(d,p):
    if d=='sc': f=K+f'alt/e11/sct/p-{p:03d}.png.ocr.txt'
    elif d=='mu': f=glob.glob(K+f'alt/e11/mu/p{p}-{p:03d}.png.ocr.txt')[0]
    else:
        import re as _r
        U='AuthorshipAttribution/Repositorium_Vorbereitung/Bayes_Arbeitsskripte/lb/out/'
        for a in ('St','Th'):
            raw=open(U+a+'.txt').read(); teile=_r.split(r'#### S\.(\d+)\n?',raw)
            if p==1 and a=='Th': return teile[0], cleanpage(teile[0])
            for i in range(1,len(teile),2):
                if int(teile[i])==p: return teile[i+1], cleanpage(teile[i+1])
        return None
    raw=open(f).read()
    return raw, cleanpage(raw)
def neu_seite(d,p):
    t=open(K+f'neu/{d}/{p}.txt').read().replace('ſ','s')
    t=re.sub(r'(?m)^\s*\d+\s*\*?\s*$','',t)   # Seitenzahlen/Bogensignaturen
    return '\n'.join(fix(l) for l in t.split('\n'))
def markiert(a,b):
    A=re.findall(r'\S+|\n',a); B=re.findall(r'\S+|\n',b)
    norm=lambda x:re.sub(r'[^\wäöüßÄÖÜ]','',x)
    sm=difflib.SequenceMatcher(None,[norm(x) for x in A],[norm(x) for x in B],autojunk=False)
    out=[]
    for op,a1,a2,b1,b2 in sm.get_opcodes():
        if op=='equal': out+=A[a1:a2]
        else:
            x=' '.join(t for t in A[a1:a2] if t!='\n'); y=' '.join(t for t in B[b1:b2] if t!='\n')
            out.append('{'+x+'|'+y+'}')
            if '\n' in A[a1:a2]: out.append('\n')
    return re.sub(r' ?\n ?','\n',' '.join(out))
if __name__=='__main__':
    d=sys.argv[1]
    for p in map(int,sys.argv[2:]):
        r=alt_seite(d,p)
        print(f'===== {d} {p} =====')
        print(markiert(r[1] if r else '', neu_seite(d,p)))
