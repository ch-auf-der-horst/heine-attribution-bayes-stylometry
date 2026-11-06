"""E-11 nach Protokoll II.3a (19.10.2026)."""
import pfade  # setzt Arbeitsverzeichnis und Pfade, s. pfade.py
import re, json, math, numpy as np, prep, calib, sys
sys.path.insert(0,'../norm'); import angleichen as A
from calib import cdist, auc, rate, wilson
T=str(pfade.E11 / 'texte') + '/'
AUT=['Mueller_WvK_1841','Scherr_1842','Storm_1843','ThMommsen_1843']
texts={a:open(T+a+'.txt',encoding='utf-8').read() for a in AUT}
CAND=str(pfade.KANDIDAT)
def sc(x,ref,comp): return float(np.median(cdist(x,comp))-np.median(cdist(x,ref)))
def evaluate(name,pos,imit,s_c):
    p=np.array(pos); allv=np.array([v for a in imit for v in imit[a]])
    kA,nA=int((p>=s_c).sum()),len(p); kN,nN=int((allv>=s_c).sum()),len(allv)
    lr=rate(kA,nA)/rate(kN,nN); a=auc(p,allv)
    return dict(Mass=name,Kandidat_s=round(s_c,3),AUC_A2_gg_Nachahmer=round(a,3),Tor=a>=0.75,
        A2_mind_so_nah=f'{kA}/{nA}',Nachahmer_mind_so_nah=f'{kN}/{nN}',Nachahmer_95=[round(x,2) for x in wilson(kN,nN)],
        Nachahmer_heine_nah_s_gt_0=f'{int((allv>0).sum())}/{nN}',
        je_Verfasser={a:f'{sum(v>=s_c for v in imit[a])}/{len(imit[a])} (s>0: {sum(v>0 for v in imit[a])})' for a in imit},
        LR=round(lr,2),log10LR=round(math.log10(lr),3))
res=[]
# 1+2: Delta Wörter / Zeichen-4-Gramme
mapping=prep.a2_mapping(); D=calib.build('ang',548)
cand=[(t,'K') for t in prep.toks(A.angleichen(open(CAND,encoding='utf-8').read()))]
for kind,nm in [('w','Delta Wörter (MFW150)'),('c','Zeichen-4-Gramme')]:
    Z,_=calib.featurize(D,kind); A1=np.array([Z(b) for b in D['A1L']]); C2=np.array([Z(b) for b in D['C2']])
    pos=[sc(Z(b),calib.a1_minus(D,Z,{mapping.get(p,'') for _,p in b}-{''},548),C2) for b in D['A2']]
    imit={a:[sc(Z(b),A1,C2) for b in prep.blocks([(w,a) for w in prep.toks(A.angleichen(texts[a]))],548)] for a in AUT}
    res.append(evaluate(nm,pos,imit,sc(Z(cand),A1,C2)))
# 3: Versmerkmale wie E-7
src=open('e7.py').read().split("HK=np.vstack")[0]
g={}; exec(src,g)
imit={a:[g['s'](g['Z'](g['F'](b)),g['A1'],g['CZ']['C2']) for b in g['blk'](g['sel'](g['lines_of'](texts[a])))] for a in AUT}
res.append(evaluate('Versmerkmale (E-7, gleiches Versmaß)',g['pos3'],imit,g['s'](g['Z'](g['F'](g['cl'])),g['A1'],g['CZ']['C2'])))
ok=[r['log10LR'] for r in res if r['Tor']]
w=max(-0.5,min(0.5,float(np.median(ok)))) if ok else 0.0
out=dict(Ergebnisse=res,Wertung_H1_H3=round(w,2),Massen_mit_Tor=len(ok))
json.dump(out,open('e11.json','w'),ensure_ascii=False,indent=1); print(json.dumps(out,ensure_ascii=False,indent=1))
