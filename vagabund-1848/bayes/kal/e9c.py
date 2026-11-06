import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, json, numpy as np, prep, calib, sys
sys.path.insert(0,'../norm'); import angleichen as A
_orig=prep.toks
def hn(w):
    w=w.replace('ß','ss').replace("'",'').replace('’','')
    return re.sub(r'(?i)\bwol\b',lambda m:'Wohl' if m.group(0)[0]=='W' else 'wohl',w)
NORM=len(sys.argv)>1 and sys.argv[1]=='norm'
if NORM: prep.toks=lambda text:[hn(w) for w in _orig(text) if hn(w)]
src=open('e1.py').read().split('mapping = prep.a2_mapping(); out = []')[0]
exec(src)
mapping=prep.a2_mapping()
cand=prep.toks(A.angleichen(open(CAND,encoding='utf-8').read()))
D0=calib.build('ang',548)
res={}
# Zeichen-4-Gramme ohne Verzerrung
Z,_=calib.featurize(D0,'c'); A1=np.array([Z(b) for b in D0['A1L']]); B1=np.array([Z(b) for b in D0['B1']]); BH=np.vstack([B1,np.array([Z(b) for b in D0['B2']])])
xc=Z([(t,'K') for t in cand])
res['Zeichen-4 s_H2 (gg. Vagabund)']=round(score(xc,A1,B1),3); res['Zeichen-4 s_H2 (gg. Hektor gesamt)']=round(score(xc,A1,BH),3)
for k in [150,50,300]:
    keep=topk(D0,k); D=distort(D0,keep); Z,_=calib.featurize(D,'c')
    A1=np.array([Z(b) for b in D['A1L']]); B1=np.array([Z(b) for b in D['B1']])
    xc=Z([(dist_tok(t,keep),'K') for t in cand])
    res[f'E-1 k={k} s_H2']=round(score(xc,A1,B1),3)
print('normalisiert' if NORM else 'ohne Normalisierung', json.dumps(res,ensure_ascii=False))
keep=topk(D0,150); D=distort(D0,keep); Z,_=calib.featurize(D,'c')
A1=np.array([Z(b) for b in D['A1L']]); BH=np.array([Z(b) for b in D['B1']+D['B2']])
print('E-1 k=150 gg. Hektor gesamt', round(score(Z([(dist_tok(t,keep),'K') for t in cand]),A1,BH),3))
