"""Daten für Abb. 1 (zwei Maße, Bootstrap) und den Tippett-Plot (Repositorium).
Nachträglich, nicht im Protokoll; geht nicht in die Bilanz ein."""
import os, sys
# Importpfade und Ausgabeort vom Skriptordner aus (nachträglich ergänzt, 6.11.2026)
HIER = os.path.dirname(os.path.abspath(__file__))
KAL = os.path.normpath(os.path.join(HIER, '..', '..', 'bayes', 'kal'))
sys.path[:0] = [KAL, os.path.normpath(os.path.join(KAL, '..', 'norm'))]
import re, json, numpy as np, prep, calib
import angleichen as A
from calib import cdist
from sklearn.linear_model import LogisticRegression
import pfade; T=str(pfade.E11/'texte')+'/'
AUT=['Storm_1843','ThMommsen_1843','Mueller_WvK_1841','Scherr_1842']
texts={a:open(T+a+'.txt',encoding='utf-8').read() for a in AUT}
roh=open(str(pfade.KANDIDAT),encoding='utf-8').read()
teile=[p for p in re.split(r'(?m)^\s*[IVX]+\.\s*$', roh) if p.strip()]
assert len(teile)==10, len(teile)
gedichte=[[(t,'K') for t in prep.toks(A.angleichen(p))] for p in teile]
def sc(x,ref,comp): return float(np.median(cdist(x,comp))-np.median(cdist(x,ref)))
mapping=prep.a2_mapping(); D=calib.build('ang',548)
rng=np.random.default_rng(1848); B=2000
idx=[rng.integers(0,10,10) for _ in range(B)]
out={}
for kind,nm in [('w','Delta Wörter'),('c','Zeichen-4-Gramme')]:
    Z,_=calib.featurize(D,kind); A1=np.array([Z(b) for b in D['A1L']]); C2=np.array([Z(b) for b in D['C2']])
    pos=[sc(Z(b),calib.a1_minus(D,Z,{mapping.get(p,'') for _,p in b}-{''},548),C2) for b in D['A2']]
    imit={a:[sc(Z(b),A1,C2) for b in prep.blocks([(w,a) for w in prep.toks(A.angleichen(texts[a]))],548)] for a in AUT}
    cand=[x for g in gedichte for x in g]
    sk=sc(Z(cand),A1,C2)
    boot=[sc(Z([x for i in ii for x in gedichte[i]]),A1,C2) for ii in idx]
    # score-basierte LR (logistische Kalibrierung, leave-one-out), H1 = Heine A2, H3 = Nachahmer
    s_all=np.array(pos+[v for a in AUT for v in imit[a]]); y=np.array([1]*len(pos)+[0]*(len(s_all)-len(pos)))
    prior_logit=np.log(y.mean()/(1-y.mean()))
    llr=np.zeros(len(s_all))
    for i in range(len(s_all)):
        m=np.ones(len(s_all),bool); m[i]=False
        lr=LogisticRegression(C=1e6).fit(s_all[m].reshape(-1,1),y[m])
        lo=lr.decision_function(s_all[i:i+1].reshape(-1,1))[0]
        pl=np.log(y[m].mean()/(1-y[m].mean()))
        llr[i]=(lo-pl)/np.log(10)
    full=LogisticRegression(C=1e6).fit(s_all.reshape(-1,1),y)
    llr_k=(full.decision_function([[sk]])[0]-prior_logit)/np.log(10)
    LR=10**llr
    cllr=0.5*(np.mean(np.log2(1+1/LR[y==1]))+np.mean(np.log2(1+LR[y==0])))
    out[kind]=dict(name=nm,kandidat=sk,boot_q=[float(np.quantile(boot,q)) for q in (0.025,0.5,0.975)],
                   boot_anteil_pos=float(np.mean(np.array(boot)>0)),heine_A2=pos,**imit,
                   llr_h1=llr[y==1].tolist(),llr_h3=llr[y==0].tolist(),llr_kandidat=float(llr_k),cllr=float(cllr))
    print(nm,'s',round(sk,3),'Boot 95%',[round(x,3) for x in out[kind]['boot_q']],'Anteil>0',round(out[kind]['boot_anteil_pos'],2),
          'log10LR Kand',round(llr_k,2),'Cllr',round(cllr,3))
json.dump(out,open(os.path.join(HIER,'abb_daten2_korr.json'),'w'),indent=1)  # dort lesen es abb1_EN.py und tippett_EN.py
