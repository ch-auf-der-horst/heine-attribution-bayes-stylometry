"""E-3 Versmerkmale nach II.3a."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, json, glob, os, numpy as np, prep, sys
sys.path.insert(0, '../norm'); import angleichen as A
from calib import cdist, auc, rate, wilson
NUM = re.compile(r'^\s*([IVXLC]+|\d+)\s*\.?\s*$')
CAND = str(pfade.KANDIDAT)
def lines_of(text):
    L = [l.rstrip() for l in A.angleichen(text).split('\n') if not NUM.match(l)]
    out = []
    for i, l in enumerate(L):   # isolierte Einzelzeilen zwischen Leerzeilen = Überschriften
        prev = L[i-1].strip() if i else ''; nxt = L[i+1].strip() if i + 1 < len(L) else ''
        if l.strip() and not prev and not nxt: continue
        out.append(l)
    return out
def blocks(lines, size=548):
    B, cur, n = [], [], 0
    for l in lines:
        cur.append(l); n += len(l.split())
        if n >= size: B.append(cur); cur, n = [], 0
    return B
V = re.compile(r'[aeiouyäöü]+')
def syl(w): return max(1, len(V.findall(w.lower())))
NORM = [('ie', 'i'), ('ü', 'i'), ('y', 'i'), ('ö', 'e'), ('ä', 'e'), ('äu', 'ai'), ('eu', 'ai'), ('ei', 'ai'), ('ey', 'ai'), ('h', ''), ('b', 'p'), ('d', 't'), ('g', 'k'), ('ß', 's'), ('ss', 's')]
def rkey(w):
    w = re.sub(r"[^a-zäöüß]", '', w.lower())
    if not w: return None
    g = list(V.finditer(w))
    if not g: return None
    fem = len(g) >= 2 and re.search(r'(e|en|er|el|em|es|ern|eln)$', w)
    m = g[-2] if fem else g[-1]
    return w[m.start():]
def nkey(k):
    for a, b in NORM: k = k.replace(a, b)
    return re.sub(r'(.)\1', r'\1', k)
def feats(lines):
    vs = [l.strip() for l in lines if l.strip()]
    words = sum(len(l.split()) for l in vs)
    last = [re.sub(r"[^\wäöüß']", '', l.split()[-1]) for l in vs]
    fem = np.mean([bool(re.search(r'(e|en|er|el|em|es|ern|eln)$', w.lower())) and syl(w) >= 2 for w in last])
    keys = [rkey(w) for w in last]; pure = impure = 0
    for i, k in enumerate(keys):
        if not k: continue
        for j in range(i + 1, min(len(keys), i + 4)):
            if keys[j] and keys[j] == k: pure += 1; break
            if keys[j] and nkey(keys[j]) == nkey(k): impure += 1; break
    unrein = impure / max(1, pure + impure)
    elis = 100 * sum(l.count("'") for l in vs) / words
    enj = np.mean([not re.search(r'[.,;:!?—\-"\']$', l) for l in vs])
    sy = [sum(syl(w) for w in re.findall(r"[^\W\d_]+", l)) for l in vs]
    und = np.mean([l.split()[0].strip('"').lower() == 'und' for l in vs])
    st, cur = [], 0
    for l in lines:
        if l.strip(): cur += 1
        elif cur: st.append(cur); cur = 0
    if cur: st.append(cur)
    four = np.mean([s == 4 for s in st]) if st else 0
    return np.array([fem, unrein, elis, enj, np.mean(sy), np.std(sy), und, four])
NAMES = ['weibl. Kadenz', 'unreine Reime', 'Elisionen/100 W.', 'Vers ohne Satzzeichen', 'Silben/Vers', 'Streuung Silben', '"Und" am Versanfang', 'vierzeilige Strophen']

K = prep.ANG['korpus']
_feats_full=feats
KEEP=[0,1,4,5,6]
def stanzas(lines):
    st,cur=[],[]
    for l in lines+['']:
        if l.strip(): cur.append(l.strip())
        elif cur: st.append(cur); cur=[]
    return st
def ok(stz):
    if len(stz)!=4: return False
    sy=[sum(syl(w) for w in re.findall(r"[^\W\d_]+", l)) for l in stz]
    return all(5<=x<=9 for x in sy)
def sel(lines):
    out=[]
    for stz in stanzas(lines):
        if ok(stz): out+=stz+['']
    return out
cl=sel(lines_of(open(CAND,encoding='utf-8').read()))
NL=sum(1 for l in cl if l.strip())
def blk(lines):
    B,cur,n=[],[],0
    for l in lines:
        cur.append(l)
        if l.strip(): n+=1
        if n>=NL and not l.strip(): B.append(cur); cur,n=[],0
    return B
def F(b): return _feats_full(b)[KEEP]
def files(names): return [b for nm in names for b in blk(sel(lines_of(open(prep.kf('hist', nm), encoding='utf-8').read())))]
C={c: files(prep.CLASSES[c]) for c in ['B1','B2','C2','C3']}
a2=[(pid, sel(lines_of(t))) for pid,t in prep.a2_poems('hist')]
A2B,cur,ids,n=[],[],set(),0
for pid,L in a2:
    if not L: continue
    cur+=L; ids.add(pid); n+=sum(1 for l in L if l.strip())
    if n>=NL: A2B.append((ids,cur)); cur,ids,n=[],set(),0
poems=[(f'{s} {n_}', sel(lines_of(t))) for s,n_,t in prep.bdl_poems('hist') if s in prep.LIED]
def a1blocks(excl=set()):
    L=[]
    for pid,l in poems:
        if pid not in excl: L+=l
    return blk(L)
mapping=prep.a2_mapping()
train=[F(b) for b in a1blocks()]+[F(b) for _,b in A2B]+[F(b) for c in C for b in C[c]]
M=np.array(train); mu,sd=M.mean(0),M.std(0); sd[sd==0]=1
Z=lambda f:(f-mu)/sd
A1=np.array([Z(F(b)) for b in a1blocks()]); CZ={c:np.array([Z(F(b)) for b in C[c]]) for c in C if C[c]}
def s(x,ref,comp): return float(np.median(cdist(x,comp))-np.median(cdist(x,ref)))
pos2,pos3=[],[]
for ids,b in A2B:
    ref=np.array([Z(F(x)) for x in a1blocks({mapping.get(p,'') for p in ids}-{''})]); x=Z(F(b))
    if 'B1' in CZ: pos2.append(s(x,ref,CZ['B1']))
    pos3.append(s(x,ref,CZ['C2']))
def neg_closed(c):
    out=[]
    for i in range(len(CZ[c])):
        o=np.delete(CZ[c],[j for j in (i-1,i,i+1) if 0<=j<len(CZ[c])],0)
        if len(o): out.append(s(CZ[c][i],A1,o))
    return out
def summ(pos,neg):
    p,n=np.array(pos),np.array(neg); h,f=(p>0).sum(),(n>0).sum(); hl,_=wilson(h,len(p)); _,fh=wilson(f,len(n))
    return dict(auc=round(auc(p,n),3),treffer=f'{h}/{len(p)}',fehlalarm=f'{f}/{len(n)}',LR_nah=round(rate(h,len(p))/rate(f,len(n)),2),LR_nah_min95=round(hl/max(fh,1e-9),2))
HK=np.vstack([CZ[c] for c in ['B1','B2'] if c in CZ])
res={'Verse je Block':NL,'Blöcke':dict(A1=len(A1),A2=len(A2B),**{c:len(CZ[c]) for c in CZ}),
 'H1:H3 geschlossen Geibel':summ(pos3,neg_closed('C2')),'H1:H3 offen C3':summ(pos3,[s(x,A1,CZ['C2']) for x in CZ['C3']]),
 'H1:H3 offen Hektor':summ(pos3,[s(x,A1,CZ['C2']) for x in HK])}
if 'B1' in CZ and len(CZ['B1'])>=2: res['H1:H2 geschlossen']=summ(pos2,neg_closed('B1'))
xc=Z(F(cl)); res['Kandidat']=dict(s_H3=round(s(xc,A1,CZ['C2']),3), s_H2=round(s(xc,A1,HK),3))
stl=sel(lines_of(open(prep.kf('hist','Steinmann_Lieder'),encoding='utf-8').read()))
res['Steinmann']=dict(verse=sum(1 for l in stl if l.strip()), s_H3=round(s(Z(F(stl)),A1,CZ['C2']),3)) if stl else None
nm=['weibl. Kadenz','unreine Reime','Silben/Vers','Streuung','Und']
tab={'Kandidat':F(cl),'A1':np.mean([F(b) for b in a1blocks()],0),'A2':np.mean([F(b) for _,b in A2B],0),'Hektor':np.mean([F(b) for c in ['B1','B2'] for b in C[c]],0),'Geibel':np.mean([F(b) for b in C['C2']],0),'Müller/Wh':np.mean([F(b) for b in C['C3']],0)}
res['Merkmale']={k:dict(zip(nm,[round(float(x),3) for x in v])) for k,v in tab.items()}
sds={'A1':[F(b)[3] for b in a1blocks()],'A2':[F(b)[3] for _,b in A2B],'Hektor':[F(b)[3] for c in ['B1','B2'] for b in C[c]],'Geibel':[F(b)[3] for b in C['C2']],'Müller/Wh':[F(b)[3] for b in C['C3']]}
res['Streuung je Block']={k:dict(n=len(v),min=round(min(v),2),median=round(float(np.median(v)),2),anteil_kleiner_gleich_Kandidat=round(float(np.mean(np.array(v)<=F(cl)[3])),2)) for k,v in sds.items() if v}
json.dump(res,open('e7.json','w'),ensure_ascii=False,indent=1)
print(json.dumps(res,ensure_ascii=False,indent=1))
